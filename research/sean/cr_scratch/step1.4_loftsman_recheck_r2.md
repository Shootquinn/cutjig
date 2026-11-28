# Step 1.4 re-check r2, The Loftsman: P7a FIX 1, R2 wing placement, r2 spec placements

Verdict: P7a FIX 1 **CLOSED**. O2 (ii) **SIGNED**. R2 wing placement **SIGNED** on its values, with one new FIX (LF1.4r2-1, a key name, 0 pixels). drill_tube_stub and core_seat depth **SIGNED**. No class repeats.

Scratch: `D:\Unleashed Robotics\_scratch\cutjig\open14\p7lr\`.
- Tree copy `ws\` (params.yaml and docs/sketches as of 20:08).
- Dry runs `wingkey_dry.txt` (S1) and `wingkey_dry_s3s4.txt` (S3, S4).

## Corrections to the brief

none

## 1 P7a findings

| Finding | Status | Evidence (MEASURED) |
|---|---|---|
| FIX 1: X1 presence rule, side_xz branch without a control | CLOSED | manifest.yaml l.712 X1-B6, fixture `step14r2_fixtures.py::x1_presence_s1_b`, planted 1, gameplan_line 144. wip/fixtures/controls_results.json: observed "fires (1 issue(s), planted 1)", match yes, reason text equal to the P7a dry run. Red by deletion of the presence branch (Engineer `deltest.txt`). The gameplan row X1 (l.144) carries B6. |
| NOTE 1 to 4 | not acted on, as filed | none moves a value |

## 2 Signatures

| Rule or placement | Signature | Basis |
|---|---|---|
| X1 O2 (ii) presence rule, both branches (X1-B5 section_yz, X1-B6 side_xz) | SIGNED | Premise drawn = spec held by K8 section_true_issues; both branches red; plan views out of scope by the rule's words |
| R2: S1 r10 `wingnut:wing` in-plane outlines | SIGNED on the values; FIX LF1.4r2-1 to apply at the same save point | Section 3 |
| s4 `drill_tube_stub` row | SIGNED; NOTE LF1.4r2-2 | Section 4 |
| core_seat depth (s1, s3, s4), TP1.4-3 | SIGNED (placement) | depth (100 + 1.0) / 2 = 50.50 = drawn ledge r 50.50 (the P7a seat bearing row, ledge r 47.50 to 50.50) (DERIVED); same form as core_seat_105 (105 + 1) / 2 = 53.00; K7-B36 to B38 match |
| K5 wing in_plane form (p0, i, ii) | concur | K5-Z9 clean on 495 artists; B74 2/2 (i), B75 2/2 (ii, the band 16.00 low at z_S 157.09 to 197.09), B76 4/4 (p0, azimuths 120 and 240): all match |

Label texts, the washer frac removal and the floor and base_plate shape texts carry no placement; they are The Designer's.

## 3 R2 wing placement (z_A unless marked)

| Quantity | Hand (DERIVED) | Spec / record (MEASURED) | Agree |
|---|---|---|---|
| nut bottom | collar top 159.84 - 6.75 - 56.0 = 97.09 | s1 wingnut z_rule z_min | yes |
| wing root band, nut.py `wing_poly` | local z H - root to H = 56 - 40 to 56 = 16 to 56; z_A 97.09 + 16 = 113.09 to 153.09 | spec wing z 113.09 to 153.09; z_S 173.09 to 213.09 (K5-B75 reason, live band) | yes |
| wing tip band, nut.py | H - (40 - 28) / 2 - 28 to H - 6 = 22 to 50; z_A 119.09 to 147.09 | outline drawn at the root band over the whole span | rectangle circumscribes the tapered wing (spec text "simplified"); every clearance read from it is a lower bound |
| wing u | body_od / 2 = 166.28 / 2 = 83.14 to span / 2 = 115.00 | K5-B75 u [83.14, 115.00], mirrored at -u | yes |
| azimuths | k 360 / wing_count = 0, 180: both in the xz plane, u = r cos theta = +-r | K5 p0 pass on the live spec | yes |
| wing to collar | collar ring r 76.20, underside 153.84; wing root top corner (83.14, 153.09): sqrt(6.94^2 + 0.75^2) = 6.98 | `wing_clear.txt` least 6.98 (collar), every pose | yes; the collar is round, so 6.98 is also the 3D least |
| wing to receiver | 83.14 - 74.79 = 8.35 (thread piece r 74.79, z band overlaps) | 8.35 | yes |
| wing to S1-5b rows | | 148.75 (bearing), capture_end | above S1-5b least 142.00; the wings do not change S1-5b |

Drawn PNG `s1_pose_load_r10.png`: two unfilled rectangles at |x| 83 to 115, z_S 173 to 213, below the nut-plate top, outboard of the body. S4 r2 `-X wing (behind)` x_band form shows the same z band (dashed, z_S 173 to 213).

**FIX LF1.4r2-1 (key of the wing z band).**
- nut.py builds the wing z band from `wingnut.wing_root_width` (40, `wing_poly`: H - root). The s1 wing block reads `wingnut.wing_height` (40, params source "wing seed; at least 30 (S2-5)", a hand-room seed). The two agree by value only. K5 (ii) holds drawn = spec, so a change to either leaf would move the drawn band off nut.py with every check green.
- Class: every wing z band in the specs. s1 wing (in_plane), s3 l.566 and s4 l.521 wing (x_band form) carry the same key.
- Fix: in s1_spec.yaml, s3_spec.yaml and s4_spec.yaml, wing `z` lower bound `collar_top - collar.top_above_plate - wingnut.wing_root_width`. Add `wingnut.wing_root_width` to each wingnut `keys` list where absent.
- Dry run (MEASURED) in the `ws\` copy with the three edits:
  - `check_sketch.py s1 --rev 10`: 19/19 pass, K5 495 artists, X1 72 rows.
  - `s3 --rev 9`: 16/16 pass. `s4 --rev 2`: 14/14 pass.
  - Re-drawn PNGs against the live wip PNGs, differing pixels: s1 load, start, capture_end, park 0, 0, 0, 0; s3_jackscrew_section_r9 0; s4_base_section_r2 0; s4_liner_section_r2 0.
- No drawing change. The S3 and S4 edits ride the open S3 r9 and S4 r2 revisions; --stale re-runs per (i). No revision opens.

## 4 drill_tube_stub

| Quantity | Hand (DERIVED) | Record (MEASURED) | Agree |
|---|---|---|---|
| z_min head_top | tip 184.84 + drill.head_length 106.369 = 291.209; z_S 351.21 | K7 drill_tube_stub\|drill_head C 0.0 (both figures) | yes |
| z_max | crop z_A [1] = 330; z_S 390 | PNG top at z_S 390 | yes |
| r | drill.tube_od / 2 = 76.20; inside the head r 88.90 | PNG | yes |
| core_100 inside the bore | core r 50.50 < tube ID / 2 = 73.025; core top 302.50 inside 291.21 to 330 | N declared | yes |

NOTE LF1.4r2-2: z_max 330 is a literal tied to `crop.z_A[1]` by the shape text only. If the crop moves, the stub ends off the crop edge with every check green. Proposed for the Step 2 harness: z_max reads `crop.z_A[1]`, or a spec lint holds them equal. No change at r2.

## Gameplan lines to change

none
