"""One folder per (setting, source, mode) under ``runs/``, and the record each step leaves.

Steps 1 to 3 (cohort, models, gateway fits) do not depend on the agent and write to the base
folder, ``runs/<setting>_<source>[_smoke]/``. Steps 4 to 10 belong to one agent run and
write to ``agent_<run>/`` inside it, so a scripted run and an LLM run sit side by side instead
of overwriting each other. Reads look in the run folder first, then in the base folder.

Every step writes ``records/<step>.json`` with its arguments, versions, timing and outputs.
A number that has no record behind it does not go in the paper.
"""

from __future__ import annotations

import json
import platform
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Any

from .data.access import REPO_ROOT

PACKAGES = ("numpy", "pandas", "scipy", "scikit-learn", "joblib", "pyarrow")
RUN_NAME = re.compile(r"[A-Za-z0-9._-]{1,64}")


@dataclass(frozen=True)
class Workspace:
    setting: str
    source: str
    smoke: bool
    run: str | None = None  # agent run name: steps 4 to 10 live in agent_<run>/

    def __post_init__(self) -> None:
        if self.smoke and self.source == "full":
            raise ValueError("--smoke lowers minimums for the demos; never use it on full data")
        if self.run is not None and not RUN_NAME.fullmatch(self.run):
            raise ValueError(f"run name {self.run!r}: use letters, digits, '.', '_' or '-'")

    @property
    def base(self) -> Path:
        """Folder of the agent-independent steps 1 to 3."""
        name = f"{self.setting}_{self.source}" + ("_smoke" if self.smoke else "")
        path = REPO_ROOT / "runs" / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def root(self) -> Path:
        """Where this workspace writes: the agent run's folder, or the base without a run."""
        if self.run is None:
            return self.base
        path = self.base / f"agent_{self.run}"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def path(self, *parts: str) -> Path:
        p = self.root.joinpath(*parts)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def require(self, *parts: str) -> Path:
        """An input from an earlier step: this run's folder first, then the shared base."""
        for folder in dict.fromkeys((self.root, self.base)):
            p = folder.joinpath(*parts)
            if p.exists():
                return p
        raise FileNotFoundError(f"{self.root.joinpath(*parts)} not found; run the earlier "
                                "step first")

    def record(self, step: str, args: dict[str, Any], outputs: dict[str, Any],
               started: float) -> Path:
        payload = {
            "step": step,
            "setting": self.setting,
            "source": self.source,
            "smoke": self.smoke,
            "args": args,
            "outputs": outputs,
            "seconds": round(time.time() - started, 2),
            "finished": time.strftime("%Y-%m-%d %H:%M:%S"),
            "versions": versions(),
        }
        path = self.path("records", f"{step}.json")
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return path


def versions() -> dict[str, Any]:
    out: dict[str, Any] = {"python": sys.version.split()[0], "platform": platform.platform(),
                           "machine": platform.machine()}
    for pkg in PACKAGES:
        try:
            out[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            out[pkg] = None
    try:
        out["git_commit"] = subprocess.run(
            ["git", "rev-parse", "HEAD"], check=False, cwd=REPO_ROOT, capture_output=True, text=True,
            timeout=10).stdout.strip() or None
        out["git_dirty"] = bool(subprocess.run(
            ["git", "status", "--porcelain", "."], check=False, cwd=REPO_ROOT, capture_output=True,
            text=True, timeout=10).stdout.strip())
    except (OSError, subprocess.SubprocessError):
        out["git_commit"] = None
    return out


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
