"""Compare the parametric 30-6060 section against the human's STEP section (1 mm slab, same centre).
Run: freecadcmd.exe build_parts/profile_fidelity.py  -> results/profile_fidelity.json, sentinel PROFILE_FIDELITY_OK"""
import json, os, sys, time
_here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts"
sys.path.insert(0, os.path.dirname(_here))
import FreeCAD as App
import Part
from build_parts import common

D = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\Planet Enterprises\NIAC\BOREBOTS\Unleashed Robotics\ENGINEERING\FractalMining\Borebot Hardware"
t0 = time.time()
s = Part.Shape()
s.read(os.path.join(D, "8020-30-6060 X 1540.step"))
bb = s.BoundBox
zmid = (bb.ZMin + bb.ZMax) / 2
slab = Part.makeBox(200, 200, 1, App.Vector(-100, -100, zmid - 0.5))
step_sec = s.common(slab)
model = common.build_profile(1.0, common.load_params())
model.translate(App.Vector((bb.XMin + bb.XMax) / 2, (bb.YMin + bb.YMax) / 2, zmid - 0.5))
d1 = step_sec.cut(model).Volume
d2 = model.cut(step_sec).Volume
res = {"sentinel": "PROFILE_FIDELITY_OK", "run_started_epoch": t0, "step_area_mm2": step_sec.Volume,
       "model_area_mm2": model.Volume, "step_not_model_mm2": d1, "model_not_step_mm2": d2, "sym_diff_mm2": d1 + d2,
       "sym_diff_pct_of_step": 100 * (d1 + d2) / step_sec.Volume}
common.RESULTS_DIR.mkdir(exist_ok=True)
with open(common.RESULTS_DIR / "profile_fidelity.json", "w") as f:
    json.dump(res, f, indent=1)
print("PROFILE_FIDELITY_OK", res)
sys.stdout.flush()
