"""A1a and the pose-dependent measures: for every parts_cache/assembly/pose_<P>_<tag>.FCStd, the 45 part pairs
(min distance, overlap volume, contact area), the six feature-pair gaps, and the measures below. Objects are found by Label equal to the
ASSEMBLY.md part name (base, holder, collet, nut, washer, core, frame, bracket, tnut, cutter). Output results/probes/pose_<P>_<tag>.json
with keys pairs, feature_pairs, measures, controls, absent, tree, visible_count. Nothing is saved to any document.
A measure whose object is missing is not written; it is listed under "absent" with the reason, and the test reports ABSENT FEATURE.
Every measure with a control writes controls[key] = {"good": the measured value, "bad": the value on a known-bad variant built inside the probe};
tests/test_step7_assembly.py asserts that the threshold passes the good value and fires on the bad one.

MEASURE DEFINITIONS (units mm, mm2, mm3, degrees; z up; sign stated; shapes are the built final shapes, Rule M)
 floor_z                    z of the first solid top on the vertical line (r 50, azimuth key_offset+180) through base. Reads: base.
 holder_bottom_above_floor  holder ZMin - floor_z. Positive = holder above the floor. Reads: holder, base.
 nut_skirt_bottom_above_floor  nut ZMin - floor_z (A3h, A3i neighbours). Reads: nut, base.
 engaged_mm                 overlap of the axial thread zone of nut and base: tooth-sized solid intervals (< pitch long) on the circle at the
                            pitch radius, six azimuths 30 deg apart; min(top) - max(bottom) of the two zones, floored at 0. Reads: nut, base.
 core_axis_offset (A3c)     hypot(x, y) of the centroid of the core cross-section at the mid-height of the collet; the datum B axis is x = y = 0.
                            Reads: core, collet. Control bad: the core translated 1.0 mm in +X.
 clamped_tilt_deg (A3f)     atan(hypot(dx, dy) / dz) between the core cross-section centroids at z_a = collet ZMin + 0.25 collet height and
                            z_b = core ZMax - 20. Always >= 0. Reads: core, collet. Control bad: the core turned 1.0 deg about X through (0, 0, z_a).
 lead_in_bore_radius        smallest coaxial cylindrical face radius of cutter (the lead-in working bore, icd.core_lead_in_bore). Reads: cutter.
 lead_in_clearance (A3d)    lead_in_bore_radius - core radius (half the X extent of the core cross-section at the collet mid-height).
                            Reads: cutter, core. Control bad: core radius + 5.
 funnel_capture_radius (A3g)  largest circular edge radius on a Z-axis cone face of cutter (the funnel mouth) - core radius. Reads: cutter, core.
                            Control bad: core radius + 20.
 receiver_underside_contact_mm2 (A6a)  area of base faces with outward normal -Z and centre radius < receiver.spigot_od / 2 that lie within 0.01 mm
                            of a face of frame (sum of the smaller face of each touching pair). Reads: base, frame.
                            Control bad: a 20 x 20 x 5 block centred under the first vertex of the first such face.
 frame_footprint_x / _y (P6b)  X and Y extent of the frame bounding box (optimal). Reads: frame.
                            Control bad (y): extent with the solid of lowest YMin removed.
 slit_width_clamped_min (T5)  smallest slit width over the collet.slit_count slits (azimuth key_offset + 15 + 360 k / N): tangential gap
                            between solid intervals at the slit-free mid radius, z = top-3 (even k) or 5 (odd k). Reads: collet.
                            Control bad: the same read at azimuth + 180 / N deg (midway between slits; must return 0).
 nut_stop_travel_mm (S12)   Revision 1 physical stop: lower the nut along S(phi) = Rz(phi) T(0,0,L phi / 2 pi), phi = -360 t / L, in 0.25 mm steps to the first
                            base|nut common volume >= 0.01 mm3, then bisect to 0.01 mm; the value is that t. Expected 10.01 at Kmax (requirement >= thread.pitch).
                            Reads: nut, base. Control bad: the nut with its relief bore filled (r receiver.register_bore_radius to nut.relief_r, nut z relief_z to the plate underside) must read about 4.0.
 collet_volume_mm3          volume of the collet object; equals collet_<tag>_result.json volume_mm3 (R) or clamped.<pose>.volume_mm3 (G7). Reads: collet.
 nut_tilt_deg, holder_tilt_deg (T9 in the WS probe)  angle between Z and the axis of the largest cylindrical face of the part. Reads: nut, holder.
                            Control bad: the part turned 1.0 deg about X.
 fit_spigot_hole (A3b, green_at_7)  plate-hole cylinder radius (first coaxial Z cylinder in (r_spigot, r_spigot + 2)) - receiver spigot cylinder radius. Reads: base.
 fit_plate_key_stop_pin (A3b, green_at_7)  max((key pocket width - base.key_width) / 2, pin gap); absent until base.key_width/pin keys and faces exist.
 fit_column_foot, fit_carriage_guide (A3b, green_at_12)  not written; listed under "absent".
Per-instance pairs (G4) are written once, from pose R at the nominal size, to results/probes/frame_instances.json:
 {pairs: {"a|b": {overlap_mm3, min_dist}} for every instance pair whose enlarged bounding boxes meet, counts{member,bracket,tnut}, scanned,
  bbox_skipped, per_bracket_tnuts{bracket: [tnut names touching it, min_dist <= 0.01]}}. Instance names come from results/assembly_poses.json
 "instances" (member, bracket, tnut lists in the solid order of the compound objects frame, bracket, tnut).
Run: freecadcmd tests/probes/probe_poses.py   (heavy: one boolean and one distance per pair per pose; detach it)
Smoke override: CJ_POSE_DIR, CJ_OUT, CJ_LEDGER redirect input, output and ledger."""
import glob
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib as L  # noqa: E402
import gates  # noqa: E402
C = L.C
if os.environ.get("CJ_OUT"):
    L.OUT = os.environ["CJ_OUT"]
