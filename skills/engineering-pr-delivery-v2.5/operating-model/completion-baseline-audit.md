# V2.5 completion baseline audit — WP-00

## Audit identity

```text
work_package: WP-00 Kernel baseline / object matrix
audit_mode: repository-resident architecture audit
starting_head: 744bd8336b183af16f285acdd5eabbd6f29d7c36
pr: reallaksh19/Common#396
base: fed57820909f4984a97d67437340df952b73a5ab
scope: skills/engineering-pr-delivery-v2.5/** plus its scoped CI workflow
material_policy: architecture/baseline only; no WP-01 Semantic EP implementation
```

The audit reconciles the completion architecture against the actual V2.5 branch rather than assuming filenames, schemas, templates, and validators agree.

## Inventory observed at WP-00 start

PR #396 contained 119 changed files. The V2.5 tree included, among other artifacts:

- 10 quality blueprints;
- 17 declarative schemas;
- 37 scripts/validators/renderers;
- 18 templates;
- operating-model specifications;
- unit and synthetic stress tests;
- the scoped `.github/workflows/engineering-pr-delivery-v2.5.yml` workflow.

The audit reviewed the authority relationships between the major objects rather than treating file count as coverage.

## Findings

### BA-001 — relay protocol pin is produced but not enforced

**Severity:** architecture integrity

`REPO_STATE.yaml` and bootstrap output contain:

```text
relay_protocol.version
relay_protocol.basis_ref
```

but current `validate_repo_state.py` does not require or validate `relay_protocol`, and `repo-state.schema.yaml` does not define the binding. A repository can therefore carry an unverified/missing Common protocol basis while current aggregate conformance still succeeds.

**Disposition:** STRENGTHEN. Preserve the protocol pin and make it an enforced cross-object invariant during the semantic/readiness work, with final schema-conformance coverage in WP-10.

### BA-002 — REPO_PROFILE is produced but not admitted into conformance

**Severity:** baton/discovery completeness

Bootstrap creates `REPO_PROFILE.yaml`, and a schema/template exist, but there is no dedicated `validate_repo_profile.py` and aggregate conformance does not establish that the profile is complete/current.

**Disposition:** STRENGTHEN in WP-01 because semantic discovery depends on a trustworthy repository profile.

### BA-003 — declarative schemas are advisory today

**Severity:** contract alignment

The branch carries 17 schemas, but CI installs PyYAML only and executes compileall + unittest. Aggregate conformance is procedural; there is no JSON-Schema validation stage or common schema runner.

This means schema/template drift may be invisible if procedural validators do not cover the same field.

**Disposition:** KEEP the schemas, STRENGTHEN their executable role. Object-specific schemas evolve with their owning WP; comprehensive schema/template/validator convergence belongs to WP-10.

### BA-004 — EP structure is stronger than EP semantics

**Severity:** primary relay gap

`execution-package.schema.yaml`, `validate_ep_self_contained.py`, and `cold_start_check.py` prove section presence, context, basic discovery presence, scope presence, implementation-plan presence, report headings, and routing/baton identity. They do not yet prove rich input/benchmark semantics, structured staleness, executable discovery outputs, detailed implementation-step contracts, quality applicability, or source-reconciled report payloads.

**Disposition:** STRENGTHEN in WP-01. This is the principal successor of WP-00.

### BA-005 — discovery step / receipt namespace collision

**Severity:** object identity

Current EP examples use discovery step IDs such as `DISC-01`. The completion architecture also reserved `DISC-*` for the future Discovery Receipt.

**Disposition:** reserve:

```text
DSTEP-*  EP discovery instruction/step
DISC-*   candidate Discovery Receipt
```

Migration of the EP template/schema/validators belongs to WP-01; the receipt itself belongs to WP-02.

### BA-006 — cold start is not candidate certification

**Severity:** readiness integrity

`cold_start_check.py` runs aggregate conformance and extra content-presence checks, but it is not part of `validate_relay_conformance.py` and does not create candidate-specific evidence. It cannot prove independent takeover qualification.

**Disposition:** STRENGTHEN as a semantic check in WP-01, then subordinate/deprecate it as the final admission authority once WP-02 Takeover Certification exists.

### BA-007 — repository readiness is lifecycle-derived

**Severity:** critical handover semantics

Current projection validation derives repository recovery readiness essentially from:

```text
relay_state != INITIALIZING
```

rather than from semantic baton proof. This is exactly the architecture flaw identified in the completion review.

**Disposition:** REPLACE semantics in WP-02 with separate `BATON_READY`, `TAKEOVER_CERTIFIED`, `PROJECTION_READY`, `HANDOVER_READY`, and `MATERIAL_WRITE_READY` predicates. Do not conflate outgoing baton completeness with candidate certification.

### BA-008 — phase and EP progress mirrors can diverge from authority

