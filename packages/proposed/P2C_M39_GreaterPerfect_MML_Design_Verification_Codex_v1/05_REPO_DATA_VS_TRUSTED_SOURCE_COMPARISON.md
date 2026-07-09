# Repo-data vs trusted-source comparison

## Comparison result

No stop-triggering conflict was found for the Greater/Perfect MML inventory.

Repo data and trusted sources are aligned enough for a project-base design package, but not enough to close MML or SOURCE/PROVENANCE.

## Confirmed enough for project-model design

| Topic | Repo data | Trusted-source check | M39 conclusion |
|---|---|---|---|
| Greater/Perfect Transmutation | same base transmutation shape plus MML 44/70 | PoE2DB agrees; official patch notes support minimum-level wording | MML-like, but base wrapper not admitted runtime |
| Greater/Perfect Augmentation | same base augmentation shape plus MML 44/70 | PoE2DB agrees; official patch notes support minimum-level wording | MML-like, but base wrapper not admitted runtime |
| Greater/Perfect Regal | same base regal shape plus MML 35/50 | PoE2DB agrees | MML-like, but base wrapper not admitted runtime |
| Greater/Perfect Exalted | same rare add shape plus MML 35/50 | PoE2DB agrees | good future batch candidate after MML filter admission |
| Greater/Perfect Chaos | same base Chaos-like remove-then-add plus MML 35/50 on add component | PoE2DB agrees | good future batch candidate after MML filter admission |
| Greater/Perfect Essence | guaranteed crafted / removal+guaranteed crafted mechanics | not treated as ordinary MML rows | separate Essence admission required |

## Important non-confirmations

This package does not confirm:

- that MML is server-truth exact;
- that Craft of Exile currently agrees line-by-line for every Greater/Perfect row;
- that Essence rows are safe to batch with MML-only variants;
- that Greater/Perfect Transmutation/Augmentation/Regal are executable, because their base wrappers are not accepted runtime;
- that Omen/Whittling/side/desecrated filters are admitted runtime.

## Repo consistency observations

- `data/operations.yaml` correctly keeps Greater/Perfect rows as `data_reference_candidate` or `admission_candidate`, not accepted runtime.
- `data/mechanics_evidence.yaml` currently marks MML as a user-approved project rule with server confirmation still open.
- `data/sources.yaml` keeps source conflict resolution under user-approved control.
- `CURRENT_STATUS.md` and ledgers keep accepted runtime limited to current accepted operations; this package does not change that.

