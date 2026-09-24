# Coordinator information-use model

The coordinator should treat the programme record as a **semantic graph**, not a status form.

## Information graph

From the parent programme specification, effective amendments, Relay Handover ledger, child issues/plans, PRs and durable evidence, derive:

```text
OUTCOME GRAPH
what human/programme result each workstream contributes to

OWNERSHIP GRAPH
who owns each responsibility / interface / integration consequence

PRODUCER-CONSUMER GRAPH
what exact output flows from whom to whom

DEPENDENCY GRAPH
which required production truth is currently missing/satisfied

EXPECTATION GRAPH
what meaningful observable should appear next

MATERIAL GRAPH
which branch/PR/head/artifact corresponds to each workstream

EVIDENCE GRAPH
which claims are actually supported and at what exact basis

NEGATIVE-KNOWLEDGE GRAPH
what has already been disproved / rejected / settled

DECISION GRAPH
what belongs to engineer, coordinator or Owner

TEMPORAL GRAPH
what unresolved expectation merits later re-observation
```

These are coordinator-derived views. None is production authority.

## 1. Programme bootstrap

On first contact or zero-context takeover:

1. read parent programme issue;
2. resolve current basis revision + effective amendment index;
3. read the dedicated Relay Handover issue;
4. enumerate child implementation issues;
5. enumerate every nonterminal PR;
6. read current implementation-plan refs;
7. verify current repository/PR/material evidence where consequence matters;
8. reconstruct negative knowledge and unresolved programme obligations;
9. derive the graphs above;
10. compare the Handover index to live durable evidence and mark stale/unknown fields rather than trusting them blindly.

Output:

```text
PROGRAMME DESTINATION
CURRENT BASIS
ACTIVE WORKSTREAMS
PRODUCER/CONSUMER EDGES
MISSING PRODUCTION TRUTH
PARALLEL-SAFE WORK
EXPECTED NEXT OBSERVABLES
NONTERMINAL PRS
NEGATIVE KNOWLEDGE
SEMANTIC UNCERTAINTIES
OWNER DECISIONS
NEXT COORDINATOR MOVES
```

Do not require all fields to be complete before coordinating.

## 2. Work Order generation

Build each Work Order by joining:

```text
parent outcome/boundary
+ effective amendments affecting this workstream
+ child responsibility
+ current implementation plan
+ canonical inputs
+ dependency contracts
+ consumer contract
+ current durable material/evidence
+ relevant negative knowledge
```

Send only context needed for good judgement.

Do not dump the whole programme when the worker only needs a bounded responsibility.

## 3. Parallelism discovery

Parallelism is a conclusion from the ownership/dependency graph, not a predeclared serial/parallel label.

Ask:

- Does one workstream require an actual output from another?
- Is the required output already available?
- Can the consumer perform meaningful independent work meanwhile?
- Do the workstreams share a semantic interface or only files?
- Would concurrent writes conflict materially?
- Can shared-file conflict be solved by worktree/integration handling rather than programme serialization?

Prefer:

```text
CAN_RUN_NOW
CAN_RUN_PARTIALLY
NEEDS_OUTPUT_FROM <producer>
MAY_CONFLICT_WITH <workstream>
```

Avoid global BLOCKED unless describing a real production impossibility.

## 4. Dependency routing

When a producer output appears:

1. validate the durable evidence;
2. map it to declared and newly discovered consumers;
3. identify what is actually proved vs not proved;
4. update the Handover producer→consumer entry;
5. send a minimal CONTEXT_UPDATE to affected running agents/local coordinator;
6. retire obsolete dependency watches;
7. create a new re-observation only if a useful unresolved expectation remains.

Do not wait for child issue closure if the required production output already exists.

## 5. Plan-conformance reasoning

Compare:

```text
ISSUE RESPONSIBILITY
× IMPLEMENTATION PLAN
× OBSERVED MATERIAL
× CURRENT EVIDENCE
```

Use:

```text
ALIGNED
MINOR_DEVIATION
MATERIAL_DEVIATION
PLAN_STALE
PLAN_CONTRADICTED
INSUFFICIENT_EVIDENCE
```

The useful question is not "did the agent follow the plan?"

It is:

> Did reality change enough that another workstream or future reconstruction would be misled by the current plan?

If yes, suggest plan reconciliation. Never invalidate useful production solely because the plan is stale.

## 6. Helper/local-coordinator selection

Recommend a helper when a bounded environment operation can cheaply reduce uncertainty, for example:

- browser/runtime evidence is needed;
- a concrete claim can be falsified by a short probe;
- large repository investigation can run independently;
- cross-environment reproduction matters;
- an agent is about to change production code to compensate for something not yet measured.

Escalate to a **local engineering coordinator** instead when Work needs:

- parallel local workers;
- worktrees;
- terminal/browser orchestration;
- local conflict resolution;
- preservation of local material across worker loss;
- low-latency engineering routing.

The programme coordinator keeps programme meaning. The local coordinator keeps local execution moving.

## 7. Timer/event selection

Attach re-observation to unresolved expectations, not agents.

Examples:

```text
RETURN_CHECK
Has the expected producer output appeared?

DEPENDENCY_CHECK
Does the consumer's required production truth now exist?

LOCAL_RESULT_CHECK
Did the bounded probe return evidence?

PROGRAMME_RECONCILIATION
Did any cross-agent consequence change?

OWNER_UPDATE_CHECK
Is there now something meaningful to tell/ask the Owner?
```

When an event arrives earlier, consume the result and let the later timer no-op if obsolete.

## 8. Session-loss recovery

If a worker/session disappears:

1. inspect issue plan + branch + nonterminal PR + exact head + tests/artifacts;
2. determine whether useful material already exists;
3. reconstruct remaining outcome from child issue + plan + Handover + evidence;
4. preserve useful local material where available;
5. dispatch a successor with the smallest reconstruction packet;
6. do not require custody/recovery ceremony to make existing production evidence valid.

The question is:

> What production consequence remains unfinished?

not:

> Which coordination token expired?

## 9. Negative knowledge

Before dispatching/reasoning, search the owning issue and Handover negative-knowledge entries.

Do not reopen a rejected path unless its explicit reopen condition is met.

If a new falsifier disproves earlier negative knowledge:

- record the new evidence;
- mark the earlier statement superseded;
- route the semantic consequence.

## 10. Semantic-boundary detection

Routine coordination uses expected→observed→consequence.

Regenerate deeper three-pass reasoning only when evidence changes:

- programme/human outcome;
- governing issue meaning;
- ownership;
- shared architecture/interface semantics;
- core production assumption;
- canonical source authority.

A plan change, commit, PR, test completion or timer wake alone is not a semantic boundary.

## 11. Owner interaction

The coordinator should compress programme reality into:

```text
WHAT CHANGED
WHAT IS NOW TRUE
WHAT CROSS-AGENT CONSEQUENCE FOLLOWS
WHAT IS STILL UNCERTAIN
WHAT NEEDS YOU
WHAT HAPPENS NEXT
```

Do not expose routine worker chatter, lease/custody diagnostics, timer mechanics or protocol bookkeeping.

## 12. Programme closure

Do not infer closure from all child PRs being merged.

Map durable evidence back to each parent EXIT-* criterion.

For every criterion report:

```text
SATISFIED
PARTIAL
OPEN
DEFERRED
NOT_APPLICABLE
```

with exact evidence.

If a child delivered something useful but not enough to satisfy its parent criterion, preserve the child result and keep the parent obligation open.

## 13. Recorder relationship

Relay V3.1 may record/reconstruct the above facts.

The coordinator must use **V3.1 only** when Relay context is relevant.

Never use V3 or V2.5 for live coordination, status, recovery, gating, handover or Owner-command semantics.

V3.1 does not manufacture programme authority from incomplete records.
