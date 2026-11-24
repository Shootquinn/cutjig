## Feature table: Detail 6 checklist against params.yaml

Risk is to the Step 3 blocking params review. H = a placeholder part would pass or fail the gate on dimensions alone; M = partial; L = low. Text-only run: visual gate NOT RUN (none due at Step 1).

| Part | Feature | params.yaml key | Risk |
|---|---|---|---|
| Receiver | Thread (pitch, flank, starts, major, engagement) | thread.pitch, flank_deg, starts, major, min_engage_pitches | L |
| Receiver | Thread lead-in and land | MISSING | M |
| Receiver | Floor seat | seat.min_contact_area, print.seat_clearance (area and clearance only; no seat diameter, depth or ledge) | M |
| Receiver | Register (pilot for cross-thread defence, D7) | MISSING | H |
| Receiver | Asymmetric key slot | MISSING | H |
| Holder | Cone | cone.alpha, cone.alpha_release, chain.t_c, H, t_h, t_b, h | L |
| Holder | Flange | MISSING (no flange OD, thickness) | H |
| Holder | Bearing recess (thrust washer pocket) | MISSING (friction.bearing is a coefficient only) | H |
| Holder | Key (asymmetric) | MISSING | H |
| Holder | Jacking holes | MISSING | H |
| Holder | Hard-stop face | stop.hard_stop_gap (6), stop.height_z, stop.g_stop; face geometry MISSING; see Gap 2 for owner ambiguity | M |
| Collet | Cone | cone.alpha (shared with holder) | L |
| Collet | Bore | collets.diameters, core.tol, collet.c_i (bore_free = d + tau + c_i) | L |
| Collet | Alternating slits | collet.slit_count, slit_width_seed, min_slit_clamped, web_strain_allow; no alternate-from-top/bottom flag, no slit length or overlap | M |
| Collet | Slit relief holes | MISSING | M |
| Collet | Foot key | MISSING | H |
| Collet | Core stop (ledge height, width) | MISSING | H |
| Collet | Rim notches (count per size) | MISSING | M |
| Collet | Grip-window label | MISSING (window is derivable from bore_free and spacing; no text, height or depth keys) | M |
| Collet | Lead-in chamfer and bore lip radius | MISSING | M |
| Collet | Colour per size | MISSING (D4 signifier) | L |
| Wing nut | Thread | thread.* (shared) | L |
| Wing nut | Bearing face | MISSING (no bearing OD or ID, no washer size) | H |
| Wing nut | Wings and planform | wingnut.body_od, wingnut.span only; wing count, root width, thickness, taper, arm MISSING | H |
| Wing nut | Tighten and loosen arrows | MISSING | L |
| Wing nut | Tommy-bar socket | MISSING | M |
| Wing nut | Dust skirt | MISSING | M |
| Base | Plate (length, width, thickness) | MISSING (only icd.footprint_x, footprint_y for the frame) | H |
| Base | Debris tray | MISSING (icd.cable_exit is prose) | M |
| Base | Drain | MISSING | M |
| Base | Slotted holes | hardware.baseplate_fasteners (count 8), screw_length_baseplate; slot length and width MISSING | M |
| Base | T-nut provisions | hardware.tnut_thread, tnut_type, tnut_sku, profile.slot_* , slots_per_face | L |
| Base | Feet or bolt-down | MISSING as a key (icd.tipover_statement is prose) | M |
| Accessory | Collet caddy | MISSING | M |
| Accessory | Alignment gauge | MISSING | M |
| Accessory | Steady rest or cradle for a 0.75 m core | MISSING (core.length_install 750 is the driver, no cradle keys) | H |
| Accessory | Witness scale and line | MISSING | M |

Count: 14 features carry a key (some partial), 24 are MISSING.

## Generator readiness verdict

NOT READY for on-demand use. An operator can command a bore at any diameter in 85 to 110 mm, because the bore, tolerance and clearance keys exist (collets.diameters, collets.envelope_min and envelope_max, core.tol, collet.c_i). The resulting part is a bore-and-cone blank, not a usable collet. Missing keys:

- collet.height and collet.grip_height (axial length; chain.H = 30 is a holder seed, not named as the collet grip height)
- collet.slit_length, collet.slit_overlap, collet.slit_alternate (alternating pattern), and a slit-count rule against diameter (slit_count is fixed at 12; an off-family 87.3 mm collet needs a rule, for example a target slit pitch)
- collet.relief_hole_diameter
- collet.foot_key_width, collet.foot_key_height (must match the receiver key slot, itself MISSING)
- collet.core_stop_height, collet.core_stop_width
- collet.chamfer_lead_in, collet.bore_lip_radius
- collet.rim_notch_count_rule (notch count per size)
- collet.label_text_format, label_height, label_depth, and colour assignment
- collet.file_name_pattern (must carry 92.5 as 092p5)
- collet.window_low and window_high as DERIVED outputs, so the caddy and label read them

