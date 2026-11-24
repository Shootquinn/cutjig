"""Pass 1 interference and clearance data from the built solids (read only)."""
import sys
sys.path.insert(0, "C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/build_parts")
import FreeCAD as App
import Part
import cadlib as C
import step6lib as S
p = C.params()
g = lambda k: C.G(p, k)
CACHE = "C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/parts_cache/"


def load(name):
    d = App.openDocument(CACHE + name + ".FCStd")
    sh = C.final_shape(d.getObject("Body"))
    App.closeDocument(d.Name)
    return sh


nut, tray, rest, caddy, base = load("nut"), load("tray"), load("rest"), load("caddy"), load("base")
rec = load("receiver")
plug = load("plug")
floor_a = g("icd.floor_above_datum_a")
# nut at K-max: skirt bottom at receiver-floor-frame z = holder.bottom_above_floor_Kmax ... use Loftsman: skirt bottom 55.0 above the floor top
z_nut = 55.0 + floor_a
n = nut.copy()
n.translate(C.V(0, 0, z_nut))
print("P1 nut skirt bottom z (datum A) %.2f, dust skirt bottom %.2f, tray rim z %.2f" % (z_nut, z_nut + g("nut.skirt_z_lo"), tray.BoundBox.ZMax), flush=True)
print("P1 nut-to-tray min distance %.3f, common %.4f" % (n.distToShape(tray)[0], n.common(tray).Volume), flush=True)
print("P1 nut-to-plug min distance %.3f" % n.distToShape(plug)[0], flush=True)
# receiver in the base: receiver bottom at datum A (z = 0): shift by floor_above
r = rec.copy()
r.translate(C.V(0, 0, floor_a))
print("P1 receiver-to-base common %.4f, receiver-to-tray common %.4f, dist base %.3f tray %.3f" % (r.common(base).Volume, r.common(tray).Volume, r.distToShape(base)[0], r.distToShape(tray)[0]), flush=True)
# collet in caddy socket
import glob
worst = 0
for f in sorted(glob.glob(CACHE + "collet_*[0-9]p[0-9].FCStd")):
    d = App.openDocument(f)
    cs = None
    for o in d.Objects:
        if hasattr(o, "Shape") and o.Shape.Solids:
            cs = C.final_shape(o)
    bb = cs.BoundBox
    rmax = max(abs(bb.XMin), abs(bb.XMax), abs(bb.YMin), abs(bb.YMax))
    print("P1 collet %s bbox x %.2f y %.2f z %.2f half-diagonal-free max r %.2f" % (f.split("/")[-1], bb.XLength, bb.YLength, bb.ZLength, rmax), flush=True)
    worst = max(worst, max(bb.XLength, bb.YLength) / 2, 0)
    App.closeDocument(d.Name)
r_sock = (S.Rec("x"), None)
print("P1 socket radius %.2f, socket depth %.2f, widest collet half-extent %.2f" % (g("receiver.register_bore_radius") - g("register.g_reg") + g("holder.key_height") + g("caddy.socket_clear"), g("caddy.socket_depth"), worst), flush=True)
# rest rollers against cores
core_h = 200.0
for d_ in g("core.diameters"):
    core = Part.makeCylinder(d_ / 2, core_h, C.V(0, 0, -core_h / 2), C.V(0, 0, 1))
    v = rest.common(core).Volume
    print("P1 rest-vs-core d %.1f: interference %.2f mm3, min distance %.3f" % (d_, v, rest.distToShape(core)[0]), flush=True)
# rest tower and keepout
kc = Part.makeCylinder(g("icd.keepout_radius"), g("rest.height_positions")[1], C.V(0, 0, -g("rest.height_positions")[1] / 2), C.V(0, 0, 1))
print("P1 rest-vs-keepout r %.1f: common %.1f mm3" % (g("icd.keepout_radius"), rest.common(kc).Volume), flush=True)
tube = Part.makeCylinder(g("drill.tube_od") / 2, 500, C.V(0, 0, -250), C.V(0, 0, 1))
print("P1 rest-vs-tube r %.1f: min distance %.3f" % (g("drill.tube_od") / 2, rest.distToShape(tube)[0]), flush=True)
print("P1_DONE", flush=True)
