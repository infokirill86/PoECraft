# P2C M34-A Multi-Seed MC Hardening Result - Codex v1

Package type: `MC_HARDENING_RESULT_DELTA`

Status: proposed for Claude audit.

This package implements M34-A only.

M34-A scope:

- multi-seed single-step convergence hardening over accepted `ordinary_add` only;
- deterministic replay across a fixed seed set;
- tolerance breach diagnostics;
- negative-control failure reporting;
- package/report leak safety.

This package does not:

- start M34-B;
- implement multi-step or sequence validation;
- add new executable mechanics;
- expand beyond accepted `ordinary_add`;
- add optimizer, advice, ranking, economics, EV, or expected attempts;
- release public probability values;
- claim server truth;
- close SOURCE/PROVENANCE, MML, or PD-013;
- enable supervised auto-run or GitHub Actions.

Claude audit request:

- see `07_CLAUDE_AUDIT_REQUEST.md`.
