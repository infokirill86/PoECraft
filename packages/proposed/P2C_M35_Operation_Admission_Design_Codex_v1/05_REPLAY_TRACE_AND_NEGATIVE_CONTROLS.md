# Replay, Trace, and Negative Controls

## Required replay fields for later M35-A

Each Annulment sample or exact branch should be traceable with:

- operation_id;
- semantics_version;
- input_state_digest;
- removal_pool_digest;
- removal_pool_result_fingerprint;
- selected_removal_candidate_key, if transition occurs;
- selected_mod_id;
- selected_duplicate_ordinal;
- selected_instance_flags;
- output_state_digest;
- terminal_key;
- no_transition_reason, if no transition occurs.

## Required diagnostics

Any failure must identify:

- fixture id;
- operation id;
- state digest;
- pool digest or empty-pool reason;
- selected candidate key, if applicable;
- failed invariant;
- expected behavior;
- actual behavior.

## Required negative controls

M35-A must include tests or check cases proving the suite can fail for:

1. Fractured removal leak
   - fixture contains a fractured modifier and at least one removable non-fractured modifier;
   - fractured candidate must not appear in the removal pool;
   - injected fractured candidate must fail.

2. Empty removable pool
   - fixture contains only fractured installed modifiers or no installed modifiers;
   - result must be no-transition/no-consumption;
   - any mutation must fail.

3. Non-uniform selection
   - fixture has multiple removable candidates;
   - exact oracle expects uniform candidate probability;
   - biased sampler or altered branch weight must fail.

4. Unsupported operation call
   - Annulment runtime must fail closed if called before accepted M35-A scope or with unsupported operation variants.

