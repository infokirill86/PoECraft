# Plain-language summary for Kirill

What changed:

- Added the first resolver skeleton for future currency/variant/modifier handling.
- It answers a narrow question: "is this requested operation allowed to become an executable operation plan right now?"
- If yes, it returns one of the existing accepted operation objects.
- If no, it fails closed.

Why it matters:

- Without this seam, future Greater/Perfect/Whittling/Omen work would likely become scattered special-case code.
- With this seam, the engine has one narrow place where operation admission is checked.
- This keeps future expansion safer: data/catalog readiness is not confused with runtime permission.

What it can resolve now:

- `ordinary_add`;
- base `annulment`;
- base `chaos`.

What it deliberately refuses now:

- active catalog rows that are not runtime-admitted, such as Exalted-like and Greater/Perfect Chaos rows;
- variants such as `greater` or `perfect`;
- modifier layers such as Whittling or side Omens.

What remains proposed:

- The M38-A implementation itself is not accepted until Claude audit and ChatGPT/User gate acceptance.

Who is next:

- Claude audits this package.