TILT_CONTROL_DEG = 2.0   # known-bad tilt for nut_tilt_deg / holder_tilt_deg: above register.tilt_limit_deg 1.021 (a 1.0 deg control read below the limit and could not fire)
POSE_DIR = os.environ.get("CJ_POSE_DIR", os.path.join(L.CACHE, "assembly"))
LEDGER = os.environ.get("CJ_LEDGER", os.path.join(L.ROOT, "results", "assembly_poses.json"))


def _has(p, key):
    try:
        L.G(p, key)
        return True
    except KeyError:
        return False


class InvalidCommon(RuntimeError):
    """A boolean common whose result is not a valid shape: the measurement failed; it is never read as 0.0 mm3."""


def checked_common(a, b, label=""):
    c = a.common(b)
    if not c.isValid():
        raise InvalidCommon("common(%s) returned an invalid shape" % label)
    return c


def part_pairs():
    rels, _ = gates.parse_assembly()
    return [(r["a"], r["b"]) for r in rels]


def contact_area(a_shape, b_shape, tol=0.01):
    """Sum over face pairs closer than tol of the common-face intersection area (planar and conical patches). Inputs are shapes or face lists; solid pairs
    and face pairs whose enlarged bounding boxes miss are skipped."""
    def groups(x):
        if isinstance(x, list):
            return [x]
        return [list(s.Faces) for s in x.Solids] or [list(x.Faces)]
    total = 0.0
    for ga in groups(a_shape):
        bga = None
        for gb in groups(b_shape):
            if bga is None:
                bga = [(f, f.BoundBox) for f in ga]
            bgb = [(f, f.BoundBox) for f in gb]
            for fa, ba in bga:
                for fb, bb in bgb:
                    if ba.XMax + tol < bb.XMin or bb.XMax + tol < ba.XMin or ba.YMax + tol < bb.YMin or bb.YMax + tol < ba.YMin                             or ba.ZMax + tol < bb.ZMin or bb.ZMax + tol < ba.ZMin:
                        continue
                    if fa.distToShape(fb)[0] <= tol:
                        # Revision 1: area of the shared face (common-face intersection); the smaller face area over-counts partial overlaps
                        # (holder|nut R read 9,978 against a 3,694 geometric maximum).
                        total += patch_area(fa, fb, tol)
    return total


