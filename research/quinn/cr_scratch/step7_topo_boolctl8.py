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
def trial(an, a, bn, b, vec):
    b2=b.copy(); b2.translate(V(*vec))
    r={}
    try:
        c=a.common(b2); r["common"]=round(c.Volume,3); r["cvalid"]=c.isValid()
        r["implied_cut"]=round(sum(x.Volume for x in a.Solids)-a.cut(b2).Volume,3)
        r["implied_fuse"]=round(sum(x.Volume for x in a.Solids)+b2.Volume-a.fuse(b2).Volume,3)
        r["dist"]=round(a.distToShape(b2)[0],4)
    except Exception as e:
        r["err"]=str(e)[:80]
    return r
pairs=[("base","holder"),("base","collet"),("base","washer"),("base","core"),("base","nut"),("base","cutter"),("nut","holder"),("nut","collet"),("nut","washer"),("nut","core"),("nut","cutter")]
for an,bn in pairs:
    a=sh[an]; b=sh[bn]
    res={}
    for vec in ((1.5,0,0),(0,0,-1.5),(0,0,1.5)):
        res[str(vec)]=trial(an,a,bn,b,vec)
    out[an+"|"+bn]=res
    print("pc",an,bn,res,flush=True)
    # unshifted
    print("pc0",an,bn,round(a.common(b).Volume,3),flush=True)
json.dump(out,open(os.path.join(ROOT,"research", "quinn", "cr_scratch","step7_topo_boolctl8.json"),"w"),indent=1)
print("BUILD_DONE")
