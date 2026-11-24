import sys
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts")
import cadlib as C
import FreeCAD as App
for n in ("holder", "nut", "core", "cutter"):
    d = App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\%s.FCStd" % n)
    sh = d.getObject("Body").Shape
    try:
        sh.check(True); r = "clean"
    except Exception as e:
        r = "FAULT " + str(e).replace(chr(10), " | ")[:200]
    print("BOP", n, r, flush=True)
d = App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\frame.FCStd")
bad = 0
for o in d.Objects:
    if o.Name.startswith(("member_", "bracket_", "tnut_")):
        try:
            o.Shape.check(True)
        except Exception:
            bad += 1
print("BOP frame objects with faults:", bad, "of", len([o for o in d.Objects if o.Name.startswith(("member_", "bracket_", "tnut_"))]), flush=True)
print("BUILD_DONE bop_all")
