import sys, os, json, math, time, traceback
import FreeCAD as App, Part, Mesh
import FreeCADGui as Gui
if getattr(App, "_ran", False):
    sys.exit(0)
App._ran = True
V = App.Vector
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
ASM = ROOT + r"\parts_cache\assembly\pose_%s.FCStd"
JIG = ROOT + r"\output\jig_assembly.FCStd"
OUT = ROOT + r"\cr_scratch\step7_video"
FR = OUT + r"\frames"
LOG = ROOT + r"\cr_scratch\step7_video.log"
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    if f.endswith(".png"): os.remove(os.path.join(FR, f))
logf = open(LOG, "w")
def log(s):
    logf.write(s + "\n"); logf.flush()
log("VIDEO_START " + time.strftime("%H:%M:%S"))
W, H = 1280, 720
FPS = 30
LIMIT = int(os.environ.get("VLIMIT", "0"))      # smoke test: frames per segment

# ---------- shapes, read only ----------
P = {}
for tag in ("R_100p0", "Kd1_100p0", "Kmax_100p0"):
    d = App.openDocument(ASM % tag)
    P[tag] = {o.Name: o.Shape.copy() for o in d.Objects if hasattr(o, "Shape") and not o.Shape.isNull()}
    App.closeDocument(d.Name)
d = App.openDocument(JIG)
J = {o.Name: o.Shape.copy() for o in d.Objects if hasattr(o, "Shape") and not o.Shape.isNull()}
App.closeDocument(d.Name)
LED = json.load(open(ROOT + r"\results\assembly_poses.json"))["sizes"]["100p0"]
PHI = {k: LED[k]["phi_deg"] for k in ("R", "Kd1", "Kmax")}
DZ = {k: LED[k]["dz_mm"] for k in ("R", "Kd1", "Kmax")}
LEAD = json.load(open(ROOT + r"\results\assembly_poses.json"))["lead_mm"]
log("LEDGER phi %s dz %s lead %s" % (PHI, DZ, LEAD))
import yaml
PRM = yaml.safe_load(open(ROOT + r"\params.yaml", encoding="utf-8"))
def pv(sec, key):
    v = PRM[sec][key]
    return v["value"] if isinstance(v, dict) and "value" in v else v
CORE_D = pv("core", "diameters"); COLLET_NAMES = pv("collet", "colour")
RGB = {"red": (0.88,0.12,0.12), "orange": (0.95,0.55,0.10), "yellow": (0.95,0.85,0.15), "green": (0.20,0.68,0.28),
       "blue": (0.15,0.35,0.88), "violet": (0.55,0.28,0.75), "white": (0.98,0.98,0.98)}
COLLET_RGB = RGB[COLLET_NAMES[min(range(len(CORE_D)), key=lambda k: abs(CORE_D[k] - 100.0))]]

def split_base(pose):
    s = sorted(P[pose]["base"].Solids, key=lambda s: s.Volume)
    return s[0], s[1]
def split_bracket(pose):
    sols = P[pose]["bracket"].Solids
    return [s for i, s in enumerate(sols) if i not in (4, 5, 6, 7)], [sols[i] for i in (4, 5, 6, 7)]

# witness: flange gap measured from the Kmax pose
rec_k, plate_k = split_base("Kmax_100p0")
hol_k = P["Kmax_100p0"]["holder"]
best = None; rim = None
for f in hol_k.Faces:
    try:
        if f.Surface.__class__.__name__ == "Plane" and abs(f.normalAt(0, 0).z + 1) < 1e-6 and 100 < f.BoundBox.ZMin < 140 and f.Area > 1000:
            best = f.BoundBox.ZMin if best is None else min(best, f.BoundBox.ZMin)
    except Exception: pass
for f in rec_k.Faces:
    try:
        if f.Surface.__class__.__name__ == "Plane" and abs(f.normalAt(0, 0).z - 1) < 1e-6 and f.BoundBox.ZMin > 120 and f.Area > 50:
            rim = f.BoundBox.ZMin if rim is None else max(rim, f.BoundBox.ZMin)
    except Exception: pass
GAP = (best - rim) if (best is not None and rim is not None) else None
log("WITNESS holder flange underside z %s receiver rim face z %s gap %s" % (best, rim, GAP))
GAPTXT = ("%.1f" % GAP) if GAP is not None else "n/a"

