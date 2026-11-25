# Step 1.0 Wave 2: Loftsman geometry cross-review (K6, K7, S1-6)

Scope: sketches/check_stack.py, sketch_common.py (K6, K7, geometry), checks_s1.py (S1-6, and S1-5a, S1-5b where they call the K7 geometry), s1_spec.yaml (z_rule, depth), proposed_params.yaml, fixtures (K6, K7). Frame: Design Notes 17 (z_S = z_A + `jig.datum_a_above_floor` 60 ASSUMED; z_R = z_A - `icd.floor_above_datum_a` 40). Bore ceiling: Design Notes 19 (`drill.bore_ceiling_above_tip` 800 ASSUMED). Probe script, not a harness file: scratchpad `lf_probe.py`. All code values MEASURED 2026-11-24 by running check_stack.evaluate_spec on the live s1_spec.yaml and the geometry functions; hand values DERIVED.

Result: 1 BLOCK, 6 FIX, 8 NOTE. The frame arithmetic, the collar-top stack, the pose tips and the Sutherland-Hodgman and minimum-distance kernels are correct on every hand case. The defects are in how K7 treats depth separation, multi-piece and non-convex parts, and in two stack datums the draft spec carries.

## 1. Hand values beside code values

### 1.1 Frames and stack (K6, check_stack.py)

| Quantity | Hand (DERIVED) | Code (MEASURED) | Agree |
|---|---|---|---|
| Collar top, test_P18 formula: 13.626 - (13.126 - 8.59) + 88 + 8 + 8 + 6.75 | 119.840 z_R | (not output in z_R) | |
| Collar top + `icd.floor_above_datum_a` 40 | 159.840 z_A | 159.84 z_A (check_stack l.56-63); params `stop.collar_top_z` 159.84 | yes |
| Collar top in plot frame, + 60 | 219.840 z_S | wingnut z_max 213.09 + `collar.top_above_plate` 6.75 = 219.84 z_S | yes |
| Nut plate from params: 7.5 + 1.3 - 0.8 | 8.000 | 8.0 (test writes literal 8) | yes |
| Shop floor | 0 z_S (-60 z_A) | floor 0.0 z_S | yes |
| Base frame top = datum A | 60.000 z_S | base_frame z_max 60.0 | yes |
| Receiver floor | 40 z_A, 100.000 z_S | core_seat z_min 100.0 | yes |
| Core stop (correction 5, ASSUMED) | 42.5 z_A, 102.500 z_S | core_500 z_min 102.5 | yes |
| Tip, start: `stop.start_z[0]` 834.84 + 60 | 894.840 z_S | 894.84 | yes |
| Tip, end of capture: `stop.height_z` 184.84 + 60 | 244.840 z_S | 244.84 | yes |
| Tip, park and load (draft rule): max(965, 42.5 + 750) + 50 = 1015 | 1075.000 z_S | 1075.0 | yes |
| Lift stroke: 1015 - 184.84 | 830.16 | 830.16 | yes |
| Ring at end of capture: 184.84 + 200, + 12 | 384.84 to 396.84 z_A = 444.84 to 456.84 z_S | 444.84 to 456.84 | yes |
| Bore ceiling at end of capture: 184.84 + 800 + 60 | 1044.840 z_S | 1044.84 | yes |
| Soft target line: 2000 - 60 in z_A, back to z_S | 2000.000 z_S | 2000.0 | yes |

Signs: `to_shop_floor` adds 60 (l.39-41), `receiver_to_datum_a` adds 40 (l.49-51). Both correct against ASSEMBLY.md line 7 and test_P18 l.702. K6 compares in data coordinates: `artist_polys` applies `get_patch_transform()` (patch to data), Line2D reads xdata and ydata (sketch_common l.169-185); tolerance 0.05 mm on max(|z_min error|, |z_max error|) (l.590-592). K6 B2 hand 60, code 60.00; B2b hand 60 + 40 = 100, code 100.00; B1 hand 6.75, code 6.75.

### 1.2 K7 geometry

