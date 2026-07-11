# MC, Replay, and Diagnostic Evidence

Seeded MC uses the same resolver, registry, accepted harnesses, pools, and state transitions as exact execution.

Each trajectory records:

- sequence/sample identity at result level;
- per-step index, ID, currency, mode, and executor;
- pre/post state hashes;
- state-bound resolver plan digest;
- transition and selected keys;
- decision IDs;
- candidate count and pool/removal digest;
- no-transition reason;
- final execution-terminal identity.

Same request, initial state, seed, sample count, and run ID replay exactly. A deliberately altered expected result triggers the replay mismatch negative control.

A tractable mixed Annulment-to-add fixture compares seeded MC state terminals to exact rational projection under the previously accepted wide statistical envelope. The six-step and eight-step fixtures prove mixed execution and deterministic replay without planner behavior.
