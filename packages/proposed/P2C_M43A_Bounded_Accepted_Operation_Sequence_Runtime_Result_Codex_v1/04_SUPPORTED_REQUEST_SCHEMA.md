# Supported Request Schema

Runtime request objects:

```yaml
sequence_id: caller_supplied_nonempty_identifier
stop_on_no_transition: true
steps:
  - step_id: unique_nonempty_identifier
    currency_id: accepted_registered_currency_or_ordinary_add
    mode_id: nonempty_run_label
    variant_id: null
    active_modifier_ids: []
    mml: null
```

Contract:

- `steps` is a fixed tuple containing one through eight entries;
- step identifiers are unique;
- `stop_on_no_transition` is pinned true;
- variants and active modifiers fail closed;
- caller MML is accepted only where the existing resolver already permits it;
- no conditional, retry, fallback, repeat, policy, ranking, cost, or target-selection field exists.
