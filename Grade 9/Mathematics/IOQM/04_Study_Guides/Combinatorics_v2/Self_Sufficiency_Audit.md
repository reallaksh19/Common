# Combinatorics Study Guide v2 — Self-Sufficiency Audit

## Executive verdict

### Ground reality 1 — Can a student answer all 56 after reading the old guide?

**No guarantee, and the first version was not sufficiently self-contained for that claim.** It usually pointed to the correct family of methods, but several advanced moves were only named. A Grade 9 student with roughly half the background could still face an orphan trick.

Examples of v1 gaps included derangements (Q9), labeled cycle decompositions (Q34), bounded generating-function coefficient extraction (Q22), exact-adjacency counting (Q41), alternating-permutation enumeration (Q13/Q15), first-stable-prefix recurrence (Q14), and necklace/reflection symmetry (Q51).

### Ground reality 2 — What is the v2 claim?

`STATIC_CONTENT_SELF_SUFFICIENCY = PASS_56_OF_56` means every Appendix A question now maps to a method that is explicitly explained in the guide, with a recognition cue and either a worked example, derivation or executable counting recipe.

This is **not** a claim that every student will solve every question after one reading. Classroom timing, retention, problem-selection judgment under pressure and empirical success rate remain `NOT_RUN`.

### Ground reality 3 — Does the grouping suit a student with about 50% prior knowledge?

Yes as a static curriculum design. The sequence is now dependency-based rather than question-lot-based:

1. counting foundations;
2. unordered selection and logic;
3. distributions and bounded multiplicities;
4. linear arrangements;
5. relative order and rank;
6. circular symmetry;
7. graphs and colorings;
8. recurrences and state;
9. number-theoretic counting;
10. pigeonhole/extremal;
11. invariants/games.

The last two sections are included because they are part of the existing Grade 9 IOQM combinatorics architecture even though the attached Q1–Q56 set does not exercise them strongly.

## Audit standard

A question passes this static self-sufficiency audit only if the guide provides:

- a prerequisite refresh at the level expected of a half-prepared Grade 9 student;
- a way to recognize the method from the surface wording;
- the first useful mathematical step;
- enough explanation to execute the method without needing an unnamed trick;
- a common-error or legality check;
- no answer leakage in the question appendix.

## Appendix A question-to-method audit

