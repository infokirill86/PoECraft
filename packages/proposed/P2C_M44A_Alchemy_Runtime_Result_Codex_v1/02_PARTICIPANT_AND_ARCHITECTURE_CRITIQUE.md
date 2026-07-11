# Participant and architecture critique

No material objection remained after the User gate.

The boundary is right-sized because the uncertain mechanic was explicitly ratified as project-model behavior and the unresolved fractured interaction remains outside the floor. Base Alchemy is one coherent operation with one consumption boundary and therefore should not be represented as four M43-A user steps.

The implementation uses a dedicated atomic `AlchemyHarness`, but it does not copy legality or weighting mechanics. Every internal draw goes through the accepted `build_ordinary_add_pool` path. Resolver and bounded-sequence integration compile and execute the Alchemy action as one accepted operation.

The main architecture risk was partial mutation. It is prevented by building an isolated empty Rare state and returning it only after the fourth successful internal add. Failure returns the untouched input state.
