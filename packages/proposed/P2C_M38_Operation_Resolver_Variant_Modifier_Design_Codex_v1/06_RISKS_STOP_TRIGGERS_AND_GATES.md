# Risks, Stop Triggers, and Gates

## Main risks

1. **Permission confusion.** Catalog rows may look runnable because they are active in data. The resolver must require runtime admission.
2. **Variant overreach.** Greater/Perfect often look like MML-only variants, but this must be confirmed per family before runtime admission.
3. **Omen overreach.** Omens are modifier layers, not base operations. They must not be smuggled into base Chaos/Annulment/Exalted semantics.
4. **Hidden source closure.** Marking a source-backed behavior as "confirmed enough to execute" must not be misread as server truth.
5. **Over-generalization.** A universal operation algebra would slow the project and create design surface not needed yet.

## Stop triggers

Stop before implementation if:

- sources and repo data conflict;
- a user decision is required for source/provenance interpretation;
- a design step would admit Greater/Perfect runtime;
- a design step would admit Omen runtime;
- a design step would implement a new operation;
- a design step would require route planning;
- public numeric output enters scope;
- optimizer/economics/advice enters scope;
- automation enters scope;
- SOURCE/PROVENANCE, MML, or PD-013 closure enters scope.

## Gates that remain separate

Separate explicit gates are required for:

- Greater/Perfect Exalted runtime admission;
- Greater/Perfect Chaos runtime admission;
- Whittling runtime admission;
- side Omen runtime admission;
- desecrated-only Omen runtime admission;
- Essence/Jawbone/Reveal/Fracture/Desecrate runtime;
- chains longer than accepted M36-A scope;
- route planner;
- optimizer/economics/advice;
- public numeric release;
- source/provenance closure;
- MML closure;
- PD-013 closure;
- automation/GitHub Actions/watcher enablement.

