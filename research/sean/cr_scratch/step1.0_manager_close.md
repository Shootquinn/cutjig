# Step 1.0 Manager Close (sean)

Date: 2026-11-24. Verdict: **READY FOR SEAN.** D1 to D11 met. Seven gate decisions in section 3. Commits: 903755f (batch 1, DN17-19), baf3dbc (Wave 1b), 24e45cd (Wave 2), 7860c63 (revision), 6fb76bc (re-checks). No shared design file (params.yaml, ASSEMBLY.md, tests/, research/quinn/) changed in 903755f..6fb76bc.

## 1. Verification (MEASURED by the Manager, 2026-11-24, Python 3.12)

| # | Criterion | Evidence | Result |
|---|---|---|---|
| D1 | Q3-0 red-first, Z, B | `step3_check.py --batch` on step3_fixtures: empty exit 1 "table has no rows"; Z exit 0 PASS; B exit 1 "line 6 row 'B2': blank standin". Recorded in step3_check_q30_results.json | met |
| D2 | Batch 1 | step1_quinn_batch1.md, 17 rows: Q2a-e, Q9, DN23-a to -e, N5 to N10; Q3-0 exit 0 PASS. Approved by Sean as drafted (Design Notes 19), pushed in 903755f | met |
| D3 | Overlay | sketches/proposed_params.yaml namespaces jig, drill, ring, bearing, guide, gear, pinion, jackscrew, liftmotor, hold, frame_upper; K2 on the live overlay: 138 spec keys resolve, 81 leaves sourced, no shadow. Stand-in equality checked by the Software Engineer (review item 4) | met |
| D4 | sketch_common.py | loader (sketch_loader.py, re-exported), setup_figure, draw with gid, K1 to K9; K3 green on the stub "one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi 150" | met |
| D5 | check_stack.py imports | stdlib (argparse, ast, json, math, sys, pathlib) plus `sketch_loader` only; K6-B3 fires | met |
| D6 | check_sketch.py outputs, --stale | s1_checks_r0.json carries files_sha256, keys_read, per-check result, measured, threshold, z_result, b_result, source; s1_summary_r0.md written. `--stale` live: 0 records, 0 differences, exit 0; planted `ring.thickness` 13 fires (signoff section 1) | met |
| D7 | Fixtures and manifest | manifest.yaml; `--controls` exit 0: **Z clean 17/17, B fired 50/50, smoke 1/1**, 0 rows "match no", 41.3 s. All 41 Wave 1b controls (12 Z, 29 B incl. K6-B2b) present with the same outcome | met (superset) |
| D8 | Stub, draft spec, S1 checks | stubs/s1_stub.py; s1_spec.yaml line 2 `status: draft, unsigned`; checks_s1.py S1-1 to S1-6 (S1-5a, S1-5b) measure drawn patches by gid | met |
| D9 | Red-first baseline | baseline_red.json. Run 1 as D7. Run 2 `check_sketch.py s1 --rev 0`, 3.3 s: K1, K2, K3, K5 green (guard); K4, K9 red (content); K6, K7, K8, S1-1 to S1-6 red (absent, fail-closed); **16/16** against baseline run 2, cause labels included. No red from a missing file | met |
| D10 | Software Engineer signature | step1.0_software_engineer_signoff.md: "SIGNED (harness, fixture run, S1 stub run, step3_check.py Q3-0)"; SW-1 to SW-9 closed. Loftsman re-check: CROSS-REVIEW PASS. Topologist re-check: CROSS-REVIEW PASS | met |
| D11 | Gates | No visual gate. Human gate: Sean approved the batch (Design Notes 19) | met |

Re-runs rewrote controls_results.json, s1_checks_r0.json and s1_summary_r0.md; each diff is one timestamp line.

Sequencing check (details 1.1 to 1.6, recurring defect class): detail 1 common (c) ran the stub before any step wrote the sketch's own Z and B fixtures ("fixture from the spec"). Fixed: (c) now writes and runs them first. S3-3 at 1.3 (S6 segment declared), X2-3 before S5, and the 1.1 reviewer control figures (ctrl_a, ctrl_b exist) are in order.

Process note: the Engineer edited gameplan l.140 at revision (LF-1 rule); the open reserved the gameplan to the orchestrator and Manager. One-off. The wording is correct and stays, subject to G6.

## 2. Carried items

Every item has a step and an owner in gameplan Design Notes 20, with pointer lines in details 1.1, 1.2, 1.3 and 4a.

