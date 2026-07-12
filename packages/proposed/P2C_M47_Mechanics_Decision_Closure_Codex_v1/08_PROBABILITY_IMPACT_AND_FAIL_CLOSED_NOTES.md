# Probability Impact and Fail-Closed Notes

No numeric probability value is published in this package.

Each open decision changes the exact path graph:

- D1 changes the side branch and whether a removal branch exists.
- D2 changes removal candidate identity and path mass.
- D3 changes offer-category composition before row selection.
- D4 changes the joint distribution of the complete offer set; marginal row weights alone are insufficient.
- D5 changes whether an incomplete branch stops, emits a smaller decision set, or changes eligibility rules.

The exact engine must enumerate the chosen model with rational arithmetic. Seeded MC must call the same Jawbone/Reveal builders and decision stages. No exact overflow may silently substitute MC, and no missing policy may fall back to candidate YAML.

Until D1-D5 are selected, resolver admission must remain blocked. Any future mismatch between selected policy, YAML, executor, exact enumeration, and MC is a hard failure.
