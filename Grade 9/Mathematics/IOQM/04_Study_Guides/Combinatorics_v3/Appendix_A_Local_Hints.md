# Combinatorics v3 — Appendix A Local Hint Overlay

## Student instruction

Try the problem first.

- Read **Notice** only if you cannot identify the structure.
- Read **Recall** only if you recognize the topic but cannot retrieve the earlier method.
- Read **Start** only if you still cannot write the first useful mathematical move.

On a later, non-identical problem, use **less** help. The final target is no hint.

These hints are deliberately incomplete. They do not contain final numerical answers.

---

## Q1 — Pairing the integers 1 through 16

**Notice** — The largest numbers have many possible partners; the smallest numbers are much more restricted. Start with the hardest-to-pair small number, not with an arbitrary pair.

**Recall · Most-restricted-first — `COMB-ORDER-01`** — In a pairing problem, fixing the element with the fewest legal partners can force the remaining structure.

---

## Q2 — Hugs and handshakes

**Notice** — A handshake is an **unordered pair**. It may be shorter to count all pairs of people and remove the pairs that hug instead.

---

## Q3 — Subsets containing a prime

**Notice** — “At least one prime” is a complement trigger: count all subsets, then subtract subsets containing no prime.

---

## Q4 — Four-digit integers containing 2 or 3

**Notice** — “At least one digit is 2 or 3” suggests complement, but the first digit has a different legal set because it cannot be zero.

**Recall · Complement counting — `COMB-COMP-01`** — Count four-digit numbers with **neither** 2 nor 3; handle the leading digit separately from the remaining positions.

---

## Q5 — Integer angles in arithmetic progression

**Notice** — Three angles in an arithmetic progression are best written symmetrically around their middle angle.

**Recall · AP with fixed total — `COMB-AP-01`** — Write the angles as `60-d, 60, 60+d`; then apply positivity, distinctness and triangle-similarity considerations.

---

## Q6 — Restricted arrangements of five A’s, B’s and C’s

**Notice** — The three blocks have complementary forbidden letters. Once one block count is chosen, conservation of the five copies of each letter forces most of the other counts.

**Recall · One-parameter conservation — `COMB-CONS-01`** — Describe each 5-position block by the counts of its two allowed letters; use one parameter instead of six independent counts.

**Start** — Let the first block contain `k` B’s and `5-k` C’s. Use the total number of B’s and C’s to force the corresponding counts in blocks 2 and 3 before counting arrangements inside each block.

---

## Q7 — When do two parabolas intersect?

**Notice** — Do not solve two parabolas repeatedly. Their intersection condition reduces to whether `(D-B)/(A-C)` can be a nonnegative value of `x^2`.

**Recall · Algebra-to-order bridge — `COMB-ALG-01`** — After reducing to a sign condition, the remaining task is an ordered/unordered selection count on `A,B,C,D`.

---

## Q8 — Four crops in a 2 × 2 field

**Notice** — Opposite cells are **not adjacent**. Their relationship determines how many colours/crops remain possible for the other two cells.

**Recall · Proper colouring — `COMB-COLOR-01`** — Model the four cells as the 4-cycle conflict graph. Split according to whether a chosen opposite pair receives the same or different crop-class colour.

**Start** — Choose one cell `X` and its opposite cell `Z` first. Use two cases: `Z` same type as `X`, or `Z` different; then the two remaining cells become easy to count.

---

## Q9 — Three brother-sister pairs in two rows

**Notice** — Forget individual names for a moment. First decide which **family label** occupies each forbidden row/column position; the sibling restrictions behave like forbidden matching positions.

**Recall · Derangements — `COMB-DER-01`** — A derangement counts assignments in which no family/object returns to its forbidden matching position. Restore the brother/sister identities only after the family-position structure is valid.

**Start** — Fix the family labels in one row. Express the family labels in the other row as a permutation with no forbidden direct-front matches; then impose the same-row adjacency condition before restoring individual siblings.

---

## Q10 — Positive-power terms in a multinomial expansion

**Notice** — A term is determined by its exponent tuple. “All four variables have positive powers” is an integer-solution condition.

**Recall · Stars and bars — `COMB-SB-01`** — Write the exponents of `a,b,c,d` as positive variables and the exponent of `1` as a nonnegative slack variable; their sum is `N`.

---

## Q11 — Sharing 24 apples with lower bounds

**Notice** — The apples are identical and the three recipients are named. Satisfy the minimum of 2 apples each first, then distribute what remains.

---

