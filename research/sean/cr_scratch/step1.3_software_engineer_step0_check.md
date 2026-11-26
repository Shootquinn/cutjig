# Step 1.3 step 0 (P0S) Software Engineer check: parallel runner, RPT, sketch-generic routing

Verdict: **FIX (4 items).** The runner is sound: 246/246 at --jobs 12 and at --jobs 1, per-control results equal, 117.5 s against the 200 s target. Every new B I re-ran on the pre-change code is red. Deleting branches in harness copies turned up ten branches no control notices. Four of them guard requirements written into R1, R3 or R5, so they are FIX. The other six are NOTEs. No check logic changes except FIX 2 (one condition in `--accept`). The rest is fixtures, manifest rows and one small pure function.

## Corrections to the brief

1. The prompt asks me to run --controls "yourself" on the live tree. Two other agents run against the same `docs/sketches/wip/` in parallel, and `controls()` always writes `wip/fixtures/controls_results.json` and `wip/fixtures/figs/`; the harness has no output-location option for --controls (`--wip-dir` applies to `--accept`, `--stale` and the sketch record only). I ran every control in byte-identical copies of `docs/sketches/` in my scratchpad (`sw0/live`, `params.yaml` one level up; copied after my SHA-256 baseline, which equals the P0 `sha_after.txt` on all 57 files). Nothing of mine wrote to `docs/sketches/wip/`. CPU was shared with the other agents and with my mutation runs during part of the parallel run, so wall times are upper bounds. The serial run (819.6 s) ran after the mutation runs finished, with only the other agents sharing the machine.
2. Engineer Correction 1 holds. S1 r7 reads K5 fail under TP1.1-9; that is the Topologist's ruling at P0T and outside this check.
3. Engineer section 2 says R1 b equality holds on "reason" except H1-B5. Same on my runs: the one difference is the temporary-directory name in the H1-B5 refusal text, and it differs between any two runs. That is acceptable; it needs to be stated as an exception in the gameplan line, since R1 b names reason as a compared field.

Tags: runs MEASURED 2026-11-26. Hand reasoning DERIVED.

## 1 R1 runner: re-runs and equality (task 1)

| Run (scratchpad copy `sw0/live`) | Result | Wall (MEASURED) | Engineer |
|---|---|---|---|
| `--controls` (default jobs 12) | Z 67/67, B 177/177, smoke 2/2, exit 0 | 117.5 s (summary `wall_seconds`; machine shared) | 113.4 s |
| `--controls --jobs 1` | Z 67/67, B 177/177, smoke 2/2, exit 0 | 819.6 s (sum of per-control seconds 815.7 s) | 804.3 s |

Target 200 s at default jobs: **met** (117.5 s). Sum of per-control seconds in the parallel run 1212.9 s (MEASURED); slowest S2-FULL 30.2 s, K8-B35 19.4, K8-Z8 19.1, K8-B34 18.5, K8-B39 18.3. The critical path is S2-FULL plus worker start-up.

Per-control comparison on id, expected, observed, reason, match (plus check, control, reported), row order included:

| Pair | Order | id | expected | observed | reason | match |
|---|---|---|---|---|---|---|
| mine jobs 12 vs mine jobs 1 | equal | 0 | 0 | 0 | 1 (H1-B5 temp path) | 0 |
| mine jobs 12 vs Engineer jobs 12 (`p0/ctl_par.json`) | equal | 0 | 0 | 0 | 1 (H1-B5 temp path) | 0 |

Partial runs (tried, task 1). In a copy with a sentinel `wip/fixtures/controls_results.json`, `--controls --only "K1-Z,K2-*"` ran 8 controls, printed "PARTIAL, not a record", wrote `controls_results_partial.json`, exit 0. The sentinel file is byte-unchanged (SHA-256 97f508a6… before and after); `control_tally()` still reads the sentinel; `harness_outputs()` (the --accept copy-up) lists the sentinel file, not the partial. On the live code a partial run cannot reach control_tally or --accept. No control guards this, though: see FIX 1 (M1).

