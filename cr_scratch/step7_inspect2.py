import FreeCAD as App
d=App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\assembly\pose_Kmax_100p0.FCStd")
out=[]
for n in ("base","frame","bracket","cutter","collet"):
    for i,s in enumerate(d.getObject(n).Shape.Solids):
        b=s.BoundBox
        out.append("%s[%d] vol=%.0f x[%.1f,%.1f] y[%.1f,%.1f] z[%.2f,%.2f]"%(n,i,s.Volume,b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax))
open(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step7_inspect2.txt","w").write("\n".join(out))
