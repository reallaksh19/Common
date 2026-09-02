# Teacher Diagnostic Key — Games & Invariants

This file is teacher-facing. Learner files intentionally omit answer keys, internal fade labels, source-status codes, and default method hints.

Validation status for author-created items in this wave: `LEAD_STATIC_CHECKED`; fresh independent Wave-5 answer/proof audit: `NOT_RUN`.

## Internal progression map

Repository ladder terminology is used only here for authoring/diagnosis:

- `F0 FOUNDATION`: identify state, move effect, terminal rule, or proof direction;
- `F1 DIRECT`: apply one explicit structural idea cleanly;
- `F2 STANDARD`: choose the idea without being told it;
- `F3 DISGUISED`: same mechanism under a changed surface or close competing route;
- `F4 PRELIMINARY-SPEED`: mixed unhinted execution;
- `XF TRANSFER`: changed representation/context plus verification or WHY-NOT reasoning.

The learner-facing files do not print these labels.

---

## 04 Recognition & First-Line Lab

### Recognition

- `COMB04-R01` — **B**. Four toggles change the number of lit lamps by an even integer, so parity is a natural first compression. Diagnose `SIMULATION_FIRST` if the learner chooses A.
- `COMB04-R02` — **C**. Nonincrease is not strict descent; a zero-change cycle may remain. Diagnose `NONSTRICT_MONOVARIANT` for A.
- `COMB04-R03` — **B**. Exact terminal outcomes and the complete player-to-move state precede W/L recursion. Diagnose `PATH_IS_NOT_STRATEGY` if A is chosen.
- `COMB04-R04` — **C**. Matching invariant values remove one obstruction only. Diagnose `INVARIANT_SUFFICIENCY_LEAP` for A.
- `COMB04-R05` — **B**. A useful colouring is derived from move equations. Diagnose `DECORATIVE_COLOURING` for A.
- `COMB04-R06` — **B**. A `+2` extension needs property preservation and bases covering both parity classes. Diagnose `EXAMPLES_AS_CONSTRUCTION` if the learner treats examples as proof.

### First lines

- `COMB04-L01` — acceptable first line: `Let the state be (x,y,z); one move has delta (-2,+1,+1) up to permutation, so test linear/parity quantities whose delta is always 0.` Total count is an immediate invariant.
- `COMB04-L02` — `Let M be the inversion count of the list.` Swapping an adjacent inverted pair decreases `M` by exactly 1.
- `COMB04-L03` — `Let W/L refer to the player to move; seed 0 stones as L under normal play, then classify backward.`
- `COMB04-L04` — `Choose binary weights c_i satisfying c_i+c_{i+1}+c_{i+2}=0 for every cyclic length-3 move.`
- `COMB04-L05` — `Necessity: prove the obstruction; sufficiency: construct every parameter class not obstructed.`
- `COMB04-L06` — `Does another player control legal choices with an opposing objective?` If no, it is reachability/process analysis; if yes, strategic W/L reasoning is required.

---

## 05 Practice & Transfer Bank

