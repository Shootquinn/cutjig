import FreeCAD as App, collections
R = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
def load(path):
    d = App.openDocument(path)
    o = d.getObject("Body")
    sh = o.Shape.copy()
    if sh.ShapeType != "Solid" and len(sh.Solids) >= 1:
        sh = max(sh.Solids, key=lambda s: s.Volume)
    return sh
for lab, p in (("before", R + r"\research\quinn\cr_scratch\step7_before\nut.FCStd"), ("after", R + r"\parts_cache\nut.FCStd")):
    sh = load(p)
    h = collections.Counter(f.Surface.__class__.__name__ for f in sh.Faces)
    print(lab, "F", len(sh.Faces), "E", len(sh.Edges), "V", len(sh.Vertexes), "vol", round(sh.Volume, 3), dict(h), flush=True)
    # planar up/down faces at z=42 and z=48.5
    for f in sh.Faces:
        if f.Surface.__class__.__name__ == "Plane" and abs(f.BoundBox.ZMin - f.BoundBox.ZMax) < 1e-6 and abs(f.BoundBox.ZMin - 42.0) < 1e-3:
            print("  plane z42 area", round(f.Area, 2), "wires", len(f.Wires))
    ref = sh.removeSplitter()
    print("  removeSplitter F", len(ref.Faces), flush=True)
print("BUILD_DONE cmp")
