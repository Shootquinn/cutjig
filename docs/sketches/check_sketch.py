"""Run the sketch checks (contributor gameplan (sean) detail 1.0, line 124).

  check_sketch.py sN [--rev k]     K1 to K9 plus checks_sN.py, X1 and RPT on the sketch (rev 0: stubs/sN_stub.py);
                                   writes wip/sN_checks_r<k>.json and wip/sN_summary_r<k>.md (with a Reported items table
                                   when the spec declares reported_items).
  check_sketch.py --accept sN --rev k --note "<Design Notes ref>"
                                   flags the revision accepted (accepted, accepted_note, accepted_at), copies its wip/
                                   outputs up to docs/sketches/ with SHA-256 equality, marks earlier accepted records of
                                   the sketch superseded_by k. Refused (exit 1) when the record is absent, a check is not
                                   pass (RPT included; a record that declares reported_items without an RPT row), the note is empty, or a PNG of the same name in docs/sketches/ differs in pixels.
  check_sketch.py --stale          recorded key values of the latest accepted, unsuperseded record per sketch (docs/sketches/)
                                   against live params and overlay; exit 1 on any difference (--include-unaccepted also
                                   checks the unaccepted records in wip/).
  check_sketch.py --controls [--jobs N] [--only ids]
                                   every entry of fixtures/manifest.yaml against its expected result, in N spawn worker
                                   processes (default min(cpu_count - 2, 12); rows in manifest order, per-control results
                                   equal to --jobs 1); writes wip/fixtures/controls_results.json and wip/fixtures/figs/
                                   (ctrl PNGs, key.json, generated once in the main process). --only (comma-separated id
                                   globs or check ids) runs a subset to wip/fixtures/controls_results_partial.json,
                                   "PARTIAL, not a record": never read by control_tally() or --accept. --manifest runs
                                   another manifest and writes its results beside it (runner controls).
  check_sketch.py --baseline sN    assembles wip/baseline_red.json: run 1 from controls_results.json (wip/ first), run 2
                                   for sN from sN_checks_r0.json (wip/ first, else docs/sketches/); prior records kept.
Output rule (sketch_loader docstring, Design Notes 26 decision 1): every output goes to wip/; only --accept writes to
docs/sketches/. Options --params and --overlay point the loader at other files; --docs-dir and --wip-dir point --accept
and --stale at other directories (temporary copies for the H1 controls).
Exit 0 when every result matches its expectation (controls), or every check passes (sN), else 1.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import re
import shutil
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import WIP, Params, find_output, load_spec, load_yaml, output_path  # noqa: E402

K_ALL = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9"]
K_BY_SKETCH = {"s5": ["K1", "K2", "K3", "K4", "K9"]}
# Per-sketch tables (H3). A sketch's checks_sN.py may define STUB_EXPECT, STUB_CAUSE and SOURCES (each for that sketch
# only); they take precedence over the entries here, so S2 to S6 add theirs at step (c) without editing baseline().
_ABS_K = ("absent", "red (absent, fail-closed; content evidence run 1)")
_ABS_S = ("absent", "red (absent, fail-closed; content evidence run 1, S1-x B fixtures 1.1 (c))")
K_SOURCES = {
    "K1": "gameplan l.134; LLM-PLM 8.4.2; design freedom rule (P23)", "K2": "gameplan l.135; Design Notes 6",
    "K3": "gameplan l.136; LLM-PLM 8.4.2", "K4": "gameplan l.137; LLM-PLM 8.4.2",
    "K5": "gameplan l.138; LLM-PLM 8.4.1", "K6": "gameplan l.139 as replaced by Design Notes 17 (frame ruling)",
    "K7": "gameplan l.140; LLM-PLM 7.4; g_min seeds l.144-149 ASSUMED", "K8": "gameplan l.141; ASSEMBLY.md Coordinate frame",
    "K9": "gameplan l.142",
    "X1": "Loftsman 1.2 (b) section 2 and re-check ruling 5 (shared-row premise of the S1/S2 footprint identity)",
    "RPT": "1.3 open O10; Step 1.2 gate D3; gameplan detail 1.3 Reported (spec reported_items)",
}
SKETCH_TABLES = {
    "s1": {
        "STUB_EXPECT": {"guard": ["K1", "K2", "K3", "K5", "X1"],
                        "red": ["K4", "K6", "K7", "K8", "K9", "S1-1", "S1-2", "S1-3", "S1-4", "S1-5a", "S1-5b", "S1-6", "S1-7"]},
        "STUB_CAUSE": {"K6": _ABS_K, "K7": _ABS_K, "K8": _ABS_K,
                       **{k: _ABS_S for k in ("S1-1", "S1-2", "S1-3", "S1-4", "S1-5a", "S1-5b", "S1-6", "S1-7")}},
        "SOURCES": {
            "S1-1": "travel DECLARED [CP §15], [DN23]; advance DERIVED", "S1-2": "[DN23] (U13 re-derive, option R, Design Notes 22); park ASSUMED",
            "S1-7": "G2 (Design Notes 21); advance DERIVED; collet.core_stop_z ASSUMED",
            "S1-3": "core.length_install DECLARED; clearance ASSUMED", "S1-4": "overlay jackscrew.* ASSUMED",
            "S1-5a": "stop.g_stop reuse ASSUMED; bore ceiling ASSUMED (Q2e, Design Notes 19)",
            "S1-5b": "10 mm ASSUMED; wingnut.sweep_clear_radius DERIVED", "S1-6": "overlay jackscrew.angle, spacing DECLARED [DN23]",
        },
    },
}


def k_checks(s):
    """K checks run on sketch s: checks_sN.py's K_CHECKS when it defines one (S3 on), else K_BY_SKETCH, else K1 to K9."""
    p = HERE / f"checks_{s}.py"
    if p.is_file():
        mod = load_module(p, f"checks_{s}")
        if hasattr(mod, "K_CHECKS"):
            return list(mod.K_CHECKS)
    return K_BY_SKETCH.get(s, K_ALL)


