---
name: ioqm-grade9-study-guide-builder
description: Build or revise Grade 9 competitive-exam study guides from supplied corpora using a two-layer Analysis Engine -> Student Book Generator process, stable skills, dependency graphs, loss-preserving compression, concept assimilation, transfer labs, progressive practice, visual obligations, and rendered PDF QA.
---

# IOQM Grade 9 Study Guide Builder

## Purpose

Turn a supplied competitive-exam corpus into a student-friendly guide without losing the recognition, representation, execution, legality, transfer, or visual support needed by the target questions.

The builder has two layers:

1. **Analysis Engine** - determine what the corpus actually requires.
2. **Student Book Generator** - turn that model into a readable learner interface.

Core principle:

```text
rich internal analysis
-> simple student surface
-> no silent loss of executable support
```

## Mandatory references and precedence

Read in this order for every production build:

1. `references/analysis-engine-student-book-generator-contract-v3.md`
   - corpus decomposition, opening signatures, stable skills, prerequisite DAG, orphan methods, transfer gaps, student/reviewer separation.

2. `references/compression-loss-preservation-and-concept-assimilation-addendum-v1.md`
   - packaging mode, compression/loss ledger, concept assimilation, adaptive page depth, concrete FIRST MOVE/WATCH OUT/CHECK, variants, readable transfer maps, prototype and final-size legibility gates.

3. `references/question-driven-self-sufficient-study-guide-skill-v2.md`
   - detailed question-to-method support, stable IDs, Appendix A/B/C behavior, progressive hints, custody and integrated self-sufficiency.

4. `references/difficulty-badges-portability-and-challenge-ladders-addendum.md`
   - difficulty/source badges and Challenge Ladders.

5. `references/learner-knowledge-profile-and-readiness-addendum.md` when learner-specific routing is required.

6. `references/question-driven-self-sufficient-study-guide-skill-v2-visual-production-addendum.md` whenever any visual obligation is not NONE.

7. Read the relevant domain profile after the generalized contracts. Current profiles include Algebra and Number Theory.

Precedence:

- v3 controls architecture, concept splitting, dependency order and transfer-gap triggering;
- compression/assimilation addendum controls compact packaging, student teaching depth, readable navigation and prototype/legibility gates;
- v2 remains authoritative for detailed custody, question support and appendix behavior not replaced above;
- domain profiles specialize, but may not weaken generalized gates;
- explicit user requirements override defaults.

# Layer A - Analysis Engine

## A1. Freeze the corpus

Inventory and preserve:

- target stems / custody IDs;
- provenance and corrections;
- answers when supplied;
- source-required figures;
- stable local IDs.

Source order does not determine teaching order.

## A2. Decompose every question

Record at minimum:

```text
question ID
-> topic / subtopic / concept
-> candidate stable skill
-> recognition cue
-> representation/compression
-> first executable move
-> execution requirements
-> legality/check
-> prerequisites
-> misconception risk
-> difficulty / priority / mastery separately
-> visual obligation
-> transfer-gap status
-> provenance
-> final support status
```

## A3. Build the concept/method graph

For large corpora construct an auditable graph before chapter writing.

## A4. Split by Opening Signature

```text
Opening Signature
= recognition + representation + first move + legality/check
```

Split an umbrella concept when any of these materially differs.

## A5. Assign stable skills

Each stable skill needs:

- stable ID and readable learner name;
- prerequisites;
- recognition/representation/first move;
- execution closure;
- legality/check;
- close contrast;
- question links;
- transfer links;
- visual obligation when needed.

Readable names lead in the student artifact; internal IDs are secondary anchors.

## A6. Build prerequisite DAG

Teaching order comes from dependencies, not question numbering.

## A7. Orphan-method audit

Every question needs a route:

```text
recognition
-> retrieval
-> first move
-> executable continuation
-> legality/check
```

`ORPHAN_METHODS = 0`

## A8. Transfer-gap audit

Classify question-to-skill edges as NONE / MODERATE / HARD.

Every HARD gap requires a student-usable transfer lab/bridge.

## A9. Visual audit

Choose VISUAL_NONE / OPTIONAL / REQUIRED / SOURCE_REQUIRED. Required visuals enter the visual-production lifecycle and final-size QA.

## A10. Packaging and loss analysis

Before compact generation choose:

```text
SELF_CONTAINED_EDITION
or
REFERENCE_PLUS_PRACTICE_BOOK
```

If condensing an existing richer build, create the compression/loss ledger before generation.

A reference-plus-practice package may omit target stems from the reference, but may not drop required mechanisms, variants, transfer edges, visuals, or question routing.

## A11. Analysis hard gate

At minimum:

```text
CORPUS_FROZEN = PASS_n_OF_n
QUESTION_DECOMPOSITION = PASS_n_OF_n
QUESTION_TO_CONCEPT_BINDING = PASS_n_OF_n
CONCEPT_SPLIT_AUDIT = PASS
PREREQUISITE_GRAPH = PASS
UNJUSTIFIED_PREREQUISITE_CYCLES = 0
ORPHAN_METHODS = 0
TRANSFER_GAP_AUDIT = PASS_n_OF_n
HARD_TRANSFER_GAPS_WITHOUT_BRIDGE = 0
VISUAL_OBLIGATIONS = PASS_n_OF_n
PACKAGING_MODE_DECLARED = PASS
COMPRESSION_LOSS_LEDGER = PASS_IF_COMPACTED
ASSIMILATION_CRITICAL_LOSSES_UNRESOLVED = 0
TRANSFER_CRITICAL_LOSSES_UNRESOLVED = 0
```

