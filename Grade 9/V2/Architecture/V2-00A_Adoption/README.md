# V2-00A — Authority-Safe Adoption and Migration Control Plane

Parent issues: #174, #175  
Implementation issue: #178

## Purpose

This folder is the clean V2 control plane for reusing proven work from PR #160–#168 without making those branches runtime dependencies.

The rule is:

```text
old artifact
→ classify authority
→ COPY | ADAPT | REWRITE | REJECT | TEST_FIXTURE_ONLY | REFERENCE_ONLY
→ clean V2 destination
→ V2 validation
```

This PR does **not** migrate Physics, Chemistry, or Mathematics canonical content. It does not generate learner artifacts and does not implement longitudinal scheduling.

## Authority classes

- `CANONICAL` — learner-independent subject truth, scope, formal objects, representations and dependencies.
- `EVIDENCE` — source/exam evidence or learner attempts; evidence is not diagnosis.
- `INFERENCE` — observations, diagnostic cases and learner-state derivation methodology.
- `DECISION` — StudyModel / LearningDesign / future programme decisions.
- `REALIZATION` — semantic product, structure, physical placement, artifact/audit machinery.
- `VALIDATION` — independent subject, pedagogy, visual, benchmark and human review evidence.

Cross-class transformation must be owned by an explicit downstream V2 contract.

## Source disposition for this PR

| Source | Initial V2 disposition |
| --- | --- |
| PR #160 | Adapt canonical/evidence custody and deterministic research mechanisms |
| PR #161 | Adapt publication/custody engineering; rewrite educational ownership |
| PR #166 | Adapt learner evidence/state contracts |
| PR #167 | Adapt reasoning/capability contracts after canonical vs learner ownership split |
| PR #168 | Adapt inference policy; keep synthetic fixtures test-only |
| #162 / PR #163/#164 | Reference/selectively re-justify general invariants; do not copy Primary ontology |
| #165 | Reference-only pedagogical RCA/falsifier evidence |
| PR #156/#157 | Final validation references only; forbidden as producer inputs |

## Files

- `ADOPTION_LEDGER.schema.json` — machine-readable ledger contract.
- `adoption_ledger.json` — seeded artifact-family dispositions.
- `validate_adoption_ledger.py` — dependency-free semantic validator/falsifier.
- `test_validate_adoption_ledger.py` — regression tests.
- `fixtures/` — valid and deliberately invalid ledgers.
- `PR_PLAN.md` — implementation and review sequence.

## Local validation

From repository root:

```bash
python "Grade 9/V2/Architecture/V2-00A_Adoption/validate_adoption_ledger.py" \
  "Grade 9/V2/Architecture/V2-00A_Adoption/adoption_ledger.json"

python -m unittest \
  "Grade 9/V2/Architecture/V2-00A_Adoption/test_validate_adoption_ledger.py"
```

Expected result: both commands pass.

## Non-negotiable firewall

This V2-00A contract fails closed if an entry permits an old-branch runtime dependency, treats #168 synthetic evidence as production learner evidence, writes learner inference into Core1 canonical truth, lets publication realization own StudyModel decisions, or promotes benchmark-derived PR #156/#157/#165 material into producer truth.

## Next step after V2-00A

V2-01 and V2-02 may consume this ledger as migration governance. Actual canonical or learner-state migration must occur in those owning PRs and must add destination-specific validation rather than inheriting old PASS claims.
