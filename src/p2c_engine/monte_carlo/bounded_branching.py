from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Literal, Mapping, TypeAlias

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.static_data.game_data import StaticGameData

from .bounded_sequence import (
    AcceptedStepCeilingExceeded,
    BoundedAcceptedOperationSequenceHarness,
    BoundedSequenceStep,
    M43A_MAX_CANDIDATES_PER_POOL,
    M43A_MAX_STEPS,
    M43ASequenceAdmissionError,
    M43ASequenceInvariantViolation,
    SequenceStepTrace,
)
from .ordinary_add import M32_VALUE_POLICY, M32MonteCarloError


M48A_SCHEMA_VERSION = "p2c.m48a.bounded_branching_runtime.v1"
M48A_SEMANTICS_VERSION = "p2c.m48a.caller_authored_dag.project_model.v1"
M48A_SUCCESS_PREDICATE_ID = "success_class.v1"
M48A_MAX_NODES = 64
M48A_MAX_EDGES = 128
M48A_MAX_OPERATION_STEPS = M43A_MAX_STEPS
M48A_MAX_EXACT_PATHS = 65_536
M48A_MAX_EXACT_TERMINALS = 65_536
M48A_FIXED_SEEDS = (48_001, 48_002, 48_003)
M48A_SAMPLE_TIERS = (512, 2_048, 8_192)

PredicateValue = Literal["TOP", "ACCEPTABLE", "NOT_SUCCESS"]
RouteNodeKind = Literal["operation", "predicate_branch", "terminal"]


class M48ABranchingError(M32MonteCarloError):
    """Base error for the bounded caller-authored route evaluator."""


class M48ARouteAdmissionError(M48ABranchingError):
    """Structured fail-closed graph, operation, or predicate admission error."""

    def __init__(self, code: str, message: str, *, node_id: str | None = None) -> None:
        self.code = code
        self.node_id = node_id
        prefix = f"{code}"
        if node_id is not None:
            prefix += f"[{node_id}]"
        super().__init__(f"{prefix}: {message}")


class M48APredicateError(M48ABranchingError):
    """The accepted predicate contract cannot be interpreted safely."""


class M48ABranchingInvariantViolation(
    M48ABranchingError, M43ASequenceInvariantViolation
):
    """Accepted evaluator invariants failed."""


@dataclass(frozen=True, slots=True)
class OperationRouteNode:
    node_id: str
    step: BoundedSequenceStep
    on_transition: str
    on_no_transition: str
    kind: Literal["operation"] = "operation"


@dataclass(frozen=True, slots=True)
class PredicateRouteNode:
    node_id: str
    predicate_id: str
    cases: tuple[tuple[str, str], ...]
    kind: Literal["predicate_branch"] = "predicate_branch"


@dataclass(frozen=True, slots=True)
class TerminalRouteNode:
    node_id: str
    terminal_label: str
    kind: Literal["terminal"] = "terminal"


RouteNode: TypeAlias = OperationRouteNode | PredicateRouteNode | TerminalRouteNode


@dataclass(frozen=True, slots=True)
class BoundedBranchingRequest:
    route_id: str
    start_node_id: str
    nodes: tuple[RouteNode, ...]
    node_ceiling: int = M48A_MAX_NODES
    edge_ceiling: int = M48A_MAX_EDGES
    max_operation_steps_per_path: int = M48A_MAX_OPERATION_STEPS


@dataclass(frozen=True, slots=True)
class PredicateDecision:
    predicate_id: str
    result: PredicateValue
    state_hash: str

    def public_payload(self) -> dict[str, str]:
        return {
            "predicate_id": self.predicate_id,
            "result": self.result,
            "state_hash": self.state_hash,
        }


@dataclass(frozen=True, slots=True)
class RouteTraceEvent:
    node_id: str
    node_kind: RouteNodeKind
    pre_state_hash: str
    post_state_hash: str
    next_node_id: str | None
    operation_trace: SequenceStepTrace | None = None
    predicate_decision: PredicateDecision | None = None
    terminal_label: str | None = None

    def public_payload(self) -> dict[str, object]:
        return {
            "node_id": self.node_id,
            "node_kind": self.node_kind,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "next_node_id": self.next_node_id,
            "operation_trace": (
                self.operation_trace.public_payload()
                if self.operation_trace is not None
                else None
            ),
            "predicate_decision": (
                self.predicate_decision.public_payload()
                if self.predicate_decision is not None
                else None
            ),
            "terminal_label": self.terminal_label,
        }


@dataclass(frozen=True, slots=True)
class ExactRouteCeilingStop:
    stop_code: Literal[
        "candidate_branch_ceiling_exceeded",
        "exact_path_ceiling_exceeded",
        "exact_terminal_ceiling_exceeded",
    ]
    ceiling_name: str
    ceiling_limit: int
    observed_count: int
    node_id: str
    operation_step_index: int
    message: str