**Severity:** Owner-report fidelity

`validate_progress.py` validates the calculated contents of `PROGRESS.yaml` and cross-checks `REPO_STATE.progress.overall_percent`. It does not cross-check `phase_percent` or `ep_percent`. `render_handover.py` renders those mirrored fields directly.

**Disposition:** REPLACE those mirrored human-report values with source-derived/reconciled progress projections in WP-04.

### BA-009 — report validation proves headings rather than report truth

**Severity:** handover completeness

`REPORT.md` is a Markdown section template. `validate_report_contract.py` verifies the required section names but not the payload each section must reconcile to EP/CP/progress/issue/quality/certification source objects.

**Disposition:** REPLACE in WP-04/WP-07 with a structured, source-derived report projection. Reports must never become an independent writable authority.

### BA-010 — phase qualification is question metadata only

**Severity:** candidate admission

`validate_phase_transition_questions.py` correctly grounds Q1–Q5 in the incoming EP and rejects stale anchors, but it does not evaluate candidate answers, concrete reconstruction, falsifiers, independent verification, or evaluator independence.

**Disposition:** STRENGTHEN in WP-03 with Question Set → candidate answers → independent evaluation → `QUAL-*` receipt.

### BA-011 — handover projection is coupled to machine vocabulary

**Severity:** Owner usability

Current handover rendering includes relay lifecycle, material authority, projection state, hard-stop state, join/replan vocabulary, and readiness booleans. These are valuable technical facts but there is no separate plain-language Owner representation. Acceptance rendering is also not yet a complete evidence-aware Objective→Phase→WP→Task→AC checklist.

**Disposition:** WP-04 owns complete checklist/next-work projection; WP-07 owns Owner versus technical communication separation.

### BA-012 — quality blueprints are useful principles, not full procedures

**Severity:** quality-system maturity

The blueprint set covers the right disciplines, but current files are primarily principles/checklists and do not uniformly define applicability, procedure, artifacts, verification, quality classification, actual stop conditions, Owner report, and successor duties.

**Disposition:** STRENGTHEN in WP-06 with applicability routing and `QRV-*` Quality Review evidence.

### BA-013 — procedural validation is the actual enforcement layer

**Severity:** architecture documentation

The real kernel is enforced primarily by procedural Python validators and their cross-object composition. Schemas and templates are support contracts; generated Markdown is projection. This authority distinction must remain explicit during the revamp.

**Disposition:** KEEP procedural semantic/cross-object validation as a first-class layer; add schema validation rather than substituting schema validation for semantic validation.

## Strong kernel components retained

WP-00 did not find a reason to redesign these foundations:

- Owner Decision Records and roadmap intent mutation rules;
- Overall Roadmap and deterministic executable frontier;
- serial-by-default execution;
- Owner-approved parallel plan, join, and replan custody;
- checkpoint versus EP separation;
- exact-head validation evidence;
- live branch/worktree/Git-basis observation separation;
- drift and long-lived roadmap continuity receipts;
- independent execution/quality/evidence/stop planes;
- calculated Progress Basis philosophy;
- deep issue parent/child projection and evidence-preserving supersession;
- crash-safe projection generations;
- safe bootstrap and evidence-first V2 migration.

These are `KEEP` foundations. Later work may integrate them with new readiness/certification objects, but should not rewrite them without a newly demonstrated defect.

## WP ownership map

| Finding | Owning WP |
| --- | --- |
| BA-001 protocol pin enforcement | WP-01 / final WP-10 audit |
| BA-002 REPO_PROFILE validation | WP-01 |
| BA-003 executable schema conformance | object WPs + WP-10 |
| BA-004 semantic EP | WP-01 |
| BA-005 discovery namespaces | WP-01 / WP-02 |
| BA-006 cold start vs certification | WP-01 / WP-02 |
| BA-007 readiness predicates | WP-02 |
| BA-008 progress mirrors | WP-04 |
| BA-009 structured report | WP-04 / WP-07 |
| BA-010 qualification receipt | WP-03 |
| BA-011 human handover | WP-04 / WP-07 |
| BA-012 quality procedures | WP-06 |
| BA-013 procedural + schema validation layers | WP-10 |

## WP-00 acceptance assessment

```text
AC-00-01 actual branch inventory captured                         PASS
AC-00-02 authority role assigned to existing control objects      PASS
AC-00-03 KEEP/STRENGTHEN/REPLACE/ADD disposition recorded         PASS
AC-00-04 authority/projection leaks identified                    PASS
AC-00-05 target namespace collision resolved architecturally       PASS
AC-00-06 successor WP ownership assigned                          PASS
AC-00-07 no WP-01 semantic implementation performed               PASS
```

WP-00 is complete when the accompanying completion checkpoint is present and the scoped V2.5 CI passes on the exact checkpoint head.
