# Issue #49 — Wave 1A Interface: Term vs Sum Recognition

`STREAM: W1-A`

`STATUS: PASS_INTERNAL`

This is an interface contract, not student teaching prose.

## 1. CONCEPT_SCOPE

Owns target-object selection before formula selection: `a_n`, `S_n`, block sums, term counts, index shifts, and the reverse relation `a_n=S_n-S_{n-1}` at the boundary with W1-F.

Does not own general AP/GP derivation or telescoping technique.

## 2. PREREQUISITES

- sequence versus series vocabulary;
- indexed notation;
- ordinary addition;
- simple substitution;
- basic AP/GP familiarity.

## 3. LIKELY_HALF_KNOWLEDGE

Learner remembers nth-term and sum formulas but may choose a formula from surface words rather than first deciding whether the requested object is one term or an accumulation. `n-1` and block endpoints are especially unstable.

## 4. RECOGNITION_CUES

- “nth term”, “20th term”, “term at position” -> `a_n`;
- “sum of first n” -> `S_n`;
- “sum from pth through qth term” -> `S_q-S_{p-1}`;
- formula for `S_n` but target asks for a term -> reverse cumulative information.

## 5. FIRST_MOVES

1. Write `TARGET = a_n`, `TARGET = S_n`, or `TARGET = S_q-S_{p-1}`.
2. Only then choose the relevant sequence structure.
3. If `S_n` is supplied and `a_n` is requested, write `a_n=S_n-S_{n-1}`.

## 6. INVARIANT_OR_STRUCTURE

- one term is local information;
- `S_n` is cumulative information;
- adjacent cumulative values differ by exactly one local term;
- moving from term 1 to term n applies the repeated step exactly `n-1` times.

## 7. REPRESENTATION_SWITCHES

- wording -> target symbol;
- list -> indexed term;
- cumulative formula -> difference of partial sums;
- block sum -> endpoint subtraction.

## 8. CONDITION_INDEX_ENDPOINT_CHECKS

- `a_1=S_1`; for `n>=2`, `a_n=S_n-S_{n-1}`;
- block `a_p+...+a_q=S_q-S_{p-1}`;
- count of terms from p through q is `q-p+1`;
- distinguish index n from number of transitions `n-1`.

## 9. DECISION_BOUNDARIES

- `a_20` versus `S_20`;
- nth term from AP data versus nth term reconstructed from `S_n`;
- sum of first q terms versus sum from p through q;
- formula selection after object identification, never before it.

## 10. MISCONCEPTION_TRAPS

- `TERM_SUM_CONFUSION`;
- `INDEX_SHIFT_OFF_BY_ONE`;
- `BLOCK_SUM_ENDPOINT_ERROR`;
- treating the word “first” as a signal for an AP sum formula;
- differentiating/guessing `S_n` instead of differencing it.

## 11. CONTRAST_PAIRS

1. “20th term” -> `a_20`; “sum of first 20 terms” -> `S_20`.
2. “sum of terms 15 through 40” -> `S_40-S_14`, not `S_40-S_15`.
3. Given `a,d` -> direct nth-term route; given `S_n` formula -> reverse by adjacent partial sums.

## 12. TRANSFER_MECHANISMS

- same underlying AP, target changes from term to sum;
- cumulative attendance/score/table data reinterpreted as local increments;
- block accumulation recovered from two checkpoints;
- reverse from a polynomial `S_n` without fitting sample terms.

## 13. SOURCE_CUSTODY

No clean Preliminary anchor is required to justify the foundational object distinction. Deep Sequence & Series authority owns the derivation. `NMTC-BH-P-2018-Q17` may serve only as light POSITION/CHANGE reconnect support, not as major sequence-frequency evidence.

All interface examples below are `AUTHOR_CREATED_FOUNDATION`.

## 14. CANDIDATE_MASTERY_ITEMS

1. AP: `a=5,d=3`. Find `a_20`. Expected `62`.
2. Same AP. Find `S_20`. Expected `670`.
3. `S_n=2n^2+3n`. Find `a_n`. Expected `4n+1`.
4. `S_n=n(n+1)/2`. Find `a_15+...+a_40`. First move `S_40-S_14`; expected `715`.
5. AP with `a_7=20,a_15=44`. Find `S_20`. Expected `610`.

`CANDIDATE_AUDIT: 5/5 independently recomputed — PASS`

## 15. DIAGNOSTIC_TAGS

`TERM_SUM_CONFUSION`, `INDEX_SHIFT_OFF_BY_ONE`, `TERM_COUNT_ERROR`, `BLOCK_SUM_ENDPOINT_ERROR`, `REVERSE_CUMULATIVE_MISSED`, `FORMULA_BEFORE_OBJECT`.

## 16. H3_TO_H0_FADE_PLAN

- H3: explicitly label target and write the correct structural relation.
- H2: ask “one term, cumulative sum, or block sum?”
- H1: point only to the target wording.
- H0: mixed unlabelled prompt; learner must label the object and begin independently.

Progression must include at least one `a_n`/`S_n` contrast and one block endpoint item before H0.

`W1-A_GATE: PASS`