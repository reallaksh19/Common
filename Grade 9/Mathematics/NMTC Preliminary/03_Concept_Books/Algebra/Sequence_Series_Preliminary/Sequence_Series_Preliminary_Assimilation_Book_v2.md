# Sequence & Series Preliminary Overlay — Assimilation Book v2

`ISSUE_AUTHORITY: #49`

`WAVE: 2 — INTEGRATED_ASSIMILATION_BOOK`

`STUDENT_LAYER: YES`

`ANSWERS_INLINE_WITH_ATTEMPTS: NO`

This book is for a learner who remembers much of AP/GP notation and formulas but does not yet choose the right **object, invariant, representation, transform, endpoint or condition** reliably.

The deep chapter remains the derivation authority. This book repairs the missing links needed for Preliminary problem solving.

---

# 0. The governing question

Do not begin a sequence problem by asking:

> Which formula do I remember?

Begin with:

> **What object is the question asking for, and what structure survives after I represent that object correctly?**

Use this spine throughout the unit:

`TARGET OBJECT -> STABLE STRUCTURE -> REPRESENTATION SWITCH -> COLLAPSE -> CHECK -> ORIGINAL OBJECT`

The six deep lenses are:

- `POSITION` — where is the term?
- `CHANGE` — what repeats additively?
- `RATIO` — what repeats multiplicatively?
- `ACCUMULATION` — what is being added?
- `TRANSFORM` — can the variable/representation be changed?
- `REVERSE` — can local information be recovered from cumulative information?

Under Preliminary conditions, the learner must make those choices before calculation.

---

# 1. RECONNECT — attempt before teaching

Attempt these without a formula sheet. Write only the **first useful line** if you cannot finish.

Do not use the hint bank until you have made a genuine attempt.

## D1

The sequence is `4, 7, 10, 13, ...`. The question asks for the 25th term.

What is the target object and first move?

## D2

The same sequence asks for the sum of the first 25 terms.

What changed mathematically?

## D3

`S_n = n(2n+1)`. Find a route to `a_n` without guessing terms from a table.

## D4

Classify the structure of `3, 6, 12, 24, ...`, and state what extra check would be necessary only if an **infinite** sum were requested.

## D5

In a GP, `a_5=48` and `a_8=384`. The target is `a_30/a_27`.

What should be cancelled before solving anything large?

## D6

A sum is written as

`sum_{k=1}^{10} k(3k-1)`.

What should be made visible before any numerical summation?

## D7

`a_1=1` and

`a_{n+1}=a_n/(1+2a_n)`.

What change of variable is suggested by the algebraic shape?

## D8

Evaluate structurally rather than by a common denominator:

`sum_{k=1}^{5} 1/[(k+1)(k+2)]`.

What representation would create cancellation?

## D9

The sequence is

`3, 7, 13, 21, 31, ...`.

It is neither AP nor GP. What should you inspect next?

## D10

A reproduced historical GP question and a provisional answer key imply different mathematics. What is the first mathematical action?

---

# 2. DISCOVER — object first, formula second

The same sequence can generate different mathematical objects.

Consider an AP with first term `5` and common difference `3`.

The twentieth term is one local object:

`a_20 = 5 + 19(3)`.

The sum of the first twenty terms is an accumulation:

`S_20 = 20/2 [2(5)+19(3)]`.

The formulas differ because the objects differ.

## Contrast 1 — `a_n` versus `S_n`

- “20th term” -> one position -> `a_20`.
- “sum of first 20 terms” -> cumulative object -> `S_20`.

The surface sequence is identical. The requested object changes the method.

## Reconnect rule

Before writing any AP/GP relation, label the target:

- `TARGET = a_n`
- `TARGET = S_n`
- `TARGET = S_q-S_{p-1}`
- `TARGET = transformed recurrence state`

That one line prevents many formula-selection errors.

---

# 3. MAKE SENSE — why `n-1` keeps appearing

From term 1 to term 2 there is one change.

From term 1 to term 5 there are four changes.

From term 1 to term `n` there are exactly `n-1` changes.

That is why:

- AP: `a_n=a+(n-1)d`;
- GP: `a_n=ar^(n-1)`.

The `n-1` is not a decorative formula feature. It is the number of transitions between positions.

## Error trigger

If you write `ar^n` for the nth term, ask:

> How many multiplications by `r` occur before I reach the first term?

The answer is zero. Therefore term 1 must contain `r^0`, not `r^1`.

---

