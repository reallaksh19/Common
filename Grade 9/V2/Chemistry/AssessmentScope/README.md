# Chemistry V2 C-C — Source / Scope Reconciliation

Implements issue **#265** and depends on Chemistry V2 C-A / C-B.

This phase resolves the supplied source, assessment questions, external-corpus candidates, declared topic boundary, and canonical Chemistry authority into explicit scope records. It does **not** diagnose a learner and does not author Core1/Core2 material.

## Mandatory authority order

```text
C-A exact source/question/corpus custody
→ C-B source integrity + item validity
→ C-C source obligations + scope reconciliation
→ only then later problem-family / learner-state / authoring phases
```

Four authorities stay distinct:

```text
ChemistrySourceSet      = what the supplied source actually contains
QuestionSet / CorpusSet = evidence of assessment / transfer demand
DeclaredTopicScope      = publication boundary
Canonical Chemistry     = chemical meaning / capabilities / prerequisites
```

No authority silently overwrites another.

## Pilot baseline

The mixed Grade-9 Chemistry fixture resolves:

```text
SOURCE UNITS                    12
SOURCE ELIGIBLE                 10
SOURCE OUTSIDE DECLARED SCOPE    2

QUESTION / SUBPART ITEMS        17
QUESTION ELIGIBLE               14
QUESTION OUTSIDE SCOPE           2
QUESTION SOURCE-UNRESOLVED       1

EXTERNAL CANDIDATES              6
EXTERNAL ELIGIBLE                5
EXTERNAL SOURCE-UNRESOLVED       1
```

The explicit mismatches are intentional architecture evidence:

- `CS08` / `CQ08`: structure/site reasoning exists in the supplied fixture but is absent from the declared topic/subtopic boundary.
- `CS11` / `CQ11`: oxidation-state tracking exists in the supplied fixture but is absent from the declared topic/subtopic boundary.
- `CQ13`: C-B marks the low-confidence formula/charge item `REVIEW_REQUIRED`, so C-C refuses to promote it.
- `EXT06`: extraction confidence is below the pilot threshold and the source body is unavailable, so the title alone cannot make it eligible.

This proves that source presence, question presence, and external topic/title labels do not automatically enlarge the declared learner scope.

## Canonical mapping

The pilot authority registry is intentionally narrow and repository-safe. It provides concept/capability IDs, prerequisite edges, declared-topic allowances, and provisional problem-family mechanism IDs. C-D owns later problem-family/reasoning-route maturity.

Every eligible question/candidate receives exactly one `primary_learner_unit`. `SUPPORTS`-style secondary linkage belongs to later transfer/publication semantics.

## Record-derived counters

All totals are recomputed from source obligations, question bindings, and external classification records. Input registries containing asserted summary/counter fields are rejected.

## Fail-closed rules

The engine rejects:

```text
SOURCE_OBLIGATION_DROPPED_DURING_SCOPE_DERIVATION
EXAMSIDE_TOPIC_LABEL_TREATED_AS_ELIGIBILITY
DECLARED_SCOPE_SILENTLY_OVERRIDES_SOURCE
QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE
CANONICAL_CHEMISTRY_SILENTLY_ADDS_UNDECLARED_TOPIC
QUESTION_WITHOUT_EXPLICIT_SCOPE_STATE
PREREQUISITE_INFERRED_BUT_NOT_RECORDED
CONDITION_EXCEPTION_INFERRED_BUT_NOT_RECORDED
REPRESENTATION_DEPENDENCY_DROPPED
ELIGIBLE_ITEM_WITHOUT_UNIQUE_PRIMARY_HOME
COUNTERS_ACCEPTED_WITHOUT_RECORD_DERIVATION
```

Low-confidence external evidence is also prevented from becoming eligible merely because its title looks relevant.

## Outputs

`build_chemistry_scope.py` emits one deterministic bundle containing:

- source-obligation closure;
- scope-reconciliation findings;
- Chemistry assessment-scope model;
- prerequisite closure;
- external-corpus classification counters;
- end-to-end coverage matrix;
- exact upstream source/question/corpus/review digests.

## Boundary

This phase does **not** claim:

- learner diagnosis or treatment;
- mature problem-family definitions or ChemistryReasoningRoutes;
- Core Study Guide authoring;
- Appendix A/B/C quality;
- ExamSIDE hint/solution maturity;
- publication readiness;
- human Chemistry-expert approval.

The pilot authority and mappings are `AI_ASSISTED_PILOT_AUTHORITY` artifacts for architecture validation.
