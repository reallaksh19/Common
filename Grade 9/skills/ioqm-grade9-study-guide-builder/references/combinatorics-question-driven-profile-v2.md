# Combinatorics Question-Driven Study Guide Profile v2

## Role

Use this profile with `../SKILL.md` and `question-driven-self-sufficient-study-guide-skill-v2.md`.

The generalized contract owns production mechanics. This profile owns Combinatorics-specific recognition, stable skill IDs, first-line models, visual use, common orphan methods, Appendix A hint behavior, and the exam-in-three-days routing hooks used by the Combinatorics v3 study guide.

The motivating learner knows roughly 30–50% of the school-level background but is unreliable at deciding which counting model applies. The central learner move is:

**surface wording -> counted object -> identity/equivalence rule -> restriction -> smallest useful representation -> disjoint construction/count -> overcount check.**

Do not treat a list of formulas as a self-sufficient Combinatorics guide.

---

## 1. Stable Combinatorics skill families

Student-facing text should show the readable name first and the stable ID second.

### Counting foundations

- `COMB-COUNT-01 · Stages and disjoint cases`
- `COMB-PAIR-01 · Unordered pairs and pair counting`
- `COMB-COMP-01 · Complement counting`
- `COMB-IE-01 · Inclusion–exclusion`
- `COMB-IDENT-01 · What counts as the same object?`

### Selection and logical restrictions

- `COMB-SELECT-01 · Ordered versus unordered selection`
- `COMB-LOGIC-01 · Conditional membership and case splits`
- `COMB-PAIRRULE-01 · Exactly one / together-or-neither pair rules`

### Distributions and repeated copies

- `COMB-SB-01 · Stars and bars with lower bounds`
- `COMB-MULTI-01 · Bounded multiplicities / generating polynomial`
- `COMB-MULTI-02 · Multiplicity-pattern classification`
- `COMB-CONS-01 · One-parameter conservation across blocks`

### Linear arrangements

- `COMB-PERM-01 · Permutations with repeated objects`
- `COMB-BLOCK-01 · Block method`
- `COMB-GAP-01 · Gap method`
- `COMB-DER-01 · Derangements`
- `COMB-ADJ-01 · Forbidden adjacency by inclusion–exclusion`
- `COMB-ADJ-02 · Exact adjacency events`
- `COMB-POS-01 · Fixed separation / position patterns`

### Relative order and rank

- `COMB-ORDER-01 · Relative-order and precedence symmetry`
- `COMB-ALT-01 · Alternating comparison patterns`
- `COMB-RANK-01 · Dictionary rank, distinct letters`
- `COMB-RANK-02 · Dictionary rank, repeated letters`

### Circular arrangements and symmetry

- `COMB-CIRC-01 · Circular normalization and numbered seats`
- `COMB-CIRC-02 · Circular gaps and wrap-around restrictions`
- `COMB-CIRC-03 · Forced local circular blocks`
- `COMB-SYM-01 · Rotation/reflection orbit check`
- `COMB-SYM-02 · Necklace/garland symmetry`
- `COMB-SYM-03 · Cube rotations`

### Graphs, matchings and colourings

- `COMB-GRAPH-01 · Translate pairwise relations into a graph`
- `COMB-DEG-01 · Handshake lemma / degree sum`
- `COMB-MATCH-01 · Perfect matchings under restrictions`
- `COMB-CYCLE-01 · Degree 2 implies disjoint cycles`
- `COMB-COLOR-01 · Proper graph/cycle colouring`
- `COMB-INC-01 · Incidence double counting`

### Recurrences and state

- `COMB-STATE-01 · Define the smallest sufficient state`
- `COMB-REC-01 · Exactly-once first/last-step recurrence`
- `COMB-ENC-01 · Encode changes instead of full symbols`
- `COMB-REVERSE-01 · Reverse-state search`
- `COMB-RATIO-01 · Ratio substitution in a nonlinear recurrence bridge`

### Number-theoretic counting bridges

