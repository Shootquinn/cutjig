"""Pure-python predicates shared by tests (pytest), probe_poses.py and probe_ws.py (freecadcmd). No FreeCAD, no pytest import.
Holds: the A1a class predicates, the six wrong-state gates, per-instance pair checks (G4), the pose-ledger screw-motion check (G5)
and the interference-report parser (G6). Thresholds arrive in a dict T built by cad_helpers.gate_thresholds(); this module holds none."""
import math
import re

OVERLAP_TOL = 0.01  # mm3, tdd_method and llm_plm_cad 7.4 (cad_helpers.ANALYTIC asserts the same value)
GATES = ("A1", "A3", "T1", "T9", "F1", "F3")
import os
ASSEMBLY_MD = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ASSEMBLY.md")


# ------------------------------------------------------------------ class predicates (moved from cad_helpers)
def parse_gap_text(text):
    """Feature-pair gap cell -> (kind, values). 'a / b / c' -> ('exact', [a,b,c]); 'at least X ...' -> ('min', X)."""
    t = text.strip()
    if t.lower().startswith("at least"):
        nums = re.findall(r"\(?(\d+(?:\.\d+)?)\)?", t)
        if "/" in t and len(nums) == 3:  # Revision 1: per-pose minima 'at least a / b / c' (R / Kd1 / Kmax)
            return "min", [float(x) for x in nums]
        return "min", float(nums[-1])
    return "exact", [float(x) for x in re.findall(r"\d+(?:\.\d+)?", t)]


def min_for_pose(vals, i):
    """Per-pose minimum: a list indexed by pose (R, Kd1, Kmax) or one scalar for every pose."""
    return vals[i] if isinstance(vals, list) else vals


def check_class(cls, m, g_min, patch_floor=0.0, tol_c=0.01, rel_g=1e-3, pad=None):
    """A1a pair predicate. m: {min_dist, overlap_mm3, contact_area_mm2}. pad: (min, max) overlap mm3 of class P (press pads, nut|washer;
    contact_area_mm2 is the common-face intersection area, never a sum of face areas). Returns a list of violations."""
    e = []
    if cls == "P":
        if pad is None or None in pad:
            return ["MISSING: params keys nut.pad_overlap_min / nut.pad_overlap_max for class P"]
        if abs(m["min_dist"]) > tol_c:
            e.append(f"P: min_dist {m['min_dist']}")
        if not (pad[0] - 1e-9 <= m["overlap_mm3"] <= pad[1] + 1e-9):
            e.append(f"P: overlap {m['overlap_mm3']} outside [{pad[0]}, {pad[1]}]")
        return e
    if cls == "C":
        if abs(m["min_dist"]) > tol_c:
            e.append(f"C: min_dist {m['min_dist']}")
        if m["overlap_mm3"] >= OVERLAP_TOL:
            e.append(f"C: overlap {m['overlap_mm3']}")
        if m["contact_area_mm2"] <= patch_floor:
            e.append(f"C: patch {m['contact_area_mm2']} <= floor {patch_floor}")
    elif cls == "G":
        if m["min_dist"] < g_min * (1 - rel_g) - 1e-9:
            e.append(f"G: min_dist {m['min_dist']} < g_min {g_min}")
        if m["contact_area_mm2"] != 0:
            e.append(f"G: contact {m['contact_area_mm2']}")
        if m["overlap_mm3"] >= OVERLAP_TOL:
            e.append(f"G: overlap {m['overlap_mm3']}")
    elif cls == "F":
        if m["overlap_mm3"] >= OVERLAP_TOL:
            e.append(f"F: overlap {m['overlap_mm3']}")
    else:
        e.append(f"unknown class {cls}")
    return e


