## Gate status

visual gate RUN. 122 of 122 PNGs read (INDEX.md rows). Unreadable: none. Pose numbers checked against step7_engineer_renders_findings.md before any verdict.

## 1. Rubric verdicts

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Base plate | PASS | baseplate_top/bottom: -Y slot row sits 25 px +X of the +Y row, so a mirrored plate differs; 180 deg yaw maps the slots onto themselves and is caught by the pin pocket (+X) and the two plate keys (+Y edge) in baseplate_bottom. Receiver-foot flat in receiver_iso. Seat on frame in frame_plate_seat_closeup. baseplate_slots_closeup shows one slot only (clerical) |
| 2 | Receiver | PASS (features); WRONG (render) | Key slot at 37 deg (receiver_top), external thread and ruler pad (receiver_iso, witness_*). Lead-in and floor seat never shown: the receiver is uncut in receiver_section, section_R/Kd1/Kmax, core_R_100p0_stand_section, witness_Kd1/Kmax_section (7 PNGs). core_Kmax_100p0_stand_section cuts it correctly, so the harness cut fails silently |
| 3 | Holder | PASS | Collar and four holes (holder_top, holder_iso), cone (holder_section), index notch and key tab (holder_iso), HD7 tick (holder_tick_*). The two tick PNGs are pixel-identical (camera tracks the holder); pose reads from the witness set |
| 4 | Collet | PASS (features); WRONG (render colour) | Foot key at 37 deg seated in the receiver slot (in_situ_top), slits narrower at Kmax than R, notch count 1 / 5 / 7 for 90 / 100 / 105, label recess. Render colours 90 blue, 100 gold, 105 copper; collet.colour gives red, blue, white |
| 5 | Nut | PASS | Single marked wing (wing1 PNGs blank in R, wing0 blank at Kmax). nut_R_top: NT4 at az 78 points +X, clockwise; NT8 arc counter-clockwise. nut_R_bottom: NT5 points -X at the same wing, counter-clockwise. Kmax set agrees at az 241.5. Sockets and skirt in nut_*_iso |
| 6 | Washer | PASS | Off-axis tab notch (washer_*_top); notch turns R to Kmax by the nut's own angle (about +164 deg); ring in the nut pocket in section_* |
| 7 | Core stand-in | PASS (feature); WRONG (render) | Top chamfer in core_*_top_closeup; square bottom end on the collet core stop in core_Kmax_100p0_stand_section. core_*_top_section are flat grey frames with no edge (framing) |
| 8 | Frame | PASS | Six members (frame_top), datum notch on one rail only (frame_notch_*, c6_site_2_top shows it, c6_site_4_top does not) |
| 9 | Brackets / C6 | PASS | All four sites: printed bracket on the outer face of the end member, purchased bracket on the inner face, member between; no overlap, no member through another (c6_site_1..4 top/under) |
| 10 | T-nuts | PASS | 8 per bracket (bracket_tnut_closeup), in the slots (whole_*_side) |
| 11 | Cutter keep-out | PASS | Tube, face annulus, funnel, ring coaxial; face annulus clear above the collar in both poses (cutter_*) |
| 12 | Tray, plug, stop | PASS | Hip lines to the drain, bar-lug plug seated on the plate (tray_*). ST1 pad at its declared interface (centre about 223 mm +Y by pixel scale against 214 declared), no support drawn |
| 13 | Pose legibility, witness | PASS | Nut and holder drop R to Kd1 to Kmax in section_* and cutter_*_section. Closeups: Kmax index sits above k1, reads 1.5; Kd1 nine lines below, reads about 8.6; R reads about 13.9 (= 8.6 + 5.27, the reading-face shift). Agrees with probe 1.525 / 8.615 |
| 14 | Placement | PASS with one ABSORB | No part flipped, displaced or on the wrong plane; marked wing and washer notch follow S(phi). Caddy and gauge on the floor at -Y and +X. Rest post through the +Y plate notch onto the rail. Rest ring and rollers sit at mid-height of the cutter sweep; one roller projects about 82 mm off axis against the tube's 76.2 (context_side), so the hold position lies inside the keep-out (D14) |
| 15 | Pride test | WRONG (render) until R1 to R3 close | Geometry: yes. Square plate, tray, receiver and red nut read as one product; the C6 joints are clean. The render set as delivered: no. A client sees section views with a solid receiver, a 100 mm collet in gold, and a pad floating in air |

