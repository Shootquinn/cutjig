"""Harness controls for 1.2 step 0 (gameplan Design Notes 25 H1, H5). Each builder returns a check result
{id, result, reason, n_issues}: result "pass" = clean, "fail" = fires (check_sketch.run_control takes it as is).

H1 controls run check_sketch.accept / stale_records / stale_diffs / write_record on temporary copies (a docs/ and a
wip/ directory under tempfile), never on the live records. The record template is docs/sketches/s1_checks_r4.json,
read only, with its accepted fields removed and its keys_read values set from the live params and overlay, so the
controls do not drift when the overlay changes. H5 controls read the live s1_spec.yaml through check_stack.
"""
import copy
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
SK = HERE.parent
if str(SK) not in sys.path:
    sys.path.insert(0, str(SK))
import check_sketch as cs  # noqa: E402
import check_stack  # noqa: E402
from sketch_loader import Params, load_spec  # noqa: E402

NOTE = "Design Notes 24"
PNG = "s1_pose_load_r4.png"


def _res(cid, fired, reason, n_issues):
    return {"id": cid, "result": "fail" if fired else "pass", "reason": reason, "n_issues": n_issues}


def _template(rev=4):
    rec = json.loads((SK / "s1_checks_r4.json").read_text(encoding="utf-8"))
    for k in ("accepted_note", "accepted_at", "superseded_by"):
        rec.pop(k, None)
    rec["accepted"], rec["rev"] = False, rev
    P = Params()
    for k, v in rec["keys_read"].items():
        if P.has(k):
            v["value"] = P.get(k)
    return rec


def _write(d, rec):
    p = Path(d) / cs.record_name(rec["sketch"], rec["rev"])
    p.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    return p


def _png(path, flip=False):
    import matplotlib.image as mpimg
    a = np.zeros((8, 8, 3))
    a[2:6, 2:6] = 1.0
    if flip:
        a[0, 0] = [1.0, 0.0, 0.0]
    mpimg.imsave(str(path), a)


def _dirs(tmp):
    docs, wip = Path(tmp) / "docs", Path(tmp) / "wip"
    docs.mkdir()
    wip.mkdir()
    return docs, wip


def _quiet(_m):
    pass


def h1_z_accept():
    """Z: accept a passing record from wip/ (record, summary, PNG byte-equal to the docs copy): exit 0, flag and note in
    the docs record, PNG kept; --stale reads 1 record, 0 differences."""
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        _write(wip, _template())
        (wip / "s1_summary_r4.md").write_text("summary\n", encoding="utf-8")
        _png(wip / PNG)
        _png(docs / PNG)
        rc, msgs = cs.accept("s1", 4, NOTE, docs, wip, out=_quiet)
        issues = [] if rc == 0 else [f"accept exit {rc}: {' / '.join(msgs)}"]
        rec = json.loads((docs / "s1_checks_r4.json").read_text(encoding="utf-8")) if (docs / "s1_checks_r4.json").is_file() else {}
        if not (rec.get("accepted") is True and rec.get("accepted_note") == NOTE and rec.get("accepted_at")):
            issues.append(f"docs record flag {rec.get('accepted')!r}, note {rec.get('accepted_note')!r}")
        recs = cs.stale_records(docs, wip)
        diffs = cs.stale_diffs(Params(), recs)
        if len(recs) != 1 or diffs:
            issues.append(f"--stale {len(recs)} record(s), {len(diffs)} difference(s)")
        return _res("H1", bool(issues), "; ".join(issues) or f"accepted; flag, note set; --stale {len(recs)} record, 0 differences; {len(msgs)} message(s)", len(issues))


