import json, math, numpy as np
ROOT=r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
P=json.load(open(ROOT+r"\research\quinn\cr_scratch\step7_topo_poses.json"))
L=json.load(open(ROOT+r"\results\assembly_poses.json"))
PARTS=["base","holder","collet","nut","washer","core","frame","bracket","tnut","cutter"]
bad=[]
# poses
rows=[]
for key,objs in P["poses"].items():
    pose,tag=key.split("_",1)
    led=L["sizes"][tag][pose]
    names=set(objs)
    if not set(PARTS)<=names: bad.append((key,"parts",sorted(names)))
    for k in PARTS:
        o=objs[k]
        if o["solids"]<1 or o["vol"]<=0 or not o["valid"]: bad.append((key,k,"solid",o["solids"],o["vol"],o["valid"]))
        m=np.array(o["mat"]); lm=np.array(led["placements"][k])[:3]
        if k in ("bracket","tnut"):  # compounds / instance groups: compare only identity expectation
            pass
        diff=np.abs(m-lm).max()
        if diff>1e-4: bad.append((key,k,"placement diff",diff))
        det=np.linalg.det(m[:,:3])
        if abs(det-1)>1e-6: bad.append((key,k,"det",det))
        if o.get("vis") is False: bad.append((key,k,"invisible"))
    # nut phi
    n=np.array(objs["nut"]["mat"]); phi=math.degrees(math.atan2(n[1][0],n[0][0]))
    z0=n[2][3]-40.0
    inv=(z0-8*(phi)/360.0)
    rows.append((key,round(phi,3),round(z0,3),led["phi_deg"],round(((phi-led["phi_deg"]+180)%360)-180,4)))
print("bad",len(bad)); [print(b) for b in bad[:20]]
# screw invariant using ledger unwrapped phi
for tag in L["sizes"]:
    s=L["sizes"][tag]
    r=[]
    for pose in ("R","Kd1","Kmax"):
        v=s[pose]; r.append(round(v["nut_z0_floor_frame"]-8*v["nut_azimuth_deg"]/360.0,3))
    print(tag,"invariant z0-8az/360:",r, "phi",[s[p]["phi_deg"] for p in ("R","Kd1","Kmax")],"dz",[round(s[p]["dz_mm"],3) for p in ("R","Kd1","Kmax")])
    break
# check dz = 8*phi/360
for tag in L["sizes"]:
    for pose in ("Kd1","Kmax"):
        v=L["sizes"][tag][pose]
        e=v["dz_mm"]-8*v["phi_deg"]/360
        nutdz=v["nut_z0_floor_frame"]-L["sizes"][tag]["R"]["nut_z0_floor_frame"]
        if abs(e)>1e-3 or abs(nutdz-v["dz_mm"])>1e-3: print("ledger diff",tag,pose,e,nutdz-v["dz_mm"])
# per size: which parts move between R and K
for tag in L["sizes"]:
    for pose in ("Kd1","Kmax"):
        mv=[k for k in PARTS if np.abs(np.array(P["poses"][pose+"_"+tag][k]["mat"])-np.array(P["poses"]["R_"+tag][k]["mat"])).max()>1e-6]
        if tag in("100p0","090p0") or set(mv)!={"holder","nut","washer","core","collet"}&set(mv) : print(tag,pose,"moved",mv)
# nut modular check: nut(P)=S(phi) nut(R)
for tag in L["sizes"]:
    for pose in ("Kd1","Kmax"):
        v=L["sizes"][tag][pose]; ph=math.radians(v["phi_deg"])
        S=np.eye(4); S[0][0]=math.cos(ph);S[0][1]=-math.sin(ph);S[1][0]=math.sin(ph);S[1][1]=math.cos(ph);S[2][3]=8*ph/(2*math.pi)
        for k in ("nut","washer"):
            R=np.eye(4); R[:3]=np.array(P["poses"]["R_"+tag][k]["mat"])
            Q=np.eye(4); Q[:3]=np.array(P["poses"][pose+"_"+tag][k]["mat"])
            d=np.abs(S@R-Q).max()
            if d>1e-3: print("S(phi) mismatch",tag,pose,k,d)
print("S(phi) check done")
# frame/feet/frame heights
for pose in("R","Kd1","Kmax"):
    o=P["poses"][pose+"_100p0"]
    print(pose,{k:(o[k]["bb"][4],o[k]["bb"][5]) for k in ("base","holder","collet","nut","washer","core","frame","cutter")})
print({k:(v["solids"],v["F"],v["euler"]) for k,v in P["poses"]["Kd1_100p0"].items()})
