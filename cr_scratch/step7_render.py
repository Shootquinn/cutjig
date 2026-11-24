import sys, os, json, math, shutil, time, traceback
import FreeCAD as App, Part, Mesh
import FreeCADGui as Gui
if getattr(App, "_ran", False):
    sys.exit(0)
App._ran = True
V = App.Vector
ROOT = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig"
ASM = ROOT + r"\parts_cache\assembly\pose_%s.FCStd"
JIG = ROOT + r"\output\jig_assembly.FCStd"
FR = r"C:\Users\Quinn Morley\AppData\Local\Temp\rend7\frames"
FINAL = ROOT + r"\cr_scratch\step7_renders"
LOG = ROOT + r"\cr_scratch\step7_render.log"
RES = r"C:\Users\Quinn Morley\AppData\Local\Temp\rend7\results.json"
os.makedirs(FR, exist_ok=True); os.makedirs(FINAL, exist_ok=True)
ONLY = os.environ.get("RONLY", "")
logf = open(LOG, "a" if ONLY else "w")
def log(s):
    logf.write(s + "\n"); logf.flush()
log("RENDER_START " + time.strftime("%H:%M:%S") + " only=" + ONLY)

# ---------- load shapes (read only, never saved) ----------
POSES = ["R_100p0", "Kd1_100p0", "Kmax_100p0", "Kmax_090p0", "Kmax_105p0"]
P = {}
for tag in POSES:
    d = App.openDocument(ASM % tag)
    P[tag] = {o.Name: o.Shape.copy() for o in d.Objects if hasattr(o, "Shape") and not o.Shape.isNull()}
    App.closeDocument(d.Name)
d = App.openDocument(JIG)
J = {o.Name: o.Shape.copy() for o in d.Objects if hasattr(o, "Shape") and not o.Shape.isNull()}
App.closeDocument(d.Name)

def split_base(pose):
    s = sorted(P[pose]["base"].Solids, key=lambda s: s.Volume)
    return s[0], s[1]               # receiver, plate
def split_bracket(pose):
    sols = P[pose]["bracket"].Solids
    pur = [s for i, s in enumerate(sols) if i not in (4, 5, 6, 7)]
    prn = [sols[i] for i in (4, 5, 6, 7)]
    return pur, prn

def reading_z(nut):
    best = None
    for f in nut.Faces:
        try:
            if f.Surface.__class__.__name__ != "Plane": continue
            n = f.normalAt(0, 0)
            if abs(abs(n.z) - 1) > 1e-6: continue
            rs = [math.hypot(v.X, v.Y) for v in f.Vertexes]
            if abs(min(rs) - 73.54) < 0.3 and abs(max(rs) - 83.14) < 0.3:
                best = f.BoundBox.ZMin
        except Exception:
            pass
    return best

def surf_z(sh, x, y, z0=-100, z1=700):
    ln = Part.makeLine(V(x, y, z0), V(x, y, z1))
    c = sh.common(ln)
    if not c.Edges: return (None, None)
    return (min(e.BoundBox.ZMin for e in c.Edges), max(e.BoundBox.ZMax for e in c.Edges))

XG = (95.14 + 0.5 + 115.0 - 6.0) / 2.0
MEAS = {}
for tag in POSES:
    nut = P[tag]["nut"]; hol = P[tag]["holder"]; col = P[tag]["collet"]
    far = max(nut.Vertexes, key=lambda v: v.X*v.X + v.Y*v.Y)
    MEAS[tag] = dict(nut_zmin=nut.BoundBox.ZMin, nut_zmax=nut.BoundBox.ZMax, reading_z=reading_z(nut),
                     holder_zmin=hol.BoundBox.ZMin, holder_zmax=hol.BoundBox.ZMax,
                     collet_zmin=col.BoundBox.ZMin, collet_zmax=col.BoundBox.ZMax,
                     washer_zmin=P[tag]["washer"].BoundBox.ZMin,
                     nut_far_vertex_az=math.degrees(math.atan2(far.Y, far.X)), nut_far_vertex_r=math.hypot(far.X, far.Y))
    log("MEAS %s %s" % (tag, json.dumps(MEAS[tag])))

def wing_centres(nut):
    have = []
    for a in range(0, 360, 1):
        r = math.radians(a)
        zb, zt = surf_z(nut, XG*math.cos(r), XG*math.sin(r))
        if zt is not None: have.append(a)
    runs, cur = [], []
    for a in range(0, 360, 1):
        if a in have: cur.append(a)
        elif cur: runs.append(cur); cur = []
    if cur: runs.append(cur)
    if len(runs) > 1 and runs[0][0] == 0 and runs[-1][-1] == 359:
        runs[0] = runs[-1] + runs[0]; runs.pop()
    out = []
    for r_ in runs:
        angs = [a if a >= r_[0] else a + 360 for a in r_]
        out.append((sum(angs)/len(angs)) % 360)
    return out
