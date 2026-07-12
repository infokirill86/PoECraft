# Participant and Architecture Critique

## Is M48 needed now?

Yes, but it should not be another isolated operation admission. Thirty-five of thirty-seven `operations.yaml` rows and ten of seventeen Omen rows are already executable. The two non-admitted operation rows are Reveal and Astrid. Reveal is blocked by real-observation work; Astrid alone does not make the accepted Essence executors use a second crafted slot without a separate crafted-capacity contract.

## Material challenge to the obvious framing

Omen of Light looks like the simplest next mechanic, but accepted runtime cannot yet create a revealed Desecrated modifier. Implementing it now would be mechanically testable only through constructed states and would not close the live quarterstaff route.

Simply increasing fixed sequence length is also weak framing: M43-A already handles one to eight operations. The missing capability is branching on actual results, not a ninth unconditional step.

## Selected correction

Design a finite branching evaluator over accepted operations. Keep it strictly caller-authored and acyclic. It may evaluate a submitted route, but may not generate alternatives, compare routes, choose actions, attach costs, rank outcomes, or publish numeric guidance.

## Right-sized split

M48-A should batch the state classifier, finite-DAG validation, exact/MC execution, replay, and parity because they form one auditable evaluator contract. Cycles, compact `repeat until`, route search, policy synthesis, and optimization stay behind later gates. A caller can explicitly unroll a small retry branch inside the finite graph without introducing loop semantics.

No material mechanics or source objection remains with this boundary.
