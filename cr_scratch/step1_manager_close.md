## What did we produce?

Step 1 Foundation, closed 2026-11-08.

| Output | State |
|---|---|
| `params.yaml`: 118 leaves, each with source and status (DECLARED 23, ASSUMED 69, VERIFIED 11, DERIVED 15) | green |
| `build_parts/common.py`, `bom_tools.py`, `frame_profiles.py`; six 30-6060 members built in FreeCAD 1.1.4 | green |
| `tests/test_params_bom.py`: 28 tests, written red-first | 28 passed, re-run by the Manager (0.60 s) |
| `bom_stock_allocation.md`, `bom_purchased.md`, `report_assumptions.md` (92 rows), `ASSEMBLY.md` skeleton | generated |
| Literature summaries, `reference/vendor_sources.md`, patched extraction file | done |
| Fact-Checker signature | SIGNED (after one WITHHELD) |
| Designer seed params review | recorded: 24 missing feature params, generator NOT READY |
| Gameplan repairs | lines 60, 706 (Mines PDFs read, silent on core dimensions); test specs C6, F1 and the Echo registry now name `collet.min_wall`, `fit.seat_clearance`, `core.diameters`; Detail 1 FreeCAD path; Design Notes 13 added; Steps 1, 3, 5 rows updated; Progress Log row; Current step 2 |

## Gate verification

- Fact-Checker signature: SIGNED (`step1_fact_checker_corrections.md`, "Re-check after corrections").
- Designer record: exists (`step1_designer_params.md`).
- Manager test run: `python -m pytest tests/test_params_bom.py -q` returned `28 passed in 0.60s`.

## Defects: system problem or one-off?

- Fact-Checker WITHHELD: cause was a path re-typed in the spawn prompt (`gpr\double_dong_params.py`; the file is in `gpr\build_parts_double_dong\`). System problem, small. Fix in process: Design Notes 13 rule, spawn prompts name paths copied from a Glob or the Engineer's report, never re-typed.
- Stale gameplan rows (Mines PDFs, `print.*`, `collets.diameters`, FreeCAD path): system problem. Each step's findings change values that the gameplan echoes. The Echo Site Registry and Design Notes 13 now carry the corrections; the Step close checks the registry against the Engineer's "gameplan versus directives" list.
- Designer seed defects (envelope above throat, duplicate diameters, keepout contradiction, independent iris diameter, placeholder stop height, printer-basis keys): one-off seed errors, fixed and each now guarded by a test.

## What the human should know at the gate

- The 108.585 mm open diameter is DERIVED from the DECLARED 54.2925 mm radius. Changing the radius moves the diameter and the collet envelope cap (106.585 mm).
- Optional download: the 80/20 30-6060 STEP was not obtained because the vendor form needs personal details and a PartCommunity account; none were entered. The frame profile is built from stated parameters (ASSUMED) and is a solid section of 2893 mm2 against the catalog hollow 929.9 mm2. Mass and tip-over work use the catalog 2.573 kg/m. If you download the STEP files, drop them into `reference/`; Step 2 begins by importing and measuring them. Without them, work continues on the ASSUMED profile.
- Stock: the jig uses 3,200 mm of the 15,688 mm on hand with no extra cuts. The 468 mm cross members leave 20 mm slack between the 488 mm-spaced rails; Step 12 places them.
- T-nuts: 80/20 lists M6 ball-spring roll-in nuts for 10, 15 and 40 series only. 40-3914 and 13031 are assumed to fit the 30 series; verify the SKU at purchase.
- The collet generator is NOT READY for on-demand collets: 24 of 38 Detail 6 features have no param key. This is carried to the Step 3 blocking params review and the Step 5 generator deliverable.
- Items the Fact-Checker did not check (C3, C4 envelope line 58, C8, extraction rows 77-78, csm_sow.md 24, cutter OD 177.8) stay on the Step 4 gate list.
- Assumptions adopted without asking: ASSUMED seeds stand until Step 3; `stop.height_z` 160 mm is a placeholder; the printer remains a non-input.

## Recommendation

Approve. Step 2 (system concept) opens next. No further cycle is needed on Step 1.
