# Implementation summary

## Catalog admission

`data/operations.yaml` changes only the four authorized rows from `admission_candidate` to `accepted_executable_runtime`.

## Resolver compilation

`OperationResolver` now:

- checks each row's `runtime_admission_status`;
- rejects caller-supplied MML for catalog operations;
- reads the fixed MML from the admitted row;
- checks rare-item input compatibility;
- validates the expected transition shape before compiling;
- compiles Greater/Perfect Exalted to `OrdinaryAddOperation`;
- compiles Greater/Perfect Chaos to `ChaosLikeOperation`;
- keeps all active modifier IDs and non-base `variant_id` values fail-closed.

## Shared kernels

No variant-specific add or remove implementation was created.

- Exalted variants execute through `OrdinaryAddMonteCarloHarness` and the accepted ordinary add pool builder.
- Chaos variants execute through `ChaosLikeMonteCarloHarness`; base removal is unchanged, and `operation.mml` is passed only into the branch-specific ordinary add pool request.
- The existing atomic rollback, fractured protection, exact path multiplication, and canonical terminal aggregation remain shared.

## Semantic fingerprint

The project semantic fingerprint was intentionally retuned because four catalog rows now participate in the proposed executable runtime surface. This is runtime-admission evidence, not SOURCE/PROVENANCE or broader MML closure.
