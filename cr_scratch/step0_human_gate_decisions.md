## Human decisions at the Step 0 gate (DECLARED by the human, 2026-11-08). These override defaults, reviewer findings and any UNVERIFIED flags they touch.

**B1, iris aperture.** 54.2925 mm is a radius (open diameter 108.585 mm). The new drill is being fabricated, so the value may change: the iris throat opening is a parameter, not a fixed gate. The cutting head sets core diameter, not the iris. Rule: core diameter must be less than the iris throat opening in the open position. Nominal core target is 100 mm. Mines manufacturing variation is expected. A narrower kerf (process optimization) is under consideration. Do not cut the 90 to 105 mm collet range on aperture grounds.

**B2, printer.** Not a design input. Do not ask about bed size, material or nozzle. Do not split any part to fit a bed. Design freely; the human will ask for help if something does not print.

**B3, collet family.** Seven collets at 2.5 mm spacing across 90 to 105 mm. Custom collets will be requested as needed. At project end the team must be ready to design a new collet at a moment's notice: the parametric collet generator and its usage instructions are a deliverable.

**B4, holding torque.** Friction collet holding will reach the requirement; the collet type is highly efficient. Torque is unknown. Design assumption: 10 N m. The core itself will likely fail before the collet slips. No positive core lock, no escalation path, no 20 N m or 50 N m placeholders.

**B5, nut role.** Yes: the metal hard stop belongs to the upper assembly. The wing nut only tightens the collet. It carries no descent load.

**B6, core length and height.** Goal: capture 0.5 m cores. The drill and upper assembly need no more than 0.5 m of travel. Plan to install a 0.75 m core, and potentially a 1 m core if that eases constraints. Total jig height should not exceed 2 m, but this is soft: members can be shortened later, and the limit must not constrain design freedom or become a source of stress.

**All other open or unverified items.** Resolve them. Adopt a stated assumption and move on. Do not carry an open-questions list, a to-do list, or a request for more human input into Step 1.

## Addendum at the Step 1 gate (DECLARED by the human, 2026-11-08)
- Step 2 approved: open it.
- Real 80/20 geometry exists locally: C:\Users\Quinn Morley\OneDrive\PROJECTS\Planet Enterprises\NIAC\BOREBOTS\Unleashed Robotics\ENGINEERING\FractalMining\Borebot Hardware\ holds "8020-30-6060 X 1540.step" (profile, 1540 mm long; the human usually keeps a 10 cm extrusion of the profile, so measure the cross-section from this file), "8020-14089.step", "8020-14089 qmod v0.step", "8020 30 Series Corner Bracket 3dp.stl/.3mf/XL.3mf" (the human's printed brackets). No 30-6060 DXF exists on OneDrive. Use these local files first; vendor download only if a needed part is not on disk. The human authorized entering their contact details on 80/20's CAD download form for that case; the orchestrator supplies them to the agent that needs them.
- Brackets: team chooses per joint. Full-size only, never mini ("no little Japanese hands": large, hand-friendly hardware throughout, including bracket and fastener access).
- FreeCAD is 1.1.4 at %LOCALAPPDATA%\Programs\FreeCAD 1.1\.
- Downloads are allowed.