| Q | Guide section | Required method | v1 issue / v2 disposition | v2 |
|---:|---|---|---|---|
| Q1 | Relative order & rank | forced small/large pairing; most restricted first | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q2 | Graphs & colorings | unordered pairs; complement | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q3 | Counting foundations | subset complement | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q4 | Counting foundations | digit complement; leading digit | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q5 | Relative order & rank | arithmetic progression with fixed sum | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q6 | Distributions & multisets | block-count parameter; conservation; binomial sum | v1 gap: only named one-parameter idea; no full bridge; v2 explicitly repairs it | PASS |
| Q7 | Relative order & rank | reduce algebraic intersection to sign/order condition | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q8 | Graphs & colorings | small-grid coloring by opposite cells | v1 gap: no complete small-grid counting example; v2 explicitly repairs it | PASS |
| Q9 | Linear arrangements | family labels + derangement + identity restoration | v1 gap: derangements not taught; v2 explicitly repairs it | PASS |
| Q10 | Distributions & multisets | positive exponent stars and bars | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q11 | Distributions & multisets | lower-bound stars and bars | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q12 | Recurrences & states | change encoding + Fibonacci recurrence | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q13 | Relative order & rank | alternating relative-order patterns + leading zero | v1 gap: alternating pattern count not developed; v2 explicitly repairs it | PASS |
| Q14 | Recurrences & states | first stable prefix recurrence | v1 gap: recurrence idea stated but not sufficiently worked; v2 explicitly repairs it | PASS |
| Q15 | Relative order & rank | alternating comparison signs; peak counting | v1 gap: alternating pattern enumeration not developed; v2 explicitly repairs it | PASS |
| Q16 | Recurrences & states | consecutive-ratio substitution | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q17 | Selections & logical restrictions | exactly one from each forbidden pair | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q18 | Selections & logical restrictions | conditional committee case split | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q19 | Circular symmetry | directional circular neighbors | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q20 | Circular symmetry | circular gap selection with spacing cap | v1 gap: gap spacing restriction only named; v2 explicitly repairs it | PASS |
| Q21 | Circular symmetry | circular complement + gaps | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q22 | Distributions & multisets | bounded multiset selection / generating function | v1 gap: bounded coefficient extraction not worked; v2 explicitly repairs it | PASS |
| Q23 | Selections & logical restrictions | together-or-neither + forbidden pair | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q24 | Counting foundations | independent category selections | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q25 | Linear arrangements | independent precedence pairs | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q26 | Number-theoretic counting | divisor count + square factor-pair correction | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q27 | Number-theoretic counting | product of divisors + valuations | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q28 | Counting foundations | two-set inclusion–exclusion | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q29 | Number-theoretic counting | prime-exponent grid boundary | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q30 | Linear arrangements | repeated-letter adjacency inclusion–exclusion | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q31 | Linear arrangements | overlapping/chained adjacency blocks | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q32 | Linear arrangements | category adjacency inclusion–exclusion | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q33 | Graphs & colorings | perfect matching in symmetric allowed graph | v1 gap: matching strategy too generic; v2 explicitly repairs it | PASS |
| Q34 | Graphs & colorings | degree-2 graph → cycle decomposition + labeled cycle count | v1 gap: labeled cycle count missing; v2 explicitly repairs it | PASS |
| Q35 | Linear arrangements | gap method with repeated letters | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q36 | Linear arrangements | two repeated adjacency restrictions | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q37 | Linear arrangements | complement via color blocks | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q38 | Number-theoretic counting | digit residues modulo 3 | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q39 | Distributions & multisets | multiplicity-pattern classification | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q40 | Linear arrangements | ordered positions with limited repeats | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q41 | Linear arrangements | exact adjacency events | v1 gap: exact-adjacency subtraction only sketched; v2 explicitly repairs it | PASS |
| Q42 | Linear arrangements | fixed-separation position patterns | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q43 | Relative order & rank | dictionary rank, distinct letters | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q44 | Relative order & rank | fixed leading digit + repeated-pair case split | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q45 | Relative order & rank | dictionary rank with repeated letters | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q46 | Circular symmetry | numbered circular seats; rotations distinct | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q47 | Circular symmetry | mixed circular vs labeled table symmetry | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q48 | Circular symmetry | forced local block in a circle | v1 gap: forced local circular block missing; v2 explicitly repairs it | PASS |
| Q49 | Graphs & colorings | proper coloring of a cycle | v1 gap: formula given with little derivation; v2 explicitly repairs it | PASS |
| Q50 | Circular symmetry | circular multiset; orbit-size check | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q51 | Circular symmetry | garland/bracelet rotation+reflection via gap patterns | v1 gap: reflection/necklace treatment too brief; v2 explicitly repairs it | PASS |
| Q52 | Circular symmetry | circular empty chairs; fix reference person | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q53 | Circular symmetry | cube rotation group | v1 had basic coverage; v2 deepens explanation/checks | PASS |
| Q54 | Counting foundations | condition on subset size | v1 gap: self-referential subset-size method missing; v2 explicitly repairs it | PASS |
| Q55 | Distributions & multisets | multiplicity patterns under distinct-letter cap | v1 gap: multiplicity-pattern case audit too brief; v2 explicitly repairs it | PASS |
| Q56 | Counting foundations | independent nonempty subset choices | v1 had basic coverage; v2 deepens explanation/checks | PASS |

## Appendix B audit

Appendix B contains 20 author-created IOQM-style mock questions. They are not represented as official past-year questions. They deliberately test the guide without telling the student which chapter to use.

Coverage:

- B1: complement and leading digit;
- B2: committee logic;
- B3: lower-bound stars and bars;
- B4: bounded multiplicity selection;
- B5: adjacency inclusion–exclusion;
- B6: derangement;
- B7: gap method;
- B8: alternating relative order;
- B9: dictionary rank with repeated letters;
- B10: circular gap method;
- B11: bracelet rotation/reflection;
- B12: restricted perfect matching;
- B13: degree-2 labeled graph / cycle decomposition;
- B14: cycle coloring;
- B15: no-adjacent-1 recurrence;
- B16: reverse-state search;
- B17: divisor product and valuations;
- B18: digit residues modulo 3;
- B19: pigeonhole;
- B20: winning positions / modular invariant.

All 20 answers were independently recomputed during authoring. Static answer audit: `PASS_20_OF_20`.

## What remains unproven

- whether one reading is enough for a particular student;
- median time required per chapter;
- retention after one week or one month;
- success rate on a fresh unseen IOQM paper;
- psychometric difficulty calibration.

Those require classroom or learner evidence and should not be inferred from document completeness.
