p = "C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/cr_scratch/probe_step6_marks_patched.py"
s = open(p, encoding="utf-8").read()
s = s.replace("sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))", "sys.path.insert(0, 'C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/tests/probes')")
a = s.index("    bx = C.V(0, 0, 0)")
b = s.index("    for wing, sx in")
s = s[:a] + '''    import Part
    crops = [Part.makeBox(r_out - r_in + 2, 2 * SPAN_Y, z_hi + 20, C.V(r_in - 1, -SPAN_Y, -10)),
             Part.makeBox(r_out - r_in + 2, 2 * SPAN_Y, z_hi + 20, C.V(-(r_out + 1), -SPAN_Y, -10))]
    sh = sh.common(Part.makeCompound(crops))
''' + s[b:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