| Case | Hand | Code | Agree |
|---|---|---|---|
| Two 10 x 10 squares offset (5, 5), CW subject against CCW clipper | overlap 25 | 25.0 | yes |
| 2 x 2 square inside 10 x 10, both argument orders (clipper contains subject, subject contains clipper) | 4 | 4.0, 4.0 | yes |
| Collinear partial edge contact (10 x 10 and 10 x 4 sharing x = 10 over z 3 to 7) | distance 0, overlap 0 | 0.0, 0.0 | yes |
| Cross: 10 x 2 bar over 2 x 10 bar, no vertex of either inside the other | distance 0, overlap 4 | 0.0, 4.0 | yes |
| Vertex-edge: triangle vertex (13, 5) to edge x = 10 | 3 | 3.0 | yes |
| Touching at a float coordinate (z = 894.84 shared) | distance 0, overlap 0 | 0.0, 0.0 | yes |
| Z1 F: rectangles 100 apart | distance 100, overlap 0, F | clean, F | yes |
| Z3 C: shared edge | 0, 0, C | clean, C | yes |
| Z2: bands [0, 10] and [20, 30] | depth-separated | depth-separated | yes |
| B1: 1 x 100 overlap per pair, C, G, F | 100 mm² each, all fire | 100.000 x 3 | yes |
| B2: C pair, gap 1 > 0.05 | fires | fires, 1.000 | yes |
| B3: G pair, 9 < 10 - 0.05 | fires | fires, 9.000 | yes |
| Z4: hull top p4 tip 500 + 100 + 20 = 620; member 700 | gap 80 >= 10, clean | clean | yes |
| B4: member 200 x 10 inside hull z 100 to 620 | 2000 mm² | 2000.000 | yes |

Sutherland-Hodgman (l.250-281): both windings normalised CCW; points on a clip edge count inside (>= -1e-12); a contained subject or a containing clipper returns the right polygon. Minimum distance (l.322-330): vertex-in-polygon, proper edge crossing, then vertex-to-edge both ways; overlap returns 0. Correct for convex inputs. Swept hull in side views: for a pure vertical translation the swept region of a convex piece is exactly the hull of its lowest and highest positions, so two poses suffice.

### 1.3 S1-6 screw by hand

`jackscrew.pitch_radius` 160, `jackscrew.angle` [30, 150, 270] (overlay, ASSUMED phase). screw_a uses angle[1] = 150 deg: x = 160 cos 150 = -138.564; depth centre = 160 sin 150 = 80.000, band 80 +/- 4 = [76, 84]. Code: depth [76.000, 84.000] (check_stack, capture_end); S1-6 compares the drawn centroid x with `r * cosd(150)` = -138.564 (checks_s1 l.153). screw_b, 30 deg: x = +138.564, depth [76, 84]; code [76.000, 84.000]. The B "screw drawn at x = r" misses by 298.564 (screw_a) and 21.436 (screw_b); both fire. theta is counter-clockwise from +X seen from +Z, y = r sin theta; in side_xz the viewer stands at -Y, so depth increases away from the viewer. Consistent.

## 2. Findings

**LF-1 BLOCK. K7 passes any depth-separated pair without testing its class.** sketch_common.py l.622-624 (static) and l.655-657 (swept): when the depth bands are disjoint the pair is logged "depth-separated" and skipped, whatever its class and g_min. Probes: a C pair with bands 490 mm apart reads `pass, states ['depth-separated']`; a G pair with g_min 10 and a depth gap of 1 mm reads `pass`. Disjoint bands prove "not overlapping", which satisfies F only. For C they prove the contact is absent; for G the certified gap is the band gap, which may be below g_min. S6-3 (gameplan l.315) closes the torque loop on "class C in the spec and touching in the figures (K7 C)"; a chain pair drawn at the wrong depth would report the loop closed. The gameplan K table wording (l.140, "tested only when its depth bands overlap") produces the defect; the code follows it. Fix: with band gap d_y = max(lo_b - hi_a, lo_a - hi_b) > 0, C fails when d_y > 0.05; G passes when max(d_y, XZ distance) >= g_min - tol (3D distance is at least each projected distance), else fails; F passes. Add controls K7-B5 (C pair depth-separated, fires) and K7-B6 (G pair, g_min 10, depth gap 1, XZ overlapping, fires). Orchestrator note: K table l.140 needs the same correction.

**LF-2 FIX. No control anchors the frame conversion or the stack to an independent number.** Every K6 fixture is drawn from check_stack values (builders.py l.3, l.103-128), so a sign error in `to_shop_floor` (z_A - 60) or `receiver_to_datum_a` leaves K6 Z clean and B1, B2, B2b firing: B2 would still sit 60 below the (wrong) stack. Collar top is reported, never asserted (check_stack l.195-196; check_sketch l.186). Fix: a K6 anchor control with hand numbers written in the manifest: floor 0, datum A 60, receiver floor 100, collar top 219.84 z_S, and `collar_top_z_A(P)` equal to `stop.collar_top_z` within 0.01 (test_P18 tolerance). A planted sign flip in a scratch copy of check_stack must fire it.

