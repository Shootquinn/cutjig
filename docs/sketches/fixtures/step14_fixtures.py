"""Controls for 1.4 step 0 (research/sean/cr_scratch/step1.4_engineer_step0.md; Step 1.3 gate G2 to G5, Design Notes 25
C1.3-a, C1.3-b). Harness controls return a check result {id, result, reason, n_issues} (result "pass" = clean, "fail" =
fires); drawing controls return a context.

R1 c  FAST: the fast tier list fixtures/fast.yaml keeps, per check family, a Z and a B, and every smoke control
      (Software Engineer P0S ruling, FIX 2; P0f).
R2    DEPS: records carry deps (spec, script, certifier records); --stale deps branch on temporary trees (tempfile, under
      TMP), never on the live records.
R3    M1C: check_sketch.py --m1-controls (blinded reviewer control figures; key outside the project root and the out
      folder).
R4    K4 rule (l) by class: reference lines, gridlines, part edges, in side, plan and section views and every declared
      Axes, on the live drawings of record.
R5    C1.3-b items: not_drawn literal x bands (R2-6), the arc plan-only branch (R2-7), terminator form (DR4-2), every number
      of a stall literal (rule (j) NOTE).
P0f (research/sean/cr_scratch/step1.4_engineer_step0_fixes.md): Software Engineer FIX 1 to 9, Designer FIX L1 to L4, J1,
Topologist FIX TP1.4-1, Loftsman FIX 1 to 3.
Each B was run on the pre-change code (copy of docs/sketches/ before the first edit of the pass) first, or shown red by
branch deletion where the branch existed; observed results in the step 0 file, section 8, and the P0f file, section 2.
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

def _families(man):
    """{check: {"Z": [ids], "B": [ids]}} and the smoke ids of the manifest."""
    out, smoke = {}, []
    for e in man:
        if e["control"] == "smoke":
            smoke.append(e["id"])
            continue
        out.setdefault(e["check"], {"Z": [], "B": []}).setdefault(e["control"], []).append(e["id"])
    return out, smoke


def fast_issues(man, fast):
    """Software Engineer P0S fast-tier ruling (FIX 2): every check family with a Z keeps a Z, every family with a B keeps a
    B, and every smoke control is listed; branch coverage is the full set's job at every run of record."""
    fs = set(fast)
    issues = [f"fast.yaml id {i} not in the manifest" for i in sorted(fs - {e['id'] for e in man})]
    fam, smoke = _families(man)
    for chk, t in sorted(fam.items()):
        if t.get("Z") and not fs & set(t["Z"]):
            issues.append(f"{chk} has no Z in the fast tier")
        if t.get("B") and not fs & set(t["B"]):
            issues.append(f"{chk} has no B in the fast tier")
    issues += [f"smoke {i} not in the fast tier" for i in smoke if i not in fs]
    return issues


def _fast_res(fast):
    man = load_yaml(cs.MANIFEST)["controls"]
    iss = fast_issues(man, fast)
    return _res("FAST", bool(iss), sc._summ(iss) if iss else f"{len(fast)} fast control(s): every family's Z and B, every smoke control", len(iss))


def fast_z():
    """FAST Z: the live fast.yaml keeps every check family's Z and B and every smoke control."""
    return _fast_res(cs.fast_ids())


def fast_b_no_z():
    """FAST B: fast.yaml with every K4 Z removed."""
    man = load_yaml(cs.MANIFEST)["controls"]
    kz = {e["id"] for e in man if e["check"] == "K4" and e["control"] == "Z"}
    return _fast_res([i for i in cs.fast_ids() if i not in kz])


def fast_b_family_b():
    """FAST B (P0S FIX 2, re-planted at P0f): fast.yaml with every K8 B removed."""
    man = load_yaml(cs.MANIFEST)["controls"]
    kb = {e["id"] for e in man if e["check"] == "K8" and e["control"] == "B"}
    return _fast_res([i for i in cs.fast_ids() if i not in kb])


def fast_b_smoke():
    """FAST B (P0S FIX 2): fast.yaml with S2-FULL removed."""
    return _fast_res([i for i in cs.fast_ids() if i != "S2-FULL"])


