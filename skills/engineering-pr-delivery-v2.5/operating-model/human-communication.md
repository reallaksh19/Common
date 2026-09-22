# Human communication

V2.5 exposes two generated human views over one derived communication projection:

```text
repository authority objects
  -> report_projection.py
  -> communication_projection.py
      -> TECHNICAL_STATUS.md
      -> OWNER_STATUS.md
```

Neither generated view is authority. Both are disposable projections and must be regenerated from current repository truth.

## Technical status

`TECHNICAL_STATUS.md` preserves protocol precision for engineering operators. It includes lifecycle, roadmap position, calculated progress, execution/material authority, evidence state, quality/QRV state, active stop, protected/prohibited scope, Owner decisions, ordered next work, readiness, and source-basis identifiers needed for diagnosis.

## Owner status

`OWNER_STATUS.md` translates the same source projection into plain language. It must answer:

- what can happen now;
- what the current work is intended to achieve;
- what will not change without authority;
- what evidence exists and what evidence is missing;
- what material quality risks or limitations remain;
- what changed in roadmap/progress at the last checkpoint;
- whether an Owner decision is genuinely required now;
- what happens next;
- what currently stops progress, if anything;
- which deferred validations remain OPEN, what work is still allowed, and which delivery/checkpoint boundaries they block;
- which known issues are intentionally carried forward;
- which delegated checks remain OPEN and are read-only monitoring work.

The Owner view must not invent urgency. A choice reserved to the Owner is not the same as an Owner decision required now. `OWNER_DECISION_REQUIRED` is shown only when current repository truth actually requires an Owner decision to proceed.

## Truth-preservation rules

The Owner view must never hide or soften away:

- active hard stops;
- `NOT_RUN` or otherwise missing evidence;
- unresolved/deferred quality findings;
- protected, prohibited, and deliberate non-goal scope;
- known limitations/problems;
- roadmap/progress reconciliation;
- exact ordered next work;
- OPEN `PEND-*`, `KI-*`, and `DLG-*` control obligations;
- active bounded Owner execution overrides and their blocked boundaries;
- execution custody when enforcement is enabled.

Quality severity alone does not become a hard stop in communication. A non-blocking quality risk remains visible as a risk, while execution-stop language is reserved for the STOP plane / valid hard-stop mapping.

## Environment-blocked local-agent delegation

An external/local execution requirement is incomplete unless the Owner can immediately delegate it.

Every such delegation must be bound to one durable `DLG-*` control obligation. Repeated observation of the same unresolved external action must reuse/update that DLG rather than publish another logically identical handoff.

The Owner view must expose:

- the exact copy-pasteable local-agent prompt;
- whether it was published as a current-issue comment or sub-issue;
- that provider readback is required;
- where the local result must be posted;
- the 30- or 60-minute response-check timer and why that interval fits the task;
- what the agent will do when the timer fires;
- what happens if no response is present;
- the DLG id and current lifecycle state;
- that the timer callback is a **READ_ONLY monitor** and terminates when the DLG is no longer OPEN.

A local/browser/tool limitation is therefore not merely `NOT_RUN`; it becomes a bounded, observable delegation with a return path.

When the response timer fires, it must first read the DLG lifecycle. If the obligation is `SATISFIED | SUPERSEDED | CANCELLED | EXPIRED`, the timer terminates without restarting the engineering transaction. While OPEN, it may inspect evidence and publish waiting/status truth only. It must not create a candidate identity, DISC/QUAL/TC, execution custody, product writes, or another delegation.

This prevents timer callbacks from recursively becoming replacement engineers.

## Plain-language boundary

The Owner view should avoid relay-internal object jargon where ordinary language carries the same meaning. It may name stable identifiers when they materially help traceability, but it must not require the Owner to understand internal terms such as EP, QRV, GHOP, or QSET in order to know capability, risk, evidence, decisions, and next work.

The technical view is intentionally allowed to retain protocol terms and object identifiers.

## Validation

`validate_human_communication.py` checks projection convergence and verifies that the Owner view cannot omit current stop/evidence/quality/scope/decision/next-work truth. Aggregate relay conformance invokes it.