# 4. REVERSE — local information from cumulative information

Suppose:

`S_n = 3n^2+2n`.

The nth term is the new amount added when cumulative total `S_{n-1}` becomes `S_n`:

`a_n = S_n-S_{n-1}`.

So:

`a_n = (3n^2+2n)-[3(n-1)^2+2(n-1)]`

which simplifies to a local term rule.

This is not a special trick. It is the discrete version of “new cumulative total minus old cumulative total = latest contribution.”

## Block sums

If the target is:

`a_p+a_{p+1}+...+a_q`,

then everything before `p` must be removed:

`S_q-S_{p-1}`.

## Contrast 2 — direct nth-term route versus reverse-from-sum

- given `a,d` and asked for an AP term -> direct position relation may be best;
- given a formula for `S_n` and asked for `a_n` -> adjacent cumulative difference is exact and immediate.

## Endpoint falsifier

For terms 15 through 40, the block is:

`S_40-S_14`,

not `S_40-S_15`.

Term 15 must remain in the result.

---

# 5. DISCOVER — CHANGE or RATIO?

Do not classify a sequence by how fast its numbers grow.

For

`5, 9, 13, 17, ...`

the first differences are constant:

`4,4,4,...`

so the invariant is additive.

For

`5,10,20,40,...`

the adjacent ratios are constant:

`2,2,2,...`

so the invariant is multiplicative.

## Contrast 3 — AP versus GP

- AP asks whether `a_{n+1}-a_n` is constant;
- GP asks whether `a_{n+1}/a_n` is constant where defined.

Visual growth is not the criterion.

## Normalize before classifying

A sequence such as

`2, 2sqrt(2), 4, 4sqrt(2), ...`

may look irregular if you stare only at decimal size. The adjacent ratio reveals the invariant immediately.

---

# 6. Finite versus infinite GP — same pattern, different admissibility

A finite geometric sum is an algebraic object. It can be evaluated even when `|r|>1`.

For example, the finite GP

`3+6+12+24+48+96`

is perfectly valid.

An infinite GP asks whether the remaining tail shrinks to zero.

Therefore, before using

`S = a/(1-r)`,

write:

`|r|<1`.

For

`2,-1,1/2,-1/4,...`

we have `r=-1/2`, so the alternating signs do not prevent convergence. What matters is `|r|`.

## Contrast 4 — finite versus infinite GP

- finite GP: no convergence condition required;
- infinite GP: tail decay must be justified first.

A formula that is valid for a finite sum cannot be extended to infinity merely because the terms look geometric.

---

# 7. HIGH INDEX — compare before calculating

Suppose a GP satisfies:

`a_3=12`, `a_6=96`.

If the target is `a_20/a_17`, writing two enormous terms separately is wasted work.

From the same GP:

`a_6/a_3 = r^3`.

The target ratio also sees only an index gap:

`a_20/a_17 = r^3`.

The first term and common powers cancel.

## Governing invariant

For selected terms from the same nonzero GP:

`a_p/a_q = r^(p-q)`.

The target may depend only on **index distance**, not on the actual large terms.

## Contrast 5 — absolute target versus relative target

- find `a_40` -> you may need `a` as well as `r`;
- find `a_40/a_35` -> only `r^5` is visible.

## Sign custody

If `r^3=-8`, then the real ratio is `r=-2`.

But if only `r^2=4` is known, the sign is not determined by that relation alone.

Do not invent uniqueness when the exponent parity does not support it.

---

# 8. ACCUMULATION — expose the kth term

A weighted sum is often difficult only because the summand has not been written clearly.

Consider:

`sum_{k=1}^{10} k(2k+1)`.

First expose the summand:

`k(2k+1)=2k^2+k`.

Then use summation linearity:

`sum(2k^2+k)=2sum k^2 + sum k`.

The sequence need not be AP or GP. The correct structure is **polynomial accumulation**.

## Contrast 6 — indexed polynomial versus AP/GP reflex

A formula such as `k(3k+1)` contains an index, but that does not make the resulting list an AP or GP.

The right question is:

> What is the summand, and into which standard pieces can it be split?

---

# 9. Nested sums — count multiplicity instead of expanding everything

Consider:

`sum_{k=1}^{10} sum_{j=1}^{k} 1`.

The inner sum is simply the number of ones being added:

`sum_{j=1}^{k}1 = k`.

So the nested object becomes a single familiar accumulation:

`sum_{k=1}^{10} k`.

For more complicated nested sums, ask:

> How many times does each underlying term appear?

That count is often the real weight.

---

# 10. Weighted geometric sums — align before subtracting

Polynomial weights and geometric weights need different structural moves.

For a finite pattern such as

`1+2·2+3·2^2+4·2^3+5·2^4`,

writing a shifted multiple aligns most geometric powers. Subtraction then reduces the weighted sum to a simpler finite geometric expression plus endpoint terms.

## Contrast 7 — polynomial weight versus geometric weight

- `sum k(2k+1)` -> expand polynomial and split standard sums;
- `sum k2^(k-1)` -> align a shifted geometric copy and subtract.

Do not choose a method from the word “weighted.” Inspect what the weight is multiplying.

---

# 11. TRANSFORM — recurrences are coordinate-choice problems

A recurrence may be hard in `a_n` but easy in another variable.

## 11.1 Reciprocal transform

Suppose:

`a_{n+1}=a_n/(1+a_n)`.

Taking reciprocals gives:

`1/a_{n+1}=1/a_n+1`.

The transformed sequence is now an AP.

The recurrence was nonlinear only in the original coordinate.

## 11.2 Fixed-point shift

Suppose:

`a_{n+1}=2a_n+3`.

Find a value `c` that would stay fixed:

`c=2c+3`.

This gives `c=-3`.

Now define the deviation from that fixed point:

`b_n=a_n+3`.

Then:

`b_{n+1}=2b_n`.

An affine recurrence becomes a GP after shifting the origin.

## Contrast 8 — reciprocal versus fixed-point shift

- fractional denominator structure -> test reciprocal;
- affine `pa_n+q` structure -> test a shift by a fixed point.

A transform is useful only if it simplifies the update rule.

---

# 12. Functional recurrences — navigate the index before deriving a universe

Suppose:

`a_{m+n}=a_m+a_n+2mn`, with `a_1=1`,

and the target is `a_8`.

A closed form is possible, but it is not required.

Use strategic equal indices:

- `(1,1)` reaches `a_2`;
- `(2,2)` reaches `a_4`;
- `(4,4)` reaches `a_8`.

The recurrence becomes an **index-navigation problem**.

## Contrast 9 — strategic indices versus global closed form

If only one target index is needed, the shortest route may be a carefully chosen sequence of substitutions rather than a formula for every `a_n`.

---

# 13. Discovery is not verification

Suppose someone proposes:

`a_n=2^n-1`

for a recurrence.

Substituting the formula into the recurrence and checking the initial condition can prove the proposal is valid.

But that does not explain how the formula was discovered.

Discovery may come from:

- a reciprocal transform;
- a fixed-point shift;
- a difference table;
- pattern recognition;
- strategic recursion;
- another invariant.

## Contrast 10 — discovery versus verification

- transformation/pattern may **discover** a candidate form;
- substitution or induction may **verify** it.

Do not confuse “I proved this formula works” with “I found the structural reason to think of it.”

---

# 14. REVERSE + TRANSFORM — telescoping is endpoint custody

Consider:

`sum_{k=1}^{20} 1/[k(k+1)]`.

Partial fractions give:

`1/[k(k+1)] = 1/k - 1/(k+1)`.

Expand the first few and last few terms:

`(1-1/2)+(1/2-1/3)+...+(1/20-1/21)`.

The middle terms cancel, but the answer is controlled by the two survivors.

This is the key idea:

> **Telescoping is not “everything cancels.” It is “adjacent states cancel, leaving boundary states.”**

## Radical telescope

For

`1/(sqrt(k)+sqrt(k+1))`,

rationalization gives:

`sqrt(k+1)-sqrt(k)`.

Again, the sum becomes a chain of neighboring differences.

## Contrast 11 — recognizing cancellation versus preserving endpoints

A student can correctly notice telescoping and still get the final answer wrong by losing the first or last survivor.

Write the first two and last two expanded terms before collapsing.

---

# 15. FINITE DIFFERENCES — when AP and GP both fail

Consider:

`2,6,12,20,30,...`.

First differences:

`4,6,8,10,...`

Second differences:

`2,2,2,...`

The sequence is not an AP because its **first** differences are not constant.

The constant second difference suggests a quadratic rule.

A candidate is:

`a_n=n(n+1)`.

Now verify that the rule matches the supplied terms and any stated conditions.

## Contrast 12 — constant second difference versus AP

- constant first difference -> AP;
- constant second difference -> quadratic-type signal.

