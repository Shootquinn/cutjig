import sys
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts")
import FreeCAD as App
import cadlib as C
p = C.params()
g = lambda k: C.G(p, k)
d = App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\receiver.FCStd")
sh = C.final_shape(d.getObject("Body"))
az = g("witness.azimuth_deg")
r_rim = g("thread.major") / 2 - 1.0
for a in (az + 120.0, az - 120.0, az, 0.0, 90.0, 180.0, 270.0):
    iv = C.axial_ivals(sh, a, r_rim, 0.0, 200.0)
    print("RIM", a % 360, round(r_rim, 3), [(round(x, 3), round(y, 3)) for x, y in iv[-2:]], flush=True)
print("DIAG_DONE", flush=True)
