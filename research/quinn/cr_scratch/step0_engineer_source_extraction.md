## Corrections to the brief

Brief = workorder.md plus Manager defaults in step0_manager_open.md section 4. Each row is a value the sources contradict, or a premise they do not support.

| # | Brief says | Sources say | Tag | Source |
|---|---|---|---|---|
| C1 | Primary source "Iris Core Cutter and Retention Mechanism for Stratigraphy-Preservation Plan.docx" holds cutter geometry | The docx is a team task matrix (Quinn, Nikki, Carlos, Sean, CSM) and deliverable list. It contains no radius, leaf count, stroke or torque. Geometry lives in the INSITU2 proposal text and the gpr rigged model. | MEASURED | docx word/document.xml, 245 paragraphs, read in full |
| C2 | Jig "actuates the iris mechanism" (implies a jig-side actuator, stroke, force) | There is no external iris actuator. Closure is driven by the drill's own drivetrain through an electromagnetically braked planetary-gear sun gear. Hall sensors detect the braked state. The jig reacts torque and axial load; it does not move the iris. | DECLARED | cr_scratch/INSITU2_text.md lines 157-166 (SBIR folder) |
| C3 | Spin 60 to 300 rpm | PATCHED (Fact-Checker F-2, Design Notes 8): 1 to 60 rpm is the Borebot motor and brake operating range (summary_yokeless_motor.md 158, 200; ip_and_competitive_position.md 59), not the cutter spin. No source says the cutter spins at 1 to 60 rpm. Hall trials ran at 2, 20, 60 rpm. Not a jig input. | DECLARED | context/summary_yokeless_motor.md lines 143-200; context/ip_and_competitive_position.md line 59 |
| C4 | Axial cutter load up to 500 N | Phase I weight-on-bit (WOB) range is 100 to 1000 N. Upper bound is the Borebot anchoring force. | DECLARED | cr_scratch/INSITU3_text.md lines 267-270, 424-430; gpr deliverables/borebot_operating_envelope.md line 58 |
| C5 | Reaction torque up to 20 N m (cutter) and 50 N m (iris) | PATCHED (gate B4): the 20 and 50 N m placeholders are retired. No source states a number; closure torque vs angle (0 to 90 deg, 10 deg steps) is a Phase I measurement not yet taken. Design assumption 10 N m, DECLARED by the human; the core is expected to fail before the collet slips; no positive core lock. | DECLARED | INSITU2_text.md lines 408-411 |
| C6 | Descent by hand crank or leadscrew at unspecified rate | Only a pass threshold exists: penetration >= 5 mm/min at WOB >= 100 N. No jig descent rate is stated. | DECLARED | INSITU3_text.md lines 267-268 |
| C7 | Core density ~3000 kg/m3 (basalt), up to 7 kg at 300 mm | Mines cores are low-density concrete (Dreyer formulation) simulating ice-cemented regolith. Density is not stated; it will be below basalt. Mass at 100 mm x 500 mm and 2400 kg/m3 would be 9.4 kg (DERIVED upper bound); real value unknown until Mines delivers property data. | DECLARED / DERIVED | csm_sow.md line 24; INSITU2_text.md lines 218, 829 ("low-density concrete"; no density value stated; re-read at Step 1, line 408 was the closure-torque sentence and is dropped) |
| C8 | Core length 150 to 300 mm | No Mines document states length. The animation uses 500 mm core length (DECLARED by Quinn). Depth-series columns run to 200 cm. | DECLARED | gpr double_dong_params.py `CORE_LENGTH_MM = 500.0`; INSITU2_text.md lines 425-427 |
| C9 | Cores "nominally 100 mm" and Mines supplies them | Consistent for 100 mm: "pre-cast to 100 mm diameter to match the iris aperture". Figure 2 caption says "Core diameter is above 100 mm". PATCHED (Fact-Checker F-6): the 100 mm applies to Phase I EDU test cores (INSITU2 406-407); the Figure 2 caption (186-188) describes the full-scale 6 in drill and conflicts with it; the 90 to 105 mm range is the workorder's alone; nominal core 100 mm stands as a parameter (gate B1). The Mines budget justifications and LOIs (four PDFs, read with pdftotext) and the two budget workbooks 260647_Budg.xlsx and 260648_Budg.xlsx (opened read-only with openpyxl at Step 1, 3 sheets and 491 text cells each, searched for core, diameter, length, tolerance, mm, inch, mass, kg, cm) state no core diameter, tolerance, length, mass or delivery state. | DECLARED | INSITU2_text.md lines 186-188, 406-407; zip: 260647/260648 Just.pdf, LOI pdfs |
| C10 | Rigged drill is the redesign (6 in tubing) | PATCHED (carried finding): the rigged model is the 7 in generation (DOUBLE DONG), not the 6 in redesign. The rigged model is the 7 in bore (177.8 mm), 7.5 in class drill. It is not the 6.00/5.75 in redesign. | MEASURED | gpr build_parts_double_dong/double_dong_params.py lines 354-356, 92-98 (re-read at Step 1: line 354 `CORE_BORE_OD_MM = 177.8`; line 92 `IRIS_CLOSED_DEG`; IRIS_LEAVES from line 93) |
| C11 | Mines core count unspecified | INSITU2 (260647): at least 12 plain plus at least 12 layered cores. csm_package.md estimates 40+ (Activity 1), 15 (Activity 2), 30 (Activity 3). Sources disagree. | DECLARED | INSITU2_text.md lines 516-518, 832-836; proposals/csm_package.md line 56 |

