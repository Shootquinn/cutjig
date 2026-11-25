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
**Current step:** 0 (drafted, awaiting approval)
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

1. Step 0: a team-reviewed gameplan that Sean approves at the Step 0 gate.
2. Settle the cut jig configuration on paper with the 2D matplotlib sketch set S1 to S6 (LLM-PLM 8.4, recorded deviation in Design Notes 3), plotted from `params.yaml` plus a proposed-keys overlay. Each sketch passes its scripted checks, an image-capable visual gate and a human correction pass before the next sketch is drawn. Every correction goes to Design Notes 13.
3. Draw the configuration Quinn decided on 2026-11-24 (Design Notes 1): 650 mm travel; the drill spun by a bevel ring gear on three NEMA 23 pinions at 120 deg, the pinions carrying drill weight (support ring with bushings if needed); drill, ring gear and motors on one ring structure lifted by three jack screws at 120 deg (NEMA 17 probable); T8 screws 800 to 900 mm, anchored at the bottom so cutting load puts them in tension; the three lift motors moving as one axis.
4. The lift is chosen. Decide what remains open on it: screw sync (single controller or belt link), screw anchoring and top guide, ring anti-rotation and spin-torque reaction, and the frame that carries the screws (Step 2).
5. Show the jig is tall enough in all four poses (load, start of cut, end of 500 mm capture, park) and re-derive the park rule so that test_P10_working_stroke_per_core_class goes green or is retired on the record (S1, Step 4).
6. Give every open question (Q1 to Q11 and the Design Note 23 opens) an answer or a named owner (Step 3).
7. Close the week with the chosen configuration and the list of params keys and tests that change or retire (Q11), executed through LLM-PLM: params first, re-run the tests, record each retired test with its reason; no test or key deleted unrecorded (Steps 4 to 6).
8. No extrusion cut, no production CAD for the upper assembly and no 3D sketch assembly this week. Upper-assembly CAD is scoped at the week-close gate (Step 7 placeholder).

---

## Document Structure

Steps 1 to 4 produce sketches, scripts, check records and decision tables; none is a prose document. The one prose document this phase is the week-close configuration record for Quinn (Step 5), and it runs the TDD stages as ordered sub-steps 5.1 to 5.4. Sean confirms at the Step 0 gate that it is prose (Design Notes 9); if he rules it a table-only record, Steps 5.1 to 5.4 collapse into one table step with its own checks.

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
| Iris drive with three pinions open (INSITU2 157-166 via Quinn DN23) | Open items table with owner | Next action |

---

## Steps

| # | Step | Assigned To | Status |
|---|------|-------------|--------|
| 0 | Team wave to draft this gameplan from the critical-path file | The Manager, The Engineer, The Designer, The Systems Engineer, The Software Engineer | In progress (drafted; Software Engineer revision, Wave 2 review, Engineer revision and Manager close to follow) |
| 1 | Sketch set S1 to S6, one sub-step per sketch, each with its own human correction pass before the next is drawn. See detail 1. | The Engineer (scripts, checks), The Designer (params review, visual gate on an image-capable model), The Loftsman and The Topologist (geometry cross-review on 1.1, 1.2, 1.3, 1.5), The Software Engineer (check harness review at 1.0), Sean (human correction pass) | Not started |
| 1.0 | Sketch harness: proposed-keys overlay, shared plot and check library, controls, red-first baseline | The Engineer (write), The Software Engineer (review, signs) | Not started |
| 1.1 | S1 side XZ, whole jig, four poses: is it tall enough, where does the ring sit on the drill, what is the park rule | The Engineer, The Designer, The Loftsman, The Topologist, Sean | Not started |
| 1.2 | S2 plan XY: footprint, three screws and three pinions at 120 deg, drill and keep-out, collet axis, operator side | The Engineer, The Designer, The Loftsman, The Topologist, Sean | Not started |
| 1.3 | S3 (redefined) side section through one jack screw: bottom anchor, screw, nut on ring, top guide, motor, sync method, load arrows | The Engineer, The Designer, The Loftsman, The Topologist, Sean | Not started |
| 1.4 | S4 side section through the base: collet, holder, nut, receiver, push-pop advance path | The Engineer, The Designer, Sean | Not started |
| 1.5 | S6 side, ring-gear and pinion close-up: gear on drill tube, pinions, NEMA 23 motors, support ring, torque reaction path to the frame | The Engineer, The Designer, The Loftsman, The Topologist, Sean | Not started |
| 1.6 | S5 stock map: each on-hand 30-6060 length placed in the frame, leftovers | The Engineer, The Designer, Sean | Not started |
| 2 | Lift detail decision record: screw sync, anchoring, top guide, anti-rotation and torque reaction, screw size (T8 or TR10/TR12), NEMA 17 count. See detail 2. | The Engineer (author), The Systems Engineer (review), Sean (decides), Quinn (consulted on motors) | Not started |
| 3 | Open-question sweep: each Q1 to Q11 and each DN23 open gets an answer or an owner. See detail 3. | The Engineer (table), The Manager (owner check), Sean, Quinn (answers Q2 and the DN23 drill items) | Not started |
| 4 | Params and test change list (Q11), then execution through LLM-PLM: params first, re-run pytest, retirement record. See detail 4. | The Software Engineer (test audit, signs), The Engineer (params change, test run), The Systems Engineer (ICD and ASSEMBLY.md coherence), Sean (approves the list before execution) | Not started |
| 5 | Week-close configuration record for Quinn: 5.1 test suite, 5.2 outline validated against the suite, 5.3 write, 5.4 revise. See detail 5. | The Software Engineer (5.1, signs 5.2), The Engineer (5.2, 5.3), The Designer (5.4 review), Sean | Not started |
| 6 | Manager week close: configuration accepted, change list executed, every question answered or owned, accumulator entries | The Manager, Sean | Not started |
| 7 | Upper-assembly CAD: placeholder, scoped at the week-close gate | Scoped at the week-close gate | Not started |

