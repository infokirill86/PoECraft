"""Claude cross-audit additions for Codex M5 test-gap closure."""
from pathlib import Path
import random

import pytest

from p2c_engine.static_data import build_static_game_data
from p2c_engine.domain.item_state import ItemState, ModifierInstance, DesecratedPlaceholder
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.domain.defects import SamplingContractDefect, StaticDataDefect
from p2c_engine.legality.pool_builders import (
    OrdinaryAddPoolRequest,
    RemovalPoolRequest,
    RevealBasePoolRequest,
    build_ordinary_add_pool,
    build_removal_pool,
    build_reveal_base_pool,
    apply_family_mml,
)

ROOT = Path(__file__).resolve().parents[2]
STATIC = build_static_game_data(ROOT)


def _state(mods, placeholder=None, rarity=Rarity.RARE, item_level=82):
    return ItemState("quarterstaff", rarity, item_level, tuple(mods), placeholder, 2, 0, False)


def test_removal_duplicate_ordinals_synthetic_and_permutation_independent():
    # Direct construction bypasses duplicate-family validation to exercise the ordinal path.
    dup = [ModifierInstance("value_increased_attack_speed_t1") for _ in range(3)]
    res = build_removal_pool(RemovalPoolRequest("quarterstaff", _state(dup)), STATIC)
    assert sorted(m.duplicate_ordinal for m in res.removal_metadata) == [0, 1, 2]
    assert all(c.weight == 1 for c in res.candidates)
    assert all(c.key.startswith("rm:") and c.key.endswith(("o0", "o1", "o2")) for c in res.candidates)
    shuffled = dup[:]
    random.Random(7).shuffle(shuffled)
    res2 = build_removal_pool(RemovalPoolRequest("quarterstaff", _state(shuffled)), STATIC)
    assert tuple(c.key for c in res.candidates) == tuple(c.key for c in res2.candidates)
    assert res.result_fingerprint == res2.result_fingerprint


def test_flag_variants_form_distinct_identity_groups():
    mods = [
        ModifierInstance("value_increased_attack_speed_t1", crafted=False),
        ModifierInstance("value_increased_attack_speed_t1", crafted=True),
    ]
    res = build_removal_pool(RemovalPoolRequest("quarterstaff", _state(mods)), STATIC)
    keys = {c.key for c in res.candidates}
    assert "rm:value_increased_attack_speed_t1:c0:d0:f0:o0" in keys
    assert "rm:value_increased_attack_speed_t1:c1:d0:f0:o0" in keys


def test_mml_fallback_cannot_resurrect_item_level_ineligible_row():
    # Two-tier synthetic family; strongest tier is item-level-ineligible; only weaker tier is eligible.
    fam = (
        StaticModifier("z_t1", "famZ", Side.PREFIX, ("gZ",), 1, 80, (), 100, "ordinary"),
        StaticModifier("z_t2", "famZ", Side.PREFIX, ("gZ",), 2, 30, (), 100, "ordinary"),
    )
    eligible = tuple(m for m in fam if m.modifier_level <= 40)
    kept, _ev, fb = apply_family_mml(eligible, 80)
    assert tuple(m.mod_id for m in kept) == ("z_t2",)
    assert fb[0].retained_mod_id == "z_t2"


def test_pure_cross_family_group_block_synthetic():
    groups = {"shared_group"}
    a = StaticModifier("a1", "famA", Side.PREFIX, ("shared_group",), 1, 1, (), 100, "ordinary")
    b = StaticModifier("b1", "famB", Side.PREFIX, ("other",), 1, 1, (), 100, "ordinary")
    assert not groups.isdisjoint(a.group_ids)
    assert groups.isdisjoint(b.group_ids)


def test_reveal_non_empty_when_side_full_including_placeholder():
    ph = DesecratedPlaceholder(Side.SUFFIX, "gnawed_jawbone", None, None)
    item_state = _state(
        [
            ModifierInstance("value_increased_attack_speed_t1"),
            ModifierInstance("value_to_critical_damage_bonus_t1"),
        ],
        placeholder=ph,
    )
    res = build_reveal_base_pool(RevealBasePoolRequest("quarterstaff", item_state), STATIC)
    cats = {STATIC.modifier_index[c.key].static_category for c in res.candidates}
    assert res.candidates and {"ordinary", "desecrated"} <= cats
    assert not any(c.key.startswith("crafted_") for c in res.candidates)


def test_bool_request_fields_rejected():
    item_state = _state([])
    with pytest.raises((SamplingContractDefect, StaticDataDefect)):
        build_ordinary_add_pool(OrdinaryAddPoolRequest("quarterstaff", item_state, mml=True), STATIC)
    with pytest.raises((SamplingContractDefect, StaticDataDefect)):
        build_removal_pool(RemovalPoolRequest("quarterstaff", item_state, exact_modifier_level=True), STATIC)
    with pytest.raises((SamplingContractDefect, StaticDataDefect)):
        build_removal_pool(RemovalPoolRequest("quarterstaff", item_state, minimum_modifier_level=True), STATIC)
    placeholder = DesecratedPlaceholder(Side.SUFFIX, "gnawed_jawbone", True, None)
    with pytest.raises((SamplingContractDefect, StaticDataDefect)):
        build_reveal_base_pool(
            RevealBasePoolRequest("quarterstaff", _state([], placeholder=placeholder)), STATIC
        )
