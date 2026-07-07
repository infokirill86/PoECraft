from __future__ import annotations

import re
from collections.abc import Sequence

from p2c_engine.canonical.hashes import sha256_canonical

from .candidate import Candidate
from .defects import SamplingContractDefect

_KEY_RE = re.compile(r"[a-z0-9][a-z0-9_.:-]*\Z")
CANDIDATE_DIGEST_VERSION = 1


def _valid_positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def ordered_candidates(candidates: Sequence[Candidate]) -> tuple[Candidate, ...]:
    if not candidates:
        raise SamplingContractDefect("candidate pool must not be empty")

    seen: set[str] = set()
    normalized: list[Candidate] = []
    for candidate in candidates:
        if not isinstance(candidate, Candidate):
            raise SamplingContractDefect("all candidates must be Candidate instances")
        if not isinstance(candidate.key, str) or _KEY_RE.fullmatch(candidate.key) is None:
            raise SamplingContractDefect(f"invalid candidate key: {candidate.key!r}")
        if candidate.key in seen:
            raise SamplingContractDefect(f"duplicate candidate key: {candidate.key}")
        if not _valid_positive_int(candidate.weight):
            raise SamplingContractDefect(
                f"candidate weight must be a positive non-bool integer: {candidate.key}"
            )
        seen.add(candidate.key)
        normalized.append(candidate)

    return tuple(sorted(normalized, key=lambda candidate: candidate.key.encode("ascii")))


def pool_digest(candidates: Sequence[Candidate]) -> str:
    ordered = ordered_candidates(candidates)
    payload = [[candidate.key, candidate.weight] for candidate in ordered]
    return sha256_canonical(payload, schema_version=CANDIDATE_DIGEST_VERSION)
