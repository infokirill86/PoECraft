from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable, TypeVar

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.canonical.normalize import normalize_primitive
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.candidate_pool import ordered_candidates, pool_digest
from p2c_engine.domain.defects import SamplingContractDefect, StaticDataDefect, UnknownModifierIdDefect
from p2c_engine.domain.enums import Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.pool_building import (
    EvidenceParam,
    MmlFallbackEvidence,
    PoolBuildResult,
    PoolStageEvidence,
    ReasonExclusion,
    RemovalInstanceMetadata,
)
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.static_data.game_data import StaticGameData

M5_RESULT_FINGERPRINT_VERSION = 1


@dataclass(frozen=True, slots=True)
class OrdinaryAddPoolRequest:
    item_class: str
    state: ItemState
    side_filter: Side | None = None
    mml: int | None = None


@dataclass(frozen=True, slots=True)
class RemovalPoolRequest:
    item_class: str
    state: ItemState
    side_filter: Side | None = None
    desecrated_only: bool = False
    crafted_only: bool = False
    exact_modifier_level: int | None = None
    minimum_modifier_level: int | None = None
    lowest_modifier_level: bool = False


@dataclass(frozen=True, slots=True)
class RevealBasePoolRequest:
    item_class: str
    state: ItemState
    placeholder_side: Side | None = None
    reveal_mml: int | None = None
    required_tag: str | None = None
    excluded_family_ids: tuple[str, ...] = ()
    excluded_group_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class _RemovalRow:
    key: str
    instance: ModifierInstance
    static: StaticModifier
    duplicate_ordinal: int


T = TypeVar("T")


def build_ordinary_add_pool(request: OrdinaryAddPoolRequest, static: StaticGameData) -> PoolBuildResult:
    _assert_request_item_class(request.item_class, static)
    _assert_known_installed_mods(request.state, static)
    _require_int_or_none("mml", request.mml)

    rows: tuple[StaticModifier, ...] = tuple(static.modifier_index.values())
    stages: list[PoolStageEvidence] = []

    rows, evidence = _filter_static(
        rows,
        "item_class",
        "category_mismatch",
        lambda mod: request.item_class == _active_item_class(static),
        params=(EvidenceParam("item_class", request.item_class),),
    )
    stages.append(evidence)

    rows, evidence = _filter_static(
        rows,
        "category",
        "category_mismatch",
        lambda mod: mod.static_category == "ordinary",
        params=(EvidenceParam("static_category", "ordinary"),),
    )
    stages.append(evidence)

    rows, evidence = _filter_static(
        rows,
        "item_level",
        "item_level_too_high",
        lambda mod: mod.modifier_level <= request.state.item_level,
        params=(EvidenceParam("item_level", request.state.item_level),),
    )
    stages.append(evidence)

    if request.side_filter is not None:
        rows, evidence = _filter_static(
            rows,
            "side",
            "side_mismatch",
            lambda mod: mod.side == request.side_filter,
            params=(EvidenceParam("side_filter", request.side_filter.value),),
        )
        stages.append(evidence)
    else:
        stages.append(
            _stage(
                "side",
                len(rows),
                len(rows),
                (),
                (EvidenceParam("side_filter", None),),
            )
        )

    free_by_side = _free_slots_by_side(request.state, static)
    rows, evidence = _filter_static(
        rows,
        "current_side_capacity",
        "side_capacity_full",
        lambda mod: free_by_side[mod.side.value] > 0,
        params=tuple(EvidenceParam(side, free_by_side[side]) for side in sorted(free_by_side)),
    )
    stages.append(evidence)

    installed_families, installed_groups = _installed_blocker_sets(request.state, static)
    rows, evidence = _filter_static(
        rows,
        "installed_family",
        "installed_family_blocked",
        lambda mod: mod.family_id not in installed_families,
        params=(EvidenceParam("installed_family_ids", tuple(sorted(installed_families))),),
    )
    stages.append(evidence)

    rows, evidence = _filter_static(
        rows,
        "installed_groups",
        "installed_group_intersection",
        lambda mod: installed_groups.isdisjoint(mod.group_ids),
        params=(EvidenceParam("installed_group_ids", tuple(sorted(installed_groups))),),
    )
    stages.append(evidence)

    rows, evidence, fallbacks = apply_family_mml(rows, request.mml)
    stages.append(evidence)

    rows, evidence = _filter_static(
        rows,
        "positive_weight",
        "non_positive_weight",
        lambda mod: _positive_int(mod.generation_weight),
    )
    stages.append(evidence)

    candidates = tuple(Candidate(mod.mod_id, mod.generation_weight) for mod in rows)
    return _build_result(
        builder_kind="ordinary_add_pool",
        request_payload=_ordinary_request_payload(request),
        candidates=candidates,
        stages=tuple(stages),
        mml_fallbacks=fallbacks,
        empty_reason="ordinary_pool_exhausted" if not candidates else None,
    )