def check_feature_gap(cls, gap, expect, kind, tol=0.05):
    """Feature-pair predicate: exact value (+/- tol, C reads 0 +/- 0.01) or a minimum."""
    if kind == "min":
        return [] if gap >= expect - 1e-9 else [f"gap {gap} < {expect}"]
    if cls == "C":
        return [] if abs(gap) <= 0.01 else [f"C gap {gap}"]
    return [] if abs(gap - expect) <= tol else [f"gap {gap} vs {expect}"]


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_assembly(text=None):
    """Return (relations, features). relations: dicts a, b, r, k, g_min, note. features: dicts fa, fb, r, kd1, kmax, gaps, note."""
    text = text if text is not None else open(ASSEMBLY_MD, encoding="utf-8").read()
    rel_txt = text.split("## Relations")[1].split("### Feature pairs")[0]
    feat_txt = text.split("### Feature pairs")[1].split("## Load path")[0]
    rels, feats = [], []
    for ln in rel_txt.splitlines():
        if ln.startswith("|") and "Part_A" not in ln and "---" not in ln:
            c = _cells(ln)
            rels.append({"a": c[0], "b": c[1], "r": c[2], "k": c[3], "g_min": float(c[4]), "note": c[5]})
    for ln in feat_txt.splitlines():
        if ln.startswith("|") and "Feature_A" not in ln and "---" not in ln:
            c = _cells(ln)
            feats.append({"fa": c[0], "fb": c[1], "r": c[2], "kd1": c[3], "kmax": c[4], "gaps": c[5], "note": c[6]})
    return rels, feats




def thresholds(G, rels, feats):
    """Threshold dict for fired() / pair_violations(). G(key) reads params.yaml; rels, feats from parse_assembly()."""
    return {"rels": rels, "feats": feats, "seat_min_area": G("seat.min_contact_area"), "min_patch": G("fit.min_contact_patch"),
            "holder_bottom": {"R": G("seat.holder_bottom_R"), "Kd1": G("seat.holder_bottom_R") - (G("holder.stroke_gap_R") - G("witness.zone_high")),
                              "Kmax": G("holder.bottom_above_floor_Kmax")},
            "pitch": G("thread.pitch"), "min_engage_mm": G("thread.min_engage_pitches") * G("thread.pitch"),
            "core_axis_max": G("icd.core_axis_offset_max"), "tilt_max": G("register.clamped_tilt_max_deg"), "tilt_limit": G("register.tilt_limit_deg"),
            "footprint_x": G("icd.footprint_x"), "footprint_y": G("icd.footprint_y"), "seat_clearance": G("fit.seat_clearance"),
            "pad": (_opt(G, "nut.pad_overlap_min"), _opt(G, "nut.pad_overlap_max"))}


def _opt(G, key):
    try:
        return G(key)
    except KeyError:
        return None


# ------------------------------------------------------------------ pose evaluation shared by the matrix test, the report and the gates
POSE_IDX = {"R": 0, "Kd1": 1, "Kmax": 2}


def pair_floor(r, T):
    return T["seat_min_area"] if {r["a"], r["b"]} == {"holder", "collet"} else T["min_patch"]


def pair_class_letter(key, pose, T):
    a, b = key.split("|")
    for r in T["rels"]:
        if r["a"] == a and r["b"] == b:
            return r["r"] if pose == "R" else r["k"]
    for f in T["feats"]:
        if f["fa"] == a and f["fb"] == b:
            return (f["r"], f["kd1"], f["kmax"])[POSE_IDX[pose]]
    return "?"


def pair_violations(out, pose, T):
    """[(key, [violations])] for the 45 part pairs and 6 feature pairs of a pose probe dict. Absent entries are violations."""
    res = []
    for r in T["rels"]:
        key = f"{r['a']}|{r['b']}"
        m = out["pairs"].get(key)
        cls = r["r"] if pose == "R" else r["k"]
        res.append((key, [f"pair {key} absent"] if m is None else check_class(cls, m, r["g_min"], pair_floor(r, T), pad=T.get("pad"))))
    i = POSE_IDX[pose]
    for f in T["feats"]:
        key = f"{f['fa']}|{f['fb']}"
        fp = out["feature_pairs"].get(key)
        if fp is None or fp.get("gap") is None:
            res.append((key, [f"feature pair {key} absent"]))
            continue
        kind, vals = parse_gap_text(f["gaps"])
        cls = (f["r"], f["kd1"], f["kmax"])[i]
        res.append((key, check_feature_gap(cls, fp["gap"], min_for_pose(vals, i) if kind == "min" else vals[i], kind)))
    return res


