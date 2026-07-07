from __future__ import annotations

from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
src = root / "src"
for candidate in (src, root):
    text = str(candidate)
    if text not in sys.path:
        sys.path.insert(0, text)

from p2c_engine import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID, TRACE_SCHEMA_VERSION
from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, ReplayDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import Candidate
from p2c_engine.sampling.exact import branch_options
from p2c_engine.trace import ReplayContext, build_compact_ledger, build_full_ledger


def main() -> None:
    candidates = (
        Candidate("alpha", 1),
        Candidate("beta", 2),
        Candidate("gamma", 3),
    )
    recording = RecordingDecisionSource(SeededDecisionSource(77))
    sampled = recording.choose_one("fixture.add", candidates)

    replay = ReplayDecisionSource(recording.records)
    replayed = replay.choose_one("fixture.add", tuple(reversed(candidates)))
    if replayed != sampled or not replay.exhausted:
        raise RuntimeError("M4 replay round-trip failed")

    options = branch_options("fixture.add", candidates)
    numerator_sum = sum(
        option.probability_numerator * (6 // option.probability_denominator)
        for option in options
    )
    if numerator_sum != 6:
        raise RuntimeError("M4 exact branch probabilities do not sum to one")

    context = ReplayContext(
        trace_schema_version=TRACE_SCHEMA_VERSION,
        semantic_fingerprint="fixture-semantic",
        action_fingerprint="fixture-action",
        pre_state_hash="fixture-state",
    )
    compact = build_compact_ledger(context=context, decisions=recording.records)
    full = build_full_ledger(
        context=context,
        decisions=recording.records,
        pool_snapshots=recording.pool_snapshots,
        master_seed=77,
    )
    if compact.decisions != full.decisions:
        raise RuntimeError("compact/full ledger decision cores differ")

    print("P2C_M4_VALIDATION: PASS")
    print(f"RNG_STREAM_VERSION: {RNG_STREAM_VERSION}")
    print(f"SAMPLING_ALGORITHM_ID: {SAMPLING_ALGORITHM_ID}")
    print(f"TRACE_SCHEMA_VERSION: {TRACE_SCHEMA_VERSION}")
    print(f"SELECTED_KEY: {sampled.selected.key}")
    print(f"RAW_DRAW: {sampled.record.raw_draw}")
    print(f"CANDIDATE_DIGEST: {sampled.record.candidate_digest}")
    print(f"COMPACT_LEDGER_HASH: {sha256_canonical(compact)}")
    print(f"FULL_LEDGER_HASH: {sha256_canonical(full)}")


if __name__ == "__main__":
    main()
