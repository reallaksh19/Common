# Physics V2 — P-K Cold-start runner and authority manifest

P-K implements issue #259 under the #320 catch-up. It is the phase that makes the claim
"a fresh agent can regenerate the Physics products from the repository alone" *testable*.

Entry point for a human or an agent: [`../V2_GENERATION_ENTRYPOINT.md`](../V2_GENERATION_ENTRYPOINT.md)
and [`../GENERATION_AUTHORITY_MANIFEST.json`](../GENERATION_AUTHORITY_MANIFEST.json).

```bash
python "Grade 9/V2/Physics/ColdStart/engine/physics_cold_start_runner.py" \
  --out-dir /tmp/physics-v2-cold-start
```

## What it does

Drives the governed production chain and renders the two learner products, **twice over the same assessment**:
once with no `AttemptSet`, once with one.

```text
governed assessment inputs
-> P-C exact assessment scope
-> P-C.5 Shared EngineeringGate
-> P-D problem semantics -> P-E learner evidence -> P-F study scope/model
-> P-G Core1 -> P-H representations + realization proof -> P-I Core2 transfer
-> two learner PDFs -> P-J coverage closure over the realized product
```

The wider P-A→P-F chain is independently re-proved in CI; P-K does not claim to consume a serialized P-A envelope object. Its production boundary is the exact governed assessment inputs plus the remaining manifest-owned authorities.

## Governed routed assessment inputs

Legacy callers continue to obtain `QuestionSet`, `DeclaredTopicScope`, and optional `AttemptSet` from the generation manifest exactly as before.

For a repository-owned execution route, `run_cold_start(...)` may instead receive `assessment_input_bindings`. This is deliberately limited to:

```text
QUESTION_SET            required
DECLARED_TOPIC_SCOPE    required
ATTEMPT_SET             optional
```

Each binding must contain the exact role, required flag, repository-relative Physics path, and SHA-256. The runner rejects unknown/duplicate roles, missing required roles, paths outside the Physics tree, missing files, and digest drift before the assessment input is used.

This is an input-selection seam only. It cannot override scope authority, canonical capabilities, Engineering bindings, problem-semantics registries, treatment policy, authoring profiles, transfer policy, publication, or human-review state. Those still resolve from the exact generation manifest.

The Blueprint AgentTasks adapter uses this seam only after an opaque route ID has resolved through the manifest-declared route registry. Ordinary additional routes therefore add governed data rather than a new P-K branch.

## The two-run proof

The assessment decides what must be teachable; learner evidence decides only order, depth,
bridge, treatment and support. `comparison.json` asserts the governed invariants, including:

```text
question set / topic scope / scope authority / external corpus digests
assessment scope / Engineering readiness / Engineering requirement state
problem semantics digest       study scope digest
required capability set        required item set
problem family truth           physical model truth       law truth
external eligibility           two-product topology
```

and records the differences that are *supposed* to exist — `study_model_digest` and
`core1_plan_digest` — because a run that ignored attempt evidence would be a different
defect.

## Cold-start independence is audited, not asserted

Every runtime read is recorded and checked against governed authority. The validator rejects:

| condition | falsifier |
|---|---|
| chat/issue/transcript in the read list, or the flag set | `COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY` |
| any read of PR #156 | `PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON` |
| an unauthorized runtime read | `RUNTIME_READ_OUTSIDE_AUTHORITY_MANIFEST` or routed-input custody failure |
| a hand-supplied StudyModel / scope / family map | `MANUAL_STUDYMODEL_REQUIRED`, `GENERATION_STARTS_AFTER_SCOPE_WAS_MANUALLY_DERIVED`, … |
| a decision with no authority reference, or "agent decided" | `FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE` |

The routed-input exception is narrow and explicit: only the exact digest-bound assessment-input paths selected by current subject route authority may differ from the manifest's legacy default assessment paths.

## Two products, never three

`CORE_STUDY_GUIDE` (main teaching + Appendix A + Appendix B + Appendix C) and
`TRANSFER_SOLUTION_BOOK`. Appendix C is a section, not a third PDF
(`THIRD_PRODUCT_PDF_CREATED`, `APPENDIX_C_MISSING_FROM_CORE1`).

## Learner-surface hygiene

`physics_product_renderer.py` sanitizes every string and every figure label on its way to a
learner page: internal identifiers (`PHY-CAP-…`, `PHY-PF-…`, `REP-…`) and
`SCREAMING_SNAKE` engineering tokens are rewritten into ordinary words, and phrases like
"reserved for Core2" become learner wording. The test extracts learner-facing text and asserts zero residual internal tokens (`INTERNAL_TOKEN_LEAKED_TO_LEARNER`).

## Running

```bash
python "Grade 9/V2/Physics/ColdStart/contracts/validate_contracts.py"
python "Grade 9/V2/Physics/ColdStart/tests/test_physics_cold_start.py"
```

The routed packet proof additionally runs in `Grade 9/V2/Physics/Blueprint/tests/test_blueprint_agent_task_intake.py`.

## Non-claims

A successful cold start proves the chain is reproducible and self-contained. It says
nothing by itself about subject correctness, pedagogical quality, assessment quality or visual
usability: all four human review states remain independently governed, and machine Engineering readiness never authorizes publication or human review.
