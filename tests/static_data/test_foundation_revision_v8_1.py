from pathlib import Path
import shutil
import yaml
import pytest
from p2c_engine.static_data import build_static_game_data
from p2c_engine.domain.defects import StaticDataDefect

ROOT=Path(__file__).resolve().parents[2]

def clone(tmp_path):
    for d in ('data','config','schemas'):
        shutil.copytree(ROOT/d,tmp_path/d)

def test_static_data_is_deeply_frozen():
    s=build_static_game_data(ROOT)
    with pytest.raises(TypeError): s.operations['operations'][0]['group']='broken'
    with pytest.raises(TypeError): s.initial_states['active_start_policy']['primary']='broken'

def test_production_loader_rejects_schema_invalid_modifier(tmp_path):
    clone(tmp_path)
    p=tmp_path/'data/mods_ordinary_quarterstaff.yaml'
    data=yaml.safe_load(p.read_text())
    del data['modifiers'][0]['side']
    p.write_text(yaml.safe_dump(data,sort_keys=False))
    with pytest.raises(StaticDataDefect, match='Schema validation failed'):
        build_static_game_data(tmp_path)

def test_startup_rejects_unknown_success_family(tmp_path):
    clone(tmp_path)
    p=tmp_path/'config/success_criteria.yaml'
    data=yaml.safe_load(p.read_text())
    data['single_families']['critical_hit_chance']='missing_family'
    p.write_text(yaml.safe_dump(data,sort_keys=False))
    with pytest.raises(StaticDataDefect, match='unknown family'):
        build_static_game_data(tmp_path)

def test_startup_rejects_scope_contradiction(tmp_path):
    clone(tmp_path)
    p=tmp_path/'config/project_scope.yaml'
    data=yaml.safe_load(p.read_text())
    data['reference_only_operation_groups'].append('exalted')
    p.write_text(yaml.safe_dump(data,sort_keys=False))
    with pytest.raises(StaticDataDefect, match='both active and reference-only'):
        build_static_game_data(tmp_path)

def test_semantic_fingerprint_ignores_modifier_row_order_and_formatting(tmp_path):
    clone(tmp_path)
    baseline=build_static_game_data(tmp_path)
    p=tmp_path/'data/mods_ordinary_quarterstaff.yaml'
    data=yaml.safe_load(p.read_text())
    data['modifiers'].reverse()
    p.write_text(yaml.safe_dump(data,sort_keys=True),encoding='utf-8')
    changed=build_static_game_data(tmp_path)
    assert changed.source_fingerprint != baseline.source_fingerprint
    assert changed.semantic_fingerprint == baseline.semantic_fingerprint

def test_semantic_fingerprint_changes_on_runtime_semantic_change(tmp_path):
    clone(tmp_path)
    baseline=build_static_game_data(tmp_path)
    p=tmp_path/'config/initial_states.yaml'
    data=yaml.safe_load(p.read_text())
    data['active_start_policy']['economic_fields_pending'].append('semantic_test_field')
    p.write_text(yaml.safe_dump(data,sort_keys=False))
    assert build_static_game_data(tmp_path).semantic_fingerprint != baseline.semantic_fingerprint
