# NT-01 - Consolidated Research Interfaces

Authoring-only. These are evidence interfaces consumed by one pedagogical owner; they are not standalone student chapters.

## A. Divisibility meaning and algebra

- included: `a|b <-> b=ak`; closure under integer linear combinations; structural divisibility;
- excluded: prime-exponent divisibility canon (NT-03), congruence notation (NT-02);
- learner gap: treats divisibility as a test rather than a relation;
- invariant: integer combinations of multiples remain multiples;
- first move: rewrite/linearly combine;
- key contrast: one-number test vs variable structural relation;
- QA: derivation PASS.

## B. Euclidean algorithm

- prerequisite: division with remainder;
- invariant: `gcd(a,b)=gcd(b,a-qb)`;
- first move: replace the larger number by a remainder;
- misconception: factor both numbers by default;
- fading track: H3 explicit remainder equation -> H2 invariant cue -> H1 "shrink without changing gcd" -> H0 changed numbers;
- QA: derivation PASS.

## C. gcd/lcm reconstruction

- invariant: for positive integers `gL=ab`;
- normalization: `a=gu`, `b=gv`, `gcd(u,v)=1`, `uv=L/g`;
- boundary: product target vs actual pair target;
- excluded: full prime-exponent proof/divisor-count enumeration canon from NT-03;
- QA: promoted examples independently checked.

## D. Same remainder and differences

- theorem: equal remainders under divisor `d` imply `d` divides all differences;
- first move: subtract before enumerating divisors;
- mandatory fork: unknown divisor -> gcd differences; unknown number with prescribed remainder -> subtract remainder then lcm;
- misconception: route every remainder problem to lcm;
- QA: derivation PASS.

## E. Divisibility chains

- invariant: transitivity `a|b`, `b|c` -> `a|c`;
- derived compression: if `a|b`, gcd is `a` and lcm is `b`;
- first move: rewrite nested conditions as a chain;
- misconception: treat chain constraints as independent tests;
- QA: PASS.

## F. Source/PYQ audit

### IOQM-2025-Q02
- source authority: HBCSE official Set M1 / final official key;
- independent trace: `floor(100/3)-floor(100/6)=33-16=17`;
- source-key agreement: PASS.

### IOQM-2025-Q27
- source authority: HBCSE official Set M1 / final official key;
- independent trace: rewrite each lcm through gcd; exactly one relevant gcd equals 1; the other is forced to 2; two symmetric `(a,b)` families and 20 admissible `c` values each;
- independent result: 40;
- source-key agreement: PASS.

## Lead integration dispositions

Teach globally once:
- divisibility equation language;
- subtraction/linear-combination invariant;
- divisor-vs-multiple router;
- same-remainder fork;
- Euclidean reduction;
- gcd/lcm normalization;
- divisibility chains.

Compress later appearances into retrieval cues. Do not expose microstream letters, production states or source-audit codes in the student PDF.

## Independent QA status

`DERIVATIONS_CHECKED: PASS`  
`PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS`  
`SOURCE_IDS_VERIFIED: PASS`  
`DEPENDENCY_CONFLICTS: NONE`  
`OPEN_ISSUES: NONE_BLOCKING_STATIC`
