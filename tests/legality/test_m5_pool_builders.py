from __future__ import annotations

from types import SimpleNamespace

import pytest

from p2c_engine.domain.candidate_pool import ordered_candidates, pool_digest
from p2c_engine.domain.defects import SamplingContractDefect, StaticDataDefect, UnknownModifierIdDefect
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import DesecratedPlaceholder, ItemState, ModifierInstance
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.legality.pool_builders import (
    OrdinaryAddPoolRequest,
    RemovalPoolRequest,
    RevealBasePoolRequest,
    apply_family_mml,
    build_ordinary_add_pool,
    build_removal_pool,
    build_reveal_base_pool,
)


def mod(
    mod_id: str,
    family_id: str,
    side: Side,
    *,
    tier: int = 1,
    level: int = 1,
    weight: int = 1,
    category: str = "ordinary",
    groups: tuple[str, ...] | None = None,
    tags: tuple[str, ...] = (),
    lich_tag: str | None = None,
) -> StaticModifier:
    return StaticModifier(
        mod_id=mod_id,
        family_id=family_id,
        side=side,
        group_ids=groups or (family_id,),
        tier=tier,
        modifier_level=level,
        tags=tags,
        generation_weight=weight,
        static_category=category,
        lich_tag=lich_tag,
    )


def static(*mods: StaticModifier):
    return SimpleNamespace(
        modifier_index={row.mod_id: row for row in sorted(mods, key=lambda row: row.mod_id)},
        project_scope={"active_item_class": "quarterstaff"},
    )


def state(
    mods: tuple[ModifierInstance, ...] = (),
    *,
    item_level: int = 82,
    rarity: Rarity = Rarity.RARE,
    placeholder: DesecratedPlaceholder | None = None,
) -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=rarity,
        item_level=item_level,
        modifiers=mods,
        unrevealed_desecrated=placeholder,
        augment_socket_capacity=1,
        augment_socket_used=0,
        astrid_installed=False,
    )


def ids(result):
    return tuple(candidate.key for candidate in result.candidates)


def base_static():
    return static(
        mod("prefix_low_t2", "prefix_family", Side.PREFIX, tier=2, level=10, weight=10, groups=("prefix_group",)),
        mod("prefix_high_t1", "prefix_family", Side.PREFIX, tier=1, level=70, weight=20, groups=("prefix_group",)),
        mod("suffix_low_t2", "suffix_family", Side.SUFFIX, tier=2, level=10, weight=30, groups=("suffix_group",)),
        mod("suffix_high_t1", "suffix_family", Side.SUFFIX, tier=1, level=70, weight=40, groups=("suffix_group",)),
        mod("blocked_group_t1", "blocked_group_family", Side.SUFFIX, tier=1, level=10, weight=50, groups=("shared_group",)),
        mod("zero_weight_t1", "zero_weight_family", Side.SUFFIX, tier=1, level=10, weight=0, groups=("zero_group",)),
        mod("crafted_essence_t1", "essence_family", Side.PREFIX, tier=1, level=1, weight=1, category="perfect_essence"),
        mod("desecrated_prefix_t1", "desecrated_prefix", Side.PREFIX, tier=1, level=65, weight=1, category="desecrated", groups=("desecrated_prefix",), tags=("amanamu",), lich_tag="amanamu"),
        mod("desecrated_suffix_t1", "desecrated_suffix", Side.SUFFIX, tier=1, level=65, weight=1, category="desecrated", groups=("desecrated_suffix",), tags=("kurgal",), lich_tag="kurgal"),
        mod("installed_prefix", "installed_prefix_family", Side.PREFIX, tier=1, level=1, weight=1, groups=("installed_prefix_group",)),
        mod("installed_suffix", "installed_suffix_family", Side.SUFFIX, tier=1, level=5, weight=1, groups=("shared_group",)),
        mod("installed_desecrated", "installed_desecrated_family", Side.SUFFIX, tier=1, level=5, weight=1, groups=("installed_desecrated_group",), category="desecrated"),
    )


