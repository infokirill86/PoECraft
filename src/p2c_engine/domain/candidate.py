from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Candidate:
    """Stable machine-identified weighted candidate used by M4 sampling."""

    key: str
    weight: int


@dataclass(frozen=True, slots=True)
class BranchOption:
    """One exact branch derived from the same canonical sampling semantics."""

    decision_id: str
    candidate_digest: str
    selected_rank: int
    selected_key: str
    weight: int
    total_weight: int
    probability_numerator: int
    probability_denominator: int
