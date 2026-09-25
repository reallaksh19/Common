# V3.1 Plan for Handover and standalone two-pass integration

Engineering Relay V3.1 supplies a frozen engineering input to the standalone two-pass generator. It does not own or reproduce the prompt schema.

Canonical standalone surfaces:

```text
skills/two-pass-prompt-generator/SKILL.md
skills/two-pass-prompt-generator/schema.md
skills/two-pass-prompt-generator/validate.py
```

At generation time the launcher must fetch its schema from current `main`.

## Flow

```text
Owner handover command
→ fresh V3.1 snapshot/provider target
→ freeze HANDOVER_CONTEXT
→ publish TWO_PASS_REQUEST
→ generator fetches current-main two-pass schema
→ PASS 1 independent system baseline
→ PASS 2 improvement/task reconciliation + draft plan
→ Owner approval
→ refresh live reality
→ IMPLEMENTATION_PLAN on original child issue
→ existing/new EP binding by responsibility
→ Task Snapshot + Handover refresh
→ execution/publications within approved authority
```

## Pass 1 visibility

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

Pass 2 receives the Pass-1 result plus:

- provider-verified target;
- current material/provider state;
- programme/task context;
- accumulated learning/history.

It must:

1. refresh live evidence;
2. identify zero or more legitimate high-ROI Improvement Proposals;
3. quantify them from evidence;
4. reconcile the actual issue responsibility;
5. draft the implementation plan in chat;
6. stop for Owner approval.

No durable implementation plan, EP creation/binding, branch/PR creation, or material implementation should be performed from the proposal response.

After explicit approval, Pass 2 continues in the same conversation:

- refresh reality again;
- if the approval basis materially changed, show the delta and stop;
- otherwise publish the approved implementation plan on the original issue;
- include only approved in-scope proposals;
- route approved adjacent proposals to separate responsibilities/EPs;
- bind or create EPs by bounded engineering responsibility;
- refresh Task Snapshot/Handover so the coordinator can consume expected vs observed state;
- execute only within actual approved/authorized production authority.

## Improvement Proposal is not a fifth publication

The V3.1 publication set remains:

```text
IMPLEMENTATION_PLAN
PLAN_UPDATE
TASK_EVIDENCE
TASK_RESULT
```

Approved `IP-*` content is embedded in the implementation plan. Unapproved proposals stay in chat only.

## Generated artifacts

```text
relay/GENERATED/HANDOVER_CONTEXT.yaml
relay/GENERATED/TWO_PASS_REQUEST.yaml
relay/GENERATED/TWO_PASS_REQUEST.md
```

All are generated/non-authoritative.

## Failure isolation

Failure to generate or validate the two-pass request may deny handover preparation. It does not itself deny material engineering work.

Handover readiness remains distinct from execution safety.
