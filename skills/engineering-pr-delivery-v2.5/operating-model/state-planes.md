# Independent status planes

V2.5 separates execution, quality, evidence and stop state so a quality concern, unavailable test runner, deferred confirmation or missing evidence is not mislabeled as an engineering blocker.

## Execution

Execution state is `IDLE | READY | ACTIVE | WAITING | COMPLETE` and separately carries:

```text
can_continue: true | false
material_authority: WRITE | READ_ONLY | NONE
```

`can_continue` answers whether useful relay work can still proceed. `material_authority` is the **route/repository-level** material-write posture: whether the current route is permitted to modify engineering state in principle. These are intentionally independent.

`material_authority` is not candidate admission. Do not set it to `READ_ONLY` merely because a particular candidate lacks DISC/QUAL/TC. Candidate-specific permission is derived separately by `TAKEOVER_CERTIFIED(route,candidate)` and `MATERIAL_WRITE_READY(route,candidate,live_git)`.

Examples:
- `ACTIVE + can_continue:true + WRITE`: normal material execution.
- `ACTIVE + can_continue:true + READ_ONLY`: inspect, validate, reconcile or prepare evidence, but do not change engineering state.
- `WAITING + can_continue:false + READ_ONLY`: required execution is unavailable; preserve custody and wait/reconcile without writes.
- `INITIALIZING/IDLE/TERMINAL`: material authority is `NONE`.

An active hard stop can never retain `WRITE` authority.

## Quality

`CLEAR | NEEDS_ATTENTION | OWNER_REVIEW_REQUIRED`

Quality records design, maintainability, UX, performance, accessibility and review findings. A quality finding becomes a hard stop only when it independently violates acceptance, authority or safety.

## Evidence

`COMPLETE | PARTIAL | NOT_RUN | FAILED | NA`

Evidence records what was actually executed or proven. For `NOT_RUN`, record concrete items and causes such as `INFRASTRUCTURE`, `UNAVAILABLE_TOOL`, `NOT_SCHEDULED`, `DEPENDENCY_WAIT` or `OTHER`. `NOT_RUN` never means engineering `FAIL` and does not by itself activate the stop plane.

## Stop

The stop plane is either inactive or names one true category:

`OWNER_DECISION_REQUIRED | ESSENTIAL_INPUT_MISSING | AUTHORITY_VIOLATION | PROTECTED_INVARIANT_FAILURE | WRITE_COLLISION | SUPERSEDED_EP | ROADMAP_CONFLICT | REPOSITORY_STATE_CONFLICT | UNSAFE_ENGINEERING_RESULT`.

An active stop requires a plain-language reason and durable basis, requires `can_continue:false`, and forbids `material_authority: WRITE`. If stop is inactive, category is `NONE`.

## Human language

Render independently: execution state, whether useful work can continue, material authority, quality state/findings, evidence state/not-run items, and hard-stop state. Avoid the generic word `blocked` when a more precise state is available.
