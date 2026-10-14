"""Paper figures. Each function takes the step outputs as data, draws one figure, and writes
``<stem>.pdf`` (vector, for the manuscript), ``<stem>.png`` (300 dpi) and ``<stem>.csv``
(the values plotted: the table view, and what a reviewer can check).

Needs the ``figures`` extra (``uv sync --extra figures``); matplotlib is imported lazily so the
rest of the package works without it.

Style, for print at MDPI column widths (single 8.5 cm, double 17.4 cm):

* color only where it carries a category, at most three hues (blue, orange, aqua: validated
  for colour-vision deficiency on all pairs) plus a receding gray for "nothing happened";
  methods are named on the axis, never by color alone;
* thin marks, a surface-colored gap between adjacent fills, hairline grid on the value axis
  only, no top or right spines, one y-scale per panel (two measures = two panels).
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .benchmark.analysis import bootstrap_table, per_trajectory

INK, INK_2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE = "#e1e0d9", "#c3c2b7", "#ffffff"
BLUE, ORANGE, AQUA, NEUTRAL = "#2a78d6", "#eb6834", "#1baf7a", "#d6d4cc"

SINGLE, DOUBLE = 3.35, 6.85  # inches: MDPI single and double column

MAIN_METHODS = ("no_gate", "output_only", "confidence", "pooled_conformal", "llm_judge", "full")
METHOD_LABELS = {
    "no_gate": "No gate", "output_only": "Output-only", "confidence": "Confidence threshold",
    "pooled_conformal": "Pooled conformal", "llm_judge": "LLM-as-judge",
    "full": "Full gateway",
}
SIGNAL_LABELS = {
    "local_calibration": "M1 local calibration", "subgroup_gap": "M2 subgroup gap",
    "conformal": "M3 Mondrian conformal", "drift": "M4 drift", "timing": "M5 timing",
    "argcheck": "Argument check",
}
FAULT_LABELS = {
    "sparse": "Sparse region", "subgroup": "Subgroup miscalibration",
    "uncertainty": "High uncertainty", "drift": "Drift (unit error)",
    "duplicate": "Duplicate alert", "ungrounded": "Ungrounded argument",
}
OUTCOMES = (("premature", "Premature", ORANGE), ("early", "Early", BLUE),
            ("late", "Late", AQUA), ("missed", "Missed", NEUTRAL))


def _plt() -> Any:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5,
        "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
        "text.color": INK, "axes.labelcolor": INK_2, "axes.edgecolor": AXIS,
        "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK_2,
        "ytick.labelcolor": INK_2, "axes.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": False, "grid.color": GRID, "grid.linewidth": 0.5,
        "axes.facecolor": SURFACE, "figure.facecolor": SURFACE,
        "lines.linewidth": 1.5, "lines.markersize": 5,
        "legend.frameon": False, "pdf.fonttype": 42, "ps.fonttype": 42,
        "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
    })
    return plt


def _save(fig: Any, out: Path, data: pd.DataFrame) -> pd.DataFrame:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".pdf"))
    fig.savefig(out.with_suffix(".png"), dpi=300)
    data.to_csv(out.with_suffix(".csv"), index=False)
    import matplotlib.pyplot as plt

    plt.close(fig)
    return data


def _value_grid(ax: Any, axis: str = "x") -> None:
    ax.grid(True, axis=axis)
    ax.set_axisbelow(True)


def _methods_present(methods: Sequence[str], order: Sequence[str] = MAIN_METHODS) -> list[str]:
    return [m for m in order if m in set(methods)]


# -- RQ1: when each method stops a faulty trajectory -------------------------------------------


def interception_outcomes(rows: pd.DataFrame, out: Path) -> pd.DataFrame:
    """Small multiples, one per fault type: for each method, the share of faulty trajectories
    stopped before the fault (premature), at it (early), after it (late), or never (missed).
    ``rows`` are replay rows (step 7)."""
    df = per_trajectory(rows)
    df = df[df["kind"] != "clean"]
    methods = _methods_present(df["method"].unique())
    df = df[df["method"].isin(methods)]
    df["late"] = df["intercepted"] - df["early"]
    df["missed"] = 1 - df["intercepted"] - df["premature"]
    data = (df.groupby(["kind", "method"])[["premature", "early", "late", "missed"]].mean()
            .reset_index())
    kinds = [k for k in FAULT_LABELS if k in set(data["kind"])]

    plt = _plt()
    ncols = 2
    nrows = int(np.ceil(len(kinds) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(DOUBLE, 0.25 + 0.32 * len(methods) * nrows),
                             sharex=True, sharey=True, squeeze=False)
    y = np.arange(len(methods))
    for ax, kind in zip(axes.flat, kinds):
        part = data[data["kind"] == kind].set_index("method").reindex(methods)
        left = np.zeros(len(methods))
        for key, _label, color in OUTCOMES:
            vals = part[key].fillna(0).to_numpy()
            ax.barh(y, vals, left=left, height=0.62, color=color, edgecolor=SURFACE,
                    linewidth=1.0)
            for yi, (lft, v) in enumerate(zip(left, vals)):
                if v >= 0.12:  # direct label where the segment has room
                    ax.text(lft + v / 2, yi, f"{v:.0%}", ha="center", va="center",
                            fontsize=6, color=SURFACE if color in (BLUE, ORANGE) else INK)
            left += vals
        ax.set_title(FAULT_LABELS[kind], loc="left")
        ax.set_yticks(y, [METHOD_LABELS.get(m, m) for m in methods])
        ax.invert_yaxis()
        ax.set_xlim(0, 1)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.tick_params(axis="y", length=0)
    for ax in axes.flat[len(kinds):]:
        ax.set_visible(False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in OUTCOMES]
    fig.legend(handles, [lbl for _, lbl, _ in OUTCOMES], loc="upper center", ncols=4,
               bbox_to_anchor=(0.5, 1.02))
    fig.supxlabel("Share of faulty trajectories", fontsize=7.5, color=INK_2)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    return _save(fig, out, data)


# -- RQ1 x RQ2: detection against cost ---------------------------------------------------------


def tradeoff(rows: pd.DataFrame, out: Path) -> pd.DataFrame:
    """Early interception (mean over fault types) against false intervention on clean
    trajectories, one labelled point per method; leave-one-out variants as small gray points."""
    df = per_trajectory(rows)
    early = (df[df["kind"] != "clean"].groupby(["method", "kind"])["early"].mean()
             .groupby("method").mean())
    fi = df[df["kind"] == "clean"].groupby("method")["false_intervention"].mean()
    data = pd.DataFrame({"early_mean_over_faults": early, "false_intervention": fi}) \
        .reset_index().rename(columns={"index": "method"})

    plt = _plt()
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE * 0.85))
    _value_grid(ax, "both")
    main = data[data["method"].isin(MAIN_METHODS)]
    rest = data[~data["method"].isin(MAIN_METHODS)]
    ax.scatter(rest["false_intervention"], rest["early_mean_over_faults"], s=14, color=AXIS,
               zorder=2, label="Leave-one-out variants")
    ax.scatter(main["false_intervention"], main["early_mean_over_faults"], s=30, color=BLUE,
               edgecolor=SURFACE, linewidth=1.0, zorder=3)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    _label_points(fig, ax, data[["false_intervention", "early_mean_over_faults"]].to_numpy(),
                  main[["false_intervention", "early_mean_over_faults"]].to_numpy(),
                  [METHOD_LABELS.get(m, m) for m in main["method"]])
    ax.set_xlabel("False intervention on clean trajectories")
    ax.set_ylabel("Early interception (mean over fault types)")
    pct = plt.FuncFormatter(lambda v, _: f"{v:.0%}")
    ax.xaxis.set_major_formatter(pct)
    ax.yaxis.set_major_formatter(pct)
    if len(rest):
        ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0))
    return _save(fig, out, data)


def _text_box(text: Any, renderer: Any) -> Any:
    """Extent of an annotation's text alone; ``Annotation.get_window_extent`` also covers its
    leader line, which would make every leader label collide with its own point."""
    from matplotlib.text import Text

    text.update_positions(renderer)  # place it at its point; undrawn it sits at the origin
    return Text.get_window_extent(text, renderer)


def _segment_distance(p: tuple, a: tuple, b: tuple) -> float:
    """Distance from point p to segment ab, in display pixels."""
    pa, ba = np.subtract(p, a), np.subtract(b, a)
    t = float(np.clip(np.dot(pa, ba) / max(float(np.dot(ba, ba)), 1e-9), 0.0, 1.0))
    return float(np.hypot(*(pa - t * ba)))


def _label_points(fig, ax, points, targets, labels) -> None:  # type: ignore[no-untyped-def]
    """Direct labels that avoid each other and the other points. For each target, spots are
    tried on rings of growing distance in eight directions (nearest first); the first whose
    text stays inside the axes and clears every placed label and every other point is kept.
    Labels more than 12 pt away get a hairline leader. Boxes are measured from the rendered
    text alone."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    frame = ax.get_window_extent(renderer)
    dots = [tuple(ax.transData.transform(p)) for p in points]
    # (dx, dy, ha): straight up/down appear twice, centred and extending right of the point
    directions = ((1, 0.6, "left"), (1, -0.6, "left"), (-1, 0.6, "right"), (-1, -0.6, "right"),
                  (0, 1, "center"), (0, -1, "center"), (0, 1, "left"), (0, -1, "left"),
                  (1, 0, "left"), (-1, 0, "right"))
    candidates = [(d * sx, d * sy, ha) for d in (6, 14, 24, 36, 50) for sx, sy, ha in directions]
    taken: list[Any] = []
    for (x, y), label in sorted(zip(map(tuple, targets), labels), key=lambda t: -t[0][1]):
        own = tuple(ax.transData.transform((x, y)))
        others = [d for d in dots if np.hypot(d[0] - own[0], d[1] - own[1]) > 0.5]
        chosen = None
        for dx, dy, ha in candidates:
            va = "bottom" if dy > 0 else "top" if dy < 0 else "center"
            far = np.hypot(dx, dy) > 12
            # leader starts at the label's anchor corner, the point the clearance check uses
            relpos = ({"left": 0.0, "center": 0.5, "right": 1.0}[ha],
                      {"bottom": 0.0, "center": 0.5, "top": 1.0}[va])
            leader = ({"arrowstyle": "-", "color": AXIS, "linewidth": 0.6, "shrinkA": 1,
                       "shrinkB": 3, "relpos": relpos} if far else None)
            text = ax.annotate(label, (x, y), xytext=(dx, dy), textcoords="offset points",
                               ha=ha, va=va, fontsize=6.5, color=INK, arrowprops=leader)
            box = _text_box(text, renderer)
            inside = (box.x0 >= frame.x0 and box.x1 <= frame.x1 and box.y0 >= frame.y0
                      and box.y1 <= frame.y1)
            pad = box.expanded(1.04, 1.25)
            clear = inside and not any(pad.overlaps(b) for b in taken) and not any(
                pad.x0 - 3 <= px <= pad.x1 + 3 and pad.y0 - 3 <= py <= pad.y1 + 3
                for px, py in others)
            if clear and far:  # a leader must not pass close to another point
                scale = fig.dpi / 72.0
                end = (own[0] + dx * scale, own[1] + dy * scale)
                clear = all(_segment_distance(dot, own, end) > 6 for dot in others)
            if clear:
                chosen = box
                break
            text.remove()
        if chosen is None:  # nothing free: keep the nearest spot; the CSV has the value
            text = ax.annotate(label, (x, y), xytext=(6, 4), textcoords="offset points",
                               fontsize=6.5, color=INK)
            chosen = _text_box(text, renderer)
        taken.append(chosen)


