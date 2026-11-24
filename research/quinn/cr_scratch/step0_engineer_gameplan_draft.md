# Core Cutter Test Jig Gameplan

**Document(s) under work:** workorder.md (core cutter test jig: base, core holder, wing nut, collet family; 3D models and technical report)
**Operational guide:** C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\method\operational_guide.md
**Accumulator file:** none, new project (created by The Manager at Step 0 close from templates/accumulator.md)
**Other reference files:**
- workorder.md
- supplements/llm_plm_cad.md (CAD active), supplements/freecad_api_reference.md
- method/tdd_method.md
- supplements/writing-guides/reporting-copy.md, structure.md, style.md, style-reference.md, supplements/signs_of_ai_writing.md
- research/quinn/cr_scratch/step0_engineer_source_extraction.md (cutter, envelope, load, core facts; tagged)
- research/quinn/cr_scratch/step0_human_stock_80-20.md (30-6060 stock on hand; DECLARED)
- research/quinn/cr_scratch/step0_manager_open.md
- SBIR folder: C:\Users\Quinn Morley\OneDrive\PROJECTS\Planet Enterprises\NIAC\BOREBOTS\Unleashed Robotics\2026 PROPOSALS\2026 SBIR\ (cr_scratch/INSITU2_text.md is the iris proposal text; cr_scratch/INSITU3_text.md for WOB; proposals/csm_sow.md; context/)
- Rigged drill model: C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\gpr (DOUBLE DONG, 7 in bore, NOT the 6 in redesign; see extraction section 1)
**Date:** 2026-11-08
**Current step:** 0
**lit_review:** yes
*Reason: the report will cite Mines/SBIR numbers (aperture, WOB, rpm, core diameter). Each test asserting such a number names its primary source. Sources summarized once into context/literature/ before tests cite them (Step 1).*

---

## Objectives

1. Review workorder.md as the contract and populate the gameplan (Step 0, drafting variant).
2. Initial work as 3D models, all built from a single parametric generator: base with threaded boss, core holder, wing nut, collet family for 90 to 105 mm cores, and the 30-6060 frame.
3. Prove the models by test: parametric, topology, interference, placement, printability, clearance. Each result carries evidence.
4. Deliver a concise technical report (executive summary crossed with an engineering-school project) through the TDD document path: test suite, outline, reporting copy, writing wave, Wave 2 review.
5. Scope the drill-holding upper assembly jointly with the human after base review.

---

## Document Structure

**The point, in one sentence:** A 30-6060 frame with a printed threaded base, wing nut and a four-collet family holds any 90 to 105 mm Mines core upright and coaxial under the 6.00 in OD / 5.75 in ID drill, with the cutter's iris closing on it from the drill's own drivetrain, and every number in the design traces to a source or a test.

**Shape:** Lead-first (LDR). The reader is an SBIR program manager and an engineering faculty member who may stop after page 1. Page 1 gives the design, the verification result, and what is deferred. Later sections give method and evidence.

**Opening promises:** Audience: SBIR program manager and engineering faculty. Breadth: the base, holder, wing nut, collet family, and frame, as designed and as verified in CAD and print tests. Does not promise a built upper assembly or test data from a drill.
**Resolution delivers:** The same breadth: models, test evidence, bill of materials, status of upper assembly scoping. No claim of flight representativeness or mechanism performance.

**Known limitations and where each goes:**

| Limitation | Placed in | Why there |
|---|---|---|
| Cutting face (sets borehole and core diameter) out of scope | Scope paragraph, section 1 | Reader needs it before any dimension |
| Jig does not actuate the iris; the drill drivetrain does | Section 2 (interfaces) | A reader assuming a jig actuator would misread the load path |
| Upper assembly deferred, jointly scoped with the human | Section 7 (status and next step) | It is the next action, not a caveat |
| Printed parts are not flight-representative; PETG creep and thread wear | Section 5 (printability) with the test that bounds it | Placed with the evidence that bounds the effect |
| Core length, mass and torque not stated by any source | Section 2, as open inputs with the design margin used | Margin choice is part of the design |
| Rigged model is the 7 in drill, not 6 in | Appendix A (source notes) | Source provenance, not design |
| Printing and fit validated in CAD and analytical coupons only until the human prints | Section 7 | The human's print result is the next gate |

