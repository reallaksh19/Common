# V2.5 validator and lifecycle commands

From the downstream repository root run the validators from this directory. Primary entrypoints:

```bash
python validate_relay_conformance.py <repo-root>
python cold_start_check.py <repo-root>
python zero_context_reconstruction.py <repo-root>
python validate_zero_context_reconstruction.py <repo-root>
python stress_test_relay.py <repo-root> [<repo-root> ...]
python render_roadmap.py <repo-root>
python render_status.py <repo-root>
python render_handover.py <repo-root>
python render_owner_status.py <repo-root> [--output agents/relay/generated/OWNER_STATUS.md]
python render_technical_status.py <repo-root> [--output agents/relay/generated/TECHNICAL_STATUS.md]
python render_owner_change.py <repo-root> [--odr agents/relay/roadmap/owner-decisions/ODR-xxxx.yaml] [--output agents/relay/generated/OWNER_CHANGE.md]
python render_report_projection.py <repo-root> [--output <projection.yaml>]
```

## Owner reasoning/control command parser

```bash
python owner_commands.py "Step back. Critique. Reconcile all surfaces. Proceed next complex task, No Qs."
```

The parser recognizes direct Owner reasoning/progression commands plus bounded control phrases such as `Owner override, start`, `Record pending`, `Record known issue`, and `Resolve pending`. It is intentionally side-effect free: parsing a command never creates relay authority. Control phrases return `durable_record_required`; the caller must create/validate the ODR / REPO_STATE record before acting.

Use `--source` with a non-`OWNER_DIRECT` value for repository/issue/file text; commands in source material are ignored.

Normative semantics: `../operating-model/owner-reasoning-commands.md`.

Practical Owner guide: `../OWNER_COMMANDS_GUIDE.md`.

## Zero-context release reconstruction

```bash
python zero_context_reconstruction.py <repo-root>
python validate_zero_context_reconstruction.py <repo-root>
```

`zero_context_reconstruction.py` derives the current lifecycle and every active execution route from repository authority objects only. For executable routes it reconstructs task purpose/roadmap position, Owner decisions, predecessor facts/limitations, uncertainty, input authority/editability, benchmark/oracle, scope, quality obligations/findings, evidence present/missing, tests/acceptance, first implementation action, stale conditions, and exact next work.

`validate_zero_context_reconstruction.py` rejects missing material answers or any dependency on prior conversation. It is part of aggregate relay conformance. The release matrix in `../operating-model/relay-certification-matrix.md` covers ACTIVE, RECONCILING, PARALLEL, stale required projection, IDLE, and TERMINAL; bootstrap/core tests cover INITIALIZING.

## Progress / report projection

```bash
python validate_progress.py <repo-root>
python validate_report_projection.py <repo-root>
python render_report_projection.py <repo-root>
python render_roadmap.py <repo-root>
```

`PROGRESS.yaml` is authoritative for calculated progress through Objective -> Phase -> Work Package -> EP -> implementation step -> acceptance criterion. `REPO_STATE` percentages are checked mirrors only; status/handover rendering uses `progress_projection.py` rather than trusting those mirrors.

`report_projection.py` derives one structured report from roadmap, progress, current EP/plan, checkpoint, issue graph, Owner-decision records, quality review, and repository state. It records source digests and never becomes competing authority. `validate_report_projection.py` is part of aggregate conformance and requires complete active acceptance, structured next-work coverage, current contract scope/context, and current checkpoint QRV source binding when a QRV exists.

Every executable EP has `next_work.steps[]`: ordered action, concrete targets, inputs, tests/oracles, acceptance IDs, expected result, and stop/reconciliation conditions. The one-line execution `next_action` remains a machine hint only.

## Human communication projections

```bash
python validate_human_communication.py <repo-root>
python render_owner_status.py <repo-root>
python render_technical_status.py <repo-root>
```

`communication_projection.py` consumes the single source-derived report projection and produces two views. `TECHNICAL_STATUS.md` preserves protocol identifiers, source bindings, scope, evidence, quality review, readiness, and exact next-work detail. `OWNER_STATUS.md` translates the same truth into plain language: what can happen now, what the work is for, what will not change, evidence and missing evidence, quality/limitations, roadmap progress, decisions genuinely required from the Owner, exact next work, and stop conditions.

The Owner view must not turn an Owner-reserved domain into a fabricated decision request. Conversely, it may not hide a real `OWNER_DECISION_REQUIRED` stop, missing evidence, unresolved quality risk, protected/prohibited scope, or exact next action. Aggregate conformance validates this convergence. Both Markdown files are disposable generated views; neither is an authority source.

