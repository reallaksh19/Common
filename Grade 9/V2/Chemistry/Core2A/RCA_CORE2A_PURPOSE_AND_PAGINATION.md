# RCA — Core (2A) purpose, pagination, construction quality and competition benchmarking

## Failure observed

The first Chemical Bonding Core (2A) prototype was fundamentally mis-specified. It treated the sequence

```text
ATTEMPT -> CLUES -> QUICK CHECK -> FULL WORKING
```

as four physical pages for every question. This inflated the product and, more importantly, made Core (2A) behave like Core (2) again with more scaffolding and more pages.

A second defect was exposed by review of the first competition rewrite: although the page count was reduced, the learner surface still contained repetitive slogans, oversized generic workspace, generic “governing invariant” boxes, generic verification prose, and repeated provenance disclaimers. Competition-question construction had also not been benchmarked against external authoritative competition papers before fresh questions were authored.

## Root causes

1. **Purpose was not resolved before authoring.** The pipeline knew which product to render but not why the learner wanted it.
2. **Pedagogical states were confused with physical pages.** Attempt, clue, check and solution do not each require a page.
3. **Workspace was template-driven rather than demand-driven.** Simple one-line deductions received the same large working area as multi-step items.
4. **Support was mechanically complete but not technically selective.** Generic start rules and generic repair slogans occupied space without increasing Chemistry reasoning value.
5. **Answer-page sidebars were generic.** “The formula unit is neutral” is true but substandard if the current question needs the explicit equation `2q_X + 3(-2)=0`.
6. **Competition construction lacked external benchmarking.** Fresh questions were generated only from internal source anchors/problem families rather than first studying official school-science competition question forms.
7. **Machine closure was allowed to dominate learner efficiency.** The invariant `QUESTION = QUICK CHECK = FULL WORKING` is correct, but it does not dictate a four-page or boilerplate-heavy layout.

## Correct product rule

Before Core (2A) authoring, resolve exactly one purpose:

```text
STARTER
PRACTICE
REVISION
COMPETITION
```

If unresolved, ask the user and fail closed with:

```text
CORE2A_PURPOSE_UNRESOLVED
```

The selected mode must materially alter selection, support density, challenge mix, workspace and page density.

## Competition-mode construction research

Before fresh Competition questions are authored, inspect at least two authoritative or official external school-science competition sources. Extract only construction patterns such as:

- particle-composition tables;
- multi-statement items;
- coded-species deduction;
- reverse ion/electron inference;
- integer reconstruction;
- plausible-error diagnosis;
- information supplied inside the problem so a harder deduction remains self-contained.

Do not copy question text. The near-copy gate remains mandatory. Store benchmark URLs or stable references in machine custody. Prefer a single book-level construction-reference note rather than repeated per-question disclaimers.

Failure code:

```text
CORE2A_COMPETITION_CONSTRUCTION_RESEARCH_MISSING
```

## Correct pagination rule

Default static-PDF contract:

```text
1 learner question <= 2 physical pages
```

Preferred realization:

```text
PAGE 1 — ATTEMPT
question
+ demand-sized workspace
+ 1–2 technical clues at the bottom, only if needed

PAGE 2 — CHECK AND SOLUTION
QUICK CHECK
+ FULL WORKING
+ KEY RELATION / DECISION RULE instantiated with the current symbols/numbers
+ independent CONSISTENCY CHECK
```

A clue state is not automatically a clue page. A workspace is not automatically a full-page blank area. Any exception above two pages requires a specific reason.

## Learner-language quality guards

For Competition mode:

- generic “competition start rule” blocks are forbidden;
- repeated “not an official past question” footers are forbidden;
- generic “repair the earliest broken step” footers are forbidden;
- generic “governing invariant” sidebars are forbidden;
- technical clues must name the next executable equation, count, comparison or falsification test;
- the key relation must apply to the current question values/symbols;
- the consistency check must independently recompute or falsify the current result.

## Answer closure remains unchanged

Compression does not weaken self-study closure:

```text
closed QUESTION = QUICK CHECK = FULL WORKING
open QUESTION = EXPECTED RESPONSE RUBRIC
```

## Architectural distinction

```text
Core (2)  = source-question helper authority
Core (2A) = purpose-specific learner transfer product
```

Core (2A) is defective if changing from Core (2) only increases scaffolding or page count without materially changing learner behaviour.
