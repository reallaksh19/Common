# Mathematics V2 — Core (2A): cited challenge practice

Core (2) remains the governed semantic transfer plan over the **original source questions**. Core (2A) now has two learner-product lanes:

```text
Core (1) + Core (1A) + Core (2)
              +
verified competitive-question archives / archetypes
              ↓
Core (2A)
   ├── SOURCE lane: realize original Core (2) questions faithfully
   └── CHALLENGE lane: add fresh, grounded competitive-style questions
              ↓
core2a_challenge_plan.json
core2a_quality_audit.json
core2a_student_challenge_practice.pdf
```

The competitive corpus influences **question design and reasoning demand**, not curriculum authority. A generated challenge may only require mathematics already taught or explicitly approved upstream.

## Source lane — immutable Core (2)

For every `SOURCE_CORE2` question Core (2A) preserves:

- original source-question order;
- source stem, givens, options, units and subparts;
- source question identifier;
- Core (1) linkage state;
- assessment-safety classification;
- multiple-solution / underdetermined semantics;
- source corrections and notes;
- attempt before support and worked solution;
- immediate attempt → worked adjacency where that is the approved page contract.

Fresh challenge questions must never replace, renumber or silently rewrite a Core (2) source question.

## Challenge lane — fresh competitive practice

`GENERATED_CHALLENGE` questions may be added after or around preserved source anchors when they are grounded in:

```text
Core (1) mathematical authority
+ Core (1A) teaching buckets / representations
+ Core (2) source-question demand
+ verified JEE / IOQM / RMO / INMO / IMO-style benchmark material
```

Generated questions must be mathematically fresh. Official archives may be used to benchmark style, compactness, inference depth, representation shifts and synthesis demand, but an original generated question must not be presented as an official historical exam question.

Difficulty must come from mathematical thinking — hidden structure, reversed targets, representation shifts, mixed ideas or deeper inference — not merely larger numbers or uglier arithmetic.

## Citation contract — shown with the question itself

Every Core (2A) question must carry a learner-visible box labelled:

```text
WHERE THIS QUESTION CAME FROM
```

The citation belongs **on the question page itself**. A consolidated source list at the end is not sufficient.

For source questions, the inline note identifies the exact Core (2) source question and locator.

For fresh challenge questions, the inline note must distinguish:

- the Core (1) / Core (1A) concept being practised;
- any Core (2) source question used as the transfer anchor;
- the official competitive archive used only as a style/demand benchmark;
- the fact that the wording and mathematical instance are original to the workbook.

The canonical contract is:

`Core2A/contracts/math-core2a-challenge-plan.schema.json`

and requires `question_citation_policy = INLINE_WITH_EACH_QUESTION`.

## Learner-facing help language

Internal pipeline language must not appear in the learner product. Use stable child-friendly labels:

```text
TRY IT FIRST
SMALL CLUE
BIGGER CLUE
HOW DO I START?
THINK IT THROUGH
FULL WORKING
QUICK CHECK
WHERE THIS QUESTION CAME FROM
```

Do not expose internal terms such as `reasoning route`, `repair route`, `grounding`, `learning atom`, `demand vector`, `transfer ladder`, registry IDs or publication-engineering terminology.

The underlying semantic objects can remain technical internally; only the learner-facing surface is constrained here.

## Help progression

Core (2A) keeps the Core (2) H1/H2/H3 semantics but translates them for the learner:

```text
H0  TRY IT FIRST
H1  SMALL CLUE       — notice the useful structure
H2  BIGGER CLUE      — choose the mathematical idea / representation
H3  HOW DO I START?  — first executable mathematical move
```

After the clues, `THINK IT THROUGH` explains the strategy without hiding the key reasoning, then `FULL WORKING` executes the algebra/arithmetic, and `QUICK CHECK` verifies the result independently where appropriate.

## Core (1A) relationship

Core (1A) teaches the concept and representation. Core (2A) asks the learner to recognize and use that concept under less obvious conditions.

```text
Core (1A) bucket
     ↓
Core (2) source anchor
     ↓
fresh near challenge
     ↓
reversed / hidden-form challenge
     ↓
mixed or competitive-style challenge
```

A challenge must fail closed if it requires a capability that is not taught or otherwise approved upstream.

## Release and source integrity

Core (2A) inherits source legality and learner-state authority from upstream products. It cannot:

- upgrade provisional PCK;
- alter assessment validity;
- invent learner readiness;
- bypass human gates;
- claim a generated question is an official JEE/IOQM/RMO/INMO/IMO item without a verified exact source;
- use a competition citation without saying whether it is exact source text or style-only benchmarking.

## Required fail-closed checks

At minimum:

```text
CORE2A_SOURCE_ORDER_DRIFT
CORE2A_SOURCE_STEM_DRIFT
CORE2A_QUESTION_ID_DRIFT
CORE2A_ATTEMPT_SOLUTION_ADJACENCY_LOST
CORE2A_HINT_DISCLOSES_SOLUTION
CORE2A_SOLUTION_DEPTH_COLLAPSED
CORE2A_VERIFICATION_LOST
CORE2A_CORE1_LINK_DRIFT
CORE2A_ASSESSMENT_SAFETY_LOST
CORE2A_MULTI_SOLUTION_COLLAPSED
CORE2A_UNTAUGHT_MATH_REQUIRED
CORE2A_QUESTION_CITATION_MISSING
CORE2A_CITATION_NOT_INLINE
CORE2A_GENERATED_ITEM_FALSE_OFFICIAL_ATTRIBUTION
CORE2A_COMPETITION_SOURCE_ROLE_UNCLEAR
CORE2A_LEARNER_JARGON_LEAK
CORE2A_QUALITY_GATE_FAILED
```
