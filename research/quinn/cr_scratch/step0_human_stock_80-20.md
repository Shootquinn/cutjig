## Human input: 80/20 stock on hand (DECLARED by human, 2026-11-08; BOM text from github.com/shootquinn/qmrd3, files "QMRD3 BOM V 1-07.txt" and "QMRD3 8020 EXTRUSION ORDER - REF ONLY.docx")

Supersedes the Manager's default of 1515 / 3030 for profile series. The profile is 80/20 SKU 30-6060: 60 mm x 60 mm, metric 30-series T-slot ("big boy", structurally efficient). The QMRD3 BOM says T-slot nuts for it are M6 roll-in with spring ball ("get the one for 3030"), fasteners M6.

Stock on hand (DECLARED; the human states it is exactly this much, shuffled between projects, believed uncut):

| Length (mm) | Length (in) | Qty |
|---|---|---|
| 1540 | 60.63 | 4 |
| 980 | 38.58 | 4 |
| 952 | 37.48 | 1 |
| 728 | 28.66 | 2 |
| 644 | 25.35 | 2 |
| 488 | 19.21 | 2 |
| 468 | 18.43 | 2 |

Total 15,688 mm (DERIVED; matches the order document's 617.6 in). Cut-to-length is available and cheap in this order ($2.20 per cut at the time of the QMRD3 order; DECLARED by that document), and the human is willing to buy cut-to-order lengths of the same 30-6060 profile for this project. Constraint: stay with 30-6060, do not drop to a smaller profile.

Planning consequences for the Engineer:
- Design the frame from the stock lengths above first, with cuts from those; list any extra cut-to-order lengths separately in a BOM with quantities.
- Model the 30-6060 profile (60 x 60 mm, 30 mm slot pitch; confirm the cross-section from the 80/20 catalog or CAD file) as a parametric extrusion in the CAD.
- M6 hardware (roll-in T-nuts with spring ball, M6 screws 10/16/20/25/30 mm in the QMRD3 inventory; confirm what is on hand for this project).
- Lengths are shared with other projects: record which stock lengths the jig consumes.
- Update the echo site registry: profile series = 30-6060.
