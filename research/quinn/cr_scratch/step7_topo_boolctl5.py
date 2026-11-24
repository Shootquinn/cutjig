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

def sface(s, z):
    ws = [w for w in s.slice(V(0, 0, 1), z) if w.isClosed()]
    fs = sorted([Part.Face(w) for w in ws], key=lambda f: -f.Area)
    f = fs[0]
    for g in fs[1:]:
        f = f.cut(g)
    return f
def simpson(f, a, b, n):
    h = (b - a) / n
    v = [f(a + h * i) for i in range(n + 1)]
    return h / 3 * (v[0] + v[-1] + 4 * sum(v[1:-1:2]) + 2 * sum(v[2:-1:2]))
out = {}
# thread x thread: nut shifted +dz in z against the receiver, overlap by 2D slice commons
for dz in (-1.0, -2.0):
    s2 = nut.copy(); s2.translate(V(0, 0, dz))
    za, zb = 90.0, 112.0   # inside receiver thread zone and nut z range [93.5+dz, 153.1+dz]
    t = time.time()
    c3 = rec.common(s2).Volume
    cl = Part.makeBox(400, 400, zb - za, V(-200, -200, za))
    c3slab = rec.common(s2).common(cl).Volume
    def ar(z):
        try:
            return sface(rec, z).common(sface(nut, z - dz)).Area
        except Exception as e:
            return 0.0
    integ = simpson(ar, za, zb, 88)
    out["thread_x_thread_%s" % dz] = dict(common_3d_full=round(c3, 3), common_3d_slab=round(c3slab, 3), slice_integral_slab=round(integ, 3), secs=round(time.time() - t, 1))
    print("tt", dz, out["thread_x_thread_%s" % dz], flush=True)
json.dump(out, open(os.path.join(ROOT, "research", "quinn", "cr_scratch", "step7_topo_boolctl5.json"), "w"), indent=1)
print("BUILD_DONE")
