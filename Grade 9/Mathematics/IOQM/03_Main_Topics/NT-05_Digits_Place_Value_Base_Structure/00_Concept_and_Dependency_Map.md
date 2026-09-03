# Concept and Dependency Map - Digits, Place Value & Base Structure

## Governing learner router
`DIGIT STRING -> PLACE-VALUE EQUATION -> ARITHMETIC RESTRICTION -> CARRY / DIVISIBILITY / FACTOR STRUCTURE -> COUNT ONLY IF ASKED`

## Scope boundary
Canonical here: decimal/base place value; divisibility by 9 and 11 derived from place value; concatenation; carry effects; digit sums/products; base representation; arithmetic restrictions on digits.

Retrieval only: generic modular legality/cycles from the frozen residue provider; basic counting after an admissible digit set is known from the frozen counting provider. The digit topic derives the restriction; the counting topic counts strings satisfying it.

## Knowledge dependency map
| Need | Prior knowledge | Missing bridge | Disposition |
|---|---|---|---|
| read decimal digits | school place value | treat digit pattern as algebra | owned here |
| divisibility 9/11 | memorized tests | derive from powers of 10 | owned here |
| modular reduction | remainder arithmetic | use only after place-value equation exists | retrieve |
| concatenation | visual joining | block shift `10^k x+y` | owned here |
| carries | column addition | exact digit-sum change | owned here |
| digit product | multiplication | prime-overlap restrictions | owned here; retrieve prime facts if needed |
| base notation | informal exposure | polynomial in the base | owned here |
| count strings | permutations/combinations | arithmetic-to-counting handoff | retrieve counting owner |

## Method-selection map
| Surface | Boundary question | First move | Avoid |
|---|---|---|---|
| named digit string | what are the place weights? | expand numeral algebraically | pattern guessing |
| divisibility by 9 | can powers of 10 collapse? | replace each `10^k` by 1 mod9 | memorized test without reason |
| divisibility by 11 | what is `10 mod 11`? | alternate signs | random digit sums |
| concatenated blocks | how many digits in appended block? | `10^k x+y` | digit-by-digit expansion |
| n -> n+1 | how many trailing 9s? | `s(n+1)=s(n)+1-9t` | brute force |
| squarefree digit product | which prime exponents repeat? | classify allowed digit prime factors | numerical product search |
| numeral in base b | what are weights? | `sum d_i b^i` | read as decimal |
| arithmetic digit restriction + count request | is restriction already known? | hand off to counting | duplicate counting chapter |

## Transfer map
- decimal divisibility -> base-b polynomial evaluation;
- repeated blocks -> algebraic factors such as 101,1001;
- carry chains -> digit-sum jumps;
- squarefree digit products -> prime compatibility graph on digits;
- place-value equation -> combinatorial counting after restrictions are frozen.

## Prerequisite interface custody
- NT-02 residue/cycle interface blob `2b5c4fb1b693e1f881068ec51104d36ca46846e7`.
- COMB-01 counting/model interface blob `c4d80bfeed3bca5d2b9cc3bd02b1a92fa7b66152`.
- NT-03 prime-exponent facts may be retrieved only when a digit-product restriction needs squarefree language.

Static architecture state: WAVE0_ARCHITECTURE_FROZEN.
