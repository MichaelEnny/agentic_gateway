"""Step 1: build the cohort, label subgroups, split into five patient-disjoint parts.

    uv run python experiments/01_prepare_data.py --setting ed --source demo --smoke

Writes cohort.parquet (row-level, stays in runs/) and summary_data.json (aggregate counts).
"""

from __future__ import annotations

import time

from _common import main_guard, parser, setup

from agentic_gateway.data import ed, icu, splits
from agentic_gateway.data.access import get_source
from agentic_gateway.gateway.subgroups import group_labels
from agentic_gateway.workspace import write_json

SMOKE_SHARES = {"fit": 0.40, "reference": 0.20, "conformal": 0.20, "tune": 0.20}


def main() -> int:
    p = parser("Build cohort and splits.")
    args = p.parse_args()
    ws, setting, params = setup(args)
    started = time.time()
    source = get_source(args.source)

    cohort, info = (ed if setting.name == "ed" else icu).build(source)
    cols = params.group_cols or setting.default_groups
    cohort["group"] = group_labels(cohort, list(cols)).to_numpy()

    if setting.name == "ed":
        is_test = splits.holdout_by_period(cohort)
    else:
        is_test = splits.holdout_by_site(cohort, share=0.2, min_events=params.icu_min_events,
                                         seed=args.seed)
    shares = SMOKE_SHARES if args.smoke else None
    cohort["part"] = splits.assign_parts(cohort, is_test, seed=args.seed, shares=shares)
    cohort = cohort[cohort["part"] != "dropped"].reset_index(drop=True)
    cohort.to_parquet(ws.path("cohort.parquet"), index=False)

    group_sizes = (cohort.groupby(["part", "group"]).size().unstack(fill_value=0)
                   .to_dict(orient="index"))
    summary = {"label": source.label, "question": setting.question, "group_columns": cols,
               **info, "parts": splits.summarise(cohort, cohort["part"]),
               "group_sizes_by_part": group_sizes}
    write_json(ws.path("summary_data.json"), summary)
    ws.record("01_prepare_data", vars(args), {"rows": len(cohort)}, started)
    print(f"{setting.name}: {len(cohort)} cases")
    for name, row in summary["parts"].items():
        print(f"  {name:<10} {row['cases']:>7} cases {row['patients']:>7} patients "
              f"event rate {row['event_rate']:.3f}")
    return 0


if __name__ == "__main__":
    main_guard(main)
