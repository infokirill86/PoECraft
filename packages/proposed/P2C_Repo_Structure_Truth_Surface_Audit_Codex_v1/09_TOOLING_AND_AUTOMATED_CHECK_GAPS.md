# Tooling and Automated Check Gaps

## Healthy checks

- Root `SHA256SUMS.txt` verification: PASS.
- ACTIVE_TASK schema/status/path validation: PASS.
- Exact duplicate tracked-file scan: no duplicate groups.

## Gaps

### ACTIVE_TASK validator

It validates the file but not the directory contract. It should later fail if any other tracked file exists under `work/active/`.

### Nested-ZIP checker

It reports the three explicit Layer-A source-bundle ZIPs as violations. The checker needs a narrow exception contract based on package type/path/manifest, while ordinary packages remain ZIP-free.

### Public numeric leak checker

Repo-wide execution reports many false positives from source code, tests, version strings, evidence counts, and non-probability data. It needs explicit public-surface inputs and scoped allowlists. A repo-wide raw regex failure is not a meaningful release gate.

### Reference checker

No accepted tool verifies canonical document references or package-review-ledger lifecycle links. A small later checker could scan only canonical live surfaces, avoiding immutable historical evidence.

## Minimal automation principle

Do not add GitHub Actions or watcher automation. These checks remain local/manual pre-push tooling unless separately authorized.
