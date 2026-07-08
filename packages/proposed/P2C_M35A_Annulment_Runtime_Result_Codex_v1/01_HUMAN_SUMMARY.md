# Human Summary

M35-A adds the first proposed runtime operation beyond accepted `ordinary_add`: base Annulment.

In plain terms: Annulment removes one removable modifier from the item. The protected fractured modifier is never allowed into the removal pool. If the item has nothing removable, the operation explicitly does nothing and leaves the item unchanged.

Why this matters:

- P2C moves from a one-operation simulator toward a real crafting simulator.
- The implementation is narrow: only Annulment, no general operation engine.
- It reuses the existing shared removal-pool builder instead of inventing a parallel removal algorithm.
- It keeps exact/oracle and MC behavior auditable.

What changed:

- Added `src/p2c_engine/monte_carlo/annulment.py`.
- Exported Annulment harness symbols from `src/p2c_engine/monte_carlo/__init__.py`.
- Added `tests/monte_carlo/test_m35a_annulment_runtime.py`.
- Updated status/ledger files to record M35 design acceptance and M35-A implementation authorization, not M35-A acceptance.

What remains proposed:

- Annulment runtime is proposed for Claude audit.
- Annulment is not accepted as executable until Claude audit and ChatGPT/User gate.
- SOURCE/PROVENANCE, MML, and PD-013 remain open.

Who is next:

- Claude audits this package.

Human decision required:

- Yes. After Claude audit, ChatGPT/User must decide whether to accept M35-A.