Repository-neutral stress tests cover shared-source derivation, hard-stop visibility, missing evidence, non-blocking quality risk, Owner-reserved versus Owner-required decisions, next-work mutation, and internal-jargon rejection in Owner-facing source text.


## Plan for Handover

`Plan for Handover` is a compound Owner command, not a substitute for normal Owner status.

Sequence:

```text
publish normal Owner status
→ resolve current owned work
→ derive pending INTENT
→ publish/update and verify handover issue
→ run the live standalone three-pass generator
→ return the copy-pasteable prompts
```

Owned-work selection is:

```text
verified current GitHub issue mapped to the work
→ otherwise active task / EP
→ otherwise current roadmap work package
```

This order chooses the **handover target contract**; it does not allow issue prose to override current roadmap/progress/evidence truth.

The derived handover plan is coordination state. It contains the still-pending acceptance, evidence, next-work, checkpoint-remaining-work and genuinely required Owner-decision obligations; active EP input and benchmark definition paths; expected outcomes; scope/boundaries; and user-authored core requirements explicitly supplied in the current session.

The planner assigns a stable handover key to the ownership boundary. Repeated commands for the same still-active work update the matching open handover issue rather than creating a duplicate. Pending INTENT is recomputed from current truth each time.

Issue publication uses the existing GHGEN/GHOP transaction. Prefer a provider-native child relation when a valid parent issue exists and the integration can create and read it back; otherwise use a verified reciprocal/reference link. A body hyperlink never proves native parentage.

Three-pass generation begins only after the handover issue URL has been verified by provider readback. Follow the live compatibility redirect to `skills/three-pass-prompt-generator/SKILL.md` and `schema.md`; V2.5 does not cache or reproduce that protocol.

`Plan for Handover, complex project` enables the standalone generator's complex mode. The artifact still contains exactly three prompts; Prompt 1 additionally exposes natural target-specific Q1–Q5. A later plain handover command returns to non-complex mode.

Repository scripts must not infer chat requirements. The executing agent passes relevant user-authored session requirements explicitly to `plan_handover.py --owner-requirement ...`. Credential/secret-like values must not be published to GitHub.


## Mandatory 25-minute task heartbeat

Every active task has a default Owner status heartbeat at **minute 25 from task start**.

At task start, the executing agent must create a one-time status timer for 25 minutes unless the Owner explicitly overrides the cadence.

The heartbeat timer is also a **read-only status monitor**, not an execution handoff. Bind it to the current task/work identity. When it wakes, first verify that the task is still active; if the task completed, was superseded, or was cancelled, terminate the timer. The heartbeat must never create a new candidate, takeover certification, execution custody, product write, or delegated subtask merely because a fresh process handled the callback.

If the task completes before minute 25, the normal completion/control-return publication satisfies the obligation and the pending heartbeat may be cancelled.

If the task is still active at minute 25, publish Owner status even when nothing materially changed:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/publish_owner_progress.py <repo-root> --apply --force-record
```

A no-change heartbeat is valid and must say `NO_MATERIAL_PROGRESS`; do not invent progress merely because the timer fired.

Owner override semantics:

```text
INTERVAL <N minutes>  → use the Owner-specified first-status interval
DISABLED              → no time-based heartbeat for that task
```

The override must be explicitly attributable to the Owner. Silence is not an override.

This time-based heartbeat is additional to event-driven publication. A material event should still be published promptly rather than waiting for minute 25.

If the execution environment cannot create a timer, state `STATUS_TIMER_UNAVAILABLE`, record the 25-minute due interval, and do not claim the timer exists.

## Canonical Owner Roadmap control return

The normal Owner-facing publication is a generated roadmap/status projection, not free-form agent prose.

Every control return begins with `# Owner Roadmap` and includes the programme-level view before low-level relay detail.

Required macro sections are:

```text
Executive state
Phase status
Concept roadmap
Active work
Completed work log
Newly discovered work
Blocked / waiting
Deferred validations / known issues / delegated checks
What changed
Roadmap and progress
Delivery
Blocked / external action state
Owner decisions
Recommended forward sequence
Roadmap revision history
```

