# Engineering Relay V2.5 operator quick-start

## Goal

Recover and operate a V2.5 relay from repository state alone. Do not use prior chat as required execution context.

## 1. Discover the relay deterministically

Start from the repository root:

```text
AGENTS.md
  ↓
agents/relay/REPO_STATE.yaml
  ↓
referenced roadmap / progress / issue graph
  ↓
current serial EP or approved parallel plan
  ↓
referenced predecessor / continuity / certification evidence
```

Do not scan for the newest handover file, infer the active branch from issue comments, or guess the current EP.

## 2. Run repository-level admission

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/validate_relay_conformance.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/cold_start_check.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/zero_context_reconstruction.py <repo-root>
```

`validate_relay_conformance.py` proves the durable repository contract is coherent. `cold_start_check.py` is a recovery diagnostic. `zero_context_reconstruction.py` derives what a successor should be able to explain from repository state.

A green repository is not yet permission for an arbitrary incoming candidate to write.

## 3. Resolve the current route

For ACTIVE/SERIAL work, resolve the one current EP. For PARALLEL work, resolve the lane from the checked-out branch/worktree. For IDLE/TERMINAL there is no material route.

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/resolve_execution_route.py <repo-root>
```

If the route is ambiguous or the checkout does not belong to an approved lane, do not perform material writes.

## 4. Establish candidate admission

The baton can be `BATON_READY` before the execution candidate exists. A new successor or a continuing custodian must then produce current repository-grounded evidence:

```text
DSTEP-* contract
   ↓
DISC-* receipt
   ↓
QSET-* / QUAL-* when phase or material qualification boundary requires it
   ↓
TC-* Takeover Certification
```

Run:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/validate_baton_readiness.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/validate_discovery_receipt.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/validate_question_set.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/validate_qualification_receipt.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/validate_takeover_certification.py <repo-root>
```

Only run qualification validators when the route actually requires the corresponding objects.

The candidate may assemble its own DISC and TC files. That is evidence authorship, not certification authority. For a non-qualification route, a third agent is **not** required solely to author TC: use the deterministic TC validator. If fresh qualification is required, the candidate still may not author its own QSET or act as its own independent evaluator.

## 5. Gate every material write on live state

Immediately before material writes:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/inspect_git_context.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/material_write_ready.py <repo-root> --candidate-id <agent-instance-id>
```

`MATERIAL_WRITE_READY` is runtime-derived. A persisted `material_authority: WRITE` or ACTIVE lifecycle is not enough.

Keep the two authorization layers separate:

```text
route-level material_authority   → repository/route may write in principle
candidate admission              → this candidate has current DISC/QUAL/TC
MATERIAL_WRITE_READY             → both above + live Git/drift/stop checks
```

Do not set route-level `material_authority` to READ_ONLY merely because candidate admission is not yet complete.

If base state moved, follow the drift contract. `DISJOINT` may preserve writes; qualified-boundary movement needs required confirmation; `OVERLAPPING | UNKNOWN` withhold write authority until reconciliation.

## 6. Execute only the current slice

Follow the current EP exactly:

- use only current-slice ready inputs/oracles;
- stay inside `allowed_write` and protected/prohibited boundaries;
- execute ordered implementation steps;
- run only quality procedures routed as applicable;
- preserve exact acceptance/test/oracle evidence;
- stop on true hard-stop conditions rather than converting ordinary quality/evidence gaps into blockers.

Defined future work is not executable work.

## 7. Checkpoint reality and hand over

Before custody transfer:

```text
implementation result
  ↓
applicable tests/oracles
  ↓
QRV-* quality review
  ↓
CP-* checkpoint
  ↓
roadmap/progress/issue reconciliation
  ↓
frontier recomputation
  ↓
successor EP / approved parallel route / join / replan / terminal disposition
  ↓
QSET-* if fresh qualification is required
  ↓
BATON_READY
  ↓
required external projection convergence
```

