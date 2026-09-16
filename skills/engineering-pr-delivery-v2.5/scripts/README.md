# V2.5 validator and lifecycle commands

From the downstream repository root run the validators from this directory. Primary entrypoints:

```bash
python validate_relay_conformance.py <repo-root>
python cold_start_check.py <repo-root>
python stress_test_relay.py <repo-root> [<repo-root> ...]
python render_status.py <repo-root>
python render_handover.py <repo-root>
python render_report_projection.py <repo-root> [--output <projection.yaml>]
```

## Progress / report projection

```bash
python validate_progress.py <repo-root>
python validate_report_projection.py <repo-root>
python render_report_projection.py <repo-root>
```

`PROGRESS.yaml` is authoritative for calculated progress through Objective -> Phase -> Work Package -> EP -> implementation step -> acceptance criterion. `REPO_STATE` percentages are checked mirrors only; status/handover rendering uses `progress_projection.py` rather than trusting those mirrors.

`report_projection.py` derives one structured report from roadmap, progress, current EP/plan, checkpoint, issue graph and repository state. It records source digests and never becomes a competing authority. `validate_report_projection.py` is part of aggregate conformance and requires complete active acceptance and structured next-work coverage. `render_report_projection.py` emits that derived object as YAML.

Every executable EP has `next_work.steps[]`: ordered action, concrete targets, inputs, tests/oracles, acceptance IDs, expected result and stop/reconciliation conditions. The one-line execution `next_action` remains a machine hint only.

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

`validate_ep_semantics.py` rejects hollow forward contracts, including vague or invalid structured next work. `validate_baton_readiness.py` proves candidate-independent `BATON_READY`. `validate_discovery_receipt.py` validates route/candidate `DISC-*` evidence. `validate_question_set.py` and `validate_qualification_receipt.py` enforce strong Q1-Q5 engineering qualification. `validate_takeover_certification.py` consumes current DISC/QUAL evidence. `material_write_ready.py` derives live candidate/route write permission.

Before material writes:

```bash
python resolve_execution_route.py <repo-root>
python inspect_git_context.py <repo-root>
```

## GitHub program projection

```bash
python validate_github_projection.py <repo-root>
python validate_github_generation_history.py <repo-root>
python github_projection_next.py <repo-root>
python begin_github_operation.py <repo-root> [--apply]
python reconcile_github_projection.py <observation.yaml> <repo-root> [--apply]
python activate_github_generation.py <generation.yaml> <repo-root> [--apply]
```

GitHub is an external coordination projection, never roadmap authority. `GHGEN-*` files are immutable desired generations containing stable `GHOP-*` operations. Before an external write, `begin_github_operation.py --apply` persists `ATTEMPTED_UNCONFIRMED`; then perform the provider call; then produce/read back a `GITHUB_OBSERVATION`; finally reconcile it. A timeout or missing connector response therefore cannot justify blind retry. `ISSUE_GRAPH.github_state` is last verified external reality (`ABSENT | OPEN | CLOSED | UNKNOWN`). Native parent/sub-issue success may be claimed only when the integration can create and read back that native relationship; a body link is not equivalent.

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

## Safe initialization and migration

```bash
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root>
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root> --apply
python inventory_v2_relay.py <repo-root> --output <inventory.yaml>
python prepare_v2_migration.py <inventory.yaml> --output <reconciliation.yaml>
```

Bootstrap creates complete zero-weight roadmap progress rows without fabricating an EP or acceptance evidence.

Aggregate relay conformance verifies repository/profile/protocol admission, lifecycle/routing, roadmap topology/frontier, semantic serial EPs or every approved parallel lane EP, structured next work, QSET/QUAL/TC admission, acceptance/staleness/continuity, full calculated progress hierarchy, derived report projection, execution/material authority, projection generation/readiness, GitHub generation/operation reconciliation when enabled, drift, serial/fork/join/replan custody, Owner decisions, issue lifecycle and roadmap transactions.

Checkpoint evidence is bound to exact `execution_basis.material_ref`. Generated Markdown, generated report projections and GitHub Issues remain projections, not authority.

The scoped CI must explicitly execute both root unit discovery and the dedicated `tests/stress/` discovery; compiling stress modules is not execution evidence. See `../operating-model/ci-evidence-correction.md`.

PyYAML is required. Procedural semantic/cross-object validators are the enforcement layer today; declarative schemas/templates are contract aids.