def run_fast_call_site():
    """RUN B (P0S FIX 1, the --fast call site; the form of RUN-B4): controls() run in process with fast set on a temporary
    one-row manifest (K1-Z) set as cs.MANIFEST, the tier list patched to K1-Z and cs.output_path pointed at a temporary
    folder; all restored before return. Fires ("fast run") when only the partial file is written; if the call site
    dropped fast, the record would be written and the control reads clean."""
    import argparse
    import contextlib
    import io
    import yaml
    t = _tmp()
    man = {e["id"]: e for e in load_yaml(cs.MANIFEST)["controls"]}
    mp = t / "manifest.yaml"
    mp.write_text(yaml.safe_dump({"controls": [dict(man["K1-Z"])]}, sort_keys=False), encoding="utf-8")

    def out_path(name, wip=True):
        q = t / "wip" / name
        q.parent.mkdir(parents=True, exist_ok=True)
        return q
    saved = (cs.MANIFEST, cs.output_path, cs.fast_ids)
    try:
        cs.MANIFEST, cs.output_path, cs.fast_ids = mp, out_path, (lambda path=None: ["K1-Z"])
        with contextlib.redirect_stdout(io.StringIO()):
            rc = cs.controls(argparse.Namespace(manifest=None, only=None, fast=True, jobs=1))
    finally:
        cs.MANIFEST, cs.output_path, cs.fast_ids = saved
    rec, part = (t / "wip" / cs.CONTROLS_RESULTS).is_file(), (t / "wip" / cs.CONTROLS_PARTIAL).is_file()
    fired = rc == 0 and part and not rec
    return _res("RUN", fired, f"fast run: exit {rc}; partial file written {part}; full-results path written {rec}", 1 if fired else 0)


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
    for n in ("s1_checks_r8.json", "s2_checks_r9.json", "s3_spec.yaml", "s3_jackscrew_section.py", "s1_spec.yaml", "s1_side_poses.py",
              "s2_spec.yaml", "s2_plan.py", "s1_mass_report_r8.json"):
        shutil.copyfile(SK / n, docs / n)
    if with_s3:
        rec = json.loads((SK / "s3_checks_r7.json").read_text(encoding="utf-8"))
        rec.pop("superseded_by", None)
        rec["accepted"] = True
        if s3_deps and hasattr(cs, "record_deps"):
            rec["deps"] = _deps(docs / "s3_spec.yaml", docs / "s3_jackscrew_section.py",
                                {"s1": docs / "s1_checks_r8.json", "s2": docs / "s2_checks_r9.json"}, docs,
                                specs_read=[docs / "s1_spec.yaml", docs / "s2_spec.yaml", docs / "s3_spec.yaml"])
        (docs / "s3_checks_r7.json").write_text(json.dumps(rec), encoding="utf-8")
    return docs, wip


def _deps(spec, script, certs, docs, specs_read=None, files=None):
    """deps as record_deps writes them, with paths relative to the temporary docs/ (the pre-change three-argument form
    when record_deps takes no spec_read)."""
    try:
        d = cs.record_deps(spec, script, certs, specs_read, files)
    except TypeError:
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
    """DEPS B5 (re-planted at P0f, P0S FIX 4 b): a record never exempt, s4_checks_r1.json, accepted without deps."""
    docs, wip = _deps_tree()
    (docs / "s4_checks_r1.json").write_text(json.dumps({"sketch": "s4", "rev": 1, "accepted": True}), encoding="utf-8")
    return _deps_res(docs, wip, "S4 record without deps")


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
    sr = {(x.get("path"), x.get("sha256")) for x in d.get("spec_read") or []}   # P0f (Loftsman P0L FIX 2)
    want_sr = {(n, cs._sha(SK / n)) for n in ("s1_spec.yaml", "s2_spec.yaml")}
    if sr != want_sr:
        iss.append(f"deps spec_read {sorted(sr)} against {sorted(want_sr)}")
    return _res("DEPS", bool(iss), sc._summ(iss) if iss else "s3 run records deps: spec, script, spec_read s1 and s2 specs, certifiers s1 r8 and s2 r9", len(iss))


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