def patch_area(fa, fb, tol=0.01, n=24):
    """Contact patch of two faces closer than tol. Faces that touch exactly: area of the common face. Faces held apart by the modelled contact gap
    (fit.model_contact_gap 0.005) have an empty common face: parallel planes are brought together along the normal and intersected; other surfaces
    take fa.Area times the fraction of an n x n parameter grid on fa that lies within tol of fb."""
    import Part
    try:
        a = checked_common(fa, fb, "face pair").Area
        if a > 0.0:
            return a
    except InvalidCommon:
        raise
    except Exception:
        pass
    try:
        if fa.Surface.__class__.__name__ == "Plane" and fb.Surface.__class__.__name__ == "Plane":
            n1, n2 = fa.Surface.Axis, fb.Surface.Axis
            if abs(abs(n1.dot(n2)) - 1.0) < 1e-9:
                fb2 = fb.copy()
                fb2.translate(n1 * n1.dot(fa.Surface.Position - fb.Surface.Position))
                return checked_common(fa, fb2, "parallel faces").Area
    except InvalidCommon:
        raise
    except Exception:
        pass
    u0, u1, v0, v1 = fa.ParameterRange
    ins = hit = 0
    for i in range(n):
        for j in range(n):
            u, v = u0 + (u1 - u0) * (i + 0.5) / n, v0 + (v1 - v0) * (j + 0.5) / n
            if not fa.isPartOfDomain(u, v):
                continue
            ins += 1
            if Part.Vertex(fa.valueAt(u, v)).distToShape(fb)[0] <= tol:
                hit += 1
    return fa.Area * hit / ins if ins else 0.0


def solid_dist(a, b):
    """Minimum distance between two shapes, evaluated per solid pair in order of bounding-box separation; a pair whose box gap is at least the best
    distance found is skipped (the box gap is a lower bound, so the value equals a.distToShape(b)[0])."""
    sa, sb = list(a.Solids) or [a], list(b.Solids) or [b]
    cand = []
    for x in sa:
        bx = x.BoundBox
        for y in sb:
            by = y.BoundBox
            gx = max(0.0, bx.XMin - by.XMax, by.XMin - bx.XMax)
            gy = max(0.0, bx.YMin - by.YMax, by.YMin - bx.YMax)
            gz = max(0.0, bx.ZMin - by.ZMax, by.ZMin - bx.ZMax)
            cand.append((math.sqrt(gx * gx + gy * gy + gz * gz), x, y))
    cand.sort(key=lambda c: c[0])
    best = float("inf")
    for lb, x, y in cand:
        if lb >= best:
            break
        best = min(best, x.distToShape(y)[0])
        if best <= 0.0:
            break
    return best


def zone(sh, theta_list, r, pitch):
    """Axial extent of tooth-sized solid intervals at radius r (the thread zone)."""
    lo, hi = None, None
    for t in theta_list:
        for a, b in C.axial_ivals(sh, t, r, sh.BoundBox.ZMin, sh.BoundBox.ZMax):
            if b - a < pitch:
                lo = a if lo is None else min(lo, a)
                hi = b if hi is None else max(hi, b)
    return (lo, hi) if lo is not None else None


def screwed(shape, t, lead):
    """shape moved down by t along the screw motion: Rz(phi) T(0,0,-t), phi = -360 t / lead."""
    s = shape.copy()
    s.translate(C.V(0, 0, -t))
    s.rotate(C.V(0, 0, 0), C.V(0, 0, 1), -360.0 * t / lead)
    return s


