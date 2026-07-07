from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .enums import OperationGroup, PlanStage, Rarity, Side


class DecisionKind(StrEnum):
    ADD_MODIFIER = "add_modifier"
    REMOVE_MODIFIER = "remove_modifier"
    SELECT_JAWBONE_SIDE = "select_jawbone_side"
    CONDITIONAL_REPLACEMENT_REMOVAL = "conditional_replacement_removal"
    REVEAL_POLICY = "reveal_policy"


class M4DecisionPrimitive(StrEnum):
    CHOOSE_ONE = "choose_one"
    CHOOSE_SEQUENCE = "choose_sequence"


DECISION_KIND_TO_M4_PRIMITIVE = {
    DecisionKind.ADD_MODIFIER: M4DecisionPrimitive.CHOOSE_ONE,
    DecisionKind.REMOVE_MODIFIER: M4DecisionPrimitive.CHOOSE_ONE,
    DecisionKind.SELECT_JAWBONE_SIDE: M4DecisionPrimitive.CHOOSE_ONE,
    DecisionKind.CONDITIONAL_REPLACEMENT_REMOVAL: M4DecisionPrimitive.CHOOSE_ONE,
    DecisionKind.REVEAL_POLICY: M4DecisionPrimitive.CHOOSE_SEQUENCE,
}


class StateBinding(StrEnum):
    CURRENT = "current"
    AFTER_REMOVAL_0 = "after_removal_0"
    AFTER_ADD_0 = "after_add_0"
    PLACEHOLDER_CONTEXT = "placeholder_context"


class ResultTarget(StrEnum):
    ADD_MODIFIER = "add_modifier"
    REMOVE_MODIFIER = "remove_modifier"
    SIDE_SELECTION = "side_selection"
    REVEAL_POLICY = "reveal_policy"
    NONE = "none"


class PoolTemplateKind(StrEnum):
    ORDINARY_ADD = "ordinary_add"
    REMOVAL = "removal"
    REVEAL_BASE = "reveal_base"


class ResourceKind(StrEnum):
    OPERATION_CURRENCY = "operation_currency"
    OMEN = "omen"


@dataclass(frozen=True, slots=True)
class CanonicalParam:
    name: str
    value: Any


@dataclass(frozen=True, slots=True)
class RarityTransition:
    input_rarities: tuple[Rarity, ...]
    output: Rarity | str


@dataclass(frozen=True, slots=True)
class PoolRequestTemplate:
    template_kind: PoolTemplateKind
    params: tuple[CanonicalParam, ...]


@dataclass(frozen=True, slots=True)
class PlanStageSpec:
    stage_id: str
    order: int
    stage: PlanStage
    template_id: str
    decision_site_id: str | None
    params: tuple[CanonicalParam, ...]


@dataclass(frozen=True, slots=True)
class DecisionSiteSpec:
    decision_site_id: str
    order: int
    decision_kind: DecisionKind
    stage: PlanStage
    state_binding: StateBinding
    pool_request_template: PoolRequestTemplate | None
    result_target: ResultTarget


@dataclass(frozen=True, slots=True)
class ResourceCost:
    resource_id: str
    quantity: int
    resource_kind: ResourceKind


@dataclass(frozen=True, slots=True)
class ResolvedEffect:
    dimension: str
    params: tuple[CanonicalParam, ...]
    source_omen_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ResolvedOmenEffects:
    effects: tuple[ResolvedEffect, ...]


@dataclass(frozen=True, slots=True)
class PreconditionSpec:
    precondition_id: str
    stage: str
    params: tuple[CanonicalParam, ...]


@dataclass(frozen=True, slots=True)
class FailurePolicyBinding:
    operation_group: str
    failure_stage: str
    failure_code: str
    outcome_kind: str
    state_unchanged: bool
    consumed_resources: tuple[ResourceCost, ...]
    source_rule_key: str


@dataclass(frozen=True, slots=True)
class ActionPlanSemanticProjection:
    action_schema_version: int
    action_fingerprint_version: int
    operation_id: str
    operation_group: OperationGroup
    handler_key: str
    resolved_omen_ids: tuple[str, ...]
    resolved_effects: ResolvedOmenEffects
    rarity_transition: RarityTransition
    stages: tuple[PlanStageSpec, ...]
    decision_sites: tuple[DecisionSiteSpec, ...]
    costs: tuple[ResourceCost, ...]
    precondition_specs: tuple[PreconditionSpec, ...]
    failure_policy_bindings: tuple[FailurePolicyBinding, ...]
    static_semantic_fingerprint: str


@dataclass(frozen=True, slots=True)
class ActionIdentityEnvelope:
    action_schema_version: int
    action_fingerprint_version: int
    operation_id: str
    operation_group: OperationGroup
    handler_key: str
    resolved_omen_ids: tuple[str, ...]
    static_semantic_fingerprint: str
    action_fingerprint: str


@dataclass(frozen=True, slots=True)
class ActionPlan:
    action_schema_version: int
    action_fingerprint_version: int
    action_id: str
    operation_id: str
    operation_group: OperationGroup
    handler_key: str
    resolved_omen_ids: tuple[str, ...]
    resolved_effects: ResolvedOmenEffects
    rarity_transition: RarityTransition
    stages: tuple[PlanStageSpec, ...]
    decision_sites: tuple[DecisionSiteSpec, ...]
    costs: tuple[ResourceCost, ...]
    precondition_specs: tuple[PreconditionSpec, ...]
    failure_policy_bindings: tuple[FailurePolicyBinding, ...]
    static_semantic_fingerprint: str
    action_fingerprint: str

    @property
    def fingerprint(self) -> str:
        return self.action_fingerprint

    def semantic_projection(self) -> ActionPlanSemanticProjection:
        return ActionPlanSemanticProjection(
            action_schema_version=self.action_schema_version,
            action_fingerprint_version=self.action_fingerprint_version,
            operation_id=self.operation_id,
            operation_group=self.operation_group,
            handler_key=self.handler_key,
            resolved_omen_ids=self.resolved_omen_ids,
            resolved_effects=self.resolved_effects,
            rarity_transition=self.rarity_transition,
            stages=self.stages,
            decision_sites=self.decision_sites,
            costs=self.costs,
            precondition_specs=self.precondition_specs,
            failure_policy_bindings=self.failure_policy_bindings,
            static_semantic_fingerprint=self.static_semantic_fingerprint,
        )

    def identity_envelope(self) -> ActionIdentityEnvelope:
        return ActionIdentityEnvelope(
            action_schema_version=self.action_schema_version,
            action_fingerprint_version=self.action_fingerprint_version,
            operation_id=self.operation_id,
            operation_group=self.operation_group,
            handler_key=self.handler_key,
            resolved_omen_ids=self.resolved_omen_ids,
            static_semantic_fingerprint=self.static_semantic_fingerprint,
            action_fingerprint=self.action_fingerprint,
        )
