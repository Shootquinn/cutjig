# Step 1.4 P3b, The Loftsman: S4 spec sign-off (arithmetic, placement), S1 r9 / S3 r8 holder rows

Verdict: **NOT SIGNED. FIX 5** (FIX 1 to 4 placement and section coordinates, FIX 5 a printed slice count). Every stack height, the holder section, the spigot fit, the 100 mm core and the minimum core length match by hand. The Engineer's stack hand check holds to 0.01. O2, O5 and O8 are ruled in section 5.

## Corrections to the brief

1. **The wing nut is not axisymmetric, and its true section depends on the plane.** `build_parts/nut.py` cuts three washer windows at theta 90, 210, 330 (`180 / wingnut.wing_count + 360 / nut.washer_window_count * k`). The 90 window lies on the section_yz plane (u = +Y). The wings at 0 and 180 lie on the S1 side_xz plane. A `section_true` compared for equality across S1 (xz) and S3/S4 (yz) is valid only for the revolve profile (FIX 2, ruling O2).
2. **The S4 wing-nut section omits two revolve features of nut.py**: the relief bore r 75.34 over z_R 42.0 to 48.5 (FIX 3), and the skirt profile, which is a rim plus a slope and not a rectangle (FIX 4). Designer 1.4 (a) section 2 row wingnut has the same omissions.
3. **The advance count "0.75 m core: sliceable 496.29, 6 slices" has a fencepost error.** 496.29 is the span of tip positions between the first and last cut. That span gives 6 intervals, which is 7 cuts. The core removed is 572.73 on the axis, and the stub left on the stop after the last cut is 177.27 (axis). 253.71 is the least core that can take a cut on the stop, which is a different quantity (FIX 5).
4. **The staged X1 run needs the live s2.** `research/sean/cr_scratch/step1.4_p6_staged/` holds s1, s3 and s4 only. X1 on that folder alone compares 28 rows. With the live s2_spec.yaml added it compares 70 rows and passes (MEASURED, `p3b/x1dry2.py`). The Engineer's 70 came from his scratch staged folder, which includes s2. S2 carries none of the base rows, so the result stands.

## 1 Hand values beside the code values

Code values come from `check_stack.evaluate_spec` and `check_stack.eval_expr` on the live s4_spec.yaml (MEASURED, `D:\Unleashed Robotics\_scratch\cutjig\open14\p3b\code_vals.json`). Hand values are computed from the params and overlay leaves (DERIVED; tan 10 deg = 0.176327).

### 1a Stack (z_A)

| Item | Hand arithmetic | Hand | Code | Diff |
|---|---|---|---|---|
| Collar top, test_P18 | 40 + 13.626 - (13.126 - 8.59) + 88 + 8 + 8 + 6.75 | 159.84 | S4-1 formula 159.84; collar_top_z_A 159.84; collar z_max 159.84 | 0.00 |
| Collar top, holder.py | 49.09 + z_top 104.75 (88 + 8 + 0.50 + 7.50 + 0.75) + collar.thickness 6.0 | 159.84 | 159.84 | 0.00 |
| Holder bottom | 40 + 13.626 - 4.536 | 49.09 | 49.09 | 0.00 |
| Flange | 49.09 + 88; + 8 | 137.09 to 145.09 | flange piece 137.09 to 145.09 | 0.00 |
| Washer | 145.09 to 145.09 + 1.30 | 145.09 to 146.39 | 145.09 to 146.39 | 0.00 |
| Nut-plate top | 145.09 + (1.30 - 0.80) + 7.50; = 159.84 - 6.75 | 153.09 | wingnut z_max 153.09 | 0.00 |
| Wing-nut bottom | 153.09 - 56.0 | 97.09 | 97.09 | 0.00 |
| Tube top / collar underside | 153.09 + nut.lift_play 0.75; = 159.84 - 6.0 | 153.84 | neck z_hi 153.84; collar ring z_lo 153.84 | 0.00 |
| Receiver floor | icd.floor_above_datum_a | 40.00 | floor piece z_hi 40.00; collet z_min 40.00 | 0.00 |
| Core stop | 40 + 2.5 | 42.50 | core_seat z_max 42.50 | 0.00 |
| 100 mm core top on the carrier | 42.50 + 160 + 100 | 302.50 | core_100 z_max 302.50 | 0.00 |
| 100 mm core top on the stop | 42.50 + 100; 159.84 - 142.50 = 17.34 below the collar top | 142.50 | reported 142.50 | 0.00 |
| Exposure | 302.50 - 153.09; 142.50 - 153.09 | 149.41 (margin 6.29); -10.59 | expected 149.41 / 6.29 | 0.00 |
| Minimum core on the stop (nut-plate datum, detail 1.4 and Designer section 9) | 153.09 + 143.12 - 42.50 | 253.71 (260.46 collar datum) | reported 253.71 / 260.46 | 0.00 |
| Minimum core top line | 153.09 + 143.119 = 291.209 + 5 | 296.21 | line_min_core 296.21 | 0.00 |
| Kerf centre at the stop | 184.84 + 106.369 | 291.209 | line_kerf 291.209 | 0.00 |
| Drill tip above the collar | 184.84 - 159.84 | 25.00 | drill_head\|collar g_min 25 | 0.00 |

