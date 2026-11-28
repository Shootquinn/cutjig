"""Controls for 1.4 (h) r2 (S4 r2, S1 r10, S2 r11, S3 r9; research/sean/cr_scratch/step1.4_engineer_revision_r2.md):
Loftsman P7a FIX 1 (X1-B6), Topologist FIX TP1.4-3 (section_true depth lint), TP1.4-4 (front-surface sign, clause 6c),
TP1.4-5 (clause (6) line family), M1 S4 r1 F3 (one outlined region per cut body, K8 cut_outline_issues), Design Notes
35 R1 (rule (l) clearance at 12 px of the saved image) and R2 (S1 in-plane wings, K5 wing in_plane form).

Every B draws the live sketch by its own script (builders._script_ctx) and plants one defect, or edits the spec and
draws faithfully. A plant that undoes a renderer step monkeypatches the one sketch_common function for the build only.
"""
import contextlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent
for p in (str(SK), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import sketch_common as sc  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402


def _b():
    import builders
    return builders


def _script(s, spec_mut=None):
    return _b()._script_ctx(s, spec_mut=spec_mut)


def _fresh(s):
    """The live sketch drawn by its script, not from the draw cache (a renderer patch applies to this build)."""
    return _script(s, spec_mut=lambda sp: None)


@contextlib.contextmanager
def _patched(name, fn):
    old = getattr(sc, name)
    setattr(sc, name, fn)
    try:
        yield
    finally:
        setattr(sc, name, old)


def _row(sp, fid):
    return next(r for r in sp["features"] if r["id"] == fid)


def _ax(c, pose):
    return c.figs[pose].axes[0]


# ---------------------------------------------------------------- Loftsman P7a FIX 1: X1 presence, side_xz branch

def x1_presence_s1_b():
    """X1 B (Loftsman P7a FIX 1): the live specs with section_true removed from the s1 holder row; s3 and s4 carry it and
    s1 draws the holder in side_xz (rows without axes, main Axes id main)."""
    import check_sketch
    specs = check_sketch.specs_in(SK)
    _row(specs["s1"], "holder").pop("section_true")
    return check_sketch.x1_lint(specs)


# ---------------------------------------------------------------- TP1.4-3: section_true depth band lint (K7)

def _seat_narrow(sp):
    _row(sp, "core_seat")["depth"] = ["-core.diameter_nominal / 2", "core.diameter_nominal / 2"]


def depth_st_s1_b():
    """K7 B (TP1.4-3): live S1 with the core_seat depth back to +-core.diameter_nominal / 2 (the r9 band) under the drawn
    ledge r 50.50."""
    return _script("s1", _seat_narrow)


def depth_st_s3_b():
    """K7 B (TP1.4-3): live S3, core_seat depth +-50.00 (the r8 band)."""
    return _script("s3", _seat_narrow)


def depth_st_s4_b():
    """K7 B (TP1.4-3): live S4, core_seat depth +-50.00 (the r1 band)."""
    return _script("s4", _seat_narrow)


# ---------------------------------------------------------------- TP1.4-4: front-surface sign (clause 6c)

def _old_front(q, polys, n=None):
    return True   # the r1 renderer: every overlapping unsectioned occluder hides an unsectioned target


def occl_sign_s4_b():
    """K8 B (TP1.4-4): live S4 drawn with the pre-change occluder test (no front-surface sign): drill_head split dashed
    under carrier and core_100 (and the tube stub under the core): clause (6c) fires on the hidden copies."""
    with _patched("_in_front", _old_front):
        return _fresh("s4")


def occl_sign_s3_b():
    """K8 B (TP1.4-4): live S3 drawn with the pre-change occluder test: drill_head under core_750, coupling_c under
    screw_end_c and liftmotor_shaft_c (the P7b live firing set)."""
    with _patched("_in_front", _old_front):
        return _fresh("s3")


# ---------------------------------------------------------------- TP1.4-5: clause (6) line family

def strokes_unsplit_s4_b():
    """K8 B (TP1.4-5): live S4 with the stroke split undone (render_occlusion reads area artists only, the r1 renderer):
    carrier:line drawn solid behind the drill head (both figures)."""
    with _patched("_stroke_rows", lambda ctx, ax: []):
        return _fresh("s4")


def strokes_unsplit_s3_b():
    """K8 B (TP1.4-5): live S3 with the stroke split undone: anchor_bearing_c:line drawn solid behind screw_c."""
    with _patched("_stroke_rows", lambda ctx, ax: []):
        return _fresh("s3")


# ---------------------------------------------------------------- M1 S4 r1 F3: one outlined region per cut body (K8)

def outline_z_s4():
    """K8 Z (M1 S4 F3): live S4 r2 drawn by its script: every cut body one outline, no stroked piece edge."""
    return _script("s4")


def _restroke(c, fids, poses=None):
    for pose, fig in c.figs.items():
        if poses and pose not in poses:
            continue
        for g in fids:
            for a in sc.tagged(fig.axes[0]).get(g, []):
                if getattr(a, sc.PIECE_ATTR, None) is not None and not getattr(a, "_sc_hidden_copy", False):
                    a.set_linewidth(1.0)
    return c


def outline_seams_s4_b():
    """K8 B (F3 o1): live S4, the holder and collar pieces stroked again (the r1 drawing: lines at 79.09, 137.09, 145.09
    and the collar seam across the hatch), carrier figure."""
    return _restroke(_script("s4"), ["holder", "collar"], poses=["carrier"])


def outline_seams_s1_b():
    """K8 B (F3 o1, side view class): live S1, the holder pieces stroked again at pose load."""
    return _restroke(_script("s1"), ["holder"], poses=["load"])


def outline_missing_s3_b():
    """K8 B (F3 o4): live S3, the collet outline polylines removed except the first: part of the body boundary undrawn."""
    c = _script("s3")
    ax = _ax(c, "capture_end")
    lines = [a for a in sc.tagged(ax).get("collet:outline", []) if not getattr(a, "_sc_hidden_copy", False)]
    for a in lines[1:]:
        a.remove()
    return c


def outline_per_piece_s4_b():
    """K8 B (F3 o3): live S4 carrier figure, the wing-nut outline drawn piece by piece (each piece ring as a polyline): the
    piece seams drawn as outline."""
    c = _script("s4")
    ax = _ax(c, "carrier")
    for a in list(sc.tagged(ax).get("wingnut:outline", [])):
        a.remove()
    for a in sc.tagged(ax).get("wingnut", []):
        if getattr(a, sc.PIECE_ATTR, None) is None or getattr(a, "_sc_hidden_copy", False):
            continue
        for q in sc.artist_polys(a):
            ring = list(q) + [q[0]]
            sc.draw("wingnut:outline", Line2D([v[0] for v in ring], [v[1] for v in ring], color="k", linewidth=1), ax)
    return c


# ---------------------------------------------------------------- Design Notes 35 R1: rule (l) at 12 px (K4)

def _flat_leader(c, pose, fid, px):
    """label:fid moved onto the row's right edge (max u of its drawn pieces) at px pixels above a gridline that crosses
    that edge, its text at the same height: a horizontal leader px from the gridline (anchor still on the ink)."""
    ax = _ax(c, pose)
    t = next(t for t in ax.texts if t.get_gid() == f"label:{fid}")
    pts = [v for q in sc.pieces(ax, fid) for v in q]
    xm = max(v[0] for v in pts)
    edge = [v[1] for v in pts if abs(v[0] - xm) <= 1e-6]
    lo, hi = min(edge), max(edge)
    dz = _px(ax, px)
    ys = sorted(set(ax.yaxis.get_majorticklocs()) | set(ax.yaxis.get_minorticklocs()))
    g = min((v for v in ys if lo < v + dz < hi), key=lambda v: abs(v + dz - (lo + hi) / 2))
    t.xy = (xm, g + dz)
    t.xyann = (float(t.xyann[0]), g + dz)
    return c


def _px(ax, n):
    (a, b) = ax.transData.transform([(0, 0), (1, 0)])
    return n / abs(b[0] - a[0])


def r1_s4_b():
    """K4 B (Design Notes 35 R1; M1 S4 r1 F2 instance, 7 to 8 px): live S4 carrier figure, the core_100 label leader
    horizontal 8 px above a gridline (passes the r1 D 0.4152 paper mm, 2.45 px)."""
    c = _script("s4")
    return _flat_leader(c, "carrier", "core_100", 8)


def r1_s1_b():
    """K4 B (R1 scope, side view): live S1 load, the drill_tube label leader horizontal 8 px from a gridline."""
    return _flat_leader(_script("s1"), "load", "drill_tube", 8)


def r1_s2_b():
    """K4 B (R1 scope, plan view): live S2, the base_plate label leader horizontal 8 px from a gridline on the plate edge."""
    c = _script("s2")
    return _flat_leader(c, next(iter(c.figs)), "base_plate", 8)


def r1_s3_b():
    """K4 B (R1 scope, section view): live S3, the drill_tube label leader horizontal 8 px from a gridline."""
    return _flat_leader(_script("s3"), "capture_end", "drill_tube", 8)


# ---------------------------------------------------------------- Design Notes 35 R2: S1 in-plane wings (K5)

def wing_ip_z():
    """K5 Z (R2): live S1 r10: wingnut:wing two solid unfilled outlines at u -+(83.14 to 115.00), z_A 113.09 to 153.09."""
    return _script("s1")


def _wings(c, pose="load"):
    return [a for a in sc.tagged(_ax(c, pose)).get("wingnut:wing", [])]


def wing_ip_dashed_b():
    """K5 B (R2 (i)): live S1 load, the wing outlines drawn dashed (the S4 beyond style)."""
    c = _script("s1")
    for a in _wings(c):
        a.set_linestyle("--")
    return c


def wing_ip_low_b():
    """K5 B (R2 (ii)): live S1 load, the wings drawn 16.00 low (the r8 band, z_A 97.09 to 137.09)."""
    c = _script("s1")
    for a in _wings(c):
        a.set_y(a.get_y() - 16.0)
    return c


def wing_ip_count_b():
    """K5 B (R2 (p0)): live S1 with wing.count set to 3 (azimuths 0, 120, 240): two wings off the xz plane."""
    def sm(sp):
        _row(sp, "wingnut")["wing"]["count"] = "wingnut.wing_count + 1"
    return _script("s1", sm)


# ---------------------------------------------------------------- re-plants of signed controls (1.4 (h) r2)

def k4_frac_record_b():
    """K4 B (Rule 2 fix (a), re-plant of K4-B27): live S3; the anchor_c leader and its placer record moved to the cover
    face bottom (the r95 fallback, source ink): the frac anchor is not where the leader ends. At r2 the placer honours
    frac 0.88 with an angled leader, so the r95 plant (frac 0.88) no longer fails."""
    c = _script("s3")
    ax = next(a for a in sc.real_figure(c.figs["capture_end"]).axes if getattr(a, "sketch_axes", None) == "section")
    t = next(t for t in ax.texts if t.get_gid() == "label:anchor_c")
    pts = [v for q in sc.pieces(ax, "anchor_c") for v in q]
    xm = min(v[0] for v in pts) if float(t.xy[0]) < 0 else max(v[0] for v in pts)
    zs = [v[1] for v in pts if abs(v[0] - xm) <= 1e-6]
    q = (xm, min(zs) + 1.0)
    t.xy = q
    rec = getattr(ax, "_sc_placer", None)
    if rec is not None:
        rec["placed"]["anchor_c"].update(source="ink", anchor=[round(q[0], 2), round(q[1], 2)])
    return c


def k4_frac_removed_flat_b():
    """K4 B (re-plant of K4-B29; Design Notes 35 R1 angled candidates): live S3 with label_anchor_frac removed from guide_c
    and anchor_c and the placer's angled candidates switched off (horizontal leaders only, the r1 placer form) under the
    12 px D: rule (l) and the placer fire."""
    def sm(sp):
        for f in ("guide_c", "anchor_c"):
            _row(sp, f).pop("label_anchor_frac", None)
    with _patched("angled_candidates", lambda ink, cands, D: cands):
        return _script("s3", sm)
