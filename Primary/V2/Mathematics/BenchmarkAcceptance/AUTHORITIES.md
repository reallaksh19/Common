# Primary Mathematics V2 — Acceptance Authorities

This package is governed by the merged **Primary Grades 4–5** architecture in Common. Grade 9 visual/publication work is not normative authority for this benchmark.

## Authoring backbone

### Common PR #163 — canonical Primary educational architecture

Use for:

- Common as the owner of educational meaning;
- Grade 4 and Grade 5 sharing canonical learning objects where the mathematics is genuinely the same;
- curriculum/school mappings as overlays rather than duplicate ontologies;
- evidence ≠ judgement;
- `SkillState` ≠ `CurrentLearningState`;
- conceptual support ≠ access/load adjustment;
- representation role: `PROVIDED`, `CHILD_SELECTED`, `CHILD_PRODUCED`;
- acquisition, independent use, delayed retention, transfer and stretch as separate dimensions;
- source/scope ambiguity kept explicit.

Acceptance implication: a candidate may infer **question-derived operational scope**, but may not silently promote it to universal Grade 4/5 curriculum truth.

### Common PR #171 — MathematicalWorkEvidence

Use for:

- preserving ordered intermediate work before diagnosis;
- preserving successful substeps inside an incorrect solution;
- quantity/unit/role/relationship structure;
- child-created representations and strategy supports;
- self-corrections;
- teacher annotations with separate provenance;
- ambiguous handwriting remaining ambiguous;
- bounded Math error signatures as evidence patterns rather than learner traits.

Acceptance implication: the benchmark must include notebook/work-trace cases, not only final-answer correctness.

### Common PR #172 — work evidence into Teacher Runtime decisions

Use for the required reasoning path:

```text
CHILD WORK
→ MATHEMATICAL WORK EVIDENCE
→ ERROR SIGNATURE / STRUCTURAL PATTERN
→ BOUNDED RESPONSE DIAGNOSIS
→ SMALLEST DISCRIMINATING PROBE
→ TEACHER MOVE
→ INDEPENDENT RETRY
```

Acceptance implication: more practice on the whole topic is not a valid substitute for a narrow evidence-based teaching decision.

### Common PR #185 — diagnostic contrast/probe semantics

Use for:

- `ContrastSet` with explicit focal feature and controlled shared features;
- 2–3 bounded `CompetingHypothesis` records;
- first-class `DiagnosticProbe`;
- small controlled probe items with predicted outcome rules;
- the canonical Division contrast:
  - `366 ÷ 12` — quotient-zero feature present;
  - `7843 ÷ 13` — quotient-zero feature present;
  - `3496 ÷ 23` — comparable long division without the same focal feature.

Acceptance implication: the benchmark must reject `weak in division` when the evidence only establishes a narrower hypothesis.

### Common PR #182 — visual-first publishing contract

Use for:

- child-facing `VISUAL_FIRST` default;
- one dominant learning idea per page/spread;
- meaningful instructional visual/model/worked layout;
- short child-facing text chunks;
- visible learner action;
- adequate whitespace and response space;
- student vs teacher/parent edition separation;
- `H1 NOTICE → H2 REMEMBER → H3 REPRESENT → new independent retry → stop/fade`;
- page-image child-usability review as release-blocking.

Acceptance implication: mathematically correct, text-dense PDFs can still fail.

### Common PR #164 — operational Grade 4 Math runtime behavior

Use for:

- LearningEpisode as the learner-facing form of reusable learning content;
- conceptual support separated from language/access support;
- representation evidence roles;
- transient lapse distinguished from stable misconception/prerequisite gaps;
- meaningful route change after repeated same-route failure;
- repair followed by independent retry;
- acquisition/independent/delayed-retention/transfer evidence kept separate.

Acceptance implication: supported same-session success is not mastery or delayed retention.

## Conditional PR #207

PR #207 is relevant to English source-boundary/inference work. It is **not part of the Mathematics acceptance dependency chain** and is intentionally excluded here.

## Non-authority historical material

Grade 9 PRs such as #310/#322/#323 may be consulted only as engineering defect history (for example, hardcoded visual values, text labels standing in for diagrams, identifier leaks, or false maturity claims). They do not define Primary Math semantics, scope, hint behavior, learner evidence, or publishing acceptance.