def h1_z_rerun():
    """Z: a re-run of an accepted revision (check_sketch.write_record, the run path) writes an unflagged record to wip/;
    the docs record keeps its flag and --stale still reads it."""
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        _write(wip, _template())
        cs.accept("s1", 4, NOTE, docs, wip, out=_quiet)
        cs.write_record(_template(), wip)
        issues = []
        d = json.loads((docs / "s1_checks_r4.json").read_text(encoding="utf-8")) if (docs / "s1_checks_r4.json").is_file() else {}
        w = json.loads((wip / "s1_checks_r4.json").read_text(encoding="utf-8"))
        if d.get("accepted") is not True:
            issues.append("docs record lost its flag after the re-run")
        if w.get("accepted"):
            issues.append("re-run record in wip/ carries a flag")
        recs = cs.stale_records(docs, wip)
        if [p.parent.name for p, _ in recs] != ["docs"]:
            issues.append(f"--stale reads {[str(p) for p, _ in recs]}")
        return _res("H1", bool(issues), "; ".join(issues) or "docs record keeps accepted after a re-run to wip/; --stale reads it", len(issues))


def h1_b_failing_check():
    """B: a record with one failing check (S1-4) is refused; nothing is written to docs/."""
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        rec = _template()
        next(c for c in rec["checks"] if c["id"] == "S1-4")["result"] = "fail"
        _write(wip, rec)
        rc, msgs = cs.accept("s1", 4, NOTE, docs, wip, out=_quiet)
        written = sorted(p.name for p in docs.iterdir())
        fired = rc != 0 and not written
        return _res("H1", fired, " / ".join(msgs) + (f"; docs/ holds {written}" if written else ""), 1 if fired else 0)


def h1_b_empty_note():
    """B: an empty note is refused."""
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        _write(wip, _template())
        rc, msgs = cs.accept("s1", 4, "  ", docs, wip, out=_quiet)
        written = sorted(p.name for p in docs.iterdir())
        fired = rc != 0 and not written
        return _res("H1", fired, " / ".join(msgs), 1 if fired else 0)


def h1_b_stale_key():
    """B: --stale fires on a key change against a flagged record (jackscrew.anchor_z 265 -> 266 in a temporary overlay)."""
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        _write(wip, _template())
        cs.accept("s1", 4, NOTE, docs, wip, out=_quiet)
        P0 = Params()
        ov = yaml.safe_load(P0.overlay_path.read_text(encoding="utf-8"))
        ov["jackscrew"]["anchor_z"]["value"] = ov["jackscrew"]["anchor_z"]["value"] + 1
        tmp_ov = Path(t) / "overlay.yaml"
        tmp_ov.write_text(yaml.safe_dump(ov, sort_keys=False), encoding="utf-8")
        diffs = cs.stale_diffs(Params(overlay_path=tmp_ov), cs.stale_records(docs, wip))
        return _res("H1", bool(diffs), " || ".join(diffs) or "no difference", len(diffs))


def h1_b_superseded():
    """B: accepting r5 supersedes r4. r4 (accepted) records a stale jackscrew.anchor_z, r5 a stale ring.thickness.
    --stale must fire on r5 only: 1 difference naming s1_checks_r5.json. Reading the superseded r4 gives 2."""
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        r4 = _template(4)
        r4.update({"accepted": True, "accepted_note": NOTE, "accepted_at": "2026-11-25T00:00:00"})
        r4["keys_read"]["jackscrew.anchor_z"]["value"] = 999
        _write(docs, r4)
        r5 = _template(5)
        r5["keys_read"]["ring.thickness"]["value"] = 999
        _write(wip, r5)
        rc, msgs = cs.accept("s1", 5, "Design Notes 13 S1-r5 (control)", docs, wip, out=_quiet)
        r4d = json.loads((docs / "s1_checks_r4.json").read_text(encoding="utf-8"))
        diffs = cs.stale_diffs(Params(), cs.stale_records(docs, wip))
        extra = [] if (rc == 0 and r4d.get("superseded_by") == 5 and r4d.get("accepted") is True) else \
            [f"accept r5 exit {rc}, r4 superseded_by {r4d.get('superseded_by')!r}, r4 accepted {r4d.get('accepted')!r}"]
        return _res("H1", bool(diffs or extra), " || ".join(extra + diffs) or "no difference", len(diffs) + len(extra))


