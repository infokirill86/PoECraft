# P2C - CURRENT STATUS

last_updated: 2026-07-10

Keep this file tiny. Stable rules live in START_HERE.md and manifest/Operating_Manifest_v4.md.

## Where we are

- Operating Manifest v4: accepted operating baseline.
- Participant Voice Charter: accepted; folds into START_HERE / workflow.
- GitHub repo migration: Layer A runtime/data/config/schema/tool baseline is now accepted and pinned as the project-model GitHub baseline.
- Layer A provenance: imported from local origin working tree `Documents/GitHub/PoECraft`, byte-verified exact; no prior formal runtime package existed.
- M31 Monte Carlo policy: accepted after C-1 correction. M26-M30 is open/context only, not accepted source.
- M32 seeded MC harness (Layer B): accepted.
- A1/A2 baseline hygiene: accepted.
- Supervised auto-run protocol metadata: accepted as safe documentation-only metadata.
- M33-P0 oracle-convergence foundation: accepted.
- M33-P1 statistical convergence delta: accepted.
- Full M33 oracle-convergence validation: accepted as completed for accepted `ordinary_add` only.
- M34 MC hardening design/definition package: accepted as the plan.
- M34-A multi-seed single-step MC hardening: accepted as completed.
- ACTIVE_TASK_SCHEMA_V2: accepted as the workflow-hygiene dispatcher standard; `ACTIVE_TASK.md` is routing/control only, with standing boundaries referenced from `manifest/GitHub_Workflow_Protocol.md`.
- M34-B design: accepted as the plan after Claude GO audit; M34-B1 implementation was authorized for exactly two accepted `ordinary_add` steps.
- M34-B1 two-step accepted-ordinary-add sequence hardening: accepted as completed after Claude GO audit.
- Project next-move proposal: accepted after Claude GO audit; default work should pivot from more `ordinary_add` hardening toward controlled admission of the first new real operation.
- M35 Operation Admission Framework + Annulment candidate design: accepted after Claude GO audit.
- M35-A Annulment Runtime Admission: accepted after Claude GO audit as base Annulment runtime only, project-model semantics only.
- Operation Inventory & Admission Reconciliation: accepted after Claude GO audit; active catalog metadata is now explicitly separated from executable runtime admission.
- Operation Runtime Admission Metadata Correction Floor: accepted after Claude GO WITH CHANGES audit; `runtime_admission_status` is the accepted explicit operation runtime-admission metadata field, and Claude's root `SHA256SUMS.txt` correction is accepted.
- M36 heterogeneous-chain design: accepted after Claude GO WITH CHANGES audit as design-only; M36-A has now been accepted separately, while full M36 and longer chains remain closed.
- Repo Integrity SHA Floor: accepted after Claude GO WITH CHANGES audit; deterministic root `SHA256SUMS.txt` updater and generated-manifest rule are accepted.
- M36-A heterogeneous-chain runtime: accepted after Claude GO WITH CHANGES audit; fixed two-step chains over accepted `ordinary_add` and base Annulment only.
- Repo-integrity local pre-push hook guard: accepted; every active working clone must run `git config core.hooksPath tools/hooks`.
- Agent role-packs implementation: accepted after Claude GO audit; root `AGENTS.md`, root `CLAUDE.md`, and `manifest/Agent_Role_Pack.md` are the compact persistent repo role files. Skills remain deferred.
- M37 mechanics verification: accepted after Claude GO audit; base removal is a uniform combined eligible-instance pool, base add is a combined generation_weight legal pool, and Whittling/side/desecrated behaviors are separate Omen layers. This is project-model policy only, not server truth.
- M37 Chaos-like remove-then-add design: accepted with the M37 mechanics correction.
- M37-A base Chaos-like Remove-Then-Add Runtime: accepted after Claude GO WITH CHANGES audit as base Chaos-like runtime only; base `chaos` is admitted as `accepted_executable_runtime`, project-model only.
- M38 Operation Resolver / Variant & Modifier Layer Design: accepted after Claude GO audit as design-only.
- M38-A Operation Resolver Skeleton: accepted after Claude GO audit as a single-operation resolver/admission seam over already accepted `ordinary_add`, base Annulment, and base Chaos-like runtime only.
- M39 Greater/Perfect + MML Design Verification: accepted after Claude GO audit as design/mechanics verification only; MML is a shared add-pool filter layer, Greater/Perfect variants should compose through resolver/filtering rather than hardcoded per currency, Greater/Perfect Chaos keeps base Chaos removal and applies MML only to the post-removal add pool, Essences are excluded from the MML-only batch, and MML remains project-model/source-open.
- M39-A MML Filter Interface: accepted after Claude GO audit as an interface floor only; resolver supports optional MML only for accepted `ordinary_add`, passes it into the existing add-pool path, and keeps unsupported MML usage fail-closed. Greater/Perfect rows remain not admitted and MML remains open as a broader mechanics/source topic.
- SHA256 Git-normalized updater/checker fix: accepted after Claude GO audit as repo-integrity tooling only; `update_sha256sums.py` and `check_sha256sums.py` hash tracked files from Git normalized/index bytes (raw working-tree bytes only for untracked files), closing the recurring CRLF/LF root `SHA256SUMS.txt` drift structurally.
- M39-B Greater/Perfect Exalted + Chaos runtime batch: accepted after Claude GO audit. Accepted rows are `greater_exalted`, `perfect_exalted`, `greater_chaos`, and `perfect_chaos`; they compose through shared ordinary-add/base-Chaos kernels with row-declared MML. Base `exalted` intentionally remains not admitted, and broader MML remains source-open.
- M40-A Rarity Progression Runtime: accepted after Claude GO audit for exactly ten rows: base/Greater/Perfect Transmutation, Augmentation, and Regal, plus base Exalted. The accepted shared executor builds Transmutation/Regal pools at target rarity and commits rarity plus modifier atomically. Normal and magic starts are now in active simulator scope. Fractured prefixes and suffixes are both valid; fractured protection remains mandatory.
- ACTIVE_TASK schema-v2 validator/pre-push guard: accepted as truth-neutral tooling. It validates frontmatter, mandatory fields, status/actor consistency, referenced paths, and malformed dispatcher state before publication.
- M41 Next Operation Wave Design: accepted after Claude GO audit.
- M41-A Greater Essence Quarterstaff Runtime: accepted after Claude GO audit for exactly eight rows: Abrasion, Flames, Ice, Electricity, Battle, Haste, Seeking, and Infinite. One shared deterministic executor performs atomic Magic-to-Rare plus the row-declared canonical guaranteed modifier, preserving existing/fractured modifiers and using no random draw. General crafted-capacity semantics remain source-open/unverified.
- M42 Perfect Essence Mechanics Verification: accepted after Claude GO audit. The repo contains six prepared quarterstaff rows.
- M42-A Perfect Essence Quarterstaff Runtime: accepted after Claude GO audit for exactly six rows: Abrasion, Flames, Ice, Electricity, Battle, and Haste. The accepted project model selects uniformly over terminal-feasible non-fractured removals, installs the canonical guaranteed modifier atomically, and temporarily requires `crafted_count == 0`. Replacement, stacking, repeat application, Astrid/rune capacity, and broader crafted-capacity remain source-open.

## Next gate

- ChatGPT/User decides the next operation or modifier wave. No later mechanics/runtime wave is open.
- Perfect/Lesser/Corrupted Essences, multi-Essence capacity semantics, Whittling, Omens, Alchemy, other operations, public numeric release, optimizer/economics/advice, automation, and boundary closure remain closed until separate explicit ChatGPT/User gates.

## Not authorized / still open

Alchemy; Perfect/Lesser/Corrupted Essences; multiple-Essence stacking/replacement/capacity semantics; Whittling runtime; Omen runtime; side/desecrated modifier layers; Fracture/Desecrate/Jawbone/Reveal; other operation variants; Annulment variants/omens; heterogeneous operation chains beyond accepted M36-A fixed two-step scope; optimizer/advice/ranking; economics/EV; public numeric release; server-truth claims; source/provenance closure; broader MML closure; PD-013 closure; MC execution of unaccepted operations.
