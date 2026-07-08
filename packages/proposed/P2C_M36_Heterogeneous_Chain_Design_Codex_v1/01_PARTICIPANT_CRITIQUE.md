# Participant Critique

## Is M36 heterogeneous-chain design the right next move?

Yes, with a tight design-only boundary.

The project should not jump directly to implementation, but M36 design is the right next conceptual move after the operation-runtime admission metadata floor.

Reason:

- The simulator now has two accepted executable capabilities: accepted `ordinary_add` and accepted base Annulment.
- The metadata floor makes runtime admission explicit, so the chain layer can fail closed instead of accidentally pulling in active catalog rows.
- A real crafting simulator needs stateful operation composition. One-step evidence is not enough.
- Chain design over already accepted operations improves simulator usefulness without expanding source truth or operation scope.

## Why not next operation admission first?

Next operation admission is valuable, especially Chaos later. But admitting another operation before defining the chain contract would increase breadth without solving composition.

Chaos-like operations are themselves remove-then-add compositions. Designing accepted-operation chains first gives the project a safer foundation for future composite operations.

## Risk of overbuilding

The weak version of M36 would become a generalized planner or abstract operation algebra. That would be premature.

The better boundary is:

- fixed operation sequence;
- branch-specific state transition after every step;
- legality/pool rebuild after every step;
- exact/oracle comparison where tractable;
- MC/replay diagnostics where exact scales poorly;
- no route choice, ranking, economics, or advice.

## Final critique

M36 should proceed as design-only now. The next implementation should be M36-A, limited to two-step heterogeneous chains over accepted `ordinary_add` + accepted base Annulment.
