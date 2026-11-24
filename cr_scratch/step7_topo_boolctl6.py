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


out={}
for dz in (-1.0,-2.0):
    s2=nut.copy(); s2.translate(V(0,0,dz))
    c=rec.common(s2); u=rec.fuse(s2)
    out[str(dz)]=dict(common=round(c.Volume,3),valid=c.isValid(),union=round(u.Volume,3),implied=round(rec.Volume+s2.Volume-u.Volume,3),cut_ab=round(rec.cut(s2).Volume,3),implied2=round(rec.Volume-rec.cut(s2).Volume,3),
        zr=[round(c.BoundBox.ZMin,2),round(c.BoundBox.ZMax,2)])
    print("fz",dz,out[str(dz)],flush=True)
print("BUILD_DONE")
