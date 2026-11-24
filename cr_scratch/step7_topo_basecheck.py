import FreeCAD as App, os
AS=r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\assembly\pose_Kd1_100p0.FCStd"
d=App.openDocument(AS)
b=[o for o in d.Objects if o.Label=="base"][0].Shape
s=b.Solids
print("SOLIDS",[round(x.Volume,1) for x in s])
c=s[0].common(s[1]); print("COMMON",round(c.Volume,4))
print("DIST",s[0].distToShape(s[1])[0])
print("BUILD_DONE")
