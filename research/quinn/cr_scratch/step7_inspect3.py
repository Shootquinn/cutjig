import FreeCAD as App
d=App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\output\jig_assembly.FCStd")
out=[]
for o in d.Objects:
    if hasattr(o,"Shape") and not o.Shape.isNull():
        b=o.Shape.BoundBox
        out.append("%s | %s | nsol=%d vol=%.0f x[%.1f,%.1f] y[%.1f,%.1f] z[%.2f,%.2f]"%(o.Name,o.Label,len(o.Shape.Solids),o.Shape.Volume,b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax))
open(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step7_inspect3.txt","w").write("\n".join(out))
