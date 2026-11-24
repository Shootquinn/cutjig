## 1. Measured against params

Method: `results/step_measure.json` (build_parts/measure_step.py, freecadcmd 1.1.4) plus numpy on the .3mf vertices. Slot walls found from wall-plane clusters in the plate.

| Item | Measured | params | Status |
|---|---|---|---|
| 14089 bbox | 57.35 x 57.35 x 57.0 mm, volume 32,918.6 mm3, 1 solid | 57 legs, 57 wide | VERIFIED |
| 14089 plate | 6.0 mm | 6 | VERIFIED |
| 14089 holes | none modelled (largest bore R 1.0 is a fillet) | not stated | ASSUMED. Zoro lists 14089 as "8 hole 57mm": 4 holes per leg, not 2 |
| `8020-14089 qmod v0.step` | 565 bytes, empty DATA section, no geometry | n/a | unusable; ignore |
| Printed STL | 68 x 68 x 57, 84,888 facets, 57,203 mm3 | 68 legs, 57 wide | VERIFIED |
| Printed plate | 7 mm | 7 | VERIFIED |
| Printed slots | 7.0 wide (z walls at +-11.5 and +-18.5, centres +-15); 10.0 and 11.0 long; centres 29.2 apart | 7 mm at 30 pitch | width and across pitch VERIFIED; along-leg pitch 29.2, not 30 (params wrong by 0.8) |

## 2. Part number

8020.net returned HTTP 403 on 8020-14089.html. Zoro lists "80/20 corner bracket 8 hole 57mm 14089" (https://zoro.com/8020-corner-bracket-8-hole-57mm-14089/i/G0815838, seen in search results; page itself 403). No page I could read names the series. Sibling 14095 is the 8-hole inside bracket "for 30-3060". Result: SKU stays ASSUMED, "verify at purchase". Dimension match is geometry-only.

## 3. Which printed file is the 68 mm class

- `8020 30 Series Corner Bracket 3dp.stl`: 68 mm legs, 57 wide, 7 mm plate. This is the 68 class.
- `...3dp.3mf`: same part, 68 x 68 x 57, 57,210 mm3, same slots. Use either.
- `...3dp XL.3mf`: 58 x 58 x 57, 46,077 mm3. It is the 57-class replica (about 1 mm oversize), not 68.
- Slot 7.0 mm against M6 (6.0 shank, 6.6 clearing hole): 1.0 mm diametral clearance to the shank, 0.4 mm to the clearing hole. Slot also passes the 8.0 mm profile opening.

## 4. T-nut fit, 30-6060 slot

Profile (step2 measure): opening 8.000, neck 2.2575, cavity 16.500 wide, floor 9.165 below face (cavity 6.908 below neck), floor width 8.064.
40-3914, per supplier listings: 22.00 x 13.70 x 7.00, labelled 40 series. 13098 (Steiner): "SLOT8", A 16.00, B 8.00, C 11.80.

Verdict for 40-3914: CANNOT TELL. The decider is the nut's neck width, which must be under 8.000. No readable source publishes it, and 8020.net is 403. The cavity is not the limiter: 13.70 is under 16.500. A 40-series nut is built for a 10 mm opening, so I expect it not to enter. The 7.00 mm height also exceeds the 6.908 mm cavity depth below the neck if that height is body only.
13098 is the only 8 mm-slot M6 ball-spring roll-in nut found. 16.00 is under 16.500 by 0.5 mm. It is ASSUMED to fit; its orientation of A/B/C is unconfirmed.
Action: BOM carries 13098 as the primary candidate, 40-3914 as unverified, both "verify at purchase".

## 5. Hand-written files restating these values (not edited)

- params.yaml: 242-244 (tnut thread, type, sku), 245 (alt 13031), 246-252 (bracket class, leg min, superseded SKU, printed_bracket, joints, bracket_sku), 254 (tnuts_per_bracket 2: conflicts with 8 holes per bracket).
- reference/vendor_sources.md: 3, 10-13, 15.
- bom_purchased.md: 5, 7, 13.
- build_parts/bom_tools.py: 147-150 (generator text, "30-series slot fit not stated").
- ASSEMBLY.md: 30, 31.
- gameplan.md: 301 (P4), 560, 613, 626-627, 645-646, 658, 706 (Echo registry row), 805.