### Step details

Marks of the form **[SE: ...]** are places The Software Engineer fills in his revision pass.

**Detail 1.0. Sketch harness.**
Objective: one library every sketch script uses, so the checks are written once, shown to fire once, and applied to all six sketches.
Files (all scratch until a sketch is accepted, Design Notes 7):
- `research/sean/cr_scratch/sketches/proposed_params.yaml`: keys the sketches need that `params.yaml` lacks, same leaf schema (value, unit, source, status). Seed namespaces: `drill.length` (800, ASSUMED, critical-path 18:20), `ring.*` (structure outline, position along the drill), `gear.*` (ring gear pitch diameter, face width), `pinion.*` (count 3, angle 120 deg, motor class NEMA 23), `jackscrew.*` (count 3, angle 120 deg, pitch radius, nominal 8 mm, length 800 to 900, anchor z, top guide z), `liftmotor.*` (NEMA 17), `frame_upper.*`. Promotion into `params.yaml` happens at Step 4 only (Design Notes 6).
- `research/sean/cr_scratch/sketches/sketch_common.py`: loader (params.yaml, then overlay), feature table per sketch (name, keys, view, projection kind, neighbour class), 8.4.2 figure setup, and the check library K1 to K8.
- `research/sean/cr_scratch/sketches/check_sketch.py sN`: runs K1 to K8 on sketch N, writes `research/sean/cr_scratch/sketches/sN_checks.json`.
- `research/sean/cr_scratch/sketches/fixtures/`: one zero-control and one known-bad fixture per check.
TDD stage: test suite (the check library) before any sketch geometry.
Scripted checks (each with zero control Z and known-bad control B, tdd_method Principle 9):

| ID | Check | Z (must read clean) | B (must fire) |
|---|---|---|---|
| K1 | No hard-coded dimension: AST scan of the sketch script for numeric literals outside an allowlist (0, 1, 2, figure settings, 120 and 360 deg only through `pinion.angle` and `jackscrew.angle`) | Fixture script reading every value from the loader | Planted literal 152.4 |
| K2 | Provenance: every feature-table key resolves in params.yaml or the overlay; an overlay key that shadows a params.yaml key fails | Fixture table with resolvable keys | Overlay key `drill.tube_od` planted |
| K3 | Plot conventions (8.4.2): title names the view, axis labels in mm, equal aspect, major and minor grid, figsize at least (14, 10) side or (10, 10) plan, 150 dpi; read from the Figure object | Conforming fixture figure | `set_aspect('auto')` |
| K4 | Every labelled feature carries its dimension (8.4.2): each feature-table row has an annotation matching name plus number | Fixture with all labels dimensioned | One label without a number |
| K5 | Projection (8.4.1): no Circle patch for a cylinder whose axis is perpendicular to the view direction; circles only in end views or for spheres | Drill tube as rectangle in XZ | Drill tube as Circle in XZ |
| K6 | Stack arithmetic: each pose's z values recomputed from params by a function independent of the drawing code, compared with drawn patch extents within 0.5 mm | Fixture drawn from the same params | Drill shifted 10 mm in the drawing only |
| K7 | 2D overlap between neighbouring outlines (LLM-PLM 7.4 at sketch level; shapely absent, so polygon clipping in plain Python or `matplotlib.path`): class C contact, G gap at least g_min, F free | Two rectangles 100 mm apart read F | 1 mm overlap fires every class |
| K8 | Sense and orientation: signed predicates per part (drill tip below drill top; core bottom on the collet stop; screw anchor below the nut in every pose; ring gear plane normal to Z; motors on the side of the gear the feature table states) | Fixture in correct sense | Drill flipped tip-up |

