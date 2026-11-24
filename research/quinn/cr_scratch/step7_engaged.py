import sys, json
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts")
import FreeCAD as App
import cadlib as C
R = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache"
p = C.params(); g = lambda k: C.G(p, k)
def load(n):
    d = App.openDocument(R + "/" + n + ".FCStd"); s = C.final_shape(d.getObject("Body")); App.closeDocument(d.Name); return s
nut, rec = load("nut"), load("receiver")
pitch = g("thread.pitch"); r_pitch = (g("thread.major") - g("chain.h")) / 2
def zone(sh, azs):
    lo = hi = None
    for t in azs:
        for a, b in C.axial_ivals(sh, t, r_pitch, sh.BoundBox.ZMin, sh.BoundBox.ZMax):
            if b - a < pitch:
                lo = a if lo is None else min(lo, a); hi = b if hi is None else max(hi, b)
    return (lo, hi)
azs = [30.0 * k for k in range(6)]
zr = zone(rec, azs)
out = {"receiver_zone": zr}
# nut zone depends on nut z0 only by translation; pose z0 from the L1 table (floor frame)
zn0 = zone(nut, azs)
out["nut_zone_local"] = zn0
for lab, z0, az in (("R", 62.371, 77.670), ("Kd1", 57.099, -159.571), ("Kmax", 50.010, -478.575)):
    n = nut.copy(); n.translate(C.V(0, 0, z0)); n.rotate(C.V(0, 0, 0), C.V(0, 0, 1), az)
    zn = zone(n, azs)
    out[lab] = {"z0": z0, "engaged_mm": round(max(0.0, min(zn[1], zr[1]) - max(zn[0], zr[0])), 3), "nut_zone": [round(zn[0], 3), round(zn[1], 3)]}
json.dump(out, open(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step7_engaged.json", "w"), indent=1)
print(json.dumps(out)); print("BUILD_DONE engaged")