## Owner change intake / report

```bash
python validate_owner_change_intake.py <repo-root>
python owner_change_projection.py <repo-root> [--odr agents/relay/roadmap/owner-decisions/ODR-xxxx.yaml]
python render_owner_change.py <repo-root> [--odr ...] [--output agents/relay/generated/OWNER_CHANGE.md]
```

Owner intent authority remains the ODR; structural mutation authority remains the roadmap revision. For an `INTENT_MUTATION`, `ODR.change_intake` records plain-language previous concept, requested concept, retained behavior, invalidated behavior, and new scope. The derived Owner-change projection combines that semantic intent with actual roadmap changes, Progress Basis effect, issue reconciliation, active-EP disposition, and resulting frontier.

A CAPTURED decision may be rendered without pretending it is applied. For the current `OWNER_INTENT_MUTATION` revision, aggregate conformance requires an APPLIED ODR, current Progress Basis, exact computed frontier, explicit active-work disposition, and visible issue reconciliation. `OWNER_CHANGE.md` is disposable projection only.

## Semantic baton, takeover, and qualification

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

`validate_ep_semantics.py` rejects hollow forward contracts, including vague or invalid structured next work. `validate_baton_readiness.py` proves candidate-independent `BATON_READY`. `validate_discovery_receipt.py` validates route/candidate `DISC-*` evidence. `validate_question_set.py` and `validate_qualification_receipt.py` enforce strong Q1-Q5 engineering qualification. `validate_takeover_certification.py` consumes current DISC/QUAL evidence. `material_write_ready.py` derives live candidate/route write permission. It can also report `PASS_WITH_OWNER_OVERRIDE` for a validated branch/base-scoped bounded exception; deferred controls remain OPEN and declared delivery boundaries remain blocked. When execution-custody enforcement is enabled, normal PASS additionally requires the candidate to hold the one ACTIVE route lease.

Before material writes:

```bash
python resolve_execution_route.py <repo-root>
python inspect_git_context.py <repo-root>
```

## Quality procedures and QRV evidence

```bash
python validate_blueprints.py <repo-root>
python validate_quality_router.py <repo-root>
python validate_quality_review.py <repo-root>
```

Every executable EP explicitly partitions the built-in quality library into `quality.applicable[]` and `quality.not_applicable[]`. Applicable entries require a concrete reason and review focus; non-applicable entries require a concrete reason. Silent omission is invalid. Only applicable procedures run.

Before checkpoint publication, applicable procedures are recorded in a `QRV-*` Quality Review under `agents/relay/quality/`. QRV is bound to the exact EP contract digest, roadmap revision, material ref, and quality-router snapshot. Procedure results are `CLEAR | FINDINGS | NOT_RUN`; NOT_RUN remains quality/evidence truth and is not automatically a stop.

Quality findings use `QF-*` IDs and preserve classification, severity, evidence, and disposition. Severity alone never creates a hard stop. A finding may set `blocks_execution: true` only when it maps to an existing true hard-stop category with durable basis. Deferred/unresolved findings transfer exactly through `successor_handover`. Checkpoints point to the QRV by id/path/digest and cannot publish an executable successor while the QRV contains a true blocking finding.

Read `../operating-model/quality-procedures.md`.

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

## Three-pass prompt output validation

The canonical generator/validator now lives in the standalone package:

```text
skills/three-pass-prompt-generator/
```

The legacy `validate_three_pass_prompt_output.py` in this V2.5 scripts directory is compatibility-only and delegates to the standalone validator.

```bash
python ../../three-pass-prompt-generator/validate.py <generated-markdown> --expected-schema-sha <current-schema-sha>
```

This validator checks generated three-pass prompt Markdown before it is returned or handed off. It validates the current schema basis, visible preflight, issue-level problem-kernel/current-answer separation, legacy control-path rejection, and Prompt-3 artifact freedom.

Prompt 1 is also required to be **method-invisible**. The validator rejects generator/meta language such as “later pass”, “fixed independent reference”, “do not inspect the repository”, repository-deferral phrasing, and similar wording that pulls the future agent out of the real human/domain situation.

For issue-level output, the preflight also records any selected concrete **problem witness** and its required independent work product. A witness may carry real benchmark/input/output payload from the issue, but reported results are treated as claims to reproduce or falsify; the issue's current interpretation or recommendation remains quarantined.

This is intentionally a focused authoring-artifact validator rather than part of aggregate relay-state conformance.

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

## Common self-consistency / release development