**[SE: confirm K1 allowlist, K6 tolerance, K7 neighbour classes and g_min per pair; add or cut checks.]**
Red-first baseline (Principle 10): run `check_sketch.py` for S1 to S6 before any sketch script exists; every check reports red (missing script, missing figure). Record the result in `research/sean/cr_scratch/sketches/baseline_red.json`. Any check that passes at baseline is relabelled an invariant or replaced.
Visual gate: none (no figure).
Human gate: none; The Software Engineer signs the harness and the control results.
Run with `C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe` (matplotlib 3.11.2, PyYAML 6.0.4; shapely absent).

**Detail 1, common to 1.1 to 1.6.**
Each sketch sub-step runs in this order: (a) Designer params review of the keys the sketch will plot, with a representative-shape spec (8.4a: a ring gear reads as a toothed ring with pinions, a jack screw shows nut, bottom anchor and top guide, the ring structure reads as a structure); (b) short sketch spec written before drawing: every feature, its key, its view and its projection kind (8.4.1) **[SE: fill the spec format]**; (c) The Engineer writes the script and runs K1 to K8; (d) geometry cross-review where the sketch computes placement or projection (A.4 step 2; The Loftsman on arithmetic and placement, The Topologist on orientation and half-space sense); (e) visual gate on an image-capable model (A.3.1); (f) Sean's correction pass; (g) every correction recorded in Design Notes 13 as `S<N>-r<k>: <correction>` and the sketch redrawn as revision r<k+1> until Sean accepts it. The next sketch opens only after acceptance.
Visual gate rubric (every sketch): top on top; the drill axis is vertical and the spinning part spins about Z; the drill tip is at the bottom (tail off the nose); core upright in the collet, never inverted; screws vertical with anchors at the bottom; every label legible and dimensioned; each part reads as the part it is (8.4b). A text-only reviewer returns its numeric results and "visual gate NOT RUN". **[SE: per-sketch rubric items below are a start; complete them.]**
PNG naming: `research/sean/cr_scratch/s<N>_<name>_r<k>.png`. Accepted PNG, script and checks JSON move to the shared location proposed in Design Notes 7.

**Detail 1.1. S1, side XZ, whole jig, four poses.**
Question: is the jig tall enough, where along the drill does the ring sit, where are the screw anchors and top guides, and what is the park rule?
Shows: floor, base frame, receiver, collet, holder, nut, core (0.5 m capture core; 0.75 m install core as a dashed outline in the load and park poses), drill tube (rectangle, 152.4 wide), keep-out 86.2, ring structure, ring gear, pinions and NEMA 23 motors, two of the three jack screws as projected at their 120 deg azimuths, nuts, anchors, top guides, lift motors, height of the 2000 mm soft target as a reference line. One figure per pose: load, start of cut, end of 500 mm capture, park.
Closes: R1 to R8, R17; Q1 (confirms 650 on the drawing), Q9; carries Q2 as ASSUMED 800; re-derives the U13 park rule (`upper.park_z` 959.84 sits below `stop.start_z` 965 for the 0.75 m case) and `stop.height_range[1]` (315, marked not re-derived in params).
Params keys: `upper.travel_max`, `upper.drill_advance_500core`, `upper.load_clearance`, `upper.park_z`, `stop.collar_top_z`, `stop.height_z`, `stop.height_range`, `stop.start_z`, `stop.g_stop`, `core.length_capture`, `core.length_install`, `core.min_exposed`, `drill.tube_od`, `drill.r_face`, `drill.dome_pole_offset`, `icd.floor_above_datum_a`, `jig.height_target`, `profile.*`; overlay `drill.length`, `ring.*`, `gear.*`, `pinion.*`, `jackscrew.*`, `liftmotor.*`.
Script: `research/sean/cr_scratch/sketches/s1_side_poses.py`. PNGs: `research/sean/cr_scratch/s1_pose_load_r1.png`, `s1_pose_start_r1.png`, `s1_pose_capture_end_r1.png`, `s1_pose_park_r1.png`.
Sketch-specific checks: K6 stack per pose (tip z, drill top z, ring z, nut z on each screw, screw anchor z and top guide z, top of motors); ring z range within screw nut travel (anchor + nut length below, top guide above) at all four poses; drill tip at end of capture equals `stop.height_z`; park clears the 0.75 m core top by `upper.load_clearance`; ring and gear stay above the 0.5 m core top at end of capture (K7 class G). Known-bad: travel set to 500 in a fixture fires the capture-end check. **[SE: controls per check.]**
Rubric additions: the ring is on the drill above the core at every pose; the motors sit above or below the gear as the spec says, in every pose alike.
Cross-review: The Loftsman (stack arithmetic, projection of 120 deg screws onto XZ), The Topologist (sense: anchors below nuts, tip down).
Gate: visual gate by The Designer on an image-capable model, then Sean.

