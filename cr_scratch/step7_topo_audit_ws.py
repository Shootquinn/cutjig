import json, math, numpy as np
ROOT=r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
P=json.load(open(ROOT+r"\cr_scratch\step7_topo_poses.json"))
L=json.load(open(ROOT+r"\results\assembly_poses.json"))
pr=json.load(open(ROOT+r"\results\probes\ws1.json")) 
PARTS=["base","holder","collet","nut","washer","core","frame","bracket","tnut","cutter"]
for n in map(str,range(1,12)):
    ws=P["ws"][n]; pose=L["ws"][n]["pose"]; ref=P["poses"][pose+"_100p0"]
    diff=[]
    for k in PARTS:
        a=ws[k]; b=ref[k]
        dm=np.abs(np.array(a["mat"])-np.array(b["mat"])).max()
        dv=abs(a["vol"]-b["vol"]); dbb=max(abs(x-y) for x,y in zip(a["bb"],b["bb"]))
        if dm>1e-6 or dv>1e-3 or dbb>1e-3 or a["F"]!=b["F"] or a["euler"]!=b["euler"]:
            MF=np.array(a["mat"]); M=MF[:,:3]; det=np.linalg.det(M)
            # relative transform
            RF=np.array(b["mat"]); R0=RF[:,:3]
            rel=M@np.linalg.inv(R0)
            ang=math.degrees(math.acos(max(-1,min(1,(np.trace(rel)-1)/2))))
            diff.append((k,"det_pl %.3f"%det,"rel_ang %.3f"%ang,"nz %.4f"%M[2][2],"dz %.3f"%(MF[2][3]-RF[2][3]) ,"vol %.3f/%.3f"%(a["vol"],b["vol"]),"F %d/%d eu %d/%d"%(a["F"],b["F"],a["euler"],b["euler"]),"valid",a["valid"],"solids",a["solids"]))
    print("WS"+n,pose,diff)
    for k in PARTS:
        if ws[k]["vol"]<=0 or not ws[k]["valid"] or ws[k]["solids"]!=1 and k not in("bracket","tnut","cutter","frame"): print("   BAD",k,ws[k]["vol"],ws[k]["valid"])