# -- RQ3: what each signal buys and costs ------------------------------------------------------


def ablation(rows: pd.DataFrame, out: Path, signal_latency_ms: dict[str, float] | None = None,
             *, n_boot: int = 2000, seed: int = 0) -> pd.DataFrame:
    """Left: change in early interception when each signal is removed (pooled over fault
    types, paired patient-clustered bootstrap CI). Right, if latencies are given: that
    signal's median latency per gated action (step 8). Two panels, one scale each."""
    df = per_trajectory(rows)
    faulty = df[df["kind"] != "clean"]
    variants = [m for m in faulty["method"].unique() if m.startswith("minus_")]
    keep = faulty[faulty["method"].isin(["full", *variants])]
    table = bootstrap_table([("faulty", keep, ["early"])], ["full", *variants], n_boot=n_boot,
                            seed=seed, reference="full")
    data = table[table["method"] != "full"][["method", "diff_vs_ref", "diff_low", "diff_high"]]
    data = data.assign(signal=data["method"].str.removeprefix("minus_"))
    order = [s for s in SIGNAL_LABELS if s in set(data["signal"])]
    data = data.set_index("signal").reindex(order).reset_index()
    if signal_latency_ms:
        data["latency_p50_ms"] = data["signal"].map(signal_latency_ms)

    plt = _plt()
    panels = 2 if signal_latency_ms else 1
    fig, axes = plt.subplots(1, panels, figsize=(DOUBLE if panels == 2 else SINGLE,
                                                 0.5 + 0.3 * len(order)),
                             sharey=True, squeeze=False,
                             gridspec_kw={"width_ratios": [3, 2][:panels]})
    y = np.arange(len(order))
    ax = axes[0, 0]
    _value_grid(ax)
    ax.axvline(0, color=AXIS, linewidth=0.8)
    lo = data["diff_vs_ref"] - data["diff_low"]
    hi = data["diff_high"] - data["diff_vs_ref"]
    ax.errorbar(data["diff_vs_ref"], y, xerr=[lo, hi], fmt="o", color=BLUE, ecolor=BLUE,
                elinewidth=1.0, capsize=0, markersize=5, markeredgecolor=SURFACE)
    ax.set_yticks(y, [SIGNAL_LABELS[s] for s in order])
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Change in early interception when removed (95% CI)")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+.0%}"))
    if panels == 2:
        ax2 = axes[0, 1]
        _value_grid(ax2)
        lat = data["latency_p50_ms"].fillna(0).to_numpy()
        ax2.barh(y, lat, height=0.5, color=BLUE, edgecolor=SURFACE)
        for yi, v in enumerate(data["latency_p50_ms"]):
            ax2.text(0 if np.isnan(v) else v, yi, f"  {_ms_text(v)}", va="center",
                     fontsize=6.5, color=INK_2)
        ax2.set_xlabel("Median latency per gated action (ms)")
        ax2.tick_params(axis="y", length=0)
    fig.tight_layout()
    return _save(fig, out, data)


