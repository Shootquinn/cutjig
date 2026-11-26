"""S3 stub for the red-first run (gameplan detail 1 common (c), detail 1.3): loads params, calls setup_figure with the
spec view (section_yz) and its declared insets (TP-7: the plan inset is its own Axes), draws the shop floor line only
(row floor, across its depth band at z_S 0). One figure at the section_figure pose (capture_end)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sketch_common as sc  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402


def build(P, spec, stack):
    pid = (spec.get("section_figure") or {}).get("pose") or spec["poses"][0]["id"]
    fig, ax = sc.setup_figure(spec["view"], title=f"S3 stub, section A-A at pose {pid}", insets=spec.get("insets"))
    f = stack["poses"][pid]["features"]["floor"]
    u0, u1 = f["depth"]
    sc.draw("floor", Line2D([u0, u1], [f["z_min"], f["z_max"]]), ax)
    sc.finish_axes(ax)
    return {pid: fig}
