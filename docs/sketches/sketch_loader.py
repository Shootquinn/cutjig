"""Loader for the sketch harness: params.yaml, then the proposed-keys overlay, merged at leaf level.

Paths resolve from this file: walk up to the directory holding params.yaml; the overlay sits beside this module.
No absolute paths, so the harness moves to docs/sketches/ unchanged (gameplan Design Notes 7).
Dependencies: stdlib and PyYAML only. check_stack.py imports this module and nothing else from the harness.
Specs load through load_spec (non-string keys rejected).

Output rule (Design Notes 26 decision 1; gameplan Design Notes 25 H4): every unaccepted revision output r0 to r<k>
(checks JSON, summary, PNGs, mass report, visual-gate file) and every verification output (--controls results and
control figures, --baseline record) is written to docs/sketches/wip/ (git-ignored by docs/sketches/.gitignore), created
on demand. Only `check_sketch.py --accept` copies an accepted revision's outputs up to docs/sketches/, with a SHA-256
equality check. Every script resolves its output path through output_path() and reads through find_output() (wip/
first, then docs/sketches/), so the S2 to S6 scripts inherit the rule.
"""
import hashlib
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
LEGAL_STATUS = ("VERIFIED", "DECLARED", "ASSUMED", "DERIVED")
LEAF_FIELDS = ("value", "unit", "source", "status")


WIP = HERE / "wip"


def output_dir(wip=True):
    """docs/sketches/wip/ (created on demand) for unaccepted and verification outputs; docs/sketches/ when wip=False
    (accepted copies, written only by check_sketch.py --accept)."""
    d = WIP if wip else HERE
    d.mkdir(parents=True, exist_ok=True)
    return d


def output_path(name, wip=True):
    """Path of an output file under the output rule (module docstring). name may hold sub-directories."""
    p = output_dir(wip) / name
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def find_output(name):
    """Read path of an output: wip/ first, then docs/sketches/. Returns the wip path when neither exists."""
    for d in (WIP, HERE):
        if (d / name).is_file():
            return d / name
    return WIP / name


def find_root(start=HERE):
    for d in [Path(start).resolve()] + list(Path(start).resolve().parents):
        if (d / "params.yaml").is_file():
            return d
    raise FileNotFoundError(f"no params.yaml above {start}")


def default_params_path():
    return find_root() / "params.yaml"


def default_overlay_path():
    return HERE / "proposed_params.yaml"


_YAML_CACHE = {}   # 1.4 step 0 R1 e: parsed YAML per process, keyed by the file's bytes; each call returns a fresh copy


def load_yaml(path):
    """A YAML file as plain data. The parse is cached per process under the SHA-256 of the file's bytes (a changed file is
    a new key), and every call returns an independent deep copy (pickle round trip), so a caller that mutates the result
    never reaches another caller's copy. Equal to yaml.safe_load on every file (1.4 step 0 R1 e: controls rows equal)."""
    import pickle
    with open(path, "rb") as fh:
        raw = fh.read()
    key = hashlib.sha256(raw).hexdigest()
    blob = _YAML_CACHE.get(key)
    if blob is None:
        blob = pickle.dumps(yaml.safe_load(raw.decode("utf-8")) or {}, protocol=pickle.HIGHEST_PROTOCOL)
        _YAML_CACHE[key] = blob
    return pickle.loads(blob)


