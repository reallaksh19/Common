# Part 0 — 72-Hour Combinatorics Exam Navigator

> **Use this only when the exam is close.** The main guide remains the reference book. This Part tells you **where to go next**; it does not replace the teaching.

## 0.1 Start here

You do **not** need to read the whole book from page 1 to the end in three days.

Your job is to find which skills are blocking you, repair the highest-value ones first, and then practise choosing methods without being told the chapter.

```text
DIAGNOSE
   ↓
MARK GREEN / YELLOW / RED
   ↓
DO HIGH-VALUE WEAK SKILLS FIRST
   ↓
SOLVE
   ↓
WHY DID I GET STUCK?  R / M / S / E / C
   ↓
REPAIR ONLY THAT GAP
   ↓
RETEST WITH LESS HELP
```

### The five failure codes

| Code | What happened? | Repair |
|---|---|---|
| **R — Recognize** | I could not tell what family the problem belongs to. | Reopen the router and **Notice** cue. Compare with a nearby wrong method. |
| **M — Remember** | I knew the family but could not retrieve the method. | Read **Recall** and the named skill card/worked example. |
| **S — Start** | I knew the method but could not write line 1. | Read **Start** only. Then close it and restart. |
| **E — Execute** | My first line was good but I got stuck later. | Redo one worked bridge step by step. |
| **C — Check** | I finished but the count/answer was wrong. | Check identity, overlap, leading zero, wrap-around, symmetry division and exact-once counting. |

Do not write “bad at combinatorics.” Write the code.

---

## 0.2 See this -> think this -> try this

Use readable names first. The stable ID is there so you can jump to the same skill anywhere in the guide.

| When you see... | Think... | First move |
|---|---|---|
| choices made one after another | **Stages** `COMB-COUNT-01` | state the stages and legal choices at each stage |
| committee/subset/group | **Unordered selection** `COMB-SELECT-01` | decide what one chosen set is; do not introduce order unless roles appear |
| “at least one”, “not all” | **Complement** `COMB-COMP-01` | write `wanted = all - opposite` |
| overlapping forbidden properties | **Inclusion–exclusion** `COMB-IE-01` | name the bad events before counting them |
| identical objects into named boxes | **Stars and bars** `COMB-SB-01` | satisfy lower bounds first, then count nonnegative solutions |
| repeated letters with limited copies | **Bounded multiplicity** `COMB-MULTI-01/02` | choose copy counts or classify multiplicity patterns |
| two things must stay together | **Block method** `COMB-BLOCK-01` | merge the required block; check its internal orders |
| special objects must stay apart | **Gap method** `COMB-GAP-01` | place separators first and mark the legal gaps |
| nobody may occupy the matching/original position | **Derangement** `COMB-DER-01` | define the forbidden positions before using a derangement count |
| exactly two/three adjacency events | **Exact adjacency** `COMB-ADJ-02` | choose which events occur, make blocks, then remove extra events |
| ordinary round table | **Circular normalization** `COMB-CIRC-01` | fix one reference object unless seats are labeled/distinct |
| circular separation | **Circular gaps** `COMB-CIRC-02` | place one class, then choose gaps; check wrap-around |
| rotations/reflections considered the same | **Symmetry/orbits** `COMB-SYM-01/02` | list the allowed symmetries before dividing anything |
| people/objects with pairwise relations | **Graph model** `COMB-GRAPH-01` | write what a vertex and edge mean |
| every vertex has degree 2 | **Cycle decomposition** `COMB-CYCLE-01` | list possible cycle-size partitions |
| adjacent vertices must have different colours | **Proper colouring** `COMB-COLOR-01` | write the actual adjacency/conflict graph first |
| repeated local restriction along a string/tiling | **State/recurrence** `COMB-STATE-01` | define the smallest state that determines legal futures |
| target has few predecessors | **Reverse state** `COMB-REVERSE-01` | list predecessors of the target instead of expanding forward |
| more objects than useful categories | **Pigeonhole** `COMB-PH-01` | explicitly name objects, boxes and maximum capacity if the claim fails |
| adversarial moves / force a win | **Game states** `COMB-GAME-01` | find small losing positions; do not treat it as a static count |
| a quantity appears unchanged after every move | **Invariant** `COMB-INV-01` | name it and verify one legal move preserves it |

### Three questions to ask before any formula

1. **What exactly am I counting?**
2. **When do two constructions count as the same object?**
3. **What restriction should I build first?**

---

## 0.3 Recognition Scan — 12 questions to find what to revise

### Rules

- Spend about **60–90 seconds** per item.
- Do **not** solve the whole problem unless the answer is immediate.
- Before looking at any cue, write only:
  1. **What structure do I notice?**
  2. **Which method would I try?**
  3. **What is my first useful line/setup?**
