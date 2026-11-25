"""Run the sketch checks (research/sean/gameplan.md detail 1.0, line 124).

  check_sketch.py sN [--rev k]     K1 to K9 plus checks_sN.py on the sketch (rev 0: stubs/sN_stub.py);
                                   writes sN_checks_r<k>.json and sN_summary_r<k>.md beside this file.
  check_sketch.py --stale          recorded key values of each accepted revision against live params and overlay;
                                   exit 1 on any difference (--include-unaccepted also checks unaccepted records).
  check_sketch.py --controls       every entry of fixtures/manifest.yaml against its expected result;
                                   writes fixtures/controls_results.json.
  check_sketch.py --baseline       assembles baseline_red.json from controls_results.json and s1_checks_r0.json.
Options --params and --overlay point the loader at other files (scratch copies for --stale tests).
Exit 0 when every result matches its expectation (controls), or every check passes (sN), else 1.
"""
import argparse
import datetime
import importlib.util
import json
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import Params, load_spec, load_yaml  # noqa: E402

K_ALL = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9"]
K_BY_SKETCH = {"s5": ["K1", "K2", "K3", "K4", "K9"]}
STUB_EXPECT = {"s1": {"guard": ["K1", "K2", "K3", "K5"],
                      "red": ["K4", "K6", "K7", "K8", "K9", "S1-1", "S1-2", "S1-3", "S1-4", "S1-5a", "S1-5b", "S1-6", "S1-7"]}}
_ABS_K = ("absent", "red (absent, fail-closed; content evidence run 1)")
_ABS_S = ("absent", "red (absent, fail-closed; content at 1.1 c)")
STUB_CAUSE = {"K6": _ABS_K, "K7": _ABS_K, "K8": _ABS_K, **{k: _ABS_S for k in ("S1-1", "S1-2", "S1-3", "S1-4", "S1-5a", "S1-5b", "S1-6", "S1-7")}}
SOURCES = {
    "K1": "gameplan l.134; LLM-PLM 8.4.2; design freedom rule (P23)", "K2": "gameplan l.135; Design Notes 6",
    "K3": "gameplan l.136; LLM-PLM 8.4.2", "K4": "gameplan l.137; LLM-PLM 8.4.2",
    "K5": "gameplan l.138; LLM-PLM 8.4.1", "K6": "gameplan l.139 as replaced by Design Notes 17 (frame ruling)",
    "K7": "gameplan l.140; LLM-PLM 7.4; g_min seeds l.144-149 ASSUMED", "K8": "gameplan l.141; ASSEMBLY.md Coordinate frame",
    "K9": "gameplan l.142",
    "S1-1": "travel DECLARED [CP §15], [DN23]; advance DERIVED", "S1-2": "[DN23] (U13 re-derive, option R, Design Notes 22); park ASSUMED",
    "S1-7": "G2 (Design Notes 21); advance DERIVED; collet.core_stop_z ASSUMED",
    "S1-3": "core.length_install DECLARED; clearance ASSUMED", "S1-4": "overlay jackscrew.* ASSUMED",
    "S1-5a": "stop.g_stop reuse ASSUMED; bore ceiling ASSUMED (Q2e, Design Notes 19)",
    "S1-5b": "10 mm ASSUMED; wingnut.sweep_clear_radius DERIVED", "S1-6": "overlay jackscrew.angle, spacing DECLARED [DN23]",
}
TIMESTAMP = lambda: datetime.datetime.now().isoformat(timespec="seconds")  # noqa: E731
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
    mod = load_module(HERE / "fixtures" / file, "fixture_builders")
    built = getattr(mod, fn)()
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


