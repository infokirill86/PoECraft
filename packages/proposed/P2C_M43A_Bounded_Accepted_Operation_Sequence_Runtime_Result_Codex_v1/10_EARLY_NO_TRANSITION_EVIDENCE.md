# Early No-Transition Evidence

`stop_on_no_transition` is pinned true.

When a later step cannot execute:

- that step leaves its input state unchanged and consumes nothing;
- state committed by earlier successful steps remains committed;
- no later step executes on that branch;
- the terminal records completed-step count, failing step index, outcome code, and the last committed state.

The test fixture applies a valid Greater Essence, then attempts the same magic-only operation on the resulting Rare item, followed by Annulment. The first step remains committed, the second returns explicit no-transition, and the third is absent from the trace.

The sequence is not globally atomic; each accepted operation retains its own atomic contract.
