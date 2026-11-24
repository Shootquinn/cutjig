## Edits to test_step6_parts.py and the probes (reason per edit)

| Edit | Reason |
|---|---|
| NEW_IDS gains `plug` (BS6); probe PARTS gains `plug` | Loftsman C5: own part, solid_count 1 |
| RC6: graduation 0 at `rim_top_z - nut.skirt_below_flange`; predicate `scale_errors`; azimuth equals `receiver.key_offset_deg` + 90 | C1: reading plane is the skirt bottom face |
| HD7: skirt-bottom argument; `tick_count == 1`; probe tick = lowest z of the mark | Cluster centre reads 89.5, the edge reads 88.0 |
| Marks probe radii = channel floor minus 0.2, 0.5, 0.8 x `witness.line_depth`; window starts at skirt bottom - 0.5 | Lines are cut 0.5 into a floor at 71.99 |
| Frame probe id via `glyph_math.member_id`; flip about the member's own centre line | C10; rails at y +-274 read 1.0 about world X |
| FR4: `one_rail_notched` (exactly one of two rails above `FLIP_FLOOR`) | Stronger than max-above-floor |
| Glyph `surface()` y span 22 (wing root half-width 20 + 2) | 45 + 90k tommy bosses fake glyphs at 150 |
| NT4/NT5 JSON: span within 1.0 of `nut.glyph_length` | Loftsman fixes the glyph at 6.0 |
| ST1: pad underside at `stop.height_z - stop.pad_thickness` | 12 mm pad |
| Added `test_loftsman_params_keys_present_before_the_builds` | Section 7 keys first; fails `MISSING: params key <first absent>` |

Controls added: scale reference (old +40 reference, 13 marks, pitch 1.1 fire), tick-centre reading (1.5 off fires), member id (old split reads "plate"), one-rail predicate (two or zero notched rails fire). No assertion weakened.

## Gaps and cuts

Every new checklist ID maps to a test. NT9 needs no test of its own: no nut window, so the existing nut genus invariant (`1 + nut.washer_window_count`) stays green. Not tested beyond the feature row, by choice: NT7 skirt geometry, ramp and slot dimensions, C6 bracket overlap (a Step 7 finding). Cut: none; each test serves an ID or a close criterion.

## Params

P2 pins no leaf count (`> 40` and total equals the status sum). The pin is the P7 counts line in `report_assumptions.md` plus one row per ASSUMED or DECLARED key: the Engineer updates both when adding keys. P7 scans quoted test keys; the three literal keys the test reads sit in `H.PARAM_GAPS`, and the key list test builds names from fragments. Key names are pinned as `group.name`; the skirt keys carry the `skirt_` prefix (Loftsman section 7 shorthand).

## Run

| Item | Value |
|---|---|
| Collected | 582 (was 578) |
| Passed | 373 |
| Failed | 209 (MISSING 202, ABSENT FEATURE 7, other 0) |
| green_at_6 | 33 collected, 0 passing, all red by absence |
| New | 4 (plug F5, key list, two controls) |

## Test contract

| Test | Reads | Passes when |
|---|---|---|
| F5 new part (per part incl. plug) | `<part>_result.json`, `step6_parts` probe | one valid closed solid; Euler and volume match; rows for the part IDs; booleans, bboxes, run_seconds; base flip above floor |
| Frame tests | `allocation`, `bracket_count`, `tnut_instances`, probe members | 6 members named `member_<id>_<n>`; 16 brackets; 128 T-nuts; whole stock pieces; one rail notched |
| Rebuilt rows | result JSON `features` | RC6, HD7, NT4, NT5, NT7 rows, volume > 0, pass |
| Rebuilt F5 | probe, `rebuild.reason_ids` | valid solid, flip above floor, rebuild record |
| HD5, HD6 | `flange_scan`, `down_planar_z` | no hole on the annulus; no extra downward face |
| NT4/NT5 | marks probe `glyphs`; JSON `glyphs` | clockwise and counter-clockwise on opposite faces of one wing, span about 6, inside 21.86 |
| RC6 | marks probe `marks_z`, `rim_top_z` | 14 marks, pitch 1.0, first at rim top - 40 |
| RC6 zone | receiver JSON `witness` | zone and bands equal `witness.*` |
| HD7 | `tick_local_z`, `holder_under_local_z`, `tick_count` | reading equals 1.5 and 8.59 within 0.05 |
| ST1 | stop JSON `owner`; `pad_faces` | owner `upper assembly`; 60 x 60 faces at the height and 12 below; no nut volume |
| Key list | params | all Loftsman keys exist |