def build_removal_pool(request: RemovalPoolRequest, static: StaticGameData) -> PoolBuildResult:
    _assert_request_item_class(request.item_class, static)
    _assert_known_installed_mods(request.state, static)
    _require_int_or_none("exact_modifier_level", request.exact_modifier_level)
    _require_int_or_none("minimum_modifier_level", request.minimum_modifier_level)

    rows: tuple[_RemovalRow, ...] = _canonical_removal_rows(request.state, static)
    stages: list[PoolStageEvidence] = []

    rows, evidence = _filter_removal(
        rows,
        "fractured",
        "fractured_excluded",
        lambda row: not row.instance.fractured,
    )
    stages.append(evidence)

    if request.side_filter is not None:
        rows, evidence = _filter_removal(
            rows,
            "side",
            "side_mismatch",
            lambda row: row.static.side == request.side_filter,
            params=(EvidenceParam("side_filter", request.side_filter.value),),
        )
        stages.append(evidence)
    else:
        stages.append(
            _stage(
                "side",
                len(rows),
                len(rows),
                (),
                (EvidenceParam("side_filter", None),),
            )
        )

    if request.desecrated_only:
        rows, evidence = _filter_removal(
            rows,
            "desecrated_only",
            "selector_mismatch",
            lambda row: row.instance.desecrated,
            params=(EvidenceParam("desecrated_only", True),),
        )
        stages.append(evidence)
    else:
        stages.append(
            _stage(
                "desecrated_only",
                len(rows),
                len(rows),
                (),
                (EvidenceParam("desecrated_only", False),),
            )
        )

    if request.crafted_only:
        rows, evidence = _filter_removal(
            rows,
            "crafted_only",
            "selector_mismatch",
            lambda row: row.instance.crafted,
            params=(EvidenceParam("crafted_only", True),),
        )
        stages.append(evidence)
    else:
        stages.append(
            _stage(
                "crafted_only",
                len(rows),
                len(rows),
                (),
                (EvidenceParam("crafted_only", False),),
            )
        )

    if request.exact_modifier_level is not None:
        rows, evidence = _filter_removal(
            rows,
            "exact_modifier_level",
            "selector_mismatch",
            lambda row: row.static.modifier_level == request.exact_modifier_level,
            params=(EvidenceParam("exact_modifier_level", request.exact_modifier_level),),
        )
        stages.append(evidence)
    else:
        stages.append(
            _stage(
                "exact_modifier_level",
                len(rows),
                len(rows),
                (),
                (EvidenceParam("exact_modifier_level", None),),
            )
        )

    if request.minimum_modifier_level is not None:
        rows, evidence = _filter_removal(
            rows,
            "minimum_modifier_level",
            "selector_mismatch",
            lambda row: row.static.modifier_level >= request.minimum_modifier_level,
            params=(EvidenceParam("minimum_modifier_level", request.minimum_modifier_level),),
        )
        stages.append(evidence)
    else:
        stages.append(
            _stage(
                "minimum_modifier_level",
                len(rows),
                len(rows),
                (),
                (EvidenceParam("minimum_modifier_level", None),),
            )
        )

    if request.lowest_modifier_level and rows:
        lowest = min(row.static.modifier_level for row in rows)
        rows, evidence = _filter_removal(
            rows,
            "lowest_modifier_level",
            "selector_mismatch",
            lambda row: row.static.modifier_level == lowest,
            params=(EvidenceParam("lowest_modifier_level", lowest),),
        )
        stages.append(evidence)
    else:
        stages.append(
            _stage(
                "lowest_modifier_level",
                len(rows),
                len(rows),
                (),
                (EvidenceParam("lowest_modifier_level", request.lowest_modifier_level),),
            )
        )

    candidates = tuple(Candidate(row.key, 1) for row in rows)
    metadata = tuple(
        RemovalInstanceMetadata(
            candidate_key=row.key,
            mod_id=row.instance.mod_id,
            crafted=row.instance.crafted,
            desecrated=row.instance.desecrated,
            fractured=row.instance.fractured,
            duplicate_ordinal=row.duplicate_ordinal,
            modifier_level=row.static.modifier_level,
            side=row.static.side.value,
        )
        for row in rows
    )
    return _build_result(
        builder_kind="removal_pool",
        request_payload=_removal_request_payload(request),
        candidates=candidates,
        stages=tuple(stages),
        removal_metadata=metadata,
        empty_reason="removal_pool_exhausted" if not candidates else None,
    )


