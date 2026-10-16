"""Step 5: choose thresholds on the tune benchmark, then freeze them.

    uv run python experiments/05_tune_thresholds.py --setting ed --source demo --smoke

* Grid over the M1 threshold, conformal coverage and the SCDI threshold. The SCDI candidates
  are multiples (``SCDI_GRID``) of max(0.15, permutation null from step 3), so the null stays
  the lower bound. Deviation from the original plan, which fixed SCDI at the null: on the full
  ED tune set the clean subgroups already sit above the null, every clean trajectory was
  deferred and no setting met the cap (recorded in the experiment guide).
* Objective, fixed in advance: the highest share of injected faults intercepted, among
  settings whose false-intervention rate on clean trajectories is at most ``--fd-cap``. Ties go
  to the lower false-intervention rate, then the higher M1 threshold, then the SCDI threshold
  closest to the null. If none qualifies, the lowest false-intervention rate is taken and the
  record says the cap was not met.
* Confidence baseline cut: matched so it defers the same share of clean tune trajectories as
  the chosen gateway.

Writes configs/gateway_frozen.json in the workspace. Steps 6 to 8 read only that file.
Commit a copy before opening the test results.
"""

from __future__ import annotations

import itertools
import time

import joblib
import numpy as np
import pandas as pd
from _common import (
    COVERAGE_GRID,
    PRIMARY_MODEL,
    SCDI_GRID,
    add_run_arg,
    base_config,
    main_guard,
    parser,
    setup,
)

from agentic_gateway.assembly import Artifacts
from agentic_gateway.benchmark import full_factory, pooled_faults, replay
from agentic_gateway.gateway import GatewayConfig
from agentic_gateway.workspace import read_json, write_json

LOCAL_GRID = (0.05, 0.075, 0.10, 0.125, 0.15, 0.20)


def main() -> int:
    p = parser("Tune and freeze thresholds.")
    p.add_argument("--fd-cap", type=float, default=0.10)
    add_run_arg(p)
    args = p.parse_args()
    ws, setting, params = setup(args)
    started = time.time()
    bench = joblib.load(ws.require("benchmark", "tune.joblib"))
    trajectories = bench["clean"] + bench["faulty"]
    art = Artifacts(ws, PRIMARY_MODEL, cache_local=True)
    gw_summary = read_json(ws.require("summary_gateway.json"))[PRIMARY_MODEL]

    values = base_config(params, setting)
    scdi_floor = max(0.15, float(gw_summary["scdi_null_threshold"]))

    grid = []
    for local_t, coverage, mult in itertools.product(LOCAL_GRID, COVERAGE_GRID, SCDI_GRID):
        cfg = GatewayConfig.from_dict({**values, "local_threshold": local_t,
                                       "conformal_coverage": coverage,
                                       "scdi_threshold": scdi_floor * mult})
        rows = replay(trajectories, {"full": full_factory(art, cfg, "tune")})
        pf = pooled_faults(rows).loc["full"]
        grid.append({"local_threshold": local_t, "conformal_coverage": coverage,
                     "scdi_multiple": mult, "scdi_threshold": scdi_floor * mult,
                     "intercepted": pf["intercepted"], "early": pf["early"],
                     "false_intervention": pf["false_intervention"]})
    grid = pd.DataFrame(grid)
    grid.to_csv(ws.path("tuning", "grid.csv"), index=False)

    best, cap_met = select(grid, args.fd_cap)
    values["local_threshold"] = float(best["local_threshold"])
    values["conformal_coverage"] = float(best["conformal_coverage"])
    values["scdi_threshold"] = float(best["scdi_threshold"])

    clean_p = np.array([t.first("risk_score").hidden["probability"] for t in bench["clean"]])
    margin = np.minimum(clean_p, 1 - clean_p)
    fd = float(best["false_intervention"])
    cut = 0.5 if fd <= 0 or margin.size == 0 else float(np.quantile(margin, 1 - fd))

    frozen = {**values, "_meta": {
        "tuned_on": "tune", "fd_cap": args.fd_cap, "cap_met": cap_met,
        "tune_intercepted": float(best["intercepted"]), "tune_false_intervention": fd,
        "scdi_null_threshold": float(gw_summary["scdi_null_threshold"]),
        "scdi_multiple": float(best["scdi_multiple"]), "scdi_grid": list(SCDI_GRID),
        "drift_ece_critical": gw_summary.get("drift_ece_critical"),
        "confidence_cut": cut, "frozen_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "n_tune_trajectories": len(trajectories)}}
    write_json(ws.path("configs", "gateway_frozen.json"), frozen)
    ws.record("05_tune_thresholds", vars(args), frozen["_meta"], started)
    print(f"chosen: local {values['local_threshold']}, coverage {values['conformal_coverage']}, "
          f"SCDI {values['scdi_threshold']:.3f} ({best['scdi_multiple']:g} x null); tune intercepted {best['intercepted']:.2f}, "
          f"false intervention {fd:.2f}{'' if cap_met else ' (cap NOT met)'}; "
          f"confidence cut {cut:.3f}")
    return 0


def select(grid: pd.DataFrame, fd_cap: float) -> tuple[pd.Series, bool]:
    """The grid row the prespecified objective picks, and whether it meets the cap."""
    feasible = grid[grid["false_intervention"] <= fd_cap]
    cap_met = not feasible.empty
    pool = feasible if cap_met else grid[grid["false_intervention"]
                                         == grid["false_intervention"].min()]
    best = pool.sort_values(
        ["intercepted", "false_intervention", "local_threshold", "scdi_threshold"],
        ascending=[False, True, False, True]).iloc[0]
    return best, cap_met


if __name__ == "__main__":
    main_guard(main)
