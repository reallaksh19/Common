# Divisibility, GCD and LCM - Assimilation Book

This book is for a learner who can usually calculate HCF/LCM but is not yet reliable at choosing **why** gcd, lcm, subtraction or Euclid should be the first move.

The target is not a longer formula list. It is a decision habit:

`TARGET -> DIVISOR/MULTIPLE -> DIFFERENCE/REDUCTION -> GCD/LCM -> CHECK`

## 1. RECONNECT - what is already familiar?

You probably know statements such as:

- `12|60`;
- `gcd(84,126)=42`;
- `lcm(12,18)=36`;
- digit tests for divisibility by 2, 3, 5, 9 or 11.

Those are useful, but an olympiad problem often hides the important divisibility relation inside words or algebra.

### First diagnostic - do not calculate fully

Write only the first thought.

1. Greatest integer that gives the same remainder when dividing 173 and 239.
2. Least positive integer divisible by 12, 15 and 18.
3. Compute `gcd(987,610)` efficiently.
4. A number leaves remainder 7 on division by 12, 18 and 30; find the least possible number above 7.
5. `gcd(a,b)=6`, `lcm(a,b)=180`; the question asks only for `ab`.

The intended starts are: **difference**, **lcm**, **Euclid**, **subtract 7 then lcm**, **product invariant**.

If one of these starts felt surprising, that is the bridge this book builds.

---

## 2. DISCOVER - divisibility is an equation, not a symbol trick

`a|b` means:

> there is an integer `k` such that `b=ak`.

This translation is the source of nearly every structural move in this topic.

If `d|A` and `d|B`, write `A=dm`, `B=dn`. Then for any integers `r,s`,

`rA+sB = d(rm+sn)`.

So `d` divides every integer linear combination of `A` and `B`.

### Why this is stronger than a divisibility test

A divisibility test answers a local question such as "is 7425 divisible by 9?" It reads the digits of one number.

Structural divisibility answers a different kind of question: "what must divide both `4n+7` and `7n+13`?" There is no useful digit test because `n` is unknown. Instead, combine the expressions:

`7(4n+7)-4(7n+13) = -3`.

Any common divisor of the two expressions must divide 3.

### Contrast 1 - test or structure?

- `7425` divisible by 9? -> a digit-sum test is cheap.
- `d|(4n+7)` and `d|(7n+13)` -> take a linear combination; a digit test has no role.

**Decision question:** is the task about one displayed integer, or about a relation that must survive for variable expressions?

---

## 3. MAKE SENSE - subtraction preserves common divisors

Suppose `d` divides both `a` and `b`. Then it divides `a-b`. Conversely, if `d|b` and `d|(a-b)`, then `d|a`.

Therefore the common divisors of `(a,b)` are exactly the common divisors of `(b,a-b)`, so

`gcd(a,b)=gcd(b,a-b)`.

More generally, for any integer `q`,

`gcd(a,b)=gcd(b,a-qb)`.

This is the invariant behind the Euclidean algorithm.

### Euclid as repeated compression

For `gcd(987,610)`:

`987 = 1*610 + 377`

so

`gcd(987,610)=gcd(610,377)`.

Continue:

`610=1*377+233`

`377=1*233+144`

`233=1*144+89`

and so on. The pair gets smaller while the common-divisor set stays unchanged.

### Contrast 2 - Euclid or factor everything?

- If the numbers factor instantly, factorization may be fine.
- If the pair is large but division gives small remainders, Euclid is usually the cheaper route.

The question is not "which method is legal?" Both may be legal. The question is "which method exposes the invariant with the least work?"

---

## 4. MAKE SENSE - same remainder means differences

If `a` and `b` leave the same remainder `r` when divided by `d`, then

`a=dq+r`, `b=dp+r`.

Subtract:

`a-b=d(q-p)`.

Therefore

`d|(a-b)`.

For several numbers, the common divisor must divide all relevant differences.

### Example - unknown divisor

Find the greatest integer that leaves the same remainder when dividing 173 and 239.

The divisor must divide

`239-173=66`.

The greatest possible divisor is 66. Check:

`173=2*66+41`, `239=3*66+41`.

### Example - three numbers

Find the greatest integer giving the same remainder on 221, 323 and 425.

Adjacent differences are both 102, so the greatest divisor is

