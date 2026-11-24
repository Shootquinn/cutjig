## What we produced

Step 2 is Complete. Current step is 3. Tests re-run by the Manager: `python -m pytest tests/test_params_bom.py -q` = 65 passed (55 at Step 2 profile pass, 10 P10 tests at integration).

| Output | State |
|---|---|
| `research/quinn/cr_scratch/step2_system_concept.md` | Nine decisions, frozen ICD, tolerance budget, Test ID key. 6042 words (see defects). |
| Loftsman signature | SIGNED at Re-check 2 after three withheld lines (grip window, slack unit mix, collet chamfer), all corrected. |
| Topologist signature | SIGNED on U13 to U16 and decision 8. Last withhold (decision 5 wording, tests A3h, A1d, A3g) closed by ruling: the Topologist's own smallest edits were applied and grep-checked; the Topologist did not re-view the file. |
| Designer comment | Recorded. Four BLOCK items (S2-1 steady rest, S2-2 park, S2-3 strap, S2-7a manual raise) answered in the concept. ABSORB items assigned to Steps 3, 5, 7. |
| Profile | 30-6060 measured from the human's STEP: hollow 916.56 mm2, `profile.*` VERIFIED. Rebuilt model within 0.07 percent. |
| ASSEMBLY.md, params.yaml | Ten-member force loop, 45-pair table, 41 frozen ICD keys. Washer key is `washer.type` (gate B2 filter treats `material` as a printer key; not weakened). |
| gameplan.md | 45-row directive list plus the profile list applied: Steps table, Details 2, 3, 5, 6, 8, 9, 11, 12, test specs (P4, P6, P8, P9, P10, T4, T9, F4, F6, A1 to A3), Design Notes 2, 3, 5, 7, 9, 12, 13, new Design Notes 14, Echo Site Registry (rows corrected, seven added), Register, Progress Log. |
| accumulator.md | Entries for Manager, Loftsman, Systems Engineer, Designer, Engineer, Topologist. |

## Verification of the nine close items

| # | Item | Result |
|---|---|---|
| 1 | Concept exists; nine decisions each carry a number or stated assumption and a test ID | PASS on content. DEFECT on length: 6042 words against "one page plus two tables". |
| 2 | Signatures exist; cross-review records zero unresolved disagreements | PASS. Reply file: register DISPUTED (80 against 88) closed at 88.0 by number; all other items AGREED. Topologist decision 5 and test IDs closed by ruling (no re-view). |
| 3 | pytest, count at least 28 | PASS, 65 passed. |
| 4 | `profile.*` VERIFIED with STEP source; vendor note and solid-section note corrected | PASS after repair. `reference/vendor_sources.md` lines 3 and 15 still said "no STEP, ASSUMED"; rewritten. No solid-section note remains in `bom_stock_allocation.md` or `report_assumptions.md`. |
| 5 | Area within 1 percent; mass per metre within 3 percent or written down | PASS. Area 0.04 to 0.07 percent off. Mass 2.475 against catalog 2.573 kg/m is 3.8 percent under; written down in the profile file and Design Notes 14; catalog value used. |
| 6 | Force-loop sentence in ASSEMBLY.md; stop on the upper-assembly side; no human-input row; no printer key | PASS. Sentence at ASSEMBLY.md line 103 (ten members); `stop.owner` upper assembly; no concept row requests input; `_PRINTER_KEY` filter unchanged in `build_parts/common.py` line 35, and `washer.type` replaces the rejected name. |
| 7 | Engineer's directive list checked against the Echo Site Registry | PASS. All 45 rows applied (75 text replacements, each matched exactly once), plus the profile-measure list. |
| 8 | Designer comment recorded; no unresolved finding to the human gate | PASS with one carry. The Designer's comment predates three concept revisions; the Designer reviews the revised text at the Step 3 params review. The 780 mm park reading (below) goes to the human as an assumption, not a question. |
| 9 | Accumulator entries for personas that ran | PASS. |

