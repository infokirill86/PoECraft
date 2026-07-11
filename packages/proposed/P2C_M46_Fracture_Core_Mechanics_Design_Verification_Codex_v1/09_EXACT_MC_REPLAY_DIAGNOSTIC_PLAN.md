# Exact, MC, Replay, and Diagnostic Plan

## Exact/oracle

- enumerate one path per eligible installed-instance identity;
- assign equal canonical exact rational mass;
- mutate only the selected instance's fractured flag;
- aggregate canonical duplicate terminals;
- assert exact total mass conservation;
- fail closed on configured path/terminal ceiling overflow without truncation or hidden MC substitution.

## Seeded Monte Carlo

- use the same candidate builder and transition executor as exact evaluation;
- pin seeds, sample tiers, tolerance policy, and divergence rule before execution;
- compare sampled candidate/terminal behavior against exact results only inside quarantined evidence;
- expose only boolean/public-safe validation status outside quarantined numeric evidence.

## Replay and diagnostics

Replay must reproduce candidate-pool digest, selected instance key, post-state digest, and transition status from the same seed/run ID. Failures must identify precondition category, operation ID, item-state digest, candidate-pool digest when available, and whether consumption was suppressed.

Negative controls must prove that existing-fracture, fewer-than-four, Desecrated-state, missing canonical row, and unregistered executor conditions fail visibly.
