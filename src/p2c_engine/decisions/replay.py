from __future__ import annotations

from collections.abc import Sequence

from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import (
    DecisionIdMismatch,
    ReplayDigestMismatch,
    SelectedKeyMismatch,
)
from p2c_engine.sampling.digest import pool_digest
from p2c_engine.sampling.order import ordered_candidates
from p2c_engine.sampling.ppswor import choose_without_replacement

from ._guard import DecisionIdGuard
from .protocol import Decision


class ReplayDecisionSource:
    def __init__(self, records: Sequence[DecisionRecord]):
        self._records = tuple(records)
        self._position = 0
        self._guard = DecisionIdGuard()

    @property
    def exhausted(self) -> bool:
        return self._position == len(self._records)

    def choose_one(self, decision_id: str, candidates: Sequence[Candidate]) -> Decision:
        claimed_id = self._guard.claim(decision_id)
        if self._position >= len(self._records):
            raise DecisionIdMismatch("replay has no remaining DecisionRecord")
        record = self._records[self._position]
        self._position += 1

        if record.decision_id != claimed_id:
            raise DecisionIdMismatch(
                f"expected decision_id {record.decision_id}, got {claimed_id}"
            )

        ordered = ordered_candidates(candidates)
        digest = pool_digest(ordered)
        total = sum(candidate.weight for candidate in ordered)
        if (
            digest != record.candidate_digest
            or len(ordered) != record.candidate_count
            or total != record.total_weight
        ):
            raise ReplayDigestMismatch(f"candidate pool mismatch for {claimed_id}")

        if record.selected_rank < 0 or record.selected_rank >= len(ordered):
            raise SelectedKeyMismatch(f"selected rank out of range for {claimed_id}")
        selected = ordered[record.selected_rank]
        if selected.key != record.selected_key:
            raise SelectedKeyMismatch(
                f"selected key mismatch for {claimed_id}: {selected.key} != {record.selected_key}"
            )

        if record.raw_draw is not None:
            if isinstance(record.raw_draw, bool) or not isinstance(record.raw_draw, int):
                raise ReplayDigestMismatch(f"invalid raw_draw type for {claimed_id}")
            if record.raw_draw < 0 or record.raw_draw >= total:
                raise ReplayDigestMismatch(f"raw_draw out of range for {claimed_id}")
            lower_bound = sum(candidate.weight for candidate in ordered[: record.selected_rank])
            upper_bound = lower_bound + selected.weight
            if not (lower_bound <= record.raw_draw < upper_bound):
                raise ReplayDigestMismatch(
                    f"raw_draw does not select recorded candidate for {claimed_id}"
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
