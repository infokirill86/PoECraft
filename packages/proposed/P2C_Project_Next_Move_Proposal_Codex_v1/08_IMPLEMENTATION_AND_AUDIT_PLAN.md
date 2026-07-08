# Proposed Implementation and Audit Plan

## If this proposal is accepted

Next task should be:

```text
M35 Operation Admission Framework and Annulment Candidate Design
```

Still design-only.

## M35 design deliverables

Required deliverables:

- operation admission checklist;
- operation handler acceptance criteria;
- source/project-policy label requirements;
- exact/oracle proof requirements;
- seeded MC proof requirements when stochastic;
- replay/debug trace requirements;
- no-transition/failure policy requirements;
- negative-control requirements;
- Annulment candidate design;
- deferred-operation rationale.

## Later M35-A implementation floor

Only after M35 design audit and ChatGPT/User authorization:

```text
M35-A Annulment Runtime Admission
```

Expected implementation evidence:

- exact/oracle removal pool behavior;
- uniform installed-instance removal;
- fractured exclusion;
- empty removal pool no-transition;
- deterministic replay;
- negative-control failure proof;
- no public numeric probability release;
- regression that accepted `ordinary_add` behavior remains unchanged.

## Claude audit plan

Claude should audit:

- whether operation admission criteria are sufficient;
- whether Annulment is the right first candidate;
- whether any source/provenance/MML/PD-013 closure is being smuggled in;
- whether implementation is still forbidden until a later gate;
- whether the plan reduces micro-steps without becoming over-broad.

## Stop triggers

Stop if:

- implementation is requested before admission design is accepted;
- a new operation would become executable without a separate gate;
- source/provenance closure is needed;
- public numeric output is requested;
- optimizer/economics/advice appears;
- automation is requested.
