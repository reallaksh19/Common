# Pigeonhole & Extremal Reasoning

The quickest way to make many “impossible to track” configurations small is often not to count every arrangement. It is to ask what **must** happen.

## 1. Reconnect: the capacity idea

Suppose 13 cards are placed into 12 labelled folders. You do not know where any card goes.

Trying to list placements is pointless. Instead ask:

> What would be the largest total if every folder contained at most one card?

That total would be 12. But there are 13 cards. So some folder contains at least two.

The useful habit is not “remember the pigeonhole principle.” It is:

**Define the objects. Define the boxes. State the maximum capacity under the opposite assumption. Compare with the actual total.**

### First try

Among 21 integers, why must two leave the same remainder when divided by 20?

Write only the first useful line before reading on.

There are 20 possible remainders, `0,1,...,19`. Those are the boxes; the 21 integers are the objects. If every remainder occurred at most once, there could be at most 20 integers. Therefore two share a remainder.

And once two integers have the same remainder modulo 20, their difference is divisible by 20.

The box model converted a number-theory statement into a collision.

## 2. Generalized capacity: force more than two

If 17 objects are placed into 8 boxes, “some box has two” is true but weak. We can force three.

Assume every box had at most two objects. Then all 8 boxes together could hold at most 16. But there are 17. Hence some box contains at least three.

More generally, to prove that some box contains at least `k` objects, test the opposite claim:

> every box contains at most `k-1`.

With `m` boxes, that opposite world can hold at most `(k-1)m` objects.

So if the actual total exceeds `(k-1)m`, the desired multiplicity is unavoidable.

### Contrast: average versus inevitability

For 17 objects in 8 boxes, the average load is `17/8`, a little above 2. That suggests “at least 3.” But the proof is not “an average of 2.125 means someone has 3” by a vague averaging slogan. The proof is the integer capacity contradiction: eight boxes capped at two hold at most sixteen.

## 3. The main creative step: choosing the boxes

Often the theorem is easy after the right boxes are chosen.

### Consecutive integers from a selection

Choose 11 numbers from `{1,2,...,20}`. Prove that two chosen numbers are consecutive.

The natural boxes are not remainders. Pair the numbers:
`{1,2}, {3,4}, ..., {19,20}`.

There are 10 boxes and 11 chosen objects. Two chosen numbers land in the same pair, so they are consecutive.

The structure of the conclusion tells you how to build the boxes.

### Divisibility from odd parts

Choose 9 numbers from `{1,2,...,16}`. Prove that one chosen number divides another.

Every positive integer can be written uniquely as
`2^t × q`, where `q` is odd.

Use the odd part `q` as the box. Among `1,...,16` there are only eight possible odd parts:
`1,3,5,7,9,11,13,15`.

Two of the nine selected numbers have the same odd part, say `2^a q` and `2^b q` with `a<b`. Then `2^a q` divides `2^b q`.

This is a number-theoretic pigeonhole surface: the hard step is the class map, not a factorial formula.

## 4. Geometry: make every box geometrically small

Pigeonhole works in geometry when a region can be partitioned into cells whose diameter is controlled.

### Five points in a unit square

Divide the square into four equal smaller squares of side `1/2`.

Five points occupy four small squares, so two lie in the same small square. Their distance is at most that small square's diagonal:
`sqrt((1/2)^2+(1/2)^2)=sqrt(2)/2`.

The geometry is now local. We never compared all ten point-pairs.

### Design rule for geometric boxes

1. Decide the distance/angle/area relation you want to force.
2. Partition the region into cells where any two points automatically satisfy that relation.
3. Use more points than cells.
4. Check boundary assignment consistently so every point belongs to one box.

## 5. Extremal choice: when boxes are not the right language

Pigeonhole selects a crowded class. Extremal reasoning selects an object already in the configuration.

The pattern is:

1. the configuration is finite, so an extreme object exists;
2. choose the smallest/largest/nearest/farthest object relevant to the claim;
3. use the problem condition to manufacture something “more extreme”;
4. contradict the choice.

### A closest-pair contradiction

Let `S` be a finite set of real numbers with the property that the midpoint of any two distinct members of `S` is also in `S`.

Can `S` contain two distinct numbers?

Assume it can. Choose two distinct members `x<y` with the smallest positive distance `y-x`.

Their midpoint `(x+y)/2` also belongs to `S`, and lies strictly between them. Its distance from either endpoint is `(y-x)/2`, smaller than the chosen minimum. Contradiction.

So such a finite set has only one element.

Notice what happened: no expression was optimized. We chose an existing nearest pair and used its extremality as a prohibition.

## 6. Extremal choice is not inequality optimization

Compare these two problems.

**Problem A.** A finite set is closed under midpoints. Show it cannot have two distinct elements.

Choose the closest pair. That is extremal choice.

**Problem B.** Positive reals satisfy `x+y=20`. Find the largest possible value of `xy`.

Here there is no finite list of objects from which to choose a “largest object.” The target is a numerical bound over a continuum. This belongs to inequality/algebra optimization; completing the square gives
`xy = 100-(x-10)^2 <=100`.

The words “largest possible” do not automatically mean extremal-choice reasoning.

## 7. Pigeonhole is not inclusion-exclusion

Consider:

> How many integers from 1 to 100 are divisible by 2 or 3?

This asks for an exact count with overlap. Pigeonhole does not calculate it. The natural route is
`50+33-16=67`.

Now consider:

> Choose 51 integers. Prove two have the same remainder modulo 50.

This asks for inevitability, not an exact union size. Remainder classes are the boxes, so pigeonhole is the direct route.

Ask first: **am I computing how many, or proving that some collision must occur?**

## 8. Source connection: an extremal complement bound

A validated IOQM source problem from 2023 asks for the least number of “balanced” quadruples forced inside a very large chosen family. The decisive idea is not to inspect the chosen family directly.

Instead:
1. count the entire universe;
2. count how many objects can be unbalanced;
3. fill the chosen family with all possible unbalanced objects first;
4. any excess is forced to be balanced.

That is an extremal-capacity argument: maximize the bad class, then the unavoidable excess is good.

For the source parameters the universe has 4845 objects and only 4320 can be unbalanced. A family of 4411 therefore forces `4411-4320=91` balanced objects.

## 9. Source connection: local crossing restriction to global extremal size

Another validated 2023 source problem chooses diagonals of a convex 50-gon under the rule that each selected diagonal may cross at most one selected diagonal.

A construction reaches 71:
- 47 noncrossing fan diagonals from one vertex;
- 24 short alternating diagonals, each crossing exactly one of those fan diagonals.

The upper bound is a genuine global extremal statement: a local “at most one crossing per edge” rule limits the total density. The teacher/source trace proves the tight 71 bound using the outer-one-crossing density lemma.

The learner lesson is broader than the theorem: **translate the local restriction into a global structure before trying to add diagonals greedily.**

## 10. Adopt the decision rule

When a problem asks you to prove that something must exist, test these questions in order:

1. Can the objects be classified into fewer boxes than there are objects?
2. If a stronger multiplicity is needed, what is the maximum allowed load per box under the opposite assumption?
3. If geometry is involved, can I partition the region into cells where the desired local property is automatic?
4. If no useful boxes appear, is there a finite smallest/largest/nearest/farthest object whose extremality can be contradicted?
5. Is the problem actually asking for an exact count or an inequality optimum instead?

The first useful line should expose the structure, not start the arithmetic.
