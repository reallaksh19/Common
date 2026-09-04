# Combinatorics v3 — Question-to-Method Priority Matrix

## Purpose

This matrix turns the existing v2 `PASS_56_OF_56` method audit into a student-routing artifact for a learner with roughly 30–50% prior knowledge and about three days remaining.

It does **not** replace the v2 source/answer custody. It adds:

- stable skill IDs;
- three-day priority;
- adaptive hint depth;
- likely failure stage (`R/M/S/E/C`);
- visual obligation where a schematic materially lowers cognitive load.

`PriorityScore` is a curriculum-design heuristic, not a psychometric difficulty score and not official IOQM weightage. The reviewer model is `3T + 2F + 2D + R`; the score proposes and curriculum review confirms. Raw worksheet duplication is not counted as frequency evidence.

Hint notation in this QA file:

- `N` = Notice;
- `N+R` = Notice + Recall;
- `N+R+S` = Notice + Recall + Start.

Student-facing PDF text should spell out the words rather than show internal codes.

## Q1–Q56 matrix

| Q | Stable skill | Required method | Score | 72h priority | Hint | Likely fail | Useful visual |
|---:|---|---|---:|---|---|---|---|
| 1 | `COMB-ORDER-01` | forced small/large pairing; most-restricted-first | 10 | SHOULD | N+R | R/E | pairing sketch |
| 2 | `COMB-PAIR-01`, `COMB-COMP-01` | unordered pairs; complement | 13 | **MUST** | N | R/C | small graph optional |
| 3 | `COMB-COMP-01` | subset complement | 14 | **MUST** | N | R | none |
| 4 | `COMB-COMP-01`, `COMB-COUNT-01` | digit complement; leading-digit handling | 14 | **MUST** | N+R | R/C | digit-position strip |
| 5 | `COMB-AP-01` | arithmetic progression with fixed total | 5 | IF TIME | N+R | R/E | none |
| 6 | `COMB-CONS-01` | one parameter controls blocks; conservation; binomial sum | 10 | SHOULD | N+R+S | S/E | 3-block table |
| 7 | `COMB-ALG-01` | reduce parabola intersection to sign/order condition | 5 | IF TIME | N+R | R/E | sign/order sketch |
| 8 | `COMB-COLOR-01` | 2x2 colouring via opposite nonadjacent cells | 13 | **MUST** | N+R+S | R/S | 2x2 conflict graph |
| 9 | `COMB-DER-01` | family labels -> derangement -> restore identities | 13 | **MUST** | N+R+S | R/E | seat/family mapping |
| 10 | `COMB-SB-01` | positive exponents as stars and bars | 10 | SHOULD | N+R | R/S | exponent boxes |
| 11 | `COMB-SB-01` | lower-bound stars and bars | 15 | **MUST** | N | R/S | bars sketch optional |
| 12 | `COMB-ENC-01`, `COMB-REC-01` | encode symbol changes; Fibonacci-type recurrence | 14 | **MUST** | N+R+S | R/E | state/change diagram |
| 13 | `COMB-ALT-01` | alternating relative-order patterns + leading zero | 5 | IF TIME | N+R+S | R/E | comparison arrows |
| 14 | `COMB-REC-01` | first stable prefix recurrence | 10 | SHOULD | N+R+S | S/E | prefix decomposition |
| 15 | `COMB-ALT-01` | no monotone triple -> alternating comparisons / peak count | 10 | SHOULD | N+R+S | R/E | up-down arrows |
| 16 | `COMB-RATIO-01` | consecutive-ratio substitution in nonlinear recurrence | 4 | IF TIME | N+R+S | R/E | ratio chain |
| 17 | `COMB-PAIRRULE-01` | exactly one from each forbidden pair | 14 | **MUST** | N | R | pair icons |
| 18 | `COMB-LOGIC-01` | conditional committee case split | 15 | **MUST** | N+R | R/E | implication mini-diagram |
| 19 | `COMB-CIRC-01` | directional neighbours around a circle | 10 | SHOULD | N+R | R/C | circle with arrows |
| 20 | `COMB-CIRC-02` | circular gaps + extra spacing cap | 13 | **MUST** | N+R+S | S/E | circular gap pattern |
| 21 | `COMB-CIRC-02`, `COMB-COMP-01` | circular complement + gaps | 10 | SHOULD | N+R | R/E | circle/gaps |
| 22 | `COMB-MULTI-01` | bounded multiset selection / generating polynomial | 13 | **MUST** | N+R+S | R/E | copy-count table |
| 23 | `COMB-PAIRRULE-01`, `COMB-LOGIC-01` | together-or-neither + forbidden pair | 10 | SHOULD | N | R/E | case split |
| 24 | `COMB-COUNT-01` | independent nonempty category selections | 10 | SHOULD | N | R/C | product boxes |
| 25 | `COMB-ORDER-01` | independent precedence pairs | 10 | SHOULD | N+R | R/C | precedence arrows |
| 26 | `COMB-DIV-01` | divisor count + square factor-pair correction | 8 | SHOULD | N | R/C | factor-pair mirror |
| 27 | `COMB-DIV-01` | product of divisors + valuations | 9 | SHOULD | N+R | R/E | valuation table |
| 28 | `COMB-IE-01` | two-set inclusion–exclusion | 15 | **MUST** | N | R/C | Venn optional |
| 29 | `COMB-DIV-01` | prime-exponent grid boundary | 5 | IF TIME | N+R | R/E | exponent grid |
| 30 | `COMB-ADJ-01` | repeated-letter adjacency inclusion–exclusion | 10 | SHOULD | N+R+S | S/E | block diagram |
| 31 | `COMB-ADJ-01` | overlapping/chained adjacency blocks | 14 | **MUST** | N+R+S | R/E | chained blocks |
| 32 | `COMB-ADJ-01` | category adjacency inclusion–exclusion | 10 | SHOULD | N+R | R/E | bad-event blocks |
| 33 | `COMB-MATCH-01` | perfect matching in a symmetric allowed graph | 13 | **MUST** | N+R+S | R/E | allowed-edge graph |
| 34 | `COMB-CYCLE-01` | degree 2 -> cycle decomposition + labeled cycle count | 13 | **MUST** | N+R+S | R/E | cycle partition diagram |
| 35 | `COMB-GAP-01`, `COMB-PERM-01` | gap method with repeated letters | 14 | **MUST** | N | R/C | gap strip |
| 36 | `COMB-ADJ-01` | two repeated adjacency restrictions | 10 | SHOULD | N+R | R/E | two bad blocks |
| 37 | `COMB-COMP-01`, `COMB-BLOCK-01` | complement via colour blocks | 9 | SHOULD | N+R | R/C | colour blocks |
| 38 | `COMB-RES-01` | digit residues modulo 3 | 13 | **MUST** | N | R/E | residue-choice table |
| 39 | `COMB-MULTI-02` | multiplicity-pattern classification | 10 | SHOULD | N+R | R/E | partition-of-4 list |
| 40 | `COMB-PERM-01` | ordered positions with limited repeats | 5 | IF TIME | N | R/E | none |
| 41 | `COMB-ADJ-02` | exactly two adjacency events | 13 | **MUST** | N+R+S | R/E | event/block schematic |
| 42 | `COMB-POS-01` | fixed-separation position patterns | 5 | IF TIME | N+R | R/E | seat-position strip |
| 43 | `COMB-RANK-01` | dictionary rank, distinct letters | 9 | SHOULD | N | S/E | rank table |
| 44 | `COMB-MULTI-02` | fixed leading digit + exactly one repeated pair | 5 | IF TIME | N+R | R/E | `2+1+1` pattern |
| 45 | `COMB-RANK-02` | dictionary rank with repeated letters | 9 | SHOULD | N+R+S | S/E | suffix-count table |
| 46 | `COMB-CIRC-01`, `COMB-IDENT-01` | numbered circular seats; rotations distinct | 13 | **MUST** | N | R/C | labeled-seat circle |
| 47 | `COMB-CIRC-01`, `COMB-IDENT-01` | round-table vs labeled-table identity | 5 | IF TIME | N+R | R/C | two-table sketch |
| 48 | `COMB-CIRC-03` | forced local block in a circle | 9 | SHOULD | N+R+S | R/E | local circular block |
| 49 | `COMB-COLOR-01` | proper colouring of a cycle | 14 | **MUST** | N | R/C | 5-cycle |
| 50 | `COMB-SYM-01` | circular multiset; orbit-size check | 9 | SHOULD | N+R | R/C | rotation orbit |
| 51 | `COMB-SYM-02` | garland rotation/reflection via gap patterns | 8 | SHOULD | N+R+S | R/E | bracelet gap patterns |
| 52 | `COMB-CIRC-02` | circular empty chairs; fix reference person | 9 | SHOULD | N+R | R/E | 13-chair circle |
| 53 | `COMB-SYM-03` | cube rotation group | 4 | IF TIME | N | R/C | cube orientation |
| 54 | `COMB-SIZE-01`, `COMB-COMP-01` | condition on subset size | 13 | **MUST** | N+R | R/S | size-conditioned table |
| 55 | `COMB-MULTI-02` | multiplicity patterns under distinct-letter cap | 8 | SHOULD | N+R+S | R/E | pattern tree |
| 56 | `COMB-COUNT-01`, `COMB-COMP-01` | independent nonempty choices by colour | 14 | **MUST** | N | R/C | product boxes |

