import FreeCAD as App, math
d=App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\assembly\pose_Kmax_100p0.FCStd")
b=d.getObject("base").Shape; rec=sorted(b.Solids,key=lambda s:s.Volume)[0]; o=[]
for f in rec.Faces:
    try:
        if f.Surface.__class__.__name__!="Plane": continue
        n=f.normalAt(0,0)
        if abs(abs(n.z)-1)>1e-6: continue
        rs=[math.hypot(v.X,v.Y) for v in f.Vertexes]
        o.append("n.z %+d z %.3f rmin %.2f rmax %.2f area %.0f"%(n.z,f.BoundBox.ZMin,min(rs),max(rs),f.Area))
    except Exception: pass
open(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step7_dbg.txt","w").write("\n".join(sorted(o,key=lambda s:float(s.split()[3]))))
