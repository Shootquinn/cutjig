# Core Cutter Test Jig Gameplan

**Document(s) under work:** workorder.md (core cutter test jig: base with tubular receiver, core holder, wing nut, collet family; 3D models, physical hold test, technical report)
**Operational guide:** C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\method\operational_guide.md
**Accumulator file:** none, new project (created by The Manager at Step 0 close from templates/accumulator.md)
**Other reference files:**
- workorder.md
- supplements/llm_plm_cad.md (CAD active), supplements/freecad_api_reference.md
- method/tdd_method.md
- supplements/writing-guides/reporting-copy.md, structure.md, style.md, style-reference.md, supplements/signs_of_ai_writing.md
- research/quinn/cr_scratch/step0_engineer_source_extraction.md (cutter, envelope, load, core facts; corrections in Design Notes 8 must be applied to it at Step 1)
- research/quinn/cr_scratch/step0_human_stock_80-20.md (30-6060 stock on hand; DECLARED)
- research/quinn/cr_scratch/step0_manager_open.md
- research/quinn/cr_scratch/step0_systems_engineer_review.md, step0_loftsman_review.md, step0_topologist_review.md, step0_fact_checker_review.md, step0_designer_review.md (Step 0 findings; dispositions at the end of this file)
- SBIR folder: C:\Users\Quinn Morley\OneDrive\PROJECTS\Planet Enterprises\NIAC\BOREBOTS\Unleashed Robotics\2026 PROPOSALS\2026 SBIR\ (cr_scratch/INSITU2_text.md is the iris proposal text; cr_scratch/INSITU3_text.md for WOB; proposals/csm_sow.md; context/)
- Rigged drill model: C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\gpr (DOUBLE DONG, 7 in bore, NOT the 6 in redesign)
**Date:** 2026-11-08
**Current step:** 0 (Engineer final revision against the reviews; The Manager closes and gates to the human)
**lit_review:** yes
*Reason: the report will cite Mines/SBIR numbers (aperture, WOB, rpm, core diameter). Each test asserting such a number names its primary source and carries a verification status (Source Verification Register). Sources are summarized once into context/literature/ before tests cite them, and only the sources a test cites get a summary (INSITU2, INSITU3, csm_sow, gpr params, motor summary).*

---

## Objectives

