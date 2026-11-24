"""Measure the human's local 80/20 STEP/STL files in place. Writes results/step_measure.json.
Run: freecadcmd.exe build_parts/measure_step.py  (success = STEP_MEASURE_OK sentinel + fresh artifact)"""
import json, os, sys, time
import FreeCAD as App
import Part, Mesh

D = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\Planet Enterprises\NIAC\BOREBOTS\Unleashed Robotics\ENGINEERING\FractalMining\Borebot Hardware"
OUT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\results\step_measure.json"
t0 = time.time()
res = {"sentinel": "STEP_MEASURE_OK", "run_started_epoch": t0, "source_dir": D}

def bb(b):
    return {"min": [b.XMin, b.YMin, b.ZMin], "max": [b.XMax, b.YMax, b.ZMax], "size": [b.XLength, b.YLength, b.ZLength]}

def load(name):
    s = Part.Shape()
    s.read(os.path.join(D, name))
    return s

# ---- profile
s = load("8020-30-6060 X 1540.step")
res["profile_file"] = {"bbox": bb(s.BoundBox), "volume": s.Volume, "solids": len(s.Solids), "faces": len(s.Faces), "valid": s.isValid()}
zmid = (s.BoundBox.ZMin + s.BoundBox.ZMax) / 2.0
wires = s.slice(App.Vector(0, 0, 1), zmid)
sec = []
for w in wires:
    pts = []
    segs = []
    for e in w.Edges:
        c = e.Curve
        d = {"type": type(c).__name__, "p0": [e.Vertexes[0].X, e.Vertexes[0].Y], "p1": [e.Vertexes[-1].X, e.Vertexes[-1].Y], "len": e.Length}
        if hasattr(c, "Radius"):
            d["radius"] = c.Radius; d["centre"] = [c.Center.x, c.Center.y]
        segs.append(d)
    f = Part.Face(w)
    sec.append({"closed": w.isClosed(), "area": f.Area, "bbox": bb(w.BoundBox), "nedges": len(w.Edges), "segs": segs})
res["section_z"] = zmid
res["section_wires"] = sec
# section area by face-cut: common with thin slab
slab = Part.makeBox(200, 200, 1, App.Vector(-100, -100, zmid - 0.5))
c = s.common(slab)
res["section_area_from_slab"] = c.Volume / 1.0
# volume / length
res["area_from_volume"] = s.Volume / s.BoundBox.ZLength
# ---- 14089
for nm in ("8020-14089.step", "8020-14089 qmod v0.step"):
    try:
        sh = load(nm)
        res[nm] = {"bbox": bb(sh.BoundBox), "volume": sh.Volume, "solids": len(sh.Solids), "faces": len(sh.Faces)}
        cyl = []
        for f in sh.Faces:
            if type(f.Surface).__name__ == "Cylinder":
                cyl.append({"r": round(f.Surface.Radius, 3), "axis": [round(v, 3) for v in f.Surface.Axis], "c": [round(v, 3) for v in f.Surface.Center]})
        res[nm]["cylinders"] = cyl[:60]
    except Exception as ex:
        res[nm] = {"error": repr(ex)}
# ---- bracket STL
m = Mesh.Mesh(os.path.join(D, "8020 30 Series Corner Bracket 3dp.stl"))
res["bracket_stl"] = {"bbox": bb(m.BoundBox), "facets": m.CountFacets, "volume": m.Volume, "area": m.Area}
with open(OUT, "w") as f:
    json.dump(res, f, indent=1)
print("STEP_MEASURE_OK", round(time.time() - t0, 1))
sys.stdout.flush()