# ---------- GUI ----------
DARK = (60/255.0, 60/255.0, 65/255.0)
p = App.ParamGet("User parameter:BaseApp/Preferences/View")
p.SetBool("Gradient", False); p.SetBool("UseBackgroundColorMid", False)
bgi = (int(DARK[0]*255) << 24) | (int(DARK[1]*255) << 16) | (int(DARK[2]*255) << 8)
for k in ("BackgroundColor", "BackgroundColor2", "BackgroundColor3", "BackgroundColor4"):
    p.SetUnsigned(k, bgi)
Gui.showMainWindow()
import PySide6.QtWidgets as QW
doc = App.newDocument("V7")
QW.QApplication.processEvents()
gdoc = Gui.getDocument("V7")
view = gdoc.ActiveView
try: view.setCameraType("Orthographic")
except Exception as e: log("camtype " + str(e))
try: view.setAxisCross(False)
except Exception: pass
try: Gui.getMainWindow().resize(1700, 1350)
except Exception: pass

COL = dict(plate=(0.45,0.62,0.45), receiver=(0.35,0.55,0.80), holder=(0.85,0.55,0.20), nut=(0.75,0.30,0.30), washer=(0.10,0.55,0.60),
           core=(0.50,0.55,0.62), frame=(0.62,0.66,0.70), pur=(0.25,0.25,0.30), prn=(0.85,0.40,0.55), tnut=(0.97,0.55,0.05),
           cutter=(0.60,0.40,0.75), tray=(0.30,0.65,0.75), plug=(0.90,0.75,0.20), stop=(0.75,0.35,0.55), foot=(0.55,0.55,0.35))

def add(shape, color, dev=0.3, name="o", trans=0):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    vo = o.ViewObject
    vo.ShapeColor = color
    vo.DisplayMode = "Flat Lines"
    vo.LineColor = (0.05, 0.05, 0.05)
    vo.LineWidth = 1.0
    vo.Deviation = dev
    vo.AngularDeflection = 12
    if trans: vo.Transparency = trans
    return o
def addmesh(m, color, name="m"):
    o = doc.addObject("Mesh::Feature", name)
    o.Mesh = m
    vo = o.ViewObject
    vo.ShapeColor = color
    try: vo.DisplayMode = "Flat"
    except Exception: pass
    return o
def clear():
    for o in list(doc.Objects): doc.removeObject(o.Name)

def mesh_halfcut(sh, point, n, tol=0.08):
    """tessellation clipped at the plane (removes the n side), cap from the section outline. Returns (Mesh, cap Face)."""
    n = V(*n); n.normalize(); P0 = V(*point)
    vs, fs = sh.tessellate(tol)
    EPS = 7e-4
    d = [n.dot(v - P0) - EPS for v in vs]
    out = []; segs = []
    def lerp(i, j):
        t = d[i] / (d[i] - d[j]); return vs[i] + (vs[j] - vs[i]) * t
    for a, b, c in fs:
        tri = (a, b, c)
        ins = [k for k in tri if d[k] <= 0]
        if len(ins) == 3: out.append((vs[a], vs[b], vs[c])); continue
        if not ins: continue
        poly = []; cuts = []
        for q in range(3):
            i, j = tri[q], tri[(q + 1) % 3]
            if d[i] <= 0: poly.append(vs[i])
            if (d[i] <= 0) != (d[j] <= 0):
                pt = lerp(i, j) if i < j else lerp(j, i)
                poly.append(pt); cuts.append(pt)
        for k in range(1, len(poly) - 1): out.append((poly[0], poly[k], poly[k + 1]))
        if len(cuts) == 2: segs.append((cuts[0], cuts[1]))
    if not out: raise RuntimeError("mesh_halfcut: no triangles kept")
    m = Mesh.Mesh([[tuple(v) for v in tr] for tr in out])
    key = lambda v: (round(v.x, 3), round(v.y, 3), round(v.z, 3))
    adj = {}
    for si, (p0, p1) in enumerate(segs):
        adj.setdefault(key(p0), []).append(si); adj.setdefault(key(p1), []).append(si)
    used = set(); wires = []
    for s0 in range(len(segs)):
        if s0 in used: continue
        used.add(s0); pts = [segs[s0][0], segs[s0][1]]; closed = False
        while True:
            last = key(pts[-1])
            if last == key(pts[0]) and len(pts) > 2: closed = True; break
            nxt = [s for s in adj.get(last, []) if s not in used]
            if not nxt: break
            s = nxt[0]; used.add(s)
            a_, b_ = segs[s]
            pts.append(b_ if key(a_) == last else a_)
        if closed and len(pts) >= 4:
            try:
                pts[-1] = pts[0]; wires.append(Part.makePolygon(pts))
            except Exception: pass
    if not wires: raise RuntimeError("mesh_halfcut: no closed section loop")
    cap = Part.makeFace(wires, "Part::FaceMakerBullseye")
    if cap.isNull() or cap.Area < 1.0: raise RuntimeError("mesh_halfcut: cap face empty")
    return m, cap

