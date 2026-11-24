import FreeCAD as App, json, os
exec(open(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step7_topo_split.py").read().split("for name, objn")[0])
out={}
for tag,path in (("old",r"C:\Users\Quinn Morley\AppData\Local\Temp\claude\6f0343b2791941ad\200377dc-f257-44be-a8a6-5a439d6cd6be\scratchpad\nut_old.FCStd"),("new",os.path.join(PC,"nut.FCStd"))):
    d=App.openDocument(path)
    s=d.getObject("WindowsHolesGlyphs").Shape
    pairs,npl=coplanar_pairs(s)
    desc=[]
    for a,b,dd in pairs:
        fa,fb=s.Faces[a],s.Faces[b]
        n=fa.normalAt(0,0)
        desc.append((round(n.x),round(n.y),round(n.z),dd,round(fa.Area,2),round(fb.Area,2),[round(x,1) for x in (fa.BoundBox.ZMin,fa.BoundBox.ZMax)]))
    out[tag]=dict(faces=len(s.Faces),E=len(s.Edges),V=len(s.Vertexes),vol=round(s.Volume,3),pairs=desc)
    App.closeDocument(d.Name)
json.dump(out,open(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step7_topo_split2.json","w"),indent=0)
print("BUILD_DONE")