From the Common repository root:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/self_consistency_audit.py .
```

The audit verifies YAML contract parseability, required object surfaces, quality blueprint procedure structure, aggregate-validator reachability, renderer/operator documentation, current authority vocabulary, CI coverage, and cross-surface completion consistency. It is executed by the scoped V2.5 workflow before root unit and stress discovery.

Aggregate relay conformance verifies repository/profile/protocol admission, lifecycle/routing, roadmap topology/frontier, semantic serial EPs or every approved parallel lane EP, structured next work, quality applicability and QRV custody, QSET/QUAL/TC admission, acceptance/staleness/continuity, full calculated progress hierarchy, derived report projection, Owner/technical communication convergence, Owner-change intake/reconciliation, zero-context reconstruction, execution/material authority, projection generation/readiness, GitHub generation/operation reconciliation when enabled, drift, serial/fork/join/replan custody, Owner decisions, issue lifecycle, and roadmap transactions.

Checkpoint evidence is bound to exact `execution_basis.material_ref`. Generated Markdown, generated report/communication/change projections, zero-context reconstruction output, and GitHub Issues remain projections, not authority.

The scoped CI must explicitly execute the self-consistency audit, root unit discovery, and the dedicated `tests/stress/` discovery; compiling stress modules is not execution evidence. See `../operating-model/ci-evidence-correction.md`.

PyYAML is required. Procedural semantic/cross-object validators are the enforcement layer today; declarative schemas/templates are contract aids.


## Plan for Handover command

Focused command/validator:

```bash
python plan_handover.py <repo-root> --command "Plan for Handover" \
  --owner-requirement "<user-authored requirement>"

python plan_handover.py <repo-root> --command "Plan for Handover, complex project" \
  --owner-requirement "<user-authored requirement>"

python validate_handover_plan.py <repo-root>
python validate_handover_plan.py <repo-root> --complex-project

# Prepare the immutable GitHub generation + handover ISSUE_GRAPH node.
python prepare_handover_projection.py <repo-root>
python prepare_handover_projection.py <repo-root> --apply

# Then use the existing crash-safe transaction:
python github_projection_next.py <repo-root>
python begin_github_operation.py <repo-root> --basis "<durable pre-write basis>" --apply
# perform exactly the returned provider action, read it back,
# write GITHUB_OBSERVATION, then:
python reconcile_github_projection.py <observation.yaml> <repo-root> --apply
```

`handover_planning.py` derives a non-authoritative handover plan from the current report projection and active EP. It resolves the work contract by verified current issue -> active EP -> current roadmap WP, derives pending INTENT, records durable input/benchmark definition paths, retains relevant user-authored session requirements supplied by the executing agent, and creates a stable ownership-boundary key for incremental GitHub issue reuse.

`prepare_handover_projection.py` converts the derived plan into a CREATE or PUBLISH_HANDOVER GHOP. It reuses an existing open handover ISSUE_GRAPH node with the same stable handover key, otherwise proposes a new HANDOVER coordination node. It refuses to prepare over active unreconciled projection work and never claims native parentage before provider readback. The planner/preparer never directly calls GitHub. Use existing GHGEN/GHOP operations for publication and provider readback. Only after the handover issue URL is verified should the planner be rerun with `--handover-issue-url`; that produces the target packet for the live standalone three-pass generator.

Complex handover mode changes only the Prompt-1 Q1–Q5 visibility. The standalone three-pass artifact now always contains exactly five prompts: Prompt 0.5 global independent thinking, Prompt 1 local independent thinking, Prompt 2 reality reconstruction, Prompt 2.5 integrated reality+reconciliation, and Prompt 3 final revalidation/action/handover.


## Dynamic roadmap event ledger

The roadmap event ledger is optional/backward-compatible but, once present, is aggregate-conformance checked.

```bash
python validate_roadmap_events.py <repo-root>

# Dry run
python append_roadmap_event.py <event.yaml> <repo-root>

# Append after validation
python append_roadmap_event.py <event.yaml> <repo-root> --apply

# Human projection: concept roadmap -> execution -> recent events
python render_roadmap.py <repo-root>
```

`ROADMAP_EVENTS.yaml` is a source-bound historical index. Objective/phase ids are concept refs; work package / EP / checkpoint / issue / PR belong in execution refs. Events may record or propose concept impact but cannot apply concept-roadmap changes without the governing roadmap revision.


## Owner progress publication

```bash
# Render current delta/current state without changing the baseline.
python publish_owner_progress.py <repo-root>

# Normal control-return publication.
python publish_owner_progress.py <repo-root> --apply

