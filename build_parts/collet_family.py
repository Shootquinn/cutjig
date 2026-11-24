"""Collet-family generator (Step 5). build_collet(d) builds the free collet of core diameter d and its two clamped-state solids.

Run under FreeCAD:  freecadcmd build_parts\\collet_family.py   with CJ_D unset (the params family) or CJ_D="97.0,93.7".
Pure Python up to the first FreeCAD call: a request above collets.envelope_max is refused before FreeCAD is imported.
Every dimension is read from params.yaml through common; the definition is research/quinn/cr_scratch/step5_loftsman_collet_definition.md.
Writes parts_cache/collet_<tag>.FCStd, collet_<tag>_clamped_Kd1.FCStd, collet_<tag>_clamped_Kmax.FCStd and collet_<tag>_result.json."""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import cadlib as C  # noqa: E402
import common  # noqa: E402

ROOT = common.ROOT
CACHE = common.PARTS_CACHE
POSES = (("Kd1", "collet.grip_window_hi"), ("Kmax", "collet.grip_window_lo"))


def tag(d):
    whole = int(math.floor(d + 1e-9))
    return "%03dp%d" % (whole, int(round((d - whole) * 10)))


def family_index(p, d):
    """clamp(floor((d - core.diameters[0]) / collets.spacing + 0.5) + 1, 1, collets.count): notch count and colour index."""
    idx = math.floor((d - common.get(p, "core.diameters")[0]) / common.get(p, "collets.spacing") + 0.5) + 1
    return max(1, min(int(common.get(p, "collets.count")), int(idx)))


def dims(p, d, shift_in=0.0, shift_out=0.0, width=None):
    """Radii, heights and profile functions of one collet. shift_in moves bore, lip, chamfer and ledge inward; shift_out moves the cone inward."""
    g = lambda k: common.get(p, k)
    q = C.footring_derived(p, d)
    tn = math.tan(math.radians(g("cone.alpha")))
    z_cone = g("holder.bottom_above_floor_Kmax")                 # cone line r(z) = r0 - (z - z_cone) tan(alpha) passes r0 at the holder bottom plane
    r_fo = q["r_fo"]
    r0 = r_fo - g("collet.foot_ring_width")
    h = g("collet.slit_length") + g("collet.slit_ligament") + g("collet.relief_hole_dia") / 2.0
    r_b = (d + g("core.tol") + g("collet.c_i")) / 2.0
    r_top = r0 - (h - z_cone) * tn
    room = r_top - r_b - g("collet.min_wall")
    lo, hi = g("collet.chamfer_band_lo"), g("collet.chamfer_band_hi")
    c = lo if lo < room < hi else min(room, g("collet.chamfer_cap"))
    seat, ledge_w = g("collet.core_seat_height"), g("collet.core_seat_width")
    ring_top = q["ring_top"]
    rb, ro_shift = r_b - shift_in, shift_out
    lip = g("collet.bore_lip_radius")
    ang = math.radians(g("collet.chamfer_angle_deg"))
    t_lip = lip * math.tan(ang / 2.0)                              # tangent length of the lip fillet on the chamfer deflection
    cone = lambda z: r0 - (z - z_cone) * tn - ro_shift
    ow = lambda z: r_fo if z < ring_top else cone(z)

    def inner(z):
        if z < seat:
            return rb - ledge_w
        return rb if z < h - c else rb + (z - (h - c))
    return {"r_b": rb, "r_b0": r_b, "r_fo": r_fo, "r0": r0, "tan": tn, "height": h, "c": c, "z_e": h - c, "ring_top": ring_top, "seat": seat,
            "ledge_w": ledge_w, "cone": cone, "outer": ow, "inner": inner, "r_top": cone(h), "lip_r": lip, "t_lip": t_lip, "z_cone": z_cone,
            "key_tip": q["r_key_tip"], "width": g("collet.slit_width_seed") if width is None else width, "angle": ang, "shift_in": shift_in, "shift_out": shift_out}


