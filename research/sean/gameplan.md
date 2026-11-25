# Cut Jig Configuration and 2D Sketch Gameplan (sean)

**Document(s) under work:** cut jig configuration: 2D sketch set (LLM-PLM section 8.4), then the upper assembly and any base redesign it requires
**Operational guide:** method/operational_guide.md. Contributor: sean. Scratch: research/sean/cr_scratch/. Repository sync rules: section "Repository Sync" at the end of this file; they apply to every step.
**Accumulator file:** none yet; research/sean/accumulator.md is created at Step 0 close
**Other reference files:**
- context/2026-11-24_cutjig_critical_path.md (read first: this week's goal, requirements, open questions, sketch set)
- workorder.md, ASSEMBLY.md, params.yaml, bom_stock_allocation.md
- research/quinn/gameplan.md (Objectives, Design Notes, CAD Test Specification, Source Verification Register; Steps 0 to 7 record)
- supplements/llm_plm_cad.md (section 8.4 sketching phase, 8.4.1 projection checklist, 8.4.2 plot conventions), method/tdd_method.md
**Date:** 2026-11-24
**Current step:** 1.0 (Step 0 approved by Sean 2026-11-24; Step 1.0 not opened)
**lit_review:** no

---

## Start here (from Quinn, 2026-11-24)

Sean leads the cut jig; Quinn reviews. This week's job is to find out what the jig is, on paper, before any more 3D CAD or any cut extrusion.

- **The jig:** a floor-standing, arbor-press-like stand. The core stays upright in a collet at the bottom. The spinning drill (about 800 mm long) travels down over the core and back up, with about 650 mm of travel, so that it can capture a 500 mm core at the end of the project. The core is never inverted, because the test cores are weak cement with no tensile strength.
- **Two modes:**
  - Slice mode: push the core up through a tall collet and cut coaster-thick slices. The collet may be cut along with the core.
  - Capture mode: take one 500 mm core.
- **Material:** on-hand 80/20 30-6060, whole lengths where possible. Lift options are open: arbor press, twin jack screws with Sean's steppers, or something else.
- **Kept:** the collet family, generator, holder, wing nut and receiver. Everything else may be redesigned, and the redesign may change again.
- **Method:** 2D matplotlib sketches first, following LLM-PLM 8.4. The human checks each one for orientation and sense, because the model draws parts upside down and puts the tail on the nose. Start with S1, the whole-jig side view in four poses, which answers whether the jig is tall enough. The full sketch set S1 to S6, the requirements R1 to R18 and the open questions Q1 to Q11 are in `context/2026-11-24_cutjig_critical_path.md`.
- **Week done:**
  - Sketches S1 to S6 have each had a human correction pass.
  - A lift option is chosen, or narrowed to two.
  - Each open question has an answer or an owner.
  - No extrusion is cut.
- **Ask Quinn early:** Q1 (travel), Q2 (drill length and top-end hardware) and Q3 (what spins the drill).

**Update, later on 2026-11-24 (Quinn's decisions):**
- Travel is 650 mm.
- The drill spins on a big bevel ring gear driven by three NEMA 23 pinions at 120 deg. The pinions also carry the drill's weight, with a bushing support ring if needed.
- Everything rides on one ring structure that moves up and down on three jack screws, probably driven by NEMA 17s.
- Lead screws are T8, 800 to 900 mm, under $100 each.

Sketch that configuration; arbor press and hoist are off the table. Details are in section 15 of the critical-path file and Design Note 23 of `research/quinn/gameplan.md`.

Step 0 for the first session: draft the Objectives, Steps, Context Recipes and Design Notes below from `templates/gameplan.md` with the team. Keep this section, and make the sketch set the first step after Step 0.

---

## Objectives

These Objectives govern. In "Start here", the line "Lift options are open: arbor press, twin jack screws ..." and the week-done bullet "A lift option is chosen, or narrowed to two" are superseded by Quinn's update in the same section and by Design Notes 2; "arbor-press-like" describes the motion only (drill moves down over a fixed core).

1. Step 0: a team-reviewed gameplan that Sean approves at the Step 0 gate.
2. Settle the cut jig configuration on paper with the 2D matplotlib sketch set S1 to S6 (LLM-PLM 8.4, recorded deviation in Design Notes 3), plotted from `params.yaml` plus a proposed-keys overlay. Each sketch passes its scripted checks, an image-capable visual gate and a human correction pass before the next sketch is drawn. Every correction goes to Design Notes 13.
3. Draw the configuration Quinn decided on 2026-11-24 (Design Notes 1): 650 mm travel; the drill spun by a bevel ring gear on three NEMA 23 pinions at 120 deg, the pinions carrying drill weight (support ring with bushings if needed); drill, ring gear and motors on one ring structure lifted by three jack screws at 120 deg (NEMA 17 probable); T8 screws 800 to 900 mm, anchored at the bottom so cutting load puts them in tension; the three lift motors moving as one axis.
4. The lift is chosen. Decide what remains open on it: screw sync and step-loss handling, screw anchoring and top guide, ring guidance (anti-rotation, lateral guide, coaxiality carrier), the drill-to-ring bearing, the closed axial and torque load loops, descent end and power-off hold, and the frame that carries the screws (S3, S6, Step 2).
5. Show the jig is tall enough in all four poses (detail 1.1 pose table) and re-derive the park rule and the lift stroke so that test_P10_working_stroke_per_core_class goes green or is retired on the record (S1, Step 4).
6. Give every open question (Q1 to Q11 and the Design Note 23 opens) an answer or a named owner (Step 3).
7. Close the week with the chosen configuration and the list of params keys and tests that change or retire (Q11). The list goes to Quinn with the configuration record before execution; after his review it is executed through LLM-PLM: params first, re-run the tests, record each retired test with its reason; no test or key deleted unrecorded (Steps 4a, 4b, 5, 4c, 6; order in Design Notes 15, T4).
8. No extrusion cut, no production CAD for the upper assembly and no 3D sketch assembly this week. Upper-assembly CAD is scoped at the week-close gate (Step 7 placeholder).

---

## Document Structure

Steps 1 to 4 produce sketches, scripts, check records and decision tables; none is a prose document (the Step 1.0 question batch to Quinn is a question list, checked by Q3-0). The one prose document this phase is the week-close configuration record for Quinn (Step 5), and it runs the TDD stages as ordered sub-steps 5.1 to 5.4. Sean confirms at the Step 0 gate that it is prose (Design Notes 9); if he rules it a table-only record, Steps 5.1 to 5.4 collapse into one table step with its own checks.

**The point, in one sentence:** [Filled at Step 5.1 from the accepted sketches. Pattern: "The cut jig is a ring structure carrying the drill, bevel ring gear and three NEMA 23 pinions, lifted 650 mm on three bottom-anchored jack screws at 120 deg over the kept collet base and a frame of [stock], and these params keys and tests change to match."]

**Shape:** Lead-first (LDR). Quinn reviews by pulling the repo and may stop after the first screen: configuration, sketch links, decisions, change list, open items.

**Opening promises:** Audience: Quinn and Sean. Breadth: the configuration as sketched and accepted, the lift detail decisions, the params and test change list, and the owner of every open question.
**Resolution delivers:** The same breadth, ending on the next step (upper-assembly CAD scoping).

**Known limitations and where each goes:**

| Limitation | Placed in | Why there |
|---|---|---|
| Drill length about 800 mm and drill mass are ASSUMED until Quinn answers Q2 | Configuration section, beside the height stack | The height margin depends on it |
| Sketches are 2D; no interference check on solids (LLM-PLM 7.4 at sketch level is 2D outline overlap) | Method line under the sketch list | Reader weighs the evidence there |
| Ring gear size and source, NEMA 23 gearbox ratio, drill rpm and torque target open | Open items table with owners | Next action |
| Iris drive with three pinions open (INSITU2 157-166, excerpted at `context/literature/INSITU2_text.md` line 7, via Quinn DN23) | Open items table with owner | Next action |
| Kept base parts carry the cut reaction under the screw lift (Design Notes 16); their rating against it is unchecked until Quinn rules (N5) | Configuration section, beside the load loop | Changes the load on parts Quinn designed |

---

## Steps

| # | Step | Assigned To | TDD stage | Status |
|---|------|-------------|-----------|--------|
| 0 | Team wave to draft this gameplan from the critical-path file | The Manager, The Engineer, The Designer, The Systems Engineer, The Software Engineer | Acceptance list: step0_manager_open.md section 1 | Complete. Closed by Manager 2026-11-24 (`research/sean/cr_scratch/step0_manager_close.md`); approved by Sean 2026-11-24 |
| 1 | Sketch set S1 to S6, one sub-step per sketch, each with its own human correction pass before the next is drawn. See detail 1. | The Engineer (spec, scripts, checks), The Designer (params review, spec sign-off, visual gate on an image-capable model), The Loftsman and The Topologist (geometry cross-review on 1.1 (S1), 1.2 (S2), 1.3 (S3), 1.5 (S6)), The Software Engineer (harness at 1.0), Sean (human correction pass) | Per sub-step: spec (outline), red on stub, draw, checks green, orientation preview, cross-review, M1 visual gate, M2 human pass | Not started |
| 1.0 | Sketch harness: proposed-keys overlay, spec format, shared plot and check library K1 to K9, fixtures, red-first baseline; question batch 1 to Quinn pushed first (detail 1.0, last paragraph) | The Engineer (write harness and batch), The Software Engineer (review, signs harness), Sean (approves and pushes the batch) | Test suite before any sketch geometry; Z and B fixture run; stub run; Q3-0 run on the batch | Not started |
| 1.1 (S1) | S1 side XZ, whole jig, four poses: is it tall enough, where does the ring sit on the drill, what is the park rule and the lift stroke, does the axial loop close through the base | The Engineer, The Designer, The Loftsman, The Topologist, Sean | as row 1; checks K1 to K9, S1-1 to S1-6 | Not started |
| 1.2 (S2) | S2 plan XY: footprint, three screws and three pinions at 120 deg, ring guide members, drill and keep-out, collet axis, operator side | The Engineer, The Designer, The Loftsman, The Topologist, Sean | as row 1; checks K1 to K9, S2-1 to S2-5 | Not started |
| 1.3 (S3) | S3 (redefined) side section through one jack screw plus plan inset of all three: bottom anchor, screw and lead, nut mounting, top guide, motor, sync loop, hold device, load arrows, axial loop | The Engineer, The Designer, The Loftsman, The Topologist, Sean | as row 1; checks K1 to K9, S3-1 to S3-3 | Not started |
| 1.4 (S4) | S4 side section through the base: collet, holder, nut, receiver, push-pop advance path, orientation of kept parts | The Engineer, The Designer, Sean | as row 1; checks K1 to K9, S4-1 to S4-3 | Not started |
| 1.5 (S6) | S6 side, ring-gear and pinion close-up: drill head and top end, gear on drill tube, drill-to-ring bearing, pinions, NEMA 23 motors, support ring, guide member, torque and up-thrust loops | The Engineer, The Designer, The Loftsman, The Topologist, Sean | as row 1; checks K1 to K9, S6-1 to S6-5 | Not started |
| 2 | Lift detail decision record (runs after 1.5 (S6), before 1.6 (S5)): consolidates the options Sean chose at each M2 pass and adds the rows no sketch carries. See detail 2. | The Engineer (author), The Systems Engineer (review, runs checklist), Sean (decides), Quinn (consulted on motors and on the descent stop, gate B5) | Checklist plus scripted cross-check X2-1 to X2-5, red on the empty record | Not started |
| 1.6 (S5) | S5 stock map (runs after Step 2): each on-hand 30-6060 length placed in the frame as decided, leftovers | The Engineer, The Designer, Sean | as row 1; checks K1 to K4, K9, S5-1 to S5-3 | Not started |
| 3 | Open-question closeout: batch 1 answers recorded; each Q1 to Q11, DN23 open and N-row gets an answer or an owner. See detail 3. | The Engineer (table), The Manager (owner check, runs Q-check), Sean, Quinn (answers batch 1) | Scripted status check Q3-1, red on the current table | Not started |
| 4a, 4b | Params and test change list (Q11), then Sean's approval of the list. Execution waits for Quinn's review (4c below). See detail 4. | The Software Engineer (test audit, signs), The Engineer (list), The Systems Engineer (ICD and ASSEMBLY.md coherence), Sean (approves the list) | Test audit (Principle 6) is the suite; audit checks A4-1, A4-2 on the list; pytest baseline recorded | Not started |
| 5 | Week-close configuration record for Quinn (prose, A.6.2) carrying the proposed change list, as four ordered sub-steps, then pushed for Quinn's review. See detail 5. | as 5.1 to 5.4; Quinn (review on pull) | Test suite, outline, write, revise | Not started |
| 5.1 | Test suite for the record | The Software Engineer (write), The Designer (comprehension tests) | Suite, about 30 tests, sources verified | Not started |
| 5.2 | Topic-sentence outline, validated against the suite by the coverage matrix | The Engineer (write), The Software Engineer (runs matrix, signs) | Outline plus coverage matrix with Z and B | Not started |
| 5.3 | Write the record from the outline | The Engineer | Suite run on the draft | Not started |
| 5.4 | Revise; echo-site and fact audit | The Designer (review), The Engineer (fix) | Suite re-run after revision, must stay green | Not started |
| 4c | Execution after Quinn's review: params first, ASSEMBLY.md, tests, overlay reduced, re-run pytest, retirement record. See detail 4. | The Engineer (params change, test run), The Software Engineer (audit, signs), Sean (step close) | Audit checks A4-1 to A4-4; pytest before and after | Not started |
| 6 | Manager week close: configuration accepted, change list executed, every question answered or owned, accumulator entries | The Manager, Sean | Re-run of every scripted check from Steps 1 to 5 with hash comparison | Not started |
| 7 | Upper-assembly CAD: placeholder, scoped at the week-close gate | Scoped at the week-close gate | Work order and test suite before geometry (LLM-PLM 7.2) | Not started |

**Execution order:** 0, 1.0 (batch 1 to Quinn first, then the harness), 1.1 (S1), 1.2 (S2), 1.3 (S3), 1.4 (S4), 1.5 (S6), 2, 1.6 (S5), 3, 4a, 4b, 5.1 to 5.4, Quinn's review on pull, 4c, 6. Step numbers keep the draft numbering; the table lists rows in execution order (Design Notes 5 and 15).

### Step details

Source tags used below: **[CP §n, mm:ss]** is a section and meeting timestamp in `context/2026-11-24_cutjig_critical_path.md`; **[DN23]** is Design Note 23 of `research/quinn/gameplan.md`; **[params key]** carries the status written in `params.yaml`. Status words: DECLARED (a human said it), ASSUMED (working value), DERIVED (arithmetic on the others). Z is a zero control (must read clean), B a known-bad control (must fire), tdd_method Principle 9. A check whose B reads clean is broken and blocks the step.

**Reported values.** A value a sketch reports for a decision (height margin to the 2000 mm soft target, screw length against 800 to 900 mm, exposed length of a 100 mm core, leftover stock, gear ratio and torque) has no pass threshold and carries no controls. Its arithmetic is covered by K6 and by the cross-review. A soft key (`jig.height_target`, core lengths beyond 0.5 m) is never asserted (design freedom rule, preamble of Quinn's CAD Test Specification; tests P23); K1 B2 guards this.

**Detail 1.0. Sketch harness.**
Objective: one library every sketch script uses, so each check is written once, shown to fire once, and applied to all six sketches.
Files (all scratch until a sketch is accepted, Design Notes 7):
- `research/sean/cr_scratch/sketches/proposed_params.yaml`: keys the sketches need that `params.yaml` lacks, same leaf schema (value, unit, source, status). Seed namespaces: `drill.length` (800, ASSUMED, [CP §3.2, 18:20]), `drill.mass` (ASSUMED, Q2), `drill.head_od` and `drill.head_length` (cutter and iris head, ASSUMED, labelled "cutter OD ASSUMED"; 152.4 is the tube OD and keep-out basis, not a cutter OD), `drill.top_block_*` (top-end hardware block, length, OD, mass, ASSUMED, Q2), `drill.bore_ceiling_z` (lowest bore-closing part above the cutter, ASSUMED, Q2); `ring.*` with its functional features: three lead-screw nut housings at `jackscrew.pitch_radius` and `jackscrew.angle`, nut mounting (rigid or floating, sets the S3-2 K), three NEMA 23 mounts at `pinion.angle` with the S2 phase, central clearance bore over the gear and `icd.keepout_radius`, gear and support-ring seat, drill-to-ring bearing seat, guide and anti-rotation interface (N2), material and form (plate, printed, or 30-6060 triangle; ASSUMED, Sean), position along the drill (N1), mass; `bearing.*` (drill-to-ring bearing: type, bore, OD, height, axial rating both directions, radial rating; ASSUMED, N4); `guide.*` (ring guide members: type, count, positions, length; N2); `gear.*` (pitch diameter, face width, tooth count, pitch angle, bore, mass), `pinion.*` (count 3, angle 120 deg [DN23], tooth count, pitch angle, motor class NEMA 23 [DN23]), `jackscrew.*` (count 3, angle 120 deg, pitch radius, nominal 8 mm and length 800 to 900 [DN23], root diameter, lead (ASSUMED; the common T8 brass-nut lead of 8 mm back-drives), efficiency, anchor z, top guide z, anchor and guide allowances), `nut.*` is taken in params, so lead-screw nut keys go under `jackscrew.nut_*`; `liftmotor.*` (NEMA 17 [DN23], holding torque ASSUMED), `hold.*` (power-off hold device, Step 2), `frame_upper.*`. Promotion into `params.yaml` happens at Step 4c only (Design Notes 6). The Designer fails a `ring.*` seed at the 1.1 (S1) params review if any listed feature is missing (LLM-PLM 8.4a).
- `research/sean/cr_scratch/sketches/sketch_common.py`: loader (params.yaml, then overlay); `setup_figure(view)`, the only place figure size, dpi, aspect and grid are set; `draw(feature_id, patch)`, which tags each patch with `gid = feature_id`; the check library K1 to K9.
- `research/sean/cr_scratch/sketches/check_stack.py`: pose stack arithmetic from params and overlay. It imports the loader and nothing from the sketch scripts or the drawing helpers (K6 B3 guards this).
- `research/sean/cr_scratch/sketches/check_sketch.py sN [--rev k]`: runs K1 to K9 and the sketch's own checks, writes `research/sean/cr_scratch/sketches/sN_checks_r<k>.json` (per check: ID, result, measured value, threshold, Z result, B result, source tags; per file: SHA-256 of params.yaml and of the overlay, and the list of keys the spec reads with their values) and `sN_summary_r<k>.md` beside it (one screen: pass and fail per check, reported values, open items; the M2 summary Sean reads). `check_sketch.py --stale` compares each accepted revision's recorded key values with the live params and overlay and fails on any difference.
- `research/sean/cr_scratch/sketches/fixtures/`: one Z fixture and the B fixtures per check; `stubs/sN_stub.py`: loads params, calls `setup_figure`, draws the floor line only.
- `research/sean/cr_scratch/sketches/sN_spec.yaml`: the sketch spec (detail 1, step b). It is also the feature table the checks read, so the spec and the checks cannot drift apart.

Spec format (one file per sketch; the sketch's analogue of the topic-sentence outline):
- Header: question (one sentence), R-rows and Q-rows it closes, view (`side_xz`, `plan_xy`, `section_xz`, `stock`), poses, rubric additions, reported values.
- One row per feature: `id`; `name` (label text); `shape` (the Designer's representative-shape note, 8.4b); `kind` (cylinder, cone, gear, screw, prism, plate, line, arrow, callout); `axis` (X, Y or Z, for cylinders and cones); `projection` (rectangle, circle, trapezoid, polygon) per 8.4.1; `keys` (params or overlay keys for every dimension and position); `z_rule` (the stack expression check_stack.py evaluates, floor frame); `depth` (min and max along the view direction, side views only); `label` (key whose value the label prints, rounding); `neighbours` (id, class C, G or F, g_min, source); `sense` (signed predicates for K8); `chain` (torque or weight path membership, S6).

| ID | Check | Z (must read clean) | B (must fire) |
|---|---|---|---|
| K1 | Literals and soft keys: AST scan of the sketch script for numeric literals outside {0, 1, -1, 2, 0.5}; angles come from `pinion.angle`, `jackscrew.angle` or `math.tau`; figure settings live only in `setup_figure`. Also fails on any comparison with a soft key | Fixture reading every value from the loader | B1 planted literal 152.4; B2 planted `assert top < get("jig.height_target")` |
| K2 | Provenance: every spec key resolves in params.yaml or the overlay; every overlay leaf has value, unit, source and a legal status; an overlay key that shadows a params.yaml key fails; a DECLARED overlay leaf cites [CP §n, mm:ss] or [DN23] | Fixture overlay with sourced leaves | B1 overlay key `drill.tube_od`; B2 overlay leaf with empty source; B3 DECLARED leaf with no citation |
| K3 | Plot conventions (8.4.2), read from the Figure object: title contains the spec view name; both axis labels end in "(mm)"; aspect equal; major and minor grid on; figsize at least (14, 10) side or (10, 10) plan; dpi 150 | Conforming fixture figure | One mutated fixture per property (six): no view in title, label without unit, `set_aspect('auto')`, minor grid off, default figsize (6.4, 4.8), dpi 100 |
| K4 | Labels carry their dimension (8.4.2): each spec row with `label` has one annotation containing its name and the number formatted from its key; a label number that differs from the key value fails | Fixture with all labels from keys | B1 label without a number; B2 label "tube OD 150" against `drill.tube_od` 152.4 |
| K5 | Projection (8.4.1): per tagged patch, by spec kind and axis against the view normal: cylinder axis perpendicular to the view, no Circle or Ellipse; axis parallel, Circle; cone in a view showing the taper, four-vertex polygon; an untagged patch fails | Drill tube as rectangle in XZ and as circle in XY | B1 drill tube as Circle in XZ; B2 bevel pinion as rectangle in side view; B3 untagged patch |
| K6 | Stack: check_stack.py evaluates every `z_rule` per pose in the floor frame (z = z_A + `icd.floor_above_datum_a`, ASSEMBLY.md Coordinate frame) and compares each with the drawn patch extent in data coordinates, tolerance 0.05 mm | Fixture drawn from the same params | B1 drill shifted 6.75 mm in the drawing only (6.75 = `collar.top_above_plate`, the smallest term in the collar stack); B2 one part plotted in the datum-A frame (40 mm low); B3 check_stack.py importing a sketch script |
| K7 | 2D overlap between neighbours (LLM-PLM 7.4 at sketch level): convex polygon clipping (Sutherland-Hodgman) and minimum distance in plain Python; non-convex outlines are split into convex pieces in the spec. In side views disjoint depth bands (band gap d > 0) settle class F only: a C pair fails when d exceeds 0.05 mm; a G pair passes when max(d, XZ distance) is at least its g_min, since the 3D distance is at least each projected distance; pairs passed on the bands alone are listed "depth-separated". Classes: C contact (distance 0 within 0.05 mm, overlap area at most 0.01 mm²), G gap at least the pair's g_min, F free (overlap 0). Swept case, same implementation: each moving part (spec `moves: true`) is also tested as its swept envelope, in side views the convex hull of its outline at the lowest and highest pose, in plan the outline against every fixed member whose z band intersects the sweep | Z1 rectangles 100 mm apart read F; Z2 rectangles overlapping in XZ with disjoint depth bands read depth-separated; Z3 touching rectangles read C; Z4 a fixed member above the highest pose reads clean in the swept case | B1 1 mm overlap fires every class; B2 1 mm gap on a C pair fires; B3 a G pair at g_min - 1 fires; B4 a horizontal fixed member at mid-stroke inside the ring outline, clear of all four poses, fires in the swept case; B5 a C pair touching in XZ with depth bands 490 mm apart fires; B6 a G pair (g_min 10) with depth bands 1 mm apart, overlapping in XZ, fires |
| K8 | Sense and orientation: the spec's signed predicates, computed from drawn patch coordinates. Seed set: drill head feature (`drill.head_*`) below the gear and below the top-end block (tail off the nose); drill tip z below drill top z; core bottom on the collet core stop (0 within 0.05 mm); anchor z below nut z below guide z on every screw in every pose; gear section patches mirror about the drill axis at equal z (gear plane normal to Z); motors on the side of the gear the spec states; plan axes not inverted and azimuth counter-clockwise from +X seen from +Z (ASSEMBLY.md Coordinate frame) | Fixture in correct sense | B1 drill flipped tip-up; B2 a screw with its anchor above the nut; B3 plan view with the y axis inverted |
| K9 | Coverage (the figure against its spec, as an outline against its suite): every spec row has at least one patch with its gid; every tagged patch has a spec row | Fixture matching its spec | B1 spec row with no patch (anti-rotation member deleted from the figure); B2 extra tagged patch with no spec row |

g_min seed values for K7 (ASSUMED unless a source is given; The Designer confirms them in each params review, and the spec carries the value and source per pair):
- Any part other than the core, the collet (slice mode) and the gear hub against the drill swept envelope at `icd.keepout_radius` 86.2: G, g_min 0. The keep-out already carries the 10 mm face margin in `drill.r_face`.
- Moving parts (ring, gear, pinions, NEMA 23 motors, lead-screw nuts) against fixed frame members and lift motors: G, 10 mm.
- 0.5 m core top against the drill bore ceiling (`drill.bore_ceiling_z`) at end of capture: G, `stop.g_stop` 25 (DECLARED as the cutter gap; its reuse here is ASSUMED). S1-5a.
- Ring, gear, pinions, NEMA 23 motors and bearing at their lowest pose against the fixed base parts (collet, holder, wing nut sweep `wingnut.sweep_clear_radius` 115, receiver, frame): G, 10 mm. S1-5b.
- Operator loading sector against screws, motors and frame members (plan view): F.

Red-first baseline (Principle 10), two runs, recorded in `research/sean/cr_scratch/sketches/baseline_red.json`:
1. Fixture run: every K-check on its Z and B fixtures. Every Z reads clean and every B fires, or the harness is not signed.
2. Stub run for S1: `stubs/s1_stub.py` with `s1_spec.yaml`. Expected red, each for its own reason: K4, K6, K7, K8, K9 and S1-1 to S1-6. Expected green on the stub, labelled guards: K1, K2, K3, K5 (a stub has nothing to violate; their evidence is the B fixture). A check that is red on the stub only because a file is missing is rewritten until it fails on content. S2 to S6 run their stub at their own sub-step, step (c).
Visual gate: none (no figure of record).
Human gate: none; The Software Engineer signs the harness, the fixture run and the S1 stub run.
Run with `C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe` (matplotlib 3.11.2, PyYAML 6.0.4; shapely absent).

Question batch 1 to Quinn (Start here "ask Quinn early"; critical-path 13.3). File `research/sean/cr_scratch/step1_quinn_batch1.md`, written first at 1.0 open, approved by Sean and pushed as its own save point before the harness work, so Quinn has it before S1 is final. One row per question: ID, question, which sketch or record it feeds, the value used until answered (ASSUMED), answer and date (blank). Contents: Q2 (drill length, mass, top-end hardware, cutter OD); Q9 (core lengths to support; sets the lift stroke, SE-3 via detail 1.1); DN23-a to DN23-e; N5 (the kept base parts carry the cut reaction under the screw lift, Design Notes 16: accept, or name the rating check); N6 (removing the captured 500 mm core from the raised drill); N7 (descent end: is the gate B5 metal stop kept); N8 (ASSEMBLY.md authority, detail 4a); N9 (test_P10_every_key_in_concept_icd_table_exists reads Quinn's cr_scratch file, detail 4a). `research/sean/cr_scratch/step3_check.py` is written here, before the batch; its batch mode, check Q3-0, runs on the batch file: every row has a feed and an ASSUMED stand-in. Z: a complete fixture batch passes. B: a row with a blank stand-in fires. Red-first: Q3-0 on an empty batch file fails. Q3-1 (detail 3) is added to the same script at Step 3, which records the answers.

**Detail 1, common to 1.1 to 1.6.**
Each sketch sub-step runs in this order:
- (a) Designer params review of the keys the sketch will plot, with a representative-shape note per part (8.4a and 8.4b: a ring gear reads as a toothed ring with pinions, a jack screw shows nut, bottom anchor and top guide, the ring structure reads as a structure). The notes go into the spec `shape` field.
- (b) The Engineer writes `sN_spec.yaml`. The Designer signs it, and The Loftsman signs it where cross-review applies. No drawing before the spec is signed.
- (c) Red-first: `check_sketch.py sN --rev 0` on the stub with the signed spec; reds recorded in `sN_checks_r0.json`. A sketch check green on the stub is rewritten.
- (d) The Engineer writes the script and iterates until K1 to K9 (K5 to K8 do not apply to S5) and the sketch checks are green.
- (d') Orientation preview: the first drawn PNGs go to Sean as soon as they exist, for V1 to V5 only, in parallel with (d) to (f). It is not acceptance. Corrections go to Design Notes 13 in the same format as (h).
- (e) Geometry cross-review where the sketch computes placement or projection (A.4 step 2; The Loftsman on arithmetic and placement, The Topologist on orientation and half-space sense). Each reviewer re-computes at least one check value by hand and writes it next to the JSON value.
- (f) M1, visual gate on an image-capable model (A.3.1).
- (g) M2, Sean's correction pass.
- (h) Every correction is recorded in Design Notes 13 as `S<N>-r<k>`. A correction a signed predicate can express becomes a K8 predicate with a B fixture that reproduces the error, so the error cannot return in a later revision or a later sketch. The sketch is redrawn as revision r<k+1> and runs (d) to (g) again until Sean accepts it. The next sketch opens only after acceptance. Where the spec carries an option (sync method, nut mounting, guide member, bearing type, hold device), Sean picks it at this M2 pass and the pick is recorded in Design Notes 13; Step 2 consolidates the picks (Design Notes 5).
- (i) Back-propagation: an edit to any overlay or params key that an accepted spec reads re-runs `check_sketch.py --stale` and `check_sketch.py` on that sketch the same session. If the drawn geometry changes, the sketch opens a new revision and runs (d) to (g). Known back-edges: S4 (taller collet, Q5) moves `stop.collar_top_z` and every S1 height; S6 fixes gear OD, motor envelope, bearing and ring mass that S1 to S3 drew from seeds; Step 2 can change frame members, guide members and the hold device drawn in S1 to S3 and S6.

**Operator tasks (Designer, filled at each params review; the rubric item V10 reads it).**

| Task | Pose | Sketch | Reach height and stance | Sightline | Hazard | Check or rubric |
|---|---|---|---|---|---|---|
| Lift a 0.75 m core (15.6 kg) into the collet under the parked ring | load | S1, S2 | collar top 159.84 to core top; side from S2-5 sector | collet bore from the sector | ring overhead; power-off hold (Step 2) | S1-3, S2-5, V10 |
| Change a collet (wing nut, 230 mm span) beneath the ring, between screws | load | S1, S2 | wing nut sweep radius 115 | wing nut from the sector | screws and motors in reach | S1-5b, S2-5, V10 |
| Advance the core for a slice; take the slice off | start | S4 | collet top | slice plane | cutter at rest only | S4-2, V10 |
| Remove the 500 mm captured core from the raised drill | park | open | open | open | core weight 10.4 kg at height | N6, owner Quinn |
| Stand and watch during a cut | start to end of capture | S1, S2 | outside the swept envelope | cut zone | three exposed pinions and turning gear at the ring height | K7 swept case, V10 |

Rubric applicability: S1 V1 to V10; S2 V2, V6 to V10; S3 V1, V5 to V9; S4 V1, V3 (collet and nut sense), V4, V6 to V10; S6 V1 to V3, V6 to V9; S5 V8, V9 only. A reviewer marks the others N/A.

**M1, visual gate (manual, image-capable reviewer).** The Designer on an image-capable model; the reviewer did not produce the image. Inputs: the PNGs, the spec, the checks JSON. Output: `research/sean/cr_scratch/sketches/sN_visual_gate_r<k>.md`, one line per rubric item: PASS or FAIL with what the reviewer sees. Overall PASS only if every item passes. A text-only reviewer writes its numeric results and "visual gate NOT RUN", and the sub-step cannot close on that file.
Controls, once per reviewer model at the first gate (1.1): the reviewer also receives the K8 Z fixture figure and the K8 B1 figure (drill tip-up), unlabelled. Z must pass; B1 must fail V3. If B1 passes, the reviewer model is replaced before any sketch is gated.

| Item | Rubric (every sketch) |
|---|---|
| V1 | Top on top: the floor is at the bottom of every side view; parts that hang (motors, nuts) hang as the spec states |
| V2 | Spin axis: the drill axis is vertical; the gear section is symmetric about it and the pinion axes are radial, so the drill spins about Z |
| V3 | Tail off the nose: cutting head and iris at the bottom of the drill; gear and drive where the spec puts them |
| V4 | Core upright in the collet, bottom on the stop, never inverted |
| V5 | Screws vertical, anchors at the bottom, guides at the top, nut on the ring |
| V6 | Projection: cylinders seen from the side are rectangles; circles appear only in plan views and end-view insets |
| V7 | Each part reads as the part it is (8.4b): ring gear with teeth and pinions, jack screw with nut, anchor and guide, ring structure as a structure, motor as body and shaft |
| V8 | Labels legible at 100 percent, none overlapping, every labelled feature dimensioned |
| V9 | The reviewer states, from the figure alone, the answer to the spec's question in one sentence; the sentence is compared with the spec |
| V10 | The operator can reach and see each task the operator-task table assigns to this sketch; hands are clear of moving parts in the load pose |

**M2, Sean's correction pass (manual).** Sean sees the PNGs, the M1 file and `sN_summary_r<k>.md`. He answers V1 to V5 and V9 yes or no and gives free corrections. Each correction goes to Design Notes 13 with Sean's words, the fix, and the K8 predicate ID added (or "visual only"). Acceptance is recorded in Design Notes 13 as "S<N>-r<k> accepted" with the date.

PNG naming: `research/sean/cr_scratch/s<N>_<name>_r<k>.png`. Accepted PNG, script, spec and checks JSON move to the shared location proposed in Design Notes 7.

**Detail 1.1. S1, side XZ, whole jig, four poses.**
Question: is the jig tall enough, where along the drill does the ring sit, where are the screw anchors and top guides, what are the park rule and the lift stroke, and which frame and base members carry the axial loop?
Shows: floor, base frame, receiver, collet, holder, nut, core (0.5 m capture core; 0.75 m install core as a dashed outline in the load and park poses), drill as three distinct features: head (cutters and iris, `drill.head_*`, labelled "cutter OD ASSUMED"), tube (rectangle, labelled "tube OD 152.4 (keep-out basis)") and top-end block (`drill.top_block_*`, Q2); keep-out 86.2, ring structure with its functional features (detail 1.0 `ring.*`), drill-to-ring bearing, ring gear, pinions and NEMA 23 motors, two of the three jack screws as projected at their 120 deg azimuths, nuts, anchors, top guides, lift motors, ring guide members (N2) once S2 places them, the descent stop drawn or its absence stated in the spec (Step 2 row, N7), the frame members from anchor to base that close the axial loop (S3-3), the 2000 mm soft target as a reference line. One figure per pose.

Pose table (Sean confirms at the S1 spec; the `z_rule` of every spec row is written per pose from it):

| Pose | Tip z expression (floor frame) | Core drawn | Purpose |
|---|---|---|---|
| load | re-derived park tip z (S1-2 rule) | 0.75 m core mid-insertion, dashed; 0.5 m solid | operator loads a core under the held ring (operator-task table) |
| start | `stop.start_z[0]` with the 0.5 m core; `stop.start_z[1]` dashed for 0.75 m | 0.5 m in the collet | cutter at first contact |
| end of capture | `stop.height_z` | 0.5 m inside the drill bore | lowest ring position; S1-5a, S1-5b |
| park | re-derived park tip z, held by the Step 2 hold device | none required | lift idle, no operator task; top of the lift stroke |

Lift stroke = park tip z minus the lowest stop tip z, maximum over the supported core classes. It is distinct from travel 650 (`upper.travel_max`, start to stop) and sets the screw length (detail 1.3).
Closes: R1 to R8, R17; Q1 (confirms 650 on the drawing), Q9; carries Q2 as ASSUMED 800; re-derives the U13 park rule (`upper.park_z` 959.84 sits below `stop.start_z` 965 for the 0.75 m case) and `stop.height_range[1]` (315, marked not re-derived in params).
Params keys: `upper.travel_max`, `upper.drill_advance_500core`, `upper.load_clearance`, `upper.park_z`, `stop.collar_top_z`, `stop.height_z`, `stop.height_range`, `stop.start_z`, `stop.g_stop`, `core.length_capture`, `core.length_install`, `core.min_exposed`, `drill.tube_od`, `drill.r_face`, `drill.dome_pole_offset`, `drill.kerf_standoff`, `icd.floor_above_datum_a`, `icd.keepout_radius`, `wingnut.span`, `wingnut.sweep_clear_radius`, `upper.park_stroke` (old value, replaced by the reported stroke), `upper.metal_stop` (status per Step 2), `jig.height_target` (reference line only), `profile.*`; overlay `drill.length`, `drill.mass`, `drill.head_*`, `drill.top_block_*`, `drill.bore_ceiling_z`, `ring.*`, `bearing.*`, `guide.*`, `gear.*`, `pinion.*`, `jackscrew.*`, `liftmotor.*`.
Script: `research/sean/cr_scratch/sketches/s1_side_poses.py`. PNGs: `research/sean/cr_scratch/s1_pose_load_r1.png`, `s1_pose_start_r1.png`, `s1_pose_capture_end_r1.png`, `s1_pose_park_r1.png`.

| ID | Check | Z | B | Source |
|---|---|---|---|---|
| S1-1 | Capture reach: start tip z minus end-of-capture tip z is at least `upper.drill_advance_500core` and at most `upper.travel_max` | Live params | Fixture with `upper.travel_max` 500 (below 534.93) | travel DECLARED [CP §15], [DN23]; advance DERIVED |
| S1-2 | Park above the working range: park tip z above max(`stop.start_z`) for every supported core class | Fixture with the re-derived park rule | Live params.yaml (959.84 below 965), the red state of test_P10_working_stroke_per_core_class | [DN23] (U13 re-derive); park ASSUMED |
| S1-3 | Park clears the install core: park tip z minus `upper.load_clearance` at least core-stop z plus core length, for each length in the spec's Q9 list | Live params with the re-derived rule | Park z lowered by `upper.load_clearance` + 1 | `core.length_install` DECLARED; clearance ASSUMED |
| S1-4 | Ring within nut travel at all four poses: anchor z + anchor allowance + half nut length at most nut z, and nut z at most guide z - guide allowance - half nut length | Fixture from the spec | Ring 100 mm above the top guide at park | overlay `jackscrew.*` ASSUMED |
| S1-5a | Core top below the drill bore ceiling at end of capture: `drill.bore_ceiling_z` minus 0.5 m core top z at least 25 (K7 G) | Fixture from the spec | Drill internal length (tip to `drill.bore_ceiling_z`) set below `upper.drill_advance_500core` | `stop.g_stop` reuse ASSUMED; bore ceiling ASSUMED (Q2) |
| S1-5b | Ring assembly (ring, bearing, gear, pinions, NEMA 23 motors) at end of capture clears the fixed base parts (collet, holder, wing nut sweep, receiver, frame) by 10 mm (K7 G); this sets the lower bound of N1 | Fixture from the spec | `ring.position` at the drill's lower third | 10 mm ASSUMED; `wingnut.sweep_clear_radius` DERIVED |
| S1-6 | Screw projection: drawn x of each screw equals r cos(theta), depth band at r sin(theta), theta per ASSEMBLY.md Coordinate frame | Fixture from the spec | Screw drawn at x = r | overlay `jackscrew.angle` DECLARED [DN23] |

Reported: highest point at each pose and its margin to the 2000 mm soft target; ring position along the drill (N1) and the anchor and guide heights it sets; the re-derived park rule as an expression for Step 4; lift stroke and screw length L (detail 1.3 formula) for each Q9 option (0.5 m only; 0.5 and 0.75 m; plus 1 m), so Quinn's Q9 answer selects the screw length; centre-of-mass height per pose and the unbolted tip force at the top of the frame (overlay masses, ASSUMED; `icd.tipover_statement` is the old-design reference).
Rubric additions: the ring is on the drill above the core in every pose; the motors sit on the same side of the gear in every pose; the 0.75 m core is dashed in the load and park poses only; the drill head is at the bottom and the top-end block at the top.
Cross-review: The Loftsman (stack arithmetic, S1-6 projection), The Topologist (sense: anchors below nuts, tip down).
Gate: M1 by The Designer on an image-capable model (with the reviewer controls), then M2.

**Detail 1.2. S2, plan XY.**
Question: does it fit, stay coaxial, and leave the operator a side to load the core and change collets?
Shows: base footprint (644 x 608 today, open), frame members, three screw axes at 120 deg on their pitch radius, three pinion and NEMA 23 positions at 120 deg (phase relative to the screws is a sketch choice to state), ring structure with its nut housings, motor mounts and clearance bore, ring guide members (N2: rails or rods, which may also be the anti-rotation member; option drawn, Sean picks at M2), drill tube and keep-out as circles (end view), collet axis, slot lines, operator loading sector and sightline to the collet.
Closes: R9, R13, R16 (layout part); the frame's role under a ring on three screws (Design Notes 2); the operator access question.
Params keys: `drill.tube_od`, `drill.tube_id`, `icd.keepout_radius`, `icd.footprint_x`, `icd.footprint_y`, `icd.datum_*`, `icd.mounting_pattern`, `frame.*`, `profile.*`, `base.*`; overlay `pinion.*`, `jackscrew.*`, `ring.*`, `guide.*`, `frame_upper.*`.
Script: `research/sean/cr_scratch/sketches/s2_plan.py`. PNG: `research/sean/cr_scratch/s2_plan_r1.png`.

| ID | Check | Z | B | Source |
|---|---|---|---|---|
| S2-1 | Azimuths measured from drawn centres: screws 120 deg apart within 0.1 deg; pinions likewise; the stated screw-to-pinion phase within 0.1 deg | Fixture from the spec | One screw at 110 deg | [DN23], [CP §15] |
| S2-2 | Screws clear the keep-out: screw pitch radius minus nut flange radius minus `icd.keepout_radius` at least 10 mm (K7 G) | Fixture from the spec | Screw pitch radius equal to the keep-out radius | keep-out DERIVED; 10 mm ASSUMED |
| S2-3 | Pinion mesh: each pinion pitch point at the gear pitch radius within 0.05 mm | Fixture from the spec | Pinion placed on the gear OD | overlay `gear.*` ASSUMED |
| S2-4 | Nominal coaxiality: drill, collet, ring and gear centres coincide within 0.05 mm (nominal only; R13 is carried by the Step 2 guidance row) | Fixture from the spec | Collet axis drawn 2 mm off | R13 ASSUMED [CP §14] |
| S2-5 | Operator sector (apex on the axis, half-angle and radius in the spec, set by The Designer) free of screws, motors and frame members (K7 F) | Fixture with a 90 deg sector between two screws | Sector widened to 130 deg, wider than the gap between two screws at 120 deg | sector ASSUMED |

Reported: outline extents against the current 644 x 608 footprint (open, not asserted); footprint against the S1 unbolted tip force (bolt-down or footprint goes to the Step 2 row, R1).
Cross-review: The Loftsman (azimuths, radii), The Topologist (handedness: +X along slot line C, theta counter-clockwise from +X seen from +Z per ASSEMBLY.md; K8 B3).
Gate: M1, then M2.

**Detail 1.3. S3, redefined: side section through one jack screw.**
The critical-path 7.3 definition ("S1 drawn once for option A and once for option B") is void: the lift is decided. Redefinition for Sean to confirm (Design Notes 4): a one-screw section plus a plan inset of all three screws and the sync loop; S1 draws the ring and screws in elevation, which with S3 meets critical-path 15 ("S1 and S3 draw the ring and three screws").
Question: how is each screw anchored, guided, driven and synced, does the 1000 N axial load put it in tension, what holds the ring with power off, and does the axial load loop close?
Shows: bottom anchor with thrust bearing, screw (rectangle, 8 mm nominal, lead labelled from `jackscrew.lead`), brass nut on the ring with its mounting (rigid or floating, option drawn, Sean picks at M2; the choice sets the S3-2 K), top guide (radial support only), NEMA 17 mount and coupling, power-off hold device (option drawn: non-back-driving lead, brake, or park pin with visible state; Step 2 decides), load arrows per load case, frame member that carries the anchor and the guide and its connection to the base frame. Plan inset (end view, circles allowed): all three screws at 120 deg with the sync loop (belt path and pulleys at all three screws, or the single-controller callout), so K9 sees all three.
Closes: R14 (path and loop), Q7 detail, Q8 (powered feed), DN23 sync and anchoring items; TR10/TR12 fallback check; the axial-loop half of SE-2 (Design Notes 16).
Params keys: `loads.axial_design`, `loads.wob_max`, `upper.travel_max`, `core.length_capture`, `profile.*`; overlay `jackscrew.*`, `liftmotor.*`, `hold.*`, `ring.*`, `bearing.*`, `gear.*`, `pinion.*`, `drill.mass`, `frame_upper.*`.
Script: `research/sean/cr_scratch/sketches/s3_jackscrew_section.py`. PNG: `research/sean/cr_scratch/s3_jackscrew_section_r1.png`.
Load cases (spec table; per-screw force = case load / 3, equal share ASSUMED; the two-screw share, load / 2, is reported):
- Cut: 1000 N up on the ring (`loads.axial_design`, ASSUMED design choice).
- Static: W down, W = ring + drill + gear + three NEMA 23 + nuts (overlay masses, ASSUMED until Q2 and DN23-d are answered).
- Capture lift: W + the 0.5 m core, 10.4 kg (Quinn's Source Verification Register: DERIVED, density ASSUMED).
- Retract with bind: W + F_bind (ASSUMED; Sean owns the value at Step 2).
- Stall thrust: the axial force the three lift motors deliver at stall, F_stall = 3 x 2 pi T_hold eta / lead (NEMA 17 holding torque, `jackscrew.lead` and `jackscrew.efficiency` stated, all ASSUMED). It applies in both directions and is independent of the cut (a crash at the end of travel).
In the capture-lift and retract cases the screw segment below the nut is in compression; S3-2 covers them (The Software Engineer's estimate: margin 1.5 at K = 1 in capture lift, fail at K = 2).

| ID | Check | Z | B | Source |
|---|---|---|---|---|
| S3-1 | Sign: the screw segment from nut to anchor is in tension in the cut case at every nut position from the S1 poses | Spec as drawn (bottom anchor) | Anchor moved to the top guide (screw hung from the top) | [DN23] |
| S3-2 | Buckling of the nut-to-anchor segment at its longest (nut at park), worst compression case per screw: P_cr = pi² E I / (K L)², I = pi d_r⁴ / 64. Pass: P_cr / F at least SF. Inputs stated in the spec: d_r (T8 root diameter, ASSUMED until vendor data, Sean), E (ASSUMED), K from the nut mounting in the spec (1.0 rigid nut, nut and anchor both held laterally; 2.0 floating nut), SF (ASSUMED 3, Sean confirms) | 100 mm segment under W | 1000 N compression on an 850 mm T8, which [DN23] states would buckle | [DN23]; inputs ASSUMED |
| S3-3 | Axial loop closed in the cut case: spec `chain` cutter, core, collet core stop, collet, holder, receiver, base plate, base frame, anchor frame member, anchor, screw (tension), nut, ring, drill-to-ring bearing, drill tube, cutter; every consecutive pair class C in the drawn figures (S1 for core, base and frame members; S3 for anchor, screw, nut, ring; S6 for bearing and tube), K7 C | Fixture from the specs | Anchor frame member drawn 1 mm clear of the base frame (loop open) | SE-2; ASSEMBLY.md Load path (old loop, superseded in the cut case, Design Notes 16) |

S3-3 runs at 1.3 (S3) on the S1 and S3 figures, with the ring-to-bearing-to-tube segment taken from the spec as declared contacts; at 1.5 (S6) the segment is drawn and S6-5 checks it, and S3-3 re-runs on all three figures (step (i)). X2-5 confirms both green on the accepted revisions.
A failure of S3-2 is a finding for the Step 2 screw-size row (TR10 or TR12, or a compression-free mounting), not a redraw by itself.
Reported: screw length L = lift stroke (detail 1.1) + nut length + anchor allowance + guide allowance + ring nut-housing height, per Q9 option, against the 800 to 900 mm estimate in [DN23] (built on 650; outside the range goes to Sean with the sketch); critical speed at the stated rapid traverse (ASSUMED) with the end-condition factor stated; P_cr margin for every compression case; F_stall; axial force in each kept part (collet, holder, receiver, base plate) at 1000 N and at F_stall, for Quinn's N5 ruling; back-drive (lead angle against friction angle, ASSUMED friction) for the power-off hold row.
Sync: the spec states the method drawn. A belt is checked by K7 (belt path against keep-out and frame) and K9 (pulleys at all three screws in the plan inset); one controller is a K9 callout. The step-loss handling (belt, per-screw home switches, re-level at park) goes to the Step 2 sync row.
Cross-review: The Loftsman (lengths, buckling arithmetic, hand re-computation of P_cr and F_stall), The Topologist (anchor below nut in every pose, K8; S3-3 chain order).
Gate: M1, then M2.

**Detail 1.4. S4, side section through the base.**
Question: how does the core move up through the collet (push-pop), and does the kept collet family cover a 100 mm tall core?
Shows: collet, holder, wing nut, receiver, PTFE washer, core stop, and the advance path for the core (the current receiver has a floor and the core stands on the collet core stop, so nothing moves the core up today); taller collet option; sacrificial collet or liner option; 100 x 100 mm core.
Closes: R10, R11, R12; Q4, Q5, Q6, Q10.
Params keys: `collet.*`, `holder.*`, `receiver.*`, `nut.*`, `washer.*`, `seat.*`, `collar.*`, `witness.zone_high`, `core.diameters`, `core.length_*`, `icd.floor_above_datum_a`.
Script: `research/sean/cr_scratch/sketches/s4_base_section.py`. PNG: `research/sean/cr_scratch/s4_base_section_r1.png`.

| ID | Check | Z | B | Source |
|---|---|---|---|---|
| S4-1 | check_stack.py computes the collar top with the formula of test_P18_collar_top_recomputed_from_params (tests/test_params_bom.py 694-702) and gets `stop.collar_top_z` 159.84 within 0.01 mm; drawn heights follow through K6 | Live params | `holder.flange_thickness` dropped from the stack (151.84) | `stop.collar_top_z` DERIVED |
| S4-2 | Advance path against the receiver floor (K7 F): the core's upward path from the core stop does not pass through receiver solid | Fixture with a floor opening | The current receiver as built (floor present) | [CP §9, Q4] |
| S4-3 | Orientation of the kept parts (K8 predicates in the S4 spec): collet taper sense per `cone.alpha`, narrow end as in ASSEMBLY.md; wing nut above holder; washer between nut and holder; receiver floor at the bottom | Fixture in correct sense | Collet flipped end for end | ASSEMBLY.md; critical-path 7.1 (backcap failure) |

Reported: exposed length of a 100 mm tall core against `core.min_exposed` 143.12 (Q10); collet length options (Q5); sacrificial collet or liner (Q6).
Back-edge: a taller collet (Q5) moves `stop.collar_top_z` and every S1 height; step (i) re-runs S1.
Cross-review: none required (no new placement computed); The Designer reviews the kept parts as drawn.
Gate: M1, then M2.

**Detail 1.5. S6, side, ring-gear and pinion close-up (drawn before S5, Design Notes 5).**
Question: where does the spin torque go, what carries the drill weight, what locates the drill on the ring radially and against the cut up-thrust, and how does the iris drive sit with three pinions?
Shows: drill head (`drill.head_*`, "cutter OD ASSUMED"), tube ("tube OD 152.4 (keep-out basis)") and top-end block as distinct features; the ring gear mounted on the tube; the drill-to-ring bearing as a named feature (radial plus axial in both directions: slewing ring, thrust pair, or tube collar bearing on the ring; option drawn, Sean picks at M2, N4); three bevel pinions (two visible in projection, trapezoids in side view), NEMA 23 motors with optional gearbox, support ring with shaft bushings, the ring structure section, the ring guide and anti-rotation member (N2; the screws react torque only in bending), torque loop, weight path and up-thrust path. Plan inset of the gear and pinions (end view: circles allowed). A callout "iris drive: open, owner Quinn" (DN23-e).
Closes: R4, R5, R15 (torque against core holding, reported); Q3 detail; N4 option; DN23 opens on ring gear size and source, gearbox ratio, drill rpm and torque target (as owner items if unanswered), iris drive with three pinions (as owner item).
Params keys: `drill.tube_od`, `drill.r_face`, `drill.kerf_standoff`, `icd.keepout_radius`, `icd.torque_reaction` (old value "not carried by the base"; REWRITE on the Step 4 list), `loads.torque_design`, `loads.axial_design`; overlay `gear.*`, `pinion.*`, `ring.*`, `bearing.*`, `guide.*`, `drill.length`, `drill.mass`, `drill.head_*`, `drill.top_block_*`, `frame_upper.*`.
Back-edge: gear OD, motor envelope, bearing and ring mass fixed here replace the seeds S1 to S3 drew; step (i) re-runs them.
Script: `research/sean/cr_scratch/sketches/s6_ring_gear.py`. PNG: `research/sean/cr_scratch/s6_ring_gear_r1.png`.

| ID | Check | Z | B | Source |
|---|---|---|---|---|
| S6-1 | Gear bore fit: gear bore minus `drill.tube_od` inside the spec fit band | Fixture from the spec | Bore = tube OD - 1 mm | fit band ASSUMED |
| S6-2 | Bevel geometry from the drawn trapezoid edges: gear and pinion pitch lines meet within 0.5 mm of the drill axis at the spec apex height; for a 90 deg shaft angle, tan(gear pitch angle) = gear teeth / pinion teeth within 0.5 percent | Fixture from the spec | Gear and pinion pitch angles swapped | overlay `gear.*`, `pinion.*` ASSUMED |
| S6-3 | Torque loop closed: spec chain cutter, drill tube, gear, pinion, NEMA 23 mount, ring, guide and anti-rotation member, frame, base frame, base plate, receiver, collet, core, cutter; each consecutive pair is class C in the spec and touching in the figures (K7 C; base members from S1 and S4) | Fixture from the spec | Anti-rotation member removed | Design Notes 11; SE-5; `icd.torque_reaction` contradicted (REWRITE, detail 4a) |
| S6-4 | Weight chain closed: drill, gear, pinions (and support ring if drawn), ring, nuts, screws, anchors, frame; same method | Fixture from the spec | Support ring drawn 1 mm clear of the pinion shafts | [DN23] |
| S6-5 | Cut up-thrust chain closed off the pinion teeth: cutter, drill tube, tube collar or gear hub, drill-to-ring bearing, ring; each pair class C (K7 C); the pinion mesh is not in the chain | Fixture from the spec | Bearing removed, so the only path from tube to ring runs through the pinion teeth | SE-1; N4 |

Reported: gear ratio; maximum drill torque (three NEMA 23 torque times gear ratio times gearbox ratio, DN23-b, DN23-c open) against `loads.torque_design` 10 N m (R15 core holding), flagged to Sean and Quinn when above (the core spins in the collet); reaction torque the anti-rotation member carries; axial and separating force per pinion in the static and cut cases; bearing axial load in the cut case (1000 N up) and the static case (W down), against the `bearing.*` ratings.
The iris drive is untestable this week: the drivetrain that closes the iris (INSITU2 via [DN23]) has no defined path through three pinions. K9 requires the callout; Step 3 owns the question.
Cross-review: The Loftsman (bevel apex, gear ratio arithmetic, pinion force resolution), The Topologist (pinion side and spin sense; up-thrust and torque loop order).
Gate: M1, then M2.

**Detail 1.6. S5, stock map (runs after Step 2).**
Question: can the frame, screw supports, guide and anti-rotation members be built from whole on-hand lengths?
Shows: each on-hand 30-6060 length (1540 x 4, 980 x 4, 952 x 1, 728 x 2, 644 x 2, 488 x 2, 468 x 2) placed as a bar, assigned to a member from S1 to S3, S6 and the Step 2 record, with leftovers; the base members already allocated (644, 488, 468) shown as allocated.
Closes: R16; the 1540 reservation in `bom_stock_allocation.md` (held for columns that no longer exist).
Params keys: `stock.on_hand`, `frame.members`, `profile.*`; overlay `frame_upper.*`.
Script: `research/sean/cr_scratch/sketches/s5_stock_map.py`. PNG: `research/sean/cr_scratch/s5_stock_map_r1.png`.

| ID | Check | Z | B | Source |
|---|---|---|---|---|
| S5-1 | Per stock length, assigned pieces at most the on-hand quantity | Base allocation only | One 1540 assigned five times | `stock.on_hand` DECLARED |
| S5-2 | Every frame member in the accepted S1, S2, S3 and S6 specs and the Step 2 record maps to a stock length or to the extra-cut table | Fixture from the specs | One member unmapped | specs |
| S5-3 | Each member's cut length at most its source length | Fixture from the specs | A 1000 mm member from a 980 | `stock.on_hand` DECLARED |

Reported: leftovers per length; count of members that need a cut (R16 prefers whole lengths); 1540 use, which conflicts with test_P3_1540_unused and goes on the Step 4 list.
K5 to K8 do not apply (a stock map has no projection, stack or sense). Rubric: V8, V9 only. Cross-review: none (no placement). A stock shortfall that forces a member change reopens the Step 2 row and the sketch that drew the member (step (i)).
Gate: M1, then M2.

**Detail 2. Lift detail decision record.**
Objective: one table that consolidates the options Sean picked at the S1 to S4 and S6 M2 passes (Design Notes 13) and decides the rows no sketch carries. It runs before S5 so the stock map places decided members once (Design Notes 5).
Rows, each with a choice or an owner and a due step:
- Sync method and step-loss handling (belt link, or single controller with per-screw home switches and re-level at park) (S3 pick; SE-16).
- Anchoring (bottom thrust bearing, top guide type) (S3 pick).
- Nut mounting, rigid or floating, and the K it sets (S3 pick).
- Ring guidance: anti-rotation, lateral guide, coaxiality carrier; reason cites R13 (S2, S6 picks; N2).
- Drill-to-ring bearing type and source, ratings against the S6 reported loads (S6 pick; N4).
- Screw size: T8 if every compression case passes S3-2, TR10 or TR12 otherwise, or a compression-free mounting (axial bearing at the top as well).
- Lift motor count against the NEMA 17s on hand (DN23-a).
- F_bind value.
- Descent end: hard stop kept (form, location, rating against F_stall and 1000 N) or replaced by limits (switch type, per-screw homing); `upper.metal_stop` (DECLARED, gate B5) retires only on Sean's recorded ruling with the replacing function named, Quinn consulted (N7).
- Power-off hold: non-back-driving lead, brake, or park pin with visible state; replaces `upper.park_lock` (ASSUMED, flagged) only on Sean's recorded ruling (N7).
- Bolt-down or footprint against the S1 tip force, R1 named (SE-12).
- Base carries the cut reaction: Quinn's N5 ruling recorded, or the row stays OWNED by Quinn with the Step 3 due point.
Inputs: accepted S1, S2, S3, S4, S6 and their checks JSON; Design Notes 13 picks; [DN23]; batch 1 answers received so far.
Output: `research/sean/cr_scratch/step2_lift_decision.md` (table: item, options, choice, reason, sketch revision, check ID or source, owner if open). A choice that changes a member drawn in S1 to S3 or S6 opens a new revision of that sketch (step (i)).
TDD stage: checklist and one scripted cross-check, both written before the record.
Checklist (The Systems Engineer, manual): every row that consolidates a sketch pick cites the accepted sketch revision and the Design Notes 13 entry; every other row cites its source or batch 1 answer; every reason names a check ID or a DECLARED source; every row has a choice, or an owner and a due step.
Scripted cross-check `research/sean/cr_scratch/step2_check.py` (the record against the accepted sketch files, where slips between files happen):

| ID | Check | Z | B |
|---|---|---|---|
| X2-1 | Screw-size row says T8 only if every compression case passes S3-2 in the accepted S3 checks JSON | Consistent fixture record | T8 row against a failing S3-2 margin |
| X2-2 | Sync row matches the method in the accepted S3 spec | Consistent fixture | Record says belt, spec says one controller |
| X2-3 | The anti-rotation member named in the record exists in the accepted S6 spec and in the S5 allocation | Consistent fixture | Member present in S6, absent from S5 |
| X2-4 | Lift motor row: NEMA 17 count on hand at least 3, or the row states how the shortfall is met | Count 3 | Count 2 with no plan |
| X2-5 | Every accepted sketch revision the record cites is current: `check_sketch.py --stale` clean, and S3-3, S6-3, S6-5 green in the current checks JSON | Fixture record citing current revisions | Record citing an S1 revision whose recorded `stop.collar_top_z` differs from the live value |

The anti-rotation member in X2-3 is checked against the S5 allocation at 1.6 (S5) close; before S5 exists X2-3 checks the S6 spec only.
Red-first: the script on an empty record fails all five.
Visual gate: none (table).
Human gate: Sean decides each row; Quinn consulted on motor counts and the descent stop.

**Detail 3. Open-question closeout.**
Objective: every Q1 to Q11, DN23 open item and N-row has an answer (with source and date) or an owner and a due point. Batch 1 went to Quinn at 1.0; this step records his answers and sends a second batch only for questions the sketches raised.
Output: the Open Questions section of this gameplan updated, plus `research/sean/cr_scratch/step3_question_sweep.md` (batch 1 answers, any batch 2, and which sketch or record each closes).
TDD stage: scripted check `research/sean/cr_scratch/step3_check.py`, Q3-1: each row of the Open Questions table has status ANSWERED (source, date) or OWNED (name, due step); an ANSWERED source must resolve to a file on disk and a section or line that exists there (Principle 7). Z: a fully filled fixture table passes. B1: one blank owner fires; B2: an ANSWERED row citing a section that does not exist fires.
Red-first: run on the current Open Questions table, which has open rows; record the failures.
Visual gate: none.
Human gate: Sean confirms owners; Quinn answers Q2 and the drill items.

**Detail 4. Params and test change list, then execution (Q11).**
Objective: change the shared design files to match the accepted configuration through LLM-PLM 5.2 and 7.2: params first, re-run tests, record what retires. Nothing deleted unrecorded ([CP §10], tdd_method Principle 6).
4a. Change list (before any edit), file `research/sean/cr_scratch/step4_change_list.md`: every params key that changes, is added (promoted from the overlay) or becomes void; every test or probe that names those keys or the retired structure; disposition per test: KEEP, REWRITE (new criterion, LLM-PLM 7.2 change-order step 3), RETIRE (reason, replacing test or "none" with reason). Search terms: each key string, plus `column`, `hoist`, `carriage`, `park`, `strap`, `1540`, `manual_raise`, `raise_fuse`, over `tests/` and `tests/probes/`. Seed list from the current tests (grep 2026-11-24), to be completed by the audit:
- Keys: `upper.park_z`, `upper.park_stroke`, `upper.park_lock`, `upper.manual_raise`, `upper.raise_fuse`, `upper.load_clearance`, `upper.metal_stop`, `hoist.anchor_member`, `column.spacing`, `strap.rating`, `strap.handle_radial`, `stop.height_range`, `stop.start_z`, `stop.pad_xy` (column face 244), `icd.coaxiality_chain` (column foot 0.283, carriage guide 0.15), `icd.column_foot_moment`, `icd.torque_reaction`, `icd.tipover_statement`, `icd.mass_target`, `icd.footprint_x`, `icd.footprint_y`, `frame.members`, the `bom_stock_allocation.md` 1540 reservation.
- tests/test_params_bom.py: test_P10_working_stroke_per_core_class; test_P10_icd_frozen_keys_exist_with_source_and_status (ICD_FROZEN pins `upper.park_z`, `upper.manual_raise`, `upper.raise_fuse`, `hoist.anchor_member`, `column.spacing`, `strap.*`, `stop.start_z`, `stop.height_range`, `icd.coaxiality_chain` by value); test_P10_every_key_in_concept_icd_table_exists; test_P10_coaxiality_chain_sums_inside_budget; test_P10_stop_ownership_upper_assembly; test_P10_assembly_load_loop_ten_members; test_P6c_working_stroke_per_core_class; test_P6d_park_clears_core_both_lengths; test_P17_key_present[upper.load_clearance]; test_P18_changed_value rows `stop.height_range`, `stop.start_z`, `upper.park_z`, `upper.park_stroke` (values pinned); test_P18_start_z_and_park_arithmetic (park rule pinned); test_P3_1540_unused; test_P3_allocation_respects_stock; test_P5_frame_profile_bbox_and_length; test_P2_status_counts_match_register and test_P7_every_assumed_or_declared_listed (both move when keys are promoted); test_P7_keys_the_cad_tests_read_exist_or_are_declared_gaps (fails if a test still names a voided key).
- Keys with a fixed disposition: `upper.metal_stop` (DECLARED, gate B5) and `upper.park_lock` (ASSUMED, flagged for the human) retire only on Sean's recorded Step 2 ruling, with the replacing function named in the row; the strap keys follow the Step 2 power-off hold row. `icd.torque_reaction` ("not carried by the base") is REWRITE: under the decided configuration the torque loop closes through the base (S6-3). `upper.park_stroke` is REWRITE to the S1 lift stroke.
- tests/test_assembly.py: test_A2d_no_cutter_or_lead_in_face_bears_on_the_core_at_the_stop (axial force 0 at the stop; false during a powered cut, S3-3); test_A1c_no_printed_solid_in_the_column_foot_path, test_A1d_column_to_base_plate_is_class_G_or_F, test_A1e_strap_handle_clears_the_parked_upper_assembly, test_A3b_built_fits_within_the_coaxiality_chain_column_foot_and_carriage_guide (green_at_12), test_P6b_frame_solids_644_by_608. tests/test_step7_fix_controls.py: the A3b and P6b control tests. tests/probes/probe_poses.py: `fit_column_foot`, `fit_carriage_guide`. tests/test_step6_parts.py: base `column_notch` feature.
- ASSEMBLY.md: ICD row "travel 500 with start_z 684.84 / 815" (stale against params 650 and 834.84 / 965); Load path bullets for descent ("1000 N path is cutter, carriage, metal stop, columns, frame. It never enters the nut, holder, collet, receiver or base plate. Drill torque is not carried by the base."), manual raise and column feet, rewritten from the S3-3 axial loop and the S6-3 torque loop; the core-cutter pair row citing A2d.
- Cross-contributor dependencies (both in batch 1 to Quinn at 1.0, ruling needed before 4b): (N9) test_P10_every_key_in_concept_icd_table_exists reads `research/quinn/cr_scratch/step2_system_concept.md`, which this gameplan may not edit; disposition REWRITE to read a shared ICD source, or KEEP with the voided keys left in params as VOID. (N8) ASSEMBLY.md line 3 names the same file as its source and the ICD as frozen there; proposal: ASSEMBLY.md (or a shared ICD file under `docs/`) becomes the authority for the redesigned rows. 4c does not edit ASSEMBLY.md ICD or load-path rows until Quinn rules.
4b. Sean approves the list. The approved list goes into the Step 5 record as a proposal.
(Step 5 runs here; the record is pushed and Quinn reviews it on pull. His review is the gate into 4c.)
4c. Execution after Quinn's review: edit `params.yaml` first (promoted overlay keys added; each promoted key deleted from `proposed_params.yaml` in the same change, so K2 shadowing stays clean), then ASSEMBLY.md, then tests (rewrite or retire, with a retirement table in `research/sean/cr_scratch/step4_test_retirement.md`: test ID, old criterion, reason, replacement), then run pytest and record collected, pass, fail against the baseline. Repository Sync rules apply; a conflict in a shared file stops the session.
TDD stage: the test audit (Principle 6) is the suite for this step. Audit script `research/sean/cr_scratch/step4_audit.py`:

| ID | Check | Z | B |
|---|---|---|---|
| A4-1 | Every changed or voided key: each test or probe file and function that names it (grep) has a disposition row | Fixture change list covering a fixture tests directory | A planted test naming `column.spacing` with no row |
| A4-2 | Every RETIRE row has a reason and a replacement or "none" with reason | Complete fixture rows | Blank reason |
| A4-3 | Test inventory: pytest node IDs collected before and after (`--collect-only -q`); every node ID that disappears has a RETIRE row | Identical inventories | A scratch copy of the tests with one function deleted and no row |
| A4-4 | Every test red after the change and green before it is in the list as REWRITE or as expected red with a reason | Fixture before and after result files | One newly red test absent from the list |

Red-first: run pytest at 4a before any edit and again at 4c open, and record collected, pass and fail (Quinn's header gives 672 / 620 / 52; the measured figure governs; a difference between the two runs is a pull from Quinn and is named before 4c edits); run the audit on an empty change list, where A4-1 fires for every key in the seed list. A4-1 and A4-2 run at 4a; A4-3 and A4-4 at 4c.
Visual gate: none.
Human gate: Sean at 4b and at the 4c close; Quinn's review between 5.4 and 4c.

**Detail 5. Week-close configuration record (prose for Quinn, A.6.2).**
Output: `research/sean/cr_scratch/step5_configuration_record.md`; the shared location is set at the gate (Design Notes 7). Document Structure above holds the point, shape and limitation placement.
5.1 Test suite (tdd_method Prompt 1), file `research/sean/cr_scratch/step5_suite.md`, about 30 tests (tdd_method "On Test Count"; a two-page record), one deliverable:
- W, whole record (about 8): the point sentence on the first screen; first screen holds configuration, sketch links, decisions, change list and open items (LDR); every number agrees with the Echo Site Registry; every ASSUMED value is labelled at first use; no superseded option (Design Notes 2) appears as live; every internal code (S1, Q11, DN23, R14) is defined at first use; a reader holding only [DN23] and the record can find the sketch behind each decision; the ending names the next step.
- S, per section (about 12): configuration (height stack per pose with margins, ring position, frame), lift decisions (one line per Step 2 row), proposed change list (counts of keys and tests to change, retire and add, from the approved 4b list; the record states that execution follows Quinn's review), load loops (the S3-3 axial loop and S6-3 torque loop through the kept base parts, with the N5 status), open items (every OWNED row with owner and due step).
- F, facts (about 10): one test per number or decision in the record, naming its source ([CP §n, mm:ss], [DN23], accepted sketch revision and check ID, or params key) and status (DECLARED, ASSUMED, DERIVED). Each source is checked against the file before the suite becomes the contract (A.10 item 2); a source not found is UNVERIFIED and goes to the orchestrator.
5.2 Topic-sentence outline, file `research/sean/cr_scratch/step5_outline.md`, each paragraph tagged with the test IDs it serves. Coverage matrix script `research/sean/cr_scratch/step5_matrix.py`: every test maps to at least one paragraph, and every paragraph to at least one test (orphans are gaps, Principle 4). Z: complete fixture matrix passes. B1: one test unmapped fires; B2: one paragraph with no test fires. Red-first: the matrix on an empty outline fails.
5.3 Write from the outline; run the suite on the draft.
5.4 Revise (tdd_method Prompt 4). Number audit script (part of step5_matrix.py): every number in the record is extracted and matched to params, the overlay, an accepted checks JSON or the Echo Site Registry. Z: a clean fixture paragraph passes. B: a planted "travel 640 mm" fires. Link check: every sketch link resolves to an accepted PNG; B: a link to an r0 PNG fires. The suite is re-run after revision and stays green.
Red-first: the suite runs on an empty record and fails.
Visual gate: sketch links (scripted, above); the sketches themselves passed M1 at Step 1.
Human gate: Sean, then pushed for Quinn.

**Detail 6. Manager week close.** The Manager re-runs every scripted check on the accepted outputs (`check_sketch.py` and `check_sketch.py --stale` for each accepted revision, against params.yaml after 4c and the reduced overlay, `step2_check.py`, `step3_check.py`, `step4_audit.py`, the Step 5 suite and matrix); a stale accepted revision fails the close. Then the Manager verifies Objectives 2 to 8 against outputs on disk, writes accumulator entries, and presents the configuration, the executed change list and the owner table at the gate. Any red result blocks the close.

**Detail 7. Upper-assembly CAD.** Placeholder. Scoped at the week-close gate; it gets a work order and its own test suite before any geometry (LLM-PLM 7.2), and the accepted specs seed its placement tests.

---

## Context Recipes

| Step | Agent | Files / Excerpts |
|------|-------|-----------------|
| 1.0 | The Engineer | this gameplan (Objectives, Steps, detail 1.0, detail 1 common, Design Notes 1 to 14), supplements/llm_plm_cad.md 7.4, 8.4 to 8.4.2, method/tdd_method.md (Principles 9, 10), params.yaml top-level key list, ASSEMBLY.md Coordinate frame, tests/test_params_bom.py lines 694-718 (collar-top and park formulas) |
| 1.0 | The Software Engineer | detail 1.0, sketch_common.py, check_stack.py, check_sketch.py, fixtures/, stubs/, s1_spec.yaml, baseline_red.json, method/tdd_method.md |
| 1.0 (batch 1) | The Engineer | detail 1.0 last paragraph, Open Questions, detail 4a cross-contributor items, Design Notes 16, critical-path section 9, research/quinn/gameplan.md Design Note 23 (read only) |
| 1.1 (S1) to 1.6 (S5) | The Designer (params review, spec sign-off, operator-task rows) | the sub-step's detail block, detail 1 common (including the operator-task table and rubric applicability), the params keys it lists (grep, not the whole file), proposed_params.yaml, the draft sN_spec.yaml, llm_plm_cad.md 8.4 items a and b, the K7 g_min seed list, Design Notes 1, 2, 13 (no scripts) |
| 1.1 (S1) to 1.6 (S5) | The Engineer | the sub-step's detail block, detail 1 common, the signed sN_spec.yaml, the Designer's params review for that sketch, sketch_common.py, check_stack.py, proposed_params.yaml, params.yaml keys listed, context/2026-11-24_cutjig_critical_path.md sections 7, 14, 15, Design Notes 13, 14, 15, 16, prior accepted sketch specs and checks JSON, batch 1 answers received; at 1.6 (S5) also step2_lift_decision.md |
| 1.1 (S1), 1.2 (S2), 1.3 (S3), 1.5 (S6) | The Loftsman, The Topologist | the sketch script, sN_spec.yaml, sN_checks_r<k>.json, params and overlay keys it reads, ASSEMBLY.md Coordinate frame, the sub-step's check table |
| 1.1 (S1) to 1.6 (S5) | The Designer (M1 visual gate, image-capable model) | the PNGs, sN_spec.yaml, the M1 rubric (detail 1) with the applicability line, the operator-task table, sN_checks_r<k>.json, sN_summary_r<k>.md, Design Notes 13; at 1.1 (S1) also the K8 Z and B1 fixture figures, unlabelled |
| 2 | The Engineer | accepted S1, S2, S3, S4, S6 PNGs, specs and checks JSON, research/quinn/gameplan.md Design Note 23 (lines 774-780, read only), proposed_params.yaml, Design Notes 13, 15, 16, detail 2, batch 1 answers received |
| 2 | The Systems Engineer | step2_lift_decision.md, step2_check.py output, the detail 2 checklist, accepted sketch specs and checks JSON, Design Notes 1 to 5, 11, 16, critical-path section 15 |
| 3 | The Engineer, The Manager | Open Questions section, detail 3, step3_check.py, step1_quinn_batch1.md with answers, critical-path section 9, research/quinn/gameplan.md Design Note 23 (read only), Step 2 record, detail 4a cross-contributor items |
| 4a | The Software Engineer | detail 4, tests/ file list, tests/test_params_bom.py, tests/test_assembly.py, tests/test_step7_fix_controls.py, tests/probes/probe_poses.py, proposed_params.yaml, step2_lift_decision.md, accepted S1 park rule and lift stroke, Quinn's N8 and N9 rulings, method/tdd_method.md Principle 6, llm_plm_cad.md 5.2, 7.2 |
| 4a | The Systems Engineer | step4_change_list.md, ASSEMBLY.md (Load path, Interface control table), params.yaml `icd.*`, `upper.*`, `stop.*`, accepted S3 and S6 checks JSON (S3-3, S6-3, S6-5) |
| 4c | The Engineer | approved step4_change_list.md, Quinn's review of the Step 5 record, params.yaml, ASSEMBLY.md, proposed_params.yaml, tests named in the list, step4_audit.py, Repository Sync section |
| 4c | The Software Engineer | step4_audit.py output, step4_test_retirement.md, pytest before and after inventories |
| 5.1 | The Software Engineer, The Designer | Document Structure, detail 5, accepted sketches and checks JSON, step2_lift_decision.md, approved step4_change_list.md, Open Questions, Echo Site Registry, method/tdd_method.md, operational_guide A.10 |
| 5.2 | The Engineer, The Software Engineer | step5_suite.md, Document Structure, step5_matrix.py |
| 5.3 | The Engineer | step5_outline.md, step5_suite.md, supplements/writing-guides/reporting-copy.md, accepted sketches, Step 2, 3 and 4a outputs |
| 5.4 | The Designer | step5_configuration_record.md, step5_suite.md, Echo Site Registry, accepted sketch PNGs, step5_matrix.py output |
| 5.4 | The Engineer (fix) | step5_configuration_record.md, the Designer's 5.4 review, step5_suite.md, step5_matrix.py output, Echo Site Registry |
| 6 | The Manager | this gameplan, all Step 1 to 5 outputs and check scripts, research/sean/accumulator.md (persona sections) |

---

## Progress Log

| Step | Date | Notes |
|------|------|-------|
| 0 | 2026-11-24 | Drafting variant (A.6.4). Done: Engineer draft; Software Engineer TDD revision; Wave 2 review (Systems Engineer: 2 BLOCKS, 13 FIX, 3 NOTE; Designer: 10 FIX, 5 NOTE); Engineer revision (dispositions in `research/sean/cr_scratch/step0_engineer_revision_notes.md`; both BLOCKS owned by S3-3, S6-5, N4, N5 and Step 2 rows). Pending: Manager close, Sean's gate (decision list in the revision notes: lit_review, Design Notes 4 to 9, 15, 16). Baseline pytest 672 collected, 620 pass, 52 fail (Quinn's header; measured at 4a). |
| 0 | 2026-11-24 | Closed pending Sean approval. Manager close (`research/sean/cr_scratch/step0_manager_close.md`): READY FOR SEAN; acceptance list 9 of 9, Designer close checklist 12 of 12; header, Start here and Repository Sync byte-identical to commit 4bfad31 except Current step. Manager edits: Current step, Steps row 0, check Q3-0 (batch mode of step3_check.py, written at 1.0), Context Recipe 5.4 Engineer. Accumulator created (`research/sean/accumulator.md`). Gate brief: 13 decisions in the close file. |
| 0 | 2026-11-24 | Approved by Sean at the gate: all 13 decisions accepted as recommended in `research/sean/cr_scratch/step0_manager_close.md` (lit_review no; S3 one-screw section plus three-screw inset; docs/sketches/; order S1, S2, S3, S4, S6, Step 2, S5; shared-file changes after Quinn's review; base carries cut reaction, to Quinn as N5; batch 1 at Step 1.0 open; prose week-close record; proposed-keys overlay; 2D matplotlib, Engineer draws, Designer gates; owners as listed; ASSUMED seeds owned by Sean; rulings T1 to T7 ratified). Next: Step 1.0. |

---

## Design Notes

(Decisions and every human sketch correction, recorded so the next session does not repeat them.)

**1. Decisions in force (DECLARED, Quinn, 2026-11-24).** Source: Design Note 23 of `research/quinn/gameplan.md` and section 15 of `context/2026-11-24_cutjig_critical_path.md`. Travel 650 mm. Bevel ring gear on the drill, three pinions at 120 deg, each on a NEMA 23 (on hand), gearbox optional; pinions carry drill weight, support ring with shaft bushings if needed. Drill, ring gear and motors ride one ring structure; the ring moves on three jack screws at 120 deg, probably NEMA 17. T8 lead screws with brass nut, 800 to 900 mm, anchored at the bottom with a thrust bearing and guided only at the top, so cutting load puts the screw below the nut in tension; TR10 or TR12 if a compression case is needed. The three lift motors move as one axis (single controller or belt link; the sketch phase picks). Kept: collet family and generator, holder, wing nut, receiver, PTFE washer. Core never inverted; drill moves, core stays.

**2. Superseded (do not draw or test against).** Arbor press (critical-path section 6 option A); ratchet hoist and hoist cross member (`hoist.*`, `upper.manual_raise`, `upper.raise_fuse`); two-column carriage (`column.*`, 1540 mm columns in critical-path section 8 and the `bom_stock_allocation.md` reservation); "twin" jack screws (critical-path section 6 option B; three governs); S3 per lift option (critical-path 7.3); week-done bullet "lift option chosen or narrowed to two" and critical-path 7.4, which now read "lift detail decided" (Objective 4); critical-path section 8 height stack (replaced by S1). The frame's role under a ring on three screws is undefined until S1 and S2 define it. Status set at Step 2, neither in force nor superseded until then: `upper.metal_stop` (DECLARED, gate B5), `upper.park_lock`, the strap keys, `icd.torque_reaction`, `icd.tipover_statement`, and the ASSEMBLY.md Load path (Design Notes 16).

**3. Deviation from LLM-PLM 8.4 (recorded).** This week is 2D matplotlib only (critical-path 7.2): no STEP sketch assembly, no PNG render or turntable of solids, and sketch-level interference is 2D outline overlap (check K7). LLM-PLM 8.4 assigns sketch production to The Designer; here The Engineer writes the sketch scripts because they are code with scripted checks, and The Designer keeps the params review (8.4a), the representative-shape spec (8.4b) and the critique and visual gate (8.4c) on an image-capable model. The Designer did not produce the image, so the gate is independent (A.3.1).

**4. S3 redefinition (for Sean to confirm).** S3 becomes the side section through one jack screw (bottom anchor, screw and lead, nut and its mounting, top guide, lift motor, hold device, load arrows, axial loop) plus a plan inset of all three screws and the sync loop (detail 1.3). Against critical-path 15 ("S1 and S3 draw the ring and three screws"): S1 draws ring and screws in elevation, S3 draws the screw detail and all three in the inset.

**5. Sketch drawing order and decision locus (for Sean to confirm).** S1, S2, S3, S4, S6, then Step 2, then S5. S6 precedes S5 because its guide, anti-rotation and torque members are frame members the stock map must place; Step 2 precedes S5 so S5 places decided members once. One rule for decisions: a sketch spec carries the option drawn, Sean picks at that sketch's M2 pass (Design Notes 13), Step 2 consolidates the picks and decides the rows no sketch carries. Sketch IDs keep the critical-path numbering; sub-steps are labelled "1.5 (S6)" and "1.6 (S5)".

**6. Proposed-keys overlay (for Sean to confirm).** Keys the sketches need that `params.yaml` lacks live in `research/sean/cr_scratch/sketches/proposed_params.yaml` during Step 1, with source and status per leaf. `params.yaml` is unchanged until Step 4, when accepted keys are promoted and void keys are retired in one LLM-PLM change. Check K2 fails on any overlay key that shadows a params.yaml key.

**7. Shared location for accepted sketches (for Sean to confirm).** Proposed: `docs/sketches/` (shared, committed). At the first acceptance (S1) the harness moves there with it: `sketch_common.py`, `check_stack.py`, `check_sketch.py`, fixtures, stubs and `proposed_params.yaml`; each accepted PNG, script, spec, checks JSON and summary follows. An accepted sketch then imports nothing from `research/sean/`, so Quinn can run and fix what he pulls. Paths in this gameplan under `research/sean/cr_scratch/sketches/` read as `docs/sketches/` after the move. At 4c each promoted key is deleted from the overlay in the same change.

**8. Geometry cross-review (A.4 step 2).** Assigned on S1, S2, S3 and S6, where the sketch computes placement or projection: The Loftsman on arithmetic and placement, The Topologist on orientation and sense. S4 and S5 compute no new placement.

**9. Week-close record is prose (for Sean to confirm).** Step 5 treats the configuration record as a short prose document for Quinn and runs test suite, outline, write and revise (A.6.2).

**10. Test baseline.** Quinn's header (672 collected, 620 pass, 52 fail) governs over critical-path section 10 (622 / 50, Step 7 close). The two added failures: test_P10_working_stroke_per_core_class (park 959.84 below the 965 start after travel 650) and test_common_guard_shifted_partner (stale probe timestamp).

**11. Torque reaction is a design gap to close in S6 and Step 2.** The jack screws are lead screws; they resist ring rotation only in bending, and a T8 screw about 850 mm long is a poor torque member. S6 must show the member that stops the ring rotating and carries the spin-torque reaction to the frame. The loop closes through the frame, base, collet and core back to the cutter (S6-3); floor friction is not a designed member. The same member is the candidate lateral guide and coaxiality carrier (N2, SE-6): three rigid nuts on three top-guided screws overconstrain the ring, floating nuts drop S3-2 to K = 2.

**12. ASSEMBLY.md is stale on travel.** Its ICD row reads "travel 500 with start_z 684.84 / 815"; params reads 650 and 834.84 / 965. Fixed at Step 4 through LLM-PLM, with the other ASSEMBLY.md rows the redesign touches.

**13. Sketch correction log.** One row per human correction. Format `S<N>-r<k>`.

| ID | Date | Correction (Sean's words) | Fixed in |
|---|---|---|---|
| | | | |

**14. Test-design decisions (The Software Engineer, Step 0).**
- The sketch spec `sN_spec.yaml` is also the feature table every check reads. One file, so the spec and the checks cannot disagree; K9 checks the figure against the spec as an outline is checked against its suite.
- K7 tests a side-view pair only when the depth bands overlap. Two outlines that overlap in XZ while separated in Y are no interference; with depth bands, a side-view hit plus the plan view behaves as a box interference check for the prismatic parts sketched this week.
- K6 compares data coordinates at 0.05 mm, and its known-bad shift is 6.75 mm, the smallest term in the collar stack, so the control proves the check sees the smallest real term.
- Values reported for a decision carry no threshold and no controls; soft keys (`jig.height_target`, core lengths beyond 0.5 m) are never asserted (K1 B2).
- Where the live design is the defect (S1-2: park 959.84 below start 965; S4-2: receiver floor), the live params or part is the known-bad control.
- A human correction that a signed predicate can express becomes a K8 predicate with a B fixture reproducing the error.
- The M1 reviewer model is controlled once, at 1.1, with an unlabelled correct figure and a drill-tip-up figure; it must fail the second on V3. The drill is drawn with distinct head and top-end features (D4), so the tip-up figure differs from its Z.

**15. Rulings between The Software Engineer and The Systems Engineer (The Engineer, Step 0 revision; A.9).**
- T1, swept-envelope interference (SE-15) against the cut of a second overlap implementation: the swept case is added inside the one K7 implementation with its own Z4 and B4. One implementation stands; the defect (a member hit in transit) is plausible and the check fires on it.
- T2, provenance hashes and `--stale` (SE-7) against ceremony: kept. A stale accepted revision is a known back-edge (S4 collar height, S6 seeds), and the check fires on it at the moment it happens.
- T3, decision locus (SE-8) against the cut of Step 2 scripted row checks: sketch M2 decides, Step 2 consolidates, Step 2 runs before S5. The Systems Engineer checklist stays manual; the script keeps only cross-file checks (X2-1 to X2-5), where slips happen.
- T4, execution before or after Quinn's review (SE-10): after. Order 4a, 4b, 5, Quinn's review on pull, 4c, 6. Sean leads and Quinn reviews; promoting ASSUMED keys and retiring tests that encode Quinn's Steps 2 to 7 before he sees the proposal hands him a changed repo. Sean may reverse this at the gate.
- T5, orientation preview (SE-17) against spec-first order: added as step (d'), V1 to V5 only, not acceptance. Red-first and spec sign-off still precede drawing; the preview moves Sean's first look earlier without bypassing a check.
- T6, new chain checks S3-3, S6-5 and the rewritten S6-3: each has a B that reproduces a plausible defect (open loop, bearing missing, anti-rotation missing). They pass the Software Engineer's test ("a check that cannot fail on a plausible defect goes").
- T7, values the Systems Engineer asks for (lift stroke and L per Q9 option, tip force, kept-part forces, drill torque against 10 N m, pinion forces): reported, no threshold, per the Software Engineer's reported-values rule. Each goes to a named decision (Q9, Step 2 rows, N5).

**16. The kept base parts carry the cut reaction under the screw lift (for Sean to confirm; Quinn rules, N5).** With a powered screw lift, the cut force is applied by the screws and reacts through the work: cutter, core, collet core stop, collet, holder, receiver, base plate, base frame, anchor frame member, anchors, screws in tension, nuts, ring, drill-to-ring bearing, drill (S3-3). ASSEMBLY.md Load path ("1000 N path is cutter, carriage, metal stop, columns, frame. It never enters the nut, holder, collet, receiver or base plate") and A2d (axial force 0 at the stop) describe the old design and are false during a powered cut. S3 reports the axial force in each kept part at 1000 N (`loads.wob_max`) and at the lift's stall thrust. Quinn rules in batch 1 whether the kept parts accept it or need a rating check; the ASSEMBLY.md and A2d dispositions follow at 4a.

**17. Floor datum (Sean, Step 1.0, blocker B1).** Sketch heights are measured from the shop floor, which sits at z_A − `jig.datum_a_above_floor`, where datum A is the base-plate underside. The value is 60 mm ASSUMED, derived from `profile.height` on the assumption the frame has no feet; it goes to Quinn as batch row N10. This supersedes "z_A + 40" in K6. ASSEMBLY.md's "z_A − 40" refers to the receiver floor, not the shop floor. K6 B2 plants an offset 60 mm low; a new B2b plants one 100 mm low.

**19. Bore ceiling is drill-relative (Sean, Step 1.0, correction 2).** `drill.bore_ceiling_z` is replaced by the leaf `drill.bore_ceiling_above_tip` (800 mm ASSUMED; Q2e asks Quinn for the real offset). check_stack.py computes the ceiling z for each pose. Question batch 1 (`research/sean/cr_scratch/step1_quinn_batch1.md`, 17 rows) was approved by Sean as drafted on 2026-11-24.

**18. Step 1.0 review roster (Sean, Step 1.0).** The Loftsman (K6, K7, S1-6) and The Topologist (K5, K8, K7 classes, K9) cross-review the harness in Wave 2 alongside The Software Engineer, under A.4 step 2's geometry cross-review rule.

---

## Echo Site Registry

Values that must agree in every sketch, record and test. Authority is `params.yaml` (or the overlay during Step 1) unless stated.

| Value | Authority | Status |
|---|---|---|
| Travel **650 mm** | `upper.travel_max`; Quinn DN23 | DECLARED |
| Drill length **about 800 mm** | overlay `drill.length`; critical-path 18:20 | ASSUMED (Q2) |
| Capture **500 mm** core | `core.length_capture` | DECLARED |
| Three screws and three pinions at **120 deg** | overlay `jackscrew.*`, `pinion.*`; Quinn DN23 | DECLARED |
| T8 screws **800 to 900 mm** | overlay `jackscrew.length`; Quinn DN23 | DECLARED estimate (DN23, built on travel 650); reported, never asserted |
| Lift stroke (park to lowest stop), distinct from travel | S1 reported value; replaces `upper.park_stroke` 775 | DERIVED (S1) |
| Axial design load **1000 N** | `loads.axial_design`; `loads.wob_max` | ASSUMED (design choice); wob_max VERIFIED |
| Drill tube **152.4 mm** OD; keep-out radius **86.2 mm** | `drill.tube_od`, `icd.keepout_radius` | ASSUMED / DERIVED |
| Cutter OD **unknown**; 152.4 is the tube OD, not a cutter OD | overlay `drill.head_od` | ASSUMED (Q2) |
| Soft height **2000 mm**, never a limit | `jig.height_target` | DECLARED |
| Loading park **959.84 mm** (re-derived in S1) | `upper.park_z` | ASSUMED |
| Install core **0.75 m** | `core.length_install` | DECLARED |
| Core mass **10.4 kg** (0.5 m), **15.6 kg** (0.75 m) | Quinn Source Verification Register / Echo Site Registry | DERIVED (density ASSUMED) |
| Drill advance **534.93 mm** | `upper.drill_advance_500core` | DERIVED |
| Start z **834.84 / 965 mm** | `stop.start_z` | DERIVED |
| Footprint **644 x 608 mm** (open) | `icd.footprint_x`, `icd.footprint_y` | open; not asserted |
| On-hand 30-6060 stock list | `stock.on_hand` | DECLARED |
| Core holding torque **10 N m** | `loads.torque_design` | DECLARED |

---

## Open Questions

Full text of Q1 to Q11 is in section 9 of `context/2026-11-24_cutjig_critical_path.md`. Step 3 brings every row to ANSWERED or OWNED.

| # | Question | Status | Owner / closes in |
|---|---|---|---|
| Q1 | Travel | ANSWERED 2026-11-24: 650 mm | Quinn; S1 confirms on the drawing |
| Q2 | Drill length, mass, top-end hardware, cutter OD, bore ceiling | Open; S1 uses 800 mm ASSUMED | Quinn (drill in build); batch 1 |
| Q3 | What spins the drill | ANSWERED 2026-11-24: ring gear, three NEMA 23 pinions | Quinn; S6 details |
| Q4 | Push-pop advance | Open | Sean, S4 |
| Q5 | Collet length | Open | Quinn and Sean, S4 |
| Q6 | Sacrificial collet or liner | Open | Sean, S4 |
| Q7 | Lift | ANSWERED 2026-11-24: three jack screws | Quinn; detail in S3 and Step 2 |
| Q8 | Manual or powered travel; feed control | Open (powered by the decided lift; feed control open) | Sean, S3 and Step 2 |
| Q9 | Core lengths to support (selects lift stroke and screw length) | Open | Quinn; batch 1; S1 draws 500 and 750 and reports stroke per option |
| Q10 | Short 100 x 100 mm cores | Open | Sean, S4 |
| Q11 | Tests and params that become void | Open | Sean (contributor making the change), Step 4 |
| DN23-a | NEMA 17 count on hand | Open | Sean (owns the motors), Step 2 |
| DN23-b | NEMA 23 gearbox ratio | Open | Quinn and Sean, S6 |
| DN23-c | Drill rpm and torque target | Open | Quinn, S6 |
| DN23-d | Ring gear size and source | Open | Sean, S6 |
| DN23-e | Iris drive with three pinions (INSITU2 157-166, excerpted at `context/literature/INSITU2_text.md` line 7, via Quinn DN23) | Open | Quinn, S6 callout; batch 1 |
| N1 | Ring position along the drill | Open | Sean, S1 (lower bound from S1-5b) |
| N2 | Ring guidance: anti-rotation, lateral guide, coaxiality carrier (R13); nut mounting rigid or floating | Open | Sean, S2, S3, S6 picks; Step 2 row |
| N3 | lit_review flag: does this phase carry technical claims that need primary sources? (`no` here, `yes` in Quinn's plan) | Open | Sean at the Step 0 gate (A.6.1) |
| N4 | Drill-to-ring bearing: type (slewing ring, thrust pair, tube collar), source, ratings for radial load and axial load both ways | Open | Sean; S6 pick (S6-5), Step 2 row |
| N5 | Kept base parts carry the cut reaction under the screw lift (Design Notes 16): accept, or name the rating check | Open | Quinn (kept parts are his design); batch 1; Sean confirms at Step 2 |
| N6 | Removing the 500 mm captured core from the raised drill (tied to DN23-e) | Open | Quinn; batch 1 |
| N7 | Descent end (gate B5 metal stop kept or replaced by limits) and power-off hold | Open | Sean, Step 2 rows; Quinn consulted on B5 in batch 1 |
| N8 | ASSEMBLY.md authority: its source line and ICD freeze point at Quinn's cr_scratch file | Open | Quinn; batch 1; ruling before 4b |
| N9 | test_P10_every_key_in_concept_icd_table_exists reads Quinn's cr_scratch file | Open | Quinn; batch 1; ruling before 4b |

---

## Repository Sync

Repo: https://github.com/Shootquinn/cutjig (public, all rights reserved). Contributors: quinn, sean. Each contributor has `research/<name>/` holding their gameplan, accumulator and `cr_scratch/`. The design files are shared: workorder.md, params.yaml, ASSEMBLY.md, bom_*.md, report_assumptions.md, build_parts/, tests/, output/, parts_cache/, docs/, context/, reference/. Either contributor may change any shared file; a change to the other contributor's design runs through LLM-PLM like any other change (FCStd wins, sync params first, re-run the tests). Never edit files in the other contributor's `research/<name>/`.

Every step in this gameplan carries these sync points:

1. **Step open:** `git pull --ff-only` before the Manager is spawned. If the fast-forward fails, stop and report to the human. If the pull brought changes to shared design files, the Manager open reads `git log --stat` since the last sync and names what changed.
2. **Save point** (each wave close and the step close, before the inter-step gate):
   ```
   git add -A
   git commit -m "sean: Step N <what finished>"
   git pull --rebase
   git push
   ```
   The rebase lands this machine's commits on top of the other contributor's, so the next `git pull --ff-only` on their machine fast-forwards.
3. **Conflicts:** a rebase conflict in a shared design file (params.yaml, a part script, a test, an FCStd, STEP or STL, ASSEMBLY.md) stops the session; `git rebase --abort` and report to the human. No agent resolves a design conflict.
4. **Background builds:** push a save point before launching a FreeCAD build; push the build's outputs as their own save point when the build finishes. Never commit a half-finished build.
5. **Never** force-push, amend or rebase a pushed commit, or skip hooks. Undoing the other contributor's work is a new change.
6. Scratch files go to `research/sean/cr_scratch/`.
