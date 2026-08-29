# P2 Greatest / Least Integer Functions — QA v1

## Verdict

`INTERNAL_PACKAGE_COMPLETE_NOT_PUBLICATION_READY`

`SECOND_MATH_EDITORIAL_PASS: PASS`

## Authority / provenance gates

| Gate | Status | Note |
|---|---|---|
| explicit syllabus obligation identified | PASS | Five-Year Scored Recurrence classifies Greatest/Least Integer functions as P2 coverage risk |
| direct five-year recurrence claim | NOT_ESTABLISHED | intentionally not fabricated |
| bridge evidence separated from primary evidence | PASS | 2024 Q27 retained only as incidental floor bridge after GP |
| author-created material provenance | PASS | no fake NMTC year/question identifiers |
| 2022 recovery effect | OPEN_GLOBAL | may alter historical evidence status later |

## Mathematical gates

| Check | Status |
|---|---|
| `floor(x)=m <=> m<=x<m+1` | PASS |
| `ceil(x)=m <=> m-1<x<=m` | PASS |
| negative-floor examples | PASS |
| `ceil(x)=-floor(-x)` | PASS |
| fractional part range `0<={x}<1` | PASS |
| negative fractional-part examples | PASS |
| floor/ceiling inequality endpoint rules | PASS |
| `x=n+r` decomposition | PASS |
| nested floor/ceiling on integer outputs | PASS |
| floor-sum bounds | PASS |
| shifted identity with `1/2` | PASS |
| shifted identity with `1/3,2/3` | PASS |
| integer counting formula | PASS |
| square-root interval transfer | PASS |
| complete-groups vs minimum-groups floor/ceiling distinction | PASS |

## Transfer-bank second review

- A1: `2<=x<7/3` — PASS.
- A2: `-2<x<=-3/2` — PASS.
- A3: `(-sqrt5,-2] union [2,sqrt5)` — PASS.
- B1: negative floor/ceil/fractional part `-4,-3,3/5` — PASS.
- B2: four bounded `n+1/4` values — PASS.
- C1: `x+floor(x)=9/2` gives unique `x=5/2` — PASS.
- C2: `2x-floor(x)=7` gives `13/2,7` — PASS.
- C3: `floor(x)=floor(2x)` gives `[-1/2,1/2)` — PASS.
- D2: split at fractional part `1/2` — PASS.
- E2: `64<=n<81` gives 17 integers — PASS.
- F2: `ceil(sqrt(x))=6` gives `25<x<=36` — PASS.

## Mastery-test second review

Special rechecks:

1. Q1 floor endpoint orientation — PASS.
2. Q2 ceiling endpoint reversal — PASS.
3. Q3 integer/noninteger split; solution `(3,4)` — PASS.
4. Q4 only `x=0` — PASS.
5. Q6 `25<=2n<36` gives exactly 5 positive integers — PASS.
6. Q8 fractional-part condition `{x}<1/2` — PASS.
7. Q9 three-shift identity split at `1/3,2/3` — PASS.
8. Q10 value `1` for integer x, `0` otherwise — PASS.
9. Q12 evidence classification — PASS.

## Pedagogy gates

- definition precedes formulas: PASS;
- interval translation is the dominant first move: PASS;
- negative truncation is explicitly falsified: PASS;
- boundary checking is repeated across concept/practice/test: PASS;
- graph behavior is derived from intervals rather than memorized: PASS;
- method connects to number theory/counting/sequence bridges: PASS;
- source-QC is included without inventing historical support: PASS.

## Internal asset completeness

- concept spec: PASS;
- source map: PASS;
- student draft: PASS;
- 14 First-Step cards: PASS;
- 10 mechanism ladders: PASS;
- 18 reviewed transfer items: PASS;
- 20 recognition items: PASS;
- 12 first-line items: PASS;
- 12-question mixed mastery test: PASS.

## Publication-stage blockers

1. `CLASSROOM_TIMING_CALIBRATION: NOT_RUN`
2. `FINAL_STUDENT_TEACHER_SPLIT: NOT_RUN`
3. `PRODUCTION_BANK_MACHINE_METADATA: NOT_RUN`
4. `FINAL_TYPOGRAPHY_RENDER_QA: NOT_RUN`
5. `2022_SOURCE_RECOVERY: GLOBAL_OPEN`

## Promotion

`PACKAGE_STATUS: INTERNAL_PACKAGE_COMPLETE_NOT_PUBLICATION_READY`