**LF-3 FIX. Swept hull merges all pieces of a moving feature into one hull.** sketch_common.py l.658-670: `pts` gathers every piece at the lowest and highest pose and takes one convex hull. A feature drawn as two pieces either side of a bore (ring halves, gear section, bearing races) gets a hull that fills the bore. Probe: ring halves at x [-210, -100] and [100, 210], fixed post x [-20, 20] through the bore, static clearance 80 mm: K7 fails with overlap 20800 mm² (false fire). The swept region of a multi-piece part is the union over pieces of hull(piece at lowest pose, same piece at highest pose). Fix: pair pieces by index across the two poses and hull each pair; test each hull against each fixed piece.

**LF-4 FIX. Non-convex pieces reach the clipper unchecked in the swept case and in S1-5b.** The static path rejects non-convex pieces (l.630-634); the swept path (l.659-671) and checks_s1.py s1_5b (l.127-132) call `pair_measure` without `is_convex`. Sutherland-Hodgman needs a convex clipper, and `min_distance`'s inside test assumes convexity. Probe: L-shaped fixed member (arms 100 x 10) against a 10 x 10 square on its arm: overlap returned 0.0, true 100; full 100 x 100 square: returned 100.0, true 1900. The error masks overlaps. Fix: apply the same convexity guard in both places (or split in `pair_measure`).

**LF-5 FIX. Draft spec depth bands of radial-axis parts are smaller than their true Y extent.** s1_spec.yaml l.329, 345 (pinions), l.361, 377 (NEMA 23 motors): band = centre +/- face_width/2 or +/- motor_body/2. A part of axial length L and width W, axis radial at azimuth theta, spans y_c +/- (L/2 |sin theta| + W/2 |cos theta|). pinion_a at 210 deg, PD 4.1667 x 20 = 83.33 DERIVED, face 30: true half 41.67 x 0.866 + 15 x 0.5 = 43.58 against spec 15. motor23_a: 28.5 x 0.866 + 38 x 0.5 = 43.68 against spec 28.5. Depth separation is sound only when bands are true bounds; undersized bands let LF-1's skip (or its corrected form) certify pairs that overlap in 3D. The motor band centre (PD/2 + motor_length = 201) is the outer end of the body, not its centre. Fix at 1.1 (a)/(b): a helper `depth_band_radial(r_c, theta, L, W)` in check_stack (spec rows call it), and the same formula for the drawn x extent, L/2 |cos theta| + W/2 |sin theta|.

**LF-6 FIX. The draft park rule takes the core bottom at the core stop; params U13 takes it at the collar top.** check_stack.py l.71-75 and s1_spec.yaml l.19: park = max(max(start_z), core_stop + max(Q9)) + clearance, core_stop 42.5 z_A. params `upper.park_z` source (l.36) and test_P18 l.717: collar_top 159.84 + core length + clearance, the loading case where the core bottom must pass over the collar. The gameplan S1-3 text (l.227) says core-stop z, so the code follows the gameplan; params says otherwise. Hand: difference 159.84 - 42.5 = 117.34 mm. No effect at the current Q9 list (both give 1015, since 965 governs: 909.84 and 792.5 sit below it); for the 1 m core the rules give 1209.84 (U13) and 1092.5 (draft). The Designer rules which plane the core bottom crosses during loading at 1.1 (a); the spec states the plane, and S1-3 reads the same plane.

**LF-7 FIX. Core stop 42.5 z_A disagrees with the start pose and the drill advance.** With the 0.5 m core on the seat, core top = 542.5 z_A. Start tip 834.84 sits 292.34 above it, yet the pose table (gameplan l.214) defines start as "cutter at first contact". End tip 184.84 + `upper.drill_advance_500core` 534.93 = 719.77 z_A, which would be the core top if the advance runs from first contact; the gap to the stack value is 177.27 mm. S1-5a reads 442.34 on the stack value and 265.07 on 719.77 (both pass at 25). The M1 figure of the start pose will show the cutter 292 mm above the core. The Engineer flagged the datum (notes correction 5); the pose definition and the advance make it a contradiction, not only an open value. Designer rules at 1.1 (a): core seat height in z_A, or the start pose definition.

**LF-8 NOTE. Side-view box test is sound and conservative; one design value bends to it.** Depth bands that are true bounds never mask an overlap, and the XZ projected distance is a lower bound on the 3D distance, so a G pass is a true pass. Round parts over-report: frame member at radius 250 against the 420 ring reads overlap in XZ with bands overlapping, while the radial clearance is 250 - 30 - 210 = 10 (notes open item 5). `frame_upper.radius` 300 (overlay l.107, source "side-view depth-band box clearance") moves a design value to satisfy the approximation. Recommendation: when bands overlap, test the pair's XY footprints from spec radius, azimuth and section (circle or rotated rectangle); 3D clearance holds if z bands or XY footprints clear by g_min. S2 (plan) can supply the footprints. Designer resets the radius at 1.1 (a) or S2.

