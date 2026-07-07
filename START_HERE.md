# P2C — START HERE: Project Resume Kit (v2)

last_updated: `<set on commit>` · current gate: see `CURRENT_STATUS.md`

Purpose: the first file a new Claude / Codex / ChatGPT session loads to resume P2C. It is a
reconstruction aid, not memory, and **not a task authorization** — it orients the session; actual
work needs a current objective/prompt or explicit user instruction. For where the project stands
right now, read `CURRENT_STATUS.md` (this kit stays stable; volatile status lives there). Keep this
kit minimal (target under ~1200 words); grow it only on a real failure.

## 1. What P2C is
A Path of Exile 2 crafting simulator, deliberately narrow: one fixed base (physical quarterstaff)
with a fixed fractured crit suffix; affix capacity 3 prefixes / 3 suffixes. Model: item = state; a
currency = a stochastic operation (state transition); probability = mass over reachable states;
target success / attempts / cost / economics = derived. Long-term goal (built last, separately
gated): support strategy comparison and eventually optimizer-like policy search over crafting paths,
to a graded acceptance target, unbounded and within a user budget, with human decision ownership.
Data = project-model accepted truth, not server truth.

## 2. Engine direction
Exact rational engine = oracle / benchmark for narrow lanes. Seeded Monte Carlo = scalable
production engine (approximate but scales; deterministic under a fixed seed). Exact and MC MUST share
one mechanics / pool / legality / weight kernel, differing only in enumerate-vs-sample. Roadmap
(direction, not current status — see `CURRENT_STATUS.md`): M31 policy → M32 seeded MC over
ordinary_add → M33 oracle convergence → one real deterministic operation → M34 hardening → operation
breadth → cost/budget as distribution → optimizer (last).

## 3. Roles & collaboration model
- **Kirill (User):** product owner; game priorities; decides at gates; final acceptance.
- **ChatGPT:** architect / synthesis; big-plan design at forks; task authoring; plain-language summaries.
- **Codex:** builder / packager; ALSO critiques the task before building (not a blind executor).
- **Claude:** independent auditor; verifies by reconstruction / execution; ALSO contributes design.

Principle — full participants, not executors. Layered rigor: routine steps run on **Claude ⇄ Codex
mutual challenge**; forks (new mechanics, model changes, optimizer) add **ChatGPT architect** review;
Kirill approves at gates. Guard: mutual challenge fails if it becomes politeness — when everyone
agrees too easily on something high-stakes, red-team it or pull in the third head; anyone auditing
their own idea flags it.

## 4. Pre-task self-check (run before acting)
1. Does this change accepted truth / executable mechanics / the fractured-mod invariant / public numeric output? → separate gate.
2. If it were wrong, would an automatic check catch it? Is it reconstructible / testable?
3. Does the mechanic actually fit the current state model? If not, extend the model first.
4. Am I silently assuming the data / mechanics are correct? (that is the ceiling of correctness)
5. If there is a **material disagreement, unsafe assumption, or clear improvement — state it before acting.** Do not invent objections for routine, safe tasks.
6. Am I about to do something forbidden without a gate (optimizer / advice / new mechanic / public numbers / boundary closure)?

## 5. Two governance rules
- **Step size:** batch when reconstructible + auto-testable + truth-neutral; separate gate when it
  touches executable mechanics, the fractured invariant, public numbers, or moves toward
  optimizer/advice. Test: *"if wrong, would an auto-check catch it, and does it change accepted
  truth?"* catchable + truth-neutral → batch; silent-corruption or truth-changing → gate.
- **Process changes:** change the workflow or rules ONLY when a real, observed failure exposed a gap.
  Never expand process speculatively. This stops the audit-of-audits spiral.

## 6. Standing boundaries & authority
project-model, not server-truth; no public numeric release; no optimizer / advice / ranking /
EV-as-decision; no new executable mechanics (only `ordinary_add` is executable); the fractured
invariant is never modified; MC executes only accepted operations; source/provenance, MML, PD-013
remain open; costs are user assumptions, not market truth.
**Authority:** no package, audit, test result, report, Codex output, or Claude output self-accepts
into project truth. ChatGPT/User (Kirill) acceptance is required. Nothing auto-merges.

## 7. Where things live (target repo layout, once GitHub handoff is active)
- Operating Manifest v4 (full rules) — `/manifest`
- Accepted packages (audit from these bytes) — `/packages`
- Audits — `/reviews`
- This file & `CURRENT_STATUS.md` — repo root

If the layout is not present yet, verify against the local workspace artifacts and ask for the
current baseline package — do not assume missing folders are a project defect.

## 8. Communication
To Kirill: plain language, short; technical detail only on request. Long prompts as `.md` files, not
pasted into chat; avoid dumping raw code / PASS tables / SHA lists unless asked. (Full policy:
Operating Manifest v4.)

## 9. Honest limits
A new session is not the same session; this kit reconstructs, it does not remember. Models do not
follow written rules perfectly — the system is designed to survive that: the human gate (Kirill) and
the independent audit catch violations downstream. Safety rests on "violations get caught," not on
"everyone follows the manifest." Keep this kit minimal.

---
- author: `claude` (v2 folds Codex + ChatGPT review)
- document_type: `project_resume_kit`
- status: `active session-resume aid; not an implementation prompt; does not authorize new work`
