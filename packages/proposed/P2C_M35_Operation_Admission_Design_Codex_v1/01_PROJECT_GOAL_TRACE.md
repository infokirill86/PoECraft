# Project Goal Trace

## What P2C is building

P2C is a Path of Exile 2 crafting simulator and later optimizer.

The current accepted runtime is strong for accepted `ordinary_add`, but a useful simulator cannot remain a one-operation harness. It needs a controlled way to admit additional real operations while preserving exact/oracle checks, seeded MC checks, replayability, and audit boundaries.

## Current accepted foundation

Accepted foundation relevant to M35:

- GitHub Layer A runtime/data/config/schema/tool baseline is accepted and pinned as project-model baseline.
- M32 seeded MC harness is accepted.
- M33 oracle-convergence validation is accepted for accepted `ordinary_add`.
- M34-A multi-seed single-step hardening is accepted for accepted `ordinary_add`.
- M34-B1 exactly-two-step accepted-`ordinary_add` sequence hardening is accepted.
- New executable mechanics beyond accepted `ordinary_add` remain closed.

## Why M35 matters

M35 moves P2C from "we can simulate one add operation safely" toward "we can admit new crafting operations safely."

The design does this without opening implementation risk:

- it defines what any new operation must prove before runtime admission;
- it chooses one concrete first candidate, Annulment;
- it keeps SOURCE/PROVENANCE, MML, PD-013, public numeric release, optimizer/economics, and automation boundaries intact.

## Why not more M34 by default

More `ordinary_add` hardening may still be useful later, but it is no longer the highest-value default move. The main product risk is now operation breadth, not another layer of confidence around a single accepted operation.

