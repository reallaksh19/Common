# Pigeonhole & Extremal Reasoning

The common idea is **structural inevitability**. Instead of enumerating every configuration, compress the problem until failure would have too little capacity or would create an object more extreme than one already chosen.

## 1. Reconnect: capacity before formula

Put 13 objects into 12 boxes. If every box held at most one object, total capacity would be 12, not 13. Therefore a collision is unavoidable.

The reusable model is:

`OBJECTS -> BOXES -> FAILURE CAPACITY -> CONTRADICTION -> TARGET RELATION`

For example, among 21 integers there are two with the same remainder modulo 20: the 20 remainder classes are the boxes. Equal remainder then implies that their difference is divisible by 20.

## 2. Generalized pigeonhole

To force at least `k` objects into one of `m` boxes, negate the claim. If every box had at most `k-1`, the total could be at most `(k-1)m`. Any larger total forces a box with at least `k` objects.

This is stronger than an informal average slogan. The average may suggest the threshold; the proof is the integer capacity contradiction.

## 3. Box design is the creative step

The conclusion should suggest the boxes.

To prove that 11 chosen numbers from `{1,...,20}` include two consecutive numbers, use the ten boxes `{1,2},{3,4},...,{19,20}`. Eleven choices force two into one pair.

To prove a divisibility relation among selected numbers, residue classes or odd-part classes may be useful boxes. Arithmetic classification must already be justified; COMB-05 owns the collision step, not a new modular-arithmetic chapter.

## 4. Geometric pigeonhole

In geometry, a box is usually a cell in a partition. The crucial check is its **diameter**, not merely its area.

Five points in a unit square: divide the square into four half-size squares. Two points occupy one small square, whose diameter is `sqrt(2)/2`; hence their distance is at most `sqrt(2)/2`.

The design rule is:
1. decide the metric relation to force;
2. partition into cells where any same-cell pair automatically satisfies it;
3. compare the number of points with the number of cells;
4. assign boundary points consistently.

## 5. Extremal choice

Sometimes boxes are unnatural. In a finite configuration choose a smallest, largest, nearest, or farthest admissible object and exploit what its extremality forbids.

Suppose a finite set of real numbers is closed under taking the midpoint of any two distinct members. If there were two distinct members, choose the closest pair `x<y`. Their midpoint lies in the set and is closer to each endpoint than `y-x`, contradicting the choice. Thus the set has only one member.

The method is:

`CHOOSE EXTREME OBJECT -> PRESERVE CONSTRAINTS -> PRODUCE STRICT IMPROVEMENT -> CONTRADICTION`

Naming the smallest object is not enough; the proof must use the no-improvement property.

## 6. Mandatory contrasts

### Pigeonhole vs inclusion-exclusion

Pigeonhole answers an existence question: **must some collision occur?** Inclusion-exclusion answers an exact counting question with overlaps: **how many outcomes satisfy at least one property?** Do not use overlap machinery when capacity already proves existence, and do not expect pigeonhole to compute an exact union size.

### Extremal choice vs inequality optimization

Extremal choice selects an object from a finite configuration and uses the fact that no admissible object can be more extreme. Inequality optimization bounds a numerical expression over a continuous or algebraic domain. The words maximum/minimum alone do not decide the method.

### Counting average vs structural inevitability

An average is a numerical summary. Pigeonhole uses the stronger discrete statement that if every box stayed below a threshold, the total capacity would be insufficient.

## 7. Historical anchor: extremal complement

For `IOQM-2023-Q27`, the universe contains 4845 increasing quadruples. Exactly 525 are balanced, leaving 4320 unbalanced. A chosen family of 4411 therefore forces at least `4411-4320=91` balanced members. The first move is to maximize the bad class globally, not inspect the chosen family one member at a time.

## 8. Historical anchor: local crossing cap to global density

For `IOQM-2023-Q18`, a local condition says each selected diagonal of a convex 50-gon crosses at most one other selected diagonal. The successful representation is a sparse crossing graph/drawing. Teacher-side source analysis gives the tight upper bound 71 and a matching construction. The learner lesson is to translate a local restriction into a global extremal structure before greedy addition.

## 9. Adopt the router

When a problem asks what **must** happen, ask:
- What are the objects?
- What boxes make the desired relation automatic after a collision?
- What capacity would failure impose?
- If boxes do not simplify the problem, which extreme object has a useful no-improvement consequence?
- Is the task actually an exact count or a continuous inequality optimum instead?

Write the structural first line before doing arithmetic.
