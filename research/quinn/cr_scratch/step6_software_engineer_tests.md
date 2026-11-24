## Baseline run (B6 plus Step 6 tests)

540 to 578 collected (+38). 371 passed (364 baseline plus 7 controls), 207 failed: MISSING 200 (175 baseline plus 25 new), ABSENT FEATURE 7 (1 plus 6 new), other 0. Green_at_6 discriminators: 31 collected items from 15 test functions, all red by MISSING or ABSENT FEATURE. New controls: 7, all green_at_4 invariants. Suite time 57 s.

## Files

`tests\test_step6_parts.py`; probes `tests\probes\probe_step6_parts.py` (writes `step6_parts.json`), `probe_step6_marks.py` (writes `step6_marks.json`), `glyph_math.py` (pure glyph reader, shared with the controls). The probes are unrun: no Step 6 FCStd exists. The Engineer runs them and fixes probe faults inside the step.

## Result-JSON contract (every new part, plus receiver, holder, nut)

| Key | Type |
|---|---|
| part, volume_mm3, euler_VEF, run_seconds | str, float, int, float |
| isValid, isClosed, solid_count | bool, bool, int (1) |
| features[] | {feature str, id str (checklist ID), volume_mm3 float > 0, pass bool} |
| booleans[], boolean_count | {name, faces_before int, faces_after int}; int equal to list length |
| bbox_plain, bbox_optimal | objects |
| all_features_pass | bool |
| frame only | allocation[{id, qty, cut_mm, stock_piece_mm}], bracket_count, tnut_instances |
| stop only | owner "upper assembly" |
| nut | glyphs{tighten, loosen}: {wing, face, direction_sign (-1 cw, +1 ccw from +Z), radial_span} |
| receiver | witness{zone, band_low, band_high} |
| receiver, holder, nut | rebuild{before_volume, after_volume, reason_ids[]} |

Frame FCStd: one solid object per member `member_<id>_<n>`, bracket `bracket_<purchased|printed>_<n>`, T-nut `tnut_<n>`.

## Default ID-to-part map (Loftsman may amend)

base BS1-BS4; tray BS5, BS6; foot BS7; tnut FR3; both brackets FR2; frame FR1, FR4; caddy AC1; gauge AC2; rest AC3; stop ST1; receiver RC6; holder HD7; nut NT4, NT5, NT7.

## New params key

`witness.azimuth_deg`: absent; tests fail `MISSING: params key witness.azimuth_deg`.

## Where the Loftsman's numbers bind

| Test | Binding |
|---|---|
| glyph sense and span | wing face of each glyph; sense measured from +Z on the face projection; recess at least `nut.arrow_depth`/2 deep; opposite faces of one wing |
| RC6 scale | graduations rise from the rim top (graduation 0 at rim top); count 14 at pitch 1.0; scale tab height at least `holder.stroke_gap_R`; a scale below the rim fails |
| HD7 tick | tick reference at flange underside; groove or ridge on the flange rim, read at `witness.azimuth_deg` |
| HD5 annulus | r from `holder.insert_circle_radius` + insert radius + 0.5 to `holder.flange_od`/2 - `holder.index_notch_depth` - 0.5 |
| HD6 | downward planar faces of the holder only at holder bottom and flange underside |
| BS3 flip | slot pattern asymmetry above `FLIP_FLOOR` |
| FR4 | notch on one rail above `FLIP_FLOOR` |
| ST1 | pad face centre z = `stop.height_z` in the stop's own frame |
| NT9 | window, if ruled, does not alter glyph tests |

## Findings

- Footprint 644 x 608 requires rails at 644 and end members 488 plus two 60 mm rails; plate_support placement (open item B) does not change it.
- Controls: deleted row, empty result, plain-disc flip, reversed glyph, tick off 1 mm, 650 mm cut, 3 rails, 127 T-nuts, flange hole, extra downward face, missing params key.
- P7 scans test files for params keys; a control key is built from fragments to stay outside the scan.
