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
