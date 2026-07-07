from __future__ import annotations

from collections.abc import Sequence

from p2c_engine.domain.versions import RNG_STREAM_VERSION
from p2c_engine.canonical.hashes import sha256_bytes
from p2c_engine.canonical.json import canonical_json_bytes
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.defects import SamplingContractDefect

from .order import ordered_candidates


def _require_non_negative_int(name: str, value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise SamplingContractDefect(f"{name} must be a non-negative non-bool integer")
    return value


def _expand_hash_bytes(
    *, master_seed: int, decision_id: str, rejection_counter: int, size: int
) -> bytes:
    output = bytearray()
    block_index = 0
    while len(output) < size:
        payload = {
            "seed": master_seed,
            "decision_id": decision_id,
            "rejection_counter": rejection_counter,
            "block_index": block_index,
            "rng_stream_version": RNG_STREAM_VERSION,
        }
        output.extend(sha256_bytes(canonical_json_bytes(payload, schema_version=1)))
        block_index += 1
    return bytes(output[:size])


def draw_uniform(*, master_seed: int, decision_id: str, total: int) -> int:
    seed = _require_non_negative_int("master_seed", master_seed)
    total_int = _require_non_negative_int("total", total)
    if total_int < 1:
        raise SamplingContractDefect("total must be at least 1")
    if not isinstance(decision_id, str) or not decision_id:
        raise SamplingContractDefect("decision_id must be a non-empty string")

    # Draw from a power-of-two envelope and reject the unused tail.
    width = max(1, total_int.bit_length())
    byte_count = (width + 7) // 8
    mask = (1 << width) - 1
    rejection_counter = 0
    while True:
        raw_bytes = _expand_hash_bytes(
            master_seed=seed,
            decision_id=decision_id,
            rejection_counter=rejection_counter,
            size=byte_count,
        )
        draw = int.from_bytes(raw_bytes, "big") & mask
        if draw < total_int:
            return draw
        rejection_counter += 1


def weighted_choice(
    *, master_seed: int, decision_id: str, candidates: Sequence[Candidate]
) -> tuple[Candidate, int, int, int, tuple[Candidate, ...]]:
    ordered = ordered_candidates(candidates)
    total = sum(candidate.weight for candidate in ordered)
    raw_draw = draw_uniform(master_seed=master_seed, decision_id=decision_id, total=total)

    cumulative = 0
    for rank, candidate in enumerate(ordered):
        cumulative += candidate.weight
        if raw_draw < cumulative:
            return candidate, rank, raw_draw, total, ordered

    raise SamplingContractDefect("weighted selection failed to select a candidate")