- `COMB-DIV-01 · Divisor/exponent-grid counting`
- `COMB-RES-01 · Digit residue counting`

### Pigeonhole, extremal, invariants and games

- `COMB-PH-01 · Pigeonhole: objects, boxes, capacity`
- `COMB-EXT-01 · Extremal choice and forbidden improvement`
- `COMB-INV-01 · Invariant / monovariant`
- `COMB-GAME-01 · Winning and losing positions`

### Cross-domain bridge skills used by the supplied corpus

- `COMB-AP-01 · Arithmetic progression with fixed total`
- `COMB-ALG-01 · Reduce algebraic feasibility to an order/sign condition`
- `COMB-SIZE-01 · Condition on the chosen subset size`

---

## 2. One-page recognition router

Train the learner to ask these in order:

1. **What exactly is one counted object?**
2. **When are two raw constructions the same visible object?**
3. **Does order matter?**
4. **What is the strongest restriction?**
5. **Can I build the restriction directly?**
6. **If not, is complement or inclusion–exclusion shorter?**
7. **Would blocks, gaps, a graph, a state, residues, prime exponents, or symmetry make the restriction smaller?**
8. **Have I counted each valid object exactly once?**

High-value visible clues:

| Surface clue | First method to test |
|---|---|
| at least one / not all | `COMB-COMP-01` |
| two or more overlapping bad conditions | `COMB-IE-01` |
| identical objects into named boxes | `COMB-SB-01` |
| limited copies of repeated letters | `COMB-MULTI-01/02` |
| must stay together | `COMB-BLOCK-01` |
| must stay apart | `COMB-GAP-01` |
| nobody in original/family position | `COMB-DER-01` |
| exactly k adjacency events | `COMB-ADJ-02` |
| ordinary round table | `COMB-CIRC-01`; fix a reference object |
| circular separation | `COMB-CIRC-02`; choose circular gaps |
| rotations/reflections identified | `COMB-SYM-01/02`; check orbit size before dividing |
| pairwise relations | `COMB-GRAPH-01` |
| every vertex has degree 2 | `COMB-CYCLE-01` |
| adjacent vertices must differ | `COMB-COLOR-01` |
| local restriction repeated along a string/tiling | `COMB-STATE-01/REC-01` |
| fixed target with few predecessors | `COMB-REVERSE-01` |
| more objects than useful categories | `COMB-PH-01` |
| adversarial moves / force a win | `COMB-GAME-01`, not static graph counting |

---

## 3. Combinatorics orphan-method traps

A guide is incomplete if it merely says:

- “use inclusion–exclusion” without defining overlapping bad events;
- “use gaps” without identifying the separators and the legal gaps;
- “use derangements” without explaining what the objects and forbidden positions are;
- “use Burnside/symmetry” without checking which transformations identify objects or whether orbit sizes are uniform;
- “degree 2 means cycles” without teaching labeled cycle counting and repeated component-size correction;
- “use a recurrence” without defining the state, proving branches disjoint/complete, and interpreting base cases;
- “use a graph” without stating what a vertex and edge mean;
- “use pigeonhole” without naming objects, boxes and capacity;
- “use an invariant” without naming the preserved quantity and proving each move preserves it;
- “winning positions repeat mod k” without proving the losing/winning transition rule.

Repair every required orphan with chapter teaching or a non-identical worked bridge.

---

## 4. Visual-pedagogy profile

Combinatorics often benefits from schematic visuals because the representation itself is the method.

Strong-use cases:

- row/circular gap diagrams;
- block-merging diagrams for adjacency inclusion–exclusion;
- small graph and matching diagrams;
- cycle decompositions for degree-2 graphs;
- conflict graphs for colourings;
- state diagrams or two-row recurrence tables;
- rotation/reflection orbit sketches;
- pigeonhole boxes/capacity diagrams;
- game-state arrows for winning/losing positions.

A visual is required when it materially reduces hidden mental bookkeeping. Decorative grids or stock imagery do not count.

---

## 5. Appendix A local hint architecture

Use student-facing labels:

