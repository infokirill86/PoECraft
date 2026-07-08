# Replay and Diagnostics Plan

## Replay rule

For a given fixture id, sequence id, seed, run id, and sample tier, M34-B1 replay must reproduce:

- same step count;
- same decision ids;
- same selected mod ids;
- same pre-state hashes;
- same post-state hashes;
- same pool digests;
- same final result hash.

## Required trace fields

Every sampled sequence trace should contain:

- fixture id;
- sequence id;
- seed;
- run id;
- sample index;
- step index;
- operation id;
- mode id;
- pre-state hash;
- pool digest;
- candidate count;
- selected mod id or no-transition marker;
- post-state hash;
- terminal state hash;
- diagnostic category when a breach occurs.

## Required breach diagnostics

Every hard failure should identify:

- fixture id;
- sequence id;
- seed;
- run id;
- sample tier;
- sample index when applicable;
- step index;
- branch key or terminal key;
- pool digest or equivalent;
- pre-state hash;
- post-state hash;
- expected category;
- observed category;
- failure category.

## Diagnostic categories

Recommended categories:

- `m34b_operation_scope_breach`;
- `m34b_state_linkage_breach`;
- `m34b_pool_rebuild_breach`;
- `m34b_legality_rebuild_breach`;
- `m34b_replay_mismatch`;
- `m34b_oracle_tolerance_breach`;
- `m34b_negative_control_expected_failure`;
- `m34b_public_numeric_leak`.

## Human-readable failure reporting

A later M34-B1 result package should include a short plain-language section explaining:

- what failed;
- which fixture and step failed;
- why the failure matters;
- whether it is a real failure or an intentional negative control;
- what should happen next.
