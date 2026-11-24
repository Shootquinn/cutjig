## 1. Step 4 scope

Step 4 produces the CAD test suite as code, labelled and red where the artifact is missing. Baseline B4 is the repository at Step 3 close: params.yaml (319 leaves), ASSEMBLY.md (45 pair rows, 6 feature rows), five solids in `parts_cache` (receiver, holder, nut, washer, foot ring d 90) with result JSON and `step3_cross_checks.json`, `tests/test_params_bom.py` (197 pass). No collet, no assembly or pose artifact, no STEP or STL export, no frame assembly, no rebuild record, no X1 script exist at B4.

Every label is relative to B4:
- Discriminator: fails at B4 because the artifact or feature does not exist. Becomes the build target.
- Invariant: passes at B4 and must stay green. Includes every control test (zero control, known-bad control; tdd_method principle 9), which tests the checker and passes at B4.

Rules the Software Engineer applies to all five modules:
1. Failure reason. A red test fails by assertion with a message that begins `MISSING:` (names the absent path) or `ABSENT FEATURE:` (names the feature). ImportError, collection error, KeyError, TypeError, skip and xfail are defects. One helper, `require(path)`, raises the `MISSING:` assertion.
2. Marker pair on every test: `discriminator` or `invariant`; and `green_at_N`, where N is the step that builds the measured artifact (4, 5, 6, 7, 8, 10, 12). Invariants carry `green_at_4`. Markers are registered in `conftest.py`.
3. Relations are data. A1a parametrizes over the Relations table (45 rows) and the Feature pairs table (6 rows) of ASSEMBLY.md, times poses R, K d+1, K-max, times `core.diameters`. A parser test (pair count 45, class counts R: C 8 / G 12 / F 25, K: C 10 / G 10 / F 25, every unlisted pair fails; control: a deleted row fires) is an invariant at B4.
4. Thresholds are read from `params.yaml` through `common.load_params()`. A literal that duplicates a params value is a defect; analytic constants (pi, 45 degrees, Euler counts) are allowed and listed.
5. Predicates read final shapes (Rule M). Pose-dependent predicates (A1a, A3, T4, T5, F6, WS states) read assembly artifacts built by the Step 7 assembler; they never read a placement the test computed from params, which would measure the parameter against itself. The Software Engineer writes the artifact contract (file names, JSON keys, pose names) in the suite header; Step 7 builds to it.
6. Geometry access. pytest runs in system Python 3.14 and cannot import FreeCAD. Probe scripts `tests/probes/*.py` run under `freecadcmd`, open FCStd read-only (no `doc.save`; a save creates .FCBak files), and write `results/probes/<name>.json`. Test modules read that JSON and fail with `MISSING:` when it is absent or older than its FCStd inputs. pytest never launches FreeCAD. One non-collected helper `tests/cad_helpers.py` (no `test_` prefix, no assertions about the design) holds `require`, the ASSEMBLY.md parser, the probe-JSON loader and the staleness check. There is no sixth test module.
7. Source tags. Every test that cites a Register row carries a comment `# SRC: <Register row, first words> | <STATUS> | <file lines>`. STATUS is VERIFIED, DECLARED, ASSUMED, DERIVED or CONTRACT, equal to the Register and to the params.yaml tag.
8. Number basis. Each threshold row in the inventory states its basis: centre or edge, per side or diametral, formula text (Design Notes 16).
9. Gate rules carried from Step 3 (Design Notes 17, 12):
   - `stop.g_stop` (25 mm) is a mechanical clearance between the cutter lowest point at the stop and the collar top. No safety, pinch, finger, crush, hand-entry or ISO 13854 language appears in any test, helper, docstring, doc or message. A1b (fastener head clear radius and sector for a 150 mm key) is tool access, named that way. The wing-turning access key is `wingnut.hand_clearance`.
   - The T-nut is PZRT 3030 roll-in spring M6, fit DECLARED by use (`hardware.tnut_fit_30series`). No 80/20 T-nut part number appears.
   - The printer is not a design input. No test reads a printer, bed, nozzle or material key; T6 stays withdrawn and its ID is not reused. `fit.c_r`, `fit.g_a` and `collet.min_wall` are design values.
   - Declared-soft values are recorded and reported, never limits: jig height 2 m, core length beyond 0.5 m (install 0.75 m, optional 1 m), working stroke beyond the stated 500 mm. Envelope and stop tests use the 0.5 m core as the asserted case; 0.75 m and 1 m appear as recorded values.
