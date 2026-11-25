"""K6 B3 fixture: a copy of the check_stack.py header that imports a sketch script. Scanned by AST only, never run."""
import ast
import math

import sketch_loader
from stubs import s1_stub


def to_shop_floor(z_A, P):
    return z_A + P.get("jig.datum_a_above_floor")