@dataclass(frozen=True, slots=True)
class ExactRoutePath:
    path_key: tuple[str, ...]
    terminal_node_id: str
    terminal_label: str
    terminal_state: ItemState
    terminal_state_hash: str
    execution_terminal_key: str
    last_operation_outcome: str
    visited_operation_count: int
    completed_operation_count: int
    events: tuple[RouteTraceEvent, ...]
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactRouteTerminal:
    execution_terminal_key: str
    terminal_node_id: str
    terminal_label: str
    terminal_state: ItemState
    terminal_state_hash: str
    last_operation_outcome: str
    path_count: int
    path_keys: tuple[tuple[str, ...], ...]
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactRouteStateProjection:
    terminal_state: ItemState
    terminal_state_hash: str
    execution_terminal_count: int
    path_count: int
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactBranchingEvaluation:
    schema_version: str
    status: Literal["completed", "ceiling_exceeded"]
    route_id: str
    path_count: int
    terminal_count: int
    mass_sum_exactly_one: bool
    paths: tuple[ExactRoutePath, ...]
    terminals: tuple[ExactRouteTerminal, ...]
    ceiling_stop: ExactRouteCeilingStop | None

    def public_summary(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "numeric_probability_free": True,
            "public_numeric_release": False,
            "probability_values_printed": False,
            "value_policy": M32_VALUE_POLICY,
            "route_id": self.route_id,
            "path_count": self.path_count,
            "terminal_count": self.terminal_count,
            "mass_sum_exactly_one": self.mass_sum_exactly_one,
            "ceiling_hit": self.ceiling_stop is not None,
            "ceiling_stop_code": (
                self.ceiling_stop.stop_code if self.ceiling_stop else None
            ),
        }

    def state_only_projection(self) -> tuple[ExactRouteStateProjection, ...]:
        if self.status != "completed":
            return ()
        masses: dict[str, Fraction] = defaultdict(Fraction)
        states: dict[str, ItemState] = {}
        terminal_counts: dict[str, int] = defaultdict(int)
        path_counts: dict[str, int] = defaultdict(int)
        for terminal in self.terminals:
            state_hash = terminal.terminal_state_hash
            masses[state_hash] += Fraction(
                terminal.probability_numerator, terminal.probability_denominator
            )
            states[state_hash] = terminal.terminal_state
            terminal_counts[state_hash] += 1
            path_counts[state_hash] += terminal.path_count
        return tuple(
            ExactRouteStateProjection(
                terminal_state=states[state_hash],
                terminal_state_hash=state_hash,
                execution_terminal_count=terminal_counts[state_hash],
                path_count=path_counts[state_hash],
                probability_numerator=mass.numerator,
                probability_denominator=mass.denominator,
            )
            for state_hash, mass in sorted(masses.items())
        )


@dataclass(frozen=True, slots=True)
class BranchingTrajectory:
    sample_index: int
    initial_state_hash: str
    terminal_node_id: str
    terminal_label: str
    terminal_state: ItemState
    terminal_state_hash: str
    execution_terminal_key: str
    last_operation_outcome: str
    visited_operation_count: int
    completed_operation_count: int
    events: tuple[RouteTraceEvent, ...]

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "initial_state_hash": self.initial_state_hash,
            "terminal_node_id": self.terminal_node_id,
            "terminal_label": self.terminal_label,
            "terminal_state_hash": self.terminal_state_hash,
            "execution_terminal_key": self.execution_terminal_key,
            "last_operation_outcome": self.last_operation_outcome,
            "visited_operation_count": self.visited_operation_count,
            "completed_operation_count": self.completed_operation_count,
            "events": [event.public_payload() for event in self.events],
        }


@dataclass(frozen=True, slots=True)
class BranchingRunResult:
    schema_version: str
    semantics_version: str
    run_id: str
    seed: int
    sample_count: int
    route_id: str
    rng_stream_version: int
    sampling_algorithm_id: str
    source_fingerprint: str
    semantic_fingerprint: str
    code_version: str
    trajectories: tuple[BranchingTrajectory, ...]
    decisions: tuple[DecisionRecord, ...]
    result_hash: str

    def public_summary(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "status": "PASS",
            "numeric_probability_free": True,
            "public_numeric_release": False,
            "probability_values_printed": False,
            "value_policy": M32_VALUE_POLICY,
            "run_id": self.run_id,
            "seed": self.seed,
            "sample_count": self.sample_count,
            "route_id": self.route_id,
            "source_fingerprint": self.source_fingerprint,
            "semantic_fingerprint": self.semantic_fingerprint,
            "trajectory_count": len(self.trajectories),
            "execution_terminal_count": len(
                {row.execution_terminal_key for row in self.trajectories}
            ),
            "result_hash": self.result_hash,
        }


@dataclass(frozen=True, slots=True)
class _FrontierEntry:
    state: ItemState
    node_id: str
    mass: Fraction
    events: tuple[RouteTraceEvent, ...]
    path_key: tuple[str, ...]
    visited_operation_count: int
    completed_operation_count: int
    last_operation_outcome: str


