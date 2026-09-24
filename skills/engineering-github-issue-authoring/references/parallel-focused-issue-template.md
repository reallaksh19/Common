# Parallel focused engineering issue

Use for small/medium parallel work such as a falsifier, stale expectation, source-derived oracle correction, focused guardrail debt or bounded integration finding.

The issue must be rich enough for zero-context reconstruction but small enough that the agent can exercise engineering judgement.

```text
ISSUE_ROLE: PARALLEL_FOCUSED
PROGRAMME: github:<owner>/<repo>#<parent>
WORKSTREAM_ID: <F/G/H/...>
RELAY_PROTOCOL: V3.1_ONLY
```

## Outcome

What exact production truth/behavior should become correct?

## Why now / concrete witness

Exact current failure, discrepancy, evidence or programme need.

## Owned responsibility

- ...

## Ownership boundary / conflict-avoidance fence

This workstream does not own:

- ...

This is an ownership/conflict boundary, **not write permission**.

## Canonical inputs / source truth

| Ref | Meaning | Authority |
| --- | --- | --- |
| ... | ... | ... |

Do not change a canonical declaration merely to make the current test pass unless evidence shows the declaration itself is wrong.

## Preserve / invariants

- ...

## Producer / consumer contract

**Produces:** ...

**Consumed by:** ...

**Consumers must not infer:** ...

## Dependencies

For each real dependency:

**Required production output:** ...

**Producer:** ...

**Why required:** ...

**Satisfaction evidence:** ...

**Work that may continue independently:** ...

If none: state `NONE`.

## Falsifier

What evidence would prove the current assumed fix/framing wrong?

## Success oracle

What exact durable evidence proves this issue is resolved?

## Acceptance Contract

Use stable `AC-*` IDs. These are the denominator for child/work-issue completion reporting.

| ID | Criterion | Parent mapping | Weight |
| --- | --- | --- | ---: |
| AC-<workstream>-01 | ... | EXIT-... | 1 |

Keep criteria observable and evidence-bound. Do not use PR count, commit count, chat activity, or plan publication itself as acceptance.

If no weighting is genuinely needed, keep equal weights or omit weights in provider observations; V3.1 will report **unweighted acceptance coverage** rather than inventing a composite score.

## Implementation Plan

Agent-authored and revisable:

- understanding;
- source truth inspected;
- proposed approach;
- meaningful `STEP-*` slices with state and mapped `AC-*` criteria;
- expected changed files/components;
- validation;
- preserve/invariants;
- dependencies/assumptions;
- uncertainties;
- expected handoff;
- next meaningful observable.

Publishing/updating the plan is useful reconstruction context, not execution approval.

## Task publication lifecycle

Use the child issue for the engineering agent's durable semantic task record:

```text
IMPLEMENTATION_PLAN — rev 1
PLAN_UPDATE — only when material learning changes the approach
TASK_EVIDENCE — only for meaningful intermediate evidence
TASK_RESULT — at delivery/handoff
```

The engineering agent authors the plan. Plan publication/revision is not approval and does not block production. Do not post every command or test retry.

## Expected handoff

Return:

- exact output;
- exact material/evidence refs;
- proved;
- not proved;
- limitations;
- downstream consequence;
- anything consumers must not infer.

## Semantic escalation

Escalate only if evidence materially changes programme meaning, shared architecture/interface ownership, this issue's responsibility, another workstream's durable assumptions, or requires a genuine Owner decision.