### 1b Holder section (holder.py dims and profile points)

| Piece | Hand | Code |
|---|---|---|
| OD | 67.29 - 0.25 = 67.04 | 67.04 |
| Cone | r 62.04 (67.04 - 5) at 49.09 to r 62.04 - 30 x 0.176327 = 56.7502 at 79.09 | (62.04, 49.09), (67.04, 49.09), (67.04, 79.09), (56.7502, 79.09); convex, counter-clockwise |
| Tube | r 56.75 to 67.04, 79.09 to 137.09 | equal |
| Flange | r 56.75 to 72.04 (144.08 / 2), 137.09 to 145.09 | equal |
| Neck | r 56.75 to 67.04, 145.09 to 153.84 | equal |
| Collar ring | r 55.00 to 76.20, 153.84 to 159.84 (overhangs the bore 1.75) | equal |

The holder cone against the collet cone: r_h - r_c = 62.04 - 63.29 + 7.09 x 0.176327 = +0.00016, constant (parallel lines). This gives C contact over 49.09 to 72.00, which is 22.91 (DERIVED).

### 1c Collet, receiver, wing nut, spigot

- **Collet d 100 (collet_family.dims, K d+1)**
  - r_fo 66.99 and r0 63.79.
  - h = 25 + 3 + 4 = 32; r_top0 = 63.79 - 30 x 0.176327 = 58.5002.
  - room = 58.5002 - 51.0 - 1.2 = 6.3002, so c = 6.3002 and z_e = 65.6998.
  - Clamped: cone r 63.2909 at 41.995, 59.1111 at 65.70, 58.0002 at 72.00; bore 50.50; chamfer top 56.8002.
  - All pieces equal the code to 0.0001.
  - Grip 23.20.
  - Both collet polygons are convex and counter-clockwise.
- **Collet d 105**: room = 58.5002 - 53.5 - 1.2 = 3.8002, z_e 68.1998, cone 58.6703 at 68.20, grip 25.70. These equal the code.
- **Receiver (receiver.py profile points)**
  - Floor r 40 to 80, 12.00 to 40.00.
  - Wall r 67.29 to 80, 40.00 to 76.50 (z_sh = 88.5 - 48 - 4 = 36.5 z_R).
  - Land r 67.29 to 72.29, 76.50 to 80.50.
  - Thread r 67.29 to 74.79, 80.50 to 127.25.
  - Rim polygon (67.29, 127.25), (74.79, 127.25), (73.54, 128.50), (68.29, 128.50), (67.29, 127.50).
  - Shoulder r 80 to 100, 12 to 20.
  - Root r 72.29, 80.50 to 128.50.
  - All equal the code.
- **Wing nut**: plate, pocket rim and washer equal nut.py. The body and skirt are not equal: see FIX 3 and FIX 4.
- **Slit stations (collet_family.build_solid)**
  - k 2: theta 52 + 60 = 112, top-open, 72.00 to 47.00.
  - k 7: theta 262, bottom-open, 40.00 to 65.00.
  - These equal the code. The u placement fails: see FIX 1.
- **Spigot radial gap**: 160.4 / 2 - 160 / 2 = **0.20 >= g_min 0.10**, margin 0.10. Code: section_u break at u +-80.20 and spigot r 80.00.

### 1d Pair distances (DERIVED, hand)

