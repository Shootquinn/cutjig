import sys
import FreeCAD as App
import Part
for path in (r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\research\quinn\cr_scratch\step6_before\receiver.FCStd",
             r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\parts_cache\receiver.FCStd"):
    d = App.openDocument(path)
    o = d.getObject("Body")
    sh = o.Shape
    print("FILE", path.split("\\")[-2], "valid", sh.isValid(), "solids", len(sh.Solids), "vol", sh.Volume, "faces", len(sh.Faces), flush=True)
    try:
        sh.check(True)
        print("check ok", flush=True)
    except Exception as e:
        print("CHECK", str(e)[:1500], flush=True)
    for ob in d.Objects:
        if hasattr(ob, "Shape") and ob.Shape.Solids:
            print(ob.Name, ob.Shape.isValid(), len(ob.Shape.Faces), flush=True)
    App.closeDocument(d.Name)
print("DIAG_DONE", flush=True)
