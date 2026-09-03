# ALG-02 — Teacher Coverage Enrichment Addendum

Status: `STATIC_DIAGNOSTIC_ADDENDUM_V1`
Issue: `#134`

This addendum synchronizes the learner-facing absolute-value inequality bridge in `03_First_Step_Reference.md`. It does not alter historical-anchor answers or existing scored-item keys.

## Canonical absolute-value translations

For `d>=0`:

- `|u|<d` iff `-d<u<d`;
- `|u|<=d` iff `-d<=u<=d`;
- `|u|>d` iff `u<-d` or `u>d`;
- `|u|>=d` iff `u<=-d` or `u>=d`.

The distance interpretation is the preferred first explanation. Learners should not treat an absolute-value inequality as an AM-GM/Cauchy optimization problem merely because an inequality sign appears.

## Nested absolute-value diagnostic

For `||x|-k|<d`, first remove the outer absolute value:

`-d < |x|-k < d`, hence `k-d < |x| < k+d`.

Only then split according to the lower bound on `|x|`.

### Check A

Solve `||x|-7|<2`.

Expected route:

`5<|x|<9`, hence `-9<x<-5` or `5<x<9`.

### Check B — integer count

How many integers satisfy `||x|-2020|<5`?

Expected route:

`2015<|x|<2025`; the possible positive magnitudes are `2016,...,2024`, nine choices. None is zero, so each gives two signs. Answer: **18**.

### Check C — lower bound crosses zero

Solve `||x|-2|<5`.

Expected route:

`-3<|x|<7`. Since `|x|>=0`, the lower condition is automatic. Thus `|x|<7`, so `-7<x<7`.

## Required misconception contrasts

- `|u|<d` gives one interval; `|u|>d` gives two rays when `d>=0`.
- Nested absolute value is removed from the outside inward.
- Integer counting occurs **after** the real set is established.
- Strict vs non-strict endpoints must be preserved.
- A negative comparison constant requires a feasibility check before applying memorized templates.

## Diagnostic codes

- `ALG02-ABS-1`: treats `|u|<d` as two outside rays.
- `ALG02-ABS-2`: removes the inner absolute value before the outer one.
- `ALG02-ABS-3`: counts integers before solving the real interval/union.
- `ALG02-ABS-4`: loses strict/closed endpoint information.
- `ALG02-ABS-5`: imports an optimization theorem where interval translation is the governing method.

## Evidence truth

The comparison DOCX motivated this coverage check but is not the source authority. This addendum records static curriculum coverage only; classroom timing/readability, retention, psychometrics, qualification/pass-mark calibration and publication approval remain `NOT_RUN`.