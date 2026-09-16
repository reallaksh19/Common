# SKP Schema Roadmap

Status: **DESIGN ROADMAP WITH FOUNDATIONAL PILOT CONTRACTS**  
Bulk library population: **BLOCKED** until diversity-pilot exit criteria and schema activation are satisfied.

This roadmap translates `SUBTOPIC_KNOWLEDGE_MODEL.md` into staged machine contracts. Seven foundational modules now have executable **PILOT** contracts and a synthetic subject-neutral fixture. They remain **non-runtime**, do not authorize production consumption, and are not sufficient to describe a complete SKP. The remaining modules are still `PLANNED`. The machine-readable status source is `registry/skp-schema-roadmap.v1.json`.

There is still **no top-level production SKP schema, no production SKP compiler, and no active SKP-to-Engineering promotion path**. Existing Physics, Mathematics, Chemistry, Shared EngineeringGate, CrossDomain and HumanReview authorities remain unchanged.

## 1. Why modular schemas

A single giant schema would create three problems:

1. subject-specific fields would become meaningless filler for other subjects;
2. schema evolution would require breaking the whole package for local changes;
3. agents could satisfy structural counts while semantic ownership remained unclear.

SKP v1 therefore uses a small shared kernel plus subject extensions. Modules advance independently through a maturity lifecycle and must not become runtime authority merely because a contract file exists.

## 2. Shared-kernel and infrastructure modules

| Module | Status | Purpose | Initial dependency |
|---|---|---|---|
| `identity` | **PILOT** | stable package/object IDs, aliases, version/supersession | none |
| `scope` | **PILOT** | includes/excludes/boundaries | identity |
| `curriculum_binding` | **PILOT** | board/grade/version/classification/evidence | identity, scope |
| `capability` | **PILOT** | stable teachable/assessable abilities | identity, scope |
| `prerequisite_edge` | **PILOT** | typed dependencies, rationale, missing behavior, provider ownership | capability |
| `concept` | PLANNED | meaning-bearing disciplinary constructs | identity |
| `relation` | PLANNED | formal relations and applicability envelope | concept, capability |
| `reasoning_sequence` | PLANNED | semantic reasoning jobs and fragile jumps | capability, relation |
| `representation` | PLANNED | representations, purpose, alternatives, translations | capability, concept |
| `learner_conception` | PLANNED | evidence-backed errors/resources/hypotheses | capability, source_record |
| `problem_family` | PLANNED | structural task families and transfer boundaries | capability, reasoning_sequence |
| `verification_route` | PLANNED | subject-appropriate result/reasoning checks | relation, problem_family |
| `source_plan` | **PILOT** | evidence obligations by intent | scope |
| `source_record` | **PILOT** | actual sources, purpose, selection reason, limitations | source_plan |
| `assessment_binding` | PLANNED | stable question-corpus bindings | capability, problem_family |
| `adaptation_policy` | PLANNED | what learner evidence may change | capability, representation |
| `research_overlay` | PLANNED | depth-specific claims/evidence/supersession | source_record, relation |
| `provenance` | PLANNED | entities/activities/agents/custody | identity, source_record |
| `maturity` | PLANNED | discovery/pilot/validated/active/superseded lifecycle | provenance |

The seven PILOT modules are exercised only through `fixtures/skp-pilot-kernel.synthetic.fixture.json` and `tests/test_skp_pilot_kernel.py`. The synthetic fixture is deliberately not Physics, Mathematics, Chemistry, Relative Motion, or any other real content case. Shared semantics must survive without case knowledge.

## 3. What the foundational PILOT kernel proves

The current pilot contracts establish only these boundaries:

- stable package identity and version/supersession shape;
- explicit scope include/exclude/boundary structure;
- versioned curriculum classification with evidence refs;
- capability identity, disciplinary meaning, learner-success semantics and observability;
- prerequisite edge type, rationale, hardness, missing behavior and provider ownership;
- source-plan obligations by declared source intent;
- source records with purpose-specific disposition, selection reason, limitations, corroboration and licensing state.

The synthetic semantic validator additionally falsifies:

- duplicate capability IDs;
- unresolved remembered references;
- external prerequisites without provider-owned authority;
- empirical-progression claims without progression evidence;
- HARD prerequisites marked `NO_BLOCK`;
- silent prerequisite cycles;
- promoted sources without an adequate selection reason;
- disappearance of required exact source evidence without an explicit hold.

