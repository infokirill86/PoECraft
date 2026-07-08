# Exact / Oracle Plan

## Exact path mass

For a fixed chain of length `n`, exact path mass is the product of per-step exact transition masses:

```text
path_mass = step_0_mass * step_1_mass * ... * step_n_mass
```

All exact values must be represented as rational values internally.

## Per-operation mass sources

| Operation | Exact mass source |
|---|---|
| `ordinary_add` | accepted ordinary add pool weights and exact weighted branch mass |
| base `annulment` | uniform exact mass over removable non-fractured installed modifier instances |

## Terminal aggregation

Terminal probability is a sum over all valid paths that yield the same canonical terminal state:

```text
terminal_mass(T) = sum(path_mass for every path ending at canonical terminal T)
```

Path order is not terminal identity.

## Mass conservation

For exact enumeration:

- total mass over terminal states plus explicit failure/no-transition terminals must sum exactly to 1;
- any missing mass is a hard failure;
- duplicate terminal aggregation must preserve exact mass.

## Tractability ceilings

M36-A should pin exact enumeration ceilings before running:

- maximum sequence length: 2;
- maximum branch count per step;
- maximum total path count;
- maximum terminal count;
- stop if exceeded.

Design recommendation:

- exact/oracle comparison is mandatory for two-step M36-A fixtures;
- longer chains require a later gate and may move to property checks plus MC comparison if exact enumeration becomes too large.
