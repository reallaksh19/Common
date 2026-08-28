# Combinatorics Concept Book Specification v1

## Cognitive contract

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Preliminary mastery target:

`OBJECT -> RESTRICTION -> REPRESENTATION -> COUNT -> OVERLAP CHECK -> TRANSFER`

The student should finish this unit believing:

> I do not choose `nPr` or `nCr` because I see the word “arrange” or “choose.” I first define exactly what one outcome is and whether order matters.

---

# Unit architecture

## Unit 0 — Diagnostic

Check without hints:

- multiplication and addition principles;
- simple factorial arithmetic;
- ordered vs unordered outcomes;
- basic digit restrictions;
- simple set overlap;
- parity/divisibility constraints.

## Unit 1 — What exactly is one outcome?

### SEE
Compare:

- choose two students for a team;
- choose a captain and vice-captain;
- choose two digits for a two-digit number.

### REALIZE
The same underlying objects can generate different sample spaces depending on roles/order.

### UNDERSTAND
Define an outcome before counting it.

### ADOPT
For mixed prompts, state whether the outcome is an ordered tuple, unordered subset, word/string, path, configuration or integer solution.

---

## Unit 2 — Addition and multiplication principles

### SEE
A meal has 3 mains and 4 drinks.

### REALIZE
Independent sequential choices multiply.

If a result can arise through mutually exclusive cases, case totals add.

### CONTRAST
Do not add sequential independent choices. Do not multiply disjoint alternatives.

---

## Unit 3 — Permutations and combinations from structure

### SEE
From `n` distinct objects choose `r` positions.

### REALIZE
Ordered selection creates a falling product; unordered selection counts each selected group `r!` times under all internal orders.

### UNDERSTAND
Derive:

`nPr = n!/(n-r)!`

`nCr = n!/[r!(n-r)!]`

from counting, not memorization.

### ADOPT
Ask first: “If I swap the chosen objects, did I create a new outcome?”

---

## Unit 4 — Restricted arrangements and digit counts

Teach:

- no leading zero;
- parity from last digit;
- divisibility filters;
- repeated vs distinct digits;
- adjacency/separation restrictions;
- complement counting when the forbidden condition is easier.

PYQ bridge: `NMTC-BH-P-2025-Q21`.

---

## Unit 5 — Casework: disjoint and exhaustive

### SEE
Count integers/configurations satisfying several possible structural types.

### REALIZE
Good casework is a partition: no overlap, no omissions.

### UNDERSTAND
Use a case table with:

- case definition;
- count;
- why cases cannot overlap;
- why all possibilities are covered.

PYQ evidence includes 2019 geometric classification and exceptional-case enumeration.

---

## Unit 6 — Subsets and product expansions

### SEE
Expand `(1+a)(1+b)(1+c)`.

### REALIZE
Choosing either `1` or the variable term from each factor corresponds to choosing a subset.

### UNDERSTAND
The sum of products over all subsets is represented by a product expansion. Excluding the empty subset subtracts 1.

PYQ anchor: `NMTC-BH-P-2019-Q07`.

---

## Unit 7 — Coefficient as a counting question

### SEE
Coefficient of `x^k` in a product of finite geometric sums.

### REALIZE
Each term chosen from each factor contributes an exponent; the target coefficient counts exponent tuples satisfying a sum equation within bounds.

### UNDERSTAND
Translate coefficient extraction into integer-solution counting before doing algebraic expansion.

PYQ anchor: `NMTC-BH-P-2019-Q30`.

---

## Unit 8 — State/path counting

### SEE
A token makes restricted moves for exactly `m` steps.

### REALIZE
The count depends on current state and remaining steps.

### UNDERSTAND
Define states and recurrence/dynamic count; do not list raw paths when state compression is available.

Historical 2019 Q23 remains figure-gated; use author-created text-complete grids for teaching.

---

## Unit 9 — Pigeonhole principle

### SEE
Place more objects than boxes.

### REALIZE
Some box must receive multiple objects.

### UNDERSTAND
Basic form: if `N` objects enter `k` boxes, some box has at least `ceil(N/k)` objects.

Teach design of the boxes: residues, intervals, birthdays/months, last digits, parity classes, distance bins.

### WRONG MOVE
Merely saying “by pigeonhole” without identifying pigeons and boxes.

---

## Unit 10 — Inclusion–exclusion

### SEE
`|A|+|B|` double-counts `A∩B`.

### REALIZE
Overlap must be corrected.

### UNDERSTAND
For two sets:

`|A∪B|=|A|+|B|-|A∩B|`.

For three sets, add singles, subtract pairwise intersections, add triple intersection.

Use divisibility-counting and survey-style examples before abstract notation.

---

## Unit 11 — Complement counting

Use when “at least one”, “not all”, “avoid forbidden pattern” or “contains a repeated property” is easier through total minus none.

---

## Unit 12 — High-ceiling representations

Introduce only after core mastery:

- balanced signed representations;
- coefficient/exponent-pair counting;
- subset-product identities;
- state-recursion counts.

`NMTC-BH-P-2019-Q28` is evidence of ceiling, not a prerequisite entry problem.

---

# Error-check laboratory

Mandatory contrasts:

1. permutation vs combination;
2. multiplication vs addition principle;
3. overlapping vs disjoint cases;
4. leading-zero trap;
5. repeated-object overcount;
6. complement vs direct counting;
7. coefficient as algebra vs coefficient as count;
8. pigeonhole boxes chosen too coarsely/fine;
9. inclusion–exclusion sign order;
10. source/key conflict rather than forced reconciliation (`NMTC-BH-P-2023-Q25`).

# Mastery standard

Student is ready for mixed Preliminary use only if they can:

- classify at least 8/10 unseen counting structures correctly;
- write the sample-space object before computation;
- solve direct permutation/combination restrictions without formula-selection errors;
- produce disjoint exhaustive casework;
- solve one pigeonhole and one inclusion–exclusion transfer problem;
- interpret one coefficient as a count;
- solve one subset/product or state-count bridge;
- detect at least one deliberately conflicting source/key example without forcing the key.
