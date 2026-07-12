# Confirmed Mechanics

Confirmed enough to recommend as the M47 project basis, subject to later User gate:

- clean M47 applies only to Rare quarterstaff through weapon-compatible Jawbone rows;
- Gnawed Jawbone respects its displayed item-level ceiling;
- Ancient Jawbone stores its displayed MML for the later Reveal pool and uses the accepted family-fallback MML policy;
- Jawbone produces one unrevealed Desecrated placeholder;
- the placeholder has a fixed prefix or suffix identity and consumes capacity on that side;
- an item normally cannot receive another Desecration while a hidden or revealed Desecrated modifier remains;
- Reveal requires one placeholder and offers three outcomes at the Well of Souls;
- revealed output replaces the placeholder atomically with one canonical installed modifier on the same side;
- the installed result carries `desecrated: true`, participates in canonical state/replay, consumes ordinary side capacity, and blocks its family/groups like another installed explicit;
- invalid preconditions and any failed transition must be no-transition/no-consumption with the original immutable state preserved;
- fractured installed modifiers remain immutable and cannot be removed by Jawbone replacement;
- M46-A continues to reject every Desecrated or placeholder state until a later PD-013 gate.

These statements are project-model recommendations, not server-truth closure.
