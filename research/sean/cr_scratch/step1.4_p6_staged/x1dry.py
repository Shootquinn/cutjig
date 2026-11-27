"""X1 on the live specs and on the staged P6 set (this folder: s1 r9, s3 r8, s4 with x1_edits_at_p6) with the live
s2_spec.yaml added (Loftsman P3b Correction 4: S2 carries none of the base rows, but X1 on the staged three alone compares
28 rows); section_true compared on every shared row (dry run of the P4 X1 extension); holder stack ties on s1 and s4.
P2f (research/sean/cr_scratch/step1.4_engineer_spec_fixes.md)."""
import json
import sys
from pathlib import Path
sys.path.insert(0, r"D:/Unleashed Robotics/cutjig/docs/sketches")
import check_sketch as ck  # noqa: E402
import check_stack as cs  # noqa: E402
import sketch_loader  # noqa: E402
D = Path(r"D:/Unleashed Robotics/cutjig/docs/sketches"); S = Path(__file__).resolve().parent
out = {}
live = {p.stem.replace("_spec", ""): sketch_loader.load_spec(p) for p in sorted(D.glob("s*_spec.yaml"))}
staged = {p.stem.replace("_spec", ""): sketch_loader.load_spec(p) for p in sorted(S.glob("s*_spec.yaml"))}
staged.setdefault("s2", live["s2"])
for tag, specs in (("live", live), ("staged_p6", staged)):
    r = ck.x1_lint(specs)
    occ = {}
    for nm, sp in specs.items():
        for row in sp.get("features", []):
            if row.get("section_true") is not None:
                occ.setdefault(row["id"], []).append((nm, json.dumps(ck._x1_norm(row["section_true"]), sort_keys=True)))
    eq = {k: len(set(v for _, v in lst)) == 1 for k, lst in occ.items() if len(lst) > 1}
    out[tag] = {"specs": sorted(specs), "result": r["result"], "reason": r["reason"][:1500], "section_true_equal": eq}
    print(tag, sorted(specs), r["result"], r["reason"][:300], "section_true equal:", eq)
P = sketch_loader.Params(None, None)
off = P.get("jig.datum_a_above_floor")
for nm in ("s1", "s4"):
    sp = staged[nm]
    st = cs.evaluate_spec(P, sp)
    pose = next(iter(st["poses"]))
    f = st["poses"][pose]["features"]
    names = st["poses"][pose]["vars_z_A"]
    for tie in sp.get("stack_ties", []):
        if tie["feature"] == "holder":
            z = f["holder"]["z_max"] - off + cs.eval_expr(tie["offset"], P, names)
            print(f"{nm} staged tie holder_flange: {f['holder']['z_max'] - off:.3f} + offset = {z:.3f} vs {tie['term']} {names[tie['term']]:.3f} (diff {z - names[tie['term']]:.4f})")
json.dump(out, open(S / "x1dry.json", "w"), indent=1, default=str)
