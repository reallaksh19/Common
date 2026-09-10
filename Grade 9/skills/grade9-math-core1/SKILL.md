---
name: grade9-math-core1
description: Execute Mathematics Core (1) research on top of the frozen shared two-core v1 contracts: repository-first discovery, Math ScopeGraph construction, verified claims, derivations, representation semantics, source rights, exam/question evidence when needed, and a learner-neutral ResearchBundle handoff to Core (2). Use when asked to research, freeze, or prepare a Mathematics topic before learner-specific publication.
---

# Mathematics Core (1)

This is the **Math research entry point**, not the learner publisher.

Read first:

1. `Grade 9/Architecture/CORE1_RESEARCH_CONCEPT_NOTE.md`
2. `Grade 9/Architecture/MATHEMATICS_TWO_CORE_SPECIALIZATION.md`
3. `Grade 9/Architecture/contracts/v1/SCHEMA_FREEZE_V1.md`
4. `../grade9-math/SKILL.md`

The frozen v1 schemas belong to PR #160. Do not copy, fork, or locally modify their meanings.

## Intake

Search the repository before asking the user to repeat information already available.

Ask only for unresolved fields:

- topic/subtopics;
- purpose / exam target;
- supplied sources;
- learner Bxx by subtopic when the downstream publication will need it.

**Bxx is never stored in the ResearchBundle.** Record it as a separate `LearnerProfile` for Core (2).

For competitive Mathematics, inspect verified exam/PYQ evidence before finalizing the subtopic map. For generic study, confirm the topic/subtopics first and research only missing evidence.

## Core (1) research sequence

```text
REPO DISCOVERY
-> MATH AUTHORITY
-> SCOPEGRAPH
-> RESEARCH GAPS
-> CLAIMS / DERIVATIONS / CONDITIONS
-> REPRESENTATION SEMANTICS
-> FIRST MOVES / COMPETING METHODS / MISCONCEPTIONS
-> EXAM + QUESTION EVIDENCE when applicable
-> MATH VERIFICATION
-> STRUCTURED RESEARCH INPUT
-> SHARED PR #160 PACKAGE BUILDER
-> CORE1 PACKAGE VALIDATION
```

Do not run the package builder until the research input already contains verified mathematics.

## Math-specific requirements

For every included concept resolve:

- invariant / primary mathematical engine;
- prerequisites and missing bridges;
- conditions, domain and edge cases;
- proof/derivation when material;
- expert noticing / first move;
- nearest competing or wrong method;
- misconception/counterexample;
- representation semantics;
- transfer endpoint;
- source-backed ResearchClaim IDs.

A `READY_FOR_PUBLISH` Math bundle requires 100% included-concept claim coverage, no unpromoted project candidates, no blocking unresolved items, and no learner-state fields.

## External question systems

ExamSIDE/PYQ sources are evidence, not the Math ontology. Full source-backed coverage requires the shared `QuestionEvidenceLedger` with every candidate row dispositioned `REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE`. `REVIEW > 0` blocks handoff.

Discovery does not grant reproduction rights. Preserve `rights.status` from the shared SourceLedger contract.

## Build

After research is frozen:

```bash
python "Grade 9/skills/grade9-math-core1/scripts/validate_math_research_input.py" research_input.json
python "Grade 9/skills/grade9-math-core1/scripts/run_math_core1.py" --input research_input.json --out out/
python "Grade 9/skills/grade9-math-core1/scripts/validate_math_core1_package.py" --dir out --prefix <artifact-prefix>
```

`run_math_core1.py` delegates packaging to `Grade 9/Architecture/core1/build_research_package.py`. It performs no web research.

## Handoff

Core (1) outputs a learner-neutral package. Core (2) receives:

```text
ResearchBundle + ResearchBundleManifest
+ LearnerProfile + PublicationTarget
```

If Core (2) requires new mathematical truth, return `CORE1_RESEARCH_GAP` and version Core (1) after the gap is resolved. Never patch the learner book with an untracked research detour.

## Review fixture

Use `Grade 9/Mathematics/Permutations/Core1/` as the Math falsifier. It demonstrates that a previously chapter-oriented permutation project can be represented as a reusable ResearchBundle rather than a learner-specific publication schema.