## Priority totals

- Appendix A **MUST**: 22
- Appendix A **SHOULD**: 24
- Appendix A **IF TIME**: 10
- Wider-curriculum MUST transfer items: Appendix B **B19 pigeonhole** and **B20 winning positions/invariant**
- Maximum three-day core practice route: **24 items**, before removing skills already Green.

The presence of B19/B20 is intentional: the supplied Q1–Q56 corpus under-exercises pigeonhole/extremal and invariants/games even though they belong to the wider Grade 9 IOQM Combinatorics architecture.

## Hint-depth totals

- Notice only: 16
- Notice + Recall: 21
- Notice + Recall + Start: 19

These are starting assignments. Learner evidence may justify lowering or raising individual support, but a harder question does not automatically deserve higher three-day priority.

## Visual obligations

The following are strong candidates for actual figures in the rebuilt PDF rather than prose-only explanations:

- Q6: three labeled blocks with conserved A/B/C counts;
- Q8: 2x2 conflict graph emphasizing opposite cells;
- Q9: seat/family-position mapping;
- Q12: change encoding / state evolution;
- Q14: unique first-stable-prefix decomposition;
- Q20: circular gaps plus forbidden spacing pattern;
- Q31: separate blocks versus chained blocks;
- Q33: allowed-edge matching graph;
- Q34: cycle-size decompositions of a degree-2 graph;
- Q41: exact-adjacency event/block schematic;
- Q46: numbered seats showing rotations are distinct;
- Q49: 5-cycle colouring closure;
- Q51: rotation/reflection gap patterns;
- Q52: empty-chair circular gap model.

A visual is not required merely because a row lists one. It must survive the final visual-pedagogy audit and materially lower cognitive load.

## Acceptance status for this matrix

```text
QUESTION_INVENTORY = PASS_56_OF_56
QUESTION_TO_STABLE_SKILL = PASS_56_OF_56
THREE_DAY_PRIORITY_ASSIGNED = PASS_56_OF_56
INITIAL_HINT_DEPTH_ASSIGNED = PASS_56_OF_56
LIKELY_FAILURE_STAGE_ASSIGNED = PASS_56_OF_56
```

This is a static design audit. It does not claim calibrated difficulty, solve probability, classroom timing, or retention.