def _ms_text(v: float) -> str:
    if np.isnan(v):
        return "not measured"
    return f"{v * 1000:.1f} µs" if v < 0.1 else f"{v:.2f} ms"


# -- RQ4: edge measurements --------------------------------------------------------------------


def edge_latency(actions: dict[str, dict[str, pd.DataFrame]], out: Path) -> pd.DataFrame:
    """ECDF of latency per gated action, one panel per device, full gateway vs without M1.
    ``actions`` is {device: {"full": frame, "full_without_m1": frame}} from step 8."""
    variants = (("full", "Full gateway", BLUE), ("full_without_m1", "Without M1", ORANGE))
    plt = _plt()
    devices = list(actions)
    fig, axes = plt.subplots(1, len(devices), figsize=(min(DOUBLE, SINGLE * len(devices)),
                                                       SINGLE * 0.75),
                             sharey=True, squeeze=False)
    records = []
    for ax, device in zip(axes.flat, devices):
        _value_grid(ax, "both")
        for key, label, color in variants:
            frame = actions[device].get(key)
            if frame is None or frame.empty:
                continue
            ms = np.sort(frame["latency_ns"].to_numpy() / 1e6)
            ms = np.maximum(ms, 1e-4)  # log axis
            q = np.arange(1, ms.size + 1) / ms.size
            ax.step(ms, q, where="post", color=color, label=label)
            for pct in (50, 95, 99):
                records.append({"device": device, "variant": key, "percentile": pct,
                                "latency_ms": float(np.percentile(ms, pct)), "n": ms.size})
        ax.set_xscale("log")
        ax.set_title(device, loc="left")
        ax.set_xlabel("Latency per gated action (ms, log)")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    axes[0, 0].set_ylabel("Share of actions at or below")
    axes[0, 0].legend(loc="lower right")
    fig.tight_layout()
    return _save(fig, out, pd.DataFrame(records))


