from pathlib import Path
import shutil, yaml
import pytest
from p2c_engine.static_data import build_static_game_data
from p2c_engine.domain.defects import StaticDataDefect
ROOT=Path(__file__).resolve().parents[2]

def clone(tmp_path):
    for d in ('data','config','schemas'): shutil.copytree(ROOT/d,tmp_path/d)

def mutate_yaml(path, fn):
    data=yaml.safe_load(path.read_text(encoding='utf-8')); fn(data); path.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True),encoding='utf-8')

def test_semantic_fingerprint_ignores_unordered_scope_list_reorder(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path).semantic_fingerprint
    p=tmp_path/'config/project_scope.yaml'
    mutate_yaml(p, lambda d: d.__setitem__('active_operation_groups', list(reversed(d['active_operation_groups']))))
    assert build_static_game_data(tmp_path).semantic_fingerprint==baseline

def test_reference_only_operation_reorder_does_not_change_active_projection(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path).semantic_fingerprint
    p=tmp_path/'data/operations.yaml'
    def change(d):
        active=[r for r in d['operations'] if r['active_in_current_simulation']]
        reference=[r for r in d['operations'] if not r['active_in_current_simulation']]
        d['operations']=active+list(reversed(reference))
    mutate_yaml(p, change)
    assert build_static_game_data(tmp_path).semantic_fingerprint==baseline

def test_semantic_change_changes_fingerprint(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path).semantic_fingerprint
    p=tmp_path/'config/success_criteria.yaml'
    mutate_yaml(p, lambda d: d['single_families'].__setitem__('critical_hit_chance','value_to_critical_damage_bonus'))
    assert build_static_game_data(tmp_path).semantic_fingerprint!=baseline

def test_missing_active_handler_declaration_fails(tmp_path):
    clone(tmp_path); p=tmp_path/'data/operations.yaml'
    mutate_yaml(p, lambda d: d['handler_declarations'].pop('exalted'))
    with pytest.raises(StaticDataDefect, match='handler declaration'):
        build_static_game_data(tmp_path)


def test_runtime_admission_status_table_is_explicit_and_narrow():
    data=yaml.safe_load((ROOT/'data/operations.yaml').read_text(encoding='utf-8'))
    rows=data['operations']
    assert len(rows) == 37
    assert all('runtime_admission_status' in row for row in rows)
    admitted=[
        row['operation_id']
        for row in rows
        if row['runtime_admission_status'] == 'accepted_executable_runtime'
    ]
    assert admitted == [
        'greater_exalted',
        'perfect_exalted',
        'annulment',
        'chaos',
        'greater_chaos',
        'perfect_chaos',
    ]


def test_missing_runtime_admission_status_fails(tmp_path):
    clone(tmp_path); p=tmp_path/'data/operations.yaml'
    def change(d):
        row=next(r for r in d['operations'] if r['operation_id']=='greater_chaos')
        row.pop('runtime_admission_status')
    mutate_yaml(p, change)
    with pytest.raises(StaticDataDefect, match='runtime_admission_status'):
        build_static_game_data(tmp_path)


def test_inactive_operation_cannot_be_executable_admitted(tmp_path):
    clone(tmp_path); p=tmp_path/'data/operations.yaml'
    def change(d):
        row=next(r for r in d['operations'] if r['operation_id']=='alchemy')
        row['runtime_admission_status']='accepted_executable_runtime'
    mutate_yaml(p, change)
    with pytest.raises(StaticDataDefect, match='executable-admitted'):
        build_static_game_data(tmp_path)

def test_invalid_group_ids_fail(tmp_path):
    clone(tmp_path); p=tmp_path/'data/mods_ordinary_quarterstaff.yaml'
    mutate_yaml(p, lambda d: d['modifiers'][0].__setitem__('group_ids',[]))
    with pytest.raises(StaticDataDefect, match='group_ids'):
        build_static_game_data(tmp_path)

def test_unknown_guaranteed_essence_output_fails(tmp_path):
    clone(tmp_path); p=tmp_path/'data/essence_outputs.yaml'
    mutate_yaml(p, lambda d: d['perfect'][0].__setitem__('guaranteed_mod_id','missing_output'))
    with pytest.raises(StaticDataDefect):
        build_static_game_data(tmp_path)