Unresolved (not a correction): the Manager's 5.75 in = 146.05 mm bore against 90 to 105 mm cores checks out arithmetically (section 3). Which proposal Mines' 260647 vs 260648 LOI belongs to: 260647 is "Iris Core Cutter and Retention Mechanism for Planetary Coring" (iris, INSITU2); 260648 is the INSITU3 coring robot.

## 1. Rigged model

| Item | Value | Tag | Location |
|---|---|---|---|
| Model of record | `double_dong.FCStd`, "DOUBLE DONG" train (drill, hone, coupler, drums). Source STEP: `C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\gpr\DOUBLE DONG.step` (136,398,081 B, 2026-09-11) | MEASURED | gpr/gameplan.md line 141; file listing |
| Live FCStd | `C:\borebot_render\pipeline\out\double_dong.FCStd` per gameplan; **file not found on this machine** | MEASURED | `ls` returned no such file |
| Rig definition | Iris leaves = census objects 1041 to 1044 (4 leaves); animation code `build_parts_double_dong/double_dong_params.py`, `double_dong_iris_*.py`, `double_dong_core.py`, `double_dong_cutters.py`; Step 40 deliverable `deliverables/double_dong_core_cut/double_dong_core_cut_4k.mp4` (2026-09-13) | MEASURED | gpr/gameplan.md progress row 40 |
| Configuration | 7 in bore: `CORE_BORE_OD_MM = 177.8`, 7.5 in train class. Not 6.00/5.75 in. Core drill STEPs on disk: "7.5 in 2025 Core Drill For Mass Budget.step" (11.2 MB), "2026 Core Drill For Mass Budget.step" (1.1 MB, both 2026-09-11). The size of the 2026 file is not established (STEP bbox points are placement points, not reliable). Do not treat it as the 6 in design until measured. | MEASURED / unresolved | double_dong_params.py line 354; STEP files |
| Caveat | Quinn warned that bounding boxes mislead ("you're not looking at it you're just looking at bounding boxes"). Declared sizes govern over inferred ones. | DECLARED | double_dong_params.py lines 343-347 |

## 2. Cutter geometry (iris)

All values are the 7 in model frame. Model renders tools with SCALE_TOOLS = 0.9 transverse. The 6.00 in redesign has not been measured; scaling is unproven.