Render the disposable human views only after source objects are reconciled:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/render_status.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/render_handover.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/render_owner_status.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/render_technical_status.py <repo-root>
```

## 8. What the successor must be able to answer without chat

The repository must provide enough information to answer, materially and specifically:

- Why does this task exist and where is it in the roadmap?
- Which Owner decisions govern it?
- What did predecessors establish, and what remains uncertain?
- Which inputs are editable versus authoritative?
- Which benchmark/oracle proves the result?
- What may change, what is protected, and what is prohibited?
- What evidence exists or is missing?
- Which tests/quality procedures are required?
- What is the first exact implementation action?
- What makes the current EP stale or removes write authority?
- What must happen next after this slice?

If any material answer requires prior conversation, the baton is incomplete.

## 9. Maintenance / release checks for Common

Within the Common repository itself:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/self_consistency_audit.py .
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests -p 'test*.py' -v
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests/stress -p 'test*.py' -v
```

The scoped GitHub workflow runs the same audit and test surfaces.

## 8. Explicit Owner command: Plan for Handover

When the Owner explicitly says `Plan for Handover`, first render/publish the normal Owner status from current repository truth. Then derive the handover transaction:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/plan_handover.py <repo-root> \
  --command "Plan for Handover" \
  --owner-requirement "<relevant user-authored requirement>"
```

For the explicit complex variant:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/plan_handover.py <repo-root> \
  --command "Plan for Handover, complex project" \
  --owner-requirement "<relevant user-authored requirement>"
```

The first planner output intentionally stops before three-pass generation until the handover issue has been created/updated through GHGEN/GHOP and its external identity/linkage read back.

Prepare the handover GitHub generation without bypassing the existing crash-safe projection transaction:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/prepare_handover_projection.py <repo-root> --apply
python <common>/skills/engineering-pr-delivery-v2.5/scripts/github_projection_next.py <repo-root>
python <common>/skills/engineering-pr-delivery-v2.5/scripts/begin_github_operation.py <repo-root> \
  --basis "<durable pre-write basis>" --apply
```

Perform only the provider action returned by `begin_github_operation.py`, then read it back, create a `GITHUB_OBSERVATION`, and reconcile it through `reconcile_github_projection.py --apply`.

If another GitHub generation is still unreconciled, the handover preparer returns `PROJECTION_BUSY` or `RECONCILE_REQUIRED`; do not supersede or retry blindly.

After verified issue readback:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/plan_handover.py <repo-root> \
  --command "Plan for Handover" \
  --handover-issue-url "<verified handover issue URL>" \
  --owner-requirement "<relevant user-authored requirement>"
```

Use the emitted generator request as input to the **freshly fetched live** standalone three-pass generator. Do not generate against a guessed or attempted issue URL.

The stable handover key is the duplicate-prevention basis. For the same active ownership boundary, search/read back for the matching open handover issue and update it. Create a new issue only when no valid match exists or the ownership boundary materially changed.



## 9. Publish Owner progress

Before returning control after a meaningful work unit:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/publish_owner_progress.py \
  <repo-root> --apply
```

This renders the source-derived Owner status and records the exact normalized baseline under `agents/relay/publication/OWNER_PUBLICATION.yaml`.

If current truth has not changed since the previous publication, the output says `NO_MATERIAL_PROGRESS` and the cursor is not rewritten. Use `--force-record` only for an explicit heartbeat that should be retained as a publication receipt.

Focused integrity check:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/validate_owner_publication.py <repo-root>
```

For `Plan for Handover`, use the same transaction through:

```bash
python <common>/skills/engineering-pr-delivery-v2.5/scripts/plan_handover.py <repo-root> \
  --command "Plan for Handover" \
  --apply-publication \
  --owner-requirement "<relevant user-authored requirement>"
```

The handover planner derives INTENT after this Owner publication is recorded.
