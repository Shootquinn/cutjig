"""Positive control for the common-volume guard (Topologist addendum): a shifted partner with a known overlap volume must read that volume through
probe_poses.checked_common, and an invalid common result must raise InvalidCommon instead of reading 0.0.
Writes results/probes/common_guard.json {boxes{expected, measured}, tubes{expected, measured}, invalid_raises}.
Run: freecadcmd tests/probes/probe_common_guard.py   (seconds)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["CJ_PROBE_IMPORT"] = "1"
import probe_poses as PP  # noqa: E402
import probe_lib as L  # noqa: E402

SIDE, SHIFT = 10.0, 4.0                 # boxes: overlap (SIDE - SHIFT) x SIDE x SIDE
R_IN, R_OUT, H, DZ = 10.0, 20.0, 30.0, 10.0   # tubes: overlap pi (R_OUT^2 - R_IN^2) (H - DZ)


class _Bad:
    def isValid(self):
        return False

    def common(self, other):
        return self


def main():
    import Part
    box_a = Part.makeBox(SIDE, SIDE, SIDE)
    box_b = Part.makeBox(SIDE, SIDE, SIDE, L.C.V(SHIFT, 0, 0))
    tube = lambda z: Part.makeCylinder(R_OUT, H, L.C.V(0, 0, z)).cut(Part.makeCylinder(R_IN, H, L.C.V(0, 0, z)))
    raised = False
    try:
        PP.checked_common(_Bad(), _Bad(), "stub")
    except PP.InvalidCommon:
        raised = True
    L.finish("common_guard", {"boxes": {"expected": (SIDE - SHIFT) * SIDE * SIDE, "measured": PP.checked_common(box_a, box_b, "boxes").Volume},
                              "tubes": {"expected": math.pi * (R_OUT ** 2 - R_IN ** 2) * (H - DZ), "measured": PP.checked_common(tube(0), tube(DZ), "tubes").Volume},
                              "invalid_raises": raised})


if __name__ in ("__main__", "probe_common_guard"):
    L.guarded(main, "common_guard")
