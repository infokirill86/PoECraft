# P2C M36-A Heterogeneous Chain Runtime Result - Codex v1

package_id: `P2C_M36A_Heterogeneous_Chain_Runtime_Result_Codex_v1`
package_type: `IMPLEMENTATION_RESULT_DELTA`
status: `proposed_for_claude_audit`

observed_repo_head: `382e53bb54e228bb9f4193ddc2d44c302c257a83`
observed_active_task_sha: `fefc441c4e9e5c2d2fe13d0fa24df41e39f4f67d36fdf46f353cca0fc56c4e7e`

## Plain-language summary for Kirill

This wave does two things.

First, it makes the repo checksum rule harder to forget. A local Git pre-push hook now runs the checksum updater and verifier before push. If the checksum file changes, the hook blocks the push and tells the actor to stage and commit the regenerated file.

Second, it implements M36-A: a narrow two-step mixed-operation chain runtime. The simulator can now test fixed chains made only from the two accepted project-model operations:

- accepted `ordinary_add`;
- accepted base Annulment.

Example chain shapes:

- add then annul;
- annul then add.

This is not a route planner. It is not optimizer/advice. It does not add Chaos, Essence, Fracture, Desecrate, Jawbone, Reveal, Annulment variants, or any new operation.

M36-A remains proposed until Claude audit and ChatGPT/User acceptance.
