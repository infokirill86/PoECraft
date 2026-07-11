# Exact Ceiling and Mass-Conservation Evidence

Pinned first-floor ceilings:

- maximum sequence length: eight steps;
- maximum candidates from one pool: 256;
- maximum exact paths: 65536;
- maximum exact execution terminals: 65536.

Completed exact results require path mass and execution-terminal mass to sum exactly to one using canonical rational arithmetic. Early no-transition terminals remain in that mass.

Candidate, path, or terminal overflow returns a structured `ceiling_exceeded` result naming the ceiling, limit, observed count, step, and currency. The result contains no partial paths or terminals and does not call MC, truncate, renormalize, or substitute an approximation.

Tests exercise all three ceiling-stop categories and exact terminal aggregation. Optional state-only projection is separate from diagnostic execution-terminal identity.
