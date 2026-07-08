# Boundary and Risk Report

## Boundary status

| Boundary | M34 design position |
|---|---|
| New executable mechanics | Forbidden |
| Operation expansion beyond accepted `ordinary_add` | Forbidden |
| Optimizer, advice, ranking | Forbidden |
| Economics, EV, cost, budget, expected attempts | Forbidden |
| Public numeric probability release | Forbidden |
| Server-truth claims | Forbidden |
| SOURCE/PROVENANCE closure | Forbidden |
| MML closure | Forbidden |
| PD-013 closure | Forbidden |
| Supervised auto-run enablement | Forbidden |
| GitHub Actions automation | Forbidden |

## Main design risks

1. Hidden operation expansion.
   - Risk: sequence tests may accidentally become a new operation model.
   - Control: sequence fixtures must state they are accepted-ordinary-add-only and constructed if applicable.

2. Numeric leakage.
   - Risk: convergence diagnostics may tempt public probability output.
   - Control: package reports stay numeric-release safe; detailed numeric internals are quarantined or omitted.

3. Overclaiming statistical proof.
   - Risk: multi-seed tests are stronger than M33 but still not server truth.
   - Control: labels must say project-model validation only.

4. Debug artifacts too weak.
   - Risk: a future failure cannot be reproduced.
   - Control: required diagnostic fields and replay instructions.

5. Scope creep into M34 implementation.
   - Risk: design package gets treated as authorization to implement.
   - Control: this package is audit-only; implementation requires separate ChatGPT/User gate.