Report outline (8 to 12 pages, DOCX plus PDF): 1 Summary and scope; 2 Requirements and interfaces; 3 Concept (stack, load path); 4 Collet family (generator, taper, slit); 5 Printability and tolerances; 6 Verification (interference, placement, topology, independent re-measure); 7 Status, upper assembly scoping, open items; Appendix A source notes; Appendix B BOM and stock allocation; Appendix C drawings and renders. Topic-sentence outline is built in Step 11, not here.

---

## Steps

| # | Step | Assigned To | Status |
|---|------|-------------|--------|
| 0 | Team reviews workorder.md, populates this gameplan; Software Engineer revises for tests; reviewers weigh in; Engineer revises; Manager closes. Gate to human. | The Manager (open, close), The Engineer (plan, write), The Software Engineer, The Systems Engineer, The Loftsman, The Topologist, The Designer | In progress (this draft) |
| 1 | Foundation and CAD test suite (red-first). See detail 1. | The Engineer (build), The Software Engineer (review), The Fact-Checker (source gate) | Not started |
| 2 | Geometry pre-build cross-review: thread, taper, slit and seat math. See detail 2. | The Loftsman, The Topologist (cross-review), The Engineer (script), The Software Engineer (tests) | Not started |
| 3 | Parametric collet-family generator. See detail 3. | The Engineer (build), The Software Engineer (test review) | Not started |
| 4 | Exploratory pass (Pass 1): base with threaded boss, core holder, wing nut, collets, frame. See detail 4. | The Engineer, The Loftsman, The Topologist, The Designer (gate) | Not started |
| 5 | Assembly, interference and placement tests. See detail 5. | The Engineer, The Software Engineer, The Systems Engineer | Not started |
| 6 | Printability and tolerance tests (thread clearance, slit flex, bed fit, overhang). See detail 6. | The Engineer, The Loftsman, The Software Engineer | Not started |
| 7 | Production pass (Pass 2) on every part, Designer quality gate. See detail 7. | The Engineer, The Loftsman, The Topologist, The Designer (gate) | Not started |
| 8 | Final assembly, independent re-measure, STEP/STL/FCStd outputs, Software Engineer code review. See detail 8. | The Engineer, The Topologist, The Software Engineer, The Systems Engineer | Not started |
| 9 | Base review package and inter-step gate: human reviews models, prints a thread coupon and one collet. | The Manager (close), the human | Not started |
| 10 | Joint scoping step with the human for the drill-holding upper assembly. See detail 10. | The Manager, The Systems Engineer, The Engineer, the human | Not started |
| 11 | Report test suite (tdd_method Prompt 1), source-verified. | The Software Engineer (author and review), The Fact-Checker (source gate) | Not started |
| 12 | Report topic-sentence outline (Prompt 2), validated against the suite. | The Software Engineer (validate), The Engineer (draft), The Designer (structure) | Not started |
| 13 | Engineer reporting copy (loads supplements/writing-guides/reporting-copy.md). | The Engineer | Not started |
| 14 | Writing wave, Writer first: compose manuscript. | The Writer | Not started |
| 15 | Writing wave, Editor second: AI-tell removal, clarity. | The Editor | Not started |
| 16 | Wave 2 review: Designer, Fact-Checker, Systems Engineer. | The Designer, The Fact-Checker, The Systems Engineer | Not started |
| 17 | Revision, DOCX and PDF build, final suite run, echo-site audit. | The Engineer, The Software Engineer, The Designer | Not started |
| 18 | Close: accumulator, archive, gate to human. | The Manager | Not started |

Steps after 10 may be re-sequenced by the human at the Step 9 and Step 10 gates; if the upper assembly enters the report scope, Steps 11 to 13 wait for the Step 10 work order.

### Step details

