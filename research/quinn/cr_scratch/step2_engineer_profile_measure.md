## Measurements: 8020-30-6060 X 1540.step

Source path (read in place, not copied): `C:\Users\Quinn Morley\OneDrive\PROJECTS\Planet Enterprises\NIAC\BOREBOTS\Unleashed Robotics\ENGINEERING\FractalMining\Borebot Hardware\8020-30-6060 X 1540.step`

Method: `build_parts/measure_step.py` under freecadcmd 1.1.4 (sentinel `STEP_MEASURE_OK`, fresh `results/step_measure.json`). Section sliced normal to the extrusion axis at z = -770 (mid length). Edge-level dimensions read from the 196-edge outer wire and 80-edge void wire. Section area cross-checked two ways: 1 mm slab volume and total volume / 1540 mm, both 916.56 mm2.

The file is a 60 x 60 mm hollow 2 x 2 module of 30 mm cells. Its origin is not the profile centre: the section spans x -15..45, y -45..15, extruded toward -Z (z -1540..0). One solid, valid, 386 faces.

| Quantity | Unit | STEP | Prior params.yaml | Delta (STEP - prior) | Status now |
|---|---|---|---|---|---|
| Outer width | mm | 59.9999 (60.000) | 60 | 0 | VERIFIED |
| Outer height | mm | 59.9999 (60.000) | 60 | 0 | VERIFIED |
| Length | mm | 1540.000 | 1540 stock | 0 | confirmed (stock.on_hand unchanged) |
| Slots per face | count | 2 (8 total) | 2 | 0 | VERIFIED |
| Slot offset from face centreline | mm | 15.000 (slot centres 30.000 apart) | 15 | 0 (30 mm pitch confirmed) | VERIFIED |
| Slot opening | mm | 8.000 | 8.0 (ASSUMED) | 0 | VERIFIED |
| Neck depth (lip thickness) | mm | 2.2575 | 3.0 | -0.743 | VERIFIED |
| Cavity width | mm | 16.500 | 12.0 | +4.500 | VERIFIED |
| Cavity depth below neck | mm | 6.908 (floor 9.165 below face) | 5.0 (floor 8.0) | +1.908 (+1.165 total) | VERIFIED |
| Straight cavity side wall below neck | mm | 2.689, then 45 degree flank to the floor | not modelled (rectangle) | new | VERIFIED |
| Cavity floor width | mm | 8.064 (V-notch 1.9 wide x 0.51 deep in floor) | 12.0 | -3.9 | derived from the above |
| Bore diameter | mm | 7.060 (arc fit R 3.530) | 6.65 (ASSUMED, Zoro) | +0.41 | VERIFIED |
| Bore count and position | count | 4, one per 30 mm cell at (+-15, +-15); the 60 x 60 centre is open void | 1 at the centre | topology differs | recorded in `centre_bore` source |
| Bore tap-relief lobes | mm | 4 diagonal lobes per bore, R 1.072 at 4.4435 from axis; bore void 55.28 mm2 | none | new | VERIFIED (channel width 2.283 fitted, DERIVED) |
| Outer wall (face to void) | mm | 2.200 | none | new | VERIFIED |
| Slot side lining | mm | 2.200 | none | new | VERIFIED |
| 45 degree web, perpendicular thickness | mm | 2.550 | none | new | VERIFIED |
| Cell tube (block around bore) | mm | 11.67 square (half 5.835 = slot floor depth); the corner facing module centre R 2.0; V-notch 0.95 half-width x 0.51 deep in each of 16 faces | none | new | VERIFIED |
| Outer corner radius | mm | 2.000 | none (sharp) | new | VERIFIED |
| Slot lip fillets | mm | R 0.5 at the opening and under the lip | none | not modelled (about 1 mm2 effect, not resolved) | recorded only |
| Corner pockets | mm | 4.2 x 4.2, edge 1.3 from each face, 4 pockets | none | new | VERIFIED |
| Section area | mm2 | 916.56 | model 2893.27; catalog 929.9 | model -1976.7 (solid -> hollow); catalog -13.3 (-1.4 %) | `profile.area_step` VERIFIED |
| Mass per metre at 2700 kg/m3 (ASSUMED density) | kg/m | 2.475 | catalog 2.573 | -0.098 (-3.8 %) | see problems |

Rebuilt model (centred on the origin, extruded +Z): analytic area 916.17 mm2 (-0.04 % vs STEP), FreeCAD solid area 915.89 mm2 (-0.07 %). Boolean comparison against the STEP slab (`build_parts/profile_fidelity.py`, sentinel `PROFILE_FIDELITY_OK`): STEP-not-model 3.63 mm2, model-not-STEP 2.96 mm2, symmetric difference 6.59 mm2 = 0.72 % of the STEP area.

