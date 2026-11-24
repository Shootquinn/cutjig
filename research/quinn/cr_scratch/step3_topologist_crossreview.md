## 0. Frame and normals (item 8)

Right-handed; z_A up from datum A (frame top); origin on datum B (bore axis, +Z); +X along slot line C (plate keys); theta CCW from +X; theta_key 37 deg. Loftsman z = z_A - 40 (plate top z_A 12). ASSEMBLY.md line 7 states two origins; replace with this.

Mates, all n.n = -1, first face n_out: frame top +Z / plate underside; floor +Z / ring, foot key bottoms; ring, foot key tops +Z / holder, holder key bottoms; collet cone (cos a, sin a) in (rho, z) / holder cone; ledge +Z / core bottom; register bore -e_rho / holder OD, ring OD; slot floor r 70.59 -e_rho / key tips; rim +Z / flange underside; flange top +Z / washer bottom; washer top +Z / pocket floor; washer OD +e_rho / pads; notch floor +e_rho / tab; plate top +Z / collar underside; nut bearing flank n.Z > 0 / receiver flank.

## 1. Predicates S1 to S23

| ID | Substituted | Verdict |
|---|---|---|
| S1 | norm(a x Z) <= 1e-4 nominal; pose T separate | PASS |
| S2 | thread z 40.5 to 88.5, (tip - root).Z > 0 | PASS |
| S3 | ring bottom on floor: 0.000, a designed seat contact (class C, overlap 0.00 mm3); the 0.005 `fit.model_contact_gap` is carried at the ring top to holder bottom, not at the floor (amended at Step 3 close per the Designer completeness read and the built result) | PASS |
| S4 | top(C) 32 < top(H) | PASS |
| S5 | d rho/dz -0.17633 both, one `cone.alpha` | PASS |
| S6 | ring 0 < rim 1.5 < floor 2.00 at K-max | PASS |
| S7 | R 0.30 radial; K 0.005 normal | PASS |
| S8 | R 0.50 to 1.75; K slit 0.584 > 0.5 | PASS |
| S9 | ledge ID r 40.5 at d 85 > floor hole r 40.0 | PASS after W-2 |
| S10 | pocket floor / washer / flange; K 0; R p 0.75 | PASS |
| S11 | nut lowest z 50 vs collet top 32; plate hole to core 15.04 | PASS |
| S12 | skirt 13.50 above shoulder z 36.5 >= 8 | PASS |
| S13 | full-form R 24.72 >= 24 | PASS, 0.72 |
| S14 | collar top z_A 159.84 | PASS |
| S15 | 48.5 >= 1.701 + 9.925 + 24 + 8 = 43.63 | PASS |
| S16 | plate top / collar underside, 0.75 | PASS |
| S17 | outer solid d-independent | PASS |
| S18 | d-dependent set is bore, ledge ID, bore chamfer, label; test reads that set | PASS, amended |
| S19 | d 105 wall 5.00, 1.20 after chamfer | PASS |
| S20 | bore axis = outer axis | PASS |
| S21 | carried 0.954 used Step 2 inputs (slit 32, hole 6). Lines 80 to 82: 4 x 0.9163 / (2 x 26.5 x 3.0) = 0.0231, ratio 2.31 | FAIL, W-1 |
| S22 | 1 shell, genus 1, slit planes contain Z | PASS after W-2 |
| S23 | pi 3.5 / 12 = 0.916 < 1.5 | PASS |

## 2. Contact classes (item 1)

Rule for every C pair: the lower part's contact face moves -n by 0.005 (new key `fit.model_contact_gap`); placements unchanged; min distance in [0.004, 0.006], common volume 0. Values R / K d+1 / K-max.

| Pair | Class | Gap |
|---|---|---|
| holder bottom / ring top | G G C | 11.626 / 7.089 / 0: the holder stop |
| holder key bottom / foot key top | G G C | same, in parallel (W-4) |
| flange underside / rim | G | 13.126 / 8.589 / 1.500, never loaded |
| holder bottom / floor | G | 13.626 / 9.089 / 2.000 |
| holder cone / collet cone | G C C | 0.30 radial / 0.005 / 0.005 |
| holder OD / register | G | 0.25 (C only in pose T) |
| holder key / slot | G | 0.125 per side, 0.55 radial |
| ring OD / register | G | 0.30; 2.05 K-max |
| foot key / slot | G | 0.125; radial 0.55, 2.30 K-max (still 1.00 past bore) |
| ring, foot key / floor | C | 0 |
| flange OD / nut crest | G | 0.60 (offset 0.40, margin 0.20) |
| washer / flange top | G C C | 0.75 / 0 / 0 |
| washer / pocket floor | C | 0 |
| washer OD / pads | P | 0.10 interference (section 5) |
| notch / tab | G | 0.5 tangential, 1.0 radial |
| plate top / collar | C G G | 0 / 0.75 / 0.75 |
| plate hole / holder OD | G | 1.00 |
| nut skirt / shoulder | G | 25.13 / 20.59 / 13.50 |
| nut / receiver thread | C bearing flank; G crest 0.35, other flank 0.30 | |
| collar ID / core | G | 2.00 at d 105; 1.77 under A3c offset plus 0.573 deg tilt |
| receiver / base plate | C | weight only (A6a 0) |
| receiver / frame | G | >= 1.0; ASSUMED spigot depth <= 11.0 |
| holder, nut, washer, collet / frame | F | |

## 3. Register (item 2)

