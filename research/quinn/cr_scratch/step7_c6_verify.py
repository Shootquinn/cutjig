"""C6 verification (Step 7): per-instance common volumes and host contacts from the rebuilt parts_cache/frame.FCStd. Run under freecadcmd."""
import json
import os
import sys
import time
import FreeCAD as App

ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
src = os.environ.get("C6_SRC", ROOT + "/parts_cache/frame.FCStd")
out_json = ROOT + (r"\research\quinn\cr_scratch\step7_c6_verify_before.json" if "step7_before" in src else r"\research\quinn\cr_scratch\step7_c6_verify.json")
t0 = time.time()
doc = App.openDocument(src)
objs = {o.Name: o.Shape for o in doc.Objects if o.Name.startswith(("member_", "bracket_", "tnut_"))}
kind = lambda n: "member" if n.startswith("member") else ("bracket" if n.startswith("bracket") else "tnut")
names = sorted(objs)
TOL = 0.01


def near(a, b, pad=0.02):
    A, B = a.BoundBox, b.BoundBox
    return not (A.XMax + pad < B.XMin or B.XMax + pad < A.XMin or A.YMax + pad < B.YMin or B.YMax + pad < A.YMin or A.ZMax + pad < B.ZMin or B.ZMax + pad < A.ZMin)


pairs = {}
for i, a in enumerate(names):
    for b in names[i + 1:]:
        if not near(objs[a], objs[b]):
            continue
        k = "|".join(sorted((kind(a), kind(b))))
        v = objs[a].common(objs[b]).Volume
        d = objs[a].distToShape(objs[b])[0] if v < TOL else 0.0
        pairs[f"{a}|{b}"] = {"kind": k, "common_mm3": round(v, 3), "min_dist": round(d, 4)}
summ = {}
for key, m in pairs.items():
    s = summ.setdefault(m["kind"], {"pairs_near": 0, "pairs_over_tol": 0, "max_common_mm3": 0.0, "total_common_mm3": 0.0, "touching": 0})
    s["pairs_near"] += 1
    if m["common_mm3"] >= TOL:
        s["pairs_over_tol"] += 1
    s["max_common_mm3"] = max(s["max_common_mm3"], m["common_mm3"])
    s["total_common_mm3"] = round(s["total_common_mm3"] + m["common_mm3"], 3)
    if m["common_mm3"] < TOL and m["min_dist"] <= TOL:
        s["touching"] += 1
counts = {k: sum(1 for n in names if kind(n) == k) for k in ("member", "bracket", "tnut")}
tn_host = {n: [p for p in pairs if n in p.split("|") and "member" in p and pairs[p]["common_mm3"] < TOL and pairs[p]["min_dist"] <= TOL] for n in names if kind(n) == "tnut"}
br_host = {n: [p for p in pairs if n in p.split("|") and "member" in p and pairs[p]["common_mm3"] < TOL and pairs[p]["min_dist"] <= TOL] for n in names if kind(n) == "bracket"}
res = {"source": src, "counts": counts, "summary": summ,
       "tnuts_with_host_contact": sum(1 for v in tn_host.values() if v), "brackets_with_member_contact": sum(1 for v in br_host.values() if v),
       "pairs_over_tol": {k: v for k, v in pairs.items() if v["common_mm3"] >= TOL}, "seconds": round(time.time() - t0, 1)}
json.dump(res, open(out_json, "w"), indent=1)
print(json.dumps({k: res[k] for k in ("counts", "summary", "tnuts_with_host_contact", "brackets_with_member_contact", "seconds")}), flush=True)
print("BUILD_DONE c6_verify", flush=True)
