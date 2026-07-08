# Missing Capability Map

## Highest-value missing simulator capability

The highest-value missing capability is accepted-operation composition:

```text
accepted operation A -> branch-specific state -> accepted operation B
```

This is needed before the simulator becomes a practical crafting emulator rather than a set of isolated operation tests.

## Missing chain capabilities

- Heterogeneous chain model over accepted operations only.
- Per-step operation identity and semantics version.
- Branch-specific pool rebuild after each step.
- Exact/oracle path product across mixed operation types.
- Terminal aggregation across different path histories.
- No-transition semantics inside a chain.
- Deterministic replay across mixed operation steps.
- Diagnostics that identify operation step, pool digest, selected candidate, state digest, and no-transition reason.
- Negative controls for mixed-chain misuse.

## Still intentionally missing

- Annulment variants and Omens.
- Chaos.
- Essence.
- Fracture.
- Desecrate/Jawbone/Reveal.
- Lich behavior.
- Source/provenance closure.
- MML closure.
- PD-013 closure.
- Public numeric release.
- Optimizer/economics/advice.
- Automation/GitHub Actions.

