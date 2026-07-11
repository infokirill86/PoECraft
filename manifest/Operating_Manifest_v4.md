# P2C Project Operating Manifest — ChatGPT v4

Status: accepted operating baseline. Acceptance details live in `ledger/ACCEPTED_ARTIFACTS.md`.
Scope: project process, roles, data policy, Monte Carlo direction, gate policy, public-output policy, and implementation workflow.
This document does not authorize Monte Carlo implementation, new executable mechanics, optimizer/advice, public numeric release, or closure of source/provenance, MML, or PD-013.

## 1. Project identity

P2C is a Path of Exile 2 crafting simulator/emulator project.

The long-term objective is to model item crafting as state transitions under crafting operations, then later support target evaluation, cost assumptions, budget analysis, and optimizer-like strategy suggestions with the user in control.

Current executable operations, item-state scope, and milestone state are deliberately
not enumerated in this stable manifest. Read `CURRENT_STATUS.md`,
`ledger/ACCEPTED_ARTIFACTS.md`, and the admitted runtime registry. The physical
quarterstaff route remains the primary product lane; its current start and scope
come from accepted configuration and ledgers rather than this file.

## 2. Roles

### Kirill / User

Final coordinator and product owner.

Kirill owns:
- project priorities;
- gameplay relevance and real crafting goals;
- human-in-the-loop decisions;
- final acceptance of project baselines and milestones;
- decisions that require gameplay judgment.

### ChatGPT

Project lead / integrator / synthesis layer.

ChatGPT owns:
- route planning;
- synthesis across Codex and Claude outputs;
- acceptance recommendations;
- prompt/package preparation;
- scope control;
- concise human explanations for Kirill.

### Codex

Implementation and packaging executor.

Codex may implement code, produce packages, draft local blueprints/reviews/package structures when requested, and run local validations. Codex outputs remain proposals/evidence until ChatGPT/User acceptance.

### Claude

Independent external auditor.

Claude's value is independent reconstruction/execution, not process rubber-stamping. Claude audits packages, checks boundaries, and finds required changes. Claude audit verdicts are advisory; acceptance remains with ChatGPT/User.

## 3. Data policy

Project-model accepted data is the working truth for the model.

It is not server truth.

All project data remains:
- versioned;
- pinned;
- source-labeled;
- discrepancy-managed;
- bounded by open source/provenance limitations.

If trusted sources disagree or source/version compatibility is unclear, stop and escalate to human review.

No output may be framed as guaranteed hidden GGG/server behavior unless a future separate source/provenance gate explicitly permits that claim.

## 4. Foundation validity seams

The core abstraction is valid:

```text
item = state on a base with installed mods and capacity
currency/operation = transition on that state
probability = mass over reachable states
target success / attempts / costs / economics = derived layers
```

Three seams must be re-checked as the project expands:

1. Data and mechanics correctness are the ceiling. Perfect math over wrong data or wrong mechanics gives confidently wrong answers.
2. State-model completeness must be checked before each new mechanic. If a mechanic cannot be represented by the current state model, extend the state model first.
3. Fixed-plan evaluation is not adaptive strategy optimization. Current layers evaluate explicit plans. Adaptive strategy / stop-reroll-branch policy is a future modeling step.

## 5. Exact engine and Monte Carlo strategy

### 5.1 Exact engine role

The exact rational engine is retained as an oracle, benchmark, regression suite, and narrow-lane proof system.

It is not discarded.

Use exact enumeration when it is practical and load-bearing. Use it for:
- oracle validation;
- regression fixtures;
- mass-conservation checks;
- terminal-state canonicalization;
- deterministic equivalence checks;
- MC convergence validation.

### 5.2 Monte Carlo role

Seeded Monte Carlo is the future scalable runtime direction for longer paths, broader operation coverage, and strategy-scale exploration.

MC must be deterministic under seed:

```text
same inputs + same seed + same model version = same result
```

MC is not a loose replacement for exact rational discipline. It must be introduced through a formal policy and validation ladder.

### 5.3 MC statistical contract

Before MC is accepted as a runtime estimator, the project must define:
- PRNG algorithm;
- seed format and persistence;
- run identity;
- sample count policy;
- per-output-type error tolerance;
- confidence interval method;
- convergence criteria;
- stopping rule;
- replay artifact;
- exact-oracle comparison plan where available;
- public-output policy for estimates and uncertainty.

MC output should not emit bare probability estimates. Estimates require run metadata, seed, sample count, and uncertainty metadata.

### 5.4 Proportional MC rollout

The minimal contract required to start the MC harness is:
- deterministic seed/replay;
- sample count recorded;
- invariant checks;
- exact oracle comparison where available;
- per-output-type tolerance target;
- numeric/public-output boundary.

The fuller statistical contract in section 5.3 is the target required by MC acceptance, not necessarily a blocker for the first harness prototype.

### 5.5 Exact and MC share one mechanics layer

Exact and MC must share the same operation mechanics, pool construction, legality, and weight layer.

They may differ only in outcome resolution:

```text
exact engine = enumerate all outcomes
MC engine = sample one outcome from the same accepted pool
```

If exact and MC use separate mechanics implementations, oracle convergence loses meaning because the same mechanics error can exist in both.

### 5.6 Oracle frontier

Exact-oracle convergence validates the MC harness where exact answers exist.

It does not prove new operation mechanics are correct.

For mechanics beyond the exact oracle frontier, validation must use:
- hand-computable micro-cases;
- invariant checks;
- conservation checks;
- impossible-outcome checks;
- capacity/fracture invariant checks;
- property-based tests;
- corroboration against independent tools where available, as evidence, not proof.