- Score your unaided response first.

Mark:

- `✓` = I recognized it and had a plausible first line.
- `~` = I recognized something useful only after a cue or was unsure.
- `×` = I could not identify a useful method.

### D1 — order or no order?

From 10 students, choose a president, a secretary and two ordinary committee members. What should be chosen as **ordered roles** and what should be chosen as an **unordered set**?

### D2 — complement

How many 7-bit strings contain at least one `1`? Do not calculate; write the complement setup.

### D3 — overlapping bad events

Arrange six distinct letters. `A` may not be immediately followed by `B`, and `C` may not be immediately followed by `D`. Name the bad events and the first inclusion–exclusion line.

### D4 — identical objects with lower bounds

Distribute 18 identical tokens among four named boxes, with at least 2 in each. Write the shifted variables/equation only.

### D5 — separation

Arrange 6 boys and 3 girls in a row so that no two girls are adjacent. What objects should be placed first, and how many gaps do they create?

### D6 — circular identity

Six distinct people sit on six **numbered** seats arranged in a circle. Should rotations be identified? State the raw counting model before imposing any additional restriction.

### D7 — graph degree

A friendship network has vertex degrees `4,4,3,3,2,2`. What identity should be written before trying to list all edges?

### D8 — cyclic colouring

Five fixed positions form a cycle and receive one of 4 colours; adjacent positions must differ. What is the correct representation, and what global condition must not be forgotten?

### D9 — recurrence state

Binary strings have no consecutive `1`s and must contain an even number of `1`s. Why is “remaining length” alone not enough as a state? What extra information should be remembered?

### D10 — symmetry

A bracelet is considered unchanged by rotation and reflection. Before dividing a linear arrangement count by any number, what must you determine?

### D11 — pigeonhole

Seventeen integers are selected. Show that two have the same remainder modulo 16. State the objects and boxes only.

### D12 — game or static count?

Two players alternately remove 1, 2 or 3 counters; the player taking the last counter wins. What should you study first: a graph-colouring count, or small winning/losing positions?

### Recognition check — look only after attempting D1–D12

| Item | Expected family / first move |
|---|---|
| D1 | `COMB-SELECT-01`: assign the two named roles as ordered choices; ordinary members form an unordered choice from the remainder. |
| D2 | `COMB-COMP-01`: `all 7-bit strings - the all-zero string`. |
| D3 | `COMB-IE-01`: define `E1 = AB occurs`, `E2 = CD occurs`; start `valid = 6! - |E1| - |E2| + |E1∩E2|`. |
| D4 | `COMB-SB-01`: set `yi = xi-2 >= 0`, so `y1+y2+y3+y4=10`. |
| D5 | `COMB-GAP-01`: place the six boys first; they create seven linear gaps. |
| D6 | `COMB-CIRC-01`: numbered seats make rotations distinct; start from an ordinary assignment to labeled positions, not `(n-1)!`. |
| D7 | `COMB-DEG-01`: `sum degrees = 2|E|`. |
| D8 | `COMB-COLOR-01`: proper colouring of a cycle/conflict graph; remember last-first adjacency. |
| D9 | `COMB-STATE-01`: remember at least the previous bit and parity of the number of `1`s. |
| D10 | `COMB-SYM-01`: determine which rotations/reflections fix the object / whether orbit sizes are uniform before dividing. |
| D11 | `COMB-PH-01`: objects = 17 integers; boxes = 16 residue classes mod 16. |
| D12 | `COMB-GAME-01`: compute small losing/winning positions and the move-to-losing rule. |

### Internal interpretation

- recognized unaided = `R0`;
- recognized after checking one Notice cue = `R1`;
- still not recognized after a cue = `R2`.

You do not need to write these codes in the book; they help a teacher decide whether the problem is retrieval or missing understanding.

---

## 0.4 Targeted Execution Probe — do only 4–6

Do **not** do all of these automatically. Choose probes only from weak/high-value families revealed by the scan. Maximum initial full probes: **6**.

### E1 — Complement / IE
Count 5-digit strings over `{0,1,2,3}` that contain at least one `1` and at least one `2`. Leading zero is allowed.

Route: `COMB-COMP-01` + `COMB-IE-01`.

### E2 — Stars and bars
Count nonnegative integer solutions of `x+y+z=20` with `x>=3`, `y>=2`.

Route: `COMB-SB-01`.

### E3 — Linear gaps
Arrange 5 distinct boys and 3 distinct girls in a row with no adjacent girls.

Route: `COMB-GAP-01`.

### E4 — Circular gaps
Seat 5 distinct boys and 2 distinct girls around a round table with the girls nonadjacent.