## Q12 — Binary strings avoiding 101 and 010

**Notice** — The forbidden patterns are exactly the patterns where the symbol changes and immediately changes back. Encoding **changes between consecutive bits** is simpler than remembering every 3-bit substring.

**Recall · Encode changes / recurrence — `COMB-ENC-01`, `COMB-REC-01`** — A legal change-pattern cannot contain two consecutive changes. That turns the problem into a short state/Fibonacci-type count.

**Start** — For each adjacent pair, write `1` if the bit changes and `0` if it stays the same. Translate the forbidden `101`/`010` condition into a restriction on this length-9 change string, then remember the two choices for the first original bit.

---

## Q13 — Four-digit snakelike integers

**Notice** — Only the **relative order** of four distinct digits determines the up-down pattern; the leading-zero restriction must be handled separately.

**Recall · Alternating comparisons — `COMB-ALT-01`** — Count order patterns satisfying `< > <`, then separate cases in which 0 would occupy the first position.

**Start** — First choose four distinct digits and study the alternating permutations of their ranks. Only after that correct for selections containing 0 whose alternating order puts 0 first.

---

## Q14 — Permutations with no stable proper prefix

**Notice** — The bad event is not one fixed prefix size. A permutation can have several stable prefixes, so classify by the **first** stable prefix to obtain disjoint cases.

**Recall · Exactly-once recurrence — `COMB-REC-01`** — “First stable prefix of size `k`” gives a unique decomposition: an indecomposable prefix followed by an arbitrary suffix.

**Start** — Let `c_n` be the number with no proper stable prefix. Partition all `n!` permutations by the size `k` of their first stable prefix and write the resulting recurrence before substituting `n=6`.

---

## Q15 — Permutations with no monotone run of length three

**Notice** — If no three consecutive terms are increasing or decreasing, the signs of consecutive comparisons must alternate.

**Recall · Alternating comparison patterns — `COMB-ALT-01`** — Replace the actual values temporarily by an up/down pattern such as `< > < >`; count permutations realizing the two alternating patterns.

**Start** — Show that the only possible comparison-sign patterns are `< > < >` and `> < > <`. Count one pattern carefully by conditioning on the peak/valley positions, then use symmetry for the other.

---

## Q16 — Ratio of two nonlinear recurrences

**Notice** — The term `a_{n-1}^2/a_{n-2}` suggests dividing consecutive terms rather than expanding huge values.

**Recall · Ratio substitution — `COMB-RATIO-01`** — Define `r_n=a_n/a_{n-1}` (and similarly for `b_n`); the nonlinear recurrence may become a simple recurrence for ratios.

**Start** — Divide the recurrence for `a_n` by `a_{n-1}` and simplify in terms of `r_{n-1}`. Do the same for `b_n` before reconstructing `b_32/a_32` as a product of ratios.

---

## Q17 — Choosing six horses with three paired restrictions

**Notice** — Exactly three of the six special horses are chosen, and no special pair can contribute both. Therefore each of the three pairs contributes **exactly one** horse.

---

## Q18 — Committee with conditional membership

**Notice** — Translate the English first: `A` and `B` cannot both serve; `B -> C`. Splitting on whether `B` serves makes the consequences immediate.

**Recall · Conditional case split — `COMB-LOGIC-01`** — Use two disjoint cases, `B in` and `B out`, and count the remaining men/women under the consequences in each case.

---

## Q19 — Right-neighbour restrictions at a circular table

**Notice** — “Immediately to the right” is directional. Fix one person to remove rotational duplication, then place the constrained successors before the unconstrained people.

**Recall · Circular normalization — `COMB-CIRC-01`** — Around an ordinary round table, fix a reference person; do not treat right-neighbour conditions as unordered adjacency.

---

## Q20 — Three girls and five boys around a circle

**Notice** — Ordinary circular gaps guarantee that girls are separated, but the additional “at most two boys” condition restricts **which gaps may be chosen together**.

**Recall · Circular gaps — `COMB-CIRC-02`** — Arrange the boys around the circle first; their circular gaps are candidate positions for the girls. Then check cyclic distances between chosen gaps.

**Start** — Fix/arrange the five boys. Represent a choice of three girl-gaps by a circular 0/1 pattern of length 5 and exclude gap patterns that create three boys between consecutive girls.

---

## Q21 — At least two of three friends adjacent on a circle

**Notice** — “At least one adjacency among the three friends” is often easier by complement: no two of the three friends adjacent.

