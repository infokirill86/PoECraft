from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DecisionRecord:
    decision_id: str
    candidate_digest: str
    candidate_count: int
    total_weight: int | None
    raw_draw: int | None
    selected_rank: int
    selected_key: str


@dataclass(frozen=True, slots=True)
class CandidatePoolSnapshot:
    decision_id: str
    candidates: tuple[tuple[str, int], ...]
    cumulative: tuple[int, ...]
    total_weight: int