**Detail 1.2. S2, plan XY.**
Question: does it fit, stay coaxial, and leave the operator a side to load the core and change collets?
Shows: base footprint (644 x 608 today, open), frame members, three screw axes at 120 deg on their pitch radius, three pinion and NEMA 23 positions at 120 deg (phase relative to the screws is a sketch choice to state), ring structure outline, drill tube and keep-out as circles (end view), collet axis, slot lines, operator loading sector and sightline to the collet.
Closes: R9, R13, R16 (layout part); the frame's role under a ring on three screws (Design Notes 2); the operator access question.
Params keys: `drill.tube_od`, `drill.tube_id`, `icd.keepout_radius`, `icd.footprint_x`, `icd.footprint_y`, `icd.datum_*`, `icd.mounting_pattern`, `frame.*`, `profile.*`, `base.*`; overlay `pinion.*`, `jackscrew.*`, `ring.*`, `frame_upper.*`.
Script: `research/sean/cr_scratch/sketches/s2_plan.py`. PNG: `research/sean/cr_scratch/s2_plan_r1.png`.
Sketch-specific checks: screw and pinion azimuths 120 deg apart within 0.1 deg; screw axes outside the keep-out plus nut radius (K7 class G); pinion mesh points on the gear pitch circle; operator sector free of screws and motors (K7 class F). **[SE: controls.]**
Cross-review: The Loftsman (azimuths, radii), The Topologist (handedness of the plan view, +X along slot line C, theta counter-clockwise from +X seen from +Z per ASSEMBLY.md).
Gate: visual gate (image-capable), then Sean.

**Detail 1.3. S3, redefined: side section through one jack screw.**
The critical-path 7.3 definition ("S1 drawn once for option A and once for option B") is void: the lift is decided. Redefinition for Sean to confirm (Design Notes 4).
Question: how is each screw anchored, guided, driven and synced, and does the 1000 N axial load put it in tension?
Shows: bottom anchor with thrust bearing, screw (rectangle, 8 mm nominal), brass nut fixed to the ring, top guide (radial support only), NEMA 17 mount and coupling, sync method (belt loop drawn, or one controller noted), load arrows: cutting reaction up through ring, nut and screw below the nut to the anchor (tension); ring weight down (compression); frame member that carries the anchor and the guide.
Closes: R14 (path), Q7 detail, Q8 (powered feed), DN23 sync and anchoring items; TR10/TR12 fallback check.
Params keys: `loads.axial_design`, `upper.travel_max`, `profile.*`; overlay `jackscrew.*`, `liftmotor.*`, `ring.*`, `frame_upper.*`.
Script: `research/sean/cr_scratch/sketches/s3_jackscrew_section.py`. PNG: `research/sean/cr_scratch/s3_jackscrew_section_r1.png`.
Sketch-specific checks: screw length equals travel + nut length + anchor and guide allowances and falls in 800 to 900 mm (or the sketch states the change); force per screw = axial load / 3 with a stated share assumption; the segment between nut and anchor is in tension in the cut case at every nut position; Euler buckling of the compression segment under ring weight with the end condition stated, and the 1000 N compression case reported as the fallback trigger. **[SE: controls; source tags for the buckling formula inputs.]**
Cross-review: The Loftsman (lengths, buckling arithmetic), The Topologist (anchor below nut in every pose).
Gate: visual gate (image-capable), then Sean.

**Detail 1.4. S4, side section through the base.**
Question: how does the core move up through the collet (push-pop), and does the kept collet family cover a 100 mm tall core?
Shows: collet, holder, wing nut, receiver, PTFE washer, core stop, and the advance path for the core (the current receiver has a floor and the core stands on the collet core stop, so nothing moves the core up today); taller collet option; sacrificial collet or liner option; 100 x 100 mm core.
Closes: R10, R11, R12; Q4, Q5, Q6, Q10.
Params keys: `collet.*`, `holder.*`, `receiver.*`, `nut.*`, `washer.*`, `seat.*`, `core.diameters`, `core.length_*`, `icd.floor_above_datum_a`.
Script: `research/sean/cr_scratch/sketches/s4_base_section.py`. PNG: `research/sean/cr_scratch/s4_base_section_r1.png`.
Sketch-specific checks: the base parts plotted from params agree with the Step 7 built heights (`stop.collar_top_z` 159.84 recomputed) within 0.5 mm; the advance path clears the receiver floor or the sketch shows the floor change it needs (K7). **[SE: controls.]**
Cross-review: none required (no new placement computed); The Designer reviews the kept parts as drawn.
Gate: visual gate (image-capable), then Sean.

