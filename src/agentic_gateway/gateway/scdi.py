"""M2: Subgroup Calibration Deviation Index, computed offline and looked up at run time.

Definition (spec para. [0021]): for subgroup g,

    SCDI_g = max over other subgroups h of |ECE_g - ECE_h|, divided by the overall ECE.

This is per subgroup. It is not the DCGS statistic (max ECE - min ECE, one number per model)
used in the breast cancer paper; the PRD records why the two must not be mixed.

Subgroups smaller than ``min_size`` are left out of the table, so at run time they come back
as UNAVAILABLE instead of carrying an ECE estimated from a handful of patients.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from ..metrics import ece

SCHEMA_VERSION = 1


@dataclass(frozen=True)
class SCDITable:
    scdi: dict[str, float]
    subgroup_ece: dict[str, float]
    subgroup_n: dict[str, int]
    overall_ece: float
    computed_at: float
    excluded: dict[str, int]  # subgroups below min_size, with their counts

    def lookup(self, group: str) -> float | None:
        return self.scdi.get(group)

    def save(self, path: str | Path) -> None:
        payload = {"schema_version": SCHEMA_VERSION, **self.__dict__}
        Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> SCDITable:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        version = payload.pop("schema_version", None)
        if version != SCHEMA_VERSION:
            raise ValueError(f"SCDI table schema {version}, expected {SCHEMA_VERSION}")
        return cls(**payload)


def compute_scdi_table(
    labels: NDArray[np.float64],
    probabilities: NDArray[np.float64],
    groups: NDArray[np.str_] | list[str],
    *,
    min_size: int = 50,
    computed_at: float = 0.0,
) -> SCDITable:
    """Offline job. Run on a held-out validation split, never on the test split."""
    y = np.asarray(labels, dtype=np.float64).ravel()
    p = np.asarray(probabilities, dtype=np.float64).ravel()
    g = np.asarray(groups, dtype=object).ravel()
    if not (y.size == p.size == g.size):
        raise ValueError("labels, probabilities and groups must have the same length")

    overall = ece(y, p)
    per_group: dict[str, float] = {}
    sizes: dict[str, int] = {}
    excluded: dict[str, int] = {}
    for name in sorted(set(g.tolist())):
        mask = g == name
        n = int(mask.sum())
        if n < min_size:
            excluded[str(name)] = n
            continue
        per_group[str(name)] = ece(y[mask], p[mask])
        sizes[str(name)] = n

    scdi: dict[str, float] = {}
    if len(per_group) >= 2:
        if overall <= 0.0:
            raise ValueError("overall ECE is zero; SCDI is undefined (division by zero)")
        values = np.array(list(per_group.values()))
        for name, e in per_group.items():
            scdi[name] = float(np.abs(values - e).max() / overall)
    elif len(per_group) == 1:
        # With one subgroup there is nothing to compare against: no gap by definition.
        scdi[next(iter(per_group))] = 0.0

    return SCDITable(
        scdi=scdi,
        subgroup_ece=per_group,
        subgroup_n=sizes,
        overall_ece=float(overall),
        computed_at=float(computed_at),
        excluded=excluded,
    )


def scdi_null_threshold(
    labels: NDArray[np.float64],
    probabilities: NDArray[np.float64],
    groups: NDArray[np.str_] | list[str],
    *,
    n_permutations: int = 200,
    quantile: float = 0.95,
    min_size: int = 50,
    seed: int = 0,
) -> float:
    """SCDI value that subgroups with no real calibration difference reach by chance.

    ECE estimated on a few hundred patients is noisy, and SCDI divides that noise by the
    overall ECE, which is small for a well-calibrated model. So SCDI is well above zero even
    when every subgroup is calibrated alike: on synthetic data with 8 random subgroups, the
    largest SCDI was 0.80 at n = 3,000 and 0.47 at n = 30,000. The patent's example
    threshold of 0.15 would flag every subgroup.

    This shuffles the subgroup labels (keeping the subgroup sizes), recomputes the largest
    SCDI each time, and returns the requested quantile of that maximum. A threshold set at or
    above it flags a subgroup only when its gap exceeds what chance produces at these sizes.
    """
    y = np.asarray(labels, dtype=np.float64).ravel()
    p = np.asarray(probabilities, dtype=np.float64).ravel()
    g = np.asarray(groups, dtype=object).ravel()
    rng = np.random.default_rng(seed)
    maxima = np.empty(n_permutations)
    for i in range(n_permutations):
        table = compute_scdi_table(y, p, rng.permutation(g), min_size=min_size)
        maxima[i] = max(table.scdi.values(), default=0.0)
    return float(np.quantile(maxima, quantile))
