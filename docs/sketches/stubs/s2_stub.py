"""S2 stub for the red-first run (gameplan detail 1 common (c), detail 1.2): loads params, calls setup_figure plan_xy, draws
the base footprint outline only (row base_plate, its plan_poly pieces from check_stack). One figure at the spec
plan_figure pose (S2 draws one plan figure; z bands per pose come from the stack)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sketch_common as sc  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402


def build(P, spec, stack):
    pid = (spec.get("plan_figure") or {}).get("pose") or spec["poses"][0]["id"]
    fig, ax = sc.setup_figure(spec["view"], title=f"S2 stub, plan at pose {pid}")
    for piece in stack["poses"][pid]["features"]["base_plate"]["plan_pieces"]:
        sc.draw("base_plate", Polygon(piece, closed=True, fill=False), ax)
    sc.finish_axes(ax)
    return {pid: fig}
