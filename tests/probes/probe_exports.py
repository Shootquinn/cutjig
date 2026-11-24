"""E1 and T1d inputs: re-import every output/step/<name>.step and report solid count, volume, unit check against the FCStd result JSON,
product-tree labels, and the nut and receiver ridge phase at theta 0 and 90. Output results/probes/exports.json.
Run: freecadcmd tests/probes/probe_exports.py"""
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib as L  # noqa: E402
C = L.C


def ridge(sh, p, zlo, zhi):
    P = L.G(p, "thread.pitch")
    r = (L.G(p, "thread.major") - L.G(p, "chain.h")) / 2.0
    out = []
    for th in (0.0, 90.0):
        iv = C.axial_ivals(sh, th, r, zlo, zhi)
        c = [(a + b) / 2.0 for a, b in iv]
        out.append(min(c, key=lambda x: abs(x - (zlo + zhi) / 2.0)) % P if c else None)
    return out


def main():
    import FreeCAD as App
    import Part
    p = L.params()
    out, inputs = {}, []
    for path in sorted(glob.glob(os.path.join(L.ROOT, "output", "step", "*.step"))):
        name = os.path.splitext(os.path.basename(path))[0]
        sh = Part.read(path)
        rj = os.path.join(L.CACHE, name + "_result.json")
        fc = json.load(open(rj)) if os.path.exists(rj) else {}
        bb = sh.BoundBox
        want = fc.get("bbox")
        unit_ok = bool(want) and abs(bb.XMax - bb.XMin - (want["xmax"] - want["xmin"])) < 1e-3 * max(1.0, bb.XMax - bb.XMin)
        doc = App.newDocument("exp_" + name)
        try:
            import Import
            Import.insert(path, doc.Name)
            labels = [o.Label for o in doc.Objects]
        except Exception:
            labels = []
        rec = {"step_solids": len(sh.Solids), "step_volume": sh.Volume, "fcstd_volume": fc.get("volume_mm3"),
               "unit": "mm" if unit_ok else "unverified", "tree_names": labels}
        if name in ("nut", "receiver"):
            zr = (8.0, 32.0) if name == "nut" else (48.5, 80.5)
            rec["ridge_theta0_90"] = ridge(sh, p, *zr)
        out[name] = rec
        inputs.append(path)
        App.closeDocument(doc.Name)
    L.finish("exports", out, inputs)


if __name__ in ("__main__", "probe_exports"):
    L.guarded(main, "exports")
