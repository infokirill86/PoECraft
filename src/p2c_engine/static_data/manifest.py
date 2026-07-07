from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True, slots=True)
class DataManifest:
    ordinary_mods: str = "data/mods_ordinary_quarterstaff.yaml"
    desecrated_mods: str = "data/mods_desecrated_quarterstaff.yaml"
    essence_outputs: str = "data/essence_outputs.yaml"
    operations: str = "data/operations.yaml"
    omens: str = "data/omens.yaml"
    family_registry: str = "data/family_registry.yaml"
    initial_states: str = "config/initial_states.yaml"
    project_scope: str = "config/project_scope.yaml"
    success_criteria: str = "config/success_criteria.yaml"
    failure_consumption_matrix: str = "config/failure_consumption_matrix.yaml"
    item_state_schema: str = "schemas/item_state.schema.yaml"
    static_modifier_schema: str = "schemas/static_modifier.schema.yaml"

    def ordered_paths(self) -> tuple[str, ...]:
        return tuple(getattr(self, name) for name in self.__dataclass_fields__)

DEFAULT_MANIFEST = DataManifest()
