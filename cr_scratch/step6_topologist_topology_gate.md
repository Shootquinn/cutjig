## Topology table

All parts: isValid T, isClosed T, solids 1, shells 1 (frame: 150 objects, each valid, closed, one solid). bbox_plain equals bbox_optimal on every new part.

| Part | euler_VEF | Predicted | faces_before to after | Result |
|---|---|---|---|---|
| base | 5 | 5 | fuse 84 to 84; cut 6 to 63 | hit |
| tray | 0 | 0 | fuse 26 to 30 (24 clean); cut 6 to 26 | hit |
| plug | 4 | 4 | 9 to 7 | hit |
| foot | 2 | 2 | fuse 9 to 9; cut 6 to 9 | hit |
| caddy | 16 | 16 | fuse 63 to 63; cut 6 to 55 | hit |
| receiver | 20 (was 4) | +16 | 12 to 113 (cut), stud 113 to 195 | hit |
| holder | 8 (was 8) | 0 change | 13 to 28 (dF +4 on 24 to 28) | hit |
| nut | 10 (was 8) | +2 | 136 to 195 after glyphs; 183 to 195 | hit |
| tnut | 3 | none | fuse 14 to 13; cut 13 to 14 | no prediction; blind hole adds an inner loop |
| bracket_purchased | 2 | none | 8 to 16 | no prediction |
| bracket_printed | 2 | none | 8 to 40 | no prediction |
| gauge | 3 | none | 17 to 17 | no prediction |
| stop | 2 | none | 6 to 8 | no prediction |
| rest | 13 | none | fuse 48 to 52 (47 clean); cut 47 to 51 | no prediction |
| frame | 11 (sum) | none | notch 414 to 420 (408 clean) | no prediction |

No miss. Signed volume positive on every part.

Bbox basis: receiver plain 92.1 against optimal 88.5, nut z -3.6 against 0.0: helicoid control points, as in Steps 3 and 4. Both pass.

## Rebuilt parts

- Receiver 91 to 195, euler 4 to 20: 16 merged line-digit pockets.
- Holder 24 to 28, euler 8: tick dF +4, Euler-neutral.
- Nut 183 to 195, euler 8 to 10: skirt +4, two glyphs +16, old mark -8.
- Flip mismatch: base 0.0027 (pass), receiver 0.583, holder 0.118. Foot 0.0: symmetric part, no Rule P claim.

## Sign checks

- Glyphs (patched probe): wing 0 +z sense -1 (tighten), -z sense +1 (loosen), span 5.013, 43 samples each.
- Tick: local z 88.0, coplanar with the flange underside; HD7 reads 1.525 and 8.615 after the radius patch.
- Rule P: nut wing 0 marked, wing 1 bare; receiver key and holder notch off-axis; all True.
- Stop: pad top z 184.84, n = +z, underside 172.84; common volume with nut 0.0.

## Probe note

`step6_marks.json` carries the stale rim radius and glyph window (D2, D3); the patched file reads rim 88.5 and 43 samples. Test windows, not a gate defect.

## Rest re-check after the fix pass

Rollers interfere at d 102.5 and 105. After rebuild re-check: solids 1, isValid, euler_VEF (13 now), faces (51 now), plain equals optimal bbox, roller-to-ring gap open beside the pin, common volume 0.0 with each collet 90 to 105, interface plane y 244 unchanged.

SIGNED: base, tray, plug, foot, caddy, tnut, bracket_purchased, bracket_printed, frame, gauge, stop, rest (as built), receiver, holder, nut.


## Addendum: fix-pass parts

Source: result JSON and read-only FCStd. Identity: euler_VEF = 2(S - G) + R, R = inner loops. All four: isValid T, isClosed T, solids 1, shells 1, plain bbox equals optimal (nut z -3.6 plain, 0.0 optimal: helicoid control points, both pass).

| Part | euler | faces | R | G | faces_before to after |
|---|---|---|---|---|---|
| rest | 16 | 66 | 14 | 0 | slots cut 6 to 21; fuse 63 to 67 (62 clean); detent 62 to 66 |
| tray | 2 | 29 | 4 | 2 | common 14 to 9; fuse 30 to 34 (27 clean); cut 6 to 29 |
| plug | 5 | 12 | 3 | 0 | fuse 15 to 12 |
| nut | 10 | 195 | 19 | n/a | fuse 9 to 54; stud 54 to 136; glyphs 136 to 195 |

Rest. 13/51 is superseded by the pin-slot ruling. Three blind slots (ring bottom z 15.5 to 18.5) add 5 faces each and a slot-floor loop where the pin tip touches; the ring-bottom loop replaces the old pin-contact loop. Delta +15 faces, +3 euler. Fuse and detent deltas equal the first build, so pins add no faces. Probe: 54 rows (9 collets, poses R, K d+1, K-max, 2 heights) all valid, common volume with collet 0.0 and with core 0.0, rest-to-core 0.005, rest-to-collet minimum 262.0. Sizes 88.5 and 106 have no collet; the core test covers them.

Tray. Euler 0 to 2: both through holes now lie inside single floor planes (drain in the flat spot face, the other on one slope), so each floor face carries an inner loop; before, they straddled a crease and gave none. R 4 gives G 2. Faces 26 to 29: cavity common has 9 (4 walls, top, 4 floor planes from max(f, h)); the spot face adds a wall and a flat.

Plug. Euler 4 to 5, faces 7 to 12: the lug footprint (corner 17.46 inside head r 20) is an inner loop on the head top; 4 sides and a top are +5; embedded base absorbed (15 to 12).

Nut. Euler 10, faces 195, same as the gate; the NT4/NT8 resize leaves feature topology unchanged.

SIGN: rest, tray, plug, nut.
