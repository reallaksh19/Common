# GitHub issue projection

The roadmap is engineering authority. GitHub Issues are coordination projections.

Supported relationships: `PARENT_OF`, `DEPENDS_ON`, `BLOCKS`, `SUPERSEDES`, `REVISION_OF`, `RELATES_TO`, `INTEGRATED_BY`, `DUPLICATES`.

Future `DISCOVERY_REQUIRED` nodes need not create speculative issues. Executable issue-based work should have an issue.

## Separate work lifecycle from GitHub state

Every issue-graph node records both:

```text
state        = OPEN | ACTIVE | COMPLETE | SUPERSEDED | CANCELLED
github_state = OPEN | CLOSED
```

This prevents a closed GitHub issue from being mistaken for completed engineering work, and allows repository truth to show a terminal/superseded work state while external projection closure is still pending.

## Closure receipt

A GitHub issue may become `github_state: CLOSED` only when its work lifecycle is terminal and the mapped roadmap node is terminal. The closure receipt must retain:

- explicit terminal acceptance entries and their durable basis;
- explicit evidence entries with `PASS | FAIL | NOT_RUN | NA`, exact `basis_ref`, and terminal disposition;
- PR disposition;
- final checkpoint;
- every unresolved item and its current state/basis;
- remaining-work disposition and successor when work was transferred or superseded.

`evidence_terminal: true` never means all evidence passed. A retained `FAIL` or `NOT_RUN` may be terminal only when its limitation/transfer disposition is explicit. `FAIL` or `NOT_RUN` cannot be relabeled `SATISFIED` merely to close an issue.

## Supersession

`SUPERSEDES` is two-sided and evidence-preserving. The predecessor receipt transfers unresolved acceptance, inputs, risks, decisions and evidence together with durable transfer basis. The successor inheritance repeats the transferred values exactly.

Transferred acceptance/evidence is structured, not identifier-only. A successor may not inherit `EV-7` by name while silently changing its status from `NOT_RUN` to `PASS`, changing its exact evidence basis, or dropping its reason.

A superseded issue may remain `github_state: OPEN` while projection closure is pending; that is external projection lag, not renewed engineering authority. When it is closed, its closure receipt must identify the successor and the `SUPERSEDES` relationship.

Unresolved work may never disappear through issue closure or supersession.