| Pair | Hand |
|---|---|
| receiver\|holder | 67.29 - 67.04 = 0.25 |
| receiver_spigot\|base_plate | 0.20 |
| wingnut\|holder | axial 145.59 - 145.09 = 0.50; radial at the plate hole 68.04 - 67.04 = 1.00; flange to the body 74.79 - 72.04 = 2.75 (over 137.09 to 139.09; 3.30 in the relief zone after FIX 3) |
| collar\|wingnut | 0.75 |
| holder\|core and carrier | 56.75 - 50.50 = 6.25 |
| collar\|core | 55.00 - 50.50 = 4.50 |
| wingnut\|core | 68.04 - 50.50 = 17.54 |
| liner\|holder | 3.75 |
| liner\|collar | 2.00 |
| carrier top above the tip | 202.50 - 184.84 = 17.66 |

### 1e Advance path for the drawn option D

F4: the core top must be at least kerf centre + stop.margin, that is at least tip + 111.369. The dome pole is at tip + 34.9315, and the sphere r 71.4375 meets r 50 at tip + 106.369 - 51.023 = tip + 55.346.

| Case | Hand (DERIVED) | Code / spec | Status |
|---|---|---|---|
| Least slice | 296.209 - 219.772 = 76.44 (axis); 296.209 - 240.186 = 56.02 (surface) | 76.44 / 56.02 | equal |
| 100 mm core on the carrier (drawn) | one cut, tip window 184.84 to 302.50 - 111.369 = 191.13 (extent 6.29, the exposure margin). At the stop: slice 82.73 (axis), stub 219.77 - 202.50 = 17.27 (axis) to 240.19 - 202.50 = 37.69 (surface) | 1 slice, stub 17.27 / 37.69 | equal |
| 0.75 m core on the stop | first cut tip <= 792.50 - 111.369 = 681.13; last tip >= 184.84; tip span 496.29, within travel (start 834.84, 153.71 to spare). Cuts at 76.44 steps: tips 681.13, 604.69, ..., 222.51, which is **7 cuts**. Core removed 792.50 - 219.77 = 572.73 (axis). Stub after a last cut at the stop **177.27** (axis) / 197.69 (surface) | "sliceable 496.29, 6 slices"; spec text "stub 253.71 onto the carrier"; `checks_s4.slice_numbers` slices_075 = floor(496.29 / 76.44) = 6 | FIX 5 |

## 2 Shared rows (X1), S4-only expressions, DERIVED overlay leaves

- **X1 on the live set: pass, 70 shared rows** (MEASURED, `p3b/x1dry.py`).
  - Skipped: base_frame plan_poly, base_plate plan_poly, keepout place.
  - The S4 shared rows carry the s3 place, z_rule and plan_poly verbatim.
- **Staged P6 set** (staged s1, s3, s4 and the live s2): X1 passes on 70 rows. `section_true` is equal on all six base rows. The stack tie holder z_max 153.840 + collar.thickness 6.0 = 159.840 has diff 0.0000 on staged s1 and on staged s4 (MEASURED, `p3b/x1dry2.py`). I sign the staged text, subject to FIX 3 and FIX 4 being applied to all three copies.
- **S4-only rows**
  - washer z_min equals the flange top.
  - carrier z_min = core_stop = core_seat z_max.
  - core_seat_105 and collet_105 z_rules are equal to core_seat and collet.
  - receiver_spigot 0 to 12 meets base_plate z_max and receiver z_min.
  - line_min_core = wingnut z_max + core.min_exposed.
  - The wing sub-artist z_max equals the wingnut z_max.
  - No S4-only expression disagrees with a shared row (DERIVED, evaluated in `code_vals.json`).
- **Overlay**
  - carrier.diameter has expr `core.diameter_nominal + collet.grip_window_hi` = 101.
  - liner.wall has expr `(liner.od_offset - core.tol) / 2` = 2.0.
  - liner.collet_d has expr `core.diameter_nominal + liner.od_offset` = 105.
  - Every DERIVED leaf added carries expr, and each agrees with its value (MEASURED through the loader).
- **Liner pose consistency**: the drawn liner OD 106 equals d 105 + grip_window_hi, which is the K d+1 clamp of the d 105 collet. So the liner figure stands at the same holder pose (collar top 159.84). Wall 2.50 drawn means core 101 cast in; 2.0 is the worst case, core d + tol inside D.

## 3 S4-2 in the ruled form

The ruling (Design Notes 34): short-core exposure and grip, asserted on the drawn configuration. checks_s4.s4_2 tests (a) rests_on within 0.05, (b) drawn core top minus drawn nut-plate top >= 143.12, and (c) grip-member z extent covering the straight-bore band. This is what the ruling says.

