"""S1 stub for the red-first run (gameplan detail 1.0 line 125): loads params, calls setup_figure, draws the floor line only."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sketch_common as sc  # noqa: E402


def build(P, spec, stack):
    figs = {}
    half = P.get("icd.footprint_x")
    for pose in spec["poses"]:
        pid = pose["id"]
        fig, ax = sc.setup_figure(spec["view"], title=f"S1 stub, pose {pid}")
        z = stack["poses"][pid]["features"]["floor"]["z_min"]
        sc.draw_hline(ax, "floor", -half, half, z)
        sc.finish_axes(ax)
        figs[pid] = fig
    return figs
