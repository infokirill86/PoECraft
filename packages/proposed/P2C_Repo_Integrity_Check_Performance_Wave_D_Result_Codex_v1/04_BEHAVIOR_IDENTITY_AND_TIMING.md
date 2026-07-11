# Behavior Identity and Timing

## Byte identity

- committed manifest SHA before Wave D execution: `da397ba651e6d63b42a75a64f6707609bec859fd983f8669db19905d8a9ab65d`
- manifest SHA after old updater: `da397ba651e6d63b42a75a64f6707609bec859fd983f8669db19905d8a9ab65d`
- manifest SHA after batched updater: `da397ba651e6d63b42a75a64f6707609bec859fd983f8669db19905d8a9ab65d`
- byte-identical result: PASS

The byte-identity comparison was run on the same pre-Wave-D Git index before the
new tooling/docs were staged. The final commit-level manifest must naturally
update hashes for the changed tools, ledgers, dispatcher, tests, and new package;
that expected repository-content delta is separate from behavioral equivalence.

## Measured elapsed time

Single-run measurements on the same Windows clone and manifest:

| Tool | Before | Batched | Approximate speedup |
|---|---:|---:|---:|
| updater | 57007 ms | 266 ms | 214x |
| checker | 57015 ms | 543 ms | 105x |

These measurements demonstrate removal of the process-launch bottleneck. They are not performance promises for other hardware.