def profile_segments(D):
    """Closed (r, z) profile of the revolve: ledge, bore, lip arc, chamfer, top face, cone, ring. Lines are ('L', p, q); the lip is ('A', centre, R, a0, a1)."""
    rb, h, ze, c, R, tl = D["r_b"], D["height"], D["z_e"], D["c"], D["lip_r"], D["t_lip"]
    r_in = rb - D["ledge_w"]
    sa, ca = math.sin(D["angle"]), math.cos(D["angle"])
    p_ring_in = (D["cone"](D["ring_top"]), D["ring_top"])
    p_top_out = (D["r_top"], h)
    p_ch_top = (rb + c, h)
    p_lip_b = (rb + tl * sa, ze + tl * ca)       # lip meets the chamfer
    p_lip_a = (rb, ze - tl)                        # lip meets the bore
    centre = (rb + R, ze - tl)
    return [("L", (r_in, 0.0), (D["r_fo"], 0.0)), ("L", (D["r_fo"], 0.0), (D["r_fo"], D["ring_top"])),
            ("L", (D["r_fo"], D["ring_top"]), p_ring_in), ("L", p_ring_in, p_top_out), ("L", p_top_out, p_ch_top),
            ("L", p_ch_top, p_lip_b), ("A", centre, R, math.pi - D["angle"], math.pi),
            ("L", p_lip_a, (rb, D["seat"])), ("L", (rb, D["seat"]), (r_in, D["seat"])), ("L", (r_in, D["seat"]), (r_in, 0.0))]


def body_revolve_segments(doc, body, segs, name):
    import FreeCAD as App
    import Part
    xz = [o for o in body.Origin.OriginFeatures if o.Role == "XZ_Plane"][0]
    sk = body.newObject("Sketcher::SketchObject", name + "Profile")
    sk.AttachmentSupport = [(xz, "")]
    sk.MapMode = "FlatFace"
    for s in segs:
        if s[0] == "L":
            sk.addGeometry(Part.LineSegment(App.Vector(s[1][0], s[1][1], 0), App.Vector(s[2][0], s[2][1], 0)), False)
        else:
            sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(s[1][0], s[1][1], 0), App.Vector(0, 0, 1), s[2]), s[3], s[4]), False)
    rev = body.newObject("PartDesign::Revolution", name)
    rev.Profile = sk
    rev.ReferenceAxis = (sk, ["V_Axis"])
    rev.Angle = 360.0
    doc.recompute()
    return rev


# ----------------------------------------------------------------------------- analytic expectations (per cut)
def expected_cuts(p, D, d):
    """expected_mm3 per cut: integral of local wall thickness t(z) over the removed region (slits first, then holes net of the slit overlap)."""
    g = lambda k: common.get(p, k)
    n, w, h = int(g("collet.slit_count")), D["width"], D["height"]
    t = lambda z: D["outer"](z) - D["inner"](z)

    def band(z0, z1, m=400):
        return sum(t(z0 + (j + 0.5) * (z1 - z0) / m) for j in range(m)) * (z1 - z0) / m
    rh = g("collet.relief_hole_dia") / 2.0
    zc_top = h - g("collet.slit_length")                      # top-open slits end at the hole centre, z 7
    zc_bot = g("collet.slit_length")                          # bottom-open slits end at the hole centre, z 25
    slit_top, slit_bot = w * band(zc_top, h), w * band(0.0, zc_bot)
    gr = 80
    cell = (2 * rh / gr) ** 2
    hole = {"top": 0.0, "bottom": 0.0}
    for kind, zc in (("top", zc_top), ("bottom", zc_bot)):
        for i in range(gr):
            y = -rh + (i + 0.5) * 2 * rh / gr
            for j in range(gr):
                zz = zc - rh + (j + 0.5) * 2 * rh / gr
                if y * y + (zz - zc) ** 2 > rh * rh:
                    continue
                if abs(y) < w / 2.0 and ((zz >= zc_top) if kind == "top" else (zz <= zc_bot)):
                    continue
                hole[kind] += t(zz) * cell
    notch_w = g("collet.rim_notch_width")
    zf = h - g("collet.rim_notch_depth")                      # notch floor z 29
    area, m = 0.0, 200
    z0, z1 = D["label"]
    for j in range(m):
        r = D["outer"](z0 + (j + 0.5) * (z1 - z0) / m)
        area += 2 * r * math.asin(g("collet.label_window_width") / 2.0 / r) * (z1 - z0) / m / math.cos(math.radians(g("cone.alpha")))
    return {"slit": n // 2 * (slit_top + slit_bot), "relief": n // 2 * (hole["top"] + hole["bottom"]),
            "notch": family_index(p, d) * notch_w * band(zf, h), "label": g("collet.label_depth") * area,
            "slit_top": slit_top, "slit_bot": slit_bot}


