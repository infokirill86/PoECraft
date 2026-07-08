# Implementation Report

## Runtime module

New module:

```text
src/p2c_engine/monte_carlo/annulment.py
```

It defines:

- `AnnulmentOperation`
- `AnnulmentMonteCarloHarness`
- `ExactAnnulmentPath`
- `ExactAnnulmentTerminalOption`
- `AnnulmentTrajectory`
- `AnnulmentRunResult`
- `M35AAnnulmentInvariantViolation`

## Load-bearing shared kernel

Annulment uses:

```text
p2c_engine.legality.pool_builders.build_removal_pool
```

through `RemovalPoolRequest`.

The harness accepts an injected removal-pool builder only for testability, mirroring the existing accepted `ordinary_add` harness pattern. The default runtime path is the accepted shared removal-pool builder.

## Semantics implemented

Base Annulment:

- operation id: `annulment`;
- semantics version: `p2c.m35.annulment.project_model.v1`;
- supported rarities: `magic`, `rare`;
- item class: `quarterstaff`;
- selected unit: installed modifier instance / removal candidate key;
- fractured candidates are invalid and fail closed;
- empty removal pool returns explicit no-transition/no-consumption;
- exact/oracle path masses use reduced rational fields;
- terminal distribution aggregates by canonical post-state hash.

## Duplicate-instance handling

Removal-path identity and terminal-state identity are separate:

- path identity is the removal candidate key;
- terminal identity is the canonical post-removal item state hash.

If multiple removal keys produce the same canonical terminal state, terminal mass is aggregated.

## What was intentionally not added

No generalized operation algebra was added.

No Chaos, Essence, Fracture, Desecrate, Jawbone, Reveal, optimizer, economics, advice, or public numeric release code was added.

