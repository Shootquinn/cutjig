import FreeCAD as App, Part, json, os, time
V = App.Vector
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
d = App.openDocument(os.path.join(ROOT, "parts_cache", "assembly", "pose_Kd1_100p0.FCStd"))
sh = {o.Label: o.Shape.copy() for o in d.Objects if hasattr(o, "Shape") and o.Shape.Solids}
base, nut = sh["base"], sh["nut"]
rec = [s for s in base.Solids if abs(s.Volume - 955593.2) < 1000][0]
def area_at(s, z):
    ws = s.slice(V(0, 0, 1), z)
    fs = []
    for w in ws:
        if w.isClosed():
            fs.append(abs(Part.Face(w).Area))
    fs.sort(reverse=True)
    return fs[0] - sum(fs[1:]) if fs else 0.0, len(fs)

bb=rec.BoundBox
zs=[bb.ZMin+0.5+i*1.0 for i in range(int(bb.ZLength-1))]
A=[area_at(rec,z)[0] for z in zs]
print("SCAN",[ (round(z,1),round(a)) for z,a in zip(zs,A)],flush=True)
print("BUILD_DONE")
