import FreeCAD as App, Part, json, os, time
V = App.Vector
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
d = App.openDocument(os.path.join(ROOT, "parts_cache", "assembly", "pose_Kd1_100p0.FCStd"))
sh = {o.Label: o.Shape.copy() for o in d.Objects if hasattr(o, "Shape") and o.Shape.Solids}
base, nut = sh["base"], sh["nut"]
rec = [s for s in base.Solids if abs(s.Volume - 955593.2) < 1000][0]
def area_at(s, z):
    ws = s.slice(V(0, 0, 1), z)
    fs = []
    for w in ws:
        if w.isClosed():
            fs.append(abs(Part.Face(w).Area))
    fs.sort(reverse=True)
    return fs[0] - sum(fs[1:]) if fs else 0.0, len(fs)
out = {}
t0 = time.time()
for name, s, z0, z1 in (("receiver", rec, None, None), ("nut", nut, None, None)):
    bb = s.BoundBox
    za = bb.ZMin + 0.3 * bb.ZLength
    zb = za + 16.0   # two pitches
    n = 64
    A = [area_at(s, za + (zb - za) * i / n)[0] for i in range(n + 1)]
    h = (zb - za) / n
    simp = h / 3 * (A[0] + A[-1] + 4 * sum(A[1:-1:2]) + 2 * sum(A[2:-1:2]))
    slab = Part.makeBox(2 * bb.XLength, 2 * bb.YLength, zb - za, V(bb.XMin - bb.XLength / 2, bb.YMin - bb.YLength / 2, za))
    t = time.time()
    c = s.common(slab).Volume
    cc = (base if name == "receiver" else nut).common(slab).Volume
    out[name] = dict(z=[round(za, 3), round(zb, 3)], slice_integral=round(simp, 2), common=round(c, 2), common_compound=round(cc, 2),
                     rel_err=round((c - simp) / simp, 6), secs=round(time.time() - t, 1), checkA=A[:3])
    print(name, out[name], flush=True)
# receiver cylinder intruding into the threaded wall: tube r in [r1,r2] over slab; compare slice integral of annulus-clipped area via common of slice faces
json.dump(out, open(os.path.join(ROOT, "research", "quinn", "cr_scratch", "step7_topo_boolctl2.json"), "w"), indent=1)
print("secs", time.time() - t0); print("BUILD_DONE")
