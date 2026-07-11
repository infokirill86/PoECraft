# Risks, Deferred Work, and Rollback

Remaining risks:

- accepted evidence still resides under `packages/proposed/`; this is intentionally deferred;
- first-read prose can become stale again if future authors copy volatile truth instead of referencing canonical sources;
- untracked local notes can exist under `work/active/`, but cannot be committed while validation passes.

Deferred behind later gates:

- package lifecycle/migration cleanup;
- archive or directory restructuring;
- any M43 implementation decision;
- runtime, mechanics, data, operation, optimizer/public-output, or automation work.

Rollback is ordinary Git revert of this cleanup commit. No history rewrite or evidence deletion is needed.
