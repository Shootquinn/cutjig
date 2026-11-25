# Step 1.1 (c) Software Engineer check of the S1-x fixtures (H6)

Verdict: FIX (1 item). The fourteen new controls are real. Each Z is the signed spec drawn faithfully, and each B plants one plausible defect and fires on its reason with its planted count. One branch of S1-2, the load pose, has no B. FIX 1 is a two-line fixture addition with no change to the check or the spec, and it can ride with P6.

## Corrections to the brief

1. The P4 text for S1-2 B (park at `upper.park_z` 959.84) and for S1-3 B (`park_tip - load_clearance - 1`) is void under option R. Those are my own SW-10 values. The Engineer's replacements are the correct reading of SW-10 on the signed rule (section 2).
2. l.144 lags the manifest by 30 controls, not 14: sixteen came in at 1.1 (b) and fourteen at 1.1 (c). Replacement text for all thirty is given in section 6.

Tags: run results MEASURED 2026-11-25; hand values DERIVED.

## 1. Re-runs against the Engineer's counts

| Command | Exit | Mine (MEASURED) | Engineer | Same |
|---|---|---|---|---|
| `check_sketch.py --controls` | 0 | 98 controls: Z clean 30/30, B fired 67/67, smoke 1/1; 88.0 s | 30/30, 67/67, 1/1; 91.3 s | yes |
| `check_sketch.py s1 --rev 0` (stub, signed spec) | 1 | 4 pass (K1, K2, K3, K5 guards); K4, K9 red content; K6, K7, K8, S1-1 to S1-7 red absent | 4 green, 13 red, same causes | yes |
| s1_checks_r0.json against baseline_red.json run 2 | | 17/17 match, cause labels included; prior 1.0 record kept under `prior["2026-11-24T23:26:11 (spec draft, unsigned)"]` | 17/17 | yes |

My runs rewrote controls_results.json, s1_checks_r0.json and s1_summary_r0.md. The content is the same; only the timestamps changed. baseline_red.json was not rewritten.

## 2. Per-fixture verdict (task 1, 2)

| ID | Z is the signed spec | B defect plausible | Fires on reason, planted count | Verdict |
|---|---|---|---|---|
| S1-1 | s1_live, 650.00 on the upper bound 650 (margin 0.00, inside TOL) | B1 is the gameplan B: `upper.travel_max` 500. The band [534.93, 500] is empty, but 650 >= 534.93 holds, so B1 exercises the high bound alone. B2 exercises the low bound: start 1 below capture_end + advance gives 533.93 | 1/1, 1/1 | real |
| S1-2 | s1_live, +125.00 | B1: park at the top of travel (stroke conflated with travel, SE-3). Hand: 184.84 + 650 = 834.84 z_A = 894.84 z_S, margin 0.00 | 1/1 | real; load branch uncovered (FIX 1) |
| S1-3 | s1_live, 367.34 / 117.34 | B1: park 42.50 + 750 + 50 - 1 = 841.50 z_A, margin 841.50 - 50 - 792.50 = -1.00. This is the boundary of a park rule that reads the core stop with no margin | 1/1 | real |
| S1-4 | S1-4-Z from (b), 0.84 | B1 (b): guides 20 low. B2: nut and housing at guide_a top + 100 at park, 1325 against hi 1170, margin -155.00. B2 is a drawing-only defect and is the gameplan l.231 B | 4/4, 1/1 | real |
| S1-5a | s1_live, 192.34 against 25 | B1: bore ceiling 1 below the advance. Hand: 184.84 + 533.93 - 792.50 = -73.73 | 1/1 | real |
| S1-5b | S1-5b-Z from (b), 77 pairs, 142.00 | B1 (b): collar 133 high, bearing 9 above the collar top against g_min 10 | 1/1 | real; gameplan B text wrong (section 6) |
| S1-6 | s1_live, 8 projections | B1: screw_b at x = r = 160 against r cos 30 = 138.56, all four poses. Drawing-only | 4/4 | real |
| S1-7 | s1_live, 607.66 against 534.93, spare 72.73 | B1: core_750 row drawn core.length_capture long (the G2 defect). Hand: 42.50 + 500 - 184.84 = 357.66, short 177.27 | 1/1 | real |

Every B lists its reason substrings. Entries with no `planted` field take the default 1 in `compare()` (check_sketch.py l.118), which equals the observed count.

**SW-10:** applied as I specified it in substance. S1-2-B1 and S1-3-B1 mutate the spec park `tip_z` through `_pose_tip` and draw the mutated spec faithfully, so the drawn tip agrees with check_stack and the check fires on the park rule, not on a `_tip` disagreement. The values differ from my 1.0 text because option R moved the live park to 959.84, which passes. The replacements fire at margins 0.00 and -1.00, the tightest boundary each check has.

## 3. LF-16 controls (task 3)

| ID | Expected | Observed | Reason substrings |
|---|---|---|---|
| K6-Z3 | clean | clean | live load_plane (core_stop, core_seat z_max) and entry_plane (collar_top, collar z_max) agree within 0.05 |
| K6-B5 | fires | fires, 1/1 | "LF-16 load_plane", "term core_stop 42.50", "wingnut.z_max", "117.34 apart" |
| K6-B6 | fires | fires, 1/1 | "LF-16 entry_plane", "term collar_top 159.84", "core_seat.z_max", "117.34 apart" |