# ---------------------------------------------------------------- RPT reported items (1.3 step 0 R3, O10, Step 1.2 gate D3)

# Records accepted before the RPT rule: their specs declare no reported_items; RPT reads exempt by record name (as K4's
# figure-note exemption reads by sketch id). A record of any other name whose spec declares no reported_items fails.
RPT_EXEMPT = {"s1_checks_r7.json": "S1 r7 accepted 2026-11-25 (Design Notes 13)",
              "s2_checks_r5.json": "S2 r5 accepted 2026-11-25 (Design Notes 13)"}
RPT_FIELDS = ("id", "text", "source", "needs_drawing")


def rpt_check(spec, items, rec_name, rev):
    """RPT: every id in the spec's reported_items has a value in items ({id: {value, basis, tag}}, from checks_sN.py
    reported(ctx)["items"]). A declared id with no value (absent or None) fails; on rev 0 the cause is "absent" when every
    missing item has needs_drawing: true, else "content". A spec with no reported_items fails unless the record name is
    in RPT_EXEMPT. Malformed entries (missing field, duplicate id) are spec errors."""
    decl = spec.get("reported_items")
    if not decl:
        if rec_name in RPT_EXEMPT:
            return {"id": "RPT", "result": "pass", "reason": f"not declared, exempt (accepted before RPT): {rec_name}, {RPT_EXEMPT[rec_name]}",
                    "measured": 0, "threshold": 0, "n_issues": 0, "cause": None, "exempt": True}
        return {"id": "RPT", "result": "fail", "reason": f"spec declares no reported_items ({rec_name} is not a record accepted before RPT)",
                "measured": 1, "threshold": 0, "n_issues": 1, "cause": "content"}
    items = items or {}
    issues, missing, seen = [], [], set()
    for it in decl:
        miss = [f for f in RPT_FIELDS if not isinstance(it, dict) or f not in it]
        iid = it.get("id") if isinstance(it, dict) else None
        if miss:
            issues.append(f"reported_items {iid!r}: spec error, missing {miss}")
            continue
        if iid in seen:
            issues.append(f"reported_items {iid}: spec error, duplicate id")
            continue
        seen.add(iid)
        v = items.get(iid)
        if not isinstance(v, dict) or v.get("value") is None:
            missing.append(it)
            issues.append(f"reported item {iid} ({it['text']}): no value" + (" (needs drawing)" if it["needs_drawing"] else ""))
    absent = rev == 0 and missing and len(missing) == len(issues) and all(m["needs_drawing"] for m in missing)
    ok = not issues
    return {"id": "RPT", "result": "pass" if ok else "fail",
            "reason": f"{len(decl)} reported item(s) declared, every one has a value" if ok else sc._summ(issues),
            "measured": len(issues), "threshold": 0, "n_issues": len(issues),
            "cause": None if ok else ("absent" if absent else "content")}


def sketch_table(s, name):
    """STUB_EXPECT, STUB_CAUSE or SOURCES for sketch s: checks_sN.py's attribute when it defines one, else SKETCH_TABLES."""
    p = HERE / f"checks_{s}.py"
    if p.is_file():
        mod = load_module(p, f"checks_{s}")
        if hasattr(mod, name):
            return getattr(mod, name)
    return SKETCH_TABLES.get(s, {}).get(name, {})


def source_of(s, cid):
    return K_SOURCES.get(cid) or sketch_table(s, "SOURCES").get(cid, "")


# ---------------------------------------------------------------- X1 shared-row lint (1.2 (c), Loftsman 1.2 (b))

X1_FIELDS = ("place", "z_rule", "plan_poly")


def _x1_norm(v):
    if isinstance(v, str):
        return " ".join(v.split())
    if isinstance(v, dict):
        return {str(k): _x1_norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_x1_norm(x) for x in v]
    return v


def x1_lint(specs=None):
    """Premise of the S1/S2 footprint identity (Loftsman 1.2 (b) section 2): for every row id present in two or more
    specs, the place, z_rule and plan_poly expressions are equal after whitespace normalisation, so one check_stack
    evaluation gives one footprint and one z band in every sketch. A field present in one spec only is skipped and
    listed; a row carrying x1_exempt: {reason} in any spec passes and is listed. specs: {name: spec} (default: every
    s*_spec.yaml beside this file)."""
    if specs is None:
        specs = {p.stem.replace("_spec", ""): load_spec(p) for p in sorted(HERE.glob("s*_spec.yaml"))}
    by_id = {}
    for name, spec in specs.items():
        for row in spec.get("features", []):
            by_id.setdefault(row["id"], []).append((name, row))
    issues, skipped, exempt, n = [], [], [], 0
    for fid, occ in sorted(by_id.items()):
        if len(occ) < 2:
            continue
        n += 1
        ex = next((r.get("x1_exempt") for _, r in occ if r.get("x1_exempt")), None)
        if ex:
            exempt.append(f"{fid} ({ex.get('reason') if isinstance(ex, dict) else ex})")
            continue
        for fld in X1_FIELDS:
            have = [(nm, r[fld]) for nm, r in occ if r.get(fld) is not None]
            if not have:
                continue
            if len(have) < len(occ):
                skipped.append(f"{fid} {fld} (only in {', '.join(nm for nm, _ in have)})")
                continue
            ref_nm, ref = have[0][0], json.dumps(_x1_norm(have[0][1]), sort_keys=True)
            for nm, v in have[1:]:
                if json.dumps(_x1_norm(v), sort_keys=True) != ref:
                    sub = ""
                    if isinstance(have[0][1], dict) and isinstance(v, dict):
                        keys = sorted(k for k in set(have[0][1]) | set(v) if _x1_norm(have[0][1].get(k)) != _x1_norm(v.get(k)))
                        sub = "." + ",".join(keys)
                    issues.append(f"{fid} {fld}{sub}: {ref_nm} and {nm} differ")
    msg = f"{n} shared row(s) compared on {', '.join(X1_FIELDS)}; skipped {len(skipped)}: {', '.join(skipped) or 'none'}" + \
          (f"; exempt: {', '.join(exempt)}" if exempt else "")
    return {"id": "X1", "result": "pass" if not issues else "fail", "reason": (sc._summ(issues) + "; " + msg) if issues else msg,
            "measured": len(issues), "threshold": 0, "n_issues": len(issues), "cause": None if not issues else "content",
            "compared": n, "skipped": skipped}


