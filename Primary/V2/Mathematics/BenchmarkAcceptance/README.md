# Primary Mathematics V2 — Benchmark & Acceptance Corpus

**Status:** independent benchmark authority for Common #324  
**Scope:** Grade 4–5 Primary Mathematics Core Skills v2  
**Authority boundary:** benchmark/acceptance only; this package does not render learner products and does not own the #324 implementation.

## Why this exists

The implementation that generates Core 1 / Core 2 must not also be free to redefine the benchmark it is judged against. This package therefore provides an implementation-independent acceptance corpus for Primary Mathematics v2.

The benchmark consumes the Primary product contract:

```text
question_set                    REQUIRED
student_workout                 OPTIONAL
topic_hints                     OPTIONAL
        ↓
PrimaryMathSkillModel
        ↓
PrimaryMathCore1StudyGuide
PrimaryMathCore2Companion
```

and evaluates whether a candidate preserves mathematical truth, scope provenance, representation obligations, learner-work provenance, Core1↔Core2 linkage, hint fading, publication custody and child-usable design boundaries.

## Independence rules

This package MUST NOT:

- import the #324 renderer or page-composer implementation;
- depend on ReportLab, a particular PDF backend, or renderer class names;
- copy Grade 9 PR #310 schemas or prototype values;
- use Grade 9 PR #310/#323 branches as runtime dependencies;
- accept an engine-generated PASS claim as evidence of acceptance;
- mutate expected results to make a candidate green without a benchmark-change review.

Older Grade 9 work may be cited only as defect history / regression rationale. Primary semantics on `main` and this corpus are the acceptance authorities.

## Package layout

```text
BenchmarkAcceptance/
├── README.md
├── BENCHMARK_SPEC.md
├── HUMAN_REVIEW_RUBRIC.md
├── contracts/
│   └── candidate_export.schema.json
├── registry/
│   ├── benchmark_cases.json
│   └── falsifier_catalog.json
├── fixtures/
│   ├── positive/
│   │   └── semantic_cases.json
│   └── negative/
│       └── semantic_mutations.json
├── validator/
│   ├── evaluate_candidate.py
│   └── validate_corpus.py
└── tests/
    └── test_benchmark_acceptance.py
```

## Benchmark philosophy

The corpus specifies **what must be true and observable**, not how it must be implemented.

A benchmark case may require, for example:

```text
- distinguish sharing from grouping;
- preserve an internal quotient zero;
- prove divisor × quotient + remainder = dividend;
- represent equal fraction partitions;
- align decimal place value;
- show perimeter as boundary rather than area;
- preserve student/teacher provenance in notebook replay;
- require a fresh independent retry after H3 representation support.
```

It does not prescribe one Python class, one drawing library, or one page coordinate system.

## Deep benchmark families

1. **Multiplication bridge** — groups → array → distributive/area → partial products → written algorithm → check.
2. **Division bridge** — sharing/grouping → structural model → partial quotient / written method → quotient-zero / remainder semantics → check.
3. **Fractions bridge** — equal partition / strip / number line → equivalence / operation semantics.

## Breadth benchmark families

The corpus also includes place value, decimals, measurement/unit chains, perimeter/area/volume, geometry/angles, data/graphs, word-problem quantity structure, error analysis and notebook provenance.

## Acceptance layers

```text
L0 CORPUS INTEGRITY
L1 MATHEMATICAL SEMANTIC ORACLE
L2 REPRESENTATION OBLIGATION
L3 LEARNER-WORK PROVENANCE
L4 CORE1 / CORE2 PRODUCT LINKAGE
L5 ENGINEERING CUSTODY
L6 CHILD-USABILITY HUMAN REVIEW
```

L0–L5 can be machine evaluated when the candidate exports the required evidence. L6 remains human review and MUST NOT be manufactured by CI.

## Candidate contract

A candidate under review exports a neutral `candidate_export.json` conforming to `contracts/candidate_export.schema.json`. The export contains benchmark-case evidence, not implementation internals. The independent evaluator recomputes the benchmark assertions from that evidence.

## Change-control rule

A change to benchmark expected values, required assertions, or falsifiers is a benchmark-contract change. It must be reviewable independently from the renderer change that benefits from it.

## Relationship to #324

#324 builds the Primary Math V2 visual/publishing engine. This package judges candidates produced by that engine. Neither package is allowed to silently redefine the other's authority.