A difference table suggests a degree. It does not excuse verification.

---

# 16. SOURCE QC — mathematical discipline, not clerical cleanup

The 2025 qualified corpus contains a GP-looking question whose reproduced stem compares one pair of term positions while the AMTI provisional key is consistent with a different comparison.

The correct response is not to edit one word until the key works.

Use:

`SOLVE PRINTED MATHEMATICS -> COMPARE WITH KEY -> RECORD CONFLICT -> BLOCK CANONICAL USE`

Disposition for Issue #49:

`NMTC-BH-P-2025-Q30 = SOURCE_CONFLICT_EVIDENCE / SOURCE_KEY_CONFLICT_NOT_CANONICAL`

## Contrast 13 — source conflict versus silent repair

A familiar GP mechanism does not give permission to change a historical stem.

Also distinguish **primary mechanism** from **incidental sequence appearance**. A geometry problem may contain geometric scaling and still remain geometry-primary bridge evidence rather than a clean Sequence-frequency anchor.

---

# 17. DIAGNOSE — error laboratory

For each case, identify the error code and write the repair in one sentence. Do not compute more than necessary.

## E1 — object error

A student sees “first 30 terms” in a sentence asking for the **30th term** and immediately writes an AP sum formula.

## E2 — index shift

A student writes the nth GP term as `ar^n`.

## E3 — surface classification

A student says `3,6,10,15,...` is an AP because the numbers “increase regularly.”

## E4 — convergence omitted

A student writes `S=a/(1-r)` for an infinite GP with `r=3/2`.

## E5 — high-power expansion

A student calculates `a_100` and `a_97` separately even though the target is `a_100/a_97`.

## E6 — weighted-sum reflex

A student tries to find a common difference for terms generated by `k(2k+1)` before evaluating their sum.

## E7 — wrong recurrence transform

For `a_{n+1}=2a_n+3`, a student takes reciprocals and obtains an even more complicated recurrence.

## E8 — discovery/verification confusion

A student substitutes a proposed formula into a recurrence and says, “This is how the formula was discovered.”

## E9 — telescope endpoint loss

After correctly writing `1/[k(k+1)]=1/k-1/(k+1)`, a student says the whole finite sum is zero because “everything cancels.”

## E10 — degree hypothesis unverified

A student sees constant second differences, writes one quadratic-looking expression from the first three terms, and never checks the remaining supplied terms.

## E11 — source silent repair

A student changes a term-position word in a historical question solely because the altered version matches the answer key.

## E12 — primary-domain inflation

A circle problem has radii in a GP. A student counts it automatically as primary Sequence & Series recurrence evidence.

---

# 18. FADE — four support tracks

The support is deliberately reduced from H3 to H0.

Attempt every item before consulting the matching support in the later Hint Bank.

## Track A — object and endpoints

### A-H3

`S_n=2n^2+3n`. Find `a_8`.

Support level: H3.

### A-H2

`S_n=n(n+1)/2`. Find the sum of terms 9 through 20.

Support level: H2.

### A-H1

An AP has `a_5=17` and `a_11=35`. Find `S_20`.

Support level: H1.

### A-H0

`S_n=4n^2-n`. Find `a_15`.

No support.

## Track B — ratio and convergence

### B-H3

Find the infinite sum of `8,-4,2,-1,...` after first checking admissibility.

Support level: H3.

### B-H2

A GP has `a_4=54` and `a_7=1458`. Find `a_50/a_47`.

Support level: H2.

### B-H1

Decide whether `5,-10,20,-40,...` has a finite infinite geometric sum.

Support level: H1.

### B-H0

A GP satisfies `a_12/a_9=-27`. Find `a_40/a_38`.

No support.

## Track C — recurrence transformation

### C-H3

`a_1=1/2`, `a_{n+1}=a_n/(1+3a_n)`. Find `a_8`.

Support level: H3.

### C-H2

`a_1=7`, `a_{n+1}=2a_n-5`. Find `a_8`.

Support level: H2.

### C-H1

`a_{m+n}=a_m+a_n+mn`, `a_1=2`. Find `a_8`.

Support level: H1.

### C-H0

`a_1=3`, `a_{n+1}=3a_n+4`. Find `a_6`.

No support.

## Track D — telescope and finite difference

### D-H3

Evaluate `sum_{k=1}^{12}1/[k(k+1)]`.

Support level: H3.

### D-H2

Evaluate `sum_{k=1}^{15}1/(sqrt(k)+sqrt(k+1))`.

