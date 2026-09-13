# RCA — Core (2A) purpose collapse and pagination inflation

## Incident

A Chemical Bonding Core (2A) prototype was realized as a four-surface sequence for every question:

```text
ATTEMPT
→ CLUES
→ QUICK CHECK
→ FULL WORKING
```

Those pedagogical states were incorrectly mapped one-to-one onto physical pages. The result was a very large book whose source-question lane substantially duplicated Core (2). The product was mechanically complete but conceptually weak: it did not first resolve why the learner wanted Core (2A).

## Root cause

The pipeline treated **product requested = Core (2A)** as sufficient intent. It was not sufficient.

Core (2) already owns source-faithful question-help. A downstream Core (2A) that repeats the same questions with more scaffolding and more pages can collapse into "Core (2) again" instead of becoming a distinct learner product.

The failure had four coupled causes:

1. **Purpose was unresolved.** The learner intent was not classified as `STARTER`, `PRACTICE`, `REVISION`, or `COMPETITION` before authoring.
2. **Reveal state was confused with page state.** Hidden/revealed support states were automatically given separate sheets.
3. **Workspace was template-sized rather than demand-sized.** Simple MCQs and multi-step constructed responses received similar physical working areas.
4. **Machine closure drove layout.** `QUESTION = QUICK CHECK = FULL WORKING` is an answerability invariant, not a requirement for three or four physical pages.

## Corrective contract

Core (2A) authoring must stop and ask the user for the intended mode when it is not explicitly supplied:

```text
STARTER
PRACTICE
REVISION
COMPETITION
```

The agent may not silently infer the mode.

Failure code:

```text
CORE2A_PURPOSE_UNRESOLVED
```

The governing policy is:

`policies/chemistry-core2a-purpose-and-pagination-policy.json`

## Purpose changes the product

### STARTER

High scaffolding, smaller progression, partially completed starts, representations and misconception prevention.

### PRACTICE

Independent routine practice with modest rescue support and enough workspace for the actual demand.

### REVISION

Compressed retrieval, fast checking, common-error repair and high question density. Minimal re-teaching.

### COMPETITION

Fresh source-anchored transfer with minimal upfront help, reversed targets, hidden information, multi-constraint chains, comparison/ranking, error diagnosis and representation switching. Difficulty comes from reasoning, not unsupported higher-grade theory or uglier arithmetic.

Competition mode must not default to rendering every Core (2) source question as another helper book.

## Pagination correction

Default physical budget:

```text
1 learner question <= 2 pages
```

Preferred static-PDF pair:

```text
PAGE 1 — ATTEMPT
question + mode-appropriate metadata/support + demand-sized workspace

PAGE 2 — CHECK AND REPAIR
compact QUICK CHECK + FULL WORKING + independent verification + provenance
```

A dedicated clue page is not the default. A dedicated blank working page is not the default. Any exception above two pages requires an explicit reason such as an unusually complex source figure or a genuinely long multi-part response.

Failure code:

```text
CORE2A_PAGE_BUDGET_EXCEPTION_UNJUSTIFIED
```

## Answer closure remains unchanged

Compression must never remove the self-study answer path.

For closed questions:

```text
QUESTION
= QUICK CHECK
= FULL WORKING
```

For genuinely open responses:

```text
QUESTION
= EXPECTED RESPONSE RUBRIC
```

## Chemical Bonding competition correction

The corrected competition realization uses Core (2) only as source/coverage authority. It does **not** duplicate the 38 source questions. Instead it builds 21 fresh competition-foundation transfers, three for each of the seven Core (1A) assimilation buckets, and uses exactly two physical pages per question:

```text
21 ATTEMPT pages
+ 21 CHECK_AND_REPAIR pages
```

This preserves the distinction:

```text
Core (2)  = source-question helper
Core (2A) = purpose-specific transfer product
```

## Prevention

Future agents must resolve purpose before selecting questions, support density, challenge mix, workspace and pagination. A Core (2A) candidate that is effectively Core (2) with more pages should be rejected as:

```text
CORE2A_BECOMES_CORE2_WITH_MORE_PAGES
```
