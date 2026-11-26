"""S1 reported values not produced by check_stack.reported (gameplan detail 1.1 Reported; no threshold, never asserted).

Appends a section to wip/s1_summary_r<rev>.md (writes wip/s1_mass_report_r<rev>.json; output rule in sketch_loader): drawn highest point per pose, ring position (N1) with anchor and guide
heights, park rule for Step 4, centre-of-mass height per pose and unbolted tip force at the frame top.
Masses: overlay leaves (ASSUMED); fixed structure from geometry with the WORKING densities below (ASSUMED, this file
only, not design values). Run after check_sketch.py s1 --rev k. checks_s1.reported (RPT items com_height, tip_force)
reads pose_data, so the record and this report carry the same numbers (1.3 P6).
r8 (1.3 P6, Designer 1.3 (b) sign-off section 8): the moving items are the s3_spec.yaml load_cases.W_kg items (ring,
drill, gear, three NEMA 23, nuts, drill-to-ring bearing, three pinions, gear hub, two guide bushings with housings;
W 24.25 kg at the overlay values); the top-end block and the capture core are listed apart from W; Tr12x3 screws at
jackscrew.nominal; NEMA 17 from liftmotor.mass.
"""
import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import Params, find_output, load_spec, output_path  # noqa: E402

G = 9.81
WORKING = {  # ASSUMED working values for the mass report only
    "rho_al_kg_m3": 2700, "rho_steel_kg_m3": 7850,
}
W_TAG = "W"   # status prefix of the items summed into W (s3_spec.yaml load_cases.W_kg)


def mid(f):
    return (f["z_min"] + f["z_max"]) / 2


def masses(P, feats):
    """(name, kg, z_S, status) per item. Moving masses from the overlay (status starts with W for the W_kg items), fixed
    structure from geometry."""
    g = P.get
    out = []
    n_scr, n_pin = g("jackscrew.count"), g("pinion.count")
    # moving: the W_kg items (s3_spec.yaml load_cases)
    dz = (feats["drill_head"]["z_min"] + feats["drill_tube"]["z_max"]) / 2
    out.append(("drill (head + tube)", g("drill.mass"), dz, "W, overlay ASSUMED"))
    out.append(("ring", g("ring.mass"), mid(feats["ring"]), "W, overlay ASSUMED"))
    out.append(("ring gear", g("gear.mass"), mid(feats["gear"]), "W, overlay ASSUMED"))
    out.append(("gear hub", g("gear.hub_mass"), mid(feats["gear_hub"]), "W, overlay ASSUMED"))
    out.append((f"NEMA 23 x{n_pin}", n_pin * g("pinion.motor_mass"), mid(feats["motor23_a"]), "W, overlay ASSUMED"))
    out.append((f"pinions x{n_pin}", n_pin * g("pinion.mass"), mid(feats["pinion_a"]), "W, overlay ASSUMED"))
    out.append((f"nuts x{n_scr}", n_scr * g("jackscrew.nut_mass"), mid(feats["nut_a"]), "W, overlay ASSUMED"))
    out.append(("drill-to-ring bearing", g("bearing.mass"), mid(feats["bearing"]), "W, overlay ASSUMED"))
    out.append((f"guide bushings with housings x{g('guide.count')}", g("guide.count") * g("guide.bushing_mass"), mid(feats["guide_bushing_a"]), "W, overlay ASSUMED"))
    # 1.3 (h) r3 (Designer r2 pick 7, Loftsman LF1.3-2): the top-end block rides on the drill and is in W_kg
    out.append(("top-end block", g("drill.top_block_mass"), mid(feats["drill_top_block"]), "W, overlay ASSUMED"))
    if "core_750" in feats and "z_min" in feats["core_750"]:
        out.append(("0.75 m core", g("core.mass_kg_d105")[1], mid(feats["core_750"]), "params DERIVED (d 105)"))
    # fixed
    frame_len = sum(m["cut_mm"] * m["qty"] for m in g("frame.members")) / 1000
    out.append(("base frame 30-6060", frame_len * g("profile.mass_per_m_catalog"), mid(feats["base_frame"]), "DERIVED (frame.members, catalog kg/m)"))
    plate = g("icd.footprint_x") * g("icd.footprint_y") * g("base.plate_thickness") * 1e-9 * WORKING["rho_al_kg_m3"]
    out.append(("base plate", plate, mid(feats["base_plate"]), "DERIVED, aluminium ASSUMED"))
    out.append((f"screw frame members x{n_scr}", n_scr * g("frame_upper.member_length") / 1000 * g("profile.mass_per_m_catalog"),
                mid(feats["frame_upper_a"]), "DERIVED (catalog kg/m)"))
    rod = math.pi * (g("guide.rod_od") / 2000) ** 2 * g("guide.length") / 1000 * WORKING["rho_steel_kg_m3"]
    out.append((f"guide rods x{g('guide.count')}", g("guide.count") * rod, mid(feats["guide_member"]), "DERIVED, steel ASSUMED"))
    scr = math.pi * (g("jackscrew.nominal") / 2000) ** 2 * g("jackscrew.length") / 1000 * WORKING["rho_steel_kg_m3"]
    out.append((f"Tr12x3 screws x{n_scr}", n_scr * scr, mid(feats["screw_a"]), "DERIVED (d jackscrew.nominal), steel ASSUMED"))
    out.append((f"NEMA 17 x{g('liftmotor.count')}", g("liftmotor.count") * g("liftmotor.mass"), mid(feats["liftmotor_a"]), "overlay ASSUMED"))
    return out