**LF-9 NOTE. G tolerance is applied in the permissive direction.** sketch_common.py l.368: passes at distance >= g_min - 0.05, so 9.95 passes g_min 10. The K table says "at least the pair's g_min". Either state the tolerance in the spec format or compare against g_min.

**LF-10 NOTE. K7 G uses unsigned distance.** A part on the wrong side of its neighbour by more than g_min passes (bore ceiling drawn below the core bottom reads G clean). S1-5a computes the signed gap (checks_s1 l.108-114), so S1 is covered; a sense predicate in K8 is the general guard. Topologist's half-space review owns the rest.

**LF-11 NOTE. A Line2D with three or more points is treated as a closed polygon.** `artist_polys` returns the polyline as one polygon (l.171-172); `_edges` closes it (l.314-319) and the clipper treats it as an area. Two-point lines (floor, bore ceiling, keep-out) are unaffected. Polylines must be split into segments, or the helpers documented as two-point only.

**LF-12 NOTE. Two inverse conversions sit outside the frame section.** check_stack.py l.97 (`height_target_z_A` = target - 60) and l.44-46 (`shop_floor_in_z_A`) write z_S to z_A inline. Values are correct (2000.0 z_S on the line). A `from_shop_floor()` beside `to_shop_floor()` keeps every frame conversion in one function pair.

**LF-13 NOTE. Nut plate written from params (7.5 + 1.3 - 0.8 = 8.0) where test_P18 writes 8.** check_stack.py l.61. Agrees today; a change to any of the three keys moves check_stack and leaves the test at 8. The test is Quinn's; record it for Step 4a (test audit).

**LF-14 NOTE. S1-6 cannot see handedness in a side view; its depth half checks the spec.** cos is even: a clockwise theta gives the same drawn x. Depth is not drawn in side_xz, so the depth comparison (checks_s1 l.155) checks the spec's depth expression against r sin theta of the spec's own azimuth field. Mirroring in X is caught (screw_a and screw_b swap x sign). Handedness is K8 azimuth on the plan view (S2).

**LF-15 NOTE. K6 and K7 assume every tagged artist lives in data coordinates.** `artist_polys` reads the patch transform only (l.174). An artist added with `transform=ax.transAxes` or a blended transform would be measured in the wrong frame. A one-line guard (`a.get_transform()` contains `ax.transData`) or a statement in the spec format closes it.

## 3. Checked and clean

- Per-pose z_rule evaluation: tip from the pose expression in z_A, stack names per pose merged over globals without collision, rows filtered by `poses`, conversion to z_S once per bound (check_stack l.167-189).
- Lowest tip = min(`stop.height_z`, `stop.height_range`) = 184.84; stroke uses it (maximum over core classes, gameplan l.218).
- Depth separation test is strict (touching bands are tested), and a missing band means the pair is tested (l.604-605).
- S1-5a hand 984.84 - 542.5 = 442.34 (code 442.34); S1-5b least clearance hand 384.84 - 153.09 = 231.75 z_A (code 231.75).

CROSS-REVIEW FAIL (LF-1; LF-2, LF-3, LF-4, LF-5, LF-6, LF-7)

## Re-check after revision

Inputs: step1.0_engineer_revision_notes.md; the revised sketch_common.py (`band_gap`, `assess_pair` l.426-468, `stack_anchor_issues` l.739-765, `k7` l.826-924), check_stack.py (`from_shop_floor`, `load_plane`, `park_tip_z_A`, `place_extents` l.180-194), checks_s1.py (`s1_3`, `s1_5b`), s1_spec.yaml, and gameplan l.140. Probe script: scratchpad `lf_recheck.py`. `check_sketch.py --controls` re-run: Z clean 17/17, B fired 50/50, smoke 1/1, exit 0 (MEASURED 2026-11-24).

Hand cases re-run: collar top 159.84 z_A and 219.84 z_S; tips 894.84, 244.84 and 1075.0 z_S; stroke 830.16; screw_a x band [-142.564, -134.564], centre -138.564, depth [76, 84]; kernels 25.0, 3.0, and 0.0 / 4.0 on the cross case. All unchanged and equal to the hand values.