class AcceptedSuccessClassifier:
    """Strict interpreter for the accepted success-criteria data shape."""

    def __init__(self, *, static: StaticGameData) -> None:
        self.static = static
        self.criteria = static.success_criteria
        self._validate_contract()

    def classify(self, state: ItemState) -> PredicateValue:
        rows = self._modifier_rows(state)
        for value in self.criteria["evaluation_order"]:
            if value == "TOP" and self._matches_top(state, rows):
                return "TOP"
            if value == "ACCEPTABLE" and self._matches_acceptable(state, rows):
                return "ACCEPTABLE"
            if value == "NOT_SUCCESS":
                return "NOT_SUCCESS"
        raise M48APredicateError("success criteria evaluation_order has no fallback")

    def _validate_contract(self) -> None:
        root = self.criteria
        _require_exact_keys(
            root,
            {
                "schema_version",
                "tier_convention",
                "family_sets",
                "single_families",
                "evaluation_order",
                "TOP",
                "ACCEPTABLE",
                "origin_flags_affect_success",
                "status",
            },
            "success_criteria",
        )
        if root["schema_version"] != 2 or root["status"] != "READY":
            raise M48APredicateError("unsupported success-criteria version/status")
        if root["tier_convention"] != "T1 is strongest; T3+ means tier <= 3.":
            raise M48APredicateError("unsupported success-criteria tier convention")
        if tuple(root["evaluation_order"]) != ("TOP", "ACCEPTABLE", "NOT_SUCCESS"):
            raise M48APredicateError("unsupported success-criteria evaluation order")
        if root["origin_flags_affect_success"] is not False:
            raise M48APredicateError("origin-flag success behavior is not admitted")
        _require_exact_keys(
            root["family_sets"],
            {
                "physical_top_families",
                "elemental_flat_families",
                "top_final_suffix_families",
            },
            "success_criteria.family_sets",
        )
        _require_exact_keys(
            root["single_families"],
            {"critical_hit_chance", "all_melee_skills"},
            "success_criteria.single_families",
        )
        top = root["TOP"]
        _require_exact_keys(top, {"occupied_explicit_slots", "prefixes", "suffixes"}, "TOP")
        _require_exact_keys(top["prefixes"], {"distinct_from_set"}, "TOP.prefixes")
        _require_exact_keys(
            top["prefixes"]["distinct_from_set"],
            {"set", "count", "all_max_tier", "at_least_one_max_tier"},
            "TOP.prefixes.distinct_from_set",
        )
        if not isinstance(top["suffixes"], tuple) or len(top["suffixes"]) != 3:
            raise M48APredicateError("TOP suffix contract must contain three rules")
        _require_exact_keys(top["suffixes"][0], {"family", "max_tier"}, "TOP.suffixes[0]")
        _require_exact_keys(top["suffixes"][1], {"family", "max_tier"}, "TOP.suffixes[1]")
        _require_exact_keys(top["suffixes"][2], {"one_from_set", "max_tier"}, "TOP.suffixes[2]")

        acceptable = root["ACCEPTABLE"]
        _require_exact_keys(
            acceptable,
            {"occupied_explicit_slots", "prefixes", "suffixes"},
            "ACCEPTABLE",
        )
        _require_exact_keys(
            acceptable["prefixes"],
            {"physical_top", "third_prefix"},
            "ACCEPTABLE.prefixes",
        )
        _require_exact_keys(
            acceptable["prefixes"]["physical_top"],
            {"distinct_count", "one_max_tier", "other_max_tier"},
            "ACCEPTABLE.prefixes.physical_top",
        )
        _require_exact_keys(
            acceptable["prefixes"]["third_prefix"],
            {"one_from_union", "max_tier", "distinct_from_selected_physical_families"},
            "ACCEPTABLE.prefixes.third_prefix",
        )
        if not isinstance(acceptable["suffixes"], tuple) or len(acceptable["suffixes"]) != 3:
            raise M48APredicateError("ACCEPTABLE suffix contract must contain three rules")
        _require_exact_keys(
            acceptable["suffixes"][0], {"family", "max_tier"}, "ACCEPTABLE.suffixes[0]"
        )
        _require_exact_keys(
            acceptable["suffixes"][1], {"family", "max_tier"}, "ACCEPTABLE.suffixes[1]"
        )
        _require_exact_keys(
            acceptable["suffixes"][2], {"any_third_suffix"}, "ACCEPTABLE.suffixes[2]"
        )
        if acceptable["suffixes"][2]["any_third_suffix"] is not True:
            raise M48APredicateError("unsupported ACCEPTABLE third-suffix rule")

    def _modifier_rows(self, state: ItemState) -> tuple[StaticModifier, ...]:
        output: list[StaticModifier] = []
        for instance in state.modifiers:
            row = self.static.modifier_index.get(instance.mod_id)
            if row is None:
                raise M48APredicateError(
                    f"success classifier encountered unknown modifier: {instance.mod_id}"
                )
            output.append(row)
        return tuple(output)

    def _matches_top(self, state: ItemState, rows: tuple[StaticModifier, ...]) -> bool:
        rule = self.criteria["TOP"]
        if not _base_success_shape(state, rows, int(rule["occupied_explicit_slots"])):
            return False
        prefixes = tuple(row for row in rows if row.side == Side.PREFIX)
        suffixes = tuple(row for row in rows if row.side == Side.SUFFIX)
        prefix_rule = rule["prefixes"]["distinct_from_set"]
        allowed = set(self.criteria["family_sets"][prefix_rule["set"]])
        if len(prefixes) != int(prefix_rule["count"]):
            return False
        if len({row.family_id for row in prefixes}) != len(prefixes):
            return False
        if any(
            row.family_id not in allowed or row.tier > int(prefix_rule["all_max_tier"])
            for row in prefixes
        ):
            return False
        if not any(row.tier <= int(prefix_rule["at_least_one_max_tier"]) for row in prefixes):
            return False
        if len(suffixes) != 3:
            return False
        rules = rule["suffixes"]
        return (
            _contains_family(
                suffixes,
                self.criteria["single_families"][rules[0]["family"]],
                rules[0]["max_tier"],
            )
            and _contains_family(
                suffixes,
                self.criteria["single_families"][rules[1]["family"]],
                rules[1]["max_tier"],
            )
            and any(
                row.family_id in set(self.criteria["family_sets"][rules[2]["one_from_set"]])
                and row.tier <= int(rules[2]["max_tier"])
                for row in suffixes
            )
        )

    def _matches_acceptable(
        self, state: ItemState, rows: tuple[StaticModifier, ...]
    ) -> bool:
        rule = self.criteria["ACCEPTABLE"]
        if not _base_success_shape(state, rows, int(rule["occupied_explicit_slots"])):
            return False
        prefixes = tuple(row for row in rows if row.side == Side.PREFIX)
        suffixes = tuple(row for row in rows if row.side == Side.SUFFIX)
        if len(prefixes) != 3 or len(suffixes) != 3:
            return False
        physical = set(self.criteria["family_sets"]["physical_top_families"])
        prefix_rule = rule["prefixes"]["physical_top"]
        third_rule = rule["prefixes"]["third_prefix"]
        union: set[str] = set()
        for set_name in third_rule["one_from_union"]:
            union.update(self.criteria["family_sets"][set_name])
        prefix_match = False
        for selected_indices in combinations(range(len(prefixes)), int(prefix_rule["distinct_count"])):
            selected = tuple(prefixes[index] for index in selected_indices)
            if any(row.family_id not in physical for row in selected):
                continue
            if len({row.family_id for row in selected}) != len(selected):
                continue
            if any(row.tier > int(prefix_rule["other_max_tier"]) for row in selected):
                continue
            if not any(row.tier <= int(prefix_rule["one_max_tier"]) for row in selected):
                continue
            remaining = tuple(
                row for index, row in enumerate(prefixes) if index not in selected_indices
            )
            if len(remaining) != 1:
                continue
            third = remaining[0]
            if third.family_id not in union or third.tier > int(third_rule["max_tier"]):
                continue
            if (
                third_rule["distinct_from_selected_physical_families"] is True
                and third.family_id in {row.family_id for row in selected}
            ):
                continue
            prefix_match = True
            break
        if not prefix_match:
            return False
        suffix_rules = rule["suffixes"]
        critical_family = self.criteria["single_families"][suffix_rules[0]["family"]]
        melee_family = self.criteria["single_families"][suffix_rules[1]["family"]]
        return _contains_family(
            suffixes, critical_family, suffix_rules[0]["max_tier"]
        ) and _contains_family(suffixes, melee_family, suffix_rules[1]["max_tier"])


