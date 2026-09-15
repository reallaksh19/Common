# Chemistry learner-product review-candidate realization

A structurally valid PDF is not automatically a review candidate.

The four-Core compiler first establishes engineering/Blueprint/source-scope custody. Rendering then produces an engineering artifact. A separate machine review-candidate gate checks the actual render trace against current Blueprint product-quality authority before the artifact may be labeled `MACHINE_REVIEW_CANDIDATE`.

Authority flow:

```text
Engineering Gate
  -> engineering closure / authorization
  -> Blueprint obligations
  -> Core semantic authority
  -> Core source-scope custody
  -> deterministic composition
  -> physical PDF preflight
  -> Blueprint review-candidate realization gate
  -> MACHINE_REVIEW_CANDIDATE
  -> human review (still required)
```

The review-candidate gate consumes the current Blueprint v5 page-architecture policy, v7 product-purpose policy, and product-control consolidation policy. It does not infer Chemistry from layout and it does not use page count as a quality metric.

The shared composition system provides page hierarchy, semantic panels, task-bound workspace, visual containers, answer/verification surfaces and mode-distinct learner actions. These are presentation and interaction structures only; Chemistry-bearing text and representations remain upstream-governed.

Core1A is a study-guide composition. Core1B is a reconstruction workbook. Core2A is attempt-first expert practice. Core2B is a transfer workbook with explicit target, representation/model choice and first-move commitment before fixed support.

Human subject correctness, pedagogy, assessment design, visual usability and mature-design approval remain separate release gates.
