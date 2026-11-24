import sys
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\probes")
import probe_lib as L
import FreeCAD as App, Part
C = L.C
def load(path):
    d = App.openDocument(path); return C.final_shape(d.getObject("Body"))
new = L.part("nut"); old = load(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step7_before\nut.FCStd")
box = Part.makeBox(300, 300, 41.0, C.V(-150, -150, -10))
for lab, s in (("old", old), ("new", new)):
    try:
        s.check(True); r = "clean"
    except Exception as e:
        r = str(e)[:1500]
    print(lab, "check:", r.replace("\n", " | "), flush=True)
    t = s.common(box)
    print(lab, "common-with-box vol", round(t.Volume, 3), flush=True)
print("DONE bop")
