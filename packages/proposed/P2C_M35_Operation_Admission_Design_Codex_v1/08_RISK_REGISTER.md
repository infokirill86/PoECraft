# Risk Register

| Risk | Severity | Why it matters | Mitigation |
|---|---:|---|---|
| Framework grows into abstract operation algebra | High | Could recreate infrastructure drift under a new name | Keep M35 lean and Annulment-anchored |
| Annulment implementation starts during design | High | Would bypass operation-admission audit | M35 is design-only; M35-A requires separate gate |
| Fractured modifier can be removed | Critical | Violates standing invariant and item model | Hard requirement plus negative-control proof |
| Empty removal pool mutates item | High | Invalid transition would corrupt probability mass | Explicit no-transition/no-consumption terminal |
| Uniform candidate unit is ambiguous | Medium | Could sample families/mod IDs instead of installed instances | Candidate unit is installed modifier instance / removal candidate key |
| Data active flag treated as runtime acceptance | High | Static data scope would bypass executable acceptance | State that data row is not runtime admission |
| Source/provenance closure smuggled into design | Medium | Would overclaim server truth | PROJECT-MODEL label and blockers remain open |
| Omen selector variants enter M35-A silently | Medium | Expands scope beyond base Annulment | Defer selectors unless separately authorized |
| Public numeric release leaks from later evidence | Medium | Violates release gate policy | Numeric evidence remains internal/quarantined unless separately approved |

