from __future__ import annotations

from collections.abc import Sequence

from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.sampling.digest import pool_digest
from p2c_engine.sampling.ppswor import choose_without_replacement
from p2c_engine.sampling.weighted import weighted_choice

from ._guard import DecisionIdGuard
from .protocol import Decision


class SeededDecisionSource:
    def __init__(self, master_seed: int):
        if not isinstance(master_seed, int) or isinstance(master_seed, bool) or master_seed < 0:
            raise SamplingContractDefect("master_seed must be a non-negative non-bool integer")
        self.master_seed = master_seed
        self._guard = DecisionIdGuard()

    def choose_one(self, decision_id: str, candidates: Sequence[Candidate]) -> Decision:
        claimed_id = self._guard.claim(decision_id)
        selected, rank, raw_draw, total, ordered = weighted_choice(
            master_seed=self.master_seed,
            decision_id=claimed_id,
            candidates=candidates,
        )
        record = DecisionRecord(
            decision_id=claimed_id,
            candidate_digest=pool_digest(ordered),
            candidate_count=len(ordered),
            total_weight=total,
            raw_draw=raw_draw,
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
