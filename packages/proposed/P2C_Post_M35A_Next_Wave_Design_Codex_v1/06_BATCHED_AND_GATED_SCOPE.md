# Batched and Gated Scope

## What should be batched in M36 design

Batch these design topics:

1. Heterogeneous sequence contract
   - accepted operation ids only;
   - fixed operation list;
   - explicit step order;
   - no planner.

2. Chain state transition model
   - branch-specific state after each step;
   - per-step pool rebuild;
   - no-transition handling per step.

3. Exact/oracle model
   - path product across operation types;
   - exact rational representation;
   - terminal aggregation by canonical terminal state;
   - ceiling policy for tractability.

4. MC validation strategy
   - fixed seeds;
   - fixed sample tiers;
   - tolerance policy;
   - replay proof;
   - negative controls.

5. Diagnostics/replay requirements
   - step index;
   - operation id;
   - semantics version;
   - pre/post state hash;
   - pool digest/fingerprint;
   - selected candidate;
   - no-transition reason.

Why safe:

- all are design-level;
- all are reconstructible from accepted repo artifacts;
- all are automatically testable in a later implementation floor;
- none require new operation mechanics.

## What must remain gated

Separate explicit gates are required for:

- M36 implementation;
- chains longer than the accepted M36 implementation boundary;
- variable-length route planner;
- any new operation after Annulment;
- Annulment variants or Omens;
- Chaos, Essence, Fracture, Desecrate, Jawbone, Reveal;
- public numeric probability release;
- target success aggregation;
- optimizer/economics/advice/ranking;
- automation/GitHub Actions;
- SOURCE/PROVENANCE closure;
- MML closure;
- PD-013 closure.

