# Participant Critique and Boundary

The proposed boundary is correct and preferable to incremental checksum scoping.

- The bottleneck was hundreds of Git process launches, not SHA-256 computation.
- One `git cat-file --batch` process preserves full verification and removes that bottleneck.
- Checking only changed files would add cache/state complexity and weaken the simple full-manifest guarantee.
- The change is reconstructible and truth-neutral because byte-identical manifest output is a hard acceptance condition.

No broader refactor or shared operation/runtime work is justified. Wave C package-index work remains a separate later decision.
