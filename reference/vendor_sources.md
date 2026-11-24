## Vendor reference record (2026-11-08)

Update 2026-11-08 (Step 2): the human supplied `8020-30-6060 X 1540.step`, `8020-14089.step` and a printed-bracket STL from their own folders (paths in research/quinn/cr_scratch/step2_engineer_profile_measure.md). The 30-6060 section is MEASURED from the STEP (916.56 mm2, VERIFIED in params.yaml `profile.*`). Earlier text, kept as history: no vendor STEP was downloaded at Step 1 because the 80/20 CAD form asks for personal details; the profile was then built from stated parameters tagged ASSUMED.

Product pages read as HTML (no download of CAD; values copied into params.yaml with the tag shown there):

| Page | Date read | Values taken |
|---|---|---|
| https://8020.net/30-6060.html | 2026-11-08 | eight open T-slots, two per 60 mm face; surface area 9.299 sq cm; weight 0.1441 lb per inch; 6063-T6 |
| https://8020.net/30-4332.html | 2026-11-08 | 30 Series 2 Hole Gusseted Inside Corner Bracket, A = B = 30 mm, C 4 mm |
| https://8020.net/30-4302.html | 2026-11-08 | 30 Series 2 Hole Inside Corner Bracket, A = B = 30 mm |
| Amazon, PZRT 3030 Series Roll-in Spring M6 T Nut, roll-ball elastic, 8 mm T-slot European standard, 12-pack (Step 3 gate) | 2026-11-08 | human-ordered part in use on 30-series stock; now `hardware.tnut_sku`; fit is declared by use |
| https://zoro.com/8020-corner-bracket-8-hole-57mm-14089/i/G0815838 (seen in search results; page 403) | 2026-11-08 | '80/20 corner bracket 8 hole 57mm 14089': 4 holes per leg; `hardware.tnuts_per_bracket` now 8 |

The `profile.*` section parameters are VERIFIED from the STEP at Step 2. Step 3 (research/quinn/cr_scratch/step3_engineer_hardware_confirm.md): the printed bracket is MEASURED, VERIFIED in params (file `8020 30 Series Corner Bracket 3dp.stl`: 68 x 68 x 57 mm, 7 mm plate, slots 7.0 mm wide at 29.2 mm pitch along the leg, not 30; the XL .3mf is 58 mm, the 57 class). The 8020-14089 geometry is VERIFIED from the human's STEP (57.35 x 57.35 x 57.0 mm, 6.0 mm plate); the SKU stays ASSUMED (8020.net returned 403, verify at purchase). The 30-series T-nut fit is declared by use.
