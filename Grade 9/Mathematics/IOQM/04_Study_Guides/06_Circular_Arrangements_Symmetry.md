# 6. Circular arrangements and symmetry

## 6.1 Ordinary round-table arrangements

For \(n\) distinct people around an unlabeled circular table, rotations are considered the same, so

\[
(n-1)!
\]

arrangements remain.

A clean explanation is to fix one named person and arrange the remaining \(n-1\) people relative to that person.

## 6.2 When rotations are different

Sometimes the chairs are individually distinguished, or the problem explicitly says rotated seatings count as different. Then do **not** divide by \(n\).

Read the equivalence convention before using any circular formula.

### Teacher contrast

- 6 people around an ordinary round table: \(5!\).
- 6 people in 6 numbered chairs placed around a circle: \(6!\).

The geometry looks similar, but the identity of an arrangement is different.

## 6.3 Directional neighbour restrictions

If “to the right of” or “clockwise from” appears, fix one named person first. The remaining positions then become ordinary labeled slots around that fixed reference point.

This removes rotational ambiguity and makes the directional restrictions concrete.

## 6.4 Circular gap method

Arrange the unrestricted type first. The gaps between them become places where special objects may be inserted.

If 5 distinct boys sit around a circle, they create 5 circular gaps. Putting at most one girl in a chosen gap guarantees that no two girls are adjacent.

Extra spacing restrictions become restrictions on which gaps may be selected.

## 6.5 At least one adjacency by complement

If the condition says “at least two of these special people sit next to each other,” it may be simpler to count the complement: no two special people adjacent.

Typical plan:

1. arrange the unrestricted people around the circle;
2. use their circular gaps;
3. place special people in distinct gaps;
4. subtract from the total circular arrangements.

## 6.6 Circular multisets

For repeated letters around a circle, dividing a linear count by \(n\) is valid only if no arrangement is fixed by a nontrivial rotation.

Unique singleton letters can guarantee that every rotational orbit has size \(n\). If the pattern could repeat periodically, simple division may fail.

## 6.7 Necklaces and garlands

If reflection is also considered the same, the symmetry group is larger than rotations alone.

For a small two-color garland, a practical hand method is often to encode the cyclic gaps between one kind of flower and classify those gap patterns up to rotation and reflection.

For larger or more symmetric problems, Burnside's lemma is the systematic tool, but do not introduce it unless the simple gap/symmetry structure is insufficient.

## 6.8 Empty chairs around a circle

If there are more chairs than people, fix one named person first when rotation is irrelevant. The remaining chair positions can then be treated as labeled slots relative to that person.

If seats adjacent to the fixed person must be occupied, handle those local slots first and only then choose the remaining occupied/empty positions.

## 6.9 Cube colorings

A cube has 24 rotational symmetries.

When all six face colors are different, no non-identity rotation fixes a coloring. Therefore inequivalent colorings are

\[
\frac{6!}{24}.
\]

If colors repeat, this simple division may fail because some colorings can have extra rotational symmetry.

## 6.10 Mixed tables

If some people sit around an unlabeled round table and others occupy distinct positions at another table, apply the symmetry convention separately to each surface.

Do not use one global factorial rule for both.

## What should I notice?

- round table, rotations same → fix one named object;
- numbered/distinct seats → rotations may be different;
- “right of” → fix a reference person;
- special objects separated → circular gaps;
- “at least one adjacency” → complement may be easiest;
- rotation/reflection equivalence → symmetry issue;
- all cube-face colors distinct → divide by 24;
- empty chairs → fix a person, then count remaining slots directly.

## Common mistakes

- dividing by \(n\) when chairs are distinct;
- forgetting the wrap-around adjacency between last and first positions;
- using \(n+1\) gaps on a circle;
- dividing by a symmetry-group size without checking whether all objects have full-size orbits;
- treating reflection as equivalent when the problem distinguishes clockwise and anticlockwise arrangements;
- forgetting to impose local occupied-seat restrictions before choosing empty chairs.

## Appendix A practice

Questions **Q19, Q20, Q21, Q46, Q47, Q48, Q50, Q51, Q52, Q53**.
