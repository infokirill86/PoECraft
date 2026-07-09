# Package Manifest

package_id: `P2C_M37_Mechanics_Verification_Codex_v1`
package_type: `MECHANICS_VERIFICATION_PROPOSAL`
status: `proposed_for_claude_audit`
observed_repo_head: `e7497b5abf01a0a4f12ce0932082517bfd86afa8`
observed_active_task_sha: `ae5c3573c5298c2d303a66e2abc9607eb4edb287199fbf8c8b6c91c8de1393ad`

## Package files

| File | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | Entry point, read receipt, plain-language summary | Proposed package only unless accepted |
| `01_PARTICIPANT_CRITIQUE.md` | new | Required critique of previous M37 assumptions | Proposed package only unless accepted |
| `02_SOURCE_TABLE.md` | new | Source inventory and evidence status | Proposed package only unless accepted |
| `03_REPO_DATA_COMPARISON.md` | new | Compares repo data against source findings | Proposed package only unless accepted |
| `04_CONFIRMED_MECHANICS.md` | new | Records mechanics confirmed enough for project-model decisions | Proposed package only unless accepted |
| `05_UNRESOLVED_MECHANICS.md` | new | Records remaining uncertainty and project-policy boundaries | Proposed package only unless accepted |
| `06_CANDIDATE_PROJECT_MODEL_DECISIONS.md` | new | Candidate decisions for ChatGPT/User after audit | Proposed package only unless accepted |
| `07_POE1_ANALOGY_NOTES.md` | new | Notes why PoE1 is support only | Proposed package only unless accepted |
| `08_RISK_AND_CORRECTION_TO_M37_DESIGN.md` | new | Explicit correction to previous M37 design | Proposed package only unless accepted |
| `09_RECOMMENDED_NEXT_GATE.md` | new | Next gate recommendation and stop triggers | Proposed package only unless accepted |
| `10_CLAUDE_AUDIT_REQUEST.md` | new | Claude audit request | Proposed package only unless accepted |
| `PACKAGE_MANIFEST.md` | new | File inventory and package metadata | Proposed package only unless accepted |
| `SHA256SUMS.txt` | generated | Package integrity hashes | Proposed package only unless accepted |

## Repo files changed outside package

| File | Status | Include reason | Future location |
|---|---|---|---|
| `CURRENT_STATUS.md` | updated | Records M37 mechanics verification proposed for Claude audit | Current status |
| `ledger/DECISIONS.md` | updated | Records ChatGPT/User authorization of mechanics verification | Decisions ledger |
| `work/active/ACTIVE_TASK.md` | updated | Routes next actor to Claude audit under schema v2 | Live dispatcher |
| `SHA256SUMS.txt` | generated | Root repository integrity hashes | Repo root |

## Explicit non-contents

This package does not include:

- runtime implementation;
- tests for Chaos runtime;
- data semantics changes;
- accepted runtime admission for Chaos;
- public numeric probability values;
- optimizer/economics/advice;
- SOURCE/PROVENANCE, MML, or PD-013 closure.

