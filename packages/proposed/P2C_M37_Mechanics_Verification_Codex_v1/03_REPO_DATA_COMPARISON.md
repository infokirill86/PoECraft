# Repo-data Comparison

## `data/operations.yaml`

The Chaos-like operation rows are catalog/admission candidates only:

| operation_id | active_in_current_simulation | runtime_admission_status | remove behavior in row | add behavior in row |
|---|---:|---|---|---|
| `chaos` | true | `admission_candidate` | uniform installed instance, exclude fractured, Omen filters available | ordinary weighted, MML null |
| `greater_chaos` | true | `admission_candidate` | uniform installed instance, exclude fractured, Omen filters available | ordinary weighted, MML 35 |
| `perfect_chaos` | true | `admission_candidate` | uniform installed instance, exclude fractured, Omen filters available | ordinary weighted, MML 50 |

The important status is `runtime_admission_status: admission_candidate`. `active_in_current_simulation: true` must not be read as executable permission.

## `data/omens.yaml`

The repo has explicit Omen metadata:

| omen_id | operation group | effect |
|---|---|---|
| `sinistral_erasure` | `chaos` | removal side filter: prefix |
| `dextral_erasure` | `chaos` | removal side filter: suffix |
| `whittling` | `chaos` | selection: minimum modifier level; tie breaker: uniform project policy |

This supports the corrected interpretation: Whittling is an Omen effect applied to Chaos-like operations, not the base Chaos rule.

## `data/mechanics_evidence.yaml`

The file records:

- Whittling official rule: remove the lowest modifier-level removable modifier.
- Whittling tie breaker: uniform random among tied lowest-level instances.
- Whittling status: `PROJECT_ADOPTED_INFERENCE`.
- MML applies to greater/perfect chaos addition.

Potential ambiguity: the file does not itself say "Whittling is Omen-only." That should be clarified before M37-A or in the M37 correction patch, because otherwise readers can misread the Whittling entry as base Chaos behavior.

## Accepted ledgers and status

Accepted executable runtime is still only:

- accepted `ordinary_add` engine primitive;
- accepted base Annulment;
- accepted M36-A fixed two-step chains over those accepted operations.

Chaos-like rows remain candidates only. No repo file should be read as accepting Chaos runtime.