System problem or one-off, per defect:
- Concept length (system). A "one page" limit that nobody counts is not a limit, and each signer round appended text. Fix in Design Notes 14: a concept step carries a word cap in the spawn prompt and the Manager counts at close.
- Signer withholds (system). The concept was written before geometry numbers existed, then rewritten after them; every withheld line was a number the first draft invented. Fix in Design Notes 14: the concept is drafted after the cross-review numbers (agent order 2, 4, 5, then 6) for any future concept step.
- vendor_sources.md stale (system). Generators rewrite generated files; hand-written files that restate a measured value are not rewritten. Fix: the Echo Site Registry names the file in the profile and bracket rows; an Engineer measurement step lists hand-written files mentioning the measured value.
- Overloaded test IDs (one-off in the concept, system for the plan). Signers split them; Step 4 rewrites the CAD Test Specification groups from the concept Test ID key.

## What the human should know at the gate

Assumptions adopted (parameters, not questions):
- Working stroke 500 mm (gate B6 "travel at most 0.5 m"); the 950 mm loading park and about 780 mm of carriage range are read as not working travel. Reached only by a manual raise, held by a pin latch.
- One 500 mm stroke retains 465.07 mm of core (534.93 mm of advance needed). A 535 mm travel option is recorded, not applied.
- Bolt-down is the operating condition. Unbolted tip-over is 68 N at the column top, 158 N at the centre of mass (23.8 degrees static tilt).
- Holding with the PTFE washer always fitted: 15.47 N m at d = 105, 13.26 at d = 90. The plain washer gives 10.65 and 9.13 and misses 10 N m at d = 90 by 8.7 percent, so no margin is claimed on it. All inputs are ASSUMED friction coefficients; the hold test decides.
- Core masses 10.4, 15.6, 20.8 kg (d = 105, 2400 kg/m3).
- Thread major 149.58 mm, nut OD 166.28 mm, cone 10 degrees, releasing cone retired, no jacking holes (collar back-off lift releases).
- Stop-height seed 160 mm; A2b computes about 170 and Step 3 fixes it.
- Brackets: 30-4332 (30 mm legs) superseded; minimum leg 57 mm. Eight joints: four outer corners take the 57 mm class (8020-14089), four plate-support ends take the printed 68 mm bracket. Purchased brackets drop from 16 to 8. The 8020-14089 SKU (identified by geometry; part number not checked against a catalog) and the 68 mm bracket facts are ASSUMED in params; Step 3 confirms both.
- Handling: steady rest at every core length with mechanical release by the upper assembly, choke strap with a 250 mm side handle, no overhead strap point, manual raise by ratchet hoist with a 300 N shear-link fuse.
- The Designer's finger-crush figure (`stop.g_stop` at least 25 mm against the concept's 10 mm) is unchecked against ISO 13854; Step 3 checks it and may change the ICD.

## Recommendation

Pass the gate and open Step 3. The signed concept, 65 passing tests and the repaired plan give Step 3 fixed numbers to build against. Residual risks are the ASSUMED friction coefficients (settled by the Step 8 coupons and Step 11 hold test) and the thin 0.69 mm lead-in capture margin.

## Step 3 preview

Step 3 is the first CAD step.
1. Blocking gate first: the Designer reviews params for the 24 missing features in `research/quinn/cr_scratch/step1_designer_params.md`, adds the Step 2 ABSORB items (Design Notes 14: witness scale, wing grip, g_stop crush gap, key sector and bolt-down method, release marker, abuse torque and bar length, captive washer, nut-top range), and re-reads the revised concept. Output `research/quinn/cr_scratch/step3_designer_params.md`. No geometry before it closes.
2. Geometry: the Loftsman and Topologist cross-review thread, cone, slits, seat, register and clamped-state solid by number, confirming the Step 2 values in the solid (holder length 88.0, g_reg 0.25, ring top z 2.00, washer notch, 8020-14089 and 68 mm bracket facts). Output `research/quinn/cr_scratch/step3_geometry_crossreview.md`.
3. The Engineer builds the first solids from `params.yaml` (receiver, holder, nut, washer, collet foot ring) only after the signed cross-review (A.4), using `build_parts/common.py` and per-part scripts; any FreeCAD run over 30 s goes background.
4. Cross-review requirement: Loftsman and Topologist both sign; disagreements resolve by number, not opinion. Spawn prompts copy paths from a Glob or an agent report, never retyped (Design Notes 13).
