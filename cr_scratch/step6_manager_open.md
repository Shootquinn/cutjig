## 1. Step 6 scope

Step 6 is Pass 1 (exploratory, LLM-PLM 7.6) for every part and accessory in Detail 6. Every functional feature on the Designer checklist exists in 3D, simplified where the rule allows. The Pass 1 data (interference, clearance, stock fit, mass, design issues) goes to `cr_scratch\step6_engineer_findings.md` and feeds Steps 7 to 9. Gate: Designer completeness against the checklist, image-capable reviewer reading rendered PNGs of every part.

## 2. Baseline B6 (measured 2026-11-10 by the Manager; full run 56.8 s)

| Item | Value |
|---|---|
| Tests | 540 collected, 364 passed, 176 failed (MISSING 175, ABSENT FEATURE 1, other 0); failures by file: test_assembly 134, test_exports 31, test_thread_clamp 11 |
| Tests labelled green_at_6 | 0. `cad_helpers.label` accepts N = 6; no test uses it. No Step 6 test exists: the TDD precondition is unmet |
| Existing F5 | `test_F5_five_parts_shell_features_and_flipped_copy` over `H.FIVE_PARTS` = receiver, holder, nut, washer, footring (invariant, green_at_4) |
| params.yaml | 332 leaves. Keys present with no builder: `base.*`, `tray.*`, `caddy.*`, `gauge.*`, `rest.*`, `bolt_down.*`, `bracket.*`, `hardware.*`, `stop.pad_*`, `witness.*`, `frame.*`, `stock.*` |
| parts_cache | receiver, holder, nut, washer, footring (Step 3/4; each with `_result.json`), `frame_profiles.FCStd` (six bare extrusions at the origin, unplaced), 27 collet FCStd (9 free, 18 clamped) with result JSON, `step3_cross_checks.json`. 48 files; mtimes in `cr_scratch\step6_fcstd_mtimes_before.txt` |
| build_parts | common, cadlib, receiver, holder, nut, washer, footring, collet_family, frame_profiles, bom_tools, measure_step, profile_fidelity, verify_step3. No script for base, tray, foot, frame placement, brackets, T-nut, caddy, gauge, rest, stop |
| On disk (read in place, no download) | `8020-30-6060 X 1540.step`, `8020-14089.step`, printed bracket `8020 30 Series Corner Bracket 3dp.stl` / `.3mf` in `C:\Users\Quinn Morley\OneDrive\PROJECTS\Planet Enterprises\NIAC\BOREBOTS\Unleashed Robotics\ENGINEERING\FractalMining\Borebot Hardware` |
| Not on disk | PZRT 3030 roll-in spring M6 T-nut CAD. Finding: proxy envelope from the slot profile (`profile.*`), dimensions ASSUMED, no download |
| Renders | None. No image exists for any part; `cr_scratch` holds no PNG. Visual gate has never run (Steps 3 and 5 were text-only) |
| FreeCAD | `%LOCALAPPDATA%\Programs\FreeCAD 1.1\bin\freecadcmd.exe` and `freecad.exe` present (1.1.4) |

## 3. Detail 6 checklist and status at B6

IDs below are the contract for tests, definition, findings and critique.

