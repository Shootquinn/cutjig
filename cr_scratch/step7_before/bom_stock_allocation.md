## On hand

| Length_mm | Qty | Total_mm |
|---|---|---|
| 1540 | 4 | 6160 |
| 980 | 4 | 3920 |
| 952 | 1 | 952 |
| 728 | 2 | 1456 |
| 644 | 2 | 1288 |
| 488 | 2 | 976 |
| 468 | 2 | 936 |

Total on hand 15688 mm (DECLARED, step0_human_stock_80-20.md; computed here). Stock is shared with other projects.

## Allocation

| Member | Source_mm | Cut_mm | Qty | Role |
|---|---|---|---|---|
| rail | 644 | 644 | 2 | base frame side rail along X |
| end | 488 | 488 | 2 | base frame end member between rails |
| plate_support | 468 | 468 | 2 | base plate support cross member, inboard of the end members |

Allocation is from on-hand stock (ASSUMED roles, Design Notes 7). Each member uses a whole stock piece, so no saw cut is needed. 1540 mm lengths are reserved for columns at Step 12 and are unused here.

## Consumption

| Source_mm | Pieces_on_hand | Pieces_used | Pieces_left | Length_used_mm | Length_left_mm |
|---|---|---|---|---|---|
| 1540 | 4 | 0 | 4 | 0 | 6160 |
| 980 | 4 | 0 | 4 | 0 | 3920 |
| 952 | 1 | 0 | 1 | 0 | 952 |
| 728 | 2 | 0 | 2 | 0 | 1456 |
| 644 | 2 | 2 | 0 | 1288 | 0 |
| 488 | 2 | 2 | 0 | 976 | 0 |
| 468 | 2 | 2 | 0 | 936 | 0 |

Jig consumes 3200 mm of 15688 mm; 12488 mm remains for other projects (computed).

## Extra cuts

| Member | Source_mm | Cut_mm | Qty | Note |
|---|---|---|---|---|

None required at Step 1. Cut-to-order lengths of 30-6060 are allowed ($2.20 per cut, DECLARED) and are listed only in this table when added.
