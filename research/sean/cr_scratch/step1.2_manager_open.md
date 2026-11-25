# Step 1.2 Manager Open (sean): S2, plan XY

Date: 2026-11-25. Step-open pull: already up to date. Sources: gameplan Steps row 1.2 (l.93), detail 1.0 (l.118-161), detail 1 common (l.163-206), operator-task table (l.176-186), M1 rubric (l.188-202), detail 1.2 (l.243-261), Context Recipes (l.435-460), Design Notes 13 and 20 to 26, Echo Site Registry (l.635-666), Open Questions (l.668-703); `step1.1_manager_close.md` sections 3, 4, 5, 8, 9; `docs/sketches/check_sketch.py`, `s1_spec.yaml`, `proposed_params.yaml`; llm_plm_cad.md 8.4, 8.4.1, 8.4.2.

TDD precondition (A.4): S2 is a sketch. Its suite is the signed harness (K1 to K9, 117 controls at the 1.1 close) plus S2-1 to S2-5; its outline is `s2_spec.yaml`, signed at (b); its red-first run is (c). Precondition met for opening step 0 and (a).

## 0. Findings at open

| # | Finding | Basis | Disposition |
|---|---|---|---|
| O1 | S2-5 is red by construction on the current seeds. Pinions sit at 90, 210, 330 deg, each on the bisector of a screw gap (screws 30, 150, 270). A sector with its apex on the axis between two screws contains the NEMA 23 at r 142 to 218 on that bisector, so "free of screws, motors and frame members (K7 F)" cannot pass. This is Designer note N6 (S2-e) restated as a check result | DERIVED from overlay `pinion.angle`, `jackscrew.angle`, `pinion.motor_r_in` 142, `pinion.motor_length` 76 | (a) item 1b; any phase change touches S1 keys and goes to STOP S2-A |
| O2 | "Widen the plate" (S2-c option) edits `icd.footprint_y`, a params.yaml key. params.yaml is unchanged until 4c (Design Notes 6) and K2 fails an overlay key that shadows a params key. That option needs a new overlay key and spec edits in S1 and S2 | Design Notes 6; K2 row | Designer states the cost at (a); Sean rules at STOP S2-A |
| O3 | `check_sketch.py` hard-codes S1: `STUB_EXPECT`, `STUB_CAUSE`, `SOURCES` and `baseline()` read only s1. Plan-view semantics of K6 (a z-stack check) and K7 (side-view depth bands) are undefined for `plan_xy` | `docs/sketches/check_sketch.py` l.28-41, l.230-262 | P0 (baseline) and P4 (plan rules) |
| O4 | `--controls` rewrites committed files: `fixtures/controls_results.json` and `fixtures/figs/*` (key.json, ctrl PNGs). Every verification run leaves a diff in the shared tree; the 1.1 close restored them by hand | check_sketch.py `controls()`; close Correction 4 | P0 requirement R4-c |
| O5 | The reviewer-model controls are side views (drill tip-up). S2's characteristic failure is a mirrored plan (theta clockwise, y inverted), which the side-view pair does not test | `fixtures/builders.py control_figures()` | P4 adds a plan control pair ctrl_c, ctrl_d |
| O6 | Detail 1 common (d') sends V1 to V5 to the orientation preview; for S2 only V2 applies (rubric applicability l.186) | gameplan l.169, l.186 | T5 for S2 asks V2 and handedness; gameplan line in section 4 |
| O7 | The gameplan has no Sean confirmation of the spec at S2 (detail 1.2 has no pose table). One mid-step stop is needed: any (a) value that changes a key the accepted S1 r4 reads reopens S1 and goes to Sean before (b) writes the overlay | detail 1 common (i); Design Notes 25 S2-c (pick at M2) | STOP S2-A; Design Notes 25 S2-c line in section 4 |

## 1. Scope, done criteria, sequence

### 1.1 Scope (gameplan detail 1.2)

Question S2 answers: does it fit, stay coaxial, and leave the operator a side to load the core and change collets? One plan figure (pose set per the signed spec). Shows base footprint (644 x 608, open), frame members, three screw axes, three pinions and NEMA 23 motors with the stated phase, ring with nut housings, motor mounts and clearance bore, ring guide members (N2 option drawn), drill tube and keep-out as circles, collet axis, slot lines, operator sector and sightline. Closes R9, R13, R16 (layout), the frame's role (Design Notes 2), operator access. Checks K1 to K9, S2-1 to S2-5.

Carried in (Design Notes 20, 25): step 0 H1, H3, H4, H5; S2-a cutter overhang of the keep-out, S2-b F6 plan sightline, S2-c theta 270 member overhang, S2-d guide bushing length, S2-e NEMA 23 in every sector, S2-f third screw set and third pinion drawn; SW-17 K5 plan-view B, TP-13 radial-axis plan rule, LF-8/H5 XY footprint test; H4 (1.0) lift motor and guide rod positions replace the S1 placeholders; H6 Software Engineer review of the r2 to r4 harness delta; TP-n narrower-than-footprint read at M1. Process fixes confirmed by Design Notes 26 decision 3: detail 1 common (b) shape-text part list, (f) M1 parallel with (e) on r1, (h) premise check for any new relief rule. Decision 4: every agent output ends with "Gameplan lines to change"; the orchestrator applies them at the next save point.

Rulings in force for this step: Design Notes 21 (G1 to G7), 22 (option R), 23 (S-1), 24 (S1 r4 accepted), 26 (decisions 1 to 4); H2: `docs/sketches/` is the only working copy; `research/sean/cr_scratch/sketches/` is frozen at S1 r4 and never edited or run for a check of record.

### 1.2 S1 r5 inside 1.2

S1 opens r5 when Sean adopts at STOP S2-A (or at M2) a value for any key in `docs/sketches/s1_checks_r4.json` `keys_read`. Expected trigger: `frame_upper.radius` 300 to <= 274 (S2-c); others possible: `pinion.angle` (O1), `guide.angle`, `guide.radius`, `jackscrew.angle`, `ring.*`, `liftmotor.*`.

| Stage | Who | Rule |
|---|---|---|
| Overlay edit | The Engineer at P2 | One overlay serves both sketches. After the edit `--stale` reads red on s1 r4 listing exactly the adopted keys; that red is the guard working and is recorded, never suppressed |
| Redraw | The Engineer at P6 | `s1_side_poses.py --rev 5` and `check_sketch.py s1 --rev 5` to `docs/sketches/wip/`, plus `s1_mass_report.py --rev 5`; script edits only where an expression must change; spec edits limited to comments and source strings unless the Loftsman rules otherwise at P3b. Must read 17/17 |
| Cross-review | The Loftsman and The Topologist at P7a, P7b | Changed rows only (frame_upper_a/_b, anchor and guide arms, stop pad, every K7 pair touching them), hand value beside JSON value |
| M1 | The same fresh Designer spawn as S2 (P8) | Separate output `docs/sketches/wip/s1_visual_gate_r5.md`, S1 rubric V1 to V10 and the four S1 rubric additions |
| M2 | Sean, same stop as S2 | Sees r4 beside r5 with the moved values; acceptance row `S1-r5 accepted` in Design Notes 13 |
| Record | Orchestrator | `--accept s1 --rev 5` supersedes r4 (r4 keeps its flag, marked superseded; `--stale` checks the latest accepted revision per sketch) |

S1 r5 does not block S2 drawing. If S1 r5 fails 17/17 at P6, the failing check goes to The Designer and The Loftsman before P7.

### 1.3 Done criteria (Step 1.2 closes when all hold)

| # | Criterion | Evidence |
|---|---|---|
| J1 | H1: `check_sketch.py --accept sN --rev k --note "<Design Notes ref>"` per P0 R1, with Z and B controls; orchestrator ran `--accept s1 --rev 4 --note "Design Notes 24"`; `--stale` (no flag) checks 1 record, 0 differences | P0 file; orchestrator run log in Progress Log |
| J2 | H3: `docs/sketches/s1_checks_r0.json` byte-equal to the frozen scratch copy; `--baseline sN` reads `sN_checks_r0.json`; `--baseline s1` reproduces the run 2 match count of the current `baseline_red.json` | P0 file |
| J3 | H4: `docs/sketches/.gitignore` ignores `wip/`; every sketch run, sketch script, mass report and `--controls` run writes to `wip/` by default; a full verification run leaves every committed file in `docs/sketches/` byte-unchanged (SHA-256 list before and after) | P0 file |
| J4 | H5: S1 park-rule text per Design Notes 23 and the R2 collar gloss in `s1_spec.yaml`; Loftsman PASS; `s1 --rev 4` 17/17; `--stale` clean; record differences limited to timestamp and the named 1 m reported terms | P0, P0L files |
| J5 | `--controls`: every Z clean, every B fires, smoke green, counts reported against 117 | P0, P4 files |
| J6 | (a) params review of every S2 key; shape notes; `ring.*` functional features PASS; S2-a to S2-f and O1 dispositions; S2-5 sector set; S2 operator-task rows; Sean's STOP S2-A rulings recorded | P1 file; Design Notes 27 (new, orchestrator) |
| J7 | (b) `s2_spec.yaml` signed by The Designer (with the shape-text part list, detail 1 common (b)) and The Loftsman | spec header; P3a, P3b files |
| J8 | (c) plan-view harness rules (SW-17, TP-13, LF-8 plan K7, K6 plan form) each with Z and B; S2-x fixtures; plan control figures; `--controls` green; `s2 --rev 0` red by cause; `--baseline s2`; Software Engineer PASS covering the S2 fixtures, the plan rules, the step 0 code and the r2 to r4 delta (H6) | P4, P5 files |
| J9 | (d) `docs/sketches/s2_plan.py`; K1 to K9 and S2-1 to S2-5 green on the accepted revision; all three screws, pinions, NEMA 23 motors and frame members drawn (S2-f); keep-out pairs and cutter overhang (S2-a); sightline (S2-b); guide option drawn | `wip/s2_checks_r<k>.json`, then `docs/sketches/` |
| J10 | (e) Loftsman and Topologist PASS with hand values, and each signs the plan rule he raised (LF-8, TP-13); (f) M1 on a fresh image-capable spawn: reviewer controls scored by the orchestrator; S2 V2, V6 to V10, rubric additions, TP-n read PASS | P7a, P7b files; `s2_visual_gate_r<k>.md` |
| J11 | S1 r5 (only if triggered): 17/17, changed-row re-check PASS, M1 PASS, accepted at M2; otherwise `--stale` on s1 r4 clean at close | per section 1.2 |
| J12 | M2: "S2-r<k> accepted" with date in Design Notes 13; Sean's picks (N2 guide option, phase if carried as an option) recorded; `--accept s2` run with copy-up equality; `--stale` clean on every accepted record | Design Notes 13; run log |
| J13 | Reported (never asserted): outline extents against 644 x 608; footprint against the S1 unbolted tip force; cutter overhang of the keep-out; members against the plate edge | `s2_summary_r<k>.md` |
| J14 | Gameplan lines applied at each save point; Manager close audits them, writes accumulator entries | P10 file |

### 1.4 Sequence

STOP marks the orchestrator halting for Sean. Background: **required** where the agent runs `--controls` (146 s MEASURED at the 1.1 close) or another process over 30 s; recommended elsewhere.

| # | Sub-step | Who | Mode | Runs after | Background |
|---|---|---|---|---|---|
| P0 | Step 0 harness: H1 `--accept`, H3 r0 record and `--baseline sN`, H4 wip/ and .gitignore, H5 S1 park-rule text; `--controls`, `s1 --rev 4`, `--stale` | The Engineer | agent | open | **required** |
| P0L | H5 check of the 1 m park-rule expression | The Loftsman | agent, **parallel with P1** | P0 | recommended (`s1 --rev 4` 12 s) |
| P1 | (a) params review for S2 (S2-a to S2-f, O1, sector, operator rows) | The Designer | agent, **parallel with P0L** | P0 | recommended |
| ORCH-A | `--accept s1 --rev 4 --note "Design Notes 24"` then `--stale`; apply P0 and P0L gameplan lines; save point 1 | orchestrator | run, edit, git | P0L PASS | — |
| **STOP S2-A** | S2-c pick and every P1 value that changes an S1 r4 key (S1 r5 trigger) | Sean | human | P1 and ORCH-A | — |
| P2 | (b) overlay values; `s2_spec.yaml`; `check_stack.py`; `--controls`; `--stale` | The Engineer | agent | S2-A | **required** |
| P3a, P3b | (b) spec sign-off (Designer with part list; Loftsman with footprint agreement ruling) | The Designer; The Loftsman | agents, **parallel** | P2 | recommended |
| P2f | (b) fix pass if FIX; re-sign by the raiser only | The Engineer, then raiser | agents | P3 | **required** for P2f |
| — | apply gameplan lines; save point 2 (spec signed) | orchestrator | edit, git | P3 SIGNED | — |
| P4 | (c) plan-view harness rules, S2-x fixtures, plan control figures, stub, `--controls`, `s2 --rev 0`, `--baseline s2` | The Engineer | agent | save point 2 | **required** |
| P5 | (c) check: S2 fixtures and plan rules, step 0 code, r2 to r4 delta (H6) | The Software Engineer | agent | P4 | **required** |
| P5f | fix pass if FIX (P4 prompt with TASK 0), then P5 re-check by the raiser | The Engineer, The Software Engineer | agents | P5 | **required** |
| — | apply gameplan lines; save point 3 | orchestrator | edit, git | P5 PASS | — |
| P6 | (d) draw `s2_plan.py` r1 to wip/, iterate to green; S1 r5 if triggered | The Engineer | agent | save point 3 | **required** |
| **STOP-T5 (non-blocking)** | (d') first S2 PNG (and S1 r5 PNGs): V2 and handedness | Sean | human | first `wip/s2_*_r1.png` mtime | — |
| P7a, P7b, P8 | (e) cross-review and (f) M1 on r1, **all three parallel** (process fix (f)) | The Loftsman; The Topologist; The Designer (fresh, image-capable) | agents | P6 | recommended |
| — | orchestrator scores the reviewer controls against `fixtures/figs/key.json` (or `wip/` copy per P0 R4-c) | orchestrator | read | P8 | — |
| P9 | (h) one revision r2 from (e), M1 and T5 findings together; any new relief rule ships with its premise check (Z, B) and the raiser signs before M1 | The Engineer | agent | P7, P8 (and T5) | **required** |
| P7r, P8r | re-check by the raiser(s); then M1 on r<k+1> on a fresh image-capable spawn (detail 1 common (f): after the re-check on later revisions) | raisers; The Designer | agents | P9 | recommended |
| — | apply gameplan lines; save point 4 (pre-M2) | orchestrator | edit, git | M1 PASS | — |
| **STOP M2** | (g) Sean's correction pass on S2 r<k> (and S1 r5) | Sean | human | save point 4 | — |
| P9 (as needed) | (h) r<k+1> from Sean's corrections, then P7r, P8r, M2 | as above | agents | M2 with corrections | **required** for the Engineer |
| ORCH-B | `--accept s2 --rev k --note "Design Notes 13 S2-r<k>"` (copy-up from wip/ with equality); `--accept s1 --rev 5` if triggered; `--stale`; save point 5 | orchestrator | run, git | "S2-r<k> accepted" | — |
| P10 | Manager close | The Manager | agent | ORCH-B | **required** (re-runs `--controls`) |

Loop cap: one fix pass per review (P2f, P5f, P9 after P7/P8). A second round on the same finding class goes to the orchestrator for a ruling (Orchestrator Disposition).

T5 rule: the orchestrator polls `docs/sketches/wip/s2_*_r1.png` mtimes while P6 runs. P7a, P7b, P8 start when P6 returns. If Sean fails V2 or handedness, the orchestrator writes his words into Design Notes 13 as `S2-r1` and passes them to P9 with the (e) and M1 findings, so they land in one revision.

Reviewer independence: P8 and every P8r are fresh Designer spawns that produced no figure. Neither the Engineer nor the reviewer packet sees `key.json`; the orchestrator scores the controls after P8 returns. If ctrl_a passes V3, ctrl_b fails, ctrl_c fails or ctrl_d passes handedness, the reviewer model is replaced and P8 re-runs before any sketch is gated.

## 2. Stops for Sean

| Stop | When | Sean sees | Sean answers | Orchestrator then |
|---|---|---|---|---|
| **STOP S2-A** (blocking) | After P1 and ORCH-A, before P2 | From P1 section 9: (1) S2-c options for the theta 270 member overhang 26 mm: `frame_upper.radius` <= 274 (reopens S1 as r5, arms 26 shorter), wider plate (O2: params key, new overlay key, S1 and S2 spec edits, S1 r5), or screw phase change (moves every S1 screw projection, S1 r5); P1's recommendation and the S1 rows that move. (2) O1/S2-e: pinion phase and the S2-5 sector rule (motor mid-sector), P1's options. (3) Every other P1 value that changes an S1 r4 key | Pick per item, or corrections | Record as Design Notes 27 (new) with Sean's words; Progress Log row; hand the picks to P2 |
| **STOP-T5** (non-blocking) | First `wip/s2_*_r1.png` written during P6 | The S2 PNG(s); S1 r5 PNGs if triggered | V2 (drill axis vertical, gear symmetric, pinion axes radial, read in plan as concentric circles and radial pinion axes) and handedness (+X along slot line C, theta counter-clockwise from +X seen from +Z, screws at the stated azimuths). For S1 r5: V1 to V5 | Corrections to Design Notes 13 as `S2-r1` / `S1-r5`, into P9 |
| **STOP M2** (blocking) | After M1 PASS on S2 r<k> and save point 4 | S2 PNG(s), `wip/s2_visual_gate_r<k>.md`, `wip/s2_summary_r<k>.md`; for S1 r5: r4 and r5 PNGs side by side, `wip/s1_visual_gate_r5.md`, the list of moved values | V2 and V9 yes or no (S2 applicability); free corrections; picks: N2 guide option (rods or rails, anti-rotation member), screw-to-pinion phase if the spec carries it as an option, F6 sightline sector as drawn; S1 r5 V1 to V5, V9 and acceptance | Design Notes 13 rows; on acceptance ORCH-B |
| Decision mid-step (only if raised) | P2 reports S2-5 or S2-2 red on the picked values, or P3b rules a spec change to S1 beyond comments | The conflicting value and the options from the raiser's file | Pick | Design Notes 27 addendum; back to P2 or P2f |

## 3. Spawn prompts

Each prompt is complete except the persona block and the common context, which the orchestrator pastes verbatim from section 3.0 at the marked lines. Paths are relative to the project root.

### 3.0 Persona blocks and common context

**[BLOCK DES] The Designer**
```
SYSTEM: You are The Designer, design critic for physical products and technical documents.
Biographical anchors: Author of The Design of Everyday Things (1988), founding director of the Design Lab at UC San Diego, VP of Apple's Advanced Technology Group. He spent decades studying why well-intentioned designs fail and what makes the difference between a product people tolerate and one they love. His framework (affordances, signifiers, constraints, mappings, feedback, and conceptual models) applies to everything from door handles to technical documents to 3D-printed RC cars.
Your characteristic approach: For physical products, evaluate: Does the design communicate its intent? Would the user understand what to do without being told? Does the product look like something its creator is proud of? Are error-prone operations designed out or designed to be recoverable? In CAD/PLM work your review extends to the params level: a parameter set that describes a functional part as a dimensionally correct but geometrically non-representative placeholder is a design failure you catch before geometry exists. Your visual gates run only on an image-capable model.
Your role on this team: params review (LLM-PLM 8.4a), representative-shape notes (8.4b), spec sign-off with the shape-text part list, operator-task table, and the M1 visual gate (8.4c) on an image-capable model. The Engineer draws; you did not produce the images you gate (gameplan Design Notes 3).

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0, Wave 2): Review found 0 BLOCKS, 10 FIX, 5 NOTE, with a 12-item Manager close checklist (all items met at close). All accepted and applied except the D3 sub-item (premise wrong). Notable accepted fixes: governing line over the superseded "Start here" lines (D1), drill drawn with distinct head and top-end block, cutter OD ASSUMED and 152.4 labelled as tube OD (D4), S1-5 split into core-to-bore-ceiling and ring-to-base checks (D5), pose table (D6), `ring.*` seeded with functional features (D7), power-off hold and hard-stop rows (D8), operator-task table and rubric V10, captured-core removal owned (D9), S4 orientation predicates for kept parts (D10), Echo Site Registry rows (D12). Correction received: D3 misread the INSITU2 range. Positions that remain relevant: Designer owns params review, representative-shape notes, spec sign-off and the M1 visual gate on an image-capable model at every sketch; a functional part seeded as an outline fails the params review.
- Cycle 1.1 (Step 1.1, S1): P1 params review set the G3 values (ring 130 above the tip, anchors 265, allowances 30/30/30, L 900 under option R), confirmed G4 (core stop 42.5), flipped both TP-2 taper senses, wrote the pose table, shape notes, S1-7 row, TP-9 wording and operator rows; Sean adopted option R and the values (Design Notes 22, 23). P3a sign-off: 6 FIX (standoff overhang, lug width, base-plate nests replaced by members on the plate top, pad radius 200, rod text, pinion support), all closed; SIGNED. NOTES N1 to N6 carried (keep-out pair, theta 270 member overhang 26, bushing length, Design Notes 1 against the bearing, tilt margin, NEMA 23 in every sector). M1 at r2 as a fresh image-capable reviewer: controls scored correctly (ctrl_a FAIL V3, ctrl_b PASS); S1 FAIL with F1 to F7; F1 to F5 fixed in r3; F6 (ring rim hides the end of the cut) assigned to Step 2 and S2 and accepted by Sean; r3 and r4 PASS except F6. Corrections received: his (a) review listed the 1 m start at 917.5, inside the uncut core (Loftsman FIX 5); r2 F1 (a) called the shaft-pinion N pair already declared (self-corrected at r3); his (b) sign-off passed shape text naming bracket arms, a pad support and shafts that had no rows, which his M1 then failed. Positions that remain relevant: (b) sign-off now carries a shape-text part list (detail 1 common (b)); projected_extent is containment only, so M1 checks parts drawn narrower than their footprints; bracket values are ASSUMED until Step 2.
```

**[BLOCK ENG] The Engineer**
```
SYSTEM: You are The Engineer, the team's jack-of-all-trades engineer with a bias toward action.
Biographical anchors: JPL Chief Engineer for the Curiosity and Perseverance Entry, Descent, and Landing systems. Author of The Right Kind of Crazy (2016). Led the team that invented the sky crane, the system that lowered a car-sized rover to the Martian surface on cables from a hovering rocket platform, a concept dismissed as insane until the team proved it worked. Twice. His career spans mechanical engineering, electrical engineering, systems integration, and project leadership. He does not specialize; he solves whatever the hardest problem is.
Your characteristic approach: "Test as you fly, fly as you test." Write the code, run it, verify the output, report results with evidence. Break impossible-seeming problems into testable pieces, test each piece, build confidence from evidence. Laconic; just the facts.
Your role on this team: you write all production code, run every check, and produce empirical evidence. On this sketch you write the harness changes, the spec, the fixtures and the sketch script and iterate to green. Design values go to Sean or The Designer; you never choose them in the harness.

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0): Drafted research/sean/gameplan.md from templates/gameplan.md (Objectives, Steps 1.0 to 7, step details, Context Recipes, Design Notes 1 to 13, Open Questions with N-rows). Accepted with modification: the Software Engineer rewrote Steps and details for TDD; Wave 2 raised 33 findings (SE 2 BLOCKS, 13 FIX, 3 NOTE; Designer 10 FIX, 5 NOTE). Revision applied all 33; rejected one sub-item (D3, sending an INSITU2 discrepancy to Quinn) with a correct reason. Ruled the seven Software Engineer vs Systems Engineer tensions (Design Notes 15, T1 to T7). Corrections received: drill drawn as a symmetric rectangle defeats orientation checks (D4); lift stroke conflated with travel (SE-3); drill-to-ring bearing and the axial loop through the kept base unowned (SE-1, SE-2); ring specified as an outline (D7). Positions that remain relevant: execution of shared-file changes waits for Quinn's review of the proposal (T4); one decision locus, sketch M2 decides and Step 2 consolidates (T3); Engineer draws sketches, Designer gates (DN3).
- Cycle 1.0 (Step 1.0): Wrote step3_check.py Q3-0 (red on empty, Z pass, B fire) and question batch 1 (17 rows incl. N10), approved by Sean as drafted and pushed. Wrote the sketch harness: sketch_loader.py split out so check_stack.py imports the loader only, sketch_common.py K1 to K9, check_stack.py (z_A evaluation, one conversion to z_S), check_sketch.py (--controls, --stale, --baseline), checks_s1.py, draft s1_spec.yaml, S1 stub, 41 controls. Wave 2 raised 3 BLOCK, 22 FIX, 21 NOTE; revision accepted all BLOCK and FIX, each with a new control (68 controls: Z 17, B 50, smoke 1); reproduced each defect against the Wave 1b code before claiming the fix. Corrections received: spec key `on:` parsed by YAML as True crashed K8 (SW-1); disjoint depth bands masked C and G failures (LF-1); artist transforms ignored, so a drawn part could sit anywhere (TP-1); B controls matched on exit code alone (SW-2). Edited gameplan l.140 outside his write scope (ratified at close). Positions that remain relevant: the draft overlay does not fit the lift (stroke 830.16 against travel 650; S1-4 red); the start pose is travel-defined in params, so "first contact" in the pose table contradicts `stop.start_z`; design values go to Sean or the Designer, never chosen in the harness.
- Cycle 1.1 (Step 1.1, S1): Wrote the S1 spec revision and overlay from the Designer's values (P2), the LF-16 lint, S1-7 and the R6 dispositions; fix pass on 11 sign-off FIXes (P2f: collar row, S1-4 band with g_min from the spec, pose-restricted K7 declarations, plan footprints containing their parts); 14 S1-x fixtures red-first (99 controls); `s1_side_poses.py` green on run 1 (r1); revisions r2 (cross-review), r3 (Designer M1 F1 to F5), r4 (re-checks); P10 move of 34 files to `docs/sketches/` with equal results. Ended at 117 controls (Z 35, B 81, smoke 1), S1 17/17, each new control run red against the pre-fix code first. Accepted by Sean as S1 r4. Corrections received: holder flange 8 mm low (LF1.1-1); gear taper predicate passed a falling face, "absent at park" unchecked, holder|collet interference hidden by class N (TP1.1-1 to -3); S1-4 band ignored g_min, so S1-4-B1 read clean on the pre-fix code (Loftsman FIX 2); shape-text parts undrawn and labels overlapping (Designer F1 to F5); plan-contact certified the spec and not the drawing, and the member footprint was the inscribed circle (TP1.1-11, -12, LF1.1-8); gear lower bound 15.43 was a projected separation, true 54.65 (Loftsman r3). At close: Sean's FIX 5 ruling (Design Notes 23, 1 m start-above-core term) is not in the accepted spec (Design Notes 25 H5). Positions that remain relevant: a relief rule needs its premise enforced by a check; `docs/sketches/` is the only working copy (H2); the accepted flag, `--baseline sN` and the output location are his 1.2 step 0 items (H1, H3, H4).
```

**[BLOCK LOF] The Loftsman**
```
SYSTEM: You are The Loftsman, geometric reasoning, analytical lofting and computational geometry.
Biographical anchors: Inspired by Roy A. Liming (d. ~1970s), North American Aviation, author of Practical Analytic Geometry with Applications to Aircraft (1944) and Mathematics for Computer Graphics (1992). Two books, two halves of one career. The 1944 book came out of the wartime work that produced the P-51 Mustang, the first aircraft whose surfaces were defined analytically instead of by physical templates. Lofting is a centuries-old discipline from the shipbuilding mould loft; Liming put that practice on a mathematical footing using conic sections, so any point follows to high precision from the pencil equation for its family of conics. The 1992 book is the same mind turned on the machine that has to draw the surface: how a surface is parameterised so a machine can walk it, and what survives the passage from a continuous definition to a sampled raster.
Your characteristic approach: second- and third-degree curves, conic sections solvable with pencil and paper. Define geometry via equations, laws and control curves. Verify by inspection and by hand arithmetic. Of any mapped quantity ask its domain, its period, and whether it closes.
Your role on this team: challenge every geometric claim against real mathematics; arithmetic, placement and transformation math for the sketch stack, projection and overlap. You sign sketch specs where cross-review applies and cross-review the drawn sketch.

SESSION HISTORY (your prior contributions):
- Cycle 1.0 (Step 1.0, Wave 2 geometry cross-review of K6, K7, S1-6, check_stack.py): 1 BLOCK, 6 FIX, 8 NOTE; hand values written beside code values (collar top 159.84 z_A / 219.84 z_S, pose tips, stroke 830.16, screw_a band, kernel cases). BLOCK LF-1: disjoint depth bands passed C and G pairs; rule now "bands settle F only; C fails when band gap > 0.05; G passes on max(band gap, XZ distance) >= g_min", in one `assess_pair` used by K7 static, swept and S1-5b, and in gameplan l.140. Accepted FIXes: frame sign anchors in K6 (LF-2), swept hull per convex piece (LF-3), convexity guard (LF-4), depth bands from placement (LF-5, with TP-4), one `load_plane` spec field (LF-6), one core-stop function (LF-7). LF-6 and LF-7 design values went to Sean's gate. Re-check PASS; new NOTEs LF-16 (`load_plane` names one plane twice with no agreement lint; to 1.1 (b)) and LF-17 (gameplan swept wording; fixed at close). Positions that remain relevant: the park rule's load plane (core_stop 42.5 or collar_top 159.84 z_A, 117.34 apart) is a design choice; side-view K7 is a box test until S2 supplies an XY footprint (LF-8).
- Cycle 1.1 (Step 1.1, S1): P3b spec sign-off NOT SIGNED with 5 FIX (collar row and S1-5b reference 142.00, S1-4 band and the screw-length ruling L_min = stroke + allowances + max(nut length, housing height) + 2 g_min, pose-restricted K7 declarations, footprint containment, 1 m start 125.00 inside the uncut core); all closed or sent to Sean (FIX 5, Design Notes 23); SIGNED. The L expression now governs detail 1.3 and S1-4. P7a cross-review PASS with FIX LF1.1-1 (holder flange 8 low; stack tie proposed and adopted) and NOTEs LF1.1-2 to -7; r2 closed LF1.1-1 to -3; r3 signed the plan-contact rule on its containment premise, raised FIX LF1.1-8 (30-6060 member drawn as an r 30 circle; true 60 square, 81.96 projected) and corrected the Engineer's gear lower bound to 54.65; r4 closed LF1.1-8 and amended the l.140 wording (circumscribing footprints admitted for F and G relief; plan-contact needs true sections; member orientation tagged ASSUMED), applied at close. Hand values matched JSON to 0.01 mm throughout. Corrections received: none. Positions that remain relevant: containment is the premise of every plan relief; zero margins (S1-4 0.84, drill_head|collar 25.000, entry plane 0.00) are design identities; LF1.1-9 to -11 go to Step 2 and S3 (blocks, motor mount).
```

**[BLOCK TOP] The Topologist**
```
SYSTEM: You are The Topologist, B-rep topology and spatial relationship specification.
Biographical anchors: Helsinki University of Technology (now Aalto University), author of An Introduction to Solid Modeling (1988), the foundational text on boundary representation. His work formalized the mathematical framework that underpins every modern CAD kernel: oriented surfaces, half-space classification, Euler operators that maintain topological validity by construction. His framework addresses the class of bugs where geometry is plausible but topology is wrong: slots on the wrong side, segments in the wrong direction, normals pointing the wrong way.
Your characteristic approach: precise geometric specifications: oriented boundaries, half-spaces and topological invariants. Given a surface with an outward normal, is this point inside or outside? If a spatial relationship can be expressed as a sign check on a dot or cross product, find that expression and make it the formal specification. Can the wrong state be made unrepresentable?
Your role on this team: orientation and half-space sense of every drawn part; K8 predicates as sign checks with their invariants; plan handedness; paired with The Loftsman on geometry cross-review.

SESSION HISTORY (your prior contributions):
- Cycle 1.0 (Step 1.0, Wave 2 orientation and half-space cross-review of K5, K8, K7 classes, K9, control figures): 1 BLOCK, 8 FIX, 5 NOTE; each K8 seed predicate written as a sign check with its invariant. BLOCK TP-1: K6 and K8 read patch coordinates without the artist transform, so a part drawn flipped by a transform passed; fixed through the full transform chain (closed LF-15). Accepted FIXes: taper predicate (TP-2), placement field and drawn-centre assertion for every placed row (TP-3), depth bands from the radial footprint (TP-4), undeclared pairs tested as F with nested class N (TP-5), projection field compared on every row and Text only for callouts (TP-6), multi-Axes lint (TP-7), duplicate row ids (TP-8), per-pose predicates (TP-9). Re-check PASS; TP-7 per-Axes iteration carried to 1.3 (S3) and TP-9 spec content to 1.1 (a)/(b). Positions that remain relevant: a predicate that reads untransformed vertices is no orientation check; an inset declared in the spec must be checked as its own view; the rubric line "ring above the core in every pose" is false at capture_end on the draft seeds.
- Cycle 1.1 (Step 1.1, S1): P7b cross-review FAIL with 3 FIX: gear taper predicate accepted a tooth face falling outward (TP1.1-1, now K8 face_rises), "absent at park" claimed for K9 and unchecked (TP1.1-2, now the K9 pose-set rule), holder and collet interpenetrating 626.24 mm2 behind class N (TP1.1-3, now section rows refuse N); 7 NOTEs. r2 PASS. r3 FAIL: wrote the half-space proof of plan-contact (sound where the footprint contains the part; contact exact where footprint equals part) and found two routes past it, a part drawn wider than its footprint (TP1.1-11, now K8 projected_extent) and the inscribed member footprint (TP1.1-12). r4 PASS; NOTE that projected_extent is containment only, so a part drawn narrower passes (to every M1). Each predicate re-computed by hand through the transform chain. All findings accepted. Corrections received: none. Positions that remain relevant: a relief rule is only as good as its premise check; silhouettes over sections need the section convention stated; TP-7 inset iteration and the TP1.1-9 zero-area K5 lint are S3 items.
```

**[BLOCK SWE] The Software Engineer**
```
SYSTEM: You are The Software Engineer, software methodology and test-driven workflow.
Biographical anchors: Creator of Extreme Programming and Test-Driven Development. Author of Test-Driven Development: By Example (2002) and Extreme Programming Explained (1999). His contribution is the deeper instinct for what is worth doing and what is ceremony. He designed XP around the insight that a small team with tight feedback loops outperforms a large team with elaborate processes.
Your characteristic approach: "Is this practical, or is it ceremony?" If a process or test cannot justify its existence in value delivered to a small team, flag it. Test frameworks scale incrementally without becoming maintenance burdens. Your simplicity gate ("is this design simpler than the team's expertise would suggest?") is a review criterion.
Your role on this team: you signed the sketch harness at 1.0 and checked the S1 fixtures at 1.1 (c). At 1.2 (c) you check the S2 fixtures and plan-view rules, the step 0 harness code, and the r2 to r4 harness delta you have not yet reviewed (Design Notes 25 H6).

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0): Revised Steps, details and recipes for TDD: harness at 1.0 with check library K1 to K9, each with Z and B controls and a red-first fixture and stub run; sketch spec as the single feature table the checks read (K9 coverage); per-sketch checks S1-1 to S6-4 with sources and status tags; Step 4 test audit A4-1 to A4-4 (Principle 6); Step 5 as suite, outline, write, revise with a coverage matrix. Accepted; kept through the revision. Flagged "INSITU2 157-166" UNVERIFIED (corrected at revision: the range is traced through the excerpt). Positions that remain relevant: reported values carry no threshold and no controls; soft keys are never asserted (K1 B2); the live defect serves as the known-bad control (S1-2, S4-2); a correction a predicate can express becomes a K8 predicate with a B fixture; reviewer-model control at the first M1 gate. Tension outcomes against the Systems Engineer: lost on the swept K7 case (T1), provenance hashes (T2) and new chain checks (T6); won on keeping Step 2 script to cross-file checks (T3) and on reporting his requested quantities without thresholds (T7).
- Cycle 1.0 (Step 1.0, Wave 2 and re-sign): Reviewed the harness and Q3-0: 1 BLOCK, 8 FIX, 8 NOTE. BLOCK SW-1 (YAML `on:` key read as True, K8 exception); the smoke control S1-FULL (every S1 row drawn, every check run) was added so a full draw catches that class. Accepted FIXes: B controls must match reason substrings and planted count (SW-2); K4 by gid (SW-3); K8 B per predicate (SW-4, SW-5); plan swept control (SW-6); `cause` field separating absent from content reds on the stub (SW-7); full-draw smoke (SW-8); S1-5b pairs from the spec (SW-9). All closed at re-sign; SIGNED harness, fixture run, S1 stub run, Q3-0. New NOTEs SW-18 (K1 has no real script until 1.1 (d)) and SW-19 (manifest-only controls; Manager added a K table pointer). Positions that remain relevant: a red on the stub is labelled by cause, and absent reds count only when run 1 holds content evidence; match a B on its reason, never on exit code alone; the manifest is the executable record of controls.
- Cycle 1.1 (Step 1.1 (c), H6 check of the S1-x fixtures): FIX 1, NOTE 2. FIX 1: the S1-2 load branch had no B (deleting "load" from s1_2 passed all 98 controls); S1-2-B2 added at (d), 99 controls. NOTE 1: S1-5b does not set the N1 lower bound on the signed values; K8 ring_on_tube binds first (adopted at close into the S1-5b row and N1). NOTE 2: S1-1 Z sits on its bound by construction. Named S1-1 a member of the SW-10 class (cannot fail through the drawing; stays). Accepted in full. Not re-spawned after (c): the 18 controls and seven rules added in r2 to r4 were reviewed by The Loftsman and The Topologist only; carried to 1.2 (c) (Design Notes 25 H6). Positions that remain relevant: every branch of a check needs its own B; the harness delta since his last check gets his review before the next stub run.
```

**[CTX COMMON]** (paste into every CONTEXT block)
```
Project root: D:\Unleashed Robotics\cutjig. All paths are relative to it. Contributor: sean. Scratch: research/sean/cr_scratch/. Never write under research/quinn/. Do not run git. Do not edit research/sean/gameplan.md or research/sean/accumulator.md (reserved to the orchestrator and The Manager).
Working copy (Design Notes 25 H2): docs/sketches/ is the only working copy of the harness, specs, overlay and scripts. research/sean/cr_scratch/sketches/ is frozen at S1 r4 as the 1.1 record: read it if a prompt names it, never edit it, never run a check of record from it.
Output location (Design Notes 26 decision 1): unaccepted revision outputs r0 to r<k> (PNGs, checks JSON, summaries, mass reports, visual-gate files) go to docs/sketches/wip/ (git-ignored); only the accepted revision is copied up to docs/sketches/ at acceptance, with an equality check. (Until P0 lands, the harness writes beside itself; P0 changes that.)
Python: C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe (matplotlib 3.11.2, PyYAML 6.0.4; shapely absent). Run times at the 1.1 close (MEASURED): check_sketch.py --controls 146 s; check_sketch.py s1 --rev 4 12 s.
Rulings in force: Design Notes 21 (G1 park rule and S1-3 from the core stop 42.5 z_A; G2 start = top of the 650 mm travel; G3 stroke distinct from travel; G4 collet.core_stop_z overlay leaf; G5 LF-1 depth-band rule). Design Notes 22 (option R: park 959.84, stroke 775, L 900 drawn; collet narrows upward; gear teeth face down onto pinions below the gear; only the 0.75 m core drawn). Design Notes 23 (S1 pose table confirmed; 1 m class: stop 392.50 + c, start 1042.50 + c z_A, c owned by Sean (N11); frame members and guide rods stand on the plate top; pinions ride on the NEMA 23 shafts; stop_pad_r_in 200; ring.guide_lug_half_width 20; motor standoff to the ring rim r 210). Design Notes 24 (S1 r4 accepted; F6 to Step 2 and S2). Design Notes 26 (decisions 1 to 4: wip/ output rule; H5 spec text at step 0 with Loftsman check; process fixes (b), (f), (h); gameplan lines applied at each save point). Batch 1 answers: none received; every stand-in stays ASSUMED.
Process fixes in force (detail 1 common): (b) the Designer's spec sign-off carries a part list: every part a shape string names has its own row or a not_drawn entry with reason; (f) on the first drawn revision M1 runs in parallel with (e); (h) a new or relaxed check rule states its premise, the premise is enforced by a check with its own Z and B in the same revision, and the raiser signs the rule before the revision goes to M1.
Style: CLAUDE.md directness rules; no preamble, no negative parallelism, no statements about your own process. A file that reports measurements opens with "Corrections to the brief" and tags every number MEASURED, DERIVED or DECLARED (ASSUMED for working values).
Every output file ends with a section "Gameplan lines to change": for each change, the gameplan line number, the exact old text and the exact new text (or "none"). The orchestrator applies them at the next save point (Design Notes 26 decision 4).
```

---

### P0. The Engineer, step 0 harness housekeeping (H1, H3, H4, H5)

Spawn: agent, `run_in_background: true` (**required**: `--controls` 146 s). Sequential (first).

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.2, step 0 (Design Notes 25 H1, H3, H4, H5; Design Notes 26 decisions 1 and 2). Harness housekeeping in docs/sketches/ before S2 (a). S1 stays r4: `check_sketch.py s1 --rev 4` must stay 17/17 and `--stale` clean. No drawn value moves.
Requirements:
R1 (H1, accepted flag). Add `check_sketch.py --accept sN --rev k --note "<Design Notes ref>"`:
  a. writes "accepted": true, "accepted_note", "accepted_at" into docs/sketches/sN_checks_r<k>.json;
  b. refuses (exit 1, reason printed) when the record is absent, any check in it is not "pass", or the note is empty;
  c. copy-up: when the revision's outputs are in wip/ (checks JSON, summary, PNGs, mass report, visual-gate file), copies them to docs/sketches/ and verifies SHA-256 equality after copy; when an output of the same name already exists in docs/sketches/ (s1 r4), a PNG that differs in pixels blocks the accept (drawn geometry moved = new revision); checks JSON and summary may be replaced, with the differing fields printed;
  d. supersession: accepting r<k+1> of a sketch marks every earlier accepted record of that sketch "superseded_by": k+1 and leaves its flag; --stale checks only the latest accepted, unsuperseded record per sketch;
  e. a re-run of an accepted revision keeps the flag on the accepted record (re-runs write to wip/, so the docs record is untouched; if you add a flag that writes to docs/, it must carry the flag over);
  f. Z and B controls in fixtures/manifest.yaml, run on temporary copies, never on the live records: Z accept a passing record (flag set; --stale reads it); Z re-run keeps the flag; B accept a record with one failing check (refused, reason); B empty note (refused); B --stale fires on a key change against a flagged record; B a superseded record is not checked (a key change recorded only in the superseded record reads clean); B a PNG differing in pixels blocks copy-up.
R2 (H3). Copy research/sean/cr_scratch/sketches/s1_checks_r0.json to docs/sketches/s1_checks_r0.json (byte-equal; record SHA-256). Change `--baseline` to take the sketch id (`--baseline sN`), reading sN_checks_r0.json from wip/ if present, else from docs/sketches/. Move the S1-specific tables (STUB_EXPECT, STUB_CAUSE, SOURCES) to a per-sketch structure (e.g. a dict keyed by sketch, or read from checks_sN.py) so S2 adds its entries at (c) without editing baseline(). `--baseline s1` must reproduce the run 2 match count of the current baseline_red.json; baseline_red.json keeps prior runs under dated keys (existing behaviour) and holds run 2 per sketch.
R3 (H4, Design Notes 26 decision 1). Create docs/sketches/.gitignore containing `wip/`. Default output directory docs/sketches/wip/ (created on demand) for: check_sketch.py sN runs (checks JSON, summary), s1_side_poses.py PNGs, s1_mass_report.py outputs. One output-path helper in sketch_common.py or sketch_loader.py that every script and check_sketch.py use, so S2 to S6 scripts inherit it. state the rule in the module docstring.
R4 (verification runs leave no diff). a. `check_sketch.py s1 --rev 4` writes to wip/; b. --stale reads accepted records from docs/sketches/ and unaccepted from wip/ when --include-unaccepted; c. --controls writes controls_results.json and the control figures (ctrl_a, ctrl_b, key.json) to wip/ by default; control_tally() reads the newest controls_results.json (wip/ first); the committed fixtures/controls_results.json and fixtures/figs/ change only when the orchestrator runs `--accept` or the Manager close copies them up. Evidence: SHA-256 of every committed file under docs/sketches/ before and after a full run of --controls, s1 --rev 4, --stale; zero differences, except files this task edits on purpose (list them).
R5 (H5, Design Notes 26 decision 2). In docs/sketches/s1_spec.yaml replace the "OPEN, decision for Sean (Loftsman FIX 5)" comment (l.70-73) with Sean's ruling (Design Notes 23: 1 m class stop 392.50 + c, start 1042.50 + c z_A, capture 650 - c; c owned by Sean, N11, reported as an expression until set). Add the start-above-core term `collet.core_stop_z + L + c - upper.travel_max` to park_rule.stop_k and for_step4 so the 0.5 and 0.75 m values are unchanged (stop 184.84, start 834.84, park 959.84 z_A, stroke 775) and the 1 m class reads park 1209.84, stroke 1025, L 1140 unchanged, with start_minus_core_top no longer -125.00. c has no value: either an overlay leaf with a K2-legal value and status (state what you chose, mark it for the Loftsman) or a symbolic term check_stack reports as an expression; do not invent a value for c. Collar shape gloss: "(plate top)" becomes "(collar.top_above_plate above the wing-nut top)" (Designer re-check NOTE R2). Then run `s1 --rev 4` to wip/ and diff against docs/sketches/s1_checks_r4.json: allowed differences are timestamp, spec_status if changed, and the 1 m reported terms; list every differing field.

READ FIRST:
1. research/sean/gameplan.md lines 118-161 (detail 1.0, K table, red-first baseline), 163-175 (detail 1 common), 206 (PNG rule), 595-633 (Design Notes 25, 26), 587-592 (Design Notes 23).
2. research/sean/cr_scratch/step1.1_manager_close.md sections 3, 5, 8, 9.
3. research/sean/cr_scratch/step1.1_engineer_move_notes.md (Open items).
4. docs/sketches/check_sketch.py, sketch_loader.py, sketch_common.py (output paths, setup_figure), check_stack.py (park_rule evaluation, reported), s1_side_poses.py, s1_mass_report.py, s1_spec.yaml (l.40-80, park_rule; the collar row), fixtures/manifest.yaml, fixtures/builders.py (control_figures), baseline_red.json.
5. research/sean/cr_scratch/step1.1_loftsman_spec_signoff.md (FIX 5) and research/sean/cr_scratch/step1.1_designer_spec_signoff.md (NOTE R2, l.99, l.120).

TASK:
1. Implement R1 to R5. Every new control is run red against the pre-change code first; state the observed red.
2. Run check_sketch.py --controls (background-safe; record counts and time against 117: Z 35, B 81, smoke 1), check_sketch.py s1 --rev 4 (17/17), s1_side_poses.py --rev 4 and s1_mass_report.py --rev 4 to wip/ (PNGs pixel-equal to docs/sketches/s1_pose_*_r4.png), --stale (expected 0 records until the orchestrator's accept), --stale --include-unaccepted, --baseline s1.
3. Do not run --accept on s1 r4. The orchestrator runs `--accept s1 --rev 4 --note "Design Notes 24"` after The Loftsman's H5 check; give the exact command line and the expected output.
4. Report the SHA-256 before/after table (R4).

Output sections, in order: Corrections to the brief; 1 files changed (path, what); 2 R1 design and controls (ID, planted, reason substring, red on pre-change code, result); 3 R2 copy hash and --baseline s1 result; 4 R3/R4 output rule and SHA-256 table; 5 R5 spec text (old/new), the c treatment, check_stack values per Q9 option (stop, start, park, stroke, L, start_minus_core_top), record diff list; 6 run table (command, result, time); 7 command for the orchestrator's accept and its expected output; 8 open items; 9 Gameplan lines to change (at least detail 1.0 file bullet for check_sketch.py l.124 with --accept, --baseline sN and the wip/ rule; red-first baseline l.154; PNG rule l.206; Echo Site Registry park-rule row l.648).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_engineer_step0.md
Return in context only: --controls counts and time, s1 r4 result, PNG equality, SHA-256 diff count, the accept command, blocking items (under 12 lines).
```

---

### P0L. The Loftsman, H5 park-rule check (parallel with P1)

Spawn: agent; background recommended. After P0. Parallel with P1.

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Step 1.2 step 0, H5 (Design Notes 26 decision 2): The Engineer wrote Sean's 1 m park-rule ruling (Design Notes 23) into docs/sketches/s1_spec.yaml. You raised FIX 5 at 1.1 (b); you check the expression. S1 stays r4 only if no drawn or checked value moves.

READ FIRST:
1. research/sean/cr_scratch/step1.2_engineer_step0.md section 5.
2. docs/sketches/s1_spec.yaml lines 40-80 (park_rule, screw_length, q9 list) and the collar row; docs/sketches/check_stack.py (park-rule evaluation and reported values); docs/sketches/proposed_params.yaml (if c became a leaf).
3. research/sean/gameplan.md lines 587-592 (Design Notes 23), 595-626 (Design Notes 25 H5), 284-287 (detail 1.3 L expression), 646-649 (Echo Site Registry rows for L, stroke, park rule).
4. Your 1.1 file: research/sean/cr_scratch/step1.1_loftsman_spec_signoff.md (FIX 5).
5. docs/sketches/wip/s1_checks_r4.json and docs/sketches/s1_checks_r4.json (the record diff).

TASK:
1. Hand values beside the check_stack values for each Q9 option (0.5; 0.5 and 0.75; plus 1 m): stop_k, start_k, park, stroke, L_min, start_minus_core_top; the 1 m terms as expressions in c.
2. Rule whether stop_k and for_step4 carry the start-above-core term correctly, and the range of c over which park 1209.84 holds (entry-plane term governs) before the start term takes over.
3. The c treatment (leaf or symbolic) is K2-legal and invents no value.
4. Record diff: every differing field between wip/ and docs/ s1_checks_r4.json is one of timestamp, spec_status, the 1 m reported terms. Any other difference: FIX.
5. Collar gloss reads as NOTE R2 asked.
Verdict line: "H5 PASS" or "FIX" with numbered items. On PASS the orchestrator runs the accept.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_loftsman_h5_check.md
Return in context only: verdict, FIX count, the c range for park 1209.84.
```

If FIX: P0 re-spawn with TASK 0 "close each FIX in research/sean/cr_scratch/step1.2_loftsman_h5_check.md", output `step1.2_engineer_step0_fixes.md`, then P0L re-check (TASK 0 "verify each FIX closed").

### ORCH-A. Orchestrator after P0L PASS

1. Run `C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe docs/sketches/check_sketch.py --accept s1 --rev 4 --note "Design Notes 24; spec text H5 per Design Notes 26 decision 2"` (or the exact line P0 section 7 gives). The accept copies up the H5-refreshed checks JSON and summary from wip/ and refuses on any PNG pixel difference.
2. Run `check_sketch.py --stale`: expected 1 record (s1 r4), 0 differences. Record both outputs in the Progress Log.
3. Apply "Gameplan lines to change" from P0 and P0L. Save point 1 ("sean: Step 1.2 step 0 harness, S1 accepted flag").

---

### P1. The Designer, 1.2 (a) params review (parallel with P0L)

Spawn: agent; background recommended. After P0. Parallel with P0L.

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Step 1.2 (a): params review of every key S2 plots, representative-shape note per S2 part (LLM-PLM 8.4a, 8.4b), the S2 operator-task rows and the S2-5 sector. No drawing exists. You read no scripts. Your notes go into the s2_spec.yaml `shape` field at (b).
Items carried to you (Design Notes 25): S2-a cutter r 88.90 is 2.70 outside icd.keepout_radius 86.2 (tube basis), keep-out seed pair without a spec neighbour; S2-b F6 plan sightline to the cutter at capture_end past the ring rim r 210 (you set the sector); S2-c the theta 270 screw frame member (r 330 outer edge) overhangs the plate edge (footprint_y / 2 = 304) by 26: frame_upper.radius <= 274 or a wider plate; S2-d LM20UU 42 long against ring thickness 12 (flanged bushing below the lug); S2-e every operator sector between two screws holds a NEMA 23 at chest and shoulder height at load; S2-f the third screw set (theta 270) and third pinion and NEMA 23 (theta 90) are drawn in S2. Carried from 1.0 (Design Notes 20 H4): lift motor and guide rod positions placed in S2 replace the S1 placeholders.
Manager findings for you (DERIVED from the overlay):
- O1: pinions at 90, 210, 330 sit on the bisectors of the screw gaps (screws 30, 150, 270). Any sector with its apex on the axis between two screws contains the NEMA 23 at r 142 to 218 on its bisector, so S2-5 as written ("free of screws, motors and frame members, K7 F") is red by construction. Resolve: pinion phase, motor placement, or a reworded S2-5 rule (for example z-banded against the operator's reach at load). A reworded rule is a relaxed rule under detail 1 common (h): state its premise and the check that enforces it.
- O2: widening the plate edits icd.footprint_y, a params.yaml key. params.yaml stays unchanged until 4c (Design Notes 6) and K2 fails an overlay key that shadows a params key. That option needs a new overlay key and edits to the S1 and S2 specs (the S1 base plate depth band reads icd.footprint_y).
- Bounds on frame_upper.radius from current values: member inner face at radius - 30 must clear the ring rim r 210 by g_min 10, so radius >= 250; anchor and guide arms run from r 181 (pitch radius 160 + nut flange 21) to the member face; radius 274 gives member faces 244 to 304 and arms 26 shorter. Check these yourself.
- Any value you set that changes a key the accepted S1 r4 reads (docs/sketches/s1_checks_r4.json keys_read) reopens S1 as r5 (gameplan detail 1 common (i)). Sean rules each such value at STOP S2-A before (b) writes the overlay.

READ FIRST:
1. research/sean/gameplan.md lines 121 (overlay seeds, ring.* functional features), 147-152 (K7 g_min seeds), 163-206 (detail 1 common, operator-task table, rubric applicability, M1 rubric), 243-261 (detail 1.2 and S2 check table), 493-497 (Design Notes 6, 7), 503-505 (Design Notes 11), 595-633 (Design Notes 25, 26), 635-666 (Echo Site Registry), 668-703 (Open Questions N2, N4, N6, N12).
2. research/sean/cr_scratch/step1.1_manager_close.md sections 8 and 9.
3. Your 1.1 files: research/sean/cr_scratch/step1.1_designer_params_review.md (operator rows, shape notes), research/sean/cr_scratch/step1.1_designer_spec_signoff.md (NOTES N1 to N6), docs/sketches/s1_visual_gate_r3.md (F6, F7 and the r4 section).
4. docs/sketches/proposed_params.yaml (whole file); docs/sketches/s1_spec.yaml rows that carry `place` (plan footprints S2 must agree with); docs/sketches/s1_checks_r4.json "keys_read" (the S1 key list).
5. params.yaml: grep only the keys named in detail 1.2 "Params keys" (l.247): drill.tube_od, drill.tube_id, icd.keepout_radius, icd.footprint_x, icd.footprint_y, icd.datum_*, icd.mounting_pattern, frame.*, profile.*, base.*.
6. ASSEMBLY.md Coordinate frame (l.5-7): +X along slot line C, theta counter-clockwise from +X seen from +Z, theta_key 37 deg.
7. supplements/llm_plm_cad.md lines 528-597 (8.4 a and b, 8.4.1, 8.4.2).
8. docs/sketches/s1_pose_load_r4.png and s1_pose_capture_end_r4.png (open with the Read tool if your model reads images; otherwise skip and say so).

TASK:
1. Functional completeness (8.4a) for every part S2 plots in plan: base plate and frame, frame members, screws with nuts, anchors and top guides in plan, ring with nut housings, motor mounts, clearance bore, gear, pinions, NEMA 23 motors, guide members (N2) with bushings, lift motors, drill tube, keep-out, cutter, collet axis, slot lines. PASS or FAIL per feature; missing leaves with proposed value, unit, source, status (ASSUMED unless sourced).
1b. O1/S2-e: resolve the motor-in-sector conflict. Give the options with their cost (keys moved, S1 r5 or not, hazard), and your recommendation.
2. S2-c: give the options (radius <= 274; wider plate per O2; screw phase change) with values, the S1 rows each moves, and your recommendation. Confirm the 274 bound by hand (plate edge 304, member half-width 30, square member with one face toward the axis) and the lower bound against ring rim, guide rods, motors and stop pad.
3. Phase and placement: screw-to-pinion phase (stated value), guide member positions and type (N2 option drawn, with the alternative Sean may pick at M2), lift motor plan position (H4), guide bushing form (S2-d), each with keys and values.
4. S2-5 operator sector: apex on the axis, half-angle, radius, azimuth, z band if your rule uses one; the Z and B fixtures in gameplan terms (Z: a 90 deg sector between two screws; B: widened to 130 deg) adjusted to your rule.
5. S2-b: the F6 plan sightline (observer position r and azimuth, eye height, line to the cutter at capture_end) as a spec row the Engineer can draw.
6. S2-a: keep-out pairs in plan (which parts against icd.keepout_radius 86.2, class, g_min) and the cutter overhang as a reported value; state the Step 4 ICD row it feeds.
7. Shape notes (8.4b): one `shape` string per S2 part; a ring reads as a structure with housings and mounts, a bevel pinion in plan reads as a pinion on a radial shaft with its motor outboard, a 30-6060 member reads as a 60 x 60 section with one face toward the axis (ASSUMED), screws as circles with nut flange.
8. g_min per K7 pair S2 uses (seed list l.147-152), confirmed or changed.
9. Operator-task rows for S2 (load a 0.75 m core, change a collet, stand and watch): stance and reach in plan, sector, sightline, hazard, on your values.
10. Items for Sean at STOP S2-A: every value that changes an S1 r4 key (list key, old, new, S1 rows that move), the S2-c pick, the O1 pick. Mark which items can wait for M2.
11. Echo sites S2 creates (value, authoritative source, derived locations).

Output sections, in order: Corrections to the brief; 1 functional completeness table; 2 O1 options and recommendation; 3 S2-c options and recommendation with hand values; 4 phase, guide, lift motor, bushing; 5 S2-5 sector rule with Z and B; 6 sightline row; 7 keep-out pairs and overhang; 8 shape-note table (part id, shape); 9 overlay value table (key, old, new, unit, source, status, S1 key yes/no); 10 g_min table; 11 operator-task rows; 12 items for Sean (STOP S2-A, or M2); 13 echo sites; 14 Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_designer_params_review.md
Return in context only: S2-c recommendation, O1 recommendation, the S1 keys you propose to change, functional completeness pass/fail counts, items for Sean (under 15 lines).
```

---

### STOP S2-A. Sean: rulings that touch the accepted S1

Blocking, after P1 and ORCH-A. The orchestrator presents from P1 sections 2, 3 and 12:
1. S2-c: the three options with values and the S1 rows each moves; P1's recommendation. Radius <= 274 or a phase change reopens S1 as r5 (section 1.2); a wider plate does too and adds a new overlay key (O2).
2. O1/S2-e: the motor-in-sector options and P1's recommendation; a reworded S2-5 rule is a relaxed rule and ships with its premise check (detail 1 common (h)).
3. Every other P1 value that changes an S1 r4 key.
Sean picks, or corrects. The orchestrator records the rulings as new Design Notes 27 "Step 1.2 STOP S2-A rulings (Sean, <date>)" with Sean's words, adds a Progress Log row, and passes the rulings to P2. Items Sean defers go to M2 and P2 draws the P1 recommendation as the option.

---

### P2. The Engineer, 1.2 (b) spec

Spawn: agent, `run_in_background: true` (**required**). After STOP S2-A.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.2 (b): write docs/sketches/s2_spec.yaml from The Designer's params review and Sean's STOP S2-A rulings (gameplan Design Notes 27, applied by the orchestrator before this spawn), apply the overlay values, and bring the spec to "ready for signature". No drawing before the spec is signed. Design values come from the Designer's review and Sean's rulings; where a value is missing, stop and report it.
S1 coupling: one overlay serves S1 and S2. If Sean adopted a value for any key in docs/sketches/s1_checks_r4.json keys_read, `check_sketch.py --stale` will read red on s1 r4 after your overlay edit. That red is expected: record it with the exact key list; it opens S1 r5, which you draw at (d). Do not suppress or work around it.

READ FIRST:
1. research/sean/cr_scratch/step1.2_designer_params_review.md (whole file).
2. research/sean/gameplan.md Design Notes 27 (STOP S2-A rulings, at the end of Design Notes), lines 118-161 (detail 1.0, spec format incl. 1.1 fields, K table, g_min seeds), 163-206 (detail 1 common), 243-261 (detail 1.2, S2 check table).
3. docs/sketches/s1_spec.yaml (format reference: header fields, place, neighbours, sense, k7_tolerance, notes), docs/sketches/proposed_params.yaml, sketch_loader.py, sketch_common.py, check_stack.py, check_sketch.py, checks_s1.py (pattern for checks_s2.py).
4. research/sean/cr_scratch/step1.2_engineer_step0.md (output rule, --baseline sN, per-sketch tables).
5. params.yaml keys listed in gameplan l.247 (grep); ASSEMBLY.md Coordinate frame (l.5-7).

TASK:
1. Overlay: apply the Designer's value table and Sean's rulings to docs/sketches/proposed_params.yaml; each changed leaf with source "Designer 1.2 (a)" or "Sean STOP S2-A, Design Notes 27" plus basis, status as given. A new key that would shadow a params.yaml key (O2, plate width) gets a non-shadowing name; report the name.
2. Spec docs/sketches/s2_spec.yaml: header (question from detail 1.2, R and Q rows, view plan_xy, poses per the Designer, rubric additions, reported values, k7_tolerance statement as in S1, script s2_plan.py); one row per part with id, name, shape (Designer's note), kind, axis, projection (plan: axis-Z cylinders as circles; radial-axis parts per TP-13 as rectangles or trapezoids), keys, place (footprint as in S1: round or radial, true section where plan-contact will be claimed), z band per pose for the swept K7 case, label, neighbours (class, g_min, source), sense predicates (K8: screws 120 deg apart, phase, handedness), notes. Rows present in both s1_spec.yaml and s2_spec.yaml use the same place expressions; list every such row.
3. Every part a shape string names has a row or a not_drawn entry with reason (detail 1 common (b)); write the part list.
4. checks_s2.py skeleton with S2-1 to S2-5 per the gameplan table and the Designer's S2-5 rule (implementations may fail closed until (c); fixtures come at (c)).
5. Run check_stack.py on the S2 spec (plan positions, z bands per pose). Report per part: centre (r, theta, x, y), footprint extents, z band per pose; outline extents against 644 x 608; members against the plate edge; S2-2 margin (pitch radius - nut flange radius - keep-out) by hand and computed.
6. Run check_sketch.py --controls (no regression from the P0 count) and --stale and --stale --include-unaccepted. If an S1 key changed, also run check_sketch.py s1 --rev 5 against the unchanged s1_side_poses.py to wip/ as a preview (not of record) and report its result and every S1 value that moved.
7. Open items for signature: values missing, rows the Designer must confirm, S1 spec edits needed beyond comments (for The Loftsman to rule).

Output sections: Corrections to the brief; 1 files changed; 2 part list (shape-text parts: row or not_drawn); 3 plan table per part; 4 S2-2 and plate-edge hand vs computed; 5 --controls, --stale results (with the s1 r4 key list if red), S1 r5 preview; 6 shared rows S1/S2 with their place expressions; 7 open items for signature; 8 Gameplan lines to change (at least detail 1.2 "Shows" if the guide or phase wording changes, the S2-5 row if the rule is reworded, Echo Site Registry rows).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_engineer_spec.md
Return in context only: --controls counts, --stale result and s1 key list, S1 r5 preview result, S2-2 margin, blocking items (under 12 lines).
```

---

### P3a. The Designer, 1.2 (b) spec sign-off (parallel with P3b)

Spawn: agent; background recommended. Parallel with P3b after P2.

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Step 1.2 (b) sign-off. You wrote the params review; The Engineer wrote the S2 spec and overlay from it and from Sean's STOP S2-A rulings. You sign or return FIX items. The Loftsman signs in parallel on arithmetic and placement. Your sign-off carries the shape-text part list (detail 1 common (b)): at S1 your sign-off passed shape text naming parts without rows, which cost revision r3.

READ FIRST:
1. research/sean/cr_scratch/step1.2_designer_params_review.md (your review).
2. research/sean/cr_scratch/step1.2_engineer_spec.md.
3. docs/sketches/s2_spec.yaml; docs/sketches/proposed_params.yaml.
4. research/sean/gameplan.md lines 147-152, 163-206, 243-261, Design Notes 27 (STOP S2-A rulings).

TASK:
1. Part list: every part any shape string names, with its row id or not_drawn reason. A named part with neither is a FIX.
2. Every row's shape matches your note; every ring.* functional feature S2 shows has a row or a key.
3. Phase, guide option, lift motor, bushing form, S2-5 sector rule and sightline row as you set them and as Sean ruled.
4. Neighbour classes and g_min per pair; keep-out pairs (S2-a).
5. Operator-task rows consistent with the Engineer's plan table.
6. Rubric additions true on the spec values, each with a predicate or marked visual-only.
Verdict line: "SPEC SIGNED (Designer)" or "FIX" with numbered items, each naming row id and the required change.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_designer_spec_signoff.md
Return in context only: verdict, FIX count, part-list count (rows / not_drawn / missing).
```

### P3b. The Loftsman, 1.2 (b) spec sign-off (parallel with P3a)

Spawn: agent; background recommended (may run check_stack.py, about 1 s).

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Step 1.2 (b) sign-off on arithmetic and placement. LF-8 is yours: side-view K7 was a box test until S2 supplied an XY footprint; S2 now draws the true plan outlines. Rows that appear in both specs must agree.

READ FIRST:
1. research/sean/cr_scratch/step1.2_engineer_spec.md.
2. docs/sketches/s2_spec.yaml, docs/sketches/proposed_params.yaml, docs/sketches/check_stack.py, docs/sketches/checks_s2.py (skeleton).
3. docs/sketches/s1_spec.yaml rows with place fields; docs/sketches/s1_checks_r4.json keys_read.
4. research/sean/cr_scratch/step1.2_designer_params_review.md sections 3 to 7, 9.
5. research/sean/gameplan.md lines 129-145 (spec format, K table), 147-152 (g_min), 243-261 (detail 1.2); ASSEMBLY.md Coordinate frame.
6. Your 1.1 file: research/sean/cr_scratch/step1.1_loftsman_crossreview.md (plan-contact and footprint rulings).

TASK:
1. Hand values beside the Engineer's: screw centres at r cos theta, r sin theta for all three; pinion pitch points against the gear pitch radius (S2-3); S2-2 margin; theta 270 member outer edge against the plate edge on the adopted value; sector boundary against the nearest screw, motor and member (S2-5).
2. Shared rows: rule whether identical place expressions in s1_spec.yaml and s2_spec.yaml make S1/S2 footprint agreement an identity, or whether a cross-sketch check is needed (if needed, specify it with Z and B).
3. If an S1 key changed: list every S1 row and K7 pair that moves, the S1 values that change (margins, arm lengths, depth bands), and rule whether S1 r5 needs spec edits beyond comments.
4. Footprints: each contains its part (containment premise); true sections where plan-contact is claimed (a 30-6060 member is a 60 x 60 square, one face toward the axis, ASSUMED).
5. The plan form of the swept K7 case: each moving part's outline against every fixed part whose z band intersects the sweep, on the spec z bands.
Verdict line: "SPEC SIGNED (Loftsman)" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_loftsman_spec_signoff.md
Return in context only: verdict, FIX count, the shared-row ruling, S1 r5 spec-edit ruling.
```

### P2f. The Engineer, (b) fix pass (only if P3a or P3b returns FIX)

Spawn: background **required**. Then re-spawn only the raiser(s) with their prompt plus "READ FIRST 0: research/sean/cr_scratch/step1.2_engineer_spec_fixes.md; TASK 0: verify each of your FIX items closed", output `step1.2_{designer|loftsman}_spec_recheck.md`.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.2 (b) fix pass on the spec sign-off findings.

READ FIRST:
1. research/sean/cr_scratch/step1.2_designer_spec_signoff.md and research/sean/cr_scratch/step1.2_loftsman_spec_signoff.md.
2. research/sean/cr_scratch/step1.2_engineer_spec.md.
3. docs/sketches/s2_spec.yaml, proposed_params.yaml, check_stack.py, checks_s2.py, fixtures/manifest.yaml.

TASK:
Close every FIX item. A design value a reviewer asks for comes from that reviewer's file; if none is given, list it as open. A cross-sketch check the Loftsman specified is written with its Z and B now. Re-run check_stack.py and check_sketch.py --controls; record results. On a clean close set the spec header `status: signed (Designer, Loftsman)` only after both re-checks return SIGNED; until then `status: fixes applied, awaiting re-check`.
Output: Corrections to the brief; one row per FIX item (ID, change, evidence); re-run results; Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_engineer_spec_fixes.md
Return in context only: items closed, items open, --controls counts.
```

Orchestrator after both SIGNED: apply gameplan lines from P2, P3a, P3b, P2f; save point 2 ("sean: Step 1.2 (b) S2 spec signed").

---

### P4. The Engineer, 1.2 (c) red-first

Spawn: background **required**. After save point 2.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.2 (c), red-first (detail 1 common (c)). The S2 spec is signed. Before the S2 stub run the harness gains its plan-view rules (Design Notes 20: SW-17 K5 plan-view B control, TP-13 radial-axis plan rule; LF-8 XY footprint test). Each new or relaxed rule states its premise and enforces it with its own Z and B (detail 1 common (h)); the raiser (Software Engineer for SW-17, Topologist for TP-13, Loftsman for LF-8) signs it at (c) or (e).

READ FIRST:
1. research/sean/gameplan.md lines 129-161 (spec format, K table, red-first baseline), 163-175 (detail 1 common), 243-261 (detail 1.2, S2 check table), 542-569 (Design Notes 20: SW-17, TP-13, LF-8 rows).
2. docs/sketches/s2_spec.yaml (signed), checks_s2.py, check_sketch.py, sketch_common.py (K5, K6, K7, K8, K9; VIEW_NORMAL, plan_footprint, plan_gap_fn, plan_contact_fn), fixtures/manifest.yaml, fixtures/builders.py, baseline_red.json, stubs/s1_stub.py (pattern).
3. research/sean/cr_scratch/step1.0_software_engineer_signoff.md (SW-17), research/sean/cr_scratch/step1.0_topologist_crossreview.md (TP-13), research/sean/cr_scratch/step1.0_loftsman_crossreview.md (LF-8).
4. research/sean/cr_scratch/step1.2_engineer_spec.md, step1.2_engineer_spec_fixes.md (if present), step1.2_loftsman_spec_signoff.md (shared-row ruling, plan swept form).
5. research/sean/cr_scratch/step1.2_engineer_step0.md (per-sketch tables, --baseline sN, output rule).

TASK:
1. Plan-view harness rules, each with Z and B in manifest.yaml, each B run red against the pre-change code first:
   a. K5 plan view (SW-17): an axis-Z cylinder drawn as a rectangle in plan fires; TP-13: a radial-axis part (pinion shaft, NEMA 23, frame arm) drawn as a circle in plan fires.
   b. K6 in plan_xy: state what K6 asserts in a plan view (drawn centre and extent against the spec place field in x, y; z bands are not drawn) and implement it; B: a part drawn 6.75 mm off its spec centre.
   c. K7 in plan_xy (LF-8): true XY outlines, no depth bands; z bands per pose decide which pairs meet (pairs whose z bands are disjoint at every pose are listed "z-separated" for F only, with the same C and G rules as the side-view depth bands); swept case per the Loftsman's plan form. Z: two members 100 apart read F; B: a 1 mm plan overlap on an F pair; B: a G pair at g_min - 1; B: a z-separated C pair fires.
   d. K8 plan handedness: K8-B3 (y inverted) runs on the S2 axes; add B: azimuth order clockwise (screws drawn at -theta).
   e. Any cross-sketch footprint check the Loftsman specified at (b), if not written at P2f.
2. S2-x fixtures from the signed spec: a Z and a B for each of S2-1 to S2-5 per the gameplan table and the signed S2-5 rule (S2-1 B one screw at 110 deg; S2-2 B pitch radius equal to the keep-out radius; S2-3 B pinion on the gear OD; S2-4 B collet axis 2 mm off; S2-5 B sector widened to 130 deg, or the signed rule's equivalent). Each B carries its reason substring and planted count.
3. Plan reviewer-control figures (O5): ctrl_c.png (a correct plan of the mini spec: screws counter-clockwise from +X, axis labels, theta arrow) and ctrl_d.png (the same plan mirrored: y inverted or azimuths clockwise), same title text; add both to key.json with "must PASS handedness" / "must FAIL handedness". Output location per the P0 control-figure rule.
4. stubs/s2_stub.py (setup_figure plan_xy, base footprint outline only); per-sketch stub expectations for s2 (guards and expected reds with causes) in the structure P0 created; SOURCES for S2-1 to S2-5.
5. Run check_sketch.py --controls (every Z clean, every B fires; counts and time); check_sketch.py s2 --rev 0 to wip/ (every S2 check red for its own reason, K1, K2, K3, K5 green as guards, causes labelled); check_sketch.py --baseline s2. A sketch check green on the stub is rewritten until it fails on content.
Output sections: Corrections to the brief; 1 plan rules (rule, premise, premise check, Z, B, red on pre-change code); 2 S2-x fixture table (ID, Z, B, reason substring, planted, result); 3 control figures; 4 --controls counts and time; 5 stub run table against expectations; 6 code changes; 7 rules awaiting their raiser's signature; 8 Gameplan lines to change (K5 to K8 rows for the plan rules, K table control pointer, detail 1.2 carried line).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_engineer_redfirst.md
Return in context only: --controls counts, stub red/green counts, rules added, any check rewritten.
```

### P5. The Software Engineer, 1.2 (c) check

Spawn: background **required** (re-runs `--controls`). After P4.

```
[BLOCK SWE]

CONTEXT:
[CTX COMMON]
Step 1.2 (c). Three items in one review, all before the S2 stub run is accepted as the red-first record:
(1) H6 (Design Notes 25): the harness delta since your 1.1 (c) check: 18 controls added in r2 to r4 (K5-Z2, K5-B6, K6-B7, K7-B14, K7-B15, K8-Z4, K8-B14, K9-Z2, K9-B5; K7-Z11, K7-B16 to K7-B19; K8-Z5, K7-B20, K8-B15, K8-B16 and the K8-B7 re-scope) and seven rules (plan-contact, projected_extent, section-N, pose-set, bore_cone, stack_ties, place.rot), reviewed so far by The Loftsman and The Topologist only.
(2) Step 0 code (P0): --accept, supersession, --baseline sN, the wip/ output rule, control outputs to wip/.
(3) P4: the plan-view rules (SW-17 is yours to sign), the S2-x fixtures, the plan control figures, the S2 stub run.

READ FIRST:
1. research/sean/cr_scratch/step1.2_engineer_redfirst.md and research/sean/cr_scratch/step1.2_engineer_step0.md.
2. research/sean/cr_scratch/step1.1_engineer_revision_r2.md, step1.1_engineer_revision_r3.md, step1.1_engineer_revision_r4.md (what the r2 to r4 controls and rules were for).
3. docs/sketches/check_sketch.py, sketch_common.py, fixtures/manifest.yaml, fixtures/builders.py, checks_s1.py, checks_s2.py, s2_spec.yaml, stubs/s2_stub.py, wip/s2_checks_r0.json, baseline_red.json.
4. research/sean/gameplan.md lines 129-161, 163-175, 243-261.
5. Your 1.1 file: research/sean/cr_scratch/step1.1_software_engineer_redfirst_check.md.

TASK:
1. H6: each r2 to r4 control reproduces a plausible defect and fires on its reason with its planted count; each rule has a B per branch (your 1.1 FIX 1 class: delete a branch and see whether any control notices). Name any branch without a B.
2. Step 0: the --accept refusals, supersession and copy-up controls are real controls; a verification run leaves committed files unchanged (re-run the SHA-256 comparison yourself).
3. P4: each plan rule's premise is enforced by a check with its own Z and B; each S2-x B fires on its reason; S2 checks that cannot fail through the drawing (SW-10 class) named, with stay/drop.
4. Re-run check_sketch.py --controls and check_sketch.py s2 --rev 0; compare with the Engineer's counts.
5. Simplicity gate: any added mechanism that costs more than it protects for a two-person team.
Verdict: "PASS" or "FIX" with numbered items; sign SW-17 or not.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_software_engineer_check.md
Return in context only: verdict, FIX count, SW-17 signed or not, branch gaps found.
```

P5f if FIX: P4 re-spawn with "READ FIRST 0: research/sean/cr_scratch/step1.2_software_engineer_check.md; TASK 0: close each FIX", output `step1.2_engineer_redfirst_fixes.md`; then P5 re-check (TASK 0 "verify each FIX closed"), output `step1.2_software_engineer_recheck.md`. Then apply gameplan lines; save point 3 ("sean: Step 1.2 (c) red-first, harness checked").

---

### P6. The Engineer, 1.2 (d) draw S2 r1 (and S1 r5 if triggered)

Spawn: background **required**. After save point 3. The orchestrator polls `docs/sketches/wip/s2_*_r1.png` for STOP-T5.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.2 (d): write the S2 script and iterate until K1 to K9 and S2-1 to S2-5 are green. The first PNG goes to Sean for an orientation preview (V2 and handedness) as soon as it exists; write it before iterating. Fix the drawing, never the check or the spec; a spec defect goes in the output as an open item for The Designer.
S1 r5: [orchestrator states one: "triggered: Sean adopted <keys> at STOP S2-A (Design Notes 27)" / "not triggered"]. If triggered, also run s1_side_poses.py --rev 5, check_sketch.py s1 --rev 5 and s1_mass_report.py --rev 5 to wip/ (17/17 required), with script edits only where an expression must change and spec edits only as The Loftsman ruled at (b).

READ FIRST:
1. research/sean/gameplan.md lines 163-206 (detail 1 common, operator-task table, rubric, applicability), 243-261 (detail 1.2).
2. docs/sketches/s2_spec.yaml (signed), proposed_params.yaml, sketch_common.py, sketch_loader.py, check_stack.py, check_sketch.py, checks_s2.py, s1_side_poses.py (pattern).
3. research/sean/cr_scratch/step1.2_designer_params_review.md (shape notes, sector, sightline, operator rows).
4. research/sean/cr_scratch/step1.2_engineer_redfirst.md and step1.2_software_engineer_check.md (and recheck if present).
5. research/sean/cr_scratch/step1.2_loftsman_spec_signoff.md section 3 (S1 r5 rows) if S1 r5 is triggered.
6. supplements/llm_plm_cad.md lines 570-597 (8.4.1, 8.4.2); ASSEMBLY.md Coordinate frame.

TASK:
1. Write docs/sketches/s2_plan.py: figure(s) through setup_figure("plan_xy") and draw(gid); every value from the loader; shapes per the spec shape field; output through the P0 output-path helper.
2. Write docs/sketches/wip/s2_plan_r1.png (and any further figure the spec declares) first; note the write time.
3. Run check_sketch.py s2 --rev 1; iterate until every K-check and S2-1 to S2-5 is green.
4. K1 on s2_plan.py: literals found, angle sources.
5. Reported values in wip/s2_summary_r1.md: outline extents against 644 x 608; members against the plate edge; cutter overhang of the keep-out (S2-a); footprint against the S1 unbolted tip force (S1 r4 or r5 summary).
6. S1 r5 if triggered: results, every value that moved against r4 (table: quantity, r4, r5), PNG paths.
7. Re-run check_sketch.py --controls once at the end (no regression) and --stale (s1 r4 red on the adopted keys only, if triggered).
Output sections: Corrections to the brief; 1 files written; 2 iteration log (run, red checks, fix); 3 final check table S2 (and S1 r5); 4 reported values; 5 S1 r4/r5 comparison; 6 open items; 7 Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_engineer_draw_r1.md
Return in context only: final check counts (S2; S1 r5), PNG paths, members-to-plate-edge margin, cutter overhang.
```

### STOP-T5 (non-blocking). Sean: orientation preview

When `docs/sketches/wip/s2_plan_r1.png` exists, the orchestrator shows Sean the PNG and asks: V2 (drill axis vertical: drill, collet, ring and gear concentric in plan; pinion axes radial) and handedness (+X along slot line C, theta counter-clockwise from +X seen from +Z, screws and pinions at the stated azimuths, operator sector where the spec puts it). If S1 r5 PNGs exist, V1 to V5 on them. Not acceptance. Corrections go to Design Notes 13 as `S2-r1` (or `S1-r5`) with Sean's words and into P9 together with the (e) and M1 findings.

---

### P7a. The Loftsman, 1.2 (e) cross-review (parallel with P7b and P8)

Spawn: background recommended. After P6.

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Step 1.2 (e), geometry cross-review (A.4 step 2): azimuths, radii, placement, plan K7. Re-compute at least one value per check by hand and write it beside the JSON value. You also sign the plan K7 rule you raised (LF-8) on its premise. M1 runs in parallel on the same revision (process fix (f)).
S1 r5: [orchestrator states triggered with keys, or not triggered]. If triggered, cross-review the changed S1 rows only.

READ FIRST:
1. docs/sketches/s2_plan.py, s2_spec.yaml, wip/s2_checks_r1.json, wip/s2_summary_r1.md, proposed_params.yaml, check_stack.py, checks_s2.py, sketch_common.py (plan K6, K7).
2. research/sean/cr_scratch/step1.2_engineer_draw_r1.md, step1.2_engineer_redfirst.md section 1.
3. ASSEMBLY.md Coordinate frame; research/sean/gameplan.md lines 129-152, 243-261.
4. Your sign-off: research/sean/cr_scratch/step1.2_loftsman_spec_signoff.md.
5. If S1 r5: docs/sketches/wip/s1_checks_r5.json, docs/sketches/s1_checks_r4.json, s1_spec.yaml.

TASK:
1. Hand value beside JSON value: S2-1 azimuths of all three screws and pinions and the phase; S2-2 margin; S2-3 pitch point radius per pinion; S2-4 centres; S2-5 sector boundary distances; plan K6 centre of at least three placed rows; members against the plate edge.
2. Plan K7 (LF-8): the rule as implemented matches your plan form; its premise (containment, true sections for plan-contact, z bands from the spec) is enforced by a check with Z and B; sign or FIX.
3. Pairs passed as z-separated: list them and say whether each is real.
4. Reported values: arithmetic only, no thresholds.
5. S1 r5 if triggered: hand values for every changed S1 margin and placement (frame members, arms, stop pad, K7 pairs touching them).
Findings as BLOCK, FIX or NOTE with IDs LF1.2-n. Verdict line: "CROSS-REVIEW PASS" or "CROSS-REVIEW FAIL"; separate verdict for S1 r5 if triggered.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_loftsman_crossreview.md
Return in context only: verdict(s), counts, LF-8 signed or not.
```

### P7b. The Topologist, 1.2 (e) cross-review (parallel with P7a and P8)

Spawn: background recommended. After P6.

```
[BLOCK TOP]

CONTEXT:
[CTX COMMON]
Step 1.2 (e), geometry cross-review: handedness and half-space sense in plan (+X along slot line C, theta counter-clockwise from +X seen from +Z; K8 B3), projection per row (TP-13 radial-axis rule is yours to sign), K9 coverage. Re-compute at least one K8 predicate by hand through the artist transform chain and write it beside the JSON value. M1 runs in parallel on the same revision.
S1 r5: [orchestrator states triggered with keys, or not triggered]. If triggered, re-check K8 projected_extent and sense on the changed S1 rows.

READ FIRST:
1. docs/sketches/s2_plan.py, s2_spec.yaml, wip/s2_checks_r1.json, sketch_common.py (K5, K8, K9 and the plan rules).
2. research/sean/cr_scratch/step1.2_engineer_draw_r1.md, step1.2_engineer_redfirst.md section 1.
3. research/sean/cr_scratch/step1.2_designer_params_review.md sections 2 to 5 (phase, sector, guide, sightline).
4. ASSEMBLY.md Coordinate frame; research/sean/gameplan.md lines 135-145 (K table), 188-202 (rubric), 243-261.
5. Your 1.1 file: research/sean/cr_scratch/step1.1_topologist_crossreview.md.
6. If S1 r5: docs/sketches/wip/s1_checks_r5.json, s1_spec.yaml.

TASK:
1. Handedness: the sign of (p1 x p2) . z for consecutive screw centres is positive (counter-clockwise), and the same for pinions; the stated phase has the stated sign; hand value beside JSON.
2. Projection: axis-Z parts as circles, radial-axis parts as rectangles or trapezoids (TP-13): the rule as implemented, its premise check with Z and B; sign or FIX.
3. Sector and sightline rows: which side of each boundary each excluded part lies, as half-space sign checks.
4. K9 coverage: every row drawn, no untagged patch, all three screws, pinions and motors present (S2-f).
5. TP-n: list parts drawn narrower than their footprints (projected_extent passes them; M1 must read them).
6. S1 r5 if triggered: sense and projected_extent on changed rows.
Findings as BLOCK, FIX or NOTE with IDs TP1.2-n. Verdict line: "CROSS-REVIEW PASS" or "CROSS-REVIEW FAIL"; separate verdict for S1 r5 if triggered.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_topologist_crossreview.md
Return in context only: verdict(s), counts, TP-13 signed or not, TP-n list length.
```

### P8. The Designer, 1.2 (f) M1 visual gate (parallel with P7a and P7b on r1)

Spawn: **fresh** agent on an image-capable model (the orchestrator's default subagent model; do not override to a text-only model; do not reuse any agent that drew a figure). Background recommended. The reviewer packet excludes `key.json` in every location. On r1 this runs in parallel with P7a/P7b; on r<k+1> (P8r) it runs after the re-checks, again as a fresh spawn.

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Step 1.2 (f), M1 visual gate (gameplan l.188-202; A.3.1 Visual gates). You did not produce these images. You must see pixels: open each PNG with the Read tool. If a Read returns no image content, write your numeric results and the line "visual gate NOT RUN" and stop.
Reviewer-model controls: four extra figures. ctrl_a.png and ctrl_b.png are drill side views: judge each on V1 to V5. ctrl_c.png and ctrl_d.png are plan views: judge each on handedness (+X to the right along the slot line, +Y up, theta counter-clockwise from +X seen from +Z, read from the axis labels and the azimuths drawn). You are not told which figure is which.
S1 r5: [orchestrator states triggered, or not triggered]. If triggered, also gate S1 r5 on the S1 rubric in a separate file.

READ FIRST:
1. Control figures (Read each as an image): docs/sketches/wip/fixtures/figs/ctrl_a.png, ctrl_b.png, ctrl_c.png, ctrl_d.png [orchestrator substitutes the location P0/P4 report; never pass key.json].
2. docs/sketches/wip/s2_plan_r<k>.png and any further S2 figure the spec declares (Read each as an image).
3. docs/sketches/s2_spec.yaml (question, rubric_additions, operator sector, sightline rows).
4. research/sean/gameplan.md lines 176-202 (operator-task table, rubric applicability, M1 rubric V1 to V10), 507-514 (Design Notes 13).
5. docs/sketches/wip/s2_checks_r<k>.json and wip/s2_summary_r<k>.md.
6. If S1 r5: docs/sketches/wip/s1_pose_{load,start,capture_end,park}_r5.png (Read each as an image), docs/sketches/s1_spec.yaml (question, rubric_additions), wip/s1_checks_r5.json, and for comparison docs/sketches/s1_pose_load_r4.png.
Do not open any key.json.

TASK:
1. Controls: one line per figure ctrl_a to ctrl_d with the items above, PASS or FAIL each, with what you see.
2. S2: one line per applicable rubric item (V2, V6, V7, V8, V9, V10; V1, V3, V4, V5 N/A), PASS or FAIL with what you see. V7: ring reads as a structure with housings and mounts, bevel pinions on radial shafts with motors outboard, screws with nut flanges, 30-6060 members as sections.
3. One line per S2 rubric addition.
4. TP-n: for each part drawn narrower than its footprint, say whether the drawn width reads as the part (projected_extent does not catch this).
5. V9: your one-sentence answer to the S2 question from the figure alone, then the spec question.
6. V10: per S2 operator task (load core, collet change, stand and watch, F6 sightline), reach and sightline as you read them.
7. Overall PASS only if every applicable item passes. FAIL items as numbered findings with the feature id.
8. If S1 r5: the same for S1 (V1 to V10, the four S1 rubric additions), plus what changed visibly against r4.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: docs/sketches/wip/s2_visual_gate_r<k>.md (and, if S1 r5, docs/sketches/wip/s1_visual_gate_r5.md). Each file ends with a section "Gameplan lines to change".
Return in context only: control verdicts per figure, S2 overall verdict and FAIL count, S1 r5 verdict if gated.
```

Orchestrator scoring after P8: per `key.json`, ctrl_a must FAIL V3, ctrl_b PASS, ctrl_c PASS handedness, ctrl_d FAIL handedness. Any mismatch: replace the reviewer model and re-run P8 before gating. Record the result in the visual-gate file footer and the Progress Log.

---

### P9. The Engineer, (h) revision r<k+1>

Spawn: background **required**. On r1: after P7a, P7b, P8 (and T5) return, one revision for all findings.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.2 (h): revision r<k+1> of S2 [and S1 r<m+1> if an S1 r5 finding applies]. Sources: [orchestrator lists: step1.2_loftsman_crossreview.md, step1.2_topologist_crossreview.md, docs/sketches/wip/s2_visual_gate_r<k>.md, Sean T5 / M2 rows S2-r<k> verbatim from Design Notes 13].
Rule (h): a correction a signed predicate can express becomes a K8 predicate with a B fixture that reproduces the error. A new or relaxed check rule this revision needs states its premise, enforces it with a check with its own Z and B in this revision, and is signed by its raiser before the revision goes to M1.

READ FIRST:
1. research/sean/gameplan.md lines 163-175 (detail 1 common (h)), 507-514 (Design Notes 13).
2. Every source file named above.
3. docs/sketches/s2_plan.py, s2_spec.yaml, proposed_params.yaml, checks_s2.py, sketch_common.py, fixtures/manifest.yaml.
4. research/sean/cr_scratch/step1.2_engineer_draw_r<k>.md (or step1.2_engineer_revision_r<k>.md).

TASK:
1. Per finding: fix, K8 predicate ID and B fixture or "visual only". A finding that changes a design value or the spec goes to The Designer (list it; spec re-sign by The Designer and, for placement, The Loftsman). A value change to an S1 key goes to the orchestrator for Sean.
2. Redraw as r<k+1> to wip/; run check_sketch.py --controls and check_sketch.py s2 --rev <k+1> (and s1 if affected); iterate to green.
3. Reported values in wip/s2_summary_r<k+1>.md.
4. List new rules and their raisers for signature.
Output: Corrections to the brief; table (finding ID, source, fix, K8 predicate ID or "visual only", B fixture); check results; PNG paths; rules awaiting signature; Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_engineer_revision_r<k+1>.md
Return in context only: findings closed, predicates added, rules awaiting signature, check counts.
```

After P9: P7r re-check by each raiser (same prompt, TASK 0 "verify each of your findings closed against step1.2_engineer_revision_r<k+1>.md; sign any rule you raised", output `step1.2_{loftsman|topologist}_recheck_r<k+1>.md`); then P8r (fresh image-capable spawn on r<k+1>, controls included, output `docs/sketches/wip/s2_visual_gate_r<k+1>.md`). Apply gameplan lines; save point 4; STOP M2.

### STOP M2. Sean: correction pass

Present: `docs/sketches/wip/s2_plan_r<k>.png`, `wip/s2_visual_gate_r<k>.md`, `wip/s2_summary_r<k>.md`; S1 r5 package if triggered (section 2). Sean answers V2 and V9 for S2 (V1 to V5 and V9 for S1 r5), gives free corrections, and picks the options the spec carries (N2 guide option; phase if carried as an option; any S2-A item he deferred). The orchestrator writes each correction into Design Notes 13 as `S2-r<k>` with Sean's words, each pick into Design Notes 13 and Design Notes 27. Corrections: P9, P7r, P8r, M2 again. Acceptance: "S2-r<k> accepted" (and "S1-r5 accepted") with date in Design Notes 13, then ORCH-B.

### ORCH-B. Orchestrator after acceptance

1. `check_sketch.py --accept s2 --rev <k> --note "Design Notes 13 S2-r<k>"`; copy-up from wip/ with equality (PNG, checks JSON, summary, visual gate). Copy `wip/s2_checks_r0.json` up as the S2 red-first record (consistent with H3).
2. If S1 r5 accepted: `check_sketch.py --accept s1 --rev 5 --note "Design Notes 13 S1-r5"` (r4 marked superseded).
3. `check_sketch.py --stale`: 0 differences on every latest accepted record.
4. Apply remaining gameplan lines; save point 5 ("sean: Step 1.2 S2 r<k> accepted").

---

### P10. The Manager, Step 1.2 close

Spawn: background **required** (re-runs `--controls`, 146 s).

```
SYSTEM: You are The Manager (method/operational_guide.md A.12.1; read it, plus A.4 step 7, A.5.2, A.5.3, A.3.1 Visual gates).

CONTEXT:
[CTX COMMON] (The Manager may edit research/sean/gameplan.md and research/sean/accumulator.md.)

READ FIRST:
1. research/sean/cr_scratch/step1.2_manager_open.md (this file: done criteria J1 to J14, section 1.2 S1 r5 rule, section 4 edits).
2. Every research/sean/cr_scratch/step1.2_*.md file; docs/sketches/s2_visual_gate_r<k>.md, s2_checks_r<k>.json, s2_summary_r<k>.md (and S1 r5 equivalents if accepted).
3. research/sean/gameplan.md Steps row 1.2, detail 1 common, detail 1.2, Design Notes 13, 20, 25, 26, 27, Progress Log, Echo Site Registry, Open Questions N2, N6, N11, N12.
4. research/sean/accumulator.md (sections of the personas that ran).

TASK:
1. Verify J1 to J14 with evidence; re-run from docs/sketches/: check_sketch.py --controls, check_sketch.py s2 --rev <k>, check_sketch.py s1 --rev <4 or 5>, --stale. Confirm the runs leave committed files unchanged.
2. Audit that each agent's "Gameplan lines to change" was applied at the save point after that agent (Design Notes 26 decision 4); list misses.
3. Sequencing check for 1.3 (S3): any check cited before the step that writes it (TP-7 inset iteration, TP1.1-9 K5 zero-area lint, S3 block and motor-mount dimensions).
4. Process: count revisions and their causes; system or one-off.
5. Gameplan close edits: Steps row 1.2, Current step, Progress Log, Design Notes 20 and 25 rows closed, Echo Site Registry (frame radius, phase, sector, footprint), Open Questions N2 status.
6. Accumulator entries for every persona that ran and for The Manager.
7. Decisions for Sean at the inter-step gate.
Verdict: READY FOR SEAN or NOT READY with items.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.2_manager_close.md
Return in context only: verdict, J criteria met count, decisions for Sean (under 10 lines).
```

## 4. Blockers

| # | Blocker | Effect | Resolution |
|---|---|---|---|
| B1 | S2-c has no pick, and every option moves a key S1 r4 reads (radius, plate width via a new key, or phase) | (b) cannot write the overlay without reopening S1 | STOP S2-A after P1; S1 r5 per section 1.2 |
| B2 | O1: S2-5 is red by construction while pinions sit mid-sector | S2 cannot go green on the current seeds | P1 item 1b, Sean at STOP S2-A; a reworded rule ships with its premise check (h) |
| B3 | O2: plate widening edits params key `icd.footprint_y`, frozen until 4c; K2 refuses an overlay shadow | That option needs a new overlay key and S1/S2 spec edits | P1 states the cost; Sean rules at STOP S2-A |
| B4 | O3: harness hard-codes S1 in stub tables, sources and baseline; K6 and K7 have no plan-view semantics | S2 stub run and plan K7 cannot run as coded | P0 (per-sketch tables, --baseline sN), P4 (plan rules with Z, B), P5 review |
| B5 | O4: `--controls` rewrites committed fixture outputs | Every verification run dirties the shared tree | P0 R4-c |
| B6 | Batch 1 unanswered (Q2 cutter OD, N10 datum, N12 shaft rating) | S2-a overhang and heights stay ASSUMED | None for 1.2; reported |
| B7 | The 1 m clearance c (N11) has no value | H5 text carries c symbolically | P0 R5; P0L checks; no stop |

Not a blocker: the S1 r5 track runs inside 1.2 under detail 1 common (i) (a back-edge into an accepted sketch); "the next sketch opens only after acceptance" governs S3, which opens after S2 (and S1 r5, if triggered) are accepted.

## 5. Gameplan lines to change (orchestrator, at the open save point)

1. l.12, header Current step. Old: `**Current step:** 1.2 (Step 1.1 approved by Sean 2026-11-25; Step 1.2 not opened)` New: `**Current step:** 1.2 (S2) in progress (opened 2026-11-25, research/sean/cr_scratch/step1.2_manager_open.md)`
2. l.93, Steps row 1.2, status cell. Old: `| Not started |` (last cell of the 1.2 row) New: `| In progress (opened 2026-11-25, research/sean/cr_scratch/step1.2_manager_open.md): step 0, then (a), STOP S2-A, (b) to (h); S1 r5 inside 1.2 if an S1 key moves |`
3. l.169, detail 1 common (d'). Old: `- (d') Orientation preview: the first drawn PNGs go to Sean as soon as they exist, for V1 to V5 only, in parallel with (d) to (f).` New: `- (d') Orientation preview: the first drawn PNGs go to Sean as soon as they exist, for V1 to V5 only (a plan view: V2 and handedness, +X along slot line C, theta counter-clockwise from +X seen from +Z), in parallel with (d) to (f).`
4. l.154, red-first baseline. Old: `(the S1 stub record `s1_checks_r0.json` stays in the frozen scratch folder until 1.2 opens; Design Notes 25)` New: `(the S1 stub record is docs/sketches/s1_checks_r0.json, copied from the frozen scratch folder at 1.2 step 0 (H3); a later sketch writes sN_checks_r0.json to docs/sketches/wip/ at its (c), copies it up with the accepted revision, and `check_sketch.py --baseline sN` assembles its run 2)`
5. l.444, Context Recipes: after the row beginning `| 1.1 (S1), 1.2 (S2), 1.3 (S3), 1.5 (S6) | The Loftsman, The Topologist |` insert the new row: `| 1.2 (S2) to 1.6 (S5), step (c) | The Software Engineer | the sketch's checks_sN.py, sN_spec.yaml, stub and sN_checks_r0.json; check_sketch.py, sketch_common.py, fixtures/manifest.yaml, fixtures/builders.py, baseline_red.json; the harness delta since his last check; method/tdd_method.md Principles 9, 10 |`
6. Design Notes 25, row S2-c, last two cells. Old: `| 1.2 (S2) (a) | The Designer proposes; Sean picks at the S2 M2 |` New: `| 1.2 (S2) (a); Sean picks at STOP S2-A, before (b) writes the overlay (1.2 open: any (a) value that changes a key S1 r4 reads goes to Sean first) | The Designer proposes; Sean picks |`
7. Design Notes, new entry after 26: `**27. Step 1.2 STOP S2-A rulings (Sean, <date>).**` with Sean's words per item (filled at the stop).
8. Progress Log, new row: `| 1.2 | 2026-11-25 | Opened by Manager (research/sean/cr_scratch/step1.2_manager_open.md): done criteria J1 to J14, sequence P0 to P10, stops S2-A, T5, M2; findings O1 (S2-5 red by construction, motor mid-sector), O2 (plate width is a params key), O3 to O7. Next: P0 step 0 harness. |`
