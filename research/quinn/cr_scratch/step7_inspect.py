import FreeCAD as App, sys, json
out=[]
for tag in ("R_100p0","Kmax_100p0","Kd1_100p0"):
    d=App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\assembly\pose_%s.FCStd"%tag)
    out.append(tag)
    for o in d.Objects:
        if hasattr(o,"Shape") and not o.Shape.isNull():
            b=o.Shape.BoundBox
            out.append("%s %s nsol=%d vol=%.0f z[%.2f,%.2f] x[%.1f,%.1f] y[%.1f,%.1f] vis=%s"%(o.Name,o.Label,len(o.Shape.Solids),o.Shape.Volume,b.ZMin,b.ZMax,b.XMin,b.XMax,b.YMin,b.YMax,getattr(o,"Visibility",None)))
    App.closeDocument(d.Name)
open(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step7_inspect.txt","w").write("\n".join(out))
print("BUILD_DONE")
