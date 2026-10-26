"""Where the data are.

``demo`` reads the open-access PhysioNet demo subsets. ``full`` reads the credentialed
MIMIC-IV, MIMIC-IV-ED and eICU-CRD files, which PhysioNet releases only to credentialed users
who have signed its data use agreements.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PATHS_FILE = REPO_ROOT / "experiments" / "configs" / "paths.json"

DEMO_LABEL = (
    "DEMO DATA: open-access PhysioNet demo subset. Exercises the pipeline; describes no "
    "population. Not a result."
)


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


def get_source(name: str) -> Source:
    if name not in ("demo", "full"):
        raise ValueError(f"unknown source {name!r}")
    paths_file = Path(os.environ.get("AGW_PATHS", PATHS_FILE))
    config = json.loads(paths_file.read_text(encoding="utf-8"))[name]
    dirs = {k: (paths_file.parent.parent.parent / v).resolve() if not Path(v).is_absolute()
            else Path(v) for k, v in config.items()}
    label = DEMO_LABEL if name == "demo" else "MIMIC-IV-ED / eICU-CRD, credentialed"
    return Source(name, dirs, label)
