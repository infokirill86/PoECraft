# Shared architecture

The resolver compiles each authorized row to:

```text
CatalogSingleAddOperation
  operation_id
  input_rarities
  pool_build_rarity
  output_rarity
  mml
  semantics_version
```

The harness then:

1. verifies the exact admitted catalog row and semantics version;
2. checks source item class, rarity, known modifier ids, and source capacity;
3. creates an isolated copy at the row's pool-build rarity;
4. calls `build_ordinary_add_pool` with the row MML;
5. enumerates exact rational branches or samples through the accepted seeded decision source;
6. appends exactly one ordinary modifier to the isolated state;
7. checks rarity, capacity, family/group conflicts, and fractured-instance immutability;
8. exposes only the successful terminal state.

No row-specific executor, fixed side lottery, threshold branch, route planner, or generalized operation algebra was introduced.