Route: `COMB-CIRC-02`.

### E5 — Graph / degree
A simple graph has 8 vertices, each of degree 3. Determine the number of edges and state why the division by 2 is legal.

Route: `COMB-DEG-01`.

### E6 — Cycle colouring
Count proper colourings of a 4-cycle with 3 labelled colours.

Route: `COMB-COLOR-01`.

### E7 — State recurrence
Let `an` count binary strings of length `n` with no adjacent `1`s. Derive a recurrence by splitting on the last symbol and give meaningful base cases.

Route: `COMB-REC-01`.

### E8 — Pigeonhole / game
Choose **one** according to your weak area:

- Pigeonhole: among any 13 integers show two differ by a multiple of 12 (`COMB-PH-01`), or
- Game: remove 1,2,3 stones, last move wins; classify losing positions (`COMB-GAME-01`).

If you recognized the route but could not finish, mark `E`, not `R`.

---

## 0.5 Build my skill map

Use your scan + targeted probes.

### GREEN
I recognized the family unaided and could execute a representative problem.

### YELLOW
I have partial control.

- `Y-R`: I needed a recognition/retrieval cue.
- `Y-E`: I recognized the method but execution was weak.

### RED
I could not identify a useful family or could not produce a workable start even after a small cue.

| Skill family | My colour | Main repair location |
|---|---|---|
| Counting / order / complement / IE | ☐ G ☐ Y ☐ R | Foundations + `COMB-COUNT/COMP/IE` |
| Selection logic | ☐ G ☐ Y ☐ R | Selecting without order + `COMB-LOGIC` |
| Stars and bars / bounded copies | ☐ G ☐ Y ☐ R | Distributions + `COMB-SB/MULTI` |
| Blocks / gaps / adjacency | ☐ G ☐ Y ☐ R | Linear arrangements + `COMB-BLOCK/GAP/ADJ` |
| Circular counting / symmetry | ☐ G ☐ Y ☐ R | Circular arrangements + `COMB-CIRC/SYM` |
| Graphs / matchings / colouring | ☐ G ☐ Y ☐ R | Graphs + `COMB-GRAPH/MATCH/COLOR/CYCLE` |
| Recurrences / state | ☐ G ☐ Y ☐ R | Recurrences + `COMB-STATE/REC` |
| Pigeonhole / extremal | ☐ G ☐ Y ☐ R | Pigeonhole/extremal + `COMB-PH/EXT` |
| Invariants / games | ☐ G ☐ Y ☐ R | Invariants/games + `COMB-INV/GAME` |

### Personal scheduler

| Global value | My status | Action |
|---|---|---|
| MUST | RED | **Do now** |
| MUST | Y-R | router + Recall + 2 recognition/first-line items |
| MUST | Y-E | worked bridge + 2 execution items |
| MUST | GREEN | one mixed retest only |
| SHOULD | RED | after all MUST-red work |
| SHOULD | YELLOW | if schedule permits after MUST |
| IF TIME | RED/YELLOW | normally skip in a three-day rescue |
| IF TIME | GREEN | no revision needed |

---

## 0.6 What matters most? Global three-day priority

This priority is based on transfer, dependency, distinct-mechanism coverage, the repository's validated 2023–2025 topic signal, and common half-knowledge failure modes. It is **not** an official IOQM weightage prediction.

### MUST — core transfer set

Do at most these 24 practice items before expanding the route.

**Counting / restrictions / selection**
- Q2 — unordered pairs + complement
- Q3 — subset complement
- Q4 — digit complement + leading-digit issue
- Q17 — exactly one from each special pair
- Q18 — conditional committee logic
- Q28 — two-set inclusion–exclusion
- Q54 — condition on subset size
- Q56 — independent nonempty choices

**Repeated objects / arrangements**
- Q9 — derangement representation
- Q11 — lower-bound stars and bars
- Q22 — bounded multiplicities
- Q31 — overlapping/chained adjacency blocks
- Q35 — gap method
- Q41 — exact adjacency events

**Circular / graph / colouring**
- Q8 — 2x2 conflict colouring
- Q20 — circular gaps with an extra spacing restriction
- Q33 — restricted perfect matching
- Q34 — degree-2 graph -> cycles
- Q46 — numbered circular seats / identity rule
- Q49 — proper colouring of a cycle

**State / residues / wider canonical tools**
- Q12 — state/change encoding recurrence
- Q38 — digit residues modulo 3
- Appendix B B19 — pigeonhole
- Appendix B B20 — winning positions / modular invariant

That is the maximum core route, not a command to complete all 24 if many are already Green.

### SHOULD — after MUST is reasonably secure

