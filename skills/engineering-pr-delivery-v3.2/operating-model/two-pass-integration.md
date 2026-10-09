# Handover custody and optional standalone Two-Pass integration

Engineering Relay treats handover as a **custody mechanism**. A custody handover freezes current Relay/provider context and does not itself request new engineering reasoning or replanning.

The standalone Two-Pass generator remains available as a separate, explicit reasoning operation.

Canonical standalone reasoning surfaces:

```text
skills/two-pass-prompt-generator/SKILL.md
skills/two-pass-prompt-generator/schema.md
skills/two-pass-prompt-generator/validate.py
```

At explicit reasoning-request generation time the helper must resolve and validate the current standalone protocol contract.

## Recovery classification — not the planned Buddy workflow

The canonical V3.2 [routing table](continuity-method-routing-v32.md) distinguishes:

- **PLANNED:** Agent A is still active. A proactively prepares a **Buddy Runner** around a source-graded ~70% episode-life threshold, followed by a **native technical handover** and Buddy Stage 2 source reconciliation. The task is **known** during Buddy Stage 1, but Agent A's actual HOW/current work is hidden. See [Runner instructions](../runner/PREPARE_FOR_RUNNER.md). `PLAN_HANDOVER` remains a custody transaction and does not initiate Two-Pass.
- **UNPLANNED, FOCUSED:** Agent A is unavailable. When independent full reconstruction is warranted, an **external agent** generates **Two-Pass** prompts from the standalone schema. Pass 1 is a **live system baseline with task/issue hidden**, Pass 2 reveals the task, current evidence and available historical handover material and drafts a plan. It must not invent a final Agent A disclosure.
- **UNPLANNED, BROADER:** A separately requested broader reimagination of the application/roadmap is a standalone **Three-Pass** generator request, not a Two-Pass handover variation. See [Three-Pass integration](three-pass-integration.md).

V3.2 fast recovery from an observed checkpoint remains the first ordinary interruption response when sufficient; no standalone prompt generator is a mandatory prerequisite. A recovery session without native `HANDOVER_CONTEXT` may inspect live provider/current source and label predecessor continuity UNKNOWN; it must **not** manufacture a predecessor-signed handover solely to satisfy a generator input. This does not weaken the canonical Two-Pass schema's Pass-1 prohibition on actual assigned-task disclosure.

## Custody flow

```text
Owner handover command
→ fresh Relay snapshot / provider target
→ freeze HANDOVER_CONTEXT
→ record HANDOVER_PLANNED
→ publish / transfer custody context
```

This flow does **not** generate:

```text
relay/GENERATED/TWO_PASS_REQUEST.yaml
relay/GENERATED/TWO_PASS_REQUEST.md
```

and it does not create an implementation plan, independent reconstruction claim, approval, merge authority, or lifecycle transition.

A previously generated Two-Pass request may still exist in a repository. It is historical/derived evidence only; its `handover_context.digest` must match the context used by an explicit reasoning operation before it can be treated as current.

## Explicit reasoning flow

When the Owner or governing responsibility separately requests reasoning:

```text
current HANDOVER_CONTEXT
→ explicit build_request(...)
→ validate current standalone Two-Pass contract
→ derived TWO_PASS_REQUEST
→ generator fetches current-main two-pass schema
→ PASS 1 independent system baseline
→ PASS 2 improvement/task reconciliation + draft plan
→ Owner approval boundary
```

The explicit request remains non-authoritative. It grants no production, lifecycle, review, merge, or programme authority.

### Execution transport after plan authority

A scheduled execution transport such as RLL-1 may be attached only **after** the applicable Pass-2 approval/publication boundary has been crossed.

The transport may remove human copy/paste between the durable child issue and the local executor, but it must not bypass the Pass-1/Pass-2 visibility boundary or manufacture approval.

For a read-only exact-head local-execution child that is already explicitly authorized by the governing issue, `EXACT_HEAD_EVIDENCE` may transport that executable evidence request without creating a new implementation plan. It still cannot broaden the engineering responsibility.

See `operating-model/transports/RLL-1.md`.

## Pass 1 visibility for an explicit reasoning request

Pass 1 may know:

- repository/application/system identity;
- broad human outcome;
- stable semantic constraints.

Pass 1 must not know or reveal:

- the actual issue/task;
- current PR/branch task state;
- requested fix;
- improvement candidate;
- implementation plan;
- further action.

The future agent inspects the live repository/application and ends at `INDEPENDENT_SYSTEM_BASELINE`.

## Pass 2 visibility and approval boundary

Pass 2 receives the Pass-1 result plus provider-verified reality and accumulated learning. It must refresh live evidence, reconcile the owned responsibility, draft any implementation plan in chat, and stop for Owner approval before durable planning or implementation authority is exercised.

## Improvement Proposal is not a fifth publication

The publication set remains:

```text
IMPLEMENTATION_PLAN
PLAN_UPDATE
TASK_EVIDENCE
TASK_RESULT
```

Approved `IP-*` content is embedded in the implementation plan. Unapproved proposals stay non-authoritative.

## Generated artifacts

Custody preparation generates:

```text
relay/GENERATED/HANDOVER_CONTEXT.yaml
```

An **explicit** reasoning-request operation may additionally derive:

```text
relay/GENERATED/TWO_PASS_REQUEST.yaml
relay/GENERATED/TWO_PASS_REQUEST.md
```

Those request artifacts are derived/non-authoritative and are never implied by custody transfer alone.

## Failure isolation

Failure to generate or validate an explicit Two-Pass request does **not** deny custody handover preparation.

Handover readiness remains distinct from reasoning readiness and execution safety.
