# ALG-05 Stable Functional-Equation Interface v1

Status: `FROZEN_FOR_DOWNSTREAM_RETRIEVAL`

Provider: `IOQM-G9-ALG-05`

Prerequisite retrieved: ALG-01 stable prerequisite interface `fc685ff0a2e9bd67fbd6a920e730b7fff633404b`.

## Exported problem-solving contract

1. State the allowed input domain before substituting.
2. Prefer a legal input that collapses a product, sum, shift, or nested argument.
3. When `f(c-x)` appears with `f(x)`, write the equation at `c-x`; the partner map returns to `x`.
4. Combine paired equations target-first; do not solve more function values than needed.
5. On an integer domain, a derived step relation may propagate values, but it remains a consequence until the candidate formula is verified in the original functional equation.
6. A finite value table supports a conjecture, not a proof.
7. To prove injectivity, start from equal outputs and force equal inputs. To prove surjectivity, construct a preimage for an arbitrary target. Use these only when the equation makes the proof concrete.
8. Domain/codomain facts are introduced only when they control legal substitutions or the requested property.

## Ownership boundary

ALG-05 owns strategic functional-equation substitutions, involution pairing, function-value elimination, integer-domain FE propagation, and equation-justified injectivity/surjectivity.

ALG-01 remains the owner of generic algebraic transformation/equivalence discipline. ALG-04 remains the owner of generic recurrence/sequence doctrine. This interface does not export abstract function theory.

## Source certification

Historical anchors:
- `IOQM-2025-Q14 = 12`;
- `IOQM-2024-Q16 = 08`.

Both are official-source, independently recomputed, and clean in the frozen verification ledger.

Classroom timing/readability, retention, psychometrics, calibration and publication approval are `NOT_RUN`.