Each B is matched on the plane it names, both z values and the 117.34 separation, not on exit code alone.

## 4. Checks that cannot fail through the drawing (task 5)

| Check | Through the drawing? | Evidence (MEASURED probe) | Stays? |
|---|---|---|---|
| S1-1 | No. `_tip` forces both drawn tips onto check_stack, so a tip drawn wrong is a `_tip` content red, never a reach red | start drill_head drawn 1 high: "drawn tip 895.84 in start differs from check_stack 894.84 z_S" | Stays under the SW-10 rule. It guards the travel-against-advance decision, and its Bs mutate params (B1) and the spec (B2). New member of the SW-10 class |
| S1-2, S1-3 | No (SW-10) | as at 1.0 | Stay |
| S1-6 depth half | No (SW-12) | reads the stack depth | Stays |
| S1-4, S1-5a, S1-5b, S1-6 x half | Yes | B2, B1 and B1 are drawing-only, or the drawn extents are measured | — |
| S1-7 | Yes | capture core drawn 73.73 short at start, spec unchanged: "533.93 mm, need 534.93 (short 1.00)" | — |

## 5. Findings

**FIX 1 (S1-2 load branch has no B).** `s1_2` tests the park and load poses (checks_s1.py l.81). Every S1-2 B mutates park only, so a version of s1_2 with "load" deleted passes all 98 controls. The load tip guards a real decision: S1-3 reads park only and K6 compares drawn against spec, so a spec with the load `tip_z` set below the park would go unflagged except by this branch. Probe (MEASURED): `_s1_ctx(spec_mut=_pose_tip("load", "start_tip_max"))` fires 1 issue, "load: drawn tip 894.84 not above the highest class start 894.84 z_S". Required change:
- builders.py: `def s1_2_b2(): return _s1_ctx(spec_mut=_pose_tip("load", "start_tip_max"))`
- manifest.yaml: `S1-2-B2`, check S1-2, B, reason `["load: drawn tip 894.84 not above the highest class start 894.84"]`, planted 1, finding "H6; SW 1.1 (c) FIX 1", gameplan_line 229
- Re-run `--controls`; expect 99 controls, B 68/68, Z 30/30, smoke 1/1. baseline_red.json run 1 is rebuilt; run 2 is unchanged.

No check or spec change is needed. It can be closed in the first P6 edit; the drawing does not need to wait for it.

**NOTE 1 (S1-5b does not set the N1 lower bound on the signed values).** Gameplan l.233 says S1-5b "sets the lower bound of N1". On the signed values the least clearance is 142.00 at ring.position_above_tip 130. Lowering the ring the 132 needed to reach g_min puts it at -2, below the tip. So K8 ring_on_tube binds first. This is reported, and no control is affected. The l.233 text change in section 6 covers the B column only. Whether the Check column text stays is the orchestrator's call.

**NOTE 2 (S1-1 Z on its bound).** S1-1 passes at margin 0.00 by construction (start = stop + travel_max). A drawn or spec start 0.06 high fires. This is accepted; Sean confirmed the pose table.

## 6. Gameplan text for the orchestrator

**l.233, S1-5b row, B column.** Replace
`` `ring.position` at the drill's lower third ``
with
`Collar drawn 133 high at end of capture: bearing bottom 9 above the collar top against g_min 10 (S1-5b-B1). The lower-third ring (266.67 above the tip) sits above the signed 130 and cannot fire (least clearance 278.67, MEASURED 1.1 (c))`

**l.144, control pointer.** Replace the whole line with:
`The K table lists the controls the gameplan requires. The Step 1.0 revision added K3-B7, K4-B3, K5-B4, K5-B5, K6-Z2, K6-B4, K7-Z5 to Z7, K7-B7 to B10, K8-Z2, K8-B4 to B11, K9-B3, K9-B4 and the smoke control S1-FULL. Step 1.1 (b) added K6-Z3, K6-B5, K6-B6 (LF-16), K7-Z8, K7-Z9, K7-Z10, K7-B11, K7-B12, K7-B13, K8-Z3, K8-B12, K8-B13, S1-4-Z, S1-4-B1, S1-5b-Z and S1-5b-B1. Step 1.1 (c) added the S1-x fixtures from the signed spec (H6): S1-1-Z, S1-1-B1, S1-1-B2, S1-2-Z, S1-2-B1, S1-3-Z, S1-3-B1, S1-4-B2, S1-5a-Z, S1-5a-B1, S1-6-Z, S1-6-B1, S1-7-Z and S1-7-B1 (98 controls: Z 30, B 67, smoke 1). `research/sean/cr_scratch/sketches/fixtures/manifest.yaml` is the executable record of every control, with reason substrings and planted issue counts.`
If FIX 1 lands, insert `S1-2-B2` after `S1-2-B1` and change the count to `(99 controls: Z 30, B 68, smoke 1)`.

**l.229, S1-2 row, B column (only if FIX 1 lands).** Append: `; the load pose at the top of travel (S1-2-B2)`.

**Design Notes 20, H6 and SW-10 rows.** H6 is checked at 1.1 (c) by the Software Engineer, with FIX 1. SW-10 is applied with the option R replacement values (S1-2-B1 margin 0.00, S1-3-B1 margin -1.00). S1-1 joins the SW-10 class: it cannot fail through the drawing, and it stays.

FIX (1 item: FIX 1).
