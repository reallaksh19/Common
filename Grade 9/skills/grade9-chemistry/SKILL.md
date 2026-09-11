---
name: grade9-chemistry
description: Apply Grade 9 Chemistry macroscopic-particle-symbolic reasoning, conservation, reaction/process reasoning, experimental evidence, misconception analysis, difficulty calibration, topic-level two-file publication, and Chemistry review contracts. Use for matter, mixtures, atomic structure, periodicity, chemical reactions, formulas/equations, separation, acids/bases, practical work, HOTS, competitive-foundation chemistry, and source-grounded Chemistry topic production.
---

# Grade 9 Chemistry

Provide the subject-specific Chemistry reasoning layer for the shared Grade 9 workflow.

## Core representation model

Treat chemistry learning as movement among:

`MACROSCOPIC <-> PARTICULATE <-> SYMBOLIC`

For each topic/question identify which level is given and which level(s) the learner must infer or construct.

## Chemistry fingerprint

Record as applicable:

- concept family;
- chemical entities/substances;
- process or reaction;
- macroscopic observations/evidence;
- particle-level model;
- symbolic formula/equation representation;
- conservation requirements;
- experimental context;
- reasoning modes;
- model limitations;
- minimum expert solution path.

## Difficulty vector

Use 0-10 dimensions:

- `particle_reasoning`
- `representation_translation`
- `classification_discrimination`
- `reaction_conservation_reasoning`
- `quantitative_reasoning`
- `experimental_inference`
- `condition_exception_handling`

Record arithmetic burden separately.

## Evidence-claim-reasoning

For experimental/inference questions distinguish:

- `evidence` — what is actually observed/measured;
- `claim` — what conclusion is proposed;
- `reasoning` — why the evidence supports the claim;
- `overclaim_warning` — what the evidence does not prove by itself.

Do not teach simplistic rules such as `bubbles always mean a chemical reaction` or `clear liquid means pure substance`.

## Conservation ledger

When formulas, reactions, or particle diagrams are involved, explicitly track as appropriate:

- atoms;
- mass;
- charge;
- species identity.

## Practical-method schema

For separation/experimental questions record:

- goal;
- selected method;
- physical/chemical property used;
- apparatus;
- expected observation;
- result/residue/filtrate/product terminology;
- limitation or unsuitable case.

## Model status

Use `EXACT_LAW`, `IDEALIZED_MODEL`, `EMPIRICAL_RULE`, `QUALITATIVE_TREND`, `APPROXIMATION`, or `SCHOOL_LEVEL_MODEL` where useful. Record known limitations of simplified particle/atomic models.

## Chemistry misconceptions

Maintain causal misconception families such as:

- dissolved means disappeared;
- homogeneous means compound;
- particles expand when matter is heated;
- isotopes are different elements;
- neutral atoms contain no charged particles;
- atoms disappear in reactions;
- coefficients change chemical formulas;
- any visible change proves chemical reaction.

## Mandatory Chemistry topic-production routing

When **any Chemistry topic** is taken up for learner-facing production, route through `$grade9-chemistry-topic-builder`.

The subject-wide topic contract is:

```text
TWO FILES ONLY PER TOPIC

1. CORE STUDY GUIDE
   -> teaching narrative
   -> Appendix A: Core Practice
   -> Appendix B: Core Solutions
   -> Appendix C: Printable Handout

2. EXAMSIDE SOLUTION & TRANSFER
   -> attempt-first question
   -> source/difficulty/transfer/concept badges
   -> primary-vs-support concept segregation label
   -> H1/H2/H3 optional hints as required
   -> concept helper / misconception watch when needed
   -> Core cross-link + source link
   -> complete solution
```

Appendix C is mandatory. Do not emit a separate handout PDF; the handout lives inside the Core Study Guide.

The generic contracts live at:

- `Grade 9/Chemistry/CHEMISTRY_PUBLICATION_SCHEMA.md`
- `Grade 9/Chemistry/schema/chemistry-topic-delivery.schema.json`
- `Grade 9/skills/grade9-chemistry-topic-builder/SKILL.md`

## Chemistry publication/review routing

After a topic/chapter has passed content/source/corpus audits and needs repository packaging, exact artifact custody, source/corpus reconciliation, PDF/link/notation/appendix QA or a draft PR review package, invoke `$grade9-chemistry-publication-review`.

Technical publication PASS must verify the two-file topic contract and Core Appendix A/B/C presence, including Appendix C handout, in addition to source/corpus and artifact QA.

## Redox authoring routing

When the topic is Redox, invoke `$grade9-chemistry-topic-builder` as the generic contract and `grade9-redox-subtopic-book-builder` as the Redox-specific reasoning adapter, together with:

- `grade9-subtopic-completeness-auditor` for source/pedagogy/typography/layout gates;
- `grade9-transfer-coverage-auditor` for canonical external-question accounting.

The Redox adapter may specialize concept helpers and misconception patterns, but it may not change the Chemistry-wide two-file or Appendix A/B/C contract.

Use the shared question-bank and learning-enrichment skills for bank construction and diagnostics.
