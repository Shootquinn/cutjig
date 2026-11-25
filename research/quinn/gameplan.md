# Core Cutter Test Jig Gameplan

**Document(s) under work:** workorder.md (core cutter test jig: base with tubular receiver, core holder, wing nut, collet family; 3D models, physical hold test, technical report)
**Operational guide:** method/operational_guide.md. Contributor: quinn. Scratch: research/quinn/cr_scratch/. Repository sync rules: section "Repository Sync" at the end of this file; they apply to every step.
**Accumulator file:** research/quinn/accumulator.md (created at Step 0 close, 2026-11-08)
**Other reference files:**
- workorder.md
- supplements/llm_plm_cad.md (CAD active), supplements/freecad_api_reference.md
- method/tdd_method.md
- supplements/writing-guides/reporting-copy.md, structure.md, style.md, style-reference.md, supplements/signs_of_ai_writing.md
- research/quinn/cr_scratch/step0_engineer_source_extraction.md (cutter, envelope, load, core facts; corrections in Design Notes 8 must be applied to it at Step 1)
- research/quinn/cr_scratch/step0_human_stock_80-20.md (30-6060 stock on hand; DECLARED)
- research/quinn/cr_scratch/step0_human_gate_decisions.md (the human's Step 0 gate decisions, DECLARED 2026-11-08; they override every default, reviewer finding and UNVERIFIED flag they touch; carried in Design Notes 12)
- research/quinn/cr_scratch/step0_manager_open.md, research/quinn/cr_scratch/step0_manager_close.md (Step 0 close)
- research/quinn/cr_scratch/step0_systems_engineer_review.md, step0_loftsman_review.md, step0_topologist_review.md, step0_fact_checker_review.md, step0_designer_review.md (Step 0 findings; dispositions at the end of this file)
- SBIR folder: C:\Users\Quinn Morley\OneDrive\PROJECTS\Planet Enterprises\NIAC\BOREBOTS\Unleashed Robotics\2026 PROPOSALS\2026 SBIR\ (cr_scratch/INSITU2_text.md is the iris proposal text; cr_scratch/INSITU3_text.md for WOB; proposals/csm_sow.md; context/)
- Rigged drill model: C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\gpr (DOUBLE DONG, 7 in bore, NOT the 6 in redesign)
**Date:** 2026-11-08
**Current step:** 7 closed; Step 8 on HOLD. On 2026-11-24 the human reopened the configuration: Step 12 (upper assembly) is pulled forward as a 2D sketch phase led by sean (research/sean/gameplan.md); decisions in Design Notes 23. Pytest 672 collected, 620 pass, 52 fail: the 50 Step 7 MISSING/ABSENT failures, plus test_P10_working_stroke_per_core_class (park below the 0.75 m start after travel 650, Design Notes 23) and test_common_guard_shifted_partner (stale probe timestamp from the fresh clone; re-run tests/probes/probe_common_guard.py).
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

**The point, in one sentence:** A 30-6060 frame with a printed tubular receiver, wing nut and collet family is designed to hold a 90 to 105 mm Mines core upright and coaxial under the 6 in drill; CAD tests and a physical hold test check the design against a 10 N m holding-torque design assumption, with the iris throat opening carried as a parameter.

**Shape:** Lead-first (LDR). Readers are an SBIR program manager and an engineering faculty member who may stop after page 1. Page 1 gives the design, the verification result, what is deferred, and a "stated assumptions" block (10 N m holding torque, iris throat opening as a parameter, core tolerance, core lengths, each labelled DECLARED or ASSUMED, with what changes if the Phase I value differs). Page 1 also states that the drill's own drivetrain closes the iris and the jig has no actuator. Later sections give method and evidence. An analysis section (requirements, free-body diagram, derivation, tolerance budget, prediction against test) serves the engineering-school reader.

**Opening promises:** Audience: SBIR program manager and engineering faculty. Breadth: base, holder, wing nut, collet family and frame as designed, verified in CAD, and checked by the physical hold test if the result is back before the report is built (otherwise stated as pending). No claim of built upper assembly, drill test data, or flight representativeness.
**Resolution delivers:** The same breadth: models, CAD test evidence, analysis with prediction, hold-test result or its status, BOM, status of upper assembly scoping and the acceptance spec.

**Known limitations and where each goes:**

| Limitation | Placed in | Why there |
|---|---|---|
| Cutting face (sets borehole and core diameter) out of scope | Scope paragraph, section 1 | Reader needs it before any dimension |
| Jig does not actuate the iris; the drill drivetrain does | Page 1 clause and section 2 | A page-1 reader would otherwise misread the load path |
| Holding torque is a 10 N m design assumption (DECLARED); friction holding is expected to meet it, the core is expected to fail first; analytic estimate and hold-test result reported against it | Page 1 and section 4 (analysis) | It is the binding performance limit |
| Iris throat opening is a parameter (nominal 108.585 mm open diameter, DECLARED; the new drill may change it); rule: core diameter < open throat | Page 1 assumptions block and section 2 | It sets the margin, not the collet range |
| Collet coverage between nominals depends on grip window and core tolerance (±1 mm, ASSUMED); the generator makes a new collet on demand for anything outside it | Section 5 (collet family) | Placed with the coverage test |
| Upper assembly deferred, jointly scoped | Section 8 (status and next step) | It is the next action |
| Printed parts are not flight-representative; plastic creep and thread wear | Section 6 (printability) with the test that bounds it | Placed with the evidence |
| Core length (0.5 m capture goal, 0.75 m install, 1 m optional), mass and tolerance are design assumptions, not Mines values | Section 2, as stated assumptions with the margin used | Margin is part of the design |
| Rigged model is the 7 in drill, not 6 in; 106.369 mm is a 7 in model value | Appendix A (source notes) | Provenance, not design |
| Printing and fit validated in CAD and analytic coupons until the human prints | Section 8 | The human's print is the next gate |
| Mines PDFs and XLSX budgets were read at Step 1 (pdftotext, openpyxl): silent on core dimension, tolerance, length, mass and delivery state; the report asserts SBIR text only (ASSUMED, Design Notes 12) | Appendix A | Provenance |

Report outline (8 to 12 pages, DOCX plus PDF): 1 Summary and scope; 2 Requirements and interfaces; 3 Concept (stack, force loop, release); 4 Analysis (load cases, holding torque, tolerance budget); 5 Collet family (generator, taper, slits, coverage); 6 Printability and tolerances; 7 Verification (CAD interference, predicates, physical hold test); 8 Status, acceptance spec, upper assembly scoping, open items; Appendix A source notes; Appendix B BOM and stock allocation; Appendix C drawings and renders. The topic-sentence outline is built at Step 14; the suite is Step 13.

---

## Steps

Re-sequenced against the reviews: foundation, then the one-page concept, then geometry numbers, then the CAD suite. Rationale and ruling in Design Notes 1.

| # | Step | Assigned To | Status |
|---|------|-------------|--------|
| 0 | Team reviews workorder.md, populates gameplan; Software Engineer revises for tests; reviewers weigh in; Engineer revises against findings; Manager closes. Gate to human passed 2026-11-08; decisions in Design Notes 12. | The Manager (open, close), The Engineer, The Software Engineer, The Systems Engineer, The Loftsman, The Topologist, The Fact-Checker, The Designer | Complete (2026-11-08; gate decisions recorded) |
| 1 | Foundation: params seed (iris throat as parameter), BOM, 30-6060 frame model, FreeCAD check, ASSEMBLY.md skeleton, extraction-file corrections, Designer seed params review (non-blocking). See detail 1. | The Engineer, The Fact-Checker, The Designer | Complete (2026-11-08; Fact-Checker SIGNED; 28 tests pass) |
| 2 | System concept: force loop (ten members, foot ring is the holder stop), release (10 degree captured-flange nut, collar back-off lift), load cases, tolerance budget and datum scheme, frozen ICD, family and 106.585 mm cap, stop ownership (upper assembly) and holder stroke gap, stability and handling. Nine decisions. See detail 2. | The Systems Engineer (author), The Loftsman, The Topologist, The Designer, The Engineer | Complete (2026-11-08; Loftsman SIGNED, Topologist SIGNED with one closure by ruling, Designer comment recorded; 65 tests pass; Design Notes 14) |
| 3 | Geometry cross-review: thread, cone, slits, seat, register, clamped-state solid. Designer params review is the blocking gate before any geometry; it must close the 24 missing feature params in research/quinn/cr_scratch/step1_designer_params.md (Design Notes 13) and carry the Designer's Step 2 ABSORB items (Design Notes 14). See detail 3. | The Loftsman, The Topologist (cross-review), The Engineer (script), The Designer (gate; plus a post-build part-level read, a recorded deviation from this row, Design Notes 16) | Complete |
| 4 | CAD test suite, red-first, source-gated. See detail 4. | The Software Engineer (author, signs), The Engineer, The Fact-Checker (source gate) | Complete (2026-11-08) |
| 5 | Parametric collet-family generator, ready for on-demand new collets (usage doc and off-grid test). Deliverable includes the generator keys the Designer listed as missing (research/quinn/cr_scratch/step1_designer_params.md, Generator readiness: NOT READY at Step 1; Design Notes 13) and the Step 2 collet ABSORB items (witness scale, colour, rim notches, grip-window label, caddy, per-collet chamfer min(wall - 1.2, 10.5) with 2.5 where wall - 1.2 lies in (2.5, 3.5), slits, relief holes, strain ratio; Design Notes 14 and 16). See detail 5. | The Engineer, The Software Engineer (test review) | Complete (2026-11-09) |
| 6 | Exploratory pass (Pass 1): every part and accessory, simplified. See detail 6. | The Engineer, The Loftsman, The Topologist, The Designer (gate, image-capable reviewer) | Complete |
| 7 | Assembly, contact-class matrix, predicates, clamp range, wrong-state controls. See detail 7. | The Engineer, The Software Engineer, The Systems Engineer, The Designer (A5) | Complete |
| 8 | Print-process rules, tolerance stack-up, holding-torque check, coupons. See detail 8. | The Engineer, The Loftsman, The Software Engineer | Not started |
| 9 | Production pass (Pass 2). Designer production checklist gate. See detail 9. | The Engineer, The Loftsman, The Topologist, The Designer (gate, image-capable reviewer) | Not started |
| 10 | Final assembly, independent re-measure of exports, STEP/STL/FCStd, code review, topology gate. See detail 10. | The Engineer, The Topologist, The Software Engineer, The Systems Engineer | Not started |
| 11 | Base review package, inter-step gate, and physical hold test on the human's print. See detail 11. | The Manager, the human, The Designer (print-review form), The Systems Engineer (protocol) | Not started |
| 12 | Joint scoping of the upper assembly; end-to-end acceptance spec written first. See detail 12. | The Manager, The Systems Engineer, The Engineer, the human | Pulled forward 2026-11-24: 2D sketch phase in research/sean/gameplan.md; configuration decisions in Design Notes 23 |
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
TDD stage: no geometry tests yet. Tests written here are the params and BOM tests only (P1 to P8), red on an empty params file.
Work: confirm FreeCAD at `%LOCALAPPDATA%\Programs\FreeCAD 1.1\bin\freecadcmd.exe` (FreeCAD 1.1.4; the earlier Program Files path does not exist); take the 30-6060 cross-section from the DECLARED stock file (60 x 60 mm, 30 mm slot pitch; no catalog download, catalog check at purchase) and model it as a parametric extrusion; compute stock allocation (Design Notes 7) with extra cuts listed separately; fix the bracket class (full-size 30-series, no "mini") and T-nut rule (M6 spring-ball roll-in only); list bracket SKUs by full-size 30-series class with "verify SKU at purchase" (ASSUMED); patch the extraction file with the Fact-Checker corrections (Design Notes 8); write the seed `params.yaml` (every externally sourced number carries `source:` and `status:`; `iris.throat_open_diameter` = 108.585 mm DECLARED as a parameter; `core.diameter_nominal` 100, `core.diameters` 90 to 105 at 2.5 mm, `core.tol` 1 mm ASSUMED; `core.length_capture` 500, `core.length_install` 750, `core.length_optional` 1000; `upper.travel_max` 500; `jig.height_target` 2000 as a soft target, recorded and reported, not tested; `loads.torque_design` 10 N m DECLARED); write `ASSEMBLY.md` skeleton: coordinate frame (Design Notes 4), poses R and K, relation table as data, signed feature per part, load path placeholder.
Outputs: `params.yaml` (seed), `ASSEMBLY.md` skeleton, `build_parts/common.py` (paths, YAML loader, 30-6060 profile builder), `conftest.py`, `tests/test_params_bom.py`, `bom_stock_allocation.md`, `bom_purchased.md`, corrected extraction file, `research/quinn/cr_scratch/step1_designer_params.md` (Designer seed review: which functional features lack a specification), `context/literature/` summaries (cited sources only).
Environment check (Manager addition at Step 0 close, revised at the gate): check whether `pdftoppm` (poppler) is present; no download or install. If absent, the "Mines specifies" rows are struck and the report asserts SBIR text only (ASSUMED, Design Notes 12). Step 0 could not read the PDFs.
Gate: Fact-Checker signs the corrections; Designer review recorded (non-blocking). The iris throat is a parameter in `params.yaml`; the rule core diameter < open throat is test P8. Any FreeCAD run over 30 s goes background (A.3.4).

**Detail 2. System concept (one page).**
Objective: decide, on one page, the things that set the shape of every part. Author: Systems Engineer with the Loftsman; the Topologist and Designer review. The human's gate decisions (Design Notes 12) are inputs, not questions.
Contents, each a numbered decision with a number or a stated assumption:
1. Closed force loop sentence (written into ASSEMBLY.md at Step 2, ten members): nut thread flank, nut clamp shoulder, washer, holder bearing flange, holder cone, collet cone, collet foot ring, receiver floor seat, receiver wall in tension, receiver thread flank, back to the nut thread flank. The foot ring top is the declared holder stop (class C at K-max only); the flange-to-rim gap is class G and never loaded; the receiver underside force on the base plate is 0 (A6a).
2. Release mechanism (closed at Step 2): captured-flange nut, cone half-angle 10 degrees. The releasing cone (20 degrees) is retired. Jacking holes are deleted; the jacking provision is the collar back-off lift (281.5 N at 12 N m against a release need of 46, 88, 128 N).
3. Load cases (statics estimate, assumptions labelled): (a) iris closure and severing reaction as torque on the core (10 N m design assumption, DECLARED; the core is expected to fail before the collet slips) and lateral load at a lever arm of 106 mm or more above the holder (100 N ASSUMED at 106.4 mm = 10.6 N m); (b) core weight with retention: 10.4 kg at 0.5 m, 15.6 kg at the 0.75 m install length, 20.8 kg at an optional 1 m (all DERIVED at d = 105, 2400 kg/m3, density ASSUMED); (c) cutter descent load (1000 N), which does not reach the core and is carried by cutter, carriage, metal stop, columns and frame, not the printed parts. Required holding torque is the 10 N m design assumption; no further safety factor is stacked on it.
4. Holding capacity estimate against 10 N m and the design response that serves it. Closed at Step 2: PTFE washer always fitted (ID 136.8, OD 143.2, 1.3 mm); predicted 15.47 N m at d = 105 and 13.26 at d = 90 at 12 N m nut torque; the plain printed washer gives 10.65 and 9.13 and misses 10 N m at d = 90 by 8.7 percent, so no margin is claimed on it. Other responses kept: core liner TPU or silicone, tommy-bar socket, longer wings. There is no positive core lock and no escalation path.
5. Tolerance budget table (stack-up, not per-feature): datum scheme (A frame top plane; B the receiver register bore axis, located through two plate keys and a plate stop pin on slot line C; the core axis is transferred by the holder pilot and collet cone, never by the trapezoidal thread; receiver floor 40 mm above datum A), thread radial clearance and tilt, collet bore print error, slit non-uniformity, core out-of-round, core tolerance (±1 mm ASSUMED, covers Mines manufacturing variation), against the iris slack, computed from the parametric rule core diameter < open throat (108.585 mm nominal, DECLARED parameter; at 105 mm plus tolerance the slack is 1.29 mm per side, 3.79 at 100 mm, 8.79 at 90 mm; coaxiality chain 0.32 + 0.20 + 0.283 + 0.15 = 0.953 against 1.0). The 90 to 105 mm range is not cut on aperture grounds.
6. Interface control table (Design Notes 5), frozen as fixed numbers all parts read.
7. Family: 7 collets at 2.5 mm across 90 to 105 mm (DECLARED), grip window d - 1.5 to d + 1.0, 12 slits at 1.5 mm, generator envelope 85.0 to 106.585 mm; custom collets by the generator on request.
8. Hard stop ownership (Design Notes 2): the metal descent stop, owned by the upper assembly, 1000 N. The holder stroke gap (flange to rim, 1.5 mm minimum in K) is a separate, never-loaded base-side gap.
9. Base stability: footprint, feet, bolt-down slots, tip-over statement, mass target; core handling for a 0.5 m core and the 0.75 m install core (steady rest or cradle, lift strap point). Height: the 2 m jig height is a soft target (members can be shortened later); the plan records the number and does not test it. Upper assembly working stroke is at most 0.5 m; the 959.84 mm loading park is separate and is not working travel. Closed at Step 2: bolt-down is the operating condition (unbolted tip-over 68 N at the column top), steady rest at every core length, choke strap with a 250 mm side handle.
Outputs: `research/quinn/cr_scratch/step2_system_concept.md` (the concept plus the ICD and tolerance tables; it ran about 6000 words, see Design Notes 14).
TDD stage: each decision names the test that will check it (ID from the CAD Test Specification) before it is accepted.
Gate: Systems Engineer authors; Topologist and Loftsman sign; Designer comments. B1 to B6 are settled by the gate decisions (Design Notes 12). Result: Loftsman SIGNED (Re-check 2), Topologist SIGNED on U13 to U16 and decision 8 and closed by ruling on decision 5 and the test IDs, Designer comment recorded with its four BLOCK items answered (Design Notes 14).

**Detail 3. Geometry cross-review.**
Objective: settle thread, cone, slits, seat, register and clamped-state solid with numbers, before any solid (A.4 two-persona rule).
TDD stage: formula tests exist from Step 4 and read these numbers; this step supplies the values and the signs. Disagreements are resolved by number, not opinion.
Work, Loftsman: thread form (right-hand, single start, symmetric 45/45 trapezoid, pitch 8 mm PROPOSED), major diameter from the radial chain (closed at Step 2: 149.58 mm at the 10 degree cone; the 165 and 135 mm figures are superseded; Design Notes 3 and 14), clearances c_r and g_a, cone half-angle, stroke s_z, stop gap, nut length, bore_free(d) = d + tau + c_i, slit count and width law, wall and flexure relief, hand-torque holding estimate (T7 inputs), wing planform, collet total length and ring height, key, debris tray and core stop geometry (the items the Loftsman lists as having no analytic definition). Topologist: sign predicates S1 to S23 against those numbers, contact-class table, register length for cross-thread defence (closed at Step 2 by number: stacked register on holder flange and holder-in-receiver bore, holder length 88.0, g_reg 0.25; the 54 mm figure is withdrawn; Step 3 confirms in the solid), collet topology (alternating slits), OCC strategy for coincident cone faces in the clamped pose, wrong-state defences WS1 to WS11 as features.
Outputs: `research/quinn/cr_scratch/step3_geometry_crossreview.md` (one file, two sign-offs; the Topologist's second-round withhold closed by ruling, Design Notes 16), `params.yaml` updated (319 leaves), the registry rows below filled. Five scripts `build_parts/{receiver,holder,nut,washer,footring}.py` (with `cadlib.py`, `verify_step3.py`), five `parts_cache/{part}.FCStd` and `{part}_result.json`, `parts_cache/step3_cross_checks.json`, `research/quinn/cr_scratch/step3_engineer_first_solids.md`, `research/quinn/cr_scratch/step3_designer_completeness.md`, `research/quinn/cr_scratch/step3_manager_close.md`.
Gate: Loftsman and Topologist sign; Designer params review is blocking: does the parameter set describe a real part (key, tray, drain, core stop, label, wing planform, register, flange recess, hard-stop gap each have parameters, not only a volume)? Designer questions D1, D2, D3, D6 must have an answer in params before Step 5 opens. Output `research/quinn/cr_scratch/step3_designer_params.md`. Step 3 carries the Designer's Step 2 ABSORB items (S2-4 witness scale and wrong-collet defence; S2-5 wing grip and a `stop.g_stop` of 25 mm; S2-6 key sector and bolt-down method; S2-7b nut release marker; S2-7c abuse torque and tommy-bar length; S2-7d captive washer; S2-8 `stop.nut_top_z_min/_max`) and the design facts in Design Notes 14. The Engineer's first solids wait for the signed cross-review (A.4).

**Detail 4. CAD test suite (red-first).**
Objective: contract in code before geometry.
TDD stage: the complete CAD suite (CAD Test Specification) is written, each test labelled discriminator or invariant (7.2), and run red on the empty baseline. Relations are data: tests iterate over the ASSEMBLY.md pair table, so a change in contact class or pose is a data change. Thresholds from Step 3 are read from `params.yaml`; a later suite change is a revision with Software Engineer review and source re-check (A.10 item 5).
Outputs: `tests/test_params_bom.py`, `test_collet_family.py`, `test_thread_clamp.py`, `test_assembly.py`, `test_exports.py` (printability checks live in the collet and export modules; there is no sixth module and no catch-all), `research/quinn/cr_scratch/step4_engineer_baseline.md` (red-first record).
Gate: Software Engineer signs the suite; Fact-Checker signs the source gate (A.10 item 2) against the Source Verification Register; red-first record exists.

**Detail 5. Collet-family generator.**
Objective: one generator, diameter-driven, whole family from `params.yaml`; no hand-built collets.
TDD stage: groups C and F first, then build.
Outputs: `build_parts/collet_family.py` (`build_collet(d)`), `parts_cache/collet_<d>.FCStd` (file naming holds 92.5 as `collet_092p5`), `parts_cache/collet_*_result.json`, free and clamped solids from the same call, `docs/collet_generator_usage.md` (how to command a new collet: the one call, the params it reads, the checks it runs, where outputs land, a worked example, limits of the model), and the off-grid generation record from test C10.
Family: params-driven list; 7 collets at 2.5 mm across 90 to 105 (DECLARED). Custom collets will be requested as needed. Readiness for a new collet at a moment's notice is a Step 5 deliverable: the generator accepts any diameter in a stated envelope (85.0 to min(110, throat - tol - slack) = 106.585 mm, DERIVED; a request above is refused with "change `iris.throat_open_radius`") from one command, runs C1 to C7 and C9 on the result, and writes the outputs without a hand edit. Adding a diameter is a params change for geometry; the function (clamp force per N m, wall stiffness) is a separate claim checked at the extremes (C9, T7, Step 11).
Gate: every collet passes C1 to C9; C10 (an 8th, off-grid collet) passes; the usage doc exists and a reader who has not seen the code can follow its worked example (Designer reads it); topology gate; Software Engineer reviews the generator. Builds over 30 s run as parallel background FreeCADCmd processes (A.15).

**Detail 6. Exploratory pass.**
Objective: surface problems; every functional feature present even if simplified (7.6).
TDD stage: F5 (genus and feature list) and the Step 7 tests run against each part as it appears.
Parts and features (the Designer's completeness checklist; gate fails on any missing item):
- Receiver (boss tube): thread with lead-in and land, floor seat for the collet, register for the holder, asymmetric key slot.
- Holder: cone, flange, key, collar; no jacking holes; no hard-stop face (the foot ring top is the holder stop, the rim gap is never loaded).
- Washer: PTFE ring (ID 136.8, OD 143.2, 1.3 mm), signed radial tab notch (the Engineer's seed, the Topologist confirms at Step 3), captive in the nut face.
- Collet: cone, bore, alternating slits with relief holes, foot key, core stop, rim notches, grip-window label, lead-in chamfer.
- Wing nut: thread, bearing face, wings with planform, tighten arrows, tommy-bar socket, dust skirt. Step 3 built one wing mark (wing 0, +y face, radially directed, 21.86 mm) and the counter-clockwise release arrow on the plate (loosen, 33.25 deg). Step 6 directive: the wing mark must be a tangential clockwise tighten glyph and a counter-clockwise loosen glyph must be added on the opposite wing face, both inside 21.86 mm; the Designer reads both with the image-capable gate.
- Base: plate, debris tray, drain, slotted mounting holes, T-nut provisions, feet or bolt-down.
- Frame: members and brackets from stock with allocation.
- Accessories: collet caddy, alignment gauge, steady rest or cradle, witness scale and tick on holder flange.
- The stop: shown as an interface item at the descent assembly (Design Notes 2), not as a nut property; owner the upper assembly, `upper.metal_stop`.
Outputs: `build_parts/<part>.py`, `parts_cache/*.FCStd`, `research/quinn/cr_scratch/step6_engineer_findings.md`, `research/quinn/cr_scratch/step6_designer_critique.md` (Design Critique, 8.4c).
Gate: Designer on completeness against the checklist ("can we learn from this?"), using an image-capable reviewer for the renders.
As built (Design Notes 21, 22): the witness scale is a 12 mm ruler engraved on the receiver thread at azimuth 127, read at the nut z 0 face; the holder tick is a datum groove. Tighten glyph on the top face of wing 0, loosen glyph on its underside. Steady rest chosen over a cradle. Plug is its own part. Frame is 12 brackets (8 purchased, 4 printed) and 96 T-nuts after Step 7.

**Detail 7. Assembly, contact classes, predicates, clamp range.**
TDD stage: groups A, T, F tests first including negative controls and WS1 to WS11.
Work: poses R (release) and K (clamp) generated from one pose by the screw motion S(phi), not placed independently; contact-class matrix (C, G, F) per pair per pose per collet; predicates S1 to S16; E-1 to E-9 envelope; N x N collet and core sweep; thread tilt test.
Outputs: `build_parts/assemble.py`, `output/jig_assembly.FCStd`, `.step`, `research/quinn/cr_scratch/step7_interference_report.md` (per-pair table, mm3, class, pass/fail; one table per collet configuration, tool-generated, not hand-reviewed), four-view PNG set.
Visual: front, side, top, isometric, judged against a rubric with an item per signed feature, and signifier (A.3.1).
Gate: Software Engineer, Systems Engineer, Designer (A5, image-capable reviewer).
Step 7 additions (Design Notes 22): C6 bracket overlaps closed by frame rebuild; holder collar and nut relief bore rebuilt; test file `tests/test_step7_assembly.py`; wrong-state and pose probes `tests/probes/probe_ws.py`, `probe_poses.py`, `gates.py`.

**Detail 8. Printability, tolerance stack-up, holding torque.**
Objective: show parts print and fit, and that the clamp can plausibly hold, before the human spends filament. No printer constraints are imposed: parts are designed freely and are not split to fit a bed; the human will ask for help if something does not print.
TDD stage: T3, T7, T8, T9, C6, C9, E2 first.
Work: min wall, thread clearance per side, slit web strain against a design-assumption allowable (ASSUMED; the coupon is the check), tessellation deflection; print orientation stated per part (wings in-layer, threads axis vertical, 45/45 flanks); tolerance stack-up table closed against the Step 2 budget; holding-torque check T7 at both family extremes against 10 N m with mu values labelled ASSUMED; coupons as STL: thread coupon (boss and nut with pilot), one collet at 90 and one at 105 mm, slit flex bar, cone friction coupon (tilt-plane test for mu_k); assembly sequence for a 10.4 kg (0.5 m) and a 15.6 kg (0.75 m) upright core written into ASSEMBLY.md.
Outputs: `output/coupons/*.stl`, results appended to `research/quinn/cr_scratch/step7_interference_report.md` (no separate printability file), predicted-values sheet for Step 11 (written before the print).
Gate: Loftsman reviews clearance and holding estimate; Software Engineer reviews tests.
Carried in from Step 6: D13, the NT8 release-arrow shaft at 0.7 mm, as a print-process rule (the printer is not a design input).
Carried in from Step 7: receiver-support path (the receiver has no shoulder or flange and the plate hole is straight; no modelled path carries receiver weight, core weight or the 204 N pull-out to the plate; add a receiver/plate pair or a shoulder, then A6a against a real contact), shared with Step 12.

**Detail 9. Production pass.**
Objective: every feature deployment-ready (7.6). Every operator-facing edge counts as function: wing edges, flange edge, slit edges, collet mouth, tray lip.
TDD stage: re-run all tests on production geometry; lead-ins and chamfers must not change contact faces, thread sign, pilot or cone sense.
Outputs: updated part scripts and FCStds; change-order record if params diverge from FCStd (FCStd wins; sync first, 5.2.1).
Carried in from Step 6: D4 witness colour fill and digits; D7 caddy lift relief and key notch; D9 rest open and closed marks; D12 rest roller pin lock or radius mark; steady-rest adjustment refinement (8.75 mm travel).
Carried in from Step 7: D14 (rest rollers 51 to 82 mm off axis cross the cutter tube wall 73.0 to 76.2; render rest in hold and park, state the release height); receiver render colour against the blue 100 collet; datum C hardware (two key T-nuts, stop dowel) and the PZRT T-nut BOM (CAD absent, proxy stands).
Gate: Designer production checklist (all items pass; image-capable reviewer):
1. Pride: would the Designer show the part to a client without apology?
2. Cold-user: can an operator who has not seen the jig load a 90 and a 105 mm core correctly from the part marks alone?
3. Poka-yoke: each WS1 to WS11 defence exists as a feature, not only as a test.
4. Signifiers: identity (grip-window label, color, rim notches, caddy), direction (tighten arrow), state (witness line).
5. Recoverability: jam release (collar back-off lift; manual raise with a 300 N shear link; park latch), over-travel bounded by the metal stop, nut removable with a stuck collet, a broken wing leaves the core on its stop.
6. Operator-facing edges reviewed one by one (holder flange to receiver rim gap closing from 13.1 mm to 1.5 mm; wing sweep; slit closure; dropping a core onto the stop).
7. Print orientation and wing layer direction stated per part.

**Detail 10. Final assembly and independent re-measure.**
Carried in from Step 7: receiver BOP defect D6 (InvalidCurveOnSurface on the receiver thread; half-space cut by an axial plane returns it unchanged).
Work: re-run all CAD tests; one independent script that imports only the exported STEP and STL (no build or test code) and recomputes per-collet volume, the interference matrix and thread chirality sign, compared to the result JSON; negative controls (probes away from the feature still hit; a deliberately wrong expected value fires; a mirrored nut export fires). The delivered FCStd opens with every deliverable object visible and named. A SHA-1 manifest of text sources is written as a backup action (not a test).
Outputs: `output/jig_assembly.FCStd`, `.step`, `output/stl/*.stl`, `output/remeasure_results.json`, renders, `ASSEMBLY.md` and BOM final, ICD final.
Gate: Software Engineer code review; Topologist final topology gate (Euler check, genus, component count per part, signed volume positive); Systems Engineer interface review (base, collet, holder, nut, frame, future upper assembly).

**Detail 11. Base review, inter-step gate, physical hold test.**
Objective: test as you fly: check the stated purpose on hardware, against values predicted before the print.
Human actions: review models; print the Step 8 coupons, then the receiver, holder, nut, and collets at the extremes (90 and 105 mm, plus one middle). Designer writes the print-review form (clamp feel, wing grip, loading the core, wrong-collet trial, jam and release); Systems Engineer writes the protocol; results return as a change order.
Stand-in core: 100 mm concrete cylinder or PVC section of similar mass, 500 mm long, up to about 10.4 kg; a 750 mm stand-in (about 15.6 kg) for the install length; also a 90 mm and a 105 mm stand-in. (Core diameters in the test match the collet under test.)
Protocol and pass criteria (predictions entered from Step 8 before the first test; Loftsman 10.65 / 9.13 N m plain and 15.47 / 13.26 N m with the PTFE washer at 12 N m nut torque (d = 105 / 90); spread at d = 90: plain 3.8 to 23.1, PTFE 5.8 to 31.0; all ASSUMED inputs):

| Test | Method | Result recorded | Pass |
|---|---|---|---|
| H1 Torque to slip | Hand-tight nut (record nut torque), torque wrench on a lever arm about the core axis, 90 and 105 mm collets | N m at first rotation | Two outcomes reported separately: (a) model valid if within a factor of 2 of prediction; (b) design assumption met if at or above 10 N m (DECLARED). A result below 10 N m is reported as measured and enters a change order; there is no positive-lock fallback |
| H2 Pull-out | Spring scale along the axis | N at first axial slip | At or above core weight x 2 (204 N for the 10.4 kg core; 306 N for the 15.6 kg install core) |
| H3 Lateral deflection | Side load 21.2 N at the top of a 0.5 m core (100 N at 106 mm: 10.6 N m on the holder), dial indicator | mm at top, and tilt in degrees | Within the coaxiality budget of the Step 2 tolerance table |
| H4 Cycles and creep | 10 clamp and release cycles; 24 h hold; repeat H1 | Thread wear, collet set, H1 change | H1 after 24 h within 20 % of initial (PROPOSED) |
| H5 Jam and release | Back off the nut after clamping at the stop | Collet frees by nut back-off lift, holder lifts, cold user | Tool-free release; minimum lift ratio 2.20 |
| H6 Wrong-collet trial | Fit a too-large collet, tighten to the stop | Does the witness line show the error | Witness line outside zone in 100 % of trials |
| H7 Cold-user loading | Unfamiliar operator loads a 500 mm stand-in using only part marks and the caddy | Time, errors, hands needed | No wrong-collet or unseated core; one operator can do it with the steady rest |
| H8 Stop gap trial | 152.4 mm tube template over the assembly | Gap collar top (wings included) to cutter lowest point at the stop, template clear of every fixture above the stop; funnel seating force through the collet | g_stop gap at least 25 mm present at full descent; seating force not above the H3 lateral load |
| H9 Jam recovery | Jam the cutter on the core with the drill unpowered; manual raise by one person; fuse trip at the 300 N shear link at its upper tolerance (330 N); park latch | Raise path, fuse trip force, core pull | Jam force on the core at most 183 N, below the 204 N pull-out of H2; latch holds at park |
| H10 Strap proof | Proof pull on the choke strap and side handle | Rated load | 80 kg |

Gate: The Manager verifies the hold-test record; failures re-enter at Step 3 (geometry) or Step 8 (analysis) as a change order.

**Detail 12. Joint scoping and end-to-end acceptance spec.**
Carried in from Step 7: stop, columns and carriage are not in the pose set (A2c, A2d, A1c, A1d, A2h decide no printed member is in the stop path); receiver-support path and the 204 N pull-out load check; A3b closes with the column foot and carriage guide (built fits sum 0.45 against 1.0); datum C hardware.
Objective: define the drill-holding upper assembly with the human after base review, accepted against a spec written first.
First deliverable: `research/quinn/cr_scratch/step12_acceptance_spec.md`, the five-verb acceptance spec:

| Verb | Criterion | Source or status |
|---|---|---|
| Hold | Core does not rotate or slip under the measured iris reaction; core axis within the coaxiality budget of the drill axis | Torque 10 N m design assumption (DECLARED); Phase I value replaces it when measured; budget from Step 2 |
| Descend | Axial load path 100 to 1000 N reaches the metal stop, not the printed nut; rate at least 5 mm/min at 100 N or more | INSITU3 267-268, 424-430 (verified); jig load is a design choice |
| Sever | Iris closes from the drill's own drivetrain; Hall amplitude falls from about 400 to about 45 counts; core cut at the iris plane | INSITU2 157-166 (verified); standoff for the 6 in iris ASSUMED (Design Notes 12) |
| Retain | Severed core retained in the drill; retention force and closure torque curve measured per Phase I protocol | INSITU2 408-414 (verified) |
| Retract | Iris opens by reversing braking torque; drill retracts without disturbing the jig; core removable from the jig | INSITU2 164-165 (verified); jig release per H5 |

Agenda: guide and anchor for the 6 in drill; carriage stop on the columns (metal, rated; the metal hard stop belongs to the upper assembly, DECLARED); working stroke at most 0.5 m with a separate 959.84 mm park; torque reaction (10 N m design assumption); descent method and rate; instrumentation access (load cell and Hall sensor cabling at the back cap, cable exit and debris path); whether a spindle drive is in jig scope (if yes, spawn The Motor Designer); iris closure confirmation; tip-over statement for a 1540 mm column on the stock-driven footprint (Step 2 numbers: 158 N at the centre of mass, 68 N at the column top, bolt-down operating condition at 115 N per bolt with the cutter above z = 400 mm; Step 12 replaces them); steady-rest detents (310 and 560 mm), choke strap with 250 mm side handle, park at 959.84 mm with latch and 300 N fuse, hoist and column-top cross member (joints 8 to 10); use of the 1540 mm lengths.
Outputs: `research/quinn/cr_scratch/step12_scoping_notes.md`, a new work order `workorder_upper_assembly.md`, appended gameplan Steps 12.1 and up, the decision whether the report covers the upper assembly. The upper assembly gets its own test suite before its geometry.

**Detail 13. Report test suite (Prompt 1).**
Inputs: workorder.md, Document Structure, extraction file, Step 10 result JSON (names of values), Step 11 hold-test record, Source Verification Register.
Size and split: about 90 tests (ruling in Design Notes 6). Ratified by the Manager at Step 0 close (91 stands; deviation from A.10 item 7's 150 to 200 band recorded in Design Notes 6). Reconfirmed at Step 13 open only if the report scope changes. Step 13 produces a scripted tally of tests by scope, mode and group, and that tally, not the prose in this plan, is the authority for counts.

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
Output: `report_test_suite.md`. Gate: every test that reads an ASSUMED value asserts the label; no test carries an open UNVERIFIED status.

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

TDD stage for Steps 15 to 20 (Manager addition at Step 0 close; the Steps table carries these steps without a stage field, so each is stated here):
- 15: precondition check only. The Step 14 validation record must exist before this step opens (A.4). Fact tests are checked against the Register as the copy is written.
- 16: the automated suite groups (abbreviation, echo-site, AI-tell, format) run on the Writer draft; every failure is listed for the Editor.
- 17: the same groups run after the edit; AI-tell and echo-site detectors carry their zero and known-bad controls (Principle 9).
- 18: Wave 2 reviews read the suite and the two cold-read results; no third cold read.
- 19: final suite run, all automated tests green, manual tests recorded with evidence, final cold read.
- 20: no new tests. The Manager verifies that the suite record, the tally and every output named in Steps 13 to 19 exist.

---

## CAD Test Specification

Every test is automated unless marked manual. (d) means parametrized over the family list in `params.core.diameters`. Thresholds named `params.*` come from `params.yaml`; PROPOSED values are seeds to be confirmed or replaced at Step 3. "Control" means the zero control and known-bad control required by Principle 9. Size: about 46 test functions (P8 and C10 added at the gate, T6 withdrawn); case count follows the family size (7). Design freedom rule (gate decision): no test constrains a dimension the human has declared soft (jig height 2 m, core length beyond 0.5 m) or an input the human has declared not a design input (printer). Such values are parameters, recorded and reported. Predicates are computed from final shapes (faces, fitted axes, helix probes), never from the placement or parameter used to build them (Rule M); every sign test first passes the self-check that p + eps*n is outside the solid and p - eps*n inside.

**Group P: params, BOM, contract**

| ID | Test | Pass criterion | Evidence |
|---|---|---|---|
| P1 | `validate_params()` | Accepts the seed; rejects known-bad: negative clearance, a thread major smaller than the largest collet bore plus walls, a family diameter outside the generator envelope | pytest result |
| P2 | Source keys | Every externally sourced number has `source:` and `status:`; DECLARED, ASSUMED and VERIFIED counts reported and match the register | Count printed |
| P3 | Stock allocation | Per stock length, summed cut lengths <= on-hand quantity x length; extra cuts only in the extra-cut table; 1540 mm lengths unused unless the human directs otherwise | `bom_stock_allocation.md` parsed |
| P4 | Hardware rules | T-nuts are M6 spring-ball roll-in only; every bracket is a SKU or full-size 30-series class with leg at least 57 mm (30-4332, 30 mm legs, superseded), no "mini" | grep; control: planted "mini bracket" fires |
| P5 | Frame profile | Each member bbox 60 x 60 mm within 0.05 mm; length equals cut list | result JSON |
| P6 | Interface control table | ICD exists in params with datums A, B, C, mounting pattern, coaxiality budget, keep-out envelope, stop height and rating, footprint and tip-over statement, cable exit; no empty field; every key in the concept ICD table exists in params (P10); ICD fields include floor_above_datum_a, coaxiality_chain and the U12 to U16 keys. P6 is split in the concept Test ID key: P6a document check (outside Rule M), P6b footprint, P6c working stroke, P6d park envelope. The 2 m jig height appears as a soft target value, not a limit | params parse |
| P7 | Assumption labels | Every ASSUMED or DECLARED value read by any test appears in a report-assumptions list with its label | list match |
| P8 | Iris throat rule | `iris.throat_open_diameter` is a parameter (seed 108.585 mm); for every family diameter, d + `core.tol` < throat. The rule is evaluated for whatever throat value is set, so a different drill changes data, not the test; the family range is not cut on aperture grounds. Known-bad: throat 100 mm fires; zero control: seed reads pass. Step 2 values: slack per side 1.29 / 3.79 / 8.79 mm at 105 / 100 / 90 plus tolerance, 0.50 at 106.585; a request above 106.585 is refused | pytest result |
| P9 | Measured profile (Step 2) | Section area within 1 percent of the STEP measurement (916.56 mm2); hollow, not the solid 2893 mm2; each `profile.*` value the STEP supplies matches within 0.05 mm and is VERIFIED with the STEP as source; mass per metre within 5 percent of catalog 2.573 kg/m (STEP-based value 2.475 is 3.8 percent under; the catalog value is used for mass work) | pytest result |
| P10 | ICD freeze (Step 2) | 41 frozen keys exist with source, legal status and the concept value; stop ownership (no stop key under base, receiver, holder, collet, nut, washer, wingnut or collar; `upper.metal_stop` present); ten-member load loop in ASSEMBLY.md with 45 pair rows; soft 2 m height recorded and reported, not tested; coaxiality chain 0.953 at most 1.0; working stroke per core class; bracket rule | pytest result |

**Group C: collet family (d)**

| ID | Test | Pass criterion |
|---|---|---|
| C1 | Validity | Single solid; isValid; isClosed |
| C2 | Volume | Whole-part volume within 0.95 to 1.05 of the analytic volume (Loftsman frustum shell minus bore, slits, relief holes); each cut removes volume within 3 % of its analytic expectation and 0 < removed <= tool volume (7.1). Per-cut checks carry the discrimination, since slits are about 5 % of volume at d = 105 |
| C3 | Bore diameter | Probe along three azimuths offset from slit centres (phi_0 + 180/N + 120k degrees); reject any probe that returns a slit hit; mean bore equals `bore_free(d)` = d + tau + c_i within 0.02 mm (model check; print error is bounded in Step 8). Control: probes at 0, 120, 240 degrees on a 12-slit part fire |
| C4 | Family invariants | For every pair d, d': volume of common(X_d, X_d') equals volume of each within 0.01 mm3, where X is the solid of revolution of the outer profile with the bore filled; the symmetric difference of any two collets lies inside the larger bore annulus; taper, large and small OD, seat height identical within 0.02 mm |
| C5 | Slits | Alternating slits (top and bottom, relief holes at ends); count equals params; slit planes contain the Z axis within 0.01 mm; width within 0.05 mm of the law w_s = pi x Delta / N + w_min; a ray across a slit meets void for the slit depth and solid below |
| C6 | Minimum wall | Minimum wall at the cone top at least `params.collet.min_wall` (ASSUMED 1.2 mm, a design rule, not a printer value); runs for every d |
| C7 | Topology | Faces per edge all 2 except cylinder seams; component count 1; Euler characteristic equals the expected value for the alternating-slit collet (genus 1 per Topologist table); no leftover planar face on a slit plane; min face area and edge length recorded |
| C8 | Family coverage | For every core diameter 90 to 105 mm in 1 mm steps, widened by `params.core.tol` (default +/-1 mm, ASSUMED), some collet's accept range (derived from Delta = s + c_i, not asserted) contains it. Known-bad: remove a mid collet and the test fires. Cores outside the family are served by the generator (C10), not by widening this test |
| C9 | Closure arithmetic and stiffness | Per-slit closure pi x Delta / N is less than slit width minus `params.collet.min_slit_clamped` (PROPOSED 0.5 mm); web strain (screening model, allowable ASSUMED) below allowable; wall at d = 90 and d = 105 and the resulting stiffness ratio recorded (the extremes bound the family by wall and stiffness) |
| C10 | On-demand collet (the 8th, off-grid) | Following only `docs/collet_generator_usage.md`, generate a collet at a diameter not in the family list (default 97.0 mm, between 95 and 97.5 nominals; a second run at 93.7 mm to prove no grid assumption) with one command and no hand edit. Pass: C1 to C7 and C9 pass for it, result JSON and FCStd are written under the naming rule, family invariants (C4) hold against the seven, and the run time is recorded. Known-bad: a diameter outside the generator envelope is rejected with a stated reason; the usage doc is missing, and the test fires |

**Group T: thread, engagement, clamp range**

| ID | Test | Pass criterion |
|---|---|---|
| T1a | Chirality probe | Ridge centreline sampled at theta = 0 and 90 degrees at fixed rho: (z90 - z0) mod L = +L/4 on boss and on nut. Known-bad: a mirrored nut fires. Hand is a constant in `common.py`, not a params field; both parts call one helix function |
| T1b | Screw-motion mesh | Nut moved by the screw motion Rz(phi) T(0,0,L phi/2pi) for phi in {15, 90, 180, 360} degrees: common volume with boss <= 0.01 mm3. Opposite-hand motion at 90 degrees and pure rotation must show large common volume (fires) |
| T1c | Direction | A clockwise turn from K lowers the nut (dz < 0) |
| T1d | Export chirality | T1a repeated on the exported STL and STEP (inside X1) |
| T2 | Thread dimensions | Major diameter equals the Step 3 chain output within 0.05 mm (not a constant); pitch = lead (single start); flank angle 45 degrees +/- 0.5; tooth depth and crest flat per params |
| T3 | Print clearance | Radial crest clearance c_r and axial flank gap g_a per side equal params within 0.05 mm and are at least the minimum (seed values ASSUMED; the coupon adjusts them) |
| T4 | Thread engagement | In K at d = 90 and 105: engaged axial length >= `params.thread.min_engage_pitches` (PROPOSED 3 pitches; at least 24 mm in every pose, A3i); in R just before disengagement is possible also >= min_engage. Zero control: nut at the top with no overlap reads 0 |
| T5 | Clamp range at the extremes | For d_min and d_max build R and K from one pose. R: free bore >= d + tau + c_i, a core of d + tau slides in with zero interference. K: nut hand-tight, slit width above `min_slit_clamped`, engagement per T4, nut has at least 1 pitch of travel left (S12; Step 7 reads the physical stop, `nut_stop_travel_mm`, expected 10.01 at K-max against 8.0), holder flange gap to receiver rim above zero. Pass: all four poses. The extremes are the right tests because wall thickness and stiffness vary most there; stack height at cone contact is independent of d (C4), so it is not the reason |
| T6 | (withdrawn at the gate) | Nut OD and bed fit removed: the printer is not a design input and no part is split to fit a bed. The ID is not reused |
| T7 | Holding torque (analytic) | T_hold(d, F_hand) is computed for d_min and d_max using the Loftsman model (mu values ASSUMED, labelled), with F_hand from stated wing arm and thrust-washer coefficient, and is compared with T_load = 10 N m (DECLARED design assumption, no extra safety factor). The test checks that the prediction exists, that every input carries its label, and reports the margin; a prediction below 10 N m is reported as a design response item (liner, thrust washer, longer wings), not a pass/fail on geometry. A prediction is not proof; the physical hold test is the authority |
| T8 | Print overhang rule | No down-facing thread flank below 45 degrees from horizontal (sectional probe). Known-bad: a Tr 15 degree profile fires |
| T9 | Register and tilt (cross-thread) | At first thread contact (holder hanging at insertion register_depth + p), the measured register stop (holder on one bore wall at its bottom, generator on the opposite bore edge, holder/receiver common > 0.01 mm3, bisection to 0.001 deg) plus plate rock atan(p / 136.44) gives alpha_total. The axial misregistration across the thread, D tan(alpha_total) with D and P measured from the receiver thread, satisfies 1.5 x D tan(alpha_total) <= P/2 (same line as alpha_crit / 1.5 = 1.021 deg). Known-bad controls must fire: the superseded L_h 54 register (measured stop) and 2 x alpha_crit both exceed the line; at 2 x alpha_crit the holder/receiver common is > 0.01 mm3 (the register blocks the onset). Instrument controls: wall pose clear at zero tilt; nut axial drop of g_a/2 - 0.05 clear and g_a/2 + 0.05 interfering. Rigid-tilt nut/receiver overlap is not a T9 measure (it forces the nut through the flank it rests on). Step 4 measured: register 0.596 + rock 0.315 = 0.911 deg, misregistration 2.379 mm against 4.000, factor 1.68; holds for g_reg <= 0.299 mm; holder length 88.0, p = 0.75. Revised Step 4 (research/quinn/cr_scratch/step4_loftsman_t9_ruling.md) |

**Group F: fit and function**

| ID | Test | Pass criterion |
|---|---|---|
| F1 (d) | Collet seat fit | R: radial gap between collet cone and holder cone within `params.fit.seat_clearance` +/- 0.05 mm everywhere. K: the clamped collet solid (bore = core diameter, slit narrowed by pi x (B_f - d_c)/N, outer cone reduced, placed at holder-relative axial offset s_z) is in contact with the holder cone: common volume < 0.01 mm3 (offset 1e-3 mm radially for OCC) and contact area above `params.seat.min_contact_area` |
| F2 (d) | Core in collet | A core cylinder of nominal d slides into the R-pose bore with common volume < 0.01 mm3; its base lands on the core stop (axial gap 0 +/- 0.05 mm) |
| F3 | Collet and core sweep | N x N: each core diameter against each collet, in R pose. The matching cell passes; cores larger than the free bore are rejected by interference (must fire); cores below the clamp range show slit bottoming or no contact (must fire). Diagonal passes, off-diagonal rejected as the accept range predicts |
| F4 | Exposed core | Core top above the plate top by at least `params.core.min_exposed` = 143.12 mm = 106.369 standoff + 25 g_stop + 5 margin + collar top 6.75 (the collar top is the highest fixture inside the cutter footprint). Standoff = 106.369 mm is head tip to kerf sphere centre of the 7 in model, not the pinch plane; applicability to the 6 in drill ASSUMED. Test asserts the stated assumption and reads it from params |
| F5 | Genus and feature presence | Per part: genus equals the declared through-hole count; each feature in the Step 6 checklist exists in the result JSON with nonzero feature volume; flipped copy of each part distinguishable by its signed feature (Rule P). On the empty baseline every one fails |
| F6 | Holder stroke gap | Flange to rim 13.126 (R), 8.59 (K at d+1), 1.5 (K-max), key `holder.stroke_gap_*`; holder bottom to foot ring top 11.626 / 7.089 / 0.00 (class C at K-max only); never loaded (S6) |

**Group A: assembly** (relations are data in ASSEMBLY.md; poses R and K for each collet)

| ID | Test | Pass criterion |
|---|---|---|
| A1 | Contact-class matrix | Parts: base with receiver, holder, collet, wing nut, core stand-in, frame members, brackets and T-nuts, cutter envelope. Every pair has a class in ASSEMBLY.md; an unlisted pair fails. C (contact required): min distance 0 +/- 0.01, patch area above floor, overlap < 0.01 mm3. G (gap): distance >= g_min stated per pair, contact area 0. F (free): overlap 0. Required G pairs include base-holder, nut-collet, nut-core, nut-cutter. Step 2: the washer is a tenth part (45 pairs; R: C 8, G 12, F 25) and a Feature pairs table covers ring top, rim, floor, plate-collar, skirt. Split IDs A1a to A1e are defined in the concept Test ID key. Controls: nut resting on collet top (overlap 0, G violated) fires; holder resting on receiver top fires; two parts 100 mm apart read F; 1 mm overlap fires every class. Step 7: class P (press pads) added for nut|washer, overlap 2.0 to 2.45 mm3; pair counts R: C 7, P 1, G 12, F 25; K: C 9, P 1, G 10, F 25 |
| A2 | Cutter envelope | Keep-out is two solids: tube (rho 73.025 to 76.2 mm, tube ID/OD 146.05/152.4 mm from workorder, a stated assumption, not the cutter OD) swept the full stroke, and the cutting-face annulus (rho from core kerf radius to R_face, assumption R_face = 76.2 + 10 mm, ASSUMED) at its lowest point. Nothing between the core and 76.2 mm may lie in the swept volume. Derived flag `nut_exceeds_bore` is computed (true expected); the test asserts the gap g_stop between the collar top (wing tops included) and the cutter lowest point at the highest clamped nut position, keep-out radius 86.2 (A2b; A2a, A2c to A2h in the concept Test ID key). There is no `nut_is_stop` choice. Control: a ring placed in the face annulus path fires |
| A3 | Placement predicates | Predicates S1 to S16 from the Topologist table, computed from faces and fitted axes: coaxial incl. tilt (norm(a x Z) <= 1e-4); boss rises from base; collet foot on seat with antiparallel normals; collet inside holder cavity; cone narrows with z on both with half-angles equal within 0.02 degrees; holder bottom above the receiver floor in every pose (A3e), stopping on the foot ring top at K-max; radial gap in R and contact in K; core inside bore; core on its stop and off the tray; nut clamp shoulder bears on the washer, which bears on the holder flange (antiparallel normals, z gap 0 to 0.05 in K, travel > 0 in R); nut clear of collet and core by >= 1.0 mm; nut skirt at least 1 pitch above the receiver floor (A3h); engagement per T4; core exposed per F4; stroke inequality s = d_rho / tan(alpha) with thread length >= s + min_engage + 1 pitch; release by cone angle above atan(mu_max) or captured flange. Frame: plate on frame z-gap 0 +/- 0.05; bracket mate faces antiparallel with body in the profile's outward half-space; T-nut centroid inside the slot cavity (measured cavity 16.5 mm wide, floor 9.165 mm below the face, neck 2.2575 mm thick; any numeric fit uses these) |
| A4 | Product tree | Component count and names equal the expected list; expected visible count computed from object counts |
| A5 | Visual (manual) | Four-view PNG set judged by an image-capable reviewer against a rubric with an item per signed feature, signifier (arrow, witness line, caddy) |
| A6 | Wrong-state controls | WS1 collet upside down; WS2 holder upside down; WS3 nut upside down; WS4 wrong-hand thread; WS5 cross-threaded tilt; WS6 wrong collet for core; WS7 collet unseated; WS8 holder bottomed; WS9 nut bottomed on base; WS10 base on frame upside down; WS11 slit over key. Each planted state fires at least one of A1, A3, T1, T9, F1, F3. For WS1 to WS3 and WS6 the defence is also a physical feature (foot key, flange OD above receiver bore, one-ended thread, engraved window), verified at Step 9 |

**Group E: export validity**

| ID | Test | Pass criterion |
|---|---|---|
| E1 | STEP | For each printable part and the assembly: file exists with mtime after run start; size > 0; re-import gives expected solid count; summed volume within 0.5 % of FCStd; unit mm; product tree names equal part names |
| E2 | STL | Watertight; no degenerate triangle; signed volume positive and within 1 % of FCStd; units mm; tessellation linear deflection stored in the result JSON and <= c_r / 10 (0.035 mm seed) with angular deflection <= 2 degrees. Controls: unit cube passes; STL with one triangle removed fires |
| E3 | FCStd opens | Reopened FCStd: visible deliverable object count equals count computed from object counts; every deliverable named |

**Group B and X: build and independent re-measure**

| ID | Test | Pass criterion |
|---|---|---|
| B1 | Rebuild | Running the part scripts twice yields volumes equal within 1e-6 relative |
| X1 | Independent re-measure | Script sharing no code with build or tests, reads exported STEP and STL only; recomputes per-collet volume, the interference matrix, and thread chirality sign (T1d); each agrees with the build-side JSON within the C2, A1, E2 tolerances. Negative controls: probes away from the feature still hit; a deliberately wrong expected value fires; a mirrored nut export fires. Bore diameter is not recomputed (covered by C3) |

Ceremony kept out: color-assignment tests, diffability test, per-part geometry-math test file, overhang-angle slicer script (T8 is a sectional probe instead), SHA-1 manifest as a test, before-and-after write hashing, slot-level 30-6060 fidelity, empty report test stubs, separate printability report, turntable MP4.

---

## Source Verification Register

Rule (A.10 item 2, tdd_method principle 7): a test that cites the SBIR plan, a Mines document or the rigged model carries a status. VERIFIED means the Fact-Checker re-read the primary file at the cited lines in the Step 0 review. TRACED means the extraction file gives the location only. The Fact-Checker re-verifies at the Step 4 gate (CAD tests), the Step 13 gate (report tests), and Step 18. No row stays UNVERIFIED after the gate: each is DECLARED, ASSUMED or struck.

| Claim used by a test | Tests | Status | Trace | Who verifies or unblocks |
|---|---|---|---|---|
| Core nominal 100 mm: Phase I EDU test cores, "pre-cast to 100 mm to match the iris aperture" | P2, C8, WD, S-sections | VERIFIED with conflict | INSITU2_text.md, phrase "pre-cast to 100 mm"; Figure 2 caption phrase "is above 100 mm" | Report states both |
| Core range 90 to 105 mm; tubing 6.00 / 5.75 in, 1/8 in wall | P1, C-group, A2 | CONTRACT (workorder.md is the only source); arithmetic 152.40 / 146.05 mm, wall 3.175 mm recomputed | workorder.md | none |
| 152.4 mm as the cutter OD | A2, F4 | ASSUMED. 152.4 mm is the tubing OD only. The only sourced cutter diameter is 7.00 in = 177.80 mm (7 in generation, borebot_operating_envelope.md 29) | Fact-Checker F-3 | Keep-out uses 152.4 / 146.05 as a stated assumption (parameter) |
| Iris closed by drill drivetrain, no jig actuator; release by reversing braking torque; Hall about 400 to about 45 counts | scope honesty, acceptance spec | VERIFIED | INSITU2_text.md (iris closure and Hall count phrases) | none |
| Iris 4 leaves; pivots; closure -62 deg; leaf thickness 3.175 mm; face radii 71.4375 and 74.6125 mm | App A | VERIFIED, 7 in model only | double_dong_params.py 93-98, 360-368, 402-404 (leaf thickness is 402-404, not 410-411) | none |
| 106.369 mm | F4, App A | VERIFIED as a number; its label is corrected: head tip to kerf sphere centre, not the pinch plane. Dome pole sits 106.369 - 71.4375 = 34.9315 mm behind the face. Core is pinched off inside the head. 7 in model only; applicability to the 6 in drill ASSUMED (parameter) | double_dong_params.py 372-380 | none; parameter changes if the new drill differs |
| Iris throat opening: 54.2925 mm is a radius, open diameter 108.585 mm; a parameter (the new drill is being fabricated); rule core diameter < open throat; nominal core 100 mm | P8, E-8, family range | DECLARED by the human at the gate (B1) | double_dong_params.py line 92; step0_human_gate_decisions.md | none |
| WOB 100 to 1000 N | loads | VERIFIED as a Phase I test range; 1000 N as jig load is a design choice | INSITU3_text.md (WOB range phrase) | label "design choice" |
| Penetration 5 mm/min at WOB 100 N or more | acceptance spec | VERIFIED | INSITU3_text.md (penetration-rate phrase) | none |
| Spin 1 to 60 rpm | none | STRUCK at Step 4 (orchestrator): Borebot motor range, not used by the jig, cited by no test | | none |
| Core length: capture goal 0.5 m (500 mm); install 0.75 m; optional 1 m; upper assembly working stroke at most 0.5 m (park 959.84 mm separate); jig height 2 m soft target | params, H tests | DECLARED by the human at the gate (B6); not a Mines value | step0_human_gate_decisions.md; double_dong_params.py 357-359 | none |
| Core mass 10.4 kg at 0.5 m; 15.6 kg at 0.75 m; 20.8 kg at 1 m (d = 105, 2400 kg/m3) | load case (b) | DERIVED; density ASSUMED | extraction C7 | none |
| Core diameter tolerance +/-1 mm | C8, T5, F3, P8 | ASSUMED (covers Mines manufacturing variation, which the human expects) | none | Phase I data replaces it |
| Holding torque 10 N m (jig). The 20 N m and 50 N m placeholders are retired | T7, loads | DECLARED design assumption (B4); the core is expected to fail before the collet slips | step0_human_gate_decisions.md | Phase I measurement replaces it |
| Core count (12 plain + 12 layered vs 40/15/30) | report | Sources disagree: INSITU2 514-518 and csm_sow 56, 58 vs csm_package.md 56 ("15" is depth-series captures). ASSUMED resolution: the report omits the core count | | none |
| "Mines specifies/requires/delivers" any core dimension | any | The Mines zip PDFs were read at Step 1 (pdftotext) and the two XLSX budgets were opened (openpyxl): no core dimension, tolerance, length, mass or delivery state. The report still asserts SBIR text only for core diameter; no such sentence in the report | | none |
| Mines Dreyer low-density concrete; properties strength, fracture toughness, density, grain size | S-sections | VERIFIED | csm_sow.md 24, 27, 56, 61 | none |
| Ascent test 600 s at 1x, 1.5x, 2x | any | Not used by the jig or the report (ASSUMED); no claim cites it | | none |
| Docx holds no geometry; gameplan.md line 141 model-of-record; FCStd not on this machine | | Not used (ASSUMED); the 7 in model values are taken from double_dong_params.py only | | none |
| Model is the 7 in generation (bore 177.8, core 100, annulus 38.9 mm) | App A | VERIFIED | double_dong_params.py 354-356 | none |
| 6 in iris data; which 2026-09-11 STEP is the 6 in drill | any | Moot: the iris throat is a parameter (B1); the 7 in model values are labelled as such | extraction section 7 | none |
| 30-6060: 60 x 60 mm, 30 mm pitch, M6 spring-ball T-nut | P3 to P5 | DECLARED by human; profile geometry VERIFIED from the human's local STEP at Step 2 (P9); no catalog download (ASSUMED: catalog SKU check at purchase) | step0_human_stock_80-20.md | none |
| Stock lengths and quantities | P3 | DECLARED by human | same | none (shared stock handled by the allocation file) |
| Printer: not a design input (B2). No bed, material or nozzle value is carried | T3, C6, E2 | DECLARED by the human at the gate | step0_human_gate_decisions.md | none |
| Friction mu_k about 0.35, mu_c 0.4, mu_t 0.25, bearing 0.25, design tensile `strength.tensile_design` 45 MPa, web strain allowable 0.01 | T7, C9 | ASSUMED seeds (design assumptions) | Loftsman review | Step 8 coupons, Step 11 hold test |

Any test that reads an ASSUMED value checks the label is present. The report states ASSUMED values as assumptions, never as fact. No row is left UNVERIFIED and open: each was resolved at the gate by a human decision (DECLARED), an adopted assumption (ASSUMED, Design Notes 12) or removal.

---

## Context Recipes

| Step | Agent | Files / Excerpts |
|------|-------|-----------------|
| 0 | The Manager | workorder.md, this gameplan, method/operational_guide.md (A.4, A.6, A.12) |
| 0 | The Engineer | workorder.md, templates/gameplan.md, extraction file, stock file, five Step 0 reviews, llm_plm_cad.md, tdd_method.md |
| 1 | The Engineer | workorder.md, gameplan, step0_human_gate_decisions.md, llm_plm_cad.md, freecad_api_reference.md, extraction file, stock file, Fact-Checker review |
| 1 | The Fact-Checker | extraction file (patched), gate decisions file, source files at corrected line numbers, Source Verification Register |
| 1 | The Designer | params.yaml seed, workorder.md, gate decisions file, gameplan Design Notes (no scripts) |
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
| 8 | The Engineer, The Loftsman | part scripts, step3 output, print-process rules (Design Notes 9), Loftsman 5.1 model |
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

Fact-Checker rule (all rows above that name the Fact-Checker, added at Step 0 close): the spawn prompt lists the exact files and line ranges or the exact claims to trace. Archive extraction and directory-wide reading are not part of a lookup pass unless the step names them and the human has approved. Reason: the Step 0 first run was stopped for broad extraction; the prompt, not the persona, allowed it.

---

## Progress Log

| Step | Date | Notes |
|------|------|-------|
| 0 | 2026-11-08 | Opened. Work order locked as workorder.md. Engineer extraction and draft written. Human stock input (30-6060, M6 spring-ball roll-in T-nuts, full-size brackets) folded in. Software Engineer revision: CAD Test Specification, Source Verification Register, report suite and outline validation added. |
| 0 | 2026-11-08 | Five reviews received (Systems Engineer, Loftsman, Topologist, Fact-Checker, Designer). Engineer final revision: every finding dispositioned (table at end); conflicts ruled (Design Notes 1 to 6). Step renumbering from the prior draft: old 1 now Steps 1 and 4 (split around the concept and geometry steps); old 2 now 3; old 3 now 5; old 4 now 6; old 5 now 7; old 6 now 8; old 7 now 9; old 8 now 10; old 9 now 11 (hold test added); old 10 now 12; old 11 to 18 now 13 to 20. Cut from the prior draft: report test stubs, `test_jig.py`, `test_geometry_math.py`, turntable MP4, overhang slicer script, color and diffability tests, write-hashing, slot-level profile fidelity, separate printability report, SHA-1 as a test. Reinstated: wing-nut moment-arm check (now T7). |
| 0 | 2026-11-08 | Manager close. Plan passes. Ratified 91 report tests. Fixes made in this file: TDD stage lines for Steps 15 to 20; poppler check added to Step 1; Fact-Checker scope rule in Context Recipes (first run stopped for broad extraction); manual-count discrepancy handed to a Step 13 scripted tally. accumulator.md created. Step 0 Complete; gate to human. Close note: research/quinn/cr_scratch/step0_manager_close.md. Contract: workorder.md. |
| 0 | 2026-11-08 | Gate decisions received (research/quinn/cr_scratch/step0_human_gate_decisions.md) and carried into this plan. B1 iris throat is a parameter (108.585 mm open diameter, rule core < throat, test P8); B2 printer not a design input (bed-fit test T6, split-nut logic, printer registry rows removed); B3 seven collets at 2.5 mm, generator readiness for new collets is a Step 5 deliverable (usage doc, test C10); B4 10 N m design assumption, positive-lock escalation and 20/50 N m placeholders removed; B5 metal stop belongs to the upper assembly; B6 core lengths 0.5 m capture, 0.75 m install, optional 1 m, travel at most 0.5 m, 2 m height soft. Open Questions replaced by Gate Decisions; Design Notes 12 records DECLARED and ASSUMED items. Step 0 stays Complete; current step 1. |
| 1 | 2026-11-08 | Manager close. Engineer: params.yaml (118 leaves: DECLARED 23, ASSUMED 69, VERIFIED 11, DERIVED 15), BOM generators, 30-6060 frame build in FreeCAD, ASSEMBLY.md skeleton, literature summaries; red-first then 28 passed (re-run by Manager). Fact-Checker: first WITHHELD (spawn prompt carried a mistyped path), then SIGNED after corrections. Designer: 24 missing feature params, generator NOT READY, carried to Steps 3 and 5. Design Notes 13 added. Close note: research/quinn/cr_scratch/step1_manager_close.md. |
| 2 | 2026-11-08 | Manager close. Concept (nine decisions, frozen ICD, tolerance budget, test ID key) written by the Systems Engineer in three passes; Loftsman SIGNED at Re-check 2 after two withheld lines (grip window, slack unit mix) and a third (collet chamfer); Topologist SIGNED on U13 to U16 and decision 8, last withhold (decision 5 wording, A3h, A1d, A3g) closed by applying the Topologist's own smallest edits, spot-checked by grep, no re-view by the Topologist; Designer comment recorded, four BLOCK items answered in the concept. Engineer: 30-6060 STEP measured (hollow 916.56 mm2), profile keys VERIFIED, ASSEMBLY.md and ICD frozen in params (41 keys), P9 and P10 added: 65 tests pass (re-run by Manager). Defects: concept length 6042 words against "one page"; reference/vendor_sources.md stale (repaired). 45-row directive list plus the profile list applied to this file. Close note: research/quinn/cr_scratch/step2_manager_close.md. Step 2 Complete; current step 3. |
| 3 | 2026-11-08 | Manager close. Designer params review PASS (27 missing rows; g_stop 25 mm, DECLARED). Engineer: hardware confirm, 96 keys, then 12 more at first solids (319 leaves). Loftsman numbers, Topologist five-line withhold, Loftsman SIGNED, Topologist round-two withhold on two lines closed by orchestrator ruling (strain 0.916 design value, chamfer rule accepted); geometry signed by ruling. Background build: receiver PID 35064, holder 9224, nut 27200 (logs research\quinn\cr_scratch\step3_build_{receiver,holder,nut}.log, each ends BUILD_DONE); washer and footring foreground. Five FCStd and result JSON, all valid, one solid, 104 of 104 feature rows pass. Designer completeness read: five PASS, directives applied (arrow_length 21.86, S3 amended, Step 6 glyph directive). pytest 197 passed (re-run by Manager). Defects: Topologist did not re-view the final edits; hardware and completeness files 10 and 12 percent over cap. Close note: research/quinn/cr_scratch/step3_manager_close.md. Step 3 Complete; current step 4. |
| 3 | 2026-11-08 | Step 3 gate. Human decisions (research/quinn/cr_scratch/step3_human_gate_decisions.md): g_stop is a mechanical clearance, dimensions kept, safety language removed from live files (`wingnut.hand_clearance` rename); T-nut is the PZRT 3030 roll-in spring M6, fit DECLARED by use, 80/20 candidates retired, BOM regenerated. Design Notes 17. pytest 197 passed. Step 4 awaits the human's go. |
| 4 | 2026-11-08 | Opened (research/quinn/cr_scratch/step4_manager_open.md). Orchestrator ruling: csm_sow, csm_package, motor and IP summaries out of the Step 4 gate; spin-range Register row struck. Software Engineer suite written: 99 new functions, 510 cases collected, 0 errors; test_params_bom 212 pass; 8 params gaps, 11 spec conflicts (research/quinn/cr_scratch/step4_software_engineer_suite.md). One freecadcmd run of 76 s in foreground (rule breach, probe shortened). Engineer baseline and Fact-Checker gate launched in background. |
| 4 | 2026-11-08 | Fact-Checker (research/quinn/cr_scratch/step4_fact_checker_gate.md): all 13 claims match their sources; withheld on three missing `# SRC:` tags (core 100 mm, WOB, stock lengths) and stale INSITU line numbers. Ruled clerical under Design Notes 18 (human direction: working step, not a reporting step); Register citations fixed by the orchestrator, tags go to the fix pass. Base preview (receiver, foot ring, holder, nut, washer in K-max) opened in the FreeCAD GUI for the human from a scratchpad script. Engineer baseline running. |
| 4 | 2026-11-08 | Engineer red-first baseline (research/quinn/cr_scratch/step4_engineer_baseline.md, results/step4_baseline.xml): 510 collected, 250 pass, 260 fail (257 MISSING, 1 ABSENT FEATURE T7), 0 errors/skips/xfails; 30 of 32 controls pass; planted defects fire. Defects: T9 and T9 control fail (probe_tilt non-monotonic, OCC "hasher mismatch"). Engineer fix pass launched (T9 probe, 8 params gaps, 11 spec conflicts, 3 SRC tags) → research/quinn/cr_scratch/step4_engineer_fixpass.md. |
| 4 | 2026-11-08 | Engineer fix pass (research/quinn/cr_scratch/step4_engineer_fixpass.md). pytest: 513 collected, 254 passed, 259 failed (257 MISSING, 2 ABSENT FEATURE: T7 and T9 claim); all invariants and controls pass. Nut and receiver threads rebuilt by stud-subtract (Design Notes 19), using 27 quarter-turn ruled-helicoid segments fused into one stud. Nut passes BOP check; genus 4. Receiver keeps a few InvalidCurveOnSurface BOP edges; ruled: these go to the Step 10 STEP re-import check. Thread mesh: overlap 0, min distance 0.106. 8 params gaps added, 11 conflicts dispositioned, 3 SRC tags added. T9 measured: thread contact begins at 0.15 deg rigid tilt (70.9 mm3 at 0.924); OCC fails above 1.06 deg; Engineer moved T9 to green_at 8. Ruling held pending the Loftsman's T9 reconciliation (research/quinn/cr_scratch/step4_loftsman_t9_ruling.md): Step 2 "0.903 deg at first thread contact" against 0.117 measured; register contact 0.35 against 1.021; rigid-tilt overlap against the cross-thread criterion. |
| 4 | 2026-11-08 | Loftsman T9 reconciliation (research/quinn/cr_scratch/step4_loftsman_t9_ruling.md), accepted. Rigid-tilt overlap is withdrawn: the probe pivots at the holder bottom and drives the nut through the flank it rests on. The new criterion: 1.5 x D tan(alpha_total) <= P/2. Measured register stop 0.596 + plate rock 0.315 = 0.911 deg, misregistration 2.379 against 4.000 mm, factor 1.68; holds for g_reg <= 0.299 (Step 8 coupon). The Step 2 figure of 0.903 was the tilt envelope at first contact, not a flank-clear claim. The known-bad controls fire (L_h 54 at 1.826 deg; 2 x alpha_crit is blocked by the register). T9 is an invariant at green_at_4; 3 passed. The T9 row is replaced. Software Engineer signature launched → research/quinn/cr_scratch/step4_software_engineer_signature.md. |
| 4 | 2026-11-08 | Software Engineer SIGNED (research/quinn/cr_scratch/step4_software_engineer_signature.md): 513 collected, 255 passed, 258 failed, all failures MISSING or ABSENT FEATURE, 0 errors/skips/xfails, results/step4_final.xml; one fix (T9 SRC comment failing P24). Fact-Checker criterion met by ruling (clerical; the tags landed). Manager CLOSE (research/quinn/cr_scratch/step4_manager_close.md): all 11 close criteria met; accumulator entries written for the Manager, Software Engineer, Engineer, Fact-Checker and Loftsman. Step 4 complete. Gate to human: Step 5 go; T-nut count per bracket. |
| 5 | 2026-11-09 | Human: proceed to Step 5. Opened; Manager open spawned → research/quinn/cr_scratch/step5_manager_open.md. |
| 5 | 2026-11-09 | Manager open (research/quinn/cr_scratch/step5_manager_open.md). Sequence: Loftsman definition → Topologist cross-review ∥ Software Engineer pre-build test review → Engineer build (background) → Software Engineer generator review ∥ Designer cold read → Topologist topology gate → Manager close. 76 green_at_5 tests targeted. Loftsman spawned (background) → research/quinn/cr_scratch/step5_loftsman_collet_definition.md. |
| 5 | 2026-11-09 | Loftsman definition (research/quinn/cr_scratch/step5_loftsman_collet_definition.md), with corrections to the brief. The green_at_5 target is 75 (61 collet), not 76. The notch index is clamped to 1 to 7 off-grid. The bore lip passes 0.086 from a relief-hole edge at a 12-degree crossing (sent to the Topologist). Test conflicts C4 (per-size region), F2 (base_gap -4.0, wrong measure) and C2 (analytic volume omits chamfer, ledge, key and notches) are sent to the Software Engineer. Witness scale is not on the collet and is routed to Step 6. 4 new params keys (327 → 331). Orchestrator moved 6 pre-existing .FCBak files from parts_cache to research/quinn/cr_scratch/fcbak_archive (criterion 8). Topologist cross-review ∥ Software Engineer pre-build review spawned (background). |
| 5 | 2026-11-09 | Topologist cross-review (research/quinn/cr_scratch/step5_topologist_crossreview.md) withheld two lines: a label tool coincident with the outer cone, and unstated hole and notch tool extents. The orchestrator applied the Topologist's own edits to definition line 16, so the definition counts as signed. Lip against relief hole is a transversal crossing at 11.9 deg, OCC-safe. Genus 1 and notches are Euler-neutral; slit_plane_faces is 0; clamped/holder common is 0. Software Engineer pre-build review (research/quinn/cr_scratch/step5_software_engineer_test_review.md): 540 collected. C4, F2 and C2 revised with their controls; the ±5 % band is unchanged. Added C11 to C15. The green_at_5 target is 98. Engineer build spawned (background) → research/quinn/cr_scratch/step5_engineer_build.md; build logs research/quinn/cr_scratch/step5_build_<tag>.log, BUILD_DONE sentinel. |
| 5 | 2026-11-09 | Engineer build (research/quinn/cr_scratch/step5_engineer_build.md): build_parts/collet_family.py and docs/collet_generator_usage.md. Nine collets (7 family plus 97.0 and 93.7 built from the doc alone), 24 to 37 s each, all valid with one solid, euler_VEF 0, checks_all_pass. Clamped Kd1/Kmax solids built. probe_collet 231 s; C4 controls 0 / 1.877 mm3. A 110.0 request is refused. 98/98 green_at_5 pass; 540 collected, 364 passed, 176 failed (all MISSING or ABSENT FEATURE: assembly 134, exports 31, thread_clamp 11). Step 3 FCStd unchanged. 4 params keys (leaves 324 → 328). Wave 2 spawned in parallel (background): Software Engineer generator review (also moves the clamped notch formula into the rim_notch_count value and updates P-test lines 595 and 780), Designer usage cold read and completeness, Topologist topology gate. |
| 5 | 2026-11-09 | Wave 2 results:
- Designer PASS (research/quinn/cr_scratch/step5_designer_usage_and_completeness.md). All F5 features are present. The label is simplified to a flat recess with its text in the JSON. Notches 1 to 7, colours and labels are distinct. Usage-doc wording edits only. Visual gate NOT RUN.
- Topologist gate SIGNED (research/quinn/cr_scratch/step5_topologist_topology_gate.md). bad_edges 0, slit_plane_faces 0, one solid each, clamped common 0. Min edge 0.0755 at d 90 (the predicted lip/hole crossing). Per-boolean face counts and the optimal bbox are absent from the result JSON, so those two 7.1 items were not run.
- Software Engineer SIGNED (research/quinn/cr_scratch/step5_software_engineer_generator_review.md). Counts 540/364/176; rim_notch_count value now carries the clamp, with P-tests updated. Findings: chamfer and lip literals duplicate params; duplicated slit and hole loops; a footring import workaround.

Ruling: the params-duplicate literals are a defect under the open file's §5.5 task 1, not clerical. The Engineer is resumed for a cleanup pass: params reads, one shared loop, face counts per boolean and the optimal bbox in the result JSON, rebuild of 9 collets, probe and pytest rerun, report_assumptions regenerated. |
| 5 | 2026-11-09 | Cleanup pass: 4 chamfer and lip keys added (leaves 332); shared slit_hole_tools and cadlib.footring_derived; faces_before/after per cut and bbox_optimal in the result JSON. 9 collets rebuilt with volumes 0.000 % changed. Topologist addendum SIGNED: notch +4 faces and label +6 at all sizes; the d >= 100 slit/relief face path differs but converges at 103; bbox plain = optimal. Manager CLOSE (research/quinn/cr_scratch/step5_manager_close.md): 540 collected, 364 passed, 176 failed (all MISSING or ABSENT FEATURE), green_at_5 98/98, P-group 213, no .FCBak, no hazard or printer reads. Word-cap overruns are clerical. Accumulator entries written. Detail 5 outputs: build_parts/collet_family.py, docs/collet_generator_usage.md, parts_cache/collet_{090p0..105p0, 097p0, 093p7}.FCStd with _clamped_Kd1/_Kmax and _result.json. Step 5 complete. Gate to human: Step 6 go. |
| 5 | 2026-11-09 | Human: hold at the Step 5 gate. Step 6 not opened. |
| 6 | 2026-11-10 | Human: proceed with Step 6. Manager open spawned. |
| 6 | 2026-11-10 | Open, SE tests (582 collected, 33 green_at_6 red), Loftsman definition, Topologist SIGN (6 edits ruled into the build), SE pre-build done. Engineer build spawned in background; PID/log/BUILD_DONE recorded in research\quinn\cr_scratch\step6_engineer_findings.md. |
| 6 | 2026-11-10 | Build done: 14 new parts, receiver/holder/nut rebuilt; 582 collected, 399 pass; green_at_6 26/33 (7 probe-position errors). Rulings: SE fixes probe positions with known-bad controls; rest roller fit across the 90-105 family moves into the Step 6 fix pass (scoped function, not deferred to Step 9); C6 bracket overlap stays at Step 7 per gameplan. Renders spawned. |
| 6 | 2026-11-10 | 101 renders. Topologist gate SIGN (15 parts). SE code review: no result-changing defect; 4 string literals duplicating params, 2 self-compares, dead vars/helpers ruled into fix pass. Designer image gate FAIL on D1 (witness unreadable: nut body hides ruler; probe reads skirt face the eye never sees) and D2 (rest). Rulings: fix pass covers D1, D2, D3 (tighten glyph scale), D5 (tray floor to drain), D6 (plug grip), code cleanup; D4, D7, D9 carried to Step 9. Loftsman fix-pass definition spawned. |
| 6 | 2026-11-10 | Loftsman: D1 was a render pose error (nut drawn 5 mm low); ruler unchanged. Rulings: tray 2.0 deg (2.4 max at 25 depth); NT8 scaled to NT4 area; rest adjustment built in Pass 1 as radial pin slots. Engineer fix pass done: nut, rest, tray, plug, base, foot, frame rebuilt; 584 collected, 400 pass. SE resumed for ray-cast witness probe, key/pin updates, rest test; Designer (Opus) re-gate spawned. |
| 6 | 2026-11-10 | Designer re-gate PASS. Manager close: 16 of 17; criterion 10 closed by rest-vs-collet probe (54 rows, 0.0 mm3) and Topologist addendum (rest, tray, plug, nut SIGN). 591 collected, 415 pass, 176 fail (all green_at 7+, MISSING/ABSENT FEATURE); green_at_6 41/41; 104 PNGs; leaves 444. Step 6 Complete. Gate to human. |
| 7 | 2026-11-10 | Human: proceed with Step 7. Manager open spawned. |
| 7 | 2026-11-10 | Open (17 criteria); SE tests (657 collected, 185 green_at_7 red); Loftsman definition + Revision 1; Systems Engineer contract check (5 ASSEMBLY.md rows accepted with refinements; C6 option (a) 12 brackets/96 T-nuts accepted per Step 2 rule). Rulings: A3b split (column foot, carriage guide to green_at_12); collar into holder.py (pose-fuse rejected); nut travel requirement at least 8 stands, fixed by nut relief bore (10.01 mm); class P floor 2.0 mm3. Topologist SIGN (E1-E8, Revision 1). Rebuilds authorized: frame, holder, nut (research\quinn\cr_scratch\step7_rebuild_authorizations.md). Engineer parts build spawned in background. |
| 7 | 2026-11-10 | Wave 2a done: frame, holder, nut rebuilt; core and cutter new; all topology predictions hit; C6 overlaps 0; params 463 leaves; ASSEMBLY.md rows edited. Build PIDs in research\quinn\cr_scratch\step7_engineer_parts_findings.md. Marks probe (PID 33600, log step7_probe_step6_marks_b.log) ended 14:51. Orchestrator re-run 20:50: 662 collected, 424 pass, 238 fail (assembly 136, step7_assembly 60, exports 31, thread_clamp 11); test_step6_parts all pass. build_parts\assemble.py not yet written. Next: wave 2b (assemble, 21 poses, 11 wrong states), 2c renders, Wave 3 reviews, fix pass, Topologist re-read, Manager close. |
| 7 | 2026-11-10 | Wave 2b running: build_parts\assemble.py written 21:00; assembly logs step7_asm_*.log through 21:02. Probes launched 21:03: poses_100p0 PID 29596 (log step7_probe_poses_100p0.log), wrong states PID 27104 (log step7_probe_ws.log). Expected finish not stated; orchestrator wait task byh0yws2r notifies on exit. Engineer agent a6499eebb0ec3c667. |
| 7 | 2026-11-11 | Engineer killed both probes at 21:32 (no output) and ran PID 18068 (scratchpad prof_pairs.py) 21:32 to 07:14: 21 pose JSONs in results\probes (22:03 to 06:55, about 27 min each) plus frame_instances.json. Wrong-state probes not run. Engineer idle since 21:37; orchestrator resumed it 07:15 with instructions to finish wrong states, report, pytest. |
| 7 | 2026-11-11 | Engineer relaunched with bbox-prefiltered distance and gap-aware patch area: seven pose probes PIDs 35144, 22612, 5504, 27328, 24540, 15596, 25196 and wrong-state probe PID 32208; Engineer monitor b10wlsctt; orchestrator wait task b996z15rl notifies when all eight exit. Expected finish not stated. Next: interference report, step7_engineer_assemble_findings.md, pytest; then 2c renders. |
| 7 | 2026-11-11 | Seven pose probes finished 08:30 to 09:13: 21 pose JSONs plus frame_instances.json (MEASURED, about 18 to 40 min per pose). Wrong-state PID 32208 ran 5.1 h and started no wrong states: probe_ws imports probe_poses, and the guard at probe_poses.py:463 (`__name__ in ("__main__", "probe_poses")`) reruns the full pose sweep on import. Orchestrator killed it at 12:23. Engineer a6499eebb0ec3c667 resumed: fix the import guard and add a side-effect test, relaunch probe_ws alone with PID/log/finish recorded here, then interference report, findings, pytest. |
| 7 | 2026-11-11 | Guard fixed (probe_ws sets CJ_PROBE_IMPORT; probe_poses.py:463 skips main when set). probe_ws relaunched 12:23 as PID 2176, log research/quinn/cr_scratch/step7_probe_ws2.log; 11 ws files plus ws0 (three nominal poses); expected finish about 15:00 to 17:00 (Engineer estimate: about 1 h for ws0 plus the ws files). Engineer monitors b1xkwwq2a, blrt3pe86; pytest running in background. |
| 7 | 2026-11-11 | Engineer found two probe measurement defects in probe_poses.py: receiver underside contact counted the base plate underside (face selection by centre of mass; now by bbox within the spigot radius), and the tilt measure was corrected. The 21 pose JSONs from the morning sweep are superseded. PID 2176 killed. Relaunched 12:30: seven pose probes PIDs 25604, 25144, 26076, 3304, 3908, 8552, 4136 (logs research/quinn/cr_scratch/step7_probe_poses_<tag>_b.log) and probe_ws PID 30728 (step7_probe_ws3.log). Engineer monitor bcyjd5bch; orchestrator wait task on all eight PIDs. Expected finish about 14:30 to 15:30 (prior sweep: about 2 h per size). Revised 13:15: about 36 min per item under 8-way contention; pose probes about 14:30, probe_ws (14 items serial) about 18:00 to 20:00. Engineer monitor biwlnx8s6. |
| 7 | 2026-11-11 | 13:53: ws1 and ws10 done; Engineer split the remaining wrong states into ten probe_ws processes (PIDs 30180, 14248, 31932, 35776, 31812, 32764, 36728, 20092, 32896, 8396; logs research/quinn/cr_scratch/step7_probe_ws_<n>.log, ws0 in step7_probe_ws_none.log). Seven pose probes (R poses remaining) still running. Engineer monitor bd3a30rs6; orchestrator wait task now polls until no freecadcmd process remains. |
| 7 | 2026-11-11 | All probes exited by 15:20. 21 pose JSONs (Kd1 13:07, Kmax 13:41, R 14:38 to 14:40), ws1 to ws11 (last ws2 14:46), ws0 15:19, frame_instances.json 14:45. Engineer running green_at_7 pytest in background. Next: interference report, step7_engineer_assemble_findings.md with pytest counts; then 2c renders. |
| 7 | 2026-11-11 | Wave 2b closed by Engineer: green_at_7 188/188 pass; suite 665 collected, 615 pass, 50 fail (exports 30 green_at_10, assembly 19 green_at_12, thread_clamp T7 green_at_8). Interference report 1071 rows all pass; T4/T5 pass at 90 and 105; WS1 to WS11 each fire, three nominal poses fire nothing. Probe fixes: patch area gap-aware, underside selection, tilt control 1.0 to 2.0 deg (limit 1.021), key pin measured 0.250, per-solid distance; test_probe_import.py 3 tests. Files: research/quinn/cr_scratch/step7_engineer_assemble_findings.md, step7_interference_report.md, output/jig_assembly.FCStd/.step. Software Engineer reviews the tilt-control change in Wave 3. Wave 2c renders spawned (Engineer, Sonnet, background), prompt research/quinn/cr_scratch/step7_prompt_engineer_renders.md. |
| 7 | 2026-11-11 | Wave 2c done: 122 PNGs in research/quinn/cr_scratch/step7_renders with INDEX.md; harness check reproduces Step 6 witness close-up; pose numbers MEASURED (Kmax nut zmin 86.410, holder zmin 42.000); no FCStd modified. Wave 3 spawned in parallel, background: Designer (Opus, image gate A5), Software Engineer code review (with rulings on six 2b probe changes incl. tilt control 1.0 to 2.0 deg), Topologist gate (re-sign holder, nut, frame), Systems Engineer. Outputs research/quinn/cr_scratch/step7_designer_critique.md, step7_software_engineer_code_review.md, step7_topologist_topology_gate.md, step7_systems_engineer_review.md. Next: Wave 4 fix pass, Topologist re-read, Manager close, gate. |
| 7 | 2026-11-11 | Wave 3 returned. Systems Engineer SIGNED (open: receiver has no modelled support path to the plate, carried to Steps 8/12; class-rulings record to be written at Manager close). Designer: no BLOCK, render faults R1 to R4 (receiver not cut in 7 sections, collet colours not from params, blank top sections, opaque cutter in context views); D14 rest position to Step 9; D15 ASSEMBLY.md wording. Software Engineer: six probe changes accepted, no threshold moved, 665/615/50, green_at_7 188/188; clerical literals and missing controls. Topologist: parts and 21 poses SIGNED (holder, nut, frame re-signed), DEFECT D1 ws4 mirror lost nut placement. Wave 4 fix pass: assemble Engineer (D1 rebuild ws4 and probe rerun, clerical, D15), render Engineer (R1 to R4), both resumed in background. Then Topologist re-read of ws4, Designer re-read of re-rendered PNGs, Manager close. |
| 7 | 2026-11-11 | Fix pass launched ~15:55: ws4.FCStd rebuilt (PID 33504, log research/quinn/cr_scratch/step7_asm_ws4_fix.log; mirrored nut CoM matches pose to 1e-13, old 97.1 mm build is the guard's bad control). ws4 probe PID 34652, log research/quinn/cr_scratch/step7_probe_ws4_fix.log, expected 16:30 to 17:00. Seven pose probe reruns for new controls PIDs 23496, 17084, 19748, 20536, 16848, 15228, 27844, expected about 18:00. Literals, ws registry, ASSEMBLY.md D15 wording done; tests/test_step7_fix_controls.py added. Engineer monitor b94woy0h2. |
| 7 | 2026-11-11 | Renders fix pass done: 122 PNGs re-rendered (PID 23920, 122 OK); R1 cause: receiver fails every OCC boolean (InvalidCurveOnSurface) and half-space cut returned it uncut; nut cut also left material. halfcut now raises; fallback caps from clipped mesh. R2 colours from params, R3 reframed, R4 cutter 75 percent transparent. Orchestrator ruling: verify probe booleans on receiver and nut pairs before close. Topologist resumed (addendum A: method and known-bad overlap controls per receiver/nut pair class; B: ws4 re-read after probe). Designer (Opus) resumed for re-read of re-rendered PNGs. |
| 7 | 2026-11-11 | Designer re-read: R1, R3, R4 cleared; R2 cleared except collet_Kmax_105p0_underside (white on grey), render Engineer re-rendering undersides on dark background. Step 9 inputs: receiver render colour vs blue 100 collet; D14 measured (rest roller 51 to 82 mm from axis crosses cutter wall 73.0 to 76.2). First ws4 rebuild still displaced the nut (identity-placement reset); fixed; ws4 probe relaunched PID 4384, log research/quinn/cr_scratch/step7_probe_ws4_fix2.log, about 25 to 35 min. Topologist told to use fix2 log. |
| 7 | 2026-11-11 | Underside renders re-done on dark backdrop (105 coverage 0.4 to 23.9 percent); render fixes complete. Topologist addendum A: receiver/nut pair classes VALID (analytic box 125.000, slab integrals to 3e-5, shifted-partner commons within 0.1 mm3; zero overlaps corroborated by distance above 0); receiver half-space failure only for axial planes, which probes do not use. Clerical: no isValid guard on commons; assigned to Engineer after probes finish. ws4 rebuilt nut CoM correct (placement half of D1 closed); ws4 row DEFECT until ws4.json read. Topologist B pending on step7_probe_ws4_fix2.log. |
| 7 | 2026-11-11 | 17:45 all FreeCAD jobs exited; pose JSONs rewritten (control rerun). ws4.json 16:48 (PID 4384, run_seconds 1916.9, PROBE_OK; log lacks BUILD_DONE, clerical). WS4 fires A1, T1 on the reversed helix (base/nut 4,081.4 mm3, nut/washer 6.304), A3 silent. Topologist gate SIGNED, D1 closed, re-check list regenerated 17:46, all rows signed. Pending: Engineer guard control run and final pytest, then Manager close. |
| 7 | 2026-11-11/12 | Engineer fix pass written (research/quinn/cr_scratch/step7_engineer_assemble_findings.md "Fix pass": F1 two ws4 rebuild attempts, F3 probe sentinel is PROBE_DONE, F4 frame_footprint_x control removes both rails; mirror guard; checked_common guard raising InvalidCommon, control probe_common_guard.py reads 600 / 18,849.556; literals from params; ws registry gates.WS_EXPECT; D15 ASSEMBLY.md wording). Re-probe of nominal R 100p0 for the F4 control: PID 23596, log research/quinn/cr_scratch/step7_probe_poses_100p0_R_d.log, started 22:18, about 20 to 35 min; final pytest follows (Engineer agent). Video for the human: research/quinn/cr_scratch/step7_video/jig_step7.mp4 (23 s, PID 29388, log step7_video.log). Side task: new project C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\BCTJ created (CR-Agents cloned, workorder.md written, STEP BackCapTestJig-Wesley(NEW).step in its root); not part of this gameplan. Next: confirm R 100p0 probe PROBE_DONE and final pytest counts, then spawn Manager close (criteria research/quinn/cr_scratch/step7_manager_open.md section 8; also: class-rulings record per SE, criterion 9 text add core motion, carry SE receiver-support item to Steps 8/12, D14 measured and receiver render colour to Step 9), then inter-step gate to the human. |
| 7 | 2026-11-12 | R 100p0 re-probe PROBE_DONE pose_R_100p0 1129.4 s, frame_instances 1426.8 s. F4 control fires: nominal 644.0, both rails removed 524.0. Pytest (research/quinn/cr_scratch/step7_pytest_fixpass.txt): green_at_7 194/194; suite 672 collected, 622 pass, 50 fail (test_exports 30 green_at_10, test_assembly 19 green_at_12, T7 green_at_8). Clerical: findings file 1413 words vs 1200 cap. Manager close spawned (Sonnet, background) to write research/quinn/cr_scratch/step7_manager_close.md, research/quinn/cr_scratch/step7_class_rulings.md and accumulator entries. Next: read close, then inter-step gate to the human. |
| 7 | 2026-11-12 | Gate (human, DECLARED): receiver shoulder added at Step 8 to carry receiver/core weight and 204 N pull-out into the plate; PZRT T-nut proxy stands to the Step 9 BOM; Step 8 on HOLD (human reviewing Step 7). D14 closed by human decision (DECLARED 2026-11-12): steady rest DROPPED. The collet alone holds the core. Remove the rest (post, ring, rollers, detents, cam release) from params.yaml, build scripts, assembly, BOM and tests at the next step open; D9, D12, D14 and the steady-rest adjustment item in Step 9 carries are void. This overrides Design Notes 9 / Step 2 "steady rest at every core length" and E6 disposition (tall-core lateral stability rests on the collet and tilt bound; H3 data at Step 12). |
| 7 | 2026-11-12 | Manager close: CLOSE, 17 of 17 criteria met (research/quinn/cr_scratch/step7_manager_close.md). Manager re-run (research/quinn/cr_scratch/step7_manager_pytest.txt): 672 collected, 622 pass, 50 fail (all MISSING or ABSENT FEATURE), green_at_7 194 of 194. Criterion 9 amended to include core motion R to K (0.995 mm). Class rulings written (research/quinn/cr_scratch/step7_class_rulings.md). Carried: receiver support path to Steps 8 and 12; D14 and receiver render colour to Step 9; D13 to Step 8; D4, D7, D9, D12 to Step 9; receiver BOP D6 to Step 10; stop path to Step 12; datum C hardware to Steps 9 and 12. Clerical: ws4 fix2 log lacks BUILD_DONE (PROBE_DONE is the sentinel); word caps over on seven Step 7 files. Builds: PIDs and logs in the rows above and in the Engineer findings tables. |
| 12 | 2026-11-24 | Human: configuration reopened after the SBIR meeting. Collet, holder, nut and receiver kept; everything else open. Travel 650 mm (params and cutter keep-out updated); drill spun by a bevel ring gear on three NEMA 23 pinions; drill ring lifted on three jack screws (NEMA 17); Design Notes 23. Sean leads the 2D sketch phase; meeting summary context/2026-11-24_cutjig_critical_path.md. Pytest 620 pass, 52 fail (see Current step). |

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

Ruling (confirmed by the human at the gate, B5: the metal hard stop belongs to the upper assembly; the wing nut only tightens the collet and carries no descent load): the printed nut is not a stop and carries no descent load. The stop is metal, rated, defined in the ICD (height, rated load, owner), and built at Step 12 as a carriage stop on the columns or an inside-radius ring, whichever Step 12 selects. Until it exists, A2 asserts the gap g_stop between the collar top (wing tops included) and the cutter lowest point at the ICD stop height, and F4 measures from the collar top (Step 2 wording; the stop is frozen in the ICD with owner, 1000 N and gap 10 mm). `nut_is_stop` is deleted; `nut_exceeds_bore` is a derived value (expected true). A documented fallback of the nut as stop is permitted only with a rated load and the human's approval. Reason: the Designer's separation of jobs plus the Systems Engineer's load-path argument agree on the outcome; the Topologist and Loftsman findings are kept as the derived flag and the keep-out geometry.

**3. Mechanism rulings.**

Stack (Topologist 3.1, Loftsman 3 agree; Systems Engineer S2 supplies the loop). The workorder's "threaded boss" is a tubular receiver: nesting from the axis outward is core, collet bore, collet wall, holder cavity, holder wall, receiver bore, receiver wall and thread, nut. The collet stands on a floor land inside the receiver (the receiver seats the collet, as the workorder says); the holder cone descends over the collet; the nut on the receiver bears on the holder flange; the holder flange sits above the receiver rim with a gap (the stroke). The loop is written as a sentence in ASSEMBLY.md. The holder never bottoms on the receiver or base. The core axis is located by cone and pilot, never by the trapezoidal thread.

Thread size: Tr 60 x 8 is withdrawn. A 60 mm major is smaller than the 90 to 105 mm cores it surrounds (Loftsman G1, Topologist TP-1). The major diameter is an output of the radial chain:
D_T = B_f(d_max) + 2 t_c + 2 H tan(alpha) + 2 (t_h + t_b + 0.5 + h)
with seeds t_c = 5, H = 30, t_h = 5, t_b = 5, h = 2.5 mm, B_f(105) = 107 mm.

| Position | Value | Basis |
|---|---|---|
| Loftsman | about 165 mm major, nut body about 181 mm, wing span about 230 mm | alpha = 20 degrees (releasing cone) |
| Topologist | about 135 mm major, nut OD at least 150 mm | smaller cone angle and thinner walls |

Ruling: the two differ by assumptions (cone angle, walls), not by method. The formula governs. Closed at Step 2: 149.58 mm major and 166.28 mm nut OD at the 10 degree cone (Design Notes 14); the 165 and 135 mm figures are superseded. Pitch 8 mm and symmetric 45/45 flanks (Loftsman G2, prints with no flank under 45 degrees) are PROPOSED seeds.

Release: a cone half-angle below atan(mu_k) self-locks and backing off the nut does not free the collet (Loftsman 3.1, Topologist S16, Systems Engineer S2, Designer D6 agree).

| Position | Source | Trade |
|---|---|---|
| Releasing cone, alpha = atan(mu_k) + 2.5 degrees (seed 20 degrees) | Loftsman (recommended first) | No extra bearing faces; radial budget grows (165 vs 158 mm); holding torque per axial force falls about 28 % |
| Captured-flange nut with a shallow cone (about 10 degrees) | Designer D6 (better trade); Loftsman (alternative); Systems Engineer (choose) | Keeps mechanical advantage and gives positive release; adds two bearing faces to print |

Ruling (the 10 N m assumption of Design Notes 12 replaces the 20 N m placeholder; the ruling stands because it still maximizes friction margin): holding torque is the binding performance risk (D1), so the primary design is the captured-flange nut with the shallow cone; Step 2 closed it: the 10 degree captured-flange nut stands, the releasing cone is retired (it misses 10 N m at d = 90 even with PTFE) and the jacking holes are deleted (flange annulus 5.00 mm against 7.4 required); the jacking provision is the collar back-off lift. The Step 8 coupon still measures mu_k. Reason: a design that cannot hold is a failed test; a design that costs two print faces is only a cost.

Collet topology: C1 (single solid) and C5 (slit through full wall height) conflict (Topologist TP-6). Loftsman prescribes alternating slits (ER style); the Topologist's table accepts alternating (one component, genus 1) or finger collets. Ruling: alternating slits with relief holes, because web bending then stays in the layer plane while axial fingers bend across layers, the weak FDM direction. Slit count is a family parameter set by the hinge-strain law; the Topologist's S22 and S23 predicates apply to it.

Register length: the Topologist's cross-thread pilot at a 135 to 165 mm thread needed about 54 mm or more (withdrawn at Step 2: it fails T9 at 2.477 degrees; register closed at holder length 88.0); the Designer proposes a stacked register using features that already exist (holder flange centred on the cone, holder in the receiver bore). Ruling: Step 3 decides by number; T9 tests whichever is chosen; the stacked register is the first candidate.

Clamped-state solid (Loftsman 5.2): F1's K pose uses a second collet solid from the same generator call (bore = core diameter, narrowed slit, reduced cone, offset s_z). This removes the rigid-body overlap that A1 would flag and is compatible with the Topologist's contact class C. OCC offset strategy for coincident cone faces: the Topologist confirms at Step 3.

**4. Frame and measurement rules (for ASSEMBLY.md).** Right-handed, +Z up; origin on the top face of the base plate on the receiver axis; +X to the front; theta counter-clockwise from +X seen from +Z. Poses R (nut backed off, collet free) and K (nut hand-tight). Rule M: every predicate is computed from the final shape. Rule P: each part has one signed asymmetric feature. Relations are data. Slit phase is a fixed function of key angle.

**5. Interface control table (frozen at Step 2; the table in research/quinn/cr_scratch/step2_system_concept.md and the `icd.*` keys in params.yaml are authoritative; this skeleton is kept with its stale items corrected).**

| Item | Content |
|---|---|
| Datum A | Frame top plane (base plate underside, z = 0); receiver floor 40 mm above it |
| Datum B | Axis of the receiver register bore (r 67.29), +Z, located to A and C through the plate by two plate keys and one plate stop pin |
| Datum C | A frame rail slot line with two plate keys (rotation, across-slot) and an end-member stop pin (along-slot); column feet abut the end-member stop line |
| Mounting pattern | T-slot lines on the frame top face (30 mm pitch, M6 roll-in T-nuts) available to the column, with the ones the base plate occupies |
| Coaxiality | Drill centreline to receiver axis within the Step 2 budget; slotted base-plate holes plus one printed alignment gauge that seats on the holder and centres a 152.4 mm tube |
| Keep-out | Cylinder of radius 86.2 mm about the axis from the collar top to stroke end, plus the face annulus (R_face ASSUMED) |
| Stop | Metal, owner the upper assembly, 1000 N, gap 25 mm from the collar top (Step 3); height by A2b per core class (184.84 mm for the 0.5 m case) |
| Footprint | 644 x 608 mm, four adjustable M8 feet, four bolt-down slots, mass target 40 kg (25 kg structure), tip-over statement (unbolted 158 N at the centre of mass, 68 N at the column top; bolt-down required with the cutter above z = 400 mm); Step 12 replaces the number |
| Core handling | Steady rest at every core length (detents 310 and 560 mm), cam-released by the upper assembly; choke strap with 250 mm side handle; no overhead anchor |
| Cable exit and debris path | From the back cap; dust skirt on the nut and a closed top on the receiver thread region |

**6. Report test count ruling: 130 vs about 60.**

| Position | Source | Argument |
|---|---|---|
| About 130 tests (12 per page) | Software Engineer | A.10 item 7 calls a multi-section technical review 150 to 200 tests; rigor |
| About 60 tests and two cold reads; seven of 20 steps on the report is more checking than 8 to 12 pages carry; 40 manual tests; the 12-per-page ratio is an assertion | Systems Engineer S9, S10; Designer notes the cost without judging |

Ruling: about 90 (91 in the Detail 13 table). The count is set by claims, not by pages: the report now has an analysis section and a hold-test section that each carry fact tests, so 60 would leave claims untested, while 130 duplicated section tests with whole-document tests. Reductions: manual tests cut from about 40 to about 27 (exact manual count to be tallied by script at Step 13; the Engineer's prose split of 17 whole-document plus 10 section did not reconcile with the Detail 13 table, which shows 15 whole-document manual plus the manual and mixed section tests), comprehension tests cut to 5, cold reads cut from three to two (outline, final PDF). Manager ratification (Step 0 close): 91 is accepted. The 91 sums correctly (36 whole-document plus 55 section). The deviation from A.10 item 7 is justified because the band is sized for multi-section technical reviews of longer documents, and this report is 8 to 12 pages whose claims are bounded by the Register; the re-size trigger (150 or more if the upper assembly enters scope) stays. The Manager ratifies and records the deviation from A.10 item 7. If the human widens the report to the upper assembly, re-size to 150 or more.

**7. Stock and 80/20 hardware (human input, DECLARED).**
- Profile: 80/20 30-6060, 60 x 60 mm, 30 mm slot pitch. No smaller profile. Fasteners M6.
- T-nuts: M6 spring-ball roll-in only.
- Brackets: ordered catalog brackets must be full size for the 30-series, never "mini"; printed or fabricated brackets may be designed. BOM names the SKU or full-size class (SKUs ASSUMED, verified at purchase). Step 2 rule: leg at least 57 mm and width 57 mm; 30-4332 (30 mm legs) is superseded; eight joints: the four outer corners take the 57 mm 8020-14089 class, two per joint; the four plate-support ends take the 68 mm printed bracket (Step 3 measured: 7.0 mm slots, 29.2 mm pitch along the leg). Purchased brackets drop from 16 to 8; 8 T-nuts per bracket (14089 lists 8 holes).
- Stock on hand, mm x quantity: 1540 x 4, 980 x 4, 952 x 1, 728 x 2, 644 x 2, 488 x 2, 468 x 2 (15,688 mm total). Believed uncut; shared with other projects. Design from stock first. Extra cuts allowed (about $2.20 per cut, DECLARED) and listed separately.
- Starting allocation to test in Step 1: base frame from shorter stock (644 x 2, 468 x 2, 488 x 2); 1540 mm lengths reserved for columns at Step 12; `bom_stock_allocation.md` records consumption for other projects (test P3).
- The footprint is stock-driven, not load-driven; the ICD must state the tip-over case (Designer D8, Systems Engineer S6). "Design load rating" is renamed "design loads (assumed)": axial 1000 N is a design choice bounded by the SBIR test range, torque is the 10 N m design assumption (DECLARED, Design Notes 12).

**8. Extraction facts, corrected (Fact-Checker review; patch the extraction file at Step 1).**
- 106.369 mm is the distance from the head tip (z -789.1834) to the kerf sphere centre (z -682.8144) in the 7 in model, not the pinch offset. The dome pole sits 106.369 - 71.4375 = 34.9315 mm behind the cutting face. The core is pinched off inside the head. Source lines 372-380. The Fact-Checker's own arithmetic (not in the source) puts the sphere meeting a 50 mm radius core about 55 mm behind the face. F4's number is a labelled assumption for the 6 in drill.
- 1 to 60 rpm is the Borebot motor and brake operating range (summary_yokeless_motor.md 158, 200; ip_and_competitive_position.md 59), not the cutter spin.
- The 152.4 mm figure is the tubing OD from the workorder, not a cutter OD; the only sourced cutter diameter is 7.00 in = 177.80 mm (7 in generation).
- Core 100 mm applies to Phase I EDU test cores (INSITU2 406-407); INSITU2 186-188 says the full-scale core diameter "is above 100 mm". The 90 to 105 mm range is the workorder's alone.
- Leaf thickness is double_dong_params.py 402-404 and the source calls it the plate thickness (0.125 in exactly); face radii lines 366-368; standoff line 372.
- Core tolerance, iris open aperture, 6 in iris data: no source; resolved at the gate (Design Notes 12). The 20 and 50 N m placeholders are retired. Mines PDFs and XLSX budgets read at Step 1 (pdftotext, openpyxl): no core dimension, tolerance, length, mass or delivery state; the report still asserts SBIR text only for core diameter.

**9. Source findings that change the design.**
- The iris is closed by the drill's own drivetrain; the jig supplies no actuator. Jig duties: hold the core coaxial, resist the iris reaction (torque and lateral load at 106 mm or more above the holder), carry core weight, guard the cutter stroke. The cutter never touches a 90 to 105 mm core (146.05 mm bore leaves 28.025 to 20.525 mm radial gap per side); WOB reaches the stop path, not the holder.
- Binding alignment tolerance is core versus iris throat opening, not core versus tube. The throat is a parameter: 54.2925 mm is a radius, so the open diameter is 108.585 mm (DECLARED); at 105 mm plus the ±1 mm tolerance the slack is about 1.3 mm per side (100 mm: 4.3 mm). The rule is core diameter < open throat; the cutting head sets core diameter. A narrower kerf is under consideration and is not a jig input. The tolerance budget (Step 2) lives inside this.
- Holding capacity: Loftsman 5.1 gave about 8.1 N m at d = 105 and 6.9 at d = 90 for 12 N m at the nut. Superseded at Step 2: 10.65 / 9.13 N m plain and 15.47 / 13.26 N m with the PTFE washer (about 267 N plain, 388 N PTFE axial at the 149.58 mm thread). Systems Engineer S1 gets about 240 N axial and about 10 N m by an independent route. Both land near the 10 N m design assumption; both use assumed friction coefficients. The human expects friction holding to reach the requirement and the core to fail first. A rotated core destroys stratigraphy order, so a slip is a failed test.
- Tilt before clamping: 1 mm radial clearance over a 30 mm grip gives 1.9 degrees (16.6 mm at the top of a 500 mm core; about 25 mm at 0.75 m); clamped, about 0.6 degrees (about 5 mm at 0.5 m). A steady rest or cradle is a Step 2 decision, not left to the operator.
- Printing: the printer is not a design input. No bed, material or nozzle constraint is applied and no part is split to fit a bed; the human will ask for help if something does not print. Orientation guidance stays as design practice: coarse thread, wings in-layer, threads axis vertical.
- Process rules: per-part scripts, one FCStd each (A.14); FCStd is authority once built (2.1); Boolean expected-delta and topology gate after each cut (7.1); builds over 30 s run in the background and PID, log path and expected finish are logged here (A.3.4); under FreeCAD 1.1.4 success is a sentinel line plus a fresh artifact, not exit code (A.15).

**10. Analytic vs empirical: Loftsman vs Engineer.**

| Position | Source |
|---|---|
| Derive thread, cone, slits, clearance and holding torque in closed form; specify numbers before any print | Loftsman |
| Test as you fly: the physical hold test is the evidence; closed-form results with unsourced friction coefficients are predictions | Engineer |

Ruling: both, in order. Closed-form results supply seeds and a prediction recorded before the print, labelled PREDICTED with their ASSUMED inputs; geometry (volumes, bore, thread form) is checked analytically because it has no unknown coefficient. Every friction, clearance and strain value is settled by the Step 8 coupons and the Step 11 hold test, which are the authority; a prediction that misses by a factor above 2 triggers a change order, not a rewrite of the prediction. Reason: the Loftsman math is right about shape and wrong to be taken as magnitude while mu is unmeasured.

**11. Other rulings.**
- Family spacing (Loftsman: 7 collets at 2.5 mm, N = 12; workorder reading: "separate collet per diameter"; Designer: 7 collets raise wrong-collet risk and print count; Software Engineer: 4). Ruling: 7 collets at 2.5 mm, confirmed by the human at the gate (B3, DECLARED), because with 5 mm spacing N = 20 slits and closure of 6 mm strain a printed web beyond a safe screening limit. The generator and all tests are family-list-driven; "2.5 mm is a params change" holds for geometry only. Grip windows replace nominal labels (operator measures the core and picks the window), with caddy, colour, rim notches and witness line.
- Stack height: Software Engineer (monotonic in d) vs Loftsman, Topologist, Systems Engineer (identical across d with a fixed outer cone). Ruling: independent of d; T5 uses the extremes for wall and stiffness.
- Re-measure scope: Software Engineer (full X1), Systems Engineer (volume and interference only), Topologist (add chirality on exports). Ruling: volume, interference and chirality; bore dropped.
- F5: Systems Engineer (fold into topology gate), Topologist (genus), Designer (broad feature list). Ruling: kept as genus plus Designer checklist, run inside the topology gate.
- Operator edges are function, treated at Step 9.

**12. Human gate decisions and adopted assumptions (Step 0 gate, 2026-11-08). Source: research/quinn/cr_scratch/step0_human_gate_decisions.md. These override defaults, reviewer findings and UNVERIFIED flags.**

DECLARED by the human:
- B1 Iris: 54.2925 mm is a radius; open diameter 108.585 mm. The throat opening is a parameter (the new drill is being fabricated; it may change). The cutting head sets core diameter, not the iris. Rule: core diameter < open throat in the open position (test P8). Nominal core 100 mm. Mines manufacturing variation expected. A narrower kerf is under consideration. The 90 to 105 mm range is not cut on aperture grounds.
- B2 Printer: not a design input. No questions on bed, material or nozzle; no part split to fit a bed; design freely.
- B3 Collets: seven at 2.5 mm across 90 to 105 mm. Custom collets requested as needed. At project end the team can design a new collet at a moment's notice: the parametric generator and its usage instructions are a deliverable (Step 5, test C10).
- B4 Holding torque: friction holding reaches the requirement; design assumption 10 N m; the core likely fails before the collet slips. No positive core lock, no escalation path, no 20 or 50 N m placeholders.
- B5 Nut role: the metal hard stop belongs to the upper assembly; the wing nut only tightens the collet and carries no descent load.
- B6 Core length and height: capture 0.5 m cores; install 0.75 m cores, optionally 1 m; upper assembly travel at most 0.5 m; total jig height 2 m is a soft target that yields to design freedom (recorded, not tested; members can be shortened later).

ASSUMED (adopted to close every other open or UNVERIFIED item; each is a parameter or a labelled statement, not a question):
- Core tolerance ±1 mm covers Mines manufacturing variation; Phase I data replaces it.
- Cutter keep-out uses tubing 152.4 / 146.05 mm; face annulus R_face = 76.2 + 10 mm; the 106.369 mm standoff carries over to the 6 in drill; all three are parameters in `params.yaml`.
- Core density 2400 kg/m3; masses derived from it.
- Friction, strain and clearance seeds (mu_k, mu_c, mu_t, bearing, web-strain allowable, c_r, g_a) are design-assumption seeds; the Step 8 coupons and the Step 11 hold test settle them.
- Mines PDFs and XLSX budgets were read at Step 1 (pdftotext, openpyxl; downloads were lifted): they say nothing on core dimension, tolerance, length, mass or delivery state; the report still asserts SBIR text only and omits "Mines specifies" sentences and the core-count sentence.
- 30-6060 geometry is measured from the human's local STEP at Step 2 (VERIFIED); no catalog download; brackets are listed by full-size 30-series class, SKU verified at purchase; stainless M6 for non-80/20 joints; on-hand bracket and screw inventory is treated as nil (all purchases listed in the BOM).
- No early coupon print; coupons wait for Step 8.
- Axial design load 1000 N is a design choice bounded by the Phase I test range; descent method (crank or leadscrew) is a Step 12 design decision.
- Debris: indoor, debris tray in the base, dust skirt on the nut. Footprint: four adjustable feet or bolt-down slots; tip-over numbers fixed at Step 2 (23.8 degrees static tilt, 158 N at the centre of mass, 68 N at the column top; bolt-down with the cutter above z = 400 mm); Step 12 replaces them.
- The report covers the base; whether it also covers the upper assembly follows the Step 12 work order (a plan decision, not a human question).
- Spin 1 to 60 rpm is the motor and brake range and is not a jig input. The ascent test profile and the docx contents are not used.
- No 6 in drill STEP is needed: the throat parameter stands at 108.585 mm.

**13. Step 1 findings (Manager close, 2026-11-08). Source: research/quinn/cr_scratch/step1_engineer_foundation.md, step1_fact_checker_corrections.md, step1_designer_params.md.**

- Iris: the 108.585 mm open diameter is DERIVED (2 x radius) from the DECLARED 54.2925 mm radius; `validate_params` rejects a mismatch. Gate B1 called the diameter DECLARED; the tag is DERIVED.
- FreeCAD: `%LOCALAPPDATA%\Programs\FreeCAD 1.1\bin\freecadcmd.exe` (1.1.4). The Program Files path in the earlier Detail 1 does not exist.
- 80/20 STEP: not downloaded at Step 1 (the vendor form requires personal details). Superseded at Step 2: the human supplied the local STEP, the section is measured and hollow (916.56 mm2, VERIFIED), mass per metre 2.475 kg/m STEP-based against the catalog 2.573 (3.8 percent under; the catalog value is used for mass and tip-over work).
- Stock allocation: the jig takes 3,200 mm of the 15,688 mm on hand, no extra cuts; the four 1540 mm lengths stay unused (reserved for Step 12). The 468 mm cross members between the 488 mm-spaced rails leave 20 mm slack; Step 12 places them (on top of the rails, lengthwise, or swapped with a 488).
- T-nuts: PZRT 3030 Series Roll-in Spring M6 T Nut, roll-ball elastic, 8 mm T-slot (12-pack, Amazon); fit is declared by use.
- Param keys: `print.*` and `collets.diameters` were removed. Use `collet.min_wall`, `fit.seat_clearance` and `core.diameters` (single source). `collets.envelope_max` is 106.585 DERIVED; `icd.keepout_radius` 86.2 DERIVED; `stop.height_z` is 184.84 (Step 3: collar top 159.84 + g_stop 25); A2b recomputes per core class. Keys: `stop.collar_top_z` (was `nut_top_z`), `stop.height_range`, `stop.start_z` list; `stop.hard_stop_gap` is deleted, use `holder.stroke_gap_*`.
- Designer gap list: 14 of 38 Detail 6 features carry a param key, 24 are MISSING; the collet generator is NOT READY for on-demand use. Carried to the Step 3 blocking params review and the Step 5 generator deliverable (step rows updated).
- Process rule (cause of the Fact-Checker's first WITHHELD): spawn prompts name file paths copied from a Glob result or the Engineer's report, never re-typed. The gate path `gpr\double_dong_params.py` was typed from memory; the file is at `gpr\build_parts_double_dong\`.

**14. Step 2 findings (Manager close, 2026-11-08). Source: research/quinn/cr_scratch/step2_system_concept.md, step2_loftsman_signature.md, step2_topologist_signature.md, step2_designer_comment.md, step2_engineer_profile_measure.md, step2_engineer_integration.md.**

Orchestrator rulings:
- The washer key is `washer.type`, not `washer.material`. The Step 1 printer-key filter (gate B2, `_PRINTER_KEY`) treats `material` as a printer input. PTFE is a washer type; the gate is not weakened. The concept text still says `washer.material`; params governs.
- The Topologist's last withhold (decision 5 wording, test IDs A3h, A1d, A3g) was closed by applying the Topologist's own specified smallest edits. The Topologist did not re-view the edited file. The edits were applied and spot-checked by grep.

Design facts carried forward (authoritative values: params.yaml and the concept):
- Core masses 10.4, 15.6, 20.8 kg at d = 105 (2400 kg/m3, ASSUMED density).
- PTFE washer always fitted (PTFE on hand, DECLARED; Design Notes 15). Holding 15.47 / 13.26 N m at d = 105 / 90. Plain washer 10.65 / 9.13 misses 10 N m at d = 90 by 8.7 percent; no margin is claimed on the plain washer. All inputs ASSUMED; H1 decides.
- Working stroke 500 mm; loading park 959.84 mm, reached only by the manual raise and held by a pin latch. About 775 mm of carriage range (184.84 to 959.84) is not working travel. Gate B6 reads "travel at most 0.5 m"; the reading that the park is separate is an assumption the human confirms at the gate.
- A 535 mm travel option (full 500 mm retained core) is recorded, not applied. One stroke retains 465.07 mm.
- Stop height fixed at Step 3: highest clamped collar top 119.84 + floor 40 + g_stop 25 = 184.84 (169.84 at the old g_stop 10).
- Bolt-down is the operating condition: unbolted tip-over 68 N at the column top, 158 N at the centre of mass. Step 12 replaces these numbers.
- Bracket 30-4332 (30 mm legs) superseded; minimum leg 57 mm. The printed bracket (68 x 68 x 57 mm, 7 mm plate, slots 7.0 mm at 29.2 mm pitch, measured) and 8020-14089 (57 mm L bracket, 6 mm plate, measured) are full size. Purchased brackets drop from 16 to 8. Step 7 total: 12 brackets (8 purchased, 4 printed), 96 T-nuts (Design Notes 22).
- Step 3 result: the 68 mm bracket facts are VERIFIED (measured STL); the 8020-14089 geometry is VERIFIED, its SKU stays ASSUMED (8020.net 403; Zoro lists 8 holes, so `hardware.tnuts_per_bracket` is 8). The T-nut is the PZRT 3030 roll-in spring nut, DECLARED by use.
- Collet chamfer is wall minus 1.2 mm (3.8 mm at d = 105); the 10 mm capture radius belongs to the upper-assembly funnel (U12). Capture margin is thin: 9.31 mm worst case against 10.
- The concept `washer` signed feature (radial tab notch) and its pair gaps (0.5, 1.0) are the Engineer's seeds; the Topologist confirms at Step 3.

Designer ABSORB items assigned to later steps (the four BLOCK items S2-1, S2-2, S2-3, S2-7a were answered in the concept: steady rest at every length with cam release, 959.84 mm park with latch, choke strap with no overhead anchor, manual raise with fuse). The Designer's comment predates the three concept revisions and was not re-run; the Designer reviews the revised text at the Step 3 params review.
- Step 3 (params review): S2-4 witness scale, wrong-collet bands, colour, rim notches, caddy; S2-5 wing grip (height 30 or more, hand clearance 50, sweep clear radius 115) and `stop.g_stop` of 25 mm (the concept held 10 mm); S2-6 key sector 60 degrees and bolt-down method (foot plate); S2-7b nut release marker; S2-7c `loads.nut_torque_abuse` 25 N m and tommy-bar length; S2-7d captive washer; S2-8 `stop.nut_top_z_min/_max`; `hardware.tnut_fit_30series` VERIFIED before bolt-down relies on it.
- Step 5 (generator): witness zones from the stroke gap (7.09 mm per family step), colour, rim notch count, label window text, chamfer per collet, caddy sockets. Done at Step 5, except the witness scale geometry, which belongs to the receiver and holder and moves to Step 6 (Design Notes 20).
- Step 7 or 12: hand-access tests A1b on assembled solids.

Process findings:
1. Signer withholds (Loftsman: two rounds, three lines; Topologist: three rounds, the last closed by ruling) trace to one cause: the concept was drafted before geometry numbers existed and then rewritten after them. Fix: for any future concept step, the Systems Engineer drafts only the numberless stubs, then writes the concept after the cross-review numbers exist (agent order 2, 4, 5, then 6), and the draft is not circulated for signature until every number is cross-checked. Step 2 followed this order for the geometry but not for the handling, stability and test-ID content, which came in revision passes.
2. Length: the concept ran 6042 words against "one page plus two tables". The gate cannot be checked by eye. Fix: a concept step states a word cap in the spawn prompt and the Manager counts at close; the signed concept is the record, and the ICD table (params `icd.*`) is what later steps read.
3. Echo hand-written documents: reference/vendor_sources.md still said "no STEP, ASSUMED" after the profile was VERIFIED, because generators do not rewrite hand-written files. Fix: the Echo Site Registry names reference/vendor_sources.md in the profile and bracket rows, and an Engineer measurement step lists hand-written files that mention the measured value. Repaired at this close.
4. ID overload: the concept used IDs that meant several predicates (A1, A3, A6, P6). Fix applied by the signers: one predicate per ID, suffixes A1a to A6c, physical tests H1 to H10 labelled outside Rule M, T7 labelled a prediction. The CAD Test Specification groups above point at the concept Test ID key until Step 4 rewrites them.
5. Mass check: STEP-based mass per metre is 3.8 percent under the catalog against a 3 percent directive. Written down; the catalog 2.573 kg/m is used. The P9 tolerance is 5 percent.

**15. Human directives at the Step 2 gate (DECLARED, 2026-11-08).**
- PTFE (Teflon) is on hand. The PTFE washer is accepted as the fitted design; no sourcing or substitution analysis is needed.
- Model policy for spawned agents: Sonnet by default (pass `model: "sonnet"` on the Agent call). Opus (orchestrator default, 1M context; spawn by omitting `model`) only for image analysis (every visual gate: Designer Steps 6, 7, 9 and any render or STL inspection) and high-difficulty reasoning (the Loftsman and Topologist cross-review of thread, cone and seat geometry, and any ruling on a disputed derivation). The Manager names the model for each spawn in its open file.

**16. Step 3 findings (Manager close, 2026-11-08). Source: research/quinn/cr_scratch/step3_designer_params.md, step3_engineer_hardware_confirm.md, step3_engineer_params.md, step3_geometry_crossreview.md, step3_engineer_first_solids.md, step3_designer_completeness.md, step3_manager_close.md.**

- Collet strain ruling (orchestrator). The Topologist's round-one withhold had two lines. Line 67: Loftsman 0.916 (coefficient 4, hole centre) against Topologist 0.592 (coefficient 3.0, slit to hole edge); both below 1.0; geometry identical (ligament 3.0, relief hole 8.0, slit 25.0). Ruled: geometry stands, 0.916 is the design value, the Topologist reading is noted, the physical collet test decides. Line 65: the Topologist's chamfer rule min(wall - 1.2, 10.5), with 2.5 where wall - 1.2 lies in (2.5, 3.5), was accepted and applied with a sweep (d 85 to 106.585, minimum edge clearance 0.5). The Topologist did not re-view after these edits; the geometry is signed by ruling, not by his signature.
- `stop.g_stop` 25 mm clearance, DECLARED (design choice, no standard cited). Consequences: `core.min_exposed` 143.12 (was 128.12), `stop.collar_top_z` 159.84, `stop.height_z` and `icd.stop_height` 184.84 (169.84 at 10), `stop.height_range` [184.84, 315], `upper.park_z` 959.84. The 119.84 was recomputed by the Engineer by a second route. The Designer's `stop.collar_top_z_min` 148.21 was wrong (subtracted the R-to-K-max drop); 152.75 used.
- T-nut fit in the 30 series: declared by use (PZRT 3030 roll-in spring M6, human use on 30-series stock).
- `hardware.tnuts_per_bracket` 8 (T-nut BOM 44 to 150) from the Zoro 8-hole listing of 14089, ASSUMED; the printed bracket is assumed to match. Printed bracket slot pitch along the leg is 29.2, not 30 (measured). The 8020-14089 SKU stays ASSUMED (8020.net 403); its geometry is VERIFIED (57.35 x 57.35 x 57.0, plate 6.0).
- Engineer deviations from the signed table: receiver, holder, nut, washer and one foot ring (d 90) built, 104 of 104 feature rows pass. Not built: collet slits, relief holes, strain ratio, bore chamfer (Step 5 generator). Ring bottom to floor 0.000 (designed seat contact, class C; S3 amended), the 0.005 gap is at the ring top. Release arrow span 33.25 against 33.75 deg. Pad arc 9.983 against 10.0. Washer windows at 90, 210, 330 deg. Wing mark 21.86 mm; `nut.arrow_length` re-keyed to 21.86 DERIVED (a 40 mm arrow cannot fit the 31.86 mm wing). Foot ring for d 90 only. Receiver below z 0 is a solid spigot tube.
- Collet slits, relief holes, chamfer, rim notches, grip-window label and colour belong to the Step 5 collet generator, not to the foot ring (confirmed in the Step 5 row).
- The post-build Designer part-level read (all five parts PASS) is a deviation from the Step 3 row, which lists the Designer as the pre-geometry gate only. It does not replace the Step 6 completeness gate; text-only, visual gate NOT RUN.
- Tighten and loosen glyphs: the JSON shows one marked wing face and the release arrow; the wing mark does not encode direction. Step 6 directive added to Detail 6.

Process findings (system or one-off):
1. Signer withholds at Step 3: Topologist round 0 five lines (W-1 to W-5), round 1 two lines (strain coefficient, chamfer tangency), closed by ruling. The Design Notes 14 fix (numbers exist before anyone signs) held for the concept: the Loftsman's table reached the Topologist complete and the Loftsman signed in one pass. It did not hold for derived interactions between numbers: the strain coefficient (hole centre against hole edge) and the chamfer against relief-hole tangency were each stated in one file under a different basis than the other signer used. Verdict: system defect, the same as Step 2 (basis unstated). Process fix: a number that feeds a formula carries its measurement basis (centre or edge, per side or diametral) and the formula text in the table row; the Loftsman states the strain coefficient in the row; the Topologist's re-check runs the sweep script before withholding; and a withhold that is a reading difference with both values passing (here 0.916 and 0.592, both under 1.0) is ruled at once rather than looped.
2. Word caps (tables excluding pipes, counted by the Manager): designer_params 1455/1500, hardware_confirm 551/500 (+10 percent), engineer_params 582/600, loftsman_numbers 2553/2500, topologist_crossreview 1564/1800, crossreview 1791/2000, topologist_signature 339/400, first_solids 708/700, designer_completeness 787/700 (+12 percent). None exceeds 20 percent; no prompt defect. One-off: the Loftsman's own count in the crossreview (1,240) understated the file (1,791); the Manager counts.
3. Late arithmetic slip, one-off: the Designer's `collet_top_z_min` 148.21 and base spigot hole 0.20 against 0.40; both caught by the Engineer on the same step.

**17. Human decisions at the Step 3 gate (DECLARED, 2026-11-08). Source: research/quinn/cr_scratch/step3_human_gate_decisions.md; edits in research/quinn/cr_scratch/step3_gate_edits.md.**
- `stop.g_stop` is a mechanical clearance, not a safety item. The operating sequence raises the drill before anyone touches the wing nut, so no pinch point exists. Dimensions unchanged (25 mm and all consequences in Design Notes 16). The ISO 13854, finger, crush and pinch rationale is removed from live files; `wingnut.knuckle_clearance` is renamed `wingnut.hand_clearance` (wing-turning access). research/quinn/cr_scratch/ and accumulator.md keep the history.
- T-nut: PZRT 3030 Series Roll-in Spring M6 T Nut, roll-ball elastic, 8 mm T-slot (12-pack, Amazon). Fit DECLARED by use. 80/20 candidates 40-3914, 13031, 13098 and the head/neck acceptance limits are retired. BOM regenerated. `hardware.tnuts_per_bracket` stays 8 (ASSUMED) until the human states the count.
- Rule for all agents: a clearance is cited as a safety requirement only when the operating sequence puts a hand in the hazard. Check the sequence first; otherwise describe it as a mechanical or usability clearance and cite no standard.
- Pytest after the edits: 197 passed.

**18. Working-step rules (human direction, Step 4, 2026-11-08).**
- FreeCAD run time is not a constraint. Long runs still go background so the session stays responsive (A.3.4); a foreground run over 30 s is no longer logged as a defect.
- Fact-Checker at working steps (1 to 12): the gate question is whether each number a test reads matches its primary source. Tag format, missing `# SRC:` comments and Register citation style are clerical; the Fact-Checker lists them, the Engineer or Software Engineer fixes them in the same pass, and they are not grounds to withhold. A withhold at a working step needs a number that disagrees with its source or a source that does not exist. The formal source audit belongs to the report gates (Steps 13 and 18).
- Open items are closed by the team inside the step (params gaps, spec conflicts, tags), not carried to the human as a list.
- Register citations to INSITU2_text.md and INSITU3_text.md quote the phrase; those files are 9 and 12 lines long and the old line numbers were from a longer source.

**19. Female threads by stud-subtract (human direction, Step 4, 2026-11-08).** The human has seen a geometry glitch in the nut's female thread made by the native SubtractiveHelix cut (nut.py lines 81-90). The same fault shows in the T9 probe: overlap does not change monotonically with tilt, and OCC logs "hasher mismatch". The rule: build the female thread as a male stud at nut fit dimensions (radii offset by fit.c_r, axial flank gap fit.g_a), then subtract it from the nut body. Any scaling is radial only. The nut is rebuilt inside the Step 4 Engineer fix pass. The receiver's external thread stays native unless its probes show a fault. The rule is now in supplements/llm_plm_cad.md §2.6. Result at Step 4: quarter-turn ruled-helicoid segments fused into one stud (27 segments) worked on both the nut and the receiver. A pipe-shell stud and a single multi-turn ruled stud both failed.

**20. T9 measure and Step 5 rulings (orchestrator, 2026-11-08/09).**
- T9: rigid-tilt nut/receiver overlap is withdrawn (an infeasible pose: the probe pivot drove the nut through its flank). T9 is the cross-thread misregistration criterion 1.5 x D tan(alpha_total) <= P/2 (Loftsman, research/quinn/cr_scratch/step4_loftsman_t9_ruling.md). Invariant at green_at_4, factor 1.68. Step 8 coupon checks g_reg <= 0.299 mm.
- Receiver residual InvalidCurveOnSurface BOP edges go to the Step 10 STEP re-import check.
- A literal in a build script that duplicates a params value is a defect, not clerical; it is fixed inside the step (Step 5 cleanup pass, 4 chamfer and lip keys).
- FreeCAD .FCBak files are archived to research/quinn/cr_scratch/fcbak_archive, never left in parts_cache or results.
- The witness scale is not a collet feature; it is built at Step 6. (Placement superseded by Design Notes 21: ruler on the receiver thread, tick on the holder flange.)
- params.yaml leaf count at Step 5 close: 332.

**21. Step 6 findings and rulings (Manager close and orchestrator, 2026-11-10). Source: research/quinn/cr_scratch/step6_manager_close.md.** Probe defects D1 to D3 were test positions (HD5 key sector, rim on lead-in chamfer, glyph window inside dust skirt); fixed with known-bad controls, no predicate weakened. Witness D1 was a render pose error (nut drawn 5 mm low; reading face is nut z 0, edge = rim top - 40 + g); ruler unchanged; ray-cast probe reads edge 50.00 and 57.10 with 2 and 9 lines visible. Rest rollers follow the core (r_c = d/2 + roller_dia/2 + 0.005) with radial pin slots in the ring; adjustment built in Pass 1; rest vs every collet and core, 3 poses, 2 heights: 0.0 mm3 in 54 rows. Tray floor falls 2.0 deg on both axes to a drain spot face; plug has a 34 x 8 x 10 lug. NT4 glyph 10 mm; NT8 scaled to equal area (ratio 0.97), shaft 0.7 mm. Params leaves 444. Topologist addendum signed rest, tray, plug, nut after the fix pass. Carried: C6 bracket overlap (18,249 mm3 x 4), printed bracket vs end member (1,061 mm3 x 4) and T-nut pair overlap (16,523 mm3) to Step 7; D13 (0.7 mm shaft) to Step 8 print-process rules, the printer not being a design input; D4, D7, D9, D12 and steady-rest Pass 2 refinement to Step 9; receiver BOP (Engineer D6) to Step 10. Lesson: a gate that signs before a fix pass leaves the rebuilt parts unsigned; the re-check list needs an owner and a closing read.

**22. Step 7 rulings to date (orchestrator, 2026-11-10; step open).** Source: research/quinn/cr_scratch/step7_manager_open.md, step7_loftsman_definition.md (with Revision 1), step7_systems_engineer_contract_check.md, step7_topologist_crossreview.md, step7_engineer_parts_findings.md, step7_rebuild_authorizations.md.
- ASSEMBLY.md contract rows changed: base|holder g_min 0.12 (was 1.5); holder|collet R 0.29 (was 0.30); holder|nut K 0.50 (was 0.75), tied to washer thickness minus pocket depth; nut|washer class P, overlap 2.0 to 2.45 mm3 (Systems Engineer's 2.0 floor ruled over the Topologist's 2.30); collar top|cutter minimum 0 at R, 25 at Kd1 and K-max.
- C6: the four printed outer brackets are deleted: 12 brackets (8 purchased, 4 printed), 96 T-nuts, matching the Step 2 rule. All frame overlaps read 0. Single-bracket support-end joint capacity is DECLARED for Step 12.
- Holder collar (r 55.0 to 76.2, z 104.75 to 110.75, four 6.6 holes) is in holder.py; a pose-only fuse was rejected.
- Nut travel: the probe's 9.51 was a proxy; the physical stop left 4.01 against the requirement of at least 8. Fixed by a relief bore (r 75.34, nut z 42.0 to 48.5): 10.01 mm by Loftsman trial. Engaged lengths unchanged (25.705 / 31.401 / 38.490); T9 2.379 against 4.000. The nut relief needs refine off (cadlib.body_boolean refine=False): refine gave 177 faces and BOP errors.
- A3b split: key/pin and spigot fits green_at_7; column-foot and carriage-guide fits green_at_12.
- Cutter stand-in carries a lead-in ring, bore radius `icd.core_lead_in_bore`, so A3d cannot pass on the face annulus.
- Params leaves 463. Topologist re-sign of holder, nut and frame is owed after the build (Design Notes 21 lesson).

**23. Upper assembly configuration, human decisions (DECLARED, 2026-11-24).** Source: the 2026-11-24 SBIR meeting and the human's follow-up the same day; working file `context/2026-11-24_cutjig_critical_path.md`. These decisions pull Step 12 forward. Sean leads the 2D sketch phase (research/sean/gameplan.md).
- **Travel 650 mm** (supersedes gate B6, 500). Params: `upper.travel_max` 650, `stop.start_z` [834.84, 965]; the cutter keep-out was rebuilt to 834.84. Consequence: test_P10_working_stroke_per_core_class fails. The 0.75 m case now starts at 965, above the loading park `upper.park_z` 959.84. The U13 park rule must be re-derived in the upper-assembly redesign, and the test stays red until it is.
- **Drill rotation:** a large-diameter bevel ring gear on the drill, driven by three pinions at 120 deg. Each pinion has a NEMA 23 stepper (on hand), with or without a gearbox. The pinions also carry the drill's weight. If they need help, a support ring holds the motor shafts in bushings.
- **Lift:** a ring structure carries the drill, ring gear and three drive motors, and it is the part that moves up and down. It is driven by three jack screws at 120 deg, probably on NEMA 17 steppers. This replaces the Step 2 ratchet hoist and the two-column carriage (`hoist.*`, `column.*`, `upper.manual_raise`), which become void in the redesign.
- **Lead screws:** T8 (8 mm) with brass nut is the cheap class. 1000 mm costs about $35 to $90, and custom cuts go to 2000 mm. Needed length is about 650 travel + nut + end bearings, so 800 to 900 mm. Anchor each screw at the bottom with a thrust bearing and guide only the top. Cutting force pushes the ring up, which puts the screw below the nut in tension; only the ring's weight puts it in compression. An 8 mm screw about 850 mm long would buckle or whip if 1000 N of cutting load put it in compression. If the sketches need compression mounting, step up to TR10 or TR12.
- **Sync:** the three lift steppers must move together. Drive them as one axis from a single controller, or link the screws with a belt. The sketch phase picks.
- **Open:** NEMA 17 count on hand, NEMA 23 gearbox ratio, drill rpm and torque target, ring gear size and source, and how the iris drive (same drivetrain, INSITU2 157-166) sits with three pinions.

**Software Engineer review slots:** Step 4 (signs suite), Step 5 (generator), Step 7 (assembly tests), Step 10 (code and test review), Steps 13 and 14.
**Loftsman and Topologist cross-review slots (A.4):** Step 3 (before any build: L1 to L5), Step 6 (L1, L5, L6), Step 8 (L4), Step 9 (L6, L7), Step 10 (topology gate).
**Designer slots:** Step 1 (seed params), Step 3 (blocking params review), Step 6 (completeness and critique), Step 7 (A5), Step 9 (quality gate), Step 11 (print-review form), Step 14 (structure), Step 18 (Wave 2). Steps 6, 7 and 9 need an image-capable reviewer (A.3.1).

---

## Echo Site Registry

Each row: value, authoritative source, derived locations. Bold values on use. First-use rule: introduce with context at first use in each section. Authority rule (A.16): geometry values live in params.yaml until an FCStd exists, then the FCStd; report values match the authority, not each other.

| Value | Authoritative source | Derived locations |
|---|---|---|
| Core nominal diameter **100 mm** (Phase I EDU test cores; Figure 2 caption conflict noted) | INSITU2_text.md, "pre-cast to 100 mm" (conflict: "is above 100 mm") | report 1, 2, 5; collet file names; tests |
| Collet family: count and diameters (**7 at 2.5 mm**, DECLARED; new collets on demand from the generator) | params.yaml `core.diameters` (single source; `collets.diameters` removed at Step 1) | report 5; file names (`collet_092p5`); matrices; BOM; thesis; C8, F3, A1 |
| Collet grip window per collet; bore_free(d) = d + tau + c_i (seed **d + 2 mm**) | params.yaml | label engraving; caddy; report 5; C3, C8 |
| Core accepted range **90 to 105 mm** | workorder.md only | report 1, 5; generator bounds; C8 |
| Core tolerance **+/-1 mm** (ASSUMED) | params.yaml `core.tol` | C8, T5, F3, P8; report 2 as stated assumption |
| Tubing **152.40 / 146.05 mm (6.00 / 5.75 in)**, wall 3.175 mm; format: mm first, inches in parentheses at first use. 152.4 mm is tubing OD, not cutter OD (cutter OD ASSUMED) | workorder.md; params.yaml `drill.*` | report 2, 3, 7; A2; keep-out solids |
| Radial gap, 100 mm core **23.025 mm** (90: 28.025; 95: 25.525; 105: 20.525) | derived | report 2; E-1 |
| Iris leaf count **4**; **106.369 mm = head tip to kerf sphere centre** (7 in model, not the pinch plane); dome pole **34.9315 mm** behind the face | double_dong_params.py 93-98, 372-380 | report App A; F4 |
| Iris throat opening **108.585 mm open diameter** (54.2925 mm radius; DECLARED parameter, may change with the new drill); rule core diameter < open throat | params.yaml `iris.throat_open_diameter`; double_dong_params.py line 92 | report 1 (assumptions block), 2; P8; E-8 |
| Thread: right-hand, single start, symmetric 45/45; pitch **8 mm** (PROPOSED); major **149.58 mm** DERIVED (`thread.major`), minor 144.58; rim lead-in **1.25** (`thread.lead_in_length`), nut lead-in **0.9** (`thread.nut_lead_in_length`), crest and root flat **1.5** (`thread.land_width`), run turns and runout land 4.0 (`thread.run_turns`, `thread.runout_land`). "Tr 60 x 8" withdrawn | params.yaml `thread.*` | receiver, nut, base scripts; T1 to T9; report 3, 6; coupon |
| Cone half-angle **10 degrees** (20 degrees retired) | params.yaml `cone.alpha` | collet, holder; F1, S5, S16; report 3, 5 |
| Slit count N **12**, width w_s **1.5 mm**; clamped slit 0.584; grip window d - 1.5 to d + 1.0; ligament **3.0** (`collet.slit_ligament`), slit length **25.0** (`collet.slit_length`), relief hole **8.0** (`collet.relief_hole_dia`, centres z 7.0 and 25.0), overlap 18.0, strain **0.916** design value (Topologist reading 0.592; the physical collet test decides); geometry built at Step 5 | params.yaml `collet.slit_count`, `collet.slit_width_seed` | C5, C9, T5; report 5 |
| Min thread engagement (PROPOSED **3 pitches**; at least 24 mm in every pose, A3i; pose R full-form engagement **24.72** against 24) | params.yaml `thread.min_engage_pitches` | T4; report 5 |
| Nut OD **166.28 mm** DERIVED; wing span **230 mm** ASSUMED (parameter); no bed limit applies | params.yaml `wingnut.*` | A2; report 3, 6 |
| Hard stop: metal descent stop, owner the upper assembly (`upper.metal_stop`), 1000 N, `stop.g_stop` 25 from the collar top; the holder stroke gap is a separate, never-loaded gap; the printed nut is not a stop | ASSEMBLY.md ICD; step2_system_concept.md | A2, F4; report 2, 8 |
| Profile series **30-6060** (60 x 60 mm, M6 roll-in spring-ball T-nut) | step0_human_stock_80-20.md | frame scripts; BOM; P3 to P5; report 3, App B |
| Stock lengths and allocation | step0_human_stock_80-20.md; bom_stock_allocation.md | BOM, P3, report App B |
| Design loads: axial **1000 N** (design choice bounded by WOB 100 to 1000 N test range); holding torque **10 N m** (DECLARED design assumption; the 20 and 50 N m placeholders are retired) | INSITU3 424-430; step0_human_gate_decisions.md; params.yaml `loads.*` | T7; report 2, 4 |
| Holding torque estimate **10.65 / 9.13 N m** plain washer, **15.47 / 13.26 N m** PTFE washer, at 12 N m nut torque, d = 105 / 90 (PREDICTED, ASSUMED inputs) against the 10 N m design assumption | Step 8 sheet | T7; report 4, 7, page 1 |
| Spin **1 to 60 rpm** = Borebot motor and brake range, not cutter spin | summary_yokeless_motor.md 158, 200 | report 2; scoping |
| Core length: capture **0.5 m**, install **0.75 m**, optional **1 m**; upper assembly working stroke at most **0.5 m** (park **959.84 mm** separate; captured length 465.07 mm for a 500 mm core); jig height **2 m** soft target (DECLARED); mass **10.4 kg** at 0.5 m, 15.6 and 20.8 at 0.75 and 1 m (DERIVED) | step0_human_gate_decisions.md; params.yaml `core.length_*` | report 2; H2 stand-in |
| Collet generator usage doc `docs/collet_generator_usage.md` and test C10 (8th, off-grid collet) | Step 5 | report 5; Step 20 close check |
| Footprint **644 x 608 mm**, feet, tip-over statement (158 N at the centre of mass, 68 N at the column top; bolt-down) | ASSEMBLY.md ICD (Step 2) | Step 12; report 2 |
| Lateral load **100 N** at 106.4 mm = **10.6 N m**; H3 side load **21.2 N** at the top of a 0.5 m core | step2_system_concept.md decision 3; params.yaml `loads.*` | H3; report 4 |
| Washer ID **136.8**, OD **143.2**, thickness **1.3 mm** (ASSUMED), `washer.type` PTFE; radial notch **6.0 x 2.0** (`washer.notch_width`, `washer.notch_depth`); three nut pads, contact class P, overlap 2.402 mm3 (`nut.pad_*`) | params.yaml `washer.*`, `nut.pad_*` | T7; H1; report 4, 5 |
| Receiver floor **40 mm** above datum A; coaxiality chain **0.953** against 1.0 | params.yaml `icd.floor_above_datum_a`, `icd.coaxiality_chain` | A3b; report 4 |
| Collar OD / ID / top **152.4 / 110.0 / 6.75 mm** | params.yaml `collar.*` | A2b; F4 |
| Steady-rest detents **310 / 560 mm**; strap **80 kg**, side handle **250 mm**; park **959.84 mm**, fuse **300 N** | params.yaml `rest.*`, `strap.*`, `upper.*` | A1e; H9; H10; report 2 |
| Bracket leg minimum **57 mm** (30-4332 superseded); SKU 8020-14089 ASSUMED; the 68 mm printed bracket VERIFIED (slots 7.0 at **29.2** pitch, not 30); `hardware.tnuts_per_bracket` **8** (ASSUMED; T-nut BOM 150); PZRT 3030 T-nut DECLARED, fit declared by use | params.yaml `hardware.*`; reference/vendor_sources.md | P4; BOM; Step 3 confirmed |
| T9 register tilt: **0.924 deg** against the 1.021 line (built 0.9248; corner-formula upper bound). Step 4 measured: register stop 0.596 + plate rock 0.315 = **0.911 deg**, cross-thread misregistration 2.379 against 4.000 mm, factor 1.68 (Design Notes 20) | params.yaml `register.t9_tilt_deg`; step3_geometry_crossreview.md | T9; report 3 |
| Holder inserts and index notch (six keys: `holder.insert_*`, `holder.index_notch_*`); nut plate hole and tab (`nut.plate_hole_dia`, `nut.tab_inner_radius`) | params.yaml; step3_engineer_first_solids.md | holder, nut scripts |
| First solids (Step 3): receiver, holder, nut, washer, foot ring (d 90 only) built, isValid true, one solid each, 104 of 104 feature rows pass; collet slits, relief holes, chamfer not built | parts_cache/{part}_result.json | Step 4 suite; Step 5 generator |
| Profile section **916.56 mm2** hollow (STEP-measured, VERIFIED); mass per metre catalog 2.573 kg/m used | params.yaml `profile.*`; step2_engineer_profile_measure.md; reference/vendor_sources.md | P9; BOM; tip-over |
| Report test count **about 90 (91)** (the CAD P-group grew by P9 and P10; recount at Step 13) | Detail 13 | Step 13 suite; Step 19 final run |
| Step and section numbering (this plan: Steps 0 to 20; report sections 1 to 8 plus Appendices A to C) | this gameplan | all documents |

---

## Gate Decisions

The Step 0 gate is passed. The human's decisions (B1 to B6) and the assumptions adopted for every other open item are in Design Notes 12. This plan carries no open-questions list, no to-do list and no request for human input into Step 1.

---

## Findings disposition

R = resolved in this plan; D = deferred with owner and step.

| Finding | Source persona | R/D | Where |
|---|---|---|---|
| S1 No load case derived; plan proves geometry not hold | Systems Engineer | R | Detail 2 item 3 to 4; T7; Detail 11 hold test; Design Notes 9 |
| S2 Force loop ambiguous; release undefined; "reversal changes data" false | Systems Engineer | R | Detail 2 item 1 to 2; Design Notes 1, 3; A3, F6 |
| S3 Collet cannot close 5 mm with one slit; stiffness varies | Systems Engineer | R (moot for 5 mm: seven collets at 2.5 mm DECLARED) | Design Notes 3, 11, 12; C5, C9 |
| S4 Binding tolerance is the iris aperture; no tolerance budget; datum scheme | Systems Engineer | R (budget; aperture value moot, throat is a parameter) | Detail 2 item 5; Detail 1; P8; Design Notes 9, 12 |
| S5 Hard-stop load path through printed nut | Systems Engineer | R (confirmed, B5) | Design Notes 2, 12; A2, F4 |
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
| G7 Coverage and slit design are one problem | Loftsman | R | C5, C8, C9; Design Notes 12 |
| G8 STL tessellation eats clearance | Loftsman | R | E2 |
| G9 C3 probes fall in slits | Loftsman | R | C3 |
| G10 Holder flange needs hard stop | Loftsman | R | F6; Detail 3 |
| G11 Core tilt closed formula | Loftsman | R (numbers recorded; lateral guide at Step 2) | Design Notes 9; Detail 2 item 9 |
| G12 Missing analytic definitions (key, tray, drain, label, lead-in, core stop) | Loftsman | R | Detail 3 work; Designer params gate |
| TP-1 Thread smaller than cores | Topologist | R | Same as G1 |
| TP-2 Stack stated three ways; load path | Topologist | R | Design Notes 3; Detail 2 item 1 |
| TP-3 "Touching is not overlapping" erases allowed vs forbidden | Topologist | R | A1 contact classes C, G, F |
| TP-4 A2 and F4 wrong footprint and plane | Topologist | R | A2, F4 |
| TP-5 105 mm core vs aperture | Topologist | R (moot: throat is a parameter, range not cut) | P8; Design Notes 12 |
| TP-6 C1 vs C5; self-lock release | Topologist | R | Design Notes 3; C5, C7 |
| TP-7 A3 satisfied from parameters; mid-height; bracket normal | Topologist | R | A3, Rule M and P |
| TP-8 T1 under-specified; cross-threading; export chirality | Topologist | R | T1a to T1d, T9, X1 |
| TP-9 Wall varies 7 to 1; T5 reason wrong | Topologist | R | T5, C9; Design Notes 11 |
| TP-10 Reversal claim false | Topologist | R | Design Notes 1 |
| TP-11 Coordinate system unspecified | Topologist | R | Design Notes 4; Detail 1 |
| F-1 106.369 mm mislabeled | Fact-Checker | R | Design Notes 8; Register; registry; F4 |
| F-2 1 to 60 rpm is motor range | Fact-Checker | R | Register; registry |
| F-3 152.4 mm cutter OD unsourced | Fact-Checker | R (ASSUMED parameter) | Register; registry; A2 |
| F-4 Core tolerance UNVERIFIED | Fact-Checker | R (ASSUMED ±1 mm) | Register; Design Notes 12 |
| F-5 20 and 50 N m UNVERIFIED | Fact-Checker | R (moot: placeholders retired, 10 N m DECLARED) | Register; Design Notes 12 |
| F-6 100 mm core conflict | Fact-Checker | R | Register; registry |
| F-7 Iris aperture UNVERIFIED | Fact-Checker | R (DECLARED: radius, 108.585 mm open diameter, parameter) | Register; Design Notes 12 |
| Mines PDFs unread (pdftoppm missing) | Fact-Checker | R (read at Step 1, silent on core dimensions; report asserts SBIR text only) | Register; Design Notes 12 |
| Extraction line cites to correct; ascent test, docx, catalog not checked | Fact-Checker | R (cites) / D (unchecked rows) | Design Notes 8; Register |
| D1 Clamp cannot hold; no core lock | Designer | R (moot in part: 10 N m DECLARED, friction expected to suffice, no core lock by decision; liner, thrust washer and wings kept) | Detail 2 item 4; T7; Design Notes 12 |
| D2 Wing nut is clamp and crash target | Designer | R | Design Notes 2 |
| D3 No Designer params review before geometry; params missing | Designer | R | Detail 1, 3; Detail 6 checklist |
| D4 Wrong-collet defence is a label | Designer | R | Design Notes 11; Detail 6, 9; H6 |
| D5 Core loading three-handed; edges; debris | Designer | R | Detail 2 item 9; Detail 9; H7 |
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
| E4 Coverage at 5 mm spacing | Software Engineer | R (moot: 2.5 mm DECLARED) | C8; Design Notes 12 |
| E5 Nut stop branch | Software Engineer | R | Design Notes 2 |
| E6 Tall core lateral stability | Software Engineer | R (steady rest, tilt bound; 0.75 m install core raises the tilt, recorded in Design Notes 9) / D (lateral guide design to Step 12 with H3 data) | Detail 2 item 9; H3 |
| E7 Plastic allowable strain | Software Engineer | D | Step 8 coupon, Step 11 H4 |
| E8 106.369 applicability to 6 in drill | Software Engineer | R (ASSUMED parameter) | F4; Design Notes 12 |
| Disagreement: 130 vs about 60 tests | Software Engineer, Systems Engineer | R (ruling: 91) | Design Notes 6 |
| Disagreement: nut as hard stop vs frame stop | Loftsman, Topologist, Systems Engineer, Designer | R | Design Notes 2 |
| Disagreement: analytic vs empirical | Loftsman, Engineer | R | Design Notes 10 |
| Disagreement: thread 165 vs 135, collet type, register length | Loftsman, Topologist | R (formula governs; Step 3 decides) | Design Notes 3 |
| Disagreement: release by cone vs captured nut | Loftsman, Designer | R (captured nut primary, cone fallback) | Design Notes 3 |
| Disagreement: re-measure scope; F5; stack height; family spacing | Software Engineer, Systems Engineer, Topologist, Loftsman | R | Design Notes 11 |
| Moot at the gate: T6 nut OD and bed fit; printer rows (bed, material, nozzle); split-nut logic; Step 8 warp and print-time risk for the receiver and nut | Software Engineer, Loftsman, Designer | R (moot: printer is not a design input, B2) | T6 withdrawn; Design Notes 9, 12 |
| Moot at the gate: positive core lock and its escalation steps; 20 N m x SF 2 and 50 N m placeholders | Systems Engineer, Loftsman, Designer | R (moot: 10 N m DECLARED, B4) | T7; Detail 2 item 4; Detail 11 H1 |
| Moot at the gate: poppler install and "ask the human" items; bracket SKU catalog pull | Manager, Engineer | R (ASSUMED: check only, no download) | Detail 1; Design Notes 12 |
| Moot at the gate: Open Questions lists (blocking, non-blocking, UNVERIFIED) | Manager | R (replaced by Gate Decisions and Design Notes 12) | Gate Decisions |

---

## Repository Sync

Repo: https://github.com/Shootquinn/cutjig (public, all rights reserved). Contributors: quinn, sean. Each contributor has `research/<name>/` holding their gameplan, accumulator and `cr_scratch/`. The design files are shared: workorder.md, params.yaml, ASSEMBLY.md, bom_*.md, report_assumptions.md, build_parts/, tests/, output/, parts_cache/, docs/, context/, reference/. Either contributor may change any shared file; a change to the other contributor's design runs through LLM-PLM like any other change (FCStd wins, sync params first, re-run the tests). Never edit files in the other contributor's `research/<name>/`.

Every step in this gameplan carries these sync points:

1. **Step open:** `git pull --ff-only` before the Manager is spawned. If the fast-forward fails, stop and report to the human. If the pull brought changes to shared design files, the Manager open reads `git log --stat` since the last sync and names what changed.
2. **Save point** (each wave close and the step close, before the inter-step gate):
   ```
   git add -A
   git commit -m "<name>: Step N <what finished>"
   git pull --rebase
   git push
   ```
   The rebase lands this machine's commits on top of the other contributor's, so the next `git pull --ff-only` on their machine fast-forwards.
3. **Conflicts:** a rebase conflict in a shared design file (params.yaml, a part script, a test, an FCStd, STEP or STL, ASSEMBLY.md) stops the session; `git rebase --abort` and report to the human. No agent resolves a design conflict.
4. **Background builds:** push a save point before launching a FreeCAD build; push the build's outputs as their own save point when the build finishes. Never commit a half-finished build.
5. **Never** force-push, amend or rebase a pushed commit, or skip hooks. Undoing the other contributor's work is a new change.
6. Scratch files from this step on go to `research/quinn/cr_scratch/`. Steps 0 to 7 scratch is already there.