TIMESTAMP = lambda: datetime.datetime.now().isoformat(timespec="seconds")  # noqa: E731
SKETCH_CHECK = re.compile(r"^S(\d+)-")   # S<n>-x routes to checks_s<n>.py (1.3 step 0 R4, O13)
_MODS = {}


def load_module(path, name=None):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"missing file: {path}")
    key = str(path)
    if key not in _MODS:
        spec = importlib.util.spec_from_file_location(name or path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MODS[key] = mod
    return _MODS[key]


def safe(fn, cid, *a):
    try:
        return fn(*a)
    except FileNotFoundError as e:
        return {"id": cid, "result": "error", "reason": f"missing file: {e}", "measured": None, "threshold": None}
    except Exception as e:  # noqa: BLE001
        return {"id": cid, "result": "error", "reason": f"{type(e).__name__}: {e}", "measured": None, "threshold": None,
                "trace": traceback.format_exc(limit=3)}


# ---------------------------------------------------------------- controls

def run_control(entry):
    file, fn = entry["fixture"].split("::")
    mod = load_module(HERE / "fixtures" / file, "fixture_builders" if file == "builders.py" else Path(file).stem)
    built = getattr(mod, fn)()
    if isinstance(built, dict) and "result" in built:   # harness controls (H1, H5): the fixture returns a check result
        return {"states": [], "failing": 0, "measured": None, "threshold": None, **built}
    if entry["check"] == "ALL":
        ctx, extra = built
        res = [safe(sc.CHECKS[k], k, ctx) for k in K_ALL] + extra(ctx)
        return {"id": "ALL", "result": "error" if any(r["result"] == "error" for r in res) else "pass",
                "reason": " || ".join(f"{r['id']} {r['result']}" + (f" ({r.get('cause')})" if r["result"] == "fail" else "") for r in res),
                "measured": None, "threshold": None, "per_check": res}
    ctxs = built if isinstance(built, list) else [built]
    for c in ctxs:
        if entry.get("anchors"):
            c.anchors = entry["anchors"]
    m = SKETCH_CHECK.match(entry["check"])
    if m:   # sketch checks S<n>-x (1.1 (b), 1.2 (c); 1.3 step 0 R4): checks_s<n>.py, judged as K checks
        s = f"s{m.group(1)}"
        smod = load_module(HERE / f"checks_{s}.py", f"checks_{s}")
        fn = dict(smod.CHECKS)[entry["check"]]
        res = [smod._run(entry["check"], fn, c) for c in ctxs]
    else:
        res = [sc.CHECKS[entry["check"]](c) for c in ctxs]
    out = {"id": entry["check"], "result": "fail" if any(r["result"] != "pass" for r in res) else "pass",
           "reason": " || ".join(r["reason"] for r in res), "measured": [r["measured"] for r in res],
           "threshold": res[0]["threshold"], "states": [s for r in res for s in r.get("states", [])],
           "failing": sum(r.get("failing", 0) for r in res), "n_issues": sum(r.get("n_issues", 0) for r in res)}
    return out


def compare(entry, res):
    """Z: clean (and, for a state expectation, every tested pair in that state). B: fires, the reason carries every
    planted substring, and the issue count equals the planted count (default 1), so a B that fires for an extra or a
    different reason is a mismatch (SW-2). smoke: every check returns pass or fail, none error, none fail-closed on
    an absent part (SW-8)."""
    exp = entry["expected"]
    if res["result"] == "error":
        return False, "error"
    if exp == "runs":
        bad = [r["id"] for r in res["per_check"] if r["result"] == "error" or r.get("cause") == "absent"]
        return not bad, "runs" if not bad else f"error or absent in {bad}"
    observed = "clean" if res["result"] == "pass" else "fires"
    if exp == "clean":
        return observed == "clean", observed
    if exp == "fires":
        want_n = entry.get("planted", 1)
        missing = [s for s in entry.get("reason", []) if s not in res["reason"]]
        ok = observed == "fires" and not missing and res.get("n_issues") == want_n
        note = f" ({res.get('n_issues')} issue(s), planted {want_n})"
        if missing:
            note += f"; reason lacks {missing}"
        return ok, observed + note
    states = res.get("states", [])
    ok = observed == "clean" and bool(states) and all(s == exp for s in states)
    return ok, f"{observed}, states {states}"


CONTROLS_RESULTS = "fixtures/controls_results.json"   # path under wip/ (written) and under docs/sketches/ (committed copy)
CONTROLS_PARTIAL = "fixtures/controls_results_partial.json"   # --only runs (1.3 step 0, O9): never a record
CONTROL_FIGS = "fixtures/figs"
MANIFEST = HERE / "fixtures" / "manifest.yaml"
# Per-control equality between --jobs 1 and --jobs N (1.3 step 0 R1 b) covers these row fields; "seconds" (wall time of
# the control in its worker) is excluded, as is the file timestamp.
CONTROL_EQ_FIELDS = ("id", "expected", "observed", "reason", "match")


def default_jobs():
    import os
    return max(1, min((os.cpu_count() or 1) - 2, 12))


def control_row(e):
    """One manifest entry run and compared; the row as written to the results file, plus the printed line."""
    import time
    t0 = time.perf_counter()
    res = safe(run_control, e["check"], e)
    ok, observed = compare(e, res)
    row = {"id": e["id"], "check": e["check"], "control": e["control"], "expected": e["expected"],
           "observed": observed, "reason": res["reason"], "match": "yes" if ok else "no", "gameplan_line": e.get("gameplan_line"),
           "finding": e.get("finding")}
    if "per_check" in res:
        row["reported"] = [{k: r.get(k) for k in ("id", "result", "cause", "measured", "reason")} for r in res["per_check"]]
    row["seconds"] = round(time.perf_counter() - t0, 3)
    return row


def _control_task(item):   # worker entry (spawn start method: module-level, picklable)
    i, e = item
    return i, control_row(e)


def select_controls(man, only):
    """--only: comma-separated tokens; an entry is kept when its id matches a token as an fnmatch glob or its check id
    equals a token."""
    import fnmatch
    toks = [t.strip() for t in str(only).split(",") if t.strip()]
    return [e for e in man if any(fnmatch.fnmatchcase(e["id"], t) or e["check"] == t for t in toks)]


def run_controls_rows(man, jobs):
    """Rows in manifest order. jobs 1: in this process; jobs > 1: a spawn pool, one entry per task (each worker keeps
    its own module cache, so a control never sees another's state except through its own worker's caches)."""
    if jobs <= 1 or len(man) <= 1:
        return [control_row(e) for e in man]
    import multiprocessing as mp
    out = [None] * len(man)
    with mp.get_context("spawn").Pool(min(jobs, len(man))) as pool:
        for i, row in pool.imap_unordered(_control_task, list(enumerate(man)), chunksize=1):
            out[i] = row
    return out


def controls(args):
    import time
    t0 = time.perf_counter()
    man_path = Path(args.manifest) if getattr(args, "manifest", None) else MANIFEST
    man = load_yaml(man_path)["controls"]
    only = getattr(args, "only", None)
    if only:
        man = select_controls(man, only)
    jobs = args.jobs if getattr(args, "jobs", None) else default_jobs()
    rows = run_controls_rows(man, jobs)
    for r in rows:
        print(f"{r['id']:9s} {r['control']} expected {r['expected']:16s} observed {r['observed'][:40]:40s} match {'yes' if r['match'] == 'yes' else 'NO'}")
    z = [r for r in rows if r["control"] == "Z"]
    b = [r for r in rows if r["control"] == "B"]
    sm = [r for r in rows if r["control"] == "smoke"]
    summary = {"z_clean": sum(r["match"] == "yes" for r in z), "z_total": len(z),
               "b_fired": sum(r["match"] == "yes" for r in b), "b_total": len(b),
               "smoke_ok": sum(r["match"] == "yes" for r in sm), "smoke_total": len(sm)}
    record = not only and man_path.resolve() == MANIFEST.resolve()
    if record:   # control figures and key.json once, in this process, only for the full live set
        figs = output_path(CONTROL_FIGS + "/key.json").parent   # wip/fixtures/figs (R4-c)
        try:
            mod = load_module(HERE / "fixtures" / "builders.py", "fixture_builders")
            key = mod.control_figures(figs)
            (figs / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            summary["ctrl_figs_error"] = f"{type(e).__name__}: {e}"
    wall = round(time.perf_counter() - t0, 1)
    summary.update(jobs=jobs, wall_seconds=wall)
    out = {"run": 1, "timestamp": TIMESTAMP(), "summary": summary, "controls": rows}
    if record:
        dst = output_path(CONTROLS_RESULTS)
    elif only and man_path.resolve() == MANIFEST.resolve():
        out["partial"] = {"only": only, "note": "PARTIAL, not a record (never read by control_tally or --accept)"}
        dst = output_path(CONTROLS_PARTIAL)
    else:   # another manifest (runner controls): results beside that manifest, never under wip/ or docs/
        out["manifest"] = str(man_path)
        dst = man_path.parent / "controls_results.json"
    dst.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"Z clean {summary['z_clean']}/{summary['z_total']}, B fired {summary['b_fired']}/{summary['b_total']}, "
          f"smoke {summary['smoke_ok']}/{summary['smoke_total']}; jobs {jobs}; wall {wall} s")
    if only:
        print(f"PARTIAL, not a record: {len(rows)} control(s) selected by --only {only!r}; written to {dst}")
    return 0 if all(r["match"] == "yes" for r in rows) else 1


def control_tally():
    p = find_output(CONTROLS_RESULTS)   # wip/ first, then the committed copy
    if not p.is_file():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    tally = {}
    for r in data["controls"]:
        if r["control"] not in ("Z", "B"):
            continue
        t = tally.setdefault(r["check"], {"Z": [0, 0], "B": [0, 0]})
        t[r["control"]][1] += 1
        t[r["control"]][0] += r["match"] == "yes"
    return {k: {"Z": f"clean {v['Z'][0]}/{v['Z'][1]}", "B": f"fired {v['B'][0]}/{v['B'][1]}", "run": data["timestamp"]} for k, v in tally.items()}


# ---------------------------------------------------------------- sketch run

def run_sketch(args):
    s, rev = args.sketch, args.rev
    P = Params(args.params, args.overlay)
    spec_path = HERE / f"{s}_spec.yaml"
    spec = load_spec(spec_path)
    stack = check_stack.evaluate_spec(P, spec)
    script = HERE / "stubs" / f"{s}_stub.py" if rev == 0 else HERE / spec["script"]
    mod = load_module(script, f"{s}_script")
    figs = mod.build(P, spec, stack)
    ctx = sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], script_paths=[script],
                 overlay_path=P.overlay_path, check_stack_path=HERE / "check_stack.py")
    results = [safe(sc.CHECKS[k], k, ctx) for k in k_checks(s)]
    for r in results:   # Loftsman 1.2 (e) LF1.2-1: the K7 record carries every test by pose and pair
        if r["id"] == "K7" and r["result"] != "error":
            lint = sc.k7_record_issues(r)
            if lint:
                r.update(result="fail", reason=sc._summ(lint) + " || " + r["reason"], n_issues=(r.get("n_issues") or 0) + len(lint), cause="content")
    smod_path = HERE / f"checks_{s}.py"
    smod = load_module(smod_path, f"checks_{s}")
    results += smod.run(ctx)
    results.append(safe(x1_lint, "X1"))
    acc = dict(P.accessed)   # keys_read keeps its pre-RPT scope: keys the reported values read are not added
    rd = safe(smod.reported, "reported", ctx) if hasattr(smod, "reported") else None
    P.accessed.clear()
    P.accessed.update(acc)
    items = rd.get("items") if isinstance(rd, dict) else None
    results.append(safe(rpt_check, "RPT", spec, items, record_name(s, rev), rev))
    tally = control_tally()
    for r in results:
        r["z_result"] = tally.get(r["id"], {}).get("Z", "not run at 1.0 (Z fixture from the signed spec, 1.1)")
        r["b_result"] = tally.get(r["id"], {}).get("B", "not run at 1.0 (B fixture from the signed spec, 1.1)")
        r["source"] = source_of(s, r["id"])
    keys_read = {}
    for k in sorted(set(sc.spec_keys(spec)) | set(P.accessed)):
        if P.has(k):
            keys_read[k] = {"value": P.get(k), "origin": P.origin(k), "status": P.leaf(k).get("status")}
    rec = {"sketch": s, "rev": rev, "timestamp": TIMESTAMP(), "spec": spec_path.name, "spec_status": spec.get("status"),
           "script": str(script.relative_to(HERE)), "accepted": False, "frame": "z_S = z_A + jig.datum_a_above_floor",
           "files_sha256": P.hashes(), "keys_read": keys_read, "reported": check_stack.reported(P, spec, stack), "checks": results}
    if rd is not None:   # per-sketch drawn reported values (no threshold, never asserted)
        rec["reported_drawn"] = rd
    if spec.get("reported_items"):   # RPT (1.3 step 0): the declared list travels with the record; --accept reads it
        rec["reported_items"] = spec["reported_items"]
    write_record(rec, args.wip_dir)
    exp = sketch_table(s, "STUB_EXPECT") if rev == 0 else {}
    for r in results:
        tag = " guard" if r["id"] in exp.get("guard", []) else ""
        print(f"{r['id']:6s} {r['result']:5s}{tag}  {r['reason'][:150]}")
    return 0 if all(r["result"] == "pass" for r in results) else 1