Q1, Q6, Q10, Q14, Q15, Q19, Q21, Q23, Q24, Q25, Q26, Q27, Q30, Q32, Q36, Q37, Q39, Q43, Q45, Q48, Q50, Q51, Q52, Q55.

### IF TIME — narrower / cross-domain / unusually specialized for this three-day route

Q5, Q7, Q13, Q16, Q29, Q40, Q42, Q44, Q47, Q53.

**Important:** `IF TIME` does not mean “bad problem.” It means lower three-day return relative to the core route for this learner model.

---

## 0.7 My personal three-day plan

Fill this after the diagnostic. Do not carry more than **four active RED families in one day**.

```text
MY RED MUST SKILLS
1. __________________________________
2. __________________________________
3. __________________________________
4. __________________________________

MY YELLOW MUST SKILLS
1. __________________________________
2. __________________________________
3. __________________________________

GREEN SKILLS — MIXED RETEST ONLY
____________________________________

SKILLS I AM DELIBERATELY SKIPPING UNLESS TIME REMAINS
1. __________________________________
2. __________________________________
3. __________________________________
```

### Day 1 — RECOGNIZE

Goal: **I can look at a problem and identify a useful family + first line.**

1. Do D1–D12.
2. Build the traffic-light map.
3. Work on RED MUST families first.
4. Use Notice/Recall freely while learning.
5. Finish with 6 short mixed recognition items.

Suggested readiness target: about **75%** correct family + plausible first line on mixed core items.

If below target: do not open more advanced material. Repeat only RED/Y-R families and run a six-item recognition rescan.

### Day 2 — EXECUTE

Goal: **Once I choose a method, I can carry it through.**

1. Work on Y-E MUST skills and remaining RED MUST skills.
2. Use worked bridges for recurring `E` errors.
3. Record only the code beside failures: `Q31 — E`, `Q20 — S`, etc.
4. Drop low-priority SHOULD/IF TIME items if core execution is weak.

Suggested readiness target: roughly **65–70%** independent execution on representative MUST families.

If below target: choose the top three recurring `S/E` families and redo one bridge + one non-identical transfer problem for each.

### Day 3 — RETRIEVE

Goal: **I can choose methods without chapter labels or hints.**

1. Use mixed unlabeled questions.
2. Hide hints initially.
3. Do one timed mixed set.
4. Review only recurring R/M/S/E/C errors.
5. Finish with Quick Reference + your personal error list.

Suggested readiness target: about **80%** recognition on mixed core items with sharply reduced hint use.

**No major new core skill on Day 3.**

---

## 0.8 Hint fading — learn -> retrieve -> transfer -> exam

Do not repeatedly solve the exact same numbers and call that mastery.

```text
ATTEMPT 1 — LEARN
Notice + Recall + Start as needed
        ↓ different nearby problem
ATTEMPT 2 — RETRIEVE
maximum Recall
        ↓ different nearby problem
ATTEMPT 3 — TRANSFER
maximum Notice
        ↓ mixed problem
ATTEMPT 4 — EXAM
no hints
```

If you needed Start on Attempt 1 and still need Start on a near-transfer problem, the skill is not yet retrievable.

---

## 0.9 What should I do next? decision tree

```text
Can I identify the family?
     NO -> R -> Notice / router
     YES
      |
Can I remember the method?
     NO -> M -> Recall / skill card
     YES
      |
Can I write the first useful line?
     NO -> S -> Start
     YES
      |
Did I start correctly but get stuck?
     YES -> E -> worked bridge
     NO
      |
Did I finish but fail identity/overlap/check?
     YES -> C -> checklist
```

The code tells you **what to revise**. Do not reread a whole chapter for an `S` problem.

---

## 0.10 Night-before 30-minute page

### Recall these triggers

- at least one -> complement;
- overlapping restrictions -> inclusion–exclusion;
- identical objects into named boxes -> stars and bars;
- together -> block;
- separated -> gaps;
- original positions forbidden -> derangement;
- circle -> first decide whether rotations are the same;
- pairwise relations -> graph;
- degree 2 -> disjoint cycles;
- adjacent colours differ -> proper colouring;
- repeated local rule -> define a state;
- more objects than categories -> pigeonhole;
- adversarial moves -> losing/winning states.

### Check before submitting

- What exactly was one counted object?
- Did I confuse ordered and unordered?
- Do my cases overlap?
- Did I forget a leading-zero restriction?
- Did I forget last-first adjacency on a circle?
- Did I divide by rotation/reflection without checking identity/orbit size?
- Did I use a recurrence whose branches overlap or whose state forgets needed information?
- Did I count every valid object exactly once?

Then stop. Sleep is more useful than opening a narrow new method late on Day 3.