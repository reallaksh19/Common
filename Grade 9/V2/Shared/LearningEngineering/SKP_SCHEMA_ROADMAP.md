# SKP Schema Roadmap

Status: **DESIGN ROADMAP**  
Bulk library population: **BLOCKED** until pilot exit criteria are satisfied.

This roadmap translates `SUBTOPIC_KNOWLEDGE_MODEL.md` into a staged machine-contract plan. It intentionally does **not** create the operational SKP schemas yet. The machine-readable status source is `registry/skp-schema-roadmap.v1.json`.

## 1. Why modular schemas

A single giant schema would create three problems:

1. subject-specific fields would become meaningless filler for other subjects;
2. schema evolution would require breaking the whole package for local changes;
3. agents could satisfy structural counts while semantic ownership remained unclear.

SKP v1 therefore uses a small shared kernel plus subject extensions.

## 2. Planned shared-kernel modules

| Module | Purpose | Initial dependency |
|---|---|---|
| `identity` | stable package/object IDs, aliases, version/supersession | none |
| `scope` | includes/excludes/boundaries | identity |
| `curriculum_binding` | board/grade/version/classification/evidence | identity, scope |
| `capability` | stable teachable/assessable abilities | identity, scope |
| `prerequisite_edge` | typed dependencies, rationale, missing behavior | capability |
| `concept` | meaning-bearing disciplinary constructs | identity |
| `relation` | formal relations and applicability envelope | concept, capability |
| `reasoning_sequence` | semantic reasoning jobs and fragile jumps | capability, relation |
| `representation` | representations, purpose, alternatives, translations | capability, concept |
| `learner_conception` | evidence-backed errors/resources/hypotheses | capability, source_record |
| `problem_family` | structural task families and transfer boundaries | capability, reasoning_sequence |
| `verification_route` | subject-appropriate result/reasoning checks | relation, problem_family |
| `source_plan` | evidence obligations by intent | scope |
| `source_record` | actual sources, purpose, provenance, limitations | source_plan |
| `assessment_binding` | stable question-corpus bindings | capability, problem_family |
| `adaptation_policy` | what learner evidence may change | capability, representation |
| `research_overlay` | depth-specific claims/evidence/supersession | source_record, relation |
| `provenance` | entities/activities/agents/custody | all promotable entities |
| `maturity` | discovery/draft/pilot/validated/active/superseded | provenance |

These names are conceptual module IDs. Exact file/field names may change during pilot design, but their semantic responsibilities should not be silently merged.

## 3. Planned subject extensions

### Physics

Candidate modules/fields:

- physical model/system;
- physical quantity/unit/dimension;
- reference frame/sign convention;
- state variables/phase continuity;
- physical laws/equations;
- vector/graph/diagram semantics;
- limiting-case and physical-plausibility verification.

### Mathematics

Candidate modules/fields:

- mathematical object/definition;
- axiom/assumption/domain restriction;
- theorem/lemma dependency;
- proof obligation/proof family;
- construction and representation semantics;
- equivalence/implication distinction;
- counterexample and proof verification.

### Chemistry

Candidate modules/fields:

- substance/species/entity;
- phenomenon/observation;
- particulate/submicroscopic model;
- symbolic/notation/formula/equation semantics;
- reaction/process conditions;
- conservation/stoichiometry;
- experiment/source-obligation semantics;
- explicit representation translations.

Extensions may add subject semantics but may not redefine shared meanings such as capability, prerequisite, source, maturity, or provenance.

## 4. Planned package composition

Target top-level shape, for discussion only:

```json
{
  "skp_id": "...",
  "schema_version": "...",
  "subject": "...",
  "subject_extension_ref": "...",
  "identity": {},
  "scope": {},
  "curriculum_bindings": [],
  "capabilities": [],
  "prerequisite_edges": [],
  "concepts": [],
  "relations": [],
  "reasoning_sequences": [],
  "representations": [],
  "learner_conceptions": [],
  "problem_families": [],
  "verification_routes": [],
  "source_plan": {},
  "source_ledger": [],
  "assessment_bindings": [],
  "learner_adaptation": {},
  "research_overlays": [],
  "open_issues": [],
  "provenance": {},
  "maturity": {}
}
```

This example is **not a schema** and has no runtime authority.

## 5. Cross-reference validation requirements

A future SKP compiler should validate more than JSON Schema can express easily:

- unique stable IDs;
- all refs resolve;
- prerequisite graph cycle policy;
- external prerequisite provider ownership;
- curriculum binding version presence;
- relation symbols/objects and validity refs resolve;
- reasoning sequences reference legal capabilities/relations;
- representation translations are semantically typed;
- problem families reference existing capabilities/reasoning/verification;
- source claims bind to existing package claims/objects;
- learner-conception classes meet evidence policy;
- research overlay base digest matches exact package;
- same-ID mutation is detected;
- maturity promotion has required evidence/tests.

