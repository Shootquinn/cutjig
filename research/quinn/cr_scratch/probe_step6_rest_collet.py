import os, sys
sys.path.insert(0, 'C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/tests/probes')
sys.path.insert(0, 'C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/build_parts')
import probe_lib as L
import rest as RS
C = L.C
TAGS = ["090p0", "092p5", "093p7", "095p0", "097p0", "097p5", "100p0", "102p5", "105p0"]


def main():
    p = L.params()
    g = lambda k: L.G(p, k)
    h = g("rest.height_positions")
    out = []
    rest_cache = {}
    for tag in TAGS:
        d = float(tag.replace("p", "."))
        for pose, suffix, cd in (("R", "", d), ("K_d+1", "_clamped_Kd1", d + 1.0), ("K_max", "_clamped_Kmax", d - 1.5)):
            col = L.part("collet_" + tag + suffix)
            key = round(cd, 4)
            if key not in rest_cache:
                rest_cache[key] = RS.shape_at(p, cd)
            for z_rest in h:
                rs = L.moved(rest_cache[key], z=z_rest)
                core = C.S.cyl_z(0.0, 0.0, cd / 2.0, 0.0, z_rest + 190.0) if hasattr(C, "S") else None
                if core is None:
                    import Part
                    core = Part.makeCylinder(cd / 2.0, z_rest + 190.0, C.V(0, 0, 0))
                rec = {"tag": tag, "pose": pose, "core_d": cd, "rest_z": z_rest, "rest_valid": bool(rs.isValid()), "collet_valid": bool(col.isValid()),
                       "common_rest_collet_mm3": round(rs.common(col).Volume, 6),
                       "min_dist_rest_collet_mm": round(rs.distToShape(col)[0], 4),
                       "common_rest_core_mm3": round(rs.common(core).Volume, 6),
                       "min_dist_rest_core_mm": round(rs.distToShape(core)[0], 4)}
                out.append(rec)
                print(rec, flush=True)
    nz = [r for r in out if r["common_rest_collet_mm3"] > 1e-6 or r["common_rest_core_mm3"] > 1e-6]
    L.finish("step6_rest_collet", {"frame": "floor frame, collet z 0..32 on receiver floor seat; rest local z0 = roller plane at rest.height_positions above the seat; core cylinder z 0 to rest_z+190",
                                   "n": len(out), "nonzero_common": nz, "rows": out}, inputs=["parts_cache/rest.py shape_at", "parts_cache/collet_*"])


L.guarded(main, "step6_rest_collet") if hasattr(L, "guarded") else main()
