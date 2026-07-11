# Plain-Language Summary for Kirill

P2C can now take a short crafting sequence written by the caller and execute it step by step. After every successful currency, the next currency is resolved again against the item that actually exists on that branch. This is the bridge from separate currency simulators to evaluating a real user-written crafting route.

The engine still does not choose a route. There are no conditions, retries, recommendations, rankings, costs, or optimization.

Exact calculation stops visibly if its safety ceilings are exceeded. It never silently cuts branches or switches to Monte Carlo. Seeded Monte Carlo uses the same accepted operation executors and can be replayed deterministically.

M43-A remains proposed until Claude audits the implementation and ChatGPT/User accepts it.
