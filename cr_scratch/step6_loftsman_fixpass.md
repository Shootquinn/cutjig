## Corrections to the brief

| # | Brief says | Number | Tag |
|---|---|---|---|
| F1 | Eye sees nut z 0, 5 mm below the declared edge | Declared edge is nut z 0: revolve starts at z 0; plate top 56; flange underside 56 - 16 = 40; edge = 40 - `nut.skirt_below_flange` 40. Probes use `rim_top_z - 40`. The renderer put the nut at edge - 5 | DERIVED |
| F2 | K-max hidden, K d+1 shows 4 lines | Render pose reproduces it (nut z 0 at 45.0 hides 14 lines; 52.09 shows k 0 to 3). Built pose shows 2 and 9 | DERIVED |
| F3 | Graduation 0 at 43.5 | Fails at the built pose: reads 6.5 and 13.59 | DERIVED |
| F4 | "Skirt bottom" | Two skirts: the 40 mm skirt (nut z 0, reading face) and the NT7 dust skirt (z 5 to 14). Name collision caused F1 | DECLARED |
| F5 | Fixed roller radius | Cores 88.5 to 106 need contact radius 44.25 to 53.0: 8.75 mm roller travel | DERIVED |
| F6 | Plug flange sits on floor | Ramp rises 0.61 at flange r 17.5: common volume | DERIVED |
| F7 | NT4 can match NT8 | NT8 222.6 mm2, NT4 12.75; wing is 14 thick, arrow capped at 10.0 | DERIVED |

## D1 Witness: pose and probe fix, ruler unchanged

| Pose | g | Edge z | Lines visible |
|---|---|---|---|
| K-max | 1.5 | 50.000 | k 0, 1 (lower band whole) |
| K d+1 | 8.59 | 57.090 | k 0 to 8 |
| R | 13.126 | 61.626 | k 0 to 12 (upper band whole) |

Ruler stays: channel z 47.0 to 63.0, line k at 48.5 + k, bands 48.5 to 50.0 and 57.09 to 61.626. K-max k1 top 49.7 clears the edge by 0.3. Parallax at 2.5 deg is 0.49; K d+1 k9 (57.5) sits 0.41 above the edge, so counts hold inside 2 deg.

1. Renderer: nut origin z = edge; holder origin = edge + 40 - 88. Re-render the six witness PNGs.
2. Key `witness.index_face_nut_z` 0.0 (DERIVED; face annulus r 73.54 to 83.14). Append to `nut.skirt_z_lo` source: "dust skirt, not the reading face".
3. Probe `probe_witness_sight`: horizontal rays at az 127, r 200 to axis, z 44 to 64 step 0.05, nut at z 48.5 + g. Edge = lowest z whose first hit is the nut. Assert |edge - (48.5 + g)| <= 0.1 and visible line counts 2 and 9. RC6 and HD7 read `rim_top_z - 40 + g`, the ray's face.

## D2 Steady rest

r_c(d) = d/2 + `rest.roller_dia`/2 + `fit.model_contact_gap` 0.005.

| Core d | r_c | Roller outer | Pin span |
|---|---|---|---|
| 88.5 | 64.255 | 84.255 | 59.255 to 69.255 |
| 90 | 65.005 | 85.005 | 60.005 to 70.005 |
| 100 | 70.005 | 90.005 | 65.005 to 75.005 |
| 105 | 72.505 | 92.505 | 67.505 to 77.505 |
| 106 | 73.005 | 93.005 | 68.005 to 78.005 |

Keys: `rest.pose_core_d` 100 (ASSUMED), `rest.roller_r_range` [64.255, 73.005] (DERIVED, Step 9 travel 8.75), `rest.ring` [58, 100, 8]. At inner radius 62 the pin crosses the bore below d 94 and changes the face count; at 58 the pin stays inside (1.255 margin), so faces 51 and euler 13 hold. Core to ring 5.0. Roller to arm 10.84 minimum. Roller top 15, ring bottom 15.5, tower base 19.5. `rest.py`: `shape_at(p, core_d)`; `build()` uses `pose_core_d`. Topologist list per d in {88.5, 90 to 105 step 2.5, 106}: solids 1, valid, common volume with a Ø d cylinder 0.0, gap 0.005, plane y 244, bbox plain = optimal.

## D3 Nut NT4

| Key | Old | New |
|---|---|---|
| nut.glyph_length | 6.0 | 10.0 |
| nut.shaft_width | 1.6 | 2.7 |
| nut.head_width | 5.0 | 8.3 |
| nut.head_length | 3.5 | 5.8 |

Length 10.0 = wing 14 minus 2.0 walls = NT8 head length. Recess 35.4 mm2 (ratio to NT8 0.057 to 0.159). Radial window 95.64 (skirt 95.14 + 0.5) to 109.0 (tip fillet start): `xc` 102.32 (was 99.07), extent 98.17 to 106.47. `nut.py`: probe columns x0g = xc - head_width/2 - 1, x1g = xc + head_width/2 + 1; wing taper samples ra, rb = 95.7, 97.2. NT5 mirrors at the same `xc`. Span test target 10.0, tolerance 1.5.

## D5 Tray

Inner x +-277, y +-244. Floor above plate top = max(f, h): f = 3.0 + |x + 172| tan(slope), h = 3.0 + |y| tan(cross). Cavity = xz prism common yz prism. `tray.floor_slope_deg` 2.0 (3.0 gives floor 26.53 at the wall, over 25), `tray.cross_fall_deg` 2.0, `tray.fall_x` [-277, 277] replaces `ramp_x`.

| Point | Floor top | Cavity |
|---|---|---|
| x +277 | 18.68 | 6.32 |
| x -277 | 6.67 | 18.33 |
| x -172, y +-244 | 11.52 | 13.48 |

Spot face `tray.drain_spot_r` 20.0 (DERIVED), flat at z 3.0 under the plug flange (declared contact; step 0.70). Tests: slope over -172 + SCAN to 277 - SCAN; end rise 3 + 449 tan 2 deg; add west-shelf and cross-fall rows. Topologist re-predicts faces and euler.

## D6 Plug

Box lug along X: `plug.lug_length` 34, `plug.lug_width` 8, `plug.lug_height` 10, embedded 1.0 in the head. Corner radius 17.46 in head r 20. Overall height 29. Rows: overall = 3 + 2 + 14 + 10; lug L, W, H.
