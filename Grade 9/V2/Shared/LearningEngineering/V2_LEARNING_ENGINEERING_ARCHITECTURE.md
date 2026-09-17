# V2 Learning Engineering Architecture

Status: **NORMATIVE ARCHITECTURE / NON-RUNTIME-AUTHORIZING**  
Owner: `Grade 9/V2/Shared/LearningEngineering`  
Applies to: Physics, Mathematics, Chemistry, and future V2 subject adapters  

This document defines the common architecture for turning curriculum scope, domain knowledge, source evidence, assessment evidence, pedagogical knowledge, and learner evidence into reproducible instructional products. It does **not** replace current subject generation manifests, the Shared Engineering Gate, CrossDomain authority, HumanReview, or subject release gates. Until the Subtopic Knowledge Package (SKP) contracts and compiler are separately promoted, this package is a design and governance authority only.

## 1. Mission

The system must be able to assimilate an ordinary new subtopic, research depth, curriculum binding, assessment corpus, and learner state without teaching a model or agent a remembered case solution.

The central scalability requirement is:

> **An ordinary new subtopic must not require a Blueprint code change.**

A clean, competent agent should be able to discover the repository, gather evidence, compile governed data, and reach the same structural result without conversation history. If successful execution depends on tacit project memory, topic-name branches, or undocumented expert intuition, the architecture is incomplete.

The intended long-term flow is:

```text
CURRICULUM / ASSESSMENT / SUBJECT SOURCES / RESEARCH
                    ↓
       DISCOVERY + EVIDENCE COLLECTION
                    ↓
       SUBTOPIC KNOWLEDGE PACKAGE (SKP)
                    ↓
         SUBJECT ENGINEERING ADAPTER
                    ↓
       SHARED ENGINEERING GATE POLICY
                    ↓
       CONSUMER-SPECIFIC READINESS
                    ↓
      SUBJECT GENERATION / BLUEPRINT
                    ↓
       LEARNER-SPECIFIC TREATMENT
                    ↓
       ASSESSMENT / TRANSFER / OUTPUT
                    ↓
         INDEPENDENT RELEASE GATES
```

The current repository already implements many of the downstream subject chains. The SKP layer is a planned normalization layer above those subject-specific chains; it must integrate with them rather than create a parallel product pipeline.

## 2. Non-negotiable invariants

1. **Engineering Gate > Blueprint.** Blueprint consumes governed Engineering decisions; Blueprint does not invent or override Engineering authority.
2. **Discovery is permissive; promotion and consumption are strict.** Discovery may retain conflicting, incomplete, or exploratory material. Canonical promotion requires evidence and exact custody.
3. **Repository authority overrides model memory.** Topic names, prior chats, fixtures, earlier agents, and remembered cases are never authority.
4. **Case facts belong in governed data.** A normal topic variation must not introduce a topic-name branch, case-ID branch, question-ID exception, or hand-maintained consumer list in global logic.
5. **Missing authority remains visible.** Use `UNKNOWN`, `UNRESOLVED`, `HELD`, `MISSING`, or a governed `NOT_APPLICABLE`; never fabricate closure to make a task pass.
6. **Learner state does not mutate domain truth.** Learner evidence may change treatment, pacing, bridge intensity, example/fading strategy, or diagnostic focus. It may not change validated equations, theorems, chemical relations, model validity, prerequisite identity, or curriculum facts.
7. **Engineering depth is independent of learner state.** `FOUNDATION`, `STANDARD`, and `RESEARCH` describe evidence/knowledge depth. They are not proxies for learner knowledge.
8. **Research overlays are additive or explicitly superseding.** A research-depth package may add deeper derivations, literature, model limits, or contested interpretations; it may not silently mutate validated base claims.
9. **Source is not authority.** A source can support a claim for a declared purpose. Search rank, familiarity, or inclusion in a question bank does not grant authority.
10. **Provenance is not truth.** Provenance proves custody and derivation history. Correct provenance can still lead to a false claim; semantic validation remains separate.
11. **Publication and human review remain independent.** Technical or pedagogical readiness cannot imply publication, mature-product, or authorized-human approval.
12. **Schema validity is necessary, not sufficient.** Well-formed JSON does not prove disciplinary correctness, pedagogical quality, curriculum alignment, or evidence quality.

## 3. Authority planes

The architecture separates authority into planes so one kind of evidence cannot impersonate another.

