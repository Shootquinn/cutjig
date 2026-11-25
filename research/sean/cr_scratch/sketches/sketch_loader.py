"""Loader for the sketch harness: params.yaml, then the proposed-keys overlay, merged at leaf level.

Paths resolve from this file: walk up to the directory holding params.yaml; the overlay sits beside this module.
No absolute paths, so the harness moves to docs/sketches/ unchanged (gameplan Design Notes 7).
Dependencies: stdlib and PyYAML only. check_stack.py imports this module and nothing else from the harness.
Specs load through load_spec (non-string keys rejected).
"""
import hashlib
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
LEGAL_STATUS = ("VERIFIED", "DECLARED", "ASSUMED", "DERIVED")
LEAF_FIELDS = ("value", "unit", "source", "status")


def find_root(start=HERE):
    for d in [Path(start).resolve()] + list(Path(start).resolve().parents):
        if (d / "params.yaml").is_file():
            return d
    raise FileNotFoundError(f"no params.yaml above {start}")


def default_params_path():
    return find_root() / "params.yaml"


def default_overlay_path():
    return HERE / "proposed_params.yaml"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_spec(path):
    """A sketch spec. Rejects non-string keys in feature rows and their sense and neighbour entries (SW-1: YAML 1.1
    reads an unquoted on/off/yes/no key as a boolean, so `on: core_seat` arrives as {True: 'core_seat'})."""
    spec = load_yaml(path)
    bad = []
    for row in spec.get("features") or []:
        rid = row.get("id", "?") if isinstance(row, dict) else "?"
        bad += [f"row {rid}: key {k!r}" for k in row if not isinstance(k, str)]
        for fld in ("sense", "neighbours", "place", "label", "z_rule"):
            items = row.get(fld) or []
            for item in (items if isinstance(items, list) else [items]):
                if isinstance(item, dict):
                    bad += [f"row {rid} {fld}: key {k!r}" for k in item if not isinstance(k, str)]
    if bad:
        raise ValueError(f"spec {Path(path).name}: non-string keys (quote on/off/yes/no or rename): " + "; ".join(bad))
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
