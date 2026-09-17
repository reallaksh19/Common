# Code review blueprint

## WHEN TO APPLY
Apply when a material code diff is ready for completion review or when risk warrants an independent second pass over implementation. It complements, not replaces, tests.

## REQUIRED INPUTS
EP scope, diff/change list, architecture/context, acceptance/test evidence, protected invariants, known limitations, and applicable quality procedures already performed.

## PROCEDURE
1. Review scope first: ensure every material diff belongs to the EP and no required change is missing.
2. Trace correctness through state/authority ownership and important failure/recovery paths.
3. Review maintainability, duplication, API compatibility, security/safety-relevant behavior, and test adequacy.
4. Classify findings by impact and disposition rather than labeling everything a blocker.
5. Re-review remediated HIGH/CRITICAL findings or changes they caused.

## BEST-PRACTICE CHECKLIST
- Review behavior and invariants before style.
- Cite concrete path/symbol/evidence for each finding.
- Distinguish defect, risk, suggestion, and Owner decision.
- Verify fixes did not widen scope or invalidate evidence.
- Keep nitpicks from obscuring material risk.

## ANTI-PATTERNS
Rubber-stamp approval, review by test-green status alone, vague "clean this up" comments, blocker inflation, style debates presented as safety, and approving unexplained generated/large changes.

## REQUIRED ARTIFACTS
QRV procedure result and findings with evidence, disposition, severity, and any required follow-up.

## VERIFICATION
Reconcile material findings to code/evidence and confirm dispositions are true on the reviewed material ref.

## QUALITY FINDING CLASSIFICATION
Use MAINTAINABILITY, DESIGN, TEST_GAP, DELIVERY_RISK, AUTHORITY, SAFETY, or OTHER according to the concrete issue.

## TRUE HARD-STOP CONDITIONS
Only findings that satisfy an existing hard-stop category block execution. A reviewer preference, refactor suggestion, or non-critical debt does not.

## OWNER REPORT
Surface only material risks, release implications, and genuine decisions; keep implementation nits in technical evidence.

## SUCCESSOR HANDOVER
Carry unresolved findings by ID, evidence, disposition, and target. Never drop a deferred review finding during handover.