Support level: H2.

### D-H1

Find the 12th term of `4,10,18,28,40,...`.

Support level: H1.

### D-H0

Evaluate

`sum_{k=1}^{10}1/[(3k-2)(3k+1)]`.

No support.

---

# 19. ADOPT — mixed unlabelled first-move and solve set

No method labels. No default hints. For each item, first write the **first useful line**, then solve.

## M1

An AP has `a_6=19` and `a_14=43`. Find `S_20`.

## M2

`S_n=5n^2-2n`. Find `a_17`.

## M3

Find the sum of the first eight terms of

`4,-2,1,-1/2,...`.

## M4

Find the infinite sum, if it exists:

`6,-3,3/2,-3/4,...`.

## M5

A GP satisfies `a_10/a_7=8`. Find `a_50/a_48`.

## M6

A GP satisfies `a_12/a_9=-8`. Find `a_30/a_28`.

## M7

Evaluate

`sum_{k=1}^{12} k(k+2)`.

## M8

Evaluate

`sum_{k=1}^{8} sum_{j=1}^{k}2`.

## M9

`a_1=1`, `a_{n+1}=a_n/(1+4a_n)`. Find `a_10`.

## M10

`a_1=0`, `a_{n+1}=2a_n+6`. Find `a_7`.

## M11

`a_{m+n}=a_m+a_n+3mn`, `a_1=2`. Find `a_8`.

## M12

Evaluate

`sum_{k=1}^{15}1/[k(k+1)]`.

## M13

Evaluate

`sum_{k=4}^{24}1/(sqrt(k)+sqrt(k+1))`.

## M14

Find the 20th term of

`5,12,21,32,45,...`.

## M15

`S_n=n^2+2n`. Find the sum of terms 7 through 18.

## M16

A historical sequence question’s printed relationship and provisional key imply different results. State the correct source disposition and what must **not** be done.

---

# 20. TRANSFER — changed surface, same structure

These are `AUTHOR_CREATED_TRANSFER`, not NMTC PYQs.

## T1 — cumulative rows

A theatre builds rows cumulatively so that the total number of seats after `n` rows is

`S_n=2n^2+n`.

How many seats are added in row 20?

## T2 — measured scale states

A quantity changes by the same multiplicative factor each step. The value at step 10 is 125 times the value at step 7.

Without reconstructing either absolute value, find the ratio of the values at steps 20 and 18.

## T3 — shrinking path

A path is divided into successive lengths

`12,6,3,3/2,...`.

Find the total length if the process continues indefinitely, and justify whether the total is finite.

## T4 — weighted scoring schedule

On day `k`, a learner earns `k(2k+3)` points. Find the total earned in the first 15 days.

## T5 — cumulative score record

A cumulative score after `n` rounds is

`S_n=3n^2+n`.

How many points were earned in round 12?

## T6 — reciprocal update

A normalized concentration obeys

`c_1=1`,

`c_{n+1}=c_n/(1+2c_n)`.

Find `c_10` without iterating decimals.

## T7 — equilibrium shift

A control value obeys

`x_1=30`,

`x_{n+1}=x_n/2+10`.

Find `x_5` by measuring deviation from the equilibrium value.

## T8 — index navigation

A function on positive integers satisfies

`F(m+n)=F(m)+F(n)+mn`,

with `F(1)=1`.

Find `F(8)` using a short index route.

## T9 — non-unit telescope step

Evaluate

`sum_{k=1}^{10}1/[k(k+2)]`.

Do not use a ten-term common denominator.

## T10 — radical block

Evaluate

`sum_{k=9}^{35}1/(sqrt(k)+sqrt(k+1))`.

## T11 — figurate growth

A tile pattern begins

`2,7,14,23,34,...`.

Use finite differences to infer and verify a rule, then find the 25th value.

## T12 — provenance decision

A geometry question creates a sequence of circle radii in constant ratio because of homothety. Classify its Sequence & Series provenance: primary anchor, bridge evidence, or source conflict? Explain the frequency implication.

---

# 21. Hint Bank — consult only after attempting

No final numerical answers are given here.

## Reconnect hints

- D1: H1 — decide whether the target is one term or an accumulation.
- D2: H1 — the underlying sequence did not change; the target object did.
- D3: H2 — compare two neighboring cumulative totals.
- D4: H2 — test ratio; if the word “infinite” appears, test tail decay.
- D5: H2 — divide selected-term equations before finding the first term.
- D6: H2 — write the kth summand as a polynomial in k.
- D7: H2 — ask what happens after taking reciprocals.
- D8: H2 — split the term into a difference of neighbors.
- D9: H2 — build first and second differences.
- D10: H1 — solve the printed mathematics before trusting the key.