**Detail 1. Foundation and CAD test suite.**
Objective: contract in code before geometry exists.
TDD stage: test suite first (llm_plm_cad 7.2); run red on the empty baseline; label invariants.
Inputs: workorder.md, extraction file, stock file, Manager defaults (resolved below).
Outputs: `params.yaml` (seed), `ASSEMBLY.md`, `build_parts/common.py` (paths, YAML loader, thread spec, 30-6060 profile builder), `conftest.py`, `tests/test_jig.py`, `tests/test_report_*.py` stubs deferred to Step 11, `research/quinn/cr_scratch/step1_engineer_baseline.md`, BOM files `bom_stock_allocation.md` and `bom_purchased.md`, `context/literature/` summaries for each cited source (md-summary-chat-prompt).
Work: confirm FreeCAD install at `C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe`; confirm the 30-6060 cross-section against the catalog (60 x 60 mm, 30 mm slot pitch) and model it as a parametric extrusion; compute the stock allocation (see Design Notes) and list extra cuts separately; fix the bracket class and T-nut rule.
Tests include: params validation; Boolean expected-delta; topology gate (7.1); every cited number names its source (lit_review); known-bad and zero control for each numeric gate (tdd_method principle 9).
Gate: Software Engineer signs the suite; Fact-Checker signs source gate (A.10 step 2); red-first record exists. Background rule: any FreeCAD run over 30 s goes background (A.3.4).

**Detail 2. Geometry pre-build cross-review.**
Objective: settle thread, taper, slit, seat math on paper and by script before any solid.
TDD stage: tests for each formula (thread major/minor, pitch, lead, chirality, taper angle, seat cone half-spaces, slit width vs wall flex) written before the generator.
Work: The Loftsman derives trapezoidal thread profile (default Tr 60 x 8, coarse for FDM), clearance per side, taper angle for the collet-to-holder cone, collet bore = core diameter with a net interference band; The Topologist defines seating half-spaces, thread handedness and mate invariants for the whole family (A.4 geometry cross-review rule: two geometry-competent personas before build). Output: `research/quinn/cr_scratch/step2_loftsman_geometry.md`, `research/quinn/cr_scratch/step2_topologist_invariants.md`, `tests/test_geometry_math.py`.
Gate: both personas sign; any disagreement resolved by number, not opinion.

**Detail 3. Collet-family generator.**
Objective: one generator, diameter-driven, producing the whole family from `params.yaml`; no hand-built collets.
TDD stage: tests first (family count, bore = d, taper identical across the family, slit count, volume bands), then build.
Outputs: `build_parts/collet_family.py` (function `build_collet(d)`), `parts_cache/collet_090.FCStd` to `collet_105.FCStd`, `parts_cache/collet_*_result.json`. Per-part scripts per A.14.
Family: 90, 95, 100, 105 mm (default). The generator takes any d in 90 to 105, so adding a 2.5 mm increment is a params change only.
Gate: every FCStd single valid solid; volume ratio 0.95 to 1.05 of analytic; topology gate. Builds are independent, so run them as parallel background FreeCADCmd processes if the batch exceeds 30 s (A.15).

**Detail 4. Exploratory pass.**
Objective: surface problems; every functional feature present, even if simplified (7.6).
Parts: base with threaded boss and debris tray, core holder, wing nut (large, with wings), collets (via generator), 30-6060 frame members and brackets as simple parametric bodies.
Required functional features present: boss thread, seat/taper, collet slit, anti-rotation key or flat, wing nut wings and thread, T-nut and bracket mounting provisions, core stop, drain/debris provision.
Outputs: `build_parts/<part>.py` per part, `parts_cache/*.FCStd`, `research/quinn/cr_scratch/step4_engineer_findings.md`.
Gate: The Designer on completeness ("can we learn from this?"). Missing feature fails the gate.

**Detail 5. Assembly, interference, placement.**
TDD stage: tests first, including negative controls.
Outputs: `build_parts/assemble.py`, `output/jig_assembly.FCStd`, `output/jig_assembly.step`, `tests/test_assembly.py`, `research/quinn/cr_scratch/step5_interference_report.md` (per-pair table, mm3, pass/fail).
Checks: all neighbor pairs Boolean-common volume < 0.01 mm3 (7.4); placement audit (7.5); fit-with-clearance family sweep (each collet with each nominal core diameter from 90 to 105); cutter envelope check: a 152.4 mm OD / 146.05 mm ID tube modeled as keep-out and swept down the axis; no fixture inside the tube radius within the descent stroke, and the exposed core above the holder at least 106.4 mm (extraction section 3) plus margin. Known-bad: a planted overlapping part must fire.
Visual: turntable or multi-view render read by an image-capable reviewer against a written rubric (A.3.1).
Gate: Software Engineer, Systems Engineer.

