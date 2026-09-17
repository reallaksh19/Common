# W1-G — Prefix Residue & State Reasoning Interface

`ISSUE_AUTHORITY: #47`

`WAVE: 1G`

`STATUS: INTERFACE_COMPLETE`

## 1. CONCEPTS

- prefix sums as cumulative state;
- consecutive block sums as differences of prefix states;
- equal prefix residues ↔ divisible block sum;
- include `S0=0`;
- counting equal-residue pairs;
- build a numeral digit by digit while maintaining current remainder state;
- attainable-score/integer-combination state restrictions;
- canonical representation / balanced-ternary ceiling bridge;
- finite-state compression rather than enumerating all objects.

## 2. PREREQUISITES

- W1-A congruence meaning;
- basic cumulative sums;
- simple counting of pairs;
- place-value update `new value = 10·old + digit`;
- elementary pigeonhole idea for existence arguments where appropriate.

## 3. LIKELY_HALF_KNOWLEDGE

- can add a consecutive block directly but does not introduce prefix sums;
- forgets `S0`, missing blocks beginning with the first term;
- sees equal prefix residues as coincidence rather than the exact divisibility condition;
- counts residue classes rather than pairs of indices inside classes;
- rebuilds every candidate number from scratch instead of updating a remainder state;
- treats high-ceiling representation questions as raw counting before choosing a canonical representation.

## 4. RECOGNITION_CUES

- many consecutive subarray/block sums;
- “some consecutive terms sum to a multiple of m”;
- count divisible consecutive blocks;
- long digit strings with divisibility/state constraints;
- attainable total from repeated allowed score increments;
- high-ceiling “represent using powers” problem where representation choice matters.

## 5. FIRST_MOVES

1. Define prefix sums `S0=0,S1,...`.
2. Reduce each prefix sum modulo `m`.
3. Use block `i+1..j = S_j-S_i`; divisible iff prefix residues match.
4. For digit-state construction, update `r_new ≡ 10r_old + d (modm)`.
5. For high-ceiling representation/counting, identify a canonical state/representation before counting cases.

## 6. INVARIANTS

- every consecutive block sum is a difference of two prefix sums;
- divisibility by `m` depends only on equality of two prefix residues;
- if a residue occurs `c` times among prefix states, it contributes `C(c,2)` divisible blocks;
- digit-by-digit modular state needs only the current residue, not the entire prefix numeral;
- canonical representations remove overcount by giving each object a unique state description.

## 7. REPRESENTATION_SWITCHES

- sequence -> prefix sums -> prefix residues;
- block endpoints `(i,j)` -> equal residue pair;
- growing numeral -> state transition `r -> (10r+d) modm`;
- scoring/attainability condition -> modular state or linear integer combination;
- signed powers of 3 -> balanced ternary coefficients in `{-1,0,1}` for ceiling work.

## 8. LEGALITY / ADMISSIBILITY CONDITIONS

- include `S0=0`;
- count index pairs, not merely distinct residue values;
- ordered endpoint pairs require `i<j`;
- digit-state transitions must preserve leading-zero and allowed-digit rules;
- high-ceiling canonical-representation claims must be justified before using uniqueness;
- ceiling bridges must not be treated as entry prerequisites.

## 9. DECISION_BOUNDARIES

**DB-G1 direct block enumeration vs prefix residues**  
One or two blocks: direct addition may be fine. Many blocks/existence/counting: prefix-state compression dominates.

**DB-G2 residue frequency vs pair count**  
A residue occurring 4 times yields 6 index pairs, not 4 blocks.

**DB-G3 prefix state vs digit state**  
Block-sum problems use cumulative additive state; growing numerals use `10r+d` transitions.

**DB-G4 core state reasoning vs ceiling representation**  
Prefix residues are a core structural bridge; balanced ternary is legitimate Preliminary ceiling evidence but not the first modular lesson.

## 10. MISCONCEPTION_TRAPS

- omitting `S0`;
- comparing terms instead of prefix sums;
- counting classes instead of endpoint pairs;
- forgetting order of endpoints;
- reconstructing full large numerals at every digit step;
- counting representations before proving they are unique/non-overlapping;
- treating a high-ceiling bridge as routine baseline expectation.

