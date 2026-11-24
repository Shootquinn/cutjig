## 1. Feature table (27 MISSING rows; Step 1 counted 24 and under-counted)

Visual gate NOT RUN. Status: A = ASSUMED, D = DERIVED, DEC = DECLARED. Units mm. R1 to R3 reviewed below; none reopens a finding.

| Feature | Current key | Verdict | Key = seed (status; basis) |
|---|---|---|---|
| Receiver thread lead-in, land | none | KEY | `thread.lead_in_length` = 8 (A; one pitch); `thread.land_width` = 1.0 (A; pitch/8) |
| Receiver register | `register.g_reg` fit only | KEY | `receiver.register_bore_radius` = 67.29 (A; datum B text); `receiver.register_depth` = 24 (A; 3 pitches, pilots before thread starts) |
| Receiver asymmetric key slot | none | KEY | `receiver.key_slot_width` = 12, `_depth` = 6, `receiver.key_offset_deg` = 37 (A; off-diametral so one orientation fits) |
| Holder flange | `holder.flange_od` | KEY | `holder.flange_thickness` = 8 (A) |
| Bearing recess | `washer.*` | KEY | `nut.washer_pocket_od` = 143.8 (D; washer.od + 2 x fit.seat_clearance); `nut.washer_pocket_depth` = 0.8 (A; washer stands 0.5 proud) |
| Holder key | none | KEY | `holder.key_width` = 11.4 (D; slot 12 - 2 x fit.seat_clearance), `holder.key_height` = 5 (A) |
| Jacking holes | deleted by concept | ADEQUATE | Retired: captive flange and collar back-off lift (decision 2) |
| Hard-stop face | `stop.*` | KEY | `stop.pad_width` = 60, `stop.pad_length` = 60 (A; column face), contact 3600 mm2 against 1000 N. Holder stop is the collet foot ring (row below) |
| Slit relief holes | none | KEY | `collet.relief_hole_dia` = 3.0 (A; 2 x slit_width_seed) |
| Collet foot key, foot ring | none | KEY | `collet.foot_key_width` = 11.4 (D), `collet.foot_key_height` = 5 (A), `collet.foot_ring_height` = 2.0 (D; holder.bottom_above_floor_Kmax), `collet.foot_ring_width` = 10 (A) |
| Core stop | none | KEY | `collet.core_stop_height` = 4, `collet.core_stop_width` = 3 (A; carries 204 N, leaves bore open) |
| Rim notches | none | KEY | `collet.rim_notch_count` = round((d-90)/2.5)+1, 1 to 7 (D; family index), `collet.rim_notch_width` = 6, `_depth` = 3 (A) |
| Grip-window label | `collet.grip_window_lo/hi` | KEY | `collet.label_text_format` = "d | lo-hi", `collet.label_height` = 8 (A; at least 6 per S2-4), `collet.label_depth` = 0.8 (A); `collet.file_name_pattern` = "collet_{int}p{frac}" (092p5) |
| Lead-in chamfer, lip | `collet.min_wall` | KEY | R3: `collet.chamfer_lead_in` = wall - min_wall, floor `collet.chamfer_floor` = 1.5 at 45 deg (D; 3.8 at d = 105); `collet.bore_lip_radius` = 1.0 (A) |
| Colour per size | none | KEY | `collet.colour` = [red, orange, yellow, green, blue, violet, white] (A); redundant with notch count; a finish, not a printer input |
| Nut bearing face | `washer.*` | KEY | Covered by the pocket keys above; `nut.bearing_face_id` = 136.8 (D; washer.id) |
| Wing planform | `wingnut.span`, `body_od` | KEY | `wingnut.wing_count` = 2, `wingnut.wing_height` = 40, `_root_width` = 40, `_tip_width` = 28, `_thickness` = 14, `wingnut.edge_radius` = 6 (all A; see wing finding) |
| Tighten/loosen arrows | none | KEY | `nut.arrow_length` = 40, `nut.arrow_depth` = 0.8 (A) |
| Tommy-bar socket | none | KEY | `nut.tommy_hole_dia` = 13, `nut.tommy_hole_count` = 4, `nut.tommy_hole_depth` = 20 (A) |
| Dust skirt | `nut.skirt_below_flange` 40 | ADEQUATE | Skirt exists; A3h holds its floor gap at 1 pitch |
| Base plate | `icd.footprint_*` | KEY | `base.plate_length` = 644, `_width` = 608 (D; footprint, soft), `base.plate_thickness` = 12 (A), `base.spigot_hole_dia` = `receiver.spigot_od` + 0.20 (D; chain entry) |
| Debris tray | prose | KEY | `tray.length` = 560, `tray.width` = 520, `tray.depth` = 25, `tray.lip_z` = wing underside - 50 (A/D) |
| Drain | none | KEY | `tray.drain_dia` = 25, `tray.floor_slope_deg` = 3, `tray.drain_plug` = threaded, large knob (A) |
| Slotted holes | count 8 | KEY | `base.slot_width` = 7, `base.slot_length` = 20 (A; M6 clearance, 7 mm as the printed bracket) |
| Feet, bolt-down | prose | KEY | S2-6 keys below |
| Collet caddy | none | KEY | `caddy.socket_count` = 7 (D; len(core.diameters)), `caddy.socket_clear` = 3 per side on collet OD, `caddy.socket_depth` = 40 (A) |
| Alignment gauge | none | KEY | `gauge.register_plug_dia` = 134.08 (D; 2 x 67.29 - 2 x g_reg), `gauge.length` = 150 (A) |
| Steady rest | `rest.height_positions`, `roller_count`, `centre_repeatability`, `release_tower`, `cam_lug_radius` | KEY | `rest.roller_dia` = 40, `rest.arm_length` = 200, `rest.swing_clear_radius` = 125 (concept), `rest.close_handle_length` = 120, `rest.hold_open_detent` = true (A). Detent rule `rest.height_rule` = L - 190 (D; gives 310, 560, and 810 for the 1 m core) |
| Witness scale | none | KEY | See S2-4 |

