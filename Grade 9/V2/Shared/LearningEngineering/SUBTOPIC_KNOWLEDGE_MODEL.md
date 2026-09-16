# Subtopic Knowledge Model

Status: **NORMATIVE ONTOLOGY / SKP v1 DESIGN INPUT**  
Runtime authority: **NONE until corresponding machine contracts are promoted**

This document defines the semantic terms that future Subtopic Knowledge Packages (SKPs) must use consistently across subjects and agents. It exists to prevent schema-compliant but semantically incompatible packages.

## 1. Granularity principle

An SKP is a bounded instructional/domain knowledge package. Its internal units should be small enough to support prerequisite, reasoning, representation, assessment, and learner-evidence relationships, but not so small that every algebraic manipulation or sentence becomes a separate capability.

A unit should be split when at least one of these changes materially:

- prerequisite set;
- validity/applicability condition;
- reasoning obligation;
- representation demand;
- assessment observability;
- transfer behavior;
- learner-evidence interpretation.

A unit should normally remain combined when the proposed split only changes wording, notation, example context, or a mechanically inseparable substep.

Granularity is a governed design decision. `more nodes = more rigor` is false.

## 2. Core entities

### Topic

A broad disciplinary/curricular grouping. Topic names are navigation metadata, not runtime logic keys.

### Subtopic

A stable bounded scope that can own an SKP. A subtopic may be curriculum-explicit, curriculum-derived, a prerequisite bridge, competitive extension, or research extension. Scope classification must be evidence-backed.

### Capability

The smallest stable teachable/assessable disciplinary ability useful to downstream reasoning, prerequisite, assessment, or learner-evidence systems.

A capability is not:

- a page heading;
- a single example;
- a learner mastery state;
- a source quotation;
- a topic-name alias.

A capability should record what successful use means and what evidence could observe it.

### Concept

A disciplinary construct or meaning-bearing object. Concepts may support multiple capabilities. A concept is not automatically a capability because knowing a definition and using it in reasoning are different claims.

### Relation

A governed formal relationship used in disciplinary reasoning. Subject adapters specialize this notion:

- Physics: laws/equations/constitutive or kinematic relations;
- Mathematics: identities, implications, equivalences, formulas, theorem conclusions, transformations;
- Chemistry: equations, quantitative relations, conservation/stoichiometric relations, process relationships.

Every relation must expose subject-appropriate meaning, symbols/objects, applicability/validity conditions, and verification routes.

### Validity / applicability condition

A condition under which a relation, theorem, model, procedure, approximation, or interpretation is legal. It is a first-class object, not prose hidden in an explanation.

### Representation

A meaning-bearing external form used to express or reason about disciplinary content: diagram, graph, table, symbolic expression, verbal form, construction, particulate model, state table, vector diagram, etc.

A representation record should distinguish:

- what information it encodes;
- instructional/disciplinary purpose;
- required noticing target;
- potential misleading affordances;
- translation obligations to other forms;
- whether it is required, optional, alternative, or selected.

### Representation translation

A governed mapping between forms, not merely co-presence on a page. It records what semantic information must survive the translation and what learner action demonstrates the translation.

Examples include picture → words → symbols → equation in Physics, diagram → statement → proof relation in Mathematics, and phenomenon/model/symbol transitions in Chemistry.

### Reasoning sequence

A reusable disciplinary route from interpretation to justified result. It records semantic jobs rather than learner-facing hint text.

A reasoning sequence may include high-fragility transitions but must not be treated as the only permissible learner strategy unless the domain requires that order.

### High-fragility jump

A reasoning transition whose omission or misuse can invalidate the result and which a novice may not automatically reconstruct. Fragility requires rationale/evidence; it is not a synonym for “important.”

### Problem family

A class of tasks that share structural reasoning demands. A family should include recognition signals, required capabilities, validity conditions, representation demands, reasoning skeleton, first moves, meaningful variants, verification routes, and transfer boundaries.

Surface context alone does not define a problem family.

### Verification route

An independent or complementary way to check a result or reasoning path. Subject-specific examples include dimensional/limiting/physical plausibility checks, proof/counterexample/substitution checks, and conservation/stoichiometric/experimental checks.

## 3. Prerequisite and progression ontology

### Prerequisite edge

A directed dependency between two capabilities or knowledge objects. Every edge must state **why** the dependency exists and what happens if it is unavailable.

Required fields conceptually include:

- `from_ref` / `to_ref`;
- `edge_type`;
- rationale;
- evidence refs;
- hardness;
- missing behavior;
- bridge availability;
- provider/owner for external-domain dependencies.

### Edge types

- `STRUCTURAL_PREREQUISITE` — logically/domain required.
- `EXTERNAL_DOMAIN_PREREQUISITE` — required but provider authority belongs to another domain.
- `CURRICULUM_PREREQUISITE` — required by curriculum ordering/expectation, which may differ from logical necessity.
- `PEDAGOGICAL_BRIDGE` — instructional support useful for access, not a domain law.
- `OPTIONAL_ENRICHMENT` — useful extension but not required for target closure.

