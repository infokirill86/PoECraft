# Acceptance Criteria and Non-Goals

## Proposed M34-B1 acceptance criteria

M34-B1 should be eligible for Claude audit only if:

- contract pinning is documented before execution;
- all executed operations are accepted `ordinary_add`;
- sequence length is exactly two;
- state linkage is verified between steps;
- branch-state pool rebuild is verified;
- legality rebuild after step 0 is verified;
- deterministic replay passes for pinned seeds and run ids;
- exact/oracle comparison passes for tractable fixtures;
- negative-control failure proof is present;
- public reports contain no public numeric probability release;
- result package includes read receipts for repo HEAD and exact `ACTIVE_TASK.md` bytes acted on.

## Not enough for acceptance

The following would not be enough:

- single-step-only checks repeated under a different name;
- building a second pool for display while MC masses use a stale pool;
- checking terminal hashes without checking step linkage;
- replaying one seed only;
- passing without a negative-control failure path;
- silently skipping exact/oracle comparison.

## Non-goals

M34-B1 is not:

- a general sequence planner;
- an optimizer;
- advice or route guidance;
- economics/EV/cost/budget work;
- operation expansion;
- public probability release;
- server-truth validation;
- SOURCE/PROVENANCE closure;
- MML closure;
- PD-013 closure.

## Human gate requirement

Even if Claude audits this design with GO, implementation still requires explicit ChatGPT/User authorization.
