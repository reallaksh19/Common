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

## Parent/child projection tree

`PARENT_OF` is a projection hierarchy, not an alternative roadmap. When any `PARENT_OF` edge exists, `ISSUE_GRAPH.yaml` declares `graph_revision` and every aggregate parent records a `child_rollup` bound to that revision.

The parent/child graph must be a DAG and every child has at most one direct parent. Each parent rollup contains the exact set of **direct** children with their current work state and GitHub state. The validator recomputes the parent projection from those children:

```text
any direct child ACTIVE  -> derived_state ACTIVE
else any direct child OPEN -> derived_state OPEN
else all direct children terminal -> derived_state COMPLETE
```

A non-superseded/non-cancelled aggregate parent's work state must equal that derived state. A closed aggregate issue may not hide a direct child that is still GitHub OPEN. Because aggregate children are validated the same way, this rule propagates recursively through deep trees.

A rollup is never authoritative engineering state. If the roadmap and issue rollup disagree, reconcile the projection to the roadmap rather than changing roadmap intent to make the issue tree look consistent.

## Closure receipt

A GitHub issue may become `github_state: CLOSED` only when its work lifecycle is terminal and the mapped roadmap node is terminal. The closure receipt must retain:

- explicit terminal acceptance entries and their durable basis;
- explicit evidence entries with `PASS | FAIL | NOT_RUN | NA`, exact `basis_ref`, and terminal disposition;
- PR disposition;
- final checkpoint;
- every unresolved item and its current state/basis;
- remaining-work disposition and successor when work was transferred or superseded.

`evidence_terminal: true` never means all evidence passed. A retained `FAIL` or `NOT_RUN` may be terminal only when its limitation/transfer disposition is explicit. `FAIL` or `NOT_RUN` cannot be relabeled `SATISFIED` merely to close an issue.

For aggregate parents, child projection must also be reconciled before closure: a parent cannot close while a direct child remains GitHub OPEN.

## Supersession

`SUPERSEDES` is two-sided and evidence-preserving. The predecessor receipt transfers unresolved acceptance, inputs, risks, decisions and evidence together with durable transfer basis. The successor inheritance repeats the transferred values exactly.

Transferred acceptance/evidence is structured, not identifier-only. A successor may not inherit `EV-7` by name while silently changing its status from `NOT_RUN` to `PASS`, changing its exact evidence basis, or dropping its reason.

Supersession lineage is linear and acyclic at the issue level. One predecessor has at most one direct successor and one successor has at most one direct predecessor. If work must split, express the split through roadmap/child-issue topology rather than competing `SUPERSEDES` successors.

A successor may itself later be superseded. For an intermediate A -> B -> C chain, every unresolved acceptance/evidence item B inherited from A must either:

1. appear unchanged in B's outgoing supersession receipt to C; or
2. appear in `B.supersession_resolution` with an explicit terminal disposition (`RESOLVED | CANCELLED_BY_OWNER | NOT_APPLICABLE`) and durable basis.

An inherited item may not be both carried and resolved, and it may not disappear silently. New unresolved B-specific items may be added to B's outgoing transfer normally.

A superseded issue may remain `github_state: OPEN` while projection closure is pending; that is external projection lag, not renewed engineering authority. When it is closed, its closure receipt must identify the successor and the `SUPERSEDES` relationship.

Unresolved work may never disappear through issue closure or supersession.
