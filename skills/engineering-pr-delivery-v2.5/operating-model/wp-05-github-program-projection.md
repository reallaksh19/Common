# WP-05 implementation report — GitHub Program Projection operations

## Result

WP-05 operationalizes GitHub Issues as a crash-safe, idempotent coordination projection while preserving repository roadmap/issue authority.

The repository remains authoritative. A connector write, issue URL, comment, body link, or publication receipt is not convergence. External state becomes trusted only after durable readback verifies the desired operation and reconciliation updates repository projection state.

## Delivered transaction model

```text
repository truth
  -> GHGEN-* immutable desired generation
  -> GHOP-* ordered operation
  -> mark ATTEMPTED_UNCONFIRMED before external mutation
  -> perform GitHub mutation
  -> durable GITHUB_OBSERVATION readback
  -> verify desired external state / relationship / marker
  -> reconcile ISSUE_GRAPH + projection state
  -> IN_SYNC only after all current operations are VERIFIED or SUPERSEDED
```

Supported operation classes:

```text
CREATE
LINK
UPDATE
PUBLISH_HANDOVER
SUPERSEDE
REVISE
CLOSE
REOPEN
```

## External presence truth

`ISSUE_GRAPH.github_state` now represents last verified external reality rather than desired state:

```text
ABSENT   no GitHub issue has been verified for the node
OPEN     verified external issue is open
CLOSED   verified external issue is closed
UNKNOWN  a prior locator exists but external state must be re-observed
```

OPEN/CLOSED require a verified GitHub locator. ABSENT cannot retain a locator. UNKNOWN exists for recovery, not as a desired-state shortcut.

## Generation and operation identity

A required GitHub projection binds `REPO_STATE.projection` to one immutable current generation under `agents/relay/projection/generations/`.

Generation IDs use `GHGEN-*`. Operations use `GHOP-*` with stable idempotency keys and operation markers. A successor generation may supersede an older generation, but the old generation remains durable history and unfinished old operations lose publication authority.

Projection history distinguishes:

```text
SUPERSEDED_BEFORE_PUBLICATION
SUPERSEDED_AFTER_ATTEMPT_UNCONFIRMED
SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED
```

The middle state is important: an external mutation may have happened even when no connector receipt exists.

## Crash-safe publication

The safe ordering is:

```text
select current GHOP
 -> persist ATTEMPTED_UNCONFIRMED + attempt basis
 -> external mutation
 -> read back by stable locator / relay-operation marker
 -> reconcile observation
```

A replacement never retries an uncertain CREATE merely because no connector response was retained. It first searches/re-observes using the durable operation identity. Verified readback can recover a lost connector receipt using explicit `READBACK_RECOVERY:*` evidence.

`github_projection_next.py` serializes publication within the current generation: unresolved/uncertain operation state must be reconciled before later operations are published.

## Repository reconciliation

`reconcile_github_projection.py` consumes a durable `GITHUB_OBSERVATION` and changes repository projection state only when observation semantics validate.

Verified CREATE captures the external issue identity and updates the node to OPEN. CLOSE/REOPEN update only after readback proves the external state. LINK/SUPERSEDE require observed relationship truth. Aggregate parent child snapshots are reconciled after verified state changes without becoming roadmap authority.

`REPO_STATE.relay_readiness.projection_ready` becomes true only when the current generation is fully reconciled; `handover_ready` remains `baton_ready AND projection_ready`.

## Native relationship capability

Repository `PARENT_OF`, `SUPERSEDES`, and other issue relationships remain desired coordination truth. An adapter may claim a native GitHub relationship only when the provider/integration can create and read back that relationship. A Markdown/body hyperlink or prose reference is not equivalent to a verified native parent/sub-issue relationship.

When provider capability is unavailable, the relevant operation remains unresolved/incomplete rather than silently degrading the contract.

## Validators and operator scripts

Delivered/reconciled surfaces include:

```text
validate_github_projection.py
validate_github_generation_history.py
begin_github_operation.py
github_projection_next.py
reconcile_github_projection.py
activate_github_generation.py
validate_projection_convergence.py
validate_issue_graph.py
validate_issue_projection_tree.py
validate_relay_conformance.py
```

Templates/schemas include `GITHUB_PROJECTION.yaml`, `GITHUB_OBSERVATION.yaml`, GitHub projection/observation schemas, and the revised ISSUE_GRAPH / REPO_STATE contracts.

## Synthetic acceptance evidence

`tests/stress/test_github_projection_operations.py` proves repository-neutral operation behavior including:

- CREATE -> LINK -> PUBLISH_HANDOVER convergence;
- uncertain CREATE recovery before retry;
- dependency and marker enforcement;
- repository-authoritative SUPERSEDE / REVISE / UPDATE;
- terminal CLOSE and reactivated REOPEN rules;
- superseding an uncertain generation without fabricating a connector receipt.

Existing issue-tree, closure, supersession, projection-generation, parallel and takeover suites continue to run in the same dedicated stress surface.

During final closure review, a pre-existing issue-tree regression was found to assert an obsolete exact diagnostic phrase. The validator still rejected the illegal closed-parent/non-closed-child state. The regression was changed to assert the specific invariant semantics rather than exact prose.

## Validation

Pre-checkpoint exact implementation head:

```text
f63fbf8fbf71a3ad24ce0fd57e4e97a584d8c02b
workflow 35140358167 — PASS
```

The workflow passed:

```text
compile
root unit tests
111 repository-neutral synthetic stress tests
```

## Deliberately not done

WP-05 does not:

- make GitHub roadmap authority;
- infer successful native relationships from body links;
- write to downstream stress repositories;
- modify Engineering Relay V2;
- implement QRV quality procedures (WP-06);
- implement Owner communication (WP-07);
- implement Owner change intake (WP-08);
- claim the A -> B -> C recursive release proof (WP-09);
- mark PR #396 ready or merge it.

## Successor

After CP-R006 exact-head validation, the only material frontier is WP-06 — Quality Procedure Library + `QRV-*` evidence.
