# Relay certification matrix

## Purpose

This matrix is the release proof for Engineering Relay V2.5. It proves that repository state, not conversation history, is sufficient to recover the current engineering situation and that lifecycle-specific authority is reconstructed without inventing write permission.

The matrix is repository-neutral. Real downstream repositories remain read-only stress sources unless separately authorized.

## Defining zero-chat proof

The release proof is:

```text
Agent A has conversation context
  -> completes its bounded work
  -> writes checkpoint / successor EP / QSET / repository state
  -> conversation deleted

Agent B receives repository only
  -> cold-starts from REPO_STATE
  -> reconstructs Owner intent, roadmap position and predecessor evidence
  -> resolves current inputs / oracle / scope / tests / acceptance / next work
  -> answers fresh Q1-Q5 from repository evidence
  -> receives independent QUAL and TC PASS
  -> completes its work
  -> writes checkpoint / successor EP / QSET
  -> conversation deleted

Agent C receives repository only
  -> repeats repository-only reconstruction
  -> independently qualifies and obtains current TC PASS
```

The strict synthetic release proof crosses three dependency-ordered work packages rather than handing the same work package between agents. `test_zero_chat_repository_only_boundary.py` deliberately ignores all handoff-helper return values after A and B publish their batons. B and C reconstruct EP identifiers, qualification payload, oracle references and certification inputs by reopening repository files only.

Any material answer that requires prior chat fails V2.5.

## Agent C reconstruction contract

For every active execution route Agent C must be able to answer from repository state alone:

1. Why does this task exist?
2. What Owner decisions govern it?
3. What did predecessors establish?
4. What remains uncertain or incomplete?
5. Which inputs are editable versus authoritative/immutable?
6. What benchmark or independent oracle proves the result?
7. What may change and what is protected/prohibited?
8. What quality obligations and prior findings exist?
9. What evidence exists and what evidence is missing?
10. What tests and acceptance criteria are required?
11. What is the exact first implementation action and what makes the EP stale?
12. What happens next after the current slice?
13. Which OPEN deferred validations, known issues and delegated checks survive from prior agents, what may continue before they resolve, and which boundaries still block?
14. Who owns current material execution custody, if custody enforcement is enabled?

`zero_context_reconstruction.py` derives this reconstruction from authority objects and current route state. `validate_zero_context_reconstruction.py` rejects a repository that cannot answer the required material questions or still requires conversation context.

A fresh observer/status/timer process does not become a material-execution candidate merely because it is new. It first reconstructs OPEN control obligations and execution custody. Re-observing a recorded PEND/DLG item does not justify creating another certification or delegation transaction.

## Lifecycle certification matrix

| Scenario | Required zero-context result | Material-authority expectation | Synthetic proof |
| --- | --- | --- | --- |
| ACTIVE | At least one reconstructable serial route with full context/input/oracle/scope/quality/evidence/test/acceptance/next-work contract | Candidate writes require current DISC/QUAL/TC plus live write gate | `test_end_to_end_relay_certification.py::test_lifecycle_cold_start_certification_matrix`; A→B→C release tests |
| ACTIVE + RECONCILING | Route remains reconstructable and explains current work | `READ_ONLY`; reconciliation may continue but material engineering writes are unavailable | lifecycle matrix + roadmap continuity stress tests |
| PARALLEL | Every approved lane is separately reconstructable with route/lane identity | Certification and write authority remain lane/candidate scoped | lifecycle matrix + `test_parallel_certification_is_route_scoped` |
| ACTIVE + stale required projection | Engineering repository state remains recoverable; stale external generation is visible | Projection lag does not rewrite engineering truth, but `projection_ready=false` and `handover_ready=false` | lifecycle matrix + projection-generation recovery tests |
| IDLE | No material execution route; repository explains why no executable frontier exists | `NONE` | lifecycle matrix |
| TERMINAL | No successor route; completed roadmap/evidence remains reconstructable | `NONE` | lifecycle matrix |
| INITIALIZING (supplemental) | No fabricated EP or material route; initialization reason remains recoverable | `NONE` | bootstrap/core stress tests |

The lifecycle matrix tests recovery semantics. It does not weaken the existing validators for serial execution, parallel routing, continuity, projection convergence, state planes, takeover certification, or material write readiness.

## Release evidence

The WP-09 implementation candidate at `0be78ca507b4eea99327713d63da3528c5df056d` passed workflow `35191523488`: compile PASS, 7 root units PASS, 134 synthetic stress tests PASS.

The stricter repository-only candidate boundary at `12440cf190fd20a2b81e265ff5d97bb6dc904ed1` passed workflow `35191938748`: compile PASS, 7 root units PASS, 135 synthetic stress tests PASS.

The final WP-09 checkpoint must still pass the same two test surfaces on the exact head containing the checkpoint and program-state reconciliation before WP-09 is considered complete.
