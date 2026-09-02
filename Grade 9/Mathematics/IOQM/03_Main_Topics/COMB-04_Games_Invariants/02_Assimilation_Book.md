# Games & Invariants

A long move sequence is often the wrong object to study.

In many olympiad problems, the decisive question is not “What happens if I try this move?” but:

- what information does a state really need;
- what does every legal move do to that information;
- what can never change;
- what must change in one direction;
- if another player chooses moves, which states can be forced to win or lose;
- and when an invariant proves only impossibility, what construction is still needed to prove possibility?

The working router for this topic is:

> **STATE → MOVE EFFECT → INVARIANT / MONOVARIANT / W-L CLASS → PROOF → STRATEGY OR OBSTRUCTION**

Use it before simulation.

---

## 1. RECONNECT — start with the state, not the story

A game or move problem may be described with coins, colours, counters, marbles, tiles, or numbers. Strip the story down to the information that determines all legal futures.

For example, suppose two heaps contain red and blue counters and legal moves depend only on the two heap sizes. A state can be written as

`(blue, red)`.

If the rules distinguish whose turn it is, the state must include that information too. If the game is impartial and turns alternate automatically, the player-to-move may be implicit.

The state is too small if two histories assigned the same state can have different legal futures. It is too large if it remembers facts that can never affect another move.

A useful test is:

> **Can two histories with this same proposed state have different legal futures?**

If yes, add the missing information. If no remembered coordinate ever changes future legality, remove it.

### Deterministic evolution is not automatically a game

A machine may allow several possible operations and still not be an adversarial game. The strategic boundary is the opponent.

- If you merely ask whether a state can be reached, the problem is a reachability problem.
- If another player chooses moves with the goal of defeating you, the problem is adversarial.

That difference changes the proof. A single successful path can prove reachability. It cannot prove that you can force a win against every reply.

---

## 2. DISCOVER — compute the effect of one arbitrary move

Before following a move sequence, ask what one legal move changes.

Suppose a board contains some heads and tails, and every move flips a specified local set of coins. Encode heads/tails by `0/1`. A move becomes a toggle vector: it changes certain coordinates modulo 2.

This suggests the central invariant question:

> **Can I combine the state coordinates so that every legal move changes the combination by zero?**

### A first parity example

Imagine three boxes `A,B,C`. A move transfers one token from `A` to each of `B` and `C` simultaneously whenever legal.

The total number of tokens is unchanged, so total count is an invariant. But if the target state has the same total, that tells us only that the target is compatible with this invariant. It does not yet tell us the target is reachable.

Now look modulo 2. One move changes the parity vector by

`(1,1,1)` modulo 2,

because subtracting 1 and adding 1 have the same parity effect. Therefore any parity combination whose coefficients add to 0 modulo 2 is preserved. For instance, parity of `A+B` changes by `1+1=0`, so `A+B (mod 2)` is invariant.

This is more informative than watching several sample moves.

### The invariant proof contract

Whenever you claim an invariant, prove three things:

1. **What is preserved?** Define it exactly.
2. **Why does every legal move preserve it?** Check an arbitrary move, not just examples.
3. **How does the invariant answer the question?** Compare the initial and target values.

If initial and target invariant values differ, the target is impossible.

If they match, stop and ask whether you have proved sufficiency. Usually you have not.

---

## 3. MAKE SENSE — parity vectors and colour weights

Parity is the simplest residue system, but the method is broader.

Suppose the state is represented by a binary vector `p`, and a legal move adds a vector `d` modulo 2. A linear expression

`I(p) = c · p (mod 2)`

is invariant when

`c · d = 0 (mod 2)`

for every legal move vector `d`.

You do not need advanced linear algebra to use this idea. It says only: choose weights so that the weighted change caused by every legal move cancels.

### Why board colourings work

A colouring is useful only when it encodes those weights.

If every move touches a local pattern, try assigning repeating labels to board positions. Then calculate the weighted change of one move. If the total weighted change is always zero, the colouring represents an invariant.

