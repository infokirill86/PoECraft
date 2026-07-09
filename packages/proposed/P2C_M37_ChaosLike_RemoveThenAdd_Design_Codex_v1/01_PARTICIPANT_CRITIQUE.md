# Participant Critique

## Is Chaos-like remove_then_add the right next move?

Yes, with a tight boundary.

After M36-A, the engine can compose accepted `ordinary_add` and base Annulment in fixed two-step chains. A Chaos-like operation is the next useful design target because it is not just another chain-hardening exercise: it starts turning accepted primitive behavior into a real game-facing crafting operation candidate.

## Why not longer chains first?

Longer fixed chains would mostly harden infrastructure that already proved its basic shape in M36-A. Useful later, but lower project value right now than designing the next real operation admission.

## Why not implement Chaos immediately?

Chaos-like runtime admission changes executable operation scope. It needs a design/audit gate first because it combines removal, branch-specific add-pool rebuild, atomic failure handling, and operation-row admission status.

## Better boundary

The safer boundary is:

- M37: design-only, covering the remove_then_add primitive and Chaos-like candidate semantics.
- M37-A later: base Chaos-like runtime only, no Omens, no Whittling, no Greater/Perfect MML variants unless explicitly authorized.
- Later gates: Greater/Perfect Chaos MML modes, Omen/Whittling variants, and route usage.

This keeps momentum toward the simulator without turning design work into premature runtime expansion.