def _nopath(m, *paths):
    """A refusal message with its absolute paths written <path> (P0S NOTE 1: per-control equality between runs)."""
    for p in sorted({str(x) for q in paths if q is not None for x in (q, Path(q).resolve())}, key=len, reverse=True):
        m = m.replace(p, "<path>")
    return m


def _refusal(out, key, what, root=None):
    r = _m1(out, key, **({"root": root} if root is not None else {}))
    if r is None:
        return _res("M1C", False, "no --m1-controls command (pre-change: control figures and key.json written to wip/fixtures/figs)", 0)
    rc, msgs, _ = r
    rt = cs.find_root_dir() if hasattr(cs, "find_root_dir") else None
    ref = [_nopath(m, out, key, root, rt) for m in msgs if m.startswith("refused")]
    return _res("M1C", rc != 0, "; ".join(ref) if ref else f"{what}: not refused ({[_nopath(m, out, key, root, rt) for m in msgs]})", len(ref))


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
    longest leader. The live guide_b firing (drawn line, P0f) reads too."""
    return _plant(_live("s1"), "main", "height_target", "reference line", poses=["load"])


def k4_l_side_edge():
    """K4 B (rule (l), side view, part edge): live S1 at pose load; a filled base_plate quad planted with one edge along
    the longest leader. The live guide_b firing (drawn line, P0f) reads too."""
    return _plant(_live("s1"), "main", "base_plate", "part edge", poses=["load"])


def k4_l_plan_ref():
    """K4 B (rule (l), plan view, reference line): live S2; a sightline_f6 line planted along the longest leader. The
    three live firings (P0f) read too."""
    return _plant(_live("s2"), "main", "sightline_f6", "reference line")


def k4_l_plan_edge():
    """K4 B (rule (l), plan view, part edge): live S2; a filled ring quad planted with one edge along the longest leader.
    The three live firings (P0f) read too."""
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
            out.append((aid, msg, _fam_of(msg)))
    return out


def _fam_of(msg):
    for key, fam in ((" along gridline ", "gridline"), (" along part edge of ", "part edge"), (" along drawn line of ", "drawn line"),
                     (" along leader of ", "leader"), ("rule (l) premise", "premise")):
        if key in msg:
            return fam
    return "reference line"


def k4_l_live_edges_refs():
    """K4 Z (rule (l); re-scoped at P0f): live S1 r8, S2 r9, S3 r7 drawn by their scripts: no reference-line, leader or
    premise firing in any Axes (side, plan, section, inset). The live part-edge (S2 keepout on pinion_b, TP1.4-1) and
    drawn-line (S1 guide_b on pinion_axis_b, FIX L2) firings are expected reds, read by K4-Z3, Z4 (B until P6)."""
    bad = [f"{s} [{aid}] {m}" for s in ("s1", "s2", "s3") for aid, m, fam in _family_firings(s) if fam in ("reference line", "leader", "premise")]
    return _res("K4", bool(bad), sc._summ(bad) if bad else "live S1, S2, S3: 0 reference-line, 0 leader and 0 premise firings in every Axes", len(bad))


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


# ======================================================================== P0f: deps (Software Engineer FIX 3, 4; Loftsman FIX 1 to 3)

def _accept_copy(docs, src, dst_rev, deps=None):
    """In a temporary docs/: src record copied as revision dst_rev of its sketch, accepted, the source superseded_by it."""
    sp = docs / src
    r = json.loads(sp.read_text(encoding="utf-8"))
    n = copy.deepcopy(r)
    n["rev"] = dst_rev
    n["accepted"] = True
    n.pop("superseded_by", None)
    n.pop("deps", None)
    if deps is not None:
        n["deps"] = deps
    (docs / f"{r['sketch']}_checks_r{dst_rev}.json").write_text(json.dumps(n), encoding="utf-8")
    r["superseded_by"] = dst_rev
    sp.write_text(json.dumps(r), encoding="utf-8")


def deps_b7_no_certifier():
    """DEPS B7 (P0S FIX 3): S1 r8 set unaccepted in the temporary tree: no accepted, unsuperseded S1 record for the S3
    certifier and for the S2 r9 exemption's certifier."""
    docs, wip = _deps_tree()
    p = docs / "s1_checks_r8.json"
    r = json.loads(p.read_text(encoding="utf-8"))
    r["accepted"] = False
    p.write_text(json.dumps(r), encoding="utf-8")
    return _deps_res(docs, wip, "S1 r8 unaccepted")


