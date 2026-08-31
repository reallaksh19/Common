# ALG-04 — Stable Recurrence Interface v1

Status: `STABLE_PREREQUISITE_INTERFACE_FOR_COMB03`

Owner: `IOQM-G9-ALG-04`

Consumer: `IOQM-G9-COMB-03`

This is an authoring/dependency interface, not a student chapter.

## 1. Notation

- `a_n`: the term/state value indexed by integer `n`.
- `a_{n+1}`, `a_{n+2}`: shifted indices.
- A recurrence is written with an explicit valid index range, e.g.
  `a_{n+2}=F(a_{n+1},a_n)` for `n>=0`.
- Initial values are written separately, e.g. `a_0=...`, `a_1=...`.

COMB-03 may rename the quantity (`t_n`, `p_n`, `c_n`) to match the state meaning, but must keep the index semantics explicit.

## 2. Recurrence semantics

A recurrence states **how a current indexed value depends on earlier indexed values**. It does not by itself explain *why* a counting problem has that recurrence.

For an order-`r` recurrence, enough independent initial data are required to determine a unique sequence.

## 3. Explicit versus recursive distinction

- Explicit: `a_n=f(n)` gives the value directly from `n`.
- Recursive: `a_n=F(a_{n-1},a_{n-2},...)` requires earlier values/states.

A recurrence can later be solved into an explicit formula, but those are different representations of the same object.

## 4. Initialization contract

Before evaluating a recurrence:
1. state the smallest index;
2. state the valid recurrence range;
3. state all necessary initial values;
4. check that the first recurrence application uses defined terms.

For counting recurrences, COMB-03 additionally owns the **base-state interpretation**, not merely the numbers.

## 5. Verification contract

To verify a proposed explicit formula against a recurrence:
1. check every initial value;
2. substitute the formula into the recurrence;
3. prove equality for every allowed index.

To verify a recurrence derived from counting:
1. COMB-03 first proves the state definition is unambiguous;
2. proves the first-step cases are disjoint;
3. proves they are exhaustive;
4. maps each case to the claimed smaller state(s);
5. records base states;
6. only then may ALG-04 algebraic verification/manipulation be applied.

## 6. Local cancellation interface

ALG-04 teaches these legal transformations:
- write recurrence copies at neighboring indices;
- subtract/add them;
- define a transformed sequence such as first differences;
- compare moving windows;
- test a neighboring-term invariant.

COMB-03 may retrieve these manipulations after its recurrence is structurally justified.

## 7. Simple neighboring-term invariant

For
`a_{n+2}=p a_{n+1}+q a_n`,
the authoring interface permits use of

`D_n=a_n^2-a_{n-1}a_{n+1}`

with derived law

`D_{n+1}=-qD_n`.

COMB-03 should not import this invariant unless it materially helps a state-count problem; it is not part of the minimum recurrence notation bridge.

## 8. Ownership boundary

### ALG-04 canonical ownership
- indexed sequence notation;
- recurrence semantics;
- initialization;
- explicit vs recursive representation;
- recurrence verification;
- local algebraic recurrence transformations;
- telescoping/window cancellation;
- algebraic high-index invariants.

### COMB-03 canonical ownership
- define the counted/state object;
- first-step decomposition;
- tiling/path/state recurrence derivation;
- deterministic state evolution;
- reverse-state search;
- representation-counting state design.

### COMB-04 canonical ownership
- adversarial game strategy;
- winning/losing states when an opponent chooses moves;
- game invariants/monovariants.

## 9. Consumer-ready summary

COMB-03 may begin integrated prose only when:
- this ALG-04 interface is stable; and
- the named COMB-01 counting/model interface is stable.

At that point COMB-03 should retrieve, not reteach:
- what `t_n` means;
- how a recurrence is initialized;
- how to distinguish explicit from recursive;
- how to verify a recurrence after derivation.

Core downstream principle:

> `DEFINE STATE -> FIRST-STEP PARTITION -> RECURRENCE -> VERIFY/USE`.

Do not write the recurrence before the state.
