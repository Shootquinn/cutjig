"""Shared CAD helpers for the Step 3 first solids. Runs inside freecadcmd (imports FreeCAD lazily).

Every dimension comes from params.yaml via common.get. Structural arithmetic only (halves, 2 pi, 360/n).
Rule M: every predicate in a result JSON is computed from the final shape.
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import common  # noqa: E402

ROOT = common.ROOT
CACHE = common.PARTS_CACHE


def params():
    p = common.load_params()
    bad = common._find_printer_keys(p)
    if bad:
        raise SystemExit("printer keys present: %s" % bad)
    return p


def G(p, key):
    return common.get(p, key)


def footring_derived(p, d):
    """Foot-ring and cone radii shared by footring.py and the collet generator (pure arithmetic from params; no FreeCAD)."""
    g = lambda k: G(p, k)
    r_reg = g("receiver.register_bore_radius")
    r_hold = r_reg - g("register.g_reg")
    r_cone_top_holder = r_hold - g("chain.t_h") - g("chain.H") * math.tan(math.radians(g("cone.alpha")))
    d_max = g("core.tol") + g("collet.c_i") - g("collet.grip_window_lo")        # Delta max = 3.5
    r_cone_base = r_cone_top_holder + d_max / 2.0 + g("chain.H") * math.tan(math.radians(g("cone.alpha")))
    return {
        "r_fo": r_reg - g("fit.seat_clearance"),
        "ring_top": g("holder.bottom_above_floor_Kmax") - g("fit.model_contact_gap"),
        "r_bore": (d + g("core.tol") + g("collet.c_i")) / 2.0,
        "r_cone_base": r_cone_base,
        "r_key_tip": r_hold + g("holder.key_height"),
        "r_hold": r_hold,
    }


# ----------------------------------------------------------------- geometry helpers (FreeCAD)
def V(x, y=0.0, z=0.0):
    import FreeCAD as App
    return App.Vector(x, y, z)


def polar(r, deg, z=0.0):
    a = math.radians(deg)
    return V(r * math.cos(a), r * math.sin(a), z)


def revolve_solid(pts):
    """Closed (r, z) polygon revolved 360 deg about Z. Returns a Part shape (tool use)."""
    import Part
    w = Part.makePolygon([V(r, 0, z) for r, z in pts] + [V(pts[0][0], 0, pts[0][1])])
    return Part.Face(w).revolve(V(0, 0, 0), V(0, 0, 1), 360)


def box_at(theta_deg, r0, r1, half_w, z0, z1):
    """Radial box: x' from r0 to r1, y' within +-half_w, z0..z1, rotated by theta about Z."""
    import Part
    b = Part.makeBox(r1 - r0, 2 * half_w, z1 - z0, V(r0, -half_w, z0))
    b.rotate(V(0, 0, 0), V(0, 0, 1), theta_deg)
    return b


def sector_solid(r0, r1, z0, z1, theta_deg, arc_deg):
    """Ring sector centred on theta_deg, spanning arc_deg."""
    import Part
    w = Part.makePolygon([V(r0, 0, z0), V(r1, 0, z0), V(r1, 0, z1), V(r0, 0, z1), V(r0, 0, z0)])
    s = Part.Face(w).revolve(V(0, 0, 0), V(0, 0, 1), arc_deg)
    s.rotate(V(0, 0, 0), V(0, 0, 1), theta_deg - arc_deg / 2.0)
    return s


def fuse_all(shapes):
    """Binary-tree fuse of tool shapes into one (llm_plm_cad 2.6)."""
    shapes = list(shapes)
    while len(shapes) > 1:
        nxt = []
        for i in range(0, len(shapes), 2):
            nxt.append(shapes[i].fuse(shapes[i + 1]) if i + 1 < len(shapes) else shapes[i])
        shapes = nxt
    return shapes[0]


def thread_ridge_ruled(r_axis_pts, pitch, z_lo, z_hi, hand_right=True):
    """Helical ridge (male thread solid) from exact helicoid faces. r_axis_pts: four (r, z') trapezoid corners in order, z' relative to the
    helix start. Each corner follows its own helix (same pitch, radius r, z offset z'); consecutive helices are joined by ruled surfaces,
    and planar end caps close the shell. No profile sweep (a Frenet pipe shell self-intersects: BOP check SelfIntersect), no scaling.
    The start cap lies at azimuth 0, z_lo; the helix runs (z_hi - z_lo) / pitch turns."""
    import Part
    height = z_hi - z_lo
    hel = []
    for r, dz in r_axis_pts:
        h = Part.makeHelix(pitch, height, r, 0, not hand_right)
        h.translate(V(0, 0, z_lo + dz))
        hel.append(h)
    faces = []
    n = len(hel)
    for i in range(n):
        e1, e2 = hel[i].Edges[0], hel[(i + 1) % n].Edges[0]
        faces.append(Part.makeRuledSurface(e1, e2))
    for end in (0, 1):
        pts = [h.Vertexes[0 if end == 0 else -1].Point for h in hel]
        faces.append(Part.Face(Part.makePolygon(pts + [pts[0]])))
    sh = Part.Shell(faces)
    sh.sewShape()
    sol = Part.Solid(sh)
    if sol.Volume < 0:
        sol.reverse()
    return sol


def thread_ridge_stud(r_axis_pts, pitch, z_lo, z_hi, turn_frac=0.25, hand_right=True):
    """Male thread solid (stud ridge) as a fuse of quarter-turn ruled-helicoid segments. One multi-turn ruled BSpline shell makes OCC
    booleans silently no-op (cut removed 1.6 of 23 500 mm3); quarter-turn faces cut correctly and pass the BOP check. Segment k starts at
    z_lo + k * turn_frac * pitch and is rotated to the matching azimuth; adjacent segments share a planar cap, which the fuse removes."""
    out, z = [], z_lo
    while z < z_hi - 1e-9:
        h = min(pitch * turn_frac, z_hi - z)
        sg = thread_ridge_ruled(r_axis_pts, pitch, z, z + h, hand_right)
        sg.rotate(V(0, 0, 0), V(0, 0, 1), 360.0 * (z - z_lo) / pitch * (1 if hand_right else -1))
        out.append(sg)
        z += h
    return fuse_all(out)


def thread_groove_tool(r_axis_pts, pitch, z_lo, z_hi, hand_right=True):
    """Helical groove tool. r_axis_pts: [(r, half_width)] trapezoid corners in the (r, z') plane, z' about the helix start.
    Sweeps along a helix of the given pitch from z_lo to z_hi (tool is longer than the part; caller trims)."""
    import Part
    r_mid = sum(r for r, _ in r_axis_pts) / len(r_axis_pts)
    height = z_hi - z_lo
    helix = Part.makeHelix(pitch, height, r_mid, 0, not hand_right)
    prof = Part.makePolygon([V(r, 0, hw) for r, hw in r_axis_pts] + [V(r_axis_pts[0][0], 0, r_axis_pts[0][1])])
    sweep = Part.Wire(helix).makePipeShell([prof], True, True)
    sweep.translate(V(0, 0, z_lo))
    return sweep


# ----------------------------------------------------------------- Body construction (PartDesign)
def new_body(name):
    import FreeCAD as App
    doc = App.newDocument(name)
    body = doc.addObject("PartDesign::Body", "Body")
    return doc, body


def body_revolve(doc, body, pts, name="Base"):
    """Sketch an (r, z) polygon on the XZ plane and revolve it in the Body (PartDesign::Revolution)."""
    import FreeCAD as App
    import Part
    import Sketcher  # noqa: F401
    xz = [o for o in body.Origin.OriginFeatures if o.Role == "XZ_Plane"][0]
    sk = body.newObject("Sketcher::SketchObject", name + "Profile")
    if hasattr(sk, "AttachmentSupport"):
        sk.AttachmentSupport = [(xz, "")]
    else:
        sk.Support = [(xz, "")]
    sk.MapMode = "FlatFace"
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        sk.addGeometry(Part.LineSegment(App.Vector(a[0], a[1], 0), App.Vector(b[0], b[1], 0)), False)
    rev = body.newObject("PartDesign::Revolution", name)
    rev.Profile = sk
    rev.ReferenceAxis = (sk, ["V_Axis"])
    rev.Angle = 360.0
    doc.recompute()
    return rev


def body_helix_cut(doc, body, pts_rz, pitch, height, name="Thread", reversed_=False):
    """PartDesign::SubtractiveHelix: closed (r, z) profile polygon on the XZ plane swept up a helix of the given pitch."""
    import FreeCAD as App
    import Part
    xz = [o for o in body.Origin.OriginFeatures if o.Role == "XZ_Plane"][0]
    sk = doc.addObject("Sketcher::SketchObject", name + "Profile")
    body.addObject(sk)
    sk.AttachmentSupport = [(xz, "")]
    sk.MapMode = "FlatFace"
    n = len(pts_rz)
    for i in range(n):
        a, b = pts_rz[i], pts_rz[(i + 1) % n]
        sk.addGeometry(Part.LineSegment(App.Vector(a[0], a[1], 0), App.Vector(b[0], b[1], 0)), False)
    h = doc.addObject("PartDesign::SubtractiveHelix", name)
    body.addObject(h)
    h.Profile = sk
    h.ReferenceAxis = (sk, "V_Axis")
    h.Pitch = pitch
    h.Height = height
    h.Mode = 0
    h.Reversed = reversed_
    doc.recompute()
    return h


def body_boolean(doc, body, shape, kind, name, refine=None):
    """One PartDesign::Boolean (Cut or Fuse) consuming one combined OCCT tool shape. refine=False switches off the feature's face-merge pass
    (nut Step 7: the merge pass over the helicoid faces left BOP errors after the thread relief cut); None keeps the document default."""
    tool = doc.addObject("Part::Feature", name + "Tool")
    tool.Shape = shape
    b = body.newObject("PartDesign::Boolean", name)
    b.Type = kind
    b.Group = [tool]
    if refine is not None and hasattr(b, "Refine"):
        b.Refine = bool(refine)
    doc.recompute()
    try:
        tool.Visibility = False
    except Exception:
        pass
    return b


def final_shape(body):
    sh = body.Shape.copy()
    if sh.ShapeType != "Solid" and len(sh.Solids) >= 1:
        sh = max(sh.Solids, key=lambda s: s.Volume)
    return sh


# ----------------------------------------------------------------- measurement (Rule M)
def line_ivals(shape, p0, p1):
    """Intervals [t0, t1] (mm along p0->p1) where the segment lies inside the solid."""
    import Part
    d = p1.sub(p0)
    L = d.Length
    u = V(d.x / L, d.y / L, d.z / L)
    c = shape.common(Part.makeLine(p0, p1))
    out = []
    for e in c.Edges:
        a = e.Vertexes[0].Point.sub(p0).dot(u)
        b = e.Vertexes[-1].Point.sub(p0).dot(u)
        out.append((min(a, b), max(a, b)))
    out.sort()
    merged = []
    for a, b in out:
        if merged and a <= merged[-1][1] + 1e-6:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [tuple(m) for m in merged]


def radial_ivals(shape, theta, z, r0, r1):
    iv = line_ivals(shape, polar(r0, theta, z), polar(r1, theta, z))
    return [(r0 + a, r0 + b) for a, b in iv]


def axial_ivals(shape, theta, r, z0, z1):
    p = polar(r, theta)
    iv = line_ivals(shape, V(p.x, p.y, z0), V(p.x, p.y, z1))
    return [(z0 + a, z0 + b) for a, b in iv]


def tangential_ivals(shape, theta, r, z, half=40.0):
    """Intervals of y' (tangential) along the line at radius r, height z, rotated by theta."""
    c, s = math.cos(math.radians(theta)), math.sin(math.radians(theta))
    p0 = V(r * c + half * s, r * s - half * c, z)
    p1 = V(r * c - half * s, r * s + half * c, z)
    iv = line_ivals(shape, p0, p1)
    return [(a - half, b - half) for a, b in iv]


def chk(name, built, expected, tol=0.05, note=""):
    ok = (built is not None) and abs(built - expected) <= tol
    return {"feature": name, "built": None if built is None else round(built, 4),
            "params": round(expected, 4), "tol": tol, "pass": bool(ok), "note": note}


def flag(name, cond, note=""):
    return {"feature": name, "built": bool(cond), "params": True, "tol": None, "pass": bool(cond), "note": note}


def bbox(shape):
    try:
        return shape.optimalBoundingBox(True, False)
    except Exception:
        return shape.BoundBox


def base_result(part, shape, features, extra=None, t0=None, notes=None):
    bb = bbox(shape)
    com = shape.CenterOfMass
    res = {
        "part": part,
        "volume_mm3": round(shape.Volume, 3),
        "bbox": {"xmin": round(bb.XMin, 3), "xmax": round(bb.XMax, 3), "ymin": round(bb.YMin, 3),
                 "ymax": round(bb.YMax, 3), "zmin": round(bb.ZMin, 3), "zmax": round(bb.ZMax, 3)},
        "isValid": bool(shape.isValid()),
        "isClosed": bool(shape.isClosed()),
        "solid_count": len(shape.Solids),
        "shell_count": len(shape.Shells),
        "genus": None,
        "genus_note": "not computable from the B-rep: faces are annular or periodic, so V-E+F is not an Euler count of discs",
        "euler_VEF": len(shape.Vertexes) - len(shape.Edges) + len(shape.Faces),
        "centre_of_mass": [round(com.x, 3), round(com.y, 3), round(com.z, 3)],
        "features": features,
        "all_features_pass": all(f["pass"] for f in features),
        "build_seconds": None if t0 is None else round(time.time() - t0, 1),
        "notes": notes or [],
    }
    if extra:
        res.update(extra)
    return res


def save(part, doc, body, res):
    CACHE.mkdir(exist_ok=True)
    doc.saveAs(str(CACHE / (part + ".FCStd")))
    with open(CACHE / (part + "_result.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


def run_main(part, builder):
    """Standard __main__: sentinel and PID/start line live in the caller's log; this prints BUILD_DONE."""
    t0 = time.time()
    print("START %s pid=%d t=%s" % (part, os.getpid(), time.strftime("%H:%M:%S")), flush=True)
    try:
        res = builder()
        print("RESULT %s volume=%.3f valid=%s solids=%d pass=%s sec=%.1f" % (
            part, res["volume_mm3"], res["isValid"], res["solid_count"], res["all_features_pass"], time.time() - t0), flush=True)
        for f in res["features"]:
            if not f["pass"]:
                print("FEATURE_FAIL", f, flush=True)
    except BaseException:
        import traceback
        traceback.print_exc()
        print("BUILD_FAILED %s" % part, flush=True)
    print("BUILD_DONE %s" % part, flush=True)
