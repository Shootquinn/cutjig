import io
p = "params.yaml"
t = open(p, newline="").read()
S7 = "research/quinn/cr_scratch/step7_loftsman_definition.md"
def after(anchor_prefix, lines):
    global t
    out, done = [], False
    for ln in t.split("\r\n"):
        out.append(ln)
        if not done and ln.startswith(anchor_prefix):
            out += lines
            done = True
    assert done, anchor_prefix
    t = "\r\n".join(out)
after("  top_above_plate:", [
 '  thickness: {value: 6.0, unit: "mm", source: "collar ring height on the holder = collar.top_above_plate 6.75 - nut.lift_play 0.75; ring z from holder tube top (%s Revision 1)", status: DERIVED}' % S7,
 '  hole_dia: {value: 6.6, unit: "mm", source: "clearance hole through the collar ring over each holder insert bore (M6 clearance, equal to bracket.hole_dia); opens the Dia 5 insert bores so the ring forms no void shell (%s Revision 1; step7_topologist_crossreview.md E1)", status: DECLARED}' % S7,
])
after("  length_optional:", [
 '  top_chamfer: {value: 3.0, unit: "mm", source: "core stand-in chamfer, 3.0 x 45 deg on the top end only; bottom end square; Rule P mark of the stand-in (%s L2)", status: DECLARED}' % S7,
])
after("  pad_id:", [
 '  pad_overlap_min: {value: 2.0, unit: "mm3", source: "class P floor on nut|washer common volume: designed 2.40 (nut.pad_id note), built 2.387; below 2.0 a pad is missing (%s Revision 1; orchestrator ruling replaces the Topologist 2.30)", status: ASSUMED}' % S7,
 '  pad_overlap_max: {value: 2.45, unit: "mm3", source: "class P ceiling on nut|washer common volume: 2.40 designed + 0.05 (%s L5 table)", status: ASSUMED}' % S7,
 '  relief_z: {value: 42.0, unit: "mm", source: "nut thread relief floor, nut frame: full-groove top 42.5 - 0.5; relief runs to the plate underside nut.length + washer proud (%s Revision 1)", status: DERIVED}' % S7,
 '  relief_r: {value: 75.34, unit: "mm", source: "nut thread relief radius = thread.major / 2 + fit.c_r + 0.2 = 74.79 + 0.35 + 0.2 (0.2 over the groove root r 75.14 avoids a sliver) (%s Revision 1)", status: DERIVED}' % S7,
])
after("  printed_bracket_slot_pitch:", [
 '  printed_brackets_per_joint: {value: 1, unit: "", source: "C6 option (a): one printed bracket per plate-support-end joint, inboard; the four outer printed brackets are deleted (rail inner face need 740 mm against 644 mm). Joint capacity with one bracket is DECLARED for Step 12 (%s L5; step7_systems_engineer_contract_check.md item 7)", status: ASSUMED}' % S7,
])
after("  pin_pocket_size:", [
 '  key_width: {value: 11.5, unit: "mm", source: "plate key width, key pocket base.key_pocket_size 12 less 0.25 per side (Step 6 BS4); A3b fit_plate_key_stop_pin = (pocket - key_width) / 2 = 0.25 (%s L6)", status: DECLARED}' % S7,
 '  pin_dia: {value: 6.0, unit: "mm", source: "end-member stop pin diameter in the stop pin pocket (Step 6 BS4) (%s L6)", status: DECLARED}' % S7,
 '  pin_x: {value: 247, unit: "mm", source: "stop pin centre x: pocket wall x 244.0 touches the pin edge, 247 - pin_dia / 2 (Step 6 BS4) (%s L6)", status: DECLARED}' % S7,
])
t = t.rstrip("\r\n") + "\r\n" + "\r\n".join([
 "",
 "pose:",
 '  core_lift_R: {value: 1.0, unit: "mm", source: "core stand-in bottom above the collet core ledge in pose R: collet|core R gap 1.0 against the 0.5 floor (%s L2)", status: DECLARED}' % S7,
 '  nut_over_holder_K: {value: 48.010, unit: "mm", source: "nut z0 above holder bottom in pose K: 96 - 48 + 2 x fit.model_contact_gap (%s L1)", status: DERIVED}' % S7,
 '  nut_over_holder_R: {value: 48.745, unit: "mm", source: "nut z0 above holder bottom in pose R: holder collar underside 104.75 - nut.overall_height 56 - fit.model_contact_gap 0.005 (plate top meets collar underside, class C) (%s L1)", status: DERIVED}' % S7,
 '  nut_phi_R_deg: {value: 77.670, unit: "deg", source: "nut azimuth in pose R, the base pose: ridge phase 0.645 mod 8 at azimuth 0 so the clamp flank sits 0.005 axial from the receiver flank (%s L1)", status: DERIVED}' % S7,
 '  washer_z_in_nut: {value: 47.995, unit: "mm", source: "washer bottom above nut z0 = nut.length 48 - fit.model_contact_gap 0.005 (%s L1)", status: DERIVED}' % S7,
 '  frame_dz: {value: -0.005, unit: "mm", source: "frame, bracket and T-nut z shift in every pose = -fit.model_contact_gap, so base|frame is class C at gap 0.005 (%s L4)", status: DERIVED}' % S7,
 "",
 "cutter:",
 '  face_thickness: {value: 3.175, unit: "mm", source: "cutting-face annulus thickness = drill.tube_wall 3.175 (%s L3)", status: DERIVED}' % S7,
 '  lead_in_height: {value: 20.0, unit: "mm", source: "lead-in ring height above the funnel throat, working bore icd.core_lead_in_bore (%s L3)", status: DECLARED}' % S7,
 "",
])
open(p, "w", newline="").write(t)
