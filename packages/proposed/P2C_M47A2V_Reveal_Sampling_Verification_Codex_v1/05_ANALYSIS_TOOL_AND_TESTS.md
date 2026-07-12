# Offline Analysis Tool and Tests

Tool: `tools/analyze_reveal_observations.py`

Example:

```text
python tools/analyze_reveal_observations.py captures.json --output internal-report.json
```

## What it does

- validates JSON/JSONL observations against the canonical schema;
- checks unique observation IDs, display order, Jawbone/MML context, and pool references;
- summarizes internal exclusive-offer counts;
- detects D3 counterexamples;
- detects family/group conflicts within an offer window and against installed state;
- checks whether offered tier rows exist in supplied eligible-pool snapshots;
- screens display positions without claiming independence;
- separates D5-supporting failures from contradictions;
- states what the current data can and cannot distinguish.

## What it cannot do

- modify runtime, mechanics evidence, ledgers, or accepted status;
- accept D3-D5;
- identify D4 from offer windows alone;
- turn a limited sample into server truth;
- produce crafting rankings, advice, or a public probability release.

The report labels itself `internal_quarantined_evidence_only` and explicitly records that no runtime/truth update was performed.

Focused tests cover valid analysis, D3 counterexamples, family/group conflicts, D5 support/contradiction, fail-closed schema behavior, CLI output, and non-mutation boundaries.
