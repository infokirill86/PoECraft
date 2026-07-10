# Expected fingerprint delta

Previous accepted semantic fingerprint: `cc391280365ab48ca02662be642ac560d8db945fc54a86eceb190edcce127eeb0`

Proposed M41-A semantic fingerprint: `251bf97728e97c1907f6d59229120544852053dd20eba728a98aabd9ac453158`

Expected semantic components changed:

1. `data/operations.yaml`: one handler declaration and admission/active metadata for exactly the eight authorized Greater Essence rows.
2. `config/project_scope.yaml`: Greater Essence moved from reference-only to active, its mechanic was added, and its excluded route marker was removed.

`data/essence_outputs.yaml` and canonical modifier rows were already present and are unchanged. The fingerprint regression test pins the proposed value. Any unrelated data/config fingerprint change is a hard-fail investigation.
