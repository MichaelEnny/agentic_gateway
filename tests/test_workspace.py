"""Run folders: shared steps 1-3 at the base, one folder per agent run for steps 4-10."""

from __future__ import annotations

import pytest

from agentic_gateway import workspace as wsmod
from agentic_gateway.workspace import Workspace


@pytest.fixture(autouse=True)
def tmp_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(wsmod, "REPO_ROOT", tmp_path)
    return tmp_path


def test_base_and_run_folders(tmp_runs):
    shared = Workspace("ed", "demo", True)
    run = Workspace("ed", "demo", True, "qwen7b")
    assert shared.root == shared.base == tmp_runs / "runs" / "ed_demo_smoke"
    assert run.base == shared.base and run.root == shared.base / "agent_qwen7b"


def test_runs_write_apart_and_read_shared_inputs_from_the_base(tmp_runs):
    shared = Workspace("ed", "demo", True)
    shared.path("cohort.parquet").write_text("steps 1-3")
    scripted = Workspace("ed", "demo", True, "scripted")
    llm = Workspace("ed", "demo", True, "qwen7b")
    scripted.path("benchmark", "test.joblib").write_text("scripted")
    llm.path("benchmark", "test.joblib").write_text("llm")
    assert scripted.require("benchmark", "test.joblib").read_text() == "scripted"
    assert llm.require("benchmark", "test.joblib").read_text() == "llm"
    assert llm.require("cohort.parquet") == shared.base / "cohort.parquet"


def test_a_run_file_shadows_the_base(tmp_runs):
    Workspace("ed", "demo", True).path("configs", "x.json").write_text("base")
    run = Workspace("ed", "demo", True, "r1")
    run.path("configs", "x.json").write_text("run")
    assert run.require("configs", "x.json").read_text() == "run"


def test_missing_input_names_the_run_folder(tmp_runs):
    with pytest.raises(FileNotFoundError, match="agent_r1"):
        Workspace("ed", "demo", True, "r1").require("benchmark", "test.joblib")


def test_records_go_to_the_run_folder(tmp_runs):
    run = Workspace("ed", "demo", True, "r1")
    path = run.record("04_build_benchmark", {}, {}, started=0.0)
    assert path.parent == run.root / "records"


@pytest.mark.parametrize("name", ["", "../x", "a b", "x" * 65])
def test_bad_run_names_are_refused(name):
    with pytest.raises(ValueError):
        Workspace("ed", "demo", True, name)


def test_smoke_is_refused_on_full_data():
    with pytest.raises(ValueError):
        Workspace("ed", "full", True)
