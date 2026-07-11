# Whittling Minimum-Level and Tie Proof

Whittling compiles to the existing `RemovalPoolRequest.lowest_modifier_level` selector.

The canonical removal builder applies stages in this order:

1. construct installed-instance identities;
2. exclude fractured instances;
3. apply any compatible side filter;
4. identify the minimum modifier level among the remaining eligible instances;
5. retain all tied instances at that minimum;
6. assign equal candidate weight for the accepted uniform tie policy.

Focused evidence includes a lower-level fractured prefix and eligible prefixes at different modifier levels. The fractured row is absent and only the minimum eligible non-fractured level remains. The subsequent Chaos add stage is unchanged.

The uniform tie rule remains an explicit source-open project-model policy, not a server-truth claim.
