# Work-Package / Revision Engineering Issue Template

Use for a bounded engineering responsibility. For small parallel tasks prefer `parallel-focused-issue-template.md`.

```markdown
ISSUE_ROLE: WORK_PACKAGE | REVISION | INTEGRATION
PROGRAMME: github:<owner>/<repo>#<parent>
WORKSTREAM_ID: <A/B/C/...>
RELAY_PROTOCOL: V3.1_ONLY
PREDECESSOR_WORK_ITEM_KEY: NONE | github:<owner>/<repo>#<predecessor>

# Outcome
<Exact production result this workstream owns.>

# Why now / concrete witness
<Exact current need/failure/evidence.>

Observed main: `<40-hex>`

# Owned responsibility
- ...

# Ownership boundary / conflict-avoidance fence
Does not own:
- ...

This boundary prevents semantic/conflict drift; it is not execution permission.

# Canonical inputs / source truth
| Ref | Meaning | Authority |
|---|---|---|
| ... | ... | ... |

# Preserve / invariants
- ...

# Producer / consumer contract
Produces:
- ...
Consumed by:
- ...
Consumers must not infer:
- ...

# Dependencies
For each real dependency:
Required production output: ...
Producer: ...
Why required: ...
Satisfaction evidence:
- ...
Work that may continue independently:
- ...

# Falsifier
- ...

# Success oracle
- ...

# Implementation Plan
Agent-authored and revisable:
- understanding;
- source truth inspected;
- approach;
- meaningful slices;
- expected files/components;
- interfaces affected;
- validation;
- preserve/invariants;
- dependencies/assumptions;
- local/browser/runtime validation;
- uncertainties;
- expected handoff;
- next meaningful observable.

A missing/stale plan is visible reconstruction debt, not a production blocker.

# Task publication lifecycle

Use the child issue for the engineering agent's durable semantic task record:

```text
IMPLEMENTATION_PLAN — rev 1
PLAN_UPDATE — only when material learning changes the approach
TASK_EVIDENCE — only for meaningful intermediate evidence
TASK_RESULT — at delivery/handoff
```

The engineering agent authors the plan. Plan publication/revision is not approval and does not block production. Do not post every command or test retry.

# Expected handoff
Return:
- exact output;
- exact material/evidence refs;
- proved;
- not proved;
- limitations;
- consumer consequence;
- anything consumers must not infer.

# Semantic escalation
Escalate only if evidence materially changes programme meaning, shared architecture/interface ownership, this issue's responsibility, another workstream's durable assumptions, or requires a genuine Owner decision.

# Optional Appendix A — implementation questions
For complex/critical tasks only. Q1–Q5 may be used to improve reasoning/falsification; they are never a qualification or permission gate.
```
