# Methodology

1. Bind every submission to one exact candidate artifact SHA256.
2. Validate reviewer class against review dimension.
3. Require explicit reviewer identity authorization in the class-specific registry list.
4. Require exact authorization-registry version match.
5. Require source `HUMAN_SUBMISSION`; AI, CI, automation, or machine evidence is inadmissible.
6. Validate complete required rubric coverage.
7. Reject internally inconsistent PASS submissions: any required criterion failure or open blocking finding makes PASS invalid.
8. Project per-dimension gates conservatively: no admissible evidence → PENDING; any admissible FAIL → FAIL; required count of admissible PASS → PASS.
9. Keep test-only reviewer registries and submissions structurally non-releaseable.
10. Emit deterministic evidence packages for fixed inputs.

The intake layer may project a quality summary but never mutates the candidate or upstream educational state.
