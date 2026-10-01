# FURTHER_TASK_SNAPSHOT — current

`AUTHORITY: DERIVED_CONTINUITY_ONLY`

Use one mutable responsibility-scoped current-state projection. Update the same managed surface at semantic events; do not append heartbeat comments.

```text
RESPONSIBILITY: <issue/task>
STATE: PLANNING | IMPLEMENTING | RECOVERING | EVIDENCING | VERIFYING | OWNER_DECISION | BLOCKED_EXTERNAL | DELIVERY_READY | COMPLETE | SUPERSEDED

PROGRESS
P: <completed>/<denominator> = <percent>
E: <evidenced>/<denominator> = <percent>
ACTIVE_UNIT: <declared unit | NONE>

PLAN
<current IMPLEMENTATION_PLAN / PLAN_UPDATE ref>

FRONTIER
MATERIAL: <head | UNKNOWN>
SEMANTIC_EVIDENCE: <head/ref | UNKNOWN>
RELATION: ALIGNED | MATERIAL_AHEAD | MATERIAL_UNKNOWN | SEMANTIC_UNKNOWN | UNRESOLVED
DELTA_COMMITS: <n | UNKNOWN>

COMPLETED
- [x] <declared unit>

ACTIVE / PENDING
- [ ] <declared unit>

CURRENT
<one concise reconstruction statement>

NEXT
<first useful engineering action>

OWNER_DECISION
NONE | <specific genuine decision>

RECOVERY
stream_loss_count: <n>
recovery_evidence_required: true | false
handover_plan_triggered_this_lifecycle: true | false
plan_for_handover_now: true | false
```

Rules:
- derive Git/material facts where automation is available;
- starting implementation changes state to `IMPLEMENTING` but earns no P/E credit;
- evidence can never outrun completion;
- title P/E is a disposable mirror;
- provider update failure is observability debt only;
- no timer/heartbeat updates.
