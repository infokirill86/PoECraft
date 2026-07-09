# Participant critique

## Is M39 the right next move?

Yes, with a narrowed boundary.

After M38-A, the repo has a single-operation resolver skeleton, but it still lacks a verified design for variant and modifier layers. Greater/Perfect variants are a good next design target because the repo already contains many Greater/Perfect rows and several `active_in_current_simulation: true` flags. Without M39, the project risks admitting variants ad hoc.

## Why not direct Greater/Perfect implementation now?

Direct implementation would be premature. The correct shared seam is MML as a pool-filter layer, not one hardcoded function per Greater/Perfect currency. However, MML itself must remain project-model and source/provenance-open.

## Why not Whittling/Omen first?

Whittling/Omen is more dangerous because it modifies removal selection and has unresolved tie behavior. MML is simpler: it filters add-pool candidate rows. It is the better first variant-layer design target.

## Why not next operation admission?

Next operation admission would move the project forward, but it would also add mechanics while the variant-layer model is still ambiguous. M39 reduces future operation-admission risk.

## Why not more chain hardening?

Chain infrastructure already works for accepted operations. The higher current risk is operation/variant scope drift, not chain proof depth.

## Correct boundary

This package should verify and design only:

- Greater/Perfect inventory;
- MML source/mechanics model;
- safe batching candidates;
- separate gates for non-MML mechanics.

It should not implement or admit runtime behavior.