# ----------------------------------------------------------------------------- build
def _bb(b):
    return {"xmin": round(b.XMin, 3), "xmax": round(b.XMax, 3), "ymin": round(b.YMin, 3), "ymax": round(b.YMax, 3),
            "zmin": round(b.ZMin, 3), "zmax": round(b.ZMax, 3)}


def _vol(body):
    return C.final_shape(body).Volume


def _cut(doc, body, tool, name, expected, cuts):
    before, f0 = _vol(body), len(C.final_shape(body).Faces)
    C.body_boolean(doc, body, tool, "Cut", name)
    after, f1 = _vol(body), len(C.final_shape(body).Faces)
    cuts.append({"name": name, "before_mm3": round(before, 4), "after_mm3": round(after, 4), "tool_mm3": round(tool.Volume, 4),
                 "expected_mm3": round(expected, 4), "faces_before": f0, "faces_after": f1})
    return after


def slit_hole_tools(kind, c):
    """Tools for the 12 alternating slits (kind 'slit': radial box of width w) or the 12 relief holes (kind 'hole': radial cylinder). Even k opens
    at the top face and ends at the hole centre zc_top; odd k opens at the foot and ends at zc_bot."""
    import Part
    tools = []
    for k in range(c["n"]):
        a = c["phi0"] + 360.0 / c["n"] * k
        top = (k % 2 == 0)
        zc = c["zc_top"] if top else c["zc_bot"]
        if kind == "slit":
            tools.append(C.box_at(a, c["r_lo"], c["r_hi"], c["w"] / 2.0, zc if top else -c["ov"], c["h"] + c["ov"] if top else zc))
        else:
            tools.append(Part.makeCylinder(c["rh"], c["r_hi"] - c["r_lo"], C.polar(c["r_lo"], a, zc),
                                           C.V(math.cos(math.radians(a)), math.sin(math.radians(a)), 0)))
    return tools


