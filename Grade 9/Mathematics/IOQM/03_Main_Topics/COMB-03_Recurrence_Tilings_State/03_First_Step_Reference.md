# First-Step Reference: State Before Recurrence

Use this page before doing arithmetic.

## A. Name the object or target

Write one sentence:

`My state counts/records ...`

A symbol without a precise meaning is not a model.

## B. Test whether the state is sufficient

Ask:

`Can two histories with this same proposed state have different legal futures?`

- Yes -> add the missing memory.
- No -> the state may be sufficient.
- If some remembered detail never changes future choices -> remove it.

## C. Try an exactly-once first/last split

For each branch check:

`Does every valid object enter exactly one branch?`

If branches overlap, do not add them. Redesign the split or use the appropriate counting method.

## D. Map branches to smaller states

A recurrence term is justified only when the branch is in a one-to-one correspondence with the claimed smaller state, with any transition choices accounted for.

## E. Give base-state meaning

Write what each initial value counts. Do not treat `T_0=1` as a magic convention: explain the empty configuration when it is used.

## F. Choose the representation

- board/tiling -> freeze the first unresolved region;
- string/path -> first or last symbol/step;
- hidden local restriction -> add a small flag/state;
- fixed target in a branching process -> compare reverse predecessors;
- digit representation -> process a digit with incoming carry;
- residual/near-boundary structure -> test a direct partition or deficit model;
- opponent optimizes choices -> this is a game, not deterministic state evolution.

## G. Verify

Check the first few small cases independently. A recurrence matching a short numerical pattern is not proof; the structural decomposition is the proof.
