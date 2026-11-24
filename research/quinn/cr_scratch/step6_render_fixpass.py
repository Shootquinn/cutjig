import sys, os, json, math, shutil, time, traceback, glob
import FreeCAD as App, Part
import FreeCADGui as Gui
if getattr(App, "_ran", False):
    sys.exit(0)
App._ran = True
V = App.Vector
BREP = r"C:\Users\Quinn Morley\AppData\Local\Temp\rend\brep"
FR = r"C:\Users\Quinn Morley\AppData\Local\Temp\rend\frames"
FINAL = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_renders"
LOG = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_render.log"
RES = r"C:\Users\Quinn Morley\AppData\Local\Temp\rend\results.json"
ONLY = os.environ.get("RONLY", "")
logf = open(LOG, "a" if ONLY else "w")
def log(s):
    logf.write(s + "\n"); logf.flush()
log("RENDER_START " + time.strftime("%H:%M:%S") + " only=" + ONLY)
Gui.showMainWindow()
import PySide6.QtWidgets as QW
BG = (0.80, 0.81, 0.83)
p = App.ParamGet("User parameter:BaseApp/Preferences/View")
p.SetBool("Gradient", False); p.SetBool("UseBackgroundColorMid", False)
bgi = (int(BG[0]*255) << 24) | (int(BG[1]*255) << 16) | (int(BG[2]*255) << 8)
for k in ("BackgroundColor", "BackgroundColor2", "BackgroundColor3", "BackgroundColor4"):
    p.SetUnsigned(k, bgi)
meta = json.load(open(os.path.join(BREP, "meta.json")))
doc = App.newDocument("R")
QW.QApplication.processEvents()
gdoc = Gui.getDocument("R")
view = gdoc.ActiveView
log("view=" + str(view))
try: view.setCameraType("Orthographic")
except Exception as e: log("camtype " + str(e))
try: view.setAxisCross(False)
except Exception: pass
try: Gui.getMainWindow().resize(1700, 1350)
except Exception: pass

def load(part, obj="Body"):
    return Part.read(os.path.join(BREP, "%s__%s.brep" % (part, obj)))

COL = {"receiver": (0.35,0.55,0.80), "holder": (0.85,0.55,0.20), "nut": (0.75,0.30,0.30), "washer": (0.10,0.55,0.60),
 "footring": (0.55,0.40,0.70), "base": (0.45,0.62,0.45), "tray": (0.30,0.65,0.75), "plug": (0.90,0.75,0.20), "foot": (0.55,0.55,0.35),
 "tnut": (0.95,0.50,0.10), "bracket_purchased": (0.30,0.30,0.35), "bracket_printed": (0.80,0.45,0.60), "frame": (0.62,0.66,0.70),
 "caddy": (0.60,0.50,0.35), "gauge": (0.40,0.70,0.55), "rest": (0.45,0.45,0.75), "stop": (0.75,0.35,0.55)}
COLLETC = {"090p0": (0.30,0.62,0.78), "097p5": (0.40,0.72,0.45), "105p0": (0.85,0.65,0.25)}

def clear():
    for o in list(doc.Objects):
        doc.removeObject(o.Name)

def add(shape, color, dev=0.15, name="o"):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    doc.recompute()
    vo = o.ViewObject
    vo.ShapeColor = color
    vo.DisplayMode = "Flat Lines"
    vo.LineColor = (0.05, 0.05, 0.05)
    vo.LineWidth = 1.0
    vo.Deviation = dev
    vo.AngularDeflection = 12
    vo.Visibility = True
    return o

def basis(d, up):
    d = V(*d); d.normalize()
    r = d.cross(V(*up))
    if r.Length < 1e-6: r = d.cross(V(0, 1, 0))
    r.normalize()
    u = r.cross(d); u.normalize()
    return d, r, u