**Detail 6. Printability and tolerance tests.**
Objective: show parts print and fit before the human spends filament.
Work: analytic checks (min wall, overhang angle, bed fit 256 mm class, thread clearance per side, slit flex strain at clamp, wing nut moment arm); print coupons as STL: threaded boss/nut coupon, one collet at 100 mm, a collet slit flex bar. Human prints at Step 9; results feed back as a change order.
Outputs: `tests/test_printability.py`, `output/coupons/*.stl`, `research/quinn/cr_scratch/step6_printability.md`.
Gate: Loftsman reviews thread clearance; Software Engineer reviews tests.

**Detail 7. Production pass.**
Objective: every feature deployment-ready (7.6): chamfers and fillets where they serve function, thread lead-ins, wing profiles, key fits, fastener counterbores, labels (core diameter engraved on each collet), poka-yoke against wrong-collet and cross-threading. Fits and tolerances specified from Step 6.
Outputs: updated part scripts and FCStds; change-order record if params diverge from FCStd (FCStd wins; sync first, 5.2.1).
Gate: The Designer, quality and pride test ("would a printer operator produce a functional part?").

**Detail 8. Final assembly and independent re-measure.**
Work: re-run Steps 5 and 6 tests on production geometry; independent re-measure script that shares no code with build or tests, with negative controls (probes away from the feature must still hit); source files hashed before and after; delivered FCStd opens with every deliverable object visible and named, count computed from object counts.
Outputs: `output/jig_assembly.FCStd`, `.step`, `output/stl/*.stl` for every printable part, `research/quinn/cr_scratch/step8_remeasure.md`, renders, turntable MP4 (background if over 30 s), `ASSEMBLY.md` complete, BOM final.
Gate: Software Engineer code review slot (tests meaningful, no ceremony); Topologist final topology gate; Systems Engineer interface review (base to collet to holder to nut to frame to future upper assembly).

**Detail 10. Joint scoping for the upper assembly.**
Objective: define the drill-holding upper assembly with the human after base review.
Agenda drawn from the extraction: guide/anchor for the 152.4 mm OD drill; WOB path up to 1000 N; torque reaction (value unknown); descent method and rate; instrumentation access (load cell and Hall sensor cabling at the back cap); whether a spindle drive is in jig scope (if yes, spawn The Motor Designer); iris closure confirmation; end stop above the wing nut.
Outputs: `research/quinn/cr_scratch/step10_scoping_notes.md`, a new work order `workorder_upper_assembly.md`, and an appended gameplan section with Steps 10.1 and up. Decision recorded: does the report cover the upper assembly or defer it.

**Detail 11 to 17. Report path** (document steps; test suite then outline, per A.4 TDD precondition).
- 11: around 150 tests (8 to 12 page report; scale by judgment), organized whole-document and section-level; thesis statement in the plan; audience-comprehension and communication-architecture tests (A.10 item 7); every numeric claim test names its primary source (lit_review); zero control and known-bad control for each detector (AI-tell grep, echo-site audit). Output: `report_test_suite.md`. Software Engineer authors and reviews; Fact-Checker verifies source attributions.
- 12: paragraph-level topic-sentence outline, validated against the suite before any prose. Output: `report_outline.md`.
- 13: Engineer writes reporting copy from the Step 8 evidence, loading supplements/writing-guides/reporting-copy.md only (no prose style reference). Output: `report_reporting_copy.md`.
- 14: Writer composes from reporting copy plus Wave 1 outputs (loads structure.md, style.md; style-reference.md on demand). Output: `report_draft_writer.md`.
- 15: Editor removes AI tells and tightens (loads signs_of_ai_writing.md). Output: `report_draft_editor.md`. Default order Writer then Editor since the input is raw reporting copy.
- 16: Wave 2: Designer (communication, echo-site audit), Fact-Checker (every cutter dimension and requirement vs SBIR and model sources, source gate), Systems Engineer (interfaces, load path, limits). Outputs: `research/quinn/cr_scratch/step16_designer.md`, `step16_factcheck.md`, `step16_systems.md`.
- 17: revise; build DOCX (claude-docx-bundle house style) and PDF; run the suite; echo audit against the registry; Software Engineer final suite run. Outputs: `CoreCutterTestJig_Report.docx`, `.pdf`.

