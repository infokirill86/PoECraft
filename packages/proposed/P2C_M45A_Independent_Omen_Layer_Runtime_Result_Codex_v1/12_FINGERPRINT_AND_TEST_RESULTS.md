# Semantic Fingerprint Delta and Test Results

## Fingerprints

- prior accepted semantic fingerprint: `fcc793113cb803c3cec71bd8582489edc0efe037fcbce169485427da0d7927b4`
- proposed M45-A semantic fingerprint: `3b20a622bbd4406ce991a4b941390f19bd4ece50afe0aa2afd6b3cc3bac21d25`
- proposed source fingerprint: `9b41bbfd65e54725774dda280158be4510c87b62e3b96502472ae6f799a43dd4`

The semantic delta is limited to:

- admission and project-model availability metadata for the ten authorized Omens;
- exclusion of blocked/reference-only Omen rows from the executable semantic projection;
- the pinned compatibility/effect data already required by the admitted modifier compiler.

No modifier pool data, operation-row admission, base operation mechanics, item state, success criteria, or source-truth closure changed.

## Tests

- focused M45-A suite: `18 passed`;
- full regression suite: `300 passed`;
- foundation validator: PASS;
- M4 validator: PASS;
- ACTIVE_TASK validator: PASS after handoff update;
- package/root checksum verification: required before publication;
- pre-push hook: required before publication.
