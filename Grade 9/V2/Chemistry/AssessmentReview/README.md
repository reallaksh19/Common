# Chemistry V2 — Source Integrity & Assessment Review (C-B)

Implements **#264** under Chemistry roadmap **#262**, consuming the exact intake authority established by **#263 / C-A**.

## Runtime position

```text
ChemistrySourceSet + QuestionSet
          ↓
C-A exact source/question custody
          ↓
C-B source-integrity + item-validity review
          ↓
C-C scope reconciliation / later learner inference
```

C-B intentionally consumes **no learner attempts**. The output bundle states:

```text
review_precedes_attempt_interpretation = true
attempt_data_consumed = false
```

## Artifacts

```text
contracts/
  chemistry-source-integrity-review.schema.json
  chemistry-assessment-item-review.schema.json
  chemistry-qc-event.schema.json
  chemistry-item-validity-registry.schema.json
  chemistry-review-shard.schema.json
  chemistry-diagnostic-use-policy.schema.json
  chemistry-assessment-review-bundle.schema.json
  validate_contracts.py

policies/
  chemistry-diagnostic-use-policy.json

registry/
  chemistry-item-validity-registry.json
  reviews/*.json
  chemistry-qc-events.json

engine/
  review_chemistry_assessment.py

fixtures/
  chemistry-review-cases.fixture.json

tests/
  test_chemistry_assessment_review.py
```

The registry is sharded so large Chemistry corpora can remain reviewable without weakening semantic custody: each shard is digested and record-counted, the manifest is digested, and an expanded-registry digest proves the assembled review set.

## Safety model

Source integrity and item validity are independent. A chemically valid question may still have damaged notation; a cleanly extracted item may still be underdetermined or domain-defective.

The diagnostic-use decision is therefore constrained by **both** states.

C-B preserves explicit states for:

```text
source typo
OCR / typographic ambiguity
formula / ionic-charge ambiguity
equation / coefficient issue
condition-sensitive chemistry
multiple valid interpretations
underdetermination
domain defect
key/data error
missing structure / figure
review required
```

## Explicit QC events

The source assertion remains immutable evidence. A learner-use repair is legal only through a provenance-bound `ChemistryQCEvent`, and every event must keep:

```text
scope_changed = false
```

This prevents a correction from becoming a hidden scope-expansion mechanism.

## Fixture coverage

The repository-safe pilot case manifest covers:

```text
CLEAN
SOURCE_INTERNAL_TYPO
FORMULA_OR_CHARGE_OCR_AMBIGUITY
UNDERDETERMINED
CONDITION_SENSITIVE
MISSING_STRUCTURE_OR_FIGURE
EXTERNAL_CLEAN
```

The baseline C-A mixed fixture itself includes a low-confidence `NH₄⁺` item. C-B leaves it `FORMULA_OR_CHARGE_AMBIGUITY / REVIEW_REQUIRED / EXCLUDE_FROM_NEGATIVE_INFERENCE` until rendered-source inspection resolves it.

## Validation

```bash
python -m pip install 'jsonschema>=4.20,<5'
python 'Grade 9/V2/Chemistry/AssessmentReview/contracts/validate_contracts.py'
python 'Grade 9/V2/Chemistry/AssessmentReview/tests/test_chemistry_assessment_review.py'
```

Deterministic replay:

```bash
D='Grade 9/V2/Chemistry/AssessmentReview'
I='Grade 9/V2/Chemistry/AssessmentIntake'
python "$D/engine/review_chemistry_assessment.py" \
  --sources "$I/fixtures/mixed-chemistry-source.fixture.json" \
  --questions "$I/fixtures/mixed-chemistry-question-set.fixture.json" \
  --registry "$D/registry/chemistry-item-validity-registry.json" \
  --policy "$D/policies/chemistry-diagnostic-use-policy.json" \
  --qc-events "$D/registry/chemistry-qc-events.json" \
  --out /tmp/a.json
python "$D/engine/review_chemistry_assessment.py" \
  --sources "$I/fixtures/mixed-chemistry-source.fixture.json" \
  --questions "$I/fixtures/mixed-chemistry-question-set.fixture.json" \
  --registry "$D/registry/chemistry-item-validity-registry.json" \
  --policy "$D/policies/chemistry-diagnostic-use-policy.json" \
  --qc-events "$D/registry/chemistry-qc-events.json" \
  --out /tmp/b.json
cmp /tmp/a.json /tmp/b.json
```

## Non-claims

C-B does not perform scope derivation, learner diagnosis, PCK, Core1/Core2 authoring or publication. AI-assisted fixture review is not a Chemistry-expert approval claim.
