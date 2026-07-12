# P2C M48 Next Independent Project Wave Design — Claude Audit

- Verdict: **GO** (design/direction only; authorizes no implementation)
- Auditor: Claude (external auditor-designer, advisory only; acceptance remains ChatGPT/User)
- observed_repo_head: `2d8f1f44ba9ad6955a65a6fb23fb1fe43dcc3a33`
- observed_active_task_sha256 (`work/active/ACTIVE_TASK.md` git-index bytes): `29a41c99f8f6f1e350fc95b561f2982af779422d86331acacc12ff61d9004767`
- Package: `packages/proposed/P2C_M48_Next_Independent_Project_Wave_Design_Codex_v1/`

## Scope audited

A next-wave direction proposal comparing candidate waves (Omen of Light, Echoes,
Putrefaction, revealed-Desecrated Fracture, Astrid/crafted-capacity, more fixed-length
sequence infra, and a bounded caller-authored **branching**-sequence evaluator) and
recommending the branching evaluator. GPT explicitly asked me to audit (a) whether the
selected boundary stays an evaluator rather than a planner, and (b) whether Omen of
Light or Astrid should be the next clean wave instead.

## Design-only confirmed

No `src/`, `tests/`, `data/operations.yaml`, `data/omens.yaml`, or mechanics change.
Only the package, `CURRENT_STATUS.md`, and two documentary ledger lines (recording the
M47-A2V acceptance and this M48 design authorization). Foundation validation PASS;
semantic fingerprint unchanged (`6e7bc414…`); root SHA PASS; 329 tests collected
(matches the package's 329-passed; 324 engine + 5 M47-A2V analysis tests). Repository
grounding in the package is accurate (35/37 operations accepted; only `install_astrid`
and `reveal_desecrated` non-admitted; 10/17 omens accepted).

## Q1 — Does the boundary stay an evaluator? Yes.

The recommended M48 evaluates a route that the **caller supplies completely**: "P2C
never proposes a node or edge." It reuses the accepted M43-A resolver/executor
registry, re-resolves each node from the actual branch state, conserves exact rational
mass, stops at honest ceilings (no renormalization, no hidden MC), and drives edges
only from a small registry of **named, versioned, deterministic, state-based**
predicates. It explicitly excludes route generation, action discovery, route
comparison, costs/economics/EV, ranking, "best" output, arbitrary expressions, cycles,
and unbounded retries. This is the honest generalization of M43-A from a linear tuple
to a bounded conditional DAG — still an evaluator, not the (gated-last) optimizer.

I concur with the boundary and its independence claim: it depends on none of D3-D5,
Reveal, Echoes, PD-013, or crafted-capacity, and monetizes the already-accepted
operation surface immediately.

## Q2 — Omen of Light or Astrid instead? No; the branching evaluator is correctly first.

- **Omen of Light is dependency-blocked**, not merely deferred: its value (next
  Annulment removes only Desecrated modifiers) requires a *revealed* Desecrated target
  state, which no accepted runtime can yet produce because Reveal (D4) is unaccepted.
  Correct to hold.
- **Astrid** is a legitimate but separate mechanics-verification wave: +1 crafted
  capacity is well-supported by wording, but replacement/removal persistence and its
  interaction with accepted Essence preconditions are open. It carries source/mechanics
  dependencies the branching evaluator does not.
- The branching evaluator is the only high-value candidate with **zero open
  mechanics/source dependencies**.

My independent view (as project participant, not just concurrence): the sequencing is
right for a second reason beyond "no dependencies." Building the evaluator substrate
now — while it is still strictly a policy *executor* — is the disciplined path toward
the eventual optimizer, because it forces us to get exact-mass, replay, branch-state
re-resolution, and predicate semantics correct on a caller-authored graph before any
layer ever *searches* over that graph. It keeps "execute a route" permanently separate
from "find a route," which is exactly the separation that will make later optimizer
output trustworthy. I'd suggest Astrid as the natural next *small* mechanics wave after
M48-A, and Omen of Light only once Reveal runtime exists.

## The one invariant to hold at the M48-A gate (routed to ChatGPT/User)

The success classifier (`TOP` / `ACCEPTABLE` / `NOT_SUCCESS` over
`config/success_criteria.yaml`) plus the predicate registry are the single place where
objective-function / optimizer creep could later enter, because a success class is
conceptually the seed of an objective. It is safe in M48 because it only drives
deterministic, caller-authored branches and never ranks or selects among routes. The
M48-A implementation gate must keep this firewall explicit: predicates stay
deterministic and state-based; **no predicate may ever return a score, probability,
cost, or ranking**, and the classifier may only *interpret* accepted criteria, never
invent a new success rule. The package already commits to all of this (risk table +
hard-stop triggers); I am elevating it as the invariant to verify at implementation.

## Checks

- `validate_active_task.py`: PASS. `check_sha256sums.py`: PASS.
  `validate_foundation.py`: PASS (fingerprint `6e7bc414…`, unchanged). 329 tests
  collected (design wave changed no code).

## Remains proposed / not accepted / gated

M48 authorizes no implementation. Separately gated: M48-A branching-sequence runtime;
D3-D5 and Reveal runtime; Echoes and Ancient-MML persistence; Omen of Light;
Putrefaction/multi-placeholder/corruption; Astrid/crafted-capacity and
repeat/replacement Essence semantics; revealed-Desecrated Fracture and PD-013; any
route generation / search / ranking / costs / economics / EV / advice / optimizer;
public numeric release; automation; source/provenance/MML/crafted-capacity closure.

## Findings

None blocking. GO as design/direction only, with the M48-A predicate-registry invariant
above carried forward to the implementation gate.