- **Notice** — recognition only;
- **Recall** — readable skill name + stable skill ID;
- **Start** — first executable mathematical move;
- **Check** — only when a legality/overcount warning is essential.

Hint depth is adaptive:

- routine transfer: Notice only;
- medium: Notice + Recall;
- hard/non-routine: Notice + Recall + Start.

Hints must not reveal the final count or complete the decisive last case split.

For a static PDF, keep the problem visually dominant and the hint strips quiet. Prefer 2–3 substantial questions per page.

---

## 6. 72-hour rescue mode

When the learner has at most three days, do not ask for sequential reading. Prepend a **Part 0 — 72-Hour Exam Navigator** that diagnoses recognition separately from execution, then routes the learner to the durable core.

The Navigator must:

- use a 12-item unaided recognition scan;
- ask for `notice -> method -> first useful line`, not 12 full solutions;
- use no more than 6 targeted execution probes initially;
- classify skills Green / Yellow / Red, while retaining internal `Y-R` (recognition/retrieval) and `Y-E` (execution) distinctions;
- route errors through `R/M/S/E/C` = Recognize / Remember / Start / Execute / Check;
- combine global educational priority with personal deficit;
- bound the workload rather than prescribe every weak skill;
- fade hints across non-identical transfer;
- introduce no major new core skill on Day 3;
- duplicate no chapter theory.

Suggested workload guards:

```text
72H_MAX_ACTIVE_RED_FAMILIES_PER_DAY = 4
72H_MAX_NEW_CORE_SKILLS_DAY3 = 0
72H_MAX_MUST_PRACTICE_ITEMS = 24
72H_MAX_FULL_EXECUTION_PROBES_INITIAL = 6
```

Suggested readiness targets are directional, not psychometric claims:

- Day 1: about 75% correct method-family recognition + plausible first line on mixed core items;
- Day 2: about 65–70% independent execution on representative MUST families;
- Day 3: about 80% recognition on mixed unlabeled core items with sharply reduced hint use.

If a target is missed, reduce scope and repair recurring errors; do not respond by opening more advanced material.

---

## 7. Priority rule for a three-day route

For each practice item, reviewers may compute:

`PriorityScore = 3T + 2F + 2D + R`, with each component in `0..2`:

- `T` transfer value;
- `F` frequency across distinct mechanisms plus canonical relevance (not raw worksheet duplicates);
- `D` dependency value;
- `R` repair value for a half-prepared learner.

Provisional bands:

- 12–16: `MUST`;
- 7–11: `SHOULD`;
- 0–6: `IF_TIME`.

The score proposes; curriculum review confirms. A foundational prerequisite may be promoted. A narrow advanced mechanism may be demoted. Difficulty alone never determines priority.

Recent-corpus topic counts may inform `F` but must never be presented as official IOQM weightage.

---

## 8. Acceptance gates

For the supplied 56-question Combinatorics corpus require:

```text
COMB_QUESTION_TO_METHOD_MATRIX = PASS_56_OF_56
COMB_STABLE_SKILL_REFERENCES = PASS_56_OF_56
COMB_ORPHAN_METHOD_AUDIT = PASS_56_OF_56
COMB_APPENDIX_A_HINT_AUDIT = PASS_56_OF_56
COMB_VISUAL_PEDAGOGY_AUDIT = PASS_56_OF_56
COMB_STATIC_CONTENT_SELF_SUFFICIENCY = PASS_56_OF_56
```

For 72-hour mode additionally require:

```text
72H_NAVIGATOR = PASS
72H_RECOGNITION_SCAN = PASS_12_OF_12
72H_EXECUTION_PROBE_ROUTING = PASS
72H_PRIORITY_RATIONALE = PASS
72H_PERSONAL_ROUTE = PASS
72H_RMSEC_REPAIR = PASS
72H_HINT_FADING = PASS
72H_WORKLOAD_BOUND = PASS
72H_THEORY_DUPLICATION = 0
```

These are document-design gates only. Classroom timing, retention, transfer rate and qualification probability remain unclaimed unless measured.