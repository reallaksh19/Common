# ALG-07 - Consolidated Research Interfaces

Authoring-only evidence. These are not standalone student chapters.

## A. Definition/order
- invariant: `floor(x)=n <=> n<=x<n+1`; `ceil(x)=n <=> n-1<x<=n`;
- first move: decode the half-open interval;
- misconception: treating the symbol as decimal deletion;
- QA: derivation PASS.

## B. Endpoint control
- invariant: floor is left-closed/right-open; ceiling is left-open/right-closed;
- first move: mark brackets before algebra;
- contrast: included vs excluded endpoint;
- QA: PASS.

## C. Negative inputs
- invariant: floor moves toward `-infinity`, not toward zero;
- first move: locate between consecutive integers;
- misconception: truncation;
- QA: PASS.

## D. Translation/reflection/fractional part
- identities: integer shifts commute with floor/ceiling; `ceil(x)=-floor(-x)`; `{x}=x-floor(x)`;
- boundary: integer shift identity does not extend naively to noninteger shifts;
- QA: PASS.

## E. Equations/inequalities
- floor equation -> double inequality;
- ceiling equation -> opposite half-open double inequality;
- general inequality doctrine is not imported from ALG-02;
- QA: PASS.

## F. Integer filtering/counting
- first solve real interval, then intersect with `Z`;
- count via first/last admissible integer and endpoint audit;
- misconception: rounding endpoints inconsistently;
- QA: PASS.

## G. Source/PYQ audit
- `IOQM-2024-Q21`: independent result 91, source/key agreement PASS;
- `IOQM-2024-Q26`: independent result 33, source/key agreement PASS;
- no metadata correction overlay applies to either anchor.

## Lead integration disposition

Teach the interval definitions once, then retrieve them. Keep one learner vocabulary: **decode -> solve -> filter -> check endpoints**. Do not expose microstream labels or control-plane terms in student exports.

`DERIVATIONS_CHECKED: PASS`
`PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS`
`SOURCE_IDS_VERIFIED: PASS`
`DEPENDENCY_CONFLICTS: NONE`