## 11. CONTRAST_PAIRS

1. Sum `a3+a4+a5` directly vs count all divisible consecutive blocks through prefix residues.
2. Residue frequency 4 -> `C(4,2)=6`, not 4.
3. Append digit 7 to a number with residue `r`: update `10r+7`, not `r+7`.
4. Ordinary residue state vs balanced ternary canonical representation: related compression idea, different difficulty ceiling.

## 12. TRANSFER_MECHANISMS

- existence proof: among sufficiently many prefix residues, two match;
- exact count of divisible blocks from residue-frequency table;
- digit-by-digit divisibility automaton for allowed digits;
- attainable-score impossibility by residue state before enumeration;
- representation counting only after a uniqueness/canonical-form argument.

## 13. SOURCE_IDS_AND_DISPOSITIONS

Clean scored ceiling/transfer anchors:
- `NMTC-BH-P-2019-Q06` — divisible consecutive blocks via equal prefix residues;
- `NMTC-BH-P-2019-Q14` — attainable totals via congruence restrictions;
- `NMTC-BH-P-2019-Q28` — balanced ternary/canonical representation.

Dispositions:
- Q06 = `CLEAN_SCORED_CEILING_BRIDGE`;
- Q14 = `CLEAN_SCORED_TRANSFER_BRIDGE`;
- Q28 = `CLEAN_SCORED_CEILING_BRIDGE`.

Digit-by-digit prefix-residue state exercises are mainly `AUTHOR_CREATED_FOUNDATION/TRANSFER` in this unit.

## 14. CANDIDATE_MASTERY_ITEMS

`G-M1` For sequence `2,5,4,7`, list prefix sums including `S0` and count consecutive blocks divisible by 3 using residues.

`G-M2` Prefix residues modulo 5 are `0,2,0,3,2,0`. Count divisible consecutive blocks.

`G-M3` A current decimal prefix has remainder 4 modulo 7. After appending digit 6, what is the new remainder?

`G-M4` Explain why among 12 integers, there exists a nonempty consecutive block whose sum is divisible by 11 when considering the 12 prefix sums plus `S0` appropriately.

`G-M5` Give the first state-based step for counting 4-digit numbers formed from digits `{1,3,7}` that are divisible by 5, and explain whether state DP is even necessary.

Independent check:
- G-M1: prefixes `0,2,7,11,18`; residues mod3 `0,2,1,2,0`; equal-pair counts: residue0 twice ->1, residue2 twice ->1, total 2 divisible blocks;
- G-M2: residue0 occurs 3 ->3 pairs; residue2 occurs2 ->1; total 4;
- G-M3: `10·4+6=46≡4 (mod7)`;
- G-M4: 12 nonzero prefix sums plus `S0` give 13 states among 11 residues; a repeated residue yields a divisible block (or a prefix residue 0 directly); 
- G-M5: divisibility by5 requires final digit 0 or5, neither allowed; answer count 0, so full state DP is inferior/unnecessary. This is a method-choice contrast.

## 15. DIAGNOSTIC_TAGS

- `S0_OMITTED`
- `BLOCK_NOT_PREFIX_DIFFERENCE`
- `RESIDUE_CLASS_NOT_PAIR_COUNT`
- `ENDPOINT_ORDER_IGNORED`
- `DIGIT_STATE_UPDATE_WRONG`
- `STATE_METHOD_OVERUSED`
- `CANONICAL_REPRESENTATION_UNPROVED`
- `CEILING_BRIDGE_PROMOTED_TO_CORE`

## 16. H3_TO_H0_FADE_PLAN

- `G-F1 H3`: supply prefix sums and ask learner to group equal residues.
- `G-F2 H2`: cue “block sum = difference of two prefix sums; include S0.”
- `G-F3 H1`: point only to “many consecutive blocks / build digit by digit.”
- `G-F4 H0`: mixed state problem where learner must decide whether prefix residues, digit-state update, simple divisibility, or no state machinery is the best first move.

`W1-G_GATE: PASS`