## Corrections to the brief

| # | Brief, open file or test says | My number | Tag |
|---|---|---|---|
| C1 | Scale rises from the rim top, read through a nut window (A, RC6, NT9) | Skirt r 72.64 to 83.14 covers the rim top. A blade above r 72.04 blocks the descending nut; below it meets the flange and washer (height at most 9.0). A window cannot track 4.45 nut turns. Reading plane is the skirt bottom face, a full circle: z_edge = z_top - 40 + g | DERIVED |
| C2 | NT9 window | None. Nut rebuild: glyphs and skirt | DERIVED |
| C3 | Slope 3 deg over 560, depth 25 | Rise 29.3 exceeds depth. Ramp x -172 to 81 (253 mm, rise 13.26, cavity 8.74) | DERIVED |
| C4 | Tray 520 wide | Column inner faces y +-244 (488). Two 72 x 19 reliefs | DERIVED |
| C5 | Plug body inside tray.FCStd | F5 test needs solid_count 1. Own part `plug` | DECLARED |
| C6 | 16 brackets | Rail inner face needs 740 against 644; 57 mm overlap at 4 sites | DERIVED |
| C7 | `nut.arrow_length` 21.86 as length | Radial band 88.14 to 110.00; glyph is 6.0 long | DERIVED |
| C8 | Socket 3 per side on collet OD | Key tip OD 140.08; socket 146.08 | DERIVED |
| C9 | Stop frame | `stop.height_z` 184.84 is datum A | DECLARED |
| C10 | Member names | `member_plate_support_1`.split("_")[1] is "plate"; FR1 id fails | MEASURED |

## 1. Witness (RC6, HD7, NT9)

Line of sight: reader at any azimuth, eye within 2.5 deg of horizontal, looks at the receiver ruler at `witness.azimuth_deg` 127 (`receiver.key_offset_deg` + 90). Index is the nut skirt bottom face. Parallax 0.195 mm per degree (11.15 mm lever). Dust skirt (nut z 5 to 14) sits above the edge.

Ruler (receiver rebuild, one fused tool, one cut): channel width 12.0 (T), floor plane at d = `thread.minor`/2 - 0.30 = 71.99 (R), z 47.0 to 63.0. Floor is 0.05 to 0.30 below the root cylinder across the width: no tangency. Graduations: 14 lines, z = 48.5 + k, k = 0..13, height 0.4 (A), depth 0.5 (R), length 4.0 (T) centred on the azimuth, 5.2 at k = 0, 5, 10. Band strips on the left of the line (t -5.6 to -3.8), depth 0.3, over z 48.5 to 50.0 and 57.09 to 61.626 (wrong-collet bands). Digit pockets 0, 5, 10 at t +2.6 to +5.6, 3.0 high, depth 0.5, text in JSON.

Reading: gap g = z_edge - 48.5. K-max: edge 50.00, gap 1.50, on the lower zone boundary. K d+1: edge 57.09, gap 8.59, on the upper boundary. R: 61.626, gap 13.126.

Tick (holder rebuild): groove open at the flange underside, azimuth 127, tangential 1.0, radial 70.04 to 72.04 (+1 overshoot), axial 88.0 to 91.0. Lower edge = flange underside = skirt bottom + 40.0. Datum for the Step 8 feeler check with the nut off. Clear of key 37, notch 323, inserts, HD5 annulus (65.0 to 68.54).

## 2. Nut glyphs (NT4, NT5), dust skirt (NT7)

Wing 0 (+X) carries both; wing 1 is bare. The +y radial mark on wing 0 is deleted. Recess normal to the face, depth `nut.arrow_depth` 0.8, face slope 10.67 deg (z drops 6 over 31.86).

| Glyph | Face | Direction at +X | Sense from +Z | Tail to tip (y) |
|---|---|---|---|---|
| NT4 tighten | wing 0 top (+z, sloped) | -y | clockwise, direction_sign -1 | +3.0 to -3.0 |
| NT5 loosen | wing 0 underside (-z) | +y | counter-clockwise, +1 | -3.0 to +3.0 |

Shape: straight shaft 1.6 wide x 2.5 long, triangular head 5.0 wide x 3.5 long. Centre x = (83.14 + 115)/2 = 99.07. Radial extent 96.57 to 101.57, inside the band 88.14 to 110.00 (21.86). Recess covers 12 of 28 y-samples per column (probe median stays on the face). Rule P: tighten sits on the top, loosen under; a flipped nut shows the loosen arrow on top, so the flipped copy differs. JSON `radial_span` = principal span 6.0.

