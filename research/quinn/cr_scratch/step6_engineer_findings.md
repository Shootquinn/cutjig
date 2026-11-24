## Corrections to the brief

| # | Brief or test says | Measured | Tag |
|---|---|---|---|
| E1 | FR4 notch removes 720 mm3 | 709.5: the notch edge y 249 breaks 0.5 mm into the profile corner pocket (y 245.3 to 249.5) | MEASURED |
| E2 | Printed outer bracket enters the end member by 3,192 mm3 per site | 1,061.4 per site (hollow section); purchased inboard against printed outer 18,248.6 per site, 72,994 over four | MEASURED |
| E3 | Probe rim top is 88.5 | Probe radius 73.79 sits on the lead-in chamfer: reads 88.25 at azimuth 247. Flat rim top is 88.5 | MEASURED |
| E4 | Glyph principal span 6.0 | 5.01 on the 0.5 grid (tip and tail sample at zero width); modelled 6.0 | MEASURED |
| E5 | Skirt to tray 58 | 58 is skirt bottom to tray rim plane. Solid-to-solid minimum is 66.7 | MEASURED |
| E6 | 14089 volume 32,919; STL 57,203 | Proxy 35,294 (+7.2 percent: no gusset, no fillets); printed proxy 47,944 (-16 percent) | MEASURED |
| E7 | Column notch "70 x 65 at x +-35" | Read as one notch per long edge, x -35 to +35. Two notches centred at +-35 would join into 140 | DECLARED |
| E8 | ST1 pad 60 x 60 x 12 | Two Ø6.6 holes at x +-15 added: `data71_errors` rejects a part with no boolean | DECLARED |
| E9 | Ruler cut after the thread stud | Unorientable shape (receiver `isValid` false). Key slot and ruler cut first, stud second: valid | MEASURED |

## Checklist table

Result-JSON row = first row with that id; volume in mm3.

| IDs | Status | Row |
|---|---|---|
| RC1-RC5, HD1-HD4, WS1-WS3, CO1-CO8, NT1-NT3, NT6, NT8 | PASS | existing Step 3-5 feature rows, unchanged (nut and receiver rows re-pass) |
| RC6 / AC4 | PASS | receiver RC6, 13 rows, 550.9 |
| HD5, HD6 | PASS by absence | holder: no annulus hole, downward faces only z 0 and 88 (evidence log); tests red, see Design issues |
| HD7 / AC5 | PASS | holder HD7, 5 rows, 6.0 |
| NT4, NT5 | PASS | nut NT4, NT5, 10.2 each; senses -1 and +1, wing 0 faces +z and -z |
| NT7 | PASS | nut NT7, 36,437.7 |
| NT9 | PASS by ruling | no window (Loftsman C1, C2) |
| BS1-BS4 | PASS | base 4,698,624; 248,853; 12,431; 110,912 |
| BS5, BS6 | PASS | tray 7,280,000; 12,272; plug 17,593 |
| BS7 | PASS | foot 48,000 |
| FR1-FR4 | PASS | frame 2,930,129; 665,902; 177,120; 709.5 |
| FR2, FR3 parts | PASS | bracket_purchased 36,936; bracket_printed 51,471; tnut 1,384 |
| AC1, AC2, AC3, ST1 | PASS | caddy; gauge; rest; stop 43,200 |

## Rebuild list

| File | Reason | Volume before to after | Faces before to after |
|---|---|---|---|
| receiver | RC6, AC4 | 955,903.8 to 955,593.2 | 91 to 195 (V-E+F 4 to 20) |
| holder | HD7, AC5 | 407,847.2 to 407,841.2 | 24 to 28 (8 to 8) |
| nut | NT4, NT5, NT7 | 322,243.8 to 358,724.8 | 183 to 195 (8 to 10) |

Mtimes: only these three FCStd and their JSON differ from `step6_fcstd_mtimes_before.txt`. Washer, footring, frame_profiles, 27 collet files and `step3_cross_checks.json` are untouched.