Problems found:
1. The mass check misses its target. Directive: within 3 percent of catalog 2.573 kg/m. STEP area at 2700 kg/m3 gives 2.475 kg/m, 3.8 percent under. Catalog implies 2807 kg/m3 on the STEP area, or a section 1.4 percent larger (929.9 against 916.56). Page says 6063-T6, which is about 2700. I did not tune anything to hit 3 percent. The test tolerance is 5 percent so the gap cannot grow. Value used for tip-over and load work: catalog 2.573 kg/m (heavier, conservative). The STEP-based figure is in params as `profile.area_step`.
2. "Centre bore" is a misnomer. The 6060 has four bores, one per 30 mm cell. Key name kept for tests and the BOM; the source string says so. The prior one-bore-at-centre model was wrong in topology as well as in diameter (6.65 against 7.06).
3. The prior slot depths were all wrong by more than 0.7 mm; cavity width was 4.5 mm too small. A T-nut fit check against the old numbers is void.
4. The human's note says they usually keep a 10 cm piece; this file is the full 1540 mm. Measurement is the same.
5. Not independent: the lobe channel width (2.283 mm) is fitted to the STEP bore area. All other builder parameters are direct edge readings.

## Red run

Added 7 test functions plus one 20-case parametrized test (27 cases) to `tests/test_params_bom.py` (group P9) before touching `common.py` or `params.yaml`. Command: `python -m pytest tests/test_params_bom.py -q`. Result on the solid-section builder: **18 failed, 28 passed**. Failures: STEP-measure sentinel (script not yet run), area vs STEP (model 2893.27 vs 916.56), hollow check (2893.27 not below 1200), built-solid area, all 11 profile-value cases then in the table (value, status or source), mass per metre, fidelity (no JSON), control. Record: `research/quinn/cr_scratch/step2_red_run.txt` (tail of output).

## Green run

After the new builder, params and the three FreeCAD runs (`measure_step.py`, `profile_fidelity.py`, `frame_profiles.py`, all sentinel plus fresh output mtime): `python -m pytest tests/test_params_bom.py -q` gives **55 passed in 2.11 s** (28 prior plus 27 new). Record: `research/quinn/cr_scratch/step2_green_run.txt`.

Six members rebuilt, all valid single solids, bbox 60 x 60 mm:

| Member | Qty | Length mm (bbox Z) | Volume mm3 | Area mm2 |
|---|---|---|---|---|
| rail | 2 | 644.0 | 589,831 | 915.89 |
| end | 2 | 488.0 | 446,953 | 915.89 |
| plate_support | 2 | 468.0 | 428,635 | 915.89 |

Prior volumes were 2893 mm2 x length (3.16 times too heavy). Status counts regenerated by `python build_parts/bom_tools.py`: DECLARED 20, ASSUMED 63, VERIFIED 34, DERIVED 16, total 133 (was 118 leaves; 15 added). `bom_stock_allocation.md` had no solid-section note in it (the note lived in `profile.slot_detail_note` and gameplan line 619); regenerated unchanged in content.

## Changed files

- `build_parts/common.py`: `profile_polygons` (now returns outer, 16 cavity polygons, bore radius), new `profile_primitives`, `profile_area_model` (scanline integral of the same primitives, no FreeCAD), `build_profile` (hollow section by Part booleans).
- `build_parts/measure_step.py` (new): measures STEP and STL in place, writes `results/step_measure.json`.
- `build_parts/profile_fidelity.py` (new): section comparison against the STEP, writes `results/profile_fidelity.json`.
- `params.yaml`: all STEP-supplied `profile.*` keys VERIFIED with the required source string; 15 keys added (`slot_cavity_vertical_depth`, `slot_flank_angle`, `slot_lining`, `web_thickness`, `wall_thickness`, `outer_corner_radius`, `bore_lobe_radius`, `bore_lobe_centre_radius`, `bore_lobe_channel_width`, `corner_hole_size`, `corner_hole_inset`, `tube_corner_radius`, `notch_half_width`, `notch_depth`, `area_step`); `slot_pitch` moved DECLARED to VERIFIED (STEP confirms); `slot_detail_note` rewritten, DERIVED. `profile.series`, `area_catalog`, `mass_per_m_catalog` unchanged.
- `tests/test_params_bom.py`: group P9 appended.
- `report_assumptions.md`, `bom_purchased.md`, `bom_stock_allocation.md`: regenerated by `build_parts/bom_tools.py`.
- `results/`: `step_measure.json`, `profile_fidelity.json`, `frame_profiles.json` (+ logs); `parts_cache/frame_profiles.FCStd` rebuilt.
- `research/quinn/cr_scratch/step2_red_run.txt`, `research/quinn/cr_scratch/step2_green_run.txt`.

## 14089 files