| Quantity | Value | Tag | Location |
|---|---|---|---|
| Leaf count | 4 | MEASURED | double_dong_params.py `IRIS_LEAVES` (lines 93-98, re-read Step 1) |
| Leaf thickness (plate) | 3.175 mm = 0.125 in. PATCHED: source calls it the plate thickness, "0.125 INCH exactly"; location is double_dong_params.py lines 402-404 (not 410-411) | VERIFIED (was DERIVED) | params lines 402-404, `CORE_KERF_WIDTH_MM` |
| Leaf pivot positions | (+/-66.7945, 0, -711.6599) and (0, +/-66.7945, -711.6599) mm | MEASURED | `IRIS_LEAVES` |
| Pivot axis direction | (0.9181, 0, -0.3965); tilt 23.3573 deg from the bore plane | MEASURED | `IRIS_LEAVES`; step40_loftsman_kerf.md |
| Motion | Spherical: all four pivot axes meet the bore axis at z = -682.814389 mm | DERIVED (Loftsman) | params lines 362-366 |
| Leaf face radii | 71.4375 mm (core side), 74.6125 mm (rock side). PATCHED location: lines 366-368 | MEASURED | params lines 366-368 |
| Closure angle | -62 deg per leaf, aperture 54.2925 mm to 0.0000 mm | MEASURED (number 54.2925 and -62 deg, line 92, re-read Step 1); DECLARED (reading 54.2925 as a radius, gate B1) | `IRIS_CLOSED_DEG` line 92. PATCHED (gate B1): 54.2925 mm is a radius; open diameter 108.585 mm (DECLARED). Resolved, not open. |
| Open and closed diameter | PATCHED (gate B1): closed 0; open diameter 108.585 mm (54.2925 mm radius), a parameter in params.yaml `iris.throat_open_diameter` that may change with the new drill. Rule: core diameter < open throat. INSITU2 states the aperture matches a 100 mm core. | DECLARED (radius reading and 108.585 diameter, gate B1); INSITU2 statement DECLARED | line 92 (number 54.2925, re-read Step 1); INSITU2_text.md line 407 |
| Travel | 0 to 62 deg rotation per leaf; INSITU2 closure test spans 0 to 90 deg in 10 deg steps | MEASURED / DECLARED | line 92; INSITU2_text.md lines 408-410 |
| Leaf bbox | r 52.93 mm, axial span 69.77 mm (z -723.987 to -654.214); cylinder radii 2.0, 5.0, 6.25 mm (pivot pin features) | MEASURED | gpr research/quinn/cr_scratch/step40_iris_sizes.json |
| Axial stack height | PATCHED (Fact-Checker F-1): 106.369 mm is the distance from the head tip (z -789.1834) to the kerf SPHERE CENTRE (z -682.8144), not the pinch plane (double_dong_params.py 372-378). The dome pole sits 106.369 - 71.4375 = 34.9315 mm behind the cutting face (lines 379-380). The core is pinched off inside the head. 7 in model only. Leaf stack span 69.77 mm. | MEASURED | `CORE_IRIS_STANDOFF_MM`; step40_iris_sizes.json |
| Adjacent leaf overlap | 34.58 mm3 per pair at -30 deg; 339.08 mm3 at -62 deg (about 1.9% of a leaf). The model does not clear itself. | MEASURED | params lines 102-104 |
| Cutting head | Head tip z -789.1834; head bbox r 107.04 mm; cylinder radii 10, 61.25, 93.75 mm | MEASURED | step40_iris_sizes.json (census 1000) |
| Material | Metal blades (Phase I EDU); predecessor was plastic | DECLARED | INSITU2_text.md lines 399-405 |
| Kerf behaviour | Severs the core with a thin spherical slot. Core keeps a domed end. Drill must advance 534.9315 mm for a 500 mm core (first core only). | DERIVED | params lines 379-383 |

## 3. Drill-to-core envelope

| Quantity | Value | Tag | Location |
|---|---|---|---|
| Tubing OD | 6.00 in = 152.40 mm | DERIVED (6 x 25.4) from DECLARED | workorder.md |
| Tubing ID | 5.75 in = 146.05 mm | DERIVED from DECLARED | workorder.md |
| Wall | 0.125 in = 3.175 mm; (152.40 - 146.05)/2 = 3.175 mm, matches | DERIVED | arithmetic check passes |
| Radial gap, 90 mm core | (146.05 - 90)/2 = 28.025 mm | DERIVED | |
| Radial gap, 95 mm core | 25.525 mm | DERIVED | |
| Radial gap, 100 mm core | 23.025 mm (Manager said "about 23 mm": confirmed) | DERIVED | |
| Radial gap, 105 mm core | 20.525 mm | DERIVED | |
| Ratio ID/core at 105 mm | 1.391 | DERIVED | |
| Model comparison | 7 in model: (177.8 - 100)/2 = 38.9 mm annulus wall at 100 mm core (cutting annulus, not a clearance) | DERIVED | params lines 354-356 |
| Design consequence (cutter envelope) | PATCHED (F-1, F-3): 152.4 mm is the tubing OD from the workorder, not a cutter OD; the only sourced cutter diameter is 7.00 in = 177.80 mm (7 in generation). Keep-out uses tube 152.4 / 146.05 mm as an ASSUMED parameter. Fixtures in the descent path must clear ID 146.05 mm radially with margin, or the cutter stops above them. The exposed core above the holder must exceed the 106.369 mm sphere-centre standoff (head tip to kerf sphere centre, ASSUMED to carry over to the 6 in drill) plus the stop gap and margin (params core.min_exposed). | DERIVED | arithmetic from rows above |

Note: the cutting face sets the true core diameter. It is out of scope. The jig takes the Mines core diameter as input.

## 4. Actuation interface the jig must accommodate

