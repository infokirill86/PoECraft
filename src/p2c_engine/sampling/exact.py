from __future__ import annotations

from collections.abc import Sequence
from math import gcd

from p2c_engine.domain.candidate import BranchOption, Candidate

from .digest import pool_digest
from .order import ordered_candidates


def branch_options(
    decision_id: str, candidates: Sequence[Candidate]
) -> tuple[BranchOption, ...]:
    ordered = ordered_candidates(candidates)
    digest = pool_digest(ordered)
    total = sum(candidate.weight for candidate in ordered)
    options: list[BranchOption] = []
    for rank, candidate in enumerate(ordered):
        divisor = gcd(candidate.weight, total)
        options.append(
            BranchOption(
                decision_id=decision_id,
                candidate_digest=digest,
                selected_rank=rank,
                selected_key=candidate.key,
                weight=candidate.weight,
                total_weight=total,
                probability_numerator=candidate.weight // divisor,
                probability_denominator=total // divisor,
            )
        )
    return tuple(options)
