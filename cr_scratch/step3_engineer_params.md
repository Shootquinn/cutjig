## Result

params.yaml: 193 to 288 leaves. 96 keys added (95 new, 1 rename). Tests: red 126 failed, 71 passed; green 197 passed (65 existing, 132 new). Runs: `cr_scratch\step3_red_run.txt`, `step3_green_run.txt`.

## 119.84 recomputed

Confirmed 119.84, by a different route than the Designer's. Floor frame: holder bottom in R 13.626, minus the drop to core d + 1.0 (13.126 - 8.59 = 4.536), plus holder 88, flange 8, nut plate 8, plus collar 6.75 = 119.84. The 40 added is `icd.floor_above_datum_a`, not the wing height. Result 159.84, as the Designer has it. Pose R (164.38) is unclamped.

Designer error: `stop.collar_top_z_min` 148.21 is wrong, because it subtracts the R-to-K-max drop. K-max is 112.75 + 40 = 152.75 (159.84 - 7.09). I used 152.75.

## Changed values

- stop.g_stop 10 to 25 (ASSUMED, ISO 13854 Table 1 secondary)
- core.min_exposed 128.12 to 143.12 (136.369 + 6.75)
- stop.collar_top_z 150 to 159.84; stop.height_z and icd.stop_height 160 to 184.84
- stop.height_range [160, 300] to [184.84, 315] (315 is the old 300 seed + 15, now ASSUMED); stop.start_z to [684.84, 815]
- upper.park_z 950 to 959.84; park_stroke 780 to 775
- hardware.tnuts_per_bracket 2 to 8; tnut_sku 13098, tnut_sku_alt "40-3914, unverified"
- hardware.printed_bracket: 7.0 mm slots, 29.2 pitch, now VERIFIED

`tnuts_per_bracket` is 8 by assumption: Zoro lists 14089 as 8-hole, and the printed bracket is assumed the same. T-nut BOM goes from 44 to 150. `bracket_sku` stays ASSUMED (403). `tnut_fit_30series` is ASSUMED, with limits head 16.0 and neck 7.7 in `tnut.*`.

## Keys added

- thread: lead_in_length, land_width
- receiver: register_bore_radius, register_depth, key_slot_width, key_slot_depth, key_offset_deg, spigot_od
- holder: flange_thickness, key_width, key_height
- nut: washer_pocket_od, washer_pocket_depth, arrow_length, arrow_depth, tommy_hole_dia, tommy_hole_count, tommy_hole_depth, tommy_bar_length, release_marker, release_dead_turn_deg, washer_window_count, washer_window_width
- washer.retention; loads: nut_torque_abuse, hand_force_bar
- wingnut: wing_count, wing_height, wing_root_width, wing_tip_width, wing_thickness, edge_radius, knuckle_clearance, sweep_clear_radius, turns_to_clamp
- collet: relief_hole_dia, foot_ring_width, core_seat_height, core_seat_width, rim_notch_count, rim_notch_width, rim_notch_depth, label_text_format, label_height, label_depth, file_name_pattern, chamfer_lead_in, chamfer_floor, bore_lip_radius, colour
- witness: zone_high, scale_pitch, wrong_collet_band_low, wrong_collet_band_high, step_per_family
- rest: roller_dia, arm_length, swing_clear_radius, close_handle_length, hold_open_detent, height_rule
- access: key_sector_deg, key_arm_length, head_clear_radius; bracket.face
- bolt_down: method, count, floor_fastener, head_access
- base: plate_thickness, spigot_hole_dia, slot_width, slot_length
- tray: length, width, depth, lip_z, drain_dia, floor_slope_deg, drain_plug
- caddy: socket_clear, socket_depth; gauge: register_plug_dia, length
- tnut: head_width_max, neck_width_max
- strength.tensile_design (rename); upper.load_clearance; stop: collar_top_z_min, pad_width, pad_length
- hardware: adjust_interface, tnut_fit_30series, printed_bracket_file, printed_bracket_slot_width, printed_bracket_slot_pitch

## Merged, not added

Nine Designer keys duplicated existing ones: collet foot_key_* and foot_ring_height, nut.bearing_face_id, base.plate_length and plate_width, caddy.socket_count, witness.zone_low, stop.collar_top_z_max, stop.floor_z, stop.travel_limit_z. A test confirms they are absent. `core.diameters` is still the only list of the seven diameters.

## Designer items changed

- `collet.core_stop_*` is renamed `core_seat_*`: P10 bans "stop" in base-side key names, and this is the core weight seat.
- `base.spigot_hole_dia` is spigot_od + 0.40, not 0.20 (the chain entry is radial). `receiver.spigot_od` 160 is my seed, because the Designer gave no value.
- `receiver.register_bore_radius` is DERIVED (134.58 / 2), not ASSUMED.
- `tray.lip_z` and `rest.height_rule` are rule strings; the wing underside z is unknown.

## Files edited

- params.yaml; tests/test_params_bom.py (P10 frozen values updated to the g_stop 25 numbers).
- build_parts/bom_tools.py line 150 (T-nut note). bom_purchased.md and report_assumptions.md are regenerated.
- reference/vendor_sources.md: lines 12 and 13 edited, 3 rows added after line 13, and the line 15 text replaced.
- ASSEMBLY.md: lines 30, 31, 69 (25.0), 99 (25).
- gameplan.md: lines 117, 168, 205, 223, 348, 398, 412, 543, 560, 611, 627, 628, 641, 643, 645, 646, 650, 692, 698, 705, 706. Unchanged and still true: 301, 613, 658, 805.

`common.py` and `_PRINTER_KEY` are unchanged; a test checks both.
