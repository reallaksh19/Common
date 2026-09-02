# Basic Counting, Restrictions & Inclusion-Exclusion
## Integrated Assimilation Book

> **Count objects, not formulas. First decide what makes two outcomes the same.**

## 1. RECONNECT - what is the counted object?

Suppose you own 3 shirts and 4 caps. An outfit is an ordered pair `(shirt, cap)`. There are `3*4=12` outfits because every shirt choice can be followed by every cap choice.

Now suppose you may travel by one of 5 buses or one of 3 trains. These are disjoint types of journey, so there are `5+3=8` choices.

The symbols `+` and `*` are not automatic. They encode different structures:
- **add** counts from disjoint alternatives;
- **multiply** counts sequential stages when every first-stage choice can be combined with the counted second-stage choices.

### The exact-one rule

Before adding case counts, ask:

`Does every valid object enter exactly one case?`

If some object enters two cases, naive addition double-counts. If some object enters no case, the split is incomplete.

## 2. DISCOVER - ordered or unordered?

Choosing a captain and vice-captain from 8 people is ordered: `(A,B)` and `(B,A)` are different roles. Count `8*7=56`.

Choosing two representatives from 8 is unordered: `{A,B}` and `{B,A}` are the same pair. The ordered count `8*7` counts each pair twice, so divide by `2!`:

`C(8,2)=8*7/2=28`.

This is the meaning behind permutation and combination notation:
- order matters -> ordered arrangements;
- order does not matter -> remove the overcount caused by rearranging the chosen objects.

## 3. MAKE SENSE - derive, do not memorize

For `r` ordered selections from `n` distinct objects without replacement:

`n*(n-1)*...*(n-r+1)`.

For an unordered `r`-subset, each chosen set appears in `r!` orders, so

`C(n,r) = n*(n-1)*...*(n-r+1) / r!`.

The formula is the last line of the reasoning, not the first question to ask.

## 4. Repeated objects change identity

How many distinct arrangements of `AABC` are there?

If the two A's were temporarily named `A1,A2`, there would be `4!` arrangements. Swapping `A1,A2` changes no visible word, so every visible arrangement was counted `2!` times.

Therefore the count is `4!/2!=12`.

For multiplicities `m1,m2,...` summing to `n`, the same identity argument gives

`n!/(m1!m2!... )`.

Use this only when objects within each repeated class are genuinely indistinguishable for the problem.

## 5. Restrictions should enter before the factorial

To form a 4-digit odd number using `1,2,3,4` exactly once, the units digit must be `1` or `3`. Choose the restricted position first:

`2 * 3! = 12`.

This is often cheaper than counting all `4!` permutations and then testing parity.

### Position-first cue

When one condition strongly controls a position (last digit, first digit, fixed role, forbidden envelope), handle that position or restriction before expanding the rest of the count.

## 6. Complement - count the easier opposite event

To count length-7 binary strings with at least one `1`, direct cases by first `1` are possible but unnecessary.

All binary strings: `2^7`.
The only forbidden string with no `1`: one string.

Required count: `2^7-1=127`.

Complement is especially useful for phrases such as:
- at least one;
- not all;
- at least one violation;
- a difficult relative-order event whose opposite has rigid structure.

## 7. Inclusion-exclusion - overlap must be repaired explicitly

Among the integers `1,...,100`, how many are divisible by 2 or 5?

Multiples of 2: 50.
Multiples of 5: 20.
Multiples of both, i.e. 10: 10.

If we add `50+20`, the multiples of 10 were counted twice. Subtract the overlap once:

`50+20-10=60`.

For three properties, the same principle continues:

`single counts - pair overlaps + triple overlap`.

Do not use inclusion-exclusion when the original cases are already disjoint.

## 8. Digit strings: counting structure versus arithmetic structure

A digit problem can belong to two different worlds.

**Counting question:** How many 4-digit odd numbers use `1,2,3,4` exactly once? The arithmetic condition only restricts the last position; the main work is counting admissible arrangements.