def test_reference_only_content_change_only_changes_source_fingerprint(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path)
    p=tmp_path/'data/operations.yaml'
    def change(d):
        row=next(r for r in d['operations'] if not r['active_in_current_simulation'])
        row['audit_note']='reference-only wording changed'
    mutate_yaml(p, change)
    changed=build_static_game_data(tmp_path)
    assert changed.source_fingerprint != baseline.source_fingerprint
    assert changed.semantic_fingerprint == baseline.semantic_fingerprint


def test_active_narrative_text_change_only_changes_source_fingerprint(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path)
    p=tmp_path/'data/operations.yaml'
    def change(d):
        row=next(r for r in d['operations'] if r['operation_id']=='reveal_desecrated')
        row['transition']['offers']['verification_basis'][0]='Reworded evidence only.'
    mutate_yaml(p, change)
    changed=build_static_game_data(tmp_path)
    assert changed.source_fingerprint != baseline.source_fingerprint
    assert changed.semantic_fingerprint == baseline.semantic_fingerprint


def test_utf8_yaml_round_trip_does_not_change_semantic_fingerprint(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path)
    p=tmp_path/'data/operations.yaml'
    data=yaml.safe_load(p.read_text(encoding='utf-8'))
    p.write_text(yaml.safe_dump(data,sort_keys=True,allow_unicode=True),encoding='utf-8')
    changed=build_static_game_data(tmp_path)
    assert changed.source_fingerprint != baseline.source_fingerprint
    assert changed.semantic_fingerprint == baseline.semantic_fingerprint


def test_active_catalog_candidate_mechanic_change_only_changes_source_fingerprint(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path)
    p=tmp_path/'data/operations.yaml'
    def change(d):
        row=next(r for r in d['operations'] if r['operation_id']=='exalted')
        row['transition']['add']['count']=2
    mutate_yaml(p, change)
    changed=build_static_game_data(tmp_path)
    assert changed.source_fingerprint != baseline.source_fingerprint
    assert changed.semantic_fingerprint == baseline.semantic_fingerprint


def test_accepted_runtime_mechanic_change_changes_semantic_fingerprint(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path).semantic_fingerprint
    p=tmp_path/'data/operations.yaml'
    def change(d):
        row=next(r for r in d['operations'] if r['operation_id']=='annulment')
        row['transition']['remove']['count']=2
    mutate_yaml(p, change)
    assert build_static_game_data(tmp_path).semantic_fingerprint != baseline


def test_perfect_essence_prevalidate_change_only_changes_source_fingerprint(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path)
    p=tmp_path/'data/operations.yaml'
    def change(d):
        row=next(r for r in d['operations'] if r['operation_id']=='perfect_essence_abrasion')
        row['transition']['prevalidate']=['crafted_capacity_free']
    mutate_yaml(p, change)
    changed=build_static_game_data(tmp_path)
    assert changed.source_fingerprint != baseline.source_fingerprint
    assert changed.semantic_fingerprint == baseline.semantic_fingerprint


def test_jawbone_prevalidate_change_only_changes_source_fingerprint(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path)
    p=tmp_path/'data/operations.yaml'
    def change(d):
        row=next(r for r in d['operations'] if r['operation_id']=='gnawed_jawbone')
        row['transition']['prevalidate']=['input_is_rare']
    mutate_yaml(p, change)
    changed=build_static_game_data(tmp_path)
    assert changed.source_fingerprint != baseline.source_fingerprint
    assert changed.semantic_fingerprint == baseline.semantic_fingerprint


def test_jawbone_legal_sides_change_only_changes_source_fingerprint(tmp_path):
    clone(tmp_path); baseline=build_static_game_data(tmp_path)
    p=tmp_path/'data/operations.yaml'
    def change(d):
        row=next(r for r in d['operations'] if r['operation_id']=='gnawed_jawbone')
        row['transition']['side_selection']['legal_sides']='free sides only'
    mutate_yaml(p, change)
    changed=build_static_game_data(tmp_path)
    assert changed.source_fingerprint != baseline.source_fingerprint
    assert changed.semantic_fingerprint == baseline.semantic_fingerprint
