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
**Current step:** 0 (Software Engineer revision of the Engineer's draft; engineering content untouched, flags in "Flags to the Engineer")
**lit_review:** yes
*Reason: the report will cite Mines/SBIR numbers (aperture, WOB, rpm, core diameter). Each test asserting such a number names its primary source and carries a verification status (see Source Verification Register). Sources are summarized once into context/literature/ before tests cite them (Step 1), and only the sources a test actually cites get a summary (INSITU2, INSITU3, csm_sow, gpr params, motor summary). No others.*

---

## Objectives

1. Review workorder.md as the contract and populate the gameplan (Step 0, drafting variant).
2. Initial work as 3D models, all built from a single parametric generator: base with threaded boss, core holder, wing nut, collet family for 90 to 105 mm cores, and the 30-6060 frame.
3. Prove the models by scripted test with named pass criteria: per-collet volume and diameter, thread engagement, collet seat fit, interference matrix, placement signs, wing nut clamp range at 90 and 105 mm, STEP/STL validity. Each result carries evidence.
4. Deliver a concise technical report (executive summary crossed with an engineering-school project) through the TDD document path: test suite (Prompt 1), topic-sentence outline (Prompt 2) validated against the suite before any drafting, reporting copy, writing wave, Wave 2 review.
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

Report outline (8 to 12 pages, DOCX plus PDF): 1 Summary and scope; 2 Requirements and interfaces; 3 Concept (stack, load path); 4 Collet family (generator, taper, slit); 5 Printability and tolerances; 6 Verification (interference, placement, topology, independent re-measure); 7 Status, upper assembly scoping, open items; Appendix A source notes; Appendix B BOM and stock allocation; Appendix C drawings and renders. The topic-sentence outline is built in Step 12 (the draft said Step 11 here and Step 12 in the table; Step 12 is correct, the suite is Step 11).

---

## Steps

| # | Step | Assigned To | Status |
|---|------|-------------|--------|
| 0 | Team reviews workorder.md, populates this gameplan; Software Engineer revises for tests; reviewers weigh in; Engineer revises; Manager closes. Gate to human. | The Manager (open, close), The Engineer (plan, write), The Software Engineer, The Systems Engineer, The Loftsman, The Topologist, The Designer | In progress (Software Engineer revision done; Engineer next) |
| 1 | Foundation and CAD test suite (red-first), source-gated. See detail 1. | The Engineer (build), The Software Engineer (review, signs suite), The Fact-Checker (source gate) | Not started |
| 2 | Geometry pre-build cross-review: thread, taper, slit and seat math. See detail 2. | The Loftsman, The Topologist (cross-review), The Engineer (script), The Software Engineer (tests) | Not started |
| 3 | Parametric collet-family generator. See detail 3. | The Engineer (build), The Software Engineer (test review) | Not started |
| 4 | Exploratory pass (Pass 1): base with threaded boss, core holder, wing nut, collets, frame. See detail 4. | The Engineer, The Loftsman, The Topologist, The Designer (gate) | Not started |
| 5 | Assembly, interference, placement, clamp-range tests. See detail 5. | The Engineer, The Software Engineer, The Systems Engineer | Not started |
| 6 | Printability and tolerance tests (thread clearance, slit strain, bed fit, min wall). See detail 6. | The Engineer, The Loftsman, The Software Engineer | Not started |
| 7 | Production pass (Pass 2) on every part, Designer quality gate. See detail 7. | The Engineer, The Loftsman, The Topologist, The Designer (gate) | Not started |
| 8 | Final assembly, independent re-measure of the exported files, STEP/STL/FCStd outputs, Software Engineer code review. See detail 8. | The Engineer, The Topologist, The Software Engineer, The Systems Engineer | Not started |
| 9 | Base review package and inter-step gate: human reviews models, prints a thread coupon and one collet. | The Manager (close), the human | Not started |
| 10 | Joint scoping step with the human for the drill-holding upper assembly. See detail 10. | The Manager, The Systems Engineer, The Engineer, the human | Not started |
| 11 | Report test suite (tdd_method Prompt 1, about 130 tests), source-verified. See detail 11. | The Software Engineer (author and review), The Fact-Checker (source gate) | Not started |
| 12 | Report topic-sentence outline (Prompt 2), validated against the suite BEFORE any drafting. See detail 12. | The Engineer (draft), The Software Engineer (validate, signs), The Designer (structure) | Not started |
| 13 | Engineer reporting copy (loads supplements/writing-guides/reporting-copy.md). Does not open until the Step 12 validation record exists (A.4). | The Engineer | Not started |
| 14 | Writing wave, Writer first: compose manuscript. | The Writer | Not started |
| 15 | Writing wave, Editor second: AI-tell removal, clarity. | The Editor | Not started |
| 16 | Wave 2 review: Designer, Fact-Checker, Systems Engineer. | The Designer, The Fact-Checker, The Systems Engineer | Not started |
| 17 | Revision, DOCX and PDF build, final suite run, echo-site audit. | The Engineer, The Software Engineer, The Designer | Not started |
| 18 | Close: accumulator, archive, gate to human. | The Manager | Not started |

Steps after 10 may be re-sequenced by the human at the Step 9 and Step 10 gates; if the upper assembly enters the report scope, Steps 11 to 13 wait for the Step 10 work order.

### Step details

**Detail 1. Foundation and CAD test suite.**
Objective: contract in code before geometry exists.
TDD stage: the complete CAD suite (all groups in the CAD Test Specification below) is written in Step 1, including gates for later steps, then run red on the empty baseline; each test is labelled discriminator or invariant (7.2). Tests whose thresholds depend on Step 2 math carry `pending: step2` and read their threshold from `params.yaml`; Step 2 fills the value, it does not rewrite the test. Any later suite change is a suite revision with Software Engineer review and source re-check (A.10 item 5).
Inputs: workorder.md, extraction file, stock file, Manager defaults (resolved below).
Outputs: `params.yaml` (seed, every externally sourced number carries a `source:` key and a `status:` of TRACED or UNVERIFIED), `ASSEMBLY.md`, `build_parts/common.py` (paths, YAML loader, thread spec, 30-6060 profile builder), `conftest.py`, five test modules (`tests/test_params_bom.py`, `test_collet_family.py`, `test_thread_clamp.py`, `test_assembly.py`, `test_exports.py`; no `test_jig.py` catch-all), `research/quinn/cr_scratch/step1_engineer_baseline.md` (red-first record), BOM files `bom_stock_allocation.md` and `bom_purchased.md`, `context/literature/` summaries (cited sources only).
Cut from the draft: `tests/test_report_*.py` stubs. The report suite is a markdown spec with a few small checker scripts, written at Step 11. Empty stubs are ceremony.
Work: confirm FreeCAD install at `C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe`; confirm the 30-6060 cross-section against the catalog (60 x 60 mm, 30 mm slot pitch) and model it as a parametric extrusion; compute the stock allocation (see Design Notes) and list extra cuts separately; fix the bracket class and T-nut rule.
Gate: Software Engineer signs the suite; Fact-Checker signs the source gate (A.10 item 2) against the Source Verification Register below; red-first record exists. Background rule: any FreeCAD run over 30 s goes background (A.3.4).

**Detail 2. Geometry pre-build cross-review.**
Objective: settle thread, taper, slit, seat math on paper and by script before any solid.
TDD stage: tests for each formula (thread major/minor, pitch, lead, chirality, taper angle, seat cone half-spaces, slit width vs wall flex, clamp-range relation) exist from Step 1; this step supplies the numbers they read.
Work: The Loftsman derives trapezoidal thread profile (default Tr 60 x 8, coarse for FDM), clearance per side, taper angle for the collet-to-holder cone, collet bore relation to core diameter, collet clamp range (the +/- mm of core diameter one collet grips); The Topologist defines seating half-spaces, thread handedness and mate invariants for the whole family (A.4 geometry cross-review rule: two geometry-competent personas before build). Output: one file `research/quinn/cr_scratch/step2_geometry_crossreview.md` with both personas' derivations and two sign-offs (the draft's two files are merged: the rule requires cross-review, not two documents). `tests/test_geometry_math.py` is dropped; its formula checks live in `test_thread_clamp.py` and `test_collet_family.py`.
Gate: both personas sign; any disagreement resolved by number, not opinion. Open numbers go to `params.yaml` with `status: UNVERIFIED` until a source or the Step 9 print confirms them.

