# Exact, MC, replay, and diagnostic evidence

## Exact/oracle

- Exact path mass multiplies the accepted weight share at each branch-current internal add.
- Paths aggregate by canonical terminal-state identity.
- Path and terminal mass conservation are hard invariants.
- Candidate, path, and terminal ceilings fail closed through explicit exceptions.
- M43-A converts an internal Alchemy exact ceiling breach into its structured exact stop rather than truncating or substituting Monte Carlo.

## Seeded Monte Carlo

- Seeded execution uses the same resolver plan, Alchemy harness, pool builder, and state transitions as exact execution.
- A deterministic fixture compares observed terminal counts with the exact distribution under the pinned wide statistical envelope.
- All seeded terminals belong to the exact terminal set.

## Replay and diagnostics

- Same seed, run id, input, and operation replay byte-for-byte equal result objects.
- Every internal trace records add index, working pre/post hashes, decision id, selected canonical modifier id, candidate count, candidate digest, and failure reason.
- Public summaries contain statuses, counts, hashes, and identifiers only; probability values remain internal.