These checks are **pilot evidence**, not production authorization.

## 4. Planned subject extensions

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

Extensions may add subject semantics but may not redefine shared meanings such as capability, prerequisite, source, maturity, provenance, or evidence state.

All three subject adapters remain `PLANNED` and `runtime_authority=false` until diversity pilots demonstrate that the shared kernel is adequate.

## 5. Target package composition

The long-term package may resemble the following composition, but this is **not a schema** and has no runtime authority:

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

A top-level SKP contract should not be created until enough component semantics exist to avoid encoding a premature Physics-shaped structure.

## 6. Cross-reference validation requirements

A future SKP compiler must validate more than JSON Schema can express reliably:

- unique stable IDs;
- all references resolve;
- prerequisite graph cycle policy;
- external prerequisite provider ownership;
- curriculum binding version presence;
- relation symbols/objects and validity refs resolve;
- reasoning sequences reference legal capabilities/relations;
- representation translations are semantically typed;
- problem families reference existing capabilities/reasoning/verification;
- source claims bind to existing package claims/objects;
- learner-conception classes meet evidence policy;
- research overlay base digest matches the exact package;
- same-ID mutation is detected;
- maturity promotion has required evidence/tests.

The PILOT kernel already begins this semantic-validation layer for the seven foundational modules. JSON Schema validity alone is not promotion authority.

## 7. Schema maturity lifecycle

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

A module must not jump directly from `PLANNED` or `PILOT` to `ACTIVE` to satisfy a production deadline.

`PILOT` means the contract is executable and falsifiable. It does **not** mean:

- valid production input;
- semantic correctness across subjects;
- permission for library backfill;
- Engineering readiness;
- publication readiness.

## 8. Activation requirements

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

Foundational PILOT contracts have not yet satisfied this full activation list.

## 9. Pilot order

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

These are bounded architecture pilots. They are not permission to populate a broad topic library.

## 10. Pilot exit criteria

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

## 11. Bulk population gate

`registry/skp-schema-roadmap.v1.json` currently declares:

```text
bulk_population_allowed = false
bulk_population_state = BLOCKED_UNTIL_DIVERSITY_PILOTS_AND_SCHEMA_ACTIVATION
```

This remains false even though seven modules are now PILOT.

Do not open bulk population until:

- required shared modules are at least `VALIDATED`;
- all four diversity pilots are complete;
- independent-agent structural comparison has run;
- schema migration policy exists;
- the architecture review explicitly opens library population.

Before that point, only bounded synthetic fixtures and declared diversity-pilot packages are legal.

## 12. Question/assessment corpus roadmap

The assessment corpus is intentionally separate from SKP content.

A planned question-record contract should eventually support:

- question/source ID and exact custody;
- exam/curriculum/year metadata;
- capability refs;
- problem-family ref;
- representation/reasoning demands;
- prerequisite refs;
- solution/answer provenance;
- reuse/licensing state;
- mapping/review status.

SKPs should bind stable question IDs rather than duplicate question bodies.

## 13. Independent-agent reproducibility roadmap

After enough schema modules exist for real pilots, run at least three clean-context agents on the same governed task and compare structural outputs:

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

## 14. Next schema tranche

Do **not** create all remaining modules at once.

The next bounded tranche should implement only the minimum semantics required to make the first diversity pilot meaningful:

- `concept`;
- `relation` plus applicability/validity semantics;
- `reasoning_sequence` and high-fragility jumps;
- `representation` and representation-translation obligations;
- `verification_route`;
- `problem_family` if required by the first pilot.

Only after those contracts survive a real Physics pilot should `learner_conception`, `assessment_binding`, `adaptation_policy`, `research_overlay`, `provenance`, and `maturity` advance as needed. Mathematics and Chemistry pilots must then challenge the shared design before any module becomes `ACTIVE`.

## 15. Roadmap success metrics

The dominant repository change for an ordinary new subtopic should eventually be `DATA_ONLY`.

Track at least:

- percentage of ordinary subtopics requiring global engine changes;
- percentage requiring Blueprint changes (target: zero);
- promoted claims with provenance;
- external prerequisites without declared provider owner (target: zero);
- learner-state mutations of domain truth (target: zero);
- research-overlay silent base mutations (target: zero);
- source records without selection reason (target: zero);
- unresolved contradictions at promotion;
- independent-agent structural agreement after calibration.

These are project engineering targets, not published educational-effect thresholds.