| Plane | Owns | Must not own |
|---|---|---|
| Curriculum | board/version/scope bindings, required/derived/enrichment status | disciplinary truth outside curriculum claims |
| Domain / Engineering | concepts, relations, model conditions, technical prerequisites, reasoning closure | learner mastery, publication |
| Research provenance | evidence depth, claim ledger, conflicts, literature custody | learner mastery |
| Pedagogical knowledge | representations, instructional strategies, learning difficulties, worked/faded design | scientific/mathematical/chemical truth |
| Assessment | question identity, source fidelity, capability/problem-family bindings | learner mastery from unanswered items |
| Learner evidence | observed capability state, uncertainty, longitudinal evidence | domain truth or curriculum scope |
| Blueprint / generation | governed transformation and composition | new upstream authority |
| Publication / release | exact artifact custody, legal/release criteria, human gates | retroactive domain authority |

No downstream plane may repair a missing upstream authority by assertion.

## 4. Current repository mapping

The shared model is designed around the repository that exists today, not an idealized greenfield system.

### Physics

`Grade 9/V2/Physics/GENERATION_AUTHORITY_MANIFEST.json` governs the current Physics cold-start path. Physics now contains a mandatory `P-C AssessmentScope → P-C.5 EngineeringReadiness → P-D ProblemSemantics` boundary. The exact P-C scope is submitted through Shared Engineering Gate policy before Problem Semantics consumes it.

### Mathematics

`Grade 9/V2/Mathematics/GENERATION_AUTHORITY_MANIFEST.json` already separates Assessment Intake/Review/Scope, Problem Semantics, Learner Intelligence, Study Synthesis, Core1 Authoring, Representation Semantics, Core2 Transfer, Coverage Closure, and cold-start custody. It also contains a topic-specific PCK promotion boundary and explicit current limitations. The shared SKP model must preserve these Math-specific semantics instead of coercing them into Physics concepts such as physical models or dimensional analysis.

### Chemistry

`Grade 9/V2/Chemistry/CHEMISTRY_GENERATION_AUTHORITY_MANIFEST.json` already separates intake, source integrity, scope, reasoning semantics, learner evidence, study model, Core1, representation, transfer, coverage, and cold-start custody. Chemistry has source-obligation and representation demands that differ materially from both Physics and Mathematics. The shared SKP model must allow Chemistry to express observed phenomena, particulate/model reasoning, symbolic/notation semantics, conditions, conservation, and experimental/source obligations without forcing a Physics ontology.

### Shared authority already present

- `Shared/EngineeringGate` — aggregate readiness and consumer-specific authorization.
- `Shared/CrossDomain` — provider-owned cross-domain authority.
- `Shared/HumanReview` — independent authorized-human review boundary.
- `Shared/LearnerIntelligence` — shared learner/control semantics where applicable.
- `Shared/MasterTemplates` — shared rendering/representation assets.

`Shared/LearningEngineering` must coordinate these layers, not duplicate them.

## 5. The Subtopic Knowledge Package

The planned durable unit is a **Subtopic Knowledge Package (SKP)**. It is not a lesson plan and not a list of links. It is a versioned, evidence-backed instructional knowledge graph that stores the knowledge an agent would otherwise have to invent.

An SKP should eventually represent:

- identity, aliases, scope, exclusions, and curriculum bindings;
- capabilities at governed granularity;
- internal and external prerequisite edges, with transition rationale and missing-behavior policy;
- concepts, laws/theorems/relations, symbols, units or formal objects as subject-appropriate;
- validity/applicability conditions and boundary cases;
- reasoning sequences and high-fragility inferential transitions;
- representation requirements, alternatives, decisions, and translation obligations;
- learner conceptions, errors, resources, and evidence strength;
- worked/example/non-example/counterexample needs;
- problem families, recognition signals, first moves, variants, and transfer limits;
- verification routes;
- source plan, source ledger, conflicts, freshness, and reuse/licensing state;
- assessment bindings to a separate question/assessment corpus;
- learner-adaptation permissions;
- research-depth overlays;
- unresolved issues, maturity, exact provenance, and version history.

The detailed ontology is normative in `SUBTOPIC_KNOWLEDGE_MODEL.md`. Planned schema modules and promotion order are in `SKP_SCHEMA_ROADMAP.md` and `registry/skp-schema-roadmap.v1.json`.

## 6. Knowledge graph, not flat catalogue

The library must not degrade into:

```text
subtopic title → links → notes
```

The important information is relational:

```text
capability A
  ├─ requires capability B because ...
  ├─ uses relation R under conditions C
  ├─ is expressed by representations X/Y
  ├─ contains fragile jump J
  ├─ appears in problem families F1/F2
  ├─ has learner conception evidence L
  ├─ is supported by sources S1/S2 for declared purposes
  └─ is assessed by question bindings Q...
```

