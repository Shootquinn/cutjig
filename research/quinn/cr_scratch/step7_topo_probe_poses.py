import FreeCAD as App, json, sys, os, math
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
AS = os.path.join(ROOT, "parts_cache", "assembly")
led = json.load(open(os.path.join(ROOT, "results", "assembly_poses.json")))
PARTS = ["base", "holder", "collet", "nut", "washer", "core", "frame", "bracket", "tnut", "cutter"]
out = {"poses": {}, "ws": {}}

def info(d):
    r = {}
    for o in d.Objects:
        if not hasattr(o, "Shape") or o.Shape.isNull():
            continue
        s = o.Shape
        m = o.Placement.Matrix
        sm = s.Placement.Matrix
        r[o.Label if o.Label in PARTS else o.Name] = dict(
            name=o.Name, solids=len(s.Solids), vol=round(s.Volume, 3), valid=s.isValid(),
            mat=[[round(m.A11, 6), round(m.A12, 6), round(m.A13, 6), round(m.A14, 4)],
                 [round(m.A21, 6), round(m.A22, 6), round(m.A23, 6), round(m.A24, 4)],
                 [round(m.A31, 6), round(m.A32, 6), round(m.A33, 6), round(m.A34, 4)]],
            smat_z=round(sm.A34, 4), vis=getattr(o, "Visibility", None),
            bb=[round(x, 3) for x in (s.BoundBox.XMin, s.BoundBox.XMax, s.BoundBox.YMin, s.BoundBox.YMax, s.BoundBox.ZMin, s.BoundBox.ZMax)],
            F=len(s.Faces), euler=len(s.Vertexes) - len(s.Edges) + len(s.Faces))
    return r

for P in ("R", "Kd1", "Kmax"):
    for tag in led["sizes"]:
        f = os.path.join(AS, "pose_%s_%s.FCStd" % (P, tag))
        d = App.openDocument(f)
        out["poses"]["%s_%s" % (P, tag)] = info(d)
        App.closeDocument(d.Name)
    print("poses", P, flush=True)
for n in range(1, 12):
    d = App.openDocument(os.path.join(AS, "ws%d.FCStd" % n))
    out["ws"][str(n)] = info(d)
    App.closeDocument(d.Name)
    print("ws", n, flush=True)
json.dump(out, open(os.path.join(ROOT, "research", "quinn", "cr_scratch", "step7_topo_poses.json"), "w"), indent=1)
print("BUILD_DONE")
