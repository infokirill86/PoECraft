from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from p2c_engine.canonical import normalize_primitive
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.domain.defects import StaticDataDefect
from .manifest import DEFAULT_MANIFEST, DataManifest
from .loaders import load_yaml, validate_schema
from .normalize import normalize_modifier
from .modifier_index import build_modifier_index
from .fingerprints import semantic_fingerprint, source_fingerprint
from .immutable import deep_freeze
from .checks import validate_cross_file_contracts
from .semantic import (normalize_scope, normalize_success, normalize_operations, normalize_omens, normalize_initial_states, normalize_family_registry, normalize_failure_policy)

@dataclass(frozen=True, slots=True)
class StaticGameData:
    modifier_index: Mapping[str, StaticModifier]
    operations: Mapping[str, Any]
    omens: Mapping[str, Any]
    family_registry: Mapping[str, Any]
    initial_states: Mapping[str, Any]
    project_scope: Mapping[str, Any]
    success_criteria: Mapping[str, Any]
    failure_policy: Mapping[str, Any]
    item_state_schema: Mapping[str, Any]
    static_modifier_schema: Mapping[str, Any]
    source_fingerprint: str
    semantic_fingerprint: str
    root: Path


def _schema_gate(row: dict[str, Any], schema: dict[str, Any], source: str) -> None:
    errors = validate_schema(row, schema)
    if errors:
        raise StaticDataDefect(f"Schema validation failed for {source}: {'; '.join(errors)}")



def _sort_registry(data: dict[str, Any], key: str, id_key: str) -> dict[str, Any]:
    result = dict(data)
    rows = result.get(key)
    if isinstance(rows, list):
        result[key] = sorted(rows, key=lambda row: row.get(id_key, '') if isinstance(row, dict) else '')
    return result


def build_static_game_data(root: Path, manifest: DataManifest = DEFAULT_MANIFEST) -> StaticGameData:
    ordinary = load_yaml(root, manifest.ordinary_mods)
    desecrated = load_yaml(root, manifest.desecrated_mods)
    essence = load_yaml(root, manifest.essence_outputs)
    operations = load_yaml(root, manifest.operations)
    omens = load_yaml(root, manifest.omens)
    families = load_yaml(root, manifest.family_registry)
    initial_states = load_yaml(root, manifest.initial_states)
    scope = load_yaml(root, manifest.project_scope)
    success = load_yaml(root, manifest.success_criteria)
    failure_policy = load_yaml(root, manifest.failure_consumption_matrix)
    item_state_schema = load_yaml(root, manifest.item_state_schema)
    static_modifier_schema = load_yaml(root, manifest.static_modifier_schema)

    records=[]
    for source, category, rows in (
        (manifest.ordinary_mods, 'ordinary', ordinary.get('modifiers', [])),
        (manifest.desecrated_mods, 'desecrated', desecrated.get('modifiers', [])),
    ):
        for i, row in enumerate(rows):
            _schema_gate(row, static_modifier_schema, f'{source}#modifiers[{i}]')
            records.append(normalize_modifier(row, category))
    for grade in ('greater','perfect'):
        for i, row in enumerate(essence.get(grade, [])):
            mapped = dict(row)
            mapped['mod_id'] = row.get('guaranteed_mod_id')
            mapped.setdefault('generation_weight', 1)
            _schema_gate(mapped, static_modifier_schema, f'{manifest.essence_outputs}#{grade}[{i}]')
            records.append(normalize_modifier(mapped, f'{grade}_essence', forced_tier=1))

    index=build_modifier_index(records)
    if len(index) != 188:
        raise StaticDataDefect(f'Expected 188 static modifiers for v7.1, got {len(index)}')

    validate_cross_file_contracts(index=index, essence=essence, operations=operations, omens=omens,
        family_registry=families, initial_states=initial_states, scope=scope, success=success,
        failure_policy=failure_policy)

    active_groups=set(scope.get('active_operation_groups') or [])
    semantic_payload={
        'modifiers': [normalize_primitive(v) for _,v in sorted(index.items())],
        'operations': normalize_operations(operations, active_groups),
        'omens': normalize_omens(omens, active_groups),
        'family_registry': normalize_family_registry(families),
        'initial_states': normalize_initial_states(initial_states),
        'project_scope': normalize_scope(scope),
        'success_criteria': normalize_success(success),
        'failure_policy': normalize_failure_policy(failure_policy),
        'item_state_schema': item_state_schema,
        'static_modifier_schema': static_modifier_schema,
    }
    return StaticGameData(
        modifier_index=index,
        operations=deep_freeze(operations), omens=deep_freeze(omens),
        family_registry=deep_freeze(families), initial_states=deep_freeze(initial_states),
        project_scope=deep_freeze(scope), success_criteria=deep_freeze(success),
        failure_policy=deep_freeze(failure_policy),
        item_state_schema=deep_freeze(item_state_schema), static_modifier_schema=deep_freeze(static_modifier_schema),
        source_fingerprint=source_fingerprint(root, manifest.ordered_paths()),
        semantic_fingerprint=semantic_fingerprint(semantic_payload), root=root,
    )
