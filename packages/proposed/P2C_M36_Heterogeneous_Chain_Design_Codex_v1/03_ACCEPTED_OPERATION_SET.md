# Accepted Operation Set

## Current accepted executable capabilities

| Capability | Kind | Admission source | Current status |
|---|---|---|---|
| `ordinary_add` | engine primitive | Accepted M32-M34 lineage; not an `operations.yaml` row | accepted executable primitive |
| `annulment` | game-facing operation row | `data/operations.yaml` with `runtime_admission_status: accepted_executable_runtime`; accepted M35-A runtime | accepted base runtime only |

## Explicit exclusions

The following are not executable runtime for M36:

| Row/family | Reason |
|---|---|
| Exalted-like rows | Catalog/currency wrappers over add behavior; not accepted executable currency runtime. |
| Chaos-like rows | Candidate remove-then-add operations; not admitted. |
| Perfect Essence rows | Candidate remove-plus-guaranteed-install operations; not admitted. |
| Greater Essence rows | Data reference candidates only. |
| Jawbone rows | Blocked/out of scope. |
| Reveal row | Blocked/out of scope. |
| `fracturing_orb` | Disputed or requires user resolution. |
| Annulment variants/omens | Not part of accepted base Annulment runtime. |

## Engine primitive registry requirement

M36 should treat engine primitives separately from operation catalog rows.

Proposed accepted primitive registry for M36-A:

```yaml
accepted_engine_primitives:
  ordinary_add:
    status: accepted_executable_runtime
    source: accepted M32-M34 ordinary_add runtime lineage
    scope: add exactly one legal ordinary modifier
```

This registry is a design proposal. It is not implemented here.
