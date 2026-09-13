# Physics V2 — P-A0 Source Question Reconciliation Ledger

The ledger is the **independent denominator** for every later completeness proof. It is frozen from the source documents *before* authoring, and P-J reconciles against it instead of against the artifact it is supposed to audit.

```text
source documents
      │  transcribed and digest-frozen, before P-A extraction runs
      ▼
P-A0 PhysicsSourceQuestionLedger
      │
      ├── P-A question set          (what extraction actually produced)
      ├── P-B item validity registry (what review deliberately excluded, and why)
      └── P-J source coverage matrix (what the product actually teaches)
      ▼
PhysicsSourceReconciliationReport
```

## The blind spot this closes

P-J's completeness proof was relative to whatever P-A's `question_set` already contained. If extraction drops a source item, every downstream matrix still reconciles perfectly — against a denominator that is itself already short. "Concept coverage looks complete" and direct source items have no home at all. That is exactly the defect the owner's independent review of PR #332 found on Newton's Laws: three direct Unit-9 items (Q5, Q9, Q11) with nowhere to live, invisible to a proof that used the question set as its own authority.

Three things can now disagree, and the report says which:

| | authority | what it answers |
|---|---|---|
| ledger | the source documents | what exists |
| question set | P-A extraction | what was captured |
| coverage matrix | P-G/P-J | what is taught, practised or explicitly excluded |

## Falsifiers

| code | what it catches |
|---|---|
| `SOURCE_ITEM_MISSING_FROM_QUESTION_SET` | the source lists it, extraction did not produce it, review did not exclude it |
| `QUESTION_SET_ITEM_NOT_IN_SOURCE_LEDGER` | an item that did not come from the declared source, or a stale ledger |
| `DIRECT_SOURCE_ITEM_WITHOUT_COVERAGE_HOME` | a direct item with no lesson, no practice item and no exclusion — the NLM defect |
| `COVERAGE_PROVEN_ONLY_AGAINST_ITSELF` | closure claimed with no ledger supplied at all |
| `SOURCE_LEDGER_DERIVED_FROM_QUESTION_SET` | a ledger generated from the artifact it audits proves nothing |
| `SOURCE_LEDGER_NOT_FROZEN_BEFORE_AUTHORING` | a ledger written after the fact is not an independent denominator |
| `SOURCE_LEDGER_DIGEST_MISMATCH` | the frozen listing, its declared count or its direct/supporting split were edited |
| `SOURCE_LEDGER_IS_SYNTHETIC_CLAIMED_AS_PRODUCTION` | a fixture ledger presented as a real transcription |

A review exclusion **is** a home: an item review deliberately excluded, with a stated reason, reconciles rather than counting as a gap.

## Genericity

The engine contains no topic knowledge. Item refs, item classes (`DIRECT` / `SUPPORTING` / `NON_ASSESSED`), source order and subtopic bindings are ledger data. A new Physics topic needs a new ledger, not a new code path — the same generic reconciliation runs over Motion, Newton's Laws or Vectors unchanged.

## Honesty about this repository's ledger

`registry/physics-source-question-ledger.json` covers the repository's **synthetic** Motion assessment (artifact `SYN-MOTION-V1`). There is no separate source PDF in-tree, so the ledger declares `ledger_class: SYNTHETIC_FIXTURE_LEDGER` and `production_claim: false`, and the validator rejects it if it ever claims otherwise. For a real source the ledger must be transcribed from the source document before P-A extraction runs. The mechanism is identical either way; what makes the transcription load-bearing is the reconciliation engine, not the note.

## Files

```text
SourceLedger/
├── contracts/
│   ├── physics-source-question-ledger.schema.json
│   ├── physics-source-reconciliation-report.schema.json
│   └── validate_contracts.py
├── engine/
│   └── build_physics_source_ledger.py
├── registry/
│   └── physics-source-question-ledger.json
└── tests/
    └── test_physics_source_ledger.py
```

## Standalone use

```bash
python "Grade 9/V2/Physics/SourceLedger/engine/build_physics_source_ledger.py" \
  --question-set "Grade 9/V2/Physics/AssessmentIntake/fixtures/motion-question-set.fixture.json" \
  --review-registry "Grade 9/V2/Physics/AssessmentReview/registry/physics-item-validity-registry.json" \
  --source-coverage-matrix /path/to/source_coverage_matrix.json \
  --strict
```

P-K loads the ledger from `GENERATION_AUTHORITY_MANIFEST.json` and passes it to P-J, so a cold start reconciles automatically and closure cannot reach `CLOSED` without it.