Edge cases tried: `--only K2-b4` (typo, case-sensitive) selects 0 controls, prints "Z clean 0/0 …", exit 0. `--jobs 0` runs 12 jobs silently (`args.jobs if args.jobs else default_jobs()`).

Runner B: RUN-B on the pre-change code with the new fixtures: argparse exit 2, no "match NO" line, so it mismatches (red). On the live code it matches.

## 2 R3 RPT (task 2)

Direct calls to `rpt_check` and `accept` in a copy (MEASURED):

| Case | Result | Cause |
|---|---|---|
| rev 0, F_stall (needs_drawing true) missing | fail, 1 | absent |
| rev 0, L_min (needs_drawing false) missing | fail, 1 | content |
| rev 0, both missing | fail, 2 | content |
| rev 1, F_stall value None | fail, 1 | content |
| rev 1, values present, no basis or tag | **pass** | - |
| rev 1, value "" (empty string) | **pass** | - |
| items None (what `reported()` raising gives) | fail, 2, no exception text in reason | content |
| spec without items, record s1_checks_r7.json | pass, exempt | - |
| spec without items, s1_checks_r8.json / s3_checks_r7.json | fail | content |
| `reported_items: []` | fail ("declares no reported_items") | content |
| duplicate id; entry missing source and needs_drawing | fail, spec error | content |
| --accept, record declaring items, RPT fail (H1-B7) | refused | - |
| --accept, record declaring items, no RPT row (H1-B8) | refused | - |
| --accept, **s3 record, no reported_items, no RPT row** | **accepted, rc 0** | - |

RPT fails on a missing item, labels it absent on the stub, and blocks --accept when the record carries an RPT fail. The exemption is keyed on the record file name: a new sketch, or a new revision of S1 or S2, cannot claim it. The last row is the gap in FIX 2. `--accept` refuses only when a record declares reported_items and has no RPT row. A record with neither is accepted. `run_sketch` is the only thing that adds the RPT row, and no control calls `run_sketch` (M6).

## 3 New B red on pre-change code; branch deletion (task 3)

Pre-change code is the P0 copy `p0/pre`. Its SHA-256 equals P0 `sha_before.txt` on every file. I copied it to `sw0/red/pre` and added only the new builders.py, step0_fixtures.py and manifest.yaml. Each entry ran through that copy's own `run_control` and `compare`.

