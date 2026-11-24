## 1. Disposition of the Topologist items

Script `xr.py` in the scratchpad, run with `python -I`. Frame: section 0 of `cr_scratch/step3_topologist_crossreview.md`. Where the two of us disagree, the formula governs.

| Item | Verdict | Formula and deciding number | Winner |
|---|---|---|---|
| W-1 collet strain | MODIFIED | eps = 4 delta / (2 L d_h), delta = pi 3.5 / 12 = 0.9163. The Step 2 check (L 32, d_h 6) gives 0.954, so the coefficient is 4, as in his own S21 line. His corrected set (L 26.0, d_h 6.0) gives **1.175** at coefficient 4; his 0.881 used 3. It fails. Requirement: L d_h >= 4 delta / (2 x 0.01) = 183.26. With ligament 3.0, hole centre = 3.0 + d_h / 2 and L = 32 - centre: d_h 7 gives 1.027 (fails), d_h 8 gives **0.916** (passes). | Formula. His ligament 3.0 stands; hole 8.0, not 6.0. |
| W-2 core seat height | ACCEPTED | Hole bottom z = ligament 3.0 sits 0.5 above the ledge top at 2.5, so there is no tangency. Ledge shear at 204 N on 2 pi x 43 x 2.5 is 0.30 MPa. The S9 margin at d 85 is 0.5 radial (ledge ID r 40.5 against hole r 40.0). | Topologist |
| W-3 T9 | ACCEPTED | Solve L sin t + D cos t = B for t, with D 134.08 and B 134.58. At L = 48.75 - 1.0 rim chamfer = 47.75, t = 0.609 deg. Adding plate rock atan(0.75 / 136.44) = 0.315 gives **0.924** against the 1.021 line. My 0.903 used the small-angle form and ignored the chamfer. The largest g_reg that passes falls from 0.3006 to 0.289, still above the 0.25 seed. | Topologist |
| W-4 foot key top | ACCEPTED | Rule `fit.model_contact_gap`: the foot key top is in the same plane as the ring top, so both sit at z = 2.00 - 0.005. | Topologist |
| W-5 washer pads | ACCEPTED | Overlap = 3 x (theta / 2)(71.6^2 - 71.5^2) x 0.8, theta = 10 / 71.5 rad, gives **2.402 mm3** (0.80 per pad). This matches his 2.40. Class P closes the exemption hole. | Topologist |

## 2. Final numbers

Floor frame z = z_A - 40, values in mm. Basis: D diametral, R radial (per side), A axial, T tangential, deg angle. Each number is stated once. Keys in backticks; "new" marks a key added at this step.