def h1_b_png_pixels():
    """B: a wip/ PNG of the same name as an accepted docs/ PNG, one pixel different, blocks the accept; the record is
    not flagged and docs/ is unchanged."""
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        _write(wip, _template())
        _png(wip / PNG, flip=True)
        _png(docs / PNG)
        rc, msgs = cs.accept("s1", 4, NOTE, docs, wip, out=_quiet)
        flagged = json.loads((wip / "s1_checks_r4.json").read_text(encoding="utf-8")).get("accepted")
        written = sorted(p.name for p in docs.iterdir())
        fired = rc != 0 and not flagged and written == [PNG]
        return _res("H1", fired, " / ".join(msgs) + (f"; flagged {flagged}, docs/ {written}" if not fired else ""), 1 if fired else 0)


def _harness_wip(wip, mismatch=0):
    """wip/ controls results (3 rows, `mismatch` of them match "no") and a baseline record, as --controls and --baseline
    leave them."""
    rows = [{"id": f"K0-B{i}", "match": "no" if i < mismatch else "yes"} for i in range(3)]
    ctrl = wip / cs.CONTROLS_RESULTS
    ctrl.parent.mkdir(parents=True, exist_ok=True)
    ctrl.write_text(json.dumps({"controls": rows}, indent=1), encoding="utf-8")
    (wip / cs.BASELINE).write_text(json.dumps({"s1": {"run2": "fixture"}}, indent=1), encoding="utf-8")
    return ctrl, wip / cs.BASELINE


def h1_z_harness_copy():
    """Z (SW 1.2 (c) FIX 4): H1-Z1 plus a matched wip/ controls results file and baseline record: accept exit 0 and both
    land in docs/ byte-equal."""
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        _write(wip, _template())
        (wip / "s1_summary_r4.md").write_text("summary\n", encoding="utf-8")
        _png(wip / PNG)
        _png(docs / PNG)
        srcs = _harness_wip(wip)
        rc, msgs = cs.accept("s1", 4, NOTE, docs, wip, out=_quiet)
        issues = [] if rc == 0 else [f"accept exit {rc}: {' / '.join(msgs)}"]
        for p in srcs:
            dst = docs / p.relative_to(wip)
            if not dst.is_file() or cs._sha(dst) != cs._sha(p):
                issues.append(f"{p.relative_to(wip).as_posix()} not byte-equal in docs/")
        return _res("H1", bool(issues), "; ".join(issues) or "accepted; controls results and baseline copied up byte-equal", len(issues))


def h1_b_controls_mismatch():
    """B (SW 1.2 (c) FIX 4): the same with one wip/ control row match "no": accept refused, record not flagged, docs/
    unchanged."""
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        _write(wip, _template())
        _png(wip / PNG)
        _png(docs / PNG)
        _harness_wip(wip, mismatch=1)
        rc, msgs = cs.accept("s1", 4, NOTE, docs, wip, out=_quiet)
        flagged = json.loads((wip / "s1_checks_r4.json").read_text(encoding="utf-8")).get("accepted")
        written = sorted(p.name for p in docs.iterdir())
        fired = rc != 0 and not flagged and written == [PNG]
        return _res("H1", fired, " / ".join(msgs) + (f"; flagged {flagged}, docs/ {written}" if not fired else ""), 1 if fired else 0)


# ---------------------------------------------------------------- H5 (1 m start-above-core term, symbol c)

def _s1_stack(spec_mut=None):
    P = Params()
    spec = load_spec(SK / "s1_spec.yaml")
    if spec_mut:
        spec_mut(spec)
    return P, spec, check_stack.evaluate_spec(P, spec)


