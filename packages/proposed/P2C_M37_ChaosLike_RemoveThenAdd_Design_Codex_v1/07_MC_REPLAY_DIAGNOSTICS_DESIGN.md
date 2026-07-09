# MC / Replay / Diagnostics Design

## MC execution shape

Later MC runtime should:

1. validate operation admission;
2. build removal pool from the current state;
3. sample removal candidate through accepted seeded decision source;
4. apply removal on a branch-copy;
5. rebuild ordinary add pool from the post-removal branch state;
6. sample add candidate through accepted seeded decision source;
7. commit full result only if both stages succeed.

## Replay requirements

Trace must include:

- run id;
- seed;
- operation id;
- remove decision id;
- removal pool fingerprint;
- selected removal candidate key;
- post-removal branch state hash;
- add decision id;
- add pool digest/fingerprint;
- selected add candidate key;
- terminal state hash;
- no-transition/failure code, if any.

Same seed and run id must replay exactly.

## Diagnostics

Every hard failure must report:

- operation id;
- input state hash;
- stage where failure occurred;
- relevant pool fingerprint or digest;
- candidate counts;
- selected candidate key, if any;
- reason category.

## Negative controls

M37-A tests should prove failure when:

- fractured modifier leaks into removal pool;
- an active catalog row is executed without accepted runtime admission;
- a branch reuses the root add pool after removal;
- removal succeeds but add pool empty is incorrectly committed as partial success;
- exact mass does not sum to one.