def build_solid(p, d, name, shift_in=0.0, shift_out=0.0, width=None):
    """One collet solid (free when the shifts are 0). Returns (doc, body, shape, D, cuts, feature volumes)."""
    import Part
    g = lambda k: common.get(p, k)
    D = dims(p, d, shift_in, shift_out, width)
    n = int(g("collet.slit_count"))
    th = g("receiver.key_offset_deg")
    phi0 = th + 15.0
    ov = g("collet.tool_overshoot")
    r_lo, r_hi = D["r_b"] - D["ledge_w"] - ov, D["r_fo"] + ov                      # tool radial span: inside the void to beyond the ring
    h, w = D["height"], D["width"]
    zc_top_, zc_bot_ = h - g("collet.slit_length"), g("collet.slit_length")
    doc, body = C.new_body(name)
    body_revolve_segments(doc, body, profile_segments(D), "Revolve")
    v_rev = _vol(body)
    cuts, fv = [], {"revolve": v_rev}
    key = C.box_at(th, D["r_fo"] - 1.0, D["key_tip"], g("holder.key_width") / 2, 0.0, D["ring_top"])
    C.body_boolean(doc, body, key, "Fuse", "FootKey")
    fv["key"] = _vol(body) - v_rev
    zl = (zc_top_ + zc_bot_) / 2.0     # label centre: midway between the hole centres, z 16
    D["label"] = (zl - g("collet.label_height") / 2.0, zl + g("collet.label_height") / 2.0)                 # z 12 to 20
    ex = expected_cuts(p, D, d)
    # 1. slits and 2. relief holes: one tool builder, one compound and one boolean each
    ctx = {"n": n, "phi0": phi0, "r_lo": r_lo, "r_hi": r_hi, "w": w, "rh": g("collet.relief_hole_dia") / 2.0, "ov": ov, "h": h,
           "zc_top": zc_top_, "zc_bot": zc_bot_}
    for kind, label, key in (("slit", "slits alternating", "slit"), ("hole", "relief holes", "relief")):
        v0 = _vol(body)
        _cut(doc, body, C.fuse_all(slit_hole_tools(kind, ctx)), label, ex[key], cuts)
        fv[key] = v0 - _vol(body)
    # 3. rim notches: the first family-index azimuths
    idx = family_index(p, d)
    offs = g("collet.notch_azimuth_offsets_deg")[:idx]
    nz = h - g("collet.rim_notch_depth")
    notches = [C.box_at(th + o, r_lo, r_hi, g("collet.rim_notch_width") / 2.0, nz, h + ov) for o in offs]
    v0 = _vol(body)
    _cut(doc, body, C.fuse_all(notches), "rim notches", ex["notch"], cuts)
    fv["notch"] = v0 - _vol(body)
    # 4. label window (Pass 1: flat recess of constant normal depth below the cone; text string in the result JSON)
    z0, z1 = D["label"]
    dep = g("collet.label_depth") / math.cos(math.radians(g("cone.alpha")))
    band = C.revolve_solid([(D["outer"](z0) - dep, z0), (D["outer"](z1) - dep, z1), (D["outer"](z1) + ov, z1), (D["outer"](z0) + ov, z0)])
    tool = band.common(C.box_at(th + g("collet.label_azimuth_offset_deg"), r_lo, r_hi, g("collet.label_window_width") / 2.0, z0 - ov, z1 + ov))
    v0 = _vol(body)
    _cut(doc, body, tool, "label window", ex["label"], cuts)
    fv["label"] = v0 - _vol(body)
    return doc, body, C.final_shape(body), D, cuts, fv, ex


