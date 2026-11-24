"""Step 4 CAD suite helpers. Not collected (no test_ prefix). Holds: require/absent, labels, the ASSEMBLY.md parser,
the probe-JSON loader with the staleness check, and pure predicate functions that the tests and their controls share.

ARTIFACT CONTRACT (Step 5, 7, 10 build to these names; B4 has none of the starred items)
---------------------------------------------------------------------------------------
tag(d)                          collet file tag, from collet.file_name_pattern: 92.5 -> "092p5", 97.0 -> "097p0", 93.7 -> "093p7"
parts_cache/collet_<tag>.FCStd            * Step 5 generator, one solid
parts_cache/collet_<tag>_clamped.FCStd    * clamped-state solid for F1 (bore = core diameter, slit narrowed)
parts_cache/collet_<tag>_result.json      * keys: part, volume_mm3, isValid, isClosed, solid_count, run_seconds,
                                            cuts[{name, before_mm3, after_mm3, tool_mm3, expected_mm3}], features[{feature, pass, volume_mm3}]
parts_cache/assembly/pose_<P>_<tag>.FCStd * Step 7 assembler; P in R, Kd1, Kmax; one solid object per part name in
                                            ASSEMBLY.md (base, holder, collet, nut, washer, core, frame, bracket, tnut, cutter)
docs/collet_generator_usage.md            * Step 5, the only instruction C10b may follow
results/probes/<name>.json                  written by tests/probes/*.py under freecadcmd (read-only on FCStd, no doc.save):
    step3_parts.json     keys per part {valid, closed, solids, shells, volume, euler_VEF, flip_mismatch_fraction, features_pass}
    thread.json          keys receiver/nut {crest_r, root_r, pitch, tooth_w_lo, tooth_w_hi, flank_deg, down_flank_deg, chirality{dz90, dz0}},
                         nut_mirrored{dz90}, clearance{c_r_crest, c_r_root, g_a}
    thread_mesh.json     keys screw_common{15,90,180,360}, opposite_hand_90, pure_rotation_90, cw_down_common
    tilt.json            keys tilt_deg, register{stop_deg, insertion_mm}, short_register, register_common_at_2x_crit_mm3, axial_drop, flank_gap_zero_tilt_mm
    collet_<tag>.json    keys valid, closed, solids, volume_mm3, profile_volume_mm3, slit_removed_analytic_mm3,
                         relief_removed_analytic_mm3, bad_edges, euler_VEF, genus, slit_plane_faces, min_face_area, min_edge_len,
                         bore{az, dia, slit_hits}, slits{count, phase_deg, width, plane_offset, void_depth, solid_below},
                         relief_holes, wall_min_cone_top, outer{half_angle_deg, large_od, small_od, seat_height}, x_solid_volume,
                         features{<name>: volume_mm3}, flip_mismatch_fraction, seat{R_gap_min, R_gap_max, K_common_mm3, K_contact_mm2},
                         sweep{<core_d>: {interference_mm3, bottoms, contact}}, core_in_bore{interference_mm3, base_gap}
    pose_<P>_<tag>.json  keys pairs{"a|b": {min_dist, overlap_mm3, contact_area_mm2}}, feature_pairs{name: {gap}},
                         measures{<key>: value}   (measure keys per ID are listed in test_assembly.MEASURES)
    exports.json         keys <name>{step_solids, step_volume, fcstd_volume, unit, tree_names, chirality_dz90}
output/step/<name>.step, output/stl/<name>.stl      * Step 10
results/rebuild_record.json                 * Step 10: {run_started_epoch, first{name: volume}, second{name: volume}}
independent/x1_remeasure.py                 * Step 10 writes it (shares no code with build_parts or tests); output results/x1_remeasure.json
                                            keys volumes{name}, interference{"a|b"}, chirality{nut_stl, boss_stl, nut_step}, controls{away, wrong_expected, mirrored_nut}
Pose names: R, Kd1 (K at d+1), Kmax. The state of each probe input is judged by file mtime: a probe older than any input FCStd is MISSING.
"""
import json
import math
import pathlib
import re
import struct
import sys

import pytest

from build_parts import common

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "probes"))
import gates  # noqa: E402  (pure predicates shared with the probes)
from gates import _cells, check_class, check_feature_gap, parse_assembly, parse_gap_text  # noqa: E402,F401

