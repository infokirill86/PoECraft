from __future__ import annotations

import re

from p2c_engine.domain.defects import SamplingContractDefect

_DECISION_ID_RE = re.compile(r"[a-z0-9][a-z0-9_.:-]*\Z")


def validate_decision_id(decision_id: object) -> str:
    if not isinstance(decision_id, str) or _DECISION_ID_RE.fullmatch(decision_id) is None:
        raise SamplingContractDefect(f"invalid decision_id: {decision_id!r}")
    return decision_id
