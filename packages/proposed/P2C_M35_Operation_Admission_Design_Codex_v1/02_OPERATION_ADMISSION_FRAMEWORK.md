# Operation Admission Framework

## Design principle

Keep the framework lean and operation-anchored.

M35 must not create a generalized operation algebra. It should define the minimum repeatable checklist needed to admit one new operation safely, then apply that checklist to Annulment.

## Admission criteria for any new operation

A new operation may be proposed for runtime admission only when the design package defines:

1. Operation identity
   - operation id;
   - operation group;
   - accepted/project-model scope;
   - explicit non-server-truth label if source/provenance is not closed.

2. Input and output state contract
   - allowed item rarities/classes;
   - state fields read;
   - state fields written;
   - fields explicitly not touched.

3. Pool-builder dependency
   - exact builder or kernel function used;
   - whether it already exists;
   - whether it is load-bearing for probabilities;
   - fail-closed behavior if the builder cannot produce a valid pool.

4. Transition semantics
   - selected candidate unit;
   - state mutation;
   - no-transition behavior;
   - atomicity and no-consumption behavior for invalid transitions.

5. Exact/oracle proof shape
   - exact rational representation;
   - terminal identity and aggregation rule;
   - no-transition mass when applicable;
   - finite ceiling for enumeration.

6. MC proof shape, if stochastic
   - fixed seed set;
   - fixed sample tiers;
   - tolerance policy;
   - replay requirements;
   - negative controls proving the suite can fail.

7. Replay and trace requirements
   - operation id and semantics version;
   - input state digest;
   - pool digest;
   - selected candidate key;
   - output state digest;
   - no-transition reason, if any.

8. Boundary labels
   - PROJECT-MODEL BEHAVIOR ONLY;
   - NOT SERVER-TRUTH;
   - SOURCE/PROVENANCE REMAINS OPEN, unless separately closed;
   - MML status if relevant;
   - PD-013 status if relevant.

9. Regression protection
   - accepted `ordinary_add` tests must remain unchanged and passing;
   - new operation must fail closed when called outside accepted scope.

## Required gates

Each new operation needs separate gates:

1. design acceptance;
2. implementation authorization;
3. implementation audit;
4. acceptance/pinning decision.

No design package may self-accept runtime behavior.

