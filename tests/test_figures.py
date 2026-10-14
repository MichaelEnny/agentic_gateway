"""Paper figures: each draws from small synthetic step outputs and writes PDF, PNG and CSV.
Skipped when the ``figures`` extra (matplotlib) is not installed."""

from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("matplotlib")

from agentic_gateway import figures as F

METHODS = ("no_gate", "output_only", "confidence", "pooled_conformal", "full",
           "minus_local_calibration", "minus_conformal", "minus_argcheck")


def replay_rows(seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for method, kind, i in itertools.product(METHODS, ["clean", "sparse", "drift"], range(20)):
        fault = -1 if kind == "clean" else 1
        stop = int(rng.choice([-1, 0, 1, 2])) if method != "no_gate" else -1
        rows.append({"method": method, "trajectory_id": f"{kind}{i}", "patient_id": f"p{i}",
                     "kind": kind, "fault_step": fault, "intercept_step": stop, "n_steps": 4})
    return pd.DataFrame(rows)


def written(out):
    return all(out.with_suffix(s).exists() for s in (".pdf", ".png", ".csv"))


def test_interception_outcomes_shares_sum_to_one(tmp_path):
    data = F.interception_outcomes(replay_rows(), tmp_path / "outcomes")
    assert written(tmp_path / "outcomes")
    shares = data[["premature", "early", "late", "missed"]].sum(axis=1)
    assert np.allclose(shares, 1.0)
    assert set(data["method"]) <= set(F.MAIN_METHODS)  # ablations are not in this figure


def test_tradeoff_has_one_point_per_method(tmp_path):
    data = F.tradeoff(replay_rows(), tmp_path / "tradeoff")
    assert written(tmp_path / "tradeoff") and set(data["method"]) == set(METHODS)


def test_ablation_with_and_without_latency(tmp_path):
    data = F.ablation(replay_rows(), tmp_path / "abl", {"local_calibration": 0.9,
                                                        "conformal": 0.004}, n_boot=50)
    assert written(tmp_path / "abl")
    assert list(data["signal"]) == ["local_calibration", "conformal", "argcheck"]
    assert data.set_index("signal").loc["conformal", "latency_p50_ms"] == 0.004
    assert np.isnan(data.set_index("signal").loc["argcheck", "latency_p50_ms"])
    plain = F.ablation(replay_rows(), tmp_path / "abl2", None, n_boot=50)
    assert "latency_p50_ms" not in plain.columns


def test_edge_and_scaling_figures(tmp_path):
    rng = np.random.default_rng(0)
    frame = pd.DataFrame({"latency_ns": rng.integers(1_000, 3_000_000, 200)})
    data = F.edge_latency({"laptop": {"full": frame, "full_without_m1": frame // 10},
                           "pi5": {"full": frame * 3}}, tmp_path / "edge")
    assert written(tmp_path / "edge")
    assert set(data["device"]) == {"laptop", "pi5"} and set(data["percentile"]) == {50, 95, 99}
    scaling = pd.DataFrame({"reference_size": [1000, 5000, 20000], "p50_ms": [1.0, 2.0, 7.0],
                            "p95_ms": [2.0, 4.0, 10.0]})
    F.m1_scaling({"laptop": scaling, "pi5": scaling * 3}, tmp_path / "scale")
    assert written(tmp_path / "scale")
    with pytest.raises(ValueError):
        F.m1_scaling({str(i): scaling for i in range(4)}, tmp_path / "too_many")


def test_subgroup_coverage(tmp_path):
    cov = {"target": 0.9,
           "mondrian": {"A": {"n": 50, "coverage": 0.91}, "B": {"n": 30, "coverage": 0.89},
                        "_all": {"n": 80, "coverage": 0.90}},
           "pooled": {"A": {"n": 50, "coverage": 0.95}, "B": {"n": 30, "coverage": 0.80},
                      "_all": {"n": 80, "coverage": 0.90}}}
    data = F.subgroup_coverage(cov, tmp_path / "cov")
    assert written(tmp_path / "cov") and list(data["group"]) == ["A", "B", "_all"]


def test_live_and_passed_quality(tmp_path):
    table = pd.DataFrame([{"kind": "clean_live", "metric": m, "method": meth, "n": 10,
                           "estimate": 0.5, "ci_low": 0.3, "ci_high": 0.7}
                          for m in ("completed", "same_decision", "alert_lost", "referred")
                          for meth in ("no_gate", "full")])
    data = F.live_completion(table, tmp_path / "live")
    assert written(tmp_path / "live") and "completed" not in set(data["metric"])
    q = {"n": 5, "ece": 0.1, "brier": 0.2, "auroc": 0.8, "coverage": {"_all": 0.9}}
    empty = {"n": 0, "ece": float("nan"), "brier": float("nan"), "auroc": float("nan")}
    quality = {"no_gate": {"clean": {"passed": q, "stopped": empty}},
               "full": {"clean": {"passed": q, "stopped": {**q, "ece": 0.3}}}}
    data = F.passed_quality(quality, tmp_path / "pq")
    assert written(tmp_path / "pq") and len(data) == 4


def test_segment_distance():
    assert F._segment_distance((0, 1), (0, 0), (2, 0)) == pytest.approx(1)
    assert F._segment_distance((3, 0), (0, 0), (2, 0)) == pytest.approx(1)  # past the end


def test_point_labels_do_not_overlap_in_a_crowd():
    from agentic_gateway.figures import _plt, _text_box

    plt = _plt()
    fig, ax = plt.subplots(figsize=(F.SINGLE, F.SINGLE))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    pts = np.array([[0.30, 0.30], [0.33, 0.32], [0.35, 0.28], [0.31, 0.26], [0.6, 0.6]])
    ax.scatter(pts[:, 0], pts[:, 1])
    F._label_points(fig, ax, pts, pts, ["Alpha method", "Beta method", "Gamma method",
                                        "Delta method", "Epsilon"])
    renderer = fig.canvas.get_renderer()
    boxes = [_text_box(t, renderer) for t in ax.texts]
    assert len(boxes) == 5
    assert not any(a.overlaps(b) for a, b in itertools.combinations(boxes, 2))
    plt.close(fig)