| ID | Part | Item | Status at B6 |
|---|---|---|---|
| RC1 | receiver | external thread with lead-in | in `receiver.FCStd` (stud not needed; native helix) |
| RC2 | receiver | thread land / runout | present |
| RC3 | receiver | floor seat for the collet foot ring | present (floor top z = 0) |
| RC4 | receiver | register bore for the holder | present |
| RC5 | receiver | asymmetric key slot (azimuth 37 deg, Rule P) | present |
| RC6 | receiver | witness scale on the rim | ABSENT. Rebuild |
| HD1-HD4 | holder | cone, flange, key, collar with M6 insert bores | present |
| HD5 | holder | no jacking holes (negative feature) | present by absence; test asserts absence |
| HD6 | holder | no hard-stop face; foot ring top is the holder stop | present by absence; test asserts absence |
| HD7 | holder | witness tick on the flange | ABSENT. Rebuild |
| WS1-WS3 | washer | PTFE ring 136.8 / 143.2 / 1.3, radial tab notch, captive in nut face (pads `nut.pad_*`) | present |
| CO1-CO8 | collet | cone, bore, alternating slits, relief holes, foot key, core stop, rim notches, grip-window label (flat recess, text in JSON), lead-in chamfer | present for all 9 sizes (Step 5 PASS); Step 6 renders only |
| NT1-NT3 | nut | captured-flange thread, bearing face, wings with planform | present |
| NT4 | nut | tighten glyph: tangential clockwise, inside `nut.arrow_length` 21.86 | CHANGE. Built mark is one radial mark on wing 0 +y face. Rebuild |
| NT5 | nut | loosen glyph: counter-clockwise, opposite wing face, inside 21.86 | ABSENT. Rebuild |
| NT6 | nut | tommy-bar sockets | present |
| NT7 | nut | dust skirt (`icd.cable_exit`, Detail 6) | ABSENT: `nut.py` has no skirt feature beyond the thread skirt. Rebuild |
| NT8 | nut | release arrow on the plate (33.25 deg) | present |
| NT9 | nut | witness line of sight (see section 9, item A) | to be ruled by the Loftsman; rebuild if a window is needed |
| BS1-BS7 | base | plate, spigot hole, slotted mounting holes (asymmetric pattern), T-nut provisions (plate keys, stop pin, fastener slots), debris tray, drain with plug, feet / bolt-down | ALL ABSENT |
| FR1 | frame | six members from stock with allocation (rail 644 x 2, end 488 x 2, plate_support 468 x 2; whole stock pieces) | ABSENT as placed geometry (bare extrusions exist) |
| FR2 | frame | brackets: 4 joints purchased 14089 class x 2, 4 joints printed 68 mm class x 2 | ABSENT |
| FR3 | frame | T-nuts, 8 per bracket (ASSUMED) | ABSENT |
| FR4 | frame | datum C slot line notch on one rail (Rule P) | ABSENT |
| AC1 | caddy | seven sockets (`caddy.socket_clear`, `socket_depth`) | ABSENT (collet fit record exists in JSON) |
| AC2 | alignment gauge | register plug 134.08 x 150 | ABSENT |
| AC3 | steady rest (or cradle) | three linked rollers, arm, close handle, hold-open detent, column interface | ABSENT |
| AC4 / AC5 | witness scale / tick | same items as RC6 / HD7 | ABSENT |
| ST1 | stop | interface item at `stop.height_z`, 60 x 60 pad (`stop.pad_*`), owner upper assembly, not a nut property | ABSENT |

Receiver key slot (RC5), PTFE washer, foot ring and all collets need no rebuild. The washer, foot ring and collet files stay unchanged unless the Engineer reports a fault and the Manager authorizes the rebuild in writing (section 6).

## 4. Deliverables (Detail 6 outputs)