def deps_b8_spec_absent():
    """DEPS B8 (P0S FIX 3): s3_spec.yaml renamed in the temporary docs/."""
    docs, wip = _deps_tree()
    (docs / "s3_spec.yaml").rename(docs / "s3_spec_renamed.yaml")
    return _deps_res(docs, wip, "S3 spec absent")


def deps_z3_s3_exempt():
    """DEPS Z3 (P0S FIX 4 a; orchestrator ruling at P0f): the accepted S3 r7 record as committed (no deps) reads exempt
    through its DEPS_EXEMPT entry, whose deps match the tree: clean."""
    docs, wip = _deps_tree(s3_deps=False)
    return _deps_res(docs, wip, "S3 r7 exempt with deps")


def deps_b9_s3_r8():
    """DEPS B9 (P0S FIX 4 c): S3 r8 accepted over r7 without deps: the exemption ends with r7."""
    docs, wip = _deps_tree(s3_deps=False)
    _accept_copy(docs, "s3_checks_r7.json", 8)
    return _deps_res(docs, wip, "S3 r8 without deps")


def deps_b10_exempt_superseded():
    """DEPS B10 (Loftsman P0L FIX 1, route 1): S3 r7 exempt (no deps of its own) and S1 r9 accepted over r8 with deps: the
    exemption's deps name s1_checks_r8.json, so S3 r7 reads certifier superseded (and S2 r9 likewise). A name-only
    exemption reads clean here (dry run A1)."""
    docs, wip = _deps_tree(s3_deps=False)
    _s1_r9(docs)
    return _deps_res(docs, wip, "S1 r9 over r8, S3 r7 exempt")


def deps_b11_spec_read():
    """DEPS B11 (Loftsman P0L FIX 2, route 2): nut_a place theta jackscrew.angle[1] written [0] in both s1_spec.yaml and
    s2_spec.yaml (X1 unchanged, every key value unchanged): S3 r7 reads the specs sym_lint reads (spec_read); S1 r8 and
    S2 r9 read their own spec."""
    docs, wip = _deps_tree(s3_deps=False)
    for n in ("s1_spec.yaml", "s2_spec.yaml"):
        p = docs / n
        t = p.read_text(encoding="utf-8")
        i = t.index("id: nut_a")
        j = t.index("jackscrew.angle[1]", i)
        p.write_text(t[:j] + "jackscrew.angle[0]" + t[j + len("jackscrew.angle[1]"):], encoding="utf-8", newline="")
    return _deps_res(docs, wip, "nut_a theta edited in s1 and s2 specs")


def deps_b12_cert_file():
    """DEPS B12 (Loftsman P0L FIX 3, route 3): s1_mass_report_r8.json edited (one field): the S2 r9 record read it through
    its S1 certifier."""
    docs, wip = _deps_tree()
    p = docs / "s1_mass_report_r8.json"
    r = json.loads(p.read_text(encoding="utf-8"))
    r["edited"] = "one field"
    p.write_text(json.dumps(r), encoding="utf-8")
    return _deps_res(docs, wip, "S1 mass report edited")


def deps_b13_name_only():
    """DEPS B13 (premise of the exemption, Loftsman P0L FIX 1): the S3 r7 exemption entry written by name alone (no deps)."""
    docs, wip = _deps_tree(s3_deps=False)
    saved = cs.DEPS_EXEMPT
    cs.DEPS_EXEMPT = dict(saved)
    cs.DEPS_EXEMPT["s3_checks_r7.json"] = {"note": "by name alone"} if isinstance(saved.get("s3_checks_r7.json", {}), dict) else "by name alone"
    try:
        return _deps_res(docs, wip, "S3 r7 exempt by name alone")
    finally:
        cs.DEPS_EXEMPT = saved


