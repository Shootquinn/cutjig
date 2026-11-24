import sys, time
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\probes")
import probe_lib as L
import FreeCAD as App, Part
C = L.C
p = L.params(); P = L.G(p, "thread.pitch")
z0 = L.G(p, "receiver.rim_above_floor") - L.G(p, "thread.run_turns") * P + P / 2.0 + 2 * P
rec = L.part("receiver"); new = L.part("nut")
def pose(n, phi, dz):
    s = n.copy(); s.rotate(C.V(0, 0, 0), C.V(0, 0, 1), phi); s.translate(C.V(0, 0, z0 + dz)); return s
def rep(lab, n):
    for phi, dz in ((90.0, -2.0), (90.0, 0.0), (90.0, 2.0)):
        s = pose(n, phi, dz)
        print(lab, phi, dz, "common", round(rec.common(s).Volume, 4), flush=True)
# 1 plain
rep("new", new)
# 2 trimmed to z < 41 (below the relief)
box = Part.makeBox(300, 300, 41.0, C.V(-150, -150, -10))
trim = new.common(box); print("trim vol", trim.Volume, "valid", trim.isValid(), flush=True)
rep("trim", trim)
# 3 nut halves: cut with a different split height 30
box2 = Part.makeBox(300, 300, 30.0, C.V(-150, -150, -10)); t2 = new.common(box2); rep("trim30", t2)
# 4 BOP check
try:
    from BOPTools import BOPFeatures
except Exception as e:
    print("no bop", e)
print("check:", new.check(True) if hasattr(new, "check") else "n/a", flush=True)
print("DONE d3")