## Builds

Logs `research\quinn\cr_scratch\step6_build_<part>.log`; all end `BUILD_DONE`.

| Part | PID | Start | run_seconds |
|---|---|---|---|
| receiver | 4364 | 02:50:33 | 98.3 |
| nut | 36108 | 02:58:40 | 94.0 |
| frame | 30800 | 02:50:45 | 12.0 |
| rest | 22720 | 02:50:41 | 3.3 |
| base, tray, plug, foot, tnut, bracket, caddy, gauge, stop, holder | in logs | 02:50 to 02:52 | 0.3 to 0.8 |

Params leaf count 332 to 429 (97 new keys, each with source and status, rows added to `report_assumptions.md`; P-group 213 of 213 pass).

7.1 data per part is in each result JSON. Face growth: base 6 to 63 (V-E+F 5), tray 6 to 26 (0), plug 9 to 7 (4), foot 6 to 9 (2), caddy 6 to 55 (16), rest 48 to 52 then 47 to 51. All match the Topologist record. Plain versus optimal bbox: 0.000 on every new part; 3.600 on receiver and nut (helicoid control points).

## Test counts

Collected 582 (540 at B6 plus 42 Step 6). Passed 399: all 364 B6 passes still pass, 35 new. Failed 183: MISSING 175, ABSENT FEATURE 2, assertion 6. By file: assembly 134, exports 31, thread_clamp 11, step6 7. Every remaining non-step6 failure is MISSING and green_at 7 or later.

green_at_6: 33 collected, 26 pass, 7 fail: HD5, HD6, NT4_NT5 (two), RC6, HD7 (two). All seven trace to probe windows (D1 to D3), not to built geometry.

The rebuild made the Step 3 and 4 probes stale (20 tests read "older than its input"); `probe_step3_parts`, `probe_thread`, `probe_thread_mesh`, `probe_tilt`, `probe_step6_parts` and `probe_step6_marks` were rerun on the final files. `probe_step6_marks` takes 3,211.8 s (PID 32564, `results\probes\step6_marks.json`).

## Pass 1 data

- Stock: rail 644, end 488, plate_support 468, two each, whole pieces, 0 left; 1540 (4), 980 (4), 952 (1), 728 (2) untouched. Frame 8.234 kg at 2.573 kg/m.
- Printed volume, base side (base, tray, plug, 4 feet, 8 printed brackets): 7,843 cm3, 9.8 kg at 1.25 g/cm3 (findings assumption, no key).
- Counts: 16 brackets (8 and 8), 128 T-nuts, 8 per bracket. T-nut against host profile: 0.0 mm3 at all eight sampled sites; 16 T-nut pairs overlap at the four C6 sites, 16,523 mm3.
- 80/20 CAD on disk and read in place: 30-6060 STEP, 14089 STEP, printed STL and 3mf. Missing: PZRT 3030 T-nut (proxy built).
- Clearances: receiver to base plate hole 0.20, to tray hole 1.20. Nut at K-max to tray 66.7. Caddy socket Ø146.08 against collet Ø133.98: 6.05 per side, 8 deep spare. Purchased outboard bracket ends 3 mm inside the rail end.
- Rest, closed pose: rollers clear d 90 to 97.5, touch at 100, interfere 895 mm3 at 102.5 and 2,526 mm3 at 105. Tower inboard face r 84 sits 2.2 inside the 86.2 keepout; rest ring is inside the keepout by function.

## Design issues