Dust skirt (nut z, mm): revolved polygon (r, z) = (82.14, 5.0), (95.14, 5.0), (95.14, 7.0), (83.14, 14.0), (82.14, 14.0), fused with the pads, tab, wings and bosses (1.0 embed into the body). Slope 30.3 deg. Top 2 below the wing underside (16). Floor frame at K-max: bottom z 55.0; tray rim -3 (gap 58); spigot r 80 under r 83.14. `stop.g_stop` (collar top 159.84) unaffected.

## 3. Base, tray, plug, foot (BS1 to BS7)

Partition amendment: add `plug` (own FCStd, BS6 plug). Frame: datum A, origin plate centre, X along rails.

| ID | Feature | Value (basis) |
|---|---|---|
| BS1 | plate | 644 x 608 x 12, z 0 to 12 |
| BS2 | spigot hole; drain hole | Ø160.4 at (0,0); Ø26 at (-172, 0) |
| BS3 | 8 slots, 7 x 20, long axis X, through | y +289: x -255, -90, 75, 240. y -289: x -240, -75, 90, 255 (diametral 7, centre-to-centre 20 - 7) |
| BS4 | key pockets 12 x 12 x 4 (underside) | (+-160, 259); key 11.5, 0.25 per side |
| BS4 | stop-pin pocket 10 x 14 x 4 | centre (249, 0); pin Ø6 at x 247 touches wall x 244.0 (contact intended) |
| BS4 | column notches 70 x 65 | x +-35, y 239 to 304, both edges |
| BS5 | tray 560 x 520 x 25, wall 3.0 | floor top f(x) = 3.0 + (x + 172) tan 3 deg on x -172 to 81, level outside; hole r 81.2; reliefs 72 x 19 at (0, +-260) |
| BS6 | drain bore Ø25 at (-172, 0) | plain bore, feature row names the thread (E) |
| BS6 | plug | head Ø40 x 14, flange Ø35 x 2, shank Ø24 x 3 |
| BS7 | foot 100 x 60 x 8 | M6 Ø6.6 at (30, +-15) (slot pitch 30); M8 Ø9 at x 88 (28 from rail end, over 25) |

Foot sits under the rail end (rail covers local x 0 to 60). Slots clear the notch and tray edge (25.5). Base flip mismatch 2.4e-3 against `FLIP_FLOOR` 1e-3.

## 4. Frame (FR1 to FR4)

| Member | Centre (x, y) | Extent | Stock |
|---|---|---|---|
| rail x2 | (0, +-274) | x +-322, y 244 to 304 | 644 whole piece |
| end x2 | (+-232, 0) | y +-244, x 202 to 262 | 488 whole piece |
| plate_support x2 | (+-112, 0) | y +-234, x 82 to 142 | 468 whole piece |

All z -60 to 0. Footprint 644 x 608. Supports stand 10 off each rail face; printed legs bridge it (first slot 13.9 to 24.9, margin 3.9). Support edge x 82 against spigot r 80.2 (1.8). Stock: 644, 488, 468 each 2 of 2 used, 0 left; 1540, 980, 952, 728 untouched.

Brackets (bracket width 57 centred on the 60 face, z -58.5 to -1.5): purchased at (+-202, +-244) inboard and (+-262, +-244) outboard, legs 57, plate 6, holes Ø6.6 at 13.9 and 43.1 along, +-15 across. Printed at (+-82, +-244) and (+-142, +-244), legs 68, plate 7, slots 7 wide, 10 and 11 long at 19.4 and 48.6, +-15 across. T-nut proxy (FR3): body 16 wide x 16 long x 6.0 high, neck 7.6 wide x 12 long x 2.2575 tall, hole Ø5.0, top flush with the face; stack 8.2575 against cavity floor 9.165; 16.5 against 16.0 wide. Span from corner 11.4 to 27.4, inside the support. 128 instances, 8 per bracket, ASSUMED.

C6 disposition: purchased inboard (x 145 to 202) and printed outer (x 142 to 210) overlap 57 mm at four sites, T-nuts included. Pass 1 builds 16 and logs the overlap; Step 7 (owner Engineer) cuts brackets or lengthens rails.

FR4: rail_1 notch, x -322 to -292, y 249 to 269, z -2.0 to 0 (T-slot line y 259). Solid removed (20 - 8) x 30 x 2.0 = 720 mm3; flip mismatch about 2.4e-3.

## 5. Accessories and stop

| ID | Value |
|---|---|
| AC1 caddy | 628.3 x 299.5 x 46. Sockets Ø146.08 x 40, rows of 4 and 3, pitch 154.08 (web 8), row spacing 133.4, border 10, floor 6. Size label recess 30 x 8 x 0.8 at each socket front, text in JSON |
| AC2 gauge | plug Ø134.08 x 150 (2 x 67.29 - 2 x 0.25), key 11.75 x 3.0 x 40 at 37 deg, cavity Ø110 x 130 from below, handle bar 160 x 25 x 25 on top |
| AC3 rest | local z 0 = roller plane (310 above the seat). Block 60 x 30 x 60, interface plane y +244 (normal -y, column face); hinge boss Ø40 at y +200; arm 20 x 24 to the ring; C-ring r 62 to 100 x 8 (z 15.5 to 23.5), mouth 90 deg centred -X; rollers Ø40 x 30 at r 70, azimuth 0, 120, 240, pin Ø10 (0.5 gap, pin bridges); close handle Ø20 x 120 on the arm; detent notch 4 deep in the boss at 90 deg swing; tower 14 x 16, inboard face r 84, top at z 250 (= 560 = L + 60) |
| ST1 stop | pad 60 x 60 x 12, z 172.84 to 184.84, centre (0, 214), owner `upper assembly`, interface record in JSON, zero nut volume |

Columns stand at x 0. Pass 1 is the closed pose; mouth retraction is the linkage (Step 9).

## 6. Conflicts by arithmetic

Skirt vs tray: 58, clear. Released rest vs keepout 86.2 and 125: nearest 182.8, clear. Tray vs column: reliefs. Caddy stands off the jig. Brackets: C6. Drain vs support and end: 17.5, clear.

## 7. New params keys (all ASSUMED unless marked; basis in the section named)

| Keys | Values |
|---|---|
| witness.azimuth_deg | 127 (key_offset_deg + 90) |
| witness.channel_width, channel_floor_depth, line_height, line_depth, band_depth | 12.0, 0.30, 0.4, 0.5, 0.3 (section 1) |
| witness.tick_width, tick_depth, tick_height | 1.0, 2.0, 3.0 |
| nut.glyph_length, shaft_width, head_width, head_length | 6.0, 1.6, 5.0, 3.5 |
| nut.skirt_r_out (DERIVED, body R + 12), z_lo, z_hi, rim, embed | 95.14, 5.0, 14.0, 2.0, 1.0 |
| base.slot_centres, key_pocket_xy, pin_pocket_xy, drain_xy, column_notch | section 3 values |
| base.key_pocket_size, pocket_depth, pin_pocket_size, drain_hole_dia | 12, 4, 10 x 14, 26 |
| tray.wall, floor_min, ramp_x, hole_r, relief | 3, 3, (-172, 81), 81.2, 72 x 19 |
| plug.head_dia, head_h, flange_dia, flange_t, shank_dia | 40, 14, 35, 2, 24 |
| foot.size, m6_xy, m6_hole, m8_x, m8_hole | 100 x 60 x 8, (30, +-15), 6.6, 88, 9 |
| tnut.body, neck, hole | 16 x 16 x 6.0, 7.6 x 12 x 2.2575, 5.0 |
| frame.end_x, support_x, notch | 232, 112, 20 x 30 x 2 |
| bracket.holes_purchased, slots_printed | 13.9 and 43.1, 19.4 and 48.6 |
| caddy.web, border, floor | 8, 10, 6 |
| gauge.cavity | 110 x 130 |
| rest.ring, roller_r, pin, mouth_deg | 62 to 100 x 8, 70, 10, 90 |
| stop.pad_thickness, pad_xy | 12, (0, 214) |

## 8. Test conflicts, smallest edit

1. `test_RC6_scale_graduation_count_and_pitch`: last assert uses `marks[0] - (w["rim_top_z"] - K("nut.skirt_below_flange"))`. Probe `witness()`: radii 71.6, 71.75, 71.9; z window from rim_top - 40.5.
2. `test_HD7_tick_reads_the_zone_edge_at_the_built_pose`: pass `w["rim_top_z"] - K("nut.skirt_below_flange")` as the rim argument. Probe `tick_local_z` = lowest z of the mark cluster (cluster centre reads 89.5).
3. Probe `frame_probe`: id = `o.Name[7:].rsplit("_", 1)[0]` (C10). `flip_mismatch` rotates about the world X axis; members need their own centre line (rails at y +-274 read 1.0).
4. Probe `surface()`: line span y +-150 to +-20; tommy bosses at 45 + 90k fake glyphs.
5. Section 7 keys must exist before the tests run.

## 9. Self-check (python)

Footprint 644 x 608; notch 720 mm3; ruler floor 0.05 to 0.30 under root; glyph inside the 21.86 band; ramp 253, cavity 8.74; tower 560 = 500 + 60; caddy web 8; base flip 2.4e-3. Only tangency: pin wall x 244.0 (declared contact); other tool faces carry `collet.tool_overshoot` 1.0 or an embed.