ROOT = common.ROOT
CACHE = common.PARTS_CACHE
PROBES = ROOT / "results" / "probes"
POSES = ("R", "Kd1", "Kmax")
FIVE_PARTS = ("receiver", "holder", "nut", "washer", "footring")
ANALYTIC = {"pi": math.pi, "45 degrees": 45.0, "Euler V-E+F for a closed genus-0 shell": 2,
            "pair count 10 choose 2": 45, "overlap tolerance mm3 (tdd_method, llm_plm_cad 7.4)": 0.01}
OVERLAP_TOL = ANALYTIC["overlap tolerance mm3 (tdd_method, llm_plm_cad 7.4)"]
assert gates.OVERLAP_TOL == OVERLAP_TOL


# ------------------------------------------------------------------ failure reasons (rule 1)
def require(path):
    """Raise the MISSING: assertion when the path is absent or empty. Returns the pathlib.Path."""
    p = pathlib.Path(path)
    assert p.exists() and p.stat().st_size > 0, f"MISSING: {p}"
    return p


def absent(feature):
    raise AssertionError(f"ABSENT FEATURE: {feature}")


def need(cond, feature):
    assert cond, f"ABSENT FEATURE: {feature}"


def label(kind, n):
    """Marker pair: discriminator|invariant plus green_at_N."""
    assert kind in ("discriminator", "invariant") and n in (4, 5, 6, 7, 8, 10, 12)
    assert kind == "discriminator" or n == 4

    def deco(f):
        return getattr(pytest.mark, f"green_at_{n}")(getattr(pytest.mark, kind)(f))
    return deco


# ------------------------------------------------------------------ params access
def P():
    return common.load_params()


def g(key, params=None):
    return common.get(params or P(), key)


def need_key(key, params=None):
    """A threshold the suite needs that params lacks fails as ABSENT FEATURE, naming the proposed key (params gap)."""
    try:
        return common.get(params or P(), key)
    except KeyError:
        absent(f"params key {key} (params gap, Manager routes it)")


def family(params=None):
    return list(common.get(params or P(), "core.diameters"))


def tag(d):
    """Collet file tag: collet.file_name_pattern 'collet_{int}p{frac}' with a three-digit integer part."""
    whole = int(math.floor(d + 1e-9))
    frac = int(round((d - whole) * 10))
    return f"{whole:03d}p{frac}"


def collet_delta(params=None):
    """Delta = s + c_i with s the grip window width (collet.grip_window_hi - collet.grip_window_lo)."""
    p = params or P()
    return (common.get(p, "collet.grip_window_hi") - common.get(p, "collet.grip_window_lo")) + common.get(p, "collet.c_i")


def accept_range(d, params=None):
    """Core diameters a collet of nominal d accepts. Top = bore_free(d) - c_i (zero closure), width s."""
    p = params or P()
    hi = common.bore_free(p, d) - common.get(p, "collet.c_i")
    s = collet_delta(p) - common.get(p, "collet.c_i")
    return hi - s, hi


def thread_major_chain(params=None):
    """Step 3 radial chain: D_T = B_f + 2 t_c + 2 H tan(alpha) - Delta + 2 (t_h + g_reg + t_b + h), B_f for the largest family d."""
    p = params or P()
    G = lambda k: common.get(p, k)
    bf = common.bore_free(p, max(family(p)))
    return (bf + 2 * G("chain.t_c") + 2 * G("chain.H") * math.tan(math.radians(G("cone.alpha"))) - collet_delta(p)
            + 2 * (G("chain.t_h") + G("register.g_reg") + G("chain.t_b") + G("chain.h")))


# ------------------------------------------------------------------ probe JSON (rule 6)
def probe(name, inputs=()):
    """Load results/probes/<name>.json. MISSING: when absent, or older than any input FCStd."""
    p = require(PROBES / f"{name}.json")
    for i in inputs:
        ip = require(i)
        assert p.stat().st_mtime >= ip.stat().st_mtime, f"MISSING: {p} is older than its input {ip}"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("sentinel") == "PROBE_OK", f"MISSING: {p} lacks the PROBE_OK sentinel"
    return data


def result_json(part):
    return json.loads(require(CACHE / f"{part}_result.json").read_text(encoding="utf-8"))


def collet_inputs(d):
    return [CACHE / f"collet_{tag(d)}.FCStd"]