def build_reveal_base_pool(request: RevealBasePoolRequest, static: StaticGameData) -> PoolBuildResult:
    _assert_request_item_class(request.item_class, static)
    _assert_known_installed_mods(request.state, static)
    _require_str_or_none("required_tag", request.required_tag)
    _require_string_tuple("excluded_family_ids", request.excluded_family_ids)
    _require_string_tuple("excluded_group_ids", request.excluded_group_ids)

    placeholder = request.state.unrevealed_desecrated
    if placeholder is None:
        raise StaticDataDefect("Reveal base pool requires an unrevealed Desecrated placeholder")
    placeholder_side = request.placeholder_side or placeholder.side
    if placeholder_side != placeholder.side:
        raise StaticDataDefect("Reveal placeholder side contradicts ItemState placeholder")
    reveal_mml = placeholder.reveal_mml if request.reveal_mml is None else request.reveal_mml
    _require_int_or_none("reveal_mml", reveal_mml)

    rows: tuple[StaticModifier, ...] = tuple(static.modifier_index.values())
    stages: list[PoolStageEvidence] = []

    rows, evidence = _filter_static(
        rows,
        "item_class",
        "category_mismatch",
        lambda mod: request.item_class == _active_item_class(static),
        params=(EvidenceParam("item_class", request.item_class),),
    )
    stages.append(evidence)

    rows, evidence = _filter_static(
        rows,
        "source_category",
        "category_mismatch",
        lambda mod: mod.static_category in {"ordinary", "desecrated"},
        params=(EvidenceParam("source_categories", ("desecrated", "ordinary")),),
    )
    stages.append(evidence)

    rows, evidence = _filter_static(
        rows,
        "item_level",
        "item_level_too_high",
        lambda mod: mod.modifier_level <= request.state.item_level,
        params=(EvidenceParam("item_level", request.state.item_level),),
    )
    stages.append(evidence)

    rows, evidence = _filter_static(
        rows,
        "placeholder_side",
        "side_mismatch",
        lambda mod: mod.side == placeholder_side,
        params=(EvidenceParam("placeholder_side", placeholder_side.value),),
    )
    stages.append(evidence)

    stages.append(
        _stage(
            "placeholder_capacity_consistency",
            len(rows),
            len(rows),
            (),
            (
                EvidenceParam("placeholder_side", placeholder_side.value),
                EvidenceParam("requires_additional_free_slot", False),
            ),
        )
    )

    installed_families, installed_groups = _installed_blocker_sets(request.state, static)
    rows, evidence = _filter_static(
        rows,
        "installed_family",
        "installed_family_blocked",
        lambda mod: mod.family_id not in installed_families,
        params=(EvidenceParam("installed_family_ids", tuple(sorted(installed_families))),),
    )
    stages.append(evidence)

    rows, evidence = _filter_static(
        rows,
        "installed_groups",
        "installed_group_intersection",
        lambda mod: installed_groups.isdisjoint(mod.group_ids),
        params=(EvidenceParam("installed_group_ids", tuple(sorted(installed_groups))),),
    )
    stages.append(evidence)

    excluded_family_ids = set(request.excluded_family_ids)
    rows, evidence = _filter_static(
        rows,
        "selected_offer_family",
        "selected_offer_family_blocked",
        lambda mod: mod.family_id not in excluded_family_ids,
        params=(EvidenceParam("excluded_family_ids", tuple(sorted(excluded_family_ids))),),
    )
    stages.append(evidence)

    excluded_group_ids = set(request.excluded_group_ids)
    rows, evidence = _filter_static(
        rows,
        "selected_offer_groups",
        "selected_offer_group_intersection",
        lambda mod: excluded_group_ids.isdisjoint(mod.group_ids),
        params=(EvidenceParam("excluded_group_ids", tuple(sorted(excluded_group_ids))),),
    )
    stages.append(evidence)

    rows, evidence, fallbacks = apply_family_mml(rows, reveal_mml)
    stages.append(evidence)

    if request.required_tag is not None:
        rows, evidence = _filter_static(
            rows,
            "required_tag",
            "required_tag_mismatch",
            lambda mod: mod.lich_tag == request.required_tag,
            params=(EvidenceParam("required_tag", request.required_tag),),
        )
        stages.append(evidence)
    else:
        stages.append(
            _stage(
                "required_tag",
                len(rows),
                len(rows),
                (),
                (EvidenceParam("required_tag", None),),
            )
        )

    rows, evidence = _filter_static(
        rows,
        "positive_weight",
        "non_positive_weight",
        lambda mod: _positive_int(mod.generation_weight),
    )
    stages.append(evidence)

    stages.append(
        _stage(
            "tag_partition_metadata",
            len(rows),
            len(rows),
            (),
            (EvidenceParam("affects_candidate_digest", False),),
        )
    )

    candidates = tuple(Candidate(mod.mod_id, mod.generation_weight) for mod in rows)
    return _build_result(
        builder_kind="reveal_base_pool",
        request_payload=_reveal_request_payload(request, placeholder_side, reveal_mml),
        candidates=candidates,
        stages=tuple(stages),
        mml_fallbacks=fallbacks,
        empty_reason="reveal_base_pool_exhausted" if not candidates else None,
    )