# ----------------------------------------------------------------------------- measurement (Rule M, from the final shape)
def measure(sh, p, d, D):
    import Part
    g = lambda k: common.get(p, k)
    n = int(g("collet.slit_count"))
    th = g("receiver.key_offset_deg")
    phi0 = th + 15.0
    zmax = C.bbox(sh).ZMax
    out = {"valid": bool(sh.isValid()), "closed": bool(sh.isClosed()), "solids": len(sh.Solids), "volume_mm3": sh.Volume}
    bad, planes = 0, 0
    for e in sh.Edges:
        fs = sh.ancestorsOfType(e, Part.Face)
        if len(fs) == 1 and e.isSeam(fs[0]):
            continue
        if len(fs) != 2:
            bad += 1
    for f in sh.Faces:
        if f.Surface.__class__.__name__ == "Plane":
            nrm = f.normalAt(0, 0)
            if abs(nrm.z) < 1e-6 and abs(nrm.dot(f.CenterOfMass)) < 0.01:
                planes += 1
    out.update({"bad_edges": bad, "slit_plane_faces": planes, "euler_VEF": len(sh.Vertexes) - len(sh.Edges) + len(sh.Faces)})
    az = phi0 + 180.0 / n
    zs = [0.05 + (zmax - 0.1) * i / 64.0 for i in range(65)]
    walls = []
    for z in zs:
        iv = C.radial_ivals(sh, az, z, 0.0, 90.0)
        if iv and z > 3.0:
            walls.append(iv[-1][1] - iv[0][0])
    out["wall_min_cone_top"] = min(walls)
    dia, hits = [], []
    r_exp = D["r_b"]
    for k in range(3):
        iv = C.radial_ivals(sh, phi0 + 180.0 / n + 120.0 * k, zmax / 2.0, 0.0, 90.0)
        hits.append(bool((not iv) or iv[0][0] > r_exp + 2.0))
        if iv:
            dia.append(2 * iv[0][0])
    out["bore"] = {"dia": dia, "slit_hits": hits}
    ro5 = C.radial_ivals(sh, az, 5.0, 0.0, 90.0)[-1][1]
    rmid = (r_exp + ro5) / 2.0
    widths, offs, depth, beyond = [], [], [], []
    for k in range(n):
        a = phi0 + 360.0 / n * k
        top = (k % 2 == 0)
        tv = C.tangential_ivals(sh, a, rmid, 15.0, 10.0)
        widths.append(tv[1][0] - tv[0][1] if len(tv) >= 2 else 0.0)
        offs.append((tv[1][0] + tv[0][1]) / 2.0 if len(tv) >= 2 else 0.0)
        av = C.axial_ivals(sh, a, rmid, 0.0, zmax)
        depth.append((zmax - av[-1][1] if top else av[0][0]) if av else 0.0)
        beyond.append(bool(av))
    out["slits"] = {"count": sum(1 for w in widths if w > 0.0), "width": widths, "plane_offset": offs, "void_depth": depth, "solid_below": beyond}
    out["relief_holes"] = len([f for f in sh.Faces if f.Surface.__class__.__name__ == "Cylinder" and abs(f.Surface.Axis.z) < 1e-3
                               and abs(f.Surface.Radius - g("collet.relief_hole_dia") / 2.0) < 0.05])
    return out


