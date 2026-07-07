from __future__ import annotations

from collections.abc import Sequence

from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.decision import CandidatePoolSnapshot, DecisionRecord
from p2c_engine.sampling.order import ordered_candidates

from .protocol import Decision, DecisionSource


class RecordingDecisionSource:
    def __init__(self, inner: DecisionSource):
        self.inner = inner
        self._records: list[DecisionRecord] = []
        self._pool_snapshots: list[CandidatePoolSnapshot] = []

    @property
    def records(self) -> tuple[DecisionRecord, ...]:
        return tuple(self._records)

    @property
    def pool_snapshots(self) -> tuple[CandidatePoolSnapshot, ...]:
        return tuple(self._pool_snapshots)

    def choose_one(self, decision_id: str, candidates: Sequence[Candidate]) -> Decision:
        ordered = ordered_candidates(candidates)
        decision = self.inner.choose_one(decision_id, ordered)
        cumulative: list[int] = []
        running = 0
        for candidate in ordered:
            running += candidate.weight
            cumulative.append(running)
        self._records.append(decision.record)
        self._pool_snapshots.append(
            CandidatePoolSnapshot(
                decision_id=decision.record.decision_id,
                candidates=tuple((candidate.key, candidate.weight) for candidate in ordered),
                cumulative=tuple(cumulative),
                total_weight=running,
            )
        )
        return decision

    def choose_sequence(
        self, decision_id: str, candidates: Sequence[Candidate], k: int
    ) -> tuple[Decision, ...]:
        from p2c_engine.sampling.ppswor import choose_without_replacement

        return choose_without_replacement(
            decision_id=decision_id,
            candidates=candidates,
            k=k,
            choose_one=self.choose_one,
        )
