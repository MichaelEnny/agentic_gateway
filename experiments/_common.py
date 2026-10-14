"""Shared command-line handling for the numbered experiment scripts."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agentic_gateway.data.access import NotAuthorisedError
from agentic_gateway.data.settings import SETTINGS, Setting
from agentic_gateway.workspace import Workspace, read_json

CONFIGS = Path(__file__).resolve().parent / "configs"
PROMPTS = Path(__file__).resolve().parent / "prompts"
PRIMARY_MODEL = "random_forest"
COVERAGE_GRID = (0.80, 0.85, 0.90, 0.95)  # conformal coverage levels tuned in step 5


@dataclass(frozen=True)
class Params:
    """Sizes and minimums. Smoke values only make the pipeline run on the tiny demos."""

    min_neighbors: int
    scdi_min_size: int
    group_cols: tuple[str, ...] | None  # None = setting default
    drift_boot: int
    drift_min_group: int
    analysis_boot: int
    bench_cases: int
    bench_min_per_group: int
    seeds: tuple[int, ...]
    icu_min_events: int
    m1_reference_cap: int
    null_permutations: int


FULL = Params(min_neighbors=30, scdi_min_size=50, group_cols=None, drift_boot=500,
              drift_min_group=50, analysis_boot=2000, bench_cases=400, bench_min_per_group=30,
              seeds=(0, 1, 2, 3, 4), icu_min_events=100, m1_reference_cap=20000,
              null_permutations=200)
SMOKE = Params(min_neighbors=5, scdi_min_size=5, group_cols=("gender",), drift_boot=100,
               drift_min_group=5, analysis_boot=300, bench_cases=60, bench_min_per_group=10,
               seeds=(0,), icu_min_events=1, m1_reference_cap=20000, null_permutations=50)


def parser(description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--setting", choices=sorted(SETTINGS), required=True)
    p.add_argument("--source", choices=("demo", "full"), default="demo")
    p.add_argument("--smoke", action="store_true",
                   help="lower every minimum so the demos run; numbers mean nothing")
    p.add_argument("--seed", type=int, default=42)
    return p


def setup(args: argparse.Namespace) -> tuple[Workspace, Setting, Params]:
    ws = Workspace(args.setting, args.source, args.smoke)
    return ws, SETTINGS[args.setting], (SMOKE if args.smoke else FULL)


def base_config(params: Params, setting: Setting) -> dict:
    """Starting values; risk tiers are per setting (ICU mortality is far rarer than ED
    admission, so the same cuts would almost never raise an ICU alert)."""
    values = read_json(CONFIGS / "gateway_base.json")
    values.pop("_comment", None)
    values["local_min_neighbors"] = params.min_neighbors
    values["risk_tier_cuts"] = values["risk_tier_cuts"][setting.name]
    return values


def add_policy_args(p: argparse.ArgumentParser) -> None:
    """Agent options shared by the steps that run the agent (4 and 9)."""
    p.add_argument("--policy", choices=("scripted", "llm"), default="scripted")
    p.add_argument("--llm-model", default="")
    p.add_argument("--llm-url", default="http://localhost:1234/v1")
    p.add_argument("--llm-model-file", type=Path, default=None,
                   help="the GGUF file the server loaded; its SHA-256 goes in the record")


def make_policy(args: argparse.Namespace, setting: Setting) -> tuple[Any, dict]:
    """The agent policy and its description for the record."""
    from agentic_gateway.agent import LLMPolicy, ScriptedPolicy

    if args.policy == "scripted":
        policy = ScriptedPolicy(cited=setting.cited)
        return policy, policy.describe()
    policy = LLMPolicy.from_prompt_file(args.llm_model, PROMPTS / f"system_{setting.name}.txt",
                                        base_url=args.llm_url)
    if not policy.available():
        raise SystemExit(f"no LLM server at {args.llm_url}; start LM Studio's server first")
    if args.llm_model_file is None:
        print("warning: --llm-model-file not given; the model's file hash will not be "
              "recorded, and a paper run needs it")
    elif not args.llm_model_file.is_file():
        raise SystemExit(f"--llm-model-file {args.llm_model_file} does not exist")
    return policy, policy.describe(args.llm_model_file)


def main_guard(fn) -> None:  # type: ignore[no-untyped-def]
    try:
        raise SystemExit(fn())
    except NotAuthorisedError as error:
        print(f"refused: {error}", file=sys.stderr)
        raise SystemExit(3) from error
    except FileNotFoundError as error:
        print(f"missing input: {error}", file=sys.stderr)
        raise SystemExit(2) from error