def pose_inputs(pose, d):
    return [CACHE / "assembly" / f"pose_{pose}_{tag(d)}.FCStd"]


# ------------------------------------------------------------------ ASSEMBLY.md parser (rule 3)
def parts_of(rels):
    out = []
    for r in rels:
        for n in (r["a"], r["b"]):
            if n not in out:
                out.append(n)
    return out


def pair_table_errors(rels):
    """Every pair of the parts listed exactly once; classes legal. Unlisted pairs are errors (A1a: an unlisted pair fails)."""
    errs, seen = [], {}
    parts = parts_of(rels)
    for r in rels:
        key = frozenset((r["a"], r["b"]))
        if key in seen:
            errs.append(f"duplicate pair {r['a']}|{r['b']}")
        seen[key] = r
        for cls in (r["r"], r["k"]):
            if cls not in ("C", "G", "F", "P"):      # P: press pads, nut|washer (Step 7 Revision 1)
                errs.append(f"illegal class {cls} on {r['a']}|{r['b']}")
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if frozenset((a, b)) not in seen:
                errs.append(f"unlisted pair {a}|{b}")
    return errs


def class_counts(rels):
    out = {}
    for col in ("r", "k"):
        c = {"C": 0, "G": 0, "F": 0, "P": 0}
        for r in rels:
            c[r[col]] += 1
        out[col] = c
    return out


def pair_class(rels, a, b, pose):
    for r in rels:
        if {r["a"], r["b"]} == {a, b}:
            return r["r"] if pose == "R" else r["k"], r["g_min"]
    raise AssertionError(f"unlisted pair {a}|{b}")  # A1a: an unlisted pair fails


# ------------------------------------------------------------------ predicates shared by tests and controls
def check_chirality(z0, z90, pitch, hand="right"):
    """T1a: (z90 - z0) mod L = +L/4 for right hand, 3L/4 for left."""
    want = pitch / 4.0 if hand == "right" else 3.0 * pitch / 4.0
    got = (z90 - z0) % pitch
    return [] if abs(got - want) <= 0.1 else [f"(z90 - z0) mod L = {got:.3f}, want {want:.3f}"]


