# Atomicity, pool rebuild, and side evidence

Focused tests prove:

- Normal and Magic input both compile and execute.
- Existing Magic explicit modifiers are absent from successful terminals.
- Every successful terminal is Rare with exactly four newly generated ordinary modifiers.
- A spy around the real `build_ordinary_add_pool` observes Rare working states containing zero, one, two, and three already selected modifiers.
- Different intermediate branch states produce different state hashes before later pool builds.
- Prefix counts of one, two, and three all occur in exact paths; zero and four do not occur.
- An injected empty pool after two successful internal draws rolls every exact branch and seeded sample back to the original Magic state.
- Failure traces identify the internal add index and pool failure while the public post-state remains the original pre-state.
- Fractured Magic input returns explicit no-transition/no-consumption before any internal draw.

This demonstrates that real pool rebuilding is load-bearing and that the four internal draws form one atomic operation.