def m1_scaling(scaling: dict[str, pd.DataFrame], out: Path) -> pd.DataFrame:
    """M1 query latency against reference cohort size, per device: median (solid) and p95
    (dashed). Devices take blue, orange, aqua in the order given; at most three."""
    colors = (BLUE, ORANGE, AQUA)
    if len(scaling) > len(colors):
        raise ValueError("at most three devices per figure; facet the rest")
    plt = _plt()
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE * 0.8))
    _value_grid(ax, "both")
    frames = []
    for (device, frame), color in zip(scaling.items(), colors):
        f = frame.sort_values("reference_size")
        ax.plot(f["reference_size"], f["p50_ms"], marker="o", color=color,
                markeredgecolor=SURFACE)
        ax.plot(f["reference_size"], f["p95_ms"], linestyle="--", color=color, linewidth=1.0)
        last = f.iloc[-1]
        ax.annotate(device, (last["reference_size"], last["p50_ms"]), xytext=(4, 0),
                    textcoords="offset points", va="center", fontsize=6.5, color=INK)
        frames.append(f.assign(device=device))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("M1 reference cohort size (log)")
    ax.set_ylabel("M1 latency per query (ms, log)")
    ax.plot([], [], color=MUTED, label="Median")
    ax.plot([], [], color=MUTED, linestyle="--", linewidth=1.0, label="95th percentile")
    ax.legend(loc="upper left")
    return _save(fig, out, pd.concat(frames, ignore_index=True))


