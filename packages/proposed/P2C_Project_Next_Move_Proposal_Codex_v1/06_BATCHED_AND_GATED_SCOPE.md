# Batched and Gated Scope

## What should be batched

Batch these in the next design wave:

1. Operation-admission framework.
   - One reusable checklist for future operation admission.

2. First operation candidate selection.
   - Recommend Annulment.
   - Explain why Chaos, Perfect Essence, Jawbone, and Reveal are deferred.

3. Annulment design contract.
   - Removal pool use.
   - Exclude fractured modifiers.
   - Uniform installed-instance selection.
   - No-transition behavior when removal pool is empty.
   - Replay/trace requirements.
   - Exact/oracle expectations.
   - Negative-control cases.

4. Audit package pattern.
   - Required files.
   - Required read receipts.
   - Required checks.

Why safe:

- design-only;
- no new executable mechanics;
- reconstructible from existing repo artifacts;
- automatically testable after later implementation;
- truth-neutral until ChatGPT/User acceptance.

## What must stay gated

Separate gates remain required for:

- Annulment implementation;
- Annulment acceptance as executable;
- Chaos implementation;
- Perfect Essence implementation;
- Jawbone/Reveal implementation;
- any operation using unresolved source/provenance, MML, PD-013, or Lich assumptions;
- public numeric probability release;
- target success/user-facing outputs;
- optimizer/advice/ranking/economics/EV;
- automation/GitHub Actions;
- source/provenance closure;
- MML closure;
- PD-013 closure.

## Why this is not over-broad

The proposed wave does not implement a generic operation engine. It defines admission rules and one first candidate.

That is wide enough to avoid micro-gates, but narrow enough to keep executable scope closed until a later explicit implementation gate.
