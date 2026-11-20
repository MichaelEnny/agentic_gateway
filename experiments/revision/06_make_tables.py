"""LaTeX for the revision tables, generated from analysis_outputs (no hand-typed numbers)."""
import json

from common import OUT as O

J = lambda n: json.loads((O / n).read_text())
F = ("drift", "subgroup", "sparse", "uncertainty", "duplicate", "ungrounded")


def pct(v):
    from decimal import ROUND_HALF_UP, Decimal
    return str((Decimal(repr(v)) * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def row(label, r, fi=True):
    cells = [pct(r[k]) for k in F] + [pct(r["mean_early"])]
    cells.append(f"{pct(r['false_intervention'])} ({pct(r['fi_low'])}--{pct(r['fi_high'])})")
    return f"{label} & " + " & ".join(cells) + r"\\"


ed_m = J("m1m3_ed.json")["test"]["table"]
icu_m = J("m1m3_icu.json")["test"]["table"]
ed_d = J("drift_variants_ed.json")["test"]
icu_d = J("drift_variants_icu.json")["test"]
ed_c = J("m2_alternatives_ed.json")["alt"]["C"]["test"]
icu_c = J("m2_alternatives_icu.json")["alt"]["C"]["test"]
ed_r = J("revised_ed.json")["wide"]["revised configuration"]
icu_r = J("revised_icu.json")["wide"]["revised configuration"]
cm = lambda d: next(v for k, v in d.items() if "complement" in k)

lines = [r"\multicolumn{9}{l}{\emph{Emergency department}}\\",
         row("Full gateway (frozen, primary)", ed_m["full"]),
         row("Without M1", ed_m["without M1"]),
         row("M3 as caveat (no stop)", ed_m["without M3 (= M3 as caveat)"]),
         row("Without M1, M3 as caveat", ed_m["without M1 and M3"]),
         row("M3 coverage 0.90", ed_m["M3 coverage 0.90"]),
         row("M2 one-sided complement gap", cm(ed_c)),
         row("M4 outcome-anchored", ed_d["M4 outcome-anchored"]),
         row(r"Revised configuration$^{a}$", ed_r),
         r"\midrule",
         r"\multicolumn{9}{l}{\emph{Intensive care, 21 held-out hospitals}}\\",
         row("Full gateway (frozen, primary)", icu_d["full (frozen)"]),
         row("Without M4 (prespecified)", icu_d["without M4"]),
         row("M4 outcome-anchored", icu_d["M4 outcome-anchored"]),
         row("M4 shadow refresh", icu_d["M4 shadow refresh"]),
         row(r"\quad shadow, without M1", icu_m["without M1"]),
         row(r"\quad shadow, M3 as caveat", icu_m["without M3 (= M3 as caveat)"]),
         row(r"\quad shadow, M2 complement gap", cm(icu_c)),
         row(r"Revised configuration$^{b}$", icu_r)]
(O / "table9_rows.tex").write_text("\n".join(lines), encoding="utf-8")

# Table 10: break-even lambda
W = {"Equal": dict.fromkeys(F, 1), r"Data faults $\times$2": dict(drift=2, subgroup=2, sparse=2, uncertainty=2, duplicate=1, ungrounded=1),
     r"Sparse, uncertainty $\times$3": dict(drift=1, subgroup=1, sparse=3, uncertainty=3, duplicate=1, ungrounded=1)}
t10 = []
for name, w in W.items():
    cells = []
    for s in ("ed", "icu"):
        for part in ("tune", "test"):
            t = J(f"m1m3_{s}.json")[part]["table"]
            f, c = t["full"], t["without M3 (= M3 as caveat)"]
            e = lambda r: sum(w[k] * r[k] for k in F) / sum(w.values())
            lam = (e(f) - e(c)) / (f["false_intervention"] - c["false_intervention"])
            cells.append("$<$0" if lam < 0 else f"{lam:.2f}")
    t10.append(f"{name} & " + " & ".join(cells) + r"\\")
(O / "table10_rows.tex").write_text("\n".join(t10), encoding="utf-8")

# Table 11: independent faults
NF = ("decimal_slip", "inverted_output", "stale_risk", "field_dropout")
names = {"full": "Full gateway", "output_only": "Output-only", "confidence": "Confidence threshold",
         "pooled_conformal": "Pooled conformal", "minus_conformal": "Full without M3",
         "revised configuration": "Revised configuration"}
t11 = []
for s, lab in (("ed", "Emergency department"), ("icu", "Intensive care (shadow-refreshed M4)")):
    d = J(f"newfaults_{s}.json")
    t11.append(rf"\multicolumn{{7}}{{l}}{{\emph{{{lab}}}}}\\")
    for m, n in names.items():
        r = d["early"][m]
        t11.append(f"{n} & " + " & ".join(pct(r[k]) for k in NF) + f" & {pct(r['mean_early'])} & "
                   f"{pct(r['false_intervention'])}" + r"\\")
    if s == "ed":
        t11.append(r"\midrule")
(O / "table11_rows.tex").write_text("\n".join(t11), encoding="utf-8")
print("\n".join(lines), "\n\n", "\n".join(t10), "\n\n", "\n".join(t11))
for s in ("ed", "icu"):
    d = J(f"newfaults_{s}.json"); print(s, d["n_faulty"], d["share_worse"], d["natural_errors"])
