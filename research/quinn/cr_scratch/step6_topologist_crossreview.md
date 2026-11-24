## 1. Topology record (Engineer reproduces; a mismatch is a finding, not a gate)

| Part | Boolean | Predicted | euler_VEF |
|---|---|---|---|
| base | one cut: spigot, drain, 8 slots, 3 underside pockets, 2 edge notches | faces 6 to 63 (slots 4 each, pockets 5, notch 3 + 1 split) | 5 (10 through holes net 0, 3 pockets +1 each) |
| tray | one cut: cavity, 2 reliefs, 2 holes | 26 (rim splits into 2 faces) | 0 (genus 2, rim ring gone, floor-straddling holes give no inner loop) |
| nut | fuse skirt (+4 faces: 3 new, cylinder splits; dV 4, dE 7), cut 2 glyphs (+8 each), old +y mark (-8) | dF +12 | +2 (annulus z 5 face +1, glyphs +1 each, old mark -1) |
| receiver | one cut: channel + 14 lines + 2 bands + 3 digits | line-digit pairs merge: 16 pockets | +16 (channel itself 0) |
| holder | tick groove on the flange OD/underside edge | dF +4 (dV 8, dE 12) | 0 |
| plug | revolve | 7 | 4 (two planar annuli) |
| foot | 3 through holes | 9 | 2 |
| caddy | 7 sockets, 7 labels | 55 | 16 |

Genus: plate-like parts carry one per through hole. Components: 1 each. Tray ramp-end crease x 81 crosses hole r 81.2 transversally (chord y +-5.7): valid.

## 2. Orientation signs (Rule M)

- Glyph sense s = sign(z . (r x d)). Tighten at (99.07, 0), d = -y: -1. Loosen: +1. Opposite faces of wing 0. Pass.
- Rule P: the glyph pair is invariant under a 180 degree flip about the wing mid-plane (z 36, X axis). The flipped nut still differs through the thread, pocket and skirt (z asymmetric), and a Y-axis flip moves wing 0 to -X. Both readings pass; the claim in the definition stands on those features.
- Scale side: t = z x r (counter-clockwise). Viewer outside has right = +t: bands at -t (left), digits at +t (right). Consistent; state the t sign in the script.
- Base slots: Z-axis rotation by 180 maps the pattern to itself, flips about X or Y do not (offset 15 on 20-long slots). Rail notch: flip about the rail axis lands on the opposite-face slot line y 289; mismatch 1440 / (644 x 916.56) = 2.4e-3. Pass.
- Stop pad: top face z 184.84, n = +z, cutter side n . (cutter - pad) > 0. Pad bottom z 172.84, collar top 159.84: 13 clear.

## 3. Booleans and tangencies

- Tick: ceiling area 2 mm2, under the probe's 50 mm2 filter; HD6 holds. Tool bottom at 88.0 is coplanar with the flange underside; run it from 87.0.
- Ruler floor 0.05 below root at the channel edge: valid, one sliver band 0.05 high.
- Line k = 0, 5, 10 (t +-2.6) shares a face with its digit pocket (t 2.6): inside one fused tool, merges.
- Skirt cone vertex (83.14, 14) lies on the body cylinder: edge on face, valid.
- Pin wall x 244.0 is the declared contact; no pin solid exists in base.

## 4. Frame contact

Rail-end, end-support, support-plate contacts: class F or C, overlap 0. T-nut stack 8.2575 against floor 9.165.

## 5. Items

| Item | Line | Edit |
|---|---|---|
| T-nut body vs 45 degree flank | 16 x 6.0 body, cavity floor width 8.06; body corners enter the profile by 3.06 mm: 150 mm3 each, 19,200 mm3 over 128 | chamfer the two long bottom edges 3.5 at 45 degrees |
| Printed outer bracket | x 142 to 210 enters end member x >= 202: 8 x 7 x 57 = 3,192 mm3, 4 sites | add to the C6 Step 7 log |
| Tray relief | "72 x 19 at (0, +-260)" centred on the wall leaves 6.5 mm in the column | read as y 241 to 260, open to the edge |
| Caddy label | position unstated; a label edge on the socket wall is tangent | 1.0 off the socket wall |
| Digit pocket | "3.0 high" unplaced; at k = 0 a centred pocket meets z 47.0 | centre it on the line z + 0.2 |

None of the five fires a test or fails a build; each closes by the stated edit inside the step.

SIGNED
