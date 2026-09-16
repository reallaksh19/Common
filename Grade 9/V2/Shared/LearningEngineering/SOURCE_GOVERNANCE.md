# Source Governance

Status: **NORMATIVE SOURCE / PROVENANCE POLICY DESIGN**  
Runtime authority: **NONE until source contracts and compilers are promoted**

This document defines how future SKPs and research workers must treat sources. It deliberately separates **discovery**, **evidence suitability**, **authority**, **promotion**, and **provenance**.

## 1. Governing rule

> **SOURCE != AUTHORITY**

A source can be useful for one purpose and inadmissible for another. A search result, popular explanation, question bank, textbook, curriculum document, research paper, or repository fixture does not acquire universal authority merely because it is available.

Discovery is permissive. Promotion is purpose-specific and strict.

## 2. Source intents

Every promoted source must declare why it is being used. Initial shared source intents are:

- `CURRICULUM_AUTHORITY` — board/standard/syllabus scope and wording;
- `SUBJECT_TRUTH` — disciplinary claim, definition, theorem/law, model or relation;
- `DERIVATION_REFERENCE` — derivation/proof/reasoning support;
- `NOVICE_EXPLANATION` — age/level-appropriate explanatory treatment;
- `ADVANCED_EXPLANATION` — deeper treatment not necessarily curriculum authority;
- `MISCONCEPTION_EVIDENCE` — empirical/theoretical evidence about learner thinking;
- `REPRESENTATION_REFERENCE` — evidence/guidance for representations or translations;
- `QUESTION_FAMILY_EVIDENCE` — evidence that a task structure/family is real and relevant;
- `LOCAL_ASSESSMENT` — repository/local assessment corpus source;
- `EXTERNAL_ASSESSMENT` — board/exam/competition/external assessment corpus;
- `RESEARCH_EXTENSION` — advanced or contested research claims beyond base scope;
- `HISTORICAL_CONTEXT` — history/context that must not silently become present-day subject authority.

A source may serve multiple intents, but each intent is evaluated separately.

## 3. Authority tiers are intent-relative

Do not define one universal source ranking. Authority depends on claim type.

Examples:

- An official CBSE syllabus is strong curriculum authority but usually not the best empirical misconception source.
- A peer-reviewed education study may support learner-conception claims but does not define CBSE scope.
- A local question bank is direct evidence of assessment content but not automatic subject-truth authority.
- A university text may support disciplinary derivation but may be unsuitable as Grade 9 novice exposition.

A source record should therefore declare both `authority_tier` and `source_intent`.

## 4. Minimum source record semantics

Future source contracts should support at least:

- `source_id`;
- source type;
- title/creator/organization;
- exact retrieval/version/publication identity;
- local vs web provenance;
- `source_intents[]`;
- authority tier per intent where needed;
- curriculum/grade/subject applicability;
- intended knowledge/research depth;
- claim refs supported;
- capability/problem-family refs supported;
- selection reason;
- limitations;
- learner/research population when relevant;
- conflicts with other sources;
- freshness/version requirements;
- corroboration policy;
- licensing/reuse status;
- retrieval reference and content digest where legally/technically available;
- review/promotion state.

Links alone are not sufficient source records.

## 5. Selection reason

A promoted source must explain why it was chosen for its intent. Good selection reasons are auditable and comparative, for example:

- official curriculum authority for exact 2026–27 scope;
- peer-reviewed study directly examines the target learner conception;
- primary standards document preferred over a secondary summary;
- source contains the canonical theorem proof used to validate a derivation;
- local corpus is the actual assessment population being analyzed.

Bad selection reasons include:

- “first search result”;
- “looks reliable”;
- “common website”;
- “used in the previous topic”;
- “the agent remembers this source.”

## 6. Discovery versus promotion

Discovery may retain:

- weak candidates;
- conflicting sources;
- incomplete metadata;
- exploratory explanations;
- out-of-scope references;
- sources that fail licensing or freshness checks.

Promotion must declare a disposition such as:

- `PROMOTED_FOR_INTENT`;
- `CANDIDATE`;
- `CORROBORATION_REQUIRED`;
- `CONFLICTING`;
- `SUPERSEDED`;
- `OUT_OF_SCOPE`;
- `REJECTED_AUTHORITY`;
- `REUSE_RESTRICTED`;
- `UNRESOLVED`.

Do not delete inconvenient conflicts from the discovery record simply to obtain a clean canonical package.

## 7. Claim-level support

Sources should bind to specific claims or obligations rather than being attached only at document level.

A claim support record should be able to state:

```text
claim_ref
source_ref
source_intent
support_type
scope/applicability
limitations
corroboration_state
```

A source can support one claim and be irrelevant to another.

## 8. Corroboration

Corroboration policy should be risk-sensitive rather than count-based.

Do not require “three sources” merely to satisfy a schema. Instead consider:

- claim importance;
- authority quality;
- whether the claim is contested;
- source independence;
- target population applicability;
- freshness sensitivity;
- research depth.

A single primary/official authority may be sufficient for a curriculum fact. A contested learner-conception claim may require multiple studies or a deliberately `UNRESOLVED` state.

## 9. Conflict handling

When promoted-quality sources disagree:

1. preserve both exact source identities;
2. classify the conflict;
3. identify whether scopes/populations/definitions differ;
4. state which downstream claims are affected;
5. apply a governed adjudication rule if one exists;
6. otherwise keep the claim `CONFLICTING` or `UNRESOLVED`.

Never resolve a substantive conflict by majority vote across agents or sources alone.

Conflict types should include at least:

- curriculum-version conflict;
- terminology/definition mismatch;
- domain-truth conflict;
- model/approximation mismatch;
- population/context mismatch;
- pedagogical interpretation conflict;
- assessment-scope conflict;
- freshness/supersession conflict.

## 10. Freshness and versioning

Some source claims are stable; others are version-sensitive.

Version-sensitive examples include:

- curriculum/syllabus year;
- exam pattern/rules;
- current standards;
- current reference data or accepted nomenclature where revised;
- software/tool documentation used by generation infrastructure.

Every curriculum binding must carry the exact curriculum version/year. Do not silently reuse last year's scope.

## 11. Population and context

Education research is context-dependent. A misconception/PCK/progression source should record, where available:

- age/grade;
- prior instruction;
- country/curriculum;
- sample/task context;
- study design;
- limits on transfer to the target learners.

An observed pattern in university students must not automatically become a Grade 9 canonical misconception.

## 12. Learner-conception claims

Use the ontology in `SUBTOPIC_KNOWLEDGE_MODEL.md`. In particular, do not label an error as `MISCONCEPTION` merely because an explanatory website says “students often think…”.

Prefer empirically grounded evidence when making population claims. When evidence is weak, use `COMMON_ERROR`, `UNVERIFIED_HYPOTHESIS`, or another weaker class as appropriate.

## 13. Curriculum sources

Curriculum research should separate:

- exact explicit requirement;
- reasonable derivation/implication;
- prerequisite bridge;
- competitive extension;
- research extension.

The source ledger must preserve this distinction. A competitive-exam question does not rewrite the official curriculum; it creates a separate assessment/extension binding.

## 14. Question banks and assessments

Question banks are source corpora, not domain authority.

For local/external assessment records, capture:

- exact question identity/source;
- fidelity/review status;
- year/exam context where available;
- scope/capability/problem-family mapping;
- answer/solution provenance;
- reuse/licensing state.

A question that appears to require an unknown capability should create an explicit mapping/scope issue. Do not invent canonical content solely to absorb it.

## 15. Licensing and reuse

Source metadata should distinguish factual/research use from reproduction rights.

At minimum future contracts should be able to represent:

- public-domain/open-license;
- licensed/local-use permitted;
- citation/reference only;
- reproduction restricted;
- unknown/review required.

A technically strong source can still be unusable for reproduced learner-facing content. That is a reuse/publication constraint, not evidence that the underlying claim is technically false.

## 16. Provenance model

**Provenance is not truth.** Provenance establishes custody, derivation history, and responsibility; semantic correctness must be evaluated separately.

The target model is structurally compatible with W3C PROV:

- **Entity** — source document, dataset, question, package, receipt, generated artifact;
- **Activity** — search, extraction, normalization, reconciliation, validation, promotion, review, migration;
- **Agent** — human reviewer, organization, software/compiler, task agent.

Useful relations conceptually include “used”, “was generated by”, “was attributed to”, “was derived from”, and role-qualified responsibility.

The design goal is reproducibility and custody, not wholesale adoption of RDF/PROV serialization in v1.

## 17. Agent research protocol

A research worker should operate in this order:

1. read the package source plan and exact task scope;
2. discover broadly;
3. create candidate source records without promotion assumptions;
4. map sources to intended claims/obligations;
5. record limitations/conflicts;
6. apply intent-specific authority rules;
7. return unresolved gaps explicitly;
8. allow a separate compiler/reviewer to promote legal records.

The worker should not rewrite package scope because a convenient source covers a different topic.

## 18. Search-engine / web-ranking invariance

Canonical authority must not depend on search result order alone.

Metamorphic test:

> Reordering equivalent discovery results without changing the underlying evidence must not change the promoted package solely because a different source appeared first.

Selection must be explainable by authority/intents/evidence, not ranking position.

## 19. Research depth and sources

### FOUNDATION

Requires the minimum appropriate authority for curriculum/domain truth and critical validity/prerequisite claims.

### STANDARD

Adds broader corroboration, pedagogical evidence where available, problem-family/representation support, and explicit conflicts.

### RESEARCH

Requires a stronger claim ledger/literature dossier, explicit contested interpretations, higher provenance completeness, and stronger supersession/conflict rules.

Research depth increases evidence obligations; it does not imply a more knowledgeable learner.

## 20. Source-plan completeness versus source abundance

A package is not evidence-complete because it has many URLs. It is evidence-complete when declared evidence obligations have appropriate support or an explicit unresolved disposition.

This distinction should be enforced by future compilers:

```text
source count      ≠ evidence closure
search coverage   ≠ authority closure
provenance        ≠ truth
```

## 21. Known source-governance limitations

- Current repository source metadata is heterogeneous across Physics, Mathematics, and Chemistry.
- Licensing/reuse status is not consistently modeled.
- Many existing pedagogical claims were created before a shared intent taxonomy existed.
- Empirical learner-conception evidence is uneven across school-level subtopics.
- Web sources can disappear or change; content digests and retrieval metadata will need policy decisions.
- A source-quality scoring model is intentionally not defined here; a single scalar would hide purpose-specific authority.

## 22. Research references informing this policy

These references inform the provenance/pedagogical governance model but do not themselves authorize subject claims in SKPs:

- W3C, *PROV Model Primer*: https://www.w3.org/TR/prov-primer/
- W3C, *PROV Overview*: https://www.w3.org/TR/prov-overview/
- Jin et al. (2019), learning progression coherence/validation: https://doi.org/10.1002/sce.21525
- Grigaliūnienė et al. (2025), topic-specific Mathematics PCK: https://doi.org/10.1007/s11858-025-01684-1
- Taber (2013), chemistry representation/model complexity: https://doi.org/10.1039/C3RP00012E
