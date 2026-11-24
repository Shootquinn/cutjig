"""Applies the test predicates of tests/test_step6_parts.py to results/probes/step6_marks_patched.json (probe copy with two window corrections)."""
import json
import math
import sys

sys.path.insert(0, "C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig")
sys.path.insert(0, "C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/tests")
import test_step6_parts as T  # noqa: E402
from build_parts import common  # noqa: E402

p = common.load_params()
K = lambda k: common.get(p, k)
d = json.load(open("C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/results/probes/step6_marks_patched.json"))
print("EVID glyph_errors:", T.glyph_errors(d["glyphs"], {"tighten": -1, "loosen": +1}, K("nut.arrow_length")))
w = d["witness"]
n = int(math.floor(K("holder.stroke_gap_R") / K("witness.scale_pitch") + 1e-9)) + 1
first = w["rim_top_z"] - K("nut.skirt_below_flange")
print("EVID scale_errors:", T.scale_errors(sorted(w["marks_z"]), n, K("witness.scale_pitch"), first))
skirt_bottom = first
for name, key in (("K-max", "holder.stroke_gap_min_K"), ("K d+1", "witness.zone_high")):
    gap = K(key)
    got = T.witness_reading(w["tick_local_z"], w["holder_under_local_z"], skirt_bottom, min(w["marks_z"]), gap)
    print("EVID HD7 %s reading %.4f want %.3f diff %.4f pass %s tick_count %d" % (name, got, gap, got - gap, abs(got - gap) <= 0.05, w["tick_count"]))
rj = json.load(open("C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/parts_cache/nut_result.json"))
for nm, s in (("tighten", -1), ("loosen", +1)):
    r = rj["glyphs"][nm]
    hit = [x for x in d["glyphs"] if x["direction_sign"] == s][0]
    print("EVID json", nm, r["direction_sign"] == s, abs(r["radial_span"] - K("nut.glyph_length")) <= 1.0, abs(hit["span"] - r["radial_span"]) <= 0.5,
          "%s%s" % (hit["wing"], hit["face"]) == "%s%s" % (r["wing"], r["face"]))
