# Proposed Shared Architecture

## 1. Admission and compilation

- Add explicit Omen runtime-admission metadata; catalogue presence and project-scope activity are not execution authority.
- Resolve every requested Omen ID from canonical static data.
- Validate that the base currency row is already executable-admitted.
- Validate that each Omen targets that currency’s operation family.
- Compile effect dimensions into one immutable resolved plan.
- Fail closed on unknown, non-admitted, incompatible, duplicate, or unsupported combinations.

## 2. Effect dimensions

| Dimension | Plan field | Load-bearing application point |
|---|---|---|
| Add count | `add_count_override` | accepted sequential ordinary-add executor |
| Add side | `add_side_filter` | legal weighted add pool before each affected draw |
| Removal side | `removal_side_filter` | accepted removable/feasible-removal pool before selection |
| Removal selector | `removal_selection_policy` | after fractured/eligibility/side filtering, before uniform selection |

Same-dimension effects are mutually exclusive. Different dimensions may compose only through a pinned compatibility matrix. Compatibility is validated, never inferred from list order.

## 3. Accepted-kernel reuse

- Exalted-like: accepted ordinary weighted add; Greater Exaltation repeats it on a private working state and rebuilds the pool.
- Annulment: accepted fractured-protected removable-instance pool, then optional side filter.
- Chaos-like: accepted removal pool, then optional side/Whittling selection; post-removal add remains the accepted branch-state rebuild.
- Perfect Essence: accepted terminal-feasible removal pool first, then optional Crystallisation side filter; guaranteed modifier installation remains unchanged.

No Omen reimplements legality, capacity, family/group conflict, modifier indexing, weighting, canonical state, exact mass, or replay.

## 4. Atomicity and no-transition

- Empty filtered pool: no-transition/no-consumption; original state unchanged.
- Greater Exaltation: both adds succeed or the operation and Omen have no transition/consumption in the project model.
- Chaos and Perfect Essence remain atomic under their already accepted contracts.
- A modifier never turns a failed base operation into a partial state.

## 5. Evidence and diagnostics

Every resolved plan and failure should report currency ID, Omen IDs, compatibility dimensions, current-state digest, pool digest, selection policy, seed/run ID where applicable, and the fail-closed reason. Public docs remain numeric-free.
