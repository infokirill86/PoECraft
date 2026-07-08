# Missing Capability Map

## Missing simulator capabilities

1. Operation admission standard.
   - What must be proven before a new operation becomes executable?
   - What tests/audits are required?
   - What source/project-policy labels are required?

2. Non-add operation execution.
   - Removal-only operations.
   - Remove-then-add operations.
   - Guaranteed-mod operations.
   - Placeholder/reveal operations.

3. Heterogeneous sequence execution.
   - Sequence of different accepted operations.
   - State transition and replay across operation types.
   - Per-operation diagnostics.

4. Target/goal evaluation over real operation outcomes.
   - Not optimizer advice.
   - Just matching terminal states to target predicates.

5. Public output/release gates.
   - Numeric public release remains closed.
   - Internal evidence can exist only under existing rules.

6. Economics/optimizer.
   - Later only.
   - Should not be pulled forward before real operation execution is reliable.

## Missing governance capability

The project needs a standard way to answer:

```text
Is this operation allowed to become executable?
```

Without that, every new operation will require ad hoc scope negotiation.

## First candidate operation categories

| Category | Example | Why it matters | Risk |
|---|---|---|---|
| Removal-only | Annulment | First non-add state transition; uses existing removal pool kernel. | Medium |
| Remove-then-add | Chaos | Real route-relevant operation; combines removal and ordinary add. | Medium-high |
| Guaranteed crafted mod | Perfect Essence | Adds crafted-capacity and guaranteed-mod semantics. | Medium-high |
| Placeholder/reveal | Jawbone/Reveal | Needed eventually; much more source/mechanic complexity. | High |

## Practical implication

The next move should not be more generic MC polishing. It should prepare the first operation-admission gate.
