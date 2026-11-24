import FreeCAD as App, json, os
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
PC = os.path.join(ROOT, "parts_cache"); AS = os.path.join(PC, "assembly")
def top(d, n):
    return d.getObject(n)
def com(s):
    v=sum(x.Volume for x in s.Solids); X=Y=Z=0
    for x in s.Solids:
        c=x.CenterOfMass; X+=c.x*x.Volume; Y+=c.y*x.Volume; Z+=c.z*x.Volume
    return (round(X/v,3), round(Y/v,3), round(Z/v,3))
def shape_of(path, prefer=("Body","WindowsHolesGlyphs","NotchInsertsTick")):
    d = App.openDocument(path); sh=None
    # last visible solid
    cands=[o for o in d.Objects if hasattr(o,"Shape") and o.Shape.Solids and getattr(o,"Visibility",True)]
    o=cands[-1]
    s=o.Shape.copy(); nm=o.Name
    App.closeDocument(d.Name); return s,nm
out={}
local={}
for name,f in (("base","base"),("holder","holder"),("collet","collet_100p0_clamped_Kd1"),("nut","nut"),("washer","washer"),("core","core"),("cutter","cutter")):
    s,nm=shape_of(os.path.join(PC,f+".FCStd")); local[name]=(com(s),round(s.Volume,3),nm)
out["local"]=local
res={}
for fn in ("pose_Kd1_100p0","pose_R_100p0","pose_Kmax_100p0","ws1","ws2","ws3","ws4","ws5","ws6","ws7","ws8","ws9","ws10","ws11"):
    d=App.openDocument(os.path.join(AS,fn+".FCStd"))
    r={}
    for o in d.Objects:
        if o.Label in ("base","holder","collet","nut","washer","core","cutter"):
            s=o.Shape
            r[o.Label]=dict(com=com(s),vol=round(s.Volume,3),placement=[round(x,4) for x in (o.Placement.Base.x,o.Placement.Base.y,o.Placement.Base.z)],
                 shp_pl=[round(x,4) for x in (s.Placement.Base.x,s.Placement.Base.y,s.Placement.Base.z)])
    res[fn]=r
    App.closeDocument(d.Name)
out["poses"]=res
json.dump(out,open(os.path.join(ROOT,"research", "quinn", "cr_scratch","step7_topo_com.json"),"w"),indent=0)
print("BUILD_DONE")
