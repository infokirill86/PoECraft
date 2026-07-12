# Selected M48 Boundary and Rationale

## Selected boundary

**M48: Bounded Caller-Authored Branching Sequence Design**

Conceptual input:

```text
finite route DAG + accepted operation requests + named accepted predicates + initial ItemState
  -> exact/MC execution terminals + replay/diagnostics
```

The route is supplied completely by the caller. P2C never proposes a node or edge.

## Why this advances the intended simulator

A real crafting route reacts to outcomes. For example, a user may predeclare: execute an accepted currency; if the resulting item is TOP or ACCEPTABLE, stop; otherwise execute a particular accepted recovery step. The fixed M43-A tuple cannot represent that, even though all underlying operations already exist.

M48 therefore turns the accepted operation surface into a process evaluator. It is product progress rather than infrastructure cleanup.

## Why it is independent

- Only accepted operations and accepted Omen combinations may execute.
- Reveal, Echoes, Putrefaction, Astrid, Omen of Light, and revealed-Fracture states are unnecessary.
- It introduces no selection weights, item mechanics, source-truth decision, or public probability claim.
- Existing internal numeric quarantine remains in force.

## Why it is not a planner

- No route generation or action discovery.
- No alternative-route comparison.
- No costs, economics, EV, ranking, recommendation, or "best" output.
- No arbitrary user code or free-form expressions.
- No cycles or unbounded retries.
- Only named, versioned, accepted predicate IDs may control edges.
