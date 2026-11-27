"""Controls for 1.4 step 0 (research/sean/cr_scratch/step1.4_engineer_step0.md; Step 1.3 gate G2 to G5, Design Notes 25
C1.3-a, C1.3-b). Harness controls return a check result {id, result, reason, n_issues} (result "pass" = clean, "fail" =
fires); drawing controls return a context.

R1 c  FAST: the fast tier list fixtures/fast.yaml keeps every check family's Z and one B per branch (branch: the
      manifest finding that added it, or the control itself when it names no finding).
R2    DEPS: records carry deps (spec, script, certifier records); --stale deps branch on temporary trees (tempfile, under
      TMP), never on the live records.
R3    M1C: check_sketch.py --m1-controls (blinded reviewer control figures; key outside the project root and the out
      folder).
R4    K4 rule (l) by class: reference lines, gridlines, part edges, in side, plan and section views and every declared
      Axes, on the live drawings of record.
R5    C1.3-b items: not_drawn literal x bands (R2-6), the arc plan-only branch (R2-7), terminator form (DR4-2), every number
      of a stall literal (rule (j) NOTE).
Each B was run on the pre-change code (copy of docs/sketches/ before the first step 0 edit) first; observed results in the
step 0 file, section 8.
"""
import copy
import json
import math
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent
for p in (str(SK), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import check_sketch as cs  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import Params, load_spec, load_yaml  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402


def _res(cid, fired, reason, n_issues):
    return {"id": cid, "result": "fail" if fired else "pass", "reason": reason, "n_issues": n_issues}


def _builders():
    import builders
    return builders


def _s3fx():
    import s3_fixtures
    return s3_fixtures


# ======================================================================== R1 c: fast tier lint

def _branches(man):
    """{check: {"Z": [ids], "B": {branch: [ids]}}}: a B's branch is its manifest finding, or its own id without one."""
    out = {}
    for e in man:
        t = out.setdefault(e["check"], {"Z": [], "B": {}})
        if e["control"] == "Z":
            t["Z"].append(e["id"])
        elif e["control"] == "B":
            t["B"].setdefault(str(e.get("finding") or "own:" + e["id"]), []).append(e["id"])
    return out


def fast_issues(man, fast):
    fs = set(fast)
    issues = [f"fast.yaml id {i} not in the manifest" for i in sorted(fs - {e['id'] for e in man})]
    for chk, t in sorted(_branches(man).items()):
        if t["Z"] and not fs & set(t["Z"]):
            issues.append(f"{chk} has no Z in the fast tier")
        for br, ids in sorted(t["B"].items()):
            if not fs & set(ids):
                issues.append(f"{chk} branch {br!r} has no B in the fast tier")
    return issues


def _fast_res(fast):
    man = load_yaml(cs.MANIFEST)["controls"]
    iss = fast_issues(man, fast)
    return _res("FAST", bool(iss), sc._summ(iss) if iss else f"{len(fast)} fast control(s): every family's Z, one B per branch", len(iss))


def fast_z():
    """FAST Z: the live fast.yaml keeps every check family's Z and one B per branch."""
    return _fast_res(cs.fast_ids())


def fast_b_no_z():
    """FAST B: fast.yaml with every K4 Z removed."""
    man = load_yaml(cs.MANIFEST)["controls"]
    kz = {e["id"] for e in man if e["check"] == "K4" and e["control"] == "Z"}
    return _fast_res([i for i in cs.fast_ids() if i not in kz])


def fast_b_branch():
    """FAST B: fast.yaml with the B of branch 'Designer NOTE D-r3-1' of K8 removed (K8-B89 and its branch mates)."""
    man = load_yaml(cs.MANIFEST)["controls"]
    br = {e["id"] for e in man if e["check"] == "K8" and e["control"] == "B" and str(e.get("finding")) == "Designer NOTE D-r3-1"}
    return _fast_res([i for i in cs.fast_ids() if i not in br])


def run_dst_fast():
    """RUN Z: controls_dst of the live manifest with fast set is the partial destination, never the record."""
    got = cs.controls_dst(cs.MANIFEST, None, True) if "fast" in cs.controls_dst.__code__.co_varnames else cs.controls_dst(cs.MANIFEST, None)
    ok = got == ("partial", cs.CONTROLS_PARTIAL)
    return _res("RUN", not ok, f"controls_dst(live, only None, fast) = {got}", 0 if ok else 1)


# ======================================================================== R2: record deps and the --stale deps branch

_TMPS = []


def _tmp():
    for t in _TMPS:
        shutil.rmtree(t, ignore_errors=True)
    del _TMPS[:]
    t = tempfile.mkdtemp(prefix="deps_")
    _TMPS.append(t)
    return Path(t)


import atexit  # noqa: E402
atexit.register(lambda: [shutil.rmtree(t, ignore_errors=True) for t in _TMPS])


def _deps_tree(with_s3=True, s3_deps=True):
    """Temporary docs/ and wip/: the accepted S1 r8 and S2 r9 records (exempt), copies of s3_spec.yaml and
    s3_jackscrew_section.py, and an accepted S3 r7 record whose deps name them and the two certifier records (a refreshed
    record, as run_sketch writes it)."""
    t = _tmp()
    docs, wip = t / "docs", t / "wip"
    docs.mkdir()
    wip.mkdir()
    for n in ("s1_checks_r8.json", "s2_checks_r9.json", "s3_spec.yaml", "s3_jackscrew_section.py", "s1_spec.yaml", "s1_side_poses.py"):
        shutil.copyfile(SK / n, docs / n)
    if with_s3:
        rec = json.loads((SK / "s3_checks_r7.json").read_text(encoding="utf-8"))
        rec.pop("superseded_by", None)
        rec["accepted"] = True
        if s3_deps and hasattr(cs, "record_deps"):
            rec["deps"] = _deps(docs / "s3_spec.yaml", docs / "s3_jackscrew_section.py",
                                {"s1": docs / "s1_checks_r8.json", "s2": docs / "s2_checks_r9.json"}, docs)
        (docs / "s3_checks_r7.json").write_text(json.dumps(rec), encoding="utf-8")
    return docs, wip


def _deps(spec, script, certs, docs):
    """deps as record_deps writes them, with paths relative to the temporary docs/."""
    d = cs.record_deps(spec, script, certs)
    d["spec"]["path"], d["script"]["path"] = Path(spec).name, Path(script).name
    return d


def _stale_deps(docs, wip):
    """The deps branch; on the pre-change code (no stale_deps) the keys-only --stale, so a B reads clean there."""
    if hasattr(cs, "stale_deps"):
        return cs.stale_deps(docs, wip)
    return [], cs.stale_diffs(Params(), cs.stale_records(docs, wip))


def _deps_res(docs, wip, what):
    notes, diffs = _stale_deps(docs, wip)
    return _res("DEPS", bool(diffs), sc._summ(diffs) if diffs else f"{what}: --stale deps clean; {len(notes)} exempt", len(diffs))


def _s1_r9(docs, deps=True):
    """S1 r9 accepted over r8 in docs (r8 superseded_by 9), with deps of its own unless deps is False."""
    r8p = docs / "s1_checks_r8.json"
    r8 = json.loads(r8p.read_text(encoding="utf-8"))
    r9 = copy.deepcopy(r8)
    r9["rev"] = 9
    r9.pop("superseded_by", None)
    if deps and hasattr(cs, "record_deps"):
        r9["deps"] = _deps(docs / "s1_spec.yaml", docs / "s1_side_poses.py", {}, docs)
    (docs / "s1_checks_r9.json").write_text(json.dumps(r9), encoding="utf-8")
    r8["superseded_by"] = 9
    r8p.write_text(json.dumps(r8), encoding="utf-8")


def deps_z():
    """DEPS Z: refreshed S3 record with deps; S1 r8 and S2 r9 exempt: clean."""
    docs, wip = _deps_tree()
    return _deps_res(docs, wip, "refreshed tree")


def deps_b1_superseded():
    """DEPS B1: a temporary S1 r9 accepted over r8: the S3 certifier is superseded."""
    docs, wip = _deps_tree()
    _s1_r9(docs)
    return _deps_res(docs, wip, "S1 r9 over r8")


def deps_b2_cert_edited():
    """DEPS B2: the certifier record s1_checks_r8.json edited (one field added): its SHA-256 differs."""
    docs, wip = _deps_tree()
    p = docs / "s1_checks_r8.json"
    r = json.loads(p.read_text(encoding="utf-8"))
    r["edited"] = "one field"
    p.write_text(json.dumps(r), encoding="utf-8")
    return _deps_res(docs, wip, "certifier edited")


def deps_b3_spec_class():
    """DEPS B3: one neighbour class edited in the temporary s3_spec.yaml (the first 'class: C' to 'class: G')."""
    docs, wip = _deps_tree()
    p = docs / "s3_spec.yaml"
    t = p.read_text(encoding="utf-8")
    p.write_text(t.replace("class: C", "class: G", 1), encoding="utf-8", newline="")
    return _deps_res(docs, wip, "spec class edited")


def deps_b4_script_comment():
    """DEPS B4: one comment byte changed in the temporary s3_jackscrew_section.py."""
    docs, wip = _deps_tree()
    p = docs / "s3_jackscrew_section.py"
    b = p.read_bytes()
    i = b.index(b"# ")
    p.write_bytes(b[:i + 2] + (b"X" if b[i + 2:i + 3] != b"X" else b"Y") + b[i + 3:])
    return _deps_res(docs, wip, "script comment edited")


def deps_b5_no_deps():
    """DEPS B5: the accepted S3 r7 record without deps (not exempt)."""
    docs, wip = _deps_tree(s3_deps=False)
    return _deps_res(docs, wip, "S3 record without deps")


def deps_b6_later_rev():
    """DEPS B6: S1 r9 accepted over r8 with no deps (the exemption names s1 r8 only); no S3 record in the tree."""
    docs, wip = _deps_tree(with_s3=False)
    _s1_r9(docs, deps=False)
    return _deps_res(docs, wip, "S1 r9 without deps")


def deps_run_s3():
    """DEPS Z2: a live s3 run (records from docs/sketches/) writes deps: spec, script and the S1 and S2 certifiers the
    S3-3 check resolved, each with its SHA-256; the record goes to a temporary wip/ directory."""
    t = _tmp()
    rc = cs.main(["s3", "--rev", "7", "--wip-dir", str(t)])   # noqa: F841 (the record's checks are not judged here)
    rec = json.loads((t / "s3_checks_r7.json").read_text(encoding="utf-8"))
    d = rec.get("deps") or {}
    iss = []
    if d.get("spec", {}).get("path") != "s3_spec.yaml" or d.get("spec", {}).get("sha256") != cs._sha(SK / "s3_spec.yaml"):
        iss.append(f"deps spec {d.get('spec')}")
    if d.get("script", {}).get("path") != "s3_jackscrew_section.py" or d.get("script", {}).get("sha256") != cs._sha(SK / "s3_jackscrew_section.py"):
        iss.append(f"deps script {d.get('script')}")
    got = {(c["sketch"], c["path"], c["sha256"]) for c in d.get("certifiers") or []}
    want = {(s, n, cs._sha(SK / n)) for s, n in (("s1", "s1_checks_r8.json"), ("s2", "s2_checks_r9.json"))}
    if got != want:
        iss.append(f"deps certifiers {sorted(got)} against {sorted(want)}")
    return _res("DEPS", bool(iss), sc._summ(iss) if iss else "s3 run records deps: spec, script, certifiers s1 r8 and s2 r9", len(iss))


# ======================================================================== R3: blinded M1 reviewer control figures

def _m1(out, key, **kw):
    if not hasattr(cs, "m1_controls"):
        return None
    return cs.m1_controls(out, key, **kw)


def m1c_z():
    """M1C Z: one run into an empty folder, key beside it (outside the project root): four PNGs m1c_<token>.png, no other
    file, four distinct tokens, four key entries naming the four roles."""
    t = _tmp()
    out, key = t / "out", t / "key.json"
    r = _m1(out, key)
    if r is None:
        return _res("M1C", True, "no --m1-controls command", 1)
    rc, msgs, toks = r
    files = sorted(p.name for p in out.iterdir()) if out.is_dir() else []
    k = json.loads(key.read_text(encoding="utf-8")) if key.is_file() else []
    iss = []
    if rc != 0:
        iss.append(f"exit {rc}: {msgs}")
    if len(files) != 4 or not all(f.startswith("m1c_") and f.endswith(".png") for f in files):
        iss.append(f"{len(files)} file(s) in the out folder, need four m1c_<token>.png")
    if len(set(toks)) != 4 or len(k) != 4 or {e["token"] for e in k} != set(toks):
        iss.append(f"{len(set(toks))} distinct token(s), {len(k)} key entr(ies)")
    if {e.get("role") for e in k} != {"side_drill_tip_up", "side_correct", "plan_ccw", "plan_mirrored"}:
        iss.append("key roles differ from the four control roles")
    return _res("M1C", bool(iss), sc._summ(iss) if iss else "4 PNGs, 4 distinct tokens, 4 key entries, no other file", len(iss))


def _refusal(out, key, what):
    r = _m1(out, key)
    if r is None:
        return _res("M1C", False, "no --m1-controls command (pre-change: control figures and key.json written to wip/fixtures/figs)", 0)
    rc, msgs, _ = r
    ref = [m for m in msgs if m.startswith("refused")]
    return _res("M1C", rc != 0, "; ".join(ref) if ref else f"{what}: not refused ({msgs})", len(ref))


def m1c_b1_key_in_root():
    """M1C B1: key path inside the project root (docs/sketches/wip/m1c_key.json; refused before any write)."""
    t = _tmp()
    return _refusal(t / "out", SK / "wip" / "m1c_key_never_written.json", "key in root")


def m1c_b2_out_not_empty():
    """M1C B2: out folder holding one file."""
    t = _tmp()
    (t / "out").mkdir()
    (t / "out" / "old.png").write_bytes(b"x")
    return _refusal(t / "out", t / "key.json", "out not empty")


def m1c_b3_key_in_out():
    """M1C B3: key path inside the (empty) out folder."""
    t = _tmp()
    return _refusal(t / "out", t / "out" / "key.json", "key in out")


def _two_runs(token=None):
    t = _tmp()
    a = _m1(t / "a", t / "ka.json", token=token)
    b = _m1(t / "b", t / "kb.json", token=token)
    if a is None or b is None:
        return None
    return set(a[2]), set(b[2])


def m1c_z2_disjoint():
    """M1C Z2: two runs give disjoint token sets (counts only)."""
    r = _two_runs()
    if r is None:
        return _res("M1C", True, "no --m1-controls command", 1)
    a, b = r
    sh = len(a & b)
    return _res("M1C", sh > 0, f"token sets {len(a)} and {len(b)}, {sh} shared", int(sh > 0))


def m1c_b4_fixed_token():
    """M1C B4: the token source pinned (a stand-in for a non-random generator): the two runs share tokens."""
    seq = iter(["aaaaaa", "bbbbbb", "cccccc", "dddddd"] * 2)
    r = _two_runs(token=lambda: next(seq))
    if r is None:
        return _res("M1C", False, "no --m1-controls command", 0)
    a, b = r
    sh = len(a & b)
    return _res("M1C", sh > 0, f"token sets overlap: {sh} shared of {len(a)} and {len(b)}", int(sh > 0))


# ======================================================================== R4: K4 rule (l) by class

def _live(s):
    return _builders()._script_ctx(s)


def _ax_of(c, aid):
    fig = sc.real_figure(next(iter(c.figs.values())))
    return next(a for a in fig.axes if getattr(a, "sketch_axes", None) == aid)


def _clip(p0, p1, x0, x1, y0, y1):
    """The leader inside the Axes box (sketch_common._clip_box; a local copy so the fixture runs on the pre-change code)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, p0[0] - x0), (dx, x1 - p0[0]), (-dy, p0[1] - y0), (dy, y1 - p0[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return None
            continue
        r = q / p
        t0, t1 = (max(t0, r), t1) if p < 0 else (t0, min(t1, r))
        if t0 > t1:
            return None
    return (p0[0] + t0 * dx, p0[1] + t0 * dy), (p0[0] + t1 * dx, p0[1] + t1 * dy)


def _leader(ax, fid=None):
    """(fid, p0, p1): the label leader of fid (or the longest leader in the Axes), text end clipped to the Axes box."""
    (x0, x1), (y0, y1) = sorted(ax.get_xlim()), sorted(ax.get_ylim())
    best = None
    for t in ax.texts:
        g = t.get_gid() or ""
        if not g.startswith("label:") or getattr(t, "xyann", None) is None or (fid and g != f"label:{fid}"):
            continue
        seg = _clip((float(t.xyann[0]), float(t.xyann[1])), (float(t.xy[0]), float(t.xy[1])), x0, x1, y0, y1)
        if seg is None:
            continue
        L = math.hypot(seg[1][0] - seg[0][0], seg[1][1] - seg[0][1])
        if best is None or L > best[0]:
            best = (L, g[6:], seg[0], seg[1])
    return best[1], best[2], best[3]


def _beside(p0, p1, off=0.5, width=3.0):
    """Segment along p0-p1 from 20 to 80 percent of its length, offset off mm across it, and a quad width mm wide beyond it."""
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    d = ((p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L)
    n = (-d[1], d[0])
    a = (p0[0] + 0.2 * L * d[0] + off * n[0], p0[1] + 0.2 * L * d[1] + off * n[1])
    b = (p0[0] + 0.8 * L * d[0] + off * n[0], p0[1] + 0.8 * L * d[1] + off * n[1])
    quad = [a, b, (b[0] + width * n[0], b[1] + width * n[1]), (a[0] + width * n[0], a[1] + width * n[1])]
    return a, b, quad


def _plant(c, aid, gid, kind, fid=None, poses=None):
    """Plants one line of family kind beside a label leader in Axes aid of every figure kept (poses): a Line2D tagged
    gid (reference line) or a filled quad tagged gid (part edge), 0.5 mm off the leader over 60 percent of it."""
    if poses:
        c.figs = {p: c.figs[p] for p in poses}
    for fig in c.figs.values():
        ax = _ax_of(c, aid) if len(c.figs) == 1 else next(a for a in sc.real_figure(fig).axes if getattr(a, "sketch_axes", None) == aid)
        f, p0, p1 = _leader(ax, fid)
        a, b, quad = _beside(p0, p1)
        if kind == "reference line":
            sc.draw(gid, Line2D([a[0], b[0]], [a[1], b[1]], lw=0.6), ax)
        else:
            sc.draw(gid, Polygon(quad, closed=True, facecolor="0.85", edgecolor="0.3", zorder=1), ax)
    return c


def k4_l_side_ref():
    """K4 B (rule (l), side view, reference line): live S1 at pose load; a height_target reference line planted along the
    longest leader. The live height_target leader on the z 2000 gridline fires too (dry-run firing)."""
    return _plant(_live("s1"), "main", "height_target", "reference line", poses=["load"])


def k4_l_side_edge():
    """K4 B (rule (l), side view, part edge): live S1 at pose load; a filled base_plate quad planted with one edge along
    the longest leader. The live height_target firing reads too."""
    return _plant(_live("s1"), "main", "base_plate", "part edge", poses=["load"])


def k4_l_plan_ref():
    """K4 B (rule (l), plan view, reference line): live S2; a sightline_f6 line planted along the longest leader. The
    three live gridline firings read too."""
    return _plant(_live("s2"), "main", "sightline_f6", "reference line")


def k4_l_plan_edge():
    """K4 B (rule (l), plan view, part edge): live S2; a filled ring quad planted with one edge along the longest leader.
    The three live gridline firings read too."""
    return _plant(_live("s2"), "main", "ring", "part edge")


def k4_l_section_edge():
    """K4 B (rule (l), section view, part edge; r6 reviewer N1 class): live S3; a filled motor23_c quad planted with one
    edge along the longest section leader. The live inset gridline firing reads too."""
    return _plant(_live("s3"), "section", "motor23_c", "part edge")


def _family_firings(s, aids=None):
    """[(Axes id, issue, family)] of rule (l) on the live sketch s by Axes (every declared Axes, or aids)."""
    c = _live(s)
    subs = [(d["id"], x) for d, x in sc.axes_contexts(c)] if sc.needs_split(c) else [("main", c)]
    out = []
    for aid, x in subs:
        if aids and aid not in aids:
            continue
        for msg in sc.collinear_issues(x):
            fam = "gridline" if " along gridline " in msg else ("part edge" if " along part edge of " in msg else "reference line")
            out.append((aid, msg, fam))
    return out


def k4_l_live_edges_refs():
    """K4 Z (rule (l)): live S1 r8, S2 r9, S3 r7 drawn by their scripts: no part-edge and no reference-line firing in any
    Axes (side, plan, section, inset); the r6 reviewer's part-edge reading of r7 (clean) reproduced."""
    bad = [f"{s} [{aid}] {m}" for s in ("s1", "s2", "s3") for aid, m, fam in _family_firings(s) if fam != "gridline"]
    return _res("K4", bool(bad), sc._summ(bad) if bad else "live S1, S2, S3: 0 part-edge and 0 reference-line firings in every Axes", len(bad))


def k4_l_live_section():
    """K4 Z (rule (l)): live S3 r7 section Axes: no firing in any family (reference line, gridline, part edge)."""
    bad = [m for aid, m, fam in _family_firings("s3", aids=("section",))]
    return _res("K4", bool(bad), sc._summ(bad) if bad else "live S3 section Axes: 0 firings, every family", len(bad))


def k4_l_clip_relief():
    """K4 Z (rule (l) premise: a part edge counts only where drawn): live S3 section; the K4-B (section part edge) quad
    planted with a clip path that leaves out the leader's side of the quad, so the collinear edge is not drawn: no
    firing in the section Axes."""
    c = _live("s3")
    ax = _ax_of(c, "section")
    f, p0, p1 = _leader(ax)
    a, b, quad = _beside(p0, p1)
    poly = sc.draw("motor23_c", Polygon(quad, closed=True, facecolor="0.85", edgecolor="0.3", zorder=1), ax)
    mid = [((quad[0][0] + quad[3][0]) / 2, (quad[0][1] + quad[3][1]) / 2), ((quad[1][0] + quad[2][0]) / 2, (quad[1][1] + quad[2][1]) / 2), quad[2], quad[3]]
    clip = Polygon(mid, closed=True, transform=ax.transData)
    poly.set_clip_path(clip)
    sub = sc.axes_context(c, "section")
    bad = sc.collinear_issues(sub)
    return _res("K4", bool(bad), sc._summ(bad) if bad else "clipped edge along the leader not drawn: 0 firings", len(bad))


# ======================================================================== R5: C1.3-b items

def nd_literal_band():
    """K8 B (Topologist NOTE R2-6): the pinions entry with its literal x bands re-planted (-144.05 to -65.09, 65.09 to
    144.05): two bands read no key."""
    def sm(sp):
        for e in sp["not_drawn"]:
            if e.get("part") == "pinions a and b":
                e["x"] = [[-144.05, -65.09], [65.09, 144.05]]
    return _s3fx().s3_ctx(spec_mut=sm)


def arc_on_section_row():
    """K5 B (Topologist NOTE R2-7, arc a1 plan-only branch): screw_c declares sub_artists arc with an arc field and draws
    screw_c:arc in the section Axes."""
    fx = _s3fx()

    def sm(sp):
        r = fx._row(sp, "screw_c")
        r["sub_artists"] = list(r.get("sub_artists") or []) + ["arc"]
        r["arc"] = {"r": 40, "theta0": 0, "theta1": 90}

    def m(fig, ax, axi, P, spec, *a):
        fx._draw_arc(ax, P, fx._row(spec, "screw_c"))
    return fx.s3_ctx(spec_mut=sm, mutate=m)


def _span_arrow(**kw):
    """The live S3 drawn by its script, one span_lt terminator re-styled (the K8-Z17 drawing otherwise)."""
    c = _live("s3")
    arr = next(x for x in sc.tagged(_ax_of(c, "section"))["span_lt"] if type(x).__name__ == "FancyArrowPatch")
    for k, v in kw.items():
        getattr(arr, f"set_{k}")(v)
    return c


def term_head_wide():
    """K8 B (Designer NOTE DR4-2, head size): one span_lt terminator drawn at mutation_scale 30 against the signed 14 (head
    half-width 5.1 mm against 2.38, DERIVED at dpi 150), still on its line."""
    return _span_arrow(mutation_scale=30)


def term_curved():
    """K8 B (Designer NOTE DR4-2, connection style): one span_lt terminator drawn with connectionstyle arc3 rad 0.2 (both
    ends still on the line)."""
    return _span_arrow(connectionstyle="arc3,rad=0.2")


def stall_second_number():
    """K4 B (r6 reviewer NOTE on rule (j)): the live S3 with the stall_up literal's second number 282.21 written 283.21."""
    def sm(sp):
        for c in sp["load_cases"]["cases"]:
            if c["id"] == "stall_up":
                c["per_screw"] = c["per_screw"].replace("282.21", "283.21")
    return _builders()._script_ctx("s3", spec_mut=sm)