# -- E1: subgroup coverage ---------------------------------------------------------------------


def subgroup_coverage(coverage: dict[str, Any], out: Path) -> pd.DataFrame:
    """Conformal coverage per subgroup, Mondrian vs pooled, with the target as a line.
    ``coverage`` is ``summary_e1.json[model]["conformal_coverage"]``."""
    target = float(coverage["target"])
    groups = [g for g in coverage["mondrian"] if g != "_all"] + ["_all"]
    rows = [{"group": g, "n": coverage["mondrian"][g]["n"],
             "mondrian": coverage["mondrian"][g]["coverage"],
             "pooled": coverage["pooled"][g]["coverage"]} for g in groups]
    data = pd.DataFrame(rows)

    plt = _plt()
    fig, ax = plt.subplots(figsize=(SINGLE, 0.5 + 0.24 * len(groups)))
    _value_grid(ax)
    y = np.arange(len(groups))
    ax.axvline(target, color=MUTED, linewidth=0.8, linestyle=":")
    ax.text(target, 1.0, f"target {target:.0%}", transform=ax.get_xaxis_transform(),
            fontsize=6.5, color=INK_2, ha="center", va="bottom")
    ax.hlines(y, data["pooled"], data["mondrian"], color=AXIS, linewidth=1.0)
    # pooled as a ring around the dot, so equal values stay visible
    ax.scatter(data["pooled"], y, s=48, facecolor="none", edgecolor=ORANGE, linewidth=1.4,
               zorder=3, label="Pooled")
    ax.scatter(data["mondrian"], y, s=16, color=BLUE, edgecolor=SURFACE, zorder=4,
               label="Mondrian")
    labels = [("All" if g == "_all" else g) + f" (n={n})" for g, n in zip(groups, data["n"])]
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Conformal coverage on the test part")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.legend(loc="lower left", ncols=2, bbox_to_anchor=(0, 1.06))
    return _save(fig, out, data)


