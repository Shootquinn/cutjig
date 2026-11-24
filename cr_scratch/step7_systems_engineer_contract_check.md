## Contract check: Loftsman Step 7 definition

| # | Item | Ruling | Ground |
|---|---|---|---|
| 1 | base\|holder g_min 0.12 | ACCEPT | The pair is the key-in-slot fit ((12.0 - 11.75)/2 = 0.125), an anti-rotation clearance. Stroke is carried by holder bottom to floor (2.00 at Kmax) and the ring stop. Cite the key and slot keys in the row. |
| 2 | holder\|collet R 0.29 | ACCEPT | 0.30 x cos 10 deg = 0.2954 normal to the cone. |
| 3 | holder\|nut K 0.50 | ACCEPT | 0.75 is nut.lift_play, a different quantity. The K gap is washer proud (0.5). Tie the row to washer.thickness minus pocket depth. |
| 4 | nut\|washer class P, at most 2.45 | ACCEPT with a floor | Press pads are a declared retention feature. C6 interpenetration has no design intent; this does. Add a lower bound (at least 2.0 mm3) so a missing pad fails. Define P in the ASSEMBLY.md legend. |
| 5 | nut collar top\|cutter R: F | ACCEPT | g_stop applies at the highest clamped nut position (A2b); R is unclamped. Keep at least 25 on Kd1/Kmax (25.001 / 32.090). Written as G with g_min 0 at R and 25 at K, the gap above 0 check survives. |
| 6a | R nut at holder + 48.745 | ACCEPT | That is the Step 2 release contact, plate top on collar underside. 48.0 is the K stack. |
| 6b | Collar ring fused in the pose | REJECT as permanent; ACCEPT as interim | The collar (collar.od 152.4, id 114.0, top 6.75 above plate) is an ICD feature; A2b reads collar top from it. A pose script adding geometry the part file lacks gives the holder two definitions. Smallest fix: add the collar to holder.py, rebuild holder.FCStd (Manager authorization, Topologist re-sign). Meanwhile a test pins the ring z-span and radii to collar.* params. |
| 7 | Delete four printed outer brackets (12 / 96) | ACCEPT | Step 2 bracket rule gives two purchased 57 mm brackets at each of four outer corners (8) and one printed 68 mm bracket at each of four plate-support ends (4): 12. The 16 / 128 count exceeded the concept. The clamp loop is closed in the receiver; descent load enters at the column feet on the end-member stop line. Support-end joints carry plate weight. Base location comes from the plate keys and stop pin in the slot lines, not the brackets. Single-bracket joint capacity stays DECLARED for Step 12. Restate T-nut totals as 96. |
| 8 | Nut travel left at Kmax | REJECT the 9.51 proxy; ACCEPT geometry | The measure reads the physical stop: 4.01. Step 2 A3h and T5 (one pitch, at least 8) contradict it. Smallest fix: keep the geometry, record 4.01, send the threshold (half pitch) to the Manager and the Step 8 coupon. Past Kmax the ring stop takes load, so grip stops rising. |

## Inputs to later steps

| Item | Owner |
|---|---|
| Holder collar into holder.py | Manager authorization |
| Travel threshold 8 vs 4.01 | Manager |
| Single-bracket support-end capacity | Step 12 |
| Class P legend and bounds | Topologist sign |
