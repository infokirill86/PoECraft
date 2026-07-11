# Expected fingerprint delta

Previous accepted semantic fingerprint:

`251bf97728e97c1907f6d59229120544852053dd20eba728a98aabd9ac453158`

Proposed M42-A semantic fingerprint:

`230dc88b9e8c5cd90857fc06cb2ccec66ca58498878579cd47258766948c8979`

Expected runtime-semantic components changed in `data/operations.yaml`:

1. exactly six Perfect Essence rows move from `admission_candidate` to `accepted_executable_runtime`;
2. their removal kind becomes terminal-feasible uniform instance selection;
3. the explicit feasibility condition and selection mode are added;
4. prevalidation becomes `family_absent`, `crafted_count_zero`, and `feasible_removal_pool_nonempty`.

`data/mechanics_evidence.yaml` records the accepted source-open project rules. Under the existing data manifest it is documentary evidence rather than an input to the semantic fingerprint. Project scope and Essence output rows were already prepared and are unchanged. Any unrelated fingerprint change is a hard-fail investigation.
