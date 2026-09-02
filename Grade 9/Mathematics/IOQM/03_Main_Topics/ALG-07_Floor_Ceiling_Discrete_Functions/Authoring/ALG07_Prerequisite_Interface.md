# ALG-07 Stable Discrete-Filter Interface

main_topic_id: `IOQM-G9-ALG-07`  
status: `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`  
canonical_teaching_owner: `IOQM-G9-ALG-07`

Authoring/control material; not part of the student export.

## Prerequisites

- `G9_CORE`: order on real numbers; integer arithmetic; elementary linear inequalities.
- `IOQM_BRIDGE`: exact endpoint discipline and domain intersection.
- No dependency on general optimization/AM-GM canon from ALG-02.

## Concepts owned

1. `floor(x)=n <=> n<=x<n+1`.
2. `ceil(x)=n <=> n-1<x<=n`.
3. negative-input behavior and floor-vs-truncation boundary.
4. integer translations of floor/ceiling.
5. reflection `ceil(x)=-floor(-x)`.
6. fractional part `{x}=x-floor(x)` and `0<={x}<1`.
7. floor/ceiling equations as interval constraints.
8. floor/ceiling inequalities at integer thresholds.
9. real-interval to integer-solution filtering.
10. integer counting with endpoint custody.

## Retrieval cues

- floor value -> left-closed/right-open interval;
- ceiling value -> left-open/right-closed interval;
- negative input -> order, not truncation;
- integer shift -> translate outside the symbol;
- integer-only target -> solve real interval, then intersect `Z`;
- count integers -> identify first/last integer and audit endpoints.

## First-move rules

1. `floor(A)=n` -> write `n<=A<n+1`.
2. `ceil(A)=n` -> write `n-1<A<=n`.
3. `{x}` -> write `x-floor(x)`.
4. negative floor/ceiling -> locate x between consecutive integers.
5. integer filtering -> do not filter until the real interval is correct.
6. counting -> convert endpoints to first/last admissible integer.

## Decision boundaries

- floor vs truncation;
- floor vs ceiling;
- floor equation vs ordinary equation;
- real interval vs integer solution set;
- endpoint included vs excluded;
- fractional part vs decimal-part intuition;
- integer translation vs fresh casework;
- ALG-07 interval decoding vs ALG-02 general inequality optimization.

## Misconception traps

- dropping decimals for negative floor;
- making both interval endpoints inclusive;
- writing `f(x)=n` from `floor(f(x))=n`;
- counting integer points before solving the real interval;
- treating fractional part of a negative number as its written decimal digits;
- applying `floor(x+a)=floor(x)+a` when a is not an integer;
- importing a full inequality chapter where interval decoding suffices.

## Reusable identities

- `floor(x)=n <=> n<=x<n+1`.
- `ceil(x)=n <=> n-1<x<=n`.
- `floor(x+k)=floor(x)+k`, integer k.
- `ceil(x+k)=ceil(x)+k`, integer k.
- `ceil(x)=-floor(-x)`.
- `{x}=x-floor(x)`, with `0<={x}<1`.
- `floor(x)+floor(-x)=0` for integer x, `-1` otherwise.
- `floor(x)=ceil(x) <=> x` is an integer.

## Downstream assumptions

NT/COMB bridges may assume the ability to translate a floor/ceiling constraint into a half-open interval and to intersect the result with integers. They must retrieve this interface rather than reteach floor/ceiling canon.

`SOURCE_ANCHORS_CHECKED: PASS`
`PROMOTED_ANSWERS_RECOMPUTED: PASS (91,33)`
`DEPENDENCY_INVERSION: NONE`
`DOWNSTREAM_STATUS: READY_FOR_RETRIEVAL`
