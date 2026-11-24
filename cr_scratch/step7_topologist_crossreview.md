## Verdict: SIGN WITH EDITS (E1 to E8 enter the build; no re-view)

| Line | Verdict | Invariant or edit |
|---|---|---|
| K1 R nut at holder + 48.745 | SIGN | 104.75 - 56 - 0.005. Screw invariant z0 - 8 az/360 = 60.645 mod 8 holds at 62.371 / 77.670, 57.099 / -159.571, 50.010 / -478.575. |
| K2 collar ring fused into holder | SIGN WITH EDIT E1 | The four insert bores (d 5, depth 12) open at holder z 104.75. A plain ring r 55 to 76.2 closes them into 4 internal void shells (shell_count 5). E1: cut 4 holes d = holder.insert_dia in the ring at the insert azimuths read from the built holder, one cut on the ring alone, then fuse. |
| K3 to K7 | SIGN | K6 four solids, K7 resolved by L5. |
| L1 S(phi) sign and ledger | SIGN WITH EDITS E2 to E4 | Rz(phi) T(0,0,L phi/2pi), L 8: phi < 0 gives dz < 0, so clockwise lowers (T1c). All dz and phi rows recompute (-5.272 / -237.241, -12.361 / -556.245). No App::Link in pose files, so 2.7 does not apply. |
| L2 core | SIGN WITH EDIT E8 | Revolve, chamfer on one end: faces 4, euler_VEF 2. R bottom is 3.500 (ledge 2.5 + lift 1.0); L2 prose reads 3.505. |
| L3 cutter | SIGN WITH EDIT E8 | Four solids touch on faces, common volume 0. Min clearances at Kd1 d 105 are 3.0 and 13.0, not 3.5 and 13.5. |
| L4 placements | SIGN WITH EDITS E5, E7 | T(0,0,-0.005) lowers the frame away from the plate: gap 0.005, class C. Foot and nut\|washer rows carry E5 and E7. |
| L5 option (a) | SIGN | Deletion, no boolean, no split plane. 96 host contacts are touching (min_dist at most 0.01, common 0), measured per instance. |
| L6 measures | SIGN | Foot ring r 40 to 80 sits 2 mm inside the nearest member edge x 82: contact 0. |
| L7 planted states | SIGN WITH EDIT E6 | See sign table below. |
| L8 | SIGN | Rows follow L1. |

## Edits

- E1 as K2.
- E2: the ledger stores 4x4 matrix and unwrapped phi. The audit compares Placement.Matrix and phi mod 360 from atan2 of the matrix. Rotation.Angle wraps beyond 360 and flips the axis for phi < 0, so it is not read.
- E3: R engaged 25.705 against 88.5 - z0 = 26.129, and R travel 22.295 (= 48 - engaged) against z0 - 40.5 = 21.871; K rows agree. Basis: the probe value governs R, the formula column covers K only. Both pass (24, 8).
- E4: washer(R) = Rz(77.670) T(0,0,110.366); washer(P) = S(phi) washer(R), so pad overlap is equal in every pose. Holder moves by T(0,0,dz) only. Criterion 9 reads: fixed set base, frame, bracket, tnut, cutter; nut and washer by S(phi); holder by z.
- E5: write foot placements as Placement(position, Rz(180)) with rotation about the part origin, then translation. The product Rz(180) T(-262, ...) places the -x feet at x +262.
- E6: WS3 pivot 125.099 = nut z0 + 56/2, not bbox mid 123.299. WS2 pivot from the unfused holder bbox (101.464). WS4 is a mirror (det -1), which Placement cannot carry: bake with Shape.mirror, placement identity, require Volume > 0 and isValid. WS1 and WS11 both read 66.5 mm3; each is computed from its own ws file.
- E7: nut\|washer class P also carries common volume at least 2.30 (built 2.387), so a washer that only touches fails.
- E8: values in L2 and L3.

## Predictions for the gate

| Part | euler_VEF | Faces | Other |
|---|---|---|---|
| frame members | 11 | 2478 | volume 2,930,129.191; plain = optimal bbox (+-322, +-304, -60 to 0) |
| frame result | | | objects 114; brackets 12 (printed 191,775.468 mm3); T-nuts 96; booleans 37; overlaps none |
| pose holder with E1 | 10 | holder + 4 | shells 1; unmerged hole cylinders give 14 and + 8 |
| pose holder without E1 | | | shells 5 |
| core | 2 | 4 | |
| cutter solid, each of 4 | 2 | 4 | compound 16 faces |
| mirrored nut | 10 | unchanged | handedness reverses |

Planted-state signs: WS1 to WS3, WS5, WS10 are Rx about the x-axis through the named z, det +1. They map (y, z) to (-y, 2c - z) and flip every z-normal sign. WS11 is Rz(-15). WS5 tilts the axis by 2.000 degrees. WS4 is the only improper transform.

## Revision 1 cross-review

Verdict: SIGN, no edit. Predictions: trial booleans in FreeCAD.

| Part | Faces | Edges | Vertices | euler_VEF | Shells | Volume mm3 |
|---|---|---|---|---|---|---|
| holder before / after | 28 / 40 | 61 / 79 | 41 / 53 | 8 / 14 | 1 / 1 | 407,841.2 / 459,449.0 |
| nut before / after | 195 / 195 | 472 / 477 | 287 / 293 | 10 / 11 | 1 / 1 | 358,837.8 / 352,473.8 |

Holder. Ø6.6 holes supersede E1 (Ø5.0): the hole covers the Ø5 bore, so no void shell forms. The faces are the ring outer, top, inner and two underside remainders (+5), minus the shared tube-top annulus (-1), plus 4 hole cylinders and 4 ledge annuli (r 2.5 to 3.3, z 104.75). That is +12 faces, and my earlier +4 / euler 10 is withdrawn. Genus unchanged; bbox zmax 110.75.

Nut. The relief adds the r 75.34 cylinder (one face, 3,077 mm2, z 42.0 to 48.5) and one planar up-facing face at z 42.0 (734.96 mm2, 2 wires). The 0.2 radial margin over the thread root r 75.14 prevents a sliver. Removed thread faces offset the additions: faces net 0, euler +1.

Interactions:
- Stud-subtract faces: the relief runs in the last cut, after ThreadStud, and only trims groove faces above z 42.0, which is 0.5 below the full-groove top.
- Window boxes, tab and pads occupy z 48.5 to 49.3. They share only the plane z 48.5 with the relief top. Windows open onto the relief void with no coplanar sliver;.
- Tommy holes: bottom r 78.14 leaves a 2.80 wall to r 75.34.
- Dust skirt and glyph recesses (r above 95.64): no contact.

Note. The 9,978 mm2 holder|nut R contact exceeds ring underside on plate top (at most pi(76.2^2 - 68.04^2) = 3,694). The A1 predicate takes the shared area from the common-face intersection.
