# Participant critique

M38-A is the right next move after M38 design acceptance.

Reasoning:

- Directly implementing Greater/Perfect or Whittling now would mix operation admission with modifier semantics before the resolver boundary exists.
- Adding another operation first would repeat the ad hoc admission pattern that M38 is meant to fix.
- More chain hardening would improve already accepted operations, but it would not solve the next structural bottleneck: resolving base currency plus variants plus active modifiers into an admitted runtime plan.

Chosen boundary:

- implement only a single-operation resolver skeleton;
- dispatch only to already accepted runtime operation objects;
- define inactive filter fields as interface shape, but fail closed on any active variant or modifier layer.

This is broad enough to stop future special-case drift and narrow enough to avoid new mechanics.

