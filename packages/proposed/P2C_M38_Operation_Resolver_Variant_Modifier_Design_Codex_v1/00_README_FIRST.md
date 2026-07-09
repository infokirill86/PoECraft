# M38 Operation Resolver / Variant & Modifier Layer Design

package_id: `P2C_M38_Operation_Resolver_Variant_Modifier_Design_Codex_v1`
package_type: `DESIGN_ONLY_PROPOSED_DELTA`
status: `proposed_for_claude_audit`
author: `codex`
created_utc: `2026-07-09T13:43:50Z`

## Read receipt

- observed_repo_head: `d383e9339c245c436198c5cdb6abbd4d7c910672`
- observed_active_task_sha: `8d6d02dfb1a0e1ac8d3c4854ecdb98d490aa764941c7c797009fccd2d1fe3971`
- active_task_path: `work/active/ACTIVE_TASK.md`

## Plain-language summary for Kirill

After M37-A the simulator can execute three accepted project-model capabilities:

1. add one legal ordinary modifier;
2. remove one eligible non-fractured modifier with base Annulment;
3. remove one eligible non-fractured modifier, then add one legal ordinary modifier with base Chaos-like behavior.

The next risk is not probability math. The next risk is operation resolution: Greater/Perfect variants, Omens, and future league-specific modifiers change an operation without being standalone base operations. If we implement every combination by hand, the engine becomes brittle quickly.

This package proposes a resolver layer:

```text
currency + variant + active modifiers + item state -> resolved operation plan
```

The resolver does not execute new mechanics by itself. It decides whether a requested operation is allowed, which accepted primitive plan it resolves to, and which filters/modifier layers are applied. Unsupported combinations fail closed.

## Boundaries

This package is design-only. It does not:

- implement runtime code;
- admit Greater/Perfect runtime;
- admit Whittling/Omen runtime;
- admit additional operation runtime;
- extend chains;
- release numeric probabilities;
- close SOURCE/PROVENANCE, MML, or PD-013;
- claim server truth;
- enable automation.

