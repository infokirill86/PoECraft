# Shared Kernel Report

M32 satisfies the shared-kernel requirement by routing both exact enumeration and MC sampling through one harness method:

- `OrdinaryAddMonteCarloHarness.build_pool(...)`

That method delegates to:

- `p2c_engine.legality.pool_builders.build_ordinary_add_pool`

Exact path:

- `OrdinaryAddMonteCarloHarness.enumerate_outcomes(...)`
- calls `build_pool(...)`
- converts the returned candidate pool into exact branch options.

MC path:

- `OrdinaryAddMonteCarloHarness.sample_once(...)`
- calls `build_pool(...)`
- samples one outcome through the accepted deterministic decision source.

Evidence:

- `test_exact_and_mc_use_same_injected_pool_builder` installs a spy pool builder and verifies that exact and MC paths both call the same injected builder for the same state.

No duplicate ordinary-add pool, legality, or weight implementation was added for MC.
