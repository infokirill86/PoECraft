from __future__ import annotations

from collections.abc import Callable, Sequence

from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.defects import SamplingContractDefect


def validate_k(k: object, size: int) -> int:
    if not isinstance(k, int) or isinstance(k, bool):
        raise SamplingContractDefect("k must be a non-bool integer")
    if k < 0 or k > size:
        raise SamplingContractDefect("k must be in range 0..len(candidates)")
    return k


def choose_without_replacement(
    *,
    decision_id: str,
    candidates: Sequence[Candidate],
    k: int,
    choose_one: Callable[[str, Sequence[Candidate]], object],
) -> tuple[object, ...]:
    count = validate_k(k, len(candidates))
    remaining = list(candidates)
    decisions: list[object] = []
    for ordinal in range(count):
        child_id = f"{decision_id}.{ordinal}"
        decision = choose_one(child_id, tuple(remaining))
        decisions.append(decision)
        selected = getattr(decision, "selected")
        remaining = [candidate for candidate in remaining if candidate.key != selected.key]
    return tuple(decisions)