`gcd(102,102)=102`.

### Contrast 3 - gcd of numbers or gcd of differences?

- "divides all the numbers" -> gcd of the numbers.
- "leaves the same remainder on all the numbers" -> gcd of differences.

The visible numbers are the same kind of objects, but the words change the first line.

---

## 5. DISCOVER - prescribed remainder is a different problem

Now reverse the unknown.

Suppose **the number `N` is unknown**, but the remainder `r` is prescribed when `N` is divided by several divisors.

If `N` leaves remainder `r` on division by 12, 18 and 30, then

`N-r`

is divisible by all three. So `N-r` is a common multiple of 12, 18 and 30.

For the least such `N>r`,

`N = r + lcm(12,18,30)`.

For `r=7`, this gives

`N=7+180=187`.

### Contrast 4 - the crucial same-remainder fork

- **Unknown divisor, equal remainders from given numbers** -> subtract the given numbers; use gcd of differences.
- **Unknown number, prescribed remainder for given divisors** -> subtract the remainder from the unknown; use a common multiple/lcm.

Do not use the phrase "same remainder" alone as a method label. Ask **what is unknown?**

---

## 6. MAKE SENSE - LCM is the least synchronization point

A common multiple is reached by every given divisor. The lcm is the smallest positive one.

Typical clues:

- least positive integer divisible by several numbers;
- first time several cycles coincide again;
- smallest number satisfying several "is a multiple of" conditions;
- prescribed-remainder reconstruction after subtracting the remainder.

### Example - synchronization

Two alarms ring every 12 and 18 minutes. Starting together, they next ring together after

`lcm(12,18)=36`

minutes.

### Contrast 5 - largest step or first common time?

- greatest step size that fits several distances exactly -> gcd;
- first time several cycles meet -> lcm.

The words "greatest" and "least" are not enough by themselves. Determine whether the object sought is a **divisor** or a **multiple**.

---

## 7. MAKE SENSE - gcd and lcm carry reconstruction information

For positive integers `a,b`,

`gcd(a,b)*lcm(a,b)=ab`.

A useful normalization is

`a=gu`, `b=gv`, where `g=gcd(a,b)` and `gcd(u,v)=1`.

Then the lcm is `guv`, so if `L=lcm(a,b)`,

`uv=L/g`.

This separates a shared gcd from a coprime core.

### If only the product is requested

If `gcd(a,b)=6` and `lcm(a,b)=180`, then immediately

`ab=6*180=1080`.

Do not reconstruct `a` and `b` if the question never asks for them.

### If the pair is requested

If `g=12`, `L=420`, then

`uv=L/g=35` and `gcd(u,v)=1`.

The unordered coprime factor splits of 35 are `(1,35)` and `(5,7)`, giving

`(a,b)=(12,420)` or `(60,84)` up to order.

This is **reconstruction**, not just the product identity.

### Contrast 6 - invariant or reconstruction?

- target `ab` -> stop at `ab=gL`;
- target the actual pair(s) -> normalize, use `uv=L/g`, and enforce coprimality.

---

## 8. MAKE SENSE - divisibility chains compress several conditions

If

`a|b` and `b|c`,

then `a|c` because `b=am` and `c=bn` imply `c=a(mn)`.

This transitivity gives immediate gcd/lcm facts:

If `a|b`, then

`gcd(a,b)=a`, `lcm(a,b)=b`.

If `a|b|c`, then

`gcd(a,b,c)=a`, `lcm(a,b,c)=c`.

### Example - an unknown inside a chain

Suppose `6|x` and `x|72`.

Do not treat these as unrelated tests. Write

`6|x|72`.

So `x` must be a divisor of 72 that is also a multiple of 6. The chain is the organizing representation.

### Contrast 7 - chain or separate checking?

When one divisibility relation feeds another, transitivity may remove whole branches of work. Independent checking is useful only after the chain has been compressed.

---

## 9. TRY - attempt before help

For each problem, make a first attempt **before** reading any support. If stuck, use the fullest support first; on later problems, work with progressively less support until you can solve independently.

### Problem A

Find the greatest integer that leaves the same remainder when dividing 437, 581 and 725.

**Full support:** compute the differences `581-437` and `725-581`, then take their gcd.

**Structural prompt:** an unknown common divisor must divide every difference.