`8020-14089.step`: one solid, 293 faces, volume 32,918.6 mm3, bounding box 57.354 x 57.354 x 57.000 mm (x, y from -0.354 to 57.000, z -28.5 to 28.5). Geometry: an L corner bracket, two flat plates 6 mm thick (inner faces at x = 6 and y = 6, outer faces at 0), legs 57 mm long, 57 mm wide, with a 45 degree gusset (plane 44.55 mm from the origin along the diagonal) and small R 0.25 to 1.0 fillets; no cylinder larger than R 1.0 was found, so the plate holes are not circular bores (not resolved further). Identification is geometric: a full-size 30-series gusseted corner bracket. The part number in the filename was not checked against a catalog. `8020-14089 qmod v0.step`: 565 bytes, header only, empty DATA section; FreeCAD reports "shape is invalid". It carries no geometry.

## Brackets: facts only

| Item | 8020-14089.step | Human's printed `8020 30 Series Corner Bracket 3dp.stl` |
|---|---|---|
| Bounding box mm | 57.35 x 57.35 x 57.0 | 68 x 68 x 57 (x -11..57, y -1..67, z -28.5..28.5), 84,888 facets, volume 57,203 mm3 |
| Leg length (outer) | 57 | 68 (61 from the inner corner to the end) |
| Width | 57 | 57 |
| Plate thickness | 6 | 7 (y -1..6 and x -11..-4) |
| Holes | not resolved (no bore cylinders above R 1.0) | 4 per leg, two along the leg and two across; each section 7 mm wide (across) x 10 to 11 mm long (along the leg), full plate depth, so slotted holes; across-the-leg centres at +-15 mm from the centreline = the 30 mm slot pitch; along-the-leg centres about 15.3 and 44.5 mm from the bracket origin (29.2 spacing, within 1 mm of 30 pitch; estimate from section loops, plus or minus 0.5 mm) |
| Hole against 30-series slot | not stated | 7 mm width clears M6 (6.6 mm); fits the 8.0 mm slot opening |
| Full size, hand-friendly | yes (57 mm legs and width, nearly two 30 mm pitches) | yes, larger than the 14089 (68 mm legs); no mini |

The STL also carries lattice and text-like features on the z = +-28.5 faces. Not analysed. The `.3mf` and `XL.3mf` files were not opened. Team picks brackets per joint at a later step.

## Gameplan versus directives: stale rows

- `gameplan.md` line 101 (Step 1 Work): "take the 30-6060 cross-section from the DECLARED stock file ... model it as a parametric extrusion; no catalog download". Section now measured from the STEP; row is history, but its "no STEP" premise is stale.
- `gameplan.md` line 404 (source register row, 30-6060): status "DECLARED by human; no catalog download". Slot geometry is now VERIFIED from the STEP; pitch VERIFIED.
- `gameplan.md` line 607: "30-6060 geometry comes from the DECLARED stock file; no catalog download". Replace with the local STEP path.
- `gameplan.md` line 619: "80/20 STEP not obtained ... built from stated parameters, tagged ASSUMED ... solid section (2893 mm2) ... The human may drop real STEP files into reference/". All stale. Replace: STEP measured, hollow section 916.56 mm2, mass 2.475 kg/m STEP-based, 2.573 catalog used.
- `gameplan.md` line 299 (P5): tests bbox only; P9 now covers area, hollowness, parameters and fidelity. Add P9 to the table.
- `gameplan.md` line 353 (A3, "T-nut centroid inside the slot cavity"): cavity is now 16.5 wide, floor 9.165 below the face, neck 2.2575 thick; any numeric T-nut fit uses these, not the old 12 x 5 x 3.
- `gameplan.md` line 552 and line 554: fine (profile and brackets); line 554 "Step 1 pulls SKUs from the 80/20 catalog" is already superseded by the gate (ASSUMED check only).
- `reference/vendor_sources.md` line 3 ("No vendor STEP file ... Fallback applied: ... ASSUMED") and line 15 ("To replace the ASSUMED slot values ..."). Both stale; the STEP is a local human-supplied file, not a vendor download.
- `research/quinn/cr_scratch/step1_engineer_foundation.md` lines 44 and 47 ("solid ... 2893.3 mm2 ... 3.1 times catalog"): superseded by this file.
- `research/quinn/cr_scratch/step1_manager_close.md` line 31 (STEP not obtained): superseded.
- `report_assumptions.md` lines 68 to 73 (five ASSUMED profile rows): removed by regeneration; `report_assumptions.md` count line now ASSUMED 63.
- `bom_purchased.md` line 13 and `build_parts/bom_tools.py` line 147: "30-series slot fit not stated on any 80/20 page found". Now stated by the STEP: opening 8.0 mm, neck 2.2575 mm, cavity 16.5 mm wide. The T-nut SKU is still unverified (40-3914 is labelled 40 series); I did not touch this text. Flag for the next BOM revision.
- `accumulator.md` line 32 (Step 1 history, "listed ten conflicts"): history; no change.
- Stale only in prompt, not in a file: the directive mass check at 3 percent is unmet (3.8 percent); recorded above.
- No gameplan row should state a profile area other than 916.56 mm2 (STEP) or 929.9 mm2 (catalog). Any mass or tip-over table still using the solid model (2893 mm2, about 7.8 kg/m) is stale; none found in the repository outside the lines above.
