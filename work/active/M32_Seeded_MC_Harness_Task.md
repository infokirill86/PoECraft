# P2C M32 — Seeded Monte Carlo Harness over accepted ordinary_add only

task_id: M32_SEEDED_MC_HARNESS
task_type: implementation_sprint
source_agent: ChatGPT
target_agent: Codex
allowed_actions: implement seeded MC harness over accepted ordinary_add only; tests; docs; numeric-free public outputs
forbidden_actions: new executable mechanics; optimizer/advice/ranking; public numeric release; economics/EV; source/provenance/MML/PD-013 closure
expected_output: packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/

## Purpose

Implement the first seeded Monte Carlo harness for P2C, using only the already accepted ordinary_add mechanics.

M32 is the first MC implementation step after M31 policy. It must prove the harness can run deterministically under a fixed seed, share the same mechanics kernel as the exact engine, and enforce runtime invariants.

M32 is not oracle convergence acceptance yet. M33 will validate convergence against the exact oracle.

## Required context

Before acting, read:
- START_HERE.md
- CURRENT_STATUS.md
- Operating Manifest v4
- Participant Voice Charter
- GitHub Workflow Protocol
- M31 accepted policy / current status notes

## Core requirements

### 1. Shared mechanics kernel

Exact and MC must share one mechanics / pool / legality / weight layer.

M32 must not implement a second ordinary_add legality/pool/weight path just for MC.

Expected architecture:
- shared kernel builds the legal weighted outcome pool;
- exact engine enumerates the full weighted outcome set;
- MC engine samples one outcome from that same pool.

Include tests or clear evidence that both exact and MC paths call the same pool/legality/weight code for ordinary_add.

### 2. Deterministic PRNG and replay

Implement a named, deterministic, portable seeded PRNG policy.

Do not rely silently on an unstable language-default RNG without documenting algorithm/version risk.

Every run artifact must record:
- seed;
- sample count;
- model/data fingerprint;
- code/runtime version or commit reference if available;
- run_id;
- operation sequence identity;
- mode.

Same inputs + same seed + same model version must reproduce the same result.

### 3. Runtime invariants on every simulated run

Every simulated trajectory must assert:
- fractured suffix remains present and unchanged;
- prefix/suffix/total capacity is never exceeded;
- duplicate family/group legality is respected according to accepted mechanics;
- only accepted executable operations are used;
- mode remains explicit and unchanged;
- no unsupported operation is silently skipped.

Invariant violation = hard failure / defect status, not silent discard.

### 4. Known-answer micro-fixtures

Add tiny hand-checkable MC sampler fixtures, independent of the full game data, for example:
- two-outcome weighted pool;
- deterministic one-outcome pool;
- impossible empty-pool / invalid-pool behavior.

These are sampler sanity tests, not full mechanics proof.

### 5. Ordinary_add accepted-lane harness

Implement MC execution over the accepted ordinary_add lane only.

Scope:
- accepted initial fractured quarterstaff state;
- accepted ordinary_add operation semantics;
- accepted modes as currently represented;
- no new operation mechanics.

M32 may produce internal MC estimate artifacts, but public docs must stay numeric-safe and clearly marked as internal development output, not public release.

### 6. Numeric and public boundary

No public numeric release.
No optimizer/advice/ranking.
No target recommendation.
No EV/economics/budget.
No server-truth framing.

Internal MC artifacts may contain estimates only if labeled as project-model internal MC outputs with seed/sample/uncertainty metadata. Public summaries should prefer statuses/counts/hashes and no showcased probabilities.

### 7. Tests

Add tests for:
- same seed replay gives identical output;
- different seed can produce different trajectory/sample sequence where applicable;
- runtime invariants fire on malformed states/unsupported operations;
- known-answer micro-fixtures behave as expected within configured tolerance or exact deterministic behavior;
- shared kernel proof for ordinary_add;
- public/default outputs do not leak numeric values;
- forbidden operation / optimizer / advice requests fail closed.

### 8. Documentation

Include concise docs:
- what M32 implements;
- what it does not implement;
- how to run the MC smoke test;
- how seed/replay works;
- why exact oracle validation is deferred to M33;
- known limitations.

## Required output structure

Place result under:

packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/

Recommended files:
- 00_README_FIRST.md
- 01_IMPLEMENTATION_SUMMARY.md
- 02_SHARED_KERNEL_REPORT.md
- 03_SEED_REPLAY_AND_PRNG_REPORT.md
- 04_RUNTIME_INVARIANTS_REPORT.md
- 05_TEST_AND_SMOKE_REPORT.md
- 06_M33_ORACLE_CONVERGENCE_NEXT.md
- runtime/code changes under src/ or runtime/ matching repo convention
- tests
- examples/fixtures if needed
- PACKAGE_MANIFEST.md
- SHA256SUMS.txt

Do not include old ZIPs or bulk historical artifacts.

## Acceptance expectations

M32 can be considered ready for Claude audit if:
- MC harness runs over accepted ordinary_add only;
- seed replay is deterministic;
- runtime invariants are enforced;
- shared-kernel evidence exists;
- micro-fixtures pass;
- public outputs are numeric-safe;
- no optimizer/advice/new mechanics are opened.

## After completion

Update work/active/ACTIVE_TASK.md:

status: ready_for_claude
next_actor: claude
result_path: packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/
builder_summary: concise summary

Then commit and push.
