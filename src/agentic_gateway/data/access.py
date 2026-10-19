"""Where the data are, and whether the credentialed data may be read.

``--source full`` is refused while ``DATA_ACCESS.md`` at the repository root still contains
the sentence in :data:`NOT_AUTHORISED`. The file, not a flag, is the control, so the boundary
cannot be crossed by forgetting it exists.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
STATUS_FILE = REPO_ROOT / "DATA_ACCESS.md"
PATHS_FILE = REPO_ROOT / "experiments" / "configs" / "paths.json"
NOT_AUTHORISED = "Credentialed analysis may not begin yet"

DEMO_LABEL = (
    "DEMO DATA: open-access PhysioNet demo subset. Exercises the pipeline; describes no "
    "population. Not a result."
)


class NotAuthorisedError(RuntimeError):
    pass


@dataclass(frozen=True)
class Source:
    name: str  # "demo" or "full"
    dirs: dict[str, Path]
    label: str

    def path(self, key: str, table: str) -> Path:
        folder = self.dirs[key]
        for candidate in (folder / f"{table}.csv.gz", folder / f"{table}.csv"):
            if candidate.exists():
                return candidate
        raise FileNotFoundError(f"{table} not found in {folder}")


def require_authorised() -> None:
    if not STATUS_FILE.exists():
        raise NotAuthorisedError(f"{STATUS_FILE} is missing; refusing credentialed data")
    if NOT_AUTHORISED in STATUS_FILE.read_text(encoding="utf-8"):
        raise NotAuthorisedError(
            f"{STATUS_FILE.name} says credentialed analysis may not begin yet. "
            "Use --source demo, or update that file once access is approved."
        )


def get_source(name: str) -> Source:
    if name not in ("demo", "full"):
        raise ValueError(f"unknown source {name!r}")
    if name == "full":
        require_authorised()
    paths_file = Path(os.environ.get("AGW_PATHS", PATHS_FILE))
    config = json.loads(paths_file.read_text(encoding="utf-8"))[name]
    dirs = {k: (paths_file.parent.parent.parent / v).resolve() if not Path(v).is_absolute()
            else Path(v) for k, v in config.items()}
    label = DEMO_LABEL if name == "demo" else "MIMIC-IV-ED / eICU-CRD, credentialed"
    return Source(name, dirs, label)
