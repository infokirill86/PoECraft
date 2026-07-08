# M34 Scope and Non-Scope

## M34 goal

Define M34 as Monte Carlo hardening beyond M33, still over accepted `ordinary_add` only.

## In scope

M34 should validate:

1. Multi-seed convergence behavior.
   - Run the accepted M33 statistical convergence checks across a fixed seed set.
   - Use predeclared seed list, sample tiers, tolerance, and pass/fail rule.
   - Report pass/fail and diagnostic metadata, not public probability values.

2. Multi-step / sequence validation.
   - Exercise short sequences composed only of accepted `ordinary_add`.
   - Rebuild pools after each step through the same accepted kernel.
   - Check replay determinism and terminal-state consistency.
   - Keep sequences artificial/project-model and clearly labeled if no real operation route implies them.

3. Replay/debug diagnostics.
   - Ensure failures identify seed, run id, sample tier, step id, pool digest, selected key, terminal hash, and invariant that failed.
   - Keep diagnostics enough for deterministic reproduction.

4. Failure reporting.
   - Fail loudly on tolerance breach, seed instability, pool mismatch, replay mismatch, invariant failure, or forbidden scope entry.
   - Produce concise numeric-free public reports and quarantined/internal details only when needed.

5. Hardening before future operation expansion.
   - Prove ordinary-add MC foundation is robust enough that later operation expansion can reuse the same diagnostic pattern.

## Out of scope

M34 must not:

- add new executable mechanics;
- expand beyond accepted `ordinary_add`;
- implement new operation families;
- start optimizer/advice/ranking;
- add economics, EV, cost, budget, or expected-attempt decision layers;
- release public numeric probability values;
- claim server-truth probability;
- close SOURCE/PROVENANCE;
- close MML;
- close PD-013;
- enable supervised auto-run;
- add GitHub Actions.
