import sys, time
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\probes")
import probe_lib as L
import FreeCAD as App
C = L.C
p = L.params()
P = L.G(p, "thread.pitch")
z_run = L.G(p, "receiver.rim_above_floor") - L.G(p, "thread.run_turns") * P
z0 = z_run + P / 2.0 + 2 * P
rec = L.part("receiver")
def load(path):
    d = App.openDocument(path); s = C.final_shape(d.getObject("Body")); return s
nut_new = L.part("nut")
nut_old = load(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step7_before\nut.FCStd")
def pose(nut, phi, dz):
    s = nut.copy(); s.rotate(C.V(0, 0, 0), C.V(0, 0, 1), phi); s.translate(C.V(0, 0, z0 + dz)); return s
print("z0", z0, "rec vol", rec.Volume, "nut_new", nut_new.Volume, "nut_old", nut_old.Volume, flush=True)
for lab, nut in (("old", nut_old), ("new", nut_new)):
    for phi, dz in ((90.0, -2.0), (90.0, 0.0)):
        s = pose(nut, phi, dz)
        t = time.time()
        c = rec.common(s)
        cut = rec.cut(s)
        print(lab, phi, dz, "common", round(c.Volume, 4), "valid", c.isValid(), "viaCut", round(rec.Volume - cut.Volume, 4), "nut valid", s.isValid(), "t", round(time.time() - t, 1), flush=True)
print("DONE mesh_diag")