def halfcut(sh, point, n, size=1500):
    n = V(*n); n.normalize()
    box = Part.makeBox(2*size, 2*size, size, V(-size, -size, 0))
    box.Placement = App.Placement(V(*point), App.Rotation(V(0, 0, 1), n))
    r = sh.cut(box)
    if r.isNull() or not r.isValid() or r.Volume <= 1.0 or r.Volume > sh.Volume*0.9999:
        raise RuntimeError("halfcut FAILED")
    bb = r.BoundBox
    if max(n.dot(V(x, y, z) - V(*point)) for x in (bb.XMin, bb.XMax) for y in (bb.YMin, bb.YMax) for z in (bb.ZMin, bb.ZMax)) > 1e-3:
        raise RuntimeError("halfcut FAILED past plane")
    return r
def local(sh, target, half):
    t = V(*target)
    box = Part.makeBox(2*half[0], 2*half[1], 2*half[2], V(t.x-half[0], t.y-half[1], t.z-half[2]))
    r = sh.common(box)
    return None if (r.isNull() or r.Volume < 1.0) else r
def static_cut(sh, col, nrm=(0, -1, 0)):
    """list of (kind, obj, colour) for a static part cut at y=0; BOP, mesh fallback"""
    try:
        return [add(halfcut(sh, (0, 0, 0), nrm), col, 0.15)]
    except Exception:
        m, cap = mesh_halfcut(sh, (0, 0, 0), nrm)
        return [addmesh(m, col), add(cap, col, 0.15)]

# ---------- camera ----------
def setcam(target, d, up=(0, 0, 1), height=600.0):
    d = V(*d); d.normalize()
    r = d.cross(V(*up))
    if r.Length < 1e-6: r = d.cross(V(0, 1, 0))
    r.normalize()
    u = r.cross(d); u.normalize()
    target = V(*target)
    dist = 3000.0
    pos = target - d*dist
    rot = App.Rotation(r, u, -d, "ZXY")
    ax = rot.Axis; ang = rot.Angle
    s = ("#Inventor V2.1 ascii\nOrthographicCamera { position %f %f %f orientation %f %f %f %f "
         "nearDistance 100 farDistance 6000 aspectRatio %f focalDistance %f height %f }" %
         (pos.x, pos.y, pos.z, ax.x, ax.y, ax.z, ang, 1.0*W/H, dist, height))
    view.setCamera(s)

from PIL import Image, ImageDraw, ImageFont
try:
    FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
    FONT2 = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 26)
except Exception:
    FONT = FONT2 = ImageFont.load_default()
FRAMEN = [0]
STATS = []
def shoot(caption, sub=""):
    QW.QApplication.processEvents(); time.sleep(0.12); QW.QApplication.processEvents()
    tmp = os.path.join(FR, "f%05d.png" % FRAMEN[0])
    view.saveImage(tmp, W, H, "Current")
    im = Image.open(tmp).convert("RGB")
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, W, 56 + (34 if sub else 0)], fill=(20, 20, 24))
    dr.text((18, 8), caption, font=FONT, fill=(245, 245, 245))
    if sub: dr.text((18, 52), sub, font=FONT2, fill=(200, 205, 215))
    im.save(tmp)
    if FRAMEN[0] % 40 == 0:
        import numpy as np
        a = np.asarray(im).astype(int)
        bg = a[H-4, 4]
        cov = float((abs(a - bg).sum(axis=2) > 12)[60:].mean()) * 100
        STATS.append((FRAMEN[0], cov)); log("FRAME %d cov=%.1f corner=%s" % (FRAMEN[0], cov, tuple(bg)))
    FRAMEN[0] += 1

