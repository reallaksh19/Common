# Authority State Model — version 3

## Why state is split

One `STATE` cannot distinguish engineering readiness, custody, qualification, write authority, AUTO state, or merge permission.

## Required planes

```text
ENGINEERING_STATE
READY | IN_PROGRESS | BLOCKED | COMPLETE

CUSTODY_STATE
HELD | VACANT | TAKEOVER_REQUIRED | QUALIFIED_PENDING_RECONCILIATION | RECONCILING

QUALIFICATION_STATE
NOT_REQUIRED | PENDING | PASS | FAIL | DEFERRED | REQUALIFICATION_REQUIRED

WRITE_AUTHORITY
READ_ONLY | WRITE_ALLOWED | BLOCKED

AUTO_STATE
RUNNING | PAUSED | BLOCKED | NOT_APPLICABLE

MERGE_AUTHORITY
OWNER_ONLY | AUTHORIZED
```

`STATE` may remain a derived compatibility summary but grants no authority.

## Replacement transition

```text
agent lost
-> TAKEOVER_REQUIRED / PENDING / READ_ONLY / AUTO PAUSED

question-set admission VALID
-> exam may be administered; no authority change

independent qualification PASS
-> PASS / QUALIFIED_PENDING_RECONCILIATION / READ_ONLY

post-PASS reconciliation starts
-> RECONCILING / READ_ONLY
```

Then apply post-basis drift:

```text
NONE | METADATA_ONLY
-> qualification coverage RETAINED

MATERIAL_WITHIN_QUALIFIED_BOUNDARY
-> independent coverage confirmation required

MATERIAL_BOUNDARY_CHANGED | AUTHORITY_CHANGED | CONTAMINATED
-> QUALIFICATION_STATE REQUALIFICATION_REQUIRED
-> WRITE_AUTHORITY READ_ONLY
```

Only reconciliation with valid qualification coverage and clear current-state authority may yield:

```text
CUSTODY_STATE: HELD
WRITE_AUTHORITY: WRITE_ALLOWED
```

## Hard invalid combinations

Fail closed when:

- `TAKEOVER_REQUIRED`, `VACANT`, `QUALIFIED_PENDING_RECONCILIATION`, or `RECONCILING` has `WRITE_ALLOWED`;
- `PENDING`, `FAIL`, `DEFERRED`, or `REQUALIFICATION_REQUIRED` has `WRITE_ALLOWED`;
- `WRITE_ALLOWED` exists without `CUSTODY_STATE: HELD`;
- agent loss leaves AUTO `RUNNING`;
- question-set admission is not `VALID` but qualification proceeds;
- material/authority/contaminated drift grants write without required requalification;
- candidate self-admission/self-verification/self-confirmation is used to grant authority.

## Separate authorities

These never imply one another:

```text
question-set admission VALID
qualification PASS
engineering validation PASS
roadmap-write authorization
qualification-coverage retention
WRITE_ALLOWED
merge authorization
chain completion
```