1. Review workorder.md as the contract and populate the gameplan (Step 0).
2. Fix the mechanism on paper before any test or solid: a one-page system concept (closed force loop, release, load cases, tolerance budget, interface control table) at Step 2, then the geometry numbers at Step 3, then the CAD suite at Step 4.
3. Build every part as 3D models from one spine (`params.yaml` plus `build_parts/common.py`; the collet family comes from one generator, the other parts from per-part scripts that read the same interface table): base with tubular receiver (the workorder's "threaded boss"), core holder, wing nut, collet family for 90 to 105 mm cores, 30-6060 frame, and the accessories the Designer's checklist requires.
4. Prove the models by scripted test with named pass criteria and evidence: per-collet volume and diameter, thread engagement and handedness, seat fit, contact-class interference matrix, placement predicates, clamp range at the family extremes, holding torque estimate, STEP/STL validity.
5. Prove the jig does its job by a physical hold test at Step 11 against values predicted in advance, and write the five-verb end-to-end acceptance spec (hold, descend, sever, retain, retract) at Step 12 so the upper assembly is designed to be accepted by it.
6. Deliver a concise technical report (executive summary crossed with an engineering-school project) through the TDD document path: test suite, topic-sentence outline validated against the suite before any drafting, reporting copy, writing wave, Wave 2 review.
7. Scope the drill-holding upper assembly jointly with the human after base review.

---

## Document Structure

**The point, in one sentence:** A 30-6060 frame with a printed tubular receiver, wing nut and collet family is designed to hold a 90 to 105 mm Mines core upright and coaxial under the 6 in drill; CAD tests and a physical hold test check the design, and three inputs (closure torque, iris aperture, core tolerance) are still open.

**Shape:** Lead-first (LDR). Readers are an SBIR program manager and an engineering faculty member who may stop after page 1. Page 1 gives the design, the verification result, what is deferred, and a "what we need from you" block (iris aperture of the 6 in drill, Mines core length and tolerance, closure torque from Phase I, and the risk if each arrives late). Page 1 also states that the drill's own drivetrain closes the iris and the jig has no actuator. Later sections give method and evidence. An analysis section (requirements, free-body diagram, derivation, tolerance budget, prediction against test) serves the engineering-school reader.

**Opening promises:** Audience: SBIR program manager and engineering faculty. Breadth: base, holder, wing nut, collet family and frame as designed, verified in CAD, and checked by the physical hold test if the result is back before the report is built (otherwise stated as pending). No claim of built upper assembly, drill test data, or flight representativeness.
**Resolution delivers:** The same breadth: models, CAD test evidence, analysis with prediction, hold-test result or its status, BOM, status of upper assembly scoping and the acceptance spec.

**Known limitations and where each goes:**

| Limitation | Placed in | Why there |
|---|---|---|
| Cutting face (sets borehole and core diameter) out of scope | Scope paragraph, section 1 | Reader needs it before any dimension |
| Jig does not actuate the iris; the drill drivetrain does | Page 1 clause and section 2 | A page-1 reader would otherwise misread the load path |
| Holding torque unverified; analytic estimate (about 7 to 10 N m at hand-tight) is below the 20 N m placeholder | Page 1 and section 4 (analysis) | It is the binding performance limit |
| Iris open aperture of the 6 in drill unresolved; 105 mm core may not fit | Page 1 "what we need" block and section 2 | It can cut the range |
| Collet coverage between nominals depends on grip window and core tolerance (UNVERIFIED) | Section 5 (collet family) | Placed with the coverage test |
| Upper assembly deferred, jointly scoped | Section 8 (status and next step) | It is the next action |
| Printed parts are not flight-representative; PETG creep and thread wear | Section 6 (printability) with the test that bounds it | Placed with the evidence |
| Core length, mass, torque, tolerance stated by no source | Section 2, as open inputs with the margin used | Margin is part of the design |
| Rigged model is the 7 in drill, not 6 in; 106.369 mm is a 7 in model value | Appendix A (source notes) | Provenance, not design |
| Printing and fit validated in CAD and analytic coupons until the human prints | Section 8 | The human's print is the next gate |
| Mines documents were not read in full (PDF render unavailable) | Appendix A | Provenance |

Report outline (8 to 12 pages, DOCX plus PDF): 1 Summary and scope; 2 Requirements and interfaces; 3 Concept (stack, force loop, release); 4 Analysis (load cases, holding torque, tolerance budget); 5 Collet family (generator, taper, slits, coverage); 6 Printability and tolerances; 7 Verification (CAD interference, predicates, physical hold test); 8 Status, acceptance spec, upper assembly scoping, open items; Appendix A source notes; Appendix B BOM and stock allocation; Appendix C drawings and renders. The topic-sentence outline is built at Step 14; the suite is Step 13.

---

## Steps

Re-sequenced against the reviews: foundation, then the one-page concept, then geometry numbers, then the CAD suite. Rationale and ruling in Design Notes 1.

| # | Step | Assigned To | Status |
|---|------|-------------|--------|
| 0 | Team reviews workorder.md, populates gameplan; Software Engineer revises for tests; reviewers weigh in; Engineer revises against findings; Manager closes. Gate to human with the blocking questions (top of Open Questions). | The Manager (open, close), The Engineer, The Software Engineer, The Systems Engineer, The Loftsman, The Topologist, The Fact-Checker, The Designer | In progress (Engineer final revision done; Manager close next) |
| 1 | Foundation: params seed, BOM, 30-6060 frame model, FreeCAD check, ASSEMBLY.md skeleton, extraction-file corrections, iris aperture request, Designer seed params review (non-blocking). See detail 1. | The Engineer, The Fact-Checker, The Designer | Not started |
| 2 | System concept, one page: force loop, release, three load cases, tolerance budget, interface control table, family spacing, stop ownership. See detail 2. | The Systems Engineer (author), The Loftsman, The Topologist, The Designer, The Engineer | Not started |
| 3 | Geometry cross-review: thread, cone, slits, seat, register, clamped-state solid. Designer params review is the blocking gate before any geometry. See detail 3. | The Loftsman, The Topologist (cross-review), The Engineer (script), The Designer (gate) | Not started |
| 4 | CAD test suite, red-first, source-gated. See detail 4. | The Software Engineer (author, signs), The Engineer, The Fact-Checker (source gate) | Not started |
| 5 | Parametric collet-family generator. See detail 5. | The Engineer, The Software Engineer (test review) | Not started |
| 6 | Exploratory pass (Pass 1): every part and accessory, simplified. See detail 6. | The Engineer, The Loftsman, The Topologist, The Designer (gate, image-capable reviewer) | Not started |
| 7 | Assembly, contact-class matrix, predicates, clamp range, wrong-state controls. See detail 7. | The Engineer, The Software Engineer, The Systems Engineer, The Designer (A5) | Not started |
| 8 | Printability, tolerance stack-up, holding-torque check, coupons. See detail 8. | The Engineer, The Loftsman, The Software Engineer | Not started |
| 9 | Production pass (Pass 2). Designer production checklist gate. See detail 9. | The Engineer, The Loftsman, The Topologist, The Designer (gate, image-capable reviewer) | Not started |
| 10 | Final assembly, independent re-measure of exports, STEP/STL/FCStd, code review, topology gate. See detail 10. | The Engineer, The Topologist, The Software Engineer, The Systems Engineer | Not started |
| 11 | Base review package, inter-step gate, and physical hold test on the human's print. See detail 11. | The Manager, the human, The Designer (print-review form), The Systems Engineer (protocol) | Not started |
| 12 | Joint scoping of the upper assembly; end-to-end acceptance spec written first. See detail 12. | The Manager, The Systems Engineer, The Engineer, the human | Not started |
| 13 | Report test suite (Prompt 1, about 90 tests), source-verified. See detail 13. | The Software Engineer, The Fact-Checker | Not started |
| 14 | Report topic-sentence outline (Prompt 2), validated against the suite before any drafting. See detail 14. | The Engineer, The Software Engineer (signs), The Designer (structure) | Not started |
| 15 | Engineer reporting copy (reporting-copy.md). Opens only after the Step 14 validation record exists (A.4). | The Engineer | Not started |
| 16 | Writing wave, Writer first. | The Writer | Not started |
| 17 | Writing wave, Editor second. | The Editor | Not started |
| 18 | Wave 2 review: Designer, Fact-Checker, Systems Engineer. | The Designer, The Fact-Checker, The Systems Engineer | Not started |
| 19 | Revision, DOCX and PDF build, final suite run, final cold read, echo-site audit. | The Engineer, The Software Engineer, The Designer | Not started |
| 20 | Close: accumulator, archive, gate to human. | The Manager | Not started |

Steps after 12 may be re-sequenced by the human at the Step 11 and Step 12 gates; if the upper assembly enters the report scope, Steps 13 to 15 wait for the Step 12 work order and the suite is re-sized to 150 or more.

### Step details

**Detail 1. Foundation.**
Objective: ground the project before the mechanism is designed.
TDD stage: no geometry tests yet. Tests written here are the params and BOM tests only (P1 to P7), red on an empty params file.
Work: confirm FreeCAD at `C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe`; confirm the 30-6060 cross-section against the 80/20 catalog (60 x 60 mm, 30 mm slot pitch) and model it as a parametric extrusion; compute stock allocation (Design Notes 7) with extra cuts listed separately; fix the bracket class (full-size 30-series, no "mini") and T-nut rule (M6 spring-ball roll-in only); select bracket SKUs from the catalog; patch the extraction file with the Fact-Checker corrections (Design Notes 8); write the seed `params.yaml` (every externally sourced number carries `source:` and `status:`); write `ASSEMBLY.md` skeleton: coordinate frame (Design Notes 4), poses R and K, relation table as data, signed feature per part, load path placeholder; request the 6 in iris open aperture (unit and value) and which 2026 STEP is the 6 in drill (Blocking question B1).
Outputs: `params.yaml` (seed), `ASSEMBLY.md` skeleton, `build_parts/common.py` (paths, YAML loader, 30-6060 profile builder), `conftest.py`, `tests/test_params_bom.py`, `bom_stock_allocation.md`, `bom_purchased.md`, corrected extraction file, `research/quinn/cr_scratch/step1_designer_params.md` (Designer seed review: which functional features lack a specification), `context/literature/` summaries (cited sources only).
Gate: Fact-Checker signs the corrections; Designer review recorded (non-blocking). Iris aperture status recorded (answered, measured, or UNVERIFIED with default). Any FreeCAD run over 30 s goes background (A.3.4).

**Detail 2. System concept (one page).**
Objective: decide, on one page, the things that set the shape of every part. Author: Systems Engineer with the Loftsman; the Topologist and Designer review; the human answers or accepts defaults for B1 to B6.
Contents, each a numbered decision with a number or a stated assumption:
1. Closed force loop sentence (written into ASSEMBLY.md): nut thread flank, nut clamp shoulder, holder bearing flange, holder cone, collet cone, collet foot, receiver floor seat, receiver wall, receiver thread flank, nut thread flank. The holder never bottoms on the receiver or base (S6, G-class pair); nut and receiver alone must not form a loop that moves nothing.
2. Release mechanism: captured-flange nut with a modest cone, or releasing cone (half-angle above atan(mu_k)), with the ruling in Design Notes 3; jacking provision regardless.
3. Load cases (statics estimate, assumptions labelled): (a) iris closure and severing reaction as torque on the core (20 N m placeholder, UNVERIFIED) and lateral load at a lever arm of 106 mm or more above the holder; (b) core weight to 9.4 kg (DERIVED upper bound) with retention; (c) cutter descent load, which does not reach the core and is carried by the stop path to the frame, not the printed parts. Required holding torque stated as an assumption with safety factor 2 (provisional).
4. Holding capacity estimate and design response (core liner TPU or silicone, thrust washer pocket, tommy-bar socket, longer wings); escalation to a positive core lock (set screws onto a band, or a second clamp) if the response does not close the gap by the Step 8 analytic check.
5. Tolerance budget table (stack-up, not per-feature): datum scheme (core axis located by the cone and pilot, never by the trapezoidal thread), thread radial clearance and tilt, collet bore print error, slit non-uniformity, core out-of-round, core tolerance, against the iris slack (1.79 mm per side at 105 mm if 54.2925 mm is a radius; no core fits if it is a diameter).
6. Interface control table (Design Notes 5), frozen as fixed numbers all parts read.
7. Family spacing (4 collets at 5 mm or 7 at 2.5 mm), slit law, grip windows.
8. Hard stop ownership (Design Notes 2): not the printed nut.
9. Base stability: footprint, feet, bolt-down slots, tip-over statement, mass target; core handling (steady rest or cradle, lift strap point).
Outputs: `research/quinn/cr_scratch/step2_system_concept.md` (one page plus the two tables).
TDD stage: each decision names the test that will check it (ID from the CAD Test Specification) before it is accepted.
Gate: Systems Engineer authors; Topologist and Loftsman sign; Designer comments; human accepts or overrides B1 to B6 at the Step 0 gate (defaults apply otherwise).

**Detail 3. Geometry cross-review.**
Objective: settle thread, cone, slits, seat, register and clamped-state solid with numbers, before any solid (A.4 two-persona rule).
TDD stage: formula tests exist from Step 4 and read these numbers; this step supplies the values and the signs. Disagreements are resolved by number, not opinion.
Work, Loftsman: thread form (right-hand, single start, symmetric 45/45 trapezoid, pitch 8 mm PROPOSED), major diameter from the radial chain (Design Notes 3; seed 165 mm at 20 degree cone, reviewers' range 135 to 165 mm), clearances c_r and g_a, cone half-angle, stroke s_z, stop gap, nut length, bore_free(d) = d + tau + c_i, slit count and width law, wall and flexure relief, hand-torque holding estimate (T7 inputs), wing planform, collet total length and ring height, key, debris tray and core stop geometry (the items the Loftsman lists as having no analytic definition). Topologist: sign predicates S1 to S23 against those numbers, contact-class table, register length for cross-thread defence (confirm or replace the 54 mm figure with a stacked register on holder flange and holder-in-receiver bore), collet topology (alternating slits), OCC strategy for coincident cone faces in the clamped pose, wrong-state defences WS1 to WS11 as features.
Outputs: `research/quinn/cr_scratch/step3_geometry_crossreview.md` (one file, two sign-offs), `params.yaml` updated, the registry rows below filled.
Gate: Loftsman and Topologist sign; Designer params review is blocking: does the parameter set describe a real part (key, tray, drain, core stop, label, wing planform, register, flange recess, hard-stop gap each have parameters, not only a volume)? Designer questions D1, D2, D3, D6 must have an answer in params before Step 5 opens. Output `research/quinn/cr_scratch/step3_designer_params.md`.

**Detail 4. CAD test suite (red-first).**
Objective: contract in code before geometry.
TDD stage: the complete CAD suite (CAD Test Specification) is written, each test labelled discriminator or invariant (7.2), and run red on the empty baseline. Relations are data: tests iterate over the ASSEMBLY.md pair table, so a change in contact class or pose is a data change. Thresholds from Step 3 are read from `params.yaml`; a later suite change is a revision with Software Engineer review and source re-check (A.10 item 5).
Outputs: `tests/test_params_bom.py`, `test_collet_family.py`, `test_thread_clamp.py`, `test_assembly.py`, `test_exports.py` (printability checks live in the collet and export modules; there is no sixth module and no catch-all), `research/quinn/cr_scratch/step4_engineer_baseline.md` (red-first record).
Gate: Software Engineer signs the suite; Fact-Checker signs the source gate (A.10 item 2) against the Source Verification Register; red-first record exists.

**Detail 5. Collet-family generator.**
Objective: one generator, diameter-driven, whole family from `params.yaml`; no hand-built collets.
TDD stage: groups C and F first, then build.
Outputs: `build_parts/collet_family.py` (`build_collet(d)`), `parts_cache/collet_<d>.FCStd` (file naming holds 92.5 as `collet_092p5`), `parts_cache/collet_*_result.json`, free and clamped solids from the same call.
Family: params-driven list; default 7 collets at 2.5 mm (90 to 105), or 4 at 5 mm if the human so rules (B3). Adding a diameter is a params change for geometry; the function (clamp force per N m, wall stiffness) is a separate claim checked at the extremes (C9, T7, Step 11).
Gate: every collet passes C1 to C9; topology gate; Software Engineer reviews the generator. Builds over 30 s run as parallel background FreeCADCmd processes (A.15).

**Detail 6. Exploratory pass.**
Objective: surface problems; every functional feature present even if simplified (7.6).
TDD stage: F5 (genus and feature list) and the Step 7 tests run against each part as it appears.
Parts and features (the Designer's completeness checklist; gate fails on any missing item):
- Receiver (boss tube): thread with lead-in and land, floor seat for the collet, register for the holder, asymmetric key slot.
- Holder: cone, flange, bearing recess for thrust washer, key, jacking holes, hard-stop face.
- Collet: cone, bore, alternating slits with relief holes, foot key, core stop, rim notches, grip-window label, lead-in chamfer.
- Wing nut: thread, bearing face, wings with planform, tighten arrows, tommy-bar socket, dust skirt.
- Base: plate, debris tray, drain, slotted mounting holes, T-nut provisions, feet or bolt-down.
- Frame: members and brackets from stock with allocation.
- Accessories: collet caddy, alignment gauge, steady rest or cradle, witness scale and tick on holder flange.
- The stop: shown as an interface item at the descent assembly (Design Notes 2), not as a nut property.
Outputs: `build_parts/<part>.py`, `parts_cache/*.FCStd`, `research/quinn/cr_scratch/step6_engineer_findings.md`, `research/quinn/cr_scratch/step6_designer_critique.md` (Design Critique, 8.4c).
Gate: Designer on completeness against the checklist ("can we learn from this?"), using an image-capable reviewer for the renders.

**Detail 7. Assembly, contact classes, predicates, clamp range.**
TDD stage: groups A, T, F tests first including negative controls and WS1 to WS11.
Work: poses R (release) and K (clamp) generated from one pose by the screw motion S(phi), not placed independently; contact-class matrix (C, G, F) per pair per pose per collet; predicates S1 to S16; E-1 to E-9 envelope; N x N collet and core sweep; thread tilt test.
Outputs: `build_parts/assemble.py`, `output/jig_assembly.FCStd`, `.step`, `research/quinn/cr_scratch/step7_interference_report.md` (per-pair table, mm3, class, pass/fail; one table per collet configuration, tool-generated, not hand-reviewed), four-view PNG set.
Visual: front, side, top, isometric, judged against a rubric with an item per signed feature, signifier and pinch point (A.3.1).
Gate: Software Engineer, Systems Engineer, Designer (A5, image-capable reviewer).

**Detail 8. Printability, tolerance stack-up, holding torque.**
Objective: show parts print and fit, and that the clamp can plausibly hold, before the human spends filament.
TDD stage: T3, T7, T8, T9, C6, C9, E2 first.
Work: min wall, bed fit (256 mm class, minus 5 mm), thread clearance per side, slit web strain against the PETG allowable (UNVERIFIED; the coupon is the check), tessellation deflection; print orientation stated per part (wings in-layer, threads axis vertical, 45/45 flanks); tolerance stack-up table closed against the Step 2 budget; holding-torque check T7 reinstated at both family extremes with mu values labelled UNVERIFIED; print time and warp risk for the receiver (about 165 mm OD) and nut (about 181 mm OD, wing span about 230 mm); coupons as STL: thread coupon (boss and nut with pilot), one collet at 90 and one at 105 mm, slit flex bar, cone friction coupon (tilt-plane test for mu_k); assembly sequence for a 9 kg upright core written into ASSEMBLY.md.
Outputs: `output/coupons/*.stl`, results appended to `research/quinn/cr_scratch/step7_interference_report.md` (no separate printability file), predicted-values sheet for Step 11 (written before the print).
Gate: Loftsman reviews clearance and holding estimate; Software Engineer reviews tests.

**Detail 9. Production pass.**
Objective: every feature deployment-ready (7.6). Every operator-facing edge counts as function: wing edges, flange edge, slit edges, collet mouth, tray lip.
TDD stage: re-run all tests on production geometry; lead-ins and chamfers must not change contact faces, thread sign, pilot or cone sense.
Outputs: updated part scripts and FCStds; change-order record if params diverge from FCStd (FCStd wins; sync first, 5.2.1).
Gate: Designer production checklist (all items pass; image-capable reviewer):
1. Pride: would the Designer show the part to a client without apology?
2. Cold-user: can an operator who has not seen the jig load a 90 and a 105 mm core correctly from the part marks alone?
3. Poka-yoke: each WS1 to WS11 defence exists as a feature, not only as a test.
4. Signifiers: identity (grip-window label, color, rim notches, caddy), direction (tighten arrow), state (witness line).
5. Recoverability: jam release (jacking holes), over-travel bounded by the hard stop, nut removable with a stuck collet, a broken wing leaves the core on its stop.
6. Operator-facing edges and pinch points reviewed one by one (holder flange to receiver rim gap closing from about 6 mm; wing sweep; slit closure; dropping a core onto the stop).
7. Print orientation and wing layer direction stated per part.

**Detail 10. Final assembly and independent re-measure.**
Work: re-run all CAD tests; one independent script that imports only the exported STEP and STL (no build or test code) and recomputes per-collet volume, the interference matrix and thread chirality sign, compared to the result JSON; negative controls (probes away from the feature still hit; a deliberately wrong expected value fires; a mirrored nut export fires). The delivered FCStd opens with every deliverable object visible and named. A SHA-1 manifest of text sources is written as a backup action (not a test).
Outputs: `output/jig_assembly.FCStd`, `.step`, `output/stl/*.stl`, `output/remeasure_results.json`, renders, `ASSEMBLY.md` and BOM final, ICD final.
Gate: Software Engineer code review; Topologist final topology gate (Euler check, genus, component count per part, signed volume positive); Systems Engineer interface review (base, collet, holder, nut, frame, future upper assembly).

**Detail 11. Base review, inter-step gate, physical hold test.**
Objective: test as you fly: check the stated purpose on hardware, against values predicted before the print.
Human actions: review models; print the Step 8 coupons, then the receiver, holder, nut, and collets at the extremes (90 and 105 mm, plus one middle). Designer writes the print-review form (clamp feel, wing grip, loading the core, wrong-collet trial, jam and release, pinch points); Systems Engineer writes the protocol; results return as a change order.
Stand-in core: 100 mm concrete cylinder or PVC section of similar mass, 500 mm long, up to about 9.4 kg; also a 90 mm and a 105 mm stand-in. (Core diameters in the test match the collet under test.)
Protocol and pass criteria (predictions entered from Step 8 before the first test; Loftsman estimate 6.9 to 8.1 N m torque-to-slip at 12 N m nut torque, Systems Engineer estimate about 10 N m; both UNVERIFIED):

| Test | Method | Result recorded | Pass |
|---|---|---|---|
| H1 Torque to slip | Hand-tight nut (record nut torque), torque wrench on a lever arm about the core axis, 90 and 105 mm collets | N m at first rotation | Two outcomes reported separately: (a) model valid if within a factor of 2 of prediction; (b) requirement met if at or above the Step 2 required holding torque (20 N m x safety factor 2, provisional) |
| H2 Pull-out | Spring scale along the axis | N at first axial slip | At or above core weight x 2 (about 190 N for 9.4 kg) |
| H3 Lateral deflection | Side load at core top (10 N PROPOSED), dial indicator | mm at top, and tilt in degrees | Within the coaxiality budget of the Step 2 tolerance table |
| H4 Cycles and creep | 10 clamp and release cycles; 24 h hold; repeat H1 | Thread wear, collet set, H1 change | H1 after 24 h within 20 % of initial (PROPOSED) |
| H5 Jam and release | Back off the nut after clamping at the stop | Collet frees, holder lifts, with and without jacking holes | Release without tools beyond the jacking provision |
| H6 Wrong-collet trial | Fit a too-large collet, tighten to the stop | Does the witness line show the error | Witness line outside zone in 100 % of trials |
| H7 Cold-user loading | Unfamiliar operator loads a 500 mm stand-in using only part marks and the caddy | Time, errors, hands needed | No wrong-collet or unseated core; one operator can do it with the steady rest |
| H8 Envelope template | 152.4 mm tube template over the assembly | Gap nut top to template stop plane, template clear of every fixture above the stop | g_stop gap present at full descent |

Gate: The Manager verifies the hold-test record; failures re-enter at Step 3 (geometry) or Step 8 (analysis) as a change order.

**Detail 12. Joint scoping and end-to-end acceptance spec.**
Objective: define the drill-holding upper assembly with the human after base review, accepted against a spec written first.
First deliverable: `research/quinn/cr_scratch/step12_acceptance_spec.md`, the five-verb acceptance spec:

| Verb | Criterion | Source or status |
|---|---|---|
| Hold | Core does not rotate or slip under the measured iris reaction; core axis within the coaxiality budget of the drill axis | Torque UNVERIFIED (Phase I); budget from Step 2 |
| Descend | Axial load path 100 to 1000 N reaches the metal stop, not the printed nut; rate at least 5 mm/min at 100 N or more | INSITU3 267-268, 424-430 (verified); jig load is a design choice |
| Sever | Iris closes from the drill's own drivetrain; Hall amplitude falls from about 400 to about 45 counts; core cut at the iris plane | INSITU2 157-166 (verified); standoff for the 6 in iris UNVERIFIED |
| Retain | Severed core retained in the drill; retention force and closure torque curve measured per Phase I protocol | INSITU2 408-414 (verified) |
| Retract | Iris opens by reversing braking torque; drill retracts without disturbing the jig; core removable from the jig | INSITU2 164-165 (verified); jig release per H5 |

Agenda: guide and anchor for the 6 in drill; carriage stop on the columns (metal, rated); torque reaction (value unknown); descent method and rate; instrumentation access (load cell and Hall sensor cabling at the back cap, cable exit and debris path); whether a spindle drive is in jig scope (if yes, spawn The Motor Designer); iris closure confirmation; tip-over statement for a 1540 mm column on the stock-driven footprint; use of the 1540 mm lengths.
Outputs: `research/quinn/cr_scratch/step12_scoping_notes.md`, a new work order `workorder_upper_assembly.md`, appended gameplan Steps 12.1 and up, the decision whether the report covers the upper assembly. The upper assembly gets its own test suite before its geometry.

**Detail 13. Report test suite (Prompt 1).**
Inputs: workorder.md, Document Structure, extraction file, Step 10 result JSON (names of values), Step 11 hold-test record, Source Verification Register.
Size and split: about 90 tests (ruling in Design Notes 6). Manager ratifies at Step 13 open and records the deviation from A.10 item 7's 150 to 200 band with the reason.

| Scope | Group | Count | Mode |
|---|---|---|---|
| Whole document | Thesis and lead-first (page 1 alone states design, verification, deferrals, what we need) | 4 | manual |
| Whole document | Audience comprehension (cold read, page-1 test, zero control) | 5 | manual, fresh-context reader |
| Whole document | Communication architecture (abbreviations, figures, callouts, terminology) | 7 | 5 automated, 2 manual |
| Whole document | Consistency and echo sites against the registry | 8 | automated |
| Whole document | Prose-quality detectors | 4 | automated |
| Whole document | Format and build | 4 | automated |
| Whole document | Scope honesty (no jig actuator, no flight claim, no built upper assembly, holding torque unverified) | 4 | manual |
| Section | 1 Summary and scope | 5 | mixed |
| Section | 2 Requirements and interfaces | 9 | mixed |
| Section | 3 Concept | 4 | manual |
| Section | 4 Analysis | 7 | mixed |
| Section | 5 Collet family | 7 | mixed |
| Section | 6 Printability and tolerances | 5 | mixed |
| Section | 7 Verification and hold test | 9 | mixed |
| Section | 8 Status and open items | 4 | manual |
| Section | Appendix A source notes | 3 | manual |
| Section | Appendix B BOM and stock | 1 | automated |
| Section | Appendix C drawings | 1 | manual |
| **Total** | | **91** | |

Test record format: ID, scope, what is tested, pass/fail criterion, evidence required, automated or manual, severity, and for any fact: primary source (file and line) and verification status.
Named tests:
- WD-C1 Cold read: a fresh-context reader gets only the PDF text and answers 8 fixed questions (what the jig holds; how a core is clamped; what the wing nut does; what the iris actuation source is; what was verified and how; what is not verified; what is deferred; what the human does next). Pass: at least 7 of 8 against the answer key. Zero control: an unrelated document scores 0 of 8. Known-bad control: the report with Section 7 deleted fails "what was verified". The cold read runs twice only: on the concatenated topic sentences (Step 14) and on the final PDF (Step 19). Wave 2 (Step 18) reviews those results and does not run a third.
- WD-C2 Page 1 alone answers the first three questions and states what the program manager must supply.
- WD-A1 Abbreviations (all-caps tokens expanded at first use per section or on an allowed list); known-bad: planted undefined token fires; zero control: fully defined text reads zero.
- WD-A2 Figures: each figure maps to a body claim, a regenerating script and data, and a caption matching the plotted quantities; every labelled value traces to a results JSON field or a sourced number. Known-bad: figure with no body claim fires.
- WD-A3 No orphan callouts; WD-A4 one term per part (receiver defined once at first use as the workorder's "threaded boss", a tubular receiver; holder, collet, wing nut), synonyms counted by grep.
Fact tests: every numeric claim names its primary source and status. Controls (Principle 9): the AI-tell grep and the echo-site audit each run on a clean text (reads zero) and on a text with planted defects (fires) before output counts.
Output: `report_test_suite.md`. Gate: no test with status UNVERIFIED survives unresolved; each is listed with its unblock owner and is either resolved or rewritten to assert a stated assumption.

**Detail 14. Report topic-sentence outline and validation before any drafting.**
Inputs: signed Step 13 suite, Document Structure, structure.md.
Work: the Engineer drafts paragraph-level topic sentences, each with an ID (P2.3) and a `covers:` list of test IDs. Validation (A.4 precondition, run before Step 15 opens), recorded in `report_outline_validation.md`:
1. Scripted coverage matrix: every section test covered by a paragraph; every whole-document test covered or marked post-draft only; every paragraph covers a test or is marked connective with a reason. Orphans either way fail.
2. Any topic sentence with a number cites its fact test ID and carries the same source status.
3. Read-through: topic sentences alone given to a fresh-context reader with the 8 cold-read questions; at least 7 of 8.
4. Architecture: where each abbreviation is first introduced; the body claim for each planned figure.
5. Each limitation in the Document Structure table appears at its stated section.
Controls: zero control (the full matrix reads no orphans); known-bad (delete one paragraph and a test shows orphaned; plant a paragraph with no test and it shows as orphan).
Outputs: `report_outline.md`, `report_outline_validation.md`. Gate: Software Engineer signs; the Manager verifies both files exist before opening Step 15.

**Detail 15 to 19. Report path (remaining document steps).**
- 15: Engineer writes reporting copy from Step 10 and Step 11 evidence, loading reporting-copy.md only. Output: `report_reporting_copy.md`.
- 16: Writer composes from reporting copy plus outline (structure.md, style.md; style-reference.md on demand). Output: `report_draft_writer.md`.
- 17: Editor removes AI tells and tightens (signs_of_ai_writing.md). Output: `report_draft_editor.md`.
- 18: Wave 2: Designer (communication, echo-site audit), Fact-Checker (every cutter dimension and requirement against SBIR and model sources; source gate), Systems Engineer (interfaces, load path, limits). Outputs: `research/quinn/cr_scratch/step18_designer.md`, `step18_factcheck.md`, `step18_systems.md`.
- 19: revise; build DOCX (claude-docx-bundle house style) and PDF; run the suite; echo audit against the registry; final cold read. Outputs: `CoreCutterTestJig_Report.docx`, `.pdf`.

---

## CAD Test Specification

Every test is automated unless marked manual. (d) means parametrized over the family list in `params.collets.diameters`. Thresholds named `params.*` come from `params.yaml`; PROPOSED values are seeds to be confirmed or replaced at Step 3. "Control" means the zero control and known-bad control required by Principle 9. Size: about 45 test functions; case count follows the family size (4 or 7). Predicates are computed from final shapes (faces, fitted axes, helix probes), never from the placement or parameter used to build them (Rule M); every sign test first passes the self-check that p + eps*n is outside the solid and p - eps*n inside.

**Group P: params, BOM, contract**

| ID | Test | Pass criterion | Evidence |
|---|---|---|---|
| P1 | `validate_params()` | Accepts the seed; rejects known-bad: collet d below 90 or above 105, negative clearance, nut OD above bed minus margin, a thread major smaller than the largest collet bore plus walls | pytest result |
| P2 | Source keys | Every externally sourced number has `source:` and `status:`; UNVERIFIED count reported and matches the register | Count printed |
| P3 | Stock allocation | Per stock length, summed cut lengths <= on-hand quantity x length; extra cuts only in the extra-cut table; 1540 mm lengths unused unless the human directs otherwise | `bom_stock_allocation.md` parsed |
| P4 | Hardware rules | T-nuts are M6 spring-ball roll-in only; every bracket is a SKU or full-size 30-series class, no "mini" | grep; control: planted "mini bracket" fires |
| P5 | Frame profile | Each member bbox 60 x 60 mm within 0.05 mm; length equals cut list | result JSON |
| P6 | Interface control table | ICD exists in params with datums A, B, C, mounting pattern, coaxiality budget, keep-out envelope, stop height and rating, footprint and tip-over statement, cable exit; no empty field | params parse |
| P7 | Assumption labels | Every UNVERIFIED value read by any test appears in a report-assumptions list with its label | list match |

**Group C: collet family (d)**

| ID | Test | Pass criterion |
|---|---|---|
| C1 | Validity | Single solid; isValid; isClosed |
| C2 | Volume | Whole-part volume within 0.95 to 1.05 of the analytic volume (Loftsman frustum shell minus bore, slits, relief holes); each cut removes volume within 3 % of its analytic expectation and 0 < removed <= tool volume (7.1). Per-cut checks carry the discrimination, since slits are about 5 % of volume at d = 105 |
| C3 | Bore diameter | Probe along three azimuths offset from slit centres (phi_0 + 180/N + 120k degrees); reject any probe that returns a slit hit; mean bore equals `bore_free(d)` = d + tau + c_i within 0.02 mm (model check; print error is bounded in Step 8). Control: probes at 0, 120, 240 degrees on a 12-slit part fire |
| C4 | Family invariants | For every pair d, d': volume of common(X_d, X_d') equals volume of each within 0.01 mm3, where X is the solid of revolution of the outer profile with the bore filled; the symmetric difference of any two collets lies inside the larger bore annulus; taper, large and small OD, seat height identical within 0.02 mm |
| C5 | Slits | Alternating slits (top and bottom, relief holes at ends); count equals params; slit planes contain the Z axis within 0.01 mm; width within 0.05 mm of the law w_s = pi x Delta / N + w_min; a ray across a slit meets void for the slit depth and solid below |
| C6 | Minimum wall | Minimum wall at the cone top at least `params.print.min_wall` (PROPOSED 1.2 mm, 3 perimeters at 0.4 mm); runs for every d |
| C7 | Topology | Faces per edge all 2 except cylinder seams; component count 1; Euler characteristic equals the expected value for the alternating-slit collet (genus 1 per Topologist table); no leftover planar face on a slit plane; min face area and edge length recorded |
| C8 | Family coverage | For every core diameter 90 to 105 mm in 1 mm steps, widened by `params.core.tol` (default +/-1 mm, UNVERIFIED), some collet's accept range (derived from Delta = s + c_i, not asserted) contains it. Known-bad: remove a mid collet and the test fires |
| C9 | Closure arithmetic and stiffness | Per-slit closure pi x Delta / N is less than slit width minus `params.collet.min_slit_clamped` (PROPOSED 0.5 mm); web strain (screening model, allowable UNVERIFIED) below allowable; wall at d = 90 and d = 105 and the resulting stiffness ratio recorded (the extremes bound the family by wall and stiffness) |

**Group T: thread, engagement, clamp range**

| ID | Test | Pass criterion |
|---|---|---|
| T1a | Chirality probe | Ridge centreline sampled at theta = 0 and 90 degrees at fixed rho: (z90 - z0) mod L = +L/4 on boss and on nut. Known-bad: a mirrored nut fires. Hand is a constant in `common.py`, not a params field; both parts call one helix function |
| T1b | Screw-motion mesh | Nut moved by the screw motion Rz(phi) T(0,0,L phi/2pi) for phi in {15, 90, 180, 360} degrees: common volume with boss <= 0.01 mm3. Opposite-hand motion at 90 degrees and pure rotation must show large common volume (fires) |
| T1c | Direction | A clockwise turn from K lowers the nut (dz < 0) |
| T1d | Export chirality | T1a repeated on the exported STL and STEP (inside X1) |
| T2 | Thread dimensions | Major diameter equals the Step 3 chain output within 0.05 mm (not a constant); pitch = lead (single start); flank angle 45 degrees +/- 0.5; tooth depth and crest flat per params |
| T3 | Print clearance | Radial crest clearance c_r and axial flank gap g_a per side equal params within 0.05 mm and are at least the minimum (printer unconfirmed: UNVERIFIED until the coupon) |
| T4 | Thread engagement | In K at d = 90 and 105: engaged axial length >= `params.thread.min_engage` (PROPOSED 3 pitches); in R just before disengagement is possible also >= min_engage. Zero control: nut at the top with no overlap reads 0 |
| T5 | Clamp range at the extremes | For d_min and d_max build R and K from one pose. R: free bore >= d + tau + c_i, a core of d + tau slides in with zero interference. K: nut hand-tight, slit width above `min_slit_clamped`, engagement per T4, nut has at least 1 pitch of travel left (S12), holder flange gap to receiver rim above zero. Pass: all four poses. The extremes are the right tests because wall thickness and stiffness vary most there; stack height at cone contact is independent of d (C4), so it is not the reason |
| T6 | Nut OD and bed | Nut bbox (body and wing span) fits bed minus 5 mm in some orientation, or the split design's parts do (bed 256 mm, UNVERIFIED printer) |
| T7 | Holding torque (analytic) | T_hold(d, F_hand) >= SF x T_load for d_min and d_max, using the Loftsman model (mu values UNVERIFIED, labelled), with F_hand from stated wing arm and thrust-washer coefficient. T_load = 20 N m and SF = 2 are provisional assumptions. Expected red until the Step 2 design response closes it; if it cannot close, escalate to a positive core lock. A passing result is a prediction under labelled assumptions, not proof; the physical hold test is the authority |
| T8 | Print overhang rule | No down-facing thread flank below 45 degrees from horizontal (sectional probe). Known-bad: a Tr 15 degree profile fires |
| T9 | Register and tilt | With the nut tilted by alpha_reg about a transverse axis at the register contact, ridges do not interfere (< 0.01 mm3); tilted by 2 x alpha_crit, the register interferes before any thread does (known-bad control must fire). Register geometry from Step 3 |

**Group F: fit and function**

| ID | Test | Pass criterion |
|---|---|---|
| F1 (d) | Collet seat fit | R: radial gap between collet cone and holder cone within `params.print.seat_clearance` +/- 0.05 mm everywhere. K: the clamped collet solid (bore = core diameter, slit narrowed by pi x (B_f - d_c)/N, outer cone reduced, placed at holder-relative axial offset s_z) is in contact with the holder cone: common volume < 0.01 mm3 (offset 1e-3 mm radially for OCC) and contact area above `params.seat.min_contact_area` |
| F2 (d) | Core in collet | A core cylinder of nominal d slides into the R-pose bore with common volume < 0.01 mm3; its base lands on the core stop (axial gap 0 +/- 0.05 mm) |
| F3 | Collet and core sweep | N x N: each core diameter against each collet, in R pose. The matching cell passes; cores larger than the free bore are rejected by interference (must fire); cores below the clamp range show slit bottoming or no contact (must fire). Diagonal passes, off-diagonal rejected as the accept range predicts |
| F4 | Exposed core | Core top above the nut top (the highest fixture inside the cutter footprint) by at least `params.core.min_exposed` = standoff + g_stop + margin. Standoff = 106.369 mm is head tip to kerf sphere centre of the 7 in model, not the pinch plane; applicability to the 6 in drill UNVERIFIED. Test asserts the stated assumption |
| F5 | Genus and feature presence | Per part: genus equals the declared through-hole count; each feature in the Step 6 checklist exists in the result JSON with nonzero feature volume; flipped copy of each part distinguishable by its signed feature (Rule P). On the empty baseline every one fails |
| F6 | Hard-stop gap | Holder flange to receiver rim gap in K equals z0 + s_z + margin (about 6 mm seed); holder never bottoms in R or K (S6) |

**Group A: assembly** (relations are data in ASSEMBLY.md; poses R and K for each collet)

| ID | Test | Pass criterion |
|---|---|---|
| A1 | Contact-class matrix | Parts: base with receiver, holder, collet, wing nut, core stand-in, frame members, brackets and T-nuts, cutter envelope. Every pair has a class in ASSEMBLY.md; an unlisted pair fails. C (contact required): min distance 0 +/- 0.01, patch area above floor, overlap < 0.01 mm3. G (gap): distance >= g_min stated per pair, contact area 0. F (free): overlap 0. Required G pairs include base-holder, nut-collet, nut-core, nut-cutter. Controls: nut resting on collet top (overlap 0, G violated) fires; holder resting on receiver top fires; two parts 100 mm apart read F; 1 mm overlap fires every class |
| A2 | Cutter envelope | Keep-out is two solids: tube (rho 73.025 to 76.2 mm, tube ID/OD 146.05/152.4 mm from workorder, a stated assumption, not the cutter OD) swept the full stroke, and the cutting-face annulus (rho from core kerf radius to R_face, assumption R_face = 76.2 + 10 mm, UNVERIFIED) at its lowest point. Nothing between the core and 76.2 mm may lie in the swept volume. Derived flag `nut_exceeds_bore` is computed (true expected); the test asserts the gap g_stop between nut top (wing tops included) and the cutter lowest point at the metal stop height in the ICD. There is no `nut_is_stop` choice. Control: a ring placed in the face annulus path fires |
| A3 | Placement predicates | Predicates S1 to S16 from the Topologist table, computed from faces and fitted axes: coaxial incl. tilt (norm(a x Z) <= 1e-4); boss rises from base; collet foot on seat with antiparallel normals; collet inside holder cavity; cone narrows with z on both with half-angles equal within 0.02 degrees; holder never bottoms; radial gap in R and contact in K; core inside bore; core on its stop and off the tray; nut clamp face bears on holder flange face (antiparallel normals, z gap 0 to 0.05 in K, travel > 0 in R); nut clear of collet and core by >= 1.0 mm; >= 1 pitch of nut travel left; engagement per T4; core exposed per F4; stroke inequality s = d_rho / tan(alpha) with thread length >= s + min_engage + 1 pitch; release by cone angle above atan(mu_max) or captured flange. Frame: plate on frame z-gap 0 +/- 0.05; bracket mate faces antiparallel with body in the profile's outward half-space; T-nut centroid inside the slot cavity |
| A4 | Product tree | Component count and names equal the expected list; expected visible count computed from object counts |
| A5 | Visual (manual) | Four-view PNG set judged by an image-capable reviewer against a rubric with an item per signed feature, signifier (arrow, witness line, caddy) and pinch point |
| A6 | Wrong-state controls | WS1 collet upside down; WS2 holder upside down; WS3 nut upside down; WS4 wrong-hand thread; WS5 cross-threaded tilt; WS6 wrong collet for core; WS7 collet unseated; WS8 holder bottomed; WS9 nut bottomed on base; WS10 base on frame upside down; WS11 slit over key. Each planted state fires at least one of A1, A3, T1, T9, F1, F3. For WS1 to WS3 and WS6 the defence is also a physical feature (foot key, flange OD above receiver bore, one-ended thread, engraved window), verified at Step 9 |

**Group E: export validity**

| ID | Test | Pass criterion |
|---|---|---|
| E1 | STEP | For each printable part and the assembly: file exists with mtime after run start; size > 0; re-import gives expected solid count; summed volume within 0.5 % of FCStd; unit mm; product tree names equal part names |
| E2 | STL | Watertight; no degenerate triangle; signed volume positive and within 1 % of FCStd; bbox within bed minus 5 mm; units mm; tessellation linear deflection stored in the result JSON and <= c_r / 10 (0.035 mm seed) with angular deflection <= 2 degrees. Controls: unit cube passes; STL with one triangle removed fires |
| E3 | FCStd opens | Reopened FCStd: visible deliverable object count equals count computed from object counts; every deliverable named |

**Group B and X: build and independent re-measure**

| ID | Test | Pass criterion |
|---|---|---|
| B1 | Rebuild | Running the part scripts twice yields volumes equal within 1e-6 relative |
| X1 | Independent re-measure | Script sharing no code with build or tests, reads exported STEP and STL only; recomputes per-collet volume, the interference matrix, and thread chirality sign (T1d); each agrees with the build-side JSON within the C2, A1, E2 tolerances. Negative controls: probes away from the feature still hit; a deliberately wrong expected value fires; a mirrored nut export fires. Bore diameter and bed fit are not recomputed (covered by C3, E2) |

Ceremony kept out: color-assignment tests, diffability test, per-part geometry-math test file, overhang-angle slicer script (T8 is a sectional probe instead), SHA-1 manifest as a test, before-and-after write hashing, slot-level 30-6060 fidelity, empty report test stubs, separate printability report, turntable MP4.

---

## Source Verification Register

Rule (A.10 item 2, tdd_method principle 7): a test that cites the SBIR plan, a Mines document or the rigged model carries a status. VERIFIED means the Fact-Checker re-read the primary file at the cited lines in the Step 0 review. TRACED means the extraction file gives the location only. The Fact-Checker re-verifies at the Step 4 gate (CAD tests), the Step 13 gate (report tests), and Step 18. The orchestrator resolves UNVERIFIED rows; the human resolves rows only the human or Mines can answer.

| Claim used by a test | Tests | Status | Trace | Who verifies or unblocks |
|---|---|---|---|---|
| Core nominal 100 mm: Phase I EDU test cores, "pre-cast to 100 mm to match the iris aperture" | P2, C8, WD, S-sections | VERIFIED with conflict | INSITU2_text.md 406-407; Figure 2 caption 186-188 says full-scale core diameter "is above 100 mm"; csm_sow.md 56 gives no number | Report states both; Fact-Checker |
| Core range 90 to 105 mm; tubing 6.00 / 5.75 in, 1/8 in wall | P1, C-group, A2 | CONTRACT (workorder.md is the only source); arithmetic 152.40 / 146.05 mm, wall 3.175 mm recomputed | workorder.md | none |
| 152.4 mm as the cutter OD | A2, F4 | UNVERIFIED. 152.4 mm is the tubing OD only. The only sourced cutter diameter is 7.00 in = 177.80 mm (7 in generation, borebot_operating_envelope.md 29) | Fact-Checker F-3 | Keep-out uses 152.4 / 146.05 as a stated assumption |
| Iris closed by drill drivetrain, no jig actuator; release by reversing braking torque; Hall about 400 to about 45 counts | scope honesty, acceptance spec | VERIFIED | INSITU2_text.md 157-166 | none |
| Iris 4 leaves; pivots; closure -62 deg; leaf thickness 3.175 mm; face radii 71.4375 and 74.6125 mm | App A | VERIFIED, 7 in model only | double_dong_params.py 93-98, 360-368, 402-404 (leaf thickness is 402-404, not 410-411) | none |
| 106.369 mm | F4, App A | VERIFIED as a number; its label is corrected: head tip to kerf sphere centre, not the pinch plane. Dome pole sits 106.369 - 71.4375 = 34.9315 mm behind the face. Core is pinched off inside the head. 7 in model only; applicability to the 6 in drill UNVERIFIED | double_dong_params.py 372-380 | Engineer or human measures the 6 in iris |
| Iris open aperture 54.2925 mm | E-8, family range | UNVERIFIED: unit (radius or diameter) not stated, and not the 6 in design | double_dong_params.py line 92 | Human (B1) |
| WOB 100 to 1000 N | loads | VERIFIED as a Phase I test range; 1000 N as jig load is a design choice | INSITU3_text.md 424-430 | label "design choice" |
| Penetration 5 mm/min at WOB 100 N or more | acceptance spec | VERIFIED | INSITU3_text.md 267-268 | none |
| Spin 1 to 60 rpm | scoping | VERIFIED as text; UNVERIFIED as cutter spin. It is the Borebot motor and brake operating range | summary_yokeless_motor.md 158, 200; ip_and_competitive_position.md 59 | Source for drill spin needed |
| Core length 500 mm | params | VERIFIED as Quinn's DECLARED value (not a Mines value) | double_dong_params.py 357-359 | Human asks Mines |
| Core mass 9.4 kg at 2400 kg/m3 | S1 load case | DERIVED upper bound; density UNVERIFIED | extraction C7 | Mines property data |
| Core diameter tolerance +/-1 mm | C8, T5, F3 | UNVERIFIED (confirmed: no tolerance in the cited ranges) | none | Human asks Mines |
| Torque 20 N m (jig) and 50 N m (iris) | T7, loads | UNVERIFIED (confirmed: INSITU2 408-411 describes a measurement to be taken) | none | Phase I measurement; stated as assumption |
| Core count (12 plain + 12 layered vs 40/15/30) | report | Sources disagree: INSITU2 514-518 and csm_sow 56, 58 vs csm_package.md 56 ("15" is depth-series captures) | | Human, or cut the sentence |
| "Mines specifies/requires/delivers" any core dimension | any | UNVERIFIED. The Mines zip PDFs were not read in this review (pdftoppm is not installed); the claim rests on the Engineer's text read only | | Install poppler (pdftoppm) or human reads; tests assert SBIR text only |
| Mines Dreyer low-density concrete; properties strength, fracture toughness, density, grain size | S-sections | VERIFIED | csm_sow.md 24, 27, 56, 61 | none |
| Ascent test 600 s at 1x, 1.5x, 2x | any | NOT CHECKED (INSITU2 444-461) | | Fact-Checker at Step 4 |
| Docx holds no geometry; gameplan.md line 141 model-of-record; FCStd not on this machine | | NOT CHECKED / PARTLY VERIFIED | | Fact-Checker |
| Model is the 7 in generation (bore 177.8, core 100, annulus 38.9 mm) | App A | VERIFIED | double_dong_params.py 354-356 | none |
| 6 in iris data; which 2026-09-11 STEP is the 6 in drill | any | UNVERIFIED | extraction section 7 | Human (B1) |
| 30-6060: 60 x 60 mm, 30 mm pitch, M6 spring-ball T-nut | P3 to P5 | DECLARED by human; catalog pending, not verified in review | step0_human_stock_80-20.md | Engineer pulls catalog at Step 1; Fact-Checker confirms |
| Stock lengths and quantities | P3 | DECLARED by human | same | Human at Step 11 |
| Printer bed 256 mm, PETG/PLA, 0.4 mm nozzle | T3, T6, E2, C6 | UNVERIFIED (no printer named) | Manager default | Human (B2) |
| PETG friction mu_k about 0.35, mu_c 0.4, mu_t 0.25, bearing 0.25, in-layer tensile about 45 MPa, web strain allowable 0.01 | T7, C9 | UNVERIFIED seeds | Loftsman review | Step 8 coupons, Step 11 hold test |

Any UNVERIFIED test is either rewritten as "stated assumption, labelled as such" (the test checks the label is present) or dropped. The report may not state an UNVERIFIED value as fact.

---

## Context Recipes

| Step | Agent | Files / Excerpts |
|------|-------|-----------------|
| 0 | The Manager | workorder.md, this gameplan, method/operational_guide.md (A.4, A.6, A.12) |
| 0 | The Engineer | workorder.md, templates/gameplan.md, extraction file, stock file, five Step 0 reviews, llm_plm_cad.md, tdd_method.md |
| 1 | The Engineer | workorder.md, gameplan, llm_plm_cad.md, freecad_api_reference.md, extraction file, stock file, Fact-Checker review |
| 1 | The Fact-Checker | extraction file (patched), source files at corrected line numbers, Source Verification Register |
| 1 | The Designer | params.yaml seed, workorder.md, gameplan Design Notes (no scripts) |
| 2 | The Systems Engineer | workorder.md, gameplan, Systems Engineer and Designer reviews, extraction sections 2 to 6, params.yaml seed |
| 2 | The Loftsman, The Topologist | step2 draft, their own reviews, params.yaml |
| 3 | The Loftsman | step2 concept, params.yaml, extraction sections 2 and 3, freecad_api_reference.md (thread, helix) |
| 3 | The Topologist | step2 concept, params.yaml, llm_plm_cad.md 7.1, 7.4, 7.5, 11, Loftsman output |
| 3 | The Designer | params.yaml, step3 crossreview, Designer review (no scripts) |
| 4 | The Software Engineer | gameplan (CAD Test Specification, Register), params.yaml, ASSEMBLY.md, tdd_method.md, llm_plm_cad.md sections 7 and 10 |
| 4 | The Fact-Checker | Register, tests asserting numbers, extraction file, context/literature/, source documents |
| 5 | The Engineer | params.yaml, common.py, step3 output, tests/test_collet_family.py |
| 5 | The Software Engineer | collet_family.py, tests, params.yaml |
| 6 | The Engineer | params.yaml, common.py, collet_family.py, step3 output, ASSEMBLY.md |
| 6 | The Loftsman, The Topologist | part scripts, FCStds, result JSON, step3 output |
| 6 | The Designer | params.yaml, renders (image-capable reviewer), step6 findings, completeness checklist (no scripts) |
| 7 | The Engineer, The Software Engineer | assemble.py, tests/test_assembly.py, test_thread_clamp.py, ASSEMBLY.md, interference report |
| 7 | The Systems Engineer | ASSEMBLY.md, interference report, step2 concept, extraction sections 3 to 5 |
| 8 | The Engineer, The Loftsman | part scripts, step3 output, printer constraints (Design Notes 9), Loftsman 5.1 model |
| 9 | The Engineer, Loftsman, Topologist | step6 findings, step7 and 8 reports, part scripts |
| 9 | The Designer | step6 critique, renders of production parts (image-capable reviewer), production checklist |
| 10 | The Engineer | all of the above, SHA-1 manifest |
| 10 | The Software Engineer | build_parts/, tests/, results JSON, remeasure script |
| 10 | The Topologist, The Systems Engineer | assembly FCStd/STEP, ASSEMBLY.md, interference report |
| 11 | The Manager, The Designer, The Systems Engineer | step8 predicted-values sheet, ICD, print-review form, hold-test protocol |
| 12 | The Manager, The Systems Engineer | step10 and step11 outputs, extraction file, workorder.md, ICD |
| 13 | The Software Engineer | workorder.md, gameplan Document Structure, extraction file, tdd_method.md, operational_guide A.10, Register, hold-test record |
| 13 | The Fact-Checker | test suite, source documents, context/literature/ |
| 14 | The Software Engineer, The Engineer | test suite, Document Structure, structure.md |
| 15 | The Engineer | reporting-copy.md (full), Step 8, 10, 11 results with sources, report_outline.md, report_outline_validation.md |
| 16 | The Writer | structure.md, style.md (full), style-reference.md (on demand), reporting copy, outline |
| 17 | The Editor | signs_of_ai_writing.md (full), Writer draft, suite AI-writing criteria |
| 18 | The Designer | diff since Step 17, full report, echo registry, cold-read results |
| 18 | The Fact-Checker | full report plaintext, source documents, context/literature/, echo registry, Register |
| 18 | The Systems Engineer | report, ASSEMBLY.md, Step 10 and 11 outputs |
| 19 | The Engineer | edited draft, review outputs, claude-docx-bundle |
| 19 | The Software Engineer | final PDF text, report_test_suite.md, checker scripts |
| 20 | The Manager | gameplan, all step outputs |

---

## Progress Log

| Step | Date | Notes |
|------|------|-------|
| 0 | 2026-11-08 | Opened. Work order locked as workorder.md. Engineer extraction and draft written. Human stock input (30-6060, M6 spring-ball roll-in T-nuts, full-size brackets) folded in. Software Engineer revision: CAD Test Specification, Source Verification Register, report suite and outline validation added. |
| 0 | 2026-11-08 | Five reviews received (Systems Engineer, Loftsman, Topologist, Fact-Checker, Designer). Engineer final revision: every finding dispositioned (table at end); conflicts ruled (Design Notes 1 to 6). Step renumbering from the prior draft: old 1 now Steps 1 and 4 (split around the concept and geometry steps); old 2 now 3; old 3 now 5; old 4 now 6; old 5 now 7; old 6 now 8; old 7 now 9; old 8 now 10; old 9 now 11 (hold test added); old 10 now 12; old 11 to 18 now 13 to 20. Cut from the prior draft: report test stubs, `test_jig.py`, `test_geometry_math.py`, turntable MP4, overhang slicer script, color and diffability tests, write-hashing, slot-level profile fidelity, separate printability report, SHA-1 as a test. Reinstated: wing-nut moment-arm check (now T7). |

---

## Design Notes

**1. Sequence ruling: Software Engineer vs Systems Engineer (rigor vs coherence).**

| Position | Source | Argument |
|---|---|---|
| Write the whole CAD suite first with `pending: step2` thresholds; a stack reversal "changes data, not tests" | Software Engineer | Contract in code before geometry; tests stay stable |
| Do not write F1, T5, A3 before the force loop, release and slit design are fixed; split Step 1 | Systems Engineer S2, S8; Designer G-2; Topologist TP-10 | Loop topology changes which contacts exist; the claim is false for containment direction and signs |

Ruling: split. Foundation (1), concept (2), geometry numbers (3), suite (4). The Software Engineer's data-driven mechanism is kept: the pair table, poses and signed features live in ASSEMBLY.md and tests iterate over them, so a contact-class change is a data change. A change of loop topology is not, and is settled before the suite exists. Reason: a red-first suite is only informative if it is red for the right reasons.

**2. Hard stop ruling: wing nut as stop vs stop on the frame.**

| Position | Source |
|---|---|
| Nut OD (about 150 to 181 mm) exceeds the 146.05 mm bore, so the nut is the stop by geometry; `nut_is_stop` is derived, not chosen | Topologist E-6; Loftsman 7.3 |
| A 1000 N descent load through a printed nut and thread is the weakest path; put the stop in metal on the 30-6060 frame, nut strictly below it | Systems Engineer S5 |
| The nut is both what the operator tightens and what the cutter crashes into; one failure drops clamp and stop. The stop belongs to the descent assembly (carriage stop on the columns). A frame post outside the nut is never touched by the tube, so a frame stop must be on the drill side or inside the nut radius | Designer D2 |
| Software Engineer draft: Engineer chooses branch via `params.nut_is_stop` | Draft A2 |

Ruling: the printed nut is not a stop and carries no descent load. The stop is metal, rated, defined in the ICD (height, rated load, owner), and built at Step 12 as a carriage stop on the columns or an inside-radius ring, whichever Step 12 selects. Until it exists, A2 asserts the gap g_stop between nut top (wing tops included) and the cutter lowest point at the ICD stop height, and F4 measures from the nut top. `nut_is_stop` is deleted; `nut_exceeds_bore` is a derived value (expected true). A documented fallback of the nut as stop is permitted only with a rated load and the human's approval. Reason: the Designer's separation of jobs plus the Systems Engineer's load-path argument agree on the outcome; the Topologist and Loftsman findings are kept as the derived flag and the keep-out geometry.

**3. Mechanism rulings.**

Stack (Topologist 3.1, Loftsman 3 agree; Systems Engineer S2 supplies the loop). The workorder's "threaded boss" is a tubular receiver: nesting from the axis outward is core, collet bore, collet wall, holder cavity, holder wall, receiver bore, receiver wall and thread, nut. The collet stands on a floor land inside the receiver (the receiver seats the collet, as the workorder says); the holder cone descends over the collet; the nut on the receiver bears on the holder flange; the holder flange sits above the receiver rim with a gap (the stroke). The loop is written as a sentence in ASSEMBLY.md. The holder never bottoms on the receiver or base. The core axis is located by cone and pilot, never by the trapezoidal thread.

Thread size: Tr 60 x 8 is withdrawn. A 60 mm major is smaller than the 90 to 105 mm cores it surrounds (Loftsman G1, Topologist TP-1). The major diameter is an output of the radial chain:
D_T = B_f(d_max) + 2 t_c + 2 H tan(alpha) + 2 (t_h + t_b + 0.5 + h)
with seeds t_c = 5, H = 30, t_h = 5, t_b = 5, h = 2.5 mm, B_f(105) = 107 mm.

| Position | Value | Basis |
|---|---|---|
| Loftsman | about 165 mm major, nut body about 181 mm, wing span about 230 mm | alpha = 20 degrees (releasing cone) |
| Topologist | about 135 mm major, nut OD at least 150 mm | smaller cone angle and thinner walls |

Ruling: the two differ by assumptions (cone angle, walls), not by method. The formula governs, no single number is carried in the registry until Step 3, and the reviewers' range 135 to 165 mm bounds the seed. Pitch 8 mm and symmetric 45/45 flanks (Loftsman G2, prints with no flank under 45 degrees) are PROPOSED seeds.

Release: a cone half-angle below atan(mu_k) self-locks and backing off the nut does not free the collet (Loftsman 3.1, Topologist S16, Systems Engineer S2, Designer D6 agree).

| Position | Source | Trade |
|---|---|---|
| Releasing cone, alpha = atan(mu_k) + 2.5 degrees (seed 20 degrees) | Loftsman (recommended first) | No extra bearing faces; radial budget grows (165 vs 158 mm); holding torque per axial force falls about 28 % |
| Captured-flange nut with a shallow cone (about 10 degrees) | Designer D6 (better trade); Loftsman (alternative); Systems Engineer (choose) | Keeps mechanical advantage and gives positive release; adds two bearing faces to print |

Ruling: holding torque is the binding performance risk (D1), so the primary design is the captured-flange nut with the shallow cone; the releasing cone is the fallback if the captured nut fails the Step 8 coupon. Step 3 carries both parameter sets, the coupon (tilt-plane mu_k) decides the fallback, and two M6 jacking holes on the holder flange are required either way. Reason: a design that cannot hold is a failed test; a design that costs two print faces is only a cost.

Collet topology: C1 (single solid) and C5 (slit through full wall height) conflict (Topologist TP-6). Loftsman prescribes alternating slits (ER style); the Topologist's table accepts alternating (one component, genus 1) or finger collets. Ruling: alternating slits with relief holes, because web bending then stays in the layer plane while axial fingers bend across layers, the weak FDM direction. Slit count is a family parameter set by the hinge-strain law; the Topologist's S22 and S23 predicates apply to it.

Register length: the Topologist's cross-thread pilot at a 135 to 165 mm thread needs about 54 mm or more; the Designer proposes a stacked register using features that already exist (holder flange centred on the cone, holder in the receiver bore). Ruling: Step 3 decides by number; T9 tests whichever is chosen; the stacked register is the first candidate.

Clamped-state solid (Loftsman 5.2): F1's K pose uses a second collet solid from the same generator call (bore = core diameter, narrowed slit, reduced cone, offset s_z). This removes the rigid-body overlap that A1 would flag and is compatible with the Topologist's contact class C. OCC offset strategy for coincident cone faces: the Topologist confirms at Step 3.

**4. Frame and measurement rules (for ASSEMBLY.md).** Right-handed, +Z up; origin on the top face of the base plate on the receiver axis; +X to the front; theta counter-clockwise from +X seen from +Z. Poses R (nut backed off, collet free) and K (nut hand-tight). Rule M: every predicate is computed from the final shape. Rule P: each part has one signed asymmetric feature. Relations are data. Slit phase is a fixed function of key angle.

**5. Interface control table (Step 2 deliverable, skeleton).**

| Item | Content |
|---|---|
| Datum A | Frame top plane (base plate underside, z = 0) |
| Datum B | Receiver axis, +Z, the one alignment axis |
| Datum C | A frame slot line fixing rotation about Z |
| Mounting pattern | T-slot lines on the frame top face (30 mm pitch, M6 roll-in T-nuts) available to the column, with the ones the base plate occupies |
| Coaxiality | Drill centreline to receiver axis within the Step 2 budget; slotted base-plate holes plus one printed alignment gauge that seats on the holder and centres a 152.4 mm tube |
| Keep-out | Cylinder of radius 76.2 mm plus margin about the axis from nut top to stroke end, plus the face annulus (R_face UNVERIFIED) |
| Stop | Metal, height H_stop, rated load, owner (Step 12) |
| Footprint | Stated minimum footprint, four adjustable feet or bolt-down slots, mass target, tip-over statement for a 1540 mm column, even if the number is final at Step 12 |
| Core handling | Steady rest or cradle and lift strap point on the frame |
| Cable exit and debris path | From the back cap; dust skirt on the nut and a closed top on the receiver thread region |

**6. Report test count ruling: 130 vs about 60.**

| Position | Source | Argument |
|---|---|---|
| About 130 tests (12 per page) | Software Engineer | A.10 item 7 calls a multi-section technical review 150 to 200 tests; rigor |
| About 60 tests and two cold reads; seven of 20 steps on the report is more checking than 8 to 12 pages carry; 40 manual tests; the 12-per-page ratio is an assertion | Systems Engineer S9, S10; Designer notes the cost without judging |

Ruling: about 90 (91 in the Detail 13 table). The count is set by claims, not by pages: the report now has an analysis section and a hold-test section that each carry fact tests, so 60 would leave claims untested, while 130 duplicated section tests with whole-document tests. Reductions: manual tests cut from about 40 to about 27 (whole-document manual 17, section manual-only 10), comprehension tests cut to 5, cold reads cut from three to two (outline, final PDF). The Manager ratifies and records the deviation from A.10 item 7. If the human widens the report to the upper assembly, re-size to 150 or more.

**7. Stock and 80/20 hardware (human input, DECLARED).**
- Profile: 80/20 30-6060, 60 x 60 mm, 30 mm slot pitch. No smaller profile. Fasteners M6.
- T-nuts: M6 spring-ball roll-in only.
- Brackets: ordered catalog brackets must be full size for the 30-series, never "mini"; printed or fabricated brackets may be designed. BOM names the SKU or full-size class; Step 1 pulls SKUs from the 80/20 catalog.
- Stock on hand, mm x quantity: 1540 x 4, 980 x 4, 952 x 1, 728 x 2, 644 x 2, 488 x 2, 468 x 2 (15,688 mm total). Believed uncut; shared with other projects. Design from stock first. Extra cuts allowed (about $2.20 per cut, DECLARED) and listed separately.
- Starting allocation to test in Step 1: base frame from shorter stock (644 x 2, 468 x 2, 488 x 2); 1540 mm lengths reserved for columns at Step 12; `bom_stock_allocation.md` records consumption for other projects (test P3).
- The footprint is stock-driven, not load-driven; the ICD must state the tip-over case (Designer D8, Systems Engineer S6). "Design load rating" is renamed "design loads (assumed)": axial 1000 N is a design choice bounded by the SBIR test range, torque 20 N m is a placeholder.

**8. Extraction facts, corrected (Fact-Checker review; patch the extraction file at Step 1).**
- 106.369 mm is the distance from the head tip (z -789.1834) to the kerf sphere centre (z -682.8144) in the 7 in model, not the pinch offset. The dome pole sits 106.369 - 71.4375 = 34.9315 mm behind the cutting face. The core is pinched off inside the head. Source lines 372-380. The Fact-Checker's own arithmetic (not in the source) puts the sphere meeting a 50 mm radius core about 55 mm behind the face. F4's number is a labelled assumption for the 6 in drill.
- 1 to 60 rpm is the Borebot motor and brake operating range (summary_yokeless_motor.md 158, 200; ip_and_competitive_position.md 59), not the cutter spin.
- The 152.4 mm figure is the tubing OD from the workorder, not a cutter OD; the only sourced cutter diameter is 7.00 in = 177.80 mm (7 in generation).
- Core 100 mm applies to Phase I EDU test cores (INSITU2 406-407); INSITU2 186-188 says the full-scale core diameter "is above 100 mm". The 90 to 105 mm range is the workorder's alone.
- Leaf thickness is double_dong_params.py 402-404 and the source calls it the plate thickness (0.125 in exactly); face radii lines 366-368; standoff line 372.
- Core tolerance, 20 and 50 N m, iris open aperture, 6 in iris data: no source. Mines PDFs unread.

**9. Source findings that change the design.**
- The iris is closed by the drill's own drivetrain; the jig supplies no actuator. Jig duties: hold the core coaxial, resist the iris reaction (torque and lateral load at 106 mm or more above the holder), carry core weight, guard the cutter stroke. The cutter never touches a 90 to 105 mm core (146.05 mm bore leaves 28.025 to 20.525 mm radial gap per side); WOB reaches the stop path, not the holder.
- Binding alignment tolerance is core versus iris open aperture, not core versus tube. If 54.2925 mm is a radius, the 105 mm core has 1.79 mm per side (100 mm: 4.3 mm); if a diameter, no core in range fits. The tolerance budget (Step 2) lives inside this.
- Holding capacity: Loftsman 5.1 gives about 8.1 N m at d = 105 and 6.9 at d = 90 for 12 N m at the nut (about 250 N axial, F/T about 21 per metre at a 165 mm thread). Systems Engineer S1 gets about 240 N axial and about 10 N m by an independent route. Both are below the 20 N m placeholder; both use unsourced friction coefficients. A rotated core destroys stratigraphy order, so a slip is a failed test.
- Tilt before clamping: 1 mm radial clearance over a 30 mm grip gives 1.9 degrees (16.6 mm at the top of a 500 mm core); clamped, about 0.6 degrees (about 5 mm). A steady rest or cradle is a Step 2 decision, not left to the operator.
- Printing default: 256 mm class bed, PETG for jig parts, PLA for coupons, 0.4 mm nozzle, coarse thread, wings in-layer, threads axis vertical. Receiver (about 165 mm) and nut (about 181 mm, span about 230 mm against 251 mm usable) are large, slow, warp-prone: a Step 8 risk.
- Process rules: per-part scripts, one FCStd each (A.14); FCStd is authority once built (2.1); Boolean expected-delta and topology gate after each cut (7.1); builds over 30 s run in the background and PID, log path and expected finish are logged here (A.3.4); under FreeCAD 1.1.4 success is a sentinel line plus a fresh artifact, not exit code (A.15).

**10. Analytic vs empirical: Loftsman vs Engineer.**

| Position | Source |
|---|---|
| Derive thread, cone, slits, clearance and holding torque in closed form; specify numbers before any print | Loftsman |
| Test as you fly: the physical hold test is the evidence; closed-form results with unsourced friction coefficients are predictions | Engineer |

Ruling: both, in order. Closed-form results supply seeds and a prediction recorded before the print, labelled PREDICTED with their UNVERIFIED inputs; geometry (volumes, bore, thread form) is checked analytically because it has no unknown coefficient. Every friction, clearance and strain value is settled by the Step 8 coupons and the Step 11 hold test, which are the authority; a prediction that misses by a factor above 2 triggers a change order, not a rewrite of the prediction. Reason: the Loftsman math is right about shape and wrong to be taken as magnitude while mu is unmeasured.

**11. Other rulings.**
- Family spacing (Loftsman: 7 collets at 2.5 mm, N = 12; workorder reading: "separate collet per diameter"; Designer: 7 collets raise wrong-collet risk and print count; Software Engineer: 4). Ruling: default 7 collets at 2.5 mm pending B3, because with 5 mm spacing N = 20 slits and closure of 6 mm strain a printed web beyond a safe screening limit. The generator and all tests are family-list-driven; "2.5 mm is a params change" holds for geometry only. Grip windows replace nominal labels (operator measures the core and picks the window), with caddy, colour, rim notches and witness line.
- Stack height: Software Engineer (monotonic in d) vs Loftsman, Topologist, Systems Engineer (identical across d with a fixed outer cone). Ruling: independent of d; T5 uses the extremes for wall and stiffness.
- Re-measure scope: Software Engineer (full X1), Systems Engineer (volume and interference only), Topologist (add chirality on exports). Ruling: volume, interference and chirality; bore and bed fit dropped.
- F5: Systems Engineer (fold into topology gate), Topologist (genus), Designer (broad feature list). Ruling: kept as genus plus Designer checklist, run inside the topology gate.
- Pinch points and operator edges are function, treated at Step 9.

**Software Engineer review slots:** Step 4 (signs suite), Step 5 (generator), Step 7 (assembly tests), Step 10 (code and test review), Steps 13 and 14.
**Loftsman and Topologist cross-review slots (A.4):** Step 3 (before any build: L1 to L5), Step 6 (L1, L5, L6), Step 8 (L4), Step 9 (L6, L7), Step 10 (topology gate).
**Designer slots:** Step 1 (seed params), Step 3 (blocking params review), Step 6 (completeness and critique), Step 7 (A5), Step 9 (quality gate), Step 11 (print-review form), Step 14 (structure), Step 18 (Wave 2). Steps 6, 7 and 9 need an image-capable reviewer (A.3.1).

---

## Echo Site Registry

Each row: value, authoritative source, derived locations. Bold values on use. First-use rule: introduce with context at first use in each section. Authority rule (A.16): geometry values live in params.yaml until an FCStd exists, then the FCStd; report values match the authority, not each other.

| Value | Authoritative source | Derived locations |
|---|---|---|
| Core nominal diameter **100 mm** (Phase I EDU test cores; Figure 2 caption conflict noted) | INSITU2_text.md 406-407 (conflict 186-188) | report 1, 2, 5; collet file names; tests |
| Collet family: count and diameters (**4 at 5 mm or 7 at 2.5 mm, decided at Step 2 per B3**) | params.yaml `collets.diameters` | report 5; file names (`collet_092p5`); matrices; BOM; thesis; C8, F3, A1 |
| Collet grip window per collet; bore_free(d) = d + tau + c_i (seed **d + 2 mm**) | params.yaml | label engraving; caddy; report 5; C3, C8 |
| Core accepted range **90 to 105 mm** | workorder.md only | report 1, 5; generator bounds; C8 |
| Core tolerance **+/-1 mm** (UNVERIFIED) | params.yaml `core.tol` | C8, T5, F3; report 2 as stated assumption |
| Tubing **152.40 / 146.05 mm (6.00 / 5.75 in)**, wall 3.175 mm; format: mm first, inches in parentheses at first use. 152.4 mm is tubing OD, not cutter OD (cutter OD UNVERIFIED) | workorder.md; params.yaml `drill.*` | report 2, 3, 7; A2; keep-out solids |
| Radial gap, 100 mm core **23.025 mm** (90: 28.025; 95: 25.525; 105: 20.525) | derived | report 2; E-1 |
| Iris leaf count **4**; **106.369 mm = head tip to kerf sphere centre** (7 in model, not the pinch plane); dome pole **34.9315 mm** behind the face | double_dong_params.py 93-98, 372-380 | report App A; F4 |
| Iris open aperture **54.2925 mm, unit unresolved** (UNVERIFIED; 6 in iris unmeasured) | double_dong_params.py line 92 | report 1 (needs block), 2; family range; E-8 |
| Thread: right-hand, single start, symmetric 45/45; pitch **8 mm** (PROPOSED); major diameter = Step 3 output (reviewers' range 135 to 165 mm; no single number until Step 3). "Tr 60 x 8" withdrawn | params.yaml `thread.*` | receiver, nut, base scripts; T1 to T9; report 3, 6; coupon |
| Cone half-angle (Step 3; seeds about 10 degrees with captured nut, or 20 degrees releasing) | params.yaml `cone.alpha` | collet, holder; F1, S5, S16; report 3, 5 |
| Slit count N and width w_s (PROPOSED N = 12 at 2.5 mm spacing, 20 at 5 mm; w_s about 1.5 mm); min clamped slit **0.5 mm** (PROPOSED) | params.yaml `collet.slits` | C5, C9, T5; report 5 |
| Min thread engagement (PROPOSED **3 pitches**; 24 mm only at 8 mm pitch) | params.yaml `thread.min_engage` | T4; report 5 |
| Nut OD and wing span (Step 3; seeds **about 181 mm body, about 230 mm span**) | params.yaml `wingnut.*` | T6, A2; report 3, 6 |
| Hard stop: metal, owner and height in the ICD (Step 12); the printed nut is not a stop | ASSEMBLY.md ICD | A2, F4; report 2, 8 |
| Profile series **30-6060** (60 x 60 mm, M6 roll-in spring-ball T-nut) | step0_human_stock_80-20.md | frame scripts; BOM; P3 to P5; report 3, App B |
| Stock lengths and allocation | step0_human_stock_80-20.md; bom_stock_allocation.md | BOM, P3, report App B |
| Printer bed **256 x 256 x 256 mm** (UNVERIFIED); usable **bed minus 5 mm = 251 mm** | params.yaml `printer.bed` | T6, E2; report 6 |
| Design loads (assumed): axial **1000 N** (design choice bounded by WOB 100 to 1000 N test range); torque **20 N m** (placeholder, UNVERIFIED); iris **50 N m** (UNVERIFIED) | INSITU3 424-430; params.yaml `loads.*` | T7; report 2, 4 |
| Holding torque estimate **about 7 to 10 N m** at hand-tight (PREDICTED, UNVERIFIED inputs) | Step 8 sheet | T7; report 4, 7, page 1 |
| Spin **1 to 60 rpm** = Borebot motor and brake range, not cutter spin | summary_yokeless_motor.md 158, 200 | report 2; scoping |
| Core length **500 mm** (DECLARED by Quinn, not Mines); mass about **9.4 kg** (DERIVED) | double_dong_params.py 357-359 | report 2; H2 stand-in |
| Footprint, feet, tip-over statement | ASSEMBLY.md ICD (Step 2) | Step 12; report 2 |
| Report test count **about 90 (91)** | Detail 13 | Step 13 suite; Step 19 final run |
| Step and section numbering (this plan: Steps 0 to 20; report sections 1 to 8 plus Appendices A to C) | this gameplan | all documents |

---

## Open Questions

### Human-blocking (answers or accepted defaults needed at the Step 0 gate)

| ID | Question | Why it blocks | Proposed default |
|---|---|---|---|
| B1 | What is the iris open aperture of the 6 in drill (value and whether 54.2925 mm is a radius or a diameter), and which of the two 2026-09-11 STEP files is the 6 in drill? | If the aperture is a diameter near 54 mm or a 108.6 mm opening, a 105 mm core has 1.79 mm per side or none; the 90 to 105 range and every collet depend on it | Treat 54.2925 mm as a radius (open diameter 108.585 mm), mark UNVERIFIED, and have the Engineer measure the STEP at Step 1 if the human names the file; if the measured aperture rejects 105 mm, cut the range before Step 5 |
| B2 | Which printer (bed size, material, nozzle)? | Receiver (about 165 mm), nut (about 181 mm, span about 230 mm) and plate size depend on a 256 mm bed | 256 mm class, PETG for parts, PLA for coupons, 0.4 mm nozzle; split nut if the bed is smaller |
| B3 | Collet family: 7 collets at 2.5 mm (needed for continuous coverage with a +/-1 mm tolerance) or 4 collets at 5 mm (literal "a separate collet per diameter")? | Sets slit count (12 vs 20), strain, caddy, labels, matrices, file naming, thesis | 7 collets at 2.5 mm with grip-window labels |
| B4 | What torque and lateral load does the iris transmit to the core, and may the design add a positive core lock (set screws on a band, or a second clamp) if friction cannot reach the requirement? | Estimated hold is about 7 to 10 N m against a 20 N m placeholder; the answer sets the core liner, thrust washer, and lock escalation | Required holding torque 20 N m with safety factor 2 as a labelled assumption; liner, thrust washer and tommy-bar socket first; positive lock if the Step 8 check fails |
| B5 | Confirm that the cutter hard stop is a metal carriage stop belonging to the upper assembly, not the printed wing nut | Decides keep-out, F4 reference, and the load path | Yes: stop in metal, defined in the ICD, built at Step 12; the nut carries no descent load |
| B6 | Does Mines have a core length, tolerance and delivery state (wet, wrapped, sleeved)? | C8, F4, handling and stand-in design | Tolerance +/-1 mm (UNVERIFIED), length 150 to 500 mm, mass up to 10 kg at 2400 kg/m3 (DERIVED), indoor, bare cores |

### Not blocking, with proposed defaults

1. Bracket SKUs: full-size 30-series class; Step 1 selects SKUs from the 80/20 catalog. Confirm on-hand bracket and M6 screw inventory.
2. Optional early action: print a cone friction coupon (tilt-plane mu_k) and a thread coupon right after Step 3 so release is decided with a measured mu_k instead of a seed. Default: wait for Step 8 coupons.
3. Loads: axial design load 1000 N is a design choice; descent rate for the jig has no source (Phase I threshold 5 mm/min at WOB 100 N or more); hand crank or leadscrew deferred to Step 12.
4. Debris: indoor, debris tray in the base, dust skirt on the nut.
5. Report: 8 to 12 pages, DOCX plus PDF in house style; about 90 tests (Manager ratifies at Step 13 open, with the A.10 item 7 deviation recorded).
6. CAD chain: FreeCAD 1.1 headless per llm_plm_cad; confirm install and whether a 6 in drill STEP exists to import (tied to B1).
7. Does the report cover the upper assembly or defer it (decided at Step 12).
8. Fasteners for non-80/20 joints: stainless M6.
9. Baseline friction, strain and clearance values (mu_k, mu_c, mu_t, PETG tensile and web-strain allowable, c_r, g_a): seeds only; settled by Step 8 coupons and the Step 11 hold test.
10. Footprint and feet: default four adjustable feet or bolt-down slots; mass target and final tip-over number at Step 12.

### UNVERIFIED items the Fact-Checker could not trace (for the human)

- Core diameter tolerance (+/-1 mm): no source.
- Torque 20 N m (jig) and 50 N m (iris): no source; INSITU2 408-411 calls it a measurement to be taken.
- Iris open aperture and anything about the 6 in iris: not found; 7 in value 54.2925 mm has no stated unit.
- Cutter OD: 152.4 mm is unsourced as a cutter OD (it is the tubing OD).
- Cutter spin speed: 1 to 60 rpm is the motor and brake range, not stated as drill spin.
- Mines PDFs in the zip: not read in review because pdftoppm is not installed. Any "Mines specifies" sentence stays out of the report until the PDFs are read (install poppler, or the human reads them).
- Core count (12+12 vs 40/15/30), core length 500 mm (Quinn's value), core mass and density.
- Ascent test profile (INSITU2 444-461), docx contents, 30-6060 catalog data, printer, stock quantities: not verified in review.

---

## Findings disposition

R = resolved in this plan; D = deferred with owner and step.

| Finding | Source persona | R/D | Where |
|---|---|---|---|
| S1 No load case derived; plan proves geometry not hold | Systems Engineer | R | Detail 2 item 3 to 4; T7; Detail 11 hold test; Design Notes 9 |
| S2 Force loop ambiguous; release undefined; "reversal changes data" false | Systems Engineer | R | Detail 2 item 1 to 2; Design Notes 1, 3; A3, F6 |
| S3 Collet cannot close 5 mm with one slit; stiffness varies | Systems Engineer | R | Design Notes 3, 11; C5, C9; Open B3 |
| S4 Binding tolerance is the iris aperture; no tolerance budget; datum scheme | Systems Engineer | R (budget) / D (aperture value to human) | Detail 2 item 5; Detail 1; Open B1; Design Notes 9 |
| S5 Hard-stop load path through printed nut | Systems Engineer | R | Design Notes 2; A2, F4; Open B5 |
| S6 Upper assembly hand-off lacks an interface | Systems Engineer | R | Design Notes 5; P6; Detail 12 |
| S7 Test plan covers parts not system; no physical test; no acceptance spec; assembly sequence | Systems Engineer | R | Detail 11; Detail 12; Detail 8 |
| S8 Step sequence not by dependency; "single generator" wording | Systems Engineer | R | Steps 1 to 4; Objectives 3; Design Notes 1 |
| S9 Report overstates thesis; no decision block; no analysis section; too many cold reads | Systems Engineer | R | Document Structure; Detail 13; Design Notes 6 |
| S10 Over-engineering (X1, SHA-1, F5, four matrices, 130 tests) | Systems Engineer | R (X1 trimmed, SHA-1 demoted, F5 folded, matrices tool-generated, tests to 91) | Design Notes 6, 11; Detail 10 |
| G1 Tr 60 x 8 impossible; thread is an output | Loftsman | R | Design Notes 3; T2; registry |
| G2 Tr flank overhang; use 45/45 | Loftsman | R | Design Notes 3; T8 |
| G3 Cone angle unspecified; self-locking will not release | Loftsman | R | Design Notes 3 (ruling); Detail 3 |
| G4 Holding torque has no analytic check; reinstate moment arm | Loftsman | R | T7; Detail 8 |
| G5 A2 bare tube; F4 wrong reference | Loftsman | R | A2, F4; Design Notes 2 |
| G6 Clamp pose contradicts A1 and F1 | Loftsman | R | F1 two-state solid; Design Notes 3 |
| G7 Coverage and slit design are one problem | Loftsman | R | C5, C8, C9; Open B3 |
| G8 STL tessellation eats clearance | Loftsman | R | E2 |
| G9 C3 probes fall in slits | Loftsman | R | C3 |
| G10 Holder flange needs hard stop | Loftsman | R | F6; Detail 3 |
| G11 Core tilt closed formula | Loftsman | R (numbers recorded; lateral guide at Step 2) | Design Notes 9; Detail 2 item 9 |
| G12 Missing analytic definitions (key, tray, drain, label, lead-in, core stop) | Loftsman | R | Detail 3 work; Designer params gate |
| TP-1 Thread smaller than cores | Topologist | R | Same as G1 |
| TP-2 Stack stated three ways; load path | Topologist | R | Design Notes 3; Detail 2 item 1 |
| TP-3 "Touching is not overlapping" erases allowed vs forbidden | Topologist | R | A1 contact classes C, G, F |
| TP-4 A2 and F4 wrong footprint and plane | Topologist | R | A2, F4 |
| TP-5 105 mm core vs aperture | Topologist | R (gate) / D (value) | Open B1; Detail 1 |
| TP-6 C1 vs C5; self-lock release | Topologist | R | Design Notes 3; C5, C7 |
| TP-7 A3 satisfied from parameters; mid-height; bracket normal | Topologist | R | A3, Rule M and P |
| TP-8 T1 under-specified; cross-threading; export chirality | Topologist | R | T1a to T1d, T9, X1 |
| TP-9 Wall varies 7 to 1; T5 reason wrong | Topologist | R | T5, C9; Design Notes 11 |
| TP-10 Reversal claim false | Topologist | R | Design Notes 1 |
| TP-11 Coordinate system unspecified | Topologist | R | Design Notes 4; Detail 1 |
| F-1 106.369 mm mislabeled | Fact-Checker | R | Design Notes 8; Register; registry; F4 |
| F-2 1 to 60 rpm is motor range | Fact-Checker | R | Register; registry |
| F-3 152.4 mm cutter OD unsourced | Fact-Checker | R | Register; registry; A2 |
| F-4 Core tolerance UNVERIFIED | Fact-Checker | D | Open UNVERIFIED list; B6 |
| F-5 20 and 50 N m UNVERIFIED | Fact-Checker | D | Open B4 and UNVERIFIED list |
| F-6 100 mm core conflict | Fact-Checker | R | Register; registry |
| F-7 Iris aperture UNVERIFIED | Fact-Checker | D | Open B1 |
| Mines PDFs unread (pdftoppm missing) | Fact-Checker | D | Open UNVERIFIED list; owner human or tool install |
| Extraction line cites to correct; ascent test, docx, catalog not checked | Fact-Checker | R (cites) / D (unchecked rows) | Design Notes 8; Register |
| D1 Clamp cannot hold; no core lock | Designer | R | Detail 2 item 4; T7; Open B4 |
| D2 Wing nut is clamp and crash target | Designer | R | Design Notes 2 |
| D3 No Designer params review before geometry; params missing | Designer | R | Detail 1, 3; Detail 6 checklist |
| D4 Wrong-collet defence is a label | Designer | R | Design Notes 11; Detail 6, 9; H6 |
| D5 Core loading three-handed; pinch points; edges; debris | Designer | R | Detail 2 item 9; Detail 9; H7 |
| D6 Release undefined; jacking provision | Designer | R | Design Notes 3; Detail 3; H5 |
| D7 Thread signifiers; cross-threading register; print orientation | Designer | R | Design Notes 3; T9; Detail 6, 8 |
| D8 Base stability and tip-over | Designer | R (stated) / D (final footprint number to Step 12) | Design Notes 5, 7; Detail 12 |
| D9 Gate wording; image-capable reviewer | Designer | R | Detail 9 checklist; Designer slots |
| D10 State signifiers | Designer | R | Detail 6; Detail 9 |
| D11 "Boss" naming | Designer | R | WD-A4; Detail 13 |
| G-1 Step 9 has no detail | Designer | R | Detail 11 |
| G-2 Step 1 before Step 2 | Designer | R | Steps 1 to 4 |
| G-3 test_printability.py ambiguity | Designer | R | Detail 4 (no sixth module) |
| G-4 Single generator wording | Designer | R | Objectives 3 |
| G-5 Revision history inside the contract | Designer | R | Moved to Progress Log; removed from Document Structure and details |
| G-6 Undefined references (A.4, A.10 item 2) | Designer | R | One-line rules in Details 3, 4, 14 |
| G-7 Designer role at Step 0 | Designer | R | Step 0 row and Designer slots |
| Thesis overclaims; "four-collet" in thesis | Designer, Systems Engineer | R | Document Structure |
| Opening promise "print tests" | Designer | R | Document Structure opening promises |
| Limitations table missing holding torque, aperture, coverage | Designer, Systems Engineer | R | Document Structure |
| Echo registry stale (Tr 60 x 8, collet count, iris standoff, spin, load rating, missing rows) | Designer, Fact-Checker | R | Echo Site Registry |
| E1 Min engagement and clearance placeholders | Software Engineer | R | Registry; T3, T4 |
| E2 Collet seats in boss or holder | Software Engineer | R | Design Notes 3 |
| E3 bore_free formula | Software Engineer | R | C3; registry |
| E4 Coverage at 5 mm spacing | Software Engineer | R | C8; Open B3 |
| E5 Nut stop branch | Software Engineer | R | Design Notes 2 |
| E6 Tall core lateral stability | Software Engineer | R (steady rest, tilt bound) / D (lateral guide design to Step 12 with H3 data) | Detail 2 item 9; H3 |
| E7 PETG allowable strain | Software Engineer | D | Step 8 coupon, Step 11 H4 |
| E8 106.369 applicability to 6 in drill | Software Engineer | D | Open B1; F4 labelled assumption |
| Disagreement: 130 vs about 60 tests | Software Engineer, Systems Engineer | R (ruling: 91) | Design Notes 6 |
| Disagreement: nut as hard stop vs frame stop | Loftsman, Topologist, Systems Engineer, Designer | R | Design Notes 2 |
| Disagreement: analytic vs empirical | Loftsman, Engineer | R | Design Notes 10 |
| Disagreement: thread 165 vs 135, collet type, register length | Loftsman, Topologist | R (formula governs; Step 3 decides) | Design Notes 3 |
| Disagreement: release by cone vs captured nut | Loftsman, Designer | R (captured nut primary, cone fallback) | Design Notes 3 |
| Disagreement: re-measure scope; F5; stack height; family spacing | Software Engineer, Systems Engineer, Topologist, Loftsman | R | Design Notes 11 |
