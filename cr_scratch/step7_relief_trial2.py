import sys, glob
sys.path.insert(0, r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts")
import cadlib as C
import Part
D = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\cr_scratch\nutdump\n"
def ld(n):
    s = Part.Shape(); s.read(D + n + ".brep"); return s
base = ld("_after_stud"); tools = [ld("_tool%02d" % i) for i in range(13)]
relief, others = tools[0], tools[1:]
def clean(s):
    try:
        s.check(True); return True
    except Exception:
        return False
def rep(lab, s):
    print(lab, "vol", round(s.Volume, 3), "F", len(s.Faces), "E", len(s.Edges), "valid", s.isValid(), "bop", clean(s), flush=True)
print("relief bbox", relief.BoundBox, flush=True)
t_all = C.fuse_all(tools); rep("1 all-fused-one-cut", base.cut(t_all))
t_oth = C.fuse_all(others); s_oth = base.cut(t_oth); rep("2 others-only", s_oth)
rep("3 others then relief", s_oth.cut(relief))
rep("4 relief then others(fused)", base.cut(relief).cut(t_oth))
rep("5 one cut: multi-tool (relief, others fused separately)", base.cut([relief, t_oth]) if hasattr(base, "cut") else base)
print("DONE trial2")
