# P2C — Decisions

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
- 2026-07-07 (User): **Accept M32 seeded MC harness (Layer B)** as a passing milestone on Claude's GO
  audit (`reviews/M32_Audit_Claude_v1.md`). The GitHub baseline import (Layer A) is **NOT accepted**;
  it remains PROPOSED until required changes A1 (declare reproducible deps) and A2 (import M32
  load-bearing kernel tests + re-establish prior accepted package SHA/pin) are cleared via a separate
  audited baseline-hygiene delta (`M32_A1_A2_BASELINE_HYGIENE`). M33 does not start yet.
