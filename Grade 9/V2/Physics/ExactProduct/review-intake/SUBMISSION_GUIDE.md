# Physics P-L authorized human review intake

This directory is the governed intake surface for the four human-only P-L quality dimensions. It does not create reviewer authority.

A real submission must use the shared `HumanReviewSubmission` contract and bind both exact learner-product PDF SHA-256 values through `candidate_artifact_sha256_refs`. The single `candidate_artifact_sha256` field binds the deterministic Physics P-L artifact-set digest produced by `build_physics_human_review_binding.py`.

Required independent dimensions are `SUBJECT`, `PEDAGOGY`, `ASSESSMENT`, and `VISUAL`. Their rubrics are repository-backed projections of the existing Physics human-review packet and Physics assessment-review policy.

`reviewer_authorization.real.json` is intentionally empty until actual reviewers are explicitly appointed through repository governance. CI, AI output, ChatGPT, test fixtures and repository maintainers acting without a recorded authorization entry cannot manufacture a human PASS.

`reviewer_authorization.test-only.json` exists solely for falsifier/state-machine tests. TEST_ONLY evidence is permanently non-releaseable.

The real submissions directory contains no JSON submissions at present. Therefore the correct real projection is four PENDING human states and `release_evidence_eligible=false`.