So the logic is not:

`pretty colouring → probably useful`.

It is:

`move equations → required weights → repeating pattern → invariant`.

### When parity is too weak

Suppose two states have the same parity signature but behave differently. Then mod 2 is not fine enough. A mod-3 residue or a three-class colouring may separate them.

Use the smallest residue system that actually distinguishes the states you need. The arithmetic rules for residues are prerequisites; the new work here is choosing the state signature that makes the move effect simple.

### A quick diagnostic

For any proposed colouring, test a move that crosses the boundary between repeated colour blocks. If the weighted change is not zero there, the colouring is decorative, not invariant.

---

## 4. TRY — obstruction before simulation

Consider a row of lamps, each either off or on. A legal move toggles exactly two adjacent lamps. You want to turn all lamps off.

Do not begin by trying move sequences.

Let `N` be the number of on lamps. Every move changes `N` by `-2`, `0`, or `+2`, so the parity of `N` is preserved.

Therefore:

- if the starting number of on lamps is odd, reaching all-off is impossible;
- if it is even, parity gives no obstruction.

The second bullet is important. “Even” does **not** prove that all-off is reachable from every even configuration. It only says this particular obstruction disappears.

### Try 1

A move toggles exactly four lamps. What happens to the parity of the number of on lamps?

**Check:** changing four bits changes the number of on lamps by an even integer, so its parity is invariant.

### Try 2

A move toggles exactly three lamps. Is parity of the number of on lamps invariant?

**Check:** no. The change in the number of on lamps is odd, so the parity flips each move rather than staying fixed.

That does not make parity useless: “parity flips every move” can still connect move count to the target. But it is not an invariant.

---

## 5. DIAGNOSE — the most common invariant failures

### Failure A: “It worked for the first five moves”

Examples do not prove an invariant. The proof must cover every legal move type.

**Repair:** compute the change under an arbitrary legal move.

### Failure B: “The initial and target parity match, so it is possible”

An invariant usually gives a necessary condition.

**Repair:** find a legal construction, or prove that your invariant family completely characterizes the connected components.

### Failure C: “I coloured the board in three colours, so there is a mod-3 invariant”

Colouring is not evidence by itself.

**Repair:** derive the colour weights from the move effect and verify cancellation.

### Failure D: “There are many legal branches, so this is a game”

Branching is not the criterion.

**Repair:** ask whether an opponent controls choices with an opposing objective. If not, treat it as deterministic/nondeterministic reachability rather than W/L strategy.

---

## 6. DISCOVER AGAIN — when nothing is preserved, look for one-way progress

An **invariant** stays exactly unchanged. A **monovariant** moves strictly in one direction.

Suppose a process has an integer quantity `M(state)` such that every move satisfies

`M(next) ≤ M(current) - 1`,

and every legal state has `M ≥ L`.

Then a play starting at `M_0` lasts at most

`M_0 - L`

moves.

That proves termination and gives a move bound.

### The monovariant proof contract

1. Define the quantity or ordered pair.
2. Prove every legal move changes it in the claimed direction.
3. Prove strictness if you want termination.
4. Give a lower or upper bound, or another well-founded order.
5. State exactly what follows.

The last step prevents a major error:

> **Termination does not automatically identify the winner.**

A finite game may end under every line of play, yet which player wins can still depend on the strategic structure.

### Nonincrease is not enough

If `M` can stay unchanged, a zero-change cycle may exist. Then `M` alone does not prove termination.

Sometimes the repair is a lexicographic monovariant. Use a pair `(A,B)` and order states so that each move either lowers `A`, or keeps `A` fixed and lowers `B`. On a finite set of nonnegative pairs, cycles are impossible.

---

## 7. TRY — separate “must end” from “who wins”

A token starts at a positive integer `n`. A legal move replaces it by a smaller positive integer. Then `M=n` is a strict positive-integer monovariant, so every play terminates.