### 5.7 Disagreement rule

If MC and the exact oracle diverge beyond the accepted per-output-type tolerance, stop and treat it as a defect requiring human review. Do not ship the estimate or operation as accepted.

Potential causes include MC bug, mechanics bug, data issue, or oracle mismatch.

## 6. Step-size policy

Use large waves by default when safe.

Batch when the work is:
- reconstructible from accepted inputs;
- automatically testable;
- truth-neutral;
- not changing executable mechanics;
- not changing accepted fractured-modifier behavior;
- not releasing public numeric values;
- not moving into optimizer/advice.

Gate separately when the work:
- introduces or changes executable mechanics;
- touches fractured behavior;
- opens a new numeric floor;
- releases public numeric values;
- changes data/source/provenance policy;
- changes MML or PD-013 status;
- moves toward optimizer/advice/ranking;
- creates silent-corruption risk that automatic checks would not catch.

One-line test:

```text
If wrong, would automatic checks catch it, and does it change accepted truth?
Catchable + truth-neutral -> batch large.
Silent-corruption or truth-changing -> separate gate.
```

Large waves may skip intermediate external audits, but no wave output becomes accepted without final review of the produced delta/package. Wave mode never lowers the validation floor.

## 7. Audit style

Use lean-audit mode by default.

Claude should still:
- verify SHA/package integrity;
- independently reconstruct or execute when applicable;
- enforce numeric-free public surfaces;
- check boundary preservation;
- keep verdict advisory only.

But audit reports should be concise unless material defects are found:
- verdict first;
- what was executed/reconstructed;
- required corrections;
- material risks/limitations;
- final recommendation.

Routine PASS prose should be omitted unless it affects the decision.

## 8. Operation admission policy

Only accepted executable operation semantics may be used by runtime execution or MC.

The changing accepted executable inventory is defined by the accepted ledger and
the admitted runtime registry. Do not copy that inventory into this stable
manifest. Catalog/reference presence is not executable permission.

New executable operation mechanics require their own gate, especially:
- stochastic pool operations;
- weighted operations;
- removal/replacement/reroll operations;
- fracture-related operations;
- Reveal/Lich/Abyssal/Whittling/Erasure or similar mechanics;
- any mechanic that changes terminal states or terminal probability.

For each new operation, first ask:

```text
Can this mechanic be fully represented as a transition on the current state model?
```

If not, extend the state model first.

MC may execute only already-accepted executable operations.

## 9. Public numeric release policy

Any public display of probability, MC estimate, attempt, cost, budget, EV, optimizer, or strategy metric values requires an explicit release gate unless a later accepted policy explicitly exempts that exact output class.

Internal numeric artifacts may exist under quarantine.

Public outputs must remain controlled by:
- source labels;
- mode identity;
- value type;
- model labels;
- not-server-truth framing;
- uncertainty metadata for MC estimates;
- explicit user/ChatGPT approval where required.

## 10. Economics and EV wording

Accepted expected-attempt evidence may remain as quarantined model evidence.

EV-as-decision, EV-as-ranking, or EV-as-advice remains forbidden until an optimizer/economics decision gate.

Single-plan quarantined economics has been accepted as an internal runtime capability. Public cost/economics value display and optimizer/advice remain separately gated.

## 11. Optimizer boundary

Optimizer is last.

Optimizer behavior includes:
- generating candidate plans;
- searching plan space;
- ranking plans;
- comparing plans;
- filtering by objective;
- recommending paths;
- presenting best/worst plans;
- budget strategy suggestions;
- EV/advice framing.

None of that is authorized by the manifest.

Optimizer requires separate high-risk blueprint, implementation gate, external audit, and human-in-the-loop policy.

## 12. Artifact and package hygiene

Accepted baselines and current-truth capsules supersede older packages.

Ordinary deltas must be pinned to their base and must not embed old packages.

No nested archives, old packages, or full project dumps unless explicitly justified as a full source/repro bundle.

Long prompts should be delivered as files, not pasted into chat.

One prompt file = standalone `.md`.
Multiple files = ZIP.

## 13. Reporting to Kirill

Default human summary format:

```text
What was done.
What it means for the project.
What Claude/Codex found that matters.
What the next step is.
```

Avoid routine SHA/file-count/PASS dumps unless requested.

## 14. Strategic sequencing

Current milestone direction is intentionally not hardcoded in this stable
manifest. Read verified `work/active/ACTIVE_TASK.md` for routing, `CURRENT_STATUS.md`
for the compact checkpoint, and `ledger/DECISIONS.md` for accepted pivots.

Cost, budget, optimizer, ranking, and advice remain separately gated regardless of
the current milestone sequence.

## 15. Non-goals of this manifest

This manifest does not authorize:
- Monte Carlo implementation;
- new executable mechanics;
- public numeric release;
- optimizer/advice;
- source/provenance closure;
- MML closure;
- PD-013 closure;
- server-truth claims.

## 16. Acceptance wording

Recommended acceptance label:

```text
P2C Project Operating Manifest v4
Status: accepted operating baseline
Scope: process, roles, data policy, Monte Carlo direction, gate policy, public-output policy, implementation workflow
Does not authorize: MC implementation, new mechanics execution, optimizer/advice, public numeric release, source/provenance closure, MML closure, PD-013 closure
```

## 17. Decision authority

Accepted-truth updates, milestone closure, operating baseline adoption, public release, and boundary closure remain reserved to ChatGPT/User/Kirill.

No Codex package or Claude audit self-accepts into project truth.
