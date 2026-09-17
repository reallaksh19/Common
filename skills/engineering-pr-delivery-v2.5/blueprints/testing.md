# Testing blueprint

## WHEN TO APPLY
Apply to every material behavioral change and to protocol/control-plane changes whose correctness depends on state transitions. Narrow documentation-only changes may be not applicable.

## REQUIRED INPUTS
Acceptance criteria, implementation steps, risk areas, benchmarks/oracles, changed files, supported environments, prior regressions, and obligation class for each validation item.

## PROCEDURE
1. Map every acceptance criterion to at least one verification path.
2. Select the smallest test level that proves each behavior, then add integration/end-to-end coverage where boundaries are the risk.
3. Include negative, stale-state, recovery, and boundary cases relevant to the change.
4. Execute tests on the exact material basis and preserve PASS/FAIL/NOT_RUN honestly.
5. Distinguish a test not run from a product failure and from a quality recommendation.

## BEST-PRACTICE CHECKLIST
- Tests fail for the intended reason before/fix after when practical.
- Assertions target behavior/invariants, not incidental diagnostic prose.
- No shared mutable fixture aliases that invalidate predecessor/successor evidence.
- Deterministic fixtures and explicit external dependencies.
- MUST_PASS vs SHOULD_RUN vs INFORMATIONAL remains visible.

## ANTI-PATTERNS
Testing implementation details only, exact-string coupling without semantic need, swallowing flaky failures, converting NOT_RUN to PASS, relying on compile as execution evidence, and huge end-to-end tests for locally provable rules.

## REQUIRED ARTIFACTS
Validation result matrix with command/oracle, obligation, status, exact basis, and reason/cause for NOT_RUN; regression test for every protocol defect fixed.

## VERIFICATION
Confirm executed test discovery really includes intended suites, inspect counts when useful, and reconcile results to checkpoint material_ref and acceptance state.

## QUALITY FINDING CLASSIFICATION
Use TEST_GAP for missing/weak coverage. A gap can be NEEDS_ATTENTION without being a hard stop; an actual MUST_PASS failure belongs to evidence/acceptance truth.

## TRUE HARD-STOP CONDITIONS
Only existing safety/authority/protected-invariant conditions stop execution. A missing optional test is not automatically a stop; inability to establish a required safe result may map to an existing stop with basis.

## OWNER REPORT
State what was proven, what was not run, why, and the practical residual risk without inflating test count into confidence.

## SUCCESSOR HANDOVER
List unrun checks, flaky/limited environments, exact commands, known fixture assumptions, and which acceptance items still depend on evidence.