def load_spec(path):
    """A sketch spec. Rejects non-string keys in feature rows and their sense and neighbour entries (SW-1: YAML 1.1
    reads an unquoted on/off/yes/no key as a boolean, so `on: core_seat` arrives as {True: 'core_seat'})."""
    spec = load_yaml(path)
    expand_neighbour_groups(spec)
    bad = []
    for row in spec.get("features") or []:
        rid = row.get("id", "?") if isinstance(row, dict) else "?"
        bad += [f"row {rid}: key {k!r}" for k in row if not isinstance(k, str)]
        for fld in ("sense", "neighbours", "place", "label", "z_rule"):
            items = row.get(fld) or []
            for item in (items if isinstance(items, list) else [items]):
                if isinstance(item, dict):
                    bad += [f"row {rid} {fld}: key {k!r}" for k in item if not isinstance(k, str)]
        # 1.4 P6 (SW-1 class at any depth: the s4 collet.slits.label `on:` key arrived as True): every nested mapping of a
        # row (sub-artist blocks, their labels, section_true, plane_cuts) holds string keys only
        stack = [(f"row {rid} {k}", v) for k, v in row.items() if isinstance(k, str) and k not in ("sense", "neighbours", "place", "label", "z_rule")] if isinstance(row, dict) else []
        while stack:
            at, v = stack.pop()
            if isinstance(v, dict):
                bad += [f"{at}: key {k!r}" for k in v if not isinstance(k, str)]
                stack += [(f"{at}.{k}", x) for k, x in v.items()]
            elif isinstance(v, list):
                stack += [(f"{at}[{i}]", x) for i, x in enumerate(v)]
    if bad:
        raise ValueError(f"spec {Path(path).name}: non-string keys (quote on/off/yes/no or rename): " + "; ".join(bad))
    return spec


def expand_neighbour_groups(spec):
    """Spec-level neighbour_groups: a row's neighbours entry {use: <group>} is replaced by the group's entries, minus
    any entry whose id equals the row id or an id the row lists explicitly (explicit entries win). Unknown group:
    ValueError."""
    groups = spec.get("neighbour_groups") or {}
    for row in spec.get("features") or []:
        if not isinstance(row, dict) or not row.get("neighbours"):
            continue
        explicit = {nb.get("id") for nb in row["neighbours"] if isinstance(nb, dict) and "use" not in nb}
        out = []
        for nb in row["neighbours"]:
            if isinstance(nb, dict) and "use" in nb:
                if nb["use"] not in groups:
                    raise ValueError(f"row {row.get('id')}: unknown neighbour group {nb['use']!r}")
                out += [dict(g) for g in groups[nb["use"]] if g.get("id") != row.get("id") and g.get("id") not in explicit]
            else:
                out.append(nb)
        row["neighbours"] = out
    return spec


def is_leaf(node):
    return isinstance(node, dict) and "value" in node


def flatten(tree, prefix=""):
    out = {}
    for k, v in (tree or {}).items():
        key = f"{prefix}.{k}" if prefix else str(k)
        if is_leaf(v):
            out[key] = v
        elif isinstance(v, dict):
            out.update(flatten(v, key))
        else:
            out[key] = {"value": v, "_malformed": "bare value, no leaf schema"}
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


class Params:
    """Merged view. params.yaml leaves win; an overlay leaf that shadows one is recorded in .shadowed (K2 fails on it)."""

    def __init__(self, params_path=None, overlay_path=None):
        self.params_path = Path(params_path) if params_path else default_params_path()
        self.overlay_path = Path(overlay_path) if overlay_path else default_overlay_path()
        self.base = flatten(load_yaml(self.params_path))
        self.overlay = flatten(load_yaml(self.overlay_path)) if self.overlay_path.is_file() else {}
        self.shadowed = sorted(set(self.base) & set(self.overlay))
        self.leaves = dict(self.base)
        for k, v in self.overlay.items():
            if k not in self.base:
                self.leaves[k] = v
        self.accessed = {}

    def has(self, key):
        return key in self.leaves

    def leaf(self, key):
        return self.leaves[key]

    def origin(self, key):
        return "params.yaml" if key in self.base else ("overlay" if key in self.overlay else None)

    def get(self, key):
        if key not in self.leaves:
            raise KeyError(f"key not in params.yaml or overlay: {key}")
        val = self.leaves[key]["value"]
        self.accessed[key] = val
        return val

    def hashes(self):
        out = {"params.yaml": sha256(self.params_path)}
        if self.overlay_path.is_file():
            out[self.overlay_path.name] = sha256(self.overlay_path)
        return out
