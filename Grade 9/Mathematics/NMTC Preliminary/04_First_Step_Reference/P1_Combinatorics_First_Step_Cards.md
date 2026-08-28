# P1 Combinatorics — First-Step Cards

Performance routine:

`SEE -> DEFINE OBJECT -> IDENTIFY RESTRICTION -> CHOOSE COUNT -> CHECK OVERLAP`

## Card 1 — Ordered or unordered?

**Trigger:** selecting/assigning objects.

**First move:** ask whether swapping selected objects creates a new outcome.

- yes -> ordered / permutation-style;
- no -> unordered / combination-style.

## Card 2 — Sequential choices

**Trigger:** one outcome requires several successive choices.

**First move:** write the number of choices at each stage and multiply.

## Card 3 — Disjoint alternatives

**Trigger:** outcome may arise through one of several mutually exclusive cases.

**First move:** define the cases so they cannot overlap; add case counts.

## Card 4 — Restricted digit number

**Trigger:** digit positions + parity/divisibility/repetition/leading-zero restriction.

**First move:** handle the most restrictive position first, often units or leading digit.

## Card 5 — Complement

**Trigger:** “at least one”, “not all”, “contains a forbidden feature”.

**First move:** test whether `total - none` is simpler.

## Card 6 — Inclusion–exclusion

**Trigger:** count satisfying A or B (or A/B/C) with overlap possible.

**First move:** count singles, identify intersections, correct double counting.

## Card 7 — Pigeonhole

**Trigger:** prove repetition/collision/existence among many objects.

**First move:** name the pigeons and boxes explicitly; compare counts.

## Card 8 — Strong pigeonhole

**Trigger:** prove some box has at least `m` objects.

**First move:** assume every box has at most `m-1`; compute maximum total and contradict.

## Card 9 — Subset product

**Trigger:** sum of products over many subsets.

**First move:** ask whether each element is independently included/excluded; use `product(1+a_i)`.

## Card 10 — Coefficient as count

**Trigger:** coefficient of `x^k` in product of finite sums.

**First move:** let chosen exponents be variables; count bounded integer tuples summing to `k`.

## Card 11 — State/path count

**Trigger:** exact number of moves with restricted positions/transitions.

**First move:** define state = current position/configuration after `t` moves; write recurrence.

## Card 12 — Geometry configuration count

**Trigger:** count subsets of vertices/segments/shapes with geometric property.

**First move:** classify into disjoint geometric types before calculating combinations.

## Card 13 — Representation uniqueness

**Trigger:** signed powers / unusual representation system.

**First move:** establish whether representation is unique before counting sign/digit choices.

## Card 14 — Source/key disagreement

**Trigger:** direct counting from printed wording disagrees with supplied key.

**First move:** preserve the printed sample space, derive independently, mark `SOURCE_CONFLICT` if mismatch remains.

---

# Fast contrast table

| Looks similar | Correct distinction |
|---|---|
| choose 3 team members vs assign 3 offices | unordered vs ordered |
| sequential choices vs alternative cases | multiply vs add |
| A or B with overlap | inclusion–exclusion, not plain addition |
| at least one | test complement |
| coefficient problem | count exponent choices before expanding |
| subset products | inclusion/exclusion choice per element |
| path listing | define states if transitions repeat |
| pigeonhole claim | name boxes; do not invoke theorem vaguely |
