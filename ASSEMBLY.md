# ASSEMBLY.md (Step 2 integration of the system concept)

Source: research/quinn/cr_scratch/step2_system_concept.md (signed Loftsman; Topologist signed with the orchestrator's ruling on decision 5 wording) and research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md (governing geometry numbers). Relations are data: tests iterate over the pair table, so a change of contact class or pose is a data change. Values marked (seed) are ASSUMED until Step 3 freezes them.

## Coordinate frame

Right-handed. z_A is measured up from datum A (frame top plane, base plate underside). The origin is on datum B (receiver register bore axis, +Z). +X runs along slot line C (plate keys). theta is counter-clockwise from +X seen from +Z; theta_key = 37 deg. Floor frame z = z_A - `icd.floor_above_datum_a`. Datum C: a frame slot line with two plate keys and an end-member stop pin. Units mm. Rule M, Rule P, and slit phase theta_key + 15 + 30k.

## Poses

| Pose | Definition |
|---|---|
| R | nut backed off, collet free; core slides in with zero interference; holder bottom 13.626 above the receiver floor |
| K d+1 | nut hand-tight, collet clamped on a core at the top of the grip window (d + 1.0); clamped-state collet solid from the generator (bore = core diameter, narrowed slit); holder bottom 9.089 above the floor |
| K-max | nut hand-tight, collet clamped on a core at the window floor (d - 1.5); deepest holder travel; holder bottom 2.00 above the floor, on the collet foot ring top |

Poses are built for each collet in `collets.diameters` and for any collet from the generator. Where a table says K without a suffix, K d+1 and K-max carry the same class.

## Parts

| Part | Signed feature (Rule P, seed) |
|---|---|
| base | asymmetric bolt-down slot pattern (the -y row of four slots is the +y row shifted 15 mm in x, a whole-row offset; it identifies a flip about an in-plane axis, while a 180 degree turn about Z maps the pattern onto itself and is caught by the stop-pin pocket at +x and the two plate-key pockets on the +y slot line) plus a flat on the receiver foot |
| holder | index notch on the flange rim, off-axis; collar ring (r 55.0 to 76.2, 6.0 high) on the tube top with four 6.6 holes over the insert bores |
| collet | foot key on the underside, slit phase fixed to key angle |
| nut | one-ended thread start plus a single marked wing |
| washer | one radial tab notch on the outer edge, off-axis (seed); PTFE, always fitted, a separate part |
| core | top-end mark on the stand-in (chamfer on the top end only) |
| frame | datum C slot line marked by a notch on one rail |
| bracket | none: purchased catalog part, identified by SKU (full-size, leg at least 57 mm); the four plate-support ends take the printed 68 mm bracket (measured: 7.0 mm slots, 29.2 mm pitch along the leg) |
| tnut | none: purchased catalog part, identified by SKU (PZRT 3030 roll-in spring M6 T nut; fit declared by use) |
| cutter | keep-out solids, four in one compound touching on faces: face annulus (r 71.4375 to 86.2), tube (rho 73.025 to 76.2), lead-in funnel (mouth 66.0, throat 56.0) and lead-in ring (bore 56.0); orientation fixed by the frame |

## Relations

Classes: C contact required (min distance 0 +/- 0.01, patch area above floor, overlap < 0.01 mm3); G gap (distance >= g_min, contact area 0); F free (overlap 0); P press pads (declared retention feature: min distance 0 +/- 0.01 and common volume between nut.pad_overlap_min and nut.pad_overlap_max mm3, so a washer that only touches fails). An unlisted pair fails test A1a.

| Part_A | Part_B | Class_R | Class_K | g_min_mm | Note |
|---|---|---|---|---|---|
| base | holder | G | G | 0.12 | key in slot: (receiver.key_slot_width 12.0 - holder.key_width 11.75) / 2 = 0.125 anti-rotation clearance; stroke is carried by the feature pairs (rim gap 13.126 (R), 8.59 (K d+1), 1.5 (K-max); floor gap 2.00 at K-max (S6, A3e)); never loaded |
| base | collet | C | C | 0 | collet foot ring on receiver floor seat |
| base | nut | C | C | 0 | nut thread flank on receiver thread |
| base | washer | G | G | 0.5 | washer clear of the receiver rim (seed) |
| base | core | G | G | 1.0 | core stands on the collet core stop, off the tray |
| base | frame | C | C | 0 | base plate on frame top plane, z gap 0 +/- 0.05 |
| base | bracket | F | F | 0 | free: no contact or interaction |
| base | tnut | F | F | 0 | free: no contact or interaction |
| base | cutter | F | F | 0 | free: no contact or interaction |
| holder | collet | G | C | 0.29 | R radial gap fit.seat_clearance 0.30 measured normal to the 10 deg cone (0.30 x cos 10 deg = 0.2954); K cone contact (ring-top pair is in Feature pairs) |
| holder | nut | C | G | 0.50 | R nut plate top meets the holder collar underside (collar ring in holder.FCStd, captured, n.n = -1); K gap = washer proud: washer.thickness 1.3 - nut.washer_pocket_depth 0.8 + 0.01 stack gaps (built 0.51); nut.lift_play 0.75 is the feature pair below |
| holder | washer | G | C | 0.5 | K flange top bears on the washer (seed gap in R) |
| holder | core | G | G | 1.0 | core inside holder cavity, no contact |
| holder | frame | F | F | 0 | free: no contact or interaction |
| holder | bracket | F | F | 0 | free: no contact or interaction |
| holder | tnut | F | F | 0 | free: no contact or interaction |
| holder | cutter | F | F | 0 | free: no contact or interaction |
| collet | nut | G | G | 1.0 | required G pair; nut clear of collet by >= 1.0 mm |
| collet | washer | G | G | 1.0 | free of the washer bore (seed) |
| collet | core | G | C | 0.5 | R core slides in, zero interference; K clamped grip |
| collet | frame | F | F | 0 | free: no contact or interaction |
| collet | bracket | F | F | 0 | free: no contact or interaction |
| collet | tnut | F | F | 0 | free: no contact or interaction |
| collet | cutter | F | F | 0 | free: no contact or interaction |
| nut | washer | P | P | 0 | washer seated in the plate underside pocket (r 68.3 to 71.7); the three press pads hold it: class P, min_dist 0 +/- 0.01, common volume nut.pad_overlap_min 2.0 to nut.pad_overlap_max 2.45 mm3 (designed 2.40, built 2.387) |
| nut | core | G | G | 1.0 | required G pair |
| nut | frame | F | F | 0 | free: no contact or interaction |
| nut | bracket | F | F | 0 | free: no contact or interaction |
| nut | tnut | F | F | 0 | free: no contact or interaction |
| nut | cutter | G | G | 25.0 | required G pair; g_min = stop.g_stop 25, taken from the collar top (wings included) at the stop |
| washer | core | G | G | 1.0 | free: washer ID 136.8 against core radius 53 |
| washer | frame | F | F | 0 | free: no contact or interaction |
| washer | bracket | F | F | 0 | free: no contact or interaction |
| washer | tnut | F | F | 0 | free: no contact or interaction |
| washer | cutter | F | F | 0 | free: no contact or interaction |
| core | frame | F | F | 0 | free: no contact or interaction |
| core | bracket | F | F | 0 | free: no contact or interaction |
| core | tnut | F | F | 0 | free: no contact or interaction |
| core | cutter | F | F | 0 | free: no contact or interaction; drill to core at the stop is class F with axial force 0 (A2d) |
| frame | bracket | C | C | 0 | bracket mate faces on profile |
| frame | tnut | C | C | 0 | T-nut centroid inside slot cavity |
| frame | cutter | F | F | 0 | free: no contact or interaction |
| bracket | tnut | C | C | 0 | bolted joint |
| bracket | cutter | F | F | 0 | free: no contact or interaction |
| tnut | cutter | F | F | 0 | free: no contact or interaction |

Pair count 45 (computed, 10 parts, all 45 pairs listed): R pose C 7, P 1, G 12, F 25; K pose C 9, P 1, G 10, F 25.

### Feature pairs (Step 2, the pairs that differ by pose)

Gaps in mm from the Loftsman reply. These are rows of the same table at feature level; A1a iterates over both tables.

| Feature_A | Feature_B | Class_R | Class_K d+1 | Class_K-max | Gap R / K d+1 / K-max | Note |
|---|---|---|---|---|---|---|
| holder bottom | collet foot ring top | G | G | C | 11.626 / 7.089 / 0.00 | the declared holder stop; at contact the force enters ring and floor seat in parallel with the cone, grip stops rising |
| holder flange underside | receiver rim | G | G | G | 13.126 / 8.59 / 1.5 | the holder stroke gap; the rim is not a stop; never loaded |
| holder bottom | receiver floor | G | G | G | 13.626 / 9.089 / 2.00 | A3e: holder bottom above the floor in every pose |
| nut plate top | holder collar underside | C | G | G | 0 / 0.75 / 0.75 | release path: back-off lift play p = nut.lift_play 0.75; collar underside = holder top - collar.thickness |
| nut skirt bottom | receiver floor | G | G | G | at least 1 pitch (8) | A3h |
| nut collar top | cutter lowest point | G | G | G | at least 0 / 25 / 25 | A2b, g_stop applies at the highest clamped nut position, so minima are per pose (R unclamped 20.464 against 0; K-d+1 25.001 and K-max 32.090 against stop.g_stop 25); the metal stop bears, not the nut |

## Load path

The clamp force closes inside the receiver assembly and nowhere else: nut thread flank, nut clamp shoulder, washer (PTFE or printed), holder bearing flange, holder cone, collet cone, collet foot ring, receiver floor seat, receiver wall in tension, receiver thread flank, back to the nut thread flank (ten members). The base plate, frame and upper assembly carry none of it; the receiver underside force on the base plate is 0. The holder stroke ends on the collet foot ring top; the gap between holder flange and receiver rim is the holder stroke gap and is never loaded. Hard stop means the metal descent stop owned by the upper assembly.

Further statements from the concept (decision numbers):

- Axial clamp force about 267 N plain, 388 N PTFE at 12 N m nut torque (V). Ring top is class C at K-max only.
- Release (2): captured-flange nut, cone half-angle 10 deg; the nut backs off p = 0.75, plate top meets collar underside, collar lifts the holder; no jacking holes.
- Descent (3c, 8): 1000 N path is cutter, carriage, metal stop, columns, frame. It never enters the nut, holder, collet, receiver or base plate. Drill torque is not carried by the base.
- Core weight (3b): core stop, collet foot, floor seat.
- Manual raise (U15): carriage, hoist, cross member, columns, frame; no printed part; shear link at 300 N.
- Column feet stand on the frame slot lines, abutting the end-member stop line, never on the base plate.

## Interface control table

Fields live in params.yaml under `icd.*`, `stop.*`, `upper.*`, `core.min_exposed`, `column.*`, `strap.*`, `rest.*`, `hoist.*` (single source); the table with its checks is frozen in research/quinn/cr_scratch/step2_system_concept.md and tests/test_params_bom.py (P10) asserts that every key it names exists. Rows: datums A, B, C; mounting; coaxiality 1.0 (chain 0.953); keep-out 86.2; stop rating 1000 N; stop gap g_stop 25 from the collar top (Step 3); collar top z 159.84; stop height 184.84 / 315; travel 500 with start_z 684.84 / 815; exposed core 143.12; U12 core lead-in; U13 park 959.84 (loading position, not working travel); U14 carry strap; U15 manual raise; U16 steady rest (detents 310 and 560); column feet; torque reaction; cable and debris; footprint 644 x 608; mass target 40 kg; height. The 2 m jig height is the soft target `jig.height_target`, recorded and reported, never a limit.