def test_mml_threshold_fallback_absent_family_and_tie_defect():
    rows = (
        mod("a_t2", "a", Side.PREFIX, tier=2, level=10),
        mod("a_t1", "a", Side.PREFIX, tier=1, level=80),
        mod("b_t3", "b", Side.SUFFIX, tier=3, level=10),
        mod("b_t2", "b", Side.SUFFIX, tier=2, level=20),
    )

    kept, evidence, fallbacks = apply_family_mml(rows, 70)

    assert tuple(row.mod_id for row in kept) == ("a_t1", "b_t2")
    assert evidence.stage_id == "mml"
    assert tuple(f.family_id for f in fallbacks) == ("b",)
    assert fallbacks[0].retained_mod_id == "b_t2"

    kept_no_mml, evidence_no_mml, fallbacks_no_mml = apply_family_mml(rows, None)
    assert {row.mod_id for row in kept_no_mml} == {"a_t1", "a_t2", "b_t2", "b_t3"}
    assert evidence_no_mml.input_count == evidence_no_mml.output_count == 4
    assert fallbacks_no_mml == ()

    with pytest.raises(StaticDataDefect, match="Co-equal strongest"):
        apply_family_mml(
            (
                mod("tie_a", "tie", Side.PREFIX, tier=1, level=1),
                mod("tie_b", "tie", Side.PREFIX, tier=1, level=1),
            ),
            99,
        )


def test_ordinary_add_pool_filters_and_digest():
    s = base_static()
    item = state(
        (
            ModifierInstance("installed_prefix"),
            ModifierInstance("installed_suffix"),
        ),
        item_level=82,
    )

    result = build_ordinary_add_pool(
        OrdinaryAddPoolRequest("quarterstaff", item, side_filter=Side.SUFFIX, mml=70),
        s,
    )

    assert ids(result) == ("suffix_high_t1",)
    assert result.candidate_digest == pool_digest(result.candidates)
    assert result.empty_reason is None
    assert "blocked_group_t1" not in ids(result)
    assert "zero_weight_t1" not in ids(result)
    assert "crafted_essence_t1" not in ids(result)
    assert "desecrated_suffix_t1" not in ids(result)
    assert {stage.stage_id for stage in result.stages} >= {
        "category",
        "item_level",
        "side",
        "installed_family",
        "installed_groups",
        "mml",
        "positive_weight",
    }


def test_ordinary_add_pool_side_filter_none_keeps_mixed_single_free_sides():
    s = base_static()
    item = state(
        (
            ModifierInstance("installed_prefix"),
            ModifierInstance("installed_prefix", crafted=True),
            ModifierInstance("installed_suffix"),
            ModifierInstance("installed_suffix", crafted=True),
        ),
        item_level=82,
    )

    result = build_ordinary_add_pool(OrdinaryAddPoolRequest("quarterstaff", item), s)

    assert "prefix_low_t2" in ids(result)
    assert "suffix_low_t2" in ids(result)


def test_empty_result_has_no_candidate_digest_and_stable_fingerprint():
    s = base_static()
    item = state(
        (
            ModifierInstance("installed_prefix"),
            ModifierInstance("installed_prefix", crafted=True),
            ModifierInstance("prefix_low_t2"),
        )
    )

    request = OrdinaryAddPoolRequest("quarterstaff", item, side_filter=Side.PREFIX)
    left = build_ordinary_add_pool(request, s)
    right = build_ordinary_add_pool(request, s)

    assert left.candidates == ()
    assert left.candidate_digest is None
    assert left.empty_reason == "ordinary_pool_exhausted"
    assert left.result_fingerprint == right.result_fingerprint
    with pytest.raises(SamplingContractDefect):
        ordered_candidates(left.candidates)


def test_removal_pool_keys_ordinals_filters_and_lowest_level_selector():
    s = base_static()
    item = state(
        (
            ModifierInstance("installed_prefix"),
            ModifierInstance("installed_prefix"),
            ModifierInstance("installed_prefix", crafted=True),
            ModifierInstance("installed_suffix"),
            ModifierInstance("installed_desecrated", desecrated=True),
            ModifierInstance("suffix_low_t2", fractured=True),
        )
    )

    result = build_removal_pool(
        RemovalPoolRequest("quarterstaff", item, lowest_modifier_level=True),
        s,
    )

    assert ids(result) == (
        "rm:installed_prefix:c0:d0:f0:o0",
        "rm:installed_prefix:c0:d0:f0:o1",
        "rm:installed_prefix:c1:d0:f0:o0",
    )
    assert all(candidate.weight == 1 for candidate in result.candidates)
    assert all(":f1:" not in candidate.key for candidate in result.candidates)
    assert result.candidate_digest == pool_digest(result.candidates)
    assert tuple(meta.candidate_key for meta in result.removal_metadata) == ids(result)

    permuted = state(tuple(reversed(item.modifiers)))
    again = build_removal_pool(RemovalPoolRequest("quarterstaff", permuted, lowest_modifier_level=True), s)
    assert ids(again) == ids(result)
    assert again.result_fingerprint == result.result_fingerprint