# ------------------------------------------------------------------ the six wrong-state gates (G2, G3)
def fired(out, pose, T):
    """{gate: [reasons]} for the gates that fire on a pose probe dict. Only present objects can fire a gate that needs them;
    A1 also fires on an absent pair when `strict` is set in T (the zero control sets it)."""
    f = {}

    def add(g, msg):
        f.setdefault(g, []).append(msg)
    pv = pair_violations(out, pose, T)
    for key, errs in pv:
        for e in errs:
            if "absent" not in e or T.get("strict"):
                add("A1", f"{key}: {e}")
    ms, pairs = out.get("measures", {}), out.get("pairs", {})
    K = pose != "R"
    if "holder_bottom_above_floor" in ms and abs(ms["holder_bottom_above_floor"] - T["holder_bottom"][pose]) > 0.05:
        add("A3", f"holder bottom {ms['holder_bottom_above_floor']:.3f} vs {T['holder_bottom'][pose]:.3f}")
    if "nut_skirt_bottom_above_floor" in ms and ms["nut_skirt_bottom_above_floor"] < T["pitch"]:
        add("A3", f"nut skirt {ms['nut_skirt_bottom_above_floor']:.3f} < one pitch")
    if "engaged_mm" in ms and ms["engaged_mm"] < T["min_engage_mm"]:
        add("A3", f"engaged {ms['engaged_mm']:.3f} < {T['min_engage_mm']}")
    if K and "core_axis_offset" in ms and ms["core_axis_offset"] > T["core_axis_max"]:
        add("A3", f"core axis offset {ms['core_axis_offset']:.3f}")
    if K and "clamped_tilt_deg" in ms and ms["clamped_tilt_deg"] > T["tilt_max"]:
        add("A3", f"clamped tilt {ms['clamped_tilt_deg']:.3f}")
    if ms.get("receiver_underside_contact_mm2", 0.0) > 0.0:
        add("A3", f"receiver underside contact {ms['receiver_underside_contact_mm2']:.1f}")
    for ax, k in (("x", "frame_footprint_x"), ("y", "frame_footprint_y")):
        if k in ms and abs(ms[k] - T["footprint_" + ax]) > 0.05:
            add("A3", f"{k} {ms[k]:.2f}")
    nb = pairs.get("base|nut")
    if nb is not None and nb["overlap_mm3"] >= OVERLAP_TOL:
        add("T1", f"thread flanks interfere, base|nut {nb['overlap_mm3']:.1f} mm3")
    if "engaged_mm" in ms and ms["engaged_mm"] <= 0.0:
        add("T1", "no thread engagement")
    for k in ("nut_tilt_deg", "holder_tilt_deg"):
        if k in ms and ms[k] > T["tilt_limit"]:
            add("T9", f"{k} {ms[k]:.3f} > {T['tilt_limit']}")
    hc = pairs.get("holder|collet")
    if hc is not None:
        if K and (hc["overlap_mm3"] >= OVERLAP_TOL or hc["contact_area_mm2"] <= T["seat_min_area"]):
            add("F1", f"cone seat overlap {hc['overlap_mm3']:.3f} contact {hc['contact_area_mm2']:.1f}")
        if not K and abs(hc["min_dist"] - T["seat_clearance"]) > 0.05:
            add("F1", f"R seat gap {hc['min_dist']:.3f} vs {T['seat_clearance']}")
    cc = pairs.get("collet|core")
    if cc is not None and (cc["overlap_mm3"] >= OVERLAP_TOL or (K and cc["contact_area_mm2"] <= 0.0)):
        add("F3", f"core against collet overlap {cc['overlap_mm3']:.3f} contact {cc['contact_area_mm2']:.1f}")
    return f


