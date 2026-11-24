"""Build the base-frame members as 30-6060 extrusions and write results/frame_profiles.json.
Run: freecadcmd.exe build_parts/frame_profiles.py   (success = sentinel line + fresh artifact, A.15)
Expected duration under 30 s (six small extrusions)."""
import json
import os
import sys
import time

_here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts"
sys.path.insert(0, os.path.dirname(_here))

import FreeCAD as App  # noqa: E402
from build_parts import common  # noqa: E402

if getattr(App, "_frame_ran", False):
    sys.exit(0)
App._frame_ran = True

t0 = time.time()
p = common.load_params()
members = common.get(p, "frame.members")
doc = App.newDocument("frame_profiles")
out = []
for m in members:
    for i in range(m["qty"]):
        name = f"{m['id']}_{i + 1}"
        shp = common.build_profile(m["cut_mm"], p)
        obj = doc.addObject("Part::Feature", name)
        obj.Shape = shp
        bb = shp.BoundBox
        out.append({
            "name": name, "cut_mm": m["cut_mm"], "length_mm": bb.ZLength,
            "bbox_mm": [round(bb.XLength, 4), round(bb.YLength, 4), round(bb.ZLength, 4)],
            "volume_mm3": shp.Volume, "valid": shp.isValid(), "solids": len(shp.Solids),
            "area_mm2": shp.Volume / m["cut_mm"],
        })
doc.recompute()
common.PARTS_CACHE.mkdir(exist_ok=True)
common.RESULTS_DIR.mkdir(exist_ok=True)
doc.saveAs(str(common.PARTS_CACHE / "frame_profiles.FCStd"))
res = {"sentinel": "FRAME_PROFILES_OK", "run_started_epoch": t0, "members": out,
       "freecad_version": ".".join(App.Version()[:3]), "area_model_analytic_mm2": common.profile_area_model(p)}
with open(common.RESULTS_DIR / "frame_profiles.json", "w") as f:
    json.dump(res, f, indent=1)
print("FRAME_PROFILES_OK", len(out), "members", round(time.time() - t0, 2), "s")
sys.stdout.flush()