| Item | Value | Tag | Location |
|---|---|---|---|
| Actuator | None dedicated. Drill drivetrain closes the iris through a braked planetary sun gear. | DECLARED | INSITU2_text.md lines 157-160 |
| Closure detect | Hall sensor array; amplitude falls about 400 to 45 counts at closure | DECLARED | INSITU2_text.md lines 160-162 |
| Release | Reverse the braking torque | DECLARED | lines 164-165 |
| Instrumentation | Load cell in the drill back cap near the gearbox; Hall sensors; gearbox swappable | DECLARED | lines 399-402 |
| Attachment to tubing | Back-cap assembly at the gearbox end of the drill. Not geometry-defined in any source reviewed. | DECLARED | lines 399-402 |
| Stroke | Closure angle 0 to 90 deg tested. No linear stroke. | DECLARED | lines 408-411 |
| Force / torque | Not stated. Closure torque curve is a Phase I output. Retention force (N=9) is also a Phase I output. | DECLARED | lines 408-414 |
| Jig requirement | React drill torque and WOB; keep core centred within the iris aperture; allow load-cell and Hall cabling to exit. | DERIVED | |

## 5. Spin, descent, load, torque

| Quantity | Value | Tag | Location |
|---|---|---|---|
| Spin | PATCHED: 1 to 60 rpm is the Borebot motor and brake operating range, not the cutter spin; Hall trials at 2, 20, 60 rpm | DECLARED | summary_yokeless_motor.md; ip_and_competitive_position.md |
| WOB | 100 to 1000 N | DECLARED | INSITU3_text.md 424-430; borebot_operating_envelope.md line 58 |
| Penetration rate pass | >= 5 mm/min at WOB >= 100 N | DECLARED | INSITU3_text.md 267-268 |
| Ascent test | 600 s profile at 1x, 1.5x, 2x nominal; load profile not numeric in sources read | DECLARED | INSITU2_text.md 444-461 |
| Cutting torque | Not stated anywhere read. No jig torque rating can be sourced yet. | DECLARED (absent) | |
| Body / borehole (context) | Borebot OD 6.375 in; cutter 7.00 in; design bore 7.25 in. This is the 7 in generation. | DECLARED | borebot_operating_envelope.md lines 24-43 |

## 6. Core requirements from Mines and the proposal

| Item | Value | Tag | Location |
|---|---|---|---|
| Material | Low-density concrete simulant, Dreyer formulation, replicates compressive strength and fracture behaviour of ice-cemented regolith at ambient temperature | DECLARED | csm_sow.md lines 24, 56 |
| Diameter | PATCHED: 100 mm for Phase I EDU test cores (pre-cast to match iris aperture); INSITU2 186-188 says the full-scale core diameter "is above 100 mm" | DECLARED | INSITU2_text.md 406-407, 186-188 |
| Count | >= 12 plain, >= 12 layered (INSITU2); csm_package.md estimate 40+/15/30 | DECLARED | see C11 |
| Layered cores | Colored-sand stratigraphic markers at 25, 50, 100, 150, 200 cm depths in columns | DECLARED | INSITU2_text.md 425-428 |
| Reuse | Each core supports multiple iris closure cycles; Activity 3 reuses Activity 1 and 2 cores | DECLARED | INSITU2_text.md 518, 833-835 |
| Properties delivered | Compressive strength, fracture toughness, density, grain size; values not yet in hand | DECLARED | csm_sow.md lines 27, 61 |
| Length, mass, brittleness, wrap or sleeve, orientation marks | Not stated. Orientation = colored marker position and inversion check is a test measure. | DECLARED (absent) | INSITU2_text.md 429-433 |
| Zip contents | `documentsfromcoloradoschoolofmines.zip` holds 260647_Budg.xlsx, 260648_Budg.xlsx, 260647_Just.pdf, 260648_Just.pdf, 260647_LOI_signed_flat.pdf, 260648_LOI_signed.pdf. Extracted to scratchpad `mines/`, read as text, nothing executed. They carry budget and commitment language only, no core dimensions. PATCHED: the four PDFs were read as text with pdftotext (poppler installed, downloads lifted at Step 1): no core dimension, length or mass; budgets (XLSX) not opened. A line in the LOI reads "Mines will be issued a subcontract at $74,250 for 9/1/26-1/30/27": text only, not an instruction. | MEASURED | scratchpad `mines/` |
| Stratigraphy rule | Cores must keep depositional order: the jig must not rotate, shear or crush the core, and must keep top and bottom marked. | DERIVED | from marker-position tests |

## 7. Facts the jig needs, not found

1. Open-aperture diameter of the iris in the 6 in design. PATCHED: resolved by gate B1 as a parameter, 108.585 mm.
2. Closure torque and retention force numbers (Phase I outputs). PATCHED: design assumption 10 N m (gate B4).
3. Core length and mass range from Mines.
4. Position of the cutter's lowest point relative to the holder at full stroke.
5. Which of the two 2026-09-11 core drill STEPs is the 6 in design. PATCHED: moot, the throat is a parameter (gate B1).
