# Plain-language summary for Kirill

M39 checks one important question before we add Greater/Perfect currencies:

> Are Greater/Perfect currencies mostly the same operation with an added "minimum modifier level" filter, or do they need separate mechanics?

Short answer:

- For the normal currency families in repo data, Greater/Perfect mostly means: do the same add-type operation, but restrict the candidate add pool by a minimum modifier level.
- For Greater/Perfect Chaos, the removal part stays base Chaos-like; MML applies to the new modifier added after removal.
- For Essences, this is not just MML. Essence rows use guaranteed crafted outputs and, for Perfect Essence, removal plus guaranteed crafted installation. They need a separate gate.

Practical meaning:

The project should build one shared MML filter layer instead of hardcoding every Greater/Perfect currency separately. But we should still admit runtime support in controlled slices.

Recommended next safe implementation floor:

1. Add a fail-closed MML filter interface to the resolver/operation plan layer.
2. Keep all non-admitted Greater/Perfect rows non-executable.
3. After audit, consider batch-admitting only Greater/Perfect Exalted and Greater/Perfect Chaos first, because their base primitives are already accepted.

Still open:

- MML is not closed as server truth.
- External source/provenance remains open.
- PD-013 remains open.
- Whittling/Omens remain separate.
- Essence mechanics remain separate.