| # | Issue | Disposition |
|---|---|---|
| D1 | `probe_step6_parts` HD5 annulus r 65.0 to 68.54 crosses the key (az 33, 36, 39 read 2 intervals). HD6 `flange_interval` is read at r 66.77, inside the tube wall: interval (0, 104.75), so flange underside 88 reads as an extra face | Test defect, Manager. Edit: skip the key sector; read the interval at r 69.54. Corrected predicates pass (`step6_evidence_hd56.log`) |
| D2 | `probe_step6_marks` rim radius `thread.major/2 - 1` sits on the lead-in chamfer: rim top reads 88.25 (flat rim 88.5). RC6 reads graduation 0 at 48.475 against wanted 48.250; HD7 reads 1.275 and 8.365 against 1.5 and 8.59 | Test defect, Manager. Edit: radius `thread.minor/2 - 1` |
| D3 | `probe_step6_marks` glyph window starts at r 86.14, inside the dust skirt (r 95.14): skirt surfaces read as voids. Sense -1 count 3 (wing 0 +y, wing 1 -y, wing 1 +z), sense +1 count 4; wing 0 +z span 45.5 | Test defect, Manager. Edit: start at `nut.skirt_r_out + 0.5`. With D2 and D3 patched (probe copy in cr_scratch) every RC6, HD7, NT4, NT5 predicate passes: readings 1.525 and 8.615, spans 5.01 |
| D4 | C6 bracket overlap, 16 brackets | Input to Step 7, owner Engineer: cut brackets or lengthen rails |
| D5 | Rollers at r 70 fit d 100 only | Input to Step 9, owner Engineer: linkage radius |
| D6 | Receiver BOP check keeps Step 4 InvalidCurveOnSurface edges | Input to Step 10 |
| D7 | Purchased and printed bracket proxies carry no gusset or fillets | Closed by assumption, Pass 1 |

## Fix pass

Params leaf count 429 to 444 (16 new, `tray.ramp_x` removed); `report_assumptions.md` rows and counts line updated; literal scan 0 hits. New keys: `witness.index_face_nut_z`, `nut.release_shaft_width` 0.7, `nut.release_head_width` 3.0, `nut.release_head_length` 4.0, `rest.pose_core_d`, `rest.roller_r_range`, `rest.core_d_range`, `rest.slot_clear`, `rest.slot_depth`, `tray.cross_fall_deg`, `tray.drain_spot_r`, `tray.fall_x`, `plug.lug_length`, `plug.lug_width`, `plug.lug_height`, `plug.lug_embed`. Changed: `nut.glyph_length` 10, `shaft_width` 2.7, `head_width` 8.3, `head_length` 5.8, `rest.ring` [58, 100, 8], `rest.roller_r` 70.005, `tray.floor_slope_deg` 2.0.

### Corrections

| Item | Measured | Tag |
|---|---|---|
| `probe_step6_marks` column median | Glyph covers 21 of 29 wing samples; median sits on the glyph floor, span reads 7.14. `measure_glyph` now uses the unrecessed face level of each column: span 9.04 | MEASURED |
| NT8 arrow | Shaft 0.7 is narrower than the 0.8 mark line at the key azimuth | DECLARED |
| Collet check | Rollers tested against a Ø d core cylinder per size; collets sit below the roller plane, not tested | DECLARED |

### Rebuild list (against `step6_fcstd_mtimes_before.txt`)

Only these seven FCStd and JSON are newer; every other file is unchanged. Volume mm3 and faces, first pass to now.

| File | Reason | Volume | Faces |
|---|---|---|---|
| nut | D3, D1 key | 358,724.8 to 358,837.8 | 195 to 195 (euler 10) |
| rest | D2 | 536,079.6 to 544,617.0 | 51 to 66 (13 to 16) |
| tray | D5 | 2,924,392.9 to 3,051,605.8 | 26 to 29 (0 to 2) |
| plug | D6 | 20,874.3 to 23,594.3 | 7 to 12 (4 to 5) |
| base, foot, frame | cleanup | unchanged | unchanged |

### Builds

| Part | PID | Start | run_seconds |
|---|---|---|---|
| nut | 16828 (run 1 32636 failed the span row) | 04:18:26 | 95.6 |
| rest | 34932 | 04:15:48 | 6.9 |
| tray | 7540 (run 1 34572 failed one row) | 04:16:41 | 0.2 |
| plug, base, foot | 35360, 26444, 18876 | 04:15:48 | 0.1 to 0.4 |
| frame | 6404 | 04:15:48 | 12.5 |

