"""Step 2: train the risk models on the fit part and score every part.

    uv run python experiments/02_train_models.py --setting ed --source demo --smoke
"""

from __future__ import annotations

import time

import joblib
import pandas as pd
from _common import main_guard, parser, setup

from agentic_gateway.metrics import auroc, brier, ece
from agentic_gateway.models import MODELS, make_model
from agentic_gateway.workspace import write_json

KEEP = ("case_id", "patient_id", "period", "site", "part", "group", "y")


def main() -> int:
    p = parser("Train risk models.")
    p.add_argument("--models", default=",".join(MODELS))
    args = p.parse_args()
    ws, setting, _ = setup(args)
    started = time.time()
    cohort = pd.read_parquet(ws.require("cohort.parquet"))
    fit = cohort[cohort["part"] == "fit"]
    if fit["y"].nunique() < 2:
        raise ValueError("the fit part has one outcome class only")

    scores = {}
    for name in args.models.split(","):
        model = make_model(name, setting, seed=args.seed, smoke=args.smoke)
        model.fit(fit[list(setting.features)], fit["y"])
        joblib.dump(model, ws.path("models", f"{name}.joblib"))
        preds = cohort[list(KEEP)].copy()
        preds["prob"] = model.predict_proba(cohort[list(setting.features)])[:, 1]
        preds.to_parquet(ws.path("predictions", f"{name}.parquet"), index=False)
        scores[name] = {
            part: {"n": len(g), "auroc": auroc(g["y"], g["prob"]),
                   "brier": brier(g["y"], g["prob"]), "ece": ece(g["y"], g["prob"])}
            for part, g in preds.groupby("part")
        }
        test = scores[name].get("test", {})
        print(f"{name:<20} test AUROC {test.get('auroc', float('nan')):.3f} "
              f"ECE {test.get('ece', float('nan')):.3f}")
    write_json(ws.path("summary_models.json"), scores)
    ws.record("02_train_models", vars(args), {"models": list(scores)}, started)
    return 0


if __name__ == "__main__":
    main_guard(main)
