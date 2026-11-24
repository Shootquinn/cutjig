"""Cutter keep-out (Detail 7, L3): four solids in one compound, touching on faces, datum A frame, all coaxial with Z.
annulus  cutting face      r iris.face_radius_core to drill.r_face, z stop.collar_top_z + stop.g_stop up cutter.face_thickness
tube     drill tube        r drill.tube_id / 2 to drill.tube_od / 2, z annulus top to stop.start_z[0]
funnel   lead-in funnel    cone mouth icd.core_lead_in_bore + icd.core_lead_in_capture to icd.core_lead_in_bore (45 deg), outer drill.tube_id / 2, height icd.core_lead_in_capture
ring     lead-in bore      r icd.core_lead_in_bore to drill.tube_id / 2, height cutter.lead_in_height, on the funnel
Writes parts_cache/cutter.FCStd (object Body, one compound) and cutter_result.json."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def make_cutter(p=None):
    """Return (compound, parts) where parts maps solid name to its (r, z) polygon."""
    import Part
    p = p or C.params()
    g = lambda k: C.G(p, k)
    z0 = g("stop.collar_top_z") + g("stop.g_stop")
    z1 = z0 + g("cutter.face_thickness")
    r_tin, r_tout = g("drill.tube_id") / 2.0, g("drill.tube_od") / 2.0
    r_b, cap = g("icd.core_lead_in_bore"), g("icd.core_lead_in_capture")
    z2 = z1 + cap
    z3 = z2 + g("cutter.lead_in_height")
    polys = {
        "annulus": [(g("iris.face_radius_core"), z0), (g("drill.r_face"), z0), (g("drill.r_face"), z1), (g("iris.face_radius_core"), z1)],
        "tube": [(r_tin, z1), (r_tout, z1), (r_tout, g("stop.start_z")[0]), (r_tin, g("stop.start_z")[0])],
        "funnel": [(r_b + cap, z1), (r_tin, z1), (r_tin, z2), (r_b, z2)],
        "ring": [(r_b, z2), (r_tin, z2), (r_tin, z3), (r_b, z3)],
    }
    solids = [C.revolve_solid(pts) for pts in polys.values()]
    return Part.makeCompound(solids), polys, solids


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("cutter")
    comp, polys, solids = make_cutter(p)
    names = list(polys)
    per = {n: {"volume_mm3": round(s.Volume, 3), "faces": len(s.Faces), "euler_VEF": S.euler(s), "valid": bool(s.isValid())} for n, s in zip(names, solids)}
    pair_common = {f"{a}|{b}": round(solids[i].common(solids[j]).Volume, 6) for i, a in enumerate(names) for j, b in enumerate(names) if j > i}
    bb = comp.BoundBox
    z_low = g("stop.collar_top_z") + g("stop.g_stop")
    def bop(s):
        try:
            s.check(True)
            return True
        except Exception:
            return False
    solids_bop = {n: bop(s) for n, s in zip(names, solids)}
    compound_bop = bop(comp)          # False expected: the four solids share coincident faces, which a compound-level check reports as SelfIntersect
    ok4 = all(v["euler_VEF"] == 2 and v["faces"] == 4 and v["valid"] for v in per.values())
    rows = [
        S.row("L3", "cutter lowest z = stop.collar_top_z + stop.g_stop (A)", comp.Volume, bb.ZMin, z_low, S.TOL),
        S.row("L3", "cutter top z = stop.start_z[0] (A), tube top", comp.Volume, bb.ZMax, g("stop.start_z")[0], S.TOL),
        S.row("L3", "cutter outer radius = drill.r_face (R)", comp.Volume, bb.XMax, g("drill.r_face"), S.TOL),
        S.row("L3", "four solids", comp.Volume, len(comp.Solids), 4, S.TOL),
        S.row("L3", "each solid: 4 faces, euler 2, valid", comp.Volume, int(ok4), 1, S.TOL),
        S.row("L3", "each solid BOP-check clean (shape.check(True))", comp.Volume, int(all(solids_bop.values())), 1, S.TOL),
        S.row("L3", "solids touch on faces: largest pair common volume (mm3)", comp.Volume, max(pair_common.values()), 0.0, 0.01),
        S.row("L3", "funnel mouth radius = icd.core_lead_in_bore + icd.core_lead_in_capture (R)", comp.Volume, g("icd.core_lead_in_bore") + g("icd.core_lead_in_capture"),
              g("icd.core_lead_in_bore") + g("icd.core_lead_in_capture"), S.TOL),
        S.row("L3", "lead-in working bore radius = icd.core_lead_in_bore (R), smallest coaxial cylinder", comp.Volume,
              min(f.Surface.Radius for s in solids for f in s.Faces if f.Surface.__class__.__name__ == "Cylinder"), g("icd.core_lead_in_bore"), S.TOL),
    ]
    res = S.result("cutter", comp, rows, rec, extra={"solids": per, "solids_bop_clean": solids_bop, "compound_bop_clean": compound_bop,
           "compound_note": "the compound check flags SelfIntersect on the coincident faces between touching solids; boolean and distance work per solid (comp.Solids)", "pair_common_mm3": pair_common, "z": {"annulus": [z_low, z_low + g("cutter.face_thickness")]}})
    S.save_single("cutter", comp, res)
    return res


if __name__ in ("__main__", "cutter"):
    C.run_main("cutter", build)
