"""Edge measurement harness: action timing, latency summaries, metered energy, M1 scaling."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from agentic_gateway.agent import ScriptedPolicy, StepGate, run_episode
from agentic_gateway.agent.gate import CheckResult
from agentic_gateway.edge import (
    energy_mj,
    m1_scaling,
    machine,
    peak_rss_mb,
    summarise,
    time_actions,
    traced_peak_mb,
)
from agentic_gateway.gateway import Decision


class RecordingCheck:
    name = "rec"

    def __call__(self, prob, embedding, group, patient_id, clock):
        return CheckResult(Decision.ALLOW, (), {"local_calibration.latency_ns": 2_000_000,
                                                "conformal.latency_ns": 1_000_000,
                                                "conformal.status": "ok"})


@pytest.fixture
def trajectories(make_tools, clinical):
    setting = clinical[0]
    tools = make_tools("normal")
    out = []
    for case in ("c1", "c2", "c3"):
        row = tools.cases.loc[case]
        traj, _ = run_episode(ScriptedPolicy(cited=setting.cited), tools, case, setting="ed",
                              seed=0, y=int(row["y"]), group=str(row["group"]),
                              patient_id=str(row["patient_id"]))
        out.append(traj)
    return out


def test_time_actions_checks_every_step_every_repeat(trajectories):
    actions, (start, stop) = time_actions(trajectories, lambda c: StepGate(RecordingCheck()),
                                          repeats=3, warmup=2)
    n_steps = sum(len(t.steps) for t in trajectories)
    assert len(actions) == 3 * n_steps
    assert sorted(actions["repeat"].unique()) == [0, 1, 2]
    assert (actions["latency_ns"] >= 0).all() and start <= stop
    assert (actions["decision"] == "allow").all()
    # per-signal latencies are kept, other record fields are not
    risk = actions[actions["tool"] == "risk_score"]
    assert (risk["local_calibration.latency_ns"] == 2_000_000).all()
    assert "conformal.status" not in actions.columns
    assert actions.loc[actions["tool"] != "risk_score", "local_calibration.latency_ns"] \
        .isna().all()


def test_time_actions_uses_a_fresh_gate_per_trajectory(trajectories):
    built = []

    def factory(context):
        built.append(context)
        return StepGate(RecordingCheck())

    time_actions(trajectories, factory, repeats=2, warmup=0)
    assert built == ["normal"] * (2 * len(trajectories))


def test_summarise_reports_overall_and_per_tool_percentiles():
    actions = pd.DataFrame({
        "tool": ["risk_score"] * 100 + ["fetch_record"] * 100,
        "latency_ns": np.r_[np.arange(1, 101) * 1e6, np.full(100, 1e5)],
        "local_calibration.latency_ns": np.r_[np.full(100, 3e6), np.full(100, np.nan)],
    })
    table = summarise(actions).set_index("tool")
    assert list(table.index) == ["all", "fetch_record", "risk_score"]
    assert table.loc["all", "n"] == 200
    risk = table.loc["risk_score"]
    assert risk["p50_ms"] == pytest.approx(50.5)
    assert risk["p50_ms"] <= risk["p95_ms"] <= risk["p99_ms"]
    assert risk["local_calibration_p50_ms"] == pytest.approx(3.0)
    assert table.loc["fetch_record", "p95_ms"] == pytest.approx(0.1)


def test_energy_integrates_the_meter_log_inside_the_window(tmp_path):
    log = tmp_path / "meter.csv"
    t = np.arange(0.0, 21.0, 0.5)
    watts = np.where((t >= 5) & (t <= 15), 2.0, 50.0)  # 50 W outside the window is ignored
    pd.DataFrame({"timestamp": t, "watts": watts}).to_csv(log, index=False)
    # 2 W for 10 s = 20 J, over 100 actions = 200 mJ each
    assert energy_mj(log, (5.0, 15.0), 100) == pytest.approx(200.0)


def test_energy_is_missing_rather_than_estimated(tmp_path):
    assert np.isnan(energy_mj(None, (0.0, 1.0), 10))
    log = tmp_path / "meter.csv"
    pd.DataFrame({"timestamp": [0.0, 1.0], "watts": [2.0, 2.0]}).to_csv(log, index=False)
    assert np.isnan(energy_mj(log, (0.0, 1.0), 0))
    assert np.isnan(energy_mj(log, (0.5, 0.9), 10))  # no samples inside the window


def test_m1_scaling_skips_sizes_larger_than_the_reference(reference):
    emb = reference[["e0", "e1"]].to_numpy()
    out = m1_scaling(emb, reference["probability"].to_numpy(), reference["label"].to_numpy(),
                     "euclidean", [200, 1000, 5000], emb[:20], min_neighbors=30)
    assert list(out["reference_size"]) == [200, 1000]
    assert (out["p50_ms"] <= out["p95_ms"]).all()
    assert out["fit_peak_mb"].iloc[1] > out["fit_peak_mb"].iloc[0] > 0
    assert (out["query_peak_mb"] > 0).all()
    assert (out["process_peak_mb"] >= out["fit_peak_mb"]).all()


def test_traced_peak_sees_a_temporary_numpy_array():
    mb = traced_peak_mb(lambda: np.ones(2**20))  # 8 MiB of float64, freed at once
    assert 7.9 < mb < 9.0
    assert traced_peak_mb(lambda: None) < 0.5


def test_process_peak_never_goes_down():
    before = peak_rss_mb()
    block = np.ones(2**23)  # 64 MiB, touched
    block[::512] = 2.0
    after = peak_rss_mb()
    del block
    assert after >= before > 0
    assert peak_rss_mb() >= after


def test_machine_describes_this_computer():
    info = machine()
    assert {"platform", "machine", "processor", "cpus", "ram_gb"} <= set(info)
    assert info["cpus"] >= 1 and info["ram_gb"] > 0