WAZ = {}
for tag in ("R_100p0", "Kmax_100p0"):
    WAZ[tag] = wing_centres(P[tag]["nut"])
    log("WINGS %s centres %s" % (tag, WAZ[tag]))

Gui.showMainWindow()
import PySide6.QtWidgets as QW
BG = (0.80, 0.81, 0.83)
p = App.ParamGet("User parameter:BaseApp/Preferences/View")
p.SetBool("Gradient", False); p.SetBool("UseBackgroundColorMid", False)
bgi = (int(BG[0]*255) << 24) | (int(BG[1]*255) << 16) | (int(BG[2]*255) << 8)
for k in ("BackgroundColor", "BackgroundColor2", "BackgroundColor3", "BackgroundColor4"):
    p.SetUnsigned(k, bgi)
doc = App.newDocument("R7")
QW.QApplication.processEvents()
gdoc = Gui.getDocument("R7")
view = gdoc.ActiveView
try: view.setCameraType("Orthographic")
except Exception as e: log("camtype " + str(e))
try: view.setAxisCross(False)
except Exception: pass
try: Gui.getMainWindow().resize(1700, 1350)
except Exception: pass

COL = dict(plate=(0.45,0.62,0.45), receiver=(0.35,0.55,0.80), holder=(0.85,0.55,0.20), nut=(0.75,0.30,0.30), washer=(0.10,0.55,0.60),
           core=(0.72,0.72,0.74), frame=(0.62,0.66,0.70), pur=(0.25,0.25,0.30), prn=(0.85,0.40,0.55), tnut=(0.97,0.55,0.05),
           cutter=(0.60,0.40,0.75), tray=(0.30,0.65,0.75), plug=(0.90,0.75,0.20), stop=(0.75,0.35,0.55), foot=(0.55,0.55,0.35),
           caddy=(0.60,0.50,0.35), gauge=(0.40,0.70,0.55), rest=(0.45,0.45,0.75))
import yaml
PRM = yaml.safe_load(open(ROOT + r"\params.yaml", encoding="utf-8"))
def pv(sec, key):
    v = PRM[sec][key]
    return v["value"] if isinstance(v, dict) and "value" in v else v
CORE_D = pv("core", "diameters"); COLLET_NAMES = pv("collet", "colour")
RGB = {"red": (0.88,0.12,0.12), "orange": (0.95,0.55,0.10), "yellow": (0.95,0.85,0.15), "green": (0.20,0.68,0.28),
       "blue": (0.15,0.35,0.88), "violet": (0.55,0.28,0.75), "white": (0.98,0.98,0.98)}
COL["core"] = (0.50, 0.55, 0.62)
log("COLLET_COLOUR params collet.colour=%s core.diameters=%s" % (COLLET_NAMES, CORE_D))

def clear():
    for o in list(doc.Objects): doc.removeObject(o.Name)
def add(shape, color, dev=0.15, name="o", trans=0):
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
    if trans: vo.Transparency = trans
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
CURBG = BG
DARK = (60/255.0, 60/255.0, 65/255.0)
def backdrop(bb, zside):
    """dark flat plate behind the part for an underside view (camera looks up); the corner pixel is the reference background"""
    z = bb.ZMax + 30 if zside > 0 else bb.ZMin - 30
    o = add(Part.makeBox(900, 900, 1, V(bb.Center.x - 450, bb.Center.y - 450, z)), DARK, 1.0, "backdrop")
    o.ViewObject.LineColor = DARK
    return o
def cov(path):
    from PIL import Image
    import numpy as np
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    bg = im[3, 3] if CURBG is not BG else np.array([int(round(BG[0]*255)), int(round(BG[1]*255)), int(round(BG[2]*255))])
    diff = (abs(im - bg).sum(axis=2) > 12)
    return im.shape[1], im.shape[0], float(diff.mean())*100
RESULTS = []
RECV_EXPECTED = ("receiver_section", "section_R_100p0", "section_Kd1_100p0", "section_Kmax_100p0", "core_R_100p0_stand_section",
                 "core_Kmax_100p0_stand_section", "witness_Kd1_100p0_section", "witness_Kmax_100p0_section")
def recv_px(path):
    from PIL import Image
    import numpy as np
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    m = (r > 60) & (r < 125) & (g > 100) & (g < 175) & (b > 160) & (b < 240) & ((b - g) > 35) & ((b - g) < 95)
    cols, cnt = np.unique(im[m], axis=0, return_counts=True)
    return float(cnt.max()) / m.size * 100 if len(cnt) else 0.0   # largest flat receiver-coloured region = the cut face