def test_removal_pool_selectors_and_unknown_mod_defect():
    s = base_static()
    item = state(
        (
            ModifierInstance("installed_prefix"),
            ModifierInstance("installed_desecrated", desecrated=True),
        )
    )

    result = build_removal_pool(
        RemovalPoolRequest("quarterstaff", item, side_filter=Side.SUFFIX, desecrated_only=True),
        s,
    )

    assert ids(result) == ("rm:installed_desecrated:c0:d1:f0:o0",)

    with pytest.raises(UnknownModifierIdDefect):
        build_removal_pool(
            RemovalPoolRequest("quarterstaff", state((ModifierInstance("unknown_mod"),))),
            s,
        )


def test_reveal_base_pool_uses_ordinary_and_desecrated_union_without_extra_free_slot():
    s = base_static()
    item = state(
        (
            ModifierInstance("installed_prefix"),
            ModifierInstance("installed_prefix", crafted=True),
            ModifierInstance("installed_prefix", desecrated=True),
        ),
        item_level=82,
        placeholder=DesecratedPlaceholder(Side.PREFIX, "ancient_jawbone", 70, "amanamu"),
    )

    result = build_reveal_base_pool(RevealBasePoolRequest("quarterstaff", item), s)

    assert "prefix_high_t1" in ids(result)
    assert "desecrated_prefix_t1" in ids(result)
    assert "crafted_essence_t1" not in ids(result)
    assert "suffix_high_t1" not in ids(result)
    assert result.candidate_digest == pool_digest(result.candidates)
    assert any(stage.stage_id == "placeholder_capacity_consistency" for stage in result.stages)


def test_reveal_base_pool_requires_placeholder_and_blocks_installed_groups():
    s = base_static()

    with pytest.raises(StaticDataDefect, match="placeholder"):
        build_reveal_base_pool(RevealBasePoolRequest("quarterstaff", state()), s)

    item = state(
        (ModifierInstance("installed_suffix"),),
        item_level=82,
        placeholder=DesecratedPlaceholder(Side.SUFFIX, "preserved_jawbone", None, None),
    )
    result = build_reveal_base_pool(RevealBasePoolRequest("quarterstaff", item), s)

    assert "blocked_group_t1" not in ids(result)


def test_reveal_base_pool_blocks_selected_offer_family_and_groups():
    s = base_static()
    item = state(
        item_level=82,
        placeholder=DesecratedPlaceholder(Side.PREFIX, "ancient_jawbone", None, None),
    )

    family_result = build_reveal_base_pool(
        RevealBasePoolRequest(
            "quarterstaff",
            item,
            excluded_family_ids=("prefix_family",),
        ),
        s,
    )
    group_result = build_reveal_base_pool(
        RevealBasePoolRequest(
            "quarterstaff",
            item,
            excluded_group_ids=("desecrated_prefix",),
        ),
        s,
    )

    assert "prefix_low_t2" not in ids(family_result)
    assert "prefix_high_t1" not in ids(family_result)
    assert "desecrated_prefix_t1" in ids(family_result)
    assert "desecrated_prefix_t1" not in ids(group_result)
    assert any(stage.stage_id == "selected_offer_family" for stage in family_result.stages)
    assert any(stage.stage_id == "selected_offer_groups" for stage in group_result.stages)


def test_reveal_base_pool_required_tag_filters_lich_candidates_in_m5():
    s = base_static()
    item = state(
        item_level=82,
        placeholder=DesecratedPlaceholder(Side.PREFIX, "ancient_jawbone", None, "amanamu"),
    )

    result = build_reveal_base_pool(
        RevealBasePoolRequest("quarterstaff", item, required_tag="amanamu"),
        s,
    )

    assert ids(result) == ("desecrated_prefix_t1",)
    assert any(
        stage.stage_id == "required_tag"
        and any(param.name == "required_tag" and param.value == "amanamu" for param in stage.params)
        for stage in result.stages
    )


def test_result_fingerprint_changes_with_request_semantics():
    s = base_static()
    item = state(item_level=82)

    left = build_ordinary_add_pool(OrdinaryAddPoolRequest("quarterstaff", item, mml=None), s)
    right = build_ordinary_add_pool(OrdinaryAddPoolRequest("quarterstaff", item, mml=70), s)

    assert left.result_fingerprint != right.result_fingerprint
