# P2C - Decisions

## Accepted strategic decisions

- P2C builds a PoE2 crafting simulator, narrow first: physical quarterstaff with fixed fractured crit suffix.
- Data is project-model accepted data, not server truth. Source/provenance blockers remain open.
- Exact rational engine remains oracle/benchmark for narrow lanes.
- Seeded Monte Carlo is the scalable future runtime direction.
- Exact and MC must share one mechanics/pool/legality/weight kernel.
- MC may execute only accepted operations.
- Broad operation expansion is deferred until MC foundation is validated.
- Optimizer/advice/ranking remains last and separately gated.
- GitHub becomes the shared workspace; chats become decision/review channels.

## Gate decisions

- 2026-07-07 (User): Accept M32 seeded MC harness (Layer B) as a passing milestone on Claude's GO audit (`reviews/M32_Audit_Claude_v1.md`). The GitHub baseline import (Layer A) remains proposed until A1/A2 hygiene and byte-verification are completed. M33 does not start yet.
- 2026-07-08 (User): Accept A1/A2 baseline hygiene as completed and accept supervised auto-run protocol metadata as safe documentation-only metadata.
- 2026-07-08 (User): Accept and pin GitHub baseline import Layer A as the project-model accepted GitHub runtime/data/config/schema/tool baseline. Rationale: import fidelity is proven against the actual local origin working tree `Documents/GitHub/PoECraft`; Claude verified 79 of 79 source files byte-identical, 0 differ, 0 missing; Codex folded the working-tree comparison into the package record; no prior formal runtime package existed and should not be chased. This does not claim server truth and does not close SOURCE/PROVENANCE, MML, or PD-013. M33 remains closed until explicit authorization.
- 2026-07-08 (User): Accept M33-P0 oracle-convergence foundation as a partial first rung after Claude GO WITH CHANGES. Do not accept full M33 and do not claim MC convergence is statistically proven. Authorize M33-P1 statistical convergence delta only: statistically derived per-branch tolerance, sample-count tiers, fixed confidence/divergence policy, and broader accepted-ordinary-add fixture. M34 remains closed.
- 2026-07-08 (User): Accept full M33 oracle-convergence validation as completed after Claude GO audit of M33-P1. Accepted scope: M33-P0 foundation partial, M33-P1 statistical convergence delta, and validation that the seeded MC harness converges against the exact/oracle layer for accepted `ordinary_add` only. This does not start M34, does not introduce new executable mechanics, does not authorize optimizer/advice/ranking/economics/EV, does not release public numeric probability values, and does not claim server truth. SOURCE/PROVENANCE, MML, PD-013, and future multi-seed/sequence/operation-expansion watchpoints remain open.