| Part | Key or feature | Basis | Value |
|---|---|---|---|
| Receiver | `thread.major` / `thread.minor` | D | 149.58 / 144.58 |
| Receiver | pitch `thread.pitch`, flank `thread.flank_deg`, hand, starts | A, deg | 8, 45, right, 1 |
| Receiver | crest and root flat `thread.land_width` | A | 1.5 |
| Receiver | rim chamfer `thread.lead_in_length` | A (45 deg, to the pitch line) | 1.25 |
| Receiver | thread run z | A | 40.5 to 88.5 (`receiver.rim_above_floor` 88.5) |
| Receiver | runout land z | A | 36.5 to 40.5 |
| Receiver | shoulder, from `receiver.spigot_od` | D | 160 |
| Receiver | `receiver.register_bore_radius` | R | 67.29 |
| Receiver | `receiver.register_chamfer` (new) | A (45 deg) | 1.0 |
| Receiver | `receiver.register_depth` | A (pilot insertion at first contact) | 48.0 |
| Receiver | `receiver.key_slot_width` / `receiver.key_slot_depth` | T / R | 12 / 3.3 |
| Receiver | `receiver.key_offset_deg` | deg | 37 |
| Receiver | `receiver.floor_hole_dia` (new) | D | 80.0 |
| Holder | outer diameter | D | 134.08 |
| Holder | cone `cone.alpha`, height `chain.H` | deg, A | 10, 30 |
| Holder | inner cone radius at the bottom | R | 62.04 |
| Holder | bore above the cone | D | 113.50 |
| Holder | `holder.length` (bottom to flange underside) | A | 88.0 |
| Holder | `holder.flange_od` / `holder.flange_thickness` | D / A | 144.08 / 8 |
| Holder | `holder.key_width` / `holder.key_height` / `holder.key_length` (new) | T / R / A | 11.75 / 3.0 / 40.0 |
| Holder | `register.g_reg` | R | 0.25 |
| Holder | `register.t9_tilt_deg` (new) | deg | 0.924 |
| Nut | crest / root | D | 145.28 / 150.28 |
| Nut | `fit.c_r` / `fit.g_a` | R / A | 0.35 / 0.30 |
| Nut | `thread.nut_lead_in_length` (new) | A (45 deg) | 0.9 |
| Nut | `nut.length` / `nut.skirt_below_flange` | A | 48 / 40.0 |
| Nut | `nut.plate_thickness` (new) / `nut.overall_height` (new) | A | 7.5 / 56.0 |
| Nut | `wingnut.body_od` | D | 166.28 |
| Nut | `nut.washer_pocket_od` / `nut.washer_pocket_depth` | D / A | 143.8 / 0.8 |
| Nut | `nut.pad_count` / `nut.pad_arc` / `nut.pad_height` / `nut.pad_id` (all new) | -, T, A, D | 3 / 10.0 / 0.8 / 143.0 |
| Nut | `nut.tab_width` (new) | T | 5.0 |
| Nut | `nut.washer_window_count` / `nut.washer_window_width` | -, T | 3 / 10 |
| Nut | wings: `wingnut.wing_root_width` / `wingnut.wing_tip_width` / `wingnut.wing_thickness` / `wingnut.edge_radius` | A, A, T, R | 40 / 28 / 14 / 6 |
| Nut | `wingnut.span` | D | 230 |
| Nut | `nut.tommy_boss_od` (new) / `nut.tommy_hole_dia` / `nut.tommy_hole_depth` | D / D / R | 23 / 13 / 20 |
| Nut | `nut.tommy_grip_radius` (new) / `nut.tommy_bar_length` | R / length | 150 / 122 |
| Nut | `nut.release_dead_turn_deg` | deg | 33.75 |
| Washer | `washer.id` / `washer.od` / `washer.thickness` | D / D / A | 136.8 / 143.2 / 1.3 |
| Washer | `washer.notch_width` / `washer.notch_depth` (new) | T / R | 6.0 / 2.0 |
| Collet foot ring | height `holder.bottom_above_floor_Kmax` | A | 2.0 |
| Collet foot ring | `collet.foot_ring_width` (lip beyond the cone base) | R | 3.2 |
| Collet foot ring | `collet.core_seat_height` / `collet.core_seat_width` | A / R | 2.5 / 3 |
| Collet foot ring | foot key (width from `holder.key_width`) | R extent | r 66.99 to 70.04 |
| Collet slits | `collet.slit_count` / `collet.slit_width_seed` | -, T | 12 / 1.5 |
| Collet slits | `collet.slit_ligament` (new) / `collet.slit_length` (new) | A | 3.0 / 25.0 |
| Collet slits | `collet.relief_hole_dia` | D | 8.0 |
| Collet slits | relief hole centres z | A | 7.0 (top-open slits) and 25.0 (bottom-open slits) |
| Collet bore | lead-in chamfer `collet.chamfer_lead_in` | A (45 deg) | min(wall - 1.2, 10.5); 2.5 where wall - 1.2 lies in (2.5, 3.5) |
| Collet slits | slit overlap | A | 18.0 |
| Collet slits | strain / `collet.web_strain_allow` | ratio | 0.916 design value (conservative); Topologist reading 0.592 exists; physical collet test decides |
| Collet slits | slit phase | deg | theta_key + 15 + 30k |
| All C pairs | `fit.model_contact_gap` (new) | normal | 0.005 |

## 3. Registry rows to fill

params.yaml values changed (12): `thread.lead_in_length`, `thread.land_width`, `receiver.register_depth`, `receiver.key_slot_depth`, `holder.key_width`, `holder.key_height`, `collet.foot_ring_width`, `collet.core_seat_height`, `collet.relief_hole_dia`, `nut.tommy_bar_length`, `washer.retention`, `collar.id` (110.0).

params.yaml keys added (19): `thread.nut_lead_in_length`, `receiver.register_chamfer`, `receiver.floor_hole_dia`, `holder.key_length`, `collet.slit_ligament`, `collet.slit_length`, `nut.plate_thickness`, `nut.overall_height`, `nut.tommy_boss_od`, `nut.tommy_grip_radius`, `nut.pad_count`, `nut.pad_arc`, `nut.pad_height`, `nut.pad_id`, `nut.tab_width`, `washer.notch_width`, `washer.notch_depth`, `fit.model_contact_gap`, `register.t9_tilt_deg`.

Every changed and added key has a source and a status. `report_assumptions.md` was regenerated (`build_parts/bom_tools.py`: 307 leaves). In `tests/test_params_bom.py`, 11 frozen rows were updated, and the P18 tommy test now reads hand force x `nut.tommy_grip_radius`. Result: **197 passed**.

gameplan.md Echo Site Registry rows touched:
- line 687, Thread: add the lead-in and crest flat (keys above).
- line 689, Slits: add ligament, slit length, relief hole and strain ratio (keys above).
- line 690, Engagement: the pose R full-form engagement, 24.72 against 24.
- line 702, Washer: add the notch, and pads class P.
- line 704, Collar: OD / ID / top becomes 152.4 / 110.0 / 6.75.
- new row: T9 tilt, `register.t9_tilt_deg`.

