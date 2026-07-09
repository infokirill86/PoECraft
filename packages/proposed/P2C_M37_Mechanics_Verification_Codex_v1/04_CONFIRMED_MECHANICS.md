# Confirmed Mechanics for Project-model Use

Status labels here mean "confirmed enough for P2C project-model design", not server truth.

## Base Chaos-like operation

Project-model confirmation:

- base Chaos-like wording is random removal plus random add;
- lowest-level removal is specifically tied to Omen of Whittling;
- therefore base `chaos` should not be pinned to Whittling behavior.

Recommended base M37 model:

- build eligible removable installed modifier instance pool;
- exclude fractured modifiers;
- select a random eligible instance;
- remove on branch copy;
- rebuild ordinary add pool from the branch-specific post-removal state;
- add one legal modifier from the accepted weighted ordinary-add pool.

The project should explicitly document that "random modifier" is modeled as uniform over eligible installed modifier instances unless later verified otherwise.

## Chaos + Whittling/Omen interaction

Project-model confirmation:

- Omen of Whittling modifies the next Chaos Orb;
- it selects the lowest modifier-level removable modifier;
- tie behavior is not published enough for server truth;
- current repo policy uses uniform tie-break among tied lowest-level instances as project policy.

Whittling should remain out of base M37-A unless explicitly authorized.

## Base Annulment-like removal

Project-model confirmation:

- base Annulment wording is random modifier removal;
- side-specific Annulment behavior appears as separate Omen behavior;
- no checked source indicates base Annulment first chooses prefix/suffix side and then chooses within that side;
- no checked source indicates non-uniform removal weights.

Accepted project model remains uniform over eligible removable installed non-fractured modifier instances, with side/desecrated filters only when the relevant Omen/operation rule is explicitly in scope.

## ordinary_add / Exalted-like add

Project-model confirmation:

- Exalted-like wording is random add of a new modifier;
- side-specific Exalted behavior appears as separate Omen behavior;
- no checked source indicates base Exalted first chooses prefix/suffix side before selecting a mod;
- rare item capacity limits are explicit in the public Exalted wording.

Accepted project model remains: build one legal weighted ordinary-add pool across all eligible prefix/suffix candidates after capacity, family, group, source, and mode filters. Side Omens narrow the pool before selection; they do not imply base side-first selection.