def setcam(target, d, up, bb=None, height=None, margin=1.08):
    d, r, u = basis(d, up)
    target = V(*target)
    if height is None:
        cs = [V(x, y, z) for x in (bb.XMin, bb.XMax) for y in (bb.YMin, bb.YMax) for z in (bb.ZMin, bb.ZMax)]
        hu = [(c - target).dot(u) for c in cs]; hr = [(c - target).dot(r) for c in cs]
        eu = 2*max(abs(min(hu)), abs(max(hu))); er = 2*max(abs(min(hr)), abs(max(hr)))
        height = max(eu*margin, er*margin*1200/1600)
    dist = 3000.0
    pos = target - d*dist
    rot = App.Rotation(r, u, -d, "ZXY")
    ax = rot.Axis; ang = rot.Angle
    s = ("#Inventor V2.1 ascii\nOrthographicCamera { position %f %f %f orientation %f %f %f %f "
         "nearDistance 100 farDistance 6000 aspectRatio 1.3333 focalDistance %f height %f }" %
         (pos.x, pos.y, pos.z, ax.x, ax.y, ax.z, ang, dist, height))
    view.setCamera(s)

def shoot(name, bb=None, target=None, d=(-1,1,-1), up=(0,0,1), height=None, margin=1.08):
    if target is None:
        c = bb.Center; target = (c.x, c.y, c.z)
    setcam(target, d, up, bb, height, margin)
    for _ in range(3):
        QW.QApplication.processEvents(); time.sleep(0.2)
    tmp = os.path.join(FR, name + ".png")
    view.saveImage(tmp, 1600, 1200, "Current")
    QW.QApplication.processEvents()
    return tmp

def cov(path):
    from PIL import Image
    import numpy as np
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    bg = np.array([int(round(BG[0]*255)), int(round(BG[1]*255)), int(round(BG[2]*255))])
    diff = (abs(im - bg).sum(axis=2) > 12)
    return im.shape[1], im.shape[0], float(diff.mean())*100

RESULTS = []
def finish(name, tmp, part, view_desc, ids):
    try:
        w, h, c = cov(tmp)
        shutil.copyfile(tmp, os.path.join(FINAL, name + ".png"))
        RESULTS.append(dict(name=name, part=part, view=view_desc, ids=ids, w=w, h=h, cov=c))
        json.dump(RESULTS, open(RES if not ONLY else RES + ".test", "w"))
        log("OK %s %dx%d cov=%.1f" % (name, w, h, c))
    except Exception:
        log("FAIL %s %s" % (name, traceback.format_exc()))

def want(name):
    return (not ONLY) or any(k == name or (k.endswith("*") and name.startswith(k[:-1])) for k in ONLY.split(","))

def wantany(prefix):
    return (not ONLY) or any(k.startswith(prefix) or prefix.startswith(k.rstrip("*")) for k in ONLY.split(","))

def bbof(shapes):
    bb = None
    for s in shapes:
        bb = App.BoundBox(s.BoundBox) if bb is None else (bb.add(s.BoundBox) or bb)
    return bb

def scene(items, dev=0.15):
    clear()
    for i, (sh, col) in enumerate(items):
        add(sh, col, dev, "p%d" % i)
    return bbof([s for s, c in items])

def snap(name, part, desc, ids, **kw):
    if not want(name): return
    try:
        finish(name, shoot(name, **kw), part, desc, ids)
    except Exception:
        log("FAIL %s %s" % (name, traceback.format_exc()))

def local(sh, target, half):
    try:
        t = V(*target)
        box = Part.makeBox(2*half[0], 2*half[1], 2*half[2], V(t.x-half[0], t.y-half[1], t.z-half[2]))
        r = sh.common(box)
        if r.isNull() or r.Volume < 1.0: return sh
        return r
    except Exception:
        log("local failed " + traceback.format_exc().splitlines()[-1]); return sh

