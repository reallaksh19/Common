# Independent status planes

V2.5 separates four status planes so a quality concern, unavailable test runner or missing evidence is not mislabeled as an engineering blocker.

## Execution

`IDLE | READY | ACTIVE | WAITING | COMPLETE`

Execution answers what work is happening, whether material work can continue, and the exact next action. `WAITING` may be non-fatal; it does not imply unsafe engineering.

## Quality

`CLEAR | NEEDS_ATTENTION | OWNER_REVIEW_REQUIRED`

Quality records design, maintainability, UX, performance, accessibility and review findings. A quality finding becomes a hard stop only when it independently violates acceptance, authority or safety.

## Evidence

`COMPLETE | PARTIAL | NOT_RUN | FAILED | NA`

Evidence records what was actually executed or proven. For `NOT_RUN`, record concrete items and causes such as `INFRASTRUCTURE`, `UNAVAILABLE_TOOL`, `NOT_SCHEDULED`, `DEPENDENCY_WAIT` or `OTHER`. `NOT_RUN` never means engineering `FAIL` and does not by itself activate the stop plane.

## Stop

The stop plane is either inactive or names one true category:

`OWNER_DECISION_REQUIRED | ESSENTIAL_INPUT_MISSING | AUTHORITY_VIOLATION | PROTECTED_INVARIANT_FAILURE | WRITE_COLLISION | SUPERSEDED_EP | ROADMAP_CONFLICT | REPOSITORY_STATE_CONFLICT | UNSAFE_ENGINEERING_RESULT`.

An active stop requires a plain-language reason and durable basis. If stop is inactive, category is `NONE`.

## Human language

Render these independently: execution state, whether work can continue, quality state/findings, evidence state/not-run items, and hard stop. Avoid the generic word `blocked` when a more precise state is available.
