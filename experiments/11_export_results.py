"""Copy aggregate, non-patient-level results from runs/ into results/ for publication.

Only files matching ALLOW are copied. Each copied file is scanned and the export
stops if it contains a patient identifier column or key. Patient-level outputs
(cohorts, predictions, trajectories, fitted models, neighbour indexes, judge
caches, sampled case lists) never match ALLOW.

Demographic subgroup cells with fewer than MIN_CELL patients are suppressed in
the exported JSON: the cell keeps "n": "<10" and loses its other values.

Usage: python experiments/11_export_results.py [--dry-run]
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
OUT = ROOT / "results"

SETTINGS = {
    "ed": ("ed_full", "agent_qwen7b-ed-full-reduced-v1"),
    "icu": ("icu_full", "agent_qwen7b-icu-full-reduced-v1"),
}

# Paths relative to runs/<setting>_full/
ALLOW = [
    "summary_data.json",
    "summary_gateway.json",
    "summary_models.json",
    "records/*.json",
    "gateway/*/scdi/*.json",
    "gateway/*/drift/*.json",
    "{agent}/summary_benchmark.json",
    "{agent}/configs/gateway_frozen.json",
    "{agent}/records/*.json",
    "{agent}/e1/summary_e1.json",
    "{agent}/e1/summary_e1.md",
    "{agent}/e2/headline.json",
    "{agent}/e2/judge_headline.json",
    "{agent}/e2/judge_passed_quality.json",
    "{agent}/e2/judge_passed_quality.md",
    "{agent}/e2/judge_summary.csv",
    "{agent}/e2/judge_summary.md",
    "{agent}/e2/passed_quality.json",
    "{agent}/e2/passed_quality.md",
    "{agent}/e2/summary_e2_e3.csv",
    "{agent}/e2/summary_e2_e3.md",
    "{agent}/e4/*/latency_full.csv",
    "{agent}/e4/*/latency_full_without_m1.csv",
    "{agent}/e4/*/m1_scaling.csv",
    "{agent}/e4/*/summary_e4.json",
    "{agent}/figures/*.csv",
    "{agent}/figures/index.json",
    "{agent}/live/summary_live.csv",
    "{agent}/live/summary_live.json",
    "{agent}/live/summary_live.md",
    "{agent}/tuning/grid.csv",
    "{agent}/tuning_attempt1/grid.csv",
    "{agent}/tuning_attempt1/05_tune_thresholds.json",
    "{agent}/tuning_attempt1/summary_gateway_attempt1.json",
]
# Edge-device logs (no patient data), copied as-is.
LOG_DIRS = {"pi5_logs": "edge_logs/pi5", "laptop_rerun_logs": "edge_logs/laptop"}

# Never copied, even if a pattern above were widened by mistake.
DENY_SUFFIXES = {".parquet", ".joblib", ".jsonl", ".pkl", ".npy", ".npz", ".feather"}

ID_PATTERN = re.compile(
    r"\b(subject_id|hadm_id|stay_id|patientunitstayid|patienthealthsystemstayid|"
    r"uniquepid|patient_id|case_id|episode_id|mrn)\b",
    re.IGNORECASE,
)


MIN_CELL = 10
SUBGROUP_KEY = re.compile(r"^(Asian|Black|Hispanic|White|Other)\|(F|M|Female|Male)$|^__unknown__$")


def suppress(obj, key=""):
    """Return (obj, count) with small demographic subgroup cells removed."""
    if isinstance(obj, dict):
        n = obj.get("n")
        if SUBGROUP_KEY.match(key) and isinstance(n, (int, float)) and 0 < n < MIN_CELL:
            return {"n": f"<{MIN_CELL}", "suppressed": True}, 1
        out, total = {}, 0
        for k, v in obj.items():
            out[k], c = suppress(v, str(k))
            total += c
        return out, total
    if isinstance(obj, list):
        out, total = [], 0
        for v in obj:
            v2, c = suppress(v, key)
            out.append(v2)
            total += c
        return out, total
    return obj, 0


def candidates() -> list[tuple[Path, Path]]:
    pairs = []
    for name, (run_dir, agent) in SETTINGS.items():
        base = RUNS / run_dir
        patterns = [p.format(agent=agent) for p in ALLOW]
        for f in sorted(base.rglob("*")):
            if not f.is_file():
                continue
            rel = f.relative_to(base).as_posix()
            if any(fnmatch.fnmatchcase(rel, p) for p in patterns):
                rel_out = rel.replace(f"{agent}/", "agent/")
                pairs.append((f, OUT / name / rel_out))
    for src_dir, dst in LOG_DIRS.items():
        for f in sorted((RUNS / src_dir).glob("*")):
            if f.is_file():
                pairs.append((f, OUT / dst / f.name))
    return pairs


def check(path: Path) -> list[str]:
    problems = []
    if path.suffix.lower() in DENY_SUFFIXES:
        problems.append("denied file type")
    text = path.read_text(encoding="utf-8", errors="replace")
    for m in ID_PATTERN.finditer(text):
        problems.append(f"identifier-like token '{m.group(0)}'")
        break
    if path.suffix == ".csv":
        rows = text.count("\n")
        if rows > 5000:
            problems.append(f"{rows} rows, looks row-level")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pairs = candidates()
    bad = {src: p for src, _ in pairs if (p := check(src))}
    for src, p in bad.items():
        print(f"BLOCKED {src.relative_to(ROOT)}: {'; '.join(p)}")
    if bad:
        print("Export stopped: fix the allowlist or the files above.")
        return 1

    if OUT.exists() and not args.dry_run:
        for item in OUT.iterdir():
            if item.name == "README.md":
                continue
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    manifest, suppressed_total = [], 0
    for src, dst in pairs:
        data = src.read_bytes()
        entry = {
            "path": dst.relative_to(OUT).as_posix(),
            "source": src.relative_to(ROOT).as_posix(),
            "source_sha256": hashlib.sha256(data).hexdigest(),
        }
        if src.suffix == ".json":
            obj, n_supp = suppress(json.loads(data))
            if n_supp:
                data = (json.dumps(obj, indent=2) + "\n").encode("utf-8")
                entry["suppressed_cells"] = n_supp
                suppressed_total += n_supp
        entry["sha256"] = hashlib.sha256(data).hexdigest()
        entry["bytes"] = len(data)
        manifest.append(entry)
        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
    print(f"Suppressed {suppressed_total} subgroup cells with n < {MIN_CELL}")
    if not args.dry_run:
        (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    total = sum(m["bytes"] for m in manifest)
    print(f"{'Would copy' if args.dry_run else 'Copied'} {len(manifest)} files, {total / 1024:.0f} KiB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
