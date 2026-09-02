# First-Step Reference: Games & Invariants

Use this page before simulation, case expansion, or strategy guessing.

The governing router is:

> **STATE → MOVE EFFECT → INVARIANT / MONOVARIANT / W-L CLASS → PROOF → STRATEGY OR OBSTRUCTION**

The aim is not to recognize a chapter name. The aim is to identify the smallest useful representation and write the first mathematically productive line.

---

## 1. Recognition atlas

### A. Reachability / configuration change

Typical surface:

- “Can this configuration be reached?”
- “Can all coins be turned over?”
- “Can we transform A into B?”
- “Every move flips/toggles/transfers a local set.”

First questions:

1. What is the complete state?
2. What does one arbitrary legal move change?
3. Is some parity, residue, colour-weighted sum, or other signature preserved?

First useful line:

`Let the state record ... ; compute the change caused by one arbitrary legal move.`

Do **not** conclude reachability merely because the initial and target signatures agree. Matching an invariant is usually compatibility, not sufficiency.

### B. “Cannot happen” / impossibility

Typical surface:

- “Show that it is impossible ...”
- “Prove no sequence of moves can ...”
- “For which starting states is the target impossible?”

First questions:

1. What condition would every reachable state have to share with the start?
2. Can that condition be checked from one move rather than from all move sequences?

First useful line:

`Define I(state)=... and verify I is unchanged by every legal move.`

Then compare the start and target values.

### C. “For which n does there exist ...?”

Typical surface:

- a parameterized construction problem;
- examples work for some small values;
- parity/residue seems to rule out some classes.

First questions:

1. Which values are impossible, and why?
2. Which values remain possible candidates?
3. What explicit construction or repeatable extension proves those candidates actually work?

First useful line:

`Separate necessity from sufficiency: obstruct the impossible classes, then construct every admissible class.`

### D. Process must terminate / maximum number of moves

Typical surface:

- “Show the process eventually stops.”
- “Prove there is no cycle.”
- “Find an upper bound on the number of moves.”
- every move appears to simplify the state.

First questions:

1. Is there an integer quantity that strictly increases or decreases every move?
2. Is it bounded in the required direction?
3. If one scalar can stay unchanged, would a lexicographic pair work?

First useful line:

`Define M(state)=... and compute M(next)-M(current) for an arbitrary legal move.`

A termination proof does **not** identify a winner unless the terminal outcomes and strategic choices are separately analysed.

### E. Two players / optimal play / force a win

Typical surface:

- “Players alternate.”
- “With optimal play ...”
- “Which starting positions are winning?”
- “Can the first player force ...?”

First questions:

1. What is the complete position state, including player-to-move information when needed?
2. What exactly counts as a terminal win or loss?
3. Can terminal states be classified backward?

First useful line:

`Define the position state and label the terminal positions from the stated win condition.`

Then use:

- `W`: at least one legal move goes to `L`;
- `L`: every legal move goes to `W`.

A successful line of play is not a strategy unless it survives every opponent reply.

### F. Huge forward game tree

Typical surface:

- many legal moves from the opening;
- small terminal states are easy to understand;
- a residue pattern appears in small W/L tables.

First useful line:

`Work backward from the exact terminal states and classify their predecessors.`

If a pattern appears, prove both strategic directions for the whole claimed class before using it.

### G. Board colouring / periodic pattern

Typical surface:

- local flips on a board or lattice;
- a repeating geometric structure;
- parity alone seems too weak.

First questions:

1. What local coordinates does one move change?
2. Can positions receive weights so the total weighted change of every move is zero?
3. Do the move equations force a periodic colouring?

First useful line:

`Choose board weights so that the weighted change of every legal move is 0.`

A colouring is useful because of its move equations, not because it looks symmetric.

---

## 2. Phrase / structure decoder

| Phrase or structure | What to test first | First mathematical action |
|---|---|---|
| “flip”, “toggle”, “change an even number” | parity / binary move effect | encode relevant counts or cells modulo 2 |
| local move repeated across a board | colour/residue weights | derive weights that cancel on each move |
| “can reach”, no opponent | reachability | compare invariant signatures; construct if possibility is claimed |
| “players alternate”, “optimal play”, “force” | W/L strategy | define terminal outcomes and work backward |
| “must eventually stop” | monovariant | find strict bounded progress |
| “maximum number of moves” | quantitative monovariant | bound total possible change |
| “for which n does there exist” | obstruction + construction | split proof into necessity and sufficiency |
| many examples with a periodic pattern | theorem still needed | prove all move/successor classes, not only observed cases |
| many branches but no opponent | deterministic/reachability boundary | route generic state evolution to the earlier deterministic-state toolkit rather than calling it a game |
| same invariant at start and target | compatibility only | seek construction or completeness proof |

