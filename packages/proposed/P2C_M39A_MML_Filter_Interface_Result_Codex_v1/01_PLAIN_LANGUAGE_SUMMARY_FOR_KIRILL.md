# Plain-language summary for Kirill

M39-A adds the safe technical slot where MML can live.

In simple terms:

- the resolver can now say: "run accepted ordinary_add, but use this minimum modifier level filter";
- this is only a filter interface;
- it does not turn on Greater or Perfect currency runtime;
- it does not make MML "server truth";
- it does not touch Essences, Whittling, Omens, or new operations.

Why this matters:

Before M39-A, the project had MML logic inside the pool builder, but the operation resolver had no safe way to carry an explicit MML filter. If we later admitted Greater/Perfect variants without this interface, we would risk hardcoding each variant separately.

What changed:

- `OperationResolverRequest` now has an optional `mml` field.
- The field is accepted only for `ordinary_add`.
- Invalid MML values fail closed.
- Passing MML to base Chaos or other catalog operations fails closed.
- Greater/Perfect rows still fail closed because they are not admitted runtime.

What remains proposed:

This M39-A implementation is not accepted until Claude audits it and ChatGPT/User gates it.

Who is next:

Claude should audit this result package.

