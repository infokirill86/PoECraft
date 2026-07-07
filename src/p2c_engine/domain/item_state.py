from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Any
from p2c_engine.canonical import sha256_canonical
from .enums import Rarity, Side

@dataclass(frozen=True, slots=True)
class ModifierInstance:
    mod_id: str
    crafted: bool = False
    desecrated: bool = False
    fractured: bool = False

@dataclass(frozen=True, slots=True)
class DesecratedPlaceholder:
    side: Side
    jawbone_id: str
    reveal_mml: int | None
    lich_tag_constraint: str | None

    @property
    def lich_tag_priority(self) -> str | None:
        """Compatibility alias for pre-M7h call sites; not active model naming."""
        return self.lich_tag_constraint

@dataclass(frozen=True, slots=True)
class ItemState:
    item_class: str
    rarity: Rarity
    item_level: int
    modifiers: tuple[ModifierInstance, ...]
    unrevealed_desecrated: DesecratedPlaceholder | None
    augment_socket_capacity: int
    augment_socket_used: int
    astrid_installed: bool

    def canonical_payload(self) -> dict[str, Any]:
        mods = sorted(({
            "mod_id": m.mod_id,
            "crafted": m.crafted,
            "desecrated": m.desecrated,
            "fractured": m.fractured,
        } for m in self.modifiers), key=lambda x: (x["mod_id"], x["crafted"], x["desecrated"], x["fractured"]))
        placeholder = None
        if self.unrevealed_desecrated is not None:
            p = self.unrevealed_desecrated
            placeholder = {
                "side": p.side.value,
                "jawbone_id": p.jawbone_id,
                "reveal_mml": p.reveal_mml,
                "lich_tag_constraint": p.lich_tag_constraint,
            }
        return {
            "item_class": self.item_class,
            "rarity": self.rarity.value,
            "item_level": self.item_level,
            "modifiers": mods,
            "unrevealed_desecrated": placeholder,
            "augment_socket_capacity": self.augment_socket_capacity,
            "augment_socket_used": self.augment_socket_used,
            "astrid_installed": self.astrid_installed,
        }

    def state_hash(self) -> str:
        return sha256_canonical(self.canonical_payload(), schema_version=1)

    def with_modifiers(self, modifiers: tuple[ModifierInstance, ...]) -> "ItemState":
        return replace(self, modifiers=modifiers)

@dataclass(frozen=True, slots=True)
class InstalledInstanceKey:
    mod_id: str
    crafted: bool
    desecrated: bool
    fractured: bool
    duplicate_ordinal: int = 0