def finish(name, tmp, pose, size, view_desc, ids):
    try:
        w, h, c = cov(tmp)
        if name in RECV_EXPECTED:
            rp = recv_px(tmp)
            log("CHK %s receiver cross-section pixels %.2f percent %s" % (name, rp, "PASS" if rp >= 0.3 else "FAIL"))
            if rp < 0.3: raise RuntimeError("receiver cross-section absent in " + name)
        shutil.copyfile(tmp, os.path.join(FINAL, name + ".png"))
        RESULTS.append(dict(name=name, pose=pose, size=size, view=view_desc, ids=ids, w=w, h=h, cov=c))
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
def addmesh(m, color, name):
    o = doc.addObject("Mesh::Feature", name)
    o.Mesh = m
    doc.recompute()
    vo = o.ViewObject
    vo.ShapeColor = color
    try: vo.DisplayMode = "Flat"
    except Exception: pass
    return o
def scene(items, dev=0.15):
    clear()
    for i, it in enumerate(items):
        if isinstance(it[0], Mesh.Mesh): addmesh(it[0], it[1], "p%d" % i)
        else: add(it[0], it[1], dev, "p%d" % i, it[2] if len(it) > 2 else 0)
    return bbof([it[0] for it in items])
def snap(name, pose, size, desc, ids, **kw):
    if not want(name): return
    dark = name.endswith("_underside")
    try:
        if dark:
            global CURBG
            CURBG = DARK
        finish(name, shoot(name, **kw), pose, size, desc + (" (dark background 60/60/65)" if dark else ""), ids)
    except Exception:
        log("FAIL %s %s" % (name, traceback.format_exc()))
    finally:
        CURBG = BG
def local(sh, target, half):
    try:
        t = V(*target)
        box = Part.makeBox(2*half[0], 2*half[1], 2*half[2], V(t.x-half[0], t.y-half[1], t.z-half[2]))
        r = sh.common(box)
        if r.isNull() or r.Volume < 1.0: return None
        return r
    except Exception:
        log("local failed " + traceback.format_exc().splitlines()[-1]); return None
def _side(sh, point, n):
    """(max, min) of n.(corner - point) over the bounding box"""
    bb = sh.BoundBox
    vs = [n.dot(V(x, y, z) - V(*point)) for x in (bb.XMin, bb.XMax) for y in (bb.YMin, bb.YMax) for z in (bb.ZMin, bb.ZMax)]
    return max(vs), min(vs)
def halfcut(sh, point, n, size=1500):
    """remove the half-space on the n side. Raises when the cut did not happen."""
    n = V(*n); n.normalize()
    hi, lo = _side(sh, point, n)
    if lo >= -1e-6: raise RuntimeError("halfcut: shape entirely on the removed side")
    if hi <= 1e-6: return sh                      # shape does not reach the plane
    box = Part.makeBox(2*size, 2*size, size, V(-size, -size, 0))
    box.Placement = App.Placement(V(*point), App.Rotation(V(0, 0, 1), n))
    r = sh.cut(box)
    if r.isNull() or not r.isValid() or r.Volume <= 1.0 or r.Volume > sh.Volume*0.9999:
        raise RuntimeError("halfcut FAILED: volume %.1f -> %.1f valid=%s" % (sh.Volume, 0 if r.isNull() else r.Volume, (not r.isNull()) and r.isValid()))
    h2, l2 = _side(r, point, n)
    if h2 > 1e-3: raise RuntimeError("halfcut FAILED: result extends %.3f past the plane" % h2)
    return r
def mesh_halfcut(sh, point, n, tol=0.05):
    """Receiver only: its helical faces fail OCC booleans (BOPAlgo_InvalidCurveOnSurface, Step 4).
    Clip the tessellation at the plane and cap it with the slice wires. Returns [(Mesh, 'half'), (cap Face, 'cap')]. Raises when the cap is empty."""
    n = V(*n); n.normalize(); P0 = V(*point)
    vs, fs = sh.tessellate(tol)
    EPS = 7e-4                                   # plane offset keeps vertices off the cut plane
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
    used = set(); wires = []; open_loops = 0
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
            except Exception: open_loops += 1
        else: open_loops += 1
    if not wires: raise RuntimeError("mesh_halfcut: no closed section loop")
    cap = Part.makeFace(wires, "Part::FaceMakerBullseye")
    if cap.isNull() or cap.Area < 1.0: raise RuntimeError("mesh_halfcut: cap face empty")
    log("mesh_halfcut: triangles %d kept of %d, cap area %.1f mm2 (%d loops, %d open)" % (len(out), len(fs), cap.Area, len(wires), open_loops))
    return [(m, None), (cap, None)]