def deps_run_s2():
    """DEPS Z4 (Loftsman P0L FIX 3): a live s2 run (records from docs/sketches/) writes deps with certifier s1
    s1_checks_r8.json and its file s1_mass_report_r8.json, each with its SHA-256; record to a temporary wip/."""
    t = _tmp()
    cs.main(["s2", "--rev", "9", "--wip-dir", str(t)])
    d = json.loads((t / "s2_checks_r9.json").read_text(encoding="utf-8")).get("deps") or {}
    got = [(c.get("sketch"), c.get("path"), c.get("sha256"), tuple((f.get("path"), f.get("sha256")) for f in c.get("files") or []))
           for c in d.get("certifiers") or []]
    want = [("s1", "s1_checks_r8.json", cs._sha(SK / "s1_checks_r8.json"), (("s1_mass_report_r8.json", cs._sha(SK / "s1_mass_report_r8.json")),))]
    iss = [] if got == want else [f"deps certifiers {got} against {want}"]
    return _res("DEPS", bool(iss), sc._summ(iss) if iss else "s2 run records certifier s1 r8 with its mass report", len(iss))


# ======================================================================== P0f: M1C (Software Engineer FIX 5)

def m1c_b5_spelling():
    """M1C B5 (P0S FIX 5): key paths inside a temporary root (passed as root=) written in extended-length form and in
    admin-share UNC form, each with its own empty out folder: both refused before any write."""
    t = _tmp()
    root = (t / "root").resolve()
    (root / "sub").mkdir(parents=True)
    ab = str(root)
    forms = ["\\\\?\\" + ab + "\\sub\\key.json", "\\\\localhost\\" + ab[0] + "$" + ab[2:] + "\\sub\\key.json"]
    rs = [_refusal(t / f"out{i}", k, f"form {i}", root=root) for i, k in enumerate(forms)]
    for i in range(len(forms)):
        q = root / "sub" / "key.json"
        if q.exists():
            q.unlink()
    n = sum(r["n_issues"] for r in rs)
    return _res("M1C", n > 0, " || ".join(r["reason"] for r in rs), n)


# ======================================================================== P0f: K4 rule (l) (Designer FIX L1 to L4, Topologist TP1.4-1,
# Software Engineer FIX 6, 7)

def _l(c, aid="main", row=None, fam=None, pose=None):
    """Rule (l) issues of Axes aid of a context, filtered by labelled row, family and pose."""
    sub = sc.axes_context(c, aid) if sc.needs_split(c) else c
    out = []
    for m in sc.collinear_issues(sub):
        if row and f"/{row}:" not in m:
            continue
        if fam and _fam_of(m) != fam:
            continue
        if pose and not m.startswith(f"{pose}/"):
            continue
        out.append(m)
    return out


def _lres(iss, what):
    return _res("K4", bool(iss), sc._summ(iss) if iss else f"{what}: 0 rule (l) firings", len(iss))


def _beside_axes(c, aid, fid=None, pose=None):
    fig = c.figs[pose] if pose else next(iter(c.figs.values()))
    ax = next(a for a in sc.real_figure(fig).axes if getattr(a, "sketch_axes", None) == aid) if sc.needs_split(c) else fig.axes[0]
    f, p0, p1 = _leader(ax, fid)
    return ax, f, p0, p1


def k4_l_paper_side():
    """K4 B (Designer P0D FIX L1, paper thresholds): live S1 at pose start: the drill_tube leader 1.0 px off gridline z 1350
    over 278 data mm (0.53 px per data mm; D 4.50 data mm on S1) fires. Read with the 1.0 data mm of step 0 it is clean."""
    c = _live("s1")
    return _lres(_l(c, row="drill_tube", pose="start"), "S1 start drill_tube")


def k4_l_aspect():
    """K4 B (premise of FIX L1, equal aspect): live S3 with the section Axes set to aspect 2: px per data mm differs in x
    and y, reported and not judged."""
    c = _live("s3")
    ax = _ax_of(c, "section")
    ax.set_aspect(2.0)
    ax.apply_aspect()
    return _lres([m for m in _l(c, "section") if "rule (l) premise" in m], "S3 section aspect 2")