---

## 3. Decision router

Start here:

### Step 1 — Is there an optimizing opponent?

- **No** → this is reachability/process analysis. Continue to Step 2.
- **Yes** → define terminal outcomes and player-to-move state. Test W/L retrograde reasoning.

### Step 2 — What does every move do to a candidate quantity?

- exactly unchanged → **invariant**;
- strictly one-way → **monovariant**;
- neither → try a richer state signature or different representation.

### Step 3 — Is parity enough?

- yes → use the smallest parity state that captures the move effect;
- no → try residue classes, a parity vector, or derived colour weights;
- if the arithmetic itself becomes the lesson → retrieve the needed residue rule from prior number theory rather than rebuilding it here.

### Step 4 — What is the proof direction?

- impossibility only → an obstruction may finish the proof;
- possibility/existence → give a legal construction;
- “if and only if” → prove both obstruction and construction directions;
- winning strategy → prove W/L classes, not merely existence of one favourable path.

### Step 5 — Would reverse reasoning be smaller?

If terminal states are simpler than the opening tree, work backward. In a game, preserve the quantifiers:

- W requires **one** L-successor;
- L requires **all** successors to be W.

---

## 4. First-step cards

### Card 1 — Parity invariant

**Cue:** every move has a fixed even/odd effect.

**Write:**

`Let p record the relevant counts modulo 2. Under an arbitrary legal move, p changes by ...`

**Check:** every legal move type, not just one example.

**Finish condition:** differing initial/target parity signatures prove impossibility.

### Card 2 — Colour / residue invariant

**Cue:** local geometric moves and repeating board structure.

**Write:**

`Assign weights to positions so that the weighted change of every legal move is 0.`

**Check:** derive the pattern from move equations; test boundary-crossing moves.

**Finish condition:** signature mismatch obstructs reachability; signature match needs more if possibility is claimed.

### Card 3 — Monovariant

**Cue:** every move seems to make irreversible progress.

**Write:**

`Define M(state)=... . For every legal move, M(next) ≤ M(current)-... .`

**Check:** strictness and a bound.

**Finish condition:** conclude only termination / no cycles / move bound unless further strategic work is supplied.

### Card 4 — W/L classification

**Cue:** opponent, optimal play, forceability.

**Write:**

`Let W mean the player to move can force a win and L mean the player to move cannot avoid loss. Seed the terminal states from the exact rule.`

**Check:**

- every claimed W class has an L-successor;
- every move from every claimed L class reaches W.

**Finish condition:** strategy is “move to a certified L state for the opponent.”

### Card 5 — Reverse strategic reasoning

**Cue:** forward branches explode; terminal layer is simple.

**Write:**

`Classify the terminal frontier, then propagate labels to predecessors.`

**Check:** do not swap existential and universal predecessor rules.

**Finish condition:** prove any observed periodic class for all states in the class.

### Card 6 — Construction / obstruction

**Cue:** “for which n”, “show possible”, “iff”.

**Write:**

`Necessity: ... . Sufficiency: ... .`

For an inductive construction, record:

1. base configurations;
2. legal extension step;
3. property preservation;
4. coverage of all required residue classes.

**Finish condition:** every admissible parameter is reached from a base.

---

## 5. Contrast strip — same surface, different decision

### Reachability vs forceability

- “There exists a legal sequence” → reachability.
- “I can win regardless of the opponent’s replies” → forceability.

One path can certify the first. It cannot certify the second.

### Invariant vs monovariant

- invariant: `I(next)=I(current)`;
- monovariant: `M(next)<M(current)` or the reverse, with a bound.

Do not call strict descent an invariant.

### Necessary vs sufficient

- invariant mismatch can prove impossibility;
- invariant match usually proves only that one obstruction disappears.

Possibility needs construction or a completeness theorem.

### W-state vs L-state proof

- W: exhibit at least one move to L;
- L: check every legal move goes to W.

The quantifiers are different.

### Deterministic branching vs adversarial game

Several possible next states do not automatically create a game. The boundary is whether an opponent controls choices with an opposing objective.

### Reverse reachability vs reverse strategy

Working backward in a deterministic state graph asks which predecessors can reach a target. Working backward in a game attaches W/L quantifiers to those transitions.

### Construction vs strategy

A legal move sequence proves possibility only when no opponent can interfere. In an adversarial setting, a strategy must specify responses to every relevant opponent move.

---

## 6. Traps and checks

### Trap: PATH_IS_NOT_STRATEGY

**Wrong:** “Here is a line in which the first player wins.”

**Check:** can the opponent choose a different legal reply?

### Trap: WL_ONE_DIRECTION

**Wrong:** show only that W can move to L.

**Check:** also prove that every move from L goes to W.

### Trap: INVARIANT_SUFFICIENCY_LEAP