def controls(args):
    man = load_yaml(HERE / "fixtures" / "manifest.yaml")["controls"]
    rows = []
    for e in man:
        res = safe(run_control, e["check"], e)
        ok, observed = compare(e, res)
        row = {"id": e["id"], "check": e["check"], "control": e["control"], "expected": e["expected"],
               "observed": observed, "reason": res["reason"], "match": "yes" if ok else "no", "gameplan_line": e.get("gameplan_line"),
               "finding": e.get("finding")}
        if "per_check" in res:
            row["reported"] = [{k: r.get(k) for k in ("id", "result", "cause", "measured", "reason")} for r in res["per_check"]]
        rows.append(row)
        print(f"{e['id']:9s} {e['control']} expected {e['expected']:16s} observed {observed[:40]:40s} match {'yes' if ok else 'NO'}")
    z = [r for r in rows if r["control"] == "Z"]
    b = [r for r in rows if r["control"] == "B"]
    sm = [r for r in rows if r["control"] == "smoke"]
    summary = {"z_clean": sum(r["match"] == "yes" for r in z), "z_total": len(z),
               "b_fired": sum(r["match"] == "yes" for r in b), "b_total": len(b),
               "smoke_ok": sum(r["match"] == "yes" for r in sm), "smoke_total": len(sm)}
    try:
        mod = load_module(HERE / "fixtures" / "builders.py", "fixture_builders")
        key = mod.control_figures(HERE / "fixtures" / "figs")
        (HERE / "fixtures" / "figs" / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        summary["ctrl_figs_error"] = f"{type(e).__name__}: {e}"
    out = {"run": 1, "timestamp": TIMESTAMP(), "summary": summary, "controls": rows}
    (HERE / "fixtures" / "controls_results.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"Z clean {summary['z_clean']}/{summary['z_total']}, B fired {summary['b_fired']}/{summary['b_total']}, "
          f"smoke {summary['smoke_ok']}/{summary['smoke_total']}")
    return 0 if all(r["match"] == "yes" for r in rows) else 1


def control_tally():
    p = HERE / "fixtures" / "controls_results.json"
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
    results = [safe(sc.CHECKS[k], k, ctx) for k in K_BY_SKETCH.get(s, K_ALL)]
    smod_path = HERE / f"checks_{s}.py"
    smod = load_module(smod_path, f"checks_{s}")
    results += smod.run(ctx)
    tally = control_tally()
    for r in results:
        r["z_result"] = tally.get(r["id"], {}).get("Z", "not run at 1.0 (Z fixture from the signed spec, 1.1)")
        r["b_result"] = tally.get(r["id"], {}).get("B", "not run at 1.0 (B fixture from the signed spec, 1.1)")
        r["source"] = SOURCES.get(r["id"], "")
    keys_read = {}
    for k in sorted(set(sc.spec_keys(spec)) | set(P.accessed)):
        if P.has(k):
            keys_read[k] = {"value": P.get(k), "origin": P.origin(k), "status": P.leaf(k).get("status")}
    rec = {"sketch": s, "rev": rev, "timestamp": TIMESTAMP(), "spec": spec_path.name, "spec_status": spec.get("status"),
           "script": str(script.relative_to(HERE)), "accepted": False, "frame": "z_S = z_A + jig.datum_a_above_floor",
           "files_sha256": P.hashes(), "keys_read": keys_read, "reported": check_stack.reported(P, spec, stack), "checks": results}
    out_json = HERE / f"{s}_checks_r{rev}.json"
    out_json.write_text(json.dumps(rec, indent=1, default=str), encoding="utf-8")
    write_summary(rec, HERE / f"{s}_summary_r{rev}.md")
    exp = STUB_EXPECT.get(s, {}) if rev == 0 else {}
    for r in results:
        tag = " guard" if r["id"] in exp.get("guard", []) else ""
        print(f"{r['id']:6s} {r['result']:5s}{tag}  {r['reason'][:150]}")
    return 0 if all(r["result"] == "pass" for r in results) else 1


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
                     ", ".join(f"{k} {v:.2f}" for k, v in o["L"].items()))
    lines += [
              f"- Collar top recomputed {rep['collar_top_recomputed_z_A']:.2f} z_A against params stop.collar_top_z {rep['collar_top_params_z_A']}",
              "- Park tip z_A by plane and core length: " + "; ".join(
                  f"{t}: " + ", ".join(f"{k.split('.')[-1]} {v:.2f}" for k, v in d.items()) for t, d in rep["park_tip_by_plane_z_A"].items()),
              f"- Start tip minus capture-core top ({rep['capture_core_length_key']}) on the core stop: {rep['start_tip_minus_core_top_mm']:.2f} mm "
              f"(end tip + drill_advance_500core = {rep['end_tip_plus_advance_z_A']:.2f} z_A; core top {rep['core_top_on_core_stop_z_A']:.2f} z_A)"]
    for pid, v in rep["poses"].items():
        if v["highest_z_S"] is not None:
            lines.append(f"- {pid}: highest point {v['highest_z_S']:.2f} z_S, margin to the 2000 mm soft target {v['margin_to_soft_target']:.2f} mm (spec values, not drawn)")
    lines += ["", f"Files: " + ", ".join(f"{k} {v[:12]}" for k, v in rec["files_sha256"].items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- stale

def stale(args):
    P = Params(args.params, args.overlay)
    recs = sorted(HERE.glob("s*_checks_r*.json"))
    diffs, checked = [], 0
    for p in recs:
        rec = json.loads(p.read_text(encoding="utf-8"))
        if not rec.get("accepted") and not args.include_unaccepted:
            continue
        checked += 1
        for k, v in rec.get("keys_read", {}).items():
            live = P.get(k) if P.has(k) else "<missing>"
            if live != v["value"]:
                diffs.append(f"{p.name}: {k} recorded {v['value']!r}, live {live!r}")
    for d in diffs:
        print("STALE", d)
    print(f"--stale: {checked} record(s) checked, {len(diffs)} difference(s)")
    return 1 if diffs else 0


# ---------------------------------------------------------------- baseline

def baseline(args):
    ctrl = json.loads((HERE / "fixtures" / "controls_results.json").read_text(encoding="utf-8"))
    s1 = json.loads((HERE / "s1_checks_r0.json").read_text(encoding="utf-8"))
    rows = []
    for r in ctrl["controls"]:
        rows.append({"id": f"{r['id']}", "run": 1, "expected": r["expected"], "observed": r["observed"],
                     "reason": r["reason"], "match": r["match"]})
    exp = STUB_EXPECT["s1"]
    for r in s1["checks"]:
        if r["id"] in exp["guard"]:
            e, ok = "green (guard)", r["result"] == "pass"
        elif r["id"] in exp["red"]:
            want_cause = STUB_CAUSE.get(r["id"], ("content", "red (content)"))
            e = want_cause[1]
            ok = r["result"] == "fail" and r.get("cause") == want_cause[0] and "missing file" not in r["reason"]
        else:
            e, ok = "unlisted", False
        obs = "green" if r["result"] == "pass" else ("red" if r["result"] == "fail" else "error")
        rows.append({"id": r["id"], "run": 2, "expected": e, "observed": obs + (f" ({r.get('cause')})" if obs == "red" else ""),
                     "reason": r["reason"], "match": "yes" if ok else "no"})
    for r in rows:
        if r["run"] == 1:
            cr = next(c for c in ctrl["controls"] if c["id"] == r["id"])
            r["control"] = cr["control"]
    out = {"timestamp": TIMESTAMP(), "run1": {"source": "fixtures/controls_results.json", "at": ctrl["timestamp"], **ctrl["summary"]},
           "run2": {"source": "s1_checks_r0.json", "at": s1["timestamp"], "spec_status": s1["spec_status"],
                    "matched": sum(r["match"] == "yes" for r in rows if r["run"] == 2), "total": sum(r["run"] == 2 for r in rows)},
           "checks": rows}
    (HERE / "baseline_red.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("run1", "run2")}, indent=1))
    return 0 if all(r["match"] == "yes" for r in rows) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="sketch checks")
    ap.add_argument("sketch", nargs="?")
    ap.add_argument("--rev", type=int, default=0)
    ap.add_argument("--stale", action="store_true")
    ap.add_argument("--include-unaccepted", action="store_true")
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--params")
    ap.add_argument("--overlay")
    a = ap.parse_args(argv)
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
