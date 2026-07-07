class EngineDefect(RuntimeError):
    pass


class StaticDataDefect(EngineDefect):
    pass


class UnknownModifierIdDefect(EngineDefect):
    pass


class PostValidationDefect(EngineDefect):
    pass


class ReplayDigestMismatch(EngineDefect):
    pass


class SemanticFingerprintMismatch(EngineDefect):
    pass


class SamplingContractDefect(EngineDefect):
    pass


class DuplicateDecisionIdDefect(EngineDefect):
    pass


class DecisionIdMismatch(EngineDefect):
    pass


class SelectedKeyMismatch(EngineDefect):
    pass


class TraceSchemaVersionMismatch(EngineDefect):
    pass


class ActionFingerprintMismatch(EngineDefect):
    pass


class MalformedOperationRequestDefect(EngineDefect):
    pass


class IncompatibleOmenBundleDefect(EngineDefect):
    pass


class InactiveOperationDefect(EngineDefect):
    pass


class ActionPlanContractDefect(EngineDefect):
    pass


class AmbiguousFailurePolicyDefect(EngineDefect):
    pass


from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DefectRecord:
    defect_type: str
    message: str
    context: dict[str, object]
