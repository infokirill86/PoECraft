# Single-Dispatcher Validator Evidence

The schema-v2 validator now performs a Git index check before parsing dispatcher content.

Pass condition:

- the validated path is exactly `work/active/ACTIVE_TASK.md`;
- `git ls-files -- work/active` returns exactly that one path.

Fail-closed cases include:

- a second tracked historical task or note under `work/active/`;
- a missing tracked live dispatcher;
- validating a differently located dispatcher;
- inability to query the Git tracked-file set;
- all prior YAML/schema/reference/status-actor failures.

An untracked local note does not count as a tracked live dispatcher. This preserves harmless private scratch use while preventing competing repository truth surfaces.