def interval_overlap(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    return max(0.0, hi - lo)


def slit_hit(angle_deg, phase_deg, n, half_width_deg):
    """True when the azimuth lies inside a slit of an n-slit part whose first slit centre is phase_deg."""
    step = 360.0 / n
    off = (angle_deg - phase_deg + step / 2) % step - step / 2
    return abs(off) <= half_width_deg


def check_bore(b, expected, tol=0.02):
    """C3: no probe may hit a slit; the mean bore equals expected."""
    e = []
    if any(b["slit_hits"]):
        e.append("probe returned a slit hit")
    if not b["dia"]:
        e.append("no bore probes")
    elif abs(sum(b["dia"]) / len(b["dia"]) - expected) > tol:
        e.append(f"mean bore {sum(b['dia']) / len(b['dia']):.3f} vs {expected:.3f}")
    return e


def web_strain(delta, n, slit_length, hole):
    """Screening model of the relief-hole row in params: strain = 4 x closure / (2 x slit_length x hole) with closure pi x Delta / N."""
    return 4.0 * (math.pi * delta / n) / (2.0 * slit_length * hole)


def check_collet_valid(p):
    e = []
    if p["solids"] != 1:
        e.append(f"solids {p['solids']}")
    if not p["valid"] or not p["closed"]:
        e.append("not valid/closed")
    return e


def check_volume_band(vol, analytic, lo=0.95, hi=1.05):
    r = vol / analytic if analytic else float("inf")
    return [] if lo <= r <= hi else [f"volume ratio {r:.3f}"]


def check_cuts(cuts, tol=0.03):
    e = []
    for c in cuts:
        removed = c["before_mm3"] - c["after_mm3"]
        if not (0 < removed <= c["tool_mm3"] + 1e-6):
            e.append(f"{c['name']}: removed {removed:.3f} outside (0, tool {c['tool_mm3']:.3f}]")
        elif abs(removed - c["expected_mm3"]) > tol * c["expected_mm3"]:
            e.append(f"{c['name']}: removed {removed:.3f} vs expected {c['expected_mm3']:.3f}")
    return e


def check_topology(p):
    e = []
    if p["bad_edges"] != 0:
        e.append(f"{p['bad_edges']} edges without two faces")
    if p["slit_plane_faces"] != 0:
        e.append("leftover planar face on a slit plane")
    return e


def check_slits(s, n, width_seed, tol_w=0.05, tol_plane=0.01):
    e = []
    if s["count"] != n:
        e.append(f"slit count {s['count']} vs {n}")
    if any(abs(o) > tol_plane for o in s["plane_offset"]):
        e.append("slit plane offset from the Z axis")
    if any(abs(w - width_seed) > tol_w for w in s["width"]):
        e.append("slit width off seed")
    if not all(s["solid_below"]) or any(v <= 0 for v in s["void_depth"]):
        e.append("ray across a slit: no void for the depth or no solid below")
    return e


def check_wall(wall, min_wall):
    return [] if wall >= min_wall else [f"wall {wall} < {min_wall}"]


def check_flip(frac, floor):
    """Rule P: the flipped copy differs from the original at more than `floor` of the sampled points."""
    return [] if frac > floor else [f"flipped copy indistinguishable (mismatch {frac})"]


def check_overhang(angle_from_horizontal_deg, floor=45.0, tol=0.5):
    return [] if angle_from_horizontal_deg >= floor - tol else [f"overhang flank {angle_from_horizontal_deg:.1f} deg < {floor}"]


def check_measure(value, op, thr, tol=0.0):
    ok = {"ge": value >= thr - tol, "le": value <= thr + tol, "eq": abs(value - thr) <= tol, "zero": abs(value) <= tol}[op]
    return [] if ok else [f"{value} {op} {thr} (tol {tol})"]


# ------------------------------------------------------------------ STL (pure python, pytest only)
def read_stl(path):
    """Return a list of triangles ((x,y,z) x3), binary or ASCII."""
    raw = pathlib.Path(path).read_bytes()
    if raw[:5].lower() == b"solid" and b"facet" in raw[:400]:
        nums = re.findall(rb"vertex\s+(\S+)\s+(\S+)\s+(\S+)", raw)
        v = [tuple(float(x) for x in t) for t in nums]
        return [tuple(v[i:i + 3]) for i in range(0, len(v), 3)]
    n = struct.unpack("<I", raw[80:84])[0]
    tris = []
    for i in range(n):
        o = 84 + 50 * i
        f = struct.unpack("<12f", raw[o:o + 48])
        tris.append(((f[3], f[4], f[5]), (f[6], f[7], f[8]), (f[9], f[10], f[11])))
    return tris


def stl_metrics(tris, q=1e-4):
    """Watertight (each undirected edge shared by exactly two triangles), degenerate count, signed volume."""
    edges, degenerate, vol = {}, 0, 0.0
    key = lambda v: (round(v[0] / q), round(v[1] / q), round(v[2] / q))
    for a, b, c in tris:
        ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
        vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
        cx, cy, cz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
        if 0.5 * math.sqrt(cx * cx + cy * cy + cz * cz) < 1e-12:
            degenerate += 1
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
        ks = [key(a), key(b), key(c)]
        for i in range(3):
            e = frozenset((ks[i], ks[(i + 1) % 3]))
            edges[e] = edges.get(e, 0) + 1
    open_edges = sum(1 for n in edges.values() if n != 2)
    return {"watertight": open_edges == 0, "open_edges": open_edges, "degenerate": degenerate, "signed_volume": vol, "triangles": len(tris)}


def unit_cube_tris():
    v = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    idx = lambda x, y, z: v.index((x, y, z))
    quads = [((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)), ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)),
             ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)), ((0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)),
             ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)), ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1))]
    tris = []
    for a, b, c, d in quads:
        tris += [(a, b, c), (a, c, d)]
    return [tuple(tuple(float(t) for t in p) for p in tri) for tri in tris]


def vertical_hits(tris, x, y):
    """z values where the vertical line through (x, y) pierces the triangle mesh."""
    out = []
    for a, b, c in tris:
        d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(d) < 1e-14:
            continue
        l1 = ((b[1] - c[1]) * (x - c[0]) + (c[0] - b[0]) * (y - c[1])) / d
        l2 = ((c[1] - a[1]) * (x - c[0]) + (a[0] - c[0]) * (y - c[1])) / d
        l3 = 1.0 - l1 - l2
        if min(l1, l2, l3) >= -1e-9:
            out.append(l1 * a[2] + l2 * b[2] + l3 * c[2])
    return sorted(out)


