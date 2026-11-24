## Report assumptions list

Counts: DECLARED 25, ASSUMED 283, VERIFIED 38, DERIVED 83, total 429

| Key | Label | Source |
|---|---|---|
| `meta.units` | DECLARED | gameplan Design Notes 4 |
| `meta.seed_date` | DECLARED | Step 1 run |
| `iris.throat_open_radius` | DECLARED | gate B1 (research/quinn/cr_scratch/step0_human_gate_decisions.md) rules 54.2925 a radius; number at double_dong_params.py line 92 (re-read Step 1). A parameter: the new drill is being fabricated and it may change. Change the radius only; the diameter follows. |
| `core.diameters` | DECLARED | workorder.md range 90 to 105; gate B3 seven collets at 2.5 mm (single source for core diameters and the collet family) |
| `core.tol` | ASSUMED | Design Notes 12 assumption: covers Mines manufacturing variation; Phase I data replaces it |
| `core.length_capture` | DECLARED | gate B6 (capture goal 0.5 m) |
| `core.length_install` | DECLARED | gate B6 (install 0.75 m) |
| `core.length_optional` | DECLARED | gate B6 (optional 1 m) |
| `core.density` | ASSUMED | Design Notes 12 assumption; Mines density not stated |
| `upper.travel_max` | DECLARED | gate B6 (upper assembly working stroke at most 0.5 m); the loading park is separate (upper.park_z), research/quinn/cr_scratch/step2_system_concept.md U13 |
| `upper.metal_stop` | DECLARED | gate B5 (stop owner); research/quinn/cr_scratch/step2_system_concept.md decision 8 (i) and ICD rows Stop rating, Stop gap |
| `upper.park_z` | ASSUMED | U13: stop.collar_top_z 159.84 + core.length_install 750 + upper.load_clearance 50 = 959.84 (was 950); a loading position, not working travel; the rule follows core length (1209.84 for the 1 m core) (research/quinn/cr_scratch/step2_system_concept.md) |
| `upper.park_lock` | ASSUMED | U13 (research/quinn/cr_scratch/step2_system_concept.md); flagged for the human |
| `upper.manual_raise` | ASSUMED | U15 (research/quinn/cr_scratch/step2_system_concept.md); 80 N is an assumption |
| `upper.raise_fuse` | ASSUMED | U15: shear link in the hoist line = 147 N carriage weight + 150 N jam force; jam force on the core at most 150 N below the 204 N of H2 (research/quinn/cr_scratch/step2_system_concept.md) |
| `upper.load_clearance` | ASSUMED | clearance of the cutter lowest point above the core bottom at the loading park (U13 rule) |
| `jig.height_target` | DECLARED | gate B6 (2 m soft target; recorded and reported, never tested as a limit) |
| `jig.height_is_soft` | DECLARED | gate B6 (yields to design freedom) |
| `loads.torque_design` | DECLARED | gate B4 (design assumption; 20 and 50 N m placeholders retired; no positive core lock) |
| `loads.axial_design` | ASSUMED | design choice bounded by the Phase I WOB test range, INSITU3_text.md 424-430 |
| `loads.nut_torque` | ASSUMED | nut torque used for the holding prediction, hand limit (research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md section 5) |
| `loads.lateral` | ASSUMED | lateral load on the core at 106.4 mm or more above the holder (research/quinn/cr_scratch/step2_system_concept.md decision 3a) |
| `loads.nut_torque_abuse` | ASSUMED | abuse torque (research/quinn/cr_scratch/step3_designer_params.md S2-7c); axial about 0.8 kN by linear scaling of 1.6 kN at 50 N m; ten-member check runs in Step 5 |
| `loads.hand_force_bar` | ASSUMED | hand force on a tommy bar (research/quinn/cr_scratch/step3_designer_params.md S2-7c) |
| `drill.tube_od` | ASSUMED | workorder.md 6.00 in tubing OD; used as keep-out, NOT a cutter OD (Fact-Checker F-3) |
| `drill.tube_id` | ASSUMED | workorder.md 5.75 in tubing ID; keep-out |
| `drill.r_face_margin` | ASSUMED | Design Notes 12: R_face = 76.2 + 10 mm |
| `drill.kerf_standoff` | ASSUMED | double_dong_params.py 372-378: head tip to kerf SPHERE CENTRE, 7 in model, not the pinch plane; carried to the 6 in drill by assumption |
| `collets.count` | DECLARED | gate B3 |
| `collets.spacing` | DECLARED | gate B3 |
| `collets.envelope_min` | ASSUMED | generator envelope default, Detail 1 |
| `collets.min_throat_slack` | ASSUMED | Designer defect B1: slack kept between the largest core plus tolerance and the open throat |
| `collet.c_i` | ASSUMED | bore_free(d) = d + tau + c_i; seed d + 2 mm (Echo registry), tau = core.tol |
| `collet.slit_count` | ASSUMED | Design Notes 11 seed N = 12; confirmed in research/quinn/cr_scratch/step2_system_concept.md decision 7 |
| `collet.slit_width_seed` | ASSUMED | Echo registry seed w_s about 1.5 mm; confirmed in research/quinn/cr_scratch/step2_system_concept.md decision 7 |
| `collet.min_slit_clamped` | ASSUMED | Echo registry seed |
| `collet.min_wall` | ASSUMED | design rule: minimum collet wall at the cone top, checked by C6 and C9 (formerly print.min_wall); not a printer value |
| `collet.web_strain_allow` | ASSUMED | Register row (design assumption, not a material property) |
| `collet.core_seat_height` | ASSUMED | Topologist W-2: relief hole bottom z 3.0 clears the ledge top by 0.5 (no OCC tangency); ledge shear 0.30 MPa at 204 N (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `collet.core_seat_width` | ASSUMED | core weight seat width, leaves the bore open (Designer name core_stop_width, renamed) |
| `collet.notch_azimuth_offsets_deg` | ASSUMED | rim notch azimuths relative to receiver.key_offset_deg; the first rim_notch_count entries are cut; each lies 15 deg from the nearest slit and relief hole (research/quinn/cr_scratch/step5_loftsman_collet_definition.md) |
| `collet.label_azimuth_offset_deg` | ASSUMED | label window centre relative to receiver.key_offset_deg; off the probe azimuths 67, 187, 307 and clear of every slit (research/quinn/cr_scratch/step5_loftsman_collet_definition.md) |
| `collet.label_window_width` | ASSUMED | label window chord, tangential; 3 mm margin to the nearest slit edge (research/quinn/cr_scratch/step5_loftsman_collet_definition.md) |
| `collet.tool_overshoot` | ASSUMED | boolean tool extent beyond a part face so no tool face is coincident with a part face; not a part dimension (research/quinn/cr_scratch/step5_loftsman_collet_definition.md) |
| `collet.rim_notch_width` | ASSUMED | rim notch (research/quinn/cr_scratch/step3_designer_params.md) |
| `collet.rim_notch_depth` | ASSUMED | rim notch (research/quinn/cr_scratch/step3_designer_params.md) |
| `collet.label_text_format` | ASSUMED | grip-window label, lo and hi from collet.grip_window_lo/hi |
| `collet.label_height` | ASSUMED | at least 6 per S2-4 |
| `collet.label_depth` | ASSUMED | label relief depth |
| `collet.file_name_pattern` | ASSUMED | file name, e.g. collet_092p5 for 92.5 mm |
| `collet.chamfer_angle_deg` | ASSUMED | bore lead-in chamfer angle from the axis; the lip fillet turns through the same angle (research/quinn/cr_scratch/step5_loftsman_collet_definition.md) |
| `collet.chamfer_floor` | ASSUMED | chamfer floor at 45 deg (research/quinn/cr_scratch/step3_designer_params.md R3) |
| `collet.bore_lip_radius` | ASSUMED | bore lip radius (research/quinn/cr_scratch/step3_designer_params.md) |
| `collet.colour` | ASSUMED | colour per size, smallest to largest; a finish, not a printer input; redundant with notch count |
| `collet.slit_ligament` | ASSUMED | axial, relief hole edge to far end face; hole bottom z 3.0 clears ring top z 2.0 (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `thread.pitch` | ASSUMED | Design Notes 3 seed, carried by research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md (hand, pitch 8) |
| `thread.flank_deg` | ASSUMED | Design Notes 3 symmetric 45/45 seed, carried by research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md |
| `thread.starts` | ASSUMED | Design Notes 3 single start, carried by research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md |
| `thread.min_engage_pitches` | ASSUMED | Echo registry seed |
| `thread.hand` | ASSUMED | research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md section 6 (hand, pitch 8, 45/45, single start) |
| `thread.runout_land` | ASSUMED | receiver runout land below the thread run, root radius, z 36.5 to 40.5 (Loftsman step3 section 1) (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `thread.tool_groove_fraction` | ASSUMED | helical sweep tool groove height must stay below 0.9 x pitch (freecad_api_reference helix rule); sets tool overshoot, not a part dimension (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `cone.alpha` | ASSUMED | taper half-angle; self-lock tan 10 = 0.176 < mu_k,min 0.25 (research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md section 6; research/quinn/cr_scratch/step2_system_concept.md decision 2) |
| `cone.alpha_release` | ASSUMED | RETIRED releasing-cone fallback, reference only: misses 10 N m at d = 90 within 12 N m and costs +11.26 mm of thread major (research/quinn/cr_scratch/step2_system_concept.md decision 2) |
| `chain.t_c` | ASSUMED | Design Notes 3 seed |
| `chain.H` | ASSUMED | Design Notes 3 seed |
| `chain.t_h` | ASSUMED | Design Notes 3 seed |
| `chain.t_b` | ASSUMED | Design Notes 3 seed |
| `chain.h` | ASSUMED | Design Notes 3 seed |
| `fit.c_r` | ASSUMED | generic seed; E2 deflection c_r/10 = 0.035 mm; coupon at Step 8 settles |
| `fit.g_a` | ASSUMED | generic seed; coupon at Step 8 settles |
| `fit.seat_clearance` | ASSUMED | gameplan test F1 seed (formerly print.seat_clearance) |
| `fit.model_contact_gap` | ASSUMED | normal gap modelled on every class C pair, lower part face moved -n (research/quinn/cr_scratch/step3_topologist_crossreview.md section 2) |
| `fit.min_contact_patch` | ASSUMED | A1a floor on the class C patch area per pair (a zero-area line contact fails); positive floor chosen as 1 mm2, below every modelled face contact; seat.min_contact_area governs the holder/collet pair |
| `fit.c_r_min` | ASSUMED | T3 floor on measured radial crest clearance: 0.10 = 2 x the E2 tessellation deflection c_r / 10 (0.035) rounded up; built c_r 0.35 passes |
| `fit.g_a_min` | ASSUMED | T3 floor on the total axial flank gap at the pitch line: 0.10 = 1/3 of fit.g_a 0.30; built g_a 0.30 passes |
| `seat.min_contact_area` | ASSUMED | gameplan test F1 seed |
| `wingnut.span` | ASSUMED | design value: hand-torque arm from the Loftsman model (T7), not a printer limit; Step 3 confirms |
| `wingnut.wing_count` | ASSUMED | wing planform (research/quinn/cr_scratch/step3_designer_params.md) |
| `wingnut.wing_height` | ASSUMED | wing seed; at least 30 (S2-5); NOT the 40 mm floor offset used in stop.collar_top_z |
| `wingnut.wing_root_width` | ASSUMED | wing planform (research/quinn/cr_scratch/step3_designer_params.md) |
| `wingnut.wing_tip_width` | ASSUMED | wing planform (research/quinn/cr_scratch/step3_designer_params.md) |
| `wingnut.wing_thickness` | ASSUMED | wing planform (research/quinn/cr_scratch/step3_designer_params.md) |
| `wingnut.edge_radius` | ASSUMED | wing edge radius (research/quinn/cr_scratch/step3_designer_params.md) |
| `wingnut.hand_clearance` | ASSUMED | hand access below the wings for turning them (research/quinn/cr_scratch/step3_designer_params.md S2-5) |
| `stop.owner` | DECLARED | gate B5: metal hard stop belongs to the upper assembly; wing nut only tightens the collet |
| `stop.g_stop` | DECLARED | plain mechanical clearance between the cutter lowest point at the hard stop and the collar top (wings included), at the highest clamped nut position (research/quinn/cr_scratch/step2_system_concept.md ICD row Stop gap); design choice, no standard cited |
| `stop.height_range` | ASSUMED | [0.5 m case, 0.75 m case]: first = stop.height_z 184.84 (collar top 159.84 + 25); second = the old 300 seed + 15 (g_stop 25 - 10), not re-derived, A2b recomputes at Step 5 (research/quinn/cr_scratch/step2_system_concept.md) |
| `stop.margin` | ASSUMED | F4 margin seed |
| `stop.rated_load` | ASSUMED | equals loads.axial_design |
| `stop.pad_width` | ASSUMED | hard-stop face pad on the column face (research/quinn/cr_scratch/step3_designer_params.md) |
| `stop.pad_length` | ASSUMED | 60 x 60 = 3600 mm2 against 1000 N (research/quinn/cr_scratch/step3_designer_params.md) |
| `holder.flange_thickness` | ASSUMED | t_f 8 in the Loftsman stack: plate top minus flange underside = 16 = flange 8 + nut plate 8 (research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md section 4) |
| `holder.key_length` | ASSUMED | axial, from holder bottom (research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md section 3) |
| `holder.insert_count` | ASSUMED | M6 inserts for the collar screws (Loftsman step3 section 9) (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `holder.insert_circle_radius` | ASSUMED | M6 insert circle radius (Loftsman step3 sections 7 and 9) (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `holder.insert_dia` | ASSUMED | M6 tap drill diameter for the insert bore (ISO 261 coarse thread, 5.0) (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `holder.insert_depth` | ASSUMED | insert bore depth into the holder top, 2 x M6 diameter (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `holder.index_notch_width` | ASSUMED | Rule P index notch on the flange rim, tangential (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `holder.index_notch_depth` | ASSUMED | Rule P index notch, radial from the flange rim; angle is -receiver.key_offset_deg (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `receiver.key_slot_width` | ASSUMED | asymmetric key slot in the register wall (research/quinn/cr_scratch/step3_designer_params.md) |
| `receiver.key_offset_deg` | ASSUMED | slot off-diametral so only one holder orientation fits (research/quinn/cr_scratch/step3_designer_params.md) |
| `receiver.spigot_od` | ASSUMED | Engineer seed: receiver locating spigot into the base plate hole, wall at least 5 outside thread.major 149.58 (needed by base.spigot_hole_dia; the Designer named it without a value) |
| `receiver.register_chamfer` | ASSUMED | rim inner chamfer at 45 deg, pilot lead; counted in the T9 insertion 47.75 (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `receiver.floor_hole_dia` | ASSUMED | debris hole below the smallest core ledge ID 81.0 at d 85, 0.5 radial margin (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `nut.lift_play` | ASSUMED | p, plate top to collar underside; replaces 1.5 (research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md D-3) |
| `nut.washer_pocket_depth` | ASSUMED | washer.thickness 1.3 stands 0.5 proud, so pocket 1.3 - 0.5 = 0.8 |
| `nut.arrow_depth` | ASSUMED | arrow relief depth (research/quinn/cr_scratch/step3_designer_params.md) |
| `nut.tommy_hole_dia` | ASSUMED | tommy-bar socket holes (research/quinn/cr_scratch/step3_designer_params.md) |
| `nut.tommy_hole_count` | ASSUMED | tommy-bar socket holes (research/quinn/cr_scratch/step3_designer_params.md) |
| `nut.tommy_hole_depth` | ASSUMED | tommy-bar socket holes (research/quinn/cr_scratch/step3_designer_params.md) |
| `nut.release_marker` | ASSUMED | release marker (research/quinn/cr_scratch/step3_designer_params.md S2-7b) |
| `nut.washer_window_count` | ASSUMED | three radial notches show the washer colour; absence shows a bare flange (research/quinn/cr_scratch/step3_designer_params.md S2-7d) |
| `nut.washer_window_width` | ASSUMED | radial notch width (research/quinn/cr_scratch/step3_designer_params.md S2-7d) |
| `nut.tommy_boss_od` | ASSUMED | four bosses at 45 + 90k deg; hole bottom r 78.14, 3.0 over the thread root (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `nut.tommy_grip_radius` | ASSUMED | hand grip centroid radius on the bar: loads.hand_force_bar 100 N x 0.150 m = 15 N m (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `nut.pad_count` | ASSUMED | press pads at 0/120/240 deg (research/quinn/cr_scratch/step3_topologist_crossreview.md W-5) |
| `nut.pad_arc` | ASSUMED | pad arc length at r 71.5 (research/quinn/cr_scratch/step3_topologist_crossreview.md W-5) |
| `nut.pad_height` | ASSUMED | equals nut.washer_pocket_depth (research/quinn/cr_scratch/step3_topologist_crossreview.md W-5) |
| `nut.pad_id` | ASSUMED | 0.10 radial interference on washer.od 143.2; common volume 2.40 mm3 in 3 pieces (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `nut.tab_width` | ASSUMED | anti-rotation tab, inner r 70.6; gaps 0.5 tangential per side, 1.0 radial (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `nut.tommy_hole_bottom_r` | ASSUMED | tommy hole bottom radius, 3.0 over the thread root r 75.14 (Loftsman step3 section 6); boss end radius = this + nut.tommy_hole_depth (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `nut.tab_inner_radius` | ASSUMED | anti-rotation tab inner radius: washer notch floor r 69.6 + 1.0 radial gap (Loftsman step3 section 6) (research/quinn/cr_scratch/step3_engineer_first_solids.md) |
| `register.g_reg` | ASSUMED | radial register fit, holder in receiver bore; the Step 8 coupon settles it (research/quinn/cr_scratch/step2_system_concept.md tolerance budget) |
| `collar.od` | ASSUMED | research/quinn/cr_scratch/step2_loftsman_crossreview_reply.md section 4 |
| `washer.type` | ASSUMED | key renamed from washer.material (gate B2 printer-key filter bans the name material); always fitted, adopted design response (research/quinn/cr_scratch/step2_system_concept.md decision 4) |
| `washer.id` | ASSUMED | research/quinn/cr_scratch/step2_system_concept.md decision 4 |
| `washer.od` | ASSUMED | research/quinn/cr_scratch/step2_system_concept.md decision 4 |
| `washer.thickness` | ASSUMED | research/quinn/cr_scratch/step2_system_concept.md decision 4 |
| `washer.retention` | ASSUMED | a lip on a washer standing 0.5 proud overlaps it when seated; pads nut.pad_* (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `washer.notch_width` | ASSUMED | radial tab notch, Rule P feature (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `washer.notch_depth` | ASSUMED | radial, notch floor r 69.6, 1.2 of ring left (research/quinn/cr_scratch/step3_geometry_crossreview.md) |
| `column.spacing` | ASSUMED | column centres on the rail centrelines (rails at y = +-274); 488 mm clear for the drill body (research/quinn/cr_scratch/step2_system_concept.md decision 9) |
| `hoist.anchor_member` | ASSUMED | U15 (research/quinn/cr_scratch/step2_system_concept.md); two 728 mm lengths are on hand |
| `strap.rating` | ASSUMED | 4 x the 20.8 kg core; proven by H10 (research/quinn/cr_scratch/step2_system_concept.md U14) |
| `strap.handle_radial` | ASSUMED | rigid side handle at 0.55 L; no overhead anchor (research/quinn/cr_scratch/step2_system_concept.md U14) |
| `rest.height_positions` | ASSUMED | detents above the seat for the 0.5 m and 0.75 m cores (research/quinn/cr_scratch/step2_system_concept.md U16) |
| `rest.roller_count` | ASSUMED | three linked rollers (research/quinn/cr_scratch/step2_system_concept.md U16) |
| `rest.centre_repeatability` | ASSUMED | to datum B (research/quinn/cr_scratch/step2_system_concept.md U16) |
| `rest.release_tower` | ASSUMED | trip tower on the arm, cam released by the upper assembly lug (research/quinn/cr_scratch/step2_system_concept.md U16) |
| `rest.cam_lug_radius` | ASSUMED | flush with the cutter lowest point (research/quinn/cr_scratch/step2_system_concept.md U16) |
| `rest.roller_dia` | ASSUMED | steady rest roller (research/quinn/cr_scratch/step3_designer_params.md) |
| `rest.arm_length` | ASSUMED | steady rest arm (research/quinn/cr_scratch/step3_designer_params.md) |
| `rest.swing_clear_radius` | ASSUMED | arm swing clear radius (concept U16) |
| `rest.close_handle_length` | ASSUMED | close handle (research/quinn/cr_scratch/step3_designer_params.md) |
| `rest.hold_open_detent` | ASSUMED | rest holds open on a detent (research/quinn/cr_scratch/step3_designer_params.md) |
| `friction.mu_k` | ASSUMED | Register row (design assumption, not a material property) |
| `friction.mu_c` | ASSUMED | Register row |
| `friction.mu_t` | ASSUMED | Register row |
| `friction.bearing` | ASSUMED | Register row |
| `profile.series` | DECLARED | research/quinn/cr_scratch/step0_human_stock_80-20.md |
| `stock.on_hand` | DECLARED | step0_human_stock_80-20.md (human states exactly this; shared with other projects) |
| `stock.cut_cost` | DECLARED | QMRD3 order document via step0_human_stock_80-20.md |
| `frame.members` | ASSUMED | Design Notes 7 starting allocation (644 x 2, 468 x 2, 488 x 2); roles are the Engineer's assumption, Step 12 finalises |
| `frame.joints` | ASSUMED | 4 outer corners + 4 plate-support ends |
| `hardware.tnut_thread` | DECLARED | step0_human_stock_80-20.md |
| `hardware.tnut_type` | DECLARED | human use on 30-series stock (research/quinn/cr_scratch/step3_human_gate_decisions.md) |
| `hardware.tnut_sku` | DECLARED | human use on 30-series stock (research/quinn/cr_scratch/step3_human_gate_decisions.md) |
| `hardware.bracket_class` | DECLARED | step0_human_stock_80-20.md; Design Notes 7 |
| `hardware.bracket_leg_min` | DECLARED | full-size rule, gate: minimum leg 57 mm and width 57 mm (research/quinn/cr_scratch/step2_system_concept.md bracket choice rule); no bracket below it |
| `hardware.purchased_bracket_joints` | ASSUMED | four outer corners take the purchased 57 mm class, two per joint (research/quinn/cr_scratch/step2_system_concept.md) |
| `hardware.printed_bracket_joints` | ASSUMED | four plate-support ends take the printed 68 mm bracket, two per joint (research/quinn/cr_scratch/step2_system_concept.md) |
| `hardware.bracket_sku` | ASSUMED | geometry matches the human's STEP (57.35 x 57.35 x 57.0 mm, plate 6.0 mm, VERIFIED); the part number is unconfirmed: 8020.net returned 403, Zoro lists '8 hole 57mm 14089' (research/quinn/cr_scratch/step3_engineer_hardware_confirm.md section 2); verify SKU and leg length at purchase |
| `hardware.brackets_per_joint` | ASSUMED | Engineer assumption |
| `hardware.tnuts_per_bracket` | ASSUMED | the 14089 listing is 8 holes (4 per leg, Zoro); the 2 holes assumed before conflicted with it. Assumption: every hole takes a T-nut, so 8 per bracket, applied to purchased and printed brackets alike (the printed bracket slots are assumed to form the same 2 x 2 pattern per leg, 7.0 mm wide). Set to 2 only if the human wants one T-nut per leg |
| `hardware.baseplate_fasteners` | ASSUMED | Engineer assumption: slotted base-plate holes to frame |
| `hardware.spare_fraction` | ASSUMED | Engineer assumption |
| `hardware.screw_length_bracket` | ASSUMED | QMRD3 inventory lengths 10/16/20/25/30 (stock file); on-hand treated as nil, Design Notes 12 |
| `hardware.screw_length_baseplate` | ASSUMED | same |
| `hardware.adjust_interface` | ASSUMED | adjust interface (research/quinn/cr_scratch/step3_designer_params.md S2-6) |
| `hardware.tnut_fit_30series` | DECLARED | fit in the 30-6060 slot is declared by human use on 30-series stock (research/quinn/cr_scratch/step3_human_gate_decisions.md) |
| `icd.datum_a` | ASSUMED | research/quinn/cr_scratch/step2_system_concept.md ICD Datum A |
| `icd.datum_b` | ASSUMED | research/quinn/cr_scratch/step2_system_concept.md ICD Datum B, decision 5 |
| `icd.datum_c` | ASSUMED | research/quinn/cr_scratch/step2_system_concept.md ICD Datum C, decision 5 |
| `icd.mounting_pattern` | ASSUMED | research/quinn/cr_scratch/step2_system_concept.md ICD Mounting; profile measured in step2_engineer_profile_measure.md |
| `icd.coaxiality_budget` | ASSUMED | budget; chain 0.953, margin 0.047 (research/quinn/cr_scratch/step2_system_concept.md decision 5) |
| `icd.coaxiality_chain` | ASSUMED | entries in order: 0.32 plate key and stop pin (radial), 0.20 receiver spigot in plate hole, 0.283 column foot (radial), 0.15 carriage guide; linear sum 0.953 (research/quinn/cr_scratch/step2_system_concept.md tolerance budget; A3b measures built fits) |
| `icd.floor_above_datum_a` | ASSUMED | one parameter: Detail 2 floor plane and ICD datum A are offset by it (research/quinn/cr_scratch/step2_system_concept.md decision 5) |
| `icd.stop_rating` | ASSUMED | equals stop.rated_load |
| `icd.tipover_statement` | ASSUMED | research/quinn/cr_scratch/step2_system_concept.md decision 9; Step 12 replaces |
| `icd.cable_exit` | ASSUMED | Design Notes 5, 12 |
| `icd.core_lead_in_capture` | ASSUMED | U12 funnel capture radius, upper assembly only (research/quinn/cr_scratch/step2_system_concept.md) |
| `icd.core_lead_in_centring` | ASSUMED | U12 centring to the drill axis (research/quinn/cr_scratch/step2_system_concept.md) |
| `icd.core_lead_in_bore` | ASSUMED | U12 working bore radius, at least 55.06 for all seven d (research/quinn/cr_scratch/step2_system_concept.md) |
| `icd.column_foot_moment` | ASSUMED | column foot on the frame slot lines (research/quinn/cr_scratch/step2_system_concept.md); Step 12 checks |
| `icd.torque_reaction` | ASSUMED | research/quinn/cr_scratch/step2_system_concept.md ICD Torque reaction (A2c) |
| `icd.mass_target` | ASSUMED | with upper assembly; 25 kg structure (research/quinn/cr_scratch/step2_system_concept.md decision 9) |
| `witness.scale_pitch` | ASSUMED | graduation pitch on the witness scale |
| `witness.wrong_collet_band_low` | ASSUMED | gap band below the zone (flange on the rim): wrong collet |
| `witness.wrong_collet_band_high` | ASSUMED | gap band above the zone up to the release gap holder.stroke_gap_R: wrong collet |
| `access.key_sector_deg` | ASSUMED | hand access sector (research/quinn/cr_scratch/step3_designer_params.md S2-6) |
| `access.key_arm_length` | ASSUMED | arm reach (research/quinn/cr_scratch/step3_designer_params.md S2-6) |
| `access.head_clear_radius` | ASSUMED | bolt head clearance radius (research/quinn/cr_scratch/step3_designer_params.md S2-6) |
| `bracket.face` | ASSUMED | bracket face orientation (research/quinn/cr_scratch/step3_designer_params.md S2-6) |
| `bolt_down.method` | ASSUMED | bolt-down method (research/quinn/cr_scratch/step3_designer_params.md S2-6); relies on a T-nut that fits the 30 slot: fit declared by use (hardware.tnut_fit_30series, DECLARED) |
| `bolt_down.count` | ASSUMED | bolt-down feet (research/quinn/cr_scratch/step3_designer_params.md S2-6) |
| `bolt_down.floor_fastener` | ASSUMED | floor fastener (research/quinn/cr_scratch/step3_designer_params.md S2-6) |
| `bolt_down.head_access` | ASSUMED | head access (research/quinn/cr_scratch/step3_designer_params.md S2-6) |
| `base.plate_thickness` | ASSUMED | base plate thickness; length and width are icd.footprint_x and icd.footprint_y (Designer base.plate_length/width merged) |
| `base.slot_width` | ASSUMED | M6 clearance slot, 7 mm as the measured printed bracket |
| `base.slot_length` | ASSUMED | slotted hole length |
| `tray.length` | ASSUMED | debris tray (research/quinn/cr_scratch/step3_designer_params.md) |
| `tray.width` | ASSUMED | debris tray (research/quinn/cr_scratch/step3_designer_params.md) |
| `tray.depth` | ASSUMED | debris tray (research/quinn/cr_scratch/step3_designer_params.md) |
| `tray.lip_z` | ASSUMED | tray lip below the wings (research/quinn/cr_scratch/step3_designer_params.md); wing underside z fixed at Step 5 |
| `tray.drain_dia` | ASSUMED | drain (research/quinn/cr_scratch/step3_designer_params.md) |
| `tray.floor_slope_deg` | ASSUMED | floor slope to the drain |
| `tray.drain_plug` | ASSUMED | drain plug |
| `caddy.socket_clear` | ASSUMED | per side on collet OD; socket count is collets.count (Designer caddy.socket_count merged) |
| `caddy.socket_depth` | ASSUMED | collet caddy socket depth |
| `gauge.length` | ASSUMED | alignment gauge length |
| `strength.tensile_design` | ASSUMED | design assumption, not a material property (Step 2 key renamed per research/quinn/cr_scratch/step3_designer_params.md section 4) |
| `witness.azimuth_deg` | ASSUMED | receiver.key_offset_deg 37 + 90: reader faces the ruler 90 deg from the key slot (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.channel_width` | ASSUMED | ruler channel width, tangential (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.channel_floor_depth` | ASSUMED | channel floor plane lies thread.minor/2 - 0.30 = 71.99 from the axis: 0.05 to 0.30 under the root cylinder across the width, no tangency (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.line_height` | ASSUMED | graduation line height, axial (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.line_depth` | ASSUMED | graduation line depth below the channel floor (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.band_depth` | ASSUMED | wrong-collet band depth below the channel floor (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.tick_width` | ASSUMED | holder flange tick groove width, tangential (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.tick_depth` | ASSUMED | holder flange tick groove depth, radial from the flange OD (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.tick_height` | ASSUMED | holder flange tick groove height above the flange underside (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.channel_z` | ASSUMED | ruler channel z range in the receiver frame: graduation 0 at 48.5 minus 1.5, top 1.374 above the wrong-collet band top 61.626 (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.line_length` | ASSUMED | graduation line length, tangential, centred on witness.azimuth_deg (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.line_length_major` | ASSUMED | graduation line length at every witness.major_every (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.major_every` | ASSUMED | major graduation and digit every 5th line (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.band_t` | ASSUMED | wrong-collet band strips, tangential range left of the line (t = z x r) (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.digit_t` | ASSUMED | digit pockets, tangential range right of the line (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.digit_height` | ASSUMED | digit pocket height, axial (research/quinn/cr_scratch/step6_loftsman_definition.md section 1) |
| `witness.digit_z_shift` | ASSUMED | digit pocket centre above its line z so no pocket face meets the channel floor edge z 47.0 (research/quinn/cr_scratch/step6_topologist_crossreview.md section 5) |
| `nut.glyph_length` | ASSUMED | tighten and loosen glyph length along its direction: shaft 2.5 + head 3.5 (research/quinn/cr_scratch/step6_loftsman_definition.md section 2) |
| `nut.shaft_width` | ASSUMED | glyph shaft width (research/quinn/cr_scratch/step6_loftsman_definition.md section 2) |
| `nut.head_width` | ASSUMED | glyph arrowhead width (research/quinn/cr_scratch/step6_loftsman_definition.md section 2) |
| `nut.head_length` | ASSUMED | glyph arrowhead length (research/quinn/cr_scratch/step6_loftsman_definition.md section 2) |
| `nut.skirt_z_lo` | ASSUMED | dust skirt bottom, nut frame (research/quinn/cr_scratch/step6_loftsman_definition.md section 2) |
| `nut.skirt_z_hi` | ASSUMED | dust skirt top, 2 below the wing underside z 16 (research/quinn/cr_scratch/step6_loftsman_definition.md section 2) |
| `nut.skirt_rim` | ASSUMED | dust skirt vertical rim height at the outer radius (research/quinn/cr_scratch/step6_loftsman_definition.md section 2) |
| `nut.skirt_embed` | ASSUMED | dust skirt embed into the nut body so the fuse shares volume (research/quinn/cr_scratch/step6_loftsman_definition.md section 2) |
| `base.slot_centres` | ASSUMED | slot centres (x, y), long axis X; pattern is not symmetric under a flip about X or Y (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `base.key_pocket_xy` | ASSUMED | plate key pockets at (+-x, y), underside; y is the datum C slot line (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `base.pin_pocket_xy` | ASSUMED | stop pin pocket centre; wall x 244.0 touches the pin (contact intended) (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `base.drain_xy` | ASSUMED | drain hole and tray drain centre (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `base.column_notch` | ASSUMED | plate edge notch at each column: width, depth from the long edge (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `base.column_notch_x` | ASSUMED | column notch half-width in x: the notch spans x -35 to +35 about the column at x 0 (research/quinn/cr_scratch/step6_loftsman_definition.md section 3; the 70 x 65 notch is one per long edge) |
| `base.key_pocket_size` | ASSUMED | key pocket square, key 11.5 with 0.25 per side (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `base.pocket_depth` | ASSUMED | underside pocket depth (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `base.pin_pocket_size` | ASSUMED | stop pin pocket x, y (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `base.drain_hole_dia` | ASSUMED | plate drain hole, 0.5 radial over tray.drain_dia 25 (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `tray.wall` | ASSUMED | tray wall (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `tray.floor_min` | ASSUMED | tray floor thickness at the drain end (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `tray.ramp_x` | ASSUMED | floor ramp x range: 253 x tan(tray.floor_slope_deg) = 13.26 rise; 3 deg over the full 560 would rise 29.3, over the 25 depth (research/quinn/cr_scratch/step6_loftsman_definition.md section Corrections C3) |
| `tray.hole_r` | ASSUMED | tray hole for the receiver spigot, 1.0 over receiver.spigot_od/2 (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `tray.relief` | ASSUMED | column relief at each long edge: width, depth inward from the edge, y 241 to 260 (research/quinn/cr_scratch/step6_loftsman_definition.md section 3; research/quinn/cr_scratch/step6_topologist_crossreview.md section 5) |
| `frame.end_x` | ASSUMED | end member centre x (+-) (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `frame.support_x` | ASSUMED | plate support centre x (+-) (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `frame.notch` | ASSUMED | datum C slot-line notch on one rail: across, along, depth (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.holes_purchased` | ASSUMED | purchased bracket hole positions along the leg (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.slots_printed` | ASSUMED | printed bracket slot centres along the leg (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.slot_lengths_printed` | ASSUMED | printed bracket slot overall lengths at slots_printed; hardware.printed_bracket_slot_width is the width (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.purchased_leg` | ASSUMED | purchased bracket leg (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.purchased_plate` | ASSUMED | purchased bracket plate (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.printed_leg` | ASSUMED | printed bracket leg (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.printed_plate` | ASSUMED | printed bracket plate (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.width` | ASSUMED | bracket width across the profile face (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.hole_dia` | ASSUMED | purchased bracket clearance hole for M6 (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `bracket.across` | ASSUMED | hole and slot offset across the leg from the bracket centre line (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `caddy.web` | ASSUMED | wall between sockets (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `caddy.border` | ASSUMED | border outside the outer sockets (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `caddy.floor` | ASSUMED | floor under the sockets (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `caddy.row_spacing` | ASSUMED | row spacing, staggered rows of 4 and 3 at pitch 154.08 (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `caddy.rows` | ASSUMED | sockets per row; sum equals collets.count (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `caddy.label_width` | ASSUMED | size label recess width; height collet.label_height, depth collet.label_depth (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `caddy.label_gap` | ASSUMED | size label recess edge off the socket wall (research/quinn/cr_scratch/step6_topologist_crossreview.md section 5) |
| `gauge.cavity` | ASSUMED | cavity diameter and depth from below (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `gauge.handle` | ASSUMED | handle bar on top: length, width, height (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.ring` | ASSUMED | C-ring inner radius, outer radius, thickness (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.roller_r` | ASSUMED | roller centre radius from the core axis (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.pin` | ASSUMED | roller pin diameter; the pin bridges the 0.5 gap to the ring (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.mouth_deg` | ASSUMED | C-ring mouth, centred on -X (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.block` | ASSUMED | column block x, y, z; interface plane at the column face (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.hinge_boss_dia` | ASSUMED | hinge boss at y = rest.arm_length (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.arm` | ASSUMED | arm width and height to the ring (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.roller_height` | ASSUMED | roller height, centred on the roller plane z = 0 (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.ring_z_lo` | ASSUMED | C-ring bottom: roller top 15 + rest.roller_pin_gap 0.5 (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.roller_pin_gap` | ASSUMED | axial gap between roller top and ring (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.handle_dia` | ASSUMED | close handle diameter; length rest.close_handle_length (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.detent_depth` | ASSUMED | detent notch depth in the boss at 90 deg swing (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.detent_width` | ASSUMED | detent notch width, tangential on the boss (Step 6 Pass 1 assumption, Step 9 refines) |
| `rest.tower` | ASSUMED | release tower tangential width and radial depth (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `rest.tower_inboard_r` | ASSUMED | release tower inboard face radius (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `stop.pad_thickness` | ASSUMED | stop pad thickness below stop.height_z (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `stop.pad_xy` | ASSUMED | stop pad centre; y = column face 244 - stop.pad_length/2 (research/quinn/cr_scratch/step6_loftsman_definition.md section 5) |
| `stop.pad_hole_dia` | ASSUMED | stop pad M6 clearance holes, two at x = +-stop.pad_hole_x, so the pad carries a boolean record (data71) (Step 6 Pass 1 assumption) |
| `stop.pad_hole_x` | ASSUMED | stop pad hole offset from the pad centre, equal to profile.slot_offset (Step 6 Pass 1 assumption) |
| `plug.head_dia` | ASSUMED | drain plug head (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `plug.head_h` | ASSUMED | drain plug head height (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `plug.flange_dia` | ASSUMED | drain plug flange (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `plug.flange_t` | ASSUMED | drain plug flange thickness (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `plug.shank_dia` | ASSUMED | drain plug shank, 0.5 radial clearance in tray.drain_dia 25 (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `plug.shank_h` | ASSUMED | drain plug shank length = tray.floor_min (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `foot.size` | ASSUMED | bolt-down foot plate x, y, z (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `foot.m6_xy` | ASSUMED | M6 holes at (x, +-y), slot pitch 30 (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `foot.m6_hole` | ASSUMED | M6 clearance hole (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `foot.m8_x` | ASSUMED | M8 floor fastener hole x, 28 from the rail end (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `foot.m8_hole` | ASSUMED | M8 clearance hole (research/quinn/cr_scratch/step6_loftsman_definition.md section 3) |
| `tnut.body` | ASSUMED | T-nut proxy body: across, along, height; PZRT 3030 has no CAD on disk (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `tnut.neck` | ASSUMED | T-nut proxy neck: across, along, height = profile.slot_neck_depth (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `tnut.hole` | ASSUMED | T-nut proxy tapped hole, M6 tap drill region (research/quinn/cr_scratch/step6_loftsman_definition.md section 4) |
| `tnut.chamfer` | ASSUMED | T-nut proxy long bottom edges chamfered 3.5 x 45 deg (research/quinn/cr_scratch/step6_topologist_crossreview.md section 5) |

Soft target: `jig.height_target` 2000 mm (DECLARED, gate B6), recorded and reported, not tested; frame 60 + columns 1540 = 1600 mm before overhang (Step 2).