def halfcut(sh, point, n, size=1500):
    """remove the half-space on the n side of the plane through point"""
    try:
        n = V(*n); n.normalize()
        box = Part.makeBox(2*size, 2*size, size, V(-size, -size, 0))
        rot = App.Rotation(V(0, 0, 1), n)
        box.Placement = App.Placement(V(*point), rot)
        r = sh.cut(box)
        if r.isNull(): return sh
        return r
    except Exception:
        log("halfcut failed " + traceback.format_exc().splitlines()[-1]); return sh

STD = [("iso", (-1,1,-1), (0,0,1)), ("top", (0,0,-1), (0,1,0)), ("front", (0,1,0), (0,0,1))]
IDS = {"receiver": "RC1-RC6 AC4", "holder": "HD1-HD7 AC5", "nut": "NT1-NT8", "washer": "WS1-WS3", "footring": "CO foot ring seat",
       "base": "BS1-BS4", "tray": "BS5", "plug": "BS6", "foot": "BS7", "tnut": "FR3", "bracket_purchased": "FR2", "bracket_printed": "FR2",
       "caddy": "AC1", "gauge": "AC2", "rest": "AC3", "stop": "ST1"}

def run(fn):
    try: fn()
    except Exception: log("FAIL-JOB %s %s" % (fn.__name__, traceback.format_exc()))

def std_part(part, shape=None, col=None, ids=None, dev=0.15, tag=None):
    tag = tag or part
    if not any(want("%s_%s" % (tag, v[0])) for v in STD): return
    sh = shape if shape is not None else load(part)
    bb = scene([(sh, col or COL[part])], dev)
    for vn, d, up in STD:
        snap("%s_%s" % (tag, vn), tag, vn, ids or IDS[part], bb=bb, d=d, up=up)

def job_parts():
    for part in ["washer","footring","receiver","holder","nut","base","tray","plug","foot","tnut","bracket_purchased","bracket_printed","caddy","gauge","rest","stop"]:
        std_part(part)
run(job_parts)

def job_extra_views():
    if want("base_bottom"):
        sh = load("base"); bb = scene([(sh, COL["base"])])
        snap("base_bottom", "base", "underside, key and pin pockets", "BS4", bb=bb, d=(0,0,1), up=(0,1,0))
    if want("rest_bottom"):
        sh = load("rest"); bb = scene([(sh, COL["rest"])])
        snap("rest_bottom", "rest", "from below, radial pin slots in the ring", "AC3", bb=bb, d=(0,0,1), up=(0,1,0))
    if want("rest_slot_closeup"):
        sh = load("rest"); cut = halfcut(sh, (0, 0, 17.0), (0, 0, 1)); scene([(cut, COL["rest"])], 0.1)
        snap("rest_slot_closeup", "rest", "section at z 17 (1.5 above the ring bottom) viewed from above: radial pin slot at azimuth 0 with the roller pin at the pose radius", "AC3", target=(68, 0, 17), d=(0.0, 0.0, -1.0), up=(0,1,0), height=50)
    if want("rest_iso_back"):
        sh = load("rest"); bb = scene([(sh, COL["rest"])])
        snap("rest_iso_back", "rest", "iso from the opposite corner", "AC3", bb=bb, d=(1,-1,-1), up=(0,0,1))
    if want("receiver_bottom") or want("nut_bottom") or want("holder_bottom"):
        for part, ids in (("receiver", "RC3 RC4"), ("nut", "NT2 NT5 NT7"), ("holder", "HD5 HD6 HD7")):
            nm = part + "_bottom"
            if want(nm):
                sh = load(part); bb = scene([(sh, COL[part])])
                snap(nm, part, "from below", ids, bb=bb, d=(0,0,1), up=(0,1,0))
run(job_extra_views)

