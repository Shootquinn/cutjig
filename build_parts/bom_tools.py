"""BOM and report-list helpers: markdown table parser, allocation and hardware checks,
generators for bom_stock_allocation.md, bom_purchased.md, report_assumptions.md.
Counts come from this script, not from prose.
Run: python build_parts/bom_tools.py   (rewrites the three markdown files from params.yaml)"""
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from build_parts import common  # noqa: E402


# ---------------------------------------------------------------- parsing
def parse_md_tables(text):
    """Return {heading: [row dict, ...]} for every markdown table under a '## heading'."""
    out, head, rows, cols = {}, None, None, None
    for line in text.splitlines():
        if line.startswith("## "):
            head, rows, cols = line[3:].strip(), None, None
            continue
        if head is None or not line.startswith("|"):
            if rows is not None and not line.startswith("|"):
                rows, cols = None, None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cols is None:
            cols, rows = cells, []
            out[head] = rows
        elif set("".join(cells)) <= set("-: "):
            continue
        else:
            rows.append(dict(zip(cols, cells)))
    return out


# ---------------------------------------------------------------- checks
def check_allocation(onhand, alloc, extra):
    """P3. Rows are dicts of strings. Returns list of error strings."""
    errs = []
    stock = {int(r["Length_mm"]): int(r["Qty"]) for r in onhand}
    used = {}
    for r in alloc:
        src, cut, qty = int(r["Source_mm"]), int(r["Cut_mm"]), int(r["Qty"])
        if src not in stock:
            errs.append(f"{r['Member']}: source {src} not on hand")
            continue
        if cut > src:
            errs.append(f"{r['Member']}: cut {cut} longer than source {src}")
        used[src] = used.get(src, 0) + cut * qty
    for src, total in used.items():
        if total > stock[src] * src:
            errs.append(f"source {src}: cuts sum {total} > on hand {stock[src] * src}")
    for r in extra:
        if r.get("Source_mm", "") != "cut-to-order":
            errs.append(f"extra cut {r.get('Member')} not marked cut-to-order")
    return errs


def check_hardware(text):
    """P4. T-nuts M6 spring-ball roll-in only; brackets full-size 30-series; no 'mini'."""
    errs = []
    if re.search(r"\bmini\b", text, re.I):
        errs.append("mini found")
    t = parse_md_tables(text)
    tn = t.get("T-nuts", [])
    if not tn:
        errs.append("no T-nut rows")
    for r in tn:
        s = " ".join(r.values())
        if "M6 spring-ball roll-in" not in s:
            errs.append(f"T-nut row not M6 spring-ball roll-in: {s}")
    br = t.get("Brackets", [])
    if not br:
        errs.append("no bracket rows")
    for r in br:
        s = " ".join(r.values())
        if "full-size 30-series" not in s:
            errs.append(f"bracket row not full-size 30-series: {s}")
    return errs


def assumption_rows(params):
    return [(k, l["status"]) for k, l in common.iter_leaves(params) if l["status"] in ("ASSUMED", "DECLARED")]


def check_assumptions_md(params, text):
    """P7. Each ASSUMED or DECLARED leaf has a row '| `key` | LABEL |' and the counts line matches."""
    errs = []
    for k, st in assumption_rows(params):
        pat = re.compile(r"^\|\s*`" + re.escape(k) + r"`\s*\|\s*" + st + r"\s*\|", re.M)
        if not pat.search(text):
            errs.append(f"{k} not listed with label {st}")
    c = common.status_counts(params)
    want = (f"Counts: DECLARED {c['DECLARED']}, ASSUMED {c['ASSUMED']}, VERIFIED {c['VERIFIED']}, "
            f"DERIVED {c['DERIVED']}, total {c['total']}")
    if want not in text:
        errs.append("counts line missing or wrong")
    return errs


# ---------------------------------------------------------------- generators
def gen_stock_md(p):
    onhand = common.get(p, "stock.on_hand")
    members = common.get(p, "frame.members")
    L = ["## On hand", "", "| Length_mm | Qty | Total_mm |", "|---|---|---|"]
    for r in onhand:
        L.append(f"| {r['length']} | {r['qty']} | {r['length'] * r['qty']} |")
    tot = sum(r["length"] * r["qty"] for r in onhand)
    L += ["", f"Total on hand {tot} mm (DECLARED, step0_human_stock_80-20.md; computed here). Stock is shared with other projects.", ""]
    L += ["## Allocation", "", "| Member | Source_mm | Cut_mm | Qty | Role |", "|---|---|---|---|---|"]
    for m in members:
        L.append(f"| {m['id']} | {m['source_mm']} | {m['cut_mm']} | {m['qty']} | {m['role']} |")
    L += ["", "Allocation is from on-hand stock (ASSUMED roles, Design Notes 7). Each member uses a whole stock piece, so no saw cut is needed. 1540 mm lengths are reserved for columns at Step 12 and are unused here.", ""]
    L += ["## Consumption", "", "| Source_mm | Pieces_on_hand | Pieces_used | Pieces_left | Length_used_mm | Length_left_mm |", "|---|---|---|---|---|---|"]
    used_total = 0
    for r in onhand:
        s = r["length"]
        cut_sum = sum(m["cut_mm"] * m["qty"] for m in members if m["source_mm"] == s)
        pieces = sum(m["qty"] for m in members if m["source_mm"] == s)  # whole-piece members
        used_total += cut_sum
        L.append(f"| {s} | {r['qty']} | {pieces} | {r['qty'] - pieces} | {cut_sum} | {s * r['qty'] - cut_sum} |")
    L += ["", f"Jig consumes {used_total} mm of {tot} mm; {tot - used_total} mm remains for other projects (computed).", ""]
    L += ["## Extra cuts", "", "| Member | Source_mm | Cut_mm | Qty | Note |", "|---|---|---|---|---|"]
    L += ["", f"None required at Step 1. Cut-to-order lengths of 30-6060 are allowed (${common.get(p, 'stock.cut_cost'):.2f} per cut, DECLARED) and are listed only in this table when added.", ""]
    return "\n".join(L)