def ease(t): return t*t*(3 - 2*t)

# ---------- scene builders ----------
def build_whole():
    q = P["R_100p0"]; rec, plate = split_base("R_100p0"); pur, prn = split_bracket("R_100p0")
    O = {}
    O["plate"] = add(plate, COL["plate"]); O["rec"] = add(rec, COL["receiver"])
    O["holder"] = add(q["holder"], COL["holder"])
    O["collet"] = {k: add(P[k + "_100p0"]["collet"], COLLET_RGB) for k in ("R", "Kd1", "Kmax")}
    O["nut"] = add(q["nut"], COL["nut"]); O["washer"] = add(q["washer"], COL["washer"])
    O["core"] = {k: add(P[k + "_100p0"]["core"], COL["core"]) for k in ("R", "Kd1", "Kmax")}
    for k in ("Kd1", "Kmax"):
        O["collet"][k].ViewObject.Visibility = False; O["core"][k].ViewObject.Visibility = False
    add(q["frame"], COL["frame"], 0.5); add(q["tnut"], COL["tnut"], 0.5)
    O["cutter"] = add(q["cutter"], COL["cutter"], 0.3, "cutter", 75)
    for s in pur: add(s, COL["pur"], 0.4)
    for s in prn: add(s, COL["prn"], 0.4)
    for k, c in (("tray", "tray"), ("plug", "plug"), ("stop", "stop")): add(J[k], COL[c], 0.4)
    for i in (1, 2, 3, 4): add(J["foot_%d" % i], COL["foot"], 0.4)
    return O

def pose_at(f_phase):
    """phase 0..2 along R -> Kd1 -> Kmax; returns phi, dz, collet/core set"""
    if f_phase <= 1:
        t = ease(f_phase); phi = PHI["R"] + (PHI["Kd1"] - PHI["R"])*t
    else:
        t = ease(f_phase - 1); phi = PHI["Kd1"] + (PHI["Kmax"] - PHI["Kd1"])*t
    dz = LEAD * phi / 360.0
    st = "R" if f_phase < 0.5 else ("Kd1" if f_phase < 1.5 else "Kmax")
    return phi, dz, st

def place(O, phi, dz, st):
    rot = App.Placement(V(0, 0, dz), App.Rotation(V(0, 0, 1), phi))
    O["nut"].Placement = rot; O["washer"].Placement = rot
    O["holder"].Placement = App.Placement(V(0, 0, dz), App.Rotation())
    for k in ("R", "Kd1", "Kmax"):
        O["collet"][k].ViewObject.Visibility = (k == st); O["core"][k].ViewObject.Visibility = (k == st)

def label(f_phase):
    if abs(f_phase) < 1e-9: return "R"
    if abs(f_phase - 1) < 1e-9: return "Kd1"
    if abs(f_phase - 2) < 1e-9: return "Kmax"
    return "R to Kd1" if f_phase < 1 else "Kd1 to Kmax"

def nf(n): return min(n, LIMIT) if LIMIT else n

# ---------- segment 1: turntable ----------
def seg1():
    O = build_whole(); QW.QApplication.processEvents()
    n = nf(210)
    for i in range(n):
        th = math.radians(-45 + 360.0*i/n)
        el = math.radians(32)
        d = (-math.cos(th)*math.cos(el), -math.sin(th)*math.cos(el), -math.sin(el))
        setcam((0, 0, 250), d, (0, 0, 1), 900)
        shoot("Turntable | pose R (release) | collet 100 mm", "cutter keep-out 75 percent transparent")
    log("SEG1 done frames %d" % FRAMEN[0])
    return O

