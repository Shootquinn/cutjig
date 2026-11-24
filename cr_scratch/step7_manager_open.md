## 1. Step 7 scope

Detail 7: assemble the jig in poses R (release), Kd1 (clamp at d+1) and Kmax (clamp at d-1.5) for the seven family sizes from one base pose by the screw motion S(phi) = Rz(phi) T(0,0,L phi / 2 pi); contact-class matrix (45 part pairs, 6 feature pairs, C / G / F) per pose per size; predicates A3b to A3i; clamp range T4 and T5 at 90 and 105 mm; wrong-state controls WS1 to WS11; carried geometry defects from Step 6 (C6 bracket overlap 18,249 mm3 x 4, printed bracket against end member 1,061 mm3 x 4, T-nut pair overlap 16,523 mm3). Gate: Software Engineer, Systems Engineer, Designer (A5, image-capable reviewer).

## 2. Baseline B7 (measured 2026-11-10 by the Manager; full run 81.5 s)

| Item | Value |
|---|---|
| Tests | 591 collected, 413 passed, 178 failed |
| Failures by file | test_assembly 134, test_exports 31, test_thread_clamp 11, test_step6_parts 2 |
| The 2 test_step6_parts failures | `results\probes\step6_parts.json` older than `parts_cache\rest.FCStd` (rest rebuilt 05:44 in the Step 6 fix pass; probe not refreshed). Refresh restores the Step 6 close state: 415 pass, 176 fail, green_at_6 41/41. First action of the wave-0 Software Engineer |
| Red by absence (176) | all `MISSING:` / `ABSENT FEATURE:`; green_at_7 126, green_at_8 1, green_at_10 31, green_at_12 18 |
| green_at_7 (126, all red) | test_assembly 116: A1a x21 (3 poses x 7 sizes), A3b, A3c x2, A3d x7, A3e x21, A3f x2, A3g, A3h x21, A3i x21, A4 x3, A6 x9 (WS1 to WS7, WS10, WS11), A6a, A6b (WS8), A6c (WS9), F6 x3, P6b. test_thread_clamp 10: T4 x6, T5 x4 |
| Red, later steps | green_at_8: T7 (1). green_at_10: E1 x13, E2 x12, E3 x1, T1d x2, B1, X1 x2 (31). green_at_12: A1b to A1e, A2a, A2b x7, A2c to A2h (18) |
| Existing parts | 72 files in `parts_cache` (mtimes in `cr_scratch\step7_fcstd_mtimes_before.txt`, recorded after moving the stray `rest.20261110-043849.FCBak` to `cr_scratch\fcbak_archive`) |
| Not on disk | `build_parts\assemble.py`, `parts_cache\assembly\`, core stand-in and cutter keep-out parts, `tests\probes\probe_ws.py`, probe measures for core_axis_offset, lead_in_clearance, clamped_tilt_deg, funnel_capture_radius, receiver_underside_contact_mm2, frame_footprint, slit_width_clamped_min, nut_travel_left_mm, A3b fits |
| `probe_poses.py` today | writes floor_z, holder_bottom_above_floor, collar_top_z, nut_skirt_bottom_above_floor, engaged_mm |
| 80/20 CAD | 30-6060 STEP, 14089 STEP, printed bracket STL / 3mf on disk (read in place, Step 6). PZRT 3030 T-nut CAD not on disk; proxy in `tnut.FCStd`; no download |

Test count prediction for the opening: collected = 591 + added at wave 0 and 1x. The Step 4 and Step 6 openings each mispredicted a count; the Manager close counts by a Manager run.

## 3. Deliverables (Detail 7 outputs)

1. `build_parts\assemble.py` (poses from one base pose by S(phi); explicit placements; identity-placement audit), `build_parts\assemble_ws.py` (planted states), `build_parts\assemble_report.py` (interference report generator), `build_parts\core.py`, `build_parts\cutter.py`; edits to `bracket.py`, `tnut.py`, `frame.py` per the Loftsman's C6 option.
2. `parts_cache\assembly\pose_<P>_<tag>.FCStd` (21), `parts_cache\assembly\ws<n>.FCStd` (11), `results\assembly_poses.json` (pose ledger), `results\probes\pose_*.json`, `results\probes\ws*.json`.
3. `output\jig_assembly.FCStd` and `output\jig_assembly.step` (nominal 100 mm, Kd1; every deliverable visible and named).
4. `cr_scratch\step7_interference_report.md`: tool-generated; one table per collet size; per-pair mm3, class, pass / fail; clamp-range and wrong-state tables.
5. Four-view PNG set plus close-ups in `cr_scratch\step7_renders\` with `INDEX.md`.
6. Tests: wave-0 additions (probe measures, `probe_ws.py`, zero control for A6, C6 per-instance overlaps, pose-ledger test, report parse test), all `green_at_7`.
7. Working products: `step7_software_engineer_tests.md`, `step7_loftsman_definition.md`, `step7_topologist_crossreview.md`, `step7_software_engineer_prebuild.md`, `step7_engineer_parts_findings.md`, `step7_engineer_assemble_findings.md`, `step7_engineer_renders_findings.md`, `step7_designer_critique.md`, `step7_software_engineer_code_review.md`, `step7_topologist_topology_gate.md`, `step7_systems_engineer_review.md`, `step7_manager_close.md`.

## 4. Wave plan

| Order | Agent | Model | Mode | Task | Writes | Prompt file |
|---|---|---|---|---|---|---|
| 0 | The Software Engineer | sonnet | foreground | TDD precondition: review the 126 green_at_7 tests, add G1 to G7 tests and probe code red-first, define the pose / ws / instance contract, refresh the stale `step6_parts` probe, baseline run | `tests\test_assembly.py` or `tests\test_step7_assembly.py`, `tests\probes\probe_poses.py`, `probe_ws.py`, `cad_helpers.py`, `cr_scratch\step7_software_engineer_tests.md` | `step7_prompt_software_engineer_tests.md` |
| 1 | The Loftsman | sonnet | foreground | Numbers and constructions L1 to L8: pose table by S(phi), core, cutter, frame placement, C6 resolution option, missing-measure equations, WS transforms, clamp range | `cr_scratch\step7_loftsman_definition.md` | `step7_prompt_loftsman_definition.md` |
| 1x | The Topologist | sonnet | foreground, parallel with next row | Geometry cross-review (A.4 step 2): SIGN / EDIT / WITHHOLD per line; screw-motion sign, composition order, WS orientation, C6 contact predicates, Euler predictions | `cr_scratch\step7_topologist_crossreview.md` | `step7_prompt_topologist_crossreview.md` |
| 1x | The Software Engineer | sonnet | foreground, parallel with Topologist | Pre-build review: tests against the definition, contract match, revisions with stated reasons | `cr_scratch\step7_software_engineer_prebuild.md`, test edits | `step7_prompt_software_engineer_prebuild.md` |
| 2a | The Engineer | sonnet | background, PID + log + `BUILD_DONE` | Params keys; C6 option built (frame, brackets, tnut); `core.py`, `cutter.py`; C6 numbers from rebuilt FCStd; mtime comparison | `build_parts\*`, `parts_cache\*`, `cr_scratch\step7_engineer_parts_findings.md` | `step7_prompt_engineer_parts.md` |
| 2b | The Engineer (new spawn) | sonnet | background, PID + log + `BUILD_DONE` | `assemble.py`, 21 poses, 11 planted states, probes, interference report, pytest | `build_parts\assemble*.py`, `parts_cache\assembly\*`, `output\jig_assembly.*`, `cr_scratch\step7_interference_report.md`, `cr_scratch\step7_engineer_assemble_findings.md` | `step7_prompt_engineer_assemble.md` |
| 2c | The Engineer (new spawn) | sonnet | background | Render harness check, four-view set and close-ups, INDEX.md | `cr_scratch\step7_renders\*`, `cr_scratch\step7_engineer_renders_findings.md` | `step7_prompt_engineer_renders.md` |
| 3 | The Designer | **opus** (image gate A5) | foreground | Read every PNG, rubric verdicts, pride test, Design Critique | `cr_scratch\step7_designer_critique.md` | `step7_prompt_designer_image_gate.md` |
| 3 | The Software Engineer | sonnet | foreground, parallel with Designer | Code review of assembler, probes, rebuilt generators; literal scan; final test run | `cr_scratch\step7_software_engineer_code_review.md` | `step7_prompt_software_engineer_code_review.md` |
| 3 | The Topologist | sonnet | foreground, after 2b | Topology and placement gate; owns the re-check list generated from mtimes | `cr_scratch\step7_topologist_topology_gate.md` | `step7_prompt_topologist_topology_gate.md` |
| 3 | The Systems Engineer | sonnet | foreground, parallel with the three above | System coherence of the assembled jig against the frozen concept and ICD | `cr_scratch\step7_systems_engineer_review.md` | `step7_prompt_systems_engineer_review.md` |
| 4 | Fix pass | The Engineer (SendMessage continuation of 2b) | background | Designer BLOCK items, Topologist defects, SE result-changing defects; re-render changed views | updated parts, probes, renders | none (continuation) |
| 4r | The Topologist | sonnet | foreground | Re-read: regenerate the re-check list, sign every file modified after the gate (continuation of the gate prompt via SendMessage) | `cr_scratch\step7_topologist_topology_gate.md` (addendum) | none (continuation) |
| 5 | The Manager close | sonnet | foreground | Criteria below | `cr_scratch\step7_manager_close.md` | spawned by orchestrator |

Not spawned: Fact-Checker (no new source claim; Design Notes 18), Writer, Editor, Motor Designer, Space Resources Engineer, Recruiter. Opus appears once: the Designer image gate (A.3.1). Contingency, off by default: if the Topologist withholds the screw-motion derivation (L1) a second time, the orchestrator may spawn a single Opus Loftsman re-derivation of that line.

## 5. Sequence

1. Software Engineer authors and reviews tests and refreshes the stale probe (TDD precondition, A.4 step 1). The baseline run after the refresh records the red set.
2. Loftsman writes the definition against the red tests (contract from step 1).
3. Topologist cross-review and Software Engineer pre-build review, parallel. A withhold gets one Loftsman revision (SendMessage). A second withhold is ruled by number by the Manager or orchestrator, smallest edit, no re-view (Design Notes 16).
4. Orchestrator Globs `parts_cache`, `build_parts`, `tests`, `tests\probes` and checks Engineer prompt paths against the Glob (Design Notes 13). Engineer 2a spawns in the background; PID, log path and expected finish go into the gameplan Progress Log at launch; each log ends `BUILD_DONE`.
5. Engineer 2b spawns after 2a returns (assembler reads the rebuilt parts). Engineer 2c after 2b.
6. Wave 3 runs in parallel: Designer (Opus), Software Engineer code review, Topologist gate, Systems Engineer.
7. Fix pass for BLOCK or defect items; Topologist re-read regenerates the re-check list from mtimes and signs every row. The re-check list has one owner (the Topologist) and a closing read (criterion 8).
8. Manager close.
Geometry cross-review before any geometry change (A.4 step 2): the Loftsman definition and the Topologist cross-review both precede the 2a spawn. The Engineer does not rebuild frame, bracket, tnut before that.

## 6. Rubric for gate A5 (Designer, image-capable reviewer)

One item per signed feature and signifier. Each PNG in `INDEX.md` lists the item numbers it must show.

| # | Item | Source |
|---|---|---|
| 1 | Base plate: asymmetric slotted-hole pattern (one slot offset), flat on the receiver foot, plate keys, stop pin pocket | ASSEMBLY.md Parts; BS1 to BS7 |
| 2 | Receiver: rim witness scale, thread with lead-in, key slot at 37 deg | RC1 to RC6 |
| 3 | Holder: index notch on the flange rim, witness tick (HD7), cone and collar | HD1 to HD4, HD7 |
| 4 | Collet: foot key on the underside, slit phase to key, rim notches, grip-window label, size colour | CO1 to CO8 |
| 5 | Nut: single marked wing, tighten glyph clockwise (NT4), loosen glyph counter-clockwise on the opposite wing face (NT5), release arrow on the plate (NT8), tommy-bar sockets, dust skirt | NT1 to NT8 |
| 6 | Washer: radial tab notch off-axis, PTFE ring seated in the nut pocket | WS1 to WS3 |
| 7 | Core stand-in: top-end chamfer on the top end only; stands on the collet core stop, off the tray | ASSEMBLY.md Parts |
| 8 | Frame: datum C slot-line notch on one rail; six members; base plate seated on the top plane | FR1, FR4 |
| 9 | Brackets: purchased and printed classes at four joints each, one clean joint at each of the four C6 sites, no member passing through another | FR2, C6 |
| 10 | T-nuts: eight per bracket in the slot | FR3 |
| 11 | Cutter keep-out: tube and face annulus, orientation fixed by the frame | A2 |
| 12 | Tray and drain plug; stop pad (ST1) as an interface item | BS5, BS6, ST1 |
| 13 | Pose legibility: R, Kd1 and Kmax differ visibly (nut height, holder, flange gap); witness reads at Kmax and Kd1 per Design Notes 21 | Detail 7 |
| 14 | Placement: no part flipped, displaced or on the wrong plane (errors that interference analysis misses) | llm_plm_cad.md 7.5 |
| 15 | Pride test for the assembly: would the Designer show it to a client without apology | A.12.5 |

Accessories (caddy, gauge, steady rest) are context views, judged for placement only; their Pass 2 items stay at Step 9.

## 7. Rebuild authorization

Authorized rebuilds of existing FCStd (the "authorized list"):

| FCStd | Reason |
|---|---|
| `frame.FCStd` | C6 resolution if the Loftsman's option moves or cuts members or brackets |
| `bracket_purchased.FCStd`, `bracket_printed.FCStd` | C6 resolution (bracket cut or face move) |
| `tnut.FCStd` | C6 T-nut pair overlap; count after the cut |

New files: `core`, `cutter`, `parts_cache\assembly\*`, `output\jig_assembly.*`.

Rules:
1. Every rebuild appears in `step7_engineer_parts_findings.md` with before and after volume and face count and the reason.
2. Unlisted files keep the mtimes in `step7_fcstd_mtimes_before.txt`: receiver, holder, nut, washer, footring, base, tray, plug, foot, caddy, gauge, rest, stop, frame_profiles, 27 collet FCStd, `step3_cross_checks.json`.
3. A fault found in an unlisted part is reported to the Manager. The Manager authorizes the rebuild in writing in `cr_scratch\step7_rebuild_authorizations.md` before it runs; criterion 7 reads that file.
4. A rebuild keeps every existing F5 invariant green and every Step 6 test green; a revised invariant carries a stated reason (A.10 item 5).
5. `.FCBak` files go to `cr_scratch\fcbak_archive`, never left in `parts_cache` or `results`.
6. Any FCStd modified after the Topologist's gate is on the Topologist's re-check list (criterion 8).

## 8. Close criteria

1. Tests first: wave-0 tests file and pre-build review exist; their mtimes precede the first Engineer build log; at that time every `green_at_7` discriminator is red with `MISSING:` or `ABSENT FEATURE:`; every new test carries `green_at_7`.
2. Loftsman definition and Topologist cross-review exist, with SIGNED lines or withheld-and-ruled lines recorded, mtimes earlier than the first build log.
3. Every `green_at_7` test passes in the Manager's re-run after the last edit (126 plus added): test_assembly and test_thread_clamp T4 and T5 included. Zero errors, skips, xfails.
4. Baseline: collected = 591 + added; the 415 passes at the refreshed baseline all still pass, or each is revised with a stated reason; green_at_4, 5, 6 are fully green.
5. Every remaining failure is `MISSING:` or `ABSENT FEATURE:` and belongs to green_at_8 (T7), green_at_10 (31 tests) or green_at_12 (18 tests). Counts written to the close note.
6. Carried overlaps resolved: bracket pair, bracket against end member and rail, and T-nut pair common volumes are zero (below 0.01 mm3) at all 16 brackets and 128 T-nuts in the rebuilt FCStd, or a pair carries a ruled contact class in ASSEMBLY.md (Feature pairs row or relation) backed by a written ruling and a measured predicate; the findings table shows before (18,249 / 1,061 / 16,523 mm3) and after; stock allocation (P3) and the 8-per-bracket count still pass.
7. Rebuilds: files modified in `parts_cache` since the baseline equal the authorized list plus new files plus any written authorization; mtimes of unlisted files equal `step7_fcstd_mtimes_before.txt`; the findings list every rebuilt FCStd against that baseline.
8. Topologist re-check: the topology gate file carries a re-check list generated by script from mtimes; every file modified after the baseline has a reading and a SIGNED verdict; the latest reading postdates the latest FCStd mtime (the Manager compares the two). Euler predictions from the cross-review are hit or the miss is explained.
9. Poses: `results\assembly_poses.json` records the base pose and phi per pose; the ledger test passes (nut(Kmax) = S(phi) nut(R), nothing else moves except the nut-riding parts); a clockwise turn from K lowers the nut (T1c sign in the assembled pose).
10. Contact-class matrix: A1a passes for 3 poses x 7 sizes; the interference report is tool-generated (header names `assemble_report.py`), has one table per size with 45 part pairs and 6 feature pairs, and its cells equal the probe JSON; no ASSEMBLY.md relation changed without an entry in `step7_class_rulings.md` and the Topologist's sign.
11. Clamp range: T4 (6 cases) and T5 (4 cases) pass at 90 and 105 mm; engagement is at least `thread.min_engage_pitches` x pitch in every pose and size (A3i), nut travel left is at least one pitch at Kmax (S12), holder flange gap to rim above zero.
12. Wrong states: WS1 to WS11 each fire at least one of A1, A3, T1, T9, F1, F3 and no other gate; the unplanted pose fires none (zero control).
13. Image gate: `step7_renders\INDEX.md` lists a four-view set for the nominal assembly in R and Kmax, d = 90 and d = 105 at Kmax, and close-ups for rubric items 1 to 13; the Designer critique states "visual gate RUN" with the PNG count read and a verdict per rubric item 1 to 15; no ABSENT or WRONG item stays open after the fix pass. A text-only critique fails this criterion.
14. Gates: Software Engineer code review file exists with the literal scan (zero hits in new scripts) and no open result-changing defect; Systems Engineer review is SIGNED or its withhold is closed by ruling.
15. Greps by the Manager: hazard terms (pinch, finger, crush, hand entry, 13854, knuckle, safety) in new and edited `build_parts`, `tests`, `docs` files outside the P22 allowlist return nothing; no printer, bed, nozzle, material key read by any Step 7 script; no `.FCBak` in `parts_cache` or `results`; no `SubtractiveHelix` cut into a bore in new scripts.
16. Background builds: PID, log path, expected finish in the gameplan Progress Log; each build and probe log ends `BUILD_DONE`; success judged by log sentinel and fresh artifact mtime (A.3.4).
17. Deliverables and bookkeeping: `assemble.py`, `output\jig_assembly.FCStd`, `.step`, interference report, PNG set exist; word caps (tests 600, Loftsman 1800, Topologist cross-review 700, SE pre-build 500, Engineer parts 1200, Engineer assemble 1200, renders 300, Designer 1000, SE code review 500, Topologist gate 500, Systems Engineer 700; tables counted without pipes, counted by script; overruns up to 20 percent are clerical, Design Notes 18); gameplan edits at close: Step 7 row Complete, Progress Log row with PIDs and logs, Detail 7 outputs line, params leaf count, Design Notes row if a ruling was made; accumulator entries for Software Engineer, Loftsman, Topologist, Engineer, Designer, Systems Engineer.

## 9. Open items closed by assumption at open (no human input)

A. **Which sizes get poses.** The 7 sizes in `core.diameters` (A1a, A3d, A3e, A3h, A3i parametrize over them). The two off-grid collets (093p7, 097p0) stay C10 artifacts; no Step 7 pose.
B. **Assembly of the nominal case.** Core length 0.5 m is the asserted case; 0.75 m and 1 m appear as recorded values only (test_assembly header).
C. **C6 option.** The Loftsman chooses among cutting the bracket geometry, moving one bracket class to another profile face, lengthening a rail (stock allocation consequence stated), or a ruled contact class. Default preference: the option that keeps every stock cut length and every existing test number unchanged. The rail-inner-face need (740 against 644) is a DERIVED number from the Step 6 definition; the Loftsman re-derives it.
D. **T-nut CAD.** Proxy stays; the absence is a standing finding, no download.
E. **Relation rows are data.** A change of class needs a geometric reason, a ruling in `step7_class_rulings.md`, and the Topologist's sign; no predicate threshold is weakened.
F. **Exports.** `output\jig_assembly.FCStd` and `.step` are written at Step 7 (Detail 7 outputs); E1, E2, E3, B1, X1, T1d stay green_at_10.
G. **T7 holding torque** is green_at_8 (Step 8).
H. **Printability** (print orientation, layers, nozzle): Step 8.

## 10. Rules carried

Sonnet for every spawn; Opus for the Designer image gate only. No safety, pinch, finger, crush, hand-entry, ISO 13854 wording: a clearance is mechanical or usability. The printer is not a design input. T-nuts PZRT 3030 roll-in spring M6, 8 per bracket (ASSUMED). A missing 80/20 CAD part is a finding, never a download. Clerical findings never block (Design Notes 18); FreeCAD run time is no constraint; builds go to the background. Female threads by stud-subtract (Design Notes 19). A params-duplicating literal is a defect fixed inside the step (Design Notes 20). Fuse first, boolean once. A number that feeds a formula carries its basis and formula text (Design Notes 16). Red first with `MISSING:` / `ABSENT FEATURE:` messages and `green_at_7` markers; the Software Engineer reviews tests before build. A render pose is read from the model before a BLOCK is raised (Design Notes 21). The re-check list of a gate has an owner and a closing read (Design Notes 21).

## 11. Decisions for the orchestrator

None blocking. To carry out as written:
1. Spawn order starts with the Software Engineer (wave 0); the stale `step6_parts` probe is refreshed there, which moves B7 from 413 / 178 to 415 / 176.
2. The Designer spawn uses `model: opus` and receives PNG paths only; every other prompt uses `model: sonnet`. Each prompt file's first line is an HTML comment naming model and mode; pass the text below that line verbatim.
3. Engineer spawns 2a, 2b, 2c run sequentially in the background (each depends on the previous output); Glob-check paths before 2a and 2b (Design Notes 13).
4. After the fix pass, send the Topologist a continuation (SendMessage) to regenerate the re-check list; criterion 8 reads it.
