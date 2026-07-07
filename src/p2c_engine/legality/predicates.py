from __future__ import annotations
from typing import Callable

PREDICATES: dict[str, Callable[..., bool]] = {}

def register_predicate(name: str):
    def deco(fn: Callable[..., bool]):
        if name in PREDICATES:
            raise ValueError(f"Duplicate predicate: {name}")
        PREDICATES[name]=fn
        return fn
    return deco