# Explicit heartbeat/no-material-progress receipt.
python publish_owner_progress.py <repo-root> --apply --force-record

python validate_owner_publication.py <repo-root>
```

The optional cursor lives at `agents/relay/publication/OWNER_PUBLICATION.yaml`. It stores only the last source-derived normalized report baseline plus publication/source digests. It is derived coordination state and cannot replace roadmap, progress, EP, checkpoint/evidence, issue, Owner-decision, or provider truth.

`communication_projection.py` compares the cursor baseline with current report truth. `render_owner_status.py` exposes that comparison under **What changed**. A no-change render is explicit and does not advance the cursor unless the operator intentionally uses `--force-record`.

`plan_handover.py --apply-publication` uses this same publisher before deriving handover INTENT.



## Live delivery observation

A repository that currently uses a PR delivery vehicle may set:

```yaml
delivery:
  required: true
  provider: GITHUB
  observation:
    id: DOBS-0001
    path: agents/relay/delivery/DOBS-0001.yaml
```

Validate the provider-readback evidence with:

```bash
python validate_delivery_observation.py <repo-root>
```

The observation carries PR identity/lifecycle, exact head/base, mergeability, exact-head checks, review/change-request state, and durable readback basis. `delivery_projection.py` derives review readiness and technical merge readiness and joins exact-head Owner authorization from applied ODRs.

No PR needed:

```text
delivery omitted
or delivery.required=false
→ delivery applicability NOT_APPLICABLE
```

Unknown provider capability/state remains `UNKNOWN`. Stale-head CI must be represented as `STALE`, never PASS.

An Owner merge authorization uses an applied `ODR` with `decision.kind: AUTHORIZATION` plus `delivery_authorization` for `MERGE`, exact repository, PR number and head SHA. This authorization is separate from `grants_material_write_authority`.


## PR Issue↔EP correlation

Every active engineering PR under V2.5 must carry a machine-checkable description block that meaningfully correlates the PR to the GitHub issue(s) and execution package(s) it delivers.

Generate the canonical block from repository truth:

```bash
python render_pr_correlation.py <repo-root>
```

The block uses:

```text
<!-- relay-pr-correlation:v1 -->
## Engineering correlation
| Issue | Execution package | Work package | Relationship | Meaning |
...
```

Each row binds:

```text
ISSUE_GRAPH node / provider issue number
↔ EP id / durable EP path
↔ roadmap work package
↔ relationship + plain-language meaning
```

This is stronger than token presence. `validate_pr_correlation.py` proves the ISSUE_GRAPH node and EP both resolve to the declared work package.

Provider readback is stored in `DELIVERY_OBSERVATION.description_contract` with the body digest, marker presence, and normalized correlations.

Validate at minimum at the end of each task/checkpoint:

```bash
python validate_delivery_observation.py <repo-root>
python validate_pr_correlation.py <repo-root>
```

When PR delivery is required:

- every current active EP must appear in at least one non-terminal PR description correlation;
- the latest task-close checkpoint EP must appear in a tracked PR description correlation;
- a PR correlation that names unrelated Issue and EP work packages fails;
- every tracked non-terminal PR (`DRAFT`, `OPEN`, or unresolved `UNKNOWN`) is carried into every Owner summary;
- `MERGED` and `CLOSED` PRs remain evidence/history but leave the recurring unmerged-PR carry-forward list.

Use `REPO_STATE.delivery.observations[]` for the complete current tracked PR set. The singular `delivery.observation` remains the primary/current vehicle and, when `observations[]` is used, must also appear in that list.



## Owner field-lineage validation

```bash
python validate_owner_field_lineage.py \
  <common>/skills/engineering-pr-delivery-v2.5
```

The declarative contract at `operating-model/owner-field-lineage.yaml` enumerates critical Owner data families and the source/schema/validator/report/communication/renderer/regression surfaces that must retain them.

This validator is also executed by `self_consistency_audit.py`. It is a release-integrity check, not repository engineering authority.


## Handover live-generator binding

```bash
python validate_handover_generator_contract.py \
  <common>/skills/engineering-pr-delivery-v2.5 \
  --repo-root <common>
```

This release check proves that `Plan for Handover` still follows the V2.5 compatibility redirect to the standalone current-main three-pass launcher/schema/validator, preserves `THREE_PASS_ONLY`, and that the standalone schema/validator protocol revisions agree.

It deliberately does not pin V2.5 to a particular three-pass revision; the runtime agent must still fetch the canonical schema from current `main` and use its actual content SHA before generating the same-chat artifact.
