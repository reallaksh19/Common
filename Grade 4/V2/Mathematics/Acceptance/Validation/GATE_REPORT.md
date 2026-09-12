# Primary Mathematics V2 — Engineering Gate Report

**Candidate ID:** `PRIMARY-MATH-V2-ENGINE-CANDIDATE-001`  
**Timestamp:** `2026-09-12T05:51:37.441238+00:00`  
**Overall Machine Gate Pass:** `PASS`  

## 1. Machine Verification Gates

| Gate Name | Status | Meaning |
| :--- | :---: | :--- |
| `CORPUS_INTEGRITY` | **PASS** | Evaluated by independent benchmark evaluator |
| `SEMANTIC_CONSISTENCY` | **PASS** | Evaluated by independent benchmark evaluator |
| `SCOPE_PROVENANCE_CONSISTENCY` | **PASS** | Evaluated by independent benchmark evaluator |
| `REPRESENTATION_EVIDENCE_PRESENT` | **PASS** | Evaluated by independent benchmark evaluator |
| `WORK_PROVENANCE_CONSISTENCY` | **PASS** | Evaluated by independent benchmark evaluator |
| `CORE1_CORE2_LINKAGE` | **PASS** | Evaluated by independent benchmark evaluator |
| `HINT_RETRY_CONTRACT` | **PASS** | Evaluated by independent benchmark evaluator |
| `LEARNER_SURFACE_GUARD` | **PASS** | Evaluated by independent benchmark evaluator |
| `ARTIFACT_CUSTODY` | **PASS** | Evaluated by independent benchmark evaluator |

## 2. Independent Human Review Rubric (Refinement 11 Compliance)

Per anti-gaming rules and Common PR #182/#185 standards, machine evaluation never auto-promotes human qualitative judgments. These gates remain explicitly bounded as pending human review:

| Human Review Dimension | Status | Review Scope |
| :--- | :---: | :--- |
| `SUBJECT_CORRECTNESS_HUMAN_REVIEW` | **PENDING_HUMAN_REVIEW** | Pedagogical accuracy of mathematical explanations |
| `PEDAGOGICAL_DESIGN_HUMAN_REVIEW` | **PENDING_HUMAN_REVIEW** | Notice -> Model -> Worked -> Supported progression |
| `ASSESSMENT_DESIGN_HUMAN_REVIEW` | **PENDING_HUMAN_REVIEW** | Cognitive load and prompt discrimination |
| `VISUAL_USABILITY_HUMAN_REVIEW` | **PENDING_HUMAN_REVIEW** | Visual clarity, contrast, and layout hierarchy |
| `CHILD_USABILITY_HUMAN_REVIEW` | **PENDING_HUMAN_REVIEW** | Child response space, line heights, readability |
| `MATURE_DESIGN_QUALITY_HUMAN_REVIEW` | **PENDING_HUMAN_REVIEW** | Professional publishing aesthetics & print quality |

## 3. Case Evaluation Summary

- **Total Cases Evaluated:** 20
- **Passed Cases:** 20
- **Failed Cases:** 0
- **Triggered Falsifiers:** `0`

### Evaluated Benchmark Cases

| Case ID | Machine Verdict | Triggered Falsifiers |
| :--- | :---: | :--- |
| `BENCH-DEEP-MUL-01` | PASS | None |
| `BENCH-DEEP-DIV-01` | PASS | None |
| `BENCH-DEEP-DIV-02` | PASS | None |
| `BENCH-DEEP-DIV-03` | PASS | None |
| `BENCH-DEEP-DIV-04` | PASS | None |
| `BENCH-DEEP-DIV-05` | PASS | None |
| `BENCH-DEEP-DIV-06` | PASS | None |
| `BENCH-DEEP-FRAC-01` | PASS | None |
| `BENCH-DEEP-FRAC-02` | PASS | None |
| `BENCH-DEEP-FRAC-03` | PASS | None |
| `BENCH-BREADTH-PV-01` | PASS | None |
| `BENCH-BREADTH-DEC-01` | PASS | None |
| `BENCH-BREADTH-MEAS-01` | PASS | None |
| `BENCH-BREADTH-GEOM-01` | PASS | None |
| `BENCH-BREADTH-GEOM-02` | PASS | None |
| `BENCH-BREADTH-GEOM-03` | PASS | None |
| `BENCH-BREADTH-DATA-01` | PASS | None |
| `BENCH-BREADTH-WP-01` | PASS | None |
| `BENCH-BREADTH-ERR-01` | PASS | None |
| `BENCH-BREADTH-NOTE-01` | PASS | None |

## 4. Architectural Invariant Audit

- **Independent Benchmark Authority:** Maintained under separately frozen `BenchmarkAcceptance/` suite.
- **Unified Canonical Registry:** Unified `capability_registry.json` with curriculum overlays (no separate Grade 4 vs Grade 5 canonical ontologies).
- **Authority Scope Binding:** Explicit `scope_basis: CURRICULUM_CONFIRMED` with `authority_ref: NCERT_CLASS4_CH3`, preventing illegal universal promotion.
- **Quotient-Zero Invariant:** Strict positional zero preservation validated across `366÷12=30 R6` and `7843÷13=603 R4` without leading zero pollution.
- **PR #310 Defect Elimination:** 100% parameter derivation across all primitives (`RENDERED_EVIDENCE_ARGUMENTS_IGNORED` tested and enforced).
- **Authentic Notebook Provenance:** 4-tier provenance (`STRUCTURED_REPLAY`) with strictly aligned place-value columns and non-erased intermediate substeps.
- **Child Readability Contract:** A4 Portrait, minimum 13.5pt body text, generous response boxes (>= 65pt), pagination over shrinking (`ADD_PAGE`).
- **Learner Surface Guard:** 3-pass zero false-positive token scanner verified clean.
