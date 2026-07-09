# Risk and Correction to Previous M37 Design

## Risk if we choose wrong

If base Chaos removal is modeled incorrectly, all later exact and MC calculations can be perfectly deterministic and still wrong.

High-risk wrong outcomes:

- modeling base Chaos as Whittling when base Chaos is random;
- modeling base Chaos as random when active Whittling should constrain removal;
- using the root add pool instead of rebuilding after removal;
- applying side/MML/Omen filters to base operation without gate approval;
- treating `active_in_current_simulation` as executable runtime permission.

## Explicit correction to previous M37 design

The previous design should be corrected as follows:

1. It must state that base `chaos` is source-verified as random-removal wording.
2. It must state that Whittling is an Omen modifier over Chaos, not base Chaos behavior.
3. It must state that "random" is interpreted by the P2C project model as uniform over eligible removable non-fractured installed modifier instances unless later evidence disproves that.
4. It must keep that uniformity label as project-model only, not server truth.
5. It must keep Whittling, side Omens, Greater/Perfect MML, and variants outside base M37-A.

## Does `data/mechanics_evidence.yaml` conflate base Chaos with Whittling?

It is ambiguous enough to deserve clarification.

The file records the Whittling rule, but does not explicitly say "Whittling is Omen-only." Separately, `data/omens.yaml` does show Whittling as an Omen effect for the Chaos group.

Recommended later documentation/data clarification:

- add wording that Whittling applies only when the Whittling Omen is in the action bundle;
- do not change runtime behavior in this verification package.