def ridge_phase(tris, rho, theta_deg, pitch, zmid):
    """Ridge centre z (mod pitch) at (rho, theta): the vertical line through the mesh enters and leaves the solid in pairs;
    take the interval whose centre lies nearest zmid."""
    x = rho * math.cos(math.radians(theta_deg)) + 1.234e-6   # offset off exact triangle edges
    y = rho * math.sin(math.radians(theta_deg)) + 2.345e-6
    h = []
    for z in vertical_hits(tris, x, y):
        if not h or z - h[-1] > 1e-6:
            h.append(z)
    if len(h) < 2 or len(h) % 2:
        return None
    cs = [(h[i] + h[i + 1]) / 2.0 for i in range(0, len(h), 2)]
    return min(cs, key=lambda c: abs(c - zmid)) % pitch


def helical_ridge_mesh(pitch, hand="right", width=1.5, **kw):
    """Two helical blades width apart: a vertical line pierces them in (lower, upper) pairs. Control stand-in for a thread ridge."""
    lo = helical_blade_mesh(pitch, hand, **kw)
    return lo + [tuple((v[0], v[1], v[2] + width) for v in tri) for tri in lo]


def helical_blade_mesh(pitch, hand="right", turns=4, rho_a=70.0, rho_b=76.0, seg=36):
    """Synthetic thread stand-in: a thin radial blade following the helix (right: z rises with theta). Used by the T1d control only."""
    sgn = 1.0 if hand == "right" else -1.0
    tris = []
    n = turns * seg
    for i in range(n):
        p0, p1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        z0, z1 = sgn * pitch * p0 / (2 * math.pi), sgn * pitch * p1 / (2 * math.pi)
        pts = [(r * math.cos(p), r * math.sin(p), z) for r, p, z in ((rho_a, p0, z0), (rho_b, p0, z0), (rho_b, p1, z1), (rho_a, p1, z1))]
        tris += [(pts[0], pts[1], pts[2]), (pts[0], pts[2], pts[3])]
    return tris