def apply_family_mml(
    rows: Iterable[StaticModifier], mml: int | None
) -> tuple[tuple[StaticModifier, ...], PoolStageEvidence, tuple[MmlFallbackEvidence, ...]]:
    source = tuple(rows)
    if mml is None:
        return (
            source,
            _stage("mml", len(source), len(source), (), (EvidenceParam("mml", None),)),
            (),
        )

    kept: list[StaticModifier] = []
    excluded: list[str] = []
    fallbacks: list[MmlFallbackEvidence] = []
    by_family: dict[str, list[StaticModifier]] = defaultdict(list)
    for row in source:
        by_family[row.family_id].append(row)

    for family_id in sorted(by_family):
        family_rows = sorted(by_family[family_id], key=_static_sort_key)
        qualifying = [row for row in family_rows if row.modifier_level >= mml]
        if qualifying:
            kept.extend(qualifying)
            excluded.extend(row.mod_id for row in family_rows if row.modifier_level < mml)
            continue

        strongest_tier = min(row.tier for row in family_rows)
        strongest = [row for row in family_rows if row.tier == strongest_tier]
        if len({row.mod_id for row in strongest}) != 1:
            raise StaticDataDefect(
                f"Co-equal strongest rows in family {family_id}: {sorted(row.mod_id for row in strongest)}"
            )
        retained = strongest[0]
        kept.append(retained)
        excluded.extend(row.mod_id for row in family_rows if row.mod_id != retained.mod_id)
        fallbacks.append(
            MmlFallbackEvidence(
                family_id=family_id,
                threshold=mml,
                retained_mod_id=retained.mod_id,
                strongest_tier=strongest_tier,
            )
        )

    kept_tuple = tuple(sorted(kept, key=_static_sort_key))
    return (
        kept_tuple,
        _stage(
            "mml",
            len(source),
            len(kept_tuple),
            (ReasonExclusion("mml_below_threshold", tuple(sorted(excluded))),) if excluded else (),
            (EvidenceParam("mml", mml),),
        ),
        tuple(sorted(fallbacks, key=lambda row: (row.family_id, row.retained_mod_id))),
    )


def _filter_static(
    rows: tuple[StaticModifier, ...],
    stage_id: str,
    reason_id: str,
    keep: Callable[[StaticModifier], bool],
    params: tuple[EvidenceParam, ...] = (),
) -> tuple[tuple[StaticModifier, ...], PoolStageEvidence]:
    kept: list[StaticModifier] = []
    excluded: list[str] = []
    for row in rows:
        if keep(row):
            kept.append(row)
        else:
            excluded.append(row.mod_id)
    kept_tuple = tuple(sorted(kept, key=_static_sort_key))
    return kept_tuple, _stage(
        stage_id,
        len(rows),
        len(kept_tuple),
        (ReasonExclusion(reason_id, tuple(sorted(excluded))),) if excluded else (),
        params,
    )


