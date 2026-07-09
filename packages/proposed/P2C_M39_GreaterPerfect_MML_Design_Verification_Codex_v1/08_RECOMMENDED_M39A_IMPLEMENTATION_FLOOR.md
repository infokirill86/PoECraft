# Recommended M39-A implementation floor

## Recommendation

Use M39-A for a narrow MML filter layer implementation, not full Greater/Perfect admission.

M39-A should be:

> Resolver MML filter support + fail-closed checks for non-admitted Greater/Perfect rows.

## Allowed M39-A scope

- Add an explicit MML filter field to resolved single-operation plans where the operation is already admitted or explicitly test-fixtured.
- Reuse existing `apply_family_mml` / ordinary add pool builder behavior.
- Add tests proving the resolver does not infer executability from `active_in_current_simulation`.
- Add tests proving Greater/Perfect rows fail closed unless separately admitted.
- Add fixtures for branch-specific MML application on a remove-then-add shape without admitting Greater/Perfect Chaos yet, unless a later gate explicitly authorizes admission.
- Keep public numeric output forbidden.

## Optional M39-B after M39-A audit

If M39-A passes, the next safe runtime admission floor could batch:

- `greater_exalted`;
- `perfect_exalted`;
- `greater_chaos`;
- `perfect_chaos`.

That later floor must still be explicit user-authorized runtime admission. It must not admit Transmutation, Augmentation, Regal, Essence, Omen, Whittling, or reveal behavior.

## Acceptance evidence for M39-A

M39-A should require:

- resolver-plan evidence showing MML values are compiled only through admitted operation paths;
- exact/oracle fixture evidence for MML-filtered add pools;
- branch-specific post-removal add-pool rebuild evidence for remove-then-add fixtures;
- fail-closed tests for non-admitted Greater/Perfect rows;
- checksum/status evidence;
- Claude audit request.

## Non-goals

- no Greater/Perfect runtime acceptance by default;
- no MML source closure;
- no Whittling/Omen runtime;
- no Essence runtime;
- no public probability release;
- no optimizer/economics/advice.