# ---------- segment 2: clamp, iso ----------
def seg2(O):
    seq = [(0, 0, 0.0)]
    # (frames, from phase, to phase)
    plan = [(15, 0.0, 0.0), (90, 0.0, 1.0), (15, 1.0, 1.0), (90, 1.0, 2.0), (15, 2.0, 2.0)]
    for fr, a, b in plan:
        for i in range(nf(fr)):
            ph = a + (b - a)*((i + 1)/float(fr) if b != a else 0.0)
            phi, dz, st = pose_at(ph)
            place(O, phi, dz, st)
            setcam((0, 0, 125), (-1, 1, -0.9), (0, 0, 1), 520)
            shoot("Clamp | %s | collet 100 mm" % label(ph), "nut turn %.0f deg, travel %.2f mm" % (abs(phi), abs(dz)))
    log("SEG2 done frames %d" % FRAMEN[0])

# ---------- segment 3: axial half-section ----------
def seg3():
    clear(); QW.QApplication.processEvents()
    q = P["R_100p0"]; rec, plate = split_base("R_100p0")
    pl = local(plate, (0, 0, 6), (170, 170, 20))
    static_cut(pl, COL["plate"]); static_cut(rec, COL["receiver"])
    H0 = static_cut(q["holder"], COL["holder"])
    CO = {}; CR = {}
    for k in ("R", "Kd1", "Kmax"):
        pc = P[k + "_100p0"]
        CO[k] = static_cut(pc["collet"], COLLET_RGB)
        CR[k] = static_cut(local(pc["core"], (0, 0, 120), (70, 70, 80)), COL["core"])
        if k != "R":
            for o in CO[k] + CR[k]: o.ViewObject.Visibility = False
    cut = static_cut(local(q["cutter"], (0, 0, 190), (130, 130, 60)), COL["cutter"])
    for o in cut: o.ViewObject.Visibility = True
    for o in cut:
        try: o.ViewObject.Transparency = 75
        except Exception: pass
    dyn = []
    plan = [(15, 0.0, 0.0), (80, 0.0, 1.0), (10, 1.0, 1.0), (80, 1.0, 2.0), (10, 2.0, 2.0)]
    def frame(ph, tgt, hgt, cap, sub):
        phi, dz, st = pose_at(ph)
        for o in dyn:
            try: doc.removeObject(o.Name)
            except Exception: pass
        dyn.clear()
        nrm = App.Rotation(V(0, 0, 1), -phi).multVec(V(0, -1, 0))
        plc = App.Placement(V(0, 0, dz), App.Rotation(V(0, 0, 1), phi))
        for key in ("nut", "washer"):
            m, capf = mesh_halfcut(q[key], (0, 0, 0), (nrm.x, nrm.y, nrm.z))
            for ob in (addmesh(m, COL[key]), add(capf, COL[key], 0.15)):
                ob.Placement = plc; dyn.append(ob)
        for o in H0: o.Placement = App.Placement(V(0, 0, dz), App.Rotation())
        for k in ("R", "Kd1", "Kmax"):
            for o in CO[k] + CR[k]: o.ViewObject.Visibility = (k == st)
        setcam(tgt, (0, 1, 0), (0, 0, 1), hgt)
        shoot(cap, sub)
    for fr, a, b in plan:
        for i in range(nf(fr)):
            ph = a + (b - a)*((i + 1)/float(fr) if b != a else 0.0)
            frame(ph, (0, 0, 105), 240, "Half-section | %s | collet 100 mm" % label(ph), "section y=0, nut turn %.0f deg" % abs(PHI_of(ph)))
    n = nf(30)
    for i in range(n):
        t = ease((i + 1)/float(n))
        tgt = (68*t, 0, 105 + 25*t); hgt = 240 + (30 - 240)*t
        frame(2.0, tgt, hgt, "Half-section | Kmax | collet 100 mm", "witness: holder flange to receiver rim gap %s mm" % GAPTXT)
    for i in range(nf(30)):
        frame(2.0, (68, 0, 130), 30, "Half-section | Kmax | collet 100 mm", "witness reads %s mm (flange gap at Kmax)" % GAPTXT)
    log("SEG3 done frames %d" % FRAMEN[0])

def PHI_of(ph): return pose_at(ph)[0]

try:
    O = seg1()
    seg2(O)
    seg3()
except Exception:
    log("FAIL " + traceback.format_exc())
log("FRAMES %d" % FRAMEN[0])
log("BUILD_DONE " + time.strftime("%H:%M:%S"))
logf.close()
sys.stdout.flush()
os._exit(0)