def stop_travel(nut, base, lead, step=0.25, limit=30.0):
    """Smallest descent t at which nut and base share >= 0.01 mm3 (stepped at 0.25, bisected to 0.01); None when the limit is reached."""
    t_free, t = 0.0, step
    while t <= limit:
        if checked_common(screwed(nut, t, lead), base, "stop travel").Volume >= 0.01:
            lo, hi = t_free, t
            while hi - lo > 0.01:
                mid = (lo + hi) / 2.0
                lo, hi = (mid, hi) if checked_common(screwed(nut, mid, lead), base, "stop travel").Volume < 0.01 else (lo, mid)
            return hi
        t_free, t = t, t + step
    return None


def sect(shape, z):
    """(centroid Vector, half X extent) of the largest cross-section wire of shape at height z, or None."""
    import Part
    ws = shape.slice(C.V(0, 0, 1), z)
    if not ws:
        return None
    f = Part.Face(max(ws, key=lambda w: w.BoundBox.DiagonalLength))
    return f.CenterOfMass, f.BoundBox.XLength / 2.0


def tilt_between(sh, za, zb):
    a, b = sect(sh, za), sect(sh, zb)
    if a is None or b is None or zb == za:
        return None
    return math.degrees(math.atan2(math.hypot(b[0].x - a[0].x, b[0].y - a[0].y), zb - za))


def axis_tilt(shape):
    cyl = [f for f in shape.Faces if f.Surface.__class__.__name__ == "Cylinder" and f.Area > 1000.0]
    if not cyl:
        return None
    ax = max(cyl, key=lambda f: f.Area).Surface.Axis
    return math.degrees(math.acos(min(1.0, abs(ax.z))))


def turned(shape, deg, pivot=(0, 0, 0)):
    s = shape.copy()
    s.rotate(C.V(*pivot), C.V(1, 0, 0), deg)
    return s


def z_cylinders(shape):
    return [f.Surface.Radius for f in shape.Faces if f.Surface.__class__.__name__ == "Cylinder" and abs(abs(f.Surface.Axis.z) - 1.0) < 1e-6
            and math.hypot(f.Surface.Center.x, f.Surface.Center.y) < 1e-3]


def funnel_mouth(shape):
    r = [e.Curve.Radius for f in shape.Faces if f.Surface.__class__.__name__ == "Cone" and abs(abs(f.Surface.Axis.z) - 1.0) < 1e-6
         for e in f.Edges if e.Curve.__class__.__name__ == "Circle"]
    return max(r) if r else None


def slit_widths(col, phi0, n):
    """Width of each slit: tangential gap between solid intervals at the mid wall radius (probe_collet.py method)."""
    zmax = C.bbox(col).ZMax
    out = []
    for k in range(n):
        a = phi0 + 360.0 / n * k
        top = (k % 2 == 0)
        z = zmax - 3.0 if top else C.bbox(col).ZMin + 5.0  # odd slits: 5 mm above the collet bottom (absolute 5.0 read 0.0 for a collet at z 40)
        free = C.radial_ivals(col, a + 180.0 / n, z, 0.0, 90.0)
        if not free:
            out.append(0.0)
            continue
        rmid = (free[0][0] + free[0][1]) / 2.0
        tv = C.tangential_ivals(col, a, rmid, z, 10.0)
        out.append(tv[1][0] - tv[0][1] if len(tv) >= 2 else 0.0)
    return out


def spigot_fit(base, r_sp):
    """Plate-hole cylinder radius (first coaxial Z cylinder in (r_sp, r_sp + 2)) minus the spigot cylinder radius; None when either face is absent."""
    rr = sorted(z_cylinders(base))
    hole = [r for r in rr if r_sp + 1e-6 < r < r_sp + 2.0]
    spig = [r for r in rr if abs(r - r_sp) < 1e-3]
    return min(hole) - max(spig) if hole and spig else None


