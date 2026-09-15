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

Drives P-A → P-J and renders the two learner products, **twice over the same assessment**:
once with no `AttemptSet`, once with one.

```text
P-D problem semantics -> P-E learner evidence -> P-F study scope/model
-> P-G Core1 -> P-H representations + realization proof -> P-I Core2 transfer
-> two learner PDFs -> P-J coverage closure over the realized product
```

Current run on the merged motion assessment, identical in both modes:

```text
17 capabilities   17 Core1 lessons   128 representations   8 transfer pages
coverage closure CLOSED   ~2,700 real vector operations per run
CORE_STUDY_GUIDE 75 pages   TRANSFER_SOLUTION_BOOK 9 pages
```

## The two-run proof

The assessment decides what must be teachable; learner evidence decides only order, depth,
bridge, treatment and support. `comparison.json` asserts all thirteen invariants:

```text
question set / topic scope / scope authority / external corpus digests
problem semantics digest       study scope digest
required capability set        required item set
problem family truth           physical model truth       law truth
external eligibility           two-product topology
```

and records the two differences that are *supposed* to exist — `study_model_digest` and
`core1_plan_digest` — because a run that ignored attempt evidence would be a different
defect.

## Cold-start independence is audited, not asserted

Every runtime read is recorded and checked against the manifest. The validator rejects:

| condition | falsifier |
|---|---|
| chat/issue/transcript in the read list, or the flag set | `COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY` |
| any read of PR #156 | `PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON` |
| a read of a file the manifest does not declare | `RUNTIME_READ_OUTSIDE_AUTHORITY_MANIFEST` |
| a hand-supplied StudyModel / scope / family map | `MANUAL_STUDYMODEL_REQUIRED`, `GENERATION_STARTS_AFTER_SCOPE_WAS_MANUALLY_DERIVED`, … |
| a decision with no authority reference, or "agent decided" | `FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE` |

That last check is why the legacy `Publication/` engine cannot creep back in: it is not in
the manifest, so reading it fails the audit.

## Two products, never three

`CORE_STUDY_GUIDE` (main teaching + Appendix A + Appendix B + Appendix C) and
`TRANSFER_SOLUTION_BOOK`. Appendix C is a section, not a third PDF
(`THIRD_PRODUCT_PDF_CREATED`, `APPENDIX_C_MISSING_FROM_CORE1`).

## Learner-surface hygiene

`physics_product_renderer.py` sanitizes every string and every figure label on its way to a
learner page: internal identifiers (`PHY-CAP-…`, `PHY-PF-…`, `REP-…`) and
`SCREAMING_SNAKE` engineering tokens are rewritten into ordinary words, and phrases like
"reserved for Core2" become learner wording. The test extracts the text of all four
generated PDFs and asserts **zero** residual internal tokens
(`INTERNAL_TOKEN_LEAKED_TO_LEARNER`). This is the same class of defect the Chemistry C-L
remediation had to fix, caught here before release rather than after.

## Running

```bash
python "Grade 9/V2/Physics/ColdStart/contracts/validate_contracts.py"
python "Grade 9/V2/Physics/ColdStart/tests/test_physics_cold_start.py"
```

## Non-claims

A successful cold start proves the chain is reproducible and self-contained. It says
nothing about subject correctness, pedagogical quality, assessment quality or visual
usability: all four human review states are `PENDING` in every run report, and claiming one
`PASS` fails `FAKE_HUMAN_REVIEW_STATE`. P-L owns those gates.