def drawn_highest(fig, spec):
    ref = {r["id"] for r in spec["features"] if r.get("reference")}
    best = None
    for gid, arts in sc.tagged(fig.axes[0]).items():
        if gid in ref:
            continue
        for a in arts:
            for poly in sc.artist_polys(a):
                for _, zz in poly:
                    if best is None or zz > best[0]:
                        best = (zz, gid)
    return best


def pose_data(P, spec, stack, figs):
    """{pose: values} for the report and for checks_s1.reported (RPT items highest_point, com_height, tip_force)."""
    g = P.get
    target = g("jig.height_target")
    half_a = min(g("icd.footprint_x"), g("icd.footprint_y")) / 2
    data = {}
    for pid, pr in stack["poses"].items():
        feats = pr["features"]
        hz, hid = drawn_highest(figs[pid], spec)
        ms = masses(P, feats)
        M = sum(m for _, m, _, _ in ms)
        W = sum(m for _, m, _, s in ms if s.startswith(W_TAG + ","))
        zc = sum(m * z for _, m, z, _ in ms) / M
        h_top = feats["frame_upper_a"]["z_max"]
        data[pid] = {"highest_drawn_z_S": hz, "highest_part": hid, "margin": target - hz, "mass_kg": M, "W_kg": W, "com_z_S": zc,
                     "frame_top_z_S": h_top, "tip_force_frame_top_N": M * G * half_a / h_top, "tip_force_at_com_N": M * G * half_a / zc,
                     "ring_bottom_z_S": feats["ring"]["z_min"], "ring_top_z_S": feats["ring"]["z_max"],
                     "items": [(n, round(m, 3), round(z, 2), s) for n, m, z, s in ms]}
    return data, half_a


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", type=int, default=1)
    a = ap.parse_args(argv)
    P = Params()
    spec = load_spec(HERE / "s1_spec.yaml")
    stack = check_stack.evaluate_spec(P, spec)
    import importlib.util
    mspec = importlib.util.spec_from_file_location("s1_script", HERE / spec["script"])
    mod = importlib.util.module_from_spec(mspec)
    mspec.loader.exec_module(mod)
    figs = mod.build(P, spec, stack)
    g = P.get
    target = g("jig.height_target")
    data, half_a = pose_data(P, spec, stack, figs)
    rows = []
    for pid, d in data.items():
        rows.append(f"| {pid} | {d['highest_drawn_z_S']:.2f} ({d['highest_part']}) | {target - d['highest_drawn_z_S']:.2f} | "
                    f"{d['ring_bottom_z_S']:.2f} to {d['ring_top_z_S']:.2f} | {d['mass_kg']:.2f} | {d['W_kg']:.2f} | {d['com_z_S']:.1f} | "
                    f"{d['tip_force_at_com_N']:.0f} | {d['tip_force_frame_top_N']:.0f} |")
    f0 = stack["poses"]["load"]["features"]
    lines = ["", "## Reported values, drawn (s1_mass_report.py; no threshold, never asserted)", "",
             "| Pose | Highest drawn point z_S (part) | Margin to 2000 soft target | Ring z_S | Mass kg | W kg (moving, W_kg items) | COM z_S | Tip force at COM N | Tip force at frame top N |",
             "|---|---|---|---|---|---|---|---|---|"] + rows + [
             "",
             f"- Ring (N1): ring.position_above_tip {g('ring.position_above_tip')} mm, bottom of ring plate above the tip; ring thickness {g('ring.thickness')}.",
             f"- Anchors: jackscrew.anchor_z {g('jackscrew.anchor_z')} z_A, drawn {f0['anchor_a']['z_min']:.2f} to {f0['anchor_a']['z_max']:.2f} z_S; "
             f"top guides: jackscrew.top_guide_z {g('jackscrew.top_guide_z')} z_A, drawn {f0['guide_a']['z_min']:.2f} to {f0['guide_a']['z_max']:.2f} z_S; "
             f"screw length jackscrew.length {g('jackscrew.length')}.",
             f"- Park rule for Step 4: {spec['park_rule']['for_step4']}",
             f"- Moving mass W (s3_spec.yaml load_cases.W_kg items): {data['load']['W_kg']:.2f} kg, the top-end block {g('drill.top_block_mass')} kg included (1.3 (h) r3, LF1.3-2).",
             f"- Tip force: horizontal force that tips the unbolted jig about the nearest base edge, lever {half_a:.0f} mm "
             f"(min footprint / 2, COM on the drill axis by three-fold symmetry), g {G}. Masses: overlay ASSUMED; structure DERIVED; "
             f"working densities {WORKING} ASSUMED. Receiver, collet, holder, wing nut, anchor and guide blocks omitted.",
             f"- Old reference icd.tipover_statement: {g('icd.tipover_statement')}"]
    out = output_path(f"s1_summary_r{a.rev}.md")   # wip/ (sketch_loader output rule); check_sketch.py s1 writes it first
    src = find_output(f"s1_summary_r{a.rev}.md")
    txt = src.read_text(encoding="utf-8")
    marker = "\n## Reported values, drawn"
    if marker in txt:
        txt = txt[:txt.index(marker)]
    out.write_text(txt.rstrip("\n") + "\n" + "\n".join(lines) + "\n", encoding="utf-8")
    output_path(f"s1_mass_report_r{a.rev}.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