Findings on the table.
- Wing finding. Span 230 on a 166.28 body leaves each wing 31.86 proud (D). A 32 x 40 palm face is small for a full-size hand pushing 52 N. Keep the span (it sets the 115 sweep) and seed height 40, with the wing root running along the body as a ridge. If Step 5 finds the grip poor, the span key rises; no cap blocks it.
- R1 to R3 reopen nothing. R1 ring stop is the foot-ring row; the two plate keys and stop pin are covered by `icd.coaxiality_chain`, `base.spigot_hole_dia`, and `base.slot_*`. R2 lug and tower are `rest.*`. R3 is the chamfer row.
- D1: `loads.torque_design` 10, `loads.nut_torque` 12, wings, tommy hole, washer pocket now describe the torque path as parts. D2: stop is `stop.*`, owner upper assembly; nut keys carry no descent load. D3: this table; the stated test (key, tray, drain, core stop, label, wing planform, register, flange recess) now each have keys. D6: release is `nut.lift_play` 0.75 plus `holder.flange_thickness`, collar keys, and `nut.release_marker`; no jacking keys.

## 2. Step 2 ABSORB items

- S2-4 (names only): `witness.zone_low`, `witness.zone_high`, `witness.scale_pitch`, `witness.wrong_collet_band_low`, `witness.wrong_collet_band_high`, `witness.step_per_family` (D; 1.25 / tan 10 = 7.09, matches 8.59 - 1.5). Wrong-collet defence is the notch count, colour, label, caddy socket and this scale.
- S2-5: `wingnut.wing_height` 40 (at least 30), `wingnut.knuckle_clearance` 50, `wingnut.sweep_clear_radius` 115 (D; span/2), `wingnut.turns_to_clamp` 4.45 (D; (24 + 11.6)/8; about 9 regrips at half a turn).
- S2-6: `access.key_sector_deg` 60, `access.key_arm_length` 150, `access.head_clear_radius` 25; `bracket.face` = vertical inside faces; `bolt_down.method` = foot plate 100 x 60 x 8 on two M6 T-nuts at 30 pitch, `bolt_down.count` 4, `bolt_down.floor_fastener` M8, `bolt_down.head_access` = same sector (all A); `hardware.adjust_interface` = T-handle.
- S2-7b: `nut.release_marker` aligned mark plus "keep turning" arrow; dead turn 0.75/8 x 360 = 33.75 deg (D).
- S2-7c: `loads.nut_torque_abuse` 25 (A); `loads.hand_force_bar` 100 N (A); `nut.tommy_bar_length` 300 total, 150 per arm, so a hand gives 15 N m (D). Axial at 25 N m about 0.8 kN by linear scaling of 1.6 kN at 50 N m (mine); the ten-member check at 25 N m runs in Step 5.
- S2-7d: `washer.retention` = snap lip in the nut pocket; `nut.washer_window_count` = 3 radial notches 10 wide, washer in a contrast colour, so absence shows as a bare flange (A).
- S2-8: `stop.collar_top_z_max` = 159.84 (D; 119.84 + 40), `stop.collar_top_z_min` = 148.21 (D; max - 11.626 stroke); `stop.collar_top_z` retired as one value. Also `stop.floor_z` fixed, `stop.travel_limit_z` labelled detents.
- `hardware.tnut_fit_30series`: status stays ASSUMED. Acceptance keys: `tnut.head_width_max` = 16.0 (D; cavity 16.5 - 0.5), `tnut.neck_width_max` = 7.7 (D; opening 8.0 - 0.3). SKU 40-3914 is labelled 40 series, and I found no 30-series statement. A check rejects any bolt-down or strap reliance until the SKU is measured against these limits.

