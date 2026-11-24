import FreeCAD as App, os
AS=r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\assembly"
for fn in ("ws4","pose_Kd1_100p0"):
    d=App.openDocument(os.path.join(AS,fn+".FCStd"))
    for o in d.Objects:
        if o.Label=="nut":
            s=o.Shape; c=s.CenterOfMass; b=s.BoundBox
            print("NUT",fn,round(c.x,3),round(c.y,3),round(c.z,3),round(s.Volume,3),s.isValid(),len(s.Faces),round(b.ZMin,2),round(b.ZMax,2),[round(x,3) for x in (o.Placement.Base.x,o.Placement.Base.y,o.Placement.Base.z)])
    App.closeDocument(d.Name)
print("BUILD_DONE")