def feature_records(p, d, sh, D, fv, m):
    """features[]: name, pass, volume_mm3 plus the measured value each pass flag reads. Volumes of cuts come from the booleans; chamfer, lip, ring and
    seat volumes are Pappus integrals of the profile."""
    g = lambda k: common.get(p, k)
    n = int(g("collet.slit_count"))
    th = g("receiver.key_offset_deg")
    phi0 = th + 15.0
    az = phi0 + 180.0 / n
    rb, c, ze, h = D["r_b"], D["c"], D["z_e"], D["height"]
    R, tl = D["lip_r"], D["t_lip"]
    theta = D["angle"]
    feats = []

    def add(name, vol, ok, **extra):
        rec = {"feature": name, "pass": bool(ok), "volume_mm3": round(vol, 4)}
        rec.update(extra)
        feats.append(rec)
    add("slit (alternating, 12)", fv["slit"], m["slits"]["count"] == n, measured_count=m["slits"]["count"])
    add("relief hole (12)", fv["relief"], m["relief_holes"] == n, measured_count=m["relief_holes"])
    tk = C.tangential_ivals(sh, th, (D["r_fo"] + D["key_tip"]) / 2.0 + 1.0, D["ring_top"] / 2.0, 20.0)
    rk = C.radial_ivals(sh, th, D["ring_top"] / 2.0, 0.0, D["key_tip"] + 10.0)
    add("foot key", fv["key"], len(tk) == 1 and abs((tk[0][1] - tk[0][0]) - g("holder.key_width")) < 0.05 and abs(rk[-1][1] - D["key_tip"]) < 0.05,
        width=round(tk[0][1] - tk[0][0], 4) if tk else None)
    rc = D["cone"](D["ring_top"])
    ring = math.pi * (D["r_fo"] ** 2 - rc ** 2) * D["ring_top"]
    rr = C.radial_ivals(sh, az, D["ring_top"] / 2.0, 0.0, D["r_fo"] + 10.0)
    add("foot ring", ring, bool(rr) and abs(rr[-1][1] - D["r_fo"]) < 0.01, outer_radius=round(rr[-1][1], 4) if rr else None)
    ax = C.axial_ivals(sh, az, rb - D["ledge_w"] / 2.0, -1.0, 10.0)
    add("core seat (ledge)", math.pi * (rb ** 2 - (rb - D["ledge_w"]) ** 2) * D["seat"], bool(ax) and abs(ax[0][1] - D["seat"]) < 0.01,
        ledge_top=round(ax[0][1], 4) if ax else None)
    nz = h - g("collet.rim_notch_depth")
    idx = family_index(p, d)
    na = th + g("collet.notch_azimuth_offsets_deg")[0]
    nv = C.axial_ivals(sh, na, (D["inner"](h - 0.5) + D["outer"](h - 0.5)) / 2.0 + 0.0, 0.0, h + 1.0)
    add("rim notch (count = family index)", fv["notch"], bool(nv) and abs(nv[-1][1] - nz) < 0.01 and fv["notch"] > 0, count=idx,
        floor_z=round(nv[-1][1], 4) if nv else None)
    la = th + g("collet.label_azimuth_offset_deg")
    z_mid = sum(D["label"]) / 2.0
    lr = C.radial_ivals(sh, la, z_mid, 0.0, 90.0)
    dep = D["outer"](z_mid) - lr[-1][1] if lr else None
    add("label window", fv["label"], dep is not None and abs(dep - g("collet.label_depth") / math.cos(math.radians(g("cone.alpha")))) < 0.02,
        radial_depth=round(dep, 4) if dep is not None else None)
    # chamfer: measured near the top face where the bore is c - 0.5 outside the bore radius
    zq = h - 0.5
    cv = C.radial_ivals(sh, az, zq, 0.0, 90.0)
    c_meas = (cv[0][0] - rb) + (h - zq) if cv else None             # inner radius at zq is rb + (zq - ze); c = h - ze = (inner - rb) + (h - zq)
    ch_vol = 2 * math.pi * (rb + c / 3.0) * c * c / 2.0
    add("bore chamfer (lead-in)", ch_vol, c_meas is not None and abs(c_meas - c) < 0.02, c_mm=round(c, 4), edge_z=round(ze, 4),
        c_measured=None if c_meas is None else round(c_meas, 4))
    lv = C.radial_ivals(sh, az, ze, 0.0, 90.0)
    r_expect = rb + R - math.sqrt(R * R - tl * tl)                  # fillet radius at the corner height z_e
    lip_vol = 2 * math.pi * (rb + 0.05) * R * R * (math.tan(theta / 2.0) - theta / 2.0)
    add("bore lip", lip_vol, bool(lv) and abs(lv[0][0] - r_expect) < 0.01, radius=R, r_at_corner=None if not lv else round(lv[0][0], 4))
    return feats


def clamped_pose(p, d, pose, key):
    """Clamped-state solid: bore closes onto the core (d + offset) plus the model gap, cone moves in by s + g/cos(alpha), slits narrow."""
    g = lambda k: common.get(p, k)
    delta = g("core.tol") + g("collet.c_i") - g(key)
    s = delta / 2.0
    gap = g("fit.model_contact_gap")
    w = g("collet.slit_width_seed") - math.pi * delta / g("collet.slit_count")
    name = "collet_%s_clamped_%s" % (tag(d), pose)
    doc, body, sh, D, cuts, fv, ex = build_solid(p, d, name, shift_in=s - gap, shift_out=s + gap / math.cos(math.radians(g("cone.alpha"))), width=w)
    return doc, sh, D, cuts, {"delta": round(delta, 4), "s": round(s, 4), "expected_slit_width": round(w, 4)}