Premise of (b): the drawn pose K d+1 has the highest nut-plate top over the grip window, and the core stop 42.50 sits on the collet ledge on the receiver floor, independent of the clamp.
- Every other clamp lowers the plate. At K max (d - 1.5) the extra radial is 1.25, which lowers it 1.25 / 0.176327 = 7.09 to 146.00, and the exposure rises to 156.50.
- So the drawn exposure is the least over the clamp range.
- At K d+1 only, (b) equals core top >= kerf centre at the stop + 5 (153.09 + 143.119 = 291.209 + 5).
- The premise is enforced by S4-1: drawn collar top = stop.collar_top_z within 0.05, plus K6 on the wing-nut z_rule.

Premise of (c): the collet grips only on the straight bore, and radial contact is certified by K7 C pairs collet|carrier and collet_105|liner. (c) supplies the axial coverage.

B1 to B3 hand values:
- B1: -10.59, so (a) and (b) fire.
- B2: 292.50 - 153.09 = 139.41 < 143.12, so (b) fires.
- B3: 66.00 - 42.50 = 23.50 > 0.05 and 66.00 > 65.70, so (a) and (c) fire.

The grip_band expression is valid for the family (ruling O8).

## 4 FIX items

**FIX 1. The +u slit tick cannot meet its own admission.**
- Spec `collet.slits.u` reads "r_mid sin(theta), r_mid the wall mid-radius at the line's mid-height". Admission (Designer 2a, spec source): inside the collet's drawn hull, with the u > 0 line touching the top face.
- Hand: theta 112, z_mid 59.50, wall r 50.50 to 60.20, r_mid 55.352, u = **+51.322**. The hull at u 51.32 tops out at **66.52**, on the chamfer edge (50.50, 65.70) to (56.80, 72.00). The line runs to 72.00, so 5.48 of it lies outside the hull in the bore. The top face spans u 56.80 to 58.00.
- No projected position can touch it. Max |u| = 58.0002 sin 112 = 53.78 < 56.80, because the cut top face is narrower than the projection offset.
- The -u line passes: u -55.425, inside the hull to 70.62, line 40.00 to 65.00, touching the foot.
- The Designer and the Topologist pick one form, and The Engineer writes it at P2f:
  - (a) the +u line drawn schematically at the top-face mid-radius u +57.40 (length 25, touches the top face, inside the hull: hull at z 47 spans 50.50 to 62.41); or
  - (b) the projected line u +51.32 ended on the chamfer edge at 66.52 (length 19.52), with the admission text changed from "touching the top face" to "ending on the hull boundary".
- Dry run: hull and line arithmetic in `D:\Unleashed Robotics\_scratch\cutjig\open14\p3b\dryrun.py`. The sub-artist renderer lands at P4, so the harness dry run is due there.

**FIX 2. The wing-nut washer window at theta 90 lies in the section plane.**
- nut.py cuts `box_at(90, r_pk - 1, r_body + 1, nut.washer_window_width / 2, z_pu, z_pu + pd)`: r 70.90 to 84.14, z_A 145.59 to 146.39, +-5 tangential about theta 90, which is u = +Y on plane x = 0.
- Code: `pocket_rim` r 71.90 to 83.14 at 145.59 to 146.39 drawn, mirrored to both sides. The not_drawn entry reads "windows ... off the plane". In the true section the +u pocket rim is absent.
- The -u side (theta 270) is solid: the windows at 210 and 330 are 60 deg off.
- S3 r8 (same plane) carries the same staged section_true. S1 (xz) does not: no window lies on theta 0 or 180.
- Fix: draw the +u pocket rim absent (a per-side piece, `side: -u` on pocket_rim, outside the X1-compared revolve profile), or keep it drawn and replace the not_drawn reason with a drafting reason. The Designer rules the form. The washer contact with the plate underside at 146.39 is unchanged on both sides.

**FIX 3. Wing-nut relief bore missing.**
- nut.py cuts `cyl_z(0, 0, nut.relief_r 75.34, nut.relief_z 42.0, z_pu 48.5)`. The bore is r 75.34 over z_A 139.09 to 145.59.
- Code: body inner r 74.79 to 145.59.
- Fix: split the body into `body: [thread.major / 2, wingnut.body_od / 2, Z0, Z0 + nut.relief_z]` and `relief: [nut.relief_r, wingnut.body_od / 2, Z0 + nut.relief_z, Z0 + nut.length + washer.thickness - nut.washer_pocket_depth]`. Here Z0 = `collar_top - collar.top_above_plate - nut.overall_height`. Add the keys nut.relief_r and nut.relief_z.
- Apply in s4 and in staged s1 and s3.
- Dry run (MEASURED, `p3b/dryrun.py` on scratch copies in `p3b\ws`): body 74.79 to 83.14, 97.09 to 139.09; relief 75.34 to 83.14, 139.09 to 145.59; X1 pass 70; section_true equal on all six rows.
- The least flange-to-body gap stays 2.75 (flange 137.09 to 139.09 against r 74.79).