**Detail 1.5. S6, side, ring-gear and pinion close-up (drawn before S5, Design Notes 5).**
Question: where does the spin torque go, what carries the drill weight, and how does the iris drive sit with three pinions?
Shows: drill tube with the ring gear mounted on it, three bevel pinions (two visible in projection, trapezoids in side view), NEMA 23 motors with optional gearbox, support ring with shaft bushings, the ring structure section, torque reaction path from motor mounts into the ring and from the ring into whatever stops it rotating (screws are lead screws and react torque only in bending; the sketch must show the anti-rotation member), drill weight path into the pinions. Plan inset of the gear and pinions (end view: circles allowed).
Closes: R4, R5; Q3 detail; DN23 opens on ring gear size and source, gearbox ratio, drill rpm and torque target (as owner items if unanswered), iris drive with three pinions.
Params keys: `drill.tube_od`, `drill.r_face`, `icd.keepout_radius`, `icd.torque_reaction`; overlay `gear.*`, `pinion.*`, `ring.*`, `drill.length`.
Script: `research/sean/cr_scratch/sketches/s6_ring_gear.py`. PNG: `research/sean/cr_scratch/s6_ring_gear_r1.png`.
Sketch-specific checks: gear bore clears the drill tube OD by a stated fit; pinion pitch cones meet the gear pitch cone at one apex (bevel geometry); torque path drawn as a closed chain of members, each in the feature table; K5 with pinions as trapezoids in side view. **[SE: controls.]**
Cross-review: The Loftsman (bevel cone apex, gear ratio arithmetic), The Topologist (pinion side and spin sense).
Gate: visual gate (image-capable), then Sean.

**Detail 1.6. S5, stock map.**
Question: can the frame, screw supports and anti-rotation members be built from whole on-hand lengths?
Shows: each on-hand 30-6060 length (1540 x 4, 980 x 4, 952 x 1, 728 x 2, 644 x 2, 488 x 2, 468 x 2) placed as a bar, assigned to a member from S1 to S3 and S6, with leftovers; the base members already allocated (644, 488, 468) shown as allocated.
Closes: R16; the 1540 reservation in `bom_stock_allocation.md` (held for columns that no longer exist).
Params keys: `stock.on_hand`, `frame.members`, `profile.*`; overlay `frame_upper.*`.
Script: `research/sean/cr_scratch/sketches/s5_stock_map.py`. PNG: `research/sean/cr_scratch/s5_stock_map_r1.png`.
Sketch-specific checks: per length, assigned pieces at most on-hand quantity (mirrors P3); every frame member in the overlay maps to a stock length or to the extra-cut table; leftovers summed. Known-bad: one 1540 assigned five times fires. **[SE: controls.]**
Cross-review: none (no placement).
Gate: visual gate (image-capable), then Sean.

**Detail 2. Lift detail decision record.**
Objective: one table that decides sync (single controller or belt link), anchoring (bottom thrust bearing, top guide type), anti-rotation and torque reaction member, screw size (T8 if every operating case is tension, TR10 or TR12 if a compression case exists), lift motor count against the NEMA 17s on hand.
Inputs: accepted S1, S2, S3, S6; Quinn DN23.
Output: `research/sean/cr_scratch/step2_lift_decision.md` (table: item, options, choice, reason, sketch reference, owner if open). If a choice changes a frame member, S5 is re-run as a new revision and re-gated.
TDD stage: checks before writing. **[SE: fill: e.g. every row cites an accepted sketch revision; every choice traces to a K-check result or a DECLARED source; a planted row with no sketch reference fires.]**
Red-first: the checks run on an empty record and fail.
Visual gate: none (table), unless S5 is re-run.
Human gate: Sean decides each row; Quinn consulted on motor counts.

**Detail 3. Open-question sweep.**
Objective: every Q1 to Q11 and every DN23 open item has an answer (with source and date) or an owner and a due point.
Output: the Open Questions section of this gameplan updated, plus `research/sean/cr_scratch/step3_question_sweep.md` (the batch of questions sent to Quinn, his answers, and which sketch or record each closes).
TDD stage: scripted check that each Q row in Open Questions has status ANSWERED (source, date) or OWNED (name, due step); zero control: a fully filled table passes; known-bad: one blank owner fires. **[SE: confirm.]**
Red-first: run on the current Open Questions table, which has open rows, and record the failures.
Visual gate: none.
Human gate: Sean confirms owners; Quinn answers Q2 and the drill items.

