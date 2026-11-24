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
def half(axis, c, big=1000.0):
    o=[-big,-big,-big]; sz=[2*big]*3
    o[axis]=c; sz[axis]=big
    return Part.makeBox(sz[0],sz[1],sz[2],V(*o))   # keeps coordinate > c side as the tool
for name,s in (("receiver",rec),("nut",nut)):
    for axis,c in ((0,0.0),(1,0.3),(2,100.0 if name=="receiver" else 120.0),(2,60.0)):
        t=half(axis,c)
        try:
            cu=s.cut(t); co=s.common(t)
            r=dict(V=round(s.Volume,2),cut=round(cu.Volume,2),common=round(co.Volume,2),sum_err=round(cu.Volume+co.Volume-s.Volume,3),
                   cut_valid=cu.isValid(),cut_zero_change=abs(cu.Volume-s.Volume)<1e-6,
                   cut_past_plane=round((cu.BoundBox.XMax if axis==0 else cu.BoundBox.YMax if axis==1 else cu.BoundBox.ZMax)-c,4))
        except Exception as e:
            r=str(e)[:100]
        out["%s_axis%d_%s"%(name,axis,c)]=r
        print("hc",name,axis,c,r,flush=True)
print("BUILD_DONE")
