# Step 1.3 step 0 (P0S re-check) Software Engineer: FIX 1 to 4 against the P0f code

Verdict: **FIX (1 item).** FIX 1 to 4 are closed as written. All 7 re-run mutations are stopped: 6 by a named control, and M6 (no RPT row written) by `--accept`, which H1-B8 guards. The full set reads 261/261 in a scratchpad copy. One new branch has no control and guards a rule the gameplan text names: the Annulus radial-width branch of `least_thickness` (mutation MA, below). A 0.01 mm annulus wall passes K5 with that branch deleted. That is FIX R1. The `controls_dst` call site has no control either (M1b). That is NOTE 1.

## Corrections to the brief

1. M10 in my P0S file was "Polygon branch off" in a K5 that had its own Polygon area test. P0f replaced that test with one thickness test (2A/P) for every Patch, so there is no Polygon branch left to delete. I re-ran M10 as the closest equivalent: insert `if type(a).__name__ == "Polygon": return None` before the thickness test. This is the Engineer's "Polygon skipped by the thickness test".
2. M1 was "`record = not only and …`". P0f moved that logic into `controls_dst`, so M1 is now `if live and not only:` becoming `if live:`, as the Engineer states. The same hazard can also be reached at the call site (`controls_dst(man_path, only)` becoming `controls_dst(man_path, None)`). I ran that as M1b.
3. The brief counts M6 among the mutations to show "caught by a named control". No control calls `run_sketch`, so no control catches M6, as the Engineer's section 5 says. M6 is stopped at `--accept`: the refusal "RPT absent" is guarded by H1-B8. I ran it end to end (section 3).
4. `zero_area_issue`'s docstring (sketch_common.py l.1625) still describes the P0 rule ("Polygon of area <= TOL_AREA (0.01 mm2)"). The code applies the thickness rule. NOTE 3.

Tags: runs MEASURED 2026-11-26, in scratchpad copies `rc/runs/<name>/sk` with `params.yaml` one level up. Hand reasoning DERIVED.

## 1 FIX 1 to 4 in docs/sketches/ (read and run)

| Item | Asked (P0S) | Found | Controls |
|---|---|---|---|
| FIX 1 | pure `controls_dst`, Z and B; empty `--only` exits 1 | `controls_dst(man_path, only)` (check_sketch.py l.349) returns record / partial / other. `controls()` calls it (l.390). An empty selection prints "no control selected" and returns 1 before writing (l.368 to 371). Also from NOTE 1: `--jobs` < 1 exits 2, and rows out of manifest order exit 1. | RUN-Z2, RUN-B2, RUN-B3 |
| FIX 2 | `--accept` refuses any record without an RPT row; RPT row in the H1 template; H1-B8 re-planted | l.682 to 683: "RPT absent" whenever no row has id RPT. `_template()` adds an RPT pass row. `h1_b_rpt_absent` removes the RPT row and `reported_items`. | H1-B8; H1-Z1 to Z3 clean |
| FIX 3 | RPT-B3 to B5, RPT-Z2, RPT-Z3, RPT-B6 | The RPT reason ends "; cause <cause>". All six rows are in manifest.yaml l.341 to 346 and their fixtures are in step0_fixtures.py. | as named |
| FIX 4 | degenerate Polygon B | K5-B23: collinear 3-vertex Polygon under drill_tube. Reason "zero-area Polygon (least thickness 0.0000 … on a cylinder row (TP1.1-9)". | K5-B23 |

Runs (MEASURED):

| Run | Result | Wall |
|---|---|---|
| unmutated copy, `--controls --only` RUN, RPT, H1, K5 set (32 controls, jobs 8) | 32/32 match | 12.5 s |
| unmutated copy, `--controls` (full, default jobs 12) | Z 70/70, B 189/189, smoke 2/2, exit 0, 0 "match NO" | 113.3 s (machine shared with other agents) |
| H1-B8 on the P0 condition (`if rec.get("reported_items") and not any(...RPT...)`, M13p) | H1-B8 mismatch: record accepted | |

H1-B8 is red on the condition it replaced.

## 2 Mutations re-run against the P0f code

Each mutation was applied to a fresh copy (one exact-string replacement, count asserted 1), then `--controls --only <set> --jobs 8` was run in that copy. "Caught" means at least one control mismatches. Sets: RUN = RUN-Z, RUN-B, RUN-Z2, RUN-B2, RUN-B3; RPT = RPT-Z, Z2, Z3, B1 to B6, H1-B7, H1-B8; H1 = H1-*; K5 = K5-Z2, Z3, B19 to B23.