**Recall · Circular complement + gaps — `COMB-CIRC-02`, `COMB-COMP-01`** — Arrange the four other people first; choose three of their four circular gaps for the friends to force separation in the complement.

---

## Q22 — Selecting six letters from FLABELLIFORM

**Notice** — Positions do not matter; only the number of copies chosen of each letter matters, and each letter has an upper bound from the word.

**Recall · Bounded multiplicity — `COMB-MULTI-01`** — Encode each letter type by `1+x+...+x^m`; the coefficient of `x^6` counts selections of six copies. Handle “at least one vowel” directly or by complement.

**Start** — Write one generating factor for each distinct letter using its available multiplicity. Form the vowel-free product separately if complement is shorter; extract only the `x^6` coefficient rather than expanding everything.

---

## Q23 — Committee with a together-or-neither pair

**Notice** — The pair `A,B` creates exactly two disjoint cases: both in or both out. Apply the `C,D` not-together restriction inside each case.

---

## Q24 — Selecting one or two books from each subject

**Notice** — The three subjects are independent categories. For each subject count “choose 1 or choose 2,” then multiply the three category counts.

---

## Q25 — Interviewing mothers before their own children

**Notice** — For each mother-child pair, exactly half of all relative orders have the mother first. The three pairwise precedence conditions do not interact.

**Recall · Precedence symmetry — `COMB-ORDER-01`** — Start from all `6!` orders and use the independent symmetry that flips the order inside each of the three disjoint pairs.

---

## Q26 — Factor pairs of 7056

**Notice** — Factor pairs are unordered. Count divisors first, then remember that a perfect square has one middle pair with equal factors.

---

## Q27 — Largest power of 24 dividing the product of all divisors

**Notice** — The target is controlled by prime valuations, not by multiplying the divisors explicitly.

**Recall · Divisor/valuation counting — `COMB-DIV-01`** — Factor 1440 and count how often each prime exponent occurs across the divisor grid/product. Compare the resulting valuations with `24=2^3·3`.

---

## Q28 — Relay order with forbidden first and last runners

**Notice** — There are two simple bad events: `A` first and `D` last. Count all orders and use two-event inclusion–exclusion.

---

## Q29 — Divisors lost when lowering an exponent

**Notice** — Compare the prime-exponent boxes for the two numbers. Divisors present in one but not the other lie on a boundary layer of the exponent grid.

**Recall · Divisor exponent grid — `COMB-DIV-01`** — Factor both integers first; describe a divisor by its exponent tuple and count tuples allowed only by the larger exponent range.

---

## Q30 — HONOLULU with no equal adjacent letters

**Notice** — Define one bad event for each repeated letter type whose copies become adjacent. Their intersections require different block structures because multiplicities differ.

**Recall · Adjacency inclusion–exclusion — `COMB-ADJ-01`** — Count all multiset permutations, subtract arrangements with each bad adjacency, then restore intersections.

**Start** — Let `H_O, H_L, H_U` be the events that the equal O’s, L’s, or U’s are adjacent (using the actual multiplicities in the word). Write the inclusion–exclusion skeleton before evaluating any block count.

---

## Q31 — Avoiding three forbidden consecutive blocks

**Notice** — The forbidden events `CD`, `DE`, `EF` overlap. Adjacent bad events can chain into a longer block (`CDE`, `DEF`, `CDEF`) rather than two independent blocks.

**Recall · Chained adjacency blocks — `COMB-ADJ-01`** — In inclusion–exclusion, distinguish intersections of disjoint blocks from intersections that share letters and merge.

**Start** — Define `E1=CD`, `E2=DE`, `E3=EF`. Write the three-event inclusion–exclusion formula, then draw the block created by each pairwise and triple intersection before counting.

---

## Q32 — Nationalities separated in a row

**Notice** — Only the three duplicated nationalities can violate the rule. Treat “the two Americans adjacent,” “the two British adjacent,” and “the two Chinese adjacent” as bad events.

**Recall · Adjacency inclusion–exclusion — `COMB-ADJ-01`** — The people are distinct, so each bad nationality pair forms a 2-person block with an internal order.

---

## Q33 — Pairing people who know neighbours and opposites

**Notice** — This is a **perfect matching** problem in a fixed allowed-edge graph: each vertex may match only to two neighbours or its opposite.

**Recall · Restricted perfect matching — `COMB-MATCH-01`** — Draw the allowed graph before pairing. Then condition on the partner of one fixed person; symmetry reduces the branches.

**Start** — Label the ten circle positions `0,...,9` and draw/describe edges from `0` to `1,9,5`. Split on which of these three partners is matched to `0`, delete that pair, and count matchings of the remaining allowed graph.

