# Authority State Model — version 3

## Why state is split

A single `STATE: BLOCKED` cannot distinguish an engineering blocker from an absent custodian, failed qualification, paused AUTO mode, or missing merge authority. Version 3 therefore uses orthogonal state planes.

## Required state planes

```text
ENGINEERING_STATE
READY | IN_PROGRESS | BLOCKED | COMPLETE

CUSTODY_STATE
HELD | VACANT | TAKEOVER_REQUIRED | QUALIFIED_PENDING_RECONCILIATION | RECONCILING

QUALIFICATION_STATE
NOT_REQUIRED | PENDING | PASS | FAIL | DEFERRED

WRITE_AUTHORITY
READ_ONLY | WRITE_ALLOWED | BLOCKED

AUTO_STATE
RUNNING | PAUSED | BLOCKED | NOT_APPLICABLE

MERGE_AUTHORITY
OWNER_ONLY | AUTHORIZED
```

`STATE` may remain as a derived compatibility summary for existing scripts, but it does not grant authority.

## Replacement-agent transition

```text
agent lost
-> CUSTODY_STATE TAKEOVER_REQUIRED
-> QUALIFICATION_STATE PENDING
-> WRITE_AUTHORITY READ_ONLY
-> AUTO_STATE PAUSED

independent qualification PASS
-> QUALIFICATION_STATE PASS
-> CUSTODY_STATE QUALIFIED_PENDING_RECONCILIATION
-> WRITE_AUTHORITY READ_ONLY

post-PASS reconciliation starts
-> CUSTODY_STATE RECONCILING
-> WRITE_AUTHORITY READ_ONLY

reconciliation clears live/crash-window/roadmap/overlap authority
-> CUSTODY_STATE HELD
-> WRITE_AUTHORITY WRITE_ALLOWED
```

Qualification PASS is necessary but not sufficient for write authority.

## Fail/deferred

```text
FAIL or DEFERRED
-> WRITE_AUTHORITY READ_ONLY
-> no accepted production mutation
```

## Current custodian continuing

A currently accepted custodian may use:

```text
CUSTODY_STATE: HELD
QUALIFICATION_STATE: NOT_REQUIRED
WRITE_AUTHORITY: WRITE_ALLOWED
```

until a qualification-refresh trigger or custody change occurs.

## Hard invalid combinations

Reject or fail closed when:

- `TAKEOVER_REQUIRED` or `VACANT` has `WRITE_ALLOWED`;
- `PENDING`, `FAIL`, or `DEFERRED` has `WRITE_ALLOWED`;
- `QUALIFIED_PENDING_RECONCILIATION` has `WRITE_ALLOWED`;
- `RECONCILING` has `WRITE_ALLOWED`;
- `WRITE_ALLOWED` exists without `CUSTODY_STATE: HELD`;
- agent loss leaves AUTO `RUNNING`.

## Separate authorities

These do not imply one another:

```text
qualification PASS
engineering validation PASS
roadmap-write authorization
WRITE_ALLOWED
merge authorization
chain completion
```
