import sys, time
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\probes")
import probe_lib as L
import FreeCAD as App
C = L.C
rec = L.part("receiver")
def load(path):
    d = App.openDocument(path); return C.final_shape(d.getObject("Body"))
new = L.part("nut"); old = load(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step7_before\nut.FCStd")
a = old.cut(new); b = new.cut(old)
print("old-new", round(a.Volume, 3), "new-old", round(b.Volume, 3), flush=True)
print("old bbox", old.BoundBox, "new bbox", new.BoundBox, flush=True)
bb = a.BoundBox; print("old-new bbox", bb, flush=True)
print("old com", old.CenterOfMass, "new com", new.CenterOfMass, flush=True)
print("DONE d2")
