# Design Contract and Pinned Scope

## Goal

Define M34-B as MC hardening for short sequences over accepted `ordinary_add` only.

M34-B should verify that repeated accepted `ordinary_add` steps behave correctly when the state changes between steps.

## Pinned M34-B1 contract

M34-B1 should use:

- operation family: accepted `ordinary_add` only;
- sequence length: exactly two steps;
- step 0 operation: `ordinary_add`;
- step 1 operation: `ordinary_add`;
- operation semantics version: accepted ordinary-add semantics only;
- pool builder: accepted ordinary-add pool builder only;
- state transition: accepted ordinary-add state transition only;
- seeds: reuse the accepted M34-A deterministic seed set unless a later gate pins a replacement;
- sample tiers: reuse the accepted M34-A sample tiers unless a later gate pins a replacement;
- tolerance shape: reuse the accepted M34-A per-branch statistical envelope unless a later gate pins a replacement.

## Required validation properties

M34-B1 must validate:

- step ordering is deterministic and explicit;
- step 1 pre-state equals step 0 post-state;
- the pool for step 1 is rebuilt from the branch state;
- capacity, family, group, and static data invariants still hold after every step;
- replay with the same seed and run id reproduces the same trace;
- failure diagnostics identify where in the sequence the breach occurred;
- public reports remain numeric-probability-free.

## Explicit non-authorization

This design does not authorize:

- M34-B implementation;
- M34-B acceptance;
- full M34 acceptance;
- variable-length sequences;
- three-step implementation;
- new executable mechanics;
- operation expansion beyond `ordinary_add`;
- optimizer/advice/ranking/economics/EV;
- public numeric probability release;
- SOURCE/PROVENANCE, MML, or PD-013 closure;
- supervised auto-run or GitHub Actions.