**Detail 4. Params and test change list, then execution (Q11).**
Objective: change the shared design files to match the accepted configuration through LLM-PLM 5.2 and 7.2: params first, re-run tests, record what retires. Nothing deleted unrecorded (critical-path 10, tdd_method Principle 6).
4a. Change list (before any edit): every params key that changes, is added (promoted from the overlay) or becomes void; every test that opens or reads those keys or the retired structure (grep of tests/ and tests/probes/ for each key); disposition per test: KEEP, REWRITE (new criterion), RETIRE (reason, replacing test if any). Seed list for the audit, to be completed by grep:
- Keys: `upper.park_z`, `upper.park_stroke`, `upper.park_lock`, `upper.manual_raise`, `upper.raise_fuse`, `hoist.anchor_member`, `column.spacing`, `stop.height_range`, `stop.start_z`, `stop.pad_xy` (column face 244), `icd.coaxiality_chain` (column foot 0.283, carriage guide 0.15), `icd.column_foot_moment`, `icd.tipover_statement`, `icd.mass_target`, `frame.members`, `bom_stock_allocation.md` 1540 reservation.
- Tests: test_P10_working_stroke_per_core_class, test_P10_icd_frozen_keys_exist_with_source_and_status (frozen list names `upper.manual_raise`, `hoist.anchor_member`, `column.spacing`), test_P6c_working_stroke_per_core_class, test_P6d_park_clears_core_both_lengths, test_P18_start_z_and_park_arithmetic, test_P3_1540_unused, test_A1c, test_A1d, test_A1e, test_A3b column foot and carriage guide (green_at_12).
- ASSEMBLY.md: ICD row "travel 500 with start_z 684.84 / 815" (stale against params 650 and 834.84 / 965), load path bullets for descent, manual raise and column feet.
4b. Sean approves the list.
4c. Execution: edit `params.yaml` first, then ASSEMBLY.md, then tests (rewrite or retire with a retirement table in `research/sean/cr_scratch/step4_test_retirement.md`: test ID, old criterion, reason, replacement), then run pytest and record collected, pass, fail against the 672 / 620 / 52 baseline. Repository Sync rules apply; a conflict in a shared file stops the session.
TDD stage: test audit (Principle 6) is the suite for this step. **[SE: fill the controls: a key in the change list with no test disposition fires; a retired test with no reason fires; planted deletion of a test file without a retirement row fires.]**
Red-first: run pytest before any edit and record the baseline.
Visual gate: none.
Human gate: Sean at 4b and at the step close.

**Detail 5. Week-close configuration record (prose for Quinn, A.6.2).**
5.1 Test suite (tdd_method Prompt 1), sized to a short record (about 30 tests, tdd_method "On Test Count"), every fact test naming its source (critical-path section and timestamp, Quinn DN23, accepted sketch revision, or params key) and its status (DECLARED or ASSUMED). 5.2 Topic-sentence outline validated against the suite by a scripted coverage matrix. 5.3 Write. 5.4 Revise; Designer review of echo sites against the Echo Site Registry.
Output: `research/sean/cr_scratch/step5_configuration_record.md`; the shared location is set at the gate (Design Notes 7).
TDD stage: all four stages. **[SE: fill suite groups and the coverage-matrix check with controls.]**
Red-first: the suite runs on an empty record and fails.
Visual gate: sketch links resolve to accepted PNGs (scripted).
Human gate: Sean, then pushed for Quinn.

**Detail 6. Manager week close.** The Manager verifies Objectives 2 to 8 against outputs on disk, writes accumulator entries, and presents the configuration, the executed change list and the owner table at the gate.

**Detail 7. Upper-assembly CAD.** Placeholder. Scoped at the week-close gate; it gets a work order and its own test suite before any geometry.

---

## Context Recipes

| Step | Agent | Files / Excerpts |
|------|-------|-----------------|
| 1.0 | The Engineer | this gameplan (Objectives, detail 1.0, Design Notes), supplements/llm_plm_cad.md 7.4, 8.4 to 8.4.2, method/tdd_method.md (Principles 9, 10), params.yaml top-level key list |
| 1.0 | The Software Engineer | detail 1.0, sketch_common.py, check_sketch.py, fixtures/, baseline_red.json, tdd_method.md |
| 1.1 to 1.6 | The Designer (params review) | the sub-step's detail block, the params keys it lists (grep, not the whole file), proposed_params.yaml, llm_plm_cad.md 8.4 item a and b, Design Notes 1, 2, 13 (no scripts) |
| 1.1 to 1.6 | The Engineer | the sub-step's detail block, the Designer's params review for that sketch, sketch_common.py, proposed_params.yaml, params.yaml keys listed, context/2026-11-24_cutjig_critical_path.md sections 7, 14, 15, Design Notes 13 (corrections so far), prior accepted sketch PNGs and checks JSON |
| 1.1, 1.2, 1.3, 1.5 | The Loftsman, The Topologist | the sketch script, its checks JSON, the sketch spec, params and overlay keys it reads, ASSEMBLY.md Coordinate frame |
| 1.1 to 1.6 | The Designer (visual gate, image-capable model) | the PNGs, the sketch spec, the rubric in detail 1, checks JSON, Design Notes 13 |
| 2 | The Engineer | accepted S1, S2, S3, S6 PNGs and checks JSON, research/quinn/gameplan.md Design Note 23 (lines 774-780, read only), proposed_params.yaml, Design Notes 13 |
| 2 | The Systems Engineer | step2_lift_decision.md, accepted sketches, Design Notes 1 to 4, critical-path section 15 |
| 3 | The Engineer, The Manager | Open Questions section, critical-path section 9, research/quinn/gameplan.md Design Note 23 (read only), Step 2 record |
| 4 | The Software Engineer | detail 4, tests/ file list, tests/test_params_bom.py, tests/test_assembly.py, proposed_params.yaml, step2_lift_decision.md, method/tdd_method.md Principle 6, llm_plm_cad.md 5.2, 7.2 |
| 4 | The Engineer | approved change list, params.yaml, ASSEMBLY.md, proposed_params.yaml, tests named in the list, Repository Sync section |
| 4 | The Systems Engineer | change list, ASSEMBLY.md (Load path, Interface control table), params.yaml `icd.*`, `upper.*`, `stop.*` |
| 5.1, 5.2 | The Software Engineer | Document Structure, accepted sketches, step2_lift_decision.md, step4_test_retirement.md, Open Questions, tdd_method.md, operational_guide A.10 |
| 5.2, 5.3 | The Engineer | suite, Document Structure, supplements/writing-guides/reporting-copy.md, accepted sketches, Step 2 to 4 outputs |
| 5.4 | The Designer | record draft, suite, Echo Site Registry, accepted sketch PNGs |
| 6 | The Manager | this gameplan, all Step 1 to 5 outputs, research/sean/accumulator.md (persona sections) |