## Fade Track A

- A-H3: write `a_n=S_n-S_{n-1}` and substitute `n=8` only after simplifying the general difference.
- A-H2: use cumulative endpoints; the lower subtraction index is one less than the first included term.
- A-H1: recover the AP parameters from the two indexed terms before accumulating.
- A-H0: no hint.

## Fade Track B

- B-H3: first write the common ratio and `|r|<1`.
- B-H2: compare indices 7 and 4 before touching index 50.
- B-H1: the ratio magnitude, not alternating signs, controls convergence.
- B-H0: no hint.

## Fade Track C

- C-H3: set `b_n=1/a_n` and transform the recurrence before substituting the target index.
- C-H2: find the fixed point of the affine recurrence and measure deviation from it.
- C-H1: try equal-index substitutions that double the index.
- C-H0: no hint.

## Fade Track D

- D-H3: use `1/[k(k+1)]=1/k-1/(k+1)` and display the first/last survivors.
- D-H2: rationalize each term before summing.
- D-H1: inspect second differences after first differences fail to stay constant.
- D-H0: no hint.

## ADOPT hints — recognition only

- M1: indexed AP constraints.
- M2: reverse cumulative information.
- M3: finite geometric accumulation.
- M4: convergence before infinite formula.
- M5: compare index gaps.
- M6: preserve the sign of the common ratio.
- M7: expose the polynomial summand.
- M8: collapse the inner count first.
- M9: reciprocal transform.
- M10: fixed-point shift.
- M11: strategic equal indices.
- M12: neighboring-factor telescope.
- M13: rationalize.
- M14: finite differences.
- M15: block sum from cumulative endpoints.
- M16: source conflict, not source repair.

## Transfer hints — H1 only

- T1: local contribution from a cumulative total.
- T2: only index distance is visible.
- T3: convergence of a geometric tail.
- T4: polynomial weighted accumulation.
- T5: adjacent partial sums.
- T6: reciprocal state.
- T7: shift around the equilibrium/fixed point.
- T8: strategic doubling.
- T9: split into a difference two indices apart.
- T10: conjugate difference.
- T11: second differences.
- T12: primary domain versus bridge mechanism.

---

# 22. Source-to-mechanism custody

Historical IDs ground mechanisms without turning this book into a reproduction of historical wording.

## CLEAN_SCORED_ANCHOR

- `NMTC-BH-P-2019-Q29` — functional recurrence / strategic indices;
- `NMTC-BH-P-2023-Q15` — weighted polynomial accumulation;
- `NMTC-BH-P-2023-Q29` — selected/high-index GP cancellation;
- `NMTC-BH-P-2024-Q10` — weighted-square accumulation;
- `NMTC-BH-P-2024-Q11` — reciprocal recurrence transform with telescoping behavior;
- `NMTC-BH-P-2024-Q27` — coupled infinite GP and convergence.

`NMTC-BH-P-2024-Q11` may support both recurrence-transform and telescoping teaching, but it remains one historical item and receives one frequency credit.

## SCORED FOUNDATION SUPPORT

- `NMTC-BH-P-2018-Q17` — consecutive-integer/average symmetry reconnect only; not promoted to a major Sequence anchor.

## BRIDGE_EVIDENCE

- `NMTC-BH-P-2024-Q13` — geometric scaling of circle radii; geometry-primary, no Sequence-frequency inflation.

## SOURCE_CONFLICT_EVIDENCE

- `NMTC-BH-P-2025-Q30` — reproduced term-position wording and provisional key disagree; exact canonical use remains blocked.

No author-created item receives an NMTC historical question ID.

---

# 23. ADOPT rule

Before calculation, train yourself to say one sentence of the form:

> “The target is ___; the stable structure is ___; therefore my first move is ___; before accepting the result I must check ___.”

Examples of checks include:

- index distance;
- number of terms;
- block endpoints;
- ratio domain;
- infinite-GP convergence;
- recurrence initial condition;
- telescope survivors;
- finite-difference verification;
- source wording/key agreement.

The goal is not faster formula recall. The goal is correct structural choice under an unlabelled problem.

`WAVE2_STUDENT_BOOK_STATUS: AUTHORED_PENDING_INDEPENDENT_QA`
