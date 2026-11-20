"""Copy the aggregate results of the peer-review analyses from runs/revision/ to results/revision/.

Only aggregate files are exported: JSON reports, per-method summary CSVs, the M2 detectability
tables (one row per subgroup), the shadow-window draws (one row per draw) and the recomputed drift
states (test statistics per feature). Replay rows (*_rows.parquet) carry patient and stay
identifiers and are never exported. Every exported file is screened: an integer of six or more
digits (the form of MIMIC and eICU identifiers) or a home-folder path stops the export.
"""
from __future__ import annotations

import re
import shutil
import sys

from common import OUT, REPO

DEST = REPO / "results" / "revision"
PATTERNS = ["*.json", "*_summary.csv", "m2_detectability_*.csv", "r2_shadow_length_draws.csv",
            "drift_states/*.json"]
ID = re.compile(r"(?<![\d.eE+-])\d{6,}(?![\d.])")
HOME = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+|/home/|/Users/")


def main() -> None:
    files = sorted({f for p in PATTERNS for f in OUT.glob(p)})
    problems = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        for m in ID.finditer(text):
            problems.append(f"{f.relative_to(OUT)}: integer {m.group()} at {m.start()}")
        if HOME.search(text):
            problems.append(f"{f.relative_to(OUT)}: home-folder path")
    if problems:
        print("export stopped:\n  " + "\n  ".join(problems[:30]))
        sys.exit(1)
    if DEST.exists():
        shutil.rmtree(DEST)
    for f in files:
        target = DEST / f.relative_to(OUT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f, target)
    print(f"exported {len(files)} files to {DEST.relative_to(REPO)}")


if __name__ == "__main__":
    main()
