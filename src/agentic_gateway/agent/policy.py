"""Agent policies: a scripted one for development, and a local LLM through an OpenAI-compatible
endpoint (LM Studio serves one at http://localhost:1234/v1).

The scripted policy follows the task exactly and is deterministic, which makes it the right
tool for building and testing the benchmark machinery. The paper's agent results must come
from :class:`LLMPolicy`; numbers from the scripted policy measure the gate, not an agent.
"""

from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .tools import TOOL_SCHEMAS

ToolCall = tuple[str, dict[str, Any]]

# Fields of LM Studio's model description worth keeping in the run record.
SERVER_FIELDS = ("id", "publisher", "arch", "compatibility_type", "quantization",
                 "max_context_length", "loaded_context_length")


def require_local(base_url: str) -> None:
    """Credentialed data must not be sent to hosted APIs: only localhost is accepted."""
    host = base_url.split("//", 1)[-1].split("/", 1)[0].split(":")[0]
    if host not in ("localhost", "127.0.0.1"):
        raise ValueError("only a local LLM server is allowed; credentialed data must not be "
                         "sent to hosted APIs")


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            digest.update(block)
    return digest.hexdigest()


class Policy(Protocol):
    name: str

    def start(self, case_id: str, task: str, seed: int) -> None: ...

    def next(self, last_output: Any) -> ToolCall | None: ...

    def describe(self) -> dict[str, Any]: ...


def tokens_of(policy: Policy) -> int | None:
    """Tokens the policy's last decision consumed, if it reports them (an LLM does; the
    scripted policy does not)."""
    return getattr(policy, "last_tokens", None)


@dataclass
class ScriptedPolicy:
    """fetch_record -> risk_score -> prior_alerts -> draft_alert (tier >= alert_tier) or close.
    If the alert is withheld, it closes the case for clinician review, as the LLM prompts say."""

    cited: tuple[str, ...]
    alert_tier: int = 2
    name: str = "scripted"
    _state: dict[str, Any] = field(default_factory=dict)

    def start(self, case_id: str, task: str, seed: int) -> None:
        self._state = {"case_id": case_id, "stage": 0}

    def describe(self) -> dict[str, Any]:
        return {"policy": self.name, "cited": list(self.cited), "alert_tier": self.alert_tier}

    def next(self, last_output: Any) -> ToolCall | None:
        s = self._state
        stage = s["stage"]
        s["stage"] += 1
        if stage == 0:
            return "fetch_record", {"case_id": s["case_id"]}
        if stage == 1:
            s["record"] = last_output
            return "risk_score", {"case_id": s["case_id"]}
        if stage == 2:
            s["risk"] = last_output
            return "prior_alerts", {"patient_id": s["record"]["patient_id"]}
        if stage == 3:
            risk = s["risk"]
            if not isinstance(risk, dict) or "probability" not in risk:
                return "close_case", {"case_id": s["case_id"],
                                      "note": "risk withheld by gateway; for clinician review"}
            if risk["risk_tier"] >= self.alert_tier and not last_output:
                cited = {f: s["record"].get(f) for f in self.cited}
                return "draft_alert", {
                    "patient_id": s["record"]["patient_id"], "risk": risk["probability"],
                    "cited": cited,
                    "text": f"High risk ({risk['probability']:.2f}) at triage review."}
            return "close_case", {"case_id": s["case_id"], "note": "no alert needed"}
        if stage == 4 and isinstance(last_output, dict) and last_output.get("withheld"):
            return "close_case", {"case_id": s["case_id"],
                                  "note": "alert withheld by gateway; for clinician review"}
        return None


class LLMUnavailable(RuntimeError):
    pass


@dataclass
class LLMPolicy:
    """Chat-completions tool loop against a local server. Nothing leaves this machine."""

    model: str
    base_url: str = "http://localhost:1234/v1"
    temperature: float = 0.2
    max_steps: int = 10
    system_prompt: str = ""
    timeout_s: float = 300.0
    name: str = "llm"
    _messages: list[dict[str, Any]] = field(default_factory=list)
    _pending_id: str | None = None
    _seed: int = 0
    _steps: int = 0
    # Total tokens (prompt + completion) of the last chat call, from the server's ``usage``.
    # The prompt re-sends the whole conversation, so later steps cost more, as they do in use.
    last_tokens: int | None = None

    def __post_init__(self) -> None:
        require_local(self.base_url)

    @classmethod
    def from_prompt_file(cls, model: str, prompt: Path, **kw: Any) -> LLMPolicy:
        return cls(model=model, system_prompt=prompt.read_text(encoding="utf-8"), **kw)

    def describe(self, model_file: Path | None = None) -> dict[str, Any]:
        """What the paper must report about the agent. ``model_file`` is the GGUF the server
        loaded; its SHA-256 is the only reliable identity of the weights."""
        return {
            "policy": self.name,
            "model": self.model,
            "base_url": self.base_url,
            "temperature": self.temperature,
            "max_steps": self.max_steps,
            "system_prompt_sha256": hashlib.sha256(self.system_prompt.encode()).hexdigest(),
            "model_file": str(model_file) if model_file else None,
            "model_file_sha256": sha256_file(model_file) if model_file else None,
            "server_model": self.server_model(),
        }

    def server_model(self) -> dict[str, Any] | None:
        """Quantisation and architecture as LM Studio reports them (its REST API, ``/api/v0``).
        None if the server does not offer that endpoint."""
        root = self.base_url.rstrip("/").removesuffix("/v1")
        try:
            with urllib.request.urlopen(f"{root}/api/v0/models/{self.model}", timeout=5) as r:
                info = json.loads(r.read())
        except (urllib.error.URLError, OSError, ValueError):
            return None
        return {k: info.get(k) for k in SERVER_FIELDS if k in info} or None

    def available(self) -> bool:
        try:
            with urllib.request.urlopen(f"{self.base_url}/models", timeout=3) as r:
                return r.status == 200
        except (urllib.error.URLError, OSError):
            return False

    def start(self, case_id: str, task: str, seed: int) -> None:
        self._messages = [{"role": "system", "content": self.system_prompt},
                          {"role": "user", "content": task}]
        self._pending_id, self._seed, self._steps = None, seed, 0

    def _chat(self) -> dict[str, Any]:
        body = json.dumps({"model": self.model, "messages": self._messages,
                           "tools": TOOL_SCHEMAS, "temperature": self.temperature,
                           "seed": self._seed}).encode()
        req = urllib.request.Request(f"{self.base_url}/chat/completions", data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as r:
                reply = json.loads(r.read())
        except (urllib.error.URLError, OSError) as error:
            raise LLMUnavailable(str(error)) from error
        total = (reply.get("usage") or {}).get("total_tokens")
        self.last_tokens = int(total) if total is not None else None
        return reply["choices"][0]["message"]

    def next(self, last_output: Any) -> ToolCall | None:
        if self._pending_id is not None:
            self._messages.append({"role": "tool", "tool_call_id": self._pending_id,
                                   "content": json.dumps(last_output, default=str)})
        if self._steps >= self.max_steps:
            return None
        self._steps += 1
        self.last_tokens = None
        message = self._chat()
        calls = message.get("tool_calls") or []
        self._messages.append({k: v for k, v in message.items() if v is not None})
        if not calls:
            return None
        call = calls[0]  # one action per step; extra parallel calls are ignored and logged
        self._pending_id = call.get("id", f"call{self._steps}")
        try:
            args = json.loads(call["function"].get("arguments") or "{}")
        except json.JSONDecodeError:
            args = {"_unparseable": call["function"].get("arguments")}
        return call["function"]["name"], args
