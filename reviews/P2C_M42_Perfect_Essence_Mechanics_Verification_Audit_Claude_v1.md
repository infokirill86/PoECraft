# M42 Perfect Essence Mechanics Verification Audit (Claude)

audit_id: `P2C_M42_Perfect_Essence_Mechanics_Verification_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M42_Perfect_Essence_Mechanics_Verification_Codex_v1/`
observed_repo_head: `128f2c9d496169c898329ecdbd42b3b0c317cf62`
observed_active_task_sha: `440d34f025fb13361ba3167d712857c4313f1af84aab76c488adf7f000fac6cb`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Verification only; two probability-affecting mechanics decisions are genuinely ChatGPT/Kirill's to make before any M42-A runtime.

---

## Plain-language summary
This checks Perfect Essence before we build it. A Perfect Essence works on a yellow (Rare) item: it **removes
one modifier and then adds one guaranteed modifier**. The good news: the six staff rows are real, fully
described, and match our data. The honest news — and the whole point of this package — is that **two rules
genuinely can't be pinned from official sources**, and both change the odds, so they're yours (and GPT's) to
decide, not something to quietly bake in:
1. **Which mod gets removed when the guaranteed side is full.** If the guaranteed mod is a prefix and the item
   already has 3 prefixes, does the game only remove prefixes (to make room), or can it waste the currency
   removing a suffix and do nothing? Players report it makes room — so removal is probably limited to
   "removals that leave space." That changes the exact probabilities.
2. **Whether Perfect Essence needs a totally clean item.** The current game rule is "one crafted modifier at a
   time." So the safe default is: only usable on an item with **zero** crafted mods (fail otherwise). Whether
   it can instead *replace* an existing crafted mod is not documented.
The package does the right thing: it recommends conservative defaults but explicitly hands both decisions to
you, and admits nothing. **Verdict: GO** on the verification — with the clear condition that these two
decisions must be made before any M42-A build.

## Verified against real bytes
- **Verification/design only.** No `src`/`data`/`config`/`tests` change since M41-A acceptance
  (`1a73d51..HEAD`). All six `perfect_essence` rows stay `admission_candidate` — nothing admitted.
- **Inventory is accurate.** Six rows (abrasion/flames/ice/electricity/battle/haste), rare→rare,
  `remove: uniform_installed_instance`; each guaranteed mod resolves in the runtime `modifier_index` (verified
  live). Correctly notes there is **no** prepared Perfect Seeking/Infinite row and refuses to invent one from
  external catalogs without a source gate.
- **Source discipline is honest.** Official 0.3.0 confirms the "remove random + guaranteed add" shape but not
  the removal domain/side-capacity handling; official 0.5 confirms the one-crafted-modifier rule but not
  replacement; community reports support capacity-constrained removal but are explicitly treated as supporting,
  not authoritative; PoE1 Essence is excluded as mechanically different. The current YAML's unconditioned
  uniform-removal wording is labeled an **unaccepted hypothesis, not proof** — not promoted silently.
- **Both open decisions are genuinely surfaced, not decided.** Docs 06/07 lay out the candidate models, state
  plainly "this recommendation is not accepted truth in M42," and list the exact ChatGPT/User decisions
  required before M42-A. Proposed atomic contract (doc 08) is sound: feasible removal pool → uniform select →
  isolated post-removal state → guaranteed install (no add-pool/weighted draw) → shared validation → atomic
  commit; empty feasible pool → no-transition/no-consumption before any draw; fractured protected.

## My participant view on the two decisions (for the gate — advisory, yours to ratify)
- **Removal model → I lean to the "feasible removal pool" (doc 07, option 3).** It is the only one of the three
  consistent with *both* the community reports of successful full-item use *and* atomicity (no
  remove-a-mod-then-do-nothing waste). Option 1 (uniform + opposite-side rollback) and option 2 (unusable when
  side full) each contradict observed behavior. Caveat: this is **project-model, server-unconfirmed** (primary
  wording is absent), and it **changes exact probabilities vs the current YAML**, so it needs your explicit
  ratification and a matching `operations.yaml` update at M42-A — it cannot ride in on the existing wording.
- **Crafted-capacity → I agree with conservative `crafted_count == 0` fail-closed for M42-A.** It matches the
  confirmed 0.5 one-crafted-modifier rule, fails closed, and doesn't over-claim a replacement mechanic.
  Replacement/repeat can be a separate later expansion **only** with verified evidence.

## Recommendation
**GO** on the M42 verification. Do **not** authorize M42-A until ChatGPT/User explicitly decide (a) the removal
feasibility model and (b) the crafted-capacity precondition — both change probabilities or applicability and
must be project-model decisions, recorded in `mechanics_evidence.yaml` as source-open, not derived from the
current YAML. Then one M42-A batch may implement all six rows through one shared remove-then-guaranteed-add
executor over the accepted M40-A/M41-A patterns. Omens/side filters stay a separate later layer.

## Remains proposed / not accepted / gated
- No M42 runtime/admission; six rows stay candidates. Perfect Essence removal/repeat model undecided; crafted
  replacement undecided; Omens/Whittling/side/desecrated, Lesser/Corrupted Essences, external non-inventory
  rows, Alchemy/Fracture/Jawbone/Reveal, longer chains, planner/optimizer/economics, public numbers — all
  closed. MML/SOURCE-PROVENANCE/crafted-capacity/PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `perfect_essence_mechanics_verification_audit`
- status: `advisory verdict — GO on verification; two probability-affecting decisions (removal feasibility, crafted-capacity) required from ChatGPT/User before M42-A`
