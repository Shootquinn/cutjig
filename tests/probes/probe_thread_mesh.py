"""T1b screw-motion mesh and T1c direction. The nut starts in the meshed pose (groove centres on receiver tooth centres,
the pose verify_step3 measured at zero overlap) and moves by Rz(phi) T(0, 0, L phi / 360). Common volume with the receiver is the measurement.
Heavy: about nine thread-on-thread booleans. Launch detached with a PID and a log: freecadcmd tests/probes/probe_thread_mesh.py
Output results/probes/thread_mesh.json: screw_common{phi: mm3}, opposite_hand_90, pure_rotation_90, cw_down_common."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib as L  # noqa: E402
C = L.C


def main():
    p = L.params()
    P = L.G(p, "thread.pitch")
    z_run = L.G(p, "receiver.rim_above_floor") - L.G(p, "thread.run_turns") * P
    z0 = z_run + P / 2.0 + 2 * P
    rec, nut = L.part("receiver"), L.part("nut")

    def pose(phi, dz):
        s = nut.copy()
        s.rotate(C.V(0, 0, 0), C.V(0, 0, 1), phi)
        s.translate(C.V(0, 0, z0 + dz))
        return s

    def common(phi, dz):
        t = time.time()
        v = rec.common(pose(phi, dz)).Volume
        print("COMMON phi=%g dz=%g -> %.4f mm3 (%.1fs)" % (phi, dz, v, time.time() - t), flush=True)
        return v

    lead = lambda phi: P * phi / 360.0
    out = {"baseline_common": common(0.0, 0.0),
           "screw_common": {str(int(f)): common(f, lead(f)) for f in (15, 90, 180, 360)},
           "opposite_hand_90": common(90.0, -lead(90.0)),
           "pure_rotation_90": common(90.0, 0.0),
           "cw_down_common": common(-90.0, lead(-90.0)), "cw_down_dz": lead(-90.0)}
    L.finish("thread_mesh", out, [os.path.join(L.CACHE, "receiver.FCStd"), os.path.join(L.CACHE, "nut.FCStd")])


if __name__ in ("__main__", "probe_thread_mesh"):
    L.guarded(main, "thread_mesh")
