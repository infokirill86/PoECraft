# Implementation summary

## Resolver interface

Changed `OperationResolverRequest`:

- added `mml: int | None = None`.

Changed resolver behavior:

- validates `mml` as a positive integer or `None`;
- rejects `bool`, non-integer, zero, and negative MML values;
- for `currency_id == ordinary_add`, compiles MML into `OrdinaryAddOperation(mml=...)`;
- records the resolved filter as `ResolvedOperationFilters(mml=...)`;
- for accepted catalog operations such as base `chaos`, rejects explicit MML;
- for non-admitted rows such as `greater_chaos`, rejects by `runtime_admission_status` before any MML behavior executes.

## Schema

Added:

```text
M39A_RESOLVER_SCHEMA_VERSION = p2c.m39a.operation_resolver_mml_filter_interface.v1
```

The previous M38-A schema constant remains exported for compatibility/history, but resolved plans now report the M39-A schema version.

## Scope preserved

No operation row in `data/operations.yaml` was changed.

No Greater/Perfect runtime was admitted.

No runtime behavior was added for:

- Greater/Perfect Exalted;
- Greater/Perfect Chaos;
- Essence;
- Whittling;
- Omen;
- side/desecrated filters;
- any new base operation.