def _plant_line(c, aid, gid, kind, pose=None, off=0.5):
    """One line of family kind beside the longest leader of Axes aid, 0.5 data mm off over 60 percent of it: kind line
    (Line2D), collection (LineCollection), outline_clipped (unfilled dashed Patch inside a clip path that contains it),
    outline (unfilled solid Patch), leader (a label annotation, gid label:<gid>). Returns (context, leader row)."""
    from matplotlib.collections import LineCollection
    ax, f, p0, p1 = _beside_axes(c, aid, pose=pose)
    a, b, quad = _beside(p0, p1, off=off)
    if kind == "line":
        sc.draw(gid, Line2D([a[0], b[0]], [a[1], b[1]], lw=0.6, color="0.3"), ax)
    elif kind == "collection":
        sc.draw(gid, LineCollection([[a, b]], linewidths=0.6, colors="0.3"), ax)
    elif kind in ("outline", "outline_clipped"):
        poly = sc.draw(gid, Polygon(quad, closed=True, fill=False, edgecolor="0.3", lw=0.6,
                                    linestyle="--" if kind == "outline_clipped" else "-", zorder=1), ax)
        if kind == "outline_clipped":
            cx, cy = sum(q[0] for q in quad) / 4, sum(q[1] for q in quad) / 4
            big = [(cx + 2 * (q[0] - cx), cy + 2 * (q[1] - cy)) for q in quad]
            poly.set_clip_path(Polygon(big, closed=True, transform=ax.transData))
    elif kind == "leader":
        t = ax.annotate("", xy=b, xytext=a, arrowprops={"arrowstyle": "-", "lw": 0.6})
        t.set_gid(f"label:{gid}")
    return c, f


def k4_l_drawn_side():
    """K4 B (FIX L2 / TP1.4-1, drawn line, side): live S1 at pose load; a Line2D tagged pinion_axis_a (a non-reference row)
    beside the longest leader."""
    c = _live("s1")
    c.figs = {"load": c.figs["load"]}
    c, f = _plant_line(c, "main", "pinion_axis_a", "line")
    return _lres(_l(c, fam="drawn line", row=f), "S1 drawn line")


def k4_l_drawn_plan():
    """K4 B (FIX L2 / TP1.4-1, drawn line, plan, Collection branch): live S2; a LineCollection tagged collet_axis beside
    the longest leader."""
    c = _live("s2")
    c, f = _plant_line(c, "main", "collet_axis", "collection")
    return _lres(_l(c, fam="drawn line", row=f), "S2 drawn line")


def k4_l_drawn_section():
    """K4 B (FIX L2 / TP1.4-1, drawn line, section): live S3; a Line2D tagged pinion_axis_c beside the longest section leader."""
    c = _live("s3")
    c, f = _plant_line(c, "section", "pinion_axis_c", "line")
    return _lres(_l(c, "section", fam="drawn line", row=f), "S3 section drawn line")


def k4_l_outline_plan():
    """K4 B (TP1.4-1, stroked outline, plan): live S2; an unfilled dashed ring Patch inside a clip path that contains it
    (a renderer hidden piece) with one edge beside the longest leader."""
    c = _live("s2")
    c, f = _plant_line(c, "main", "ring", "outline_clipped")
    return _lres(_l(c, fam="part edge", row=f), "S2 dashed clipped outline")


def k4_l_outline_side():
    """K4 B (TP1.4-1, stroked outline, side): live S1 at pose load; an unfilled solid base_frame Patch with one edge beside
    the longest leader."""
    c = _live("s1")
    c.figs = {"load": c.figs["load"]}
    c, f = _plant_line(c, "main", "base_frame", "outline")
    return _lres(_l(c, fam="part edge", row=f), "S1 unfilled outline")


def k4_l_leader_side():
    """K4 B (FIX L4, leader family, side): live S1 at pose load; a second label leader beside the longest leader."""
    c = _live("s1")
    c.figs = {"load": c.figs["load"]}
    c, f = _plant_line(c, "main", "plant_leader", "leader")
    return _lres(_l(c, fam="leader"), "S1 leaders")


