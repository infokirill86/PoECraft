# P2C M32 — Seeded Monte Carlo Harness over accepted ordinary_add

task_id: M32
task_type: implementation_floor
source_agent: ChatGPT/Codex/Claude contributions via accepted M31 policy
target_agent: Codex
allowed_actions: implement seeded MC harness over already-accepted ordinary_add only; tests; replay metadata; runtime invariants
forbidden_actions: new mechanics; optimizer/advice/ranking; public numeric release; source/provenance/MML/PD-013 closure
stop_triggers: cannot prove shared kernel with exact engine; seed replay not deterministic; invariants cannot be enforced; MC requires unaccepted operation semantics
expected_output: one M32 result package / branch delta with tests and lean audit request
related_artifacts: Operating Manifest v4; START_HERE; CURRENT_STATUS; M31 accepted policy

## Objective
Build the first seeded Monte Carlo harness over accepted ordinary_add only. Exact and MC must share the same mechanics/pool/legality/weight kernel and differ only in enumerate-vs-sample.
