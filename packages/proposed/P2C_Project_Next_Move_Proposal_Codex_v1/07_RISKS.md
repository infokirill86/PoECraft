# Risks

## Risk of continuing infrastructure-only work

If P2C continues with only `ordinary_add` hardening:

- the system may become very robust around one operation but still not useful as a crafting simulator;
- each new operation will remain an ad hoc exception;
- project momentum may drift toward audit infrastructure rather than simulator capability;
- user-facing value remains delayed.

Mitigation:

- pivot to operation admission now;
- keep infrastructure work only when it directly supports operation admission.

## Risk of moving too early to new mechanics

If P2C implements a new operation without an admission framework:

- executable scope can expand without consistent proof;
- source/project-policy labels can be inconsistent;
- exact/MC/replay requirements can be under-specified;
- future operations can accumulate incompatible handlers;
- Claude audit becomes harder and more subjective.

Mitigation:

- create an M35 admission framework first;
- use Annulment as the first candidate only after the framework is audited.

## Risk of choosing the wrong first operation

Chaos or Perfect Essence may feel more route-relevant, but they introduce more moving parts.

Mitigation:

- choose Annulment first because it isolates removal semantics;
- use Chaos later to compose removal plus ordinary add after Annulment is proven.

## Risk of public-output drift

Once new operations are admitted, the temptation to show route probabilities increases.

Mitigation:

- keep public numeric release closed;
- keep reports status/count/hash oriented until a separate release gate.

## Risk of prompt-driven micro-stepping

The current workflow can ask for a small next step even when a wider design wave is safer.

Mitigation:

- require every major next-move prompt to include a project reality check and options comparison.