def gen_purchased_md(p):
    g = lambda k: common.get(p, k)
    bpj, tpb = g("hardware.brackets_per_joint"), g("hardware.tnuts_per_bracket")
    pj = g("hardware.purchased_bracket_joints")
    brackets = pj * bpj                      # purchased
    printed = g("hardware.printed_bracket_joints") * g("hardware.printed_brackets_per_joint")      # C6 option (a): one printed bracket per support-end joint
    all_brackets = brackets + printed        # T-nuts and screws serve purchased and printed brackets
    tn_base = all_brackets * tpb + g("hardware.baseplate_fasteners")
    spare = g("hardware.spare_fraction")
    tn = math.ceil(tn_base * (1 + spare))
    scr_br = math.ceil(all_brackets * tpb * (1 + spare))
    scr_bp = math.ceil(g("hardware.baseplate_fasteners") * (1 + spare))
    L = ["## Brackets", "",
         "| Class | Candidate SKU | Qty | Note |", "|---|---|---|---|",
         f"| full-size 30-series corner bracket, leg at least {g('hardware.bracket_leg_min')} mm | {g('hardware.bracket_sku')} | {brackets} | {pj} outer-corner joints x {bpj}; verify SKU and leg length at purchase |", "",
         f"Superseded: {g('hardware.bracket_sku_superseded')}. Source: Step 2 bracket choice rule (full-size only, per joint). Bracket count is ASSUMED. {printed} printed brackets (not purchased) take the {g('hardware.printed_bracket_joints')} plate-support ends: {g('hardware.printed_bracket')}.", ""]
    L += ["## T-nuts", "",
          "| Type | Candidate SKU | Qty | Note |", "|---|---|---|---|",
          f"| M6 spring-ball roll-in | {g('hardware.tnut_sku')} | {tn} | {all_brackets} brackets (purchased and printed) x {tpb} + {g('hardware.baseplate_fasteners')} base plate, plus {int(spare * 100)} % spares; fit in the 30 slot is declared by use (hardware.tnut_fit_30series) |", ""]
    L += ["## Fasteners", "",
          "| Item | Qty | Note |", "|---|---|---|",
          f"| M6 x {g('hardware.screw_length_bracket')} stainless button or socket head screw | {scr_br} | bracket to T-nut |",
          f"| M6 x {g('hardware.screw_length_baseplate')} stainless socket head screw | {scr_bp} | base plate to frame T-nuts |",
          f"| M6 stainless flat washer | {scr_br + scr_bp} | one per screw |", "",
          "Stainless M6 for non-80/20 joints. On-hand screw inventory is treated as nil (Design Notes 12); lengths follow the QMRD3 inventory list. Counts are computed by build_parts/bom_tools.py from params.yaml `hardware.*` and `frame.joints`.", ""]
    return "\n".join(L)


def gen_assumptions_md(p):
    c = common.status_counts(p)
    L = ["## Report assumptions list", "",
         f"Counts: DECLARED {c['DECLARED']}, ASSUMED {c['ASSUMED']}, VERIFIED {c['VERIFIED']}, DERIVED {c['DERIVED']}, total {c['total']}", "",
         "| Key | Label | Source |", "|---|---|---|"]
    for k, st in assumption_rows(p):
        src = common.leaf(p, k)["source"].replace("|", "/")
        L.append(f"| `{k}` | {st} | {src} |")
    L += ["", f"Soft target: `jig.height_target` {common.get(p, 'jig.height_target')} mm (DECLARED, gate B6), recorded and reported, not tested; frame 60 + columns 1540 = 1600 mm before overhang (Step 2).", ""]
    return "\n".join(L)


def main():
    p = common.load_params()
    (ROOT / "bom_stock_allocation.md").write_text(gen_stock_md(p), encoding="utf-8")
    (ROOT / "bom_purchased.md").write_text(gen_purchased_md(p), encoding="utf-8")
    (ROOT / "report_assumptions.md").write_text(gen_assumptions_md(p), encoding="utf-8")
    print("BOM_TOOLS_OK", common.status_counts(p))


if __name__ == "__main__":
    main()
