# Shared Bounded Sequence Architecture

## One sequence layer, existing operation executors

M43-A should generalize the accepted M36-A chain seam. It must not copy operation semantics into the sequence layer.

For each live branch and step:

1. Validate the sequence and step bounds.
2. Resolve the step against that branch's current `ItemState` through `OperationResolver`.
3. Reject any non-admitted operation, variant, or modifier.
4. Dispatch the resolved operation to its accepted exact or MC executor.
5. Apply the operation's existing atomic failure/commit contract.
6. Record the branch-specific before/after state and pool/removal digest.
7. Re-resolve and rebuild from the new branch state for the next step.

No pool, precondition result, or resolved operation object may be reused across branches when state can differ.

## Operation coverage

M43-A should consume the accepted runtime registry, with an explicit supported-executor mapping for:

- `ordinary_add`;
- admitted rarity-progression and Exalted single-add rows;
- base Annulment;
- admitted Chaos-like rows;
- admitted Greater Essence rows;
- admitted Perfect Essence rows.

Registry admission is necessary but not sufficient: an admitted row without a registered accepted executor must fail closed.

## No-transition policy

`stop_on_no_transition` is pinned to `true` for M43-A.

When step `i` cannot execute:

- that step consumes nothing and does not mutate its input state;
- earlier committed steps remain committed;
- no later step runs on that branch;
- the path terminates with the last committed item state plus an explicit step/outcome code;
- exact mass is conserved.

The sequence is not globally atomic. Each accepted currency action retains its own atomic contract.

## Identity model

Keep three identities distinct:

- path identity: all step transition keys and branch order;
- item-state identity: canonical final `ItemState`;
- execution-terminal identity: canonical item state plus completed-step count, terminal step, and outcome code.

Correctness aggregation uses execution-terminal identity. A separate state-only projection may aggregate item states after validation, but must not erase early-failure diagnostics.

## Fail-closed contract

Reject:

- a sequence outside the bound;
- duplicate/missing step identifiers;
- unadmitted operation rows;
- admitted rows without an accepted executor mapping;
- non-empty modifier or unsupported variant requests;
- current-state rarity/precondition mismatch;
- stale resolver/static fingerprints;
- ceiling overflow without an explicit exact-stop record.