Have we proved the first player wins?

No. The move rules could make `n=1` terminal, and different starting values could be winning or losing depending on which smaller values are reachable. The monovariant tells us the game graph is finite in the direction of play. It does not perform the W/L classification.

This gives a useful division of labour:

`MONOVARIANT → finite/acyclic structure`

then, if a winner is asked,

`TERMINAL STATES → W/L RECURSION`.

---

## 8. MAKE SENSE — winning and losing states

Now suppose two players alternate moves and each tries to force the stated winning condition.

First read the terminal rule exactly. Do not assume the usual “no move loses” convention if the problem says something special such as “the player who takes the last red marble wins”.

With the terminal outcomes fixed, define:

- `W`: the player to move can force a win;
- `L`: the player to move cannot avoid losing against correct play.

For a finite game, the recursive rules are:

> A state is **W** if it has **at least one** legal move to an L state.

> A state is **L** if **every** legal move goes to a W state.

These two quantifiers are the heart of the method.

### Why one winning line is not enough

Suppose from state `S` you can play to `A`, then imagine the opponent plays to `B`, then you reach a win.

That only proves a line exists. If the opponent has another legal reply from `A`, your line may be irrelevant.

A strategy proof must survive every opponent reply. The W/L rules encode exactly that requirement.

### The full W/L proof contract

For a claimed class of losing states:

1. every move from the class must leave it and enter a certified winning class;
2. for every claimed winning state, exhibit at least one legal move into the losing class.

A pattern in a small table is evidence for a conjecture, not the theorem. The theorem is the two-direction successor proof.

---

## 9. REVERSE — work backward from endings

Forward game trees grow quickly because each player may have several choices. Terminal states are often much simpler.

So reverse the viewpoint:

1. label the terminal states from the actual rule;
2. any predecessor with a move to an L state is W;
3. once all successors of a state are known W, that state is L;
4. repeat backward.

This is **retrograde analysis**.

It resembles reverse search in a state graph, but adversarial quantifiers make it strategically different. In ordinary reachability, a predecessor is useful if a path exists. In a game, one must track who controls the next choice.

### A tiny example

There is a pile of `n` stones. A player may remove 1 or 2 stones. The player taking the last stone wins.

Take `n=0` as losing for the player to move: there is no legal move and the previous player took the last stone.

Then:

- `1` is W because `1 → 0`;
- `2` is W because `2 → 0`;
- `3` is L because both moves go to W states `2` and `1`;
- `4` is W because `4 → 3`;
- `5` is W because `5 → 3`;
- `6` is L.

The pattern suggests multiples of 3 are losing. Now prove it:

- from `3k`, legal moves go to `3k-1` or `3k-2`, neither a multiple of 3;
- from a nonmultiple of 3, remove 1 or 2 to reach a multiple of 3.

So every losing-class move goes to W, and every W state has a move to L.

The strategy is therefore not “follow this sample line”. It is:

> **After each opponent move, return the opponent to the losing residue class.**

---

## 10. DIAGNOSE — strategic errors

### PATH IS NOT STRATEGY

**Wrong move:** show one favorable sequence.

**Repair:** prove the opponent cannot choose a reply outside your plan.

### W/L ONE DIRECTION

**Wrong move:** show every W state has one move to the proposed L class, but never prove that L states have no move back to L.

**Repair:** keep both quantifiers visible:

`W: ∃ move to L`

`L: ∀ moves go to W`.

### WRONG TERMINAL SEED

**Wrong move:** import the normal-play ending into a game with a special last-object or colour rule.

**Repair:** translate the exact terminal statement before labelling any state.

### SMALL-TABLE PATTERN

**Wrong move:** extrapolate a periodic W/L pattern from a few rows.

**Repair:** prove the successor classes for the whole claimed residue family, including states where new move types first become legal.

---

## 11. MAKE SENSE — construction and obstruction are different proof directions

Many invariant problems ask for a complete classification:

`Property P holds exactly when condition C holds.`

That contains two separate jobs.

### Obstruction: prove necessity

Show

`P ⇒ C`.

A parity, residue, colour, or other invariant is often ideal here. If violating `C` forces an invariant mismatch, those cases are impossible.

### Construction: prove sufficiency

Show

`C ⇒ P`.

Now you must actually build a legal realization, give a move sequence, produce a pairing, or prove a recursive construction covers every permitted case.

An invariant match is not a construction.

### Inductive constructions need coverage

Suppose you prove:

- valid examples exist for parameters `2` and `3`;
- every valid example at `n` can be extended to one at `n+2`.

Then both parity classes are covered, so every `n ≥ 2` is reached.

If you had only the base `n=2`, the `+2` step would cover only even values. A correct extension rule without enough base classes is an incomplete classification.

---

## 12. HISTORICAL ANCHOR — the pairing architecture

One validated IOQM problem asks for which values of a parameter a pairing can be arranged so that a product of pair-sums is a perfect square.

The independently verified route has exactly the structure we want to learn:

1. one smallest parameter value is obstructed;
2. explicit constructions exist for two consecutive base sizes;
3. if a valid construction exists for size `n`, four new numbers can be added in two pairs whose sums are equal;
4. the two equal new sums contribute a square factor;
5. the construction therefore extends `n → n+2`;
6. the two base sizes cover both parity classes.

For the historical range, this yields **36** valid parameter values.

The reusable lesson is not the number 36. It is the proof architecture:

> **obstruct the impossible class, then construct every remaining class.**

---

## 13. HISTORICAL ANCHOR — local flips and a period-3 signature

Another validated IOQM problem uses local flips on a triangular arrangement.

The efficient route does not simulate long sequences. Encode the flips modulo 2 and search for weights on positions such that each legal local flip has weighted change zero. The local equations force a repeating period-3 pattern.

Comparing the initial and desired global states gives a condition based on whether the side parameter is divisible by 3. The independently verified classification yields **67** valid values in the stated range.

Two lessons matter:

1. a useful colouring is derived from the move equations, not guessed aesthetically;
2. an obstruction/class condition must be paired with sufficiency when the problem asks exactly which targets are achievable.

The original historical diagram remains a source object. For learning the method, an abstract binary-state model is enough.

---

## 14. HISTORICAL ANCHOR — a marble game and 66 winning starts

A validated IOQM marble game uses a two-coordinate state and a special terminal rule involving the last red marble.

The independently verified solution evaluates the finite state grid recursively and obtains **66** winning starting states among the 121 specified starts.

The transferable method is:

1. preserve the special terminal convention;
2. define the complete state;
3. label small terminal-near states first;
4. work backward using `W: exists L-successor` and `L: all successors W`;
5. prove any discovered pattern before counting states in the pattern.

This is a forceability problem. A single legal path ending with the desired last red marble would not be enough.

---

## 15. FADE — reduce the help in stages

### Stage A: invariant supplied

You are told a candidate parity or weighted sum. Your job is to verify every move and state the conclusion.

### Stage B: representation supplied

You are told to encode the state modulo 2 or by periodic colours, but must discover the invariant yourself.

### Stage C: recognition cue only

You are told only: “Compare the effect of one arbitrary move before simulating.”

### Stage D: no method label

You receive a changed-surface move problem and must decide whether the correct tool is:

- invariant;
- monovariant;
- W/L classification;
- reverse strategic reasoning;
- construction/obstruction;
- or a deterministic state method outside this topic.

Independence begins when you can make that choice without a label.

---

## 16. ADOPT — a compact decision router

For a new problem, write these questions before doing substantial arithmetic or simulation.

### Step 1 — STATE

What information determines every legal future move and the objective?

If an opponent matters, is player-to-move represented correctly?

### Step 2 — MOVE EFFECT

What changes under one arbitrary legal move?

Write a parity delta, residue delta, colour-weight change, potential change, or successor list.