class AcceptedPredicateRegistry:
    """Closed deterministic state-predicate registry; no callback/plugin seam."""

    def __init__(self, *, static: StaticGameData) -> None:
        self.classifier = AcceptedSuccessClassifier(static=static)

    @property
    def predicate_ids(self) -> tuple[str, ...]:
        return (M48A_SUCCESS_PREDICATE_ID,)

    def result_values(self, predicate_id: str) -> tuple[str, ...]:
        self._require(predicate_id)
        return ("TOP", "ACCEPTABLE", "NOT_SUCCESS")

    def evaluate(self, predicate_id: str, state: ItemState) -> PredicateDecision:
        self._require(predicate_id)
        return PredicateDecision(
            predicate_id=predicate_id,
            result=self.classifier.classify(state),
            state_hash=state.state_hash(),
        )

    def _require(self, predicate_id: str) -> None:
        if predicate_id != M48A_SUCCESS_PREDICATE_ID:
            raise M48ARouteAdmissionError(
                "unsupported_predicate",
                f"predicate is not in the accepted registry: {predicate_id}",
            )


class BoundedBranchingRouteHarness:
    """Evaluate caller-authored finite DAGs; never create or rank routes."""

    def __init__(
        self,
        *,
        static: StaticGameData,
        sequence_harness: BoundedAcceptedOperationSequenceHarness | None = None,
        predicate_registry: AcceptedPredicateRegistry | None = None,
        code_version: str = "p2c.m48a.dev",
    ) -> None:
        self.static = static
        self.sequence = sequence_harness or BoundedAcceptedOperationSequenceHarness(
            static=static, code_version=code_version
        )
        self.predicates = predicate_registry or AcceptedPredicateRegistry(static=static)
        self.code_version = code_version

    def validate_request(self, request: BoundedBranchingRequest) -> None:
        if not isinstance(request.route_id, str) or not request.route_id.strip():
            _route_fail("invalid_route_id", "route_id must be a non-empty string")
        if not isinstance(request.start_node_id, str) or not request.start_node_id:
            _route_fail("invalid_start_node", "start_node_id must be a non-empty string")
        _validate_request_ceiling("node_ceiling", request.node_ceiling, M48A_MAX_NODES)
        _validate_request_ceiling("edge_ceiling", request.edge_ceiling, M48A_MAX_EDGES)
        _validate_request_ceiling(
            "max_operation_steps_per_path",
            request.max_operation_steps_per_path,
            M48A_MAX_OPERATION_STEPS,
        )
        if not isinstance(request.nodes, tuple) or not request.nodes:
            _route_fail("invalid_nodes", "nodes must be a non-empty tuple")
        if len(request.nodes) > request.node_ceiling:
            _route_fail(
                "node_ceiling_exceeded",
                f"graph has {len(request.nodes)} nodes; ceiling is {request.node_ceiling}",
            )

        by_id: dict[str, RouteNode] = {}
        terminal_labels: set[str] = set()
        for node in request.nodes:
            if not isinstance(node, (OperationRouteNode, PredicateRouteNode, TerminalRouteNode)):
                _route_fail("invalid_node_type", f"unsupported node type: {type(node).__name__}")
            if not isinstance(node.node_id, str) or not node.node_id:
                _route_fail("invalid_node_id", "every node_id must be a non-empty string")
            if node.node_id in by_id:
                _route_fail("duplicate_node_id", "node_id must be unique", node.node_id)
            by_id[node.node_id] = node
            if isinstance(node, TerminalRouteNode):
                if not node.terminal_label:
                    _route_fail("invalid_terminal_label", "terminal_label is required", node.node_id)
                if node.terminal_label in terminal_labels:
                    _route_fail(
                        "ambiguous_terminal_label",
                        f"terminal_label is duplicated: {node.terminal_label}",
                        node.node_id,
                    )
                terminal_labels.add(node.terminal_label)

        if request.start_node_id not in by_id:
            _route_fail("missing_start_node", "start_node_id does not exist")
        if not terminal_labels:
            _route_fail("missing_terminal", "graph requires at least one terminal node")

        edges: dict[str, tuple[str, ...]] = {}
        edge_count = 0
        for node in request.nodes:
            if isinstance(node, OperationRouteNode):
                try:
                    self.sequence.validate_composition_step(node.step, 0)
                except M43ASequenceAdmissionError as exc:
                    _route_fail("unsupported_operation", str(exc), node.node_id)
                targets = (node.on_transition, node.on_no_transition)
            elif isinstance(node, PredicateRouteNode):
                if not node.predicate_id:
                    _route_fail("invalid_predicate", "predicate_id is required", node.node_id)
                expected = self.predicates.result_values(node.predicate_id)
                if not isinstance(node.cases, tuple):
                    _route_fail("invalid_predicate_cases", "cases must be a tuple", node.node_id)
                labels = tuple(label for label, _ in node.cases)
                if len(labels) != len(set(labels)):
                    _route_fail("duplicate_predicate_case", "predicate cases must be unique", node.node_id)
                if set(labels) != set(expected) or len(labels) != len(expected):
                    _route_fail(
                        "incomplete_predicate_cases",
                        f"cases must exactly cover {expected}",
                        node.node_id,
                    )
                targets = tuple(target for _, target in node.cases)
            else:
                targets = ()
            for target in targets:
                if not isinstance(target, str) or not target or target not in by_id:
                    _route_fail(
                        "missing_edge_target",
                        f"edge references missing node: {target!r}",
                        node.node_id,
                    )
            edges[node.node_id] = targets
            edge_count += len(targets)
        if edge_count > request.edge_ceiling:
            _route_fail(
                "edge_ceiling_exceeded",
                f"graph has {edge_count} edges; ceiling is {request.edge_ceiling}",
            )

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in visiting:
                _route_fail("cycle_detected", "route graph must be acyclic", node_id)
            if node_id in visited:
                return
            visiting.add(node_id)
            for target in edges[node_id]:
                visit(target)
            visiting.remove(node_id)
            visited.add(node_id)

        visit(request.start_node_id)
        unreachable = sorted(set(by_id) - visited)
        if unreachable:
            _route_fail(
                "unreachable_nodes",
                f"all declared nodes must be reachable: {unreachable}",
            )

        depth_cache: dict[str, int] = {}

        def max_operation_depth(node_id: str) -> int:
            if node_id in depth_cache:
                return depth_cache[node_id]
            node = by_id[node_id]
            own = 1 if isinstance(node, OperationRouteNode) else 0
            child = max((max_operation_depth(target) for target in edges[node_id]), default=0)
            depth_cache[node_id] = own + child
            return depth_cache[node_id]

        depth = max_operation_depth(request.start_node_id)
        if depth > request.max_operation_steps_per_path:
            _route_fail(
                "operation_step_ceiling_exceeded",
                f"root-to-leaf operation depth {depth} exceeds {request.max_operation_steps_per_path}",
            )

    def enumerate_exact(
        self,
        *,
        initial_state: ItemState,
        request: BoundedBranchingRequest,
        decision_id_prefix: str,
        max_candidates_per_pool: int = M43A_MAX_CANDIDATES_PER_POOL,
        max_exact_paths: int = M48A_MAX_EXACT_PATHS,
        max_exact_terminals: int = M48A_MAX_EXACT_TERMINALS,
    ) -> ExactBranchingEvaluation:
        self.validate_request(request)
        _validate_positive_ceiling("max_candidates_per_pool", max_candidates_per_pool)
        _validate_positive_ceiling("max_exact_paths", max_exact_paths)
        _validate_positive_ceiling("max_exact_terminals", max_exact_terminals)
        by_id = {node.node_id: node for node in request.nodes}
        frontier = deque(
            [
                _FrontierEntry(
                    state=initial_state,
                    node_id=request.start_node_id,
                    mass=Fraction(1, 1),
                    events=(),
                    path_key=(request.start_node_id,),
                    visited_operation_count=0,
                    completed_operation_count=0,
                    last_operation_outcome="not_started",
                )
            ]
        )
        paths: list[ExactRoutePath] = []

        while frontier:
            entry = frontier.popleft()
            node = by_id[entry.node_id]
            if isinstance(node, TerminalRouteNode):
                event = RouteTraceEvent(
                    node_id=node.node_id,
                    node_kind="terminal",
                    pre_state_hash=entry.state.state_hash(),
                    post_state_hash=entry.state.state_hash(),
                    next_node_id=None,
                    terminal_label=node.terminal_label,
                )
                paths.append(self._exact_path(entry, node, event))
            elif isinstance(node, PredicateRouteNode):
                decision = self.predicates.evaluate(node.predicate_id, entry.state)
                target = dict(node.cases)[decision.result]
                event = RouteTraceEvent(
                    node_id=node.node_id,
                    node_kind="predicate_branch",
                    pre_state_hash=entry.state.state_hash(),
                    post_state_hash=entry.state.state_hash(),
                    next_node_id=target,
                    predicate_decision=decision,
                )
                frontier.append(
                    _FrontierEntry(
                        state=entry.state,
                        node_id=target,
                        mass=entry.mass,
                        events=entry.events + (event,),
                        path_key=entry.path_key + (f"{node.node_id}:{decision.result}", target),
                        visited_operation_count=entry.visited_operation_count,
                        completed_operation_count=entry.completed_operation_count,
                        last_operation_outcome=entry.last_operation_outcome,
                    )
                )
            else:
                try:
                    transitions = self.sequence.enumerate_accepted_step(
                        state=entry.state,
                        step=node.step,
                        step_index=entry.visited_operation_count,
                        decision_id_prefix=decision_id_prefix,
                        max_candidates_per_pool=max_candidates_per_pool,
                    )
                except AcceptedStepCeilingExceeded as exc:
                    return self._ceiling_result(
                        request,
                        ExactRouteCeilingStop(
                            stop_code=exc.stop.stop_code,
                            ceiling_name=exc.stop.ceiling_name,
                            ceiling_limit=exc.stop.ceiling_limit,
                            observed_count=exc.stop.observed_count,
                            node_id=node.node_id,
                            operation_step_index=entry.visited_operation_count,
                            message=exc.stop.message,
                        ),
                    )
                for transition in transitions:
                    no_transition = transition.trace.outcome == "no_transition_no_consumption"
                    target = node.on_no_transition if no_transition else node.on_transition
                    event = RouteTraceEvent(
                        node_id=node.node_id,
                        node_kind="operation",
                        pre_state_hash=transition.trace.pre_state_hash,
                        post_state_hash=transition.trace.post_state_hash,
                        next_node_id=target,
                        operation_trace=transition.trace,
                    )
                    frontier.append(
                        _FrontierEntry(
                            state=transition.state,
                            node_id=target,
                            mass=entry.mass * transition.probability,
                            events=entry.events + (event,),
                            path_key=entry.path_key
                            + (f"{node.node_id}:{transition.path_component}", target),
                            visited_operation_count=entry.visited_operation_count + 1,
                            completed_operation_count=(
                                entry.completed_operation_count + (0 if no_transition else 1)
                            ),
                            last_operation_outcome=transition.trace.outcome,
                        )
                    )

            observed_paths = len(frontier) + len(paths)
            if observed_paths > max_exact_paths:
                return self._ceiling_result(
                    request,
                    ExactRouteCeilingStop(
                        stop_code="exact_path_ceiling_exceeded",
                        ceiling_name="max_exact_paths",
                        ceiling_limit=max_exact_paths,
                        observed_count=observed_paths,
                        node_id=entry.node_id,
                        operation_step_index=entry.visited_operation_count,
                        message="M48-A exact route path ceiling exceeded",
                    ),
                )
            observed_terminals = len({path.execution_terminal_key for path in paths})
            if observed_terminals > max_exact_terminals:
                return self._ceiling_result(
                    request,
                    ExactRouteCeilingStop(
                        stop_code="exact_terminal_ceiling_exceeded",
                        ceiling_name="max_exact_terminals",
                        ceiling_limit=max_exact_terminals,
                        observed_count=observed_terminals,
                        node_id=entry.node_id,
                        operation_step_index=entry.visited_operation_count,
                        message="M48-A exact route terminal ceiling exceeded",
                    ),
                )

        terminals = _aggregate_route_terminals(paths)
        path_mass = sum(
            (
                Fraction(path.probability_numerator, path.probability_denominator)
                for path in paths
            ),
            Fraction(0, 1),
        )
        terminal_mass = sum(
            (
                Fraction(row.probability_numerator, row.probability_denominator)
                for row in terminals
            ),
            Fraction(0, 1),
        )
        if path_mass != Fraction(1, 1) or terminal_mass != Fraction(1, 1):
            raise M48ABranchingInvariantViolation(
                f"M48-A exact mass violation: paths={path_mass}, terminals={terminal_mass}"
            )
        return ExactBranchingEvaluation(
            schema_version=M48A_SCHEMA_VERSION,
            status="completed",
            route_id=request.route_id,
            path_count=len(paths),
            terminal_count=len(terminals),
            mass_sum_exactly_one=True,
            paths=tuple(paths),
            terminals=terminals,
            ceiling_stop=None,
        )

    def sample_once(
        self,
        *,
        initial_state: ItemState,
        request: BoundedBranchingRequest,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
    ) -> BranchingTrajectory:
        self.validate_request(request)
        by_id = {node.node_id: node for node in request.nodes}
        state = initial_state
        node_id = request.start_node_id
        events: list[RouteTraceEvent] = []
        visited_count = 0
        completed_count = 0
        last_outcome = "not_started"

        while True:
            node = by_id[node_id]
            if isinstance(node, TerminalRouteNode):
                event = RouteTraceEvent(
                    node_id=node.node_id,
                    node_kind="terminal",
                    pre_state_hash=state.state_hash(),
                    post_state_hash=state.state_hash(),
                    next_node_id=None,
                    terminal_label=node.terminal_label,
                )
                events.append(event)
                terminal_key = _route_terminal_key(
                    node_id=node.node_id,
                    label=node.terminal_label,
                    state_hash=state.state_hash(),
                    outcome=last_outcome,
                )
                return BranchingTrajectory(
                    sample_index=sample_index,
                    initial_state_hash=initial_state.state_hash(),
                    terminal_node_id=node.node_id,
                    terminal_label=node.terminal_label,
                    terminal_state=state,
                    terminal_state_hash=state.state_hash(),
                    execution_terminal_key=terminal_key,
                    last_operation_outcome=last_outcome,
                    visited_operation_count=visited_count,
                    completed_operation_count=completed_count,
                    events=tuple(events),
                )
            if isinstance(node, PredicateRouteNode):
                decision = self.predicates.evaluate(node.predicate_id, state)
                target = dict(node.cases)[decision.result]
                events.append(
                    RouteTraceEvent(
                        node_id=node.node_id,
                        node_kind="predicate_branch",
                        pre_state_hash=state.state_hash(),
                        post_state_hash=state.state_hash(),
                        next_node_id=target,
                        predicate_decision=decision,
                    )
                )
                node_id = target
                continue

            transition = self.sequence.sample_accepted_step(
                state=state,
                step=node.step,
                step_index=visited_count,
                decision_source=decision_source,
                sample_index=sample_index,
                run_id=run_id,
            )
            no_transition = transition.trace.outcome == "no_transition_no_consumption"
            target = node.on_no_transition if no_transition else node.on_transition
            events.append(
                RouteTraceEvent(
                    node_id=node.node_id,
                    node_kind="operation",
                    pre_state_hash=transition.trace.pre_state_hash,
                    post_state_hash=transition.trace.post_state_hash,
                    next_node_id=target,
                    operation_trace=transition.trace,
                )
            )
            state = transition.state
            visited_count += 1
            if not no_transition:
                completed_count += 1
            last_outcome = transition.trace.outcome
            node_id = target

    def run(
        self,
        *,
        initial_state: ItemState,
        request: BoundedBranchingRequest,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> BranchingRunResult:
        self.validate_request(request)
        if isinstance(sample_count, bool) or not isinstance(sample_count, int) or sample_count < 0:
            raise SamplingContractDefect(
                "sample_count must be a non-negative non-bool integer"
            )
        source = RecordingDecisionSource(SeededDecisionSource(seed))
        trajectories = tuple(
            self.sample_once(
                initial_state=initial_state,
                request=request,
                decision_source=source,
                sample_index=index,
                run_id=run_id,
            )
            for index in range(sample_count)
        )
        payload = {
            "schema_version": M48A_SCHEMA_VERSION,
            "semantics_version": M48A_SEMANTICS_VERSION,
            "run_id": run_id,
            "seed": seed,
            "sample_count": sample_count,
            "route_id": request.route_id,
            "rng_stream_version": RNG_STREAM_VERSION,
            "sampling_algorithm_id": SAMPLING_ALGORITHM_ID,
            "source_fingerprint": self.static.source_fingerprint,
            "semantic_fingerprint": self.static.semantic_fingerprint,
            "code_version": self.code_version,
            "trajectories": [row.public_payload() for row in trajectories],
            "decisions": list(source.records),
        }
        return BranchingRunResult(
            schema_version=M48A_SCHEMA_VERSION,
            semantics_version=M48A_SEMANTICS_VERSION,
            run_id=run_id,
            seed=seed,
            sample_count=sample_count,
            route_id=request.route_id,
            rng_stream_version=RNG_STREAM_VERSION,
            sampling_algorithm_id=SAMPLING_ALGORITHM_ID,
            source_fingerprint=self.static.source_fingerprint,
            semantic_fingerprint=self.static.semantic_fingerprint,
            code_version=self.code_version,
            trajectories=trajectories,
            decisions=source.records,
            result_hash=sha256_canonical(payload, schema_version=1),
        )

    def verify_replay(
        self,
        *,
        expected: BranchingRunResult,
        initial_state: ItemState,
        request: BoundedBranchingRequest,
    ) -> BranchingRunResult:
        replayed = self.run(
            initial_state=initial_state,
            request=request,
            seed=expected.seed,
            sample_count=expected.sample_count,
            run_id=expected.run_id,
        )
        if replayed != expected:
            raise M48ABranchingInvariantViolation("M48-A deterministic replay mismatch")
        return replayed

    def _exact_path(
        self,
        entry: _FrontierEntry,
        node: TerminalRouteNode,
        event: RouteTraceEvent,
    ) -> ExactRoutePath:
        state_hash = entry.state.state_hash()
        key = _route_terminal_key(
            node_id=node.node_id,
            label=node.terminal_label,
            state_hash=state_hash,
            outcome=entry.last_operation_outcome,
        )
        return ExactRoutePath(
            path_key=entry.path_key + (f"{node.node_id}:{node.terminal_label}",),
            terminal_node_id=node.node_id,
            terminal_label=node.terminal_label,
            terminal_state=entry.state,
            terminal_state_hash=state_hash,
            execution_terminal_key=key,
            last_operation_outcome=entry.last_operation_outcome,
            visited_operation_count=entry.visited_operation_count,
            completed_operation_count=entry.completed_operation_count,
            events=entry.events + (event,),
            probability_numerator=entry.mass.numerator,
            probability_denominator=entry.mass.denominator,
        )

    def _ceiling_result(
        self, request: BoundedBranchingRequest, stop: ExactRouteCeilingStop
    ) -> ExactBranchingEvaluation:
        return ExactBranchingEvaluation(
            schema_version=M48A_SCHEMA_VERSION,
            status="ceiling_exceeded",
            route_id=request.route_id,
            path_count=0,
            terminal_count=0,
            mass_sum_exactly_one=False,
            paths=(),
            terminals=(),
            ceiling_stop=stop,
        )


def _require_exact_keys(value: Mapping[str, object], expected: set[str], label: str) -> None:
    if not isinstance(value, Mapping) or set(value) != expected:
        actual = sorted(value) if isinstance(value, Mapping) else type(value).__name__
        raise M48APredicateError(
            f"unsupported {label} shape; expected={sorted(expected)}, actual={actual}"
        )


def _base_success_shape(
    state: ItemState, rows: tuple[StaticModifier, ...], occupied_slots: int
) -> bool:
    occupied = len(rows) + (1 if state.unrevealed_desecrated is not None else 0)
    return (
        state.item_class == "quarterstaff"
        and state.rarity == Rarity.RARE
        and occupied == occupied_slots
    )


def _contains_family(
    rows: tuple[StaticModifier, ...], family_id: str, max_tier: int | None
) -> bool:
    return any(
        row.family_id == family_id and (max_tier is None or row.tier <= int(max_tier))
        for row in rows
    )


def _route_fail(code: str, message: str, node_id: str | None = None) -> None:
    raise M48ARouteAdmissionError(code, message, node_id=node_id)


def _validate_request_ceiling(name: str, value: int, maximum: int) -> None:
    _validate_positive_ceiling(name, value)
    if value > maximum:
        _route_fail(
            "ceiling_above_accepted_maximum",
            f"{name}={value} exceeds accepted maximum {maximum}",
        )


def _validate_positive_ceiling(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise SamplingContractDefect(f"{name} must be a positive non-bool integer")


def _route_terminal_key(*, node_id: str, label: str, state_hash: str, outcome: str) -> str:
    return sha256_canonical(
        {
            "terminal_node_id": node_id,
            "terminal_label": label,
            "terminal_state_hash": state_hash,
            "last_operation_outcome": outcome,
        },
        schema_version=1,
    )


def _aggregate_route_terminals(
    paths: list[ExactRoutePath],
) -> tuple[ExactRouteTerminal, ...]:
    masses: dict[str, Fraction] = defaultdict(Fraction)
    rows: dict[str, ExactRoutePath] = {}
    path_keys: dict[str, list[tuple[str, ...]]] = defaultdict(list)
    for path in paths:
        key = path.execution_terminal_key
        masses[key] += Fraction(path.probability_numerator, path.probability_denominator)
        rows[key] = path
        path_keys[key].append(path.path_key)
    return tuple(
        ExactRouteTerminal(
            execution_terminal_key=key,
            terminal_node_id=rows[key].terminal_node_id,
            terminal_label=rows[key].terminal_label,
            terminal_state=rows[key].terminal_state,
            terminal_state_hash=rows[key].terminal_state_hash,
            last_operation_outcome=rows[key].last_operation_outcome,
            path_count=len(path_keys[key]),
            path_keys=tuple(sorted(path_keys[key])),
            probability_numerator=mass.numerator,
            probability_denominator=mass.denominator,
        )
        for key, mass in sorted(masses.items())
    )


__all__ = [
    "AcceptedPredicateRegistry",
    "AcceptedSuccessClassifier",
    "BoundedBranchingRequest",
    "BoundedBranchingRouteHarness",
    "BranchingRunResult",
    "BranchingTrajectory",
    "ExactBranchingEvaluation",
    "ExactRouteCeilingStop",
    "ExactRoutePath",
    "ExactRouteStateProjection",
    "ExactRouteTerminal",
    "M48A_FIXED_SEEDS",
    "M48A_MAX_EDGES",
    "M48A_MAX_EXACT_PATHS",
    "M48A_MAX_EXACT_TERMINALS",
    "M48A_MAX_NODES",
    "M48A_MAX_OPERATION_STEPS",
    "M48A_SAMPLE_TIERS",
    "M48A_SCHEMA_VERSION",
    "M48A_SEMANTICS_VERSION",
    "M48A_SUCCESS_PREDICATE_ID",
    "M48ABranchingError",
    "M48ABranchingInvariantViolation",
    "M48APredicateError",
    "M48ARouteAdmissionError",
    "OperationRouteNode",
    "PredicateDecision",
    "PredicateRouteNode",
    "RouteTraceEvent",
    "TerminalRouteNode",
]
