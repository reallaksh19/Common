# Work Order

Send a substantial outcome-oriented assignment. Do not nano-manage implementation.

**Relay protocol rule:** use Engineering Relay **V3.1 only** if Relay context is relevant. Do not consult or use V3 or V2.5 for live status, coordination, gating, recovery, handover, or Owner-command semantics.

```text
WORK_ORDER

WORKSTREAM
<alias / issue>

OUTCOME
<what must become true in production>

PRODUCTION BOUNDARY

OWNS
- ...

EXCLUDES
- ...

CURRENT DURABLE INPUTS
- <issue / commit / PR / artifact / canonical source>
- include observed head/digest/time only when it materially improves reconstruction

DEPENDENCY CONTRACTS

1. REQUIRED OUTPUT
   <actual missing production truth>

   PRODUCER
   <if known>

   WHY REQUIRED
   ...

   SATISFACTION EVIDENCE
   - ...

   WORK THAT MAY CONTINUE INDEPENDENTLY
   - ...

FALSIFIER
- <what would show the intended work is unnecessary/wrong/differently framed>

SUCCESS ORACLE
- <observable evidence that proves the owned outcome works>

EXPECTED NEXT OBSERVABLE
<the next useful production/evidence event, not a heartbeat>

Examples:
- implementation plan persisted;
- falsifier result;
- durable commit/PR;
- exact runtime evidence;
- producer handoff;
- dependency discovery;
- verified negative result.

CONSUMERS
- <who needs the result and what they consume>

SEMANTIC ESCALATION
Return early only if evidence materially changes:
- product meaning;
- shared architecture/interface ownership;
- this issue's responsibility;
- another workstream's durable assumptions;
- a genuine Owner decision.

OWNER DECISIONS ALREADY MADE
- ...

EXECUTION STYLE
Design the detailed implementation yourself.
Use falsifiers and validation appropriate to the issue.
Do not wait on coordination/reporting metadata.
If a dependency is missing, continue any explicitly independent work.
Return durable evidence and cross-workstream consequences.
```