### Step 3 — CHOOSE THE STRUCTURE

- exactly unchanged → **invariant**;
- strictly one-way with a bound → **monovariant**;
- opponent chooses moves and outcome must be forced → **W/L classification**;
- terminal states are simpler than opening branches → **reverse strategic reasoning**.

### Step 4 — IDENTIFY THE PROOF DIRECTION

- impossibility → seek an **obstruction**;
- possibility/existence → give a **construction**;
- exact classification → expect both directions;
- winner → prove forceability, not mere reachability.

### Step 5 — CHECK THE BOUNDARY

Ask:

- Am I merely rebuilding modular arithmetic instead of using it?
- Is this actually deterministic state evolution with no opponent?
- Have I proved all legal move types?
- Have I confused a necessary condition with sufficiency?
- Have I confused termination with winner identity?

---

## 17. TRANSFER — same mechanism, different surface

### Transfer A: coins to lamps

A coin flip system and a lamp toggle system may have identical binary move vectors. Ignore the story and compare the move effect.

### Transfer B: board colouring to weighted residue signature

A repeating board colour pattern can be rewritten as coefficients in a weighted residue sum. Conversely, a short system of move equations may reveal the right colouring.

### Transfer C: potential to strategy

A monovariant may prove that a game cannot continue forever. Then W/L recursion can classify the finite game. Do not ask one tool to do the other tool’s job.

### Transfer D: reachability to forceability

A legal sequence proves that a state is reachable when you control the sequence. If an opponent chooses alternate moves, replace the sequence by a strategy proof that survives every reply.

### Transfer E: examples to recursive construction

Several successful parameter values suggest a construction. The proof begins only when you identify a legal extension rule and show the base cases cover every required residue class.

---

## 18. Mixed practice — choose the first useful line

For each prompt, do not solve completely. Write only the first mathematical object or statement you would use.

1. Every move toggles the vertices of one small local shape. Can a target pattern be reached?
2. Every move reduces a nonnegative “disorder” count, but sometimes by different amounts. Must the process terminate?
3. Two players alternately remove allowed numbers of stones; determine winning starts.
4. A target configuration has the same parity signature as the start. Does that prove reachability?
5. A construction works for `n=2,3`, and a legal extension maps `n` to `n+2`. What coverage check remains?
6. A process has many legal branches, but no opponent. Should you build a W/L table?
7. You find a three-colour board pattern that looks periodic. What must be verified before calling it an invariant?
8. A game always terminates because a bounded integer decreases. Can you name the winner from that fact alone?

### First-line checks

1. Encode one legal move as a parity/residue vector and search for a zero-change weight.
2. Define the disorder count precisely; prove strict decrease and a lower bound.
3. State terminal outcomes and begin W/L classification backward.
4. No; require construction or completeness for sufficiency.
5. Verify the bases cover both parity classes reached by the `+2` extension.
6. No; without an optimizing opponent, use state/reachability methods instead.
7. Check the weighted change for every legal move type, including boundary-crossing moves.
8. No; termination is separate from winner classification.

---

## 19. Final checklist

Before you accept your own solution, ask:

- Is the state complete and minimal enough?
- Did I compute the effect of an arbitrary legal move?
- Did I prove an invariant for every move type?
- If I used a monovariant, is the change strict and bounded?
- If I claimed a win, did I prove a strategy against every reply?
- If I used W/L classes, did I prove both directions?
- If an invariant matches, did I avoid assuming reachability?
- If I claimed an iff classification, did I separately prove obstruction and construction?
- If I worked backward, did I seed the exact terminal rule first?
- Did I accidentally treat a deterministic state problem as an adversarial game?

Then return to the router:

> **STATE → MOVE EFFECT → INVARIANT / MONOVARIANT / W-L CLASS → PROOF → STRATEGY OR OBSTRUCTION**

The goal is not to memorize one game or one colouring. It is to recognize the smallest structure that makes a long move sequence unnecessary.