Short, auditable rationale should be stored for governed decisions. Do **not** store hidden chain-of-thought. A good rationale names the semantic dependency and evidence; it does not narrate private internal reasoning.

## 7. Learning progressions and learner models

The architecture distinguishes a disciplinary dependency graph from a learner-development hypothesis.

A prerequisite relation can be technically valid without proving that all learners must traverse it in one fixed sequence. Likewise, a pedagogically plausible progression is not automatically empirical learner evidence.

Progression evidence must distinguish at least:

- `STRUCTURAL_PREREQUISITE` — logically/domain required;
- `PEDAGOGICAL_BRIDGE` — useful instructional transition, not a domain law;
- `HYPOTHESIZED_PROGRESSION` — theory/expert/evidence-informed sequence not yet empirically validated in the target population;
- `EMPIRICALLY_SUPPORTED_PROGRESSION` — supported by learner evidence with declared population/context limitations.

This distinction is motivated by learning-progression research emphasizing developmental coherence and the need for validation/intervention evidence rather than assuming a proposed sequence is established fact. See Jin et al. (2019), DOI `10.1002/sce.21525`.

## 8. Learner adaptation boundary

The same technical package must be stress-tested against different learner states. The domain kernel remains invariant; treatment may adapt.

Must remain invariant unless scope/evidence itself changes:

- canonical domain claims;
- relation/theorem/law identity;
- validity conditions;
- exact source provenance for those claims;
- technical prerequisite graph;
- curriculum classification;
- Engineering closure.

May adapt under governed learner evidence:

- explanation depth and language;
- bridge intensity;
- worked-example count;
- fading schedule;
- self-explanation prompts;
- retrieval/application order;
- representation sequencing;
- hint availability;
- pacing and diagnostic checks.

`ENGINEERING_DEPTH != LEARNER_STATE` is a permanent invariant.

## 9. Research depth

Research depth controls the evidence envelope, not student ability.

### FOUNDATION

Minimum governed subject truth, curriculum binding, core prerequisites, high-risk validity conditions, essential representations, and assessment/problem-family coverage.

### STANDARD

Adds fuller reasoning closure, broader source corroboration, characteristic problem families, pedagogical evidence where available, representation alternatives, and explicit unresolved/conflict handling.

### RESEARCH

Adds a formal claim ledger, literature dossier, contested interpretations, advanced derivations/model limits, stronger provenance/corroboration requirements, and explicit base-claim supersession rules.

A RESEARCH overlay may add depth. If it changes a canonical base claim, the change requires an explicit conflict/supersession receipt and cannot occur silently.

## 10. Source and provenance model

Source governance is defined in `SOURCE_GOVERNANCE.md`.

The target provenance model is compatible with the W3C PROV distinction among **entities, activities, and agents**: a source or artifact is an entity; compilation/review/promotion is an activity; a human, organization, agent, or software component can be an agent with a declared role. This is a useful structural model for reproducibility, but PROV-style custody does not determine whether a claim is true.

Every promoted substantive claim should be able to answer:

- What entity supports it?
- For what source intent was that entity selected?
- What activity extracted/reconciled/promoted it?
- Which agent or governed compiler performed that activity?
- What exact version/digest was used?
- What limitations/conflicts remain?

## 11. Shared kernel and subject adapters

The common kernel should encode relations that are meaningful across subjects: identity, scope, capability, prerequisite, evidence, reasoning, representation, problem family, assessment binding, provenance, learner adaptation, research overlay, and maturity.

It must **not** require every subject to pretend the same disciplinary ontology applies.

### Physics adapter

Expected extension concepts include:

- physical systems/models;
- quantities, units, dimensions;
- reference frames and sign conventions;
- laws/equations and relation-selection conditions;
- state variables and phase continuity;
- vector/graph/diagram representations;
- boundary/limiting cases and experimental/physical plausibility checks.

### Mathematics adapter

Expected extension concepts include:

- mathematical objects and definitions;
- axioms/assumptions and theorem dependencies;
- proof obligations and proof families;
- procedures/transformations with domain restrictions;
- constructions, diagrams, graphs, tables, symbolic forms;
- counterexamples and equivalence/implication distinctions;
- conceptual versus procedural learning difficulties.

Mathematics PCK research strongly supports treating instructional strategies/representations and topic-specific learning difficulties as first-class pedagogical knowledge rather than generic lesson metadata. See Grigaliūnienė et al. (2025), DOI `10.1007/s11858-025-01684-1`.

### Chemistry adapter

Expected extension concepts include:

- substances/species/entities and state/condition semantics;
- observed/macroscopic phenomena;
- particulate/submicroscopic models;
- formulas, equations, notation, graphs and other symbolic representations;
- reaction/process conditions;
- conservation and stoichiometric constraints;
- experimental observations and source obligations;
- explicit transitions among phenomenon, model, and symbolic representations.

Chemistry education literature commonly discusses macroscopic, submicroscopic and symbolic aspects, but the architecture must not freeze one simplistic triangle as ontology. Taber (2013), DOI `10.1039/C3RP00012E`, explicitly notes that the triplet has multiple reconceptualizations and no single canonical form. The Chemistry adapter should therefore encode representation purpose and translation obligations, not merely a three-value label.

## 12. Assessment corpus separation

Questions should not be copied wholesale into every SKP. The long-term architecture should maintain a separate Assessment Corpus Library with stable question IDs and metadata such as:

- source and exact custody;
- curriculum/grade binding;
- capability refs;
- problem-family ref;
- representation and reasoning demands;
- prerequisite refs;
- solution/answer provenance;
- difficulty dimensions where governed;
- reuse/licensing state.

An SKP stores bindings to assessment IDs and coverage expectations. This avoids duplication and allows one question to inform several packages without becoming multiple inconsistent copies.

## 13. Consumer-specific readiness

A single universal `READY=true` is insufficient. Readiness is dimensional and consumer-specific.

The Shared Engineering Gate already establishes the intended pattern. Future SKP compilation should expose dimensions such as:

- domain technical closure;
- internal prerequisite closure;
- external-domain prerequisite closure;
- curriculum binding;
- source authority/provenance;
- research-provenance requirements;
- pedagogical evidence maturity;
- assessment coverage;
- representation closure.

Consumers declare what they require. A missing Math provider receipt, for example, may block a technical consumer while discovery/research remains valid. Publication remains separately governed.

## 14. Agent reproducibility and anti-drift

A clean agent should not have to invent:

- capability identities or granularity rules;
- scope boundaries;
- prerequisite edges;
- source hierarchy or selection reasons;
- relation meanings or validity conditions;
- high-fragility reasoning jumps;
- representation obligations;
- problem-family structure;
- misconception/error classification policy;
- promotion criteria.

Independent clean-agent runs should be compared structurally, not by prose similarity. Disagreement should be classified (scope, granularity, prerequisite, source, domain truth, pedagogical choice, evidence gap, schema ambiguity) and treated as a diagnostic for missing repository knowledge.

## 15. Metamorphic scalability tests

Before calling the architecture general, it should pass transformations such as:

| Perturbation | Invariant expected |
|---|---|
| learner state `UNKNOWN → LOW → MODERATE` | domain kernel, curriculum truth and Engineering closure unchanged |
| `STANDARD → RESEARCH` | validated base claims unchanged unless explicit supersession |
| curriculum overlay changes | domain truth unchanged; curriculum bindings may change |
| local source removed | explicit source hold/unresolved state; no fabricated replacement |
| external provider receipt absent | explicit consumer hold |
| web ranking/order changes | canonical authority cannot change solely due to rank |
| question corpus expands | existing domain truth unchanged |
| representation alternative added | decision is re-evaluated; prior decision not silently overwritten |
| independent agent changes | structural disagreements exposed rather than averaged away |

## 16. Schema evolution

Planned SKP schemas will be modular and versioned. Do not create one monolithic schema with hundreds of always-required subject-specific fields.

Rules:

1. A schema version is immutable once promoted `ACTIVE`.
2. Breaking semantic changes require a new version plus migration rules.
3. `NOT_APPLICABLE` is governed and meaningful; it is not a filler escape hatch.
4. Unknown evidence stays unknown rather than being coerced to a default.
5. Subject extensions must not redefine shared field meaning.
6. New invariant classes may extend shared contracts; ordinary content cases may not.
7. Every active schema must have a producer, consumer(s), positive fixture, negative/falsifier coverage, and migration/deprecation policy.
8. Human-readable docs explain contracts; machine schemas remain the executable source of structural truth.

The machine-readable roadmap is `registry/skp-schema-roadmap.v1.json`. Planned modules have no runtime authority until their status is explicitly promoted under tests.

## 17. Known limitations and risks

The architecture deliberately records limitations rather than masking them.

### Current limitations

- There is not yet an active SKP schema or SKP compiler.
- Capability granularity is not yet empirically calibrated across subjects.
- The Physics Engineering Gate is more mature than equivalent Math/Chem Engineering adapters.
- Current learner-state evidence is sparse and uneven across topics.
- Topic-specific PCK/misconception literature is uneven; some subtopics will legitimately remain `UNRESOLVED`.
- Existing subject chains use different terminology and maturity levels; convergence requires adapters, not search-and-replace normalization.
- Source licensing/reuse metadata is not consistently represented across existing corpora.
- There is no universal, validated difficulty scalar suitable for all topics, subjects, learners, and exams.
- Structural reproducibility across independent agents has not yet been measured systematically.

