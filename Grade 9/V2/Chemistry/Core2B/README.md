# Chemistry Core2B — Elicitation-First Problem-Solving Self-Tutor

Core2B is a **static learner-facing self-tutoring product** downstream of Core2A legality, Chemistry transfer eligibility and LearningBlueprint v4 learner conditioning. Core2A remains the authority for question legality, source/generated identity, provenance, answer custody, challenge validation and taught-scope closure.

## v4 learner conditioning is mandatory

Core2B compilation must resolve exactly one of:

```text
KNOWLEDGE_PERCENT
OWNER_OVERRIDE
```

### KNOWLEDGE_PERCENT

`0..100` is a **support prior, not a mastery score**. The v4 policy maps it to a compile-time support profile controlling:

- support density;
- hint entry level;
- representation support;
- first-move support;
- solution delay.

It must not change the frozen question, source provenance, validated Chemistry scope or answer authority.

### OWNER_OVERRIDE

When knowledge percentage is unknown, the owner may waive it only with an explicit reason plus auditable support and demand profiles. No fake percentage is synthesized.

```text
no knowledge %
+ no owner override
= BLOCK
```

## Purpose

Core2A demonstrates and supports legal problem solving. Core2B withholds the method label and asks the learner to select the appropriate Chemistry before progressively revealing only the support authorized by v4.

Core2B does **not** generate a harder replacement question. It selects an already-legal item and changes the learner experience around that item.

## Attempt-first grammar

```text
SOURCE / PROVENANCE
QUESTION
large workspace

H0 ATTEMPT WITHOUT HELP

CONDITIONED HELP LADDER
H1 ORIENT
H2 STRUCTURE
H3 REPRESENTATION
H4 PRINCIPLE
H5 FIRST_MOVE
H6 PARTIAL_PATH
H7 FULL_SOLUTION
H8 VERIFY_REFLECT
```

The complete authored ladder remains in the governed input, but the learner-visible entry point is compiled from the v4 support profile. A high-support profile may begin at H1; a minimal-support profile may defer early hints and begin at H4. `solution_delay` can keep the full solution on a separate page until after a full attempt.

This is compile-time/static conditioning. The PDF does not observe learner answers and does not adapt while being used.

## Authority custody

For a source item Core2B preserves exactly:

- item ID;
- source locator;
- source stem/options/subparts;
- source-vs-generated classification;
- provenance;
- canonical answer / marking authority;
- existing Core2A legality.

If the desired transfer form is absent from the Core2A-legal pool, Core2B records a gap. It may not invent a replacement question.

## Difficulty and demand

The existing difficulty vector can record conceptual novelty, representation distance, method visibility, discrimination, step depth, information structure, reversal, synthesis, calculation burden and time pressure.

Learner conditioning controls **support**. Owner purpose/demand controls **transfer demand** within existing legality. These axes must not be conflated.

## Outputs

The reference compiler emits:

```text
core2b_plan.json
chemistry_core2b.pdf
core2b_quality_audit.json
```

The plan/audit record conditioning mode and resolved support profile. A knowledge-percent product records the supplied percentage with the interpretation `SUPPORT_PRIOR_NOT_MASTERY_MEASUREMENT`; an owner-waiver product records no fabricated percentage.

The first goldens validate:

1. `U2Q35` with `knowledge_percent = 50`, resolving to MEDIUM support;
2. `U2Q29A` with an explicit owner waiver, LOW support and full-solution delay to a later page.
