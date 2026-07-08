# Proposed Tests and Checks

## M34-A: multi-seed single-step hardening

Proposed tests:

- multi-seed two-branch ordinary-add fixture;
- multi-seed broad skewed ordinary-add fixture;
- deterministic replay test for every seed in the seed list;
- negative-control test proving a deliberately biased sampler or altered expected probability would fail;
- public leak-scan test for result package docs.

Proposed checks:

- `python -m pytest tests/monte_carlo -q`
- `python tools/validate_foundation.py`
- `python tools/validate_m4.py`
- `python -m pytest -q`
- package SHA check;
- root SHA check;
- package public numeric leak scan;
- `git diff --check`.

## M34-B: multi-step accepted-ordinary-add sequence validation

Proposed tests:

- short two-step accepted-ordinary-add sequence fixture;
- branch-state pool rebuild proof;
- replay determinism for the full sequence;
- terminal canonical identity stability;
- no-transition handling when a later step has no legal candidates;
- failure report contains seed/run/step/pool digest/state hash.

Important boundary:

If a two-step sequence is constructed rather than representing a real operation route, it must be explicitly labeled as a constructed sequence for MC hardening only.

## Diagnostics checks

Diagnostics should be tested directly:

- failure object includes required fields;
- failure object avoids public probability values;
- replay instructions are enough to rerun the same failing case.

## Non-checks

M34 should not test:

- optimizer strategy;
- EV/cost;
- new operations;
- server-truth probability;
- source/provenance closure.