def k4_l_leader_plan():
    """K4 B (FIX L4, leader family, plan): live S2; a second label leader beside the longest leader."""
    c = _live("s2")
    c, f = _plant_line(c, "main", "plant_leader", "leader")
    return _lres(_l(c, fam="leader"), "S2 leaders")


def k4_l_leader_section():
    """K4 B (FIX L4, leader family, section): live S3; a second label leader beside the longest section leader."""
    c = _live("s3")
    c, f = _plant_line(c, "section", "plant_leader", "leader")
    return _lres(_l(c, "section", fam="leader"), "S3 section leaders")


def k4_l_clip_fires():
    """K4 B (P0S FIX 6, clip-region firing path): live S3 section; K4-Z11's quad with the complementary clip (the leader's
    side of the quad kept), so the edge along the leader is drawn."""
    c = _live("s3")
    ax = _ax_of(c, "section")
    f, p0, p1 = _leader(ax)
    a, b, quad = _beside(p0, p1)
    poly = sc.draw("motor23_c", Polygon(quad, closed=True, facecolor="0.85", edgecolor="0.3", zorder=1), ax)
    near = [quad[0], quad[1], ((quad[1][0] + quad[2][0]) / 2, (quad[1][1] + quad[2][1]) / 2), ((quad[0][0] + quad[3][0]) / 2, (quad[0][1] + quad[3][1]) / 2)]
    near = [(p[0] - 0.2 * (quad[3][0] - quad[0][0]), p[1] - 0.2 * (quad[3][1] - quad[0][1])) if k < 2 else p for k, p in enumerate(near)]
    poly.set_clip_path(Polygon(near, closed=True, transform=ax.transData))
    return _lres(_l(c, "section"), "S3 section clipped quad, leader side kept")


def k4_l_own_row():
    """K4 Z (P0S FIX 7, own-row relief; Designer NOTE N-l3): live S3 section; a filled quad and a Line2D, each tagged with
    the longest leader's own row, one edge along that leader: 0 firings."""
    c = _live("s3")
    ax = _ax_of(c, "section")
    f, p0, p1 = _leader(ax)
    a, b, quad = _beside(p0, p1)
    sc.draw(f, Polygon(quad, closed=True, facecolor="0.85", edgecolor="0.3", zorder=1), ax)
    sc.draw(f, Line2D([a[0], b[0]], [a[1], b[1]], lw=0.6), ax)
    return _lres(_l(c, "section"), f"S3 section, own-row plants on {f}")


# FIX L3 relief: Z on the live rows it relieves; a B per term, each red by deleting that term.

def k4_l_relief_live():
    """K4 Z (Designer P0D FIX L3): live S1 height_target (every pose; line z 2000 on gridline z 2000) and live S2
    slot_line_c (line y 259, 1.00 data mm under gridline y 260): each line row's leader continues its own line: 0 firings."""
    iss = _l(_live("s1"), row="height_target") + _l(_live("s2"), row="slot_line_c")
    return _lres(iss, "S1 height_target, S2 slot_line_c")


def _slot(c):
    ax = _ax_of(c, "main") if sc.needs_split(c) else next(iter(c.figs.values())).axes[0]
    t = next(x for x in ax.texts if x.get_gid() == "label:slot_line_c")
    ln = next(a for a in sc.tagged(ax)["slot_line_c"] if isinstance(a, Line2D))
    return ax, t, ln


def k4_l_relief_area():
    """K4 B (FIX L3 term 1, line rows only): live S2 with slot_line_c declared kind area in the context's spec copy, its
    drawing unchanged: the gridline y 260 firing returns."""
    c = _live("s2")
    c.spec = copy.deepcopy(c.spec)
    next(r for r in c.spec["features"] if r["id"] == "slot_line_c")["kind"] = "area"
    return _lres(_l(c, row="slot_line_c"), "S2 slot_line_c as an area row")