def ridge_dz_blade(tris, rho, pitch):
    """Control-side chirality reading on the synthetic blade: single pierce per turn."""
    def z_at(theta):
        x, y = rho * math.cos(math.radians(theta)), rho * math.sin(math.radians(theta))
        h = vertical_hits(tris, x, y)
        return (h[len(h) // 2] % pitch) if h else None
    return z_at(0.0), z_at(90.0)


# ------------------------------------------------------------------ source tags (rule 7, P24)
SRC_RE = re.compile(r"^\s*#\s*SRC:\s*(?P<row>[^|]+?)\s*\|\s*(?P<status>[A-Z]+)\s*\|\s*(?P<lines>[^|]+?)\s*(?:\|\s*key=(?P<key>[\w.]+)\s*)?$")
LEGAL_SRC_STATUS = ("VERIFIED", "DECLARED", "ASSUMED", "DERIVED", "CONTRACT")


def parse_src_tags(text):
    tags, bad = [], []
    for i, ln in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*#\s*SRC:", ln):
            m = SRC_RE.match(ln)
            (tags if m else bad).append((i, m.groupdict()) if m else (i, ln))
    return tags, bad


def register_rows(gameplan_text):
    """(claim, first status word) for each Source Verification Register row."""
    sect = gameplan_text.split("## Source Verification Register")[1]
    out = []
    for ln in sect.splitlines():
        if ln.startswith("|") and "---" not in ln and "Claim used by a test" not in ln:
            c = _cells(ln)
            if len(c) >= 5:
                out.append((c[0], c[2].split()[0].strip(".,;:()") if c[2] else ""))
    return out


# ------------------------------------------------------------------ params gaps (thresholds the suite needs that params lacks)
# Keys the suite needs that params lacks are listed here and read through need_key(); a missing key fails as ABSENT FEATURE.
# Step 5: the Loftsman's four collet keys are now in params.yaml, so no gaps remain.
# Step 6: literal keys read by test_step6_parts.py before the Engineer adds them (Loftsman section 7); P7 accepts them until params carries them.
PARAM_GAPS = {"witness.azimuth_deg": "Step 6", "nut.glyph_length": "Step 6", "stop.pad_thickness": "Step 6",
              # Step 7 (Loftsman L5, L-collar): keys the Engineer adds to params.yaml at Step 7
              "hardware.printed_brackets_per_joint": "Step 7", "collar.thickness": "Step 7"}


def measure(data, key):
    """A named scalar from a pose probe JSON; absent means the Step 7 or Step 12 probe has not produced it yet."""
    ms = data.get("measures", {})
    need(key in ms and ms[key] is not None, f"pose measure {key}")
    return ms[key]


def has_key(key, params=None):
    try:
        common.get(params or P(), key)
        return True
    except KeyError:
        return False


def part_inputs(*names):
    return [CACHE / f"{n}.FCStd" for n in names]


def declared_genus(part, params=None):
    """Declared through-hole count of a Step 3 part: one central bore, plus one tunnel per nut washer window (radial slots that open the
    washer pocket wall to the outside between plate and skirt). Key slots, notches, pockets and tommy holes are open or blind."""
    p = params or P()
    return 1 + (common.get(p, "nut.washer_window_count") if part == "nut" else 0)


FLIP_FLOOR = 1e-3  # numerical floor of the flipped-copy mismatch fraction (a plain cylinder reads 0)


def check_usage_doc(path):
    p = pathlib.Path(path)
    if not p.exists():
        return [f"usage doc missing: {p}"]
    t = p.read_text(encoding="utf-8")
    return [] if len(t.split()) > 50 and "freecadcmd" in t.lower() else ["usage doc empty or lacks the freecadcmd command"]


def rel_diff(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def check_step_record(rec, expect_solids, tol=0.005, at_least=False):
    """E1: solid count, summed volume within 0.5 percent of the FCStd, unit mm."""
    e = []
    if (rec["step_solids"] < expect_solids) if at_least else (rec["step_solids"] != expect_solids):
        e.append(f"solids {rec['step_solids']} vs {expect_solids}")
    if rec["fcstd_volume"] is None or rel_diff(rec["step_volume"], rec["fcstd_volume"]) > tol:
        e.append("STEP volume off the FCStd")
    if rec["unit"] != "mm":
        e.append(f"unit {rec['unit']}")
    return e


def check_tessellation(t, c_r):
    """E2: linear deflection at most c_r / 10, angular at most 2 degrees."""
    e = []
    if t is None or t.get("linear_deflection") is None or t.get("angular_deflection_deg") is None:
        return ["tessellation deflections not stored in the result JSON"]
    if t["linear_deflection"] > c_r / 10.0 + 1e-12:
        e.append(f"linear deflection {t['linear_deflection']} > c_r/10")
    if t["angular_deflection_deg"] > 2.0:
        e.append(f"angular deflection {t['angular_deflection_deg']} > 2")
    return e


def stl_bbox_size(tris):
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    return (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))


# ------------------------------------------------------------------ collet definition (Step 5: cr_scratch/step5_loftsman_collet_definition.md)
COLLET_RING_TOP = 1.995        # foot ring and key thickness, z 0 to 1.995
COLLET_KEY_TIP_R = 70.04       # foot key tip radius (holder key tip); key width is holder.key_width
COLLET_NOTCH_FLOOR_Z = 29.0    # rim notch floor, tool z 29 to 33
COLLET_NOTCH_CHORD = 3.0       # half chord of a rim notch
COLLET_LABEL_Z = (12.0, 20.0)
COLLET_LABEL_HALF_CHORD = 12.0
COLLET_SKIN = 1.2              # C4 compares only r >= r_out(z) - 1.2 (collet.min_wall)
NOTCH_OFFSETS_DEFAULT = (60.0, 90.0, 120.0, 180.0, 210.0, 240.0, 300.0)  # collet.notch_azimuth_offsets_deg (new key, Loftsman value)
LABEL_OFFSET_DEFAULT = -30.0                                               # collet.label_azimuth_offset_deg (new key, Loftsman value)


def _pget(params, key, default):
    try:
        return common.get(params, key)
    except KeyError:
        return default


def collet_dims(d, params=None):
    """Radii and heights of collet d from params, per the Loftsman definition. outer(z), inner(z) are slit-free radial limits."""
    p = params or P()
    G = lambda k: common.get(p, k)
    r_b = (d + G("core.tol") + G("collet.c_i")) / 2.0
    r_fo = G("receiver.register_bore_radius") - G("fit.seat_clearance")
    r0 = r_fo - G("collet.foot_ring_width")
    tn = math.tan(math.radians(G("cone.alpha")))
    h = G("collet.slit_length") + G("collet.slit_ligament") + G("collet.relief_hole_dia") / 2.0
    room = r0 - (h - 2.0) * tn - r_b - G("collet.min_wall")
    c = 2.5 if 2.5 < room < 3.5 else min(room, 10.5)
    seat, ledge_w = G("collet.core_seat_height"), G("collet.core_seat_width")

    def outer(z):
        return r_fo if z < COLLET_RING_TOP else r0 - (z - 2.0) * tn

    def inner(z):
        if z < seat:
            return r_b - ledge_w
        return r_b if z < h - c else r_b + (z - (h - c))
    return {"r_b": r_b, "r_fo": r_fo, "r0": r0, "tan": tn, "height": h, "c": c, "edge_z": h - c, "outer": outer, "inner": inner}


def collet_chamfer_c(d, params=None):
    return collet_dims(d, params)["c"]


def collet_family_index(d, params=None):
    """Family index 1 to 7: clamp(floor((d - core.diameters[0]) / collets.spacing + 0.5) + 1, 1, collets.count). Also the notch count and colour index."""
    p = params or P()
    idx = math.floor((d - family(p)[0]) / common.get(p, "collets.spacing") + 0.5) + 1
    return max(1, min(int(common.get(p, "collets.count")), idx))


def collet_label_text(d, params=None):
    p = params or P()
    return f"{d:.1f} | {d + common.get(p, 'collet.grip_window_lo'):.1f}-{d + common.get(p, 'collet.grip_window_hi'):.1f}"


def collet_clamped_slit_width(core_offset, params=None):
    """Slit width with the collet closed on a core of diameter d + core_offset: w = seed - pi x Delta / N, Delta = tol + c_i - core_offset."""
    p = params or P()
    G = lambda k: common.get(p, k)
    delta = G("core.tol") + G("collet.c_i") - core_offset
    return G("collet.slit_width_seed") - math.pi * delta / G("collet.slit_count")


def base_gap(z_ledge, seat_height):
    """F2: the core lands on the ledge. Gap = measured ledge top z minus collet.core_seat_height (the 1.0 radial bore clearance is not a gap)."""
    return z_ledge - seat_height


def check_base_gap(gap, tol=0.05):
    return [] if abs(gap) <= tol else [f"ledge top off collet.core_seat_height by {gap:.3f}"]


def collet_marker_azimuths(params=None):
    p = params or P()
    key = common.get(p, "receiver.key_offset_deg")
    offs = _pget(p, "collet.notch_azimuth_offsets_deg", list(NOTCH_OFFSETS_DEFAULT))
    return [(key + o) % 360.0 for o in offs], (key + _pget(p, "collet.label_azimuth_offset_deg", LABEL_OFFSET_DEFAULT)) % 360.0


def _in_box(r, az, a0, half_chord):
    da = math.radians(az - a0)
    return r * math.cos(da) > 0 and abs(r * math.sin(da)) <= half_chord


def collet_c4_region(r, z, az_deg, params=None):
    """C4 comparison region: sizes must agree where r >= r_out(z) - 1.2, 0 <= z <= 32, outside the notch boxes of the whole family and the
    label box. Bore, ledge, chamfer and lip (always inside r_out - 1.2) are not compared."""
    p = params or P()
    dims = collet_dims(family(p)[0], p)
    if not (0.0 <= z <= dims["height"]) or r < dims["outer"](z) - COLLET_SKIN:
        return False
    notches, label = collet_marker_azimuths(p)
    if z >= COLLET_NOTCH_FLOOR_Z and any(_in_box(r, az_deg, a, COLLET_NOTCH_CHORD) for a in notches):
        return False
    return not (COLLET_LABEL_Z[0] <= z <= COLLET_LABEL_Z[1] and _in_box(r, az_deg, label, COLLET_LABEL_HALF_CHORD))


def collet_expected_volume(d, params=None):
    """Reference volume of collet d from params alone: revolve profile (ring, ledge, bore, chamfer, cone) by integration, plus the key beyond
    the ring, minus slit, relief-hole, notch, label and lip terms. Returns a dict of mm3 terms; "total" is the reference for C2."""
    p = params or P()
    G = lambda k: common.get(p, k)
    D = collet_dims(d, p)
    outer, inner, h = D["outer"], D["inner"], D["height"]
    n, w = int(G("collet.slit_count")), G("collet.slit_width_seed")
    seat, ledge_w = G("collet.core_seat_height"), G("collet.core_seat_width")
    t = lambda z: outer(z) - inner(z)
    N = 3200
    dz = h / N
    zs = [(i + 0.5) * dz for i in range(N)]
    profile = sum(math.pi * (outer(z) ** 2 - inner(z) ** 2) * dz for z in zs)
    plain = sum(math.pi * (outer(z) ** 2 - (D["r_b"] - ledge_w if z < seat else D["r_b"]) ** 2) * dz for z in zs)
    key = G("holder.key_width") * (COLLET_KEY_TIP_R - D["r_fo"]) * COLLET_RING_TOP

    def band(z0, z1):
        m = max(1, int(round((z1 - z0) / dz)))
        return sum(t(z0 + (j + 0.5) * (z1 - z0) / m) for j in range(m)) * (z1 - z0) / m
    slit_cut = {"top": w * band(7.0, h), "bottom": w * band(0.0, 25.0)}
    slits = (n // 2) * (slit_cut["top"] + slit_cut["bottom"])
    rh = G("collet.relief_hole_dia") / 2.0
    g = 80
    cell = (2 * rh / g) ** 2
    hole_cut = {"top": 0.0, "bottom": 0.0}
    for kind, zc in (("top", 7.0), ("bottom", 25.0)):
        for i in range(g):
            y = -rh + (i + 0.5) * 2 * rh / g
            for j in range(g):
                zz = zc - rh + (j + 0.5) * 2 * rh / g
                if y * y + (zz - zc) ** 2 > rh * rh:
                    continue
                in_slit = abs(y) < w / 2.0 and ((zz >= 7.0) if kind == "top" else (zz <= 25.0))  # slits are cut first
                if not in_slit:
                    hole_cut[kind] += t(zz) * cell
    holes = (n // 2) * (hole_cut["top"] + hole_cut["bottom"])
    notches = collet_family_index(d, p) * 2 * COLLET_NOTCH_CHORD * band(COLLET_NOTCH_FLOOR_Z, h)
    area, m = 0.0, 200
    zl0, zl1 = COLLET_LABEL_Z
    for j in range(m):
        r = outer(zl0 + (j + 0.5) * (zl1 - zl0) / m)
        area += 2 * r * math.asin(COLLET_LABEL_HALF_CHORD / r) * (zl1 - zl0) / m / math.cos(math.radians(G("cone.alpha")))
    label = G("collet.label_depth") * area
    th = math.pi / 4.0
    lip = 2 * math.pi * D["r_b"] * (G("collet.bore_lip_radius") ** 2) * (math.tan(th / 2.0) - th / 2.0)
    total = profile + key - slits - holes - notches - label - lip
    return {"total": total, "profile": profile, "key": key, "chamfer": plain - profile, "slits": slits, "holes": holes,
            "notches": notches, "label": label, "lip": lip, "slit_cut": slit_cut, "hole_cut": hole_cut}


# ------------------------------------------------------------------ Step 7 additions: thresholds for the shared gates, ledger and instance helpers
def gate_thresholds(rels=None, feats=None):
    """Threshold dict for gates.fired / pair_violations, from params.yaml and ASSEMBLY.md (probe_ws builds the same dict through gates.thresholds)."""
    r0, f0 = parse_assembly()
    return gates.thresholds(g, rels or r0, feats or f0)


def nominal_tag():
    return tag(common.get(P(), "core.diameter_nominal"))


def ruled_instance_pairs(text=None):
    """Optional '### Instance pair rulings' section of ASSEMBLY.md: rows `| kind_a|kind_b | max overlap mm3 | note |`. Absent section = no rulings."""
    text = text if text is not None else (ROOT / "ASSEMBLY.md").read_text(encoding="utf-8")
    if "### Instance pair rulings" not in text:
        return {}
    sec = text.split("### Instance pair rulings")[1]
    sec = re.split(r"^#{1,3} ", sec, flags=re.M)[0]
    out = {}
    for ln in sec.splitlines():
        if ln.startswith("|") and "---" not in ln and "kind" not in ln.lower().split("|")[1]:
            c = _cells(ln)
            out[c[0]] = float(c[1])
    return out


LEDGER = ROOT / "results" / "assembly_poses.json"
REPORT = ROOT / "cr_scratch" / "step7_interference_report.md"
