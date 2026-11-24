import FreeCAD as App, math
d=App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\assembly\pose_Kmax_100p0.FCStd")
out=[]
br=d.getObject("bracket").Shape.Solids; fr=d.getObject("frame").Shape.Solids
for i in range(len(br)):
    for j in range(i+1,len(br)):
        c=br[i].common(br[j]).Volume
        dist=br[i].distToShape(br[j])[0]
        if c>0.01 or dist<0.05: out.append("br%d|br%d common=%.0f dist=%.3f"%(i,j,c,dist))
    for k in range(len(fr)):
        c=br[i].common(fr[k]).Volume
        if c>0.01: out.append("br%d|fr%d common=%.0f"%(i,k,c))
# nut wing azimuth and ruler
n=d.getObject("nut").Shape
far=max(n.Vertexes,key=lambda v:v.X**2+v.Y**2)
out.append("nut far vertex az=%.3f r=%.2f z=%.2f"%(math.degrees(math.atan2(far.Y,far.X)),math.hypot(far.X,far.Y),far.Z))
open(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step7_inspect4.txt","w").write("\n".join(out))
