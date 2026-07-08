# Source / Provenance Consistency Check

Files checked:

- `data/sources.yaml`
- `data/mechanics_evidence.yaml`
- `data/operations.yaml`
- `config/project_scope.yaml`
- `CURRENT_STATUS.md`
- `ledger/ACCEPTED_ARTIFACTS.md`
- `ledger/DECISIONS.md`
- `ledger/OPEN_BLOCKERS.md`

No external fetch, source capture, live web check, or source-truth update was performed.

## Source policy consistency

`data/sources.yaml` states:

- PoE2DB and Craft of Exile agreement is accepted as project-model truth;
- RePoE is structural support, not primary weight source;
- automatic overwrite for conflicting evidence is forbidden;
- new external data is `PROPOSED_CHANGE`;
- user approval is required before runtime changes.

This reconciliation is consistent with that policy because it does not import new external data, overwrite conflicts, or close provenance.

## Mechanics evidence consistency

`data/mechanics_evidence.yaml` contains open or project-policy mechanics that affect operation admission:

| Evidence area | Current status | Relevance to operation admission |
|---|---|---|
| MML | `USER_APPROVED_PROJECT_RULE`, server-unconfirmed | Applies to greater/perfect variants and Ancient Jawbone. Must remain labeled project-model. |
| Whittling | `PROJECT_ADOPTED_INFERENCE` | Affects Chaos-like remove filtering. Not admitted here. |
| Lich guarantee-one | `USER_APPROVED_PROJECT_RULE` / source-aligned model | Affects Reveal. Not admitted here. |
| Fracturing revealed Desecrated | `DISPUTED_OUT_OF_ACTIVE_SCOPE` | Blocks Fracture admission without user-approved resolution. |

## Ledger/status consistency

Accepted ledgers and `CURRENT_STATUS.md` consistently say:

- accepted executable operations are accepted `ordinary_add` and base Annulment;
- heterogeneous operation chains remain closed;
- additional operations remain closed;
- SOURCE/PROVENANCE, MML, and PD-013 remain open.

## Inconsistency found

The inconsistency is not a direct source-data conflict. It is a metadata semantics conflict:

- `data/operations.yaml` and `config/project_scope.yaml` use `active_in_current_simulation` to mark broad project-scope operation groups;
- accepted runtime ledgers permit execution only for `ordinary_add` and base Annulment.

That mismatch can mislead future agents into treating prepared catalog rows as accepted executable runtime.

## Source/provenance conclusion

No user source decision is required to complete this reconciliation package because no source conflict is being resolved and no external data is being changed.

A later metadata correction should be audited before changing YAML semantics or validators.