### Missing behavior

A prerequisite gap can produce one of:

- `HARD_BLOCK`;
- `BRIDGE_REQUIRED`;
- `EXTRA_SCAFFOLD`;
- `DIAGNOSTIC_CHECK`;
- `NO_BLOCK`;
- `UNRESOLVED`.

The behavior is policy/data, not inferred from topic identity.

### Progression status

Do not equate prerequisite structure with empirical learning order.

- `HYPOTHESIZED_PROGRESSION` — proposed developmental/instructional sequence supported by theory, expert reasoning, or indirect evidence but not validated for the target learner population/context.
- `EMPIRICALLY_SUPPORTED_PROGRESSION` — supported by declared learner/population evidence, with context limitations recorded.

The same subtopic may contain both structural prerequisites and multiple viable pedagogical routes.

## 4. Learner-conception ontology

Incorrect responses must not automatically be labeled misconceptions.

Allowed conceptual classes should include:

- `MISCONCEPTION` — sufficiently supported evidence for a relatively stable incorrect conceptual model in a declared context/population;
- `COMMON_ERROR` — recurring wrong result or action without a warranted stable-conception claim;
- `CONTEXTUAL_RESOURCE` — productive or partially productive idea activated appropriately/inappropriately depending on context;
- `OVERGENERALIZATION` — valid rule/resource extended beyond its legal domain;
- `REPRESENTATION_ERROR` — error primarily in reading/translating/constructing a representation;
- `PROCEDURAL_ERROR` — execution/procedure error without evidence of conceptual model failure;
- `LANGUAGE_CONFUSION` — ambiguity or ordinary/technical-language mismatch;
- `UNVERIFIED_HYPOTHESIS` — plausible teaching hypothesis not yet supported enough for stronger classification.

Every learner-conception record should include:

- target concept/capability refs;
- evidence source(s);
- population/context;
- task context;
- strength/limitations;
- distinguishing diagnostic evidence;
- instructional implications where warranted.

## 5. Cognitive transformation

A pedagogical record can describe a learner-state transition such as:

```text
novice/initial state
→ instructional transformation
→ intended disciplinary state
→ verification/observation
```

This is not chain-of-thought. It is an auditable state-transition specification useful for teaching design.

The initial state may be `UNKNOWN`; no deficiency should be invented when learner evidence is absent.

## 6. Examples and fading

Examples are governed by purpose, not count.

Useful roles include:

- worked example;
- partially worked/faded example;
- guided attempt;
- independent attempt;
- retrieval task;
- non-example;
- counterexample;
- boundary/limiting case;
- error diagnosis;
- transfer task.

A worked→faded→independent lineage should preserve the structural invariant/problem family being learned while withdrawing support deliberately. It should not be claimed merely because three questions appear in increasing numerical difficulty.

## 7. Curriculum binding

Curriculum is an overlay on domain truth. A subtopic/capability can be classified per curriculum/version as:

- `CURRICULUM_REQUIRED`;
- `CURRICULUM_DERIVED`;
- `PREREQUISITE_BRIDGE`;
- `COMPETITIVE_EXTENSION`;
- `RESEARCH_EXTENSION`;
- `OUT_OF_SCOPE`;
- `UNRESOLVED`.

A curriculum binding records exact board/authority, grade, year/version, unit/topic, source evidence, explicit versus inferred status, exclusions, and ambiguity.

Changing curriculum binding must not silently change stable domain truth.

## 8. Source plan versus source ledger

### Source plan

Declares the evidence obligations a package must satisfy before research begins or before promotion. Examples: curriculum authority, domain truth, novice-explanation support, misconception evidence, problem-family evidence, research corroboration.

### Source ledger

Records actual discovered sources and how they satisfy or fail those obligations. Discovery sources can remain candidates without promotion.

Source selection semantics are normative in `SOURCE_GOVERNANCE.md`.

## 9. Assessment binding

The SKP does not own duplicated question bodies. It binds stable assessment IDs from a separate corpus to:

- capabilities;
- concepts/relations;
- problem families;
- representation demands;
- reasoning demands;
- prerequisites;
- verification obligations;
- curriculum and exam contexts.

Bindings may be `MAPPED`, `PARTIAL`, `OUTSIDE_SCOPE`, `UNMAPPED`, or another explicitly governed status. An unmapped question does not justify inventing a capability solely to eliminate the gap.

## 10. Difficulty dimensions

Do not encode a universal `difficulty = 7/10` as canonical truth.

Subject packages may record multidimensional intrinsic demand such as:

- reasoning-chain length;
- representation translation;
- model/theorem selection;
- hidden-condition load;
- algebraic/procedural load;
- spatial/vector reasoning;
- proof demand;
- notation density;
- multi-step state tracking;
- verification demand;
- transfer distance.

