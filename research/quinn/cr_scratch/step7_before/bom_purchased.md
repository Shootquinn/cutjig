## Brackets

| Class | Candidate SKU | Qty | Note |
|---|---|---|---|
| full-size 30-series corner bracket, leg at least 57 mm | 8020-14089 | 8 | 4 outer-corner joints x 2; verify SKU and leg length at purchase |

Superseded: 30-4332 (legs A = B = 30 mm, below bracket_leg_min); 30-4302 retired with it. Source: Step 2 bracket choice rule (full-size only, per joint). Bracket count is ASSUMED. 8 printed brackets (not purchased) take the 4 plate-support ends: 68 mm legs, 57 mm wide, 7 mm plate, slotted 7.0 mm holes (10.0 and 11.0 long) at 29.2 mm pitch along the leg, 30 mm across, clearing M6; file 8020 30 Series Corner Bracket 3dp.stl.

## T-nuts

| Type | Candidate SKU | Qty | Note |
|---|---|---|---|
| M6 spring-ball roll-in | PZRT 3030 Series Roll-in Spring M6 T Nut, roll-ball elastic, 8 mm T-slot European standard, 12-pack (Amazon) | 150 | 16 brackets (purchased and printed) x 8 + 8 base plate, plus 10 % spares; fit in the 30 slot is declared by use (hardware.tnut_fit_30series) |

## Fasteners

| Item | Qty | Note |
|---|---|---|
| M6 x 16 stainless button or socket head screw | 141 | bracket to T-nut |
| M6 x 20 stainless socket head screw | 9 | base plate to frame T-nuts |
| M6 stainless flat washer | 150 | one per screw |

Stainless M6 for non-80/20 joints. On-hand screw inventory is treated as nil (Design Notes 12); lengths follow the QMRD3 inventory list. Counts are computed by build_parts/bom_tools.py from params.yaml `hardware.*` and `frame.joints`.