def key_pin_fit(base, G):
    """max((key pocket width - base.key_width) / 2, stop pin gap), read on a line through each pocket at mid pocket depth; None when a pocket is not found."""
    kx, ky = G("base.key_pocket_xy")
    px, py = G("base.pin_pocket_xy")
    zc = C.bbox(base).ZMin + G("base.pocket_depth") / 2.0
    half = 2.0 * G("base.key_pocket_size")
    kiv = C.line_ivals(base, C.V(kx - half, ky, zc), C.V(kx + half, ky, zc))
    piv = C.line_ivals(base, C.V(px - 2.0 * half, py, zc), C.V(px + 2.0 * half, py, zc))
    if len(kiv) != 2 or len(piv) != 2:
        return None
    pin_gap = (px - 2.0 * half + piv[0][1]) - (G("base.pin_x") - G("base.pin_dia") / 2.0)
    return max((kiv[1][0] - kiv[0][1] - G("base.key_width")) / 2.0, pin_gap)


def analyse(sh, p, pairs):
    """pairs, feature_pairs, measures, controls, absent for one dict {Label: shape}."""
    G = lambda k: L.G(p, k)
    pitch = G("thread.pitch")
    r_pitch = (G("thread.major") - G("chain.h")) / 2.0
    out = {"pairs": {}, "feature_pairs": {}, "measures": {}, "controls": {}, "absent": {}}
    for a, b in pairs:
        if a in sh and b in sh:
            md = solid_dist(sh[a], sh[b])
            out["pairs"]["%s|%s" % (a, b)] = {"min_dist": md, "overlap_mm3": checked_common(sh[a], sh[b], "%s|%s" % (a, b)).Volume,
                                              "contact_area_mm2": contact_area(sh[a], sh[b]) if md <= 0.01 else 0.0}
    ms, ctl, ab = out["measures"], out["controls"], out["absent"]
    zlo = lambda s: C.bbox(sh[s]).ZMin
    zhi = lambda s: C.bbox(sh[s]).ZMax

    def need(name, *objs):
        miss = [o for o in objs if o not in sh]
        if miss:
            ab[name] = "ABSENT FEATURE: object %s" % ",".join(miss)
        return not miss

    def put(name, good, bad=None):
        if good is None:
            ab[name] = "ABSENT FEATURE: could not read %s from the built shape" % name
            return
        ms[name] = good
        if bad is not None:
            ctl[name] = {"good": good, "bad": bad}
    clr = G("receiver.key_offset_deg") + 180.0                 # azimuth clear of every key
    fp = out["feature_pairs"]
    nz = None
    if "base" in sh:
        iv = C.axial_ivals(sh["base"], clr, 50.0, zlo("base") - 1, zhi("base") + 1)
        fl = iv[0][1] if iv else None
        ms["floor_z"] = fl
        rim = C.axial_ivals(sh["base"], clr, 69.5, zlo("base") - 1, zhi("base") + 1)
        if fl is not None and "holder" in sh:
            ms["holder_bottom_above_floor"] = zlo("holder") - fl
            ms["collar_top_z"] = max(zhi("holder"), zhi("nut")) if "nut" in sh else zhi("holder")
            fp["holder bottom|receiver floor"] = {"gap": zlo("holder") - fl}
            if rim:
                r_f = (G("holder.flange_od") / 2.0 + G("receiver.register_bore_radius")) / 2.0
                under = C.axial_ivals(sh["holder"], clr, r_f, zlo("holder") - 1, zhi("holder") + 1)
                if under:
                    fp["holder flange underside|receiver rim"] = {"gap": under[0][0] - rim[-1][1]}
        if fl is not None and "nut" in sh:
            ms["nut_skirt_bottom_above_floor"] = zlo("nut") - fl
            fp["nut skirt bottom|receiver floor"] = {"gap": zlo("nut") - fl}
            azs = [30.0 * k for k in range(6)]
            zn, zr = zone(sh["nut"], azs, r_pitch, pitch), zone(sh["base"], azs, r_pitch, pitch)
            ms["engaged_mm"] = max(0.0, min(zn[1], zr[1]) - max(zn[0], zr[0])) if zn and zr else 0.0
            if _has(p, "nut.relief_r"):
                lead = G("thread.pitch")
                import Part
                zl = zlo("nut")
                z_fill = zl + G("nut.relief_z")                                                      # relief floor
                h_fill = G("nut.length") + G("washer.thickness") - G("nut.washer_pocket_depth") - G("nut.relief_z")   # up to the plate underside
                fill = Part.makeCylinder(G("nut.relief_r"), h_fill, C.V(0, 0, z_fill)).cut(Part.makeCylinder(G("receiver.register_bore_radius"), h_fill, C.V(0, 0, z_fill)))
                put("nut_stop_travel_mm", stop_travel(sh["nut"], sh["base"], lead), stop_travel(sh["nut"].fuse(fill), sh["base"], lead))
            else:
                ab["nut_stop_travel_mm"] = "ABSENT FEATURE: params key nut.relief_r (nut thread relief, Revision 1)"
        if "holder" in sh and "nut" in sh:
            if _has(p, "collar.thickness"):
                # the pose fuses the collar ring into holder: collar underside = holder top - collar.thickness (holder top alone reads the collar top)
                fp["nut plate top|holder collar underside"] = {"gap": zhi("holder") - G("collar.thickness") - zhi("nut")}
            else:
                ab["nut plate top|holder collar underside"] = "ABSENT FEATURE: params key collar.thickness"
        if "nut" in sh and "cutter" in sh:
            fp["nut collar top|cutter lowest point"] = {"gap": zlo("cutter") - ms.get("collar_top_z", zhi("nut"))}
    if "collet" in sh and "holder" in sh:
        r_ring = G("receiver.register_bore_radius") - G("fit.seat_clearance") - G("collet.foot_ring_width") / 2.0
        ring = C.axial_ivals(sh["collet"], clr, r_ring, zlo("collet") - 1, zhi("collet") + 1)
        if ring:
            fp["holder bottom|collet foot ring top"] = {"gap": zlo("holder") - ring[0][1]}
    # --- Step 7 measures
    if need("core_axis_offset", "core", "collet"):
        zm = (zlo("collet") + zhi("collet")) / 2.0
        s0 = sect(sh["core"], zm)
        sb = sect(L.moved(sh["core"], 1.0), zm)
        put("core_axis_offset", None if s0 is None else math.hypot(s0[0].x, s0[0].y), None if sb is None else math.hypot(sb[0].x, sb[0].y))
        za = zlo("collet") + 0.25 * (zhi("collet") - zlo("collet"))
        put("clamped_tilt_deg", tilt_between(sh["core"], za, zhi("core") - 20.0), tilt_between(turned(sh["core"], 1.0, (0, 0, za)), za, zhi("core") - 20.0))
        if s0 is not None and "cutter" in sh:
            radii = z_cylinders(sh["cutter"])
            mouth = funnel_mouth(sh["cutter"])
            if radii:
                put("lead_in_bore_radius", min(radii))
                put("lead_in_clearance", min(radii) - s0[1], min(radii) - (s0[1] + 5.0))
            else:
                ab["lead_in_clearance"] = "ABSENT FEATURE: no coaxial cylinder face on cutter (lead-in working bore)"
            if mouth is not None:
                put("funnel_capture_radius", mouth - s0[1], mouth - (s0[1] + 20.0))
            else:
                ab["funnel_capture_radius"] = "ABSENT FEATURE: no Z-axis cone face with a circular rim on cutter (funnel)"
        else:
            for k in ("lead_in_clearance", "funnel_capture_radius"):
                ab[k] = "ABSENT FEATURE: object cutter" if "cutter" not in sh else "ABSENT FEATURE: core section"
    else:
        for k in ("clamped_tilt_deg", "lead_in_clearance", "funnel_capture_radius"):
            ab[k] = ab["core_axis_offset"]
    if need("receiver_underside_contact_mm2", "base", "frame"):
        r_sel = G("receiver.spigot_od") / 2.0
        under = [f for f in sh["base"].Faces if f.Surface.__class__.__name__ == "Plane" and f.normalAt(0, 0).z < -0.99
                 and max(abs(f.BoundBox.XMin), abs(f.BoundBox.XMax), abs(f.BoundBox.YMin), abs(f.BoundBox.YMax)) <= r_sel + 1e-6]   # face lies inside the receiver spigot radius (the plate underside has its centre of mass there but spans the plate)
        if under:
            import Part
            c = under[0].Vertexes[0].Point
            blk = Part.makeBox(20, 20, 5, C.V(c.x - 10, c.y - 10, c.z - 5))
            put("receiver_underside_contact_mm2", contact_area(under, sh["frame"]), contact_area(under, blk))
        else:
            ab["receiver_underside_contact_mm2"] = "ABSENT FEATURE: no downward planar face of base inside the receiver spigot radius"
    if need("frame_footprint_x", "frame"):
        bb = C.bbox(sh["frame"])
        ms["frame_footprint_x"], ms["frame_footprint_y"] = bb.XLength, bb.YLength
        rest = sorted(sh["frame"].Solids, key=lambda s: s.BoundBox.YMin)[1:]
        if rest:
            import Part
            ctl["frame_footprint_y"] = {"good": bb.YLength, "bad": Part.makeCompound(rest).BoundBox.YLength}
        restx = [s for s in sh["frame"].Solids if s.BoundBox.XLength < 0.9 * bb.XLength]      # known-bad: both full-length rails removed (dropping one leaves the other spanning x)
        if restx:
            import Part
            ctl["frame_footprint_x"] = {"good": bb.XLength, "bad": Part.makeCompound(restx).BoundBox.XLength}
    else:
        ab["frame_footprint_y"] = ab["frame_footprint_x"]
    if need("collet_volume_mm3", "collet"):
        put("collet_volume_mm3", sh["collet"].Volume)
    if need("slit_width_clamped_min", "collet"):
        n, phi0 = int(G("collet.slit_count")), G("receiver.key_offset_deg") + 15.0
        w = slit_widths(sh["collet"], phi0, n)
        put("slit_width_clamped_min", min(w), min(slit_widths(sh["collet"], phi0 + 180.0 / n, n)))
    for nm, key in (("nut", "nut_tilt_deg"), ("holder", "holder_tilt_deg")):
        if need(key, nm):
            put(key, axis_tilt(sh[nm]), axis_tilt(turned(sh[nm], TILT_CONTROL_DEG)))
    if "base" in sh:
        # A3b at 7: spigot fit = radius of the plate-hole cylinder face just outside the receiver spigot face (base keeps both solids, 0.2 radial gap)
        r_sp = G("receiver.spigot_od") / 2.0
        good = spigot_fit(sh["base"], r_sp)
        if good is not None:
            import Part
            # known-bad: receiver proxy cylinder in a plate whose hole is 0.6 mm too large
            bad_base = Part.makeCompound([Part.makeCylinder(r_sp, 20.0), Part.makeCylinder(3.0 * r_sp, 12.0).cut(Part.makeCylinder(r_sp + 0.6, 12.0))])
            put("fit_spigot_hole", good, spigot_fit(bad_base, r_sp))
        else:
            ab["fit_spigot_hole"] = "ABSENT FEATURE: base lacks coaxial cylinder faces at the receiver spigot radius and the plate hole radius"
    else:
        ab["fit_spigot_hole"] = "ABSENT FEATURE: object base"
    if "base" in sh and all(_has(p, k) for k in ("base.key_width", "base.pin_dia", "base.pin_x")):
        # A3b at 7: plate key fit = (key pocket width read from base - base.key_width) / 2; stop pin gap = pin pocket wall x - (base.pin_x - base.pin_dia / 2); value = the larger
        good = key_pin_fit(sh["base"], G)
        if good is not None:
            import Part
            kx, ky = G("base.key_pocket_xy")
            kp, pd = G("base.key_pocket_size"), G("base.pocket_depth")
            wide = sh["base"].cut(Part.makeBox(kp + 1.0, kp + 1.0, pd, C.V(kx - (kp + 1.0) / 2.0, ky - (kp + 1.0) / 2.0, zlo("base"))))   # known-bad: key pocket 1.0 mm too wide
            put("fit_plate_key_stop_pin", good, key_pin_fit(wide, G))
        else:
            ab["fit_plate_key_stop_pin"] = "ABSENT FEATURE: key pocket (2 solid intervals) or stop pin pocket (2 intervals) not found in base"
    else:
        ab["fit_plate_key_stop_pin"] = "ABSENT FEATURE: object base or params keys base.key_width, base.pin_dia, base.pin_x"
    for k in ("fit_column_foot", "fit_carriage_guide"):
        ab[k] = "ABSENT FEATURE: %s needs a separate spigot, key, pin, column foot or carriage guide object; none is in the 10-part tree" % k
    return out


