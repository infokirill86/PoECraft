# P2C M37 Mechanics Verification - Codex v1

package_id: `P2C_M37_Mechanics_Verification_Codex_v1`
package_type: `MECHANICS_VERIFICATION_PROPOSAL`
status: `proposed_for_claude_audit`

observed_repo_head: `e7497b5abf01a0a4f12ce0932082517bfd86afa8`
observed_active_task_sha: `ae5c3573c5298c2d303a66e2abc9607eb4edb287199fbf8c8b6c91c8de1393ad`

## Plain-language summary for Kirill

The previous M37 design was structurally useful, but it left one dangerous mechanics point too implicit: how a Chaos-like operation chooses the modifier to remove.

The verification result is:

- base Chaos-like public wording says it removes a random modifier, then adds a random modifier;
- Omen of Whittling separately changes the next Chaos Orb so it removes the lowest-level modifier;
- base Annulment public wording says it removes a random modifier;
- Exalted-like add wording says it adds a random modifier, while side Omens narrow add side;
- repo data correctly keeps Chaos-like rows as `admission_candidate`, not executable runtime.

Recommended project-model correction before M37 acceptance:

1. M37 should explicitly model base Chaos-like removal as random over eligible removable non-fractured installed modifier instances for the base `chaos` candidate.
2. Whittling / lowest modifier-level selection should be treated as an Omen override, not base Chaos behavior.
3. This remains project-model truth only, not PoE2 server truth.
4. If we want server-truth confidence for uniformity, that requires later user-approved in-game/emulator verification.

No runtime implementation was added. No Chaos row was marked executable.

