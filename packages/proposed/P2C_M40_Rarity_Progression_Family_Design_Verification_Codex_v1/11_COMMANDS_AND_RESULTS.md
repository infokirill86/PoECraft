# Commands and results

## State and source inspection

- verified current Git HEAD and clean starting worktree;
- hashed exact starting `work/active/ACTIVE_TASK.md` bytes;
- read `AGENTS.md`, `manifest/Agent_Role_Pack.md`, `CURRENT_STATUS.md`, and live dispatcher;
- inspected `data/operations.yaml`, `data/mechanics_evidence.yaml`, `data/sources.yaml`, `config/project_scope.yaml`, and relevant domain/capacity code/tests;
- checked official Content Update 0.3.0, PoE2DB Currency/Crafting, supporting PoE2 Wiki capacity pages, and a PoE1 capacity analogue.

## Validation

Final command results before checksum generation:

- `python tools/validate_foundation.py`: PASS (`P2C_FOUNDATION_VALIDATION: PASS`)
- `python tools/validate_m4.py`: PASS (`P2C_M4_VALIDATION: PASS`)
- `python -m pytest -q`: PASS (`161 passed`)

Repo-integrity results:

- `git config core.hooksPath tools/hooks`: configured
- `python tools/update_sha256sums.py`: PASS; root manifest regenerated from final Git-normalized/index bytes
- `python tools/check_sha256sums.py SHA256SUMS.txt`: PASS
- `git diff --check`: PASS