def _filter_removal(
    rows: tuple[_RemovalRow, ...],
    stage_id: str,
    reason_id: str,
    keep: Callable[[_RemovalRow], bool],
    params: tuple[EvidenceParam, ...] = (),
) -> tuple[tuple[_RemovalRow, ...], PoolStageEvidence]:
    kept: list[_RemovalRow] = []
    excluded: list[str] = []
    for row in rows:
        if keep(row):
            kept.append(row)
        else:
            excluded.append(row.key)
    kept_tuple = tuple(sorted(kept, key=lambda row: row.key.encode("ascii")))
    return kept_tuple, _stage(
        stage_id,
        len(rows),
        len(kept_tuple),
        (ReasonExclusion(reason_id, tuple(sorted(excluded))),) if excluded else (),
        params,
    )


def _stage(
    stage_id: str,
    input_count: int,
    output_count: int,
    excluded: tuple[ReasonExclusion, ...],
    params: tuple[EvidenceParam, ...] = (),
) -> PoolStageEvidence:
    return PoolStageEvidence(
        stage_id=stage_id,
        input_count=input_count,
        output_count=output_count,
        excluded=tuple(sorted(excluded, key=lambda item: item.reason_id)),
        params=tuple(sorted(params, key=lambda item: item.name)),
    )


def _build_result(
    *,
    builder_kind: str,
    request_payload: dict[str, object],
    candidates: tuple[Candidate, ...],
    stages: tuple[PoolStageEvidence, ...],
    mml_fallbacks: tuple[MmlFallbackEvidence, ...] = (),
    removal_metadata: tuple[RemovalInstanceMetadata, ...] = (),
    empty_reason: str | None = None,
) -> PoolBuildResult:
    if candidates:
        ordered = ordered_candidates(candidates)
        digest: str | None = pool_digest(ordered)
        if empty_reason is not None:
            raise StaticDataDefect("empty_reason must be None for non-empty PoolBuildResult")
    else:
        ordered = ()
        digest = None
        if empty_reason is None:
            raise StaticDataDefect("empty PoolBuildResult requires an empty_reason")

    result_without_fingerprint = {
        "builder_kind": builder_kind,
        "request": request_payload,
        "candidates": normalize_primitive(ordered),
        "candidate_digest": digest,
        "empty_reason": empty_reason,
        "stages": normalize_primitive(stages),
        "mml_fallbacks": normalize_primitive(mml_fallbacks),
        "removal_metadata": normalize_primitive(removal_metadata),
    }
    fingerprint = sha256_canonical(
        result_without_fingerprint, schema_version=M5_RESULT_FINGERPRINT_VERSION
    )
    return PoolBuildResult(
        candidates=ordered,
        candidate_digest=digest,
        result_fingerprint=fingerprint,
        stages=stages,
        mml_fallbacks=mml_fallbacks,
        removal_metadata=removal_metadata,
        empty_reason=empty_reason,
    )


def _active_item_class(static: StaticGameData) -> str:
    return str(static.project_scope.get("active_item_class", "quarterstaff"))


def _assert_request_item_class(item_class: str, static: StaticGameData) -> None:
    if item_class != _active_item_class(static):
        raise StaticDataDefect(
            f"Unsupported item_class for active static data: {item_class!r}"
        )


def _assert_known_installed_mods(state: ItemState, static: StaticGameData) -> None:
    unknown = [instance.mod_id for instance in state.modifiers if instance.mod_id not in static.modifier_index]
    if unknown:
        raise UnknownModifierIdDefect(f"Unknown installed mod_id values: {sorted(unknown)}")


def _installed_blocker_sets(state: ItemState, static: StaticGameData) -> tuple[set[str], set[str]]:
    families: set[str] = set()
    groups: set[str] = set()
    for instance in state.modifiers:
        mod = static.modifier_index[instance.mod_id]
        families.add(mod.family_id)
        groups.update(mod.group_ids)
    return families, groups


def _free_slots_by_side(state: ItemState, static: StaticGameData) -> dict[str, int]:
    capacity = {"normal": {"prefix": 0, "suffix": 0}, "magic": {"prefix": 1, "suffix": 1}, "rare": {"prefix": 3, "suffix": 3}}
    rarity_capacity = capacity[state.rarity.value]
    used = Counter()
    for instance in state.modifiers:
        used[static.modifier_index[instance.mod_id].side.value] += 1
    if state.unrevealed_desecrated is not None:
        used[state.unrevealed_desecrated.side.value] += 1
    return {
        side: max(0, rarity_capacity[side] - used[side])
        for side in ("prefix", "suffix")
    }