def instances(doc, sh, ledger_path):
    """Per-instance pair table for pose R (G4)."""
    import json
    led = json.load(open(ledger_path, encoding="utf-8"))
    names = led["instances"]
    solids = {"member": sh["frame"].Solids, "bracket": sh["bracket"].Solids, "tnut": sh["tnut"].Solids}
    items = []
    for kind in ("member", "bracket", "tnut"):
        nm = names[kind]
        if len(nm) != len(solids[kind]):
            raise RuntimeError("instance list %s has %d names for %d solids" % (kind, len(nm), len(solids[kind])))
        items += list(zip(nm, solids[kind]))
    res = {"pairs": {}, "counts": {k: len(v) for k, v in names.items() if k in solids}, "scanned": 0, "bbox_skipped": 0, "per_bracket_tnuts": {}}
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            (na, a), (nb, b) = items[i], items[j]
            ba = a.BoundBox
            ba.enlarge(0.01)
            res["scanned"] += 1
            if not ba.intersect(b.BoundBox):
                res["bbox_skipped"] += 1
                continue
            md = a.distToShape(b)[0]
            res["pairs"]["%s|%s" % (na, nb)] = {"overlap_mm3": checked_common(a, b, "%s|%s" % (na, nb)).Volume, "min_dist": md}
            if gates.pair_kind(na, nb) == "bracket|tnut" and md <= 0.01:
                br, tn = (na, nb) if na.startswith("bracket") else (nb, na)
                res["per_bracket_tnuts"].setdefault(br, []).append(tn)
    return res