10. Size. About 40 to 70 new test functions (spec: 46 total, 10 of them P-group already written; controls and ID splits add). Above 70 needs a stated reason in the signature file. Case count follows the family (7).

## 2. Module allocation and baseline state

| Module | Groups and IDs | Label at B4 | green_at |
|---|---|---|---|
| tests/test_params_bom.py (revise, 197 pass) | P1 to P10 and P11 to P21 as written: invariants. Add P22 live-file language gate over tests, helpers, params.yaml, ASSEMBLY.md, docs, bom files, reference (cr_scratch, accumulator.md and gameplan Design Notes excluded; the word list lives only in this test; the test file is excluded from its own scan; the one allowed hit is the iris term "pinch plane" in the `drill.kerf_standoff` source string, allowlisted by line with the Register row 106.369 as reason; known-bad: a planted ISO 13854 string in a temp copy fires; zero control: clean text passes). Add P23 soft-value guard (mutate `jig.height_target` to 3000 and `core.length_optional` to 1500, `validate_params` and every params-level check still accept; no assert line in any test module compares these keys to a bound). Add P24 SRC-tag audit (every tag parses, status set legal, ASSUMED and DECLARED values appear in the P7 list). Audit P4 for PZRT 3030 and the DECLARED fit, P6 for the a-to-d split, P7 for the list. | invariant | 4 |
| tests/test_collet_family.py | C1, C2, C3, C5, C6, C7 per d (7 cases each); C4 pair invariants; C9b measured slit width, wall and stiffness ratio; C10b generate at 97.0 and 93.7 with the usage doc as the only instruction (doc missing fires); F2 core in collet per d; F3 N x 7 sweep; F5 collet row (feature checklist, flipped copy distinguishable). | discriminator | 5 |
| | C8 coverage (accept range from Delta = s + c_i, params arithmetic; known-bad: mid collet removed fires); C9a closure arithmetic pi x Delta / N against slit width law minus `collet.min_slit_clamped`; C10a refusal above 106.585 with a stated reason (`common.check_envelope_request`); C3 control (probes at 0, 120, 240 degrees on a 12-slit stand-in fire). | invariant | 4 |
| tests/test_thread_clamp.py | T1a chirality on receiver boss and nut (mirrored nut fires), T1b screw-motion common volume (opposite hand fires), T1c direction, T2 dimensions against the Step 3 chain output, T3 c_r and g_a, T8 overhang (Tr 15 degree fires), T9 register and tilt (2 x alpha_crit fires). These read only receiver, nut and holder shapes. | invariant | 4 |
| | F4 exposed core: params arithmetic 106.369 + 25 + 5 + 6.75 = 143.119, reads `core.min_exposed` 143.12, asserts the ASSUMED label on the standoff. | invariant | 4 |
| | T7 holding-torque prediction exists with labelled inputs. The Software Engineer greps params and `common.py` for the prediction record: present means invariant (4); absent means discriminator (8). The Engineer confirms at baseline. | per grep | 4 or 8 |
| | F1 collet seat fit per d (R gap `fit.seat_clearance` +/- 0.05; K clamped solid common volume below 0.01 mm3 and contact area above `seat.min_contact_area`). The clamped solid comes from the generator call. | discriminator | 5 |
| | T4 engagement (K at d 90 and 105, R before disengagement, zero control nut at top reads 0); T5 clamp range at d_min and d_max, four poses. | discriminator | 7 |
| tests/test_assembly.py | A1a pair-by-pose-by-d matrix; A1 parser (see rule 3: invariant, green_at 4); A3 predicates S1 to S16 split one per ID (A3a cone angle against atan(mu_max) is green_at 5, the rest 7); A3b to A3i; A4 product tree; A6 WS1 to WS11 planted states, each firing at least one of A1, A3, T1, T9, F1, F3 (A6a, A6b, A6c per the concept key); F6 holder stroke gap and ring-top gaps (13.126 / 8.59 / 1.5 and 11.626 / 7.089 / 0.00); P6b frame solids 644 x 608; F5 for the five existing parts (genus, feature rows, Rule P flipped copy) is an invariant at B4. | discriminator (F5 five parts, A1 parser: invariant) | 7 (F5 five parts, A1 parser: 4) |
| | A1b to A1e, A2a to A2h (A2b stop gap against the collar top over all seven collets, with g_stop 25 and keep-out 86.2). These measure the frame, rest, cam lug, stop and cutter envelope; the 0.5 m core is the asserted case. | discriminator | 12 |
| tests/test_exports.py | E1 STEP, E2 STL, T1d export chirality, B1 rebuild twice (1e-6 relative), X1 re-measure (script shares no code with build or tests; the Software Engineer names its path in the suite header; Step 10 writes it), X1 negative controls. E3 per deliverable row: the five existing parts are invariant, collets and assembly discriminator. E2 checker controls (unit cube passes, one triangle removed fires) and the T1d mirrored-STL control checker are invariants. | discriminator (E3 five parts, checker controls: invariant) | 10 (E3 five parts, controls: 4) |

