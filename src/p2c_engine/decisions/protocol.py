from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.decision import DecisionRecord


@dataclass(frozen=True, slots=True)
class Decision:
    selected: Candidate
    record: DecisionRecord


class DecisionSource(Protocol):
    def choose_one(self, decision_id: str, candidates: Sequence[Candidate]) -> Decision:
        ...

    def choose_sequence(
        self, decision_id: str, candidates: Sequence[Candidate], k: int
    ) -> tuple[Decision, ...]:
        ...
