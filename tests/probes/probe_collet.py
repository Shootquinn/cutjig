"""C-group, F1, F2, F3, F5, A3a inputs for every collet in parts_cache (family from core.diameters plus the off-grid sizes in
CJ_EXTRA, default "97.0,93.7"). A missing collet FCStd is skipped (the tests then report MISSING). Writes
results/probes/collet_<tag>.json per collet and results/probes/collet_family.json (C4 pair data).
Axis is Z, open face at the bbox top, foot ring at z 0. Slit centres sit at receiver.key_offset_deg + 15 + 360/N k (ASSEMBLY.md).
Clamped-state solids for F1 are parts_cache/collet_<tag>_clamped_Kd1.FCStd and _clamped_Kmax.FCStd (generator output, Step 5).
Built at Step 4 against the contract in tests/cad_helpers.py; the first run is the Step 5 acceptance run. Heavy (C4 pairs): detach it.
Run: freecadcmd tests/probes/probe_collet.py"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib as L  # noqa: E402
C = L.C


def tag(d):
    whole = int(math.floor(d + 1e-9))
    return "%03dp%d" % (whole, int(round((d - whole) * 10)))


def slit_free(phi0, n, k=0):
    return phi0 + 180.0 / n + 120.0 * k


def contact_fraction(hol_placed, coll, z_hb, zmax, phi0, n):
    """Fraction of sampled cone points (4 azimuths x 11 heights) where holder and collet cone radii agree within 0.01 mm."""
    touch, tot, gaps = 0, 0, []
    for i in range(1, 12):
        z = z_hb + 2.0 + 2.2 * i
        for k in range(4):
            a = slit_free(phi0, n, k)
            ci, hi = C.radial_ivals(coll, a, z, 0.0, 90.0), C.radial_ivals(hol_placed, a, z, 0.0, 90.0)
            if ci and hi and z < zmax:
                g = hi[0][0] - ci[-1][1]
                gaps.append(g)
                tot += 1
                touch += 1 if abs(g) < 0.01 else 0
    return (touch / tot if tot else 0.0), gaps


def measure(d, path, p, hol):
    import FreeCAD as App
    import Part
    sh, doc = L.open_shape(path)
    G = lambda k: L.G(p, k)
    n = int(G("collet.slit_count"))
    phi0 = G("receiver.key_offset_deg") + 15.0
    zmax = C.bbox(sh).ZMax
    out = {"d": d, "height": zmax, "valid": bool(sh.isValid()), "closed": bool(sh.isClosed()), "solids": len(sh.Solids), "volume_mm3": sh.Volume}
    # topology: faces per edge (seam edges excepted), planar faces on a slit centre plane, minimum face area and edge length
    bad = 0
    for e in sh.Edges:
        fs = sh.ancestorsOfType(e, Part.Face)
        if len(fs) == 1 and e.isSeam(fs[0]):
            continue
        if len(fs) != 2:
            bad += 1
    plane_faces = 0
    for f in sh.Faces:
        if f.Surface.__class__.__name__ == "Plane":
            nrm = f.normalAt(0, 0)
            if abs(nrm.z) < 1e-6 and abs(nrm.dot(f.CenterOfMass)) < 0.01:
                plane_faces += 1
    out.update({"bad_edges": bad, "slit_plane_faces": plane_faces, "euler_VEF": len(sh.Vertexes) - len(sh.Edges) + len(sh.Faces),
                "min_face_area": min(f.Area for f in sh.Faces), "min_edge_len": min(e.Length for e in sh.Edges), "genus": None})
    # outer profile and wall at a slit-free azimuth
    az = slit_free(phi0, n)
    zs = [0.05 + (zmax - 0.1) * i / 64.0 for i in range(65)]
    prof, walls = [], []
    for z in zs:
        iv = C.radial_ivals(sh, az, z, 0.0, 90.0)
        if iv:
            prof.append((round(iv[-1][1], 3), z))
            walls.append((z, iv[-1][1] - iv[0][0]))
    out["wall_min_cone_top"] = min([w for z, w in walls if z > 3.0] or [None])
    zb, zt = 5.0, zmax - 12.0
    ro = {z: C.radial_ivals(sh, az, z, 0.0, 90.0)[-1][1] for z in (zb, zt)}
    steps = [z for (r, z), (r2, z2) in zip(prof, prof[1:]) if r - r2 > 1.0]
    out["outer"] = {"half_angle_deg": math.degrees(math.atan2(ro[zb] - ro[zt], zt - zb)), "large_od": 2 * ro[zb], "small_od": 2 * ro[zt],
                    "seat_height": max(steps) if steps else 0.0}
    out["cone_half_angle_deg"] = out["outer"]["half_angle_deg"]
    # bore probes at three slit-free azimuths; a probe whose first solid starts well outside the expected bore hit a slit
    r_bore_exp = (G("core.tol") + G("collet.c_i") + d) / 2.0
    dia, hits = [], []
    for k in range(3):
        iv = C.radial_ivals(sh, slit_free(phi0, n, k), zmax / 2.0, 0.0, 90.0)
        hits.append(bool((not iv) or iv[0][0] > r_bore_exp + 2.0))
        if iv:
            dia.append(2 * iv[0][0])
    out["bore"] = {"az": [slit_free(phi0, n, k) for k in range(3)], "dia": dia, "slit_hits": hits}
    # slits: width, plane offset, void depth, solid beyond the void (even k open at the top face, odd k at the foot)
    rmid = (r_bore_exp + ro[zb]) / 2.0
    widths, offs, depth, beyond = [], [], [], []
    for k in range(n):
        a = phi0 + 360.0 / n * k
        top = (k % 2 == 0)
        tv = C.tangential_ivals(sh, a, rmid, zmax - 3.0 if top else 5.0, 10.0)
        widths.append(tv[1][0] - tv[0][1] if len(tv) >= 2 else 0.0)
        offs.append((tv[1][0] + tv[0][1]) / 2.0 if len(tv) >= 2 else 0.0)
        av = C.axial_ivals(sh, a, rmid, 0.0, zmax)
        depth.append((zmax - av[-1][1] if top else av[0][0]) if av else 0.0)
        beyond.append(bool(av))
    out["slits"] = {"count": sum(1 for w in widths if w > 0.0), "phase_deg": phi0, "width": widths, "plane_offset": offs,
                    "void_depth": depth, "solid_below": beyond}
    out["relief_holes"] = len([f for f in sh.Faces if f.Surface.__class__.__name__ == "Cylinder" and abs(f.Surface.Axis.z) < 1e-3
                               and abs(f.Surface.Radius - G("collet.relief_hole_dia") / 2.0) < 0.05])
    # F2: nominal core slides in (common volume) and lands on the ledge (axial gap)
    ledge = C.axial_ivals(sh, az, r_bore_exp - 1.0, 0.0, zmax)
    z_ledge = ledge[0][1] if ledge else 0.0
    core = Part.makeCylinder(d / 2.0, 60.0, C.V(0, 0, z_ledge + 5.0))
    out["core_in_bore"] = {"interference_mm3": sh.common(core).Volume, "base_gap": z_ledge - G("collet.core_seat_height"), "ledge_top": z_ledge}  # F2: ledge top against core_seat_height
    # F3 sweep: every family core (diameter plus tolerance) against this collet in the R pose
    mean_bore = sum(dia) / len(dia) if dia else 0.0
    out["sweep"] = {}
    for dc in G("core.diameters"):
        cyl = Part.makeCylinder((dc + G("core.tol")) / 2.0, 60.0, C.V(0, 0, z_ledge + 5.0))
        out["sweep"][str(dc)] = {"interference_mm3": sh.common(cyl).Volume, "bore_minus_core": mean_bore - dc}
    # F1 seat fit: R gap between collet cone and holder cone; K clamped solids against the holder cone
    z_hb = {"R": G("seat.holder_bottom_R"), "Kd1": G("seat.holder_bottom_R") - (G("holder.stroke_gap_R") - G("witness.zone_high")),
            "Kmax": G("holder.bottom_above_floor_Kmax")}
    _, gaps = contact_fraction(L.moved(hol, z=z_hb["R"]), sh, z_hb["R"], zmax, phi0, n)
    seat = {"R_gap_min": min(gaps) if gaps else None, "R_gap_max": max(gaps) if gaps else None}
    lateral = math.pi * (out["outer"]["large_od"] + out["outer"]["small_od"]) / 2.0 * G("chain.H") / math.cos(math.radians(out["outer"]["half_angle_deg"]))
    for pose in ("Kd1", "Kmax"):
        cp = os.path.join(L.CACHE, "collet_%s_clamped_%s.FCStd" % (tag(d), pose))
        if os.path.exists(cp):
            cl = L.open_shape(cp)[0]
            hk = L.moved(hol, z=z_hb[pose])
            frac, _ = contact_fraction(hk, cl, z_hb[pose], zmax, phi0, n)
            seat[pose] = {"common_mm3": hk.common(cl).Volume, "contact_mm2": lateral * frac}
    out["seat"] = seat
    # Rule P: flipped copy
    f = sh.copy()
    f.rotate(C.V(0, 0, zmax / 2.0), C.V(1, 0, 0), 180.0)
    out["flip_mismatch_fraction"] = 1.0 - sh.common(f).Volume / sh.Volume
    App.closeDocument(doc.Name)
    return out, sh, prof, r_bore_exp


def x_solid(prof):
    """Solid of revolution of the sampled outer profile with the bore filled (C4)."""
    import Part
    pts = [C.V(0, 0, prof[0][1])] + [C.V(r, 0, z) for r, z in prof] + [C.V(0, 0, prof[-1][1])]
    return Part.Face(Part.makePolygon(pts + [pts[0]])).revolve(C.V(0, 0, 0), C.V(0, 0, 1), 360)


def region_mask(p):
    """C4 comparison region (Loftsman): r >= r_out(z) - 1.2, z 0 to 32, minus the seven notch boxes (z >= 29, chord +-3) and the label box
    (az key - 30, z 12 to 20, chord +-12). r_out(z) = r_fo - foot_ring_width - (z - 2) tan(alpha)."""
    import Part
    G = lambda k: L.G(p, k)
    r0 = G("receiver.register_bore_radius") - G("fit.seat_clearance") - G("collet.foot_ring_width")
    tn = math.tan(math.radians(G("cone.alpha")))
    h = G("collet.slit_length") + G("collet.slit_ligament") + G("collet.relief_hole_dia") / 2.0
    lo = lambda z: r0 - (z - 2.0) * tn - G("collet.min_wall")
    pts = [C.V(lo(0.0), 0, 0), C.V(200, 0, 0), C.V(200, 0, h), C.V(lo(h), 0, h)]
    region = Part.Face(Part.makePolygon(pts + [pts[0]])).revolve(C.V(0, 0, 0), C.V(0, 0, 1), 360)
    key = G("receiver.key_offset_deg")
    try:
        offs = G("collet.notch_azimuth_offsets_deg")
    except KeyError:
        offs = [60, 90, 120, 180, 210, 240, 300]
    try:
        lab = G("collet.label_azimuth_offset_deg")
    except KeyError:
        lab = -30.0
    boxes = []
    for o in offs:
        b = Part.makeBox(40.0, 2 * 3.0, 4.0, C.V(38.0, -3.0, 29.0))
        b.rotate(C.V(0, 0, 0), C.V(0, 0, 1), key + o)
        boxes.append(b)
    b = Part.makeBox(40.0, 24.0, 8.0, C.V(38.0, -12.0, 12.0))
    b.rotate(C.V(0, 0, 0), C.V(0, 0, 1), key + lab)
    boxes.append(b)
    for b in boxes:
        region = region.cut(b)
    return region


def main():
    import Part
    p = L.params()
    sizes = list(L.G(p, "core.diameters")) + [float(x) for x in os.environ.get("CJ_EXTRA", "97.0,93.7").split(",") if x]
    hol = L.part("holder")
    done, xs, shapes, rbore = [], {}, {}, {}
    for d in sizes:
        path = os.path.join(L.CACHE, "collet_%s.FCStd" % tag(d))
        if not os.path.exists(path):
            continue
        out, sh, prof, rb = measure(d, path, p, hol)
        xs[tag(d)], shapes[tag(d)], rbore[tag(d)] = x_solid(prof), sh, rb
        out["x_solid_volume"] = xs[tag(d)].Volume
        L.finish("collet_" + tag(d), out, [path])
        done.append(tag(d))
    ts = sorted(xs)
    pairs, sym_out = {}, {}
    region = region_mask(p)
    for i, a in enumerate(ts):
        for b in ts[i + 1:]:
            key = "%s|%s" % (a, b)
            pairs[key] = xs[a].common(xs[b]).Volume
            sym = shapes[a].cut(shapes[b]).fuse(shapes[b].cut(shapes[a]))
            sym_out[key] = sym.common(region).Volume
    # controls: a size against itself (zero) and a size with one slit widened by 0.5 mm in the skin (known-bad, must be seen)
    sym_zero, sym_bad = None, None  # None fails the C4 test as ABSENT only when no collet exists
    if ts:
        a0 = shapes[ts[0]]
        phi0 = L.G(p, "receiver.key_offset_deg") + 15.0
        tool = Part.makeBox(10.0, 0.5, 4.0, C.V(60.5, 0.75, 10.0))
        tool.rotate(C.V(0, 0, 0), C.V(0, 0, 1), phi0)
        bad = a0.cut(tool)
        sym_bad = a0.cut(bad).fuse(bad.cut(a0)).common(region).Volume
        same = a0.copy()
        sym_zero = a0.cut(same).fuse(same.cut(a0)).common(region).Volume
    L.finish("collet_family", {"tags": done, "x_volume": {t: xs[t].Volume for t in ts}, "x_common": pairs, "symdiff_region_mm3": sym_out,
             "symdiff_zero_control_mm3": sym_zero, "symdiff_known_bad_mm3": sym_bad},
             [os.path.join(L.CACHE, "collet_%s.FCStd" % t) for t in done])


if __name__ in ("__main__", "probe_collet"):
    L.guarded(main, "collet")