def cut_items(pairs, point, n):
    """pairs of (shape, colour); returns scene items cut at the plane; the receiver goes through mesh_halfcut"""
    out = []
    for s, c in pairs:
        try:
            out.append((halfcut(s, point, n), c))
        except RuntimeError as e:
            log("FALLBACK mesh cut (%s)" % str(e)[:120])
            for o, _ in mesh_halfcut(s, point, n): out.append((o, c))
    return out
def run(fn):
    try: fn()
    except Exception: log("FAIL-JOB %s %s" % (fn.__name__, traceback.format_exc()))

def collet_col(tag):
    dia = float(tag.split("_")[1].replace("p", "."))
    i = min(range(len(CORE_D)), key=lambda k: abs(CORE_D[k] - dia))
    return RGB[COLLET_NAMES[i]]
def whole_items(tag, cutter_trans=75):
    q = P[tag]; rec, plate = split_base(tag); pur, prn = split_bracket(tag)
    it = [(plate, COL["plate"]), (rec, COL["receiver"]), (q["holder"], COL["holder"]), (q["collet"], collet_col(tag)),
          (q["nut"], COL["nut"]), (q["washer"], COL["washer"]), (q["core"], COL["core"]), (q["frame"], COL["frame"]),
          (q["tnut"], COL["tnut"]), (q["cutter"], COL["cutter"], cutter_trans)]
    it += [(s, COL["pur"]) for s in pur] + [(s, COL["prn"]) for s in prn]
    it += [(J["tray"], COL["tray"]), (J["plug"], COL["plug"]), (J["stop"], COL["stop"])]
    it += [(J["foot_%d" % i], COL["foot"]) for i in (1, 2, 3, 4)]
    return it
def sz(tag):
    return "%g" % float(tag.split("_")[1].replace("p", "."))
def pose_of(tag): return tag.split("_")[0]
VIEWS = [("front", (0,1,0), (0,0,1)), ("side", (-1,0,0), (0,0,1)), ("top", (0,0,-1), (0,1,0)), ("iso", (-1,1,-1), (0,0,1))]

# ---------- whole assembly, four views ----------
def job_whole():
    for tag in ("R_100p0", "Kmax_100p0", "Kmax_090p0", "Kmax_105p0"):
        if not wantany("whole_%s" % tag): continue
        bb = scene(whole_items(tag), 0.4)
        for vn, d, up in VIEWS:
            snap("whole_%s_%s" % (tag, vn), pose_of(tag), sz(tag), "whole assembly, %s (cutter keep-out transparent)" % vn,
                 "1-15", bb=bb, d=d, up=up)
run(job_whole)

# ---------- axis sections, three poses ----------
def job_sections():
    for tag in ("R_100p0", "Kd1_100p0", "Kmax_100p0"):
        n = "section_%s" % tag
        if not want(n): continue
        q = P[tag]; rec, plate = split_base(tag)
        its = [(plate, COL["plate"]), (rec, COL["receiver"]), (q["holder"], COL["holder"]), (q["collet"], collet_col(tag)), (q["nut"], COL["nut"]),
               (q["washer"], COL["washer"]), (q["core"], COL["core"]), (q["cutter"], COL["cutter"])]
        pairs = []
        for it in its:
            l = it[0] if it[1] == COL["receiver"] else local(it[0], (0, 0, 120), (170, 170, 200))
            if l is None: continue
            pairs.append((l, it[1]))
        scene(cut_items(pairs, (0, 0, 0), (0, -1, 0)), 0.12)
        snap(n, pose_of(tag), sz(tag), "section y=0 viewed from -Y: receiver, holder, collet, core, nut, washer, cutter", "2 3 4 5 6 7 11 13 14",
             target=(0, 0, 110), d=(0,1,0), up=(0,0,1), height=240)
run(job_sections)

