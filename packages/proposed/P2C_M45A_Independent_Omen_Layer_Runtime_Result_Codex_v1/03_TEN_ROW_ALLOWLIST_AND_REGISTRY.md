# Ten-Row Allowlist and Registry

| Omen ID | Runtime admission | Availability | Effect dimension |
|---|---|---|---|
| `greater_exaltation` | proposed accepted executable modifier | project-model available | add count |
| `sinistral_exaltation` | proposed accepted executable modifier | project-model available | add side: prefix |
| `dextral_exaltation` | proposed accepted executable modifier | project-model available | add side: suffix |
| `sinistral_annulment` | proposed accepted executable modifier | project-model available | removal side: prefix |
| `dextral_annulment` | proposed accepted executable modifier | project-model available | removal side: suffix |
| `sinistral_erasure` | proposed accepted executable modifier | project-model available | Chaos removal side: prefix |
| `dextral_erasure` | proposed accepted executable modifier | project-model available | Chaos removal side: suffix |
| `whittling` | proposed accepted executable modifier | project-model available | minimum-level removal selector |
| `sinistral_crystallisation` | proposed accepted executable modifier | project-model available | Perfect Essence removal side: prefix |
| `dextral_crystallisation` | proposed accepted executable modifier | project-model available | Perfect Essence removal side: suffix |

Every other `data/omens.yaml` row is explicitly blocked/reference-only. Static-data validation fails on missing/invalid statuses, duplicate IDs, or executable admission without project-model availability.

Runtime compilation additionally pins each allowed row's operation group and exact effect shape. Catalogue presence, `active_omen_system`, row name, and narrative mechanics text are never sufficient authority.