**Wrong:** “The parity matches, therefore the target is reachable.”

**Check:** where is the construction or completeness argument?

### Trap: PARTIAL_MOVE_CHECK

**Wrong:** verify a candidate invariant for one move type.

**Check:** list every legal move type and compute its effect.

### Trap: DECORATIVE_COLOURING

**Wrong:** choose colours because the board looks periodic.

**Check:** do the weights make the change of every move zero?

### Trap: NONSTRICT_MONOVARIANT

**Wrong:** claim termination from a quantity that merely never increases.

**Check:** can a zero-change cycle occur?

### Trap: MONOVARIANT_WINNER_LEAP

**Wrong:** “Every play ends, so the first player wins.”

**Check:** what are the terminal outcomes and W/L classes?

### Trap: WRONG_TERMINAL_SEED

**Wrong:** assume normal-play rules without reading the problem’s ending condition.

**Check:** write the exact win/loss rule before retrograde analysis.

### Trap: PATTERN_FROM_SMALL_TABLE

**Wrong:** extrapolate a W/L residue pattern from a few rows.

**Check:** prove successor behavior for every claimed class, especially where new moves first become legal.

### Trap: EXAMPLES_AS_CONSTRUCTION

**Wrong:** show several small values and say the pattern continues.

**Check:** identify a repeatable legal extension and prove coverage.

---

## 7. Recognition-only drill

For each item, choose the **first useful representation or proof route**. Do not solve the whole problem.

1. Every move flips four specified lamps. Can an all-off target be reached from a state with an odd number of on lamps?
2. Local triangle moves toggle three vertices on a repeating triangular board; ordinary parity does not distinguish the target.
3. A process repeatedly replaces a positive integer state by a strictly smaller positive integer. The question asks only whether the process can continue forever.
4. Two players alternate removals. The problem asks which starts let the first player force a win.
5. A game has many opening branches but only a few terminal states; small W/L labels appear periodic.
6. A parameterized pairing construction works for `n=2` and `n=3`, and a legal gadget would extend any solution from `n` to `n+2`.
7. A machine offers two possible operations, but there is no opponent; the question is whether a target state is reachable.
8. Initial and target configurations have the same parity signature, and the problem asks to prove the target is reachable.
9. A candidate quantity decreases on most moves but can remain unchanged on one legal move type.
10. A board is coloured in three colours, but no calculation has connected those colours to the legal move.
11. A proposed losing class has one legal move to another state in the same losing class.
12. A legal sequence reaches a winning terminal configuration, but an opponent makes every second move.

### Drill check

1. parity obstruction; compute one-move parity effect.
2. derived colour/residue weights from local move equations.
3. strict bounded monovariant.
4. terminal states + W/L recursion.
5. reverse strategic classification, then prove the pattern.
6. construction by base cases plus `n→n+2` extension; check coverage.
7. deterministic/reachability analysis; do not call it adversarial strategy.
8. invariant is only necessary so far; seek a construction/completeness proof.
9. current quantity does not prove termination; refine it or use a lexicographic measure.
10. decorative colouring; derive and verify weighted move cancellation.
11. the proposed L class is false because L may not have an L-successor.
12. a path is not a strategy; classify opponent replies / W-L states.

---

## 8. Source-to-mechanism map

Historical problem text and figures remain source-controlled. Use the mechanism map for recognition, not for memorizing paper solutions.

| Historical anchor | Verified answer | Recognition target | First-step lesson |
|---|---:|---|---|
| `IOQM-2025-Q22` | `66` | adversarial game; player-to-move W/L states; retrograde reasoning | preserve the exact terminal convention, seed terminal states, classify backward |
| `IOQM-2025-Q25` | `36` | obstruction plus construction | separate impossibility from sufficiency; use base constructions and a legal extension |
| `IOQM-2023-Q28` | `67` | local toggle reachability; parity/colour invariant | model one move over binary states, derive a periodic invariant, then keep sufficiency separate from obstruction |

For the 2023 anchor, do not recreate a historical diagram and present it as exact unless its source custody is preserved. An authored schematic must be clearly authored.

---

## 9. Thirty-second checklist

Before calculation, ask:

1. What is the complete state?
2. Is there an opponent, or only reachability/process evolution?
3. What does one arbitrary legal move change?
4. Is something exactly preserved?
5. If not, is something strictly one-way and bounded?
6. If there is an opponent, what are the exact terminal outcomes?
7. Would working backward be smaller than expanding forward?
8. Does my proof need impossibility, possibility, or both?
9. If I used an invariant, have I accidentally treated necessity as sufficiency?
10. If I claimed a winning strategy, have I handled every opponent reply through a valid W/L argument?

**State first. Move effect second. Proof obligation before simulation.**