# ---------- receiver witness, holder tick ----------
RAZ = math.radians(127.0); RC, RS = math.cos(RAZ), math.sin(RAZ)
def job_witness():
    for tag in ("R_100p0", "Kd1_100p0", "Kmax_100p0"):
        if not wantany("witness_%s" % tag) and not wantany("holder_tick_%s" % tag): continue
        q = P[tag]; rec, plate = split_base(tag)
        edge = MEAS[tag]["reading_z"] if MEAS[tag]["reading_z"] is not None else MEAS[tag]["nut_zmin"]
        hz0 = MEAS[tag]["holder_zmin"]
        its = [(rec, COL["receiver"]), (q["holder"], COL["holder"]), (q["nut"], COL["nut"]), (q["washer"], COL["washer"]), (q["collet"], collet_col(tag))]
        loc = [(local(s, (0, 0, edge), (130, 130, 80)), c) for s, c in its]
        loc = [(s, c) for s, c in loc if s is not None]
        scene(loc, 0.1)
        snap("witness_%s_view" % tag, pose_of(tag), sz(tag), "receiver rim scale, holder, nut: horizontal line of sight at az 127, reading face z %.2f" % edge, "2 3 5 13",
             target=(0, 0, edge + 12), d=(-RC, -RS, 0), up=(0,0,1), height=190)
        snap("witness_%s_closeup" % tag, pose_of(tag), sz(tag), "RC6 ruler graduations at the nut skirt bottom, z %.2f, eye level, ruler below the reading face" % edge, "2 5 13",
             target=(72.0*RC, 72.0*RS, edge - 6), d=(-RC, -RS, 0), up=(0,0,1), height=36)
        if tag != "R_100p0":
            if want("witness_%s_section" % tag):
                nrm = (-RS, RC, 0)
                scene(cut_items(loc, (0, 0, 0), nrm), 0.1)
                snap("witness_%s_section" % tag, pose_of(tag), sz(tag), "section through the axis at az 127, ruler and skirt profile, viewed from the cut side", "2 5 13",
                     target=(75.0*RC, 75.0*RS, edge + 5), d=(RS, -RC, 0), up=(0,0,1), height=70)
            hz = hz0 + 90.0
            hl = local(q["holder"], (72*RC, 72*RS, hz), (28, 28, 16))
            if hl is not None:
                scene([(hl, COL["holder"])], 0.08)
                snap("holder_tick_%s" % tag, pose_of(tag), sz(tag), "HD7 tick at az 127 on the flange rim, radial view, z %.2f" % hz, "3 13",
                     target=(72*RC, 72*RS, hz), d=(-RC, -RS, 0), up=(0,0,1), height=18)
run(job_witness)

# ---------- single parts in pose ----------
def job_parts():
    tag = "R_100p0"; q = P[tag]; rec, plate = split_base(tag)
    if wantany("receiver_"):
        bb = scene([(rec, COL["receiver"])], 0.1)
        snap("receiver_top", "R", "100", "receiver from above: bore thread lead-in, key slot at 37 deg, rim scale", "2", bb=bb, d=(0,0,-1), up=(0,1,0))
        snap("receiver_iso", "R", "100", "receiver iso", "2", bb=bb, d=(-1,1,-1), up=(0,0,1))
        bb2 = scene(cut_items([(rec, COL["receiver"])], (0, 0, 0), (0, -1, 0)), 0.1)
        snap("receiver_section", "R", "100", "receiver section y=0: thread, lead-in, floor seat", "2", bb=bb2, d=(0,1,0), up=(0,0,1))
        ka = math.radians(37.0)
        loc = local(rec, (80*math.cos(ka), 80*math.sin(ka), 120), (40, 40, 20))
        if loc is not None:
            scene([(loc, COL["receiver"])], 0.08)
            snap("receiver_keyslot_closeup", "R", "100", "key slot at 37 deg on the rim, oblique", "2", target=(80*math.cos(ka), 80*math.sin(ka), 125),
                 d=(-math.cos(ka)*0.7, -math.sin(ka)*0.7, -0.7), up=(0,0,1), height=70)
    if wantany("holder_"):
        bb = scene([(q["holder"], COL["holder"])], 0.1)
        snap("holder_top", "R", "100", "holder from above: collar, four holes, index notch", "3", bb=bb, d=(0,0,-1), up=(0,1,0))
        snap("holder_iso", "R", "100", "holder iso: cone, collar", "3", bb=bb, d=(-1,1,-1), up=(0,0,1))
        snap("holder_bottom", "R", "100", "holder from below: flange underside, cone, index notch", "3", bb=bb, d=(0,0,1), up=(0,1,0))
        bb2 = scene([(halfcut(q["holder"], (0, 0, 0), (0, -1, 0)), COL["holder"])], 0.1)
        snap("holder_section", "R", "100", "holder section y=0: cone and collar", "3", bb=bb2, d=(0,1,0), up=(0,0,1))
    if wantany("baseplate_"):
        bb = scene([(plate, COL["plate"])], 0.15)
        snap("baseplate_top", "R", "100", "base plate from above: asymmetric slot pattern, one slot offset", "1", bb=bb, d=(0,0,-1), up=(0,1,0))
        snap("baseplate_bottom", "R", "100", "base plate from below: plate keys, stop pin pocket", "1", bb=bb, d=(0,0,1), up=(0,1,0))
        snap("baseplate_iso", "R", "100", "base plate iso", "1", bb=bb, d=(-1,1,-1), up=(0,0,1))
        bb = scene([(plate, COL["plate"]), (rec, COL["receiver"])], 0.15)
        snap("baseplate_receiver_iso", "R", "100", "plate with receiver foot", "1 2", bb=bb, d=(-1,1,-1), up=(0,0,1))
        loc = local(plate, (-262, 200, 6), (70, 110, 20))
        if loc is not None:
            scene([(loc, COL["plate"])], 0.1)
            snap("baseplate_slots_closeup", "R", "100", "slot pattern at the -X +Y corner, top", "1", target=(-262, 200, 12), d=(0,0,-1), up=(0,1,0), height=230)
    if wantany("tray_"):
        bb = scene([(plate, COL["plate"]), (J["tray"], COL["tray"]), (J["plug"], COL["plug"])], 0.15)
        snap("tray_plug_iso", "R", "100", "plate with tray and drain plug, iso", "1 12", bb=bb, d=(-1,1,-1), up=(0,0,1))
        snap("tray_plug_top", "R", "100", "tray and plug from above", "12", bb=bb, d=(0,0,-1), up=(0,1,0))
        cut = [(halfcut(s, (0, 0, 0), (0, -1, 0)), c) for s, c in ((plate, COL["plate"]), (J["tray"], COL["tray"]), (J["plug"], COL["plug"]))]
        scene(cut, 0.15)
        snap("tray_plug_drain_section", "R", "100", "section y=0 at the drain and plug", "12", target=(-172, 0, 25), d=(0,1,0), up=(0,0,1), height=90)
    if want("stop_closeup"):
        its = [(J["stop"], COL["stop"]), (q["cutter"], COL["cutter"], 70), (q["nut"], COL["nut"]), (q["holder"], COL["holder"])]
        out = []
        for it in its:
            l = local(it[0], (0, 214, 178), (110, 110, 80))
            if l is not None: out.append((l,) + tuple(it[1:]))
        out.append((Part.makeBox(90, 6, 130, V(-45, 244, 172.84)), (0.92, 0.86, 0.55), 55))
        scene(out, 0.12)
        snap("stop_closeup", "R", "100", "stop pad ST1 (magenta) on the translucent yellow plate that stands for the upper-assembly column face (phantom, context only), cutter keep-out transparent, iso", "11 12", target=(0, 214, 178), d=(-1,1,-0.6), up=(0,0,1), height=200)
