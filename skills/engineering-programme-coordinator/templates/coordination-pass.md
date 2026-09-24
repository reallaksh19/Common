# Coordination pass

Use this prompt for ChatGPT Work or another programme coordinator to re-observe a live multi-agent programme.

This is a reasoning/reporting pass. It does not authorize or deny production.

```text
COORDINATION PASS

Read current durable production reality first:

- governing parent/programme issue;
- active child issue contracts;
- each agent's latest durable implementation plan;
- current branch/PR/commit/test/runtime evidence;
- recent durable handoffs;
- local engineering coordinator snapshot/returns when available;
- relevant canonical source truth;
- source freshness.

Do not treat chat activity, timers, Relay state, leases, checkpoints or coordinator metadata as production permission.

For each workstream, reconstruct:

1. ISSUE RESPONSIBILITY
   What does this issue actually own?

2. PLAN
   Is a durable implementation plan PRESENT, MISSING, STALE or UNKNOWN?
   Missing/stale reduces confidence only.

3. EXPECTED
   What concrete production/evidence event was expected next?

4. OBSERVED
   What is actually true now?
   Cite durable evidence.

5. PLAN CONFORMANCE
   Classify:
   ALIGNED
   MINOR_DEVIATION
   MATERIAL_DEVIATION
   PLAN_STALE
   PLAN_CONTRADICTED
   INSUFFICIENT_EVIDENCE

   Judge unreconciled semantic deviation, not harmless implementation churn.

6. DEPENDENCIES
   For each real dependency state the required production output.
   Classify:
   SATISFIED
   MISSING
   UNCERTAIN
   DISCOVERED
   SUPERSEDED

   Also state what work may continue independently.

7. HELPER NEED
   Would a bounded local/browser/runtime helper materially reduce uncertainty or protect production?
   Recommend only when useful.

8. EVIDENCE SCOPE
   Which evidence is LOCAL_ONLY?
   Which is SHARED_DURABLE?
   Does anything need promotion because another workstream now depends on it?

9. UNCERTAINTY
   Distinguish:
   OPEN_QUESTION
   RISK
   FALSIFIER_IN_FLIGHT
   UNKNOWN

10. CONSEQUENCE
    What, if anything, follows for another agent, this plan, the Owner or next observation?

11. SUGGESTED ACTION
    Only if useful.
    State target, reason, action, affected workstreams, evidence and whether Owner judgement is required.

Then reconcile cross-workstream reality:

- newly discovered dependencies;
- newly satisfied dependencies;
- conflicting assumptions;
- overlapping ownership;
- producer results that should be routed to consumers;
- local evidence that now needs promotion;
- any semantic-boundary change.

Ask whether a genuine semantic boundary changed:

- product goal/meaning;
- governing issue meaning;
- ownership;
- shared architecture/interface contract;
- fundamental capability assumption.

If NO:
keep prior direction and make the smallest coordinator move.

If YES:
identify exactly what changed and whether fresh three-pass reasoning is warranted.

OWNER

Report only genuine decisions or material risks that belong to the Owner.

NEXT OBSERVATION

State why another observation would be useful and what evidence would make it informative.
Do not create a timer merely to have one.

OUTPUT

Produce a coordination observation matching
engineering-coordinator-observation-v1.

The central calculation is:

EXPECTED
→ OBSERVED
→ CONSEQUENCE

If nothing meaningful changed:
say so.
Do not manufacture an intervention.
```
