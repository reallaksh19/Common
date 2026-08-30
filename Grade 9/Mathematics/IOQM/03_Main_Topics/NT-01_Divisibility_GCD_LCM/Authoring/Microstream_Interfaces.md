# NT-01 — Wave-1 Microstream Interfaces

Authoring-only. Do not export to the student PDF.

## A. Divisibility meaning and algebra
- prerequisite: integer multiplication;
- missing bridge: `a|b` means existence of integer `k` with `b=ak`;
- invariant: integer linear combinations of multiples remain multiples;
- misconception: treating `a|b` as ordinary fraction notation;
- first move: rewrite divisibility as an integer equation.

## B. Euclidean algorithm
- prerequisite: division with remainder;
- derivation: `gcd(a,b)=gcd(b,a-qb)`;
- invariant: common divisors are unchanged by subtracting multiples;
- first move: replace the larger number by a remainder;
- contrast: factor both numbers vs Euclidean reduction.

## C. gcd/lcm reconstruction
- prerequisite: common divisor/common multiple meaning;
- invariant for positive integers: `gcd(a,b) lcm(a,b)=ab`;
- first move: normalize `a=gu, b=gv` with `gcd(u,v)=1` when useful;
- boundary: prime-exponent proof belongs to NT-03; use a short proof or retrieve it.

## D. Same remainder and differences
- key theorem: if `a,b` leave the same remainder on division by `d`, then `d | (a-b)`;
- first move: subtract before enumerating divisors;
- misconception: taking lcm when the task is to find a divisor.

## E. Divisibility chains / extremal divisors
- key move: largest valid divisor -> gcd of all required differences/terms;
- smallest common multiple -> lcm;
- contrast: greatest divisor vs least multiple.

## F. Source/PYQ audit
- `IOQM-2025-Q02`: verified; use for direct divisibility counting bridge;
- `IOQM-2025-Q27`: verified; use for higher-ceiling lcm/gcd normalization;
- no source correction overlay required for these IDs.

## Lead integration rule

The student book must not expose these microstream boundaries. The lead should weave them around one repeated router: **divisor? difference? gcd? multiple? lcm?**
