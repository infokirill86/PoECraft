# Candidate Project-model Decisions

These are proposed decisions for ChatGPT/User after Claude audit. They are not self-accepted by this package.

## Decision 1: base Chaos removal rule

Recommended:

`BASE_CHAOS_REMOVAL = random eligible removable non-fractured installed modifier instance`

Reason:

- PoE2DB and PoE2 Wiki both state base Chaos removes a random modifier;
- both distinguish Whittling as an Omen affecting the next Chaos Orb;
- repo `data/omens.yaml` also models Whittling as an Omen effect.

Label:

- PROJECT-MODEL ONLY;
- NOT SERVER-TRUTH EXACT PROBABILITY;
- SOURCE/PROVENANCE remains open.

## Decision 2: base Chaos is not Whittling

Recommended:

`BASE_CHAOS_DOES_NOT_USE_LOWEST_MODIFIER_LEVEL_SELECTION`

Reason:

- lowest-level selection is attached to Omen of Whittling, not base Chaos.

Required follow-up:

- clarify M37 design so it does not imply Whittling is base behavior;
- optionally clarify `data/mechanics_evidence.yaml` later with "Omen-only" wording in a separately gated metadata/doc correction.

## Decision 3: base Annulment removal rule

Recommended:

`BASE_ANNULMENT_REMOVAL = random eligible removable non-fractured installed modifier instance`

Reason:

- public source wording says random modifier removal;
- side/desecrated filtering exists as Omen behavior;
- no checked source supports base side-first selection or weights.

## Decision 4: ordinary_add / Exalted-like add selection

Recommended:

`ORDINARY_ADD_SELECTION = one combined legal weighted pool after capacity and legality filters`

Reason:

- accepted project runtime already uses this model;
- public source wording says random add, while side Omens explicitly constrain prefix/suffix;
- no checked source supports base side-first selection.

## Decision 5: M37-A scope after correction

Recommended:

M37-A may be base `chaos` runtime only after:

- this verification passes Claude audit;
- ChatGPT/User explicitly accepts the base Chaos project-model decision;
- M37 design is patched or accepted with the correction.

M37-A should still exclude:

- Whittling;
- side Omens;
- Greater/Perfect Chaos MML modes;
- public numeric release;
- optimizer/economics/advice.