| ID | Pre-change observed | Red |
|---|---|---|
| K2-B4, K2-B5 | clean (no expr lint) | yes |
| K6-B10, K6-B11 | clean (0 z_rules / plan centres) | yes |
| RPT-B1, RPT-B2, H1-B7 | error (no rpt_check) | yes (H1-B7's refusal itself pre-exists through the generic not-pass rule, as the Engineer states) |
| H1-B8 | clean: record accepted and copied | yes |
| K5-B19 | clean (296 artists projected) | yes |
| K8-B42, K8-B43 | clean (190 / 185 predicates hold) | yes |
| K7-B34 | clean (1 pair test, F) | yes |
| RUN-B | exit 2, unrecognized arguments | yes |

Branch deletion. Each mutation went into a fresh copy of `docs/sketches/` (wip/ excluded) and I ran the listed controls with the copy's code. "Caught" means at least one mismatch. All controls matched in the unmutated copy.

| ID | Mutation | Controls run | Result |
|---|---|---|---|
| M1 | `record = not only and …` to `record = …` (partial run writes the record file) | RUN-Z, RUN-B | **not caught**. In that copy `--only "K1-Z,K2-*"` overwrote `wip/fixtures/controls_results.json` with 8 rows; `control_tally()` reported K1 and K2 only; `harness_outputs()` offered the 8-row file for copy-up at --accept |
| M2 | rows placed in completion order (`out[out.index(None)] = row`) | RUN-Z, RUN-B | not caught (two rows; completion order equals manifest order) |
| M3 | RPT cause "absent" never set | RPT-Z, B1, B2, H1 (11) | **not caught** |
| M4 | RPT exemption branch removed | same | **not caught** (no Z on the exempt path; the live S1 r7 / S2 r5 runs would go red, and no control runs them) |
| M5 | Reported items table removed from write_summary | same | **not caught** |
| M6 | RPT no longer appended in run_sketch | H1 (11), S1-FULL, S2-FULL | **not caught** |
| M7 | --accept "RPT absent" branch removed | H1 (11) | caught: H1-B8 |
| M8 | `K_CHECKS` override in k_checks removed | H1, S1-FULL | not caught (no sketch defines K_CHECKS; no control calls run_sketch) |
| M9 | `SKETCH_CHECK` pinned to `^S([12])-` | S1-1-Z, S1-2-B1, S2-1-Z | not caught (no S3 check exists yet) |
| M10 | K5 zero-area Polygon branch off (`if area <= TOL_AREA` to `if False`) | K5-B19, K5-Z2, K5-Z3 | **not caught** (K5-B19 plants a Rectangle) |
| M11 | RPT treats `value: None` as present | RPT-Z, B1, B2 | not caught (RPT-B1 omits the key) |

By inspection: the K2 expr branches "does not evaluate" and "non-numeric" have no B. Deleting either lets the exception escape to `safe()`, which reports K2 as an error, and an error fails closed. NOTE. RPT spec-error branches (duplicate id, missing field) have no B; if deleted, a malformed entry raises KeyError inside `safe()`, also an error. NOTE.

## 4 SHA-256 of committed files (task 4)

57 committed files under `docs/sketches/` (wip/ and __pycache__ excluded). Before my first run they equal P0 `sha_after.txt` (MEASURED). After my last run: 57 files, 0 differences from my before list (`diff` empty). No `__pycache__` or wip/ file written in the committed tree by me (all runs in scratchpad copies).

## 5 Simplicity gate (task 5)

- R1: about 60 lines: a spawn pool, `imap_unordered` with chunk 1, rows put back by index, figures built once in the main process. That is the least code that does the job. `--manifest` exists only so RUN-Z and RUN-B can run. It is small, and it is the only way to test the runner end to end. PASS. With 12 workers each control runs about 1.5 times slower (1213 s summed against about 800 s serial) because they share memory bandwidth. Still a 7x wall gain (819.6 s to 117.5 s).
- R3: `rpt_check` is about 35 lines, plus the summary table and one --accept condition. The exemption is a two-entry dict keyed on record name. PASS. FIX 2 makes it simpler: "every record carries an RPT row" replaces "a record that declares reported_items carries an RPT row".
- R4: the regex routing is a one-line change and correct. The `K_CHECKS` override in `k_checks()` has no user and no control. K_BY_SKETCH already covers a reduced K list (s5). That makes it ceremony until S3 needs it. Drop it, or keep it and give it a control at S3 (c) when checks_s3.py defines one (NOTE 3).

## 6 Findings

**FIX 1 (R1 c, partial-run rule).** The live code keeps a partial run away from the record. No control guards that: with M1, `--only` overwrites `wip/fixtures/controls_results.json`, control_tally reads the subset, and --accept would copy it up as the controls record, while RUN-Z, RUN-B and all H1 stay matched. Also, an `--only` that selects nothing exits 0. Fix: move the destination decision into a pure function `controls_dst(man_path, only)`, returning CONTROLS_RESULTS, CONTROLS_PARTIAL or "beside the manifest", and call it from `controls()`. Z: the full live manifest gives CONTROLS_RESULTS. B: `only` set on the live manifest gives CONTROLS_PARTIAL; the control fires when the function returns CONTROLS_RESULTS. Also: zero rows selected means exit 1 with "no control selected", plus one B. Show each B red with the `not only` deleted.

**FIX 2 (R3, --accept through RPT).** `--accept` takes a record with no RPT row when it declares no reported_items. I tried it: an s3 record, rc 0. Deleting the RPT call in `run_sketch` (M6) passes every control. Fix: `--accept` refuses any record without an RPT row ("RPT absent"). Every record written by the current `run_sketch` has one, and s1 r7 and s2 r5 carry the exempt row once refreshed. `_template()` in step0_fixtures.py gains an RPT pass row so H1-Z1 to Z3 stay clean. Re-plant H1-B8 as a record with no RPT row and no reported_items. Show it red on the current condition. This also closes Engineer open item 2.

**FIX 3 (R3, RPT branches and the summary table).** R3 asks for "cause absent on rev 0", the exemption and the Reported items table. None of them has a control (M3, M4, M5, M11). Fixtures, all through `rpt_check` / `write_summary`, no drawing:
- RPT-B3: rev 0 with F_stall missing. The fixture fires only when cause is "absent", and puts the cause in the reason (substring "cause absent").
- RPT-B4: rev 0 with L_min (needs_drawing false) missing. Cause "content".
- RPT-B5: F_stall `value: None`.
- RPT-Z2: no items under record name s1_checks_r7.json gives pass with "exempt".
- RPT-Z3 / RPT-B6: `write_summary` on a temporary record declaring two items. Z: the "Reported items" table has two rows with the values. B: one value missing makes that row read ABSENT.

Each one red under the matching M mutation.

**FIX 4 (R5 a, TP1.1-9 Polygon branch).** The lint as written covers "Polygon area <= 0.01 mm²". K5-B19 plants only a Rectangle, and turning the Polygon branch off (M10) passes K5-B19, K5-Z2 and K5-Z3. Fix: K5-B20, a degenerate Polygon (collinear vertices) on a cylinder row, reason "zero-area Polygon", red under M10. I raise this here under task 3. The Topologist owns the rule at P0T.

NOTE 1 (R1). Rows are put back by index (M2) and nothing checks it beyond the 246-row equality runs. A one-line assertion in `controls()` (`[r["id"] for r in rows] == [e["id"] for e in man]`) fails closed and costs nothing. `--jobs 0` silently means 12: reject values < 1.

NOTE 2 (R3). RPT passes a value of "" and a missing basis or tag. The summary then prints ABSENT in the Tag column under a green RPT. The style rule tags every number. Consider failing a tag outside MEASURED, DERIVED, DECLARED, ASSUMED. When `reported()` raises, RPT reports "no value" for every item with no exception text. Carry `rd["reason"]` into the RPT reason.

NOTE 3 (R4). `K_CHECKS` (M8) and the `S<n>-` routing for n > 2 (M9) are untested until checks_s3.py exists. The first S3-x control at (c) exercises the routing. K_CHECKS: drop it, or give it a control in the same revision that uses it. One more place for the R4 list: `run_sketch` builds one `Ctx` with `view=spec["view"]`. S3 is a section plus a plan inset (TP-7), so it needs a per-Axes view there. Add that to the S3 (c) items next to VIEW_NORMAL and SIDE_VIEWS.

NOTE 4 (R2). The K2 expr error branches (does not evaluate, non-numeric) and the RPT spec-error branches have no B. Deleting any of them turns the check into an error, which fails closed. Mandatory expr on the three chain leaves is not enforced (Engineer open item 3). That is the Loftsman's call at P0L.

NOTE 5 (process). `--controls` has no output-location option. With three agents on one tree, concurrent runs overwrite `wip/fixtures/controls_results.json` and figs. That matters at accept, since `harness_outputs` copies whatever the last run left. Either serialise runs of record through the orchestrator, or give `--controls` a `--wip-dir`. A copy of the tree works today (this check).

## Gameplan lines to change

none. The FIX closures carry their lines at P0f. Hold the Engineer's proposed l.124 text ("refuses a record declaring reported_items without an RPT row") until FIX 2 lands, since FIX 2 changes that clause to "refuses a record without an RPT row".
