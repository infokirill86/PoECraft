# Annulment Candidate Design

## Candidate scope

operation_id: `annulment`
operation_group: `annulment`
candidate_status: `design_only`
runtime_status: `not_accepted_as_executable`

Annulment is the first candidate because it is removal-only and can be anchored to the existing `build_removal_pool` kernel. This exercises a new state transition without introducing add/remove composition, Essence crafted-mod semantics, Jawbone/Reveal placeholders, Lich behavior, or PD-013 complexity.

## Project-model label

Annulment semantics in this design are PROJECT-MODEL BEHAVIOR ONLY.

They are not a PoE2 server-truth claim. SOURCE/PROVENANCE remains open.

## Minimal M35-A candidate shape

The proposed later M35-A implementation should admit only base Annulment:

- one operation invocation;
- no Omen selectors;
- no desecrated-only selector variant;
- no side-filter selector variant;
- no composition with add operations;
- no sequences beyond single Annulment in M35-A.

Selector variants may be designed later, but they should not be smuggled into the first runtime admission.

## State contract

Inputs:

- item state;
- installed modifier instances;
- static modifier index;
- rarity must be `magic` or `rare`, if the implementation chooses to enforce the data row contract.

Outputs:

- either one selected removable modifier instance is removed;
- or the operation produces explicit no-transition with no state mutation.

Fields that must not be mutated:

- fractured flag on any modifier;
- crafted/desecrated flags on remaining modifiers;
- item class;
- item level;
- unrelated augment/reveal state.

## Removable unit

The selected unit is an installed modifier instance, not a static mod family and not a display row.

Duplicate installed instances must remain distinguishable by canonical removal candidate key. Terminal states may later aggregate if duplicate removals lead to the same canonical item state.

## Fractured protection

Hard required property:

```text
Annulment must never remove fractured modifiers.
```

This is not advisory. It must be enforced by the load-bearing removal pool and by explicit negative-control tests.

## No-transition behavior

If there are no removable non-fractured installed modifiers, Annulment must return:

```text
NO_TRANSITION_NO_CONSUMPTION
```

The result must not fabricate a removal, must not remove a fractured modifier, and must not mutate the input item state.

## Selection rule

If there are `k` removable installed non-fractured modifier instances, Annulment selects uniformly over those `k` instances.

The exact/oracle branch probability is:

```text
1 / k
```

stored as exact rational numerator/denominator in later runtime evidence.

## Existing kernel anchor

The design should anchor M35-A to:

- `p2c_engine.legality.pool_builders.RemovalPoolRequest`;
- `p2c_engine.legality.pool_builders.build_removal_pool`.

The existing builder already has a fractured-exclusion stage. M35-A must prove that this builder, or a directly equivalent load-bearing path, is the one feeding Annulment probabilities.