**Recognition prompt:** equal remainders disappear under subtraction.

**Independent target:** later problems give no support.

Answer: `144`.

### Problem B

Find the least `N>9` that leaves remainder 9 when divided by 12, 15 and 20.

**Full support:** `N-9=lcm(12,15,20)` for the least solution.

**Structural prompt:** remove the prescribed remainder so that every divisor divides the same number.

**Recognition prompt:** the unknown is the number being constructed, not the divisor.

**Independent target:** later problems give no support.

Answer: `69`.

### Problem C

Compute `gcd(2025,748)`.

**Full support:** repeatedly use `a=qb+r` and replace `(a,b)` by `(b,r)`.

**Structural prompt:** preserve the common-divisor set while shrinking the pair.

**Recognition prompt:** division with remainder is cheaper than full factorization here.

**Independent target:** later problems give no support.

Answer: `1`.

---

## 10. DIAGNOSE - tempting wrong moves

### Error A - "same remainder means lcm"

Why tempting: remainder construction often uses lcm.

Repair: ask **which object is unknown?** Unknown divisor -> differences/gcd. Unknown number with prescribed remainder -> subtract remainder/lcm.

### Error B - "gcd means factor both numbers"

Why tempting: school examples often teach HCF through prime factors.

Repair: choose a representation. Euclid can preserve the same gcd while making the numbers much smaller.

### Error C - "divisibility test solves every divisibility problem"

Why tempting: tests are memorable.

Repair: tests detect a property of one integer. Variable expressions and common-divisor conditions require structural algebra.

### Error D - using `gcd*lcm=ab` without deciding the target

Why tempting: the identity looks powerful.

Repair: if the pair itself is required, the product identity is only the first constraint; normalize and enforce `gcd(u,v)=1`.

### Error E - ignoring a divisibility chain

Why tempting: each condition looks separate.

Repair: write the chain first. Transitivity can make some conditions automatic.

---

## 11. ADOPT - the first-move rules

1. Translate `a|b` into `b=ak` when a proof or variable relation is hidden.
2. For a common divisor of expressions, take integer linear combinations.
3. For equal remainders with unknown divisor, subtract the given numbers.
4. For large gcd pairs, try Euclidean reduction before full factorization.
5. For least simultaneous divisibility, build an lcm.
6. For a prescribed remainder, subtract the remainder before building the lcm.
7. If gcd and lcm are both given, use `gL=ab`; reconstruct only if necessary.
8. Compress `a|b|c` as a chain before enumerating cases.

---

## 12. VALIDATED IOQM ANCHORS - source to mechanism

### IOQM-2025-Q02

The official item is a counting question about integers up to 100 divisible by 3 but not by 2. The structural move is to count multiples of 3 and remove those also divisible by 2, i.e. multiples of 6. The independently checked answer is 17.

Learning use: divisibility condition -> common-multiple overlap. This is not a claim that inclusion-exclusion belongs canonically to this topic; the counting machinery is a bridge.

### IOQM-2025-Q27

The official item asks for ordered positive integer triples under an equation involving two lcm terms. The first decisive conversion is

`lcm(x,c)=xc/gcd(x,c)`.

This turns the lcm equation into restrictions on gcd values and collapses the search to two symmetric families. The independently checked answer is 40.

Learning use: when lcm appears inside an algebraic relation, rewrite it through gcd structure before brute-force enumeration.

---

## 13. TRANSFER - same invariant, changed surface

### Representation change

"Several measurements have the same remainder when measured in units of length `d`." Translate to differences divisible by `d`.

### Context change

"Three machines reset every 18, 24 and 40 minutes." Translate to the first positive common multiple.

### Spacing change

"Marks are at positions 1001, 1457 and 1913 on a line. What is the largest equal step that lands on all marks after a common offset?" Translate to gcd of differences.

### Downstream modular bridge

A later modular-arithmetic chapter may write equal-remainder information with congruence notation. The underlying fact from this chapter remains `d|(a-b)`; the later chapter retrieves it rather than requiring this chapter to introduce its notation.

### Final self-check

Before calculating, can you state:

- the target object: divisor or multiple?
- the smallest useful representation?
- the first useful line?
- the nearby tempting route and why it is less direct?
- a final divisibility/remainder/coprimality check?

If yes, you are using the topic structurally rather than procedurally.
