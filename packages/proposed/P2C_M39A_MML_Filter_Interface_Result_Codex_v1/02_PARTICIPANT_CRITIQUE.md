# Participant critique

## Boundary check

The safe M39-A boundary is narrower than "turn on Greater/Perfect".

Correct boundary:

- add an explicit MML interface to the resolver;
- prove it can narrow an add pool when supplied;
- prove Greater/Perfect runtime remains not admitted;
- keep MML source-open and project-model only.

Unsafe boundary:

- admitting Greater/Perfect Exalted or Chaos in the same commit;
- allowing MML through base Chaos catalog operation;
- treating MML as server-truth exact;
- mixing Essence, Whittling, Omen, or side/desecrated behavior into this floor.

## Design choice

Codex deliberately allowed explicit MML only for the `ordinary_add` engine primitive in M39-A.

Reason:

- `ordinary_add` already has an accepted MML-capable operation parameter and shared pool-builder support;
- Greater/Perfect catalog rows remain `admission_candidate` / `data_reference_candidate`;
- base Chaos is admitted, but Greater/Perfect Chaos is not, so MML on Chaos must wait for a separate admission gate.

This avoids a hidden admission path.