## 2. Pride test, whole assembly

Shown without apology: whole_* four-view sets, frame_iso, c6 sites, nut and witness closeups. R and Kmax differ visibly in nut height and wing azimuth in every whole view; Kd1 reads in the sections and witness set. The opaque cutter tube in context_* hides the core and the rest rollers; the whole_* views use transparency and read correctly.

## 3. Design Critique

| # | Item | Type | Tag | Owner |
|---|---|---|---|---|
| R1 | Receiver uncut in 7 section PNGs; re-render with the receiver cut (verify a cut face exists before writing the PNG) | render | ABSORB | Step 7 fix pass (render harness) |
| R2 | Collet render colour from collet.colour per size | render | ABSORB | Step 7 fix pass |
| R3 | core_*_top_section reframed to show the top edge; stop pad drawn with a phantom column face or label "upper assembly" | render | ABSORB | Step 7 fix pass |
| R4 | context_* cutter keep-out transparent, as in whole_* | render | ABSORB | Step 7 fix pass |
| D14 | Rest hold position inside the cutter sweep; no park or released state shown. Render rest in hold and park with the keep-out and state the release height | functional | ABSORB | Step 9 (rest Pass 2) |
| D15 | Slot pattern built as a row offset; ASSEMBLY.md says "one slot offset". Align the wording | clerical | ABSORB | Step 7 close |

Carried, unchanged by the assembled views: D4, D7, D9, D12, D13.

BLOCK: none. No geometry defect is visible in more than one view, and the measured pose numbers agree with every image. R1 to R4 are presentation faults; criterion 13 requires them closed in the fix pass.

## 4. Fix-pass re-read list

receiver_section, section_R/Kd1/Kmax_100p0, core_R_100p0_stand_section, witness_Kd1/Kmax_100p0_section, core_R/Kmax_100p0_top_section, collet_* (12), stop_closeup, whole_* (16), context_* (7).

## Addendum: fix pass re-read

Read: receiver_section, section_R/Kd1/Kmax_100p0, core_R/Kmax_100p0_stand_section, witness_Kd1/Kmax_100p0_section, core_R/Kmax_100p0_top_section, collet_* (all 16), stop_closeup, context_side, whole_Kmax_100p0_iso, whole_Kmax_105p0_top (31 PNGs).

| # | Verdict | Evidence |
|---|---|---|
| R1 | CLEARED | Receiver cut in all 8: thread profile, top lead-in chamfer and floor seat in receiver_section; nut teeth mesh the receiver thread in section_*; collet on the floor seat and core on the core stop in both stand sections; ruler graduations show in profile in witness_*_section. FALLBACK flat caps read as solid section faces |
| R2 | CLEARED except one PNG | 90 red, 100 blue, 105 white in top, in-situ and underside views. collet_Kmax_105p0_underside: still WRONG on legibility. The white face renders at background grey and the part reads only by its outline; key and slits survive, the size colour does not. Fix: dark background (about 60/60/65) or raking side light for underside views. Leave the params colour unchanged |
| R3 | CLEARED | core_*_top_section show the 45 deg chamfer on the +X edge; stop_closeup shows the pad against a translucent column face. whole_* still show the pad free-floating, which the closeup now explains |
| R4 | CLEARED | context_side: cutter translucent, core and three rollers visible |
| 15 | CLEARED, conditional on the R2 underside fix | Section set, colours and context now present cleanly |

Observations, non-blocking:
- The 100 mm collet in blue sits beside a steel-blue receiver in section_* and the in-situ views. The two parts separate by saturation only. ABSORB, Step 9: change the receiver render colour.
- context_side now measures D14. The left roller spans x 975 to 1020 px, about 51 to 82 mm off axis, which crosses the cutter tube wall (73.0 to 76.2). D14 stays ABSORB at Step 9 and is now measured.

BLOCK: none.
