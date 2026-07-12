# P2C M48 Next Independent Project Wave Design

Status: **PROPOSED design - ready for Claude audit; no runtime implementation or new mechanics admission**.

## Plain-language conclusion for Kirill

P2C already knows how to execute a large set of currencies, Omens, Essences, Fracture, Jawbones, and fixed sequences. The immediate problem is no longer a shortage of individual buttons. The engine still cannot follow a route that says: "after this result, stop if the item is good enough; otherwise follow this prewritten recovery branch."

The recommended M48 wave is therefore a **bounded caller-authored branching-sequence evaluator**. The user supplies the complete finite route graph. P2C evaluates it; it does not invent, rank, improve, or recommend routes.

This wave is independent of unresolved Reveal sampling. It reuses accepted operations and exact/MC infrastructure, adds no crafting mechanic, and moves the simulator from fixed scripts toward realistic route evaluation without crossing into planner or optimizer work.

## Package map

- `01_PARTICIPANT_AND_ARCHITECTURE_CRITIQUE.md`
- `02_CURRENT_CAPABILITY_AND_MISSING_CAPABILITY_MAP.md`
- `03_CANDIDATE_COMPARISON.md`
- `04_SELECTED_M48_BOUNDARY_AND_RATIONALE.md`
- `05_OPEN_DEPENDENCIES_AND_SOURCE_EVIDENCE.md`
- `06_PROPOSED_BRANCHING_SEQUENCE_ARCHITECTURE.md`
- `07_RECOMMENDED_M48A_IMPLEMENTATION_BATCH.md`
- `08_SEPARATE_GATES_RISKS_AND_STOP_CONDITIONS.md`
- `09_CLAUDE_AUDIT_REQUEST.md`
- `10_READ_RECEIPT.md`
- `11_CHECKS.md`