ASSEMBLY.md line 7: it states two origins (base plate top face, and datum A at z = 0). Replace with: "Right-handed. z_A is measured up from datum A (frame top plane, base plate underside). The origin is on datum B (receiver register bore axis, +Z). +X runs along slot line C (plate keys). theta is counter-clockwise from +X seen from +Z; theta_key = 37 deg. Floor frame z = z_A - `icd.floor_above_datum_a`. Datum C: a frame slot line with two plate keys and an end-member stop pin. Units mm. Rule M, Rule P, and slit phase theta_key + 15 + 30k."

Not done here: gameplan.md and ASSEMBLY.md are not edited. The rows above are for the Engineer to apply.

Grep check: I searched this file for every changed and added value. Each one appears in one unit basis only. Where a value repeats, it is the section 1 derivation pointing at the section 2 table row, in the same unit.

## 4. LOFTSMAN SIGNATURE

**SIGNED.** This covers thread, cone, seat, register, slits, the clamped-state solid, the nut and the stop height (`stop.collar_top_z` and `stop.height_z` unchanged). One note, not a withhold: W-1 is MODIFIED (section 1). The Topologist countersigns the relief hole once he confirms the strain coefficient is 4.

Word count, with table pipes not counted: 1,240 (cap 2,000).

## TOPOLOGIST SIGNATURE

Script `sig.py`, `python -I`. Line numbers refer to `cr_scratch/step3_geometry_crossreview.md`.

Confirmed:
- W-2: line 60, seat 2.5.
- W-3: line 40, T9 0.924; lines 28, 36, 39 read 48.0, 88.0, 0.25.
- W-4: lines 10 and 69, key and ring top 1.995, gap 0.005.
- W-5: lines 48 and 11, pads 3 / 10.0 / 0.8 / 143.0, 2.402 mm3, class P.
- Lines 29, 30, 38, 57: 12 / 3.3, 37 deg, 11.75 / 3.0 / 40.0, 6.0 / 2.0.
- Lines 62 to 68: 12 slits, ligament 3.0, hole 8.0, centres 7.0 and 25.0, phase theta_key + 15 + 30k.

W-1 coefficient: h_w is `collet.web_height`, the ligament. Step 2 had L_c = h_w + h_s = 4 + 32, with h_s measured to the hole's far edge (centre 29, diameter 6). The check 4 x 0.9163 / (2 x 32 x 6) = 0.954 reproduces. Final geometry: h_w 3.0, h_s 29.0, l_h 8.0, strain **0.592**. The Loftsman's 0.916 used h_w 4 and h_s to the hole centre. My 0.881 also measured to the centre; read consistently, the 6.0 hole gives 0.790. Both readings pass with the 8.0 hole; the geometry stands.

Tangency, 8.0 hole:
- Top hole z 3.0 to 11.0: 0.5 over the 2.5 ledge, 1.0 over the ring top. Clear.
- Bottom hole z 21.0 to 29.0, ligament 3.0.
- Slit ends cross the hole circle 3.93 from its centre (1.5 against 8.0): transverse, clear.
- New: the bore chamfer edge sits at z = 32 - c, c = wall - 1.2. It meets the hole bottom (21.0) at d 90.6 and sits 0.0075 below the hole top (29.0) at d 106.585.

WITHHELD.

- Line 67: 0.916 -> 0.592.
- Line 65: chamfer edge meets hole bottom 21.0 at d 90.6 and is 0.0075 from hole top 29.0 at d 106.585 -> c = min(wall - 1.2, 10.5), and 2.5 where wall - 1.2 lies in (2.5, 3.5); the edge then clears both by at least 0.5 for d 85 to 106.585.

## Ruling and final edits

Orchestrator ruling applied.

- Strain (line 67): the geometry stands (ligament 3.0, hole 8.0, slit 25.0). 0.916 is recorded as the design value. The Topologist's reading of 0.592 is noted, and the physical collet test decides between them.
- Lead-in chamfer (new row after line 65): the Topologist's fix is accepted. Chamfer edge z = 32 - c, where c = min(wall - 1.2, 10.5), set to 2.5 where wall - 1.2 lies in (2.5, 3.5). Script `ch.py` (`python -I`) swept d from 85 to 106.585 in 0.001 steps. Minimum clearance of the edge to the hole tangent levels (z 3.0, 11.0, 21.0, 29.0) is 0.5. At d 90.6: c 10.5, edge z 21.5, 0.5 above the hole bottom. At d 106.585: wall - 1.2 = 3.0075, so c 2.5, edge z 29.5, 0.5 above the hole top.
- params.yaml: `collet.chamfer_lead_in` is set to this rule, with source and status DERIVED. The frozen test row was updated and `report_assumptions.md` regenerated. `python -m pytest tests/test_params_bom.py -q`: **197 passed**.