---

## Q34 — 2-regular handshake graphs on nine people

**Notice** — Every vertex has degree 2, so every component is a cycle. The problem becomes a count over possible **cycle-size partitions of 9**.

**Recall · Degree 2 -> cycles — `COMB-CYCLE-01`** — On a fixed `k`-set, an undirected cycle has `(k-1)!/2` arrangements. If equal-sized components repeat, swapping whole components must not create a new graph.

**Start** — List all partitions of 9 into parts at least 3. For each cycle-size type, choose the labeled vertex sets and multiply by the cycle counts on those sets; correct for repeated component sizes.

---

## Q35 — MAXIMUM with no adjacent consonants

**Notice** — Arrange the vowels/separators first. Their gaps are the legal homes for consonants; repeated letters affect the internal permutation count.

---

## Q36 — ARRANGE with neither A’s nor R’s adjacent

**Notice** — Use two bad adjacency events: `AA together` and `RR together`. Because A’s and R’s are repeated, each event creates one identical-letter block without an internal factor of 2.

**Recall · Repeated adjacency IE — `COMB-ADJ-01`** — Count all distinct multiset permutations, subtract each bad block count, then add back the arrangement count with both blocks.

---

## Q37 — Colored balls with at least one broken color-block

**Notice** — The wording gives the complement explicitly: subtract arrangements in which **all three colour classes each form one block** from all multiset arrangements.

**Recall · Complement + blocks — `COMB-COMP-01`, `COMB-BLOCK-01`** — Be careful that the four green balls are distinguishable even though white and red balls are identical.

---

## Q38 — Three-digit multiples of 3 from four allowed digits

**Notice** — Divisibility by 3 depends only on the sum of digit residues modulo 3. Classify the allowed digits by residue before counting ordered triples.

---

## Q39 — Four-letter arrangements from EXAMINATION

**Notice** — Classify four-letter words by their multiplicity pattern: `1+1+1+1`, `2+1+1`, `2+2`, `3+1`, `4`, then remove patterns impossible with the available letters.

**Recall · Multiplicity patterns — `COMB-MULTI-02`** — For each feasible pattern, choose the letter types first and then count distinct arrangements of that multiset.

---

## Q40 — Three-letter words from PROPOSAL with a vowel in the middle

**Notice** — The middle position is the strongest restriction. Choose its vowel first, then count the two ordered outer positions using the remaining available copies.

---

## Q41 — Eight-digit multiple of 5 with exactly two adjacent equal pairs

**Notice** — There are three possible adjacency events (`11`,`22`,`33`) and the requirement is **exactly two**, not at least two. The final digit restriction from divisibility by 5 must be imposed as well.

**Recall · Exact adjacency events — `COMB-ADJ-02`** — Choose which two pair-events are required, merge them into blocks, count, then subtract arrangements where the third pair is also adjacent.

**Start** — Split first by which two of `{11,22,33}` are adjacent. In each branch treat those pairs as blocks and enforce the last digit (`5` here) before subtracting the all-three-adjacent overlap.

---

## Q42 — Three teachers separated by exactly two students

**Notice** — The teacher positions, not the identities of the students, carry the spacing condition. Find the position pattern first, then permute teachers and students.

**Recall · Fixed separation — `COMB-POS-01`** — If successive teachers have exactly two students between them, their seat indices differ by 3.

---

## Q43 — Lexicographic rank of ZENITH

**Notice** — Build the rank left to right. At each position count how many unused letters smaller than the target letter could appear there, multiplied by all suffix permutations.

---

## Q44 — Four-digit numbers beginning with 1 and exactly one repeated pair

**Notice** — The multiplicity pattern is fixed as `2+1+1`, but the leading `1` creates separate cases depending on whether `1` is the repeated digit.

**Recall · Multiplicity case split — `COMB-MULTI-02`** — Split on “1 is the doubled digit” versus “some other digit is doubled,” then handle zero restrictions in the remaining positions.

---

## Q45 — Lexicographic rank of PROPER

**Notice** — Dictionary rank still proceeds position by position, but repeated letters change the number of distinct suffix permutations.

**Recall · Dictionary rank with repeats — `COMB-RANK-02`** — For every smaller available letter at a position, count suffix arrangements by dividing by factorials of repeated remaining letters.

**Start** — At the first position, list available letters alphabetically smaller than `P`. For each candidate, count distinct arrangements of the remaining multiset; then move to the second position of `PROPER`.