# Expected firing gates per planted state. A WS passes G2 when the fired set meets this set (any member) and stays inside GATES.
WS_EXPECT = {1: {"A1", "F1"}, 2: {"A1", "A3"}, 3: {"A1", "T1"}, 4: {"T1", "A1"}, 5: {"T9", "T1"}, 6: {"F3", "A1"}, 7: {"A1", "F1"},
             8: {"A1", "A3"}, 9: {"A3", "A1"}, 10: {"A1", "A3"}, 11: {"F1", "A1"}}
WS_NAMES = {1: "collet upside down", 2: "holder upside down", 3: "nut upside down", 4: "wrong-hand thread", 5: "cross-threaded tilt",
            6: "wrong collet for core", 7: "collet unseated", 8: "holder bottomed", 9: "nut bottomed on base", 10: "base on frame upside down",
            11: "slit over key"}


# ------------------------------------------------------------------ per-instance pairs (G4)
def kind_of(name):
    for k in ("bracket", "member", "tnut"):
        if name.startswith(k):
            return k
    return "?"


def pair_kind(a, b):
    return "|".join(sorted((kind_of(a), kind_of(b))))


def instance_errors(pairs, tol=OVERLAP_TOL, ruled=None):
    """pairs {"a|b": {overlap_mm3, min_dist}}. A pair fails when its common volume reaches tol, unless a ruled row for its kind
    (ruled {kind: max_overlap_mm3}) allows it and the measured volume stays within that ruling."""
    ruled = ruled or {}
    e = []
    for key, m in pairs.items():
        a, b = key.split("|")
        k = pair_kind(a, b)
        if m["overlap_mm3"] >= tol and not (k in ruled and m["overlap_mm3"] <= ruled[k]):
            e.append(f"{key} ({k}): {m['overlap_mm3']:.3f} mm3")
    return e


# ------------------------------------------------------------------ pose ledger (G5)
def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def screw(phi_rad, lead):
    """S(phi) = Rz(phi) T(0, 0, L phi / 2 pi), 4x4 row-major."""
    c, s = math.cos(phi_rad), math.sin(phi_rad)
    rz = [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    t = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, lead * phi_rad / (2 * math.pi)], [0, 0, 0, 1]]
    return mat_mul(rz, t)


def mat_diff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(4) for j in range(4))


RIDERS = ("nut", "holder", "washer", "collet", "core")
FIXED = ("base", "frame", "bracket", "tnut", "cutter")


def ledger_errors(led, lead, tol=1e-6):
    """led: {"sizes": {tag: {pose: {"phi_deg", "dz_mm", "placements": {part: 4x4}}}}}. Checks per size and non-R pose:
    nut(P) = S(phi) nut(R), phi = 2 pi dz / L (radians) within tol; FIXED parts equal their R placement; the nut-riding parts may differ."""
    e = []
    for tag, poses in led["sizes"].items():
        r = poses["R"]["placements"]
        for pose in ("Kd1", "Kmax"):
            p = poses[pose]
            phi = 2 * math.pi * p["dz_mm"] / lead
            if abs(math.radians(p["phi_deg"]) - phi) > tol:
                e.append(f"{tag} {pose}: phi_deg {p['phi_deg']} vs 2 pi dz / L = {math.degrees(phi):.9f}")
            want = mat_mul(screw(phi, lead), r["nut"])
            d = mat_diff(want, p["placements"]["nut"])
            if d > tol:
                e.append(f"{tag} {pose}: nut(P) differs from S(phi) nut(R) by {d:.3g}")
            for part in FIXED:
                if part in p["placements"] and mat_diff(p["placements"][part], r[part]) > 1e-9:
                    e.append(f"{tag} {pose}: {part} moved between poses")
            if p["dz_mm"] >= 0 or p["phi_deg"] >= 0:
                e.append(f"{tag} {pose}: clockwise turn from R must lower the nut (dz {p['dz_mm']}, phi {p['phi_deg']})")
        if abs(poses["Kmax"]["dz_mm"]) <= abs(poses["Kd1"]["dz_mm"]):
            e.append(f"{tag}: Kmax nut not lower than Kd1")
    return e