def k4_l_relief_mid():
    """K4 B (FIX L3 term 2, anchor at an end of the own ink): live S2; the slot_line_c anchor moved to the middle of its
    line, text unchanged."""
    c = _live("s2")
    ax, t, ln = _slot(c)
    xs, ys = list(ln.get_xdata()), list(ln.get_ydata())
    t.xy = ((float(xs[0]) + float(xs[-1])) / 2, (float(ys[0]) + float(ys[-1])) / 2)
    return _lres(_l(c, row="slot_line_c"), "S2 slot_line_c anchored mid-line")


def k4_l_relief_back():
    """K4 B (FIX L3 term 3, the leader leaves the end away from the ink): live S2; the slot_line_c text moved past the far
    end of its line, so the leader runs back over its own ink to the anchor."""
    c = _live("s2")
    ax, t, ln = _slot(c)
    xs, ys = [float(v) for v in ln.get_xdata()], [float(v) for v in ln.get_ydata()]
    ax_, ay_ = float(t.xy[0]), float(t.xy[1])
    far = (xs[0], ys[0]) if math.hypot(xs[0] - ax_, ys[0] - ay_) > math.hypot(xs[-1] - ax_, ys[-1] - ay_) else (xs[-1], ys[-1])
    t.xyann = (far[0] + 0.2 * (far[0] - ax_), far[1] + 0.2 * (far[1] - ay_))
    return _lres(_l(c, row="slot_line_c"), "S2 slot_line_c leader back over its ink")


def k4_l_relief_slant():
    """K4 B (FIX L3 term 4, the own ink runs along the line judged): live S2; slot_line_c redrawn slanted from its anchor
    (the far end moved 100 mm down across), anchor and text unchanged: its ink no longer runs along gridline y 260."""
    c = _live("s2")
    ax, t, ln = _slot(c)
    xs, ys = [float(v) for v in ln.get_xdata()], [float(v) for v in ln.get_ydata()]
    ax_, ay_ = float(t.xy[0]), float(t.xy[1])
    if math.hypot(xs[0] - ax_, ys[0] - ay_) < math.hypot(xs[-1] - ax_, ys[-1] - ay_):
        xs[-1], ys[-1] = xs[-1], ys[-1] - 100.0
    else:
        xs[0], ys[0] = xs[0], ys[0] - 100.0
    ln.set_data(xs, ys)
    return _lres(_l(c, row="slot_line_c"), "S2 slot_line_c slanted")


# ======================================================================== P0f: rule (j) (Designer FIX J1; Software Engineer FIX 9)

def _stall(new):
    def sm(sp):
        for c in sp["load_cases"]["cases"]:
            if c["id"] == "stall_up":
                c["per_screw"] = new
    return _builders()._script_ctx("s3", spec_mut=sm)


def stall_no_mu():
    """K4 B (Designer P0D FIX J1; P0S FIX 9, no mu list): stall_up per_screw written '343.18 / 282.21' (mu list removed)."""
    return _stall("343.18 / 282.21")


def stall_count():
    """K4 B (P0S FIX 9, value and mu counts differ): stall_up per_screw '343.18 / 282.21 / 250.00 (mu 0.15 / 0.20)'."""
    return _stall("343.18 / 282.21 / 250.00 (mu 0.15 / 0.20)")


def stall_mu_unknown():
    """K4 B (P0S FIX 9, a mu that is not a thread_mu value): stall_up per_screw '343.18 / 282.21 (mu 0.15 / 0.25)'."""
    return _stall("343.18 / 282.21 (mu 0.15 / 0.25)")


def stall_mu_bare():
    """K4 B (rule (j), malformed mu list): stall_up per_screw '343.18 / 282.21 mu 0.15 / 0.20' (no parentheses)."""
    return _stall("343.18 / 282.21 mu 0.15 / 0.20")


# ======================================================================== P0f: DR4-2 sub-conditions (Software Engineer FIX 8)

def term_style_wide():
    """K8 B (P0S FIX 8, arrowstyle tuple): one span_lt terminator drawn '-|>,head_width=0.5' at mutation_scale 14."""
    return _span_arrow(arrowstyle="-|>,head_width=0.5")


def term_angle3():
    """K8 B (P0S FIX 8, connection class): one span_lt terminator drawn with connectionstyle angle3 (both ends on the line)."""
    return _span_arrow(connectionstyle="angle3")
