from __future__ import annotations

from collections.abc import Mapping, Sequence

from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.sampling.digest import pool_digest
from p2c_engine.sampling.order import ordered_candidates
from p2c_engine.sampling.ppswor import choose_without_replacement

from ._guard import DecisionIdGuard
from .protocol import Decision


class ExactBranchingDecisionSource:
    def __init__(self, pins: Mapping[str, int]):
        self._pins = dict(pins)
        self._guard = DecisionIdGuard()

    def choose_one(self, decision_id: str, candidates: Sequence[Candidate]) -> Decision:
        claimed_id = self._guard.claim(decision_id)
        if claimed_id not in self._pins:
            raise SamplingContractDefect(f"missing exact pin for {claimed_id}")
        rank = self._pins[claimed_id]
        if not isinstance(rank, int) or isinstance(rank, bool):
            raise SamplingContractDefect("selected pin must be a non-bool integer")

        ordered = ordered_candidates(candidates)
        if rank < 0 or rank >= len(ordered):
            raise SamplingContractDefect(f"selected pin out of range for {claimed_id}")
        selected = ordered[rank]
        total = sum(candidate.weight for candidate in ordered)
        record = DecisionRecord(
            decision_id=claimed_id,
            candidate_digest=pool_digest(ordered),
            candidate_count=len(ordered),
            total_weight=total,
            raw_draw=None,
            selected_rank=rank,
            selected_key=selected.key,
        )
        return Decision(selected=selected, record=record)

    def choose_sequence(
        self, decision_id: str, candidates: Sequence[Candidate], k: int
    ) -> tuple[Decision, ...]:
        return choose_without_replacement(
            decision_id=decision_id,
            candidates=candidates,
            k=k,
            choose_one=self.choose_one,
        )
