"""Witness ray-cast (Loftsman fix pass D1): horizontal rays at witness.azimuth_deg from r 200 toward the axis, z 44 to 64 step 0.05, nut placed at
z = rim_top_z - nut.skirt_below_flange + gap (nut z 0 is the reading face). Edge = lowest ray z whose first hit is the nut. A graduation line is visible
when the first hit is the receiver deeper than the channel floor (a run of hits at r < channel floor - 0.8 x witness.line_depth below the edge).
Poses: K-max (gap holder.stroke_gap_min_K), K d+1 (witness.zone_high); control: nut placed 5 mm below the K-max edge (must misread the edge).
Writes results/probes/witness_sight.json {az, rim_top_z, poses: {name: {gap, nut_z, edge, expected_edge, lines_visible, line_z[]}}, control: {...}}
Run: freecadcmd tests/probes/probe_witness_sight.py"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib as L  # noqa: E402
C = L.C
DZ = 0.05
Z0, Z1, R0 = 44.0, 64.0, 200.0


def cast(rec_slab, nut_slab, az, nut_dz, floor_r, line_depth):
    u = C.V(math.cos(math.radians(az)), math.sin(math.radians(az)), 0.0)
    nut = nut_slab.copy()
    nut.translate(C.V(0, 0, nut_dz))
    n = int(round((Z1 - Z0) / DZ))
    first_nut, hit_r = [], []
    for i in range(n + 1):
        z = Z0 + i * DZ
        p0, p1 = C.V(u.x * R0, u.y * R0, z), C.V(0.0, 0.0, z)
        a = C.line_ivals(nut, p0, p1)
        b = C.line_ivals(rec_slab, p0, p1)
        t_n = a[0][0] if a else None
        t_r = b[0][0] if b else None
        first_nut.append(t_n is not None and (t_r is None or t_n <= t_r))
        hit_r.append(None if t_r is None else R0 - t_r)
    edge = next((Z0 + i * DZ for i, f in enumerate(first_nut) if f), None)
    thr = floor_r - 0.8 * line_depth
    runs, cur = [], []
    for i, (f, r) in enumerate(zip(first_nut, hit_r)):
        if (not f) and r is not None and r < thr:
            cur.append(Z0 + i * DZ)
        elif cur:
            runs.append(sum(cur) / len(cur))
            cur = []
    if cur:
        runs.append(sum(cur) / len(cur))
    return edge, runs


def main():
    p = L.params()
    az = L.G(p, "witness.azimuth_deg")
    rsh, _ = L.open_shape(os.path.join(L.CACHE, "receiver.FCStd"))
    nsh, _ = L.open_shape(os.path.join(L.CACHE, "nut.FCStd"))
    rim_top = C.axial_ivals(rsh, (az + 120.0) % 360.0, L.G(p, "thread.minor") / 2 - 1.0, 0.0, 200.0)[-1][1]
    edge0 = rim_top - L.G(p, "nut.skirt_below_flange")
    floor_r = L.G(p, "thread.minor") / 2 - L.G(p, "witness.channel_floor_depth")
    depth = L.G(p, "witness.line_depth")
    rec_slab, nut_slab = rsh, nsh      # full shapes: a boolean slab of the threaded receiver returns empty
    out = {"az": az, "rim_top_z": rim_top, "edge_zero": edge0, "poses": {}}
    for name, key in (("K-max", "holder.stroke_gap_min_K"), ("K d+1", "witness.zone_high")):
        gap = L.G(p, key)
        e, runs = cast(rec_slab, nut_slab, az, edge0 + gap, floor_r, depth)
        out["poses"][name] = {"gap": gap, "nut_z": edge0 + gap, "edge": e, "expected_edge": edge0 + gap, "lines_visible": len(runs), "line_z": runs}
        print("POSE", name, e, len(runs), flush=True)
    gap = L.G(p, "holder.stroke_gap_min_K")
    e, runs = cast(rec_slab, nut_slab, az, edge0 + gap - 5.0, floor_r, depth)
    out["control"] = {"gap": gap, "nut_z": edge0 + gap - 5.0, "edge": e, "expected_edge": edge0 + gap, "lines_visible": len(runs)}
    L.finish("witness_sight", out, [os.path.join(L.CACHE, "receiver.FCStd"), os.path.join(L.CACHE, "nut.FCStd")])


if __name__ in ("__main__", "probe_witness_sight"):
    L.guarded(main, "witness_sight")
