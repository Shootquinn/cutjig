"""Brackets (FR2): bracket_purchased (14089 class, legs bracket.purchased_leg, plate bracket.purchased_plate, Ø bracket.hole_dia holes) and
bracket_printed (68 mm class, slots hardware.printed_bracket_slot_width wide, bracket.slot_lengths_printed long). Local frame: inside corner
at the origin, legs along +x and +y, z 0 to bracket.width. Placement of the 12 in the frame is frame.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402
import hardware_geom as HG  # noqa: E402


def one(kind, p):
    g = lambda k: C.G(p, k)
    rec = S.Rec("bracket_" + kind)
    W, acr = g("bracket.width"), g("bracket.across")
    sh, info = HG.bracket_shape(p, kind, 0.0, 0.0, 1.0, 1.0, W / 2, rec)
    L, t = info["L"], info["t"]
    tool = info["tool"]
    pos = g("bracket.holes_purchased") if kind == "purchased" else g("bracket.slots_printed")
    lens = [g("bracket.hole_dia")] * 2 if kind == "purchased" else g("bracket.slot_lengths_printed")
    zc = W / 2
    vol_legs, vol_tool = info["legs"].Volume, S.removed(tool, info["legs"])
    # leg B: plate along y at mid x; holes read along x at y = t/2, z = zc +- across
    lx = lambda z: C.line_ivals(sh, C.V(0.0, t / 2, z), C.V(L, t / 2, z))
    iv = lx(zc + acr)
    gaps = [(a[1], b[0]) for a, b in zip(iv, iv[1:])]
    centres = [(a + b) / 2 for a, b in gaps]
    lens_m = [b - a for a, b in gaps]
    iv_dn = lx(zc - acr)
    xm = (pos[0] + pos[1]) / 2
    thick = C.line_ivals(sh, C.V(xm, 0.0, zc), C.V(xm, 2 * t, zc))
    wid = C.line_ivals(sh, C.V(xm, t / 2, -1.0), C.V(xm, t / 2, W + 1.0))
    leg_a = C.line_ivals(sh, C.V(t / 2, 0.0, zc), C.V(t / 2, L + 1.0, zc))
    hole_cnt = sum(1 for a in pos for dz in (-acr, acr) for pt in (C.V(a, t / 2, zc + dz), C.V(t / 2, a, zc + dz)) if not sh.isInside(pt, 1e-6, True))
    rows = [
        S.row("FR2", f"{kind} bracket leg B length (L)", vol_legs, sh.BoundBox.XLength, L, S.TOL),
        S.row("FR2", f"{kind} bracket leg A length (L)", vol_legs, leg_a[-1][1] - leg_a[0][0], L, S.TOL),
        S.row("FR2", f"{kind} bracket plate thickness (T)", vol_legs, thick[0][1] - thick[0][0] if thick else None, t, S.TOL),
        S.row("FR2", f"{kind} bracket width (Z)", vol_legs, wid[0][1] - wid[0][0], g("bracket.width"), S.TOL),
        S.row("FR2", f"{kind} bracket holes or slots per bracket (8: two per row, two rows, two legs)", vol_tool, hole_cnt, g("hardware.tnuts_per_bracket"), S.TOL),
        S.row("FR2", f"{kind} first hole or slot position along the leg (A)", vol_tool, centres[0] if centres else None, pos[0], 0.02),
        S.row("FR2", f"{kind} second hole or slot position along the leg (A)", vol_tool, centres[1] if len(centres) > 1 else None, pos[1], 0.02),
        S.row("FR2", f"{kind} first hole or slot length along the leg (A)", vol_tool, lens_m[0] if lens_m else None, lens[0], 0.02),
        S.row("FR2", f"{kind} second hole or slot length along the leg (A)", vol_tool, lens_m[1] if len(lens_m) > 1 else None, lens[1], 0.02),
        S.row("FR2", f"{kind} hole rows across the leg: lower row positions equal upper (A)", vol_tool,
              (iv_dn[0][1] if iv_dn else None), iv[0][1] if iv else None, 0.02),
    ]
    res = S.result("bracket_" + kind, sh, rows, rec, extra={"kind": kind})
    S.save_single("bracket_" + kind, sh, res)
    return res


def build():
    p = C.params()
    r1 = one("purchased", p)
    r2 = one("printed", p)
    return r2 if r1["all_features_pass"] else r1


if __name__ in ("__main__", "bracket"):
    C.run_main("bracket", build)
