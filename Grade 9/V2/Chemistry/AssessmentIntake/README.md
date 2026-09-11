# Chemistry V2 — Source & Assessment Intake (C-A)

Implements #263 under Chemistry roadmap #262 / programme #234.

## Runtime boundary

```text
ChemistrySourceSet        REQUIRED
QuestionSet / CorpusSet   REQUIRED
AttemptSet                OPTIONAL
DeclaredTopicScope        REQUIRED
```

C-A owns normalization, stable identities, exact Chemistry source/representation custody, the frozen external-corpus denominator, explicit attempt binding, extraction-confidence preservation, deterministic package digests, and the `AssessmentIntakeEnvelope`.

C-A does **not** decide source correctness, item validity, eligibility/scope classification, learner diagnosis, PCK, Core Study Guide content, ExamSIDE transfer support, or publication layout.

## Chemistry fidelity

Contracts preserve distinctions that can carry chemical meaning: formula text, subscript-bearing formulas, ionic charges, coefficients, reaction conditions, physical states, structures, figures/apparatus, observations, and units. Source assertions are immutable evidence here—even when chemically suspect. C-B owns QC and validity.

Each source unit and assessment question has a source-content SHA-256. Mutating a charge, formula, figure dependency, source statement, option set, or part structure without corresponding source evidence fails closed.

## External corpus custody

The full candidate denominator is frozen before any `ELIGIBLE/PARTIAL/OUT_OF_SCOPE` decision. The fixture uses a repository-safe synthetic corpus; this phase deliberately performs no eligibility classification.

## Stable identity

Package digests canonicalize records by stable IDs. Reordering a JSON list does not change semantic package identity, while each record preserves `source_order`.

## Attempt binding

Attempts use `question_ref` plus optional `part_ref`, with `binding_method = EXPLICIT_ID`. Page/order guessing is forbidden.

## Low-confidence preservation

Extraction confidence below 0.90 remains visible in `low_confidence_refs`; intake never upgrades it silently.

## Validation

```bash
python -m pip install 'jsonschema>=4.20,<5'
python 'Grade 9/V2/Chemistry/AssessmentIntake/contracts/validate_contracts.py'
python 'Grade 9/V2/Chemistry/AssessmentIntake/tests/test_chemistry_assessment_intake.py'
```

The synthetic mixed Grade-9 fixture has 14 questions and covers formula/charge parsing, particle↔symbolic representation, conservation, physical/chemical evidence, rules/exceptions, reaction conditions, structure/site dependency, observation/inference, apparatus, oxidation-state tracking, species roles, low-confidence extraction, and a multi-part item.
