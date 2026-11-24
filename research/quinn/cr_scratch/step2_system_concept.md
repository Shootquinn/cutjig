## System concept (Detail 2). Nine decisions. Governing numbers: Loftsman cross-review reply.

Status tags: D declared, A assumed, V derived. Every decision names its checking test. A test that cannot fail on a wrong value does not count.

**1. Closed force loop.** The clamp force closes inside the receiver assembly and nowhere else. Chain, ten members: nut thread flank, nut clamp shoulder, washer, holder bearing flange, holder cone, collet cone, collet foot ring, receiver floor seat, receiver wall in tension, receiver thread flank, then back to the nut thread flank. The nut thread flank starts and closes the chain; it is not an eleventh member. Base plate, frame and upper assembly carry none of it; the receiver underside force on the base plate is 0 (A6a computes it). Stroke stop: the collet foot ring top (z 2.00) is the declared stop of the holder. Pair holder bottom to ring top: gap 11.626 (R), 7.089 (K at core d+1), 0.00 (K-max, core d-1.5); class C at K-max only (limit contact at the window floor), class G elsewhere. At contact the force enters ring and floor seat in parallel with the cone, so grip stops rising there. The holder rim is not a stop: flange underside to rim, class G, 13.126 (R), 8.59 (K at d+1), 1.5 (K-max), never loaded. Holder bottom to receiver floor, class G, 2.00 at K-max. The earlier "0.50 after margin" is withdrawn. Axial force about 267 N plain, 388 N PTFE at 12 N m nut torque (V). Checks: A3e (holder bottom above receiver floor), A3h (nut clamp shoulder bears on the washer, 1 pitch of travel left), A3i (engaged length at least 24 mm in every pose), A1a (pair table including the ring pair), F6, S6, T4, T5, A6a (receiver underside force 0), A6b (WS8, ledge at z 2.00, corrected), A6c (WS9).

**2. Release.** Captured-flange nut, cone half-angle 10 deg (self-lock tan 10 = 0.176 < mu_k,min 0.25). Ruling by the Loftsman: the releasing cone (20 deg) is retired. It misses 10 N m at d = 90 even with PTFE inside a 12 N m hand limit (10.72 and 9.19 N m) and costs +11.26 mm of thread major. Release path: nut backs off lift play p = 0.75 mm, plate top meets collar underside (n.n = -1), the collar lifts the holder. Jacking holes are deleted (flange annulus 5.00 mm against 7.4 required, and they sat under the plate). The jacking provision is the collar back-off lift: 281.5 N at 12 N m against a release need of 46, 88, 128 N at mu_k 0.25, 0.35, 0.50. Minimum ratio 2.20 (V, from A friction). Checks: A3a (cone angle above atan(mu_max) or capture), T1c, H5 (physical).

**3. Load cases.** (a) Torque 10 N m (D), no factor. Lateral 100 N (A) at 106.4 mm or more above the holder: 10.6 N m (V). Grip couple over a 30 mm grip is 354 N edge force against about 500 N total clamp normal, so an unguided core uses most of the clamp. (b) Core weight at d = 105, 2400 kg/m3 (A): 10.4 kg (102 N) at 0.5 m, 15.6 kg (153 N) at 0.75 m, 20.8 kg (204 N) at 1 m. Path: core stop, collet foot, floor seat; floor stress about 2.3 MPa. (c) Cutter descent 1000 N (A): cutter, carriage, metal stop, columns, frame. It never enters the nut, holder, collet, receiver or base plate. Hold test H3 is raised from 10 N to 21.2 N at the top of a 0.5 m core (or 100 N at 106 mm) so it loads the holder to 10.6 N m, not 5 N m. Checks: T7 (prediction, counts only if r_p, r_bm and lambda are read from the final threads), A3c, A3f, F2, F4, A2c, A1c; physical: H1, H3 (21.2 N), H2 (pull at 2 x weight: 204 N at 0.5 m, 306 N at 0.75 m), H8.

**4. Holding capacity.** Required 10 N m. Predicted with a PTFE washer always fitted (adopted design response): 15.47 N m at d = 105 and 13.26 N m at d = 90, nut torque 12 N m, hand force 52 N per hand on a 230 mm wing span. Margin 33 percent at d = 90. Plain printed washer: 10.65 and 9.13 N m. It misses 10 N m at d = 90 by 8.7 percent and I claim no margin on it. The washer is a separate part: ID 136.8, OD 143.2, thickness 1.3 (A), pocket r 68.3 to 71.7. Other responses kept: TPU or silicone core liner (mu_c 0.40 to 0.70, A), tommy-bar socket, wing span as a parameter. No positive lock. These are predictions from assumed coefficients (spread at d = 90: plain 3.8 to 23.1, PTFE 5.8 to 31.0 N m). H1 is the authority; a miss over a factor 2 is a change order. Checks: T7 (prediction), T5, C9; physical: H1, H4.

**5. Tolerance budget.** Table below. Datum scheme: A frame top plane; C a frame slot line, with two plate keys (T-nuts with square keys) in the rail slot line, one each side of the receiver, whose two spaced contacts remove rotation and translation across the slot, and a plate stop pin (6 mm dowel in a T-nut) in the crossing slot line of an end member, bearing on a plate edge, fixing translation along the slot: plate on A removes 3, keys 2, pin 1, six in all. Every part located to C is located by two spaced contacts along its slot line: two plate keys, and each column foot abutting the end-member stop line, bearing on the frame and not through the printed plate (A1d); B the axis of the receiver register bore (r 67.29), one feature of one part, located to A and C through the plate (plate on A, key in C, receiver spigot in the plate hole). B is then transferred to the core by the holder pilot and the collet cone, never by the trapezoidal thread. The nut is not a locating member; its 0.30 thread play enters only the flange clearance. Receiver floor is 40 mm above datum A (`icd.floor_above_datum_a`, A; one parameter, the Detail 2 floor plane and ICD datum A are offset by it). The 1.0 mm coaxiality (drill axis to B) is bounded in both in-plane directions by the chain in the table; the along-slot clearance is carried by the stop pin entry. A3b measures the built clearances, it does not add assumed numbers. Iris slack by the rule core diameter + tol < throat: throat 108.585 mm nominal (A: a parameter), slack per side (108.585 - 106) / 2 = 1.29 mm at 105 plus tolerance, 3.79 mm at 100 mm, 8.79 mm at 90 mm. The 90 to 105 range is not cut on aperture grounds. Checks: P8, C3, T3, T9, A3b, A3c, A3d; physical: H3.

**6. Interface control table.** Frozen below. Checks: P6a, A1c, A2a, A2b, A2c, F4.

**7. Collet family.** Seven collets, 90 to 105 mm at 2.5 mm (D). Accepts d - 1.5 to d + 1.0 (window 2.5, centre d - 0.25); coverage 88.5 to 106.0, windows abut, against the widened core range 89 to 106. Free bore d + 2, window d - 1.5 to d + 1.0, 12 slits at 1.5 mm, clamped slit 0.584. Generator envelope 85.0 to 106.585 mm. The cap governs: the "85 to 110 mm" text in Detail 5 is the build range and reads "85 to min(110, throat - tol - slack)"; a request above 106.585 is refused with "change `iris.throat_open_radius`". Custom collets are a generator argument. Checks: P1, P8, C4, C8, C9, C10.

**8. Hard stop.** Two things carry that name; they are separate. (i) Metal descent stop: owner is the upper assembly (D, B5); the nut is never a stop. It carries the 1000 N descent load. (ii) Holder stroke gap: holder flange to receiver rim, 1.5 mm minimum in K, a base-side gap that is never loaded. Rename F6 and key `stop.hard_stop_gap` to "holder stroke gap" and `holder.stroke_gap_*`. Only (i) is called "hard stop". Checks: A2b, A2c, F4, P6c for (i), H8 physical; F6, S6 for (ii). The drill to core pair is class F at the stop with axial force 0 (A2d: common volume of the cutter, iris and lead-in solids with the core at the stop is 0 except the open throat band), so the 1000 N never enters the collet.

**9. Stability, handling, height.** Frame stock-driven: rails 644, ends 488, plate supports 468: 3200 mm at 2.573 kg/m = 8.2 kg. Footprint 644 x 608 mm; four adjustable M8 feet with four bolt-down slots in the rails (M6 T-nuts, 30 mm pitch). Mass (A, drill mass appears in no source read): frame 8.2, brackets 1.4, printed base 4, two 1540 columns 7.9, upper assembly 15: 36.5 kg; target 40 kg with the upper assembly, structure alone at most 25 kg. Centre of mass about 0.69 m above the floor at the top of travel (V). Tip-over: unbolted, static tilt 23.8 deg about the 608 side; a horizontal push of 158 N at the centre of mass, or 68 N at the column top (1.6 m), tips it. The 100 N core lateral at 0.3 m has a factor 3.6. The 68 N margin at the top is thin, so the design response is bolt-down as the operating condition with the cutter above z = 400 mm: 140 N m overturn from 100 N at 1.4 m gives 115 N per bolt on a 608 mm couple, within M6 in 30 series T-nuts (A). Step 12 replaces this with its own number. Core handling: the steady rest is used at every core length, 0.5 m included. A 10.4 kg core in a bore with 1 mm per side tips freely (about 1.9 deg) while two hands turn the nut; the rest holds it so the sequence never needs more than two hands, and it is closed during clamping so the core pose is fixed before the collet locks. Rest: a swing-away arm with three linked rollers (a self-centring linkage, not three independent rollers) centring to plus or minus 0.25 mm of datum B, two positive detents on the frame at 310 mm (0.5 m) and 560 mm (0.75 m) above the seat, a one-handed large closing handle and a hold-open detent. The release is mechanical, not procedural: a cam lug on the upper assembly, flush with the cutter lowest point (it projects nothing below it, radius 95 mm), meets a 250 mm trip tower on the rest arm and pushes the arm out to a radius of at least 125 mm (30 mm outside the lug) when the cutter lowest point is 60 mm above the core top, before the lead-in touches the core. The tower top is at core top + 60 (600 mm at 0.5 m, 850 mm at 0.75 m); nothing of the upper assembly goes below the cutter lowest point, so only the metal stop bears at the stop. Lifting: the 0.75 m core (15.6 kg, 153 N, top at about 790 mm) is carried and lowered on a choke strap with a rigid side handle projecting 250 mm radially at 0.55 L, held by one hand from the side, plumb, while the other hand works the rest. There is no overhead anchor: the parked cutter and drill body occupy every vertical line over the axis from z 950 up (a rope from an anchor 300 mm off axis at z 1600 to the core top crosses z 950 at 21 to 59 mm from the axis, inside the 88.9 mm cutter radius), so an overhead strap point cannot exist; this replaces the earlier M6 eye and rope-and-block. Strap rated 80 kg (4 x the 20.8 kg core), proven by physical test H10. Columns stand on the rail centrelines, 548 mm centre to centre (A, rails at y = plus or minus 274), leaving 488 mm clear between columns for the drill body. The collet bore has a lead-in chamfer sized per collet to wall minus 1.2 mm minimum wall (3.8 mm at d = 105, 11.3 at d = 90; 1.5 mm x 45 deg is the floor); the 10 mm capture radius belongs to the upper-assembly funnel (U12) only. Parking for loading: the cutter parks at 950 mm (row U13), a loading position and not working travel, so a core of either length clears it. Height: 2 m is soft, recorded and reported (frame 60 + columns 1540 = 1600 mm before overhang), not tested. Upper assembly working stroke at most 500 mm (D, governs `upper.travel_max`); the park is separate (row U13). Checks: P6b, P6c, P6d, A1b, A1c, A1e, A2e, A2f, A2g; physical: H7 (handling), H9, H10.

**Items from my draft, resolved.**
- 500 mm core: it needs 534.93 mm of drill advance (500 + 34.93 dome offset) against the 500 mm ceiling. The ceiling holds. One stroke delivers 500 - 34.93 = 465.07 mm of retained core. The upper-assembly step must report the captured length as `upper.captured_length` 465.07 and size nothing for 535. If the human wants a full 500 mm retained, the single change is `upper.travel_max` 535; I do not make it.
- Cutter-start range: the stop height moves with core length so the stroke stays 500. Core top about 790 mm at 0.75 m gives `stop.start_z` at least 800 mm and `stop.height_z` 300 mm (660 and 160 mm for the 0.5 m case). Range for the adjustable start: 660 to 800 (0.75 m), with 1060 at 1 m. A 1 m core is not a design case: with a 1540 mm column the drill body above the cutter's lowest point would have to be 480 mm or less.
- H3 and the 85 to 110 text are fixed in decisions 3 and 7.

**Defects found while writing.** (1) Tilt: clamped tilt 0.57 deg gives a core-top offset of 5.0 mm (0.5 m) and 7.5 mm (0.75 m) against iris slack of 1.29 mm at d = 105. The core cannot reach the throat unguided. Response: upper-assembly funnel lead-in (U12), capture radius 10 mm, which seats the core top into the clamp play once and then clears it. (2) `hardware.bracket_sku` 30-4332 has A = B = 30 mm legs; that is below the full-size rule and is superseded. (3) The 1.0 mm coaxiality budget plus the 0.805 mm core offset exceeds slack by linear sum (1.805 against 1.29); with the lead-in the throat check uses 0.25 + 0.25.

**Bracket choice rule.** Full-size only, chosen per joint, hand-friendly. Minimum leg 57 mm and width 57 mm (the 8020-14089 class; the human's printed bracket is 68 mm legs, 57 wide, 7 mm plate, slotted 7 mm holes at 30 mm pitch, clearing M6). Eight joints: the four outer corners take the 57 mm 8020-14089 class, two per joint; the four plate-support ends take the 68 mm printed bracket where the 57 mm bracket collides with an M6 head. Access: each fastener head has at least 25 mm of clear radius for a 150 mm hex key swing, measured on the assembled solids (test A1b). No mini brackets.

### Tolerance budget (core axis to datum B, then to iris throat)

| Entry | Value (mm) | Kind | Test |
|---|---|---|---|
| Register fit, holder in receiver bore (g_reg) | 0.25 radial | pilot, A | T9 |
| Holder cone to collet cone, clamped | 0.005 | V | C3 |
| Slit non-uniformity | 0.15 | A | C9b |
| Core out-of-round, centre shift | 0.25 (half of core tol 1.0, A) | A | T3 |
| Collet bore print error | 0.15 (A) | A | C3 |
| Core axis offset at collet, linear / RSS | 0.805 / 0.41 | V | A3c |
| Nut thread lateral play + register | 0.30 + 0.25 = 0.55 (flange clearance only, not core location) | V | A1a |
| Register-limited tilt, seated / hanging | 0.597 / 0.588 deg; plate rock 0.315 deg | V | T9 |
| Total tilt at first thread contact | 0.903 deg against line 1.021 (alpha_crit 1.532 / 1.5) | V | T9 |
| Clamped core tilt over 30 mm contact | 0.57 deg; offset at core top 5.0 (0.5 m), 7.5 (0.75 m) | A | A3f |
| Coaxiality chain, datum B to drill axis: plate key in rail slot line C (across slot) 0.25, plate stop pin (along slot) 0.20, radial 0.32 | 0.32 | A | A3b |
| Receiver spigot in plate hole | 0.20 | A | A3b |
| Column foot on frame slot line: across 0.20, along (abutting the end-member stop line) 0.20, radial 0.283 | 0.283 | A | A3b |
| Carriage guide to drill axis | 0.15 | A | A3b |
| Chain total, linear: 0.32 + 0.20 + 0.283 + 0.15 (budget `icd.coaxiality_budget` 1.0, margin 0.05) | 0.953 | V | A3b measures the built fits |
| Lead-in residual at throat (stage: after the funnel has seated the core, before the iris closes) | 0.25 + 0.25 | A | A3d |
| Iris slack per side at 105 + 1.0 / 100 / 90 | 1.29 / 3.79 / 8.79 | V | P8 |
| Slack at envelope max 106.585 + 1.0 | 0.50 per side (1.00 diametral) | V | P8 |

Check at d = 105: lead-in 0.50 against slack 1.29, margin 0.79 mm. Without the lead-in the check fails (tilt 7.5 + 1.0). The collet bore print error row is assumed; the printed hardware value arrives from the Step 8 coupon. Tests C3, T3 and C9b are min-distance or common-volume predicates on the built collet and core envelope, not a restatement of the 0.15 or 0.25 entries; a wrong entry must fail them.

### Interface control table (frozen)

| Row | Value | Key | Test |
|---|---|---|---|
| Datum A | frame top plane, z = 0; receiver floor 40 mm above it | `icd.datum_a`, `icd.floor_above_datum_a` | no test (definition) |
| Datum B | axis of the receiver register bore (r 67.29), +Z | `icd.datum_b` | A3b |
| Datum C | rail slot line with plate key (rotation, across-slot) and end-member stop pin (along-slot) | `icd.datum_c` | A3b |
| Mounting | T-slot lines, 30 mm pitch, M6 roll-in T-nuts; slot centres 15 mm off centreline | `icd.mounting_pattern` | no test (definition) |
| Coaxiality | 1.0 mm budget; chain 0.32 + 0.20 + 0.283 + 0.15 = 0.953 | `icd.coaxiality_budget` | A3b |
| Keep-out radius | 86.2 mm, collar top to stroke end | `icd.keepout_radius` | A2a |
| Stop rating | 1000 N axial | `icd.stop_rating` | A2c |
| Stop gap g_stop | 10 mm minimum, collar top (wings included) to cutter lowest point, taken at the highest clamped nut position | `stop.g_stop` | A2b; H8 physical |
| Collar top z | 150 mm seed (placeholder; A2b computes the maximum over clamped poses plus g_stop, about 170 mm at floor 40 mm; Step 3 fixes) | `stop.collar_top_z` (was `stop.nut_top_z`) | A2b |
| Stop height H_stop | 160 mm at 0.5 m core; 300 mm at 0.75 m (seeds, recomputed by A2b) | `stop.height_z`, `stop.height_range` | A2b per class |
| Travel | 500 mm; start_z 660 (0.5 m), 800 (0.75 m) | `upper.travel_max`, `stop.start_z` | P6c |
| Exposed core | at least 128.12 mm above the plate top (collar top is 6.75 above plate) | `core.min_exposed` | F4 |
| U12 Core lead-in | a funnel, not a guide: capture radius 10 mm; it seats the core top once (centring plus or minus 0.25 mm to the drill axis, using the 0.30 clamp play), then the working bore radius is 56.0 mm, at least (d+1)/2 + 1.0 + 0.805 + 0.25 = 55.06 for all seven d, so core to lead-in distance is above 0 for the whole stroke and no lateral loop closes through the receiver. Order: rest cam releases at cutter lowest point = core top + 60; funnel touches the core top at +0; loop opens 40 mm below first touch where the bore steps to 56.0. At no instant do rest and funnel both hold the core | `icd.core_lead_in_capture`, `icd.core_lead_in_bore` | A3d (clearance, all seven d), A3g (capture radius), A2e |
| U13 Park and load position | two separate numbers. Working stroke: at most 500 mm (start_z 660 or 800 down to the stop, `upper.travel_max`). Loading park: cutter lowest point 950 mm, reached only by the manual raise (U15) and held by a metal pin latch above the working range (above start_z 800), visible locked flag. Carriage range stop to park is about 780 mm (170 to 950); the 780 is not working travel. 950 = core top while lowering (core bottom at the collar top 150 + 750 = 900) + 50; seated 0.75 m core top 790, clearance 160; 0.5 m loads at 650 | `upper.park_z`, `upper.park_lock`, `upper.travel_max` | P6c (working stroke), P6d (park envelope); H9 physical |
| U14 Core carry strap | choke strap with rigid side handle 250 mm radial at 0.55 L, rated 80 kg; no overhead anchor (the parked drill occupies the vertical lines over the axis). Column centres 548 mm apart (rail centrelines), 488 mm clear | `strap.rating` 80 kg, `strap.handle_radial` 250, `column.spacing` 548 | A1e (handle at carry position clear of the parked envelope); H10 physical |
| U15 Manual raise | one person raises the upper assembly from the stop to park with the drill unpowered: ratchet hoist, hand force at most 80 N (A), raise at least 100 mm to expose the wings. Anchor: a stock 728 mm 30-6060 cross member across the two column tops, metal brackets at both joints (joints 8 to 10), hoist hook on it. Load path: carriage, hoist, cross member, columns, frame; no printed part. Fuse: a shear link in the hoist line at 300 N rope tension (147 N carriage weight + 150 N jam force), so a jammed cutter pulls the core with at most 150 N, below the 204 N pull proven by H2; above that the link fails and the printed collet, receiver and base plate see nothing more | `upper.manual_raise`, `upper.raise_fuse` 300 N, `hoist.anchor_member` | A2h (raise path has no printed member); H9 physical (jam trial, drill unpowered) |
| U16 Steady rest | used at every core length; arm detents 310 and 560 mm above the seat; three linked rollers, repeatability 0.25 mm; cam-released: the lug on the upper assembly is flush with the cutter lowest point (radius 95) and trips a 250 mm tower on the arm; released arm and tower at radius 125 or more, 30 mm outside the lug | `rest.height_positions`, `rest.roller_count`, `rest.centre_repeatability`, `rest.release_tower` 250, `rest.cam_lug_radius` 95 | A2e, A2f, A2g, A1b |
| Column feet | on frame slot lines, abutting the end-member stop line (frame, not plate), never on the base plate; foot moment 100 N m (A) | `icd.column_foot_moment` | A1c, A1d; Step 12 |
| Torque reaction | drill torque not carried by the base | `icd.torque_reaction` | A2c |
| Cable and debris | back cap through upper assembly clear of r = 86.2; tray in base; dust skirt on nut | `icd.cable_exit` | A2a |
| Footprint | 644 x 608 mm | `icd.footprint_x`, `icd.footprint_y` | P6b |
| Mass target | 40 kg with upper assembly, 25 kg structure | `icd.mass_target` | H7 physical (scale) |
| Height | 2000 mm soft, not tested | `jig.height_target` | none |

### Test ID key (one predicate per ID, from final shapes unless marked physical)

| ID | Predicate |
|---|---|
| A1a | every pair in the contact-class table holds its class (G min distance > 0, C contact, F free) in poses R, K d+1, K-max; includes holder bottom to ring top |
| A1b | each fastener head has 25 mm clear radius and a 60 deg sector for a 150 mm key, on assembled solids |
| A1c | no printed solid lies in the column-foot path to the frame |
| A1d | column-to-base-plate pair is class G or F |
| A1e | the carry-strap handle at its carry position has zero common volume with the parked upper assembly envelope |
| A2a | common volume of any frame, rest (released) or cable solid with the keep-out cylinder r 86.2 is 0 |
| A2b | cutter lowest point at the stop is at least g_stop above the highest collar top over clamped poses and all seven collets |
| A2c | stop and torque-reaction path contains no nut, holder, collet, receiver or base-plate member |
| A2d | no cutter, iris or lead-in face bears on the core at the stop |
| A2e | released rest arm and tower stay at radius 125 or more |
| A2f | cam lug lowest point is not below the cutter lowest point, so the swept volume of the upper assembly to the stop has zero common volume with any printed solid, base plate and wings included |
| A2g | released arm and tower have zero common volume with the cutter and lug swept volume |
| A2h | the manual-raise path (hoist, cross member, columns, frame) contains no printed member |
| A3a | cone half-angle above atan(mu_max), or the plate-collar capture pair exists |
| A3b | measured built fits (key to slot, pin to slot, spigot to hole, foot to slot, guide to rail) from final shapes; their chain total is at most 1.0 |
| A3c | core axis offset at the collet at most 0.805, min-distance on the built collet and core envelope |
| A3d | lead-in working bore radius minus core radius at least 2.055 for all seven d |
| A3g | funnel capture radius at least 9.31 |
| A3e | holder bottom above the receiver floor in every pose |
| A3h | nut skirt bottom is at least 1 pitch above the receiver floor in every pose |
| A3i | engaged thread length at least 24 mm in every pose |
| A6a | receiver underside force on the base plate is 0 |
| A6b | WS8 planted state (holder on the ring ledge at z 2.00) fires |
| A6c | WS9 planted state (nut bottomed on base) fires |
| A3f | clamped tilt at most 0.573 deg from collet and core envelope |
| P6a | document check, not a shape test, outside Rule M: ICD has no empty field |
| P6b | frame solids measure 644 x 608 |
| P6c | working stroke (start_z minus stop height) at most 500 |
| P6d | park envelope clears the core in both lengths (core top 650 and 900 plus 50) |
| H1 to H4, H5, H7 to H10 | physical measurements (torque wrench, force gauge, scale, hand trial), outside Rule M. H1 hold torque; H2 pull-out; H3 side load 21.2 N at the top of a 0.5 m core; H4 creep; H5 cold-user release; H7 mass and handling; H8 stop gap trial, and the funnel seating force through the collet must not exceed the lateral load H3 takes; H9 jam recovery with drill unpowered, fuse trip at 300 N, and park latch; H10 carry strap proof pull at 80 kg |

T7 is a prediction from assumed coefficients; it informs, it does not pass a requirement. IDs T1c, T4, T5, T9, F2, F4, F6, S6, C3, C4, C8, C9, C10, P1, P8, A6 are defined in the CAD Test Specification and not restated here.

### Absorbed at Step 3 or 5

- Witness scale: rim rule in 1 mm steps with zone and wrong-collet bands from the stroke gap (7.09 mm per family step); colour, notch count and caddy per collet.
- Wing grip: wing height 30 mm or more, knuckle clearance 50 mm, sweep clear radius 115 mm, turns to clamp reported.
- Hex-key swing sector: 60 deg, already the A1b predicate; knobs or T-handles on rest, stop and feet.
- Tommy-bar abuse torque: `loads.nut_torque_abuse` 25 N m checked on the ten members; bar length sized so a hand gives at most 15 N m.
- Captive washer: washer retained in the nut face, visible gap when absent, H1 with and without.
- Nut-top travel: `stop.nut_top_z_min` and `_max` replace the single value; A2b runs at the highest.

## DECISIONS FOR SIGNATURE

1 Closed loop (ten members including the washer; ring is the holder stop, rim is not). 2 Release: 10 deg captured-flange nut, collar back-off lift, no jacking holes. 3 Load cases (10 N m, 100 N lateral at 106.4 mm, core masses, 1000 N descent, H3 at 21.2 N). 4 PTFE washer fitted; plain washer misses at d = 90 by 8.7 percent. 5 Tolerance budget and datum scheme. 6 Frozen ICD. 7 Family and 106.585 mm cap. 8 Hard stop: upper assembly; holder stroke gap renamed. 9 Stability, bolt-down, handling (steady rest at every length, choke strap with a 250 mm side handle, no overhead strap point), 465 mm captured length, soft height.

## LINES FOR INTEGRATION

ASSEMBLY.md: "The clamp force closes inside the receiver assembly and nowhere else: nut thread flank, nut clamp shoulder, washer (PTFE or printed), holder bearing flange, holder cone, collet cone, collet foot ring, receiver floor seat, receiver wall in tension, receiver thread flank, back to the nut thread flank (ten members). The base plate, frame and upper assembly carry none of it; the receiver underside force on the base plate is 0. The holder stroke ends on the collet foot ring top; the gap between holder flange and receiver rim is the holder stroke gap and is never loaded. Hard stop means the metal descent stop owned by the upper assembly."

params.yaml (key: value, status):
- `thread.major`: 149.58, DERIVED
- `wingnut.body_od`: 166.28, DERIVED
- `holder.flange_od`: 144.08, DERIVED
- `holder.length`: 88.0, DERIVED
- `receiver.rim_above_floor`: 88.5, DERIVED
- `nut.lift_play`: 0.75, ASSUMED
- `holder.stroke_gap_R`: 13.126; `holder.stroke_gap_min_K`: 1.5; delete `stop.hard_stop_gap`
- `holder.jack_hole_*`: delete
- `collar.od` 152.4, `collar.id` 114.0, `collar.top_above_plate` 6.75
- `washer.material`: PTFE; `washer.id` 136.8; `washer.od` 143.2; `washer.thickness` 1.3 (ASSUMED)
- `core.min_exposed`: 128.12, DERIVED
- `core.mass_kg_d105`: [10.4, 15.6, 20.8], DERIVED
- `loads.lateral`: 100 N, ASSUMED; `loads.lateral_moment`: 10.6 N m, DERIVED; `loads.h3_side_load`: 21.2 N
- `upper.captured_length`: 465.07, DERIVED; `upper.drill_advance_500core`: 534.93, DERIVED
- `stop.height_range`: [160, 300] for 0.5 and 0.75 m; `stop.start_z`: 660 (0.5 m), 800 (0.75 m)
- `icd.core_lead_in_capture`: 10; `icd.core_lead_in_centring`: 0.25; `icd.core_lead_in_bore`: 56.0 (A)
- `icd.floor_above_datum_a`: 40, ASSUMED; `icd.coaxiality_chain`: [0.32, 0.20, 0.283, 0.15]; `column.spacing`: 548
- `upper.park_z`: 950; `upper.park_lock`: positive mechanical, flagged; `upper.manual_raise`: ratchet hoist, 80 N, 100 mm minimum; `upper.raise_fuse`: 300 N; `hoist.anchor_member`: 728 mm 30-6060 across the column tops
- `rest.height_positions`: [310, 560]; `rest.roller_count`: 3; `rest.centre_repeatability`: 0.25; `rest.release_tower`: 250; `rest.cam_lug_radius`: 95
- `strap.rating`: 80 kg; `strap.handle_radial`: 250; `stop.collar_top_z` replaces `stop.nut_top_z`
- `stop.g_stop` reference: collar top (wording change)
- `icd.mass_target`: 40 kg; `icd.tipover_statement`: "unbolted tip force 158 N at COM (0.69 m), 68 N at column top; bolt-down required with cutter above z = 400 mm"
- `icd.column_foot_moment`: 100 N m, ASSUMED; `icd.torque_reaction`: "not carried by the base"
- `hardware.bracket_leg_min`: 57 mm, DECLARED by the gate rule; retire `bracket_sku` 30-4332 (30 mm legs)
- `collets.envelope_max`: 106.585, DERIVED (unchanged, stated)

## Revisions

- Decision 1: chain now ten members (washer added, foot ring replaces foot); foot ring top declared the holder stop (class C at K-max, G elsewhere); rim gap class G never loaded; "0.50 after margin" withdrawn; receiver underside force 0; checks A3e, A1a, WS8 corrected.
- Decision 2, 3, 4 check lines: IDs suffixed (A3a, A3c, A3f, A2c, A1c), H-series marked physical, T7 marked prediction.
- Decision 5: datum B redefined as the receiver register bore axis, located through plate key in slot line C and spigot; floor 40 mm above datum A; coaxiality 1.0 as a four-entry chain; checks A3b, A3c, A3d.
- Decision 6 checks: P6a, A1c, A2a to A2c, F4.
- Decision 7: grip window d-1.5 to d+1.0, coverage 88.5 to 106.0 (Loftsman W-1).
- Decision 8: checks split (A2b, A2c, P6c, H8 physical); drill to core pair A2d added.
- Decision 9: steady rest at all lengths, linked rollers, detents 310 and 560, cam release by the upper assembly; M8 eye replaced by an M6 eye on a 728 mm column-top cross member with 2:1 rope-and-block; collet funnel chamfer; park at 950; checks P6b, P6c, A1b, A1c, A2e, H7, H9, H10.
- Defects line (1): lead-in described as a funnel that seats then clears.
- Tolerance table: slack at envelope max 0.50 per side, 1.00 diametral (W-2); coaxiality chain rows added; test IDs A3c, A3f, A3d; predicate note for C3, T3, C9b.
- ICD table: datum rows (B bore, A and mounting marked no test); g_stop reads from the collar top; stop and nut rows renamed collar top, IDs split; U12 rewritten as funnel with handoff order; U13 park, U14 strap anchor, U15 manual raise, U16 steady rest added; remaining rows re-IDed.
- New sections: Test ID key, Absorbed at Step 3 or 5.
- Integration lines: ASSEMBLY.md sentence now ten members with ring stop and zero receiver underside force; params additions for floor offset, coaxiality chain, lead-in bore, park, manual raise, rest, strap, g_stop reference.
- Open flag, not changed: collar-top reference moves the stop seed from 160 to about 170 mm at floor 40 mm; A2b computes it and Step 3 fixes it.

### Revisions, second pass

- Decision 9 collet line: lead-in chamfer is wall minus 1.2 (3.8 mm at d = 105, 1.5 x 45 deg floor); the 10 mm capture belongs to the upper-assembly funnel only (Loftsman).
- Decision 9 strap: the overhead anchor is withdrawn. A strap from an anchor 300 mm off axis crosses the parked drill at 21 to 59 mm from the axis. Replaced by a choke strap with a 250 mm side handle; column spacing 548 mm (rail centrelines), 488 mm clear, stated; U14 rewritten; A1e and H10 updated.
- Decision 5 and datum rows: second constraint added, a plate stop pin in an end-member slot (along-slot); key 0.25 across, pin 0.20 along; chain re-budgeted to 0.32 + 0.20 + 0.20 + 0.15 = 0.87 against 1.0; A3b rewritten as a measurement of built fits.
- U13: working stroke (at most 500, `upper.travel_max`) separated from the loading park (950, manual raise only, pin latch above start_z 800); about 780 mm of carriage range stated and not working travel; 950 geometry restated (900 + 50 while lowering, 160 above the seated 790 core); P6c split into P6c and P6d.
- U15: anchor is a metal 728 mm column-top cross member (joints 8 to 10), load path hoist to frame with no printed part, fuse a 300 N shear link limiting jam force on the core to 150 N, below the 204 N of H2; A2h and H9 added.
- U16 and decision 9 rest: the 250 mm finger below the cutter is withdrawn (it would land on the base plate about 80 mm before the stop). Cam lug is flush with the cutter lowest point, radius 95, and trips a 250 mm tower on the arm; arm clears to radius 125; A2e split into A2e, A2f, A2g; key renamed `rest.release_tower`. Decision 8 stands on this.
- Test IDs: A1c split into A1c, A1d, A1e; A3d split into A3d, A3g; A3e split into A3e, A3h, A3i; A6 split into A6a, A6b, A6c; P6a reclassified as a document check; bare A1 replaced (A1a, A1b); H8 now covers funnel seating force.
- Renames: `stop.nut_top_z` to `stop.collar_top_z`; exposed-core row reads from the plate top.
- Final edits: decision 5 has two plate keys bracketing the receiver and column feet abutting the end-member stop line, foot along-slot clearance added (foot radial 0.283), chain 0.32 + 0.20 + 0.283 + 0.15 = 0.953 against 1.0; A3h reworded to skirt bottom at least 1 pitch above the floor; A1d cited in the Column feet row and decision 5, A3g in U12; H8 reads stop gap trial; signature line 9 matches the choke strap.
