# IOQM Grade 9 — Combinatorics Study Guide

## What this guide is for

Combinatorics is the art of counting **without listing everything**. The hard part is rarely the arithmetic. The hard part is deciding what one object is, what makes two outcomes different, and which restriction should be handled first.

This guide is written as a teacher would teach the subject at the board: one idea at a time, with a reason for each formula, short worked examples, common mistakes, and a clear first step to try.

The attached Q1–Q56 compilation is used here as a practice source and as a source of useful problem-solving cues. It is **not treated as an official IOQM syllabus or as source authority**. The attachment itself says its question numbers are study-compilation numbers rather than confirmed lecture numbering. Appendix A reproduces all 56 attached questions as a clean practice set. The worked solutions and source notes from the attachment are deliberately omitted; the answer key appears only at the very end of Appendix A.

The Grade 9 Quadratics benchmark is used only as a quality reference: this guide aims for the same clarity of explanation, strong contrasts between similar methods, and independence in starting unfamiliar problems. It does not copy the benchmark's wording or layout.

## How to use this guide

For each subtopic:

1. Read the explanation and the worked teacher example.
2. Cover the example and reproduce the first two lines yourself.
3. Do the suggested Appendix A questions **without looking at the answer key**.
4. If stuck, return to the section titled **What should I notice?**
5. Only after a full attempt, check the answer at the end of Appendix A.

A good combinatorics solution should answer four questions:

- **What exactly am I counting?**
- **Does order matter?**
- **Are my cases disjoint?**
- **Have I counted every valid object exactly once?**

## Subtopic study sequence

1. [Counting basics: stages, cases and complements](01_Counting_Basics_Complements.md)
2. [Restricted selections and committees](02_Restricted_Selections_Committees.md)
3. [Distributions, binomial counts and multiset selections](03_Distributions_Multisets.md)
4. [Linear arrangements, blocks and adjacency](04_Linear_Arrangements_Adjacency.md)
5. [Order patterns, inequalities and dictionary rank](05_Order_Patterns_Dictionary_Rank.md)
6. [Circular arrangements and symmetry](06_Circular_Arrangements_Symmetry.md)
7. [Graphs, matchings and colourings](07_Graphs_Matchings_Colourings.md)
8. [Recurrences and state encodings](08_Recurrences_State_Encodings.md)
9. [Number-theoretic counting and divisibility](09_Number_Theoretic_Counting.md)
10. [Appendix A — Attached Q1–Q56 practice set](Appendix_A_Q1-Q56.md)

---

# A teacher's decision guide

When you read a new problem, do not ask, “Which formula is this?” Ask the following in order.

## Step 1: Name one counted object

Is it a:

- subset?
- committee?
- string?
- seating?
- pairing?
- graph?
- coloring?
- divisor?
- distribution of identical objects?

## Step 2: Decide whether order matters

Compare:

- choose 4 students for a team → unordered;
- choose president, vice-president, secretary, treasurer → ordered roles;
- select 5 letters from a word → unordered multiplicities;
- form a 5-letter word → ordered.

## Step 3: Locate the strongest restriction

A strong restriction is usually one that sharply reduces the next choice. Examples include a forced leading digit, a person whose membership triggers two conditions, the largest “small” number in a constrained pairing, a specified person around a circle, a repeated letter that must be a block, or a divisibility condition on the final digit.

Handle that restriction early.

## Step 4: Ask whether the complement is shorter

Typical triggers:

- at least one;
- not all;
- some pair adjacent;
- some color missing;
- at least one condition fails.

## Step 5: Ask whether the problem naturally splits

Good cases are exhaustive, mutually exclusive, and easy to count individually. If two cases overlap, either repair the split or use inclusion–exclusion.

## Step 6: Check for a hidden representation

- people knowing each other → graph;
- paired people → matching;
- no adjacent colors → graph coloring;
- repeated local string restrictions → state/recurrence;
- divisor conditions → prime-exponent choices;
- circular separation → gaps;
- repeated letters → multiset permutations.

