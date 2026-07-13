# Implementation Map

| File | Change | Why |
|---|---|---|
| `src/p2c_engine/monte_carlo/bounded_branching.py` | New finite-DAG request model, strict success classifier, closed predicate registry, validation, exact traversal, seeded traversal, replay, diagnostics and aggregation | Implements M48-A without adding crafting mechanics |
| `src/p2c_engine/monte_carlo/bounded_sequence.py` | Exposes a small accepted-step composition seam and structured step-ceiling signal | Lets M48-A reuse M43-A resolution/execution instead of copying operation logic |
| `src/p2c_engine/monte_carlo/__init__.py` | Exports M48-A public contracts | Makes the proposed evaluator importable through the package API |
| `tests/monte_carlo/test_m48a_bounded_branching_runtime.py` | Twenty-one focused contract, parity, exact, seeded, replay, firewall and negative-control tests | Provides reconstructible acceptance evidence |
| `CURRENT_STATUS.md` | Records M48 design accepted and M48-A proposed for audit | Status only; no self-acceptance |
| `ledger/ACCEPTED_ARTIFACTS.md` | Adds accepted M48 design row | Records the explicit ChatGPT/User design gate only |
| `ledger/DECISIONS.md` | Records M48 design acceptance and M48-A authorization/boundaries | Preserves the gate decision |
| `work/active/ACTIVE_TASK.md` | Hands the proposed implementation to Claude | Routing only |

## Reuse boundary

M48-A does not contain currency-specific pool construction, removal, add, rarity, Essence, Omen, Fracture, Jawbone, or Alchemy logic. `AcceptedStepTransition`, `enumerate_accepted_step`, and `sample_accepted_step` expose the already accepted M43-A composition result; the explicit M43-A executor registry remains authoritative and fail-closed.

No operation/catalog/omen data, success criteria, source evidence, admission status, or semantic fingerprint input changed.
