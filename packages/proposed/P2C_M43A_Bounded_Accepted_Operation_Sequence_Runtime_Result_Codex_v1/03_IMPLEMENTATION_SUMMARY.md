# Implementation Summary

Primary implementation:

- `src/p2c_engine/monte_carlo/bounded_sequence.py`
- exports in `src/p2c_engine/monte_carlo/__init__.py`
- `tests/monte_carlo/test_m43a_bounded_sequence_runtime.py`

The runtime provides:

- fixed one-to-eight-step request objects;
- exact rational branch enumeration;
- execution-terminal and optional state-only aggregation;
- exact per-step marginals;
- seeded MC execution and deterministic replay verification;
- branch-specific resolver plan and pool/removal diagnostics;
- structured exact ceiling stops;
- explicit accepted executor registry.

Parity testing exposed an existing container-compatibility defect: the resolver accepted immutable mapping/tuple data from real `StaticGameData`, while direct Chaos/M40 and the shared M36 row helper still required mutable dictionaries/lists. Those checks now accept the same immutable mapping/sequence shapes. No transition rule, weight, pool, operation admission, or data value changed.