def main():
    p = L.params()
    pairs = part_pairs()
    nominal = L.G(p, "core.diameter_nominal")
    nom_tag = "%03dp%d" % (int(math.floor(nominal + 1e-9)), int(round((nominal - math.floor(nominal + 1e-9)) * 10)))
    inputs = sorted(glob.glob(os.path.join(POSE_DIR, "pose_*_*.FCStd")))
    for path in inputs:
        m = re.match(r"pose_(R|Kd1|Kmax)_(.+)\.FCStd$", os.path.basename(path))
        if not m:
            continue
        import FreeCAD as App
        doc = App.openDocument(path)
        sh = {o.Label: C.final_shape(o) if o.TypeId == "PartDesign::Body" else o.Shape.copy() for o in doc.Objects
              if hasattr(o, "Shape") and o.Shape.Solids}
        out = {"pose": m.group(1), "tag": m.group(2), "tree": sorted(sh), "visible_count": len(sh)}
        out.update(analyse(sh, p, pairs))
        L.finish("pose_%s_%s" % (m.group(1), m.group(2)), out, [path])
        if m.group(1) == "R" and m.group(2) == nom_tag and all(k in sh for k in ("frame", "bracket", "tnut")) and os.path.exists(LEDGER):
            L.finish("frame_instances", instances(doc, sh, LEDGER), [path, LEDGER])
        App.closeDocument(doc.Name)


if __name__ in ("__main__", "probe_poses") and not os.environ.get("CJ_PROBE_IMPORT"):   # probe_ws sets CJ_PROBE_IMPORT before importing this module
    L.guarded(main, "poses")
