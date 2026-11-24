## Table per size

| d | valid | closed | solids | bad_edges | slit_plane_faces | euler_VEF | min_face_area | min_edge_len | flip_mismatch |
|---|---|---|---|---|---|---|---|---|---|
| 90.0 | T | T | 1 | 0 | 0 | 0 | 4.466 | 0.0755 | 1.0 |
| 92.5 | T | T | 1 | 0 | 0 | 0 | 4.603 | 0.7854 | 1.0 |
| 93.7 | T | T | 1 | 0 | 0 | 0 | 4.669 | 0.7854 | 1.0 |
| 95.0 | T | T | 1 | 0 | 0 | 0 | 4.740 | 0.7854 | 1.0 |
| 97.0 | T | T | 1 | 0 | 0 | 0 | 4.850 | 0.7177 | 1.0 |
| 97.5 | T | T | 1 | 0 | 0 | 0 | 4.878 | 0.3641 | 1.0 |
| 100.0 | T | T | 1 | 0 | 0 | 0 | 5.015 | 0.2858 | 1.0 |
| 102.5 | T | T | 1 | 0 | 0 | 0 | 5.152 | 0.7854 | 1.0 |
| 105.0 | T | T | 1 | 0 | 0 | 0 | 5.289 | 0.7854 | 1.0 |

Predictions held: euler_VEF 0 for every size (notches Euler-neutral), slit_plane_faces 0, one solid, clamped Kd1 and Kmax each valid, closed, one solid, common volume 0.0.

## Gate, llm_plm_cad 7.1

- Edge multiplicity: bad_edges 0, nine of nine.
- Leftover faces: slit_plane_faces 0, nine of nine.
- Face-count growth per boolean: the cut records carry volumes only, no face counts. Volume per cut: slits and notches and label match expected within 0.5 mm3. Relief holes read 32 to 57 mm3 under expected (d 90: 7148.5 against 7205.9). Basis difference: expected counts each hole whole, the built delta excludes the part of the hole already inside a slit void. Both pass.
- Plain versus optimal bounding box: result JSON carries the plain box only (66.99, 66.99, 32.0, identical at all nine). Gate on this item: not available.
- Family probe: pairwise symdiff 0.0 in the region, zero control 0.0, known-bad 1.877 mm3.

## Differences from the family

- d 90: min_edge_len 0.0755, the predicted lip-to-hole separation 0.075 in t (crossing 11.9 deg). Expected, OCC-safe, 7.5e5 times tolerance.
- d 97.0, 97.5, 100.0: min_edge_len 0.72, 0.36, 0.29 against 0.7854 elsewhere. Cause not in the probe; edges stay above 2.8e6 times tolerance. Pass.
- flip_mismatch 1.0: the 180 degree flipped copy shares no volume with the part (cone inverts), well above the floor. Pass.

SIGNED.

## Addendum: face growth and bounding box

| d | slits | relief | notches | label | final |
|---|---|---|---|---|---|
| 90 to 97.5, 93.7, 97.0 | 13 to 103 | +0 | +4 per notch | +6 | 113 to 125 |
| 100, 102.5, 105 | 13 to 92 | +11 | +4 per notch | +6 | 129, 133, 137 |

- Notch +4 per notch matches the predicted dF +4; label +6 is the same at all sizes. Final = 113 + 4 (n - 1) + 0, so counts follow the notch count only.
- d 100 and above differ mid-sequence: slits leave 92 faces, holes restore 103. Both groups reach 103 after the holes; the sequence differs, the topology does not. Cause not in the records. Pass.
- No cut loses faces after the holes; euler_VEF 0 at every size.
- bbox_plain equals bbox_optimal at all nine (66.99, 66.99, 0 to 32.0). No rotated-box slack.

SIGNED.