**Detail 3. Collet-family generator.**
Objective: one generator, diameter-driven, producing the whole family from `params.yaml`; no hand-built collets.
TDD stage: tests first (groups C and F below), then build.
Outputs: `build_parts/collet_family.py` (function `build_collet(d)`), `parts_cache/collet_090.FCStd` to `collet_105.FCStd`, `parts_cache/collet_*_result.json`. Per-part scripts per A.14.
Family: 90, 95, 100, 105 mm (default). The generator takes any d in 90 to 105, so adding a 2.5 mm increment is a params change only.
Gate: every collet passes tests C1 to C7 (volume and diameter checks, below) and the coverage test C8; topology gate. Builds are independent, so run them as parallel background FreeCADCmd processes if the batch exceeds 30 s (A.15).

**Detail 4. Exploratory pass.**
Objective: surface problems; every functional feature present, even if simplified (7.6).
Parts: base with threaded boss and debris tray, core holder, wing nut (large, with wings), collets (via generator), 30-6060 frame members and brackets as simple parametric bodies.
Required functional features present: boss thread, seat/taper, collet slit, anti-rotation key or flat, wing nut wings and thread, T-nut and bracket mounting provisions, core stop, drain/debris provision. Feature presence is test F5 (a list-driven check: feature name in the part's result JSON with a nonzero removed or added volume).
Outputs: `build_parts/<part>.py` per part, `parts_cache/*.FCStd`, `research/quinn/cr_scratch/step4_engineer_findings.md`.
Gate: The Designer on completeness ("can we learn from this?"). Missing feature fails the gate.

**Detail 5. Assembly, interference, placement, clamp range.**
TDD stage: tests first (groups T, A below), including negative controls.
Outputs: `build_parts/assemble.py`, `output/jig_assembly.FCStd`, `output/jig_assembly.step`, `tests/test_assembly.py`, `tests/test_thread_clamp.py`, `research/quinn/cr_scratch/step5_interference_report.md` (per-pair table, mm3, pass/fail, one table per collet configuration).
Checks: interference matrix (A1), cutter envelope keep-out (A2), placement and sign checks (A3), thread engagement and clamp range at 90 and 105 mm (T4, T5), collet and core fit sweep (F1 to F3). Known-bad: a planted overlapping part must fire; a planted flipped part must fire.
Visual: a four-view PNG set (front, side, top, isometric) read by an image-capable reviewer against a written rubric (A.3.1). The draft's turntable MP4 is cut (Recommended in Section 10, not mandatory, and the PNG set carries the same gate for a one-off jig).
Gate: Software Engineer, Systems Engineer.

**Detail 6. Printability and tolerance tests.**
Objective: show parts print and fit before the human spends filament.
Work: analytic and geometric checks (min wall, bed fit 256 mm class, thread clearance per side, slit strain at clamp); print coupons as STL: threaded boss/nut coupon, one collet at 100 mm, a collet slit flex bar. Human prints at Step 9; results feed back as a change order.
Cut from the draft: analytic overhang-angle script (the slicer preview at Step 9 shows overhangs in ten seconds and the printer is unconfirmed) and the wing nut moment-arm check (hand tightening; the human's first turn of the nut is the real test; the nut is already bounded by the bed-fit test).
Outputs: `tests/test_printability.py` (part of `test_collet_family.py` and `test_exports.py` where it shares fixtures), `output/coupons/*.stl`; results table appended to `research/quinn/cr_scratch/step5_interference_report.md` rather than a separate `step6_printability.md`.
Gate: Loftsman reviews thread clearance; Software Engineer reviews tests.

**Detail 7. Production pass.**
Objective: every feature deployment-ready (7.6): chamfers and fillets where they serve function, thread lead-ins, wing profiles, key fits, fastener counterbores, labels (core diameter engraved on each collet), poka-yoke against wrong-collet and cross-threading. Fits and tolerances specified from Step 6.
Outputs: updated part scripts and FCStds; change-order record if params diverge from FCStd (FCStd wins; sync first, 5.2.1). Engraved label is a manual check on the render, not an automated test.
Gate: The Designer, quality and pride test ("would a printer operator produce a functional part?").

**Detail 8. Final assembly and independent re-measure.**
Work: re-run all CAD tests on production geometry; one independent re-measure script that imports only the exported STEP and STL files (no import of build or test code) and recomputes per-collet volume and bore diameter, the interference matrix, and bed fit, then compares to the result JSON; negative controls (probes away from the feature must still hit; a deliberately wrong expected value must fire). A SHA-1 manifest of text sources is written (Section 10 backup item); the draft's before/after hash guard for every write is a change-order requirement, not a new work-order one, and is cut here. The delivered FCStd opens with every deliverable object visible and named, count computed from object counts (test E3).
Outputs: `output/jig_assembly.FCStd`, `.step`, `output/stl/*.stl` for every printable part, `output/remeasure_results.json`, renders (PNG), `ASSEMBLY.md` complete, BOM final.
Gate: Software Engineer code review slot (tests meaningful, no ceremony); Topologist final topology gate; Systems Engineer interface review (base to collet to holder to nut to frame to future upper assembly).

**Detail 10. Joint scoping for the upper assembly.**
Objective: define the drill-holding upper assembly with the human after base review.
Agenda drawn from the extraction: guide/anchor for the 152.4 mm OD drill; WOB path up to 1000 N; torque reaction (value unknown); descent method and rate; instrumentation access (load cell and Hall sensor cabling at the back cap); whether a spindle drive is in jig scope (if yes, spawn The Motor Designer); iris closure confirmation; end stop above the wing nut.
Outputs: `research/quinn/cr_scratch/step10_scoping_notes.md`, a new work order `workorder_upper_assembly.md`, and an appended gameplan section with Steps 10.1 and up. Decision recorded: does the report cover the upper assembly or defer it. The upper assembly gets its own test suite before its geometry (same rule as Step 1).

**Detail 11. Report test suite (Prompt 1).**
Inputs: workorder.md, this gameplan's Document Structure (thesis and limitations table), extraction file, Step 8 result JSON (names of the values, not the values: tests say "matches results JSON field X").
Size: about 130 tests, set per A.10 item 7. A.10 calls a multi-section technical review a 150-to-200-test document; this report is 8 to 12 pages with seven sections and three appendices, about 12 tests per page, so the target sits below the band on purpose. The Manager ratifies at Step 11 open; if the human widens the report to the upper assembly, re-size to 150 or more. Split:

| Scope | Group | Count | Mode |
|---|---|---|---|
| Whole document | Thesis and lead-first (page 1 alone states design, verification result, deferrals) | 5 | manual |
| Whole document | Audience comprehension (cold cognizant outsider) | 8 | manual, fresh-context reader |
| Whole document | Communication architecture (abbreviations, figures, callouts, captions) | 10 | 6 automated, 4 manual |
| Whole document | Consistency and echo sites against the registry | 8 | automated |
| Whole document | Prose-quality detectors (AI tells, filler) | 5 | automated |
| Whole document | Format and build (8 to 12 pages, DOCX plus PDF, figures embedded) | 5 | automated |
| Whole document | Scope honesty (no jig iris actuator, no flight-representativeness, no built upper assembly) | 4 | manual |
| Section | 1 Summary and scope | 10 | mixed |
| Section | 2 Requirements and interfaces (about 9 are fact tests) | 14 | mixed |
| Section | 3 Concept | 9 | manual |
| Section | 4 Collet family | 12 | mixed |
| Section | 5 Printability and tolerances | 10 | mixed |
| Section | 6 Verification | 14 | mixed |
| Section | 7 Status and open items | 8 | manual |
| Section | Appendix A source notes | 4 | manual |
| Section | Appendix B BOM and stock | 3 | automated |
| Section | Appendix C drawings | 1 | manual |
| **Total** | | **130** | |

Test record format (Prompt 1): ID, scope, what is tested, pass/fail criterion, evidence required, automated or manual, severity, and for any test touching a fact: the primary source (file and line) and verification status (see Source Verification Register).
Comprehension and communication-architecture tests (named, with criteria):
- WD-C1 Cold read. A fresh-context reader gets only the PDF text and answers 8 fixed questions in the suite (what the jig holds; how a core is clamped; what the wing nut does; what the iris actuation source is; what was verified and how; what is not verified; what is deferred; what the human does next). Pass: at least 7 of 8 correct against the answer key. Zero control: the same reader given an unrelated document scores 0 of 8 on the same questions. Known-bad control: the report with Section 6 deleted must fail the "what was verified" question.
- WD-C2 Page 1 alone answers the first three questions.
- WD-A1 Abbreviations. Script lists every all-caps token and defined short form (SBIR, WOB, BOM, STEP, STL, PETG, FDM, CSM, 30-6060, and so on). Pass: each is expanded at first use in its section, or sits in a short allowed list (e.g. mm, N, PDF). Known-bad control: a planted undefined token fires. Zero control: a text with all tokens defined reads zero.
- WD-A2 Figures. A figure manifest maps each figure to (a) the body sentence making the claim it shows, (b) the script and data that regenerate it, (c) its caption. Pass: every figure has all three; the caption matches the plotted or rendered quantities; every labelled value traces to a results JSON field or a sourced number (no invented dimension). Known-bad control: a figure with no body claim fires.
- WD-A3 No orphan callouts or hero elements; each is referenced in the body.
- WD-A4 Terminology: one term per part (holder, collet, boss, wing nut) used consistently; synonyms listed and counted by grep.
Fact tests: every numeric claim has a test naming its primary source (Section 2 and Appendix A carry most). Source status is recorded per the register. Controls (Principle 9): the AI-tell grep and the echo-site audit each run on a clean text (reads zero) and on a text with planted defects (fires) before their output counts.
Output: `report_test_suite.md`. Software Engineer authors and reviews; Fact-Checker verifies source attributions. Gate: no test with status UNVERIFIED survives unresolved into the contract (A.10 item 2); the suite lists each as UNVERIFIED with the unblock owner, and the orchestrator resolves or the test is rewritten to assert a stated assumption instead of a sourced fact.

**Detail 12. Report topic-sentence outline (Prompt 2) and validation before any drafting.**
Inputs: the signed Step 11 suite, Document Structure, structure.md.
Work: the Engineer drafts the paragraph-level outline as full topic sentences (not headings). Each outline entry carries an ID (P2.3) and a `covers:` list of test IDs.
Validation (the A.4 precondition, run before Step 13 opens), recorded in `report_outline_validation.md`:
1. Coverage matrix, scripted: every section-level test is covered by at least one paragraph; every whole-document test is covered or marked "post-draft only" (consistency, AI-tell, page count, build, format); every paragraph covers at least one test or is marked connective with a reason. Orphans in either direction fail.
2. Fact paragraphs: any topic sentence containing a number cites its fact test ID and carries the same source status as that test.
3. Topic-sentence read-through: the topic sentences alone, concatenated in order, are given to a fresh-context reader with the 8 cold-read questions. Pass: at least 7 of 8 answered. This catches comprehension failures before prose exists.
4. Architecture: the outline names where each abbreviation is first introduced and the body claim for each planned figure.
5. Limitations table placements (Document Structure) each appear at their stated section.
Controls: zero control (the full matrix reads no orphans); known-bad control (delete one paragraph, a test must show as orphaned; plant a paragraph with no test, it must show as orphan).
Output: `report_outline.md`, `report_outline_validation.md`. Gate: Software Engineer signs the validation; the Manager verifies both files exist before opening Step 13 (A.4). Failure returns to the Engineer; no drafting begins.

**Detail 13 to 17. Report path (remaining document steps).**
- 13: Engineer writes reporting copy from the Step 8 evidence, loading supplements/writing-guides/reporting-copy.md only (no prose style reference). Output: `report_reporting_copy.md`.
- 14: Writer composes from reporting copy plus Wave 1 outputs (loads structure.md, style.md; style-reference.md on demand). Output: `report_draft_writer.md`.
- 15: Editor removes AI tells and tightens (loads signs_of_ai_writing.md). Output: `report_draft_editor.md`. Default order Writer then Editor since the input is raw reporting copy.
- 16: Wave 2: Designer (communication, echo-site audit, cold-read tests), Fact-Checker (every cutter dimension and requirement vs SBIR and model sources, source gate), Systems Engineer (interfaces, load path, limits). Outputs: `research/quinn/cr_scratch/step16_designer.md`, `step16_factcheck.md`, `step16_systems.md`.
- 17: revise; build DOCX (claude-docx-bundle house style) and PDF; run the suite; echo audit against the registry; Software Engineer final suite run, including re-running the cold read on the final PDF. Outputs: `CoreCutterTestJig_Report.docx`, `.pdf`.

---

## CAD Test Specification

Every test is automated unless marked manual. Parametrized over the four collets {90, 95, 100, 105} where marked (d). Thresholds named `params.*` come from `params.yaml`; values marked PROPOSED are the Software Engineer's placeholders for the Engineer and Loftsman to confirm or replace in Step 2. "Control" means the zero control and known-bad control required by Principle 9 for gates and detectors. About 30 test functions, about 80 parametrized cases. That is the size of this jig; the draft's open-ended "tests include" list is replaced by this table.

**Group P: params, BOM, contract**

| ID | Test | Pass criterion | Evidence |
|---|---|---|---|
| P1 | `validate_params()` | Accepts the seed; rejects known-bad: collet d = 89 and d = 106, clearance negative, nut OD above bed minus margin | pytest result |
| P2 | Source keys | Every externally sourced number in params has `source:` and `status:`; count of UNVERIFIED reported | Count printed; list matches the register |
| P3 | Stock allocation | For each stock length, summed cut lengths of frame members from that length <= on-hand quantity x length; extra cuts appear only in the extra-cut table; the 1540 mm lengths unused unless the human directed otherwise | `bom_stock_allocation.md` parsed |
| P4 | Hardware rules | T-nut entries are M6 spring-ball roll-in only; every bracket entry is a SKU or the full-size 30-series class and contains no "mini" | grep on BOM files; control: planted "mini bracket" fires |
| P5 | Frame profile | Each frame member bbox 60 x 60 mm cross-section within 0.05 mm; length equals cut list. Slot detail is not tested (catalog fidelity is not worth a test for stock the human already owns) | result JSON |

**Group C: collet family (d)**

| ID | Test | Pass criterion |
|---|---|---|
| C1 | Validity | Single solid; isValid; isClosed |
| C2 | Volume | Whole-part volume within 0.95 to 1.05 of the analytic volume from params. Each cut (bore, slit, thread or key, as present) removes volume within 3 % of its analytic expectation and 0 < removed <= tool volume (7.1 expected-delta) |
| C3 | Bore diameter | Probe through the bore along three azimuths 120 degrees apart; mean bore diameter equals `params.collet.bore_free(d)` within 0.02 mm. The relation between bore_free and d (the draft says "bore = d with a net interference band") is one formula, stated by the Loftsman in Step 2 |
| C4 | Family invariants | Taper angle, large OD, small OD and seat height are identical across the four collets within 0.02 mm, so one holder seats every collet |
| C5 | Slit | Slit count equals params; width within 0.05 mm; a ray across the slit meets void along the full wall height |
| C6 | Minimum wall | Minimum wall over the collet at least `params.print.min_wall` (PROPOSED 1.2 mm, 3 perimeters at 0.4 mm). Tightest case expected at d = 105 if the outer taper is fixed; test runs all four |
| C7 | Topology | Faces per edge all 2 except documented cylinder seams; no leftover planar face on the slit plane; minimum face area and edge length recorded |
| C8 | Family coverage (one test, whole family) | For every core diameter from 90 to 105 mm in 1 mm steps, widened by the core tolerance `params.core.tol` (default +/-1 mm, UNVERIFIED), at least one collet's accept range contains it. Accept range per collet is the Engineer's stated clamp range (+/- mm about d). Known-bad control: remove the 100 mm collet from the family, the test must fire. See Flag E4: with 5 mm spacing the range must be at least +/-2.5 mm |

**Group T: thread, engagement, clamp range**

| ID | Test | Pass criterion |
|---|---|---|
| T1 | Chirality | Boss and nut threads right-handed (helix sign probe). Known-bad control: a mirrored nut fires |
| T2 | Thread dimensions | Major, minor, pitch, lead match params within 0.05 mm (default Tr 60 x 8, pending Step 2) |
| T3 | Print clearance | Radial clearance per side between boss and nut flanks equals `params.print.thread_clearance` within 0.05 mm and is at least `params.print.thread_clearance_min` (value set by the Loftsman from printer data; printer unconfirmed, so UNVERIFIED until the Step 9 coupon) |
| T4 | Thread engagement | In the clamp pose with the 90 mm collet and again with the 105 mm collet: engaged axial length of nut thread on boss thread at least `params.thread.min_engage` (PROPOSED 3 pitches = 24 mm for Tr 60 x 8). Zero control: nut at the top of the boss with no overlap reads 0 |
| T5 | Wing nut clamp range at 90 and 105 mm | For each of d = 90 and d = 105 build two poses. Release pose: nut backed off, collet free bore at least d + `params.insert_clearance` (PROPOSED 1.0 mm), a core of diameter d + `params.core.tol` slides in with zero interference. Clamp pose: nut hand-tight on the holder, the slit still has width above `params.collet.min_slit_clamped` (PROPOSED 0.5 mm; the slit has not bottomed out, so the collet can still close on a core at d - `params.core.tol`), thread engagement per T4, and the nut has at least 1 pitch of thread travel left before bottoming on the base. Pass: all four poses pass. The 95 and 100 mm collets are not run because the taper is identical across the family (C4), so stack height is monotonic in d and the extremes bound the middle. If C4 is ever relaxed, run all four |
| T6 | Nut OD and bed | Wing nut bounding box fits the printer bed minus 5 mm in any orientation, or the split design's parts do each (bed 256 mm, UNVERIFIED printer) |

**Group F: fit and function**

| ID | Test | Pass criterion |
|---|---|---|
| F1 (d) | Collet seat fit | Minimum radial gap between the collet's tapered seat surface and its mating seat (boss or holder cone, whichever Step 2 fixes; the workorder says collet in boss, the draft's stack says collet in holder, see Flag E2) is within `params.print.seat_clearance` +/- 0.05 mm at the release pose. At the clamp pose the seat surfaces are in contact: Boolean common volume < 0.01 mm3 with a contact-area probe above `params.seat.min_contact_area` |
| F2 (d) | Core in collet | A core cylinder of nominal d slides into the release-pose bore with common volume < 0.01 mm3 and its base lands on the core stop (axial gap to stop 0 +/- 0.05 mm) |
| F3 | Collet and core sweep | For each core diameter 90 to 95 to 100 to 105 (the four nominals) and the tolerance ends, the matching collet passes F2 in release pose; a mismatched pairing (e.g. 105 core in 90 collet) is rejected, common volume above 0.01 mm3 (this is the known-bad control, it must fire) |
| F4 | Exposed core | Core top above holder top by at least `params.core.min_exposed` = standoff + margin, where standoff is 106.369 mm from the 7 in model (applicability to the 6 in drill UNVERIFIED) and margin is a params value |
| F5 | Feature presence | Each Step 4 feature (boss thread, seat taper, slit, anti-rotation key or flat, wing nut wings and thread, T-nut and bracket mounting provisions, core stop, drain) is present in its part's result JSON with nonzero feature volume. On the empty baseline every one fails (red-first discriminator) |

**Group A: assembly**

| ID | Test | Pass criterion |
|---|---|---|
| A1 | Interference matrix | Parts: base, holder, wing nut, collet, core stand-in (cylinder of d), frame members, brackets, cutter keep-out (A2). One matrix per collet configuration (4 matrices). Every neighbor pair: Boolean common volume < 0.01 mm3. Pairs in intended contact (thread flanks, seat taper, core in bore, base on frame) are listed in `ASSEMBLY.md` and must also read < 0.01 mm3 (touching is not overlapping). Report: part A, part B, mm3, pass or fail. One fail blocks. Controls: zero control (two parts 100 mm apart reads 0); known-bad (a copy of the holder offset 1 mm into the base fires) |
| A2 | Cutter envelope | A tube solid, 152.4 mm OD and 146.05 mm ID, swept the full descent stroke (`params.stroke`) along the core axis, is Boolean-intersected with every fixture. Branch 1: no fixture inside the tube wall volume. Branch 2: any fixture wider than the 146.05 mm bore is the declared hard stop, its top face must sit below the cutter's lowest point by `params.stop_margin`, and a flag `params.nut_is_stop` states which branch applies. The Engineer chooses the branch. Control: a ring placed in the tube path fires |
| A3 | Placement and signs | (a) All link placements identity or equal to the expected placement in `ASSEMBLY.md` within 0.01 mm and 0.01 degree. (b) Sign checks: boss axis points +Z; z-order base top < holder seat < nut mid-height < core top; boss, holder, collet, nut and core axes coincide within 0.05 mm in x and y; frame members sit under the base plate with z-gap 0 +/- 0.05 mm; each bracket's outward normal points away from the frame centroid. (c) Control: a part flipped 180 degrees about x, and a part offset 5 mm in y, each fires |
| A4 | Product tree | Component count and names equal the expected list; the expected visible object count is computed from object counts, not read from the saved file |
| A5 | Visual (manual) | Four-view PNG set judged against a written rubric by the Designer (does it look like the design: stack order, nut on top, wings present, collet visible); evidence: the rubric sheet with four ticks |

**Group E: export validity**

| ID | Test | Pass criterion |
|---|---|---|
| E1 | STEP | For each printable part and the assembly: file exists with mtime after the run started; size > 0; re-import gives the expected solid count; summed volume within 0.5 % of the FCStd; unit is mm; product tree names equal the part names |
| E2 | STL (each printable part) | Watertight (every edge shared by exactly two triangles); no degenerate triangle; signed volume positive and within 1 % of the FCStd volume; bounding box within bed minus 5 mm; units mm (largest dimension sanity). Controls: zero control (a unit cube STL passes); known-bad (an STL with one triangle removed fires watertight) |
| E3 | FCStd opens | Reopen the saved FCStd; visible deliverable object count equals the count computed from the object counts; every deliverable object named |

**Group W and X: workflow and independent re-measure**

| ID | Test | Pass criterion |
|---|---|---|
| W1 | Rebuild | Running the part scripts twice yields volumes equal within 1e-6 relative (also the check that nothing depends on stale state) |
| W2 | Backup manifest | SHA-1 manifest of text sources exists and matches current files |
| X1 | Independent re-measure | Step 8 script, sharing no code with build or tests, reads the exported STEP and STL only; recomputes per-collet volume and bore diameter, the interference matrix and bed fit; each agrees with the build-side result JSON within the tolerance of C2, C3, A1, E2. Negative controls: probes away from the feature still return a hit; a deliberately wrong expected value fires |

**Cut from the draft as ceremony for a one-off jig:** color-assignment tests; diffability test; generic "reproducibility from a commit" (W1 covers it); per-part separate geometry-math test file; overhang-angle script; wing nut moment-arm check; turntable MP4; before-and-after source hashing on every write (not required on a work order); slot-level 30-6060 fidelity; empty report test stubs; separate `step6_printability.md`; two-document Step 2 output.

---

## Source Verification Register

Rule (A.10 item 2, tdd_method principle 7): a test that cites the SBIR plan, a Mines document or the rigged model is marked UNVERIFIED unless the extraction file traces it to a file and line. TRACED means the extraction file gives the location; it does not mean anyone has re-read the primary file. The Software Engineer did not open the SBIR folder, the Mines zip or the gpr model in this revision and cannot assert any of them. The Fact-Checker verifies every TRACED row against the primary file on disk at the Step 1 gate (CAD tests) and the Step 11 gate (report tests), and records the date and result in the table. The orchestrator resolves any row that stays UNVERIFIED; the human resolves rows only the human or Mines can answer.

| Claim used by a test | Tests | Status | Extraction trace | Who verifies / unblocks |
|---|---|---|---|---|
| Core nominal 100 mm | P2, C8, WD, S2 | TRACED | INSITU2_text.md lines 406-407 (C9) | Fact-Checker re-reads the lines |
| Core range 90 to 105 mm, 6.00/5.75 in tubing | P1, C-group, A2 | CONTRACT | workorder.md (the work order is the primary source) | none needed; arithmetic 152.40/146.05 DERIVED, Fact-Checker recomputes |
| Iris closed by drill drivetrain, no jig actuator | S2, scope-honesty | TRACED | INSITU2_text.md lines 157-166 (C2) | Fact-Checker |
| Iris standoff 106.369 mm, 4 leaves | F4, S2, App A | TRACED but for the 7 in model only | gpr double_dong_params.py `CORE_IRIS_STANDOFF_MM`, `IRIS_LEAVES` (extraction section 2) | Fact-Checker verifies the number in the file; applicability to the 6 in drill is UNVERIFIED until the 6 in iris is measured (extraction section 7, item 1 and 5); Engineer or human supplies |
| WOB 100 to 1000 N | S2, params loads | TRACED | INSITU3_text.md 267-270, 424-430; borebot_operating_envelope.md line 58 (C4) | Fact-Checker |
| Spin 1 to 60 rpm | S2 | TRACED | summary_yokeless_motor.md 143-200 (C3) | Fact-Checker |
| Core length 500 mm | params, S2 | TRACED as DECLARED by Quinn, not a Mines value | double_dong_params.py `CORE_LENGTH_MM` (C8) | UNVERIFIED as a Mines requirement; human asks Mines |
| Core mass 9.4 kg at 2400 kg/m3 | S2 | DERIVED upper bound, density UNVERIFIED | extraction C7 | Mines property data (not in hand) |
| Core diameter tolerance +/-1 mm | C8, T5, F-group | UNVERIFIED | Extraction states Mines gave none | Human asks Mines |
| Torque 20 N m (jig) and 50 N m (iris) | S2, any loads test | UNVERIFIED | Extraction C5: no source states a number | Phase I measurement; until then the report states it as an assumption, not a fact |
| Core count 12+12 vs 40/15/30 | any report test mentioning Mines core count | UNVERIFIED (sources disagree) | extraction C11 | Human, or cut the sentence |
| "Mines specifies/requires/delivers" anything (diameter beyond 100 mm, length, wrap, tolerance) | any | UNVERIFIED | Extraction section 6: the Mines zip carries budget and commitment text only, no core dimensions | Human; the tests assert the SBIR proposal text, not the Mines documents |
| Mines Dreyer low-density concrete | S2 | TRACED | csm_sow.md 24, 56 (section 6) | Fact-Checker |
| Penetration pass 5 mm/min at WOB 100 N | S7 only | TRACED | INSITU3_text.md 267-268 | Fact-Checker |
| 30-6060 is 60 x 60 mm, 30 mm pitch, M6 spring-ball T-nut | P3 to P5, App B | DECLARED by human; catalog check pending | research/quinn/cr_scratch/step0_human_stock_80-20.md; QMRD3 BOM text | Engineer pulls catalog at Step 1; Fact-Checker confirms; stock quantities are the human's statement |
| Stock lengths and quantities | P3 | DECLARED by human | step0_human_stock_80-20.md | Human at Step 9 |
| Printer bed 256 mm, PETG/PLA, 0.4 mm nozzle | T3, T6, E2, C6 | UNVERIFIED (no printer named) | Manager default only | Human names printer at Step 1 or Step 9 |
| Rigged model identity (7 in, not 6 in) | App A | TRACED MEASURED | double_dong_params.py line 354 (C10) | Fact-Checker |
| Which 2026 STEP is the 6 in drill; 6 in iris open aperture | any | UNVERIFIED | extraction section 7 | Human or Engineer measures |

Any test that is UNVERIFIED must either be rewritten as "stated assumption, documented as such" (the test then checks the assumption is present and labelled, not that it is true) or be dropped from the contract. Report text may not state an UNVERIFIED value as fact.

---

## Context Recipes

| Step | Agent | Files / Excerpts |
|------|-------|-----------------|
| 0 | The Manager | workorder.md, this gameplan, method/operational_guide.md (A.4, A.6, A.12), accumulator (none) |
| 0 | The Engineer | workorder.md, templates/gameplan.md, extraction file, stock file, supplements/llm_plm_cad.md, method/tdd_method.md |
| 0 | The Software Engineer | workorder.md, Engineer's draft, extraction file, method/tdd_method.md, operational_guide A.4 and A.10, llm_plm_cad.md sections 7 and 10, stock file |
| 0 | Reviewers (Systems Eng, Loftsman, Topologist, Designer) | workorder.md, revised draft, extraction file |
| 1 | The Engineer | workorder.md, gameplan, llm_plm_cad.md, freecad_api_reference.md, extraction file, stock file |
| 1 | The Software Engineer | gameplan (CAD Test Specification, Source Verification Register), tests/, params.yaml, tdd_method.md, llm_plm_cad.md section 7 |
| 1 | The Fact-Checker | Source Verification Register, tests asserting numbers, extraction file, context/literature/ summaries, source documents on disk |
| 2 | The Loftsman | params.yaml, extraction sections 2 and 3, freecad_api_reference.md (thread/helix), test_thread_clamp.py, test_collet_family.py |
| 2 | The Topologist | params.yaml, llm_plm_cad.md 7.1, 11, Loftsman output |
| 3 | The Engineer | params.yaml, common.py, step 2 output, tests/test_collet_family.py |
| 3 | The Software Engineer | collet_family.py, tests, params.yaml (code review recipe) |
| 4 | The Engineer | params.yaml, common.py, collet_family.py, step 2 output, ASSEMBLY.md |
| 4 | The Loftsman, Topologist | part scripts, FCStds results JSON, step 2 output |
| 4 | The Designer | params.yaml, renders, step 4 findings (no scripts) |
| 5 | The Engineer, Software Engineer | assemble.py, tests/test_assembly.py, test_thread_clamp.py, ASSEMBLY.md, interference report |
| 5 | The Systems Engineer | ASSEMBLY.md, interference report, extraction sections 3 to 5 |
| 6 | The Engineer, Loftsman | part scripts, step 2 thread clearance output, printer constraints (Design Notes) |
| 7 | The Engineer, Loftsman, Topologist | step 4 findings, step 5 and 6 reports, part scripts |
| 7 | The Designer | step 4 findings, renders of production parts |
| 8 | The Engineer | all of the above, SHA-1 manifest |
| 8 | The Software Engineer | build_parts/, tests/, results JSON, remeasure script |
| 8 | The Topologist, The Systems Engineer | assembly FCStd/STEP, ASSEMBLY.md, interference report |
| 10 | The Manager, Systems Engineer | step 8 outputs, extraction file, workorder.md |
| 11 | The Software Engineer | workorder.md, gameplan Document Structure, extraction file, tdd_method.md, operational_guide A.10, Source Verification Register |
| 11 | The Fact-Checker | test suite, source documents, context/literature/ |
| 12 | The Software Engineer, Engineer | test suite, gameplan Document Structure, structure.md |
| 13 | The Engineer | reporting-copy.md (full), Step 5 to 8 results with sources, report_outline.md, report_outline_validation.md |
| 14 | The Writer | structure.md, style.md (full), style-reference.md (on demand), reporting copy, outline |
| 15 | The Editor | signs_of_ai_writing.md (full), Writer draft, suite AI-writing criteria, origin info |
| 16 | The Designer | diff since Step 15, full report, echo site registry, cold-read tests |
| 16 | The Fact-Checker | full report plaintext, source documents, context/literature/, echo registry, Source Verification Register |
| 16 | The Systems Engineer | report, ASSEMBLY.md, step 8 outputs |
| 17 | The Engineer | edited draft, review outputs, claude-docx-bundle |
| 17 | The Software Engineer | final PDF text, report_test_suite.md, checker scripts |
| 18 | The Manager | gameplan, all step outputs |

---

## Echo Site Registry

Each row: value, authoritative source, derived locations. Bold values on use. First-use rule: introduce with its context the first time in each section.

| Value | Authoritative source | Derived locations |
|---|---|---|
| Core nominal diameter **100 mm** | INSITU2_text.md line 406-407; params.yaml `core.nominal_d` | report 1, 2, 4; collet 100 file name; tests |
| Collet diameters **90, 95, 100, 105 mm** | params.yaml `collets.diameters` | report 4; collet filenames; interference matrices; BOM |
| Core accepted range **90 to 105 mm** | workorder.md | report 1, 4; collet generator bounds; test C8 |
| Core tolerance **+/-1 mm** (UNVERIFIED) | params.yaml `core.tol` | tests C8, T5, F3; report 2 as stated assumption |
| Tubing **6.00 in OD / 5.75 in ID (152.40 / 146.05 mm)**, wall 1/8 in | workorder.md; params.yaml `drill.*` | report 2, 3, 6; test A2; cutter keep-out solid |
| Radial gap 100 mm core **23.025 mm** (90: 28.025; 105: 20.525) | derived from the two rows above, params.yaml | report 2; clearance test |
| Iris leaf count **4** and standoff **106.369 mm** (7 in model) | gpr double_dong_params.py `IRIS_LEAVES`, `CORE_IRIS_STANDOFF_MM` | report Appendix A; test F4 |
| Boss thread spec **Tr 60 x 8** (default, pending Step 2) | params.yaml `boss.thread` | boss, wing nut, base scripts; tests T1 to T5; report 4, 5; thread coupon |
| Min thread engagement (PROPOSED **3 pitches**) | params.yaml `thread.min_engage` | test T4; report 4 |
| Wing nut diameter (**TBD in Step 2**, bounded by bed 256 mm) | params.yaml `wingnut.od` | report 3; tests T6, A2; cutter stop height |
| Profile series **30-6060** (60 x 60 mm, M6 roll-in T-nut) | research/quinn/cr_scratch/step0_human_stock_80-20.md | frame scripts; BOM; tests P3 to P5; report 3, Appendix B |
| Printer bed **256 x 256 x 256 mm** (default, UNVERIFIED) | params.yaml `printer.bed` | tests T6, E2; report 5 |
| Design load rating (axial **1000 N** WOB upper bound; torque placeholder 20 N m, unsourced) | extraction C4, C5; params.yaml `loads.*` | frame sizing; report 2 |
| Spin **1 to 60 rpm** | context/summary_yokeless_motor.md | report 2; scoping step |
| Stock lengths and allocation | step0_human_stock_80-20.md; bom_stock_allocation.md | BOM, test P3, report Appendix B |
| Report test count **about 130** | this gameplan, Detail 11 | Step 11 suite; Step 17 final run |

Authority rule (A.16): geometry values live in params.yaml until an FCStd exists, then the FCStd; report values must match the authority, not each other. A within-file contradiction is a nonconformance and blocks step close.

---

## Progress Log

| Step | Date | Notes |
|------|------|-------|
| 0 | 2026-11-08 | Opened. Work order locked as workorder.md. Engineer extraction and draft written (cr_scratch). Human stock input (30-6060) and T-nut/bracket constraints folded in. Software Engineer revision: CAD Test Specification, Source Verification Register, report suite and outline validation steps added; ceremony cut. |

---

## Design Notes

**Source findings that change the design (extraction file):**
- The iris is closed by the drill's own drivetrain (braked planetary sun gear). The jig supplies no iris actuator. Jig duties: hold the core coaxial, react WOB and torque, guard the cutter stroke.
- Bore check: 146.05 mm vs 90 to 105 mm cores leaves 28.025 to 20.525 mm radial gap per side. Pass.
- The iris pinches the core 106.369 mm behind the cutting face (7 in model). The exposed core above the holder must exceed that, so the holder must be low and the cutter's lowest point must stop above the holder top. Re-derive for the 6 in drill when its iris is measured.
- Fixtures inside the descent path must clear 146.05 mm bore minus margin; a wing nut wider than 146.05 mm is a hard cutter stop and must sit below the cutting face's lowest position. Stop height is a parameter.
- The rigged model is the 7 in generation, not the 6 in. The 2026 STEP's size is not confirmed.

**Stack concept (tentative, Step 2 confirms):** Base plate with threaded boss rising (external trapezoidal thread). Core holder is a sleeve with an internal taper that seats on the boss. A slit collet with matching external taper and a bore equal to the core diameter sits inside the holder. The wing nut threads onto the boss and presses the holder axially, which closes the collet on the core. The core base seats on a stop inside the collet. Collet inside diameter chosen per diameter, family generated from d. The Loftsman and Topologist may reverse the stack order if the half-space analysis requires. Tests F1, T5 and A3 read the stack order from `ASSEMBLY.md`, so a reversal changes data, not tests.

**80/20 hardware (human input, DECLARED):**
- Profile: 80/20 30-6060, 60 x 60 mm, 30 mm slot pitch. No smaller profile. Fasteners M6.
- T-nuts: M6 spring-ball roll-in only, for the 30-6060 slot. No other T-nut type anywhere in the design or BOM.
- Brackets: ordered catalog brackets are acceptable; printed or fabricated brackets may be designed. Any ordered bracket must be full size for the 30-series profile, never a "mini" bracket. BOM names the bracket SKU or the full-size class. SKUs are not verified in Step 0; Step 1 pulls them from the 80/20 catalog (open question).
- Stock on hand, mm x quantity: 1540 x 4, 980 x 4, 952 x 1, 728 x 2, 644 x 2, 488 x 2, 468 x 2 (15,688 mm total). Believed uncut; shared with other projects. Design from stock first. Extra cuts of 30-6060 are allowed (about $2.20 per cut at the QMRD3 order, DECLARED) and go in a separate BOM table with quantities.
- Starting allocation to test in Step 1, to be confirmed: base frame from the shorter stock (644 x 2, 468 x 2, 488 x 2 for perimeter and cross members); the 1540 mm lengths are reserved for columns in the upper-assembly work (Step 10) and are not consumed in Steps 1 to 9 except as the human directs. `bom_stock_allocation.md` records which stock lengths the jig consumes, for the other projects. Test P3 enforces this.

**Printing:** default 256 mm class bed, PETG for jig parts, PLA for fit coupons, 0.4 mm nozzle; coarse Tr thread because fine printed threads fail. Wing nut sized to the bed or split.

**Process rules carried in:** per-part scripts, one FCStd each (A.14); FCStd is authority once built (2.1); Boolean expected-delta and topology gate after each cut (7.1); any build over 30 s runs in the background and the PID, log path and expected finish are logged here (A.3.4); under FreeCAD 1.1.4 success is a sentinel line plus a fresh artifact, not exit code (A.15).

**Software Engineer review slots:** Step 1 (suite, signs it), Step 3 (generator code), Step 5 (assembly tests), Step 8 (code and test review), Steps 11 and 12 (report suite, outline validation).
**Loftsman and Topologist cross-review slots (A.4 geometry rule):** Step 2 (before any build: thread, taper, slit, seat), Step 4 (exploratory geometry), Step 7 (production geometry), Step 8 (topology gate).

---

## Open Questions

Resolved by the human: item 1, profile series = 30-6060, M6 spring-ball roll-in T-nuts, full-size brackets only.

Proposed defaults (Manager section 4, adjusted by the sources):
1. Bracket SKUs: full-size 30-series class; Step 1 selects SKUs from the 80/20 catalog. Confirm on-hand bracket and M6 screw inventory.
2. Printer bed, material, nozzle: 256 mm class, PETG/PLA, 0.4 mm. Need actual printer (feeds UNVERIFIED rows T3, T6, E2).
3. Collet increments: 90, 95, 100, 105 mm; add a plain 100 mm master only if the human wants one. Mines core tolerance: default +/-1 mm. Mines has not stated one (UNVERIFIED; drives test C8).
4. Core length and mass: default 100 mm x 150 to 500 mm (500 mm used by Quinn's animation), mass up to 10 kg at an assumed 2400 kg/m3 (DERIVED, unverified). Ask Mines for length, density and delivery state (wet, wrapped, sleeved).
5. Loads: sources give WOB 100 to 1000 N, so the default axial design load rises to 1000 N (was 500 N). Torque: no source; keep 20 N m as a placeholder for the jig and mark it UNVERIFIED until Phase I measures closure torque. Safety factor 3 on printed parts.
6. Spin and descent: 1 to 60 rpm (was 60 to 300). Descent rate: no source for the jig; Phase I pass threshold is 5 mm/min at WOB 100 N or more. Hand crank or leadscrew deferred to Step 10.
7. Debris: indoor, debris tray in the base.
8. Report: 8 to 12 pages, DOCX plus PDF in house style; about 130 tests (ratify at Step 11 open).
9. CAD chain: FreeCAD 1.1 headless per llm_plm_cad; confirm install and whether a 6 in drill STEP exists to import.
10. Boss thread: Tr 60 x 8 default; Step 2 may change it.
11. Which of the two 2026-09-11 STEP files is the 6 in drill, and the iris open aperture in that design (extraction section 7).
12. Does the report cover the upper assembly or defer it (decided at Step 10).
13. Fasteners for non-80/20 joints: stainless M6 (was M8 under 1515 assumption; 30-6060 uses M6).

---

## Flags to the Engineer (engineering content not rewritten)

- E1. Thread engagement minimum (PROPOSED 3 pitches = 24 mm) and print clearance are placeholders. Loftsman to set from printer data; test reads params.
- E2. The workorder says the boss "seats the collet". The draft's stack seats the collet in the holder and the holder on the boss. Test F1 and the "collet-in-boss fit" requirement need one answer; fix in Step 2.
- E3. "Collet bore = core diameter with a net interference band" is ambiguous (a bore smaller than the core cannot accept it). Test C3 needs one formula for bore_free(d) and one for the clamped bore.
- E4. Coverage: with collets 5 mm apart and a core tolerance of +/-1 mm, each collet must grip about +/-2.5 mm about its nominal or the 92.5, 97.5 and 102.5 mm cores fall between collets. A slit collet that closes 5 mm in diameter is a large closure (circumference change about 15.7 mm at one slit). If the clamp range is smaller, the family needs 2.5 mm spacing (7 collets) or the workorder's "separate collet per diameter" reading is limited to nominal sizes. Test C8 will fire either way; decide in Step 2.
- E5. Wing nut OD versus the 146.05 mm bore: choose the stop or pass-over branch for test A2 (`params.nut_is_stop`).
- E6. Core length 500 mm, mass up to ~10 kg standing upright in a printed collet: no lateral support or tip-over check exists and no source gives the load. A tall core is a lateral-stability question for Step 2 or Step 10. I did not add a test without a source or a model.
- E7. Slit strain at clamp needs a PETG allowable strain; no source. Mark the allowable UNVERIFIED and let the Step 9 print be the check.
- E8. The 106.369 mm iris standoff is the 7 in model. Test F4 passes against a number that may not apply to the 6 in design.

---

## Software Engineer changes

1. Replaced the draft's "tests include" list with a CAD Test Specification (groups P, C, T, F, A, E, W, X): named IDs, pass criteria, evidence, controls. Added per-collet volume and diameter, thread engagement, collet seat fit, interference matrix per collet, placement sign checks, wing nut clamp range at 90 and 105 mm, STEP/STL validity.
2. Added the Source Verification Register: every SBIR, Mines or rigged-model citation is TRACED to the extraction file or UNVERIFIED. Fact-Checker verifies at Steps 1, 11 and 16; the human resolves Mines and printer items. I did not open the primary sources; TRACED is not VERIFIED.
3. Report path: Step 11 suite sized at about 130 (below A.10's 150 to 200 band on purpose, needs Manager ratification), with the split by group and named comprehension and communication-architecture tests (cold read, abbreviations, figures regenerable from a body claim). Step 12 outline validated against the suite by a scripted coverage matrix and a topic-sentence read-through before any drafting, with controls; Step 13 does not open without the validation record. Fixed the Step 11/12 inconsistency in Document Structure.
4. Cut as ceremony: report test stubs, `test_jig.py` catch-all, `test_geometry_math.py`, turntable MP4, overhang script, wing nut moment-arm check, color and diffability tests, write-guard hashing, slot-level profile fidelity, separate printability report, two-file Step 2 output.
5. Added eight flags for the Engineer (E1 to E8), the most consequential being E2 (where the collet seats), E3 (bore formula) and E4 (the 5 mm collet spacing may not cover the 90 to 105 range).