These semantic validators are as important as structural schema validation.

## 6. Planned schema maturity lifecycle

Each module follows:

```text
PLANNED
  ↓ ontology + fixture design
PILOT
  ↓ diversity cases + falsifiers
VALIDATED
  ↓ migration/version policy + declared producers/consumers
ACTIVE
  ↓ production use
DEPRECATED / SUPERSEDED
```

A module must not jump directly from `PLANNED` to `ACTIVE` to satisfy a production deadline.

## 7. Activation requirements

Before any shared module can become `ACTIVE`, it must have:

- normative semantic definition;
- JSON Schema or equivalent executable contract;
- positive minimal fixture;
- positive rich fixture;
- negative/falsifier fixtures;
- semantic cross-reference validator where needed;
- producer ownership;
- declared consumers;
- digest/version custody;
- migration/supersession rule;
- at least one non-Physics pilot if the module claims shared applicability.

## 8. Pilot order

### Pilot P1 — Physics Relative Motion / STANDARD

Stress:

- curriculum explicit-vs-derived classification;
- reference frames;
- vector/cross-domain prerequisites;
- representation translation;
- question-family mapping;
- clean-agent reproducibility.

### Pilot P2 — Physics Thermodynamics / RESEARCH

Stress:

- large prerequisite graph;
- model/applicability conditions;
- research claim ledger;
- contested/advanced source handling;
- STANDARD→RESEARCH invariance.

### Pilot P3 — Mathematics geometry or trigonometry

Stress:

- definition/theorem/proof dependency rather than physical models;
- construction/diagram/symbolic representations;
- counterexamples;
- conceptual versus procedural PCK.

### Pilot P4 — Chemistry atomic/bonding/reaction case

Stress:

- phenomenon ↔ model ↔ symbolic transitions;
- condition semantics;
- conservation/stoichiometry;
- source/experiment obligations;
- notation ambiguity.

## 9. Pilot exit criteria

Do not freeze SKP v1 until all four pilots establish:

1. no normal case requires a topic-specific global Blueprint branch;
2. shared fields remain meaningful across all subjects;
3. subject-specific semantics are expressible through adapters;
4. missing evidence remains held/unresolved without filler;
5. learner state does not mutate domain truth;
6. research depth does not silently mutate base truth;
7. independent clean agents can reconstruct package structure from repository authority;
8. source-selection reasons are auditable;
9. assessment bindings do not force domain ontology changes merely to absorb questions;
10. semantic falsifiers detect same-ID drift, broken refs, unsupported promotion, and illegal cross-domain ownership.

## 10. Bulk population gate

`registry/skp-schema-roadmap.v1.json` currently declares:

```text
bulk_population_allowed = false
```

This should remain false until:

- required shared modules are at least `VALIDATED`;
- all four diversity pilots are complete;
- independent-agent structural comparison has run;
- schema migration policy exists;
- the architecture review explicitly opens library population.

Before that point, only bounded pilot packages/fixtures should be created.

## 11. Question/assessment corpus roadmap

The assessment corpus is intentionally separate from SKP content.

Planned question-record contract should eventually support:

- question/source ID and exact custody;
- exam/curriculum/year metadata;
- capability refs;
- problem-family ref;
- representation/reasoning demands;
- prerequisite refs;
- solution/answer provenance;
- reuse/licensing state;
- mapping/review status.

SKPs bind question IDs rather than duplicate source text.

## 12. Independent-agent reproducibility roadmap

After schema pilots, run at least three clean-context agents on the same task package and compare structural outputs:

- scope;
- capability IDs/granularity;
- prerequisite edges;
- relation/validity identities;
- source obligations;
- representation requirements;
- problem families;
- learner-conception classification;
- unresolved issues;
- readiness result.

Disagreement classes should include:

- wording/alias only;
- granularity difference;
- scope difference;
- prerequisite conflict;
- domain truth conflict;
- source conflict;
- pedagogical choice;
- evidence gap;
- schema ambiguity.

Do not resolve domain conflicts by agent majority vote.

## 13. Roadmap success metric

The dominant repository change for an ordinary new subtopic should eventually be `DATA_ONLY`.

Track at least:

- percentage of ordinary subtopics requiring global engine changes;
- percentage requiring Blueprint changes (target: zero);
- promoted claims with provenance;
- external prerequisites without declared provider owner (target: zero);
- learner-state mutations of domain truth (target: zero);
- research overlay silent base mutations (target: zero);
- source records without selection reason (target: zero);
- unresolved contradictions at promotion;
- independent-agent structural agreement after calibration.

These are project engineering targets, not published educational-effect thresholds.
