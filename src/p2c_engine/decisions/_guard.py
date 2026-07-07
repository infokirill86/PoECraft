from __future__ import annotations

from p2c_engine.domain.defects import DuplicateDecisionIdDefect

from .ids import validate_decision_id


class DecisionIdGuard:
    def __init__(self) -> None:
        self._used_decision_ids: set[str] = set()

    def claim(self, decision_id: str) -> str:
        valid = validate_decision_id(decision_id)
        if valid in self._used_decision_ids:
            raise DuplicateDecisionIdDefect(f"decision_id reused in one execution: {valid}")
        self._used_decision_ids.add(valid)
        return valid
