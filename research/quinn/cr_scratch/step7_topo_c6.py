import FreeCAD as App, os, json, time, collections
PC=r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\frame.FCStd"
d=App.openDocument(PC)
objs=[o for o in d.Objects if hasattr(o,"Shape") and o.Shape.Solids]
def kind(n):
    for k in ("tnut","bracket_purchased","bracket_printed","member"):
        if n.startswith(k): return k
res=collections.defaultdict(lambda:[0,0.0,0.0]); mx=0; over=[]
t=time.time()
for i in range(len(objs)):
    a=objs[i]; ba=a.Shape.BoundBox
    for j in range(i+1,len(objs)):
        b=objs[j]; bb=b.Shape.BoundBox
        bx=App.BoundBox(ba); bx.enlarge(0.02)
        if not bx.intersect(bb): continue
        c=a.Shape.common(b.Shape).Volume
        k="|".join(sorted((kind(a.Name),kind(b.Name))))
        res[k][0]+=1; res[k][1]+=c; res[k][2]=max(res[k][2],c)
        if c>0.01: over.append((a.Name,b.Name,c))
json.dump({"pairs":{k:v for k,v in res.items()},"over":over,"n":len(objs),"secs":time.time()-t},open(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step7_topo_c6.json","w"),indent=0)
print("BUILD_DONE")