# -- RQ2: live reruns and the quality of what passes ------------------------------------------


def live_completion(table: pd.DataFrame, out: Path) -> pd.DataFrame:
    """Three panels (same decision, alert lost, referred): estimate and 95% CI per method.
    ``table`` is ``live/summary_live.csv`` (step 9)."""
    panels = (("same_decision", "Same decision as ungated"), ("alert_lost", "Alert lost"),
              ("referred", "Referred to a clinician"))
    panels = tuple(p for p in panels if p[0] in set(table["metric"]))
    methods = _methods_present(table["method"].unique())
    data = table[table["metric"].isin([p[0] for p in panels])
                 & table["method"].isin(methods)].copy()

    plt = _plt()
    fig, axes = plt.subplots(1, len(panels), figsize=(DOUBLE, 0.5 + 0.28 * len(methods)),
                             sharey=True, squeeze=False)
    y = np.arange(len(methods))
    for ax, (metric, title) in zip(axes.flat, panels):
        _value_grid(ax)
        part = data[data["metric"] == metric].set_index("method").reindex(methods)
        est = part["estimate"].to_numpy(dtype=float)
        lo = est - part["ci_low"].to_numpy(dtype=float)
        hi = part["ci_high"].to_numpy(dtype=float) - est
        ax.errorbar(est, y, xerr=[np.nan_to_num(lo), np.nan_to_num(hi)], fmt="o", color=BLUE,
                    elinewidth=1.0, markersize=5, markeredgecolor=SURFACE)
        ax.set_title(title, loc="left")
        ax.set_xlim(-0.03, 1.03)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.tick_params(axis="y", length=0)
    axes[0, 0].set_yticks(y, [METHOD_LABELS.get(m, m) for m in methods])
    axes[0, 0].invert_yaxis()
    fig.supxlabel("Share of clean runs (95% CI)", fontsize=7.5, color=INK_2)
    fig.tight_layout()
    return _save(fig, out, data)


def passed_quality(quality: dict[str, Any], out: Path, subset: str = "clean") -> pd.DataFrame:
    """Per method, calibration error (ECE) and conformal coverage of the predictions the gate
    let through vs those it stopped. ``quality`` is ``e2/passed_quality.json`` (step 7)."""
    methods = _methods_present(quality)
    rows = []
    for m in methods:
        for label in ("passed", "stopped"):
            q = quality[m][subset][label]
            rows.append({"method": m, "set": label, "n": q["n"], "ece": q["ece"],
                         "coverage": (q.get("coverage") or {}).get("_all", np.nan)})
    data = pd.DataFrame(rows)

    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE, 0.6 + 0.28 * len(methods)), sharey=True)
    y = np.arange(len(methods))
    for ax, (metric, title) in zip(axes, (("ece", "Calibration error (ECE)"),
                                          ("coverage", "Conformal coverage"))):
        _value_grid(ax)
        wide = data.pivot(index="method", columns="set", values=metric).reindex(methods)
        ax.hlines(y, wide["passed"], wide["stopped"], color=AXIS, linewidth=1.0)
        ax.scatter(wide["stopped"], y, s=22, color=ORANGE, edgecolor=SURFACE, zorder=3,
                   label="Stopped")
        ax.scatter(wide["passed"], y, s=22, color=BLUE, edgecolor=SURFACE, zorder=3,
                   label="Passed")
        ax.set_title(title, loc="left")
        ax.tick_params(axis="y", length=0)
        if metric == "coverage":
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    axes[0].set_yticks(y, [METHOD_LABELS.get(m, m) for m in methods])
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower left", ncols=2, bbox_to_anchor=(0, 1.08))
    fig.tight_layout()
    return _save(fig, out, data)
