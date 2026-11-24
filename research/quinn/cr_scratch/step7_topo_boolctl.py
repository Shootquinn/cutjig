import FreeCAD as App, Part, json, os, random, time
V = App.Vector
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
AS = os.path.join(ROOT, "parts_cache", "assembly")
out = {}
t0 = time.time()
random.seed(7)

def objs(fn):
    d = App.openDocument(os.path.join(AS, fn + ".FCStd"))
    r = {o.Label: o.Shape.copy() for o in d.Objects if hasattr(o, "Shape") and o.Shape.Solids}
    App.closeDocument(d.Name)
    return r

def bopcheck(s):
    try:
        s.check(True)
        return "OK"
    except Exception as e:
        return str(e)[:200]

def planar_straddle(solid, name):
    """Box 5x5 in the face plane, 5 mm into the material and 5 mm outside, on a z-facing planar face. Analytic common = 125."""
    res = []
    for f in sorted([f for f in solid.Faces if f.Surface.__class__.__name__ == "Plane" and abs(abs(f.normalAt(0, 0).z) - 1) < 1e-9], key=lambda f: -f.Area):
        n = f.normalAt(0, 0)           # outward normal
        u0, u1, v0, v1 = f.ParameterRange
        for i in range(1, 12):
            for j in range(1, 12):
                p = f.valueAt(u0 + (u1 - u0) * i / 12.0, v0 + (v1 - v0) * j / 12.0)
                if not f.isInside(p, 1e-6, True):
                    continue
                # footprint corners and inward depth must be inside the face / material
                ok = True
                for dx in (-3, 3):
                    for dy in (-3, 3):
                        q = V(p.x + dx, p.y + dy, p.z)
                        if not f.isInside(q, 1e-6, True):
                            ok = False
                        qi = V(p.x + dx, p.y + dy, p.z - n.z * 5.5)
                        if not solid.isInside(qi, 1e-6, True):
                            ok = False
                        qo = V(p.x + dx, p.y + dy, p.z + n.z * 0.5)
                        if solid.isInside(qo, 1e-6, True):
                            ok = False
                if ok:
                    zlo = min(p.z, p.z - n.z * 5.0) - (5.0 if n.z > 0 else 0)
                    z0 = p.z - 5.0 if n.z > 0 else p.z - 5.0
                    # box spans z in [p.z-5, p.z+5] for either normal: 5 inside + 5 outside
                    box = Part.makeBox(5, 5, 10, V(p.x - 2.5, p.y - 2.5, p.z - 5.0))
                    return box, (p.x, p.y, p.z), n.z, f.Area
    return None

def mc_overlap(a, b, n=3000):
    bb = a.BoundBox
    cb = b.BoundBox
    lo = V(max(bb.XMin, cb.XMin), max(bb.YMin, cb.YMin), max(bb.ZMin, cb.ZMin))
    hi = V(min(bb.XMax, cb.XMax), min(bb.YMax, cb.YMax), min(bb.ZMax, cb.ZMax))
    vol = (hi.x - lo.x) * (hi.y - lo.y) * (hi.z - lo.z)
    k = 0
    for _ in range(n):
        p = V(random.uniform(lo.x, hi.x), random.uniform(lo.y, hi.y), random.uniform(lo.z, hi.z))
        if a.isInside(p, 1e-7, True) and b.isInside(p, 1e-7, True):
            k += 1
    pf = k / float(n)
    return vol * pf, vol * (pf * (1 - pf) / n) ** 0.5, vol

sh = objs("pose_Kd1_100p0")
base, nut = sh["base"], sh["nut"]
rec = max(base.Solids, key=lambda s: s.Volume)  # placeholder, reselected below
rec = [s for s in base.Solids if abs(s.Volume - 955593.2) < 1000][0]
plate = [s for s in base.Solids if s is not rec and abs(s.Volume - 4326428.1) < 1000][0]
out["validity"] = {"receiver_check": bopcheck(rec), "plate_check": bopcheck(plate), "nut_check": bopcheck(nut),
                   "receiver_isValid": rec.isValid(), "nut_isValid": nut.isValid()}
print("validity", out["validity"], flush=True)

ctl = {}
for name, solid, compound in (("receiver", rec, base), ("plate", plate, base), ("nut", nut, nut)):
    r = planar_straddle(solid, name)
    if r is None:
        ctl[name] = "no straddle site"
        continue
    box, p, nz, area = r
    c_solid = solid.common(box).Volume
    c_comp = compound.common(box).Volume
    try:
        cut_v = solid.cut(box).Volume
    except Exception as e:
        cut_v = str(e)[:80]
    ctl[name] = dict(site=[round(x, 3) for x in p], nz=nz, analytic=125.0, common_solid=round(c_solid, 4), common_via_compound=round(c_comp, 4),
                     cut_removed=(round(solid.Volume - cut_v, 4) if not isinstance(cut_v, str) else cut_v),
                     dist_box_to_solid=round(solid.distToShape(box)[0], 6))
    # box fully inside material
    print(name, ctl[name], flush=True)
out["planar_control"] = ctl

# distToShape control: sphere r=3 placed 7 mm outside a planar face
dctl = {}
for name, solid in (("receiver", rec), ("nut", nut)):
    r = planar_straddle(solid, name)
    if r is None:
        continue
    box, p, nz, area = r
    sph = Part.makeSphere(3.0, V(p[0], p[1], p[2] + nz * 7.0))
    dctl[name] = dict(analytic=4.0, measured=round(solid.distToShape(sph)[0], 6))
out["dist_control"] = dctl
print("dist", dctl, flush=True)

# thread-zone control: nut(Kd1) pure +z shift (no rotation) against receiver; common vs Monte Carlo
th = {}
for dz in (0.3, 1.0, 2.0):
    s = nut.copy()
    s.translate(V(0, 0, dz))
    c = rec.common(s).Volume
    cc = base.common(s).Volume
    chk = len(rec.common(s).Solids)
    est, se, bv = mc_overlap(rec, s, 3000)
    th[str(dz)] = dict(common=round(c, 2), common_compound=round(cc, 2), mc=round(est, 2), mc_se=round(se, 2), bboxvol=round(bv, 0))
    print("thread", dz, th[str(dz)], round(time.time() - t0), flush=True)
out["thread_control"] = th
# unshifted
out["thread_zero"] = dict(common=rec.common(nut).Volume, dist=rec.distToShape(nut)[0])
# inclusion-exclusion consistency at dz=1
s = nut.copy(); s.translate(V(0, 0, 1.0))
try:
    u = rec.fuse(s).Volume
    out["incl_excl_dz1"] = dict(Va=rec.Volume, Vb=s.Volume, Vunion=u, implied_common=rec.Volume + s.Volume - u, common=rec.common(s).Volume)
except Exception as e:
    out["incl_excl_dz1"] = str(e)[:100]
print("incl", out["incl_excl_dz1"], flush=True)
json.dump(out, open(os.path.join(ROOT, "research", "quinn", "cr_scratch", "step7_topo_boolctl.json"), "w"), indent=1)
print("secs", time.time() - t0)
print("BUILD_DONE")
