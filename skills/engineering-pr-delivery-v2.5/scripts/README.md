# V2.5 validator and lifecycle commands

From the downstream repository root run the validators from this directory. Primary entrypoints:

```bash
python validate_relay_conformance.py <repo-root>
python cold_start_check.py <repo-root>
python stress_test_relay.py <repo-root> [<repo-root> ...]
python render_status.py <repo-root>
python render_handover.py <repo-root>
```

## Semantic baton, takeover and qualification

```bash
python validate_repo_profile.py <repo-root>
python validate_ep_semantics.py <repo-root>
python validate_baton_readiness.py <repo-root>
python validate_discovery_receipt.py <repo-root>
python validate_question_set.py <repo-root>
python validate_qualification_receipt.py <repo-root>
python validate_takeover_certification.py <repo-root>
python material_write_ready.py <repo-root> --candidate-id <agent-instance-id>
```

`validate_ep_semantics.py` rejects hollow forward contracts. It validates `DSTEP-*` discovery instructions, typed current-slice inputs, benchmarks/oracles, semantic write/read/protected/prohibited/Owner-reserved scope, structured anti-drift, implementation-step mappings, source-bound report payloads and durable successor outputs. `validate_repo_profile.py` and the pinned relay-protocol basis are also part of aggregate admission.

`validate_baton_readiness.py` proves candidate-independent `BATON_READY`. If an EP requires fresh qualification, its referenced `QSET-*` must already exist and pass strong question validation before the outgoing baton can be ready.

`validate_discovery_receipt.py` validates route/candidate `DISC-*` evidence for the EP's required `DSTEP-*` instructions.

`validate_question_set.py` enforces the durable Q1-Q5 engineering contract for `PHASE_CHANGED` or `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED`: actual production trace, engineering reconstruction, mutation/invariant/falsifier, independent oracle and exact first safe slice. Quantitative Q2 requires concrete payload values.

`validate_qualification_receipt.py` validates candidate answers, required structured outputs/evidence, evaluator independence and per-question PASS/FAIL. Candidate-authored question sets and candidate-as-independent-evaluator are invalid. Deterministic evaluation requires an exact answer key in the QSET.

`validate_takeover_certification.py` requires current DISC evidence and, when the EP requires qualification, a current PASS `QUAL-*` receipt plus its exact digest. Editing QUAL evidence after TC issuance invalidates takeover.

`material_write_ready.py` derives live `MATERIAL_WRITE_READY` for one candidate/route. It combines current takeover certification with live route/Git inspection, current drift qualification, `material_authority: WRITE`, `can_continue: true` and no hard stop. It is deliberately not a persisted readiness boolean.

Before material writes, route and Git observation are independently available through:

```bash
python resolve_execution_route.py <repo-root>
python inspect_git_context.py <repo-root>
```

`resolve_execution_route.py` selects the serial EP or exactly one approved parallel lane from the checked-out branch/worktree. `inspect_git_context.py` verifies expected branch/material ancestry and compares the current base branch with the EP's observed base. If the base moved it returns `NEEDS_DRIFT_RECEIPT`; it never auto-classifies drift safe.

## Other focused diagnostics

```bash
python validate_projection_convergence.py <repo-root>
python validate_drift_receipt.py <repo-root>
python validate_issue_graph.py <repo-root>
python validate_issue_projection_tree.py <repo-root>
python validate_issue_closure.py <repo-root>
python validate_supersession.py <repo-root>
python validate_parallel_plan.py <repo-root>
python validate_parallel_join.py <repo-root>
python validate_parallel_replan.py <repo-root>
python validate_roadmap_continuity.py <repo-root>
```

Projection convergence distinguishes newest desired projection state from the older generation actually observed externally. Superseded publication operations have no retry authority.

Issue projection treats `PARENT_OF` as a coordination tree, supports evidence-preserving multi-generation supersession, and refuses closure that hides unresolved work/evidence.

Parallel lane checkpoints converge through JOIN; partial invalidation freezes the old topology and uses a durable replan transaction. Route resolution reads only the current approved plan.

Roadmap continuity handles long-lived serial EPs across revisions: `CONTINUE_UNCHANGED`, `RECONCILE_REQUIRED` (READ_ONLY), or `INVALIDATED`.

## Safe initialization and migration

```bash
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root>
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root> --apply
python inventory_v2_relay.py <repo-root> --output <inventory.yaml>
python prepare_v2_migration.py <inventory.yaml> --output <reconciliation.yaml>
```

Aggregate relay conformance verifies repository/profile/protocol admission, lifecycle/routing, roadmap topology/frontier, semantic serial EPs or every approved parallel lane EP, QSET/QUAL/TC admission, acceptance/staleness/continuity, calculated progress, execution/material authority, projection generation/readiness, drift, serial/fork/join/replan custody, Owner decisions, issue lifecycle and roadmap transactions.

Checkpoint evidence is bound to exact `execution_basis.material_ref`. Generated Markdown and GitHub Issues remain projections, not authority.

The scoped CI must explicitly execute both root unit discovery and the dedicated `tests/stress/` discovery; compiling stress modules is not execution evidence. See `../operating-model/ci-evidence-correction.md`.

PyYAML is required. Procedural semantic/cross-object validators are the enforcement layer today; declarative schemas/templates are contract aids.
