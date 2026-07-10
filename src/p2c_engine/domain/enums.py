from enum import StrEnum

class Rarity(StrEnum):
    NORMAL = "normal"
    MAGIC = "magic"
    RARE = "rare"

class Side(StrEnum):
    PREFIX = "prefix"
    SUFFIX = "suffix"

class OperationGroup(StrEnum):
    TRANSMUTATION = "transmutation"
    AUGMENTATION = "augmentation"
    REGAL = "regal"
    EXALTED = "exalted"
    ANNULMENT = "annulment"
    CHAOS = "chaos"
    SUPPORT_AUGMENT = "support_augment"
    GREATER_ESSENCE = "greater_essence"
    PERFECT_ESSENCE = "perfect_essence"
    JAWBONE = "jawbone"
    REVEAL = "reveal"

class OutcomeKind(StrEnum):
    APPLIED = "applied"
    NO_TRANSITION = "no_transition"
    CRAFTING_FAILED = "crafting_failed"

class FailureStage(StrEnum):
    COMPILE = "compile"
    PRECONDITION = "precondition"
    EXECUTION = "execution"
    POST_VALIDATION = "post_validation"

class FailureCode(StrEnum):
    INVALID_REQUEST = "invalid_request"
    INVALID_ACTION = "invalid_action"
    INVALID_ITEM_STATE = "invalid_item_state"
    UNKNOWN_MOD_ID = "unknown_mod_id"
    SIDE_CAPACITY_EXCEEDED = "side_capacity_exceeded"
    TOTAL_CAPACITY_EXCEEDED = "total_capacity_exceeded"
    DUPLICATE_FAMILY_BLOCKED = "duplicate_family_blocked"
    GROUP_CONFLICT_BLOCKED = "group_conflict_blocked"
    CRAFTED_CAPACITY_EXCEEDED = "crafted_capacity_exceeded"
    DESECRATED_LIMIT_EXCEEDED = "desecrated_limit_exceeded"
    ASTRID_SOCKET_UNAVAILABLE = "astrid_socket_unavailable"
    INVALID_PLACEHOLDER_SIDE = "invalid_placeholder_side"
    AUGMENT_SOCKET_CAPACITY_EXCEEDED = "augment_socket_capacity_exceeded"

class PlanStage(StrEnum):
    VALIDATE_STATE = "validate_state"
    BUILD_REMOVAL_POOL = "build_removal_pool"
    SAMPLE_REMOVAL = "sample_removal"
    REMOVE_MODIFIER = "remove_modifier"
    BUILD_ADD_POOL = "build_add_pool"
    SAMPLE_ADD = "sample_add"
    ADD_MODIFIER = "add_modifier"
    CREATE_PLACEHOLDER = "create_placeholder"
    BUILD_REVEAL_OFFER_SET = "build_reveal_offer_set"
    INSTALL_ASTRID = "install_astrid"
    VALIDATE_POST_STATE = "validate_post_state"
    COMMIT = "commit"
