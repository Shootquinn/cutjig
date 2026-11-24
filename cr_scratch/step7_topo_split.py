import FreeCAD as App, json, os
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
PC = os.path.join(ROOT, "parts_cache")
res = {}

def coplanar_pairs(s):
    pl = []
    for i, f in enumerate(s.Faces):
        try:
            if f.Surface.__class__.__name__ == "Plane":
                n = f.normalAt(0, 0)
                p = f.Surface.Position
                d = n.dot(p)
                pl.append((i, n, d, f))
        except Exception:
            pass
    pairs = []
    for a in range(len(pl)):
        for b in range(a + 1, len(pl)):
            ia, na, da, fa = pl[a]; ib, nb, db, fb = pl[b]
            if na.dot(nb) > 0.99999 and abs(da - db) < 1e-6:
                # share an edge?
                ea = set(e.hashCode() for e in fa.Edges)
                if any(e.hashCode() in ea for e in fb.Edges):
                    pairs.append((ia, ib, round(da, 3)))
    return pairs, len(pl)

def planes_at(s, z):
    out = []
    for f in s.Faces:
        if f.Surface.__class__.__name__ == "Plane":
            n = f.normalAt(0, 0)
            if abs(abs(n.z) - 1) < 1e-9 and abs(f.Surface.Position.z - z) < 1e-6:
                out.append((round(n.z), round(f.Area, 3), len(f.Wires)))
    return out

for name, objn in (("holder", "NotchInsertsTick"), ("nut", "WindowsHolesGlyphs"), ("core", "Body"), ("cutter", "Body"), ("frame", "member_rail_1"), ("frame", "member_end_1")):
    d = App.openDocument(os.path.join(PC, name + ".FCStd"))
    s = d.getObject(objn).Shape
    pairs, npl = coplanar_pairs(s)
    r = dict(planar=npl, coplanar_adjacent=pairs)
    if name == "holder":
        r["z104.75"] = planes_at(s, 104.75)
        r["z110.75"] = planes_at(s, 110.75)
    if name == "nut":
        r["z42"] = planes_at(s, 42.0)
        r["z48.5"] = planes_at(s, 48.5)
    res[name + ":" + objn] = r
    App.closeDocument(d.Name)
json.dump(res, open(os.path.join(ROOT, "cr_scratch", "step7_topo_split.json"), "w"), indent=1)
print("BUILD_DONE")