def _canonical_removal_rows(state: ItemState, static: StaticGameData) -> tuple[_RemovalRow, ...]:
    identities = [
        (instance.mod_id, instance.crafted, instance.desecrated, instance.fractured)
        for instance in state.modifiers
    ]
    counts = Counter(identities)
    rows: list[_RemovalRow] = []
    for mod_id, crafted, desecrated, fractured in sorted(counts, key=_identity_sort_key):
        for ordinal in range(counts[(mod_id, crafted, desecrated, fractured)]):
            instance = ModifierInstance(
                mod_id=mod_id,
                crafted=crafted,
                desecrated=desecrated,
                fractured=fractured,
            )
            rows.append(
                _RemovalRow(
                    key=_removal_key(instance, ordinal),
                    instance=instance,
                    static=static.modifier_index[mod_id],
                    duplicate_ordinal=ordinal,
                )
            )
    return tuple(sorted(rows, key=lambda row: row.key.encode("ascii")))


def _identity_sort_key(identity: tuple[str, bool, bool, bool]) -> tuple[str, int, int, int]:
    mod_id, crafted, desecrated, fractured = identity
    return (mod_id, int(crafted), int(desecrated), int(fractured))


def _removal_key(instance: ModifierInstance, ordinal: int) -> str:
    return (
        f"rm:{instance.mod_id}:"
        f"c{int(instance.crafted)}:"
        f"d{int(instance.desecrated)}:"
        f"f{int(instance.fractured)}:"
        f"o{ordinal}"
    )


def _static_sort_key(mod: StaticModifier) -> tuple[bytes, int, int]:
    return (mod.mod_id.encode("ascii"), mod.tier, mod.modifier_level)


def _require_int_or_none(name: str, value: object) -> None:
    if value is None:
        return
    if not isinstance(value, int) or isinstance(value, bool):
        raise SamplingContractDefect(f"{name} must be an int or None, got {value!r}")


def _require_str_or_none(name: str, value: object) -> None:
    if value is None:
        return
    if not isinstance(value, str) or not value:
        raise SamplingContractDefect(f"{name} must be a non-empty str or None, got {value!r}")


def _require_string_tuple(name: str, value: object) -> None:
    if not isinstance(value, tuple) or any(not isinstance(item, str) for item in value):
        raise SamplingContractDefect(f"{name} must be a tuple[str, ...], got {value!r}")


def _positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _ordinary_request_payload(request: OrdinaryAddPoolRequest) -> dict[str, object]:
    return {
        "item_class": request.item_class,
        "state": request.state.canonical_payload(),
        "side_filter": request.side_filter.value if request.side_filter is not None else None,
        "mml": request.mml,
    }


def _removal_request_payload(request: RemovalPoolRequest) -> dict[str, object]:
    return {
        "item_class": request.item_class,
        "state": request.state.canonical_payload(),
        "side_filter": request.side_filter.value if request.side_filter is not None else None,
        "desecrated_only": request.desecrated_only,
        "crafted_only": request.crafted_only,
        "exact_modifier_level": request.exact_modifier_level,
        "minimum_modifier_level": request.minimum_modifier_level,
        "lowest_modifier_level": request.lowest_modifier_level,
    }


def _reveal_request_payload(
    request: RevealBasePoolRequest, placeholder_side: Side, reveal_mml: int | None
) -> dict[str, object]:
    return {
        "item_class": request.item_class,
        "state": request.state.canonical_payload(),
        "placeholder_side": placeholder_side.value,
        "reveal_mml": reveal_mml,
        "required_tag": request.required_tag,
        "excluded_family_ids": tuple(sorted(set(request.excluded_family_ids))),
        "excluded_group_ids": tuple(sorted(set(request.excluded_group_ids))),
    }


__all__ = [
    "M5_RESULT_FINGERPRINT_VERSION",
    "OrdinaryAddPoolRequest",
    "RemovalPoolRequest",
    "RevealBasePoolRequest",
    "build_ordinary_add_pool",
    "build_removal_pool",
    "build_reveal_base_pool",
    "apply_family_mml",
]
