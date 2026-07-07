from pathlib import Path
import shutil, yaml
import pytest
from p2c_engine.static_data import build_static_game_data
from p2c_engine.domain.defects import StaticDataDefect

ROOT=Path(__file__).resolve().parents[2]

def test_index_and_aliases_and_essence_tiers():
    s=build_static_game_data(ROOT)
    assert len(s.modifier_index)==188
    assert all(isinstance(m.tags,tuple) for m in s.modifier_index.values())
    assert all(m.tier==1 for m in s.modifier_index.values() if m.static_category.endswith('_essence'))
    assert {'amanamu','kurgal','ulaman'} <= {m.lich_tag for m in s.modifier_index.values() if m.static_category=='desecrated'}

def test_semantic_fingerprint_stable():
    assert build_static_game_data(ROOT).semantic_fingerprint==build_static_game_data(ROOT).semantic_fingerprint

def test_manifest_not_directory_scan():
    from p2c_engine.static_data.manifest import DEFAULT_MANIFEST
    assert all(isinstance(p,str) for p in DEFAULT_MANIFEST.ordered_paths())
    assert len(DEFAULT_MANIFEST.ordered_paths())==12

def test_non_integer_active_weight_fails(tmp_path):
    for d in ('data','config','schemas'): shutil.copytree(ROOT/d,tmp_path/d)
    p=tmp_path/'data/mods_ordinary_quarterstaff.yaml'; data=yaml.safe_load(p.read_text())
    data['modifiers'][0]['generation_weight']=1.5; p.write_text(yaml.safe_dump(data,sort_keys=False))
    with pytest.raises(ValueError): build_static_game_data(tmp_path)

def test_superseded_lich_tagged_first_fill_effect_is_rejected(tmp_path):
    for d in ('data','config','schemas'): shutil.copytree(ROOT/d,tmp_path/d)
    p=tmp_path/'data/omens.yaml'; data=yaml.safe_load(p.read_text())
    liege=next(row for row in data['omens'] if row['omen_id']=='liege')
    liege['effect']={'tagged_first_fill': {'tag': 'amanamu'}}
    p.write_text(yaml.safe_dump(data,sort_keys=False))
    with pytest.raises(StaticDataDefect, match='tagged_first_fill'):
        build_static_game_data(tmp_path)
