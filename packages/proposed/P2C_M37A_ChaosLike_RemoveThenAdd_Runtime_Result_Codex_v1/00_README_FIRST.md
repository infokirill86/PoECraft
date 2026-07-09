# P2C M37-A Chaos-like Remove-Then-Add Runtime Result - Codex v1

package_id: `P2C_M37A_ChaosLike_RemoveThenAdd_Runtime_Result_Codex_v1`
package_type: `IMPLEMENTATION_RESULT_PROPOSAL`
status: `proposed_for_claude_audit`

observed_repo_head: `3a9db200ac367e7c441074d27c6803f15a67c752`
observed_active_task_sha: `379e4bfcfda888f87db24599f7385035ec424926dfdb7f5f5188bef22c6513e6`

## Plain-language summary for Kirill

M37-A adds the proposed runtime for base Chaos-like behavior.

In simple terms:

1. The operation removes one removable non-fractured modifier from a branch-copy of the item.
2. It rebuilds the ordinary add pool from that changed branch-copy.
3. It adds one legal modifier using the already accepted ordinary_add pool rules.
4. It commits only the full remove-plus-add result.
5. If remove or add cannot happen, it returns no-transition/no-consumption and does not leave a partial remove-only item.

This is still proposed pending Claude audit and ChatGPT/User acceptance. It does not self-accept M37-A.

## Important boundaries

- Base `chaos` only.
- No Whittling.
- No side Omens.
- No Greater/Perfect Chaos.
- No Essence, Fracture, Desecrate, Jawbone, Reveal runtime.
- No optimizer/advice/ranking/economics/EV.
- No public numeric probability release.
- No server-truth claim.
- SOURCE/PROVENANCE, MML, and PD-013 remain open.

