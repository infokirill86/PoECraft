# Implementation Summary

## Shared runtime

`src/p2c_engine/monte_carlo/jawbone.py` adds one data-driven executor for exactly:

- `gnawed_jawbone` — Rare quarterstaff, maximum item level 64;
- `preserved_jawbone` — Rare quarterstaff;
- `ancient_jawbone` — Rare quarterstaff, stores Reveal MML 40.

The executor builds one of two mutually exclusive candidate pools:

- D1-A free-capacity pool: one deterministic free side or a uniform prefix/suffix choice when both sides are free; no installed modifier enters the pool.
- D2-A full-item pool: all removable non-fractured installed modifier-instance identities across both sides with unit weights. The selected instance is removed and the placeholder inherits its side.

All validation and candidate selection occur before a frozen terminal state is created. Any invalid input or empty pool returns the original object state as no-transition/no-consumption.

## Canonical state and integrations

- Uses the existing `DesecratedPlaceholder` type and existing capacity/state validators.
- `OperationResolver` compiles only the three runtime-admitted rows and rejects variants/modifiers.
- The explicit bounded-sequence executor registry contains the three rows; exact and seeded paths use the same Jawbone pool/executor.
- Fracture now counts an unrevealed placeholder toward the minimum installed-count precondition while its target pool still iterates installed modifier instances only. Revealed Desecrated modifier instances remain fail-closed.
- `data/operations.yaml` records D1-A/D2-A and admits only the three authorized rows.
- `data/mechanics_evidence.yaml` records the proposed runtime delta without closing D3-D5, Reveal, or PD-013.

## Expected semantic fingerprint delta

The accepted-baseline fingerprint changes from `2e5e4454f941d01d1b31da143db5a34480a9865fa4e1dd9cd6302de16b0eccdf` to `6e7bc414416189d3d02941b63945457f4a35afafc475bc8bde54d0ddc1659a05`.

The intended semantic components are limited to:

- runtime admission and D1-A/D2-A transition metadata for the three Jawbone rows;
- the explicit `installed_modifier_or_placeholder_count` Fracture minimum-count/non-target contract.

No modifier rows, weights, Reveal pools, accepted Omen behavior, or other operation semantics changed.
