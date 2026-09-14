# Chemistry Core1B / Core2B — Static Self-Tutor Product Kit

This kit is stacked on **Chemistry LearningBlueprint v4** and does not redefine bucket depth or learner conditioning locally.

```text
LearningBlueprint v4
├─ Core1 bucket authority
│    intrinsic EASY / MEDIUM / HARD
│    page-envelope ceiling
│    research obligation
│    visual reasoning jobs
│    decomposition decision
│
└─ Core2 learner conditioning
     KNOWLEDGE_PERCENT or OWNER_OVERRIDE
     resolved support profile
     demand profile when owner-overridden

          ↓
Core1B / Core2B static learner products
```

Core1A and Core2A remain upstream learner-product authorities and are not modified by this kit.

## Governing distinction

```text
Core1A = exposition-first deep teaching
Core1B = elicitation-first conceptual self-tutoring

Core2A = exposition-rich legal problem practice
Core2B = elicitation-first problem-solving self-tutoring
```

All products are static. `OPEN_ENDED` means the learner is asked to think before help is revealed; it does not mean answers are absent.

## Core1B — v4 bucket realization

Core1B asks:

> Can the learner reconstruct, explain, compare, correct and generalize Chemistry that Core1A has already taught?

Every Core1B input must carry a v4 `instruction_bucket` and pass the upstream validator. Core1A/Core1B share the same bucket badge and knowledge graph.

```text
EASY   <= 10 pages, research optional
MEDIUM <= 20 pages, web research required
HARD   <= 30 pages, deep research required
```

These are ceilings, not quotas. Learner knowledge percentage is forbidden from controlling Core1 depth.

Core1B learner cycle:

```text
PREDICT -> REPRESENT -> EXPLAIN -> COMPARE -> CORRECT -> GENERALIZE
```

Released tasks contain an open-ended attempt, fixed progressive self-help, canonical/expected response, explanation and independent check.

## Core2B — v4 learner-conditioned realization

Core2B asks:

> Can the learner select and use the appropriate Chemistry when the problem surface no longer names the method or problem family?

Compilation requires exactly one v4 conditioning route:

```text
KNOWLEDGE_PERCENT 0..100
or
OWNER_OVERRIDE with explicit reason + support profile + demand profile
```

No unresolved/default 50% route exists.

Knowledge percentage is interpreted only as a **support prior**, controlling support density, hint entry, representation support, first-move support and solution delay. It cannot alter frozen question identity, provenance, validated semantic scope or answer authority.

Core2B authors the full ladder:

```text
H0 ATTEMPT
H1 ORIENT
H2 STRUCTURE
H3 REPRESENTATION
H4 PRINCIPLE
H5 FIRST_MOVE
H6 PARTIAL_PATH
H7 FULL_SOLUTION
H8 VERIFY_REFLECT
```

The v4 support profile determines which early hints are exposed and whether the full solution appears after the hint ladder or on a later page after a full attempt.

## Hard authority boundaries

1. Core1B may use only upstream-authorized capabilities, representations, problem families, misconceptions and Chemistry entities.
2. Core1B may not use learner knowledge to change bucket depth or page budget.
3. Core2B may select only items already legal under Core2A / transfer eligibility.
4. Core2B conditioning may change support but not question/source/semantic/answer custody.
5. Source item identity, stem, options/subparts, provenance and canonical answer remain immutable.
6. Neither B-layer consumes learner responses at runtime or dynamically chooses the next task.
7. A static artifact cannot assert mastery, retention or transfer readiness merely because an exercise is present.

## Self-study closure

```text
OPEN-ENDED TASK
-> attempt
-> progressively stronger fixed help
-> EXPECTED / CANONICAL RESPONSE
-> EXPLANATION
-> VERIFY / REFLECT
```

## Validation families

### Core1B

1. `CAP-SEPARATE-OBSERVATION-INFERENCE` / `PF-EVIDENCE_TO_CLAIM` — EASY bucket.
2. `CAP-ATTACH-SPECIES-ROLE` / `PF-AGENT_ROLE_ASSIGNMENT` — HARD bucket with deep-research and sub-subtopic decomposition authority.

### Core2B

1. `U2Q35` / `PF-EVIDENCE_TO_CLAIM` — `knowledge_percent = 50` -> MEDIUM support.
2. `U2Q29A` / `PF-REACTION_PROCESS_CLASSIFICATION` — explicit owner waiver -> LOW support with solution deferred until after a full attempt.

## Release falsifiers

The implementation fails closed for, at minimum:

```text
CHEM_B_LIVE_RUNTIME_FIELD_PRESENT
CHEM_B_NEW_CHEMISTRY_INTRODUCED
CHEM_CORE1B_BLUEPRINT_V4_BUCKET_REQUIRED
CHEM_CORE1B_KNOWLEDGE_CONTAMINATION
CHEM_V4_BUCKET_PAGE_ENVELOPE_INVALID
CHEM_V4_MEDIUM_RESEARCH_MISSING
CHEM_V4_HARD_DEEP_RESEARCH_MISSING
CHEM_CORE1B_HELP_ORDER_INVALID
CHEM_CORE1B_ANSWER_CLOSURE_MISSING
CHEM_CORE2_LEARNER_CONDITION_UNRESOLVED
CHEM_V4_KNOWLEDGE_PERCENT_INVALID
CHEM_V4_CONDITIONING_DUAL_AUTHORITY
CHEM_CORE2B_SUPPORT_PROFILE_INVALID
CHEM_CORE2B_ITEM_NOT_CORE2A_LEGAL
CHEM_CORE2B_SOURCE_IDENTITY_DRIFT
CHEM_CORE2B_ANSWER_CLOSURE_MISSING
```

Machine PASS means contract closure only. Subject correctness, pedagogy, assessment design, actual-size usability and mature-design approval remain separate review gates.