1. `build_parts\<part>.py` for: `base`, `tray`, `foot`, `tnut`, `bracket` (writes `bracket_purchased` and `bracket_printed`), `frame`, `caddy`, `gauge`, `rest`, `stop`; edits to `receiver.py`, `holder.py`, `nut.py`. This partition is the default; the Loftsman may amend it in his definition and the Software Engineer follows his amendment.
2. `parts_cache\<part>.FCStd` and `<part>_result.json` for every part above, with `euler_VEF`, `faces_before` / `faces_after` per boolean, `bbox_plain`, `bbox_optimal`, boolean count, `features` rows (name, volume_mm3, pass), `run_seconds`.
3. `cr_scratch\step6_engineer_findings.md` (opens with "Corrections to the brief"; Pass 1 data; Detail 6 checklist table with status per ID; the rebuild list; 80/20 CAD findings).
4. `cr_scratch\step6_designer_critique.md` (Design Critique, llm_plm 8.4c; per-part verdict per checklist ID; "visual gate RUN" with image count).
5. Renders: `cr_scratch\step6_renders\<part>_<view>.png` plus `cr_scratch\step6_renders\INDEX.md` (one row per PNG: part, view, checklist IDs the view must show).
6. `tests\test_step6_parts.py` (new; green_at_6) and any helper edits in `tests\cad_helpers.py`, `tests\probes\`.

## 5. Wave plan

| Order | Agent | Model | Mode | Task | Writes | Prompt file |
|---|---|---|---|---|---|---|
| 0 | The Software Engineer | sonnet | foreground | Author Step 6 tests red-first: F5-style per new part, checklist-ID feature rows, negative features HD5 HD6, signed-feature flip checks, nut glyph sense, witness reading, stock allocation, T-nut count, stop interface; controls; baseline run | `tests\test_step6_parts.py`, `cr_scratch\step6_software_engineer_tests.md` | `step6_prompt_software_engineer_tests.md` |
| 1 | The Loftsman | sonnet | foreground | Numbers and constructions for every NEW or CHANGED item, bases stated per row, new params keys | `cr_scratch\step6_loftsman_definition.md` | `step6_prompt_loftsman_definition.md` |
| 1x | The Topologist | sonnet | foreground, parallel with next row | Cross-review: SIGN or WITHHOLD per line; boolean order, tangencies, genus and Euler predictions, glyph and tick orientation signs | `cr_scratch\step6_topologist_crossreview.md` | `step6_prompt_topologist_crossreview.md` |
| 1x | The Software Engineer | sonnet | foreground, parallel with Topologist | Pre-build review: tests against the definition, result-JSON contract, revisions with stated reasons | `cr_scratch\step6_software_engineer_prebuild.md`, test edits | `step6_prompt_software_engineer_prebuild.md` |
| 2 | The Engineer | sonnet | background, PID + log + `BUILD_DONE` | params keys, rebuilds, new parts, parallel detached `freecadcmd` jobs, probes, pytest | `build_parts\*.py`, `parts_cache\*`, `cr_scratch\step6_engineer_findings.md` | `step6_prompt_engineer_build.md` |
| 2r | The Engineer (second spawn) | sonnet | background | Render harness verified, PNG set, INDEX.md | `cr_scratch\step6_renders\*` | `step6_prompt_engineer_renders.md` |
| 3 | The Designer | **opus** (image gate) | foreground | Read every PNG, completeness against the checklist, Design Critique | `cr_scratch\step6_designer_critique.md` | `step6_prompt_designer_image_gate.md` |
| 3 | The Software Engineer | sonnet | foreground, parallel with Designer | Code review of new generators; final test run vs close criteria | `cr_scratch\step6_software_engineer_code_review.md` | `step6_prompt_software_engineer_code_review.md` |
| 3 | The Topologist | sonnet | foreground, after the Engineer | Topology gate from probe and result JSON for every new and rebuilt part | `cr_scratch\step6_topologist_topology_gate.md` | `step6_prompt_topologist_topology_gate.md` |
| 4 | Fix pass | The Engineer (SendMessage continuation) | background | Designer ABSENT or glyph-unreadable items; topology-gate defects | updated parts, re-renders | none (continuation) |
| 5 | The Manager close | sonnet | foreground | Criteria below | `cr_scratch\step6_manager_close.md` | spawned by orchestrator |

Not spawned: Fact-Checker (no new source claim; Design Notes 18), Systems Engineer (ICD keys frozen; stop stays an interface item), Writer, Editor, Motor Designer, Space Resources Engineer, Recruiter.

Opus appears once: the Designer image gate (A.3.1). A same-model look by the Engineer is a numeric check only (nonblank PNG, part pixel coverage) and not a gate.

## 6. Sequence

1. Software Engineer authors the tests (TDD precondition, A.4). Baseline run records the red set.
2. Loftsman writes the definition with the red tests as the acceptance contract.
3. Topologist cross-review and Software Engineer pre-build review, parallel. A withhold gets one Loftsman revision (SendMessage). A second withhold is ruled by number by the Manager or orchestrator, smallest edit, no re-view (Design Notes 16 lesson).
4. Orchestrator Globs `parts_cache`, `build_parts`, `tests`, `tests\probes` and checks the Engineer prompt paths (Design Notes 13). Engineer spawns in the background.
5. Engineer adds params keys first (one pass, single writer), then launches detached `freecadcmd` jobs in parallel: rebuilds (receiver, holder, nut) and new parts. PID, log path and expected finish go into the gameplan Progress Log at launch. Each log ends with `BUILD_DONE`.
6. Engineer renders (second spawn).
7. Wave 3: Designer (Opus) in parallel with Software Engineer code review; Topologist topology gate.
8. Fix pass for ABSENT or unreadable items, re-render the changed parts, Designer re-reads only those PNGs.
9. Manager close.

## 7. Rebuild authorization

Authorized rebuilds of Step 3/4 files (the "authorized list"):

| FCStd | Reason | Items |
|---|---|---|
| `receiver.FCStd` | witness scale on the rim; line-of-sight provision if ruled | RC6, AC4, NT9 partner |
| `holder.FCStd` | witness tick on the flange | HD7, AC5 |
| `nut.FCStd` | tighten and loosen glyphs, dust skirt, witness window if ruled | NT4, NT5, NT7, NT9 |

Rules:
1. Every rebuild is listed in `step6_engineer_findings.md` with before and after volume, face count, feature rows added, and the reason ID.
2. Unlisted files keep their mtimes from `step6_fcstd_mtimes_before.txt`: `washer`, `footring`, `frame_profiles`, all 27 collet FCStd, `step3_cross_checks.json`.
3. A fault found in an unlisted part is reported to the Manager. The Manager authorizes the rebuild in writing in `cr_scratch\step6_rebuild_authorizations.md` before it runs; close criterion 5 reads that file.
4. A rebuild keeps every existing F5 invariant green (genus 1 for receiver and holder, `1 + washer_window_count` for the nut, flipped-copy mismatch above `FLIP_FLOOR`). A rebuilt nut keeps its thread by stud-subtract (Design Notes 19). An invariant that fires after an authorized rebuild is revised by the Software Engineer with a stated reason (A.10 item 5), never weakened to pass.
5. `.FCBak` files go to `cr_scratch\fcbak_archive`, never left in `parts_cache` or `results`.

## 8. Close criteria

1. Tests exist first: `tests\test_step6_parts.py` carries `green_at_6` on every Step 6 test; at the first build-log timestamp every `green_at_6` discriminator is red with `MISSING:` or `ABSENT FEATURE:`; Software Engineer pre-build review file exists and predates the first build log.
2. Loftsman definition and Topologist cross-review exist, with SIGNED or withheld-and-ruled lines recorded, mtimes earlier than the first build log.
3. Every part in section 4 item 1 has a builder, an FCStd, and a result JSON; each FCStd shape `isValid`, `isClosed`, one solid per part (frame: one valid closed solid per member and per bracket); `run_seconds` present; boolean data per 7.1 recorded (`faces_before` / `faces_after` per boolean, `bbox_plain`, `bbox_optimal`, count of booleans).
4. Detail 6 checklist: every ID in section 3 reads PASS in the findings table, each backed by a result-JSON feature row with nonzero `volume_mm3` (negative features HD5 and HD6 by a test asserting absence). No ABSENT.
5. Rebuilds: modified files equal the authorized list (section 7) plus any written authorizations; mtimes of unlisted files equal the before file.
6. Test counts (Manager re-run after the last edit): collected = 540 + added; all 364 baseline passes still pass (or each revised with a stated reason); every `green_at_6` test passes; every remaining failure is `MISSING:` or `ABSENT FEATURE:` and labelled green_at 7 or later; zero errors, skips, xfails. Counts written to the close note.
7. Nut glyphs (NT4, NT5): result JSON records for each glyph the wing face, the tangential direction sign as seen from +Z (tighten clockwise, loosen counter-clockwise), and the radial span inside 21.86 mm; the two glyphs are on opposite wing faces; flipped-copy mismatch stays above `FLIP_FLOOR`; the Designer reads both in a render and states which way each turns.
8. Witness (RC6, HD7): graduations at `witness.scale_pitch` over 0 to `holder.stroke_gap_R`; zone 1.5 to 8.59 and wrong-collet bands match `witness.*`; a built-shape test places tick against scale at K-max and K d+1 and reads 1.5 and 8.59 within 0.05 mm; the line of sight to the reading is stated and the Designer confirms it in a render.
9. Image gate: `cr_scratch\step6_renders\INDEX.md` lists at least one PNG per part (collets at 90, 97.5, 105; nut with both wing faces; receiver rim scale close-up; holder tick close-up; base with tray; frame with brackets; accessories); the Designer critique states "visual gate RUN" with the PNG count read, and carries a verdict per checklist ID. A text-only critique fails this criterion.
10. Topology gate file lists per part: `euler_VEF`, genus, component count, signed volume sign, faces per boolean, bbox plain versus optimal, and ends SIGNED or names the defect lines; defects are closed in the fix pass.
11. Female threads: any internal thread modeled in Step 6 (nut rebuild; tray drain) is built by stud-subtract; a plain bore plus a feature row naming the thread is the Pass 1 form for the drain plug. Grep of `build_parts\{nut,tray,base}.py` shows no `SubtractiveHelix` cut into a bore.
12. Params: every key a Step 6 script reads exists in `params.yaml` with `source:` and `status:`; no numeric literal in a new script duplicates a params value (Software Engineer code review lists the grep); leaf count stated; P-group tests pass.
13. Findings file covers: Pass 1 data (interference, clearance, mass estimate of printed base and frame, stock fit and consumption against `stock.on_hand`), each design issue discovered with its disposition (closed by assumption inside the step, or an input to Step 7 with the owner named), 80/20 CAD parts on disk versus missing.
14. Greps by the Manager: hazard terms (pinch, finger, crush, hand entry, 13854, knuckle, safety) in new and edited `build_parts`, `docs`, `tests` files outside the P22 allowlist return nothing; no printer, bed, nozzle, material key read by any Step 6 script; no `.FCBak` in `parts_cache` or `results`.
15. Background builds: PID, log path, expected finish in the gameplan Progress Log; each build log ends `BUILD_DONE`; success judged by log sentinel and fresh artifact mtime (A.3.4).
16. Word caps (tables counted without pipes, counted by script at close): Software Engineer tests 600, Loftsman definition 1800, Topologist cross-review 700, Software Engineer pre-build 500, Engineer findings 1200, Designer critique 1000, Software Engineer code review 500, Topologist gate 500. Overruns up to 20 percent are clerical (Design Notes 18). Each spawn prompt instructs a script count before finishing.
17. Gameplan edits at close: Step 6 row Complete; Progress Log row with PIDs and logs; Detail 6 outputs line; params leaf count; Design Notes row only if a ruling was made. Accumulator entries for Software Engineer, Loftsman, Topologist, Engineer, Designer.

## 9. Open items closed by assumption at open (no human input)

A. **Witness line of sight.** Geometry from `params.yaml` and the Step 3 solids: the holder flange (r 72.04, 8 thick) sits above the receiver rim inside the nut; the gap to read (1.5 to 13.126 mm) is axial, between flange underside and rim top, and the nut skirt (40 mm, threaded onto the receiver) surrounds it. The three washer windows open the washer pocket above the flange, not the gap. Ruling: the Loftsman states the line of sight (window in the nut skirt at the gap height, or a reading path through the existing windows) and the numbers; if a nut window is required it is part of the authorized nut rebuild (NT9). The ruling holds for Pass 1; Step 9 refines.
B. **plate_support 468 against the 488 mm clear span between rails** (rails 644, ends 488; footprint 644 x 608). The Loftsman states placement (for example plate supports seated on the rails' inside faces with printed brackets bridging 10 mm per end, or supports on the end-member line) and the Engineer reports the fit in findings. Disposition closes inside the step.
C. **Steady rest versus cradle.** Default is the steady rest from `rest.*` (3 rollers, 200 mm arm, 120 mm close handle, hold-open detent), with its column interface plane as a stated interface item. The column is upper-assembly scope; the rest is built as a free part at its detent height 310 mm.
D. **T-nut proxy.** One `tnut` solid sized from `profile.*` (neck under 8.0, cavity 16.5 wide x 6.908 deep), instanced 8 per bracket; counts in the frame result JSON (16 brackets, 128 T-nut instances, ASSUMED).
E. **Drain plug.** Pass 1 is a plain bore with a feature row naming the thread; the plug is a separate knob body inside `tray.FCStd`. Female thread, if modeled, by stud-subtract.
F. **Print orientation, layer direction, bed fit** are Step 8 items and appear in no Step 6 file.
G. **Collet label** stays a flat recess with text in the JSON (Step 5 Pass 1 acceptance). The Designer judges legibility in the renders and records a Step 9 item if needed.

## 10. Rules carried

Sonnet for every spawn; Opus for the Designer image gate only. No safety, pinch, finger, crush, hand-entry, ISO 13854 wording: a clearance is mechanical or usability. The printer is not a design input. T-nuts PZRT 3030 roll-in spring M6, 8 per bracket (ASSUMED). Frame 80/20 30-series (30-6060); a missing 80/20 CAD part is a finding, never a download. Clerical findings never block (Design Notes 18); FreeCAD run time is no constraint; builds go to the background. Female threads by stud-subtract (Design Notes 19). A params-duplicating literal is a defect fixed inside the step (Design Notes 20). Fuse first, boolean once; 7.1 topology data per part. A number that feeds a formula carries its basis (centre or edge, per side or diametral) and formula text in the table row (Design Notes 16).

## 11. Decisions for the orchestrator

None blocking. Two items to carry out as written: (1) spawn order starts with the Software Engineer (no `green_at_6` test exists at B6); (2) the Designer spawn uses `model: opus` and receives PNG paths only.
