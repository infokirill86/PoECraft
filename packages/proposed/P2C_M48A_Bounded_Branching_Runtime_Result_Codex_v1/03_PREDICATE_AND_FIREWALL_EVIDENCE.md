# Predicate Registry and Evaluator/Optimizer Firewall

## Accepted predicate floor

The registry is closed and has no callback, plugin, expression-language, or caller-function seam.

| Predicate | Input | Output | Data authority |
|---|---|---|---|
| `success_class.v1` | Current canonical `ItemState` | `TOP`, `ACCEPTABLE`, or `NOT_SUCCESS` | Existing `config/success_criteria.yaml` only |

The classifier validates the exact currently accepted criteria shape before use. Unknown keys, unsupported schema/status/tier convention/evaluation order, or origin-flag behavior fail closed. It does not write, extend, or reinterpret the config outside that shape.

## Firewall controls

- The caller supplies every node, edge, operation request, predicate node, and terminal label.
- The evaluator has no route-generation, comparison, ranking, recommendation, search, retry, or optimization API.
- `PredicateDecision` contains only predicate ID, categorical result, and state hash.
- Predicate outputs contain no score, probability, cost, EV, utility, desirability, or ranking.
- Predicates inspect only current state and accepted static success data.
- Internal exact masses remain quarantined; public summaries state `public_numeric_release: false` and omit probability values.
- Unknown predicates and incomplete categorical coverage fail closed.

## Evidence

Focused tests prove:

- deterministic classifier known answers for TOP/ACCEPTABLE/NOT_SUCCESS;
- config-shape mutation fails closed rather than inventing behavior;
- registry contains only `success_class.v1`;
- decision fields/payload contain none of the forbidden scoring vocabulary;
- a probability-threshold predicate is rejected;
- route-generation/ranking/recommendation methods do not exist;
- branches use the post-operation state hash, not the root state.