---

## Context Recipes

| Step | Agent | Files / Excerpts |
|------|-------|-----------------|
| 0 | The Manager | workorder.md, this gameplan, method/operational_guide.md (A.4, A.6, A.12), accumulator (none) |
| 0 | The Engineer | workorder.md, templates/gameplan.md, extraction file, stock file, supplements/llm_plm_cad.md, method/tdd_method.md |
| 0 | The Software Engineer | workorder.md, Engineer's draft, method/tdd_method.md, llm_plm_cad.md section 7 |
| 0 | Reviewers (Systems Eng, Loftsman, Topologist, Designer) | workorder.md, revised draft, extraction file |
| 1 | The Engineer | workorder.md, gameplan, llm_plm_cad.md, freecad_api_reference.md, extraction file, stock file |
| 1 | The Software Engineer | gameplan, tests/, params.yaml, tdd_method.md, llm_plm_cad.md section 7 |
| 1 | The Fact-Checker | tests asserting numbers, extraction file, context/literature/ summaries, source documents on disk |
| 2 | The Loftsman | params.yaml, extraction sections 2 and 3, freecad_api_reference.md (thread/helix), step 2 test file |
| 2 | The Topologist | params.yaml, llm_plm_cad.md 7.1, 11, Loftsman output |
| 3 | The Engineer | params.yaml, common.py, step 2 outputs, tests/test_collet_family.py |
| 3 | The Software Engineer | collet_family.py, tests, params.yaml (code review recipe) |
| 4 | The Engineer | params.yaml, common.py, collet_family.py, step 2 outputs, ASSEMBLY.md |
| 4 | The Loftsman, Topologist | part scripts, FCStds results JSON, step 2 outputs |
| 4 | The Designer | params.yaml, renders, step 4 findings (no scripts) |
| 5 | The Engineer, Software Engineer | assemble.py, tests/test_assembly.py, ASSEMBLY.md, interference report |
| 5 | The Systems Engineer | ASSEMBLY.md, interference report, extraction sections 3 to 5 |
| 6 | The Engineer, Loftsman | part scripts, step 2 thread clearance outputs, printer constraints (Design Notes) |
| 7 | The Engineer, Loftsman, Topologist | step 4 findings, step 5 and 6 reports, part scripts |
| 7 | The Designer | step 4 findings, renders of production parts |
| 8 | The Engineer | all of the above, hash manifest |
| 8 | The Software Engineer | build_parts/, tests/, results JSON |
| 8 | The Topologist, The Systems Engineer | assembly FCStd/STEP, ASSEMBLY.md, interference report |
| 10 | The Manager, Systems Engineer | step 8 outputs, extraction file, workorder.md |
| 11 | The Software Engineer | workorder.md, gameplan Document Structure, extraction file, tdd_method.md |
| 11 | The Fact-Checker | test suite, source documents, context/literature/ |
| 12 | The Software Engineer, Engineer | test suite, gameplan Document Structure, structure.md |
| 13 | The Engineer | reporting-copy.md (full), Step 5 to 8 results with sources, report_outline.md |
| 14 | The Writer | structure.md, style.md (full), style-reference.md (on demand), reporting copy, outline |
| 15 | The Editor | signs_of_ai_writing.md (full), Writer draft, suite AI-writing criteria, origin info |
| 16 | The Designer | diff since Step 15, full report, echo site registry |
| 16 | The Fact-Checker | full report plaintext, source documents, context/literature/, echo registry |
| 16 | The Systems Engineer | report, ASSEMBLY.md, step 8 outputs |
| 17 | The Engineer | edited draft, review outputs, claude-docx-bundle |
| 18 | The Manager | gameplan, all step outputs |

---

## Echo Site Registry

Each row: value, authoritative source, derived locations. Bold values on use. First-use rule: introduce with its context the first time in each section.

