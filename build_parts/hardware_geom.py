"""Geometry shared by tnut.py, bracket.py and frame.py (no build entry point, so importing it runs nothing).
T-nut proxy (PZRT 3030 has no CAD on disk; envelope from profile.* and tnut.*) and the two bracket classes."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def tnut_shape(p, rec=None):
    """T-nut proxy, local frame: face plane z = 0 (top flush with the slot face), +z out of the face, slot axis along x, across along y.
    Neck in the slot opening, body in the cavity, long bottom edges (along x) chamfered tnut.chamfer x 45 deg, tapped-hole region Ø tnut.hole through."""
    g = lambda k: C.G(p, k)
    rec = rec or S.Rec("tnut")
    bw, bl, bh = g("tnut.body")
    nw, nl, nh = g("tnut.neck")
    ch, ov = g("tnut.chamfer"), g("collet.tool_overshoot")
    z_top_b, z_bot_b = -nh, -(nh + bh)
    body = S.extrude_poly([(-bw / 2, z_top_b), (bw / 2, z_top_b), (bw / 2, z_bot_b + ch), (bw / 2 - ch, z_bot_b), (-bw / 2 + ch, z_bot_b), (-bw / 2, z_bot_b + ch)],
                          "yz", -bl / 2, bl / 2)
    neck = S.box(-nl / 2, nl / 2, -nw / 2, nw / 2, -nh, 0.0)
    nut = rec.fuse("body_neck_fuse", [body, neck])
    hole = S.cyl_z(0.0, 0.0, g("tnut.hole") / 2, z_bot_b - ov, ov)
    return S.solid_of(rec.cut("hole_cut", nut, hole)), {"body": body, "neck": neck, "hole": hole, "z_bot": z_bot_b}


def bracket_shape(p, kind, cx, cy, sx, sy, zc, rec):
    """L bracket with corner (cx, cy); leg B along (sx, 0) with its plate on y in [cy, cy + sy t]; leg A along (0, sy) with its plate on x in
    [cx, cx + sx t]. Width hardware-wide `bracket.width` centred on z = zc. purchased: round holes at bracket.holes_purchased; printed: slots at
    bracket.slots_printed (lengths bracket.slot_lengths_printed). Two holes or slots across at +-bracket.across of zc on each leg."""
    g = lambda k: C.G(p, k)
    L = g("bracket.purchased_leg") if kind == "purchased" else g("bracket.printed_leg")
    t = g("bracket.purchased_plate") if kind == "purchased" else g("bracket.printed_plate")
    W, acr, ov = g("bracket.width"), g("bracket.across"), g("collet.tool_overshoot")
    z0, z1 = zc - W / 2, zc + W / 2
    xs = lambda a, b: (min(a, b), max(a, b))
    bx0, bx1 = xs(cx, cx + sx * L)
    by0, by1 = xs(cy, cy + sy * t)
    ax0, ax1 = xs(cx, cx + sx * t)
    ay0, ay1 = xs(cy, cy + sy * L)
    legs = rec.fuse(f"{kind}_legs_fuse", [S.box(bx0, bx1, by0, by1, z0, z1), S.box(ax0, ax1, ay0, ay1, z0, z1)])
    tools = []
    pos = g("bracket.holes_purchased") if kind == "purchased" else g("bracket.slots_printed")
    lens = [None, None] if kind == "purchased" else g("bracket.slot_lengths_printed")
    r = g("bracket.hole_dia") / 2
    for a, ln in zip(pos, lens):
        for dz in (-acr, acr):
            # leg B: axis along y at x = cx + sx a; leg A: axis along x at y = cy + sy a
            ob = C.V(cx + sx * a, cy - sy * ov, zc + dz)
            oa = C.V(cx - sx * ov, cy + sy * a, zc + dz)
            if kind == "purchased":
                tools.append(S.cyl_dir(ob, C.V(0, sy, 0), r, t + 2 * ov))
                tools.append(S.cyl_dir(oa, C.V(sx, 0, 0), r, t + 2 * ov))
            else:
                w = g("hardware.printed_bracket_slot_width")
                tools.append(S.stadium(ob, C.V(sx, 0, 0), C.V(0, sy, 0), ln, w, t + 2 * ov))
                tools.append(S.stadium(oa, C.V(0, sy, 0), C.V(sx, 0, 0), ln, w, t + 2 * ov))
    tool = rec.fuse(f"{kind}_hole_tools_fuse", tools)
    sh = S.solid_of(rec.cut(f"{kind}_holes_cut", legs, tool))
    return sh, {"L": L, "t": t, "legs": legs, "tool": tool, "n_tools": len(tools)}