def job_collets():
    for sz, c in COLLETC.items():
        n = "collet_" + sz
        if not wantany(n): continue
        sh = load(n)
        bb = scene([(sh, c)], 0.1)
        snap(n + "_iso", n, "iso", "CO1-CO8", bb=bb, d=(-1,1,-1), up=(0,0,1))
        snap(n + "_top", n, "top", "CO3 CO5 CO7", bb=bb, d=(0,0,-1), up=(0,1,0))
        if want(n + "_section"):
            a = meta[n][0]
            ar = math.radians(a)
            nrm = (-math.sin(ar), math.cos(ar), 0)
            cut = halfcut(sh, (0, 0, 0), nrm)
            bb2 = scene([(cut, c)], 0.1)
            snap(n + "_section", n, "section through slit plane az %.0f deg, viewed from the cut side" % a, "CO3 CO4 CO2",
                 bb=bb2, d=(-nrm[0], -nrm[1], 0), up=(0,0,1))
run(job_collets)

def surf_z(sh, x, y, z0=-60, z1=200):
    ln = Part.makeLine(V(x, y, z0), V(x, y, z1))
    c = sh.common(ln)
    if not c.Edges: return (None, None)
    return (min(e.BoundBox.ZMin for e in c.Edges), max(e.BoundBox.ZMax for e in c.Edges))

XG = (95.14 + 0.5 + 115.0 - 6.0) / 2.0          # glyph centre: nut.skirt_r_out + 0.5 to wing tip - edge_radius

def job_nut():
    names = ["nut_top","nut_bottom","nut_wing0_top","nut_wing0_under","nut_glyph_nt4_top","nut_glyph_nt4_oblique","nut_glyph_nt5_under","nut_glyph_nt5_oblique","nut_skirt_below","nut_skirt_section"]
    if not any(want(n) for n in names): return
    nut = load("nut")
    ang = math.radians(35)
    # glyph surface normals
    xg = XG
    zb0, zt0 = surf_z(nut, xg, 5.0); zb1, zt1 = surf_z(nut, xg + 6, 5.0)
    log("nut z at y7.5: x%.2f bot %s top %s ; x%.2f bot %s top %s" % (xg, zb0, zt0, xg+6, zb1, zt1))
    ft = (zt1 - zt0)/6.0; fb = (zb1 - zb0)/6.0
    ntop = V(-ft, 0, 1); ntop.normalize()
    nbot = V(fb, 0, -1); nbot.normalize()
    bbn = scene([(nut, COL["nut"])], 0.12)
    snap("nut_top", "nut", "top, wing 0 at +X carries the NT4 tighten glyph", "NT4 NT1-NT3 NT6", bb=bbn, d=(0,0,-1), up=(0,1,0))
    snap("nut_bottom", "nut", "from below, wing 0 underside carries the NT5 loosen glyph, dust skirt", "NT5 NT7 NT8", bb=bbn, d=(0,0,1), up=(0,1,0))
    snap("nut_wing0_top", "nut", "wing 0 top face, NT4 glyph, normal to face", "NT4", target=(XG, 0, zt0), d=(-ntop.x, -ntop.y, -ntop.z), up=(0,1,0), height=70)
    snap("nut_wing0_under", "nut", "wing 0 underside, NT5 glyph, normal to face", "NT5", target=(XG, 0, zb0), d=(-nbot.x, -nbot.y, -nbot.z), up=(0,1,0), height=70)
    # local solids for glyph close-ups
    if any(want(n) for n in names[4:8]):
        loc = local(nut, (XG, 0, (zt0 + zb0)/2), (22, 22, 22))
        scene([(loc, COL["nut"])], 0.2)
        for nm, n, z, desc, idn in (("nut_glyph_nt4_top", ntop, zt0, "NT4 tighten glyph, normal to face, +Y up, clockwise from +Z", "NT4"),
                                    ("nut_glyph_nt5_under", nbot, zb0, "NT5 loosen glyph, seen from below along +Z, +Y up", "NT5")):
            snap(nm, "nut", desc, idn, target=(XG, 0, z), d=(-n.x, -n.y, -n.z), up=(0,1,0), height=16)
            dd = V(-n.x, -n.y, -n.z)*math.cos(ang) + V(0, 1, 0)*math.sin(ang)
            snap(nm.replace("_top", "_oblique").replace("_under", "_oblique"), "nut", desc.split(",")[0] + ", oblique 35 deg from -Y for recess walls", idn,
                 target=(XG, 0, z), d=(dd.x, dd.y, dd.z), up=(0,0,1) if abs(dd.z) < 0.99 else (0,1,0), height=16)
    if want("nut_skirt_below"):
        bb = scene([(nut, COL["nut"])], 0.12)
        snap("nut_skirt_below", "nut", "dust skirt from below and outside, -Y side", "NT7", target=(0, -88, 8), d=(0, 0.6, 0.8), up=(0,0,1), height=90)
    if want("nut_skirt_section"):
        cut = halfcut(nut, (0, 0, 0), (1, 0, 0))
        scene([(cut, COL["nut"])], 0.1)
        snap("nut_skirt_section", "nut", "section at x=0, skirt profile on the -Y side, viewed from +X", "NT7", target=(0, -88, 8), d=(-1, 0, 0), up=(0,0,1), height=50)
