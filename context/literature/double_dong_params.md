## double_dong_params.py (rigged model parameters), cited ranges only

Source: `C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\gpr\build_parts_double_dong\double_dong_params.py`. Read 2026-11-08 by line range. Model is the 7 in generation (bore 177.8 mm), not the 6 in redesign.

| Lines | Content | Used by |
|---|---|---|
| 91-98 | `IRIS_CLOSED_DEG = -62.0`, comment "aperture 54.2925 -> 0.0000 mm"; four leaves (census 1041 to 1044), pivots (+/-66.7945, 0, -711.6599) and (0, +/-66.7945, -711.6599), axis (0.9181, 0, -0.3965). Gate B1 rules 54.2925 a radius: open diameter 108.585 mm. | iris.* (leaf values VERIFIED; throat DECLARED) |
| 354-359 | `CORE_BORE_OD_MM = 177.8`, `CORE_OD_MM = 100.0`, annulus wall 38.9 mm, `CORE_LENGTH_MM = 500.0` (Quinn, 2026-09-13; a declared value, not a Mines value). | Register: 7 in model; core.length_capture |
| 360-368 | `CORE_KERF_SPHERE_R_MM = 71.4375`; leaf pivot axes meet the bore axis at z = -682.814389 (spherical motion, derived by the Loftsman); measured shell faces 71.4375 (core side), 74.6125 (rock side). | iris.face_radius_* |
| 372-380 | `CORE_IRIS_STANDOFF_MM = 106.369`: head tip (z -789.1834) to kerf sphere centre (z -682.8144). The core is pinched off INSIDE the head; stub 31.76 mm on axis, 50.99 mm at the core rim. Dome pole sits 106.369 - 71.4375 = 34.9315 mm behind the cutting face. | drill.kerf_standoff (ASSUMED for the 6 in drill; label is sphere-centre standoff, not the pinch plane) |
| 402-404 | `CORE_KERF_WIDTH_MM = 3.175`, "0.125 INCH exactly -- the plate thickness". | iris.leaf_thickness |