Defects in what is present:
- collets.diameters and core.diameters duplicate the seven values; a custom collet edits only the first, so the core list drifts. Make core.diameters derived or drop it.
- collets.envelope_max 110 exceeds iris.throat_open_diameter 108.585. Gate B1: core diameter must be less than the throat in the open position. The generator needs a check (warn, not refuse, since the throat is a parameter) tied to the throat key.
- No key for the request interface or usage instructions (the gate deliverable). That belongs in the generator's own documentation, but params should carry the defaults it prints.

## Over-constraint list (against gate decisions)

1. stop.height_z 850 (and icd.stop_height 850, a duplicate): a fixed stop height above datum A. Gate B6 allows a 0.75 m core and possibly 1 m; 850 mm is below the top of a 1 m core standing on the base. Make it DERIVED from core length, upper travel and holder height, or label it a seed that Step 12 overwrites. Do not let it act as a limit.
2. jig.height_target 2000 with height_is_soft true: correctly soft. Keep it out of any test as a bound. No hard limit found.
3. upper.travel_max 500: named "max" and DECLARED as a limit. Gate says the need is no more than 0.5 m of travel; fine as a ceiling for the drill, but must not cap core length. core.length_capture, install and optional are separate keys and do not reference it. No conflict.
4. frame.members, footprint_x 644, footprint_y 608: footprint is set by the stock bin (D8 repeats). The stock is human-declared, so not a violation, but the base plate, tray, steady rest and tip-over all inherit a footprint no load case chose. Treat as soft; allow longer or extra cuts.
5. wingnut.span 230 and body_od 181: the source (Loftsman, earlier review) fitted the span to a printer bed minus margin. Gate B2 makes the printer not a design input. The span must come from the moment-arm requirement (10 N m holding torque), not the bed. Confirm the seed is not bed-derived; it is the only suspect printer-derived number.
6. print.min_wall 1.2: a nozzle-width multiple in disguise. Gate B2 forbids nozzle values. Keep as a design rule only; do not let it veto a thin wing or slit web.
7. thread.major 165 (ASSUMED, from the 20 degree cone chain): it drives nut OD 181 and the whole radial layout. Step 3 replaces it; do not let downstream keys hard-code it.
8. icd.keepout_radius 81.2 is described as including the face annulus r_face (86.2), but equals 76.2 + 5. The derived value contradicts its own source line. Not a constraint on freedom, but a stale derivation the Step 3 gate will trip on.
9. iris.throat_open_diameter and throat_open_radius are two independent DECLARED keys. The drill is being re-made; if one changes the other goes stale. Make one DERIVED.
10. iris.leaf_count 4 (VERIFIED) cites a 7-in-model line; the source note says "7 in model". Reads as a count mismatch, not a constraint.

No printer bed, material or nozzle key is present; P1 enforces it. No hard limit on core length or jig height.

## Ranked gap list (risk to Step 3 blocking gate)

1. Wing nut wings, bearing face, tommy-bar socket. Without them the nut is a ring with two stated sizes (181 body, 230 span). The 10 N m holding-torque design assumption cannot be checked against a clamp force; there is no moment arm, root section or washer radius. Placeholder part: the "very large wing nut".
2. Holder flange, bearing recess, key, jacking holes, hard-stop face; and the stop owner. Placeholder: the holder is a cone plus a ring. Release (D6) and jam recovery have no geometry. Also resolve one ambiguity: stop.* is the upper-assembly metal stop (gate B5), but stop.hard_stop_gap 6 ("z0 + s_z + margin") reads as the holder-flange-to-boss-rim over-travel gap that bounds clamp force. Two different stops, one gap key. Add holder.flange_rim_gap as its own key.
3. Receiver register, asymmetric key slot, thread lead-in and land, floor seat dimensions. Placeholder: the receiver is a threaded tube. A key defined only by volume is the pressure-plate-as-flat-ring failure; the cross-thread defence at 135 to 165 mm is the register alone.
4. Collet foot key and core stop, plus the generator keys listed above. Placeholder: all seven collets are bore-and-cone blanks, and the generator cannot serve a custom request. This is a gate B3 deliverable.
5. Base plate dimensions, debris tray, drain, slotted-hole size, feet or bolt-down. Placeholder: a plate with no size and a tray that is prose. Tip-over (D8) stays unquantified.
6. Steady rest or cradle for the 0.75 m core. Placeholder: none; the operator holds the core. A 750 mm core has about 1.9 degree free tilt in the release pose (Loftsman), so this is the most visible loading hazard.
7. Slit alternation, slit length, relief holes, rim notches, grip-window label, lead-in chamfer, colour. Placeholder: slits without relief crack; unlabelled collets at 2.5 mm spacing are indistinguishable (D4).
8. Dust skirt, tighten arrows, caddy, alignment gauge, witness scale. Placeholder: signifiers and accessories absent. Low consequence for geometry, but the Step 4 completeness gate fails without them.

Recorded, not blocking. Step 3 carries the blocking params review.