run(job_nut)

RAZ = math.radians(127.0)
RC, RS = math.cos(RAZ), math.sin(RAZ)

def job_receiver_holder():
    if any(want(n) for n in ("receiver_rim_scale_closeup", "receiver_rim_scale_oblique", "receiver_rim_scale_context")):
        rec = load("receiver")
        r_t = (72.0*RC, 72.0*RS, 56.0)
        scene([(local(rec, r_t, (32, 32, 22)), COL["receiver"])], 0.1)
        snap("receiver_rim_scale_closeup", "receiver", "RC6 ruler at az 127 deg, radial view, z 44 to 68", "RC6 AC4", target=r_t, d=(-RC, -RS, 0), up=(0,0,1), height=26)
        dd = V(-RC, -RS, 0)*math.cos(math.radians(30)) + V(-RS, RC, 0)*math.sin(math.radians(30))
        snap("receiver_rim_scale_oblique", "receiver", "RC6 ruler, oblique 30 deg about the axis", "RC6 AC4", target=r_t, d=(dd.x, dd.y, dd.z), up=(0,0,1), height=26)
        bb = scene([(rec, COL["receiver"])], 0.1)
        snap("receiver_rim_scale_context", "receiver", "RC6 ruler in context, whole upper receiver, radial view at az 127", "RC6 RC5 RC1", target=(0, 0, 60), d=(-RC, -RS, 0), up=(0,0,1), height=130)
    if any(want(n) for n in ("holder_tick_closeup", "holder_tick_below", "holder_tick_oblique")):
        hol = load("holder")
        h_t = (72.0*RC, 72.0*RS, 90.0)
        scene([(local(hol, h_t, (25, 25, 14)), COL["holder"])], 0.08)
        snap("holder_tick_closeup", "holder", "HD7 tick at az 127 deg on the flange rim, radial view", "HD7 AC5", target=h_t, d=(-RC, -RS, 0), up=(0,0,1), height=16)
        snap("holder_tick_below", "holder", "HD7 tick from below, flange underside, radial up", "HD7 HD5 HD6", target=h_t, d=(0, 0, 1), up=(RC, RS, 0), height=22)
        dd = V(-RC, -RS, 0)*math.cos(math.radians(40)) + V(0, 0, 1)*math.sin(math.radians(40))
        snap("holder_tick_oblique", "holder", "HD7 tick, oblique from below and outside", "HD7", target=h_t, d=(dd.x, dd.y, dd.z), up=(0,0,1), height=18)
run(job_receiver_holder)

