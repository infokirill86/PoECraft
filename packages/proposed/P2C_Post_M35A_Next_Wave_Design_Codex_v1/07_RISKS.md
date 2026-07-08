# Risks

## Risk of moving too slowly

If the project keeps hardening isolated operations without connecting them, it risks becoming a polished test harness rather than a simulator.

Symptoms:

- many single-operation proofs;
- no useful crafting sequence;
- no branch-state story across different operation types;
- no progress toward target success or later optimizer.

Mitigation:

- choose M36 mixed accepted-operation chain design now;
- keep it design-only and accepted-ops-only.

## Risk of moving too fast

If the project adds Chaos, Essence, Jawbone, Reveal, or Annulment variants before proving accepted-operation composition, it risks expanding mechanics before the chain model can carry them.

Symptoms:

- isolated operation handlers;
- inconsistent no-transition semantics across operations;
- duplicated replay/diagnostic logic;
- harder future audits.

Mitigation:

- prove composition over `ordinary_add` + base Annulment first;
- keep additional operations behind admission gates.

## Risk of overbuilding M36

M36 could turn into a planner or generic optimizer if the boundary is not explicit.

Mitigation:

- fixed operation lists only;
- no route search;
- no ranking;
- no economics;
- no advice;
- no variable-length planning.