The agent may append technical detail after that projection. It may not substitute a custom summary that omits calculated progress or roadmap/delivery context.

## Deterministic Owner publication cursor

Owner status is not merely a renderer. Control-return publication uses a durable, derived baseline:

```text
agents/relay/publication/OWNER_PUBLICATION.yaml
```

The cursor records the normalized source-derived state that the Owner was last shown, plus source/report/view digests. It is **coordination metadata**, not engineering authority.

Current truth remains in roadmap, PROGRESS, EP, checkpoint/evidence, ISSUE_GRAPH, ODR, REPO_STATE control obligations/execution custody, state planes, and verified external observations.

Every communication projection derives:

```text
previous published normalized baseline
vs
current report projection
        ↓
event class
changed dimensions
concise transitions
publication_due
```

Supported Owner publication classes include:

```text
INITIAL_SNAPSHOT
TASK_PROGRESS
TASK_REGRESSION
IMPLEMENTATION_CHANGE
EVIDENCE_PROGRESS
DELIVERY_OR_CUSTODY_PROGRESS
CONTROL_STATE_CHANGE
WAITING_OR_MONITORING
NO_MATERIAL_PROGRESS
```

The Owner view begins with **What changed** and must not force the Owner to infer a delta from current percentages.

Examples:

- evidence-only movement explicitly says acceptance/progress did not move;
- custody-only movement does not imply implementation;
- no material movement is stated directly;
- task regression is visible rather than hidden by aggregate percentages.

Use `publish_owner_progress.py --apply` before normal control return. The command renders from one communication projection and only then records exactly that projection's normalized baseline, avoiding a recompute-after-write race.

An unchanged repeat does not advance the cursor. `--force-record` is reserved for an intentional heartbeat publication.

Material publication cadence is triggered by a change to accepted progress, implementation result, evidence, blocker/quality/control state, current issue/delivery/custody, roadmap disposition, Owner-decision requirement, required external/local action, or exact next-work contract. Repeated unchanged polling/retries are suppressed while autonomous work continues.



## Live PR delivery/readiness

When the current slice has a pull-request delivery vehicle, Owner communication must project a **vector**, not a single "ready" label.

Provider external reality is recorded as evidence in a current `DELIVERY_OBSERVATION` referenced by optional `REPO_STATE.delivery`.

The Owner delivery section keeps these dimensions independent:

```text
PR identity / URL
lifecycle: DRAFT | OPEN | CLOSED | MERGED | UNKNOWN
head / base
exact-head checks
mergeability / conflict
review / change-request state
ready for review
technical ready to merge
merge authorization
```

Rules:

- mergeable does not mean ready for review;
- green checks on an older head do not count as current PASS;
- ready for review does not mean engineering acceptance is complete;
- technical readiness does not grant merge authority;
- merge authorization comes only from an applied Owner `ODR` with structured `delivery_authorization` bound to the exact repository / PR / head SHA;
- a head change makes an older grant stale;
- when provider review/check data cannot be observed, report `UNKNOWN` rather than infer success.

`technical_ready_to_merge` is derived from current acceptance/evidence plus current provider lifecycle/check/mergeability/review facts. It returns `YES | NO | UNKNOWN` with reasons.

The delivery observation is evidence, not roadmap authority and not authorization.


## Unmerged PR carry-forward

Owner status must never silently forget a still-active PR.

When `REPO_STATE.delivery.observations[]` contains provider observations, every PR last observed as:

```text
DRAFT
OPEN
UNKNOWN
```

is listed under **Unmerged PRs carried forward** on every Owner publication.

For each carried PR, show at least:

- PR number / URL;
- lifecycle;
- current observed head SHA;
- correlated Issue number(s);
- correlated EP id(s) / work package(s);
- relationship meaning.

A PR leaves this recurring list only after provider readback records terminal `MERGED` or `CLOSED` state. It can remain in durable evidence/history without cluttering every future summary.

This carry-forward is based on provider observation evidence, not memory of prior chat.

