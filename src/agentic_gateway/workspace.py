"""One folder per (setting, source, mode) under ``runs/``, and the record each step leaves.

Every step writes ``records/<step>.json`` with its arguments, versions, timing and outputs.
A number that has no record behind it does not go in the paper.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Any

from .data.access import REPO_ROOT

PACKAGES = ("numpy", "pandas", "scipy", "scikit-learn", "joblib", "pyarrow")


@dataclass(frozen=True)
class Workspace:
    setting: str
    source: str
    smoke: bool

    def __post_init__(self) -> None:
        if self.smoke and self.source == "full":
            raise ValueError("--smoke lowers minimums for the demos; never use it on full data")

    @property
    def root(self) -> Path:
        name = f"{self.setting}_{self.source}" + ("_smoke" if self.smoke else "")
        path = REPO_ROOT / "runs" / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def path(self, *parts: str) -> Path:
        p = self.root.joinpath(*parts)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def require(self, *parts: str) -> Path:
        p = self.root.joinpath(*parts)
        if not p.exists():
            raise FileNotFoundError(f"{p} not found; run the earlier step first")
        return p

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