**Arithmetic digit question:** Which numbers are divisible by 11, or how does a decimal block reduce modulo a divisor? That arithmetic mechanism belongs to the later digit-structure topic. Here we may retrieve such a restriction, but we do not reteach its number-theory derivation.

Boundary rule:

`If the property is already known and the task is to count strings satisfying it -> count here.`

`If the task is to derive or exploit the arithmetic digit property itself -> route to number theory.`

## 9. Historical anchors as decision models

### Restricted digit relation
The 2025 three-digit anchor is not a permutation problem. The relation `c=a+b` converts the number into bounded integer-pair choices. Counting admissible `(a,b)` pairs gives 45.

### Grouped restricted assignment
The 2025 coupon anchor treats `(1,2)`, `(3,4)`, `(5,6)` as three grouped objects assigned injectively to six envelopes, each with two forbidden envelopes. The restriction belongs in the assignment model before any factorial shortcut. The verified count is 40.

### Multiset + complement
For permutations of `223334444`, repeated digits require multiset counting. The relative-order condition becomes simpler when phrased through the last symbol among the 3/4 subsequence; the verified count is 540, giving remainder 40 modulo 100.

### Position restriction
The 2024 odd-number anchor chooses the units digit first, then permutes the remaining symbols: 12.

### Rotational equivalence
The 2023 dice anchor first fixes the opposite `1,2` axis. The remaining four labels have six cyclic orders around that axis; the three opposite face-pairs each choose one of two colours. The repository's independent verification gives 48. No formal group-action machinery is needed for this Grade-9 interface.

### Unordered selection symmetry
The 2023 order-statistic anchor treats increasing 5-tuples as 5-subsets. Reflection/order-statistic symmetry avoids enumerating every subset and leads to 66.

### Finite-set constraints
The 2023 finite-set anchor first solves constraints on set size and maximum, then uses binomial counts for lower elements. It is a model-first count, not raw subset enumeration; the verified requested value is 43.

## 10. TRY - support fades toward independence

### Full support
How many 5-bit strings contain exactly two `1`s?
Identify the two positions of the `1`s: `C(5,2)`.

### Medium support
How many 4-person committees from 10 contain at least one of two specified people?
Cue: the complement excludes both specified people.

### Light support
How many arrangements of `AABBCC` have the two A's nonadjacent?
Cue: total minus an `AA` block.

### Independent
How many 6-letter strings over `{A,B,C,D}` use every symbol at least once?
Choose and justify direct/complement/inclusion-exclusion without a method label.

## 11. DIAGNOSE - common counting failures

- **Object drift:** switching halfway from ordered sequences to unordered sets.
- **Case overlap:** adding counts when one object satisfies two cases.
- **Case gap:** a split does not cover every valid object.
- **Factorial reflex:** writing `n!` before restrictions are modeled.
- **Repeated-object overcount:** treating identical copies as labelled.
- **Complement mismatch:** subtracting from the wrong universe.
- **Arithmetic/counting collision:** deriving a divisibility rule inside a problem whose actual task is only to count already-characterized strings.

## 12. ADOPT - the counting checklist

1. What exactly is one object/outcome?
2. When are two outcomes considered the same?
3. Is order structural?
4. What restrictions must every object satisfy?
5. If splitting into cases, are the cases disjoint and exhaustive?
6. If making stages, does each stage count the choices available after previous choices?
7. Would the complement be simpler?
8. If properties overlap, where is inclusion-exclusion needed?
9. Are repeated symbols genuinely indistinguishable?
10. Does a digit condition belong to counting or to arithmetic structure?
11. Check small cases or an alternate count when practical.

## 13. TRANSFER

This language is designed to be retrieved downstream.

For recurrence/state problems, the consumer may say: define the counted state, split every valid object into exactly one first-step branch, multiply within stages, and add only disjoint branches. It should not re-teach combinations, repeated-object formulas or inclusion-exclusion.

For graph/coloring problems, the same counted-object, restriction and complement vocabulary applies, while graph-specific canon remains with its owner.
