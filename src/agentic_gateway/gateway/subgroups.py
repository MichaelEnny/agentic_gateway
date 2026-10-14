"""Subgroup labels shared by M2 (SCDI) and M3 (Mondrian conformal).

The patent requires both modules to use the same subgroup definitions (dependent claim 9), so
both take labels from this one function.
"""

from __future__ import annotations

from collections.abc import Sequence
from itertools import pairwise

import numpy as np
import pandas as pd

UNKNOWN = "__unknown__"


def group_labels(frame: pd.DataFrame, columns: Sequence[str], sep: str = "|") -> pd.Series:
    """One label per row, the intersection of ``columns``, e.g. ``"F|65+"``.

    A missing value in any column gives the UNKNOWN label rather than a silent new category,
    so a patient with unrecorded demographics is visibly outside every calibrated subgroup.
    """
    if not columns:
        raise ValueError("at least one subgroup column is required")
    missing = [c for c in columns if c not in frame.columns]
    if missing:
        raise KeyError(f"subgroup columns not in frame: {missing}")
    parts = frame[list(columns)]
    # pandas 3 keeps NaN through astype(str), so blank it first and overwrite below.
    labels = parts.astype(object).where(parts.notna(), "").astype(str).agg(sep.join, axis=1)
    labels[parts.isna().any(axis=1).to_numpy()] = UNKNOWN
    return labels


def age_band(age: Sequence[float] | pd.Series, cuts: Sequence[float] = (65.0,)) -> pd.Series:
    """Age bands such as ``"<65"`` and ``"65+"``; NaN stays NaN."""
    values = pd.Series(age, dtype="float64")
    edges = [-np.inf, *cuts, np.inf]
    names = [f"<{int(cuts[0])}"]
    names += [f"{int(lo)}-{int(hi) - 1}" for lo, hi in pairwise(cuts)]
    names += [f"{int(cuts[-1])}+"]
    return pd.cut(values, bins=edges, labels=names, right=False).astype("object")
