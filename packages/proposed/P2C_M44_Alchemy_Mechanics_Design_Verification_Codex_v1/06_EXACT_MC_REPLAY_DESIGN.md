# Exact, Monte Carlo, replay, and diagnostics design

## Exact/oracle

- Enumerate each legal four-selection path using exact rational mass.
- At each depth, derive path mass from the accepted ordinary-add candidate weight and the total legal pool weight for that branch state.
- Multiply exact branch masses across the four selections.
- Aggregate paths by canonical terminal-state identity while preserving separate path identities for diagnostics.
- Require total terminal mass conservation as a boolean invariant.
- Pin path and terminal ceilings before execution. Overflow returns a structured stop with no truncation, renormalization, or hidden Monte Carlo substitution.

## Seeded Monte Carlo

- Use the same resolver plan, pool builder, weighting kernel, state transition, and atomic boundary as exact evaluation.
- Pin seed set, sample tiers, tolerance policy, and negative controls before running.
- Compare against exact/oracle output only on fixtures below the exact ceilings.
- Keep all probability values quarantined; public package reports may contain only boolean statuses, identifiers, hashes, counts, and schema/version metadata.

## Replay and diagnostics

Each replay trace should identify operation, run/seed, source state digest, each draw index, branch-current-state digest, legal-pool digest, selected canonical modifier identity, and final terminal digest. Failures must identify the first failing draw and category without committing an intermediate state.

## Required negative controls

- invalid input rarity;
- fractured input under the conservative floor;
- non-quarterstaff/special-capacity item class;
- missing canonical modifier data;
- intermediate empty pool;
- exact path or terminal ceiling overflow;
- unsupported modifier/variant layer.