run(job_parts)

# ---------- washer, nut, collet, core, cutter ----------
def job_internals():
    for tag in ("R_100p0", "Kmax_100p0"):
        q = P[tag]
        if wantany("washer_%s" % tag):
            bb = scene([(q["washer"], COL["washer"])], 0.08)
            snap("washer_%s_top" % tag, pose_of(tag), sz(tag), "washer from above: radial tab notch off-axis", "6", bb=bb, d=(0,0,-1), up=(0,1,0))
            snap("washer_%s_iso" % tag, pose_of(tag), sz(tag), "washer iso", "6", bb=bb, d=(-1,1,-1), up=(0,0,1))
            zc = q["washer"].BoundBox.Center.z
            pairs = []
            for s, c in ((q["nut"], COL["nut"]), (q["washer"], COL["washer"])):
                l = local(s, (0, 0, zc), (130, 130, 30))
                if l is not None: pairs.append((l, c))
            scene(cut_items(pairs, (0, 0, 0), (0, -1, 0)), 0.08)
            snap("washer_%s_section" % tag, pose_of(tag), sz(tag), "nut and washer section y=0: PTFE ring seated in the nut pocket", "5 6", target=(0, 0, zc), d=(0,1,0), up=(0,0,1), height=90)
        if wantany("nut_%s" % tag):
            nut = q["nut"]; bb = scene([(nut, COL["nut"])], 0.12)
            snap("nut_%s_top" % tag, pose_of(tag), sz(tag), "nut from above: marked wing, NT4 glyph, release arrow, tommy-bar sockets", "5", bb=bb, d=(0,0,-1), up=(0,1,0))
            snap("nut_%s_bottom" % tag, pose_of(tag), sz(tag), "nut from below: NT5 glyph, dust skirt", "5", bb=bb, d=(0,0,1), up=(0,1,0))
            snap("nut_%s_iso" % tag, pose_of(tag), sz(tag), "nut iso", "5", bb=bb, d=(-1,1,-1), up=(0,0,1))
            for wi, waz in enumerate(WAZ[tag]):
                th = math.radians(waz); er = V(math.cos(th), math.sin(th), 0); et = V(-math.sin(th), math.cos(th), 0)
                def at(r, t=5.0):
                    pnt = er*r + et*t
                    return surf_z(nut, pnt.x, pnt.y)
                zb0, zt0 = at(XG); zb1, zt1 = at(XG + 6)
                if zt0 is None or zt1 is None: continue
                ft = (zt1 - zt0)/6.0; fb = (zb1 - zb0)/6.0
                ntop = er*(-ft) + V(0, 0, 1); ntop.normalize()
                nbot = er*fb + V(0, 0, -1); nbot.normalize()
                log("wing %d az %.1f %s: top %.3f..%.3f bot %.3f..%.3f" % (wi, waz, tag, zt0, zt1, zb0, zb1))
                cpt = er*XG
                loc = local(nut, (cpt.x, cpt.y, (zt0+zb0)/2), (22, 22, 22))
                if loc is None: continue
                scene([(loc, COL["nut"])], 0.2)
                for nm, nv, z, desc in (("nt4", ntop, zt0, "top face, normal to face"), ("nt5", nbot, zb0, "underside, normal to face")):
                    dv = V(-nv.x, -nv.y, -nv.z)
                    upv = (er.x, er.y, 0) if abs(dv.z) > 0.9 else (0, 0, 1)
                    snap("nut_%s_wing%d_%s" % (tag, wi, nm), pose_of(tag), sz(tag), "wing %d at az %.0f deg, %s (%s)" % (wi, waz, desc, nm.upper()), "5",
                         target=(cpt.x, cpt.y, z), d=(dv.x, dv.y, dv.z), up=upv, height=22)
                    dd = dv*math.cos(math.radians(35)) + et*math.sin(math.radians(35))
                    snap("nut_%s_wing%d_%s_oblique" % (tag, wi, nm), pose_of(tag), sz(tag), "wing %d, %s, oblique 35 deg for recess walls" % (wi, nm.upper()), "5",
                         target=(cpt.x, cpt.y, z), d=(dd.x, dd.y, dd.z), up=(0, 0, 1), height=22)
    for tag in ("R_100p0", "Kmax_090p0", "Kmax_100p0", "Kmax_105p0"):
        q = P[tag]; rec, plate = split_base(tag)
        if wantany("collet_%s" % tag):
            bb = scene([(q["collet"], collet_col(tag))], 0.1)
            backdrop(bb, 1)
            snap("collet_%s_underside" % tag, pose_of(tag), sz(tag), "collet from below: foot key, slit phase", "4", bb=bb, d=(0,0,1), up=(0,1,0))
            clear(); bb = scene([(q["collet"], collet_col(tag))], 0.1)
            snap("collet_%s_top" % tag, pose_of(tag), sz(tag), "collet alone from above: rim notches, grip-window label", "4", bb=bb, d=(0,0,-1), up=(0,1,0))
            loc = [(local(s, (0, 0, 60), (90, 90, 60)), c) for s, c in ((rec, COL["receiver"]), (q["collet"], collet_col(tag)))]
            scene([(s, c) for s, c in loc if s is not None], 0.1)
            snap("collet_%s_in_situ_top" % tag, pose_of(tag), sz(tag), "collet in the receiver (holder, nut, core removed), top: rim notches, label, size colour", "4", target=(0, 0, 70), d=(0,0,-1), up=(0,1,0), height=190)
            snap("collet_%s_in_situ_iso" % tag, pose_of(tag), sz(tag), "collet in the receiver, iso", "4", target=(0, 0, 70), d=(-1,1,-1), up=(0,0,1), height=200)
    for tag in ("R_100p0", "Kmax_100p0"):
        q = P[tag]; rec, plate = split_base(tag)
        if wantany("core_%s" % tag):
            zt = q["core"].BoundBox.ZMax
            loc = local(q["core"], (0, 0, zt - 8), (60, 60, 20))
            if loc is not None:
                scene([(loc, COL["core"])], 0.05)
                snap("core_%s_top_closeup" % tag, pose_of(tag), sz(tag), "core stand-in top end: chamfer", "7", target=(0, 0, zt - 4), d=(-1,1,-0.5), up=(0,0,1), height=70)
                scene([(halfcut(loc, (0, 0, 0), (0, -1, 0)), COL["core"])], 0.05)
                snap("core_%s_top_section" % tag, pose_of(tag), sz(tag), "core top end section at the +X edge: chamfer on the top end only", "7", target=(46, 0, zt - 8), d=(0,1,0), up=(0,0,1), height=28)
            zb = q["core"].BoundBox.ZMin
            pairs = []
            for s, c in ((q["core"], COL["core"]), (q["collet"], collet_col(tag)), (rec, COL["receiver"])):
                l = s if c == COL["receiver"] else local(s, (0, 0, zb + 5), (90, 90, 40))
                if l is not None: pairs.append((l, c))
            scene(cut_items(pairs, (0, 0, 0), (0, -1, 0)), 0.08)
            snap("core_%s_stand_section" % tag, pose_of(tag), sz(tag), "core bottom end on the collet core stop: section y=0", "7 14", target=(0, 0, zb + 15), d=(0,1,0), up=(0,0,1), height=110)
        if wantany("cutter_%s" % tag):
            out = []
            for s, c in ((q["cutter"], COL["cutter"]), (q["nut"], COL["nut"]), (q["holder"], COL["holder"]), (J["stop"], COL["stop"])):
                l = local(s, (0, 0, 180), (130, 130, 120))
                if l is not None: out.append((l, c))
            scene(out, 0.1)
            snap("cutter_%s_iso" % tag, pose_of(tag), sz(tag), "cutter keep-out: face annulus, tube, funnel, ring above the nut and holder", "11", target=(0, 0, 190), d=(-1,1,-0.5), up=(0,0,1), height=330)
            scene(cut_items(out, (0, 0, 0), (0, -1, 0)), 0.1)
            snap("cutter_%s_section" % tag, pose_of(tag), sz(tag), "cutter keep-out section y=0 over the nut collar", "11 13", target=(0, 0, 175), d=(0,1,0), up=(0,0,1), height=280)
