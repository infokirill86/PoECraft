# Seed Replay and PRNG Report

M32 uses the existing deterministic sampling stack:

- `SeededDecisionSource`
- `RecordingDecisionSource`
- `p2c.sha256_rejection.v1`
- `RNG_STREAM_VERSION`

Run metadata records:

- seed;
- sample count;
- run id;
- operation sequence id;
- mode id;
- operation id;
- RNG stream version;
- sampling algorithm id;
- source fingerprint;
- semantic fingerprint;
- code version;
- result hash.

Replay evidence:

- `test_same_seed_replay_gives_identical_public_summary` verifies same-seed deterministic replay.
- `test_different_seed_can_change_sample_sequence` verifies seed-sensitive sampling behavior where the fixture permits it.

M32 does not accept MC convergence as final probability evidence. M33 remains the exact-oracle convergence gate.