Until these pass:

`STUDENT_BOOK_GENERATION_ALLOWED = FALSE`

# Layer B - Student Book Generator

## B1. Derive teaching order from the graph

Do not recreate source order.

## B2. Adaptive concept-assimilation grammar

Student pages are not required to use a fixed stack of equal-weight cards.

Available teaching roles:

```text
WHAT IS THIS?
TINY EXAMPLE
THE EXAM / OLYMPIAD LINK
WHY IT WORKS
WORKED EXAMPLE
FIRST MOVE
VARIANTS AND CLOSE CONTRASTS
WATCH OUT
CHECK
GUIDED PRACTICE
PRACTISE NEXT
```

Use the smallest set that achieves assimilation for that skill.

A direct/familiar skill may be compact. A transfer-heavy or unfamiliar skill must include enough mechanism, variants, checking, and guided practice to become executable.

## B3. Concrete retrieval objects

FIRST MOVE is visually prominent and should show an actual miniature mathematical opening whenever practical.

WATCH OUT should demonstrate a real wrong/illegal route for subtle skills.

CHECK should execute a verification rather than merely tell the learner to check.

## B4. Readable-name-first navigation

Primary learner navigation uses readable concept names.

Internal IDs may appear in small secondary type or in reviewer artifacts, but must not dominate:

```text
RAW_SKILL_ID_PRIMARY_NAVIGATION = 0
RAW_TRANSFER_IDS_AS_PRIMARY_NAVIGATION = 0
```

## B5. Practice Map and Transfer Map

Practice Map means:

```text
readable stable skill -> target question IDs
```

For questions that require more than the core skill, use a separate readable transfer route:

```text
question ID -> readable transfer-lab name -> readable core concepts to review
```

Do not expose the raw reviewer matrix as learner UI.

## B6. Progressive help

When hints are allowed:

- Notice = recognition only;
- Recall = readable prior skill;
- Start = first executable setup only.

Fade support over later attempts. Strict user-requested questions-only mode overrides this display.

## B7. Transfer labs

A transfer lab exists only because a target question needs an extra jump.

It should contain recognition, concrete first move, executable core route, legality/wrong route, and a non-identical guided transfer prompt.

## B8. Challenge Ladders vs mixed transfer

```text
CHALLENGE_LADDER = TRAIN_PROGRESSION
APPENDIX_B = TEST_INDEPENDENT_TRANSFER
```

Do not merge their roles.

## B9. Navigator

A short-horizon Navigator is a routing layer, not the knowledge architecture. Run the unaided recognition check before exposing method-revealing routing.

## B10. Prototype gate before bulk generation

Render and inspect at least:

- one transfer-heavy concept page;
- one navigation/router page;
- one practice/transfer-map page;
- one required-visual page when applicable.

Do not generate the long book until prototypes pass.

## B11. Final student/reviewer split

Normal learner artifact may contain Navigator, teaching core, transfer labs, Practice Map, target practice if self-contained, mixed challenge set and quick reference.

Reviewer/build dossier contains graph/matrices, loss ledger, custody/provenance, visual audit, static gates and final QA evidence.

## B12. Final integrated gates

At minimum:

```text
QUESTION_SUPPORT_PACKAGE = PASS_n_OF_n
STUDENT_SURFACE_SEMANTIC_GRAMMAR = PASS
FIRST_MOVE_PRESENT = PASS_n_OF_n
FIRST_MOVE_VISUAL_PROMINENCE = PASS_n_OF_n
FIRST_MOVE_CONCRETE_INSTANCE = PASS_n_OF_n
SUBTLE_SKILLS_WITH_VARIANT_OR_CLOSE_CONTRAST = PASS_n_OF_n
CORE_CHECKS_WITH_EXECUTED_VERIFICATION = PASS_n_OF_n
TRANSFER_EDGE_MANIFEST = PASS_n_OF_n
TRANSFER_MAP_READABLE_NAME_FIRST = PASS
ANALYSIS_JARGON_LEAKAGE = 0
DIFFICULTY_PRIORITY_MASTERY_CONFLATION = 0
```

Then apply the visual, provenance, answer and appendix gates from the referenced contracts.

# PDF rule

The rendered page is authoritative.

Reject clipping, overlap, broken glyphs, black squares, missing figures, low-contrast or broken heading colors, off-page tables, tiny learner navigation, unreadable badges, raw-ID dominance, and card-reader layouts without teaching flow.

Required final-size gates include:

```text
LOW_CONTRAST_HEADINGS = 0
BROKEN_HEADING_COLORS = 0
TINY_NAVIGATION_TABLES = 0
OFF_PAGE_TABLES = 0
CARD_READER_PAGE_FAILURES = 0
```

Render the complete artifact and inspect critical pages at final reading size.

# Evidence boundary

Static document gates do not prove retention, classroom timing, psychometric difficulty, contest score, or learner success. Those require observed learner evidence.

# Final rule

A strong student guide should let the learner answer:

```text
What is this idea?
What should make me notice it?
Why does the representation work?
What do I write or draw first?
How do I continue?
What nearby variant changes the route?
What can make the move illegal or wrong?
How do I check it?
Where do I practise core and transfer versions?
```

without exposing the complexity of the production machinery.
