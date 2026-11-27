"""X1 on the live specs and on the staged P6 set (s1 r9, s3 r8 edits, s4 with x1_edits_at_p6); section_true and section
compared on every shared row (dry run of the P4 X1 extension); stack ties on the staged s1 and s4."""
import json
import sys
from pathlib import Path
sys.path.insert(0, r"D:/Unleashed Robotics/cutjig/docs/sketches")
import check_sketch as ck  # noqa: E402
import check_stack as cs  # noqa: E402
import sketch_loader  # noqa: E402
D = Path(r"D:/Unleashed Robotics/cutjig/docs/sketches"); S = Path(r"D:/Unleashed Robotics/_scratch/cutjig/open14/p2/staged")
out = {}
live = {p.stem.replace("_spec", ""): sketch_loader.load_spec(p) for p in sorted(D.glob("s*_spec.yaml"))}
staged = {p.stem.replace("_spec", ""): sketch_loader.load_spec(p) for p in sorted(S.glob("s*_spec.yaml"))}
for tag, specs in (("live", live), ("staged_p6", staged)):
    r = ck.x1_lint(specs)
    out[tag] = {"result": r["result"], "reason": r["reason"][:1500]}
    print(tag, r["result"], r["reason"][:600])
    for fld in ("section_true", "section"):
        occ = {}
        for nm, sp in specs.items():
            for row in sp.get("features", []):
                occ.setdefault(row["id"], []).append((nm, row.get(fld)))
        diffs, same = [], []
        for rid, lst in occ.items():
            if len(lst) < 2:
                continue
            have = [(nm, v) for nm, v in lst if v is not None]
            if not have:
                continue
            ref = json.dumps(ck._x1_norm(have[0][1]), sort_keys=True)
            bad = [nm for nm, v in lst if json.dumps(ck._x1_norm(v), sort_keys=True) != ref]
            (diffs if bad else same).append((rid, [nm for nm, _ in lst], bad))
        out[f"{tag}_{fld}"] = {"equal": same, "differ": diffs}
        print(f"  {fld}: equal {[s[0] for s in same]}; differ {[(d[0], d[1], d[2]) for d in diffs]}")
P = sketch_loader.Params(None, None)
for nm in ("s1", "s3", "s4"):
    sp = staged[nm]
    st = cs.evaluate_spec(P, sp)
    pose = next(iter(st["poses"]))
    f = st["poses"][pose]["features"]
    off = P.get("jig.datum_a_above_floor")
    names = st["poses"][pose]["vars_z_A"]
    for tie in sp.get("stack_ties", []):
        if tie["feature"] != "holder":
            continue
        z = f["holder"]["z_max"] - off + cs.eval_expr(tie["offset"], P, names)
        print(f"{nm} staged tie holder_flange: holder z_max {f['holder']['z_max'] - off:.3f} + offset = {z:.3f} vs {tie['term']} {names[tie['term']]:.3f} (diff {z - names[tie['term']]:.4f})")
    print(f"{nm} staged holder z_A {f['holder']['z_min'] - off:.2f} to {f['holder']['z_max'] - off:.2f}; collar {f['collar']['z_min'] - off:.2f} to {f['collar']['z_max'] - off:.2f}")
json.dump(out, open(S.parent / "x1dry.json", "w"), indent=1, default=str)
