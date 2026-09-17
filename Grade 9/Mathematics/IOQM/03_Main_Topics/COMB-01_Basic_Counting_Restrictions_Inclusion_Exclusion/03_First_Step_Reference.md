# Basic Counting - First-Step Reference

## One-question router

> **What is one counted object, and when are two objects the same?**

Then ask:

`ORDER? -> RESTRICTIONS? -> DISJOINT CASES OR STAGES? -> DIRECT / COMPLEMENT / IE -> CHECK`

## Recognition atlas

| Visible clue | First move |
|---|---|
| one choice followed by another | define stages; multiply stage counts |
| one of several nonoverlapping types | prove disjointness; add case counts |
| roles/sequence/positions | treat as ordered unless the problem identifies orders |
| committee/subset/group | treat as unordered unless roles are later assigned |
| repeated symbols | divide labelled count by permutations of identical copies |
| last/first digit restriction | handle the restricted position first |
| at least one / not all | test whether complement is shorter |
| two properties joined by “or” | check overlap before adding |
| multiple overlapping restrictions | consider inclusion-exclusion |
| digit condition | decide whether arithmetic property is given or must be derived |

## Exact-one case test

Before adding branches:
1. Every valid object belongs to at least one branch.
2. No valid object belongs to two branches.

If either fails, repair the split before counting.

## Identity test

Before dividing by a factorial, state exactly which labelled arrangements become the same visible object.
