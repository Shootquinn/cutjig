import sys
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\probes")
import probe_lib as L
import FreeCAD as App, Part
C = L.C
d = App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step7_before\nut.FCStd")
old = C.final_shape(d.getObject("Body"))
box = Part.makeBox(300, 300, 41.0, C.V(-150, -150, -10))
def clean(s):
    try:
        s.check(True); return True
    except Exception:
        return False
for zlo in (42.0, 41.9, 42.1, 41.75, 42.3, 41.0):
    for r in (75.34, 75.5):
        cyl = Part.makeCylinder(r, 48.5 - zlo, C.V(0, 0, zlo), C.V(0, 0, 1))
        s = old.cut(cyl)
        t = s.common(box)
        print("z", zlo, "r", r, "vol", round(s.Volume, 3), "valid", s.isValid(), "bop", clean(s), "boxcommon", round(t.Volume, 1), "F", len(s.Faces), flush=True)
print("DONE trial")