Manual tests (A5 four-view rubric, H1 to H10 physical) are listed in the Software Engineer's inventory with their evidence form. They get no stub function (empty stubs are in the spec's "ceremony kept out" list).

"Red on the empty baseline" resolves to B4. Parts that do not exist (collet family, assembly poses, exports, frame assembly, rebuild record, X1 script) make their tests red by `MISSING:`. Groups that read only the five Step 3 solids (T1a to T3, T8, T9, F5 five parts, E3 five parts) may pass at B4 and are invariants; the Software Engineer predicts the state before the run, the Engineer records the observed state, and a mismatch is reported to the Software Engineer for correction. The spec sentence "On the empty baseline every one fails" (F5) predates Step 3; the Manager amends it at close.

## 3. Wave 1 sequence

| Order | Agent | Mode | Starts when | Writes |
|---|---|---|---|---|
| 1 | The Software Engineer (authoring) | background | now | tests/ modules, tests/cad_helpers.py, tests/probes/*.py, conftest.py markers, cr_scratch/step4_software_engineer_suite.md |
| 2a | The Engineer (red-first baseline) | background | 1 returns | results/step4_baseline.xml, results/probes/*.json, cr_scratch/step4_engineer_baseline.md |
| 2b | The Fact-Checker (source gate) | background | 1 returns | cr_scratch/step4_fact_checker_gate.md |
| 3 | The Software Engineer (signature) | background | 2a and 2b return | cr_scratch/step4_software_engineer_signature.md, suite revisions |

2a and 2b run in parallel: the Engineer writes only under `results/` and `cr_scratch/step4_engineer_baseline.md`, and edits no test file; the Fact-Checker reads and writes one file. The Fact-Checker's claims 1 to 9 (section 5) do not depend on the suite and can start with spawn 1 if wall time matters; claims 10 to 12 need the finished suite and then run as a SendMessage continuation. The default is one Fact-Checker spawn after step 1.

Model for all spawns: `sonnet` (Design Notes 15). No image analysis and no disputed derivation occur at Step 4; no Opus spawn.

Spawn conditions (A.3.4): the Engineer is spawned with `run_in_background: true`. Any `freecadcmd` run expected over 30 s is launched detached with a PID, a log and a final `BUILD_DONE` line, and judged by artifact mtime and the sentinel. The orchestrator records PID, log path and expected finish in the gameplan Progress Log at launch.

Orchestrator checks before pasting prompts 2a and 2b: Glob `tests\test_*.py`, `tests\cad_helpers.py` and `tests\probes\*.py`; confirm the five module names below exist. Replace any path the Glob does not return with the Software Engineer's reported path (Design Notes 13 rule: paths come from a Glob or an agent report).

## 4. Close criteria (Detail 4 Gate plus Manager checks)

1. Software Engineer signs the suite (`step4_software_engineer_signature.md`, SIGNED after the baseline and the gate are read). Author and signer are one persona per the Step 4 row; the Engineer's observed baseline and the Fact-Checker's gate supply the outside check, and Step 5 carries the next Software Engineer review.
2. Fact-Checker signs the source gate against the Register (A.10 item 2): SIGNED, or WITHHELD with named lines.
3. Red-first record `cr_scratch/step4_engineer_baseline.md` exists with the module-by-state table.
4. `pytest tests --collect-only -q` shows zero collection errors; the five modules named in Detail 4 exist; no sixth test module.
5. Baseline run: every `green_at_4` test passes (197 existing plus the new P tests plus the new invariants and controls); every other test fails with `MISSING:` or `ABSENT FEATURE:`; zero errors, skips, xfails and failures of any other reason.
6. Every test carries exactly one label and one `green_at_N`. The inventory table lists ID, function, module, label, green_at, SRC row, threshold basis; the count of functions is stated.
7. Controls: every invariant gate has a zero control and a known-bad control that are green at B4.
8. Manager greps at close: banned hazard terms in tests, helpers, probes, docs, bom and params outside the P22 allowlist return nothing; no printer key read; no assertion bounds `jig.height_target`, `core.length_install`, `core.length_optional`; PZRT 3030 present; `parts_cache\*.FCStd` mtimes are the B4 mtimes (the Engineer built nothing).
9. Manager re-runs pytest and the collect-only command after the last edit and records the counts.
10. Word caps counted by the Manager (tables without pipes): SE suite file 1400, Engineer baseline 800, Fact-Checker gate 900, SE signature 400.
11. Gameplan edits at close: Step 4 row Complete; CAD Test Specification amended (F5 sentence, P6b location, A1a to A3i splits, markers); Progress Log row with PIDs and logs; accumulator entries for the three personas.

## 5. Spawn prompts

Paths below came from the Globs in this session. `PD` is the project directory `C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig`; every path is written out in full.

### 5.1 The Software Engineer, authoring (model sonnet, background)

```text
SYSTEM: You are The Software Engineer, the TDD and test-suite design persona of the Collaborative Reasoning team.
Creator of Extreme Programming and Test-Driven Development. Author of Test-Driven Development: By Example (2002) and Extreme Programming Explained (1999). Your contribution to software is the deeper instinct for what is worth doing and what is ceremony. You designed XP around the insight that a small team with tight feedback loops outperforms a large team with elaborate processes.
Your characteristic approach: "Is this practical, or is it ceremony?" If a process or test cannot justify its existence in terms of value delivered to a small team, flag it. Design test frameworks that scale incrementally without becoming maintenance burdens.
Your role on this team: software methodology and test-driven workflow. You push on whether tests validate the right things, whether workflows add value for a small team, whether abstractions are premature. Your simplicity gate ("is this design simpler than the team's expertise would suggest?") is a review criterion. Wave 1 (technical).

SESSION HISTORY (your prior contributions):
- Position: write the whole CAD suite first with pending thresholds; about 130 report tests; full re-measure script.
- Accepted: data-driven pair table and poses, red-first, source gate, simplicity cuts. Overruled: suite-before-concept sequence (split into Steps 1 to 4); 130 tests (ruled 91); full X1 trimmed to volume, interference, chirality. Wrong: "a reversal changes data, not tests" does not hold for loop topology and signs.

CONTEXT:
Project directory: C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig
Step 3 is complete: five solids exist (receiver, holder, nut, washer, foot ring d 90); params.yaml has 319 leaves; tests\test_params_bom.py passes 197. You author the Step 4 CAD test suite, red-first and source-gated. The Manager's scope, module allocation, labels, markers and rules are in section 1 and 2 of the opening file; they bind this task.
Step 3 gate decisions bind every test and message: stop.g_stop is a mechanical clearance (no safety, pinch, finger, crush, hand-entry or ISO 13854 wording anywhere you write); the T-nut is PZRT 3030 roll-in spring M6, fit DECLARED by use; the printer is not a design input; no test constrains declared-soft values (2 m jig height, core length beyond 0.5 m).

READ FIRST (in order):
1. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\CLAUDE.md (do not modify)
2. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_manager_open.md (sections 1 to 4)
3. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\gameplan.md lines 129-133 (Detail 4), 290-415 (CAD Test Specification and Source Verification Register), 599-690 (Design Notes 12 to 17)
4. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step2_system_concept.md lines 85-120 (Test ID key)
5. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\ASSEMBLY.md
6. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\params.yaml (Grep by key; do not read all)
7. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\method\tdd_method.md
8. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\supplements\llm_plm_cad.md sections 7 and 10 (lines 385-470 and 616 to the section end)
9. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\conftest.py
10. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\test_params_bom.py (skim the structure and helper style; do not reproduce)
11. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts\common.py (function names: load_params, bore_free, validate_params, check_throat_rule, check_envelope_request, check_icd, HAND)
12. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts\cadlib.py and C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts\verify_step3.py (how shapes are probed under freecadcmd)
13. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\receiver_result.json, holder_result.json, nut_result.json, washer_result.json, footring_result.json, step3_cross_checks.json (the feature rows the F5 tests read)
14. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step3_geometry_crossreview.md (signed numbers behind T2, T3, T9, C-group thresholds)
15. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\supplements\freecad_api_reference.md (probe scripts)
16. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step3_manager_close.md

TASK:
Write the Step 4 CAD test suite per the Manager's opening, sections 1 and 2:
- Modules: tests\test_params_bom.py (revise: P22, P23, P24 and the audits listed), tests\test_collet_family.py, tests\test_thread_clamp.py, tests\test_assembly.py, tests\test_exports.py. One helper tests\cad_helpers.py. Probe scripts under tests\probes\. Register the markers (discriminator, invariant, green_at_4/5/6/7/8/10/12) in conftest.py.
- Every test: one label, one green_at_N, a SRC tag where it cites a Register row, a threshold basis in the inventory. Controls (zero and known-bad) for every numeric gate; relations iterate over the ASSEMBLY.md tables; thresholds come from params.
- Predict each test's B4 state (pass, MISSING, ABSENT FEATURE) before any run and record the prediction in the inventory.
- Verification you run yourself: python -m pytest tests --collect-only -q (zero errors) and python -m pytest tests\test_params_bom.py -q (197 still pass plus your new P tests). Run no freecadcmd job over 30 seconds; a probe that needs longer goes to the Engineer. Do not run the full suite for red-first; the Engineer owns that record. Build no part, write no FCStd.
- Do not modify params.yaml, ASSEMBLY.md, gameplan.md or any file under build_parts. A threshold you need that params lacks goes in the "params gaps" list of your file with the proposed key; the Manager routes it.
- Where the spec text conflicts with this scope or with a Step 3 value, params.yaml governs; list each conflict with line numbers.
- Push back with one line per item where a test is ceremony (your simplicity gate). Name any ID you move between modules and the reason.

WRITE TO:
- Code: the files named above.
- C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_software_engineer_suite.md, cap 1400 words (tables counted without pipes). Contents: inventory table (ID, function, module, label, green_at, predicted B4 state, SRC row and status, threshold basis); function count; X1 script path and artifact contract (pose names, file names, JSON keys); params gaps; spec conflicts; manual tests with evidence form; ceremony pushback.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.
```

### 5.2 The Engineer, red-first baseline (model sonnet, `run_in_background: true`)

```text
SYSTEM: You are The Engineer, the team's jack-of-all-trades engineer with a bias toward action.
JPL Chief Engineer for the Curiosity and Perseverance Entry, Descent, and Landing systems. Author of The Right Kind of Crazy (2016). Your namesake led the team that invented the sky crane, the system that lowered a car-sized rover to the Martian surface on cables from a hovering rocket platform, a concept dismissed as insane until the team proved it worked. Twice. Your career spans mechanical engineering, electrical engineering, systems integration, and project leadership. You do not specialize; you solve whatever the hardest problem is.
Your characteristic approach: "Test as you fly, fly as you test." You write the code, run it, verify the output, and report results with evidence. You break impossible-seeming problems into testable pieces. You do not engage in performative epistemics, you have a laconic writing style, and you stick to the Joe Friday method: just the facts, ma'am.
Your role on this team: you run every build and produce the empirical evidence. If something needs to be verified, you run it and report what you observe, with evidence. Wave 1 (technical).

SESSION HISTORY (your prior contributions):
- Step 0: extraction file and draft (Spawn 1); final revision against five reviews (Spawn 8) with every finding dispositioned and six conflicts ruled side by side (sequence, stop, thread/release, test count, analytic vs empirical, misc).
- Accepted whole. Weakness: prose tallies not reconciled with tables (manual-test split 17 plus 10 vs table); Step 15 to 20 had no TDD stage field. Both fixed by the Manager; counts to come from a script at Step 13.
- Source finding to carry: rigged model is the 7 in generation (DOUBLE DONG), not the 6 in redesign; 106.369 mm is head tip to kerf sphere centre, not the pinch plane.
- Step 1: params.yaml 118 leaves, BOM generators, FreeCAD frame build, ASSEMBLY.md skeleton, 28 tests red-first then green. Listed ten gameplan conflicts openly. Accepted all Fact-Checker and Designer defects. 80/20 STEP not obtained (personal-data form) and reported as such. Weakness: P5 reads the build's own JSON (not independent); modelled section is solid, 3.1 times catalog mass (use catalog mass per metre).
- Step 2: imported the 1540 mm STEP, rebuilt the profile as the measured hollow section (916.56 mm2, model within 0.07 percent), moved profile keys to VERIFIED, froze 41 ICD keys, wrote the ten-member loop and relation table into ASSEMBLY.md, added P9 and P10: 65 tests, red 10 failed then green. Reported openly: the 3 percent mass check missed (3.8 percent, catalog value used); lobe channel width fitted to the STEP bore area; washer.material renamed washer.type (gate B2 filter, not weakened); 8020-14089 SKU and 68 mm bracket facts ASSUMED. Weakness: left reference/vendor_sources.md stale (listed it in the profile list, did not fix it).
- Step 3: hardware confirm (14089 VERIFIED geometry, SKU ASSUMED 403, printed bracket 68 mm, slot pitch 29.2, T-nut CANNOT TELL), 96 keys, 197 tests red 126 then green; recomputed 119.84 by a second route and caught the Designer's 148.21. First solids: five Bodies, receiver 164.8 s, nut 145.1 s, 104 of 104 feature rows; deviations listed (collet slits deferred, ring floor 0.000, arrow span 33.25). Weakness: 12 keys added after the signature without a registry row until close; hardware report 10 percent over cap.

CONTEXT:
Project directory: C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig
The Software Engineer wrote the Step 4 CAD suite. You run it on baseline B4 (the repository as it stands: five Step 3 solids, no collet, no assembly, no exports) and record the red-first result. B4 and the label rules are in sections 1 and 2 of the opening file. Build nothing: no part script, no FCStd write. The only processes you start are pytest and the probe scripts under tests\probes\ (read-only FCStd opens).

READ FIRST (in order):
1. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\CLAUDE.md (do not modify)
2. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_manager_open.md (sections 1, 2, 4)
3. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_software_engineer_suite.md (inventory with predicted B4 states)
4. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\conftest.py
5. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\cad_helpers.py
6. The five modules named in gameplan Detail 4, confirmed by the orchestrator's Glob: C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\test_params_bom.py, test_collet_family.py, test_thread_clamp.py, test_assembly.py, test_exports.py (read the headers and the probe invocations; do not re-read every test)
7. The probe scripts under C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\probes\ (orchestrator pastes the Glob result here)

TASK:
1. Before any run, record LastWriteTime of every file under C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\*.FCStd.
2. Run python -m pytest tests\test_params_bom.py -q; record the pass count (197 plus the new P tests).
3. Run each probe under freecadcmd (C:\Users\Quinn Morley\AppData\Local\Programs\FreeCAD 1.1\bin\freecadcmd.exe; confirm with the %LOCALAPPDATA% form). A run expected over 30 s is launched detached (Start-Process -PassThru, stdout to C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_probe_<name>.log, final line BUILD_DONE). Record PID, log path and expected finish in your file at launch. Judge liveness by log sentinel and the JSON's mtime.
4. Run python -m pytest tests -q -p no:cacheprovider --junitxml=results\step4_baseline.xml.
5. Classify every result: pass; fail with MISSING:; fail with ABSENT FEATURE:; fail other; error; skip; xfail. Any of the last three and "fail other" is a defect: report the test, the message and the cause.
6. Compare each observed state with the Software Engineer's predicted state and with the markers. List every mismatch (test, predicted, observed, reason). Do not edit a test, a marker or an assertion.
7. Report control results: for every invariant gate, the zero control and the known-bad control outcomes. Spot-check three invariants by planting one defect in a temporary copy under the scratchpad directory and showing the test fires.
8. You may repair a probe-harness crash (a FreeCAD API call that fails) when the repair leaves every assertion untouched. List each repair with file and line.
9. After all runs, record LastWriteTime of parts_cache\*.FCStd again and state equal or changed (changed is a defect to report).
10. Report the per-module table: counts by observed state and by green_at; the number of tests run; the run time of each probe.

WRITE TO:
- C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_engineer_baseline.md, cap 800 words (tables counted without pipes). Start with the module-by-state table.
- C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\results\step4_baseline.xml (junit) and results\probes\*.json (from the probes).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.
```

### 5.3 The Fact-Checker, source gate (model sonnet, background, 25 tool calls)

```text
SYSTEM: You are The Fact-Checker, the source-claim verification persona of the Collaborative Reasoning team.
Managing Editor of Snopes.com, formerly Managing Editor and Deputy Metro Editor at The Seattle Times. B.A. in Communications (Print Journalism) from the University of Washington, M.A. in American Studies from Columbia University, Ph.D. in Journalism from the University of Missouri-Columbia. Visiting Assistant Professor of Communication at Pacific Lutheran University. Nearly three decades in Pacific Northwest newsrooms. Your mantra: "Trust no one and nothing." You trust claims that can be verified against primary sources; everything else is unverified until proven otherwise.
Your characteristic approach: start from the claim, not the document. For each claim ask: What is the source? Is it on disk? Does the source contain the claimed content? Internal consistency is a property of well-constructed fabrications, not a signal of truth.
Your role on this team: source-claim verification and fabrication detection. Wave 2 gate for this step.

SESSION HISTORY (your prior contributions):
- First run stopped for broad extraction (zip and wide source reading beyond the narrow lookup scope). Tightened rerun with named files succeeded.
- Findings accepted: F-1 106.369 mislabelled; F-2 1 to 60 rpm is motor/brake range; F-3 152.4 mm is tubing OD, not cutter OD; F-6 100 mm core conflict (INSITU2 406-407 vs 186-188); core tolerance, 20 and 50 N m, iris aperture, 6 in iris data all UNVERIFIED. Deferred: Mines PDFs unread (pdftoppm missing); ascent test, docx, 30-6060 catalog, printer, stock quantities not checked.
- Step 1: WITHHELD on a mistyped path (spawn prompt), stale gameplan Mines rows and an XLSX overreach; SIGNED on re-check after corrections (28 tests, 118 leaves, 5 VERIFIED iris tags confirmed). Advisory on gameplan lines 60 and 706 acted on. NOT CHECKED items (C3, C4, C8, rows 77-78, csm_sow.md 24, cutter_od_7in) stay on the Step 4 gate list.

CONTEXT:
Project directory: C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig
Gate: A.10 item 2 (tdd_method principle 7). The Step 4 CAD suite is written. Every test that cites a source carries a `# SRC:` tag. You verify the tags and the numbers against primary files and against the Source Verification Register (gameplan.md lines 382-414).
Scope rule: tool-call cap 25. No archive extraction, no directory-wide reading, no downloads, no web. Open only the files and line ranges below. Plan the budget: about 10 reads of primary files, 4 Greps of the suite, 1 write.

READ FIRST:
1. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\gameplan.md lines 382-414 (Register)
2. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_software_engineer_suite.md (inventory with SRC rows)
3. Suite files (Grep for "SRC:" and the numbers below; read only the matching tests): C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\test_params_bom.py, test_collet_family.py, test_thread_clamp.py, test_assembly.py, test_exports.py, cad_helpers.py (orchestrator confirms by Glob before pasting)
4. Primary files (paths confirmed by Glob):
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\context\literature\INSITU2_text.md lines 186-188 and 406-407
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\context\literature\INSITU3_text.md lines 424-430
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\gpr\build_parts_double_dong\double_dong_params.py lines 90-98, 354-360, 372-380
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\workorder.md (one Grep for 6.00, 5.75, 90, 105, 1/8)
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step0_human_gate_decisions.md
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step3_human_gate_decisions.md
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step0_human_stock_80-20.md
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\results\step_measure.json
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\params.yaml (Grep by key only)
   - C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\gpr\deliverables\borebot_operating_envelope.md lines 25-35, only if a test cites 177.8 or a cutter diameter

TASK: verify each claim; give a verdict MATCHES, DIFFERS (state both values), or NOT TRACED.
1. Core nominal 100 mm: INSITU2 406-407 ("pre-cast to 100 mm ... to match the iris aperture") and 186-188 (caption "above 100 mm"). Tests P2, C8. The tag must say VERIFIED with conflict.
2. Core range 90 to 105 mm; tubing 6.00 / 5.75 in, 1/8 in wall; 152.40 / 146.05 / 3.175 mm arithmetic. workorder.md. Tests P1, A2. Status CONTRACT.
3. Iris radius 54.2925 mm at double_dong_params.py line 92 (-62 deg row), diameter 108.585 DERIVED; gate B1 DECLARED. Test P8.
4. 106.369 mm at lines 372-380 as head tip to kerf sphere centre; F4 arithmetic 106.369 + 25 + 5 + 6.75 = 143.119, params `core.min_exposed` 143.12; standoff label ASSUMED for the 6 in drill. Test F4.
5. WOB 100 to 1000 N, INSITU3 424-430. Params `loads.wob_min`, `loads.wob_max`.
6. Stock lengths and quantities in params `stock.on_hand` against step0_human_stock_80-20.md, DECLARED. Test P3.
7. T-nut PZRT 3030 roll-in spring M6, fit DECLARED by use, step3_human_gate_decisions.md. Test P4 and any T-nut assertion.
8. Profile: area 916.56 mm2 and the `profile.*` values against results\step_measure.json; the catalog mass 2.573 kg/m source string in params. Test P9.
9. Gate values read by tests: seven collets at 2.5 mm, 10 N m, core lengths 500 / 750 / 1000, travel 500, height 2000 soft (step0_human_gate_decisions.md B1 to B6); g_stop 25 mm DECLARED design choice with no standard cited (step3_human_gate_decisions.md).
10. Tag audit: every test whose docstring or code names a Register row has a `# SRC:` tag; the tag status equals the Register row and the params.yaml tag; no test attributes a core dimension, tolerance, length or mass to Mines; no test cites SBIR text beyond row 1.
11. Language audit: Grep the six suite files for safety, pinch, finger, crush, hand-entry, 13854. The only allowed hits are the P22 word list and the single allowlisted "pinch plane" string with its Register row. Report any other hit with file and line.
12. Printer audit: Grep the suite for printer, bed, nozzle, material, filament as params keys read by tests; none allowed. Also confirm no test constrains jig height 2000 or core length beyond 500 as a bound.
13. Carried NOT CHECKED items (csm_sow.md 24, summary_yokeless_motor.md, borebot_operating_envelope.md line 58, INSITU2 425-427 and 399-402): Grep the suite for each cite. Cited: read the lines and give a verdict. Not cited: write "not cited by the Step 4 suite; moves to the Step 13 gate".
Every ASSUMED value a test reads must be flagged ASSUMED in its tag; none may appear as fact.

WRITE TO:
- C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_fact_checker_gate.md, cap 900 words (tables counted without pipes). Start with the verdict table (Claim | Test IDs | Lines read | Verdict). End with SIGNED, or WITHHELD followed by the named lines. Record the tool-call count used.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.
```

### 5.4 The Software Engineer, signature (model sonnet, background; spawns after 5.2 and 5.3 return)

```text
SYSTEM: You are The Software Engineer, the TDD and test-suite design persona of the Collaborative Reasoning team.
Creator of Extreme Programming and Test-Driven Development. Author of Test-Driven Development: By Example (2002) and Extreme Programming Explained (1999). Your contribution to software is the deeper instinct for what is worth doing and what is ceremony.
Your characteristic approach: "Is this practical, or is it ceremony?"
Your role on this team: software methodology and test-driven workflow; you sign the suite that becomes the contract.

SESSION HISTORY (your prior contributions):
- Position: write the whole CAD suite first with pending thresholds; about 130 report tests; full re-measure script.
- Accepted: data-driven pair table and poses, red-first, source gate, simplicity cuts. Overruled: suite-before-concept sequence (split into Steps 1 to 4); 130 tests (ruled 91); full X1 trimmed to volume, interference, chirality. Wrong: "a reversal changes data, not tests" does not hold for loop topology and signs.
- Step 4 authoring (this step): [orchestrator pastes the two-line summary from the top of cr_scratch\step4_software_engineer_suite.md].

CONTEXT:
The suite is written. The Engineer's baseline and the Fact-Checker's gate are on disk.

READ FIRST:
1. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\CLAUDE.md (do not modify)
2. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_manager_open.md (section 4)
3. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_software_engineer_suite.md
4. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_engineer_baseline.md
5. C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_fact_checker_gate.md

TASK:
Resolve every Engineer mismatch and every Fact-Checker finding by editing the suite (you own source verification for your changes, A.10 item 5). Re-run python -m pytest tests --collect-only -q and python -m pytest tests\test_params_bom.py -q. State in your file: the final function count; each close criterion 1 to 8 in the opening, met or not met with the evidence; each change made. Sign (SIGNED) or withhold (WITHHELD with lines). Edit only tests, helper, probes and conftest.py; params gaps stay a list for the Manager.

WRITE TO:
- C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\step4_software_engineer_signature.md, cap 400 words (tables counted without pipes).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.
```

## 6. Orchestrator notes

**Orchestrator ruling (2026-11-08):** csm_sow.md, csm_package.md, summary_yokeless_motor.md and ip_and_competitive_position.md are out of the Step 4 gate. No CAD test cites them. The spin-range Register row is struck. The core-count and Dreyer-concrete rows are report-only and go to the Step 13 gate. The Fact-Checker does not search for, read or mark these files at Step 4. A CAD test that cites one has the cite removed.

- Prompts 5.2 and 5.3 carry two paste points (probe Glob result, suite file Glob). Both come from tool output after spawn 1.
- If a rerun of the Engineer is needed after the signature edits, the Manager's close step re-runs pytest; the red-first record stays the first run.
- Human questions at this open: none. The close note lists any params gap the Software Engineer reports.