## Step 7: Check symmetry only after the raw count is correct

Ask exactly what the problem considers identical: rotation, reflection, neither, both, or numbered seats. Never divide by a symmetry factor merely because the picture is circular.

---

# Common mistakes to eliminate

1. **Selection versus arrangement.** \(\binom nr\) is unordered; \({}^nP_r\) is ordered.
2. **Overlapping cases.** If one object can lie in two cases, simple addition overcounts.
3. **Leading zero.** A digit allowed internally may be forbidden in the first position.
4. **Identical copies.** Swapping identical letters does not make a new arrangement.
5. **Automatic circular division.** Do not divide by \(n\) when seats are labeled or rotations count as different.
6. **Forgotten wrap-around.** In a circle, the final listed position is adjacent to the first.
7. **Reversed “only if.”** “A only if B” means \(A\Rightarrow B\).
8. **Unnecessary inclusion–exclusion.** If a restriction can be built directly into the construction, do that.
9. **Unproved recurrence.** Every recurrence term must correspond to a disjoint family of objects.
10. **Unchecked symmetry.** First decide what counts as the same object; only then divide by rotations/reflections.

---

# Formula sheet with meaning

| Situation | Formula / idea | Meaning |
|---|---|---|
| \(r\) ordered choices from \(n\) distinct objects | \({}^nP_r=\frac{n!}{(n-r)!}\) | order matters |
| choose \(r\) from \(n\) | \(\binom nr\) | order does not matter |
| repeated objects \(m_1,m_2,\ldots\) | \(\frac{n!}{m_1!m_2!\cdots}\) | identical swaps do not create new objects |
| nonnegative \(x_1+\cdots+x_r=n\) | \(\binom{n+r-1}{r-1}\) | stars and bars |
| positive \(x_1+\cdots+x_r=n\) | \(\binom{n-1}{r-1}\) | give 1 to each first |
| all minus none | complement | useful for “at least one” |
| overlapping bad events | inclusion–exclusion | corrects double counting |
| \(n\) distinct people around unlabeled circle | \((n-1)!\) | rotations identified |
| degree sum | \(\sum d(v)=2|E|\) | every edge has two ends |
| cycle coloring | \((q-1)^n+(-1)^n(q-1)\) | proper \(q\)-colorings of \(C_n\) |
| divisor count | \(\tau(\prod p_i^{a_i})=\prod(a_i+1)\) | choose prime exponents independently |
| no-adjacent-1 binary strings | Fibonacci recurrence | split by final digit |
| distinct cube-face colors up to rotation | \(6!/24\) | 24 cube rotations |

The formula sheet is a reminder, not a substitute for deciding what is being counted.

---

# Appendix A practice map

The 56 attached questions are grouped below by the main idea that should be tried first. Some questions naturally connect to more than one topic; each is placed once here so that the full set is covered without duplication.

| Subtopic | Appendix questions |
|---|---|
| Counting basics: stages, cases and complements | Q3, Q4, Q24, Q28, Q54, Q56 |
| Restricted selections and committees | Q17, Q18, Q23 |
| Distributions, binomial counts and multiset selections | Q6, Q10, Q11, Q22, Q39, Q55 |
| Linear arrangements, blocks and adjacency | Q9, Q25, Q30, Q31, Q32, Q35, Q36, Q37, Q40, Q41, Q42 |
| Order patterns, inequalities and dictionary rank | Q1, Q5, Q7, Q13, Q15, Q43, Q44, Q45 |
| Circular arrangements and symmetry | Q19, Q20, Q21, Q46, Q47, Q48, Q50, Q51, Q52, Q53 |
| Graphs, matchings and colourings | Q2, Q8, Q33, Q34, Q49 |
| Recurrences and state encodings | Q12, Q14, Q16 |
| Number-theoretic counting and divisibility | Q26, Q27, Q29, Q38 |

The full question set is in [`Appendix_A_Q1-Q56.md`](Appendix_A_Q1-Q56.md).