---

## Progress Log

| Step | Date | Notes |
|------|------|-------|
| 0 | 2026-11-24 | Drafting variant (A.6.4). The Engineer drafted Objectives, Document Structure, Steps and details, Context Recipes, Design Notes, Echo Site Registry and Open Questions. Pending: Software Engineer TDD revision, Wave 2 (Systems Engineer, Designer), Engineer revision, Manager close, Sean's gate (lit_review question, Design Notes 4 to 9). Baseline pytest 672 collected, 620 pass, 52 fail (Quinn's header). |

---

## Design Notes

(Decisions and every human sketch correction, recorded so the next session does not repeat them.)

**1. Decisions in force (DECLARED, Quinn, 2026-11-24).** Source: Design Note 23 of `research/quinn/gameplan.md` and section 15 of `context/2026-11-24_cutjig_critical_path.md`. Travel 650 mm. Bevel ring gear on the drill, three pinions at 120 deg, each on a NEMA 23 (on hand), gearbox optional; pinions carry drill weight, support ring with shaft bushings if needed. Drill, ring gear and motors ride one ring structure; the ring moves on three jack screws at 120 deg, probably NEMA 17. T8 lead screws with brass nut, 800 to 900 mm, anchored at the bottom with a thrust bearing and guided only at the top, so cutting load puts the screw below the nut in tension; TR10 or TR12 if a compression case is needed. The three lift motors move as one axis (single controller or belt link; the sketch phase picks). Kept: collet family and generator, holder, wing nut, receiver, PTFE washer. Core never inverted; drill moves, core stays.

**2. Superseded (do not draw or test against).** Arbor press (critical-path section 6 option A); ratchet hoist and hoist cross member (`hoist.*`, `upper.manual_raise`, `upper.raise_fuse`); two-column carriage (`column.*`, 1540 mm columns in critical-path section 8 and the `bom_stock_allocation.md` reservation); "twin" jack screws (critical-path section 6 option B; three governs); S3 per lift option (critical-path 7.3); week-done bullet "lift option chosen or narrowed to two" and critical-path 7.4, which now read "lift detail decided" (Objective 4); critical-path section 8 height stack (replaced by S1). The frame's role under a ring on three screws is undefined until S1 and S2 define it.

**3. Deviation from LLM-PLM 8.4 (recorded).** This week is 2D matplotlib only (critical-path 7.2): no STEP sketch assembly, no PNG render or turntable of solids, and sketch-level interference is 2D outline overlap (check K7). LLM-PLM 8.4 assigns sketch production to The Designer; here The Engineer writes the sketch scripts because they are code with scripted checks, and The Designer keeps the params review (8.4a), the representative-shape spec (8.4b) and the critique and visual gate (8.4c) on an image-capable model. The Designer did not produce the image, so the gate is independent (A.3.1).

**4. S3 redefinition (for Sean to confirm).** S3 becomes the side section through one jack screw: bottom anchor, screw, nut on ring, top guide, lift motor, sync method, load arrows (detail 1.3).

**5. Sketch drawing order (for Sean to confirm).** S1, S2, S3, S4, S6, S5. S6 is drawn before S5 because the anti-rotation and torque reaction members in S6 are frame members the stock map must place. Sketch IDs keep the critical-path numbering.

**6. Proposed-keys overlay (for Sean to confirm).** Keys the sketches need that `params.yaml` lacks live in `research/sean/cr_scratch/sketches/proposed_params.yaml` during Step 1, with source and status per leaf. `params.yaml` is unchanged until Step 4, when accepted keys are promoted and void keys are retired in one LLM-PLM change. Check K2 fails on any overlay key that shadows a params.yaml key.

**7. Shared location for accepted sketches (for Sean to confirm).** Proposed: `docs/sketches/` (shared, committed), holding the accepted PNG, its script and its checks JSON per sketch. The scratch copies stay in `research/sean/cr_scratch/`.