These dimensions describe the task/domain demand under a declared policy. They are not learner mastery and should not be treated as psychometric estimates unless backed by an explicit measurement model.

## 11. Learner adaptation

A package may declare treatment options conditioned on governed learner evidence. The allowed adaptation plane includes explanation, example/fading strategy, bridge intensity, practice order, representation sequencing, pacing, hints, and diagnostics.

The following are outside learner adaptation authority:

- domain claim truth;
- theorem/law/relation legality;
- curriculum source facts;
- exact prerequisite identity;
- source custody;
- research evidence requirements.

`ENGINEERING_DEPTH != LEARNER_STATE`.

## 12. Research overlay

A research overlay has an exact base package digest and may add:

- claim ledger;
- literature dossier;
- advanced derivations/proofs/models;
- deeper validity/boundary analysis;
- contested interpretations;
- research-only problem families;
- stronger provenance/corroboration.

If a base claim is challenged, the overlay creates an explicit conflict/supersession record. It cannot rewrite the base package invisibly.

## 13. Provenance

Target provenance should distinguish:

- **Entity** — source, package, fixture, generated receipt, dataset, question corpus item;
- **Activity** — research, extraction, reconciliation, validation, compilation, review, promotion, supersession;
- **Agent** — human, organization, software/compiler, execution agent.

A provenance graph records custody and responsibility. It does not assert that the referenced claim is correct.

## 14. Maturity

Recommended maturity states for SKP artifacts:

- `DISCOVERY` — broad evidence/candidate collection;
- `DRAFT` — structured package incomplete or unresolved;
- `PILOT` — compiles under prototype contracts and is being stress-tested;
- `VALIDATED` — passes promoted semantic/structural checks and required evidence review;
- `ACTIVE` — legal input to declared production consumers;
- `DEPRECATED` — retained for history/migration but not legal for new production;
- `SUPERSEDED` — replaced by an exact successor.

Maturity is not release authorization.

## 15. Subject extension boundary

The shared kernel may require that a package declares a subject adapter, but it must not require Physics-only content.

### Physics extension examples

Physical model, quantity/unit/dimension, reference frame, vector/state semantics, physical law, limiting case, experimental plausibility.

### Mathematics extension examples

Mathematical object, definition, axiom/assumption, theorem, proof obligation, construction, equivalence/implication, counterexample, proof family.

### Chemistry extension examples

Substance/species/entity, phenomenon/observation, particulate/model description, formula/equation/notation, reaction/process condition, conservation/stoichiometric relation, experimental observation.

Subject adapters may extend the kernel. They may not redefine the meaning of shared `capability`, `prerequisite`, `source`, `evidence`, `provenance`, or `maturity` semantics.

## 16. Identity and versioning

Stable identifiers must describe semantic identity, not file location. Same-ID material mutation must be detectable through content digests/version custody.

Identity rules:

- aliases do not create new semantic identity;
- materially different scope or validity can require a new identity/version;
- split/merge operations require migration mappings;
- supersession must preserve predecessor references;
- IDs must not encode learner state or transient release state unless the object itself is learner/release scoped.

## 17. `NOT_APPLICABLE`, `UNKNOWN`, and `UNRESOLVED`

These states are distinct:

- `NOT_APPLICABLE` — the field/obligation is semantically irrelevant under a governed rule;
- `UNKNOWN` — information could be meaningful but is not known;
- `UNRESOLVED` — evidence/conflict/process prevents a current decision.

Agents must not use `NOT_APPLICABLE` as a convenient replacement for missing work.

## 18. Anti-drift test for a new ordinary subtopic

When adding a normal new subtopic, classify every proposed repository change:

- `DATA_ONLY`;
- `SCHEMA_EXTENSION`;
- `GENERIC_ENGINE_CHANGE`;
- `SUBJECT_ADAPTER_CHANGE`;
- `BLUEPRINT_CHANGE`.

`DATA_ONLY` is the expected dominant case after SKP v1 stabilizes.

`BLUEPRINT_CHANGE` is presumptively an architectural failure for ordinary content and requires proof that a genuinely new invariant class has been discovered.

## 19. Pilot questions that must remain answerable

For every pilot SKP, a clean agent should be able to answer from repository authority:

1. What exactly is in and out of scope?
2. Which capabilities are stable identities?
3. Why does each prerequisite edge exist?
4. Which dependencies are external-domain owned?
5. What claims/relations are valid, and under what conditions?
6. Where are the fragile reasoning jumps?
7. Which representations are required, optional, or selected, and why?
8. Which learner conceptions are evidence-backed versus hypotheses?
9. What are the problem families and transfer boundaries?
10. Why was each promoted source selected for its purpose?
11. What remains unknown or conflicted?
12. What can learner evidence adapt without changing domain truth?
13. Which consumer permissions are currently legal?

If those answers require chat history or remembered prior cases, the package/architecture is incomplete.
