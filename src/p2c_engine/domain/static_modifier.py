from dataclasses import dataclass
from .enums import Side

@dataclass(frozen=True, slots=True)
class StaticModifier:
    mod_id: str
    family_id: str
    side: Side
    group_ids: tuple[str, ...]
    tier: int
    modifier_level: int
    tags: tuple[str, ...]
    generation_weight: int
    static_category: str
    lich_tag: str | None = None
