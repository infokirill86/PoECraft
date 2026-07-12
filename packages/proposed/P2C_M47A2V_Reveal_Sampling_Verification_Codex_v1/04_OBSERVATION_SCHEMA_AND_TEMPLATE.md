# Observation Schema and Template

Canonical schema: `schemas/reveal_observation.schema.yaml`.

The required fields capture identity, setup, item/Jawbone context, installed conflicts, compatible exclusive knowledge, offers, display order, failure state, and screenshot references. `eligible_pool_snapshot` is optional because it may not always be reconstructible, but D4 remains inconclusive without it.

## Minimal JSON template

```json
{
  "schema_version": "p2c.m47a2v.reveal_observation.v1",
  "observations": [
    {
      "observation_id": "qs-preserved-prefix-001",
      "setup_id": "qs-ilvl82-preserved-prefix-fixed-v1",
      "captured_at_utc": "2026-07-12T12:00:00Z",
      "item_class": "quarterstaff",
      "item_level": 82,
      "jawbone_row": "preserved_jawbone",
      "stored_mml": null,
      "placeholder_side": "prefix",
      "installed_modifier_ids": ["replace_with_canonical_id"],
      "installed_family_ids": ["replace_with_family_id"],
      "installed_group_ids": ["replace_with_group_id"],
      "compatible_exclusive_known": true,
      "compatible_exclusive_modifier_ids": ["replace_with_exclusive_id"],
      "eligible_pool_snapshot": null,
      "offers": [
        {"modifier_id":"id1","tier":1,"family_id":"f1","group_ids":["g1"],"exclusive":true,"generation_weight":null,"display_order":1},
        {"modifier_id":"id2","tier":2,"family_id":"f2","group_ids":["g2"],"exclusive":false,"generation_weight":null,"display_order":2},
        {"modifier_id":"id3","tier":1,"family_id":"f3","group_ids":["g3"],"exclusive":false,"generation_weight":null,"display_order":3}
      ],
      "reveal_success_or_failure": "success",
      "failure_code": null,
      "display_order_recorded": true,
      "item_unchanged_after_failure": null,
      "currency_consumed_on_failure": null,
      "screenshot_references": ["local-capture/qs-preserved-prefix-001.png"],
      "notes": "pilot capture"
    }
  ]
}
```

The schema rejects extra fields, malformed three-offer windows, invalid display order, duplicate observation IDs, and Jawbone/MML mismatches through schema plus tool validation.