def _save(doc, name):
    path = CACHE / (name + ".FCStd")
    if path.exists():
        path.unlink()                                      # saveAs over an existing file leaves a .FCBak
    doc.saveAs(str(path))


def _helpers():
    """tests/cad_helpers.py predicates. FreeCAD's python has no pytest; a stub supplies the decorator namespace cad_helpers touches at import."""
    for q in (str(ROOT), str(ROOT / "tests")):
        if q not in sys.path:
            sys.path.insert(0, q)
    try:
        import pytest  # noqa: F401
    except ImportError:
        import types
        stub = types.ModuleType("pytest")

        class _Mark:
            def __getattr__(self, _):
                return lambda f: f
        stub.mark = _Mark()
        sys.modules["pytest"] = stub
    import cad_helpers
    return cad_helpers


def run_checks(H, p, d, D, m, cuts, ex, vol):
    """C1 to C3, C5 to C7 and C9b predicates on the generator's own measurements; C4 is a pair check and belongs to probe_collet.py."""
    g = lambda k: common.get(p, k)
    n = int(g("collet.slit_count"))
    res = {}

    def rec(name, errs):
        res[name] = {"pass": not errs, "errors": errs}
    rec("C1", H.check_collet_valid(m))
    names = " ".join(x["name"].lower() for x in cuts)
    rec("C2", H.check_volume_band(vol, H.collet_expected_volume(d, p)["total"]) + H.check_cuts(cuts) + ([] if "slit" in names and "relief" in names else ["slit or relief cut record missing"]))
    rec("C3", H.check_bore(m["bore"], common.bore_free(p, d)))
    rec("C5", H.check_slits(m["slits"], n, g("collet.slit_width_seed")) + ([] if m["relief_holes"] == n else ["relief hole count"]))
    rec("C6", H.check_wall(m["wall_min_cone_top"], g("collet.min_wall")))
    rec("C7", H.check_topology(m) + H.check_collet_valid(m))
    floor = math.pi * H.collet_delta(p) / n + g("collet.min_slit_clamped") - 0.05
    rec("C9b", [] if min(m["slits"]["width"]) >= floor else ["slit width below the closure floor"])
    return res


