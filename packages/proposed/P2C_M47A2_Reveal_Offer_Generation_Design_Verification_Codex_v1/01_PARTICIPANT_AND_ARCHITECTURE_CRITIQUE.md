# Participant and Architecture Critique

## Is Reveal the right next move?

Yes. M47-A1 now creates a canonical hidden placeholder, so base Reveal is the next operation that turns the Jawbone contour into a useful crafting capability. Moving to another operation now would leave the physical-quarterstaff route with an intentional dead end.

## Is Reveal plus Echoes one coherent implementation batch?

They share one architectural kernel but should not be admitted together yet.

- Base Reveal needs a deterministic contract for D3-D5 before implementation.
- Echoes is a control layer over that generator: initial offer set, optional discard, one rerolled set.
- Public wording confirms one reroll, but player reports conflict on whether Ancient Jawbone MML and other stored constraints survive that reroll.

Recommended boundary:

1. Design the shared generator and Echoes seam now.
2. After explicit D3-D5 decisions, implement and audit base Reveal only.
3. Verify Echoes constraint persistence separately, then admit it through a later gate.

## Named-Lich and Necromancy modifiers

They belong in the same resolver architecture as filters/constraints on Jawbone and Reveal, but not in the base implementation batch. Necromancy changes placeholder side before Reveal. Named-Lich Omens change offer composition and therefore touch D3/D4. Their data shapes can be preserved, but execution remains separately gated.

## Material objection to the repository candidate YAML

The current YAML contains a complete sequential weighted algorithm, Lich guarantee model, display permutation, and fail-closed edge. Those are useful candidate specifications, not verified mechanics. Treating them as runtime truth would violate the source/conflict policy. This package keeps them explicitly proposed.