---

## Q46 — Five numbered people around five distinct circular seats

**Notice** — The seats are distinct and rotations count as different. Do **not** divide by 5 as you would for an ordinary unlabeled round table.

---

## Q47 — Five at a round table and five at a rectangular table

**Notice** — The two tables use different identity rules: a round-table seating identifies rotations, while the rectangular table has distinct positions.

**Recall · What counts as the same object? — `COMB-IDENT-01`, `COMB-CIRC-01`** — Choose which five people go to which table, then apply the correct symmetry factor to each table separately.

---

## Q48 — Same-sex neighbours for two specified people

**Notice** — The specified boy requires both neighbours to be boys and the specified girl requires both neighbours to be girls. These force local same-sex blocks around the circle.

**Recall · Forced circular block — `COMB-CIRC-03`** — Fix one reference person to remove rotation, then build the forced neighbours of `X` and `Y` before placing the remaining people.

**Start** — Fix `X` at one seat. Determine which boys must occupy the two neighbouring seats; then analyze where `Y` can be placed so that both of her neighbours are girls without conflicting with the first forced block.

---

## Q49 — Three-color hats around a 5-cycle

**Notice** — The people are fixed; this is a proper colouring of the cycle `C5`, including the edge from the last person back to the first.

---

## Q50 — Circular arrangements of ALASKA

**Notice** — There are repeated A’s, so blindly dividing a linear multiset count by 6 needs an orbit-size check. Rotation is identified but reflection is not.

**Recall · Circular multiset / orbit check — `COMB-SYM-01`** — Determine whether any nontrivial rotation can fix an arrangement with the multiplicities in ALASKA; only then use a uniform rotation factor.

---

## Q51 — Garlands from three flowers of each of two kinds

**Notice** — Both rotation and reflection identify arrangements, and repeated flowers can have nontrivial symmetry. A simple “divide by 12” is unsafe without an orbit/fixed-pattern analysis.

**Recall · Garland symmetry — `COMB-SYM-02`** — Encode one flower type by its three circular gaps among the other type, or classify binary circular patterns up to dihedral symmetry.

**Start** — Represent a garland by a binary length-6 circle with three 1’s and three 0’s. Classify patterns by the cyclic gaps between the three 1’s; then identify which gap patterns become the same under rotation and reversal.

---

## Q52 — Ten students and a teacher around thirteen chairs

**Notice** — Fix the teacher to remove rotation. The remaining problem is to choose the two empty chairs subject to avoiding the two chairs adjacent to the teacher.

**Recall · Circular empty-chair gaps — `COMB-CIRC-02`** — Once the empty positions are selected, the ten distinct students fill the remaining chairs; keep that factorial separate from the position choice.

---

## Q53 — Painting a cube with six different face colors

**Notice** — All six colours are distinct, so no non-identity cube rotation can fix a raw coloring. This makes the orbit-size check especially simple.

---

## Q54 — Subsets whose size is not one of their elements

**Notice** — The rule refers to the subset's own size. Fix the size `k` first; then the element `k` is simply forbidden.

**Recall · Condition on size — `COMB-SIZE-01`** — For a fixed `k`, choose all `k` elements from the other seven available elements, then sum over possible nonzero sizes.

---

## Q55 — HUDHUDBIRD using at most three distinct letters

**Notice** — “At most three distinct letters” and limited copies make this a multiplicity-pattern problem, not a simple `nPr` count.

**Recall · Multiplicity patterns — `COMB-MULTI-02`** — List partitions of 6 using at most three parts, then keep only patterns supported by the actual letter multiplicities in HUDHUDBIRD.

**Start** — Inventory the multiplicity of each distinct letter first. For each feasible partition of 6 into at most three positive multiplicities, choose which letter types realize those multiplicities and multiply by the corresponding multiset-permutation count.

---

## Q56 — Colored balls with at least one green and one blue

**Notice** — The balls are distinct and the colour classes can be chosen independently. For green and blue choose any **nonempty subset**; red is any subset including empty.

---

## Hint audit

```text
APPENDIX_A_QUESTION_COUNT = 56
NOTICE_PRESENT = PASS_56_OF_56
RECALL_PRESENT_WHERE_ASSIGNED = PASS_40_OF_40
START_PRESENT_WHERE_ASSIGNED = PASS_19_OF_19
FINAL_NUMERICAL_ANSWER_LEAKAGE = 0
```

The next PDF pass should place these as visually quiet local strips directly beneath each corresponding question, with the problem statement remaining visually dominant.