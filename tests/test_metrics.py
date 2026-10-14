"""Closed-form and reference checks for agentic_gateway.metrics."""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats
from sklearn.metrics import brier_score_loss, roc_auc_score

from agentic_gateway import metrics as m


def test_ece_hand_computed():
    # bin 1 (0.1-0.2): p 0.15, 0.15, y 0, 1 -> |0.3 - 1| = 0.7
    # bin 9 (0.9-1.0): p 0.95, 1.0, y 1, 1 -> |1.95 - 2| = 0.05
    y = [0, 1, 1, 1]
    p = [0.15, 0.15, 0.95, 1.0]
    assert m.ece(y, p) == pytest.approx((0.7 + 0.05) / 4)


def test_ece_zero_when_perfect_per_bin():
    assert m.ece([0, 1], [0.5, 0.5]) == pytest.approx(0.0)


def test_brier_and_auroc_match_sklearn():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 500)
    p = np.round(rng.uniform(size=500), 2)  # rounding creates ties
    assert m.brier(y, p) == pytest.approx(brier_score_loss(y, p))
    assert m.auroc(y, p) == pytest.approx(roc_auc_score(y, p))
    assert np.isnan(m.auroc([1, 1], [0.2, 0.3]))


def test_conformal_quantile_rank_and_minimum():
    scores = np.arange(1, 20) / 20.0  # 19 scores
    q, note = m.conformal_quantile(scores, 0.9)
    assert q == scores[17] and note == ""  # rank ceil(20 * 0.9) = 18
    assert m.minimum_calibration_size(0.9) == 9
    q, note = m.conformal_quantile(scores[:8], 0.9)
    assert q == 1.0 and "cannot attain" in note


def test_conformal_coverage_is_valid():
    rng = np.random.default_rng(1)
    hits = []
    for _ in range(300):
        s = rng.uniform(size=50)
        q, _ = m.conformal_quantile(s, 0.9)
        hits.append(rng.uniform() <= q)
    assert np.mean(hits) >= 0.86


def test_nonconformity():
    assert m.nonconformity([1, 0], [0.8, 0.8]).tolist() == pytest.approx([0.2, 0.8])


def test_psi_is_symmetric_kl_sum():
    r = np.array([0.2, 0.3, 0.5])
    c = np.array([0.4, 0.4, 0.2])
    assert m.psi(r, c) == pytest.approx(m.kl_divergence(r, c) + m.kl_divergence(c, r))
    assert m.psi(r, r) == 0.0


def test_reference_edges_open_and_tie_aware():
    edges = m.reference_edges(np.array([0, 0, 0, 0, 1, 2, 3, 4, 5, 6.0]), 5)
    assert edges[0] == -np.inf and edges[-1] == np.inf
    assert np.all(np.diff(edges) > 0)
    assert m.reference_edges(np.zeros(10), 5).tolist() == [-np.inf, np.inf]


def test_bh_and_holm_match_statsmodels_formulas():
    p = [0.01, 0.04, 0.03, np.nan, 0.5]
    bh = m.benjamini_hochberg(p)
    # m = 4 tests: sorted 0.01, 0.03, 0.04, 0.5 -> 0.04, 0.0533, 0.0533, 0.5
    assert bh[0] == pytest.approx(0.04)
    assert bh[1] == pytest.approx(0.04 * 4 / 3) and bh[2] == pytest.approx(0.04 * 4 / 3)
    assert np.isnan(bh[3]) and bh[4] == pytest.approx(0.5)
    hl = m.holm(p)
    # 0.01*4, 0.03*3, 0.04*2 -> 0.04, 0.09, 0.09 (monotone), 0.5*1
    assert hl[0] == pytest.approx(0.04) and hl[2] == pytest.approx(0.09)
    assert hl[1] == pytest.approx(0.09) and hl[4] == pytest.approx(0.5)
    # scipy agrees on BH
    ok = [0.01, 0.04, 0.03, 0.5]
    assert np.allclose(m.benjamini_hochberg(ok), stats.false_discovery_control(ok))
