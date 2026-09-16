# GitHub issue projection

The roadmap is engineering authority. GitHub Issues are coordination projections.

Supported relationships: `PARENT_OF`, `DEPENDS_ON`, `BLOCKS`, `SUPERSEDES`, `REVISION_OF`, `RELATES_TO`, `INTEGRATED_BY`, `DUPLICATES`.

Future `DISCOVERY_REQUIRED` nodes need not create speculative issues. Executable issue-based work should have an issue projection contract when GitHub coordination is required.

## Separate engineering lifecycle from verified GitHub presence

Every issue-graph node records engineering state separately from the **last verified** external state:

```text
state        = OPEN | ACTIVE | COMPLETE | SUPERSEDED | CANCELLED
github_state = ABSENT | OPEN | CLOSED | UNKNOWN
```

`ABSENT` means no GitHub issue has yet been verified for that node. `UNKNOWN` means a prior GitHub locator exists but its current external state must be re-observed. `OPEN|CLOSED` describe verified external state, never merely desired state.

Verified external identity belongs under:

```yaml
github:
  issue_number: 123
  issue_id: "<provider-id>"
  url: "<optional-url>"
```

This prevents a CREATE attempt or timeout from being mistaken for successful issue creation. Desired GitHub mutations and uncertain external writes live in `GHGEN-*` / `GHOP-*` operation journals until verified readback reconciles them into `ISSUE_GRAPH.yaml`.

This separation also prevents a GitHub-closed issue from being mistaken for completed engineering work, and permits terminal/superseded engineering state while external closure remains pending.

## Operational GitHub publication

When `REPO_STATE.projection.adapter: GITHUB_ISSUES`, the newest desired projection is an immutable generation:

```text
GHGEN-xxxx
  └── GHOP-xxxx CREATE | LINK | UPDATE | PUBLISH_HANDOVER |
                  SUPERSEDE | REVISE | CLOSE | REOPEN
```

Publication is crash-safe:

```text
prepare generation
→ select one dependency-ready GHOP
→ durably mark ATTEMPTED_UNCONFIRMED
→ perform external mutation
→ read back external state
→ reconcile verified observation
→ update ISSUE_GRAPH verified state
→ move to the next GHOP
```

Never update `ISSUE_GRAPH.github_state` from the write-call response alone. Verification/readback is the reconciliation boundary.

See `github-program-projection.md` for the complete transaction, idempotency markers, retry rules, capability limitations, and generation supersession semantics.

## Parent/child projection tree

`PARENT_OF` is a projection hierarchy, not an alternative roadmap. When any `PARENT_OF` edge exists, `ISSUE_GRAPH.yaml` declares `graph_revision` and every aggregate parent records a `child_rollup` bound to that revision.

The parent/child graph must be a DAG and every child has at most one direct parent. Each parent rollup contains the exact set of **direct** children with their current work state and verified GitHub state. The validator recomputes the parent projection from those children:

```text
any direct child ACTIVE    -> derived_state ACTIVE
else any direct child OPEN -> derived_state OPEN
else all direct children terminal -> derived_state COMPLETE
```

A non-superseded/non-cancelled aggregate parent's work state must equal that derived state. A closed aggregate issue may not hide a direct child whose GitHub projection is anything other than `CLOSED`. Because aggregate children are validated against their own direct children first, the same rule recursively covers arbitrarily deep parent/child trees.

The direct-child snapshot is revision-bound so a parent cannot claim current rollup state using an older child set. Multiple parents, cycles, stale snapshots, omitted direct children and invented children are invalid.

A body hyperlink or prose mention does not prove a provider-native parent/sub-issue relationship. A `LINK` operation is VERIFIED only when the external provider relation is read back. If the available integration cannot create or verify the native relation, keep the projection incomplete and report the capability limitation rather than claiming a sub-issue exists.

A rollup is never authoritative engineering state. If the roadmap and issue rollup disagree, reconcile the projection to the roadmap rather than changing roadmap intent to make the issue tree look consistent.

## Closure receipt

A GitHub issue may become `github_state: CLOSED` only after its work lifecycle is terminal and the mapped roadmap node is terminal. The repository closure receipt must retain:

- explicit terminal acceptance entries and their durable basis;
- explicit evidence entries with `PASS | FAIL | NOT_RUN | NA`, exact `basis_ref`, and terminal disposition;
- PR disposition;
- final checkpoint;
- every unresolved item and its current state/basis;
- remaining-work disposition and successor when work was transferred or superseded.

`evidence_terminal: true` never means all evidence passed. A retained `FAIL` or `NOT_RUN` may be terminal only when its limitation/transfer disposition is explicit. `FAIL` or `NOT_RUN` cannot be relabeled `SATISFIED` merely to close an issue.

Repository closure truth comes first. A `GHOP-* CLOSE` may then project it externally. Only verified external readback changes `github_state` to `CLOSED`.

For aggregate parents, child projection must also be reconciled before closure: a parent cannot close while a direct child remains externally unresolved/open. Recursive validation prevents a deep ancestor from becoming apparently terminal while a descendant remains active underneath a stale intermediate rollup.

## Supersession

`SUPERSEDES` is two-sided and evidence-preserving. The predecessor receipt transfers unresolved acceptance, inputs, risks, decisions and evidence together with durable transfer basis. The successor inheritance repeats the transferred values exactly.

Transferred acceptance/evidence is structured, not identifier-only. A successor may not inherit `EV-7` by name while silently changing its status from `NOT_RUN` to `PASS`, changing its exact evidence basis, or dropping its reason.

Supersession lineage is linear and acyclic at the issue level. One predecessor has at most one direct successor and one successor has at most one direct predecessor. If work must split, express the split through roadmap/child-issue topology rather than competing `SUPERSEDES` successors.

A successor may itself later be superseded. For an intermediate A -> B -> C chain, every unresolved acceptance/evidence item B inherited from A must either:

1. appear unchanged in B's outgoing supersession receipt to C; or
2. appear in `B.supersession_resolution` with an explicit terminal disposition (`RESOLVED | CANCELLED_BY_OWNER | NOT_APPLICABLE`) and durable basis.

An inherited item may not be both carried and resolved, may not disappear silently, and a resolution receipt may not claim an ID that was never inherited. New unresolved B-specific items may be added to B's outgoing transfer normally.

A `GHOP-* SUPERSEDE` only publishes this existing repository relationship externally. It does not create engineering supersession authority.

A superseded issue may remain `github_state: OPEN` while projection closure is pending; that is external projection lag, not renewed engineering authority. When external closure is verified, its closure receipt must already identify the successor and matching repository `SUPERSEDES` relationship.

Unresolved work may never disappear through issue closure, GitHub publication, or supersession.
