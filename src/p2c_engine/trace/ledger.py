from __future__ import annotations

from collections.abc import Sequence

from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.decision import CandidatePoolSnapshot, DecisionRecord
from p2c_engine.domain.defects import ReplayDigestMismatch
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID, TRACE_SCHEMA_VERSION
from p2c_engine.domain.candidate_pool import ordered_candidates, pool_digest

from .schema import AuditExpansion, AuditPool, LedgerEnvelope, ReplayContext


def _base_ledger(
    *, context: ReplayContext, decisions: Sequence[DecisionRecord], audit: AuditExpansion | None
) -> LedgerEnvelope:
    return LedgerEnvelope(
        trace_schema_version=TRACE_SCHEMA_VERSION,
        semantic_fingerprint=context.semantic_fingerprint,
        action_fingerprint=context.action_fingerprint,
        pre_state_hash=context.pre_state_hash,
        post_state_hash=None,
        outcome_kind=None,
        decisions=tuple(decisions),
        audit=audit,
    )


def build_compact_ledger(
    *, context: ReplayContext, decisions: Sequence[DecisionRecord]
) -> LedgerEnvelope:
    return _base_ledger(context=context, decisions=decisions, audit=None)


def build_full_ledger(
    *,
    context: ReplayContext,
    decisions: Sequence[DecisionRecord],
    pool_snapshots: Sequence[CandidatePoolSnapshot],
    master_seed: int | None,
) -> LedgerEnvelope:
    records = tuple(decisions)
    snapshots = tuple(pool_snapshots)
    if len(records) != len(snapshots):
        raise ReplayDigestMismatch("full ledger decision/pool count mismatch")

    pools: list[AuditPool] = []
    for record, snapshot in zip(records, snapshots, strict=True):
        if snapshot.decision_id != record.decision_id:
            raise ReplayDigestMismatch(
                f"full ledger decision_id mismatch for {record.decision_id}"
            )
        try:
            ordered = ordered_candidates(
                tuple(Candidate(key, weight) for key, weight in snapshot.candidates)
            )
        except (TypeError, ValueError) as exc:
            raise ReplayDigestMismatch(
                f"invalid full ledger pool snapshot for {record.decision_id}"
            ) from exc
        expected_candidates = tuple((candidate.key, candidate.weight) for candidate in ordered)
        expected_cumulative: list[int] = []
        running = 0
        for candidate in ordered:
            running += candidate.weight
            expected_cumulative.append(running)

        if snapshot.candidates != expected_candidates:
            raise ReplayDigestMismatch(
                f"full ledger candidates are not canonical for {record.decision_id}"
            )
        if snapshot.cumulative != tuple(expected_cumulative):
            raise ReplayDigestMismatch(
                f"full ledger cumulative thresholds mismatch for {record.decision_id}"
            )
        if snapshot.total_weight != running or record.total_weight != running:
            raise ReplayDigestMismatch(
                f"full ledger total weight mismatch for {record.decision_id}"
            )
        if len(ordered) != record.candidate_count:
            raise ReplayDigestMismatch(
                f"full ledger candidate count mismatch for {record.decision_id}"
            )
        if pool_digest(ordered) != record.candidate_digest:
            raise ReplayDigestMismatch(
                f"full ledger candidate digest mismatch for {record.decision_id}"
            )
        if record.selected_rank < 0 or record.selected_rank >= len(ordered):
            raise ReplayDigestMismatch(
                f"full ledger selected rank out of range for {record.decision_id}"
            )
        selected = ordered[record.selected_rank]
        if selected.key != record.selected_key:
            raise ReplayDigestMismatch(
                f"full ledger selected key mismatch for {record.decision_id}"
            )
        if record.raw_draw is not None:
            if isinstance(record.raw_draw, bool) or not isinstance(record.raw_draw, int):
                raise ReplayDigestMismatch(
                    f"invalid full ledger raw_draw type for {record.decision_id}"
                )
            lower_bound = 0 if record.selected_rank == 0 else expected_cumulative[record.selected_rank - 1]
            upper_bound = expected_cumulative[record.selected_rank]
            if not (lower_bound <= record.raw_draw < upper_bound):
                raise ReplayDigestMismatch(
                    f"full ledger raw_draw mismatch for {record.decision_id}"
                )

        pools.append(
            AuditPool(
                decision_id=snapshot.decision_id,
                candidates=snapshot.candidates,
                cumulative=snapshot.cumulative,
                total_weight=snapshot.total_weight,
            )
        )
    pools = tuple(pools)
    audit = AuditExpansion(
        pools=pools,
        master_seed=master_seed,
        rng_stream_version=RNG_STREAM_VERSION,
        sampling_algorithm_id=SAMPLING_ALGORITHM_ID,
    )
    return _base_ledger(context=context, decisions=records, audit=audit)
