import os, sys
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts")
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\tests\probes")
import FreeCAD as App
import cadlib as C
import step6lib as S
import glyph_math
p = C.params()
g = lambda k: C.G(p, k)
d = App.openDocument(r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\nut.FCStd")
sh = C.final_shape(d.getObject("Body"))
thick = g("wingnut.wing_thickness")
rb = g("wingnut.body_od") / 2
rt = g("wingnut.span") / 2
H = g("nut.overall_height")
box = S.box(rb + 3.0, rt - 3.0, -(thick / 2 + 0.5), thick / 2 + 0.5, 0.0, H)
piece = sh.common(box)
print("PIECE", piece.Volume, len(piece.Faces), flush=True)
xc = (rb + rt) / 2
depth = g("nut.arrow_depth")
r_in = g("wingnut.body_od") / 2 + 3
for face in ("+z", "-z"):
    sign = 1.0 if face == "+z" else -1.0
    void, allv = [], []
    i = 0
    while True:
        x = r_in + i * 0.5
        i += 1
        if x < xc - 5:
            continue
        if x > xc + 5:
            break
        col = []
        for j in range(31):
            y = -7.5 + j * 0.5
            iv = C.line_ivals(piece, C.V(x, y, -10.0), C.V(x, y, 90.0))
            if iv:
                col.append((y, -10.0 + (iv[-1][1] if sign > 0 else iv[0][0])))
        vals = sorted(v for _, v in col)
        med = vals[len(vals) // 2]
        allv.append((x, [round(v, 2) for _, v in col][:6], med))
        for y, v in col:
            if sign * (med - v) >= depth / 2.0:
                void.append((x, y, v))
    print(face, "void", len(void), flush=True)
    print(face, "cols", allv[:3], flush=True)
    xs = sorted(set(round(v[0], 2) for v in void)); ys = sorted(set(round(v[1], 2) for v in void))
    print(face, "x", xs[:3], xs[-3:], "y", ys[:3], ys[-3:], flush=True)
    print(face, glyph_math.analyze(void), flush=True)
print("DIAG_DONE", flush=True)