| Item | Ruling |
|---|---|
| LF-17 | Fixed: K7 swept wording now "per convex piece, the hull of that piece at the lowest and highest pose" |
| SW-19 | Fixed: line under the K table names the added controls and makes manifest.yaml the executable record |
| SW-18 | 1.1 (d), The Engineer: K1 scans `s1_side_poses.py`; no harness change |
| LF-16 | 1.1 (b), The Engineer: lint that `load_plane` term and feature edge agree within 0.05 mm, with a B control; The Loftsman signs the spec |
| TP-9 | 1.1 (a)/(b), The Designer: core_750 load z_rule; reword or replace the rubric line "ring above the core in every pose" (false at capture_end: ring bottom 384.84, core top 542.5 z_A) |
| TP-7 | 1.3 (S3) before the stub run, The Engineer: K3 to K9 iterate over declared inset Axes, B control; The Topologist verifies at (e) |
| Engineer list (harness notes section 8, revision notes section 6) | Lift fit, core stop, tapers, radial geometry, smoke clashes and N declarations to 1.1 (a)/(b) (Designer, Engineer); S1-x fixtures and SW-10 to 1.1 (c); height margin reported at 1.1; control figures at 1.1 (f); placeholders, box test (LF-8), SW-17, TP-13 to 1.2 (S2); LF-13 to 4a |

Other close edits to the gameplan: K6 row rewritten to the Design Notes 17 frame (B2 60 mm low, B2b 100 mm low); Design Notes 14 depth-band bullet marked superseded; Design Notes 18 and 19 put in order; Open Questions row N10; Echo Site Registry row for datum A 60 mm above the floor.

## 3. Decisions for Sean at this gate

**G1. Park-rule load plane.** The park rule and S1-3 need the height the install core stands on: the collet core stop (42.5 z_A, where the core physically sits) or the collar top (159.84 z_A, the plane params `upper.park_z` uses). They give the same park tip for 0.5 and 0.75 m cores (1015 z_A) and differ by 117.34 mm for a 1 m core (1092.5 against 1209.84). *Team recommendation: core_stop; the core stands on it.*

**G2. Start pose 292.34 mm gap.** With the 0.5 m core on the 42.5 stop, the start tip (834.84 z_A) is 292.34 mm above the core top, and at end of travel the cutter has gone only 357.66 mm past the core top against the 534.93 mm advance: a 500 mm capture from a 0.5 m core falls 177.27 mm short. On the 0.75 m install core (top 792.5 z_A) the same travel completes the capture with 72.73 mm to spare (DERIVED). The core seat (2.5 mm ASSUMED) cannot move a 292 mm gap, and the advance (500 plus 34.93) matches a 500 mm capture. *Team recommendation: the pose wording is wrong. Reword start to "top of the 650 mm travel" (params define start by travel). Sean confirms that the 500 mm capture is cut from the 0.75 m install core; the pose table then draws that core at start and end of capture. The Designer adds a capture-reach check from the drawn core top at 1.1 (b). If the capture comes from a 0.5 m core, the core must sit about 177 mm higher (push-pop, S4 and Q4), and the advance basis goes to Quinn.*

**G3. The draft overlay does not fit the lift.** Lift stroke (park to lowest stop) is 830.16 mm with 0.75 m cores supported (700.00 mm with 0.5 m only, DERIVED), against 650 mm travel. On the draft ring position and 900 mm screws the nut leaves the usable screw band (S1-4 red), and the screw anchors sit inside the base plate. *Team recommendation: keep stroke distinct from travel, as designed (SE-3). At 1.1 (a) the Designer sets ring position, anchor height and screw length so S1-4 passes, and S1 reports screw length per Q9 option for Quinn's Q9 answer.*

**G4. Core stop has no params key.** 42.5 z_A is derived from the receiver floor (40) plus `collet.core_seat_height` 2.5, assuming the collet foot sits on the receiver floor. *Team recommendation: the Designer confirms it at 1.1 (a), it becomes overlay leaf `collet.core_stop_z` (ASSUMED), and it goes on the Step 4a list for promotion.*

**G5. K7 depth-band rule changed (LF-1).** Disjoint depth bands now pass only class F pairs. A contact pair fails when its bands are more than 0.05 mm apart, and a gap pair passes only on max(band gap, XZ distance) ≥ g_min. The Engineer wrote this into gameplan l.140. *Team recommendation: ratify; the old rule passed a contact 490 mm out of place.*

**G6. Gameplan header.** "Accumulator file: none yet" is stale; the file exists at `research/sean/accumulator.md`. The header was held byte-identical at Step 0. *Team recommendation: approve the one-line fix.*

**G7. Height margin.** On the draft seeds the top-end block reaches 2025 mm above the floor at load and park, 25 mm over the 2000 mm soft target. It is a reported value, never a limit, and depends on Q2 (top-end hardware) and N10 (feet). *Team recommendation: no action until Quinn answers Q2.*

## 4. What Step 1.1 does first

The Manager opens 1.1 with Sean's G1 to G4 rulings written into the spawn prompts. The first wave is the Designer's params review (1.1 a) of the S1 keys, covering the Design Notes 20 rows due at (a): lift fit, core stop, taper directions, radial geometry, TP-9. The Engineer then revises the draft s1_spec.yaml for the Designer's and Loftsman's signatures, adding the LF-16 lint and the capture-reach check.
