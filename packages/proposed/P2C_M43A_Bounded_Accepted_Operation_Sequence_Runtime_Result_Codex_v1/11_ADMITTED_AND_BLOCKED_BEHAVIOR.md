# Admitted and Blocked Behavior

| Request behavior | M43-A result |
|---|---|
| fixed one-to-eight-step accepted sequence | admitted for evaluation |
| admitted row with explicit registered executor | admitted subject to resolver/current-state checks |
| admitted row without registered executor | hard fail closed |
| non-admitted operation, including Alchemy | hard fail closed |
| unsupported variant or active modifier | hard fail closed |
| more than eight steps | hard fail closed |
| `stop_on_no_transition` false | hard fail closed |
| exact ceiling overflow | structured stop; no approximation |
| conditional, fallback, retry, repeat-until, route generation | not represented or admitted |
| ranking, recommendation, optimizer, economics, EV, advice | not represented or admitted |
| public probability release | not included |

Alchemy remains deferred rather than rejected as a future project direction.