def h5_z_live():
    """Z: live S1. 1 m class reported as expressions in c (stop 392.50 + c, start 1042.50 + c, start_minus_core_top c);
    0.5 and 0.75 m starts 834.84, park 959.84 (1209.84 with 1 m), stroke 775 (1025), L_min 885 (1135) as numbers."""
    P, spec, stack = _s1_stack()
    rep = check_stack.reported(P, spec, stack)
    o = rep["q9_options"]["plus 1 m"]
    want = {"stop 1 m": (o["stops_z_A"].get("core.length_optional"), "392.50 + c for c >= 0"),
            "start 1 m": (o["starts_z_A"].get("core.length_optional"), "1042.50 + c for c >= 0"),
            "start_minus_core_top 1 m": (o["start_minus_core_top"].get("core.length_optional"), "c for c >= 0"),
            "start 0.75 m": (round(o["starts_z_A"]["core.length_install"], 2), 834.84),
            "park 1 m": (round(o["park_tip_z_A"], 2), 1209.84), "stroke 1 m": (round(o["lift_stroke"], 2), 1025.0),
            "L_min 1 m": (round(o["L"]["L_min"], 2), 1135.0),
            "park drawn": (round(stack["global_z_A"]["park_tip"], 2), 959.84),
            "stroke drawn": (round(stack["global_z_A"]["lift_stroke"], 2), 775.0)}
    bad = [f"{k} {got!r}, want {w!r}" for k, (got, w) in want.items() if got != w]
    return _res("H5", bool(bad), "; ".join(bad) or "1 m terms in c; 0.5/0.75 m and drawn values unchanged", len(bad))


def h5_b_drawn_depends_on_c():
    """B: the 1 m class made a drawn class (q9_length_keys + core.length_optional): the drawn start max reads
    1042.50 + c, which has no value, so check_stack refuses ("depends on symbol c")."""
    def mut(spec):
        spec["q9_length_keys"] = list(spec["q9_length_keys"]) + ["core.length_optional"]
    try:
        _s1_stack(mut)
    except ValueError as e:
        return _res("H5", True, str(e), 1)
    return _res("H5", False, "check_stack evaluated a drawn value that depends on c", 0)


# ---------------------------------------------------------------- 1.3 step 0 (research/sean/cr_scratch/step1.3_engineer_step0.md)
# R3 (O10, Step 1.2 gate D3): check RPT on spec field reported_items, and --accept through RPT. R1 (O9): the parallel
# controls runner on a temporary two-row manifest, run as its own process with --jobs 2.

RPT_SPEC = {"reported_items": [
    {"id": "L_min", "text": "screw length L_min per Q9 option", "source": "gameplan detail 1.3 Reported", "needs_drawing": False},
    {"id": "F_stall", "text": "stall thrust, three lift motors", "source": "gameplan detail 1.3 Reported", "needs_drawing": True}]}
RPT_VALUES = {"L_min": {"value": "885.00 / 885.00 / 1135.00", "basis": "S1 screw_length expression", "tag": "DERIVED"},
              "F_stall": {"value": 636.17, "basis": "3 x 2 pi T_hold eta / lead", "tag": "DERIVED"}}


def rpt_z():
    """RPT Z: fixture spec with two items, both supplied."""
    return cs.rpt_check(RPT_SPEC, RPT_VALUES, "s3_checks_r1.json", 1)


def rpt_b1():
    """RPT B: F_stall declared, no value supplied (rev 1: cause content)."""
    return cs.rpt_check(RPT_SPEC, {"L_min": RPT_VALUES["L_min"]}, "s3_checks_r1.json", 1)


def rpt_b2():
    """RPT B: a record that is not one accepted before the rule, spec with no reported_items."""
    return cs.rpt_check({}, {}, "s3_checks_r1.json", 1)


def _rpt_record(rpt_row):
    rec = _template()
    rec["reported_items"] = RPT_SPEC["reported_items"]
    rec["checks"] = [c for c in rec["checks"] if c["id"] != "RPT"] + ([rpt_row] if rpt_row else [])
    return rec


def _accept_refused(rec):
    with tempfile.TemporaryDirectory() as t:
        docs, wip = _dirs(t)
        _write(wip, rec)
        rc, msgs = cs.accept("s1", 4, NOTE, docs, wip, out=_quiet)
        flagged = json.loads((wip / "s1_checks_r4.json").read_text(encoding="utf-8")).get("accepted")
        written = sorted(p.name for p in docs.iterdir())
        fired = rc != 0 and not flagged and not written
        return _res("H1", fired, " / ".join(msgs) + (f"; flagged {flagged}, docs/ {written}" if not fired else ""), 1 if fired else 0)


def h1_b_rpt_fail():
    """B (R3): a record declaring reported_items with RPT fail (one item without a value): accept refused, nothing written."""
    return _accept_refused(_rpt_record(rpt_b1()))


def h1_b_rpt_absent():
    """B (R3): a record declaring reported_items with no RPT row: accept refused, nothing written."""
    return _accept_refused(_rpt_record(None))


def _runner(wrong):
    """Two rows of the live manifest (K1-Z, K2-Z) in a temporary manifest, the second with expected fires when wrong;
    check_sketch.py --controls --manifest <tmp> --jobs 2 as its own process."""
    import subprocess
    man = {e["id"]: e for e in yaml.safe_load((SK / "fixtures" / "manifest.yaml").read_text(encoding="utf-8"))["controls"]}
    rows = [dict(man["K1-Z"]), dict(man["K2-Z"])]
    if wrong:
        rows[1].update(expected="fires", reason=["planted wrong expectation"])
    with tempfile.TemporaryDirectory() as t:
        mp = Path(t) / "manifest.yaml"
        mp.write_text(yaml.safe_dump({"controls": rows}, sort_keys=False), encoding="utf-8")
        pr = subprocess.run([sys.executable, str(SK / "check_sketch.py"), "--controls", "--manifest", str(mp), "--jobs", "2"],
                            capture_output=True, text=True, timeout=600)
        res = Path(t) / "controls_results.json"
        data = json.loads(res.read_text(encoding="utf-8")) if res.is_file() else {}
    got = [(r["id"], r["match"]) for r in data.get("controls", [])]
    nos = [r for r in data.get("controls", []) if r["match"] != "yes"]
    lines = [ln for ln in pr.stdout.splitlines() if "match NO" in ln]
    return pr.returncode, got, nos, lines, data.get("summary", {}), (pr.stderr or "")[-300:]


def run_z():
    """R1 Z: the two-row manifest with correct expectations under --jobs 2: exit 0, both rows match yes, in manifest
    order, jobs 2 recorded."""
    rc, got, nos, lines, summ, err = _runner(False)
    issues = []
    if rc != 0:
        issues.append(f"exit {rc} {err}")
    if got != [("K1-Z", "yes"), ("K2-Z", "yes")]:
        issues.append(f"rows {got}")
    if summ.get("jobs") != 2:
        issues.append(f"jobs {summ.get('jobs')}")
    return _res("RUN", bool(issues), "; ".join(issues) or "--jobs 2: exit 0, K1-Z and K2-Z match yes in manifest order", len(issues))


def run_b():
    """R1 B: the same manifest with K2-Z expecting fires: under --jobs 2 the runner prints match NO for K2-Z and exits 1."""
    rc, got, nos, lines, summ, err = _runner(True)
    fired = rc == 1 and [r["id"] for r in nos] == ["K2-Z"] and len(lines) == 1 and "K2-Z" in lines[0] and summ.get("jobs") == 2
    reason = f"--jobs {summ.get('jobs')}: exit {rc}; mismatched {[r['id'] for r in nos]}; printed {lines}" + (f"; stderr {err}" if not fired else "")
    return _res("RUN", fired, reason, 1 if fired else 0)