| ID | Mutation (P0f code) | Set | Result (MEASURED) | Caught by |
|---|---|---|---|---|
| M1 | `controls_dst`: `if live and not only:` to `if live:` | RUN | exit 1. RUN-B2 reads "routes to record fixtures/controls_results.json". The `--only` run itself wrote `controls_results.json` in the copy. | **RUN-B2** |
| M3 | cause "absent" never set | RPT | RPT-B3 reason "…; cause content", lacks "cause absent" | **RPT-B3** |
| M4 | `if rec_name in RPT_EXEMPT:` to `if False:` | RPT | RPT-Z2 fires: "spec declares no reported_items (s1_checks_r7.json is not a record accepted before RPT)" | **RPT-Z2** |
| M5 | Reported items table off (`if rec.get("reported_items"):` to `if False:`) | RPT | RPT-Z3 fires "no Reported items table". RPT-B6 reads "no row". | **RPT-Z3, RPT-B6** |
| M6 | RPT row not appended in `run_sketch` | H1 + RPT (20) | 20/20 match, not caught by a control. End to end (section 3): `--accept` refuses "RPT absent". | none; stopped at `--accept` (H1-B8 guards the refusal) |
| M10 | Polygon returns before the thickness test | K5 | K5-B23 reason is "cylinder axis Z in side_xz drawn as polygon, needs rectangle", which lacks the zero-area substring | **K5-B23** |
| M11 | `v.get("value") is None` to `"value" not in v` | RPT | RPT-B5 reads "2 reported item(s) declared, every one has a value" | **RPT-B5** |

**Caught by a named control: 6 of 7.** M6 is the seventh. It is stopped by the H1-B8-guarded refusal. Extra mutations on the new P0f branches:

| ID | Mutation | Set | Result |
|---|---|---|---|
| M12 | empty-`--only` guard off (`if not man:` to `if False:`) | RUN | caught: RUN-B3 reads "exit 0 … partial file written" |
| M13 | `--accept` RPT-row condition off | H1 | caught: H1-B8 accepted and copied |
| M13p | P0 condition restored (reported_items required) | H1 | caught: H1-B8 |
| **M1b** | `controls()` calls `controls_dst(man_path, None)` | RUN | **not caught**, 5/5 match. The `--only` run wrote `wip/fixtures/controls_results.json` (5 rows). That file is the one `control_tally()` and `--accept` read. |
| **MA** | `least_thickness` Annulus branch off (`if isinstance(a, Annulus) and len(polys) >= 2:` to `if False:`) | K5 | **not caught**, 7/7 match |

MA probe (direct call, `Annulus((0,0), 150, w)` on a cylinder row, MEASURED):

| Width w (mm) | P0f code: least thickness, K5 | MA: least thickness, K5 |
|---|---|---|
| 0.01 | 0.0100, fires "zero-area Annulus (least thickness 0.0100 mm <= 0.05)" | 149.9448, passes |
| 0.04 | 0.0400, fires | 149.9148, passes |
| 0.06 | 0.0600, passes | 149.8948, passes |
| 5.0 | 5.0000, passes | 144.9563, passes |

Without the branch, each ring is taken as a filled disk, and its 2A/P comes out close to the radius (DERIVED: 2πr²/2πr = r). Any annulus wall therefore passes. K5-Z3 runs the drill_tube annulus only on its pass side. K5-B21 plants a Circle. No B plants a thin Annulus.

## 3 M6 end to end (copy `runs/M6/sk`)

| Step | Result (MEASURED) |
|---|---|
| `check_sketch.py s2 --rev 5` with RPT append deleted | exit 0, 31.9 s; the record's last checks are S2-5b, S2-6, X1 (no RPT) |
| `check_sketch.py --accept s2 --rev 5 --note "probe M6"` | "refused: s2_checks_r5.json has checks not pass: RPT absent", exit 1; the copy's docs `s2_checks_r5.json` is unchanged (SHA-256 bce3a5ae03272566 before and after) |

A run with this defect cannot reach docs/. Giving `run_sketch` its own control would mean a full sketch draw inside the controls set (S1-FULL already costs about 30 s). That is ceremony for one line whose failure `--accept` stops.

## 4 New branches with no control