run(job_internals)

# ---------- frame, brackets, T-nuts ----------
def job_frame():
    tag = "R_100p0"; q = P[tag]; pur, prn = split_bracket(tag)
    items = [(q["frame"], COL["frame"]), (q["tnut"], COL["tnut"])] + [(s, COL["pur"]) for s in pur] + [(s, COL["prn"]) for s in prn]
    if wantany("frame_"):
        bb = scene(items, 0.2)
        snap("frame_top", "R", "100", "frame from above, plate removed: six members, brackets, T-nuts", "8 9 10", bb=bb, d=(0,0,-1), up=(0,1,0))
        snap("frame_iso", "R", "100", "frame iso, plate removed", "8 9 10", bb=bb, d=(-1,1,-1), up=(0,0,1))
        snap("frame_bottom", "R", "100", "frame from below", "8 9 10", bb=bb, d=(0,0,1), up=(0,1,0))
        snap("frame_notch_top", "R", "100", "datum C notch on rail_1, top close-up", "8", target=(-307, 259, 0), d=(0,0,-1), up=(0,1,0), height=60)
        snap("frame_notch_iso", "R", "100", "datum C notch on rail_1, oblique close-up", "8", target=(-307, 259, 0), d=(-0.7, 0.5, -0.7), up=(0,0,1), height=70)
        rec, plate = split_base(tag)
        loc = [(local(plate, (300, 270, 6), (60, 60, 20)), COL["plate"]), (local(q["frame"], (300, 270, -25), (60, 60, 40)), COL["frame"])]
        scene([(s, c) for s, c in loc if s is not None], 0.1)
        snap("frame_plate_seat_closeup", "R", "100", "plate seated on the frame top plane, +X +Y corner, oblique from outside", "1 8 14", target=(300, 270, -5), d=(-1, -1, -0.5), up=(0,0,1), height=130)
    if wantany("c6_site"):
        scene(items, 0.2)
        for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1)), 1):
            snap("c6_site_%d_top" % i, "R", "100", "C6 site %d (corner %+d %+d): purchased and printed bracket joint, from above" % (i, sx, sy), "9 10",
                 target=(sx*232, sy*215, -30), d=(-sx*0.5, -sy*0.5, -1), up=(0,0,1), height=180)
            snap("c6_site_%d_under" % i, "R", "100", "C6 site %d (corner %+d %+d), from below" % (i, sx, sy), "9 10",
                 target=(sx*232, sy*215, -30), d=(-sx*0.5, -sy*0.5, 1), up=(0,0,1), height=180)
    if wantany("bracket_tnut"):
        out = []
        for s, c in items:
            l = local(s, (173, 215, -30), (45, 45, 40))
            if l is not None: out.append((l, c))
        scene([(s, c) for s, c in out if c != COL["frame"]], 0.1)
        snap("bracket_tnut_closeup", "R", "100", "one bracket with its T-nuts, frame hidden", "9 10", target=(173, 215, -30), d=(-0.6, 0.5, -1), up=(0,0,1), height=110)
        scene(out, 0.1)
        snap("bracket_tnut_in_frame", "R", "100", "one bracket with its T-nuts in the frame, from below", "9 10", target=(173, 215, -30), d=(-0.6, 0.5, 1), up=(0,0,1), height=110)
run(job_frame)

# ---------- accessories, placement only ----------
def job_context():
    if not wantany("context_"): return
    tag = "Kd1_100p0"
    its = whole_items(tag, 75) + [(J["caddy"], COL["caddy"]), (J["gauge"], COL["gauge"]), (J["rest"], COL["rest"])]
    bb = scene(its, 0.5)
    for vn, d, up in VIEWS:
        snap("context_%s" % vn, "Kd1", "100", "jig with caddy, gauge and steady rest, %s (placement only)" % vn, "14", bb=bb, d=d, up=up)
    for nm in ("caddy", "gauge", "rest"):
        bb = scene([(J[nm], COL[nm])], 0.3)
        snap("context_%s_iso" % nm, "Kd1", "100", "%s iso" % nm, "14", bb=bb, d=(-1,1,-1), up=(0,0,1))
run(job_context)

log("RENDER_DONE")
logf.close()
sys.stdout.flush()
os._exit(0)
