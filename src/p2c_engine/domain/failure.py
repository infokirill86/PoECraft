from dataclasses import dataclass
from typing import Any, Mapping
from .enums import FailureCode, FailureStage, OutcomeKind

@dataclass(frozen=True, slots=True)
class FailureConsumptionRule:
    operation_group: str
    failure_stage: FailureStage
    failure_code: str
    outcome_kind: OutcomeKind
    state_unchanged: bool
    consumed_resources: tuple[str, ...]
    contract_source: str
