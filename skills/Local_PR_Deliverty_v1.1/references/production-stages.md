# Forward-only production stages

Coder, Reviewer and Coordinator/Super Reviewer are successive producers.

Reviewer may edit product material to fix defects discovered during Reviewer production. Coordinator/Super Reviewer may edit product material to fix defects discovered during project acceptance. Both require the exclusive writer slot.

No completed downstream stage routes ordinary fix responsibility to an earlier stage. REWORK continues the same stage responsibility; it never means “send back to Coder” or “send back to Reviewer.”

## Work to exhaustion

Finding one defect is not normally a reason to stop. Continue every remaining check whose result is still meaningful, fix in batches, rerun affected checks, and publish a consolidated END. Early termination needs an explicit Owner/external/provider/protected-policy/safety boundary.

## Protected surface

Production stages may change product source and normal regression tests. They may not silently weaken the pinned project protocol, Super Reviewer harness, protected fixtures/goldens, oracle versions, expected baselines, tolerances, benchmark budgets, required-gate policy or acceptance CI.

## Education

Each stage documents what assumption failed, why earlier evidence did not catch it, which invariant matters, what regression was added, and what downstream stages must preserve. Education moves forward with the improved candidate; responsibility does not move backward.

## Production accounting

Every stage END records whether the candidate actually changed, defects found, defects fixed in that stage, regression additions, education points and external escalations. `candidate_changed` must agree with input/output identity. A stage cannot claim a fixed defect it did not record as found/consumed. BLOCKED requires an explicit genuine external/Owner/provider/protected-policy escalation and zero unresolved internal fixable defects.

Reviewer advancement must cover every project criterion marked `reviewer_check_required` with Reviewer-independent evidence. Super Reviewer advancement must cover every criterion marked `super_review_required` with Super Review/external-oracle evidence. Optional `NOT_APPLICABLE` results require explicit rationale.


## Discovery freeze and bounded repair

Reviewer and Super Reviewer do not start editing at the first observed defect. They execute the role-required discovery method set against the input candidate, freeze the discovery evidence/finding set, then begin repair. The first repair timestamp must follow the freeze.

Each finding is classified. `BOUNDED_PRODUCT_FIX` may be fixed and verified in the discovering stage. `MATERIAL_SCOPE_CHANGE`, `ACCEPTANCE_SURFACE_DEFECT` and `EXTERNAL_DEPENDENCY` cross the current stage/acceptance authority boundary and require structured escalation or a newly pinned basis; they may not be relabeled as a bounded fix to preserve flow.

After any product change, final acceptance evidence is recollected against the final candidate. Discovery evidence remains evidence about the pre-repair input, not proof of post-repair correctness.

Stage lifecycle completion is `STAGE_COMPLETE` or, only where explicit Owner risk acceptance permits a truthful required `NOT_RUN`, `STAGE_COMPLETE_WITH_WAIVER`. `PASS` remains an evidence/criterion/gate result.
