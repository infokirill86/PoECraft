from __future__ import annotations
from typing import Any
from p2c_engine.canonical import canonical_json_bytes


def _stable_sort(values: list[Any]) -> list[Any]:
    return sorted(values, key=canonical_json_bytes)


def normalize_scope(scope: dict[str, Any]) -> dict[str, Any]:
    result = dict(scope)
    for key in (
        'active_operation_groups', 'reference_only_operation_groups',
        'active_mechanics', 'excluded_from_active_solver',
    ):
        if isinstance(result.get(key), list):
            result[key] = sorted(result[key])
    return result


def normalize_success(success: dict[str, Any]) -> dict[str, Any]:
    result = dict(success)
    family_sets = result.get('family_sets')
    if isinstance(family_sets, dict):
        result['family_sets'] = {
            key: sorted(value) if isinstance(value, list) else value
            for key, value in family_sets.items()
        }
    return result


_NON_RUNTIME_OPERATION_KEYS = frozenset({
    # Human-readable explanation/evidence. These remain covered by source_fingerprint,
    # but are deliberately excluded from active runtime semantics.
    'combined_bundle',
    'condition',
    'failure_atomicity',
    'remaining_general_offers',
    'steps',
    'verification_basis',
    'verification_status',
})


def _project_runtime_value(value: Any, *, key: str | None = None) -> Any:
    """Remove narrative-only fields while preserving executable mechanic facts."""
    if key in _NON_RUNTIME_OPERATION_KEYS:
        return None
    if key == 'algorithm' and isinstance(value, list):
        # A scalar algorithm is a machine enum; a list is explanatory prose.
        return None
    if isinstance(value, dict):
        projected = {}
        for child_key, child_value in value.items():
            child = _project_runtime_value(child_value, key=child_key)
            if child is not None:
                projected[child_key] = child
        return projected
    if isinstance(value, list):
        return [_project_runtime_value(item) for item in value]
    return value


def normalize_operations(operations: dict[str, Any], active_groups: set[str]) -> dict[str, Any]:
    """Project only active executable semantics; raw/reference prose stays source-audited."""
    result = {k: v for k, v in operations.items() if k not in {'operations', 'handler_declarations'}}
    rows = []
    for row in operations.get('operations') or []:
        if (
            not isinstance(row, dict)
            or row.get('group') not in active_groups
            or not row.get('active_in_current_simulation', False)
        ):
            continue
        normalized = _project_runtime_value(row)
        if isinstance(normalized.get('input_rarity'), list):
            normalized['input_rarity'] = sorted(normalized['input_rarity'])
        rows.append(normalized)
    result['operations'] = sorted(rows, key=lambda row: row.get('operation_id', ''))
    declarations = operations.get('handler_declarations') or {}
    result['handler_declarations'] = {
        key: declarations[key] for key in sorted(declarations) if key in active_groups
    }
    return result


def normalize_omens(omens: dict[str, Any], active_groups: set[str]) -> dict[str, Any]:
    result = {k: v for k, v in omens.items() if k != 'omens'}
    rows=[]
    for row in omens.get('omens') or []:
        if not isinstance(row, dict):
            continue
        groups = row.get('operation_groups') or []
        if groups and not active_groups.intersection(groups):
            continue
        normalized=dict(row)
        if isinstance(normalized.get('operation_groups'), list):
            normalized['operation_groups']=sorted(normalized['operation_groups'])
        rows.append(normalized)
    result['omens']=sorted(rows,key=lambda row: row.get('omen_id',''))
    return result


def normalize_initial_states(initial_states: dict[str, Any]) -> dict[str, Any]:
    result=dict(initial_states)
    if isinstance(result.get('states'), list):
        result['states']=sorted(result['states'], key=lambda row: row.get('initial_state_id',''))
    policy=result.get('active_start_policy')
    if isinstance(policy, dict) and isinstance(policy.get('economic_fields_pending'), list):
        policy=dict(policy); policy['economic_fields_pending']=sorted(policy['economic_fields_pending'])
        result['active_start_policy']=policy
    return result


def normalize_family_registry(families: dict[str, Any]) -> dict[str, Any]:
    result=dict(families)
    rows=[]
    for row in result.get('families') or []:
        normalized=dict(row)
        if isinstance(normalized.get('roles'), list):
            normalized['roles']=sorted(normalized['roles'])
        rows.append(normalized)
    result['families']=sorted(rows,key=lambda row: row.get('family_id',''))
    return result


def normalize_failure_policy(policy: dict[str, Any]) -> dict[str, Any]:
    result = {k: v for k, v in policy.items() if k not in {'rules', 'notes'}}
    rows = []
    for i, row in enumerate(policy.get('rules') or []):
        if not isinstance(row, dict):
            continue
        normalized = dict(row)
        normalized['source_rule_key'] = (
            f"{normalized.get('operation_group', '')}:"
            f"{normalized.get('failure_stage', '')}:"
            f"{normalized.get('failure_code', '')}:"
            f"{i}"
        )
        consumed = normalized.get('consumed_resources')
        if isinstance(consumed, list):
            normalized['consumed_resources'] = sorted(consumed, key=lambda value: repr(value))
        rows.append(normalized)
    result['rules'] = sorted(
        rows,
        key=lambda row: (
            row.get('operation_group', ''),
            row.get('failure_stage', ''),
            row.get('failure_code', ''),
            row.get('source_rule_key', ''),
        ),
    )
    return result
