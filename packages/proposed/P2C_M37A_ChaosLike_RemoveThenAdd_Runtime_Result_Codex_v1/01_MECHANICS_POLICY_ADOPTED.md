# Mechanics Policy Adopted from M37 Verification

This result implements the M37 mechanics policy accepted by ChatGPT/User after Claude GO audit of `P2C_M37_Mechanics_Verification_Codex_v1`.

## Base removal model

- Base Annulment and base Chaos-like removal use one combined pool of eligible removable non-fractured installed modifier instances.
- Selection is uniform over eligible instances.
- Base removal does not choose prefix/suffix side first.
- Fractured modifiers are never removable.

## Base add model

- ordinary_add / Exalted-like add uses one combined legal weighted pool across eligible prefix/suffix candidates.
- Candidate weight is `generation_weight`.
- Side is a capacity/legal filter, not a fixed side-first split.
- Side Omens are separate filtering layers, not base behavior.

## Omen and modifier layers

- Whittling / lowest-modifier-level removal is an Omen layer over Chaos, not base Chaos behavior.
- Side/desecrated Omens are separate behavior layers.
- M37-A does not implement Omens.

## Source status

This is P2C project-model policy only. It is not a PoE2 server-truth claim. SOURCE/PROVENANCE, MML, and PD-013 remain open.