| ID | Status | Evidence (probe hand vs code) |
|---|---|---|
| LF-1 | CLOSED | `assess_pair` with band gap d > 0: F passes; C fails when d > 0.05; G passes when max(d, XZ distance) >= g_min - 0.05. Probes: C with bands 490 apart fails ("depth-separated by 490.000"); G10 with d 1 fails (lower bound 1.000); G10 with d 15 passes on the bands; G10 with d 5 and XZ distance 12 passes (lower bound 12); with XZ distance 3 it fails (lower bound 5); C with d 0.03 passes when touching in XZ and fails when the XZ gap is 1. Every case matches the hand rule. K7-B5 and K7-B6 fire in the controls. Gameplan l.140 now states the rule and adds B5 and B6. The same function serves K7 static, swept, undeclared pairs and S1-5b |
| LF-2 | CLOSED | `stack_anchor_issues` in K6. Live: no issues. z_S sign flipped: five issues (to_shop_floor(0) -60, datum A -60 against 60, receiver floor -20 against 100, collar top 99.84 against 219.84). z_R sign flipped: receiver_to_datum_a(0) -40 and receiver floor 20 against 100. K6-Z2 is clean and K6-B4 fires |
| LF-3 | CLOSED | Hulls are built per piece, paired by index (l.915-920), and a mismatch in piece count is an issue. Two-piece ring with a post in the bore and 80 mm static clearance: pass, swept:F (Wave 1b gave a false 20800 mm² fire). Post moved to x 95 to 135 across the right half's sweep: fires, overlap 700 = 35 x 20 per pose (hand 35 x 20 = 700). K7-Z6 is clean |
| LF-4 | CLOSED | The convexity guard sits inside `assess_pair`, so it covers the static, swept and S1-5b paths. L-shaped member in the swept path: fires "non-convex piece in ['L']". Direct `assess_pair` call on an L against a square: (False, non-convex). K7-B9 fires |
| LF-5 | CLOSED (with TP-4) | `place_extents`, radial footprint: y = [min(r_in s, r_out s) - w abs(c), max + w abs(c)]; this is the Minkowski bound of the radial rectangle, and the round case is a segment swept by a disc. pinion_a at 210 deg, r 110 to 140, w 41.67: [-106.08, -18.92], centre -62.5, half 43.58 (hand 43.58). motor23_a at r 125 to 201, w 28.5: [-125.18, -37.82] (hand: centre -100.5, half 43.68). Gear ±140. A spec band given beside a place is hulled with the true band and linted. K7-B7 fires |
| LF-6 | CLOSED (harness); value to Sean's gate | One spec field, `load_plane`. The park rule reads its `term`; S1-3 reads its `feature`, `edge` and `offset`. Probe: term collar_top with Q9 extended to 1 m gives park 1209.84 (params U13 1209.84); term core_stop gives 1092.5. Both equal the hand values. The draft keeps core_stop per gameplan l.227. The plane choice is listed for the gate (revision notes section 6, item 1) |
| LF-7 | CLOSED (harness); value to Sean's gate | Core stop comes from one function, `core_stop_z_A` (42.5 z_A). 292.34 and 719.77 against 542.5 are reported and carried to the gate with the three candidate causes (section 6, item 2). Revision correction 3 is right: `stop.start_z` is travel-derived (params l.179), so the contradiction is between the pose-table wording and the params. A design value is not the harness's to choose |

New, from the re-check:

**LF-16 NOTE. `load_plane` describes one plane twice.** check_stack.py l.108 takes the park rule from `term` (a stack name). checks_s1.py l.89-90 takes S1-3's plane from the drawn `feature` edge plus `offset`. No lint makes the two agree, so `{term: collar_top, feature: core_seat}` would put the park rule and S1-3 on planes 117.34 mm apart while both read green. Draft values agree: core_stop 42.5 z_A = core_seat z_max 102.5 z_S. Fix at 1.1 (b): K6 or a spec lint asserting that to_shop_floor(term) equals the stack z of feature.edge + offset within 0.05.

**LF-17 NOTE. Gameplan l.140 still says "the convex hull of its outline" for the swept case.** The code builds one hull per piece (LF-3). The line should read "per convex piece, the hull of that piece at the lowest and highest pose". This is the orchestrator's file.

Open NOTEs carried as dispositioned: LF-8 (frame_upper.radius 300, to 1.1 a or S2), LF-9, LF-10, LF-11, LF-13 (4a), LF-14. LF-12 and LF-15 are closed (`from_shop_floor`; TP-1 transforms).

CROSS-REVIEW PASS (LF-1 to LF-7 closed; LF-6 and LF-7 design values at Sean's gate; LF-16, LF-17 NOTE)