## 3. Finger-crush gap, `stop.g_stop`

- Document: ISO 13854, Safety of machinery, Minimum gaps to avoid crushing of parts of the human body. First edition 1996, second edition 2017 (confirmed 2023), Table 1. Secondary search summaries give finger 25 mm; hand, wrist, fist 100 mm; arm 120; foot 120; body 500. The standard text is not read: the iteh 1996 sample is a scanned image, the ANSI preview returned 403.
- Status: ASSUMED, secondary source named (search summaries of the iteh and ANSI catalogue pages). Not VERIFIED.
- Body part: finger. The gap is a slit open around the nut, below a fixed cutter. A flat adult hand is thicker than 25 mm at the knuckles, so only fingers enter it; hand gap 100 mm does not apply to a slit this thin. Hands are kept off by the 50 mm knuckle clearance below the wings and by the 25 mm slit. At 10 mm a finger fits (adult finger thickness about 15 to 20, mine) and is crushed. So 10 mm does not protect; 25 does.
- Minimum: 25 mm. Recommended `stop.g_stop` = 25.
- Arithmetic: `stop.height_z` = 119.84 + 40 + 25 = 184.84 (confirmed; 169.84 at 10). I take 119.84 from the task statement and cannot re-derive it from params. `core.min_exposed` = 106.369 + 25 + 5 + 6.75 = 143.12 (was 128.12, +15). `stop.collar_top_z` = 159.84 (replaces 150). `stop.height_range` = [184.84, 315]; `stop.start_z` = [684.84, 815]. `upper.park_z` = 159.84 + 750 + 50 = 959.84 (was 950; rule `upper.load_clearance` 50). Working stroke stays 500. The 15 mm costs nothing in the signed limits; the 2 m height is soft.

## 4. Over-constraint check

- No new key carries a printer bed, material, nozzle or part split. Colour is a finish.
- No new key is a hard 2 m limit; `upper.park_z` and `rest.height_rule` now follow core length, so the optional 1 m core is expressed (park 1209.84 by the same rule).
- No hard core-length cap. `upper.travel_max` is a stroke ceiling.
- Existing residue, not new: `friction.*`, `tensile_in_layer` and `collet.web_strain_allow` cite "FDM" in their source text. They are design coefficients; reword the source to "design assumption" and rename `tensile_in_layer` to `strength.tensile_design`.

## 5. Verdict

CONCEPT CHANGE: none. U12 and U13 cover everything above.

PASS
