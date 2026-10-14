"""LLM-as-judge baseline: a local model reviews each proposed action and allows or defers it.

The judge sees what the agent sees: the task, every earlier action with its result, and the
proposed action with the result it would pass on. It does not see the gateway's hidden data
(embedding, subgroup, reference cohort), which is the point of the comparison: can a general
model spot an unreliable step from the trace alone?

It plugs into :class:`~agentic_gateway.agent.gate.StepGate` as ``judge=``; the gate calls it
once per step and defers the step when it returns False.

* Deterministic as far as the server allows: temperature 0 and a fixed seed.
* Fail-closed: a reply that names neither "allow" nor "defer" counts as defer, and is counted.
* Cached on disk by a hash of everything sent, so replaying the same steps (shared prefixes of
  faulty and clean trajectories, reruns) costs one call each. The cache holds trace text and
  therefore credentialed data: keep it under ``runs/``.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from .policy import LLMUnavailable, require_local
from .types import Step

DECISIONS = ("allow", "defer")
THINK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
WORD = re.compile(r"\b(allow|defer)\b", re.IGNORECASE)


def _call_text(step: Step) -> str:
    return f"{step.tool}({json.dumps(step.args, sort_keys=True, default=str)})"


def _result_text(output: Any) -> str:
    return json.dumps(output, sort_keys=True, default=str)


def parse_verdict(content: str) -> tuple[str | None, str]:
    """(decision or None, reason). Reads a JSON object if there is one, else the first
    'allow' or 'defer' in the text. Reasoning blocks (<think>...</think>) are ignored."""
    text = THINK.sub("", content or "").strip()
    for match in re.finditer(r"\{.*?\}", text, re.DOTALL):
        try:
            obj = json.loads(match.group(0))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            decision = str(obj.get("decision", "")).strip().lower()
            if decision in DECISIONS:
                return decision, str(obj.get("reason", ""))
    word = WORD.search(text)
    if word:
        return word.group(1).lower(), text[:200]
    return None, text[:200]


@dataclass
class LLMJudge:
    model: str
    system_prompt: str
    task: str  # the agent's task template, with {case_id}
    base_url: str = "http://localhost:1234/v1"
    temperature: float = 0.0
    seed: int = 0
    max_tokens: int = 256
    timeout_s: float = 300.0
    cache_path: Path | None = None
    fail_closed: bool = True
    name: str = "llm_judge"
    stats: Counter[str] = field(default_factory=Counter)
    latencies_ns: list[int] = field(default_factory=list)  # uncached calls only
    _cache: dict[str, dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        require_local(self.base_url)
        if self.cache_path is not None and self.cache_path.exists():
            for line in self.cache_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    entry = json.loads(line)
                    self._cache[entry["key"]] = entry

    @classmethod
    def from_prompt_file(cls, model: str, prompt: Path, task: str, **kw: Any) -> LLMJudge:
        return cls(model=model, system_prompt=prompt.read_text(encoding="utf-8"), task=task,
                   **kw)

    def available(self) -> bool:
        try:
            with urllib.request.urlopen(f"{self.base_url}/models", timeout=3) as r:
                return r.status == 200
        except (urllib.error.URLError, OSError):
            return False

    # -- the StepGate interface --------------------------------------------------------------
    def __call__(self, step: Step, history: list[Step]) -> bool:
        verdict = self.review(step, history)
        return verdict["decision"] == "allow"

    def review(self, step: Step, history: list[Step]) -> dict[str, Any]:
        prompt = self.render(step, history)
        key = self._key(prompt)
        entry = self._cache.get(key)
        if entry is not None:
            self.stats["cached"] += 1
        else:
            t0 = time.perf_counter_ns()
            content = self._chat(prompt)
            latency = time.perf_counter_ns() - t0
            self.latencies_ns.append(latency)
            decision, reason = parse_verdict(content)
            entry = {"key": key, "decision": decision, "reason": reason, "raw": content,
                     "latency_ns": latency}
            self._cache[key] = entry
            if self.cache_path is not None:
                self.cache_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.cache_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry) + "\n")
        decision = entry["decision"]
        if decision is None:
            self.stats["unparseable"] += 1
            decision = "defer" if self.fail_closed else "allow"
        self.stats[decision] += 1
        return {"decision": decision, "reason": entry["reason"], "parsed":
                entry["decision"] is not None}

    # -- prompt --------------------------------------------------------------------------------
    def render(self, step: Step, history: list[Step]) -> str:
        first = history[0] if history else step
        case_id = first.args.get("case_id", step.args.get("case_id", "unknown"))
        lines = [f"Task given to the agent: {self.task.format(case_id=case_id)}", "",
                 "Actions so far:"]
        if not history:
            lines.append("(none)")
        for i, s in enumerate(history, 1):
            lines.append(f"{i}. {_call_text(s)} -> {_result_text(s.output)}")
        lines += ["", f"Proposed action: {_call_text(step)}",
                  f"Result it would pass on if allowed: {_result_text(step.output)}", "",
                  'Reply with JSON only: {"decision": "allow" or "defer", "reason": "<one sentence>"}']
        return "\n".join(lines)

    def _key(self, prompt: str) -> str:
        material = json.dumps([self.model, self.system_prompt, prompt, self.temperature,
                               self.seed, self.max_tokens])
        return hashlib.sha256(material.encode()).hexdigest()

    def _chat(self, prompt: str) -> str:
        body = json.dumps({"model": self.model, "temperature": self.temperature,
                           "seed": self.seed, "max_tokens": self.max_tokens,
                           "messages": [{"role": "system", "content": self.system_prompt},
                                        {"role": "user", "content": prompt}]}).encode()
        req = urllib.request.Request(f"{self.base_url}/chat/completions", data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as r:
                return json.loads(r.read())["choices"][0]["message"].get("content") or ""
        except (urllib.error.URLError, OSError) as error:
            raise LLMUnavailable(str(error)) from error

    def describe(self) -> dict[str, Any]:
        lat = np.array(self.latencies_ns, dtype=float) / 1e6
        return {
            "judge": self.name, "model": self.model, "base_url": self.base_url,
            "temperature": self.temperature, "seed": self.seed, "max_tokens": self.max_tokens,
            "fail_closed": self.fail_closed,
            "system_prompt_sha256": hashlib.sha256(self.system_prompt.encode()).hexdigest(),
            "stats": dict(self.stats),
            "uncached_calls": len(lat),
            "call_p50_ms": float(np.median(lat)) if lat.size else None,
            "call_p95_ms": float(np.percentile(lat, 95)) if lat.size else None,
        }