**8. Geometry cross-review (A.4 step 2).** Assigned on S1, S2, S3 and S6, where the sketch computes placement or projection: The Loftsman on arithmetic and placement, The Topologist on orientation and sense. S4 and S5 compute no new placement.

**9. Week-close record is prose (for Sean to confirm).** Step 5 treats the configuration record as a short prose document for Quinn and runs test suite, outline, write and revise (A.6.2).

**10. Test baseline.** Quinn's header (672 collected, 620 pass, 52 fail) governs over critical-path section 10 (622 / 50, Step 7 close). The two added failures: test_P10_working_stroke_per_core_class (park 959.84 below the 965 start after travel 650) and test_common_guard_shifted_partner (stale probe timestamp).

**11. Torque reaction is a design gap to close in S6 and Step 2.** The jack screws are lead screws; they resist ring rotation only in bending, and a T8 screw about 850 mm long is a poor torque member. S6 must show the member that stops the ring rotating and carries the spin-torque reaction to the frame.

**12. ASSEMBLY.md is stale on travel.** Its ICD row reads "travel 500 with start_z 684.84 / 815"; params reads 650 and 834.84 / 965. Fixed at Step 4 through LLM-PLM, with the other ASSEMBLY.md rows the redesign touches.

**13. Sketch correction log.** One row per human correction. Format `S<N>-r<k>`.

| ID | Date | Correction (Sean's words) | Fixed in |
|---|---|---|---|
| | | | |

---

## Echo Site Registry

Values that must agree in every sketch, record and test. Authority is `params.yaml` (or the overlay during Step 1) unless stated.

| Value | Authority | Status |
|---|---|---|
| Travel **650 mm** | `upper.travel_max`; Quinn DN23 | DECLARED |
| Drill length **about 800 mm** | overlay `drill.length`; critical-path 18:20 | ASSUMED (Q2) |
| Capture **500 mm** core | `core.length_capture` | DECLARED |
| Three screws and three pinions at **120 deg** | overlay `jackscrew.*`, `pinion.*`; Quinn DN23 | DECLARED |
| T8 screws **800 to 900 mm** | overlay `jackscrew.length`; Quinn DN23 | DECLARED range |
| Axial design load **1000 N** | `loads.axial_design` | ASSUMED (design choice) |
| Drill tube **152.4 mm** OD; keep-out radius **86.2 mm** | `drill.tube_od`, `icd.keepout_radius` | ASSUMED / DERIVED |
| Soft height **2000 mm**, never a limit | `jig.height_target` | DECLARED |
| Loading park **959.84 mm** (re-derived in S1) | `upper.park_z` | ASSUMED |

---

## Open Questions

Full text of Q1 to Q11 is in section 9 of `context/2026-11-24_cutjig_critical_path.md`. Step 3 brings every row to ANSWERED or OWNED.

| # | Question | Status | Owner / closes in |
|---|---|---|---|
| Q1 | Travel | ANSWERED 2026-11-24: 650 mm | Quinn; S1 confirms on the drawing |
| Q2 | Drill length, mass, top-end hardware | Open; S1 uses 800 mm ASSUMED | Quinn (drill in build) |
| Q3 | What spins the drill | ANSWERED 2026-11-24: ring gear, three NEMA 23 pinions | Quinn; S6 details |
| Q4 | Push-pop advance | Open | Sean, S4 |
| Q5 | Collet length | Open | Quinn and Sean, S4 |
| Q6 | Sacrificial collet or liner | Open | Sean, S4 |
| Q7 | Lift | ANSWERED 2026-11-24: three jack screws | Quinn; detail in S3 and Step 2 |
| Q8 | Manual or powered travel; feed control | Open (powered by the decided lift; feed control open) | Sean, S3 and Step 2 |
| Q9 | Core lengths to support | Open | Quinn; S1 draws 500 and 750 |
| Q10 | Short 100 x 100 mm cores | Open | Sean, S4 |
| Q11 | Tests and params that become void | Open | Sean (contributor making the change), Step 4 |
| DN23-a | NEMA 17 count on hand | Open | Sean (owns the motors), Step 2 |
| DN23-b | NEMA 23 gearbox ratio | Open | Quinn and Sean, S6 |
| DN23-c | Drill rpm and torque target | Open | Quinn, S6 |
| DN23-d | Ring gear size and source | Open | Sean, S6 |
| DN23-e | Iris drive with three pinions (INSITU2 157-166 via Quinn DN23) | Open | Quinn, S6 |
| N1 | Ring position along the drill | Open | Sean, S1 |
| N2 | Anti-rotation and torque reaction member for the ring | Open | Sean, S6 and Step 2 |
| N3 | lit_review flag: does this phase carry technical claims that need primary sources? (`no` here, `yes` in Quinn's plan) | Open | Sean at the Step 0 gate (A.6.1) |

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
