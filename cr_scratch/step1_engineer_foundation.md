## Outputs

All paths under `C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\`.

| Output | Path | State |
|---|---|---|
| Tests P1 to P8 (26 functions) | `tests/test_params_bom.py`, `conftest.py` | written first; red, then green |
| Params seed (116 leaves, each with source and status) | `params.yaml` | green |
| Shared module (paths, loader, validate_params, throat and ICD checks, 30-6060 profile builder) | `build_parts/common.py` | green |
| BOM tools and generators (counts by script) | `build_parts/bom_tools.py` | green |
| Frame member build (FreeCAD) | `build_parts/frame_profiles.py` -> `results/frame_profiles.json`, `parts_cache/frame_profiles.FCStd` | sentinel + fresh artifact |
| Stock allocation | `bom_stock_allocation.md` | generated from params |
| Purchased hardware | `bom_purchased.md` | generated from params |
| Report assumptions list (95 rows, counts line) | `report_assumptions.md` | generated; P7 checks it |
| Assembly skeleton | `ASSEMBLY.md` | frame, poses R and K, 36-pair relation table, signed feature per part, load path placeholder |
| Patched extraction file (16 lines marked PATCHED) | `cr_scratch/step0_engineer_source_extraction.md` | done |
| Literature summaries (cited ranges only) | `context/literature/INSITU2_text.md`, `INSITU3_text.md`, `double_dong_params.md`, `mines_pdfs.md` | done |
| Vendor record | `reference/vendor_sources.md` | no STEP file (see below) |
| Red and green evidence | `cr_scratch/step1_red_run1_no_modules.txt`, `step1_red_run2_empty_params.txt`, `step1_green_run.txt` | saved |

## Red-first and green

- Run 1, tests only, no modules: collection error, `ImportError: cannot import name 'common'`. Red for a wrong reason; recorded, not counted.
- Run 2, `common.py` and `bom_tools.py` present, `params.yaml` empty, no BOM files, no result JSON: 26 failed, 0 passed (0.35 s). Failures are KeyError on missing keys, FileNotFoundError on the BOM files, assertions on empty validation. Every known-bad test asserts its zero control first, so none can pass on the empty file.
- Green, seed params and generated files: `26 passed in 0.56 s` (`step1_green_run.txt`).
- P2 counts (printed by script, `results/p2_counts.json`): DECLARED 25, ASSUMED 70, VERIFIED 11, DERIVED 10, total 116. `report_assumptions.md` lists 95 rows (25 DECLARED + 70 ASSUMED).
- P5 is not independent of the build: it reads `results/frame_profiles.json` written by the FreeCAD run. Six members, bbox 60 x 60 x cut length, valid, one solid each.

## FreeCAD check

- The gameplan path `C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe` does not exist. FreeCAD 1.1.4 is at `C:\Users\Quinn Morley\AppData\Local\Programs\FreeCAD 1.1\bin\freecadcmd.exe`. `common.freecadcmd_path()` tries both.
- Minimal run: box volume 6000.0, sentinel `FC_MIN_OK` and artifact `results/fc_min.txt` (mtime 16:05:09), exit code ignored per A.15.
- `frame_profiles.py`: sentinel `FRAME_PROFILES_OK 6 members`, FCStd 30,084 bytes, JSON fresh. Wall time 6 s, so no background process was needed; PID and log fields are not applicable.
- Note: the sentinel line is partly overwritten by FreeCAD's progress carriage returns on the console; the JSON carries `"sentinel": "FRAME_PROFILES_OK"` and the test gates on that.

## Downloads (restriction lifted by the coordinator)

| Item | Result |
|---|---|
| poppler | installed with winget (`oschwartz10612.Poppler` 25.07.0). `pdftoppm` present: **yes** (renders page 1 of the LOI PDF to PNG, 35,633 bytes). It was absent at the start of the step. |
| Mines PDFs | read as text. No core dimension, length or mass in any of the four. Register claim "Mines zip holds no core dimensions" is now VERIFIED for the PDFs; XLSX budgets not opened. The report still asserts SBIR text only. |
| 80/20 30-6060 STEP | **not obtained.** The CAD button opens a form for first name, last name, email and address, and the notes say a separate PartCommunity account is required. I did not enter or invent personal data. Fallback per directive: profile built from stated parameters, tag ASSUMED. |
| Catalog pages (HTML) | read: 30-6060, 30-4332, 30-4302, 40-3914, 13031. See `reference/vendor_sources.md`. |
| Values moved to VERIFIED from downloads | `profile.area_catalog` 929.9 mm2 (page: 9.299 sq cm), `profile.slots_per_face` 2 (page: eight open T-slots, two per face). |
| Not measurable without the STEP | slot opening, T-slot undercut, wall thickness, corner radius, centre bore. Seeds are ASSUMED (centre bore 6.65 mm is a distributor listing, not 80/20). |

Problem: the modelled section is solid (area 2893.3 mm2) and the catalog section is hollow (929.9 mm2). Envelope, slot positions and length are right; modelled mass is 3.1 times catalog mass. Use `profile.mass_per_m_catalog` (2.573 kg/m, DERIVED) for tip-over and mass work. The drop-in fix is the STEP file from a human-registered download placed in `reference/`.

## pdftoppm

Present: yes, after the winget install. Original check (before the directive): absent, ASSUMED resolution "report asserts SBIR text only" is kept because the PDFs hold no dimensions anyway.

## Stock allocation summary

- On hand 15,688 mm (computed). Jig consumes 3,200 mm: 644 x 2, 488 x 2, 468 x 2, whole pieces, no saw cut. Remaining 12,488 mm for other projects, including all four 1540 mm lengths (reserved for Step 12 columns).
- Extra cuts table: empty. Cost $0.
- Purchased (counts from script): 16 full-size 30-series gusseted inside corner brackets (30-4332, alt 30-4302), 44 M6 spring-ball roll-in T-nuts (40-3914, alt 13031), 36 M6 x 16 and 9 M6 x 20 stainless screws, 45 M6 washers. All "verify SKU at purchase".

## Assumptions adopted

Full list with source text: `report_assumptions.md` (95 rows). Groups:

| Group | Keys | Tag |
|---|---|---|
| Gate decisions | iris.throat_open_diameter 108.585 and radius 54.2925; core.diameters 90 to 105 at 2.5; core.length_capture/install/optional 500/750/1000; upper.travel_max 500; jig.height_target 2000 (soft, not tested); loads.torque_design 10 N m; collets (7, 2.5 mm); stop.owner; profile 60 x 60, pitch 30; stock.on_hand; hardware rules | DECLARED |
| Tolerance and density | core.tol 1 mm; core.density 2400 | ASSUMED |
| Keep-out | drill.tube_od 152.4, tube_id 146.05, r_face_margin 10, kerf_standoff 106.369 (7 in model, carried to the 6 in drill) | ASSUMED |
| Loads | loads.axial_design 1000 N (design choice bounded by WOB 100 to 1000 N) | ASSUMED |
| Generator | collets.envelope 85 to 110; collet.c_i 1.0; slit_count 12; slit_width_seed 1.5; min_slit_clamped 0.5; web_strain_allow 0.01 | ASSUMED |
| Mechanism seeds | thread pitch 8, 45/45, major 165, min_engage 3 pitches; cone 10 and 20 degrees; chain t_c, H, t_h, t_b, h; wingnut 181 and 230; friction mu_k .35, mu_c .40, mu_t .25, bearing .25, 45 MPa; fit c_r .35, g_a .30; print.min_wall 1.2, seat_clearance .30; seat area 200; stop g_stop 10, margin 5, hard_stop_gap 6, height 850 | ASSUMED |
| Frame and hardware | frame.members roles; joints 8; brackets and T-nut counts; SKUs 30-4332, 30-4302, 40-3914, 13031; screw lengths; profile slot geometry (opening 8, neck 3, cavity 12 x 5), centre bore 6.65; ICD text fields | ASSUMED |
| Sourced | iris leaf data (7 in model), core.diameter_nominal 100 (conflict noted), loads.wob_min/max, drill.cutter_od_7in 177.8, profile.area_catalog, slots_per_face | VERIFIED |
| Derived | drill.tube_wall, r_face, dome_pole_offset 34.9315, core.min_exposed 121.369, icd.keepout_radius, footprint 644 x 608, profile.slot_offset, mass_per_m_catalog, stock.total_length | DERIVED |

## Gameplan versus gate decisions and directives (listed, not resolved silently)

1. FreeCAD path. Gameplan Detail 1 names `C:/Program Files/FreeCAD 1.1`; the install is under `%LOCALAPPDATA%\Programs`. Both paths coded; the gameplan line needs the new path.
2. Param group `print.*`. Test specs C6 and F1 read `params.print.min_wall` and `params.print.seat_clearance`; the gate says no printer keys. I kept the two names as design rules with no bed, material or nozzle value, and P1 rejects keys named printer, bed, nozzle, material or filament. Step 4 may rename.
3. "No downloads" (Detail 1, Manager scope, Step 0 Register) versus the later coordinator directives lifting it. Followed the directives. Register rows "Mines PDFs unread" and "pdftoppm absent" are out of date.
4. Detail 1 says "take the 30-6060 cross-section from the DECLARED stock file; no catalog download". The directive demands measured vendor geometry. The only vendor route for STEP is a personal-data form; not submitted. The section stays ASSUMED.
5. T-nut series. Gameplan and stock file say "M6 spring-ball roll-in for 3030". 80/20 pages list M6 ball-spring roll-in nuts for 10, 15 and 40 Series only; none labelled 30 Series. The 30-series self-aligning roll-in nut (13092) has no ball spring. Candidates 40-3914 and 13031 are ASSUMED to fit.
6. Design Notes 7 starting allocation. The 468 mm plate-support members between rails 488 mm apart leave 20 mm total slack, so full-size corner brackets cannot seat them flush. Allocation is roles-ASSUMED; Step 12 must place them (on top of the rails, or lengthwise) or swap with a 488.
7. P2 says counts "match the register". The Register has no count column. I defined the match as: each Register-mapped key carries the Register status (19 keys in the test), and the counts are printed from the script.
8. Register row "Tubing ... CONTRACT". Task and gate use ASSUMED for the keep-out; params tags tube_od and tube_id ASSUMED.
9. `core.diameters` and `collets.diameters` both exist (Detail 1 and Echo Registry name them separately); both hold the same seven values. A custom collet changes only the second.
10. Hard-stop gap and stop height: the gameplan fixes owners but no numbers; 850 mm and 6 mm are Engineer seeds, ASSUMED.

## Corrections

Response to `step1_fact_checker_corrections.md` and the Designer seed defects. Run: `cr_scratch/step1_green_run_after_corrections.txt`, **28 passed** (was 26; two tests added). New counts from script: DECLARED 23, ASSUMED 69, VERIFIED 11, DERIVED 15, total 118; `report_assumptions.md` regenerated (92 rows).

### A. Fact-Checker

| # | Item | Result |
|---|---|---|
| A1 | `double_dong_params.py` path | The path used at Step 1, `CC\gpr\build_parts_double_dong\double_dong_params.py`, was already correct; the Fact-Checker used `CC\gpr\double_dong_params.py`. Re-read with Grep: line 92 `IRIS_CLOSED_DEG = -62.0` ("aperture 54.2925 -> 0.0000 mm"); 93 `IRIS_LEAVES`; 354 `CORE_BORE_OD_MM = 177.8`; 355 `CORE_OD_MM = 100.0`; 357 `CORE_LENGTH_MM = 500.0`; 360 `CORE_KERF_SPHERE_R_MM = 71.4375`; 368 "measured shell faces: 71.4375 core side, 74.6125 rock side"; 372 `CORE_IRIS_STANDOFF_MM = 106.369`; 402 `CORE_KERF_WIDTH_MM = 3.175`. All five VERIFIED tags and the PATCHED lines confirmed; sources in params.yaml now say "re-read Step 1". Note: the 34.9315 mm dome-pole offset is arithmetic on lines 372 and 360, with the 534.9315 form at lines 379-380; tagged DERIVED. |
| A1 cites | C7 cited INSITU2 408 and 834 | Line 408 is the closure-torque sentence. Replaced by lines 218 and 829 ("low-density concrete", no density value). |
| A1 cites | C10 cited "354, 91-96" against IRIS_LEAVES 93-98 | Reconciled to 354-356 and 92-98. |
| A1 tag | Iris radius tag cell | Closure row: MEASURED for the number, DECLARED for the radius reading. Open-diameter row: DECLARED. |
| A2 | gameplan.md lines 398, 564, 605 | Edited surgically: Mines PDFs read at Step 1 (pdftotext) and XLSX opened (openpyxl); no core dimension, tolerance, length, mass or delivery state; report still asserts SBIR text only. |
| A3 | Extraction C9 and the budgets | `openpyxl` installed (download). Opened `260647_Budg.xlsx` and `260648_Budg.xlsx` read-only: 3 sheets (MinesBudgV1, Input Tables, Calculations Backup), 491 text cells each. Search for core, diameter, length, tolerance, mm, inch, mass, kg, cm: zero hits. C9 now says the PDFs and the two workbooks state no core diameter, tolerance, length, mass or delivery state. `context/literature/mines_pdfs.md` updated. |

### B. Designer seed defects (params.yaml, common.py, tests)

| # | Defect | Fix |
|---|---|---|
| B1 | envelope_max 110 above the 108.585 throat | `collets.envelope_max` = 106.585, DERIVED: throat - `core.tol` - `collets.min_throat_slack` (1.0, ASSUMED). Source states a collet above it needs a larger throat. `validate_params` rejects any envelope above the cap (new test). |
| B2 | `collets.diameters` duplicated `core.diameters` | `collets.diameters` deleted; `core.diameters` is the single source. `collets.count` and `collets.spacing` stay and are validated against it. Gameplan test specs and the Echo registry that name `collets.diameters` should read `core.diameters`. |
| B3 | keepout 81.2 vs r_face 86.2 | `icd.keepout_radius` = 86.2, DERIVED from `drill.r_face`; `check_icd` fails if it falls below r_face (new assertion). |
| B4 | iris diameter and radius independent | Radius DECLARED; `iris.throat_open_diameter` is now DERIVED (2 x radius) and `validate_params` rejects a mismatch (new test). P8 and its known-bad (radius 50 mm fires, 60 mm passes) now change the radius. Note: gate B1 called 108.585 DECLARED; the tag is DERIVED from the DECLARED radius, per this instruction. |
| B5 | stop.height_z 850 below a 1 m core | `stop.height_z` = 160 mm, DERIVED: `stop.nut_top_z` (150, placeholder, ASSUMED) + `stop.g_stop` (10); `stop.start_z` = 660 mm adds `upper.travel_max`. Source strings mark the height a placeholder; no test asserts its value (P6 checks only that it exists). `icd.stop_height` follows. |
| B6 | printer basis in wingnut.span and print.min_wall | `print` group deleted. `collet.min_wall` (1.2, design rule) and `fit.seat_clearance` (0.30) replace `print.min_wall` and `print.seat_clearance`; this also removes contradiction 2 of the earlier list (gameplan test specs C6 and F1 should read the new keys). `wingnut.span` and `wingnut.body_od` re-sourced as hand-torque and radial-chain design values, no printer reference. Friction seeds keep their "generic FDM" wording from the Register and are not changed. |

Not touched (Step 3 blocking review): missing-feature parameters.