- `COMB04-P01` — **Impossible.** Toggling four lamps changes the number on by an even number, so parity of the on-count is invariant. Start parity is odd; all-off parity is even.
- `COMB04-P02` — **No.** Each coordinate changes by `±2`, so the parity of each coordinate is preserved. `(5,7)` is odd/odd; `(8,4)` is even/even.
- `COMB04-P03` — **Impossible.** For positions modulo 6, two independent binary weightings satisfying `c_i+c_{i+1}+c_{i+2}=0` are `101101` and `011011`. Every legal triple toggle preserves both weighted parities. All-off has signature `(0,0)`; any single lit lamp has a nonzero signature.
- `COMB04-P04` — **Terminates.** Let `M=a+b`. If `a>b`, the next sum is `(a-b)+b=a<a+b`; similarly for `b>a`. `M` is a positive integer and decreases strictly.
- `COMB04-P05` — **First player wins.** Losing heaps are multiples of 3. From 17 remove 2 to 15. From any multiple of 3, removing 1 or 2 leaves a nonmultiple; from any nonmultiple there is a move to a multiple.
- `COMB04-P06` — **First player wins.** Losing heaps are exactly `n ≡ 0 or 2 (mod 7)`. From 20 remove 4 to 16. Check both directions: subtracting `1,3,4` from residues `0,2` never stays in `{0,2}`, while every other residue has a legal subtraction into `{0,2}`.
- `COMB04-P07` — one construction: `(1,4),(2,3),(5,8),(6,7)`. Pair sums are `5,5,13,13`, product `4225=65^2`.
- `COMB04-P08` — one construction: `(1,2),(3,7),(4,5),(6,9),(8,10)`. Pair sums are `3,10,9,15,18`, product `72900=270^2`.
- `COMB04-P09` — **No.** Modulo 3, both `2` and `-1` equal `-1`, so every coordinate changes by the same residue under every move. Hence all pairwise coordinate differences modulo 3 are invariant. The start has all differences 0; `(5,4,3)` does not.
- `COMB04-P10` — **First player wins.** Exactly 17 stones must be removed in total, one per move, so play has exactly 17 moves. The first player makes the last move. Choice of heap does not affect the outcome.
- `COMB04-P11` — **Terminates.** Use inversion count. Swapping an adjacent inverted pair decreases the inversion count by exactly 1; it is a nonnegative integer.
- `COMB04-P12` — **25 is losing.** Losing heaps are `n ≡ 0,1,4 (mod 7)`. From those residues, legal subtractions 2 or 5 always reach residues `2,3,5,6`; from each of `2,3,5,6` there is a subtraction to `0,1,4`.

Common diagnoses across P01–P12:

- one successful move sequence offered as a game proof → `PATH_IS_NOT_STRATEGY`;
- W witness supplied but L closure omitted → `WL_ONE_DIRECTION`;
- invariant match treated as existence → `INVARIANT_SUFFICIENCY_LEAP`;
- one move type checked → `PARTIAL_MOVE_CHECK`;
- observed W/L period without both-direction proof → `PATTERN_FROM_SMALL_TABLE`.

---

## 06 Mixed Mastery Test

The first student attempt is intentionally unlabelled and unhinted.

- `COMB04-M01` — **No.** Same parity obstruction as P01: an odd on-count cannot reach zero by four-lamp toggles.
- `COMB04-M02` — **No.** Pairwise coordinate differences modulo 3 are invariant; start differences are all 0 while the target residues are `2,1,0`.
- `COMB04-M03` — **No.** Use the two period-3 binary weight invariants `101101` and `011011`; any singleton has nonzero signature.
- `COMB04-M04` — **Terminates.** `a+b` decreases strictly and stays positive.
- `COMB04-M05` — **First player wins.** Losing heaps are multiples of 3; `2026 ≡ 1 (mod 3)`, so remove 1 to 2025.
- `COMB04-M06` — **First player wins.** Losing residues are `0,2 (mod 7)`; remove 4 from 20 to 16.
- `COMB04-M07` — e.g. `(1,2),(3,7),(4,5),(6,9),(8,10)` gives product `270^2`.
- `COMB04-M08` — **First player wins.** Exactly 17 unit removals occur, so the first player makes the final move.
- `COMB04-M09` — **Invalid in general.** A constant quantity on a two-state cycle `A -> B -> A` is nonincreasing on every move, yet the process never terminates. Strict descent or another well-founded refinement is needed.
- `COMB04-M10` — the proof still needs **sufficiency for every admissible parameter**: an explicit construction, recursive extension with complete base-class coverage, or another completeness theorem. Several examples do not prove the remaining direction.

## Mastery interpretation

A learner is not yet topic-independent if any of these occur repeatedly:

- begins with uncontrolled simulation where a move-effect invariant is available;
- cannot separate reachability from forceability;
- uses a monovariant to name a winner without W/L work;
- proves only one W/L direction;
- treats invariant compatibility as reachability;
- presents examples instead of a covering construction.

Do not convert this diagnostic interpretation into percentile, qualification-probability, pass-mark, or classroom-timing claims. Those evidence gates remain `NOT_RUN`.

## Historical anchor sanity ledger

The three source-controlled anchors remain unchanged and are not reproduced here as exercise stems:

- `IOQM-2025-Q22 = 66` — adversarial W/L / retrograde reasoning;
- `IOQM-2025-Q25 = 36` — obstruction plus construction;
- `IOQM-2023-Q28 = 67` — local toggle / period-3 invariant plus sufficiency.

Their independent verification status is inherited from the frozen corpus authority; this Wave-4 key does not re-certify that independent audit.
