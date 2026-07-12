# P2C M47-A1 Jawbone Placeholder Runtime Result

Status: **PROPOSED — ready for Claude audit; not accepted runtime truth**.

## Plain-language summary for Kirill

P2C can now model the clean first half of Jawbone crafting without pretending that Reveal is solved. Gnawed, Preserved, and Ancient Jawbone install one hidden Desecrated placeholder on a Rare quarterstaff. If the item has room, no modifier is removed. If the item is completely full, one eligible non-fractured modifier is selected uniformly and replaced atomically by the placeholder on the same side.

The placeholder is a real dedicated state object, not a fake modifier. It stores the side, the Jawbone source row, and the row's later Reveal context. Only one hidden-or-revealed Desecrated object is allowed. A hidden placeholder counts toward Fracture's minimum installed count but can never be selected as the Fracture target.

Reveal, offer construction, D3-D5, Echoes, Omen of Light, and revealed-Desecrated Fracture behavior were not implemented.

## Participant / architecture critique

No material objection to the three-row clean-core boundary. It is the smallest coherent runtime that advances the physical-quarterstaff route while keeping every unresolved Reveal probability decision outside execution. The architecture deliberately uses the existing canonical `DesecratedPlaceholder` and the accepted resolver/sequence infrastructure. Building a generic Desecrated algebra or implementing candidate Reveal YAML would have been premature.

## Result map

- `01_IMPLEMENTATION_SUMMARY.md` — runtime and integration changes.
- `02_POLICY_EVIDENCE_MATRIX.md` — D1-A/D2-A, capacity, Fracture, and admission evidence.
- `03_TESTS_AND_CHECKS.md` — commands and results.
- `04_BOUNDARIES_AND_RISKS.md` — proposed/closed scope and watchpoints.
- `05_READ_RECEIPT.md` — exact input receipt.
- `07_CLAUDE_AUDIT_REQUEST.md` — independent audit request.
