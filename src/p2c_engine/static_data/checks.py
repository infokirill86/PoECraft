from __future__ import annotations
from typing import Any, Mapping
from p2c_engine.domain.defects import StaticDataDefect


RUNTIME_ADMISSION_STATUSES = frozenset({
    'accepted_executable_runtime',
    'engine_primitive',
    'data_reference_candidate',
    'admission_candidate',
    'blocked_or_out_of_scope',
    'disputed_or_requires_user_resolution',
})
ACCEPTED_EXECUTABLE_RUNTIME = 'accepted_executable_runtime'


def _fail(message: str) -> None:
    raise StaticDataDefect(message)


def validate_cross_file_contracts(*, index: Mapping[str, Any], essence: dict[str, Any], operations: dict[str, Any], omens: dict[str, Any], family_registry: dict[str, Any], initial_states: dict[str, Any], scope: dict[str, Any], success: dict[str, Any], failure_policy: dict[str, Any] | None = None) -> None:
    families = family_registry.get('families')
    if not isinstance(families, list):
        _fail('family_registry.families must be a list')
    family_ids = [row.get('family_id') for row in families if isinstance(row, dict)]
    if any(not isinstance(v, str) or not v for v in family_ids) or len(family_ids) != len(set(family_ids)):
        _fail('family_registry contains missing or duplicate family_id')
    family_set = set(family_ids)
    index_families = {m.family_id for m in index.values() if m.static_category != 'desecrated'}
    if not index_families <= family_set:
        _fail(f'modifier index references unregistered families: {sorted(index_families-family_set)}')
    for mod in index.values():
        if not mod.group_ids or any(not isinstance(g, str) or not g for g in mod.group_ids):
            _fail(f'modifier {mod.mod_id} has invalid group_ids')

    op_rows = operations.get('operations')
    if not isinstance(op_rows, list) or not op_rows:
        _fail('operations.operations must be a non-empty list')
    declarations = operations.get('handler_declarations')
    if not isinstance(declarations, dict):
        _fail('operations.handler_declarations must be a mapping')
    op_ids, groups = [], set()
    active_groups = set(scope.get('active_operation_groups') or [])
    reference_groups = set(scope.get('reference_only_operation_groups') or [])
    if active_groups & reference_groups:
        _fail(f'operation groups cannot be both active and reference-only: {sorted(active_groups & reference_groups)}')
    for row in op_rows:
        if not isinstance(row, dict) or not isinstance(row.get('operation_id'), str) or not isinstance(row.get('group'), str):
            _fail('every operation requires operation_id and group')
        op_ids.append(row['operation_id']); groups.add(row['group'])
        runtime_status = row.get('runtime_admission_status')
        if runtime_status not in RUNTIME_ADMISSION_STATUSES:
            _fail(
                f"operation {row['operation_id']} has invalid or missing "
                f"runtime_admission_status"
            )
        expected = row['group'] in active_groups
        if bool(row.get('active_in_current_simulation')) != expected:
            _fail(f"operation {row['operation_id']} active flag contradicts project scope")
        if expected and row['group'] not in declarations:
            _fail(f"active operation {row['operation_id']} has no handler declaration")
        if row['group'] in reference_groups and row.get('active_in_current_simulation'):
            _fail(f"reference-only operation {row['operation_id']} is active-dispatchable")
        if runtime_status == ACCEPTED_EXECUTABLE_RUNTIME and not row.get('active_in_current_simulation'):
            _fail(
                f"operation {row['operation_id']} cannot be executable-admitted "
                f"while inactive in the project-scope catalog"
            )
        if runtime_status == ACCEPTED_EXECUTABLE_RUNTIME and row['group'] not in declarations:
            _fail(
                f"operation {row['operation_id']} is executable-admitted but "
                f"has no handler declaration"
            )
    if len(op_ids) != len(set(op_ids)):
        _fail('duplicate operation_id')
    essence_by_operation = {
        row.get('operation_id'): row.get('guaranteed_mod_id')
        for grade in ('greater', 'perfect') for row in (essence.get(grade) or [])
    }
    for row in op_rows:
        transition = row.get('transition') or {}
        guaranteed = transition.get('guaranteed_mod_id')
        if guaranteed is None:
            continue
        if guaranteed not in index:
            _fail(f"operation {row['operation_id']} references unknown guaranteed output {guaranteed}")
        declared = essence_by_operation.get(row['operation_id'])
        if declared != guaranteed:
            _fail(f"operation {row['operation_id']} guaranteed output contradicts essence catalog")
    unknown_scope_groups = (active_groups | reference_groups) - groups
    if unknown_scope_groups:
        _fail(f'project scope references unknown operation groups: {sorted(unknown_scope_groups)}')
    extra_declarations=set(declarations)-active_groups
    if extra_declarations:
        _fail(f'handler declarations contain non-active groups: {sorted(extra_declarations)}')

    for omen in omens.get('omens') or []:
        for group in omen.get('operation_groups') or []:
            if group not in groups:
                _fail(f"omen {omen.get('omen_id')} references unknown operation group {group}")
        effect = omen.get('effect') or {}
        if isinstance(effect, dict) and 'tagged_first_fill' in effect:
            _fail(f"omen {omen.get('omen_id')} uses superseded tagged_first_fill model")
        lich_constraint = effect.get('lich_tag_constraint') if isinstance(effect, dict) else None
        if lich_constraint is not None:
            if not isinstance(lich_constraint, dict):
                _fail(f"omen {omen.get('omen_id')} lich_tag_constraint must be a mapping")
            if lich_constraint.get('model') != 'guarantee_one':
                _fail(f"omen {omen.get('omen_id')} has unsupported Lich model {lich_constraint.get('model')!r}")
            lich_tag = lich_constraint.get('tag')
            desecrated_tags = {
                mod.lich_tag
                for mod in index.values()
                if mod.static_category == 'desecrated' and mod.lich_tag is not None
            }
            if lich_tag not in desecrated_tags:
                _fail(f"omen {omen.get('omen_id')} references unknown Lich tag {lich_tag!r}")
    for mod in index.values():
        if mod.lich_tag is not None and mod.static_category != 'desecrated':
            _fail(f'modifier {mod.mod_id} has Lich tag outside desecrated category')

    for grade in ('greater','perfect'):
        for row in essence.get(grade) or []:
            mod_id=row.get('guaranteed_mod_id')
            mod=index.get(mod_id)
            if mod is None:
                _fail(f'{grade} essence references unknown guaranteed output {mod_id}')
            if mod.tier != 1 or mod.static_category != f'{grade}_essence':
                _fail(f'{grade} essence output {mod_id} is not a valid single-tier output')
            if mod.family_id != row.get('family_id') or mod.side.value != row.get('side'):
                _fail(f'{grade} essence output {mod_id} contradicts its static modifier')

    for name, values in (success.get('family_sets') or {}).items():
        for family_id in values:
            if family_id not in family_set:
                _fail(f'success family set {name} references unknown family {family_id}')
    for name, family_id in (success.get('single_families') or {}).items():
        if family_id not in family_set:
            _fail(f'success single family {name} references unknown family {family_id}')

    states = initial_states.get('states')
    if not isinstance(states, list) or not states:
        _fail('initial_states.states must be a non-empty list')
    state_ids = {s.get('initial_state_id') for s in states if isinstance(s, dict)}
    primary = (initial_states.get('active_start_policy') or {}).get('primary')
    if primary not in state_ids or scope.get('primary_start') != primary:
        _fail('primary initial state is missing or contradicts project scope')
    active = [s for s in states if s.get('enabled')]
    if len(active) != 1 or active[0].get('initial_state_id') != primary:
        _fail('exactly one enabled initial state must match active_start_policy.primary')
    template = active[0].get('state_template') or {}
    family = template.get('required_modifier_family')
    if family not in family_set:
        _fail(f'initial state references unknown family {family}')
    allowed = (((template.get('required_modifier_tier') or {}).get('allowed_tiers')) or [])
    if not allowed or any(not isinstance(t, int) or t < 1 for t in allowed):
        _fail('initial state allowed_tiers must contain positive integers')
    pattern = (initial_states.get('canonical_materialization_contract') or {}).get('fractured_crit_mod_id_pattern')
    if not isinstance(pattern, str) or '{tier}' not in pattern:
        _fail('initial state materialization pattern must contain {tier}')
    for tier in allowed:
        mod_id = pattern.format(tier=tier)
        mod = index.get(mod_id)
        if mod is None or mod.family_id != family or mod.side.value != template.get('required_side'):
            _fail(f'initial state tier {tier} does not resolve to required static modifier')

    if failure_policy is not None:
        rules = failure_policy.get('rules')
        if not isinstance(rules, list) or not rules:
            _fail('failure_consumption_matrix.rules must be a non-empty list')
        seen: set[tuple[Any, Any, Any]] = set()
        for i, row in enumerate(rules):
            if not isinstance(row, dict):
                _fail(f'failure policy rule {i} must be a mapping')
            key = (row.get('operation_group'), row.get('failure_stage'), row.get('failure_code'))
            if any(not isinstance(v, str) or not v for v in key):
                _fail(f'failure policy rule {i} requires operation_group, failure_stage and failure_code')
            if key in seen:
                _fail(f'duplicate failure policy rule: {key}')
            seen.add(key)
            consumed = row.get('consumed_resources')
            if not isinstance(consumed, list):
                _fail(f'failure policy rule {i} consumed_resources must be a list')
            if not isinstance(row.get('state_unchanged'), bool):
                _fail(f'failure policy rule {i} state_unchanged must be bool')
            if not isinstance(row.get('outcome_kind'), str) or not row.get('outcome_kind'):
                _fail(f'failure policy rule {i} outcome_kind is required')