All end `BUILD_DONE`. Booleans: rest 3 (slot cut on the ring primitive, fuse, detent cut), tray 3 (cavity common, tool fuse, cut), plug 1. Plain equals optimal bbox on all but nut (z -3.6 helicoid control points, as before).

### Results

- D2: roller radius follows the core; each size has radial pin slots in the ring (18.76 x 11, 3 deep, inner wall 1.25). Every size: 1 solid, valid, plane y 244, faces 66, euler 16, common volume with the Ø d core 0.0, roller to core gap 0.005. Roller to arm: 12.17 (88.5), 11.97, 11.66, 11.40, 11.19, 11.03, 10.92, 10.85, 10.84 (106).
- D3: NT4 recess 35.41 mm2, NT8 34.37 (ratio 0.97). NT4 and NT5 sense -1 and +1, span 9.04 against 10.0 (tolerance 1.5). Glyph centre x 102.32.
- D5: floor top above plate 18.68 at +X wall, 6.67 at -X wall, 11.97 at the +Y wall at x -172; slopes 2.0 deg east, west and cross; spot face flat at 3.0 inside r 20.
- D6: lug 34 x 8 x 10, overall height 29, corner inside the head.
- D1: witness pose uses nut z 0 at the edge. Ruler unchanged.

### Cleanup

`tray.py` cavity-depth row and `plug.py` gap row now measure (distance to a bore-wall tube). Removed `sl_pos`, `cxp`, five dead `step6lib` helpers. Foot, FR4 and T-nut sample names derive from params.

### Renders

104 PNGs (101 plus `rest_bottom`, `rest_slot_closeup`, `tray_cross_section`). Re-rendered: all `witness_*`, `nut_*`, `rest_*`, `tray_*`, `plug_*`, `base_tray_*`. `INDEX.md` updated. Script: `research\quinn\cr_scratch\step6_render_fixpass.py`.

### Test counts

Probes rerun: `step6_parts`, `step3_parts`, `thread`, `thread_mesh`, `tilt`. `test_step6_parts.py`: 37 pass, 7 fail (six read the stale `step6_marks.json` from the old nut; `test_loftsman_params_keys_present_before_the_builds` requires `tray.ramp_x`). Full suite: 584 collected, 400 pass, 184 fail (assembly 134, exports 31, thread_clamp 11, step6 7, params_bom 1: `test_P15_key_present[tray.floor_slope_deg]` pins 3). Software Engineer updates the P15 pin, the `ramp_x` key list and the ray-cast witness probe.

## Rest vs collet probe

Step 6 close criterion 10. Probe `research/quinn/cr_scratch/probe_step6_rest_collet.py` (freecadcmd, 32.7 s, PROBE_DONE), output `results\probes\step6_rest_collet.json`, log `research\quinn\cr_scratch\step6_rest_collet.log`.

Setup: floor frame, collet z 0 to 32 on the receiver floor seat. Rest from `rest.shape_at(p, core_d)` with rollers at that core's radius, roller plane at each `rest.height_positions` (310 and 560). Core cylinder z 0 to roller plane + 190. Collets: all nine tags (090p0 to 105p0 including 093p7, 097p0); poses R (core d, free collet), K d+1 (core d + 1.0, `_clamped_Kd1`), K-max (core d - 1.5, `_clamped_Kmax`). 9 x 3 x 2 = 54 rows.

Result: all 54 rest and collet solids valid. Common volume rest-vs-collet 0.0 mm3 in every row. Common volume rest-vs-core 0.0 mm3 in every row. Minimum distance rest-to-core 0.005 mm in every row (roller gap). Minimum distance rest-to-collet 262.0 mm (smallest over all rows; the rest ring sits 280 or more above the collet top at z 32).

No nonzero common volume. No fix made.