def job_witness():
    names = [a % k for k in ("Kmax", "Kd1") for a in ("witness_%s_view", "witness_%s_section", "witness_%s_closeup")]
    if not any(want(n) for n in names): return
    rec = load("receiver"); hol = load("holder"); nut = load("nut")
    for tag, edge in (("Kmax", 50.00), ("Kd1", 57.09)):
        if not any(want(n) for n in ("witness_%s_view" % tag, "witness_%s_section" % tag, "witness_%s_closeup" % tag)): continue
        h = hol.copy(); h.translate(V(0, 0, edge + 40.0 - 88.0))
        n = nut.copy(); n.translate(V(0, 0, edge))
        items = [(rec, COL["receiver"]), (h, COL["holder"]), (n, COL["nut"])]
        scene(items, 0.1)
        eye = (0, 0, 62)
        snap("witness_%s_view" % tag, "witness", "receiver, holder, nut at %s: edge %.2f, horizontal line of sight at az 127" % (tag, edge), "RC6 HD7 NT7 NT9",
             target=eye, d=(-RC, -RS, 0), up=(0,0,1), height=190)
        pr = (72.0*RC, 72.0*RS, edge + 2)
        snap("witness_%s_closeup" % tag, "witness", "line of sight close-up, skirt bottom against ruler graduations, eye level", "RC6 HD7 NT7 NT9",
             target=pr, d=(-RC, -RS, 0), up=(0,0,1), height=40)
        if want("witness_%s_section" % tag):
            nrm = (-RS, RC, 0)
            ci = [(halfcut(s, (0, 0, 0), nrm), c) for s, c in items]
            scene(ci, 0.1)
            snap("witness_%s_section" % tag, "witness", "section through the axis at az 127, ruler and skirt profile, viewed from the cut side", "RC6 HD7 NT7 NT9",
                 target=(75.0*RC, 75.0*RS, edge + 5), d=(RS, -RC, 0), up=(0,0,1), height=70)
run(job_witness)

def job_base():
    if not (wantany("base_tray") or wantany("tray_") or wantany("base_slots") or wantany("tray_relief")): return
    base = load("base"); tray = load("tray"); plug = load("plug")
    items = [(base, COL["base"]), (tray, COL["tray"]), (plug, COL["plug"])]
    bb = scene(items, 0.15)
    snap("base_tray_iso", "base+tray+plug", "iso, base with tray and drain plug", "BS1 BS5 BS6", bb=bb, d=(-1,1,-1), up=(0,0,1))
    snap("base_tray_top", "base+tray+plug", "top, tray ramp, drain, reliefs, slots", "BS2-BS6", bb=bb, d=(0,0,-1), up=(0,1,0))
    snap("base_tray_front", "base+tray+plug", "front", "BS1 BS5", bb=bb, d=(0,1,0), up=(0,0,1))
    snap("base_tray_drain_top", "base+tray+plug", "drain and plug close-up, top", "BS2 BS6", target=(-172, 0, 20), d=(0,0,-1), up=(0,1,0), height=90)
    snap("base_tray_relief_closeup", "base+tray+plug", "column relief at +Y edge, top oblique", "BS5 BS4", target=(0, 262, 25), d=(-0.3,0.6,-0.8), up=(0,0,1), height=150)
    snap("base_slots_closeup", "base", "slotted mounting holes at +Y edge, key pocket and column notch region, top", "BS3 BS4", target=(-170, 280, 12), d=(0,0,-1), up=(0,1,0), height=130)
    if want("base_tray_section") or want("base_tray_drain_section"):
        ci = [(halfcut(s, (0, 0, 0), (0, -1, 0)), c) for s, c in items]
        bb2 = scene(ci, 0.15)
        snap("base_tray_section", "base+tray+plug", "section at y=0 viewed from -Y: ramp rise, cavity, drain bore, plug", "BS5 BS6 BS2", bb=bb2, d=(0,1,0), up=(0,0,1))
        snap("base_tray_drain_section", "base+tray+plug", "section at y=0, drain and plug close-up", "BS6 BS2", target=(-172, 0, 22), d=(0,1,0), up=(0,0,1), height=70)
    if want("base_slots_closeup_iso"):
        scene([(base, COL["base"])], 0.12)
        snap("base_slots_closeup_iso", "base", "mounting slots and column notch, oblique", "BS3 BS4", target=(-170, 285, 12), d=(0.3,-0.6,-0.8), up=(0,0,1), height=130)
