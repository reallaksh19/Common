# Engineering numerics blueprint

## WHEN TO APPLY
Apply when formulas, loads, geometry, units, material properties, tolerances, solver configuration/results, interpolation, numerical stability, or engineering limits are authoritative to the slice. Do not apply merely because numbers appear in UI or metadata.

## REQUIRED INPUTS
Governing equations/standards, units and sign/axis conventions, concrete representative inputs, validity ranges, numerical method/configuration, independent benchmark/oracle, tolerances, and protected engineering invariants.

## PROCEDURE
1. Establish the authoritative quantity, units, coordinate/sign convention, and validity domain.
2. Reconstruct at least one representative result independently where feasible.
3. Trace transformations from source inputs to final result and identify rounding/scaling/interpolation points.
4. Exercise falsifiers for unit, sign, axis, scale, boundary, and invalid-domain errors.
5. Separate workflow/UI changes from changes to numerical authority.
6. Compare against the independent oracle and record tolerance rationale.

## BEST-PRACTICE CHECKLIST
- Units explicit at every authority boundary.
- Assumptions and validity range durable.
- Tolerances justified by physics/numerics, not chosen to make tests pass.
- Representative low/high/boundary cases included.
- Solver convergence/conditioning or data interpolation behavior considered when relevant.

## ANTI-PATTERNS
Magic conversion factors, unitless authoritative values, same-implementation-as-oracle tests, unbounded extrapolation, sign corrections by trial and error, and treating plausible-looking output as validation.

## REQUIRED ARTIFACTS
Concrete reconstruction payload, oracle comparison, tolerance/units record, assumptions/validity range, and QRV findings for unresolved numerical risks.

## VERIFICATION
Use analytical/reference/manual/independent implementation evidence as applicable and show concrete expected versus observed values. Verify failure behavior outside the valid domain.

## QUALITY FINDING CLASSIFICATION
Use NUMERICAL_RISK for robustness/uncertainty and SAFETY when a numerical defect can produce unsafe engineering action. Numerical quality concern and evidence status remain distinct.

## TRUE HARD-STOP CONDITIONS
Authority-inconsistent results, protected engineering invariant failures, or unsafe engineering outputs are true stops. Advisory robustness improvements or unrun non-required sensitivity studies are not.

## OWNER REPORT
Explain the physical/engineering meaning, verified range, residual uncertainty, and any decision that changes governing engineering intent.

## SUCCESSOR HANDOVER
Transfer concrete inputs, units, oracle/tolerance, assumptions, unresolved edge cases, and the exact next reconstruction/test—not generic "verify calculations" instructions.