**FIX 4. Wing-nut skirt profile.**
- nut.py skirt_solid revolves (82.14, 5), (95.14, 5), (95.14, 7), (83.14, 14): a 2.0 rim (nut.skirt_rim), then a slope to the body.
- Code: rectangle r 83.14 to 95.14, 102.09 to 111.09, 108 mm2 per side. The true section is 66 mm2.
- Fix: `skirt: {poly: [[wingnut.body_od / 2, Z0 + nut.skirt_z_lo], [nut.skirt_r_out, Z0 + nut.skirt_z_lo], [nut.skirt_r_out, Z0 + nut.skirt_z_lo + nut.skirt_rim], [wingnut.body_od / 2, Z0 + nut.skirt_z_hi]]}`. Add the key nut.skirt_rim. Apply in s4 and in staged s1 and s3.
- Dry run (MEASURED): (83.14, 102.09), (95.14, 102.09), (95.14, 104.09), (83.14, 111.09), convex and counter-clockwise, area 66.000. X1 pass 70; section_true equal.

**FIX 5. 0.75 m slice count and stub.**
- Hand (section 1e): 7 cuts at the 76.44 axis minimum, core removed 572.73, stub on the stop after the last cut 177.27 (axis) / 197.69 (surface).
- Code: `checks_s4.slice_numbers` slices_075 = floor(sliceable_075 / slice_min_axis) = 6. Spec reported_items advance: "sliceable 496.29, 6 slices, stub 253.71 onto the carrier".
- Fix:
  - slices_075 = floor((core stop + core.length_install - min_core_top) / slice_min_axis) + 1.
  - Add stub_075_axis = dome_pole - core stop, and stub_075_surface = sphere_at_core_surface - core stop.
  - Spec text: "0.75 m core: tip span 496.29 (681.13 to 184.84), 7 slices at the F4 least slice 76.44, 572.73 removed; stub on the stop 177.27 (axis) to 197.69 (surface), onto the carrier for further slices; 253.71 is the least core that takes a cut on the stop".
- Dry run: arithmetic in section 1e. No harness value is set: RPT carries no threshold.
- Design Notes 34 quotes "the last 253.71 mm stub" in Sean's ruling text. The ruling (a carrier for the stub) is unchanged. The orchestrator decides whether that record needs a note.

## 5 Rulings on the open items

- **O2 (X1 extension)**
  - P4 compares `section_true` and leaves `section` uncompared.
  - The three live `section` differences are presence only, with no two specs holding conflicting values (MEASURED, `p3b/secfld.py`):
    - drill_tube is set in s3 only;
    - ring is s1/s2 `section` against the s3 `section_u` form;
    - gear is set in s2 only.
  - `section` is a view-specific renderer input (plan annulus in S2, cut pieces in S3).
  - Rule:
    - (i) equality of `section_true` on every shared row that carries it in two or more specs (live: s4 only, pass; staged: six rows equal);
    - (ii) a presence rule: a shared row carrying `section_true` in one spec carries it in every spec that draws that row in a side or section view. This is red on the live set (s1 and s3 lack it on six rows) and must land with P6 in one save point;
    - (iii) `section_true` holds the revolve half-profile only. Plane-dependent features (wing-nut wings in xz, the theta 90 window in yz, keys, slits) are per-spec sub-artists or side pieces outside the X1 comparison (Correction 1).
  - The header wording "mirrored about u = 0 (axis-Z rows)" must not key mirroring on `axis`: wingnut and core_seat carry axis null as a shared X1 field.
- **O5 (carrier on 0.50 of the d 105 ledge)**: accept as drawn, no geometry change.
  - Carrier annulus r 50.00 to 50.50 = pi x 50.25 = 157.86 mm2; liner annulus r 50.50 to 53.00 = pi x 258.75 = 812.88 mm2 (DERIVED).
  - At F_stall + W 1287.05 N on the carrier annulus alone: 8.15 MPa. Split by area: 1.33 MPa. Both are far above fit.min_contact_patch 1 mm2.
  - In the section the C contact is a 0.50 segment per side at z 42.50 (u 50.00 to 50.50), a face contact with no point contact.
  - The carrier|core_seat_105 source text already states it.