run(job_base)

def job_tray():
    if want("tray_ramp_section"):
        tray = load("tray")
        cut = halfcut(tray, (0, 0, 0), (0, -1, 0))
        bb = scene([(cut, COL["tray"])], 0.1)
        snap("tray_ramp_section", "tray", "section at y=0 viewed from -Y: floor falls to the drain both ways, x -277 to 277", "BS5", bb=bb, d=(0,1,0), up=(0,0,1))
    if want("tray_cross_section"):
        tray = load("tray")
        cut = halfcut(tray, (-172, 0, 0), (-1, 0, 0))
        bb = scene([(cut, COL["tray"])], 0.1)
        snap("tray_cross_section", "tray", "section at the drain x = -172 viewed from -X: cross fall to the drain, y -257 to 257", "BS5", bb=bb, d=(1,0,0), up=(0,0,1))
run(job_tray)

def job_frame():
    if not wantany("frame_"): return
    items = []
    for f in sorted(glob.glob(os.path.join(BREP, "frame__*.brep"))):
        on = os.path.basename(f)[7:-5]
        sh = Part.read(f)
        if on.startswith("member_"): c = (0.62, 0.66, 0.70)
        elif on.startswith("bracket_purchased"): c = (0.25, 0.25, 0.30)
        elif on.startswith("bracket_printed"): c = (0.85, 0.40, 0.55)
        else: c = (0.97, 0.55, 0.05)
        items.append((sh, c))
    bb = scene(items, 0.2)
    for vn, d, up in STD:
        snap("frame_" + vn, "frame", vn + " (members grey, purchased brackets black, printed brackets pink, T-nut proxies orange)", "FR1 FR2 FR3", bb=bb, d=d, up=up)
    snap("frame_bottom", "frame", "from below", "FR1 FR2 FR3", bb=bb, d=(0,0,1), up=(0,1,0))
    snap("frame_brackets_closeup", "frame", "brackets and T-nuts, corner +X +Y, iso close-up", "FR2 FR3", target=(190, 225, -30), d=(-0.9, 0.9, -0.9), up=(0,0,1), height=190)
    snap("frame_brackets_closeup_under", "frame", "brackets and T-nuts, corner +X +Y, from below", "FR2 FR3", target=(190, 225, -30), d=(-0.8, 0.8, 0.9), up=(0,0,1), height=190)
    snap("frame_notch_top", "frame", "FR4 datum C notch, rail_1, top close-up", "FR4", target=(-307, 259, 0), d=(0,0,-1), up=(0,1,0), height=60)
    snap("frame_notch_iso", "frame", "FR4 datum C notch, rail_1, oblique close-up", "FR4", target=(-307, 259, 0), d=(-0.7, 0.5, -0.7), up=(0,0,1), height=70)
run(job_frame)

def job_frame_tnuts():
    if not want("frame_tnuts_closeup"): return
    items = []
    for f in sorted(glob.glob(os.path.join(BREP, "frame__*.brep"))):
        on = os.path.basename(f)[7:-5]
        if on.startswith("member_"): continue
        sh = Part.read(f)
        if on.startswith("bracket_purchased"): c = (0.25, 0.25, 0.30)
        elif on.startswith("bracket_printed"): c = (0.85, 0.40, 0.55)
        else: c = (0.97, 0.55, 0.05)
        items.append((sh, c))
    scene(items, 0.2)
    snap("frame_tnuts_closeup", "frame", "brackets and T-nut proxies only (members hidden), corner +X +Y, iso", "FR2 FR3", target=(190, 225, -30), d=(-0.9, 0.9, -0.9), up=(0,0,1), height=190)
run(job_frame_tnuts)

log("RENDER_DONE")
logf.close()
sys.stdout.flush()
os._exit(0)