| Value | Authoritative source | Derived locations |
|---|---|---|
| Core nominal diameter **100 mm** | INSITU2_text.md line 406-407; params.yaml `core.nominal_d` | report 1, 2, 4; collet 100 file name; tests |
| Collet diameters **90, 95, 100, 105 mm** | params.yaml `collets.diameters` | report 4; collet filenames; interference sweep; BOM |
| Core accepted range **90 to 105 mm** | workorder.md | report 1, 4; collet generator bounds |
| Tubing **6.00 in OD / 5.75 in ID (152.40 / 146.05 mm)**, wall 1/8 in | workorder.md; params.yaml `drill.*` | report 2, 3, 6; envelope test; cutter keep-out solid |
| Radial gap 100 mm core **23.025 mm** (90: 28.025; 105: 20.525) | derived from the two rows above, params.yaml | report 2; clearance test |
| Iris leaf count **4** and standoff **106.369 mm** (7 in model) | gpr double_dong_params.py `IRIS_LEAVES`, `CORE_IRIS_STANDOFF_MM` | report Appendix A; minimum exposed core height |
| Boss thread spec **Tr 60 x 8** (default, pending Step 2) | params.yaml `boss.thread` | boss, wing nut, base scripts; report 4, 5; thread coupon |
| Wing nut diameter (**TBD in Step 2**, bounded by bed 256 mm) | params.yaml `wingnut.od` | report 3; print bed test; cutter stop height |
| Profile series **30-6060** (60 x 60 mm, M6 roll-in T-nut) | research/quinn/cr_scratch/step0_human_stock_80-20.md | frame scripts; BOM; report 3, Appendix B |
| Printer bed **256 x 256 x 256 mm** (default) | params.yaml `printer.bed` | bed-fit test; report 5 |
| Design load rating (axial **1000 N** WOB upper bound; torque placeholder 20 N m, unsourced) | extraction C4, C5; params.yaml `loads.*` | frame sizing; report 2 |
| Spin **1 to 60 rpm** | context/summary_yokeless_motor.md | report 2; scoping step |
| Stock lengths and allocation | step0_human_stock_80-20.md; bom_stock_allocation.md | BOM, report Appendix B |

Authority rule (A.16): geometry values live in params.yaml until an FCStd exists, then the FCStd; report values must match the authority, not each other. A within-file contradiction is a nonconformance and blocks step close.

---

## Progress Log

| Step | Date | Notes |
|------|------|-------|
| 0 | 2026-11-08 | Opened. Work order locked as workorder.md. Engineer extraction and draft written (cr_scratch). Human stock input (30-6060) and T-nut/bracket constraints folded in. |

---

## Design Notes

**Source findings that change the design (extraction file):**
- The iris is closed by the drill's own drivetrain (braked planetary sun gear). The jig supplies no iris actuator. Jig duties: hold the core coaxial, react WOB and torque, guard the cutter stroke.
- Bore check: 146.05 mm vs 90 to 105 mm cores leaves 28.025 to 20.525 mm radial gap per side. Pass.
- The iris pinches the core 106.369 mm behind the cutting face (7 in model). The exposed core above the holder must exceed that, so the holder must be low and the cutter's lowest point must stop above the holder top. Re-derive for the 6 in drill when its iris is measured.
- Fixtures inside the descent path must clear 146.05 mm bore minus margin; a wing nut wider than 146.05 mm is a hard cutter stop and must sit below the cutting face's lowest position. Stop height is a parameter.
- The rigged model is the 7 in generation, not the 6 in. The 2026 STEP's size is not confirmed.

**Stack concept (tentative, Step 2 confirms):** Base plate with threaded boss rising (external trapezoidal thread). Core holder is a sleeve with an internal taper that seats on the boss. A slit collet with matching external taper and a bore equal to the core diameter sits inside the holder. The wing nut threads onto the boss and presses the holder axially, which closes the collet on the core. The core base seats on a stop inside the collet. Collet inside diameter chosen per diameter, family generated from d. The Loftsman and Topologist may reverse the stack order if the half-space analysis requires.