### Architectural risks

- **Ontology explosion:** micro-capabilities can become too fine-grained to maintain.
- **False precision:** schemas can encourage unsupported certainty or meaningless filler.
- **Physics leakage:** shared fields may accidentally encode mechanics assumptions.
- **Source-rank bias:** agents may promote easy-to-find material over appropriate authority.
- **Provenance fallacy:** exact custody may be mistaken for correctness.
- **Misconception overclaim:** context-sensitive learner reasoning may be mislabeled as a stable misconception.
- **Progression overclaim:** a plausible teaching order may be presented as an empirically validated learner progression.
- **Schema gaming:** agents may satisfy counts without meaningful semantic closure.
- **Research-cost explosion:** RESEARCH depth can become unbounded without explicit evidence policies.
- **Cross-subject mismatch:** Mathematics and Chemistry may require extension semantics that reveal flaws in the shared kernel.
- **Human-quality gap:** machine validation cannot establish subject correctness, pedagogy quality, assessment validity, visual usability, or learning efficacy by itself.

## 18. Roadmap and exit criteria

### Phase A — architecture freeze candidate

Deliver:

- this core architecture;
- normative SKP ontology;
- source governance;
- modular schema roadmap and status registry.

Exit: terms, authority planes, shared/adaptor boundary, and non-authorizing status are unambiguous.

### Phase B — schema prototypes

Implement the smallest modular SKP contracts required by the pilots. Do not populate the library at scale.

Exit: valid/invalid fixtures and cross-reference validation exist; no subject-specific field is incorrectly mandatory in the shared kernel.

### Phase C — four diversity pilots

Recommended stress cases:

1. Physics Grade 9 Relative Motion — curriculum ambiguity, reference frames, Math dependency.
2. Physics Thermodynamics at `RESEARCH` depth — source/research depth, model conditions, larger dependency graph.
3. Mathematics geometry/trigonometry — proof/definition/construction ontology and topic-specific PCK.
4. Chemistry atomic/bonding/reaction case — phenomenon/model/symbol translation and condition semantics.

Exit: ordinary pilot differences are data/adapter changes, not global Blueprint branches.

### Phase D — independent-agent reproducibility

Run multiple clean agents against the same governed task and compare structural outputs.

Exit: disagreements are explainable by evidence gaps or declared pedagogical choice; undocumented repository dependence is reduced to an agreed threshold.

### Phase E — promote SKP v1

Only after diverse pilots, promote stable modules to `ACTIVE`, define migration rules, and connect SKP compilation to subject Engineering adapters.

### Phase F — library population

Parallelize research, source-ledger creation, question-corpus mapping, problem-family mining, and legacy migration under active contracts.

### Phase G — empirical feedback

Use real learner/assessment evidence to test and revise learner models and progression hypotheses without mutating domain truth.

## 19. Definition of architectural success

The architecture is not successful because one flagship topic produces a polished guide. It is successful when:

- a normal new subtopic is primarily a governed data/evidence addition;
- different research depths do not require case logic;
- learner evidence adapts treatment without changing domain truth;
- cross-domain dependencies are provider-owned and fail closed;
- Math and Chemistry fit through subject adapters without pretending to be Physics;
- a clean average agent can reconstruct the task from repository authority;
- independent agents converge structurally or expose explicit evidence/schema ambiguity;
- unresolved evidence remains visible;
- release authority remains independent;
- the same generic compilers/falsifiers survive diverse new cases.

The desired operating principle is:

> **Humans define ontology and authority. Agents discover, propose, normalize and test. Compilers promote. Blueprint consumes.**

## 20. Research basis used for this architecture

These sources inform architectural choices; they do not become subject-content authority merely by appearing here.

- W3C, *PROV Model Primer* (2013): https://www.w3.org/TR/prov-primer/
- Jin, H. et al., *Toward coherence in curriculum, instruction, and assessment: A review of learning progression literature* (2019), DOI: https://doi.org/10.1002/sce.21525
- Grigaliūnienė, M. et al., *Systematic Review of Research on Pedagogical Content Knowledge in Mathematics: Insights from a Topic-Specific Approach* (2025), DOI: https://doi.org/10.1007/s11858-025-01684-1
- Taber, K. S., *Revisiting the chemistry triplet* (2013), DOI: https://doi.org/10.1039/C3RP00012E
