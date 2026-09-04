# Number Theory Study Guide — Appendix Benchmark Requirements

Status: `OWNER_REQUIREMENT`

This file records the owner-specified appendix contract for the Grade 9 IOQM Number Theory study guide. It supplements the attached benchmark/instructions and takes precedence where it is more specific.

## Benchmark role

Use the supplied **Combinatorics IOQM Grade 9 Study Guide v2** for quality, audit rigor, student self-sufficiency, appendix isolation, source discipline, and production expectations.

Do **not** copy its combinatorics content or layout mechanically.

The Number Theory guide is for a roughly 50%-prepared Grade 9 learner and must teach recognition, theorem legality, the first useful mathematical line, execution, and verification rather than merely list tricks or theorem names.

---

# Appendix A — all 90 marathon questions

## Required scope

Appendix A must ultimately contain:

- **Q1 through Q90** from the Number Theory marathon/source-recovery project;
- every question exactly once;
- questions only in the question section;
- no tips, solutions, method labels, or source commentary mixed into the question statements;
- all mathematical conditions preserved;
- one answer key only after Q90.

## Provenance requirement

Every Appendix A item must retain provenance/confidence metadata in the companion source ledger, not inside the student question block.

Allowed confidence states include:

- direct video-confirmed;
- independently verified original-source match;
- verified reconstruction;
- corrected reconstruction;
- source-sequence inferred;
- continuation-source inferred;
- partial/unverified wording.

A coaching reconstruction must never be promoted to an official historical problem unless independently established.

## Current gap

The present verified extraction contains **Q1–Q83**. **Q84–Q90 remain unresolved.**

Therefore:

`APPENDIX_A_Q1_Q90_COMPLETE = BLOCKED`

until seven genuine continuation questions are recovered from reliable evidence, such as:

- direct video slide/timestamp evidence;
- official marathon slides/module continuation;
- reliable transcript continuation;
- another source that can be sequence-anchored without guessing.

Do not substitute unrelated Number Theory questions merely to make the count reach 90.

Q1 and Q18 also retain their existing source-warning status until stronger evidence is found.

---

# Appendix B — approximately 20 reliable-source Number Theory questions

## Required scope

Appendix B should contain approximately **20 externally sourced, reliable Number Theory questions** relevant to the taught guide.

These are **not** to be presented as author-created historical questions.

Prefer, in descending authority where appropriate:

1. official/validated IOQM papers and keys;
2. PRMO/RMO/INMO or other official Olympiad sources appropriate to the level;
3. AMC/AIME or other well-established contest archives when they supply a useful Number Theory mechanism;
4. other stable, independently verifiable contest sources.

Each item must have stable provenance in `Sources_and_Citations.md`, including contest/year/question where known.

## Coverage balance

Across the ~20 questions, cover a representative spread of the guide, including where taught:

- divisibility and Division Algorithm;
- gcd/lcm and Euclidean Algorithm;
- Bézout / linear Diophantine equations;
- congruences and modular inverses;
- CRT;
- residue cycles / Fermat / Euler;
- Wilson;
- Euler phi;
- valuations and factorial divisibility;
- divisor structure / perfect powers;
- digit, place-value, and base methods;
- Pythagorean triples;
- factorization-based Diophantine problems;
- one suitable pigeonhole/extremal Number Theory application.

## Presentation and checking

- Questions first; no solutions interleaved.
- Answer key only after the final Appendix B problem.
- Every answer must be independently recomputed.
- Record theorem hypotheses and source authority in companion QA/source files.
- Do not use a problem merely because an answer key exists; the statement and provenance must also be reliable.

---

# Appendix C — approximately two-page Number Theory helper

Create an approximately **2-page compact helper / memory sheet** for formulas, theorem conditions, and common facts worth memorizing.

This is a memory aid, not a replacement for the study guide and not a place for full worked solutions.

## Required content

Include compact entries for:

### Divisibility / gcd / lcm

- Division Algorithm: `a = bq + r`, `0 <= r < b`;
- Euclidean Algorithm;
- `gcd(a,b) * lcm(a,b) = |ab|`;
- Euclid's Lemma;
- Bézout identity;
- solvability criterion for `ax + by = c`.

### Congruences

- legal addition, subtraction and multiplication of congruences;
- cancellation warning;
- modular inverse condition `gcd(a,m)=1`;
- linear congruence solvability;
- CRT workflow and compatibility reminder.

### Powers modulo n

- short residue-cycle cue;
- Fermat's Little Theorem with prime/coprimality conditions;
- Euler's theorem with `gcd(a,n)=1`;
- Euler phi formulas for prime powers and factorizations;
- Wilson's theorem with prime-modulus condition;
- common order/period reminders.

### Prime factorization / valuations / divisors

For `n = product p_i^{a_i}` include:

- `tau(n) = product (a_i+1)`;
- divisor-sum formula where useful;
- `v_p(ab)=v_p(a)+v_p(b)`;
- `v_p(n!) = floor(n/p)+floor(n/p^2)+...`;
- trailing-zero reminder `min(v_2,v_5)`;
- perfect-square / perfect-kth-power exponent tests;
- lcm/gcd exponent max/min rule.

### Decimal digits / bases

- place-value expansion `(abc)_b = ab^2 + bb + c` written unambiguously with digit symbols;
- digit validity in base `b`;
- digit-sum congruence modulo `9` and `3`;
- last-digit / last-two-digit modulus cues;
- concatenation place-value identities.

### Standard algebraic Number Theory identities

Include a small set of high-value factorizations such as:

- `a^2-b^2`;
- `a^3-b^3`;
- `a^3+b^3`;
- `x^n-y^n` divisibility cues;
- product of consecutive integers and factorial divisibility cue.

### Pythagorean triples

Primitive triple form and conditions:

- `m^2-n^2, 2mn, m^2+n^2`;
- `m>n>0`;
- `gcd(m,n)=1`;
- opposite parity for primitiveness.

### Common decision cues

Very short prompts such as:

- "last digits -> modulus `10^k`";
- "factorial divisibility -> valuations";
- "gcd + lcm -> normalize by gcd";
- "same digit string in two bases -> expand place values";
- "fixed sum of consecutive blocks -> subtract overlapping sums";
- "large exponent -> find a short residue cycle before using a theorem";
- "delete/append digits -> write the place-value equation";
- "square condition -> inspect prime-exponent parity".

## Appendix C quality rule

Every formula/theorem must include the minimum hypotheses needed to use it legally. Do not write bare commands such as "use Euler", "apply CRT", or "Wilson" without the conditions that make the step valid.

---

# Completion gates affected by these requirements

The Number Theory package cannot be declared complete until:

1. Appendix A contains verified/recovered Q1–Q90 exactly once;
2. Appendix B contains ~20 reliable-source Number Theory questions with independent answer verification;
3. Appendix C fits the intended compact-helper role and includes theorem hypotheses;
4. the study guide teaches enough for the supplied Appendix A mechanisms to be executable by the target learner;
5. provenance and uncertainty remain explicit in companion source/QA files.