def record_name(s, rev):
    return f"{s}_checks_r{rev}.json"


def write_record(rec, wip_dir=None):
    """A sketch run's record and summary, to wip/ (output rule). A re-run of an accepted revision writes here too, so the
    accepted record in docs/sketches/ keeps its flag (H1 e)."""
    d = Path(wip_dir) if wip_dir else output_path(record_name(rec["sketch"], rec["rev"])).parent
    d.mkdir(parents=True, exist_ok=True)
    (d / record_name(rec["sketch"], rec["rev"])).write_text(json.dumps(rec, indent=1, default=str), encoding="utf-8")
    write_summary(rec, d / f"{rec['sketch']}_summary_r{rec['rev']}.md")
    return d / record_name(rec["sketch"], rec["rev"])


def _f2(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else str(v)


def write_summary(rec, path):
    lines = [f"# {rec['sketch'].upper()} checks, revision r{rec['rev']}", "",
             f"{rec['timestamp']}. Spec {rec['spec']} ({rec['spec_status']}); script {rec['script']}. Frame {rec['frame']}.", "",
             "| Check | Result | Measured | Threshold | Z | B | Reason |", "|---|---|---|---|---|---|---|"]
    for r in rec["checks"]:
        reason = str(r["reason"]).replace("|", "/")[:160]
        lines.append(f"| {r['id']} | {r['result']} | {r['measured']} | {r['threshold']} | {r['z_result']} | {r['b_result']} | {reason} |")
    rep = rec["reported"]
    lines += ["", "| Check | Cause of red |", "|---|---|"] + [f"| {r['id']} | {r.get('cause')} |" for r in rec["checks"] if r["result"] != "pass"]
    lines += ["", "Reported (no threshold):",
              f"- Park tip {rep['park_tip_z_A']:.2f} z_A (entry plane {rep['entry_plane']}); highest class start {rep['start_tip_max_z_A']:.2f} z_A; "
              f"lift stroke {rep['lift_stroke_mm']:.2f} mm; S1-3 load plane {rep['load_plane']}"]
    for name, o in (rep.get("q9_options") or {}).items():
        lines.append(f"- Q9 {name}: park {o['park_tip_z_A']:.2f} z_A, stroke {o['lift_stroke']:.2f} mm, L " +
                     ", ".join(f"{k} {_f2(v)}" for k, v in o["L"].items()))
        for lab, e in (o.get("symbol_terms") or {}).items():
            lines.append(f"  - {name}, {lab}: {e}")
    lines += [
              f"- Collar top recomputed {rep['collar_top_recomputed_z_A']:.2f} z_A against params stop.collar_top_z {rep['collar_top_params_z_A']}",
              "- Park tip z_A by plane and core length: " + "; ".join(
                  f"{t}: " + ", ".join(f"{k.split('.')[-1]} {_f2(v)}" for k, v in d.items()) for t, d in rep["park_tip_by_plane_z_A"].items()),
              f"- Start tip minus capture-core top ({rep['capture_core_length_key']}) on the core stop: {rep['start_tip_minus_core_top_mm']:.2f} mm "
              f"(end tip + drill_advance_500core = {rep['end_tip_plus_advance_z_A']:.2f} z_A; core top {rep['core_top_on_core_stop_z_A']:.2f} z_A)"]
    for pid, v in rep["poses"].items():
        if v["highest_z_S"] is not None:
            lines.append(f"- {pid}: highest point {v['highest_z_S']:.2f} z_S, margin to the 2000 mm soft target {v['margin_to_soft_target']:.2f} mm (spec values, not drawn)")
    rd = rec.get("reported_drawn")
    if isinstance(rd, dict) and rd.get("rows"):
        lines += ["", f"## Reported values, drawn ({rec['script']} r{rec['rev']}; no threshold, never asserted)", "",
                  "| Quantity | Value | Basis |", "|---|---|---|"] + [f"| {q} | {v} | {b} |" for q, v, b in rd["rows"]]
    rpt = next((c for c in rec["checks"] if c["id"] == "RPT"), None)   # 1.3 step 0 R3: one row per declared item
    if rec.get("reported_items"):
        vals = (rd.get("items") if isinstance(rd, dict) else None) or {}
        lines += ["", "## Reported items (spec reported_items; RPT)", "", "| ID | Item | Value | Basis | Tag |", "|---|---|---|---|---|"]
        for it in rec["reported_items"]:
            v = vals.get(it.get("id")) if isinstance(vals.get(it.get("id")), dict) else {}
            cell = lambda x: "ABSENT" if x is None else str(x).replace("|", "/")  # noqa: E731
            lines.append(f"| {it.get('id')} | {cell(it.get('text'))} | {cell(v.get('value'))} | {cell(v.get('basis'))} | {cell(v.get('tag'))} |")
    elif rpt is not None:
        lines += ["", f"Reported items: {rpt['reason']}"]
    lines += ["", f"Files: " + ", ".join(f"{k} {v[:12]}" for k, v in rec["files_sha256"].items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- stale

def _dirs(args):
    docs = Path(args.docs_dir) if getattr(args, "docs_dir", None) else HERE
    wip = Path(args.wip_dir) if getattr(args, "wip_dir", None) else WIP
    return docs, wip


def _rev_of(p):
    return int(Path(p).stem.rsplit("_r", 1)[1])


def stale_records(docs, wip, include_unaccepted=False):
    """Records --stale checks: per sketch, the latest accepted record in docs/ without superseded_by (H1 d); with
    include_unaccepted, also every unaccepted record in wip/."""
    latest = {}
    for p in sorted(Path(docs).glob("s*_checks_r*.json")):
        rec = json.loads(p.read_text(encoding="utf-8"))
        if not rec.get("accepted") or rec.get("superseded_by") is not None:
            continue
        s = rec.get("sketch", p.name.split("_")[0])
        if s not in latest or _rev_of(p) > _rev_of(latest[s][0]):
            latest[s] = (p, rec)
    out = list(latest.values())
    if include_unaccepted and Path(wip).is_dir():
        for p in sorted(Path(wip).glob("s*_checks_r*.json")):
            rec = json.loads(p.read_text(encoding="utf-8"))
            if not rec.get("accepted"):
                out.append((p, rec))
    return out


def stale_diffs(P, records):
    diffs = []
    for p, rec in records:
        for k, v in rec.get("keys_read", {}).items():
            live = P.get(k) if P.has(k) else "<missing>"
            if live != v["value"]:
                diffs.append(f"{Path(p).parent.name}/{Path(p).name}: {k} recorded {v['value']!r}, live {live!r}")
    return diffs


def stale(args):
    P = Params(args.params, args.overlay)
    docs, wip = _dirs(args)
    recs = stale_records(docs, wip, args.include_unaccepted)
    diffs = stale_diffs(P, recs)
    for p, _ in recs:
        print(f"checked {p.parent.name}/{p.name}")
    for d in diffs:
        print("STALE", d)
    print(f"--stale: {len(recs)} record(s) checked, {len(diffs)} difference(s)")
    x1 = x1_lint()   # 1.2 (c): the shared-row premise runs with every --stale
    print(f"X1 {x1['result']}: {x1['reason']}")
    return 1 if diffs or x1["result"] != "pass" else 0


# ---------------------------------------------------------------- accept (H1)

def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _png_pixels_equal(a, b):
    import matplotlib.image as mpimg
    import numpy as np
    A, B = mpimg.imread(str(a)), mpimg.imread(str(b))
    return A.shape == B.shape and bool(np.array_equal(A, B))


def _json_field_diffs(a, b, prefix=""):
    """Leaf paths whose values differ between two JSON values (sorted)."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                out.append(f"{prefix}{k} ({'added' if k not in a else 'removed'})")
            else:
                out += _json_field_diffs(a[k], b[k], f"{prefix}{k}.")
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in _json_field_diffs(x, y, f"{prefix}{i}.")]
    return [] if a == b else [prefix.rstrip(".")]


def revision_outputs(d, s, k):
    """Outputs of revision k of sketch s in directory d: checks JSON, summary, PNGs, mass report, visual-gate file."""
    d = Path(d)
    names = [record_name(s, k), f"{s}_summary_r{k}.md", f"{s}_mass_report_r{k}.json", f"{s}_visual_gate_r{k}.md"]
    out = [d / n for n in names if (d / n).is_file()]
    out += sorted(p for p in d.glob(f"{s}_*_r{k}.png"))
    return out


def harness_outputs(wip):
    """Verification records in wip/ that --accept copies up with the revision (R4-c): the --controls results and control
    figures, and the --baseline record. Copied only when the wip/ controls run matched every control."""
    wip = Path(wip)
    ctrl = wip / CONTROLS_RESULTS
    if not ctrl.is_file():
        return []
    data = json.loads(ctrl.read_text(encoding="utf-8"))
    if any(r.get("match") != "yes" for r in data.get("controls", [])):
        return []
    out = [ctrl] + sorted(p for p in (wip / CONTROL_FIGS).glob("*") if p.is_file())
    if (wip / BASELINE).is_file():
        out.append(wip / BASELINE)
    return out


def _rel_to(p, base):
    return str(Path(p).relative_to(base)).replace("\\", "/")


def accept(s, k, note, docs, wip, out=print):
    """H1. Returns (exit code, message lines). Writes nothing when refused before the copy."""
    docs, wip = Path(docs), Path(wip)
    msgs = []

    def say(m):
        msgs.append(m)
        out(m)
    if not s or k is None:
        say("refused: --accept needs a sketch id and --rev")
        return 1, msgs
    if not str(note or "").strip():
        say("refused: empty note (--note \"<Design Notes ref>\")")
        return 1, msgs
    src = wip / record_name(s, k) if (wip / record_name(s, k)).is_file() else docs / record_name(s, k)
    if not src.is_file():
        say(f"refused: record {record_name(s, k)} absent in {wip} and {docs}")
        return 1, msgs
    rec = json.loads(src.read_text(encoding="utf-8"))
    bad = [f"{c['id']} {c['result']}" for c in rec.get("checks", []) if c.get("result") != "pass"]
    if not rec.get("checks"):
        bad.append("no checks in record")
    if rec.get("reported_items") and not any(c.get("id") == "RPT" for c in rec.get("checks", [])):
        bad.append("RPT absent (record declares reported_items)")   # 1.3 step 0 R3
    if bad:
        say(f"refused: {src.name} has checks not pass: {', '.join(bad)}")
        return 1, msgs
    ups = revision_outputs(wip, s, k) if src.parent == wip else []
    blocks, plan = [], []
    for p in ups:
        dst = docs / p.name
        if not dst.exists():
            plan.append((p, dst, "new"))
        elif p.suffix == ".png":
            if _sha(p) == _sha(dst):
                plan.append((p, dst, "byte-equal, kept"))
            elif _png_pixels_equal(p, dst):
                plan.append((p, dst, "pixel-equal, kept"))
            else:
                blocks.append(f"{p.name} differs in pixels from {dst} (drawn geometry moved: new revision)")
        else:
            plan.append((p, dst, "replace"))
    if blocks:
        for b in blocks:
            say(f"refused: {b}")
        return 1, msgs
    ctrl = wip / CONTROLS_RESULTS   # SW 1.2 (c) FIX 4: a revision is not accepted on a red harness
    if ctrl.is_file():
        rows = json.loads(ctrl.read_text(encoding="utf-8")).get("controls", [])
        nbad = sum(1 for r in rows if r.get("match") != "yes")
        if nbad:
            say(f"refused: wip/ controls results: {nbad} mismatched ({CONTROLS_RESULTS}; re-run --controls)")
            return 1, msgs
    stamp = TIMESTAMP()
    rec.update({"accepted": True, "accepted_note": note.strip(), "accepted_at": stamp})
    src.write_text(json.dumps(rec, indent=1, default=str), encoding="utf-8")
    if not ups:
        say(f"flag set in {src} (no wip/ outputs; record accepted in place)")
    for p, dst, how in plan:
        if how == "replace":
            if p.suffix == ".json":
                fd = _json_field_diffs(json.loads(dst.read_text(encoding="utf-8")), json.loads(p.read_text(encoding="utf-8")))
                say(f"replace {dst.name}: {len(fd)} differing field(s): " + "; ".join(fd))
            else:
                ol, nl = dst.read_text(encoding="utf-8").splitlines(), p.read_text(encoding="utf-8").splitlines()
                dl = [i + 1 for i in range(max(len(ol), len(nl)))
                      if (ol[i] if i < len(ol) else None) != (nl[i] if i < len(nl) else None)]
                say(f"replace {dst.name}: {len(dl)} differing line(s): {dl[:40]}")
        if how in ("new", "replace"):
            shutil.copyfile(p, dst)
            eq = _sha(p) == _sha(dst)
            say(f"copied {p.name} -> {dst}: SHA-256 {'equal' if eq else 'DIFFERENT'} {_sha(dst)[:16]}")
            if not eq:
                say("refused after copy: SHA-256 mismatch")
                return 1, msgs
        else:
            say(f"kept {dst.name} ({how})")
    for p in harness_outputs(wip):   # R4-c: committed control records change only here (or at the Manager close)
        dst = docs / p.relative_to(wip)
        if dst.exists() and _sha(p) == _sha(dst):
            say(f"kept {_rel_to(dst, docs)} (byte-equal)")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, dst)
        eq = _sha(p) == _sha(dst)
        say(f"copied {_rel_to(p, wip)} -> {_rel_to(dst, docs)}: SHA-256 {'equal' if eq else 'DIFFERENT'} {_sha(dst)[:16]}")
        if not eq:
            say("refused after copy: SHA-256 mismatch")
            return 1, msgs
    for p in sorted(docs.glob(f"{s}_checks_r*.json")):
        if _rev_of(p) >= k:
            continue
        r = json.loads(p.read_text(encoding="utf-8"))
        if r.get("accepted") and r.get("superseded_by") is None:
            r["superseded_by"] = k
            p.write_text(json.dumps(r, indent=1, default=str), encoding="utf-8")
            say(f"{p.name}: superseded_by {k} (flag kept)")
    say(f"accepted {s} r{k}: note {note.strip()!r}, at {stamp}")
    return 0, msgs


def accept_cmd(args):
    docs, wip = _dirs(args)
    rc, _ = accept(args.accept, args.rev if args.rev_given else None, args.note, docs, wip)
    return rc


# ---------------------------------------------------------------- baseline

BASELINE = "baseline_red.json"


def _rel(p):
    try:
        return str(Path(p).relative_to(HERE)).replace("\\", "/")
    except ValueError:
        return str(p)


def baseline(args):
    s = args.baseline
    ctrl_path = find_output(CONTROLS_RESULTS)
    ctrl = json.loads(ctrl_path.read_text(encoding="utf-8"))
    r0_path = find_output(record_name(s, 0))
    if not r0_path.is_file():
        print(f"--baseline {s}: {record_name(s, 0)} absent in wip/ and docs/sketches/")
        return 1
    r0 = json.loads(r0_path.read_text(encoding="utf-8"))
    rows = [{"id": r["id"], "run": 1, "control": r["control"], "expected": r["expected"], "observed": r["observed"],
             "reason": r["reason"], "match": r["match"]} for r in ctrl["controls"]]
    exp, causes = sketch_table(s, "STUB_EXPECT"), sketch_table(s, "STUB_CAUSE")
    run2 = []
    for r in r0["checks"]:
        if r["id"] in exp.get("guard", []):
            e, ok = "green (guard)", r["result"] == "pass"
        elif r["id"] in exp.get("red", []):
            want_cause = causes.get(r["id"], ("content", "red (content)"))
            e = want_cause[1]
            ok = r["result"] == "fail" and r.get("cause") == want_cause[0] and "missing file" not in r["reason"]
        else:
            e, ok = "unlisted", False
        obs = "green" if r["result"] == "pass" else ("red" if r["result"] == "fail" else "error")
        run2.append({"id": r["id"], "run": 2, "sketch": s, "expected": e,
                     "observed": obs + (f" ({r.get('cause')})" if obs == "red" else ""), "reason": r["reason"],
                     "match": "yes" if ok else "no"})
    prior_path = find_output(BASELINE)
    prior = json.loads(prior_path.read_text(encoding="utf-8")) if prior_path.is_file() else {}
    # run 2 per sketch (H3): other sketches' run 2 carry over from the prior record; a pre-H3 record holds S1 run 2 only.
    if "run2_by_sketch" in prior:
        prev = prior["run2_by_sketch"]
    else:
        prev = {"s1": prior["run2"]} if prior.get("run2") else {}
    by_sketch = {k: v for k, v in prev.items() if k != s}
    rows_prev = [r for r in prior.get("checks", []) if r.get("run") == 2 and r.get("sketch") not in (None, s)]
    by_sketch[s] = {"source": _rel(r0_path), "at": r0["timestamp"], "spec_status": r0["spec_status"],
                    "matched": sum(r["match"] == "yes" for r in run2), "total": len(run2)}
    out = {"timestamp": TIMESTAMP(), "run1": {"source": _rel(ctrl_path), "at": ctrl["timestamp"], **ctrl["summary"]},
           "run2": by_sketch[s], "run2_by_sketch": by_sketch, "checks": rows + rows_prev + run2}
    if prior:   # keep earlier records under a dated key (1.1 (c) task 4)
        hist = prior.pop("prior", {})
        hist[f"{prior.get('timestamp', 'undated')} (spec {prior.get('run2', {}).get('spec_status')})"] = prior
        out["prior"] = hist
    dst = output_path(BASELINE)
    dst.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"wrote {_rel(dst)} (prior from {_rel(prior_path)})")
    print(json.dumps({k: out[k] for k in ("run1", "run2")}, indent=1))
    return 0 if all(r["match"] == "yes" for r in rows + run2) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="sketch checks")
    ap.add_argument("sketch", nargs="?")
    ap.add_argument("--rev", type=int)
    ap.add_argument("--stale", action="store_true")
    ap.add_argument("--include-unaccepted", action="store_true")
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--jobs", type=int, help="--controls worker processes (default min(cpu_count - 2, 12))")
    ap.add_argument("--only", help="--controls subset: comma-separated id globs or check ids; PARTIAL, not a record")
    ap.add_argument("--manifest", help="--controls on another manifest (runner controls); results beside it")
    ap.add_argument("--baseline", metavar="sN")
    ap.add_argument("--accept", metavar="sN")
    ap.add_argument("--note")
    ap.add_argument("--params")
    ap.add_argument("--overlay")
    ap.add_argument("--docs-dir")
    ap.add_argument("--wip-dir")
    a = ap.parse_args(argv)
    a.rev_given = a.rev is not None
    if a.rev is None:
        a.rev = 0
    if a.accept:
        return accept_cmd(a)
    if a.controls:
        return controls(a)
    if a.stale:
        return stale(a)
    if a.baseline:
        return baseline(a)
    if a.sketch:
        return run_sketch(a)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
