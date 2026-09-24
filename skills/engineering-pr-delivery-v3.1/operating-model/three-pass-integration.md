# V3 Plan for Handover and standalone three-pass integration

Engineering Relay V3.1 supplies a **frozen engineering input** to the standalone three-pass prompt generator. It does not own or reproduce the prompt schema.

Canonical standalone surfaces:

```text
skills/three-pass-prompt-generator/SKILL.md
skills/three-pass-prompt-generator/schema.md
skills/three-pass-prompt-generator/validate.py
```

At actual prompt-generation time the standalone launcher MUST still fetch its schema from current `main` and use the live protocol revision/content SHA. A V3 handover request is therefore an invocation package, not a cached copy of the generator protocol.

## Plan for Handover flow

```text
direct Owner handover command
→ relay.can(HANDOVER)
→ fresh canonical V3 snapshot
→ provider-readback handover target
→ freeze V3 basis
→ partition context by visibility
→ publish HANDOVER_CONTEXT + THREE_PASS_REQUEST
→ standalone generator fetches current-main schema
→ generator emits exactly Prompt 0.5 / 1 / 2 / 2.5 / 3
→ live standalone validator validates the generated prompt artifact
```

Prompt 0.5 and Prompt 1 are now deliberately **independent early views**:

```text
stable programme truth ──► Prompt 0.5: programme contribution
          │
          └──────────────► Prompt 1: situated local judgement

Prompt 0.5 result ─┐
Prompt 1 result   ─┼──► Prompt 2.5 reconciliation
Prompt 2 reality ──┘
```

The V3.1 adapter must not feed Prompt 0.5's speculative conclusions into Prompt 1. It also must not expose live programme reconciliation/frontier/status, accumulated learning, implementation state or active-agent conclusions to either early pass. Those are Prompt-2-and-later evidence.

Complex mode preserves the Q1–Q5 **reasoning coverage** defined by the live standalone schema. Visible Q-label headings are used only when explicitly requested; otherwise Prompt 1 remains one coherent natural practitioner prompt.

## Visibility partition

The V3 package has three explicit context surfaces.

### blind_context

May inform Prompt 0.5 and Prompt 1.

Contains only:
- programme outcome/current goal;
- roadmap identity;
- local work-package responsibility;
- stable semantic prohibitions.

It intentionally excludes:
- active lease;
- executor;
- branch;
- material/coordination heads;
- controls;
- delivery/PR state;
- current implementation evidence.

A validator also rejects dynamic reality identities if they leak back into the blind payload.

### reality_context

Reserved for Prompt 2 onward.

Contains:
- lifecycle / EP / lease / executor / branch;
- material and coordination basis;
- current evidence;
- action-scoped controls;
- delivery state.

### accumulated_learning

Contains accepted checkpoint learning/history:
- what changed;
- what is true now;
- remaining uncertainty;
- do-not-break constraints;
- attempted/rejected approaches;
- discoveries;
- known limitations;
- resume guidance.

Accumulated learning is not present action authority.

## Provider target

`HANDOVER_TARGET` is a normalized provider-readback artifact. The adapter accepts only:

```yaml
authority: PROVIDER_READBACK
provider: GITHUB
```

plus repository/kind/number/title/url/state/observed-at/provider-ref.

The repository validator proves the observation shape and binds its digest into the frozen handover context. The actual provider integration that creates the observation remains responsible for genuine provider readback; manually typed prose is not converted into provider authority.

## Prompt 3 → engineering-plan boundary

The standalone three-pass packet ends with reasoning/revalidation. It does not replace the engineering agent's own implementation plan.

For an owned implementation task, Prompt 3 should normally transition into:

```text
live revalidation
→ agent publishes IMPLEMENTATION_PLAN rev 1 on the child issue
→ V3.1 observes/binds current plan context
→ engineering execution continues without waiting for plan approval
→ PLAN_UPDATE / TASK_EVIDENCE only when meaningful
→ TASK_RESULT at handoff
```

If an EP already existed before the plan was published, keep the same EP while the owned responsibility is unchanged. Current plan revision is provider/task context, not a reason to create a replacement EP.

See `agent-task-publication.md`.

## Generated artifacts

```text
relay/GENERATED/HANDOVER_CONTEXT.yaml
relay/GENERATED/THREE_PASS_REQUEST.yaml
relay/GENERATED/THREE_PASS_REQUEST.md
```

All are generated/non-authoritative.

The request explicitly grants no new action authority. Prompt 3 must revalidate live `relay.can(action)` and explicit Owner authority before performing an action.

## Failure isolation

Failure to verify a handover target, generate the package, or satisfy a HANDOVER-only control may deny the handover operation. It does not itself deny `MATERIAL_WRITE`.

No control is automatically added merely because Plan for Handover fails.

This preserves the core V3 plane separation:

```text
handover readiness != execution safety
```

## Relationship to #420

V3-7 provides the relay-to-generator boundary: frozen basis, provider target, visibility partitions, accumulated checkpoint learning, and exact live-generator binding.

The richer handover reasoning/content redesign tracked in Common issue #420 remains separately owned. V3-7 does not silently redefine Prompt 0.5 / 1 / 2 / 2.5 / 3.


## Refinement boundary with #421 and #420

This adapter is the baseline V3 relay-to-generator boundary. Common #421 refines the handover input without changing authority ownership.

At handover freeze time, the richer task/improvement read models are derived and embedded in `HANDOVER_CONTEXT.yaml` rather than persisted again as separate synchronized files:

```text
PROJECT_SNAPSHOT
+ derived TASK_SNAPSHOT
+ derived relevant IMPROVEMENT_VIEW
+ live provider target
        ↓ freeze exact values + digests
HANDOVER_CONTEXT
        ↓
#420 five-prompt reasoning
```

The task/improvement projectors remain callable on demand for diagnostics, status rendering, or migration continuity proof; handover itself no longer depends on separate `relay/GENERATED/tasks/**` or `relay/GENERATED/improvements/**` artifacts.

Roadmap mutation remains a Relay operation. Prompt 2.5 may recommend roadmap reconciliation; Prompt 3 may return a semantic delta. Neither prompt directly writes authoritative roadmap/progress truth. Relay/checkpoint tooling performs the governed reconciliation and then regenerates projections.

The richer projections are intentionally V2.5-first: they may be generated from current V2.5 roadmap/event/checkpoint/progress intelligence before V3 becomes the selected execution protocol.