L_h 88.0, g_reg 0.25, register_depth 48.0 stand. Worst case hanging: insertion 48.75 minus the 1.0 rim chamfer (line 196) = 47.75. Exact cylinder-in-bore tilt (L sin t + D cos t = B; 134.08 in 134.58): 0.609 deg. Plate rock 0.315 (lever 136.44, conservative; true 147.8 gives 0.291). T9 = 0.924 against line 1.021; signed 0.903 becomes 0.924 (W-3), margin 0.097.

## 4. Collet topology (item 3)

N = 2 ceil(pi 3.5 / 2) = 12 for every d, 87.3 included; slit 0.584. Slits at theta_key + 15 + 30k; foot key clear 66.99 x 0.2618 - 5.875 - 0.75 = 10.91. Revolve seam at theta_key + 180, mid-finger.

Tangency: top-open relief hole bottom edge z 5.5 - 1.5 = 4.0 equals ledge top z 4.0, tangent to the ledge-bore edge (Section 11). W-2.

Strain corrected set: ligament 3.0, hole 6.0 at z 6.0 / 26.0, slit 26.0, overlap 20.0: 3 x 0.9163 / (2 x 26.0 x 6.0) = 0.00881, ratio 0.881. Hole bottom z 3.0 clears ledge 2.5 by 0.5, ring top by 1.0.

Genus: fingers joined alternately at the z 0 to 3 and z 29 to 32 ligaments: one shell, genus 1, chi 0. Hole 6.0 > slit 1.5: keyhole, no genus change.

Probes at 87.3: slit width at theta_key + 15 + 30k, z 16, mid-wall (both slit runs; chamfer starts z 19.35). Material probes at theta_key + 30k, 11.7 from any slit.

## 5. Washer (item 4)

As written (line 167) the exemption is a hole. Class P instead. Pads ASSUMED: 3, arc 10.0, height 0.8, at 0/120/240 deg; tab at 60; windows at 90 + 120k. Predicate: common(nut, washer) is 3 pieces, 2.40 +/- 0.24 mm3, each in r 71.5 to 71.6 within a pad sector; common(nut minus pads, washer) = 0. Washer absent gives 0 and fires. The washer is Z-symmetric (through notch): flipped is the same state.

## 6. OCC strategy (item 5)

No fuse across parts. Clamped collet: revolve the clamped profile (rho_C - Delta/2 - 0.00508; ring and foot key top 1.995); cut slits at 1.5 - pi Delta / 12 with one compound cutter. Bore and key slot: one fused profile cut from the floor up. Tolerance 1e-7, no fuzzy value. Per part: isValid, one solid, one shell, closed, volume > 0, 2 faces per edge, V - E + F - (L - F) = 2(1 - g), g = 1 (collet), expected-delta per cut 3 percent. Pair: BRepExtrema 0.005 +/- 0.001, common 0.

Overlap unrepresentable: z_hb = 2 + 9.925 - (Delta/2) / tan a, Delta = B_f - d_core, same `cone.alpha`; placement asserted to the formula at 1e-6. Sign predicate on every C pair: (p_B - p_A) . n_A > 0 at closest points; overlap makes it negative.

## 7. Wrong states (item 6)

| WS | Feature: predicate | Step 3 |
|---|---|---|
| 1 collet flipped | ledge d - 4 on top blocks core by 1.25; holder on ring at z 32, full-form 6.35 < 24 | yes |
| 2 holder flipped | flange 144.08 vs bore 134.58, 4.75 | yes |
| 3 nut flipped | collar 152.4 vs crest 145.28, 3.56 | yes |
| 4 wrong hand | one helix function; T1a +P/4 | yes |
| 5 cross-thread | register 47.75, p 0.75: 0.924 < 1.021 | yes |
| 6 wrong collet | K-max with core gap > 0 | predicate yes; scale Step 5 |
| 7 collet propped | full-height slot: key off-slot on rim, S3 gap 88.5 | yes |
| 8 holder bottoms | ring 0 < rim 1.5 < floor 2.0 | yes |
| 9 nut bottoms | 13.50 >= 8 | yes |
| 10 plate flipped | asymmetric slots; plate top +Z | waits |
| 11 slit over key | 10.91 clear; 15 deg control fires | yes |

The 60 deg sector was a hex-key swing, never an orientation defence. Replacement: one key at 37 deg in one slot, holder and collet foot; symmetry order 1. Predicate: rotated 30, 90 or 180 deg, common(holder key, receiver) = 2.75 x 11.75 x 40 = 1292 mm3; play +/-0.209 deg. 37 aliases no slit (52 + 30k), wing (0, 180) or boss (45 + 90k).

Slot wall to root 1.35 with groove overshoot, >= 1.2.

## 8. Brackets (item 7)

Params lines 308 to 322 match the hardware confirm (14089 57.35 x 57.0, plate 6.0, holes unmodelled; printed 68 x 57, plate 7, slots 7.0 at 29.2 along, 30 across; 8 T-nuts per bracket). Flags: 14089 SKU ASSUMED; T-nut fit unmeasured. Rows stay data: bracket/frame C, body in the profile's outward half-space; no relation reads 14089 hole positions.

## Verdict

WITHHELD.

- W-1: line 84, strain 0.954 -> 2.31; lines 80 to 83: ligament 4.0 -> 3.0, hole 3.0 at 5.5 -> 6.0 at 6.0, slit 26.5 -> 26.0, overlap 21.0 -> 20.0; strain 0.881.
- W-2: line 51, core seat height 4 -> 2.5.
- W-3: line 31, T9 0.903 -> 0.924 deg.
- W-4: line 139, "ring top 1.995" -> "ring top and foot key top 1.995".
- W-5: line 167, "exempt from the overlap test" -> "class P, 3 pads 10.0 x 0.8, common 2.40 +/- 0.24 mm3".