- **O8**
  - The chamfer expression min(room, collet.chamfer_cap) holds for all seven collets. room = 56.3002 - d / 2 enters the band (2.5, 3.5) only for d in (105.60, 107.60), above the family maximum 105. The least room is 3.80 at d 105.
  - Foot-ring top 41.995 = receiver_floor + 2.0 - 0.005 (cadlib.footring_derived) is correct.
  - The spec clamp shift 0.50 differs from build_parts (bore 0.495, cone 0.50508) by at most 0.0051, inside every K tolerance (0.05).
- **O1**: staged S1 r9 / S3 r8 text signed with FIX 3 and FIX 4 applied to all three copies, and FIX 2 to S3 r8 and S4.
- **Engineer stack hand check**: confirmed to 0.01 on every item. Collar top 159.84, holder bottom 49.09, flange 137.09 to 145.09, nut-plate top 153.09, tube top 153.84, core top 302.50 on the carrier and 142.50 on the stop, receiver floor 40.00.

## 6 NOTES (no revision)

- N1. The staged class changes assume S1 r9 and S3 r8 draw `section_true`. With the r8-era `section` fields:
  - the holder OD is the register bore 67.29, so receiver|holder G 0.25 reads distance 0;
  - the S1 stand-in receiver wall runs to r 80 over the wing-nut bore r 74.79, so receiver|wingnut C reads overlap.
  - P4 rules `section_true` as the drawn section before P6. Otherwise K7 is red on S1 r9 and S3 r8.
- N2. The bore lip fillet (collet.bore_lip_radius 1.0, tangent length 1.0 tan 22.5 = 0.414) ends the true straight bore at 65.29. The true grip is 22.79 (d 100) against the drawn 23.20 under the stated straight-chamfer convention. Reported grip_length should say which one it prints.
- N3. `checks_s4.s4_2` raises Absent when the carrier row is not drawn, so B1 as written ("(a) and (b) fire") returns cause absent and cannot match on reason. For P4 and the Software Engineer: plant B1 as the carrier drawn at zero length or below the seat, or treat a missing grip member as an (a) issue.
- N4. `s4_2` (b) reads the wingnut z_max over all its pieces. If the sweep extent lines (S3 form) run above 153.09, the datum moves. P4 should restrict the read to the plate piece.
- N5. For the Designer's part list, these features are off the plane and absent from not_drawn:
  - collet rim notches: d 100 at theta 97, 127, 157, 217, 247; d 105 adds 277 and 337. The nearest is 7 deg off the plane, 7.0 tangential at r 57.4 against the 3.0 half-width;
  - the collet label window at theta 7;
  - the holder Rule P index notch at theta 323.
- N6. collet_105 `slits: {same_as: collet}` reads receiver.key_offset_deg, which is missing from the collet_105 keys list.

## Gameplan lines to change

1. Detail 1.4, Reported line (line 318). Supersedes `research/sean/cr_scratch/step1.4_engineer_spec.md` item 5.
Old:
```
Reported: exposed length of a 100 mm tall core against `core.min_exposed` 143.12 (Q10); collet length options (Q5); sacrificial collet or liner (Q6).
```
New:
```
Reported (spec reported_items, RPT): 100 mm core top against the collar top (142.50 on the stop, 17.34 below; 302.50 on the carrier) and its exposure against `core.min_exposed` 143.12 (-10.59 / 149.41); minimum core on the stop 253.71 (nut-plate datum; 260.46 collar-top datum), the least core that takes a cut on the stop; collet grip 23.20 (d 100, straight chamfer drawn; 22.79 to the lip fillet); advance D: least slice 76.44 axis / 56.02 surface; 0.75 m core tip span 496.29 (681.13 to 184.84), 7 slices, 572.73 removed, stub on the stop 177.27 axis / 197.69 surface; 100 mm core on the carrier 1 slice, stub 17.27 / 37.69; carrier-joint shear 50.9 kPa (liner 6.37); collet length options Delta 0 / 25 / 50 (Q5, kept 32 mm); liner D = d + 5, wall 2.0 (Q6); cut-case seat as drawn; kept-part axial forces (as S3 r7).
```
