# Future M40-A batch and separate gates

## Recommended M40-A batch

After Claude audits this design and ChatGPT/User explicitly authorizes implementation, one broad M40-A may include all ten scoped rows.

Why one batch is safe:

- every row adds exactly one ordinary weighted modifier;
- variants differ only through row-declared MML;
- only two execution shapes exist: in-place add and atomic rarity-transition add;
- exact/oracle and MC behavior reuse accepted kernels;
- every admission can be mechanically enumerated and tested;
- no source truth is silently closed.

Proposed implementation deliverables:

1. narrow shared one-add plan/compiler;
2. atomic target-rarity working-state executor;
3. resolver registration for the ten explicitly admitted rows only;
4. runtime-admission metadata and project-scope updates only for those rows;
5. mechanics-evidence entries for the exact `44/70` and `35/50` thresholds with the official 0.3.0 and PoE2DB references;
6. exact/oracle, MC, replay, failure, and regression tests;
7. result package and Claude audit.

## Mandatory implementation stop points

- any source or threshold conflict;
- inability to keep rarity change and add atomic;
- pool built under input rather than target rarity for Transmutation/Regal;
- need to modify accepted ordinary-add weighting or MML policy;
- need to infer permission from `active_in_current_simulation`;
- any unrequested operation or modifier layer entering the batch.

## Separately gated

- Alchemy and any multi-add rarity transition;
- Essences and guaranteed/tagged modifiers;
- Whittling, Omens, side overrides, desecrated pools, or other modifier layers;
- Fracture, Jawbone, Reveal, and league-specific mechanics;
- longer chains or route planning;
- optimizer, ranking, advice, economics, EV, or expected attempts;
- public numeric probability release;
- SOURCE/PROVENANCE, broader MML, or PD-013 closure;
- changing the product's default starting-item workflow or UI beyond accepting valid supplied normal/magic states.
