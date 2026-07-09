# Proposed MML filter model

## Design intent

MML should be represented as a reusable add-pool filter layer, not as separate hardcoded Greater/Perfect operation functions.

## Filter input

The MML filter receives:

- candidate static modifier rows after ordinary legality filters;
- `mml` threshold, or `null`;
- family ID;
- modifier level;
- tier;
- stable mod ID for deterministic sorting;
- current item state and installed family/group blockers through the already accepted pool builder.

## Filter output

The filter outputs:

- filtered candidate rows;
- excluded row evidence;
- fallback evidence;
- fail-closed defect if strongest-family fallback is ambiguous.

## Proposed order for ordinary add pools

MML should run inside the already accepted ordinary add pool pipeline:

1. determine pool-build rarity and item class;
2. apply allowed side filter if a future admitted modifier layer supplies one;
3. apply side capacity;
4. block installed family IDs;
5. block conflicting installed group IDs;
6. apply MML family-internal threshold with strongest-family fallback;
7. remove non-positive weights;
8. perform weighted sampling over tier rows.

## Applicability

| Operation shape | MML applies? | Reason |
|---|---:|---|
| add-only ordinary weighted operations | yes, to the add pool | Greater/Perfect Transmutation/Augmentation/Regal/Exalted encode `transition.add.mml`. |
| remove-then-add ordinary weighted operations | yes, to the post-removal add pool only | Greater/Perfect Chaos encodes MML under `transition.add`; base removal selection remains separate. |
| removal-only operations | no | MML filters candidate added modifiers, not installed removal targets. |
| Whittling/Omen removal selection | no | Whittling selects lowest modifier-level installed target; it is a removal modifier layer, not MML. |
| Essence guaranteed crafted outputs | not by this model | Essence output is not ordinary weighted MML add in current repo data. |
| Jawbone/reveal MML | related but separate | Reveal has `reveal_mml`; it should not be admitted through Greater/Perfect currency batching. |

## Atomicity

For remove-then-add variants such as Greater/Perfect Chaos:

- removal branch is built first;
- branch-specific post-removal add pool is rebuilt;
- MML applies to that branch-specific add pool;
- if post-removal add pool is empty, the operation no-transitions/no-consumes and must not produce a partial remove-only terminal.

## Fail-closed rules

The resolver must fail closed if:

- a Greater/Perfect operation lacks `runtime_admission_status: accepted_executable_runtime`;
- MML value is missing where the operation requires one;
- MML value is not an integer or is negative;
- MML fallback detects co-equal strongest rows;
- a modifier/variant layer tries to execute through `active_in_current_simulation` instead of runtime admission status;
- an unsupported Omen/modifier layer is present.