**80/20 hardware (human input, DECLARED):**
- Profile: 80/20 30-6060, 60 x 60 mm, 30 mm slot pitch. No smaller profile. Fasteners M6.
- T-nuts: M6 spring-ball roll-in only, for the 30-6060 slot. No other T-nut type anywhere in the design or BOM.
- Brackets: ordered catalog brackets are acceptable; printed or fabricated brackets may be designed. Any ordered bracket must be full size for the 30-series profile, never a "mini" bracket. BOM names the bracket SKU or the full-size class. SKUs are not verified in Step 0; Step 1 pulls them from the 80/20 catalog (open question).
- Stock on hand, mm x quantity: 1540 x 4, 980 x 4, 952 x 1, 728 x 2, 644 x 2, 488 x 2, 468 x 2 (15,688 mm total). Believed uncut; shared with other projects. Design from stock first. Extra cuts of 30-6060 are allowed (about $2.20 per cut at the QMRD3 order, DECLARED) and go in a separate BOM table with quantities.
- Starting allocation to test in Step 1, to be confirmed: base frame from the shorter stock (644 x 2, 468 x 2, 488 x 2 for perimeter and cross members); the 1540 mm lengths are reserved for columns in the upper-assembly work (Step 10) and are not consumed in Steps 1 to 9 except as the human directs. `bom_stock_allocation.md` records which stock lengths the jig consumes, for the other projects.

**Printing:** default 256 mm class bed, PETG for jig parts, PLA for fit coupons, 0.4 mm nozzle; coarse Tr thread because fine printed threads fail. Wing nut sized to the bed or split.

**Process rules carried in:** per-part scripts, one FCStd each (A.14); FCStd is authority once built (2.1); Boolean expected-delta and topology gate after each cut (7.1); any build over 30 s runs in the background and the PID, log path and expected finish are logged here (A.3.4); under FreeCAD 1.1.4 success is a sentinel line plus a fresh artifact, not exit code (A.15).

**Software Engineer review slots:** Step 1 (suite), Step 3 (generator code), Step 5 (assembly tests), Step 8 (code and test review), Steps 11 and 12 (report suite, outline).
**Loftsman and Topologist cross-review slots (A.4 geometry rule):** Step 2 (before any build: thread, taper, slit, seat), Step 4 (exploratory geometry), Step 7 (production geometry), Step 8 (topology gate).

---

## Open Questions

Resolved by the human: item 1, profile series = 30-6060, M6 spring-ball roll-in T-nuts, full-size brackets only.

Proposed defaults (Manager section 4, adjusted by the sources):
1. Bracket SKUs: full-size 30-series class; Step 1 selects SKUs from the 80/20 catalog. Confirm on-hand bracket and M6 screw inventory.
2. Printer bed, material, nozzle: 256 mm class, PETG/PLA, 0.4 mm. Need actual printer.
3. Collet increments: 90, 95, 100, 105 mm; add a plain 100 mm master only if the human wants one. Mines core tolerance: default +/-1 mm. Mines has not stated one.
4. Core length and mass: default 100 mm x 150 to 500 mm (500 mm used by Quinn's animation), mass up to 10 kg at an assumed 2400 kg/m3 (DERIVED, unverified). Ask Mines for length, density and delivery state (wet, wrapped, sleeved).
5. Loads: sources give WOB 100 to 1000 N, so the default axial design load rises to 1000 N (was 500 N). Torque: no source; keep 20 N m as a placeholder for the jig and mark it UNVERIFIED until Phase I measures closure torque. Safety factor 3 on printed parts.
6. Spin and descent: 1 to 60 rpm (was 60 to 300). Descent rate: no source for the jig; Phase I pass threshold is 5 mm/min at WOB 100 N or more. Hand crank or leadscrew deferred to Step 10.
7. Debris: indoor, debris tray in the base.
8. Report: 8 to 12 pages, DOCX plus PDF in house style.
9. CAD chain: FreeCAD 1.1 headless per llm_plm_cad; confirm install and whether a 6 in drill STEP exists to import.
10. Boss thread: Tr 60 x 8 default; Step 2 may change it.
11. Which of the two 2026-09-11 STEP files is the 6 in drill, and the iris open aperture in that design (extraction section 7).
12. Does the report cover the upper assembly or defer it (decided at Step 10).
13. Fasteners for non-80/20 joints: stainless M6 (was M8 under 1515 assumption; 30-6060 uses M6).
