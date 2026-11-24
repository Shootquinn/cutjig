# Step 3 gate edits

## g_stop
- params.yaml `stop.g_stop` stays 25; source rewritten to a plain mechanical clearance (cutter lowest point at hard stop to collar top), status ASSUMED -> DECLARED, no standard cited. Derived values unchanged.
- gameplan.md: ISO 13854 / finger-crush text removed (Step 3 absorb list, Step 3 result notes, gate log row); pinch-point wording removed from the review rubric, A5, D5, Step 9 note and human-actions lines.
- Usability clearances kept, described as hand access for turning the wings.

## Renames
- `wingnut.knuckle_clearance` -> `wingnut.hand_clearance` (params.yaml, tests/test_params_bom.py, gameplan.md text "hand clearance 50"). No test IDs encoded finger or crush.

## T-nuts
- params.yaml `hardware.tnut_sku`, `tnut_type` set to PZRT 3030 Series Roll-in Spring M6 T Nut, roll-ball elastic, 8 mm T-slot European standard (12-pack, Amazon); `tnut_fit_30series` = "declared by use"; all DECLARED.
- Removed: `hardware.tnut_sku_alt`, the whole `tnut:` section (head 16.0 / neck 7.7), candidates 40-3914, 13031, 13098 from params, gameplan.md, ASSEMBLY.md, vendor_sources.md (two rows dropped, one replaced, one-line note kept).
- build_parts/bom_tools.py: BOM row text drops the alt and the acceptance limits. bom_purchased.md and report_assumptions.md regenerated via `python build_parts/bom_tools.py`.
- `tnuts_per_bracket` 8 unchanged.

## Tests
- tests/test_params_bom.py: rows updated (g_stop DECLARED, tnut rows replaced one for one, needles 13098 -> PZRT 3030). `python -m pytest tests/test_params_bom.py -q`: 197 passed (was 197).

## Remaining hits (final grep)
- "pinch plane / pinched off" (params.yaml 64, gameplan 348, 393, 567, 702, report_assumptions 34): kerf sphere geometry of the 7 in model, not a hazard.
- "safety factor" (gameplan 111, 337): structural load statement, not g_stop.
- "finger collets / axial fingers" (gameplan 526): collet slit geometry.
- "7.7", "16.0" in verify_step3.py and docs: unrelated numbers.
