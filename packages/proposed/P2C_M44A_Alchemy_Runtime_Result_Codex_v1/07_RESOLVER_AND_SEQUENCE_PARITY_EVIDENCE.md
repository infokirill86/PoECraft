# Resolver and sequence parity evidence

The direct Alchemy harness and the accepted resolver compile the same `AlchemyOperation` contract.

A one-step M43-A request containing `alchemy` was compared against direct execution:

- exact state-only terminal hashes and exact masses match;
- seeded terminal state hashes match for every sampled trajectory;
- ordered selected modifier identities match;
- the M43-A trace contains one caller-visible step with four selected internal modifier identities;
- the executor registry contains an explicit `alchemy` entry and still fails closed for admitted rows without an executor.

Alchemy is therefore composable as one accepted operation while its four internal additions remain hidden from caller sequence structure.