| Branch | If deleted | Rating |
|---|---|---|
| `least_thickness` Annulus radial width (sketch_common.py l.1648) | thin annulus wall passes K5 (MA). The proposed gameplan l.139 names "Annulus: radial width". | **FIX R1** |
| `controls_dst` call in `controls()` | `--only` overwrites the controls record (M1b) | NOTE 1 |
| `--jobs` < 1 exits 2 | `--jobs 0` runs serially, which is harmless | NOTE 2 |
| rows-in-manifest-order assertion | M2 from P0S becomes undetected again. The assertion fails closed. | NOTE 2 |
| `least_thickness`: piece with < 3 vertices or no piece gives 0 | the area of a 2-point piece is 0, so 2A/P is 0 anyway. With no piece, `min([])` raises inside `safe()`, an error that fails closed. | none |

The non-Patch clause (K5-B22, Engineer M15) and EXPR_REQUIRED (K2-B6, K2-B7, Engineer M14) have B controls. Their rules belong to the Topologist and the Loftsman.

## 5 Findings

**FIX R1 (R5 a, Annulus branch).** Add K5-B24: S2 fixture (as K5-B21), drill_tube drawn as an `Annulus` with wall width 0.01. Reason substrings "zero-area Annulus (least thickness 0.0100", "on a cylinder row (TP1.1-9)". It must be red under MA (the branch condition set to `False`). One builder, one manifest row. No check logic changes. The Topologist owns the threshold; this adds only the control. Controls become 262 (Z 70, B 190, smoke 2).

NOTE 1 (R1 c). The `controls_dst` call site is the one line that turns the rule into a write, and no control covers it (M1b). This is a residue of my P0S FIX 1, which asked only for Z and B on the function. A pass-through call is a low-probability regression. When the runner is next touched, an in-process fixture can cover it: set `cs.MANIFEST` to a temporary one-row manifest (K1-Z), point `cs.output_path` at a temporary directory, call `cs.controls(only="K1-Z", jobs=1)`, then assert the partial file exists and the record does not. Each control runs in its own pool worker, so patching module state touches no other control. Not blocking.

NOTE 2 (R1). The `--jobs` < 1 guard and the row-order assertion have no B. Both fail closed. They need no control.

NOTE 3 (doc). The `zero_area_issue` docstring states the P0 rule (Rectangle zero side, Polygon area <= 0.01 mm²). It should state the thickness rule (least 2A/P, Annulus radial width, <= TOL_Z 0.05 mm) and the non-Patch clause. Change it with FIX R1.

Carried from P0S, unchanged: NOTE 2 (tag vocabulary, `reported()` exception text into RPT), NOTE 3 (`K_CHECKS` control and per-Axes view at S3 (c)), NOTE 5 (serialise runs of record). The Engineer's section 9 lists them.

## 6 SHA-256

57 committed files under `docs/sketches/` (wip/ and __pycache__ excluded). The first-run baseline equals the Engineer's P0f after-hashes for the 5 changed files (check_sketch.py 72d126d68bde081f, builders.py 47eb9356aec759be, manifest.yaml 591de03b2e9a23eb, step0_fixtures.py b11457a84fe01921, sketch_common.py 79f7f8de9577994e). After the last run: 0 differences on all 57. No file of mine was written under `docs/sketches/`.

## Gameplan lines to change

**l.124: the Engineer's held RPT clause is released.** FIX 2 landed in the form P0S asked for, and H1-B8 is red on the P0 condition (M13p). Apply both of the Engineer's l.124 changes as written in `step1.3_engineer_step0_fixes.md`. Both Old fragments occur once in the current gameplan (MEASURED):
Old: `` `--accept` refuses through RPT and refuses a record declaring reported_items without an RPT row (RPT-Z, RPT-B1, RPT-B2, H1-B7, H1-B8; 1.3 open O10).``
New: `` `--accept` refuses through RPT and refuses any record without an RPT row; the RPT reason states its cause (RPT-Z, RPT-Z2, RPT-Z3, RPT-B1 to RPT-B6, H1-B7, H1-B8; 1.3 open O10; Software Engineer P0S FIX 2, FIX 3).``
and the Engineer's `--only` change (Old `` `--only <id globs or check ids>` writes `wip/fixtures/controls_results_partial.json`, "PARTIAL, not a record", never read by control_tally or `--accept`; runs of record use the full set.``) as written.

**l.139 and l.146: hold** until FIX R1 lands. Then the Engineer's l.139 K5 control-list New text gains, at its end before ` |`: `; K5-B24 S2 drill tube Annulus wall 0.01 (Software Engineer P0S re-check FIX R1)`, and the l.146 P0f sentence reads `K5-B20 to B24` and `262 controls: Z 70, B 190, smoke 2`. The Engineer's closure file carries the exact final texts.

All other Engineer P0f lines (l.136, l.665, l.666, l.732): no objection; outside this check.