def synth_ledger(lead, dz_kd1=-4.0, dz_kmax=-9.0, tags=("100p0",), pure_z=False, move_part=None):
    """Control ledger built from the definition. pure_z: the nut moves by T(dz) only (known-bad). move_part: a fixed part displaced."""
    ident = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    base = {p: [row[:] for row in ident] for p in RIDERS + FIXED}
    base["nut"][2][3] = 100.0
    led = {"sizes": {}}
    for t in tags:
        poses = {"R": {"phi_deg": 0.0, "dz_mm": 0.0, "placements": base}}
        for pose, dz in (("Kd1", dz_kd1), ("Kmax", dz_kmax)):
            phi = 2 * math.pi * dz / lead
            pl = {k: [row[:] for row in v] for k, v in base.items()}
            pl["nut"] = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, base["nut"][2][3] + dz], [0, 0, 0, 1]] if pure_z else mat_mul(screw(phi, lead), base["nut"])
            if move_part:
                pl[move_part][0][3] += 1.0
            poses[pose] = {"phi_deg": math.degrees(phi), "dz_mm": dz, "placements": pl}
        led["sizes"][t] = poses
    return led


# ------------------------------------------------------------------ interference report (G6)
ROW_RE = re.compile(r"^\|\s*(?P<pair>[^|]+?)\s*\|\s*(?P<pose>R|Kd1|Kmax)\s*\|\s*(?P<mm3>[^|]+?)\s*\|\s*(?P<dist>[^|]+?)\s*\|\s*(?P<cls>[CGFP])\s*\|\s*(?P<res>pass|FAIL)\s*\|\s*$")


def report_rows(text):
    """{tag: [row dicts]} from '## Size <tag>' sections; rows `| a / b | pose | mm3 | dist_mm | class | result |`."""
    out, tag = {}, None
    for ln in text.splitlines():
        m = re.match(r"^##\s+Size\s+(\S+)", ln)
        if m:
            tag = m.group(1)
            out[tag] = []
        elif tag and (rm := ROW_RE.match(ln)):
            out[tag].append(rm.groupdict())
    return out


def report_errors(rows, probes, T, tol=6e-4):
    """rows: report_rows()[tag]; probes: {pose: pose-probe dict}. Every cell must equal the probe value and the recomputed verdict."""
    e = []
    seen = set()
    for r in rows:
        key = r["pair"].replace(" / ", "|")
        pd = probes.get(r["pose"])
        seen.add((key, r["pose"]))
        if pd is None:
            e.append(f"{key} {r['pose']}: no probe")
            continue
        verdict = dict(pair_violations(pd, r["pose"], T)).get(key)
        if verdict is None:
            e.append(f"{key} {r['pose']}: not in the pair tables")
            continue
        if key in pd["pairs"]:
            m = pd["pairs"][key]
            want_mm3, want_dist = m["overlap_mm3"], m["min_dist"]
        else:
            want_mm3, want_dist = None, pd["feature_pairs"][key]["gap"]
        try:
            got_dist = float(r["dist"])
            got_mm3 = None if r["mm3"] == "-" else float(r["mm3"])
        except ValueError:
            e.append(f"{key} {r['pose']}: unreadable cell")
            continue
        if (want_mm3 is None) != (got_mm3 is None) or (want_mm3 is not None and abs(got_mm3 - want_mm3) > tol):
            e.append(f"{key} {r['pose']}: mm3 {r['mm3']} vs probe {want_mm3}")
        if abs(got_dist - want_dist) > tol:
            e.append(f"{key} {r['pose']}: dist {r['dist']} vs probe {want_dist}")
        if r["cls"] != pair_class_letter(key, r["pose"], T):
            e.append(f"{key} {r['pose']}: class {r['cls']} vs ASSEMBLY.md")
        if r["res"] != ("pass" if not verdict else "FAIL"):
            e.append(f"{key} {r['pose']}: result {r['res']} vs recomputed")
    want = len(T["rels"]) + len(T["feats"])
    for pose in probes:
        n = sum(1 for k, p in seen if p == pose)
        if n != want:
            e.append(f"pose {pose}: {n} rows vs {want}")
    return e
