"""Step 3: the offline parts of the gateway, per model.

    uv run python experiments/03_fit_gateway.py --setting ed --source demo --smoke

* M1: neighbour index on the reference part (subsampled to a cap, recorded);
* M2: SCDI table on the reference part, the permutation null threshold, and one degraded
  table per subgroup for the subgroup fault;
* M4: drift states, reference vs tune, reference vs test, and both again with the unit error
  used by the drift fault.
M3 is fitted when needed from the conformal part (cheap), so coverage can be tuned.
"""

from __future__ import annotations

import time

import joblib
import numpy as np
import pandas as pd
from _common import main_guard, parser, setup

from agentic_gateway.benchmark.faults import SUBGROUP_SHIFT
from agentic_gateway.gateway import (
    LocalCalibration,
    compute_scdi_table,
    embedder_for,
    run_drift_job,
    scdi_null_threshold,
)
from agentic_gateway.models import MODELS
from agentic_gateway.workspace import subgroup_file, write_json


def main() -> int:
    p = parser("Fit the offline gateway components.")
    p.add_argument("--models", default=",".join(MODELS))
    args = p.parse_args()
    ws, setting, params = setup(args)
    started = time.time()
    cohort = pd.read_parquet(ws.require("cohort.parquet")).set_index("case_id", drop=False)
    summary = {}

    for name in args.models.split(","):
        model = joblib.load(ws.require("models", f"{name}.joblib"))
        emb = embedder_for(model)
        preds = pd.read_parquet(ws.require("predictions", f"{name}.parquet"))
        ref = preds[preds["part"] == "reference"]
        out = {"embedding": emb.kind, "metric": emb.metric}

        # M1
        rng = np.random.default_rng(args.seed)
        keep = ref if len(ref) <= params.m1_reference_cap else \
            ref.iloc[rng.choice(len(ref), params.m1_reference_cap, replace=False)]
        x = emb.transform(cohort.loc[keep["case_id"], list(setting.features)])
        local = LocalCalibration(min_neighbors=params.min_neighbors, metric=emb.metric).fit(
            x, keep["prob"].to_numpy(), keep["y"].to_numpy())
        joblib.dump(local, ws.path("gateway", name, "local.joblib"))
        out["m1_reference_size"] = len(keep)

        # M2
        table = compute_scdi_table(ref["y"], ref["prob"], ref["group"],
                                   min_size=params.scdi_min_size)
        table.save(ws.path("gateway", name, "scdi", "reference.json"))
        null = scdi_null_threshold(ref["y"], ref["prob"], ref["group"],
                                   n_permutations=params.null_permutations,
                                   min_size=params.scdi_min_size, seed=args.seed)
        out["scdi"] = table.scdi
        out["scdi_excluded"] = table.excluded
        out["scdi_null_threshold"] = null
        for g in sorted(ref["group"].unique()):
            shifted = np.where(ref["group"] == g, np.minimum(1.0, ref["prob"] + SUBGROUP_SHIFT),
                               ref["prob"])
            compute_scdi_table(ref["y"], shifted, ref["group"], min_size=params.scdi_min_size) \
                .save(ws.path("gateway", name, "scdi", f"{subgroup_file(g)}.json"))

        # M4
        field, mult, offset = setting.unit_shift
        reference = _window(cohort, ref, setting)
        states = {}
        for part in ("tune", "test"):
            rows = preds[preds["part"] == part]
            current = _window(cohort, rows, setting)
            shifted = current.copy()
            shifted[field] = shifted[field] * mult + offset
            shifted["probability"] = model.predict_proba(shifted[list(setting.features)])[:, 1]
            for label, window in ((part, current), (f"{part}_shifted", shifted)):
                state = run_drift_job(
                    reference, window, features=list(setting.features),
                    n_boot=params.drift_boot, min_group_size=params.drift_min_group,
                    computed_at=0.0, window=label, seed=args.seed)
                state.save(ws.path("gateway", name, "drift", f"{label}.json"))
                states[label] = {"state": state.state,
                                 "rejected": [t.target for t in state.tests if t.rejected]}
        out["drift"] = states
        summary[name] = out
        drift_text = ", ".join(f"{k}={v['state']}" for k, v in states.items())
        print(f"{name}: M1 n={len(keep)} ({emb.metric}); SCDI {_fmt(table.scdi)} "
              f"null {null:.3f}; drift {drift_text}")

    write_json(ws.path("summary_gateway.json"), summary)
    ws.record("03_fit_gateway", vars(args), {"models": list(summary)}, started)
    return 0


def _window(cohort: pd.DataFrame, preds: pd.DataFrame, setting) -> pd.DataFrame:  # type: ignore[no-untyped-def]
    frame = cohort.loc[preds["case_id"], list(setting.features)].reset_index(drop=True)
    frame["probability"] = preds["prob"].to_numpy()
    frame["label"] = preds["y"].to_numpy()
    frame["group"] = preds["group"].to_numpy()
    return frame


def _fmt(values: dict) -> str:
    return "{" + ", ".join(f"{k}: {v:.2f}" for k, v in values.items()) + "}"


if __name__ == "__main__":
    main_guard(main)