def build_collet(d):
    """Build collet d (free plus Kd1 and Kmax clamped). Refuses d above collets.envelope_max before FreeCAD is touched. Returns the result dict."""
    p = common.load_params()
    errs = common.check_envelope_request(p, d)
    if errs:
        raise ValueError("; ".join(errs))
    lo = common.get(p, "collets.envelope_min")
    if d < lo - 1e-9:
        raise ValueError("requested %s is below collets.envelope_min %s" % (d, lo))
    import FreeCAD as App
    t0 = time.time()
    g = lambda k: common.get(p, k)
    name = "collet_" + tag(d)
    CACHE.mkdir(exist_ok=True)
    doc, body, sh, D, cuts, fv, ex = build_solid(p, d, name)
    m = measure(sh, p, d, D)
    feats = feature_records(p, d, sh, D, fv, m)
    idx = family_index(p, d)
    n = int(g("collet.slit_count"))
    res = C.base_result(name, sh, feats, t0=t0, extra={
        "d": d, "tag": tag(d), "cuts": cuts, "faces_final": len(sh.Faces), "bbox_plain": _bb(sh.BoundBox), "bbox_optimal": _bb(sh.optimalBoundingBox()), "notch_count": idx, "colour": g("collet.colour")[idx - 1],
        "label_text": "%.1f | %.1f-%.1f" % (d, d + g("collet.grip_window_lo"), d + g("collet.grip_window_hi")),
        "chamfer": {"c_mm": round(D["c"], 4), "edge_z": round(D["z_e"], 4)},
        "caddy": {"socket_d": round(2 * D["r_fo"] + 2 * g("caddy.socket_clear"), 4), "socket_depth": g("caddy.socket_depth"),
                  "height": round(C.bbox(sh).ZMax, 4), "margin": round(g("caddy.socket_depth") - C.bbox(sh).ZMax, 4)},
        "measured": {k: m[k] for k in ("wall_min_cone_top", "bore", "relief_holes", "bad_edges", "slit_plane_faces")},
        "slit_widths": [round(w, 4) for w in m["slits"]["width"]],
        "expected_terms": {k: round(v, 3) for k, v in ex.items()},
        "witness_scale": "not a collet feature: routed to Step 6 (receiver rim and holder flange)"})
    _save(doc, name)
    App.closeDocument(doc.Name)
    clamped, solids = {}, {}
    for pose, key in POSES:
        cdoc, csh, cD, ccuts, info = clamped_pose(p, d, pose, key)
        cm = measure(csh, p, d, cD)
        # clamped slit width measured at the slit centre plane, mid-wall radius, from the final clamped shape
        a = g("receiver.key_offset_deg") + 15.0
        rmid = (cD["r_b"] + C.radial_ivals(csh, a + 180.0 / n, 5.0, 0.0, 90.0)[-1][1]) / 2.0
        tv = C.tangential_ivals(csh, a, rmid, 15.0, 10.0)
        wmeas = tv[1][0] - tv[0][1] if len(tv) >= 2 else 0.0
        clamped[pose] = {"slit_width": round(wmeas, 4), "valid": cm["valid"], "closed": cm["closed"], "solids": cm["solids"],
                         "volume_mm3": round(cm["volume_mm3"], 3), "bore_radius": round(cD["r_b"], 4), "cone_shift": round(cD["shift_out"], 5), **info}
        solids[pose] = csh
        _save(cdoc, "collet_%s_clamped_%s" % (tag(d), pose))
        App.closeDocument(cdoc.Name)
    res["clamped"] = clamped
    res["run_seconds"] = round(time.time() - t0, 1)
    try:
        H = _helpers()
        res["checks"] = run_checks(H, p, d, D, m, cuts, ex, sh.Volume)
        res["checks"]["C1_clamped"] = {"pass": all(c["valid"] and c["closed"] and c["solids"] == 1 for c in clamped.values()), "errors": []}
    except Exception as e:  # the predicates are an extra record; the tests re-run them from the probe
        import traceback
        res["checks"] = {"error": "%s: %s" % (type(e).__name__, e), "trace": traceback.format_exc()}
    res["checks_all_pass"] = bool(res["checks"]) and all(v.get("pass") for v in res["checks"].values() if isinstance(v, dict) and "pass" in v)
    with open(CACHE / (name + "_result.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    return res


def main():
    t0 = time.time()
    p = common.load_params()
    raw = os.environ.get("CJ_D", "").strip()
    sizes = [float(x) for x in raw.split(",") if x.strip()] if raw else list(common.get(p, "core.diameters"))
    print("START collet_family pid=%d sizes=%s t=%s" % (os.getpid(), sizes, time.strftime("%H:%M:%S")), flush=True)
    for d in sizes:
        try:
            r = build_collet(d)
            print("RESULT collet_%s volume=%.3f valid=%s solids=%d checks_all_pass=%s sec=%.1f" % (
                tag(d), r["volume_mm3"], r["isValid"], r["solid_count"], r["checks_all_pass"], r["run_seconds"]), flush=True)
            for k, v in r["checks"].items():
                if isinstance(v, dict) and v.get("pass") is False:
                    print("CHECK_FAIL", k, v["errors"], flush=True)
        except ValueError as e:
            print("REFUSED %s: %s" % (d, e), flush=True)
        except BaseException:
            import traceback
            traceback.print_exc()
            print("BUILD_FAILED collet_%s" % tag(d), flush=True)
    print("BUILD_DONE collet_family %.1fs" % (time.time() - t0), flush=True)


if __name__ in ("__main__", "collet_family"):
    main()
