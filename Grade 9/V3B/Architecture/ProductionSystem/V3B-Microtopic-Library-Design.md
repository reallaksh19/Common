# Microtopic teaching library — V3B design proposal

The library should preserve expert scientific and teaching decisions that can be reused and improved. It is a graph of teachable capabilities, sources, models, representations, questions and evidence. A list of headings, a collection of links, or a pile of completed books would not give a fresh agent enough guidance.

The [core guide](V3B-Core-System-Guide.md) gives the wider architecture. [V3B-Microtopic-Library.schema.json](V3B-Microtopic-Library.schema.json) is a proposed exchange schema. [The relative-motion seed](V3B-Relative-Motion-Library-Seed.json) is a worked CANDIDATE example, not a curated curriculum library or a publisher input. No runtime resolver/acceptance service is shipped in this documentation task.

## 1. Granularity: what deserves a record?

Use four linked levels: subject/domain → topic → subtopic/bucket → microtopic/capability. A capability has an observable action and criterion; a microtopic contains the teaching needed to develop it. These are related but not identical: one task may reveal several capabilities, and one capability may need several teaching episodes.

For example, “relative motion” is a subtopic. “Given two same-frame velocity vectors, construct A relative to B and explain the subtraction order” is a capability. Its teaching includes frame naming, same-time position subtraction, interval reasoning, graphical reversal, signed components and a limiting-case check. Store the actual reasoning, not just those six titles.

Split when an unresolved inference can fail independently and needs its own explanation/repair. Merge when two records are only wording variants or cannot be meaningfully assessed separately. Keep a stable ID when improving wording; create successor IDs or versions with `split_from`, `merged_from` or `supersedes` relationships when meaning changes. No fixed atom count or one-sentence atom rule.

## 2. Record families

| Record | Minimum useful content | Added for reviewed reuse |
|---|---|---|
| Package/envelope | ID, schema/version, subject, status, owner scope, provenance, known issues | Exact dependencies, accepted evidence and compatibility constraints |
| Microtopic | Outcome, entry assumptions, difficult inference, actual explanation path, misconception/repair, exit task | Scientific checks, multiple teaching routes, question/representation links, reviewer evidence |
| Capability | Observable action and success criterion, scope and prerequisite links | Calibrated observations where available; never inferred from title or page count |
| Relation/model | Expression, symbol meanings, assumptions, derivation/explanation, limits, source links | Subject checks, alternate derivation, valid transformed forms |
| Representation | Required elements, variables/relations supported, reading order and known misleading alternatives | Exact instance bindings, accessibility and final-size review evidence |
| Resource | Local/web locator, version/edition/section, access status, rights status, role and relevance | Preserved permitted snapshot/digest, checked claims and fallback sources |
| Question family | Required capabilities, reasoning structure, demand/support dimensions, common wrong routes | Valid parameter constraints, transfer boundaries and semantic exposure classification |
| Question instance | Immutable origin/number, full stem/subparts/options/figures, answer or rubric, provenance | Verified solution/checks, exposure history and supported curriculum/practice mapping |
| Teaching route | Entry needs, ordered microtopics, explanatory/interactive actions and help/reveal plan | A/B realization evidence and situations where the route fails |
| Evidence/issue | Exact target/version, method, observation, result and limitation | Independent reviewer identity/method where claimed; no self-approved acceptance |

Required substance can be inline or referenced by an immutable accessible asset; copying the same full equation/example into every record is unnecessary. A dangling reference is not useful library content.

## 3. Sources by purpose and entry capability

Store source preferences as **claim- and purpose-specific recommendations**, not global site rankings or percentage bands. Separate scientific authority, explanation suitability, question provenance, activity inspiration and curriculum alignment. A university text may be a strong scientific check but a poor first explanation for a Grade 9 learner. A simulation may support exploration but not certify an equation or exam alignment.

| Need | Preferred starting route | What to verify |
|---|---|---|
| Missing language/representation prerequisite | Supplied basic text, official grade material, a carefully chosen concrete visual/activity | Reading burden, exact bridge, whether the picture teaches the relation |
| Intrinsically difficult study concept | Authoritative source plus contrasting explanation/representation | Hard inference, model conditions, conflicts and reason for selection |
| Board practice | Supplied frozen bank, official current curriculum and traceable board resources | Edition/year/track, original item IDs, answers and all figure/subpart data |
| Competitive preparation | Authorized local bank or traceable exam/problem source, supplemented by reviewed authored tasks when allowed | Actual exam metadata, scope, transfer family, prerequisites, solution correctness |
| Research overlay | Primary papers, specialist references and explicit model/assumption comparisons | Open question, applicable regime, disagreement, evidence quality and unresolved limitations |

Available concrete starting sources for the motion seed are current CBSE Standard/Advanced documents, NCERT straight-line/plane-motion chapters and PhET Vector Addition. None is an automatic all-purpose authority. The historical CBSE competency bank is a question candidate source; local-bank paths remain empty until actual owner-supplied files exist.

For each resource record `supports_claims`, `role`, `entry_capabilities`, `depth`, `selection_reason`, `locator`, `edition`, `last_checked`, `access_status`, `rights_status` and `fallback`. If the content was not inspected, mark DISCOVERED rather than VERIFIED. A public URL does not establish permission to reproduce an entire copyrighted question bank. Keep a reference or permitted excerpt where full reproduction is not allowed.

For Core1A/1B, these recommendations help the intrinsic teaching design; they must not turn a learner percentage into a reduced study-depth contract. For Core2A/2B, source/item selection may follow scoped capabilities or the owner's waived route. Labels such as “foundation explanation” describe a resource affordance, not a measurement of a child.

## 4. Proposed schema and semantic constraints

The supplied [Draft 2020-12 JSON Schema](https://json-schema.org/draft/2020-12) specifies transport structure: types, enum values, required substantive fields and question answers. It deliberately allows CANDIDATE records to contain pending evidence and issues. Each content record has an `extensions` object for namespaced subject additions. Unknown ordinary fields are rejected to catch drift; a missing optional extension is not a reason to prevent exploration. Lightweight discovery notes precede this package schema; agents need not fill a complete package before researching.

The schema does not prove that IDs resolve, the prerequisite graph is coherent, answers are correct, sources support claims or a reviewer is independent. These require a future semantic validator/acceptance service. Marking `status: CURATED` is a requested state only, not a self-issued authorization. A consumer must require current external acceptance evidence before treating that state as accepted.

Proposed semantic checks:

1. Unique identities; resolvable local/external references; acyclic prerequisite edges. Related/example-of links may form cycles and must not be confused with prerequisites.
2. Every accepted microtopic has an actual teaching path, misconception repair and answerable exit criterion. Required model conditions cannot disappear when simplifying language.
3. Every question has origin, original identifier or truthful authored ID, full source representation and answer/rubric; every referenced figure is available or explicitly held.
4. Each relation/representation/check binds to its scientific model and version; a pretty diagram from another model is not compatible reuse.
5. Curriculum scope is per year/track/capability. A subject-level or grade-level link alone cannot authorize an advanced task.
6. Required research contributions are present for accepted Medium/Hard study records. Search activity and discovery notes remain possible before acceptance.
7. Evidence binds to the content digest/version it evaluated. Candidate self-assertions cannot become independent acceptance; data with missing review stays candidate.
8. Practice routing distinguishes observations, estimates, synthetic profiles and owner waivers. Study depth never reads the learner-percentage field.

The example and documentation are structurally checked in this task. Building the semantic validator is roadmap work, not an unexecuted PASS claim.

## 5. Creation and reuse lifecycle

Authoring ergonomics matter. The target interface should ask the agent for six substantive pieces: the capability, prerequisites, difficult reasoning, sources/representations, an exit task with answer, and unresolved issues. A tool can assign IDs, versions and repetitive envelope fields, then flag specific missing substance. It must not invent a missing explanation to make the schema pass. The full exchange schema is a storage/validation contract, not something every agent should read or hand-fill on every turn. This intake-to-schema adapter is proposed work, not implemented here.

`DISCOVERED → CANDIDATE → REVIEWED → CURATED`, with `DISPUTED`, `STALE` and `RETIRED` as explicit states. REVIEWED can include unresolved findings; CURATED requires the applicable acceptance decision. Research notes are cheaper and less structured than accepted records. Promote a coherent group of findings once useful; do not require full forms for each search result.

A reuse query should state the target capability, curriculum/depth scope, intended Core action, known prerequisites, available sources and required medium. The resolver then filters scope/model compatibility, resolves prerequisite closure, ranks useful sources/routes, reports missing dependencies, and emits a small work packet. Ranking must preserve its reasons and alternatives. Retrieval similarity alone cannot decide scientific equivalence or question-transfer novelty.

Treat retrieved web or question-bank content as evidence, not as agent instructions. Source text cannot change the owner's scope, acceptance rules or working permissions. Preserve conflicting scientific claims for comparison instead of letting a retrieved page silently replace the accepted model.

Reuse one canonical equation/model across curricula; use mapping records for different curriculum versions. Reuse a diagram specification across compatible cases; generate and check each numeric instance. Reuse an example as a declared reconstruction anchor; preserve its exposure history. Avoid caching a personalized practice route as though it were universally suitable.

## 6. Change and extension examples

**Add a new independent subtopic:** create its candidate microtopics, source/model links and prerequisite edges; resolve those edges; publish only the new accepted slice. Unrelated accepted artifacts remain valid.

**Deepen an existing gravity bucket to research level:** retain the school model, add a named depth/model overlay with a concrete research question, new prerequisites, model validity and review needs. Mark which claims generalize and which change. The higher-depth route does not silently replace school-exam scope or alter every learner's material.

**Correct a shared equation condition:** preserve the old version and correction. Traverse reverse dependency links through microtopics, examples, figures, questions and outputs; mark only affected acceptance stale. Rebuild/review those objects. Merely adding a bibliography link need not invalidate every answer.

**Split a large microtopic:** retain lineage and remap capability/evidence links. Do not move evidence blindly: confirm that old observations still support the new narrower capability. Learner history is not rewritten.

## 7. Library rollout and maintenance

Start with a small Physics seed from different kinds of reasoning: vector/frame reasoning, a graph/kinematics relation, a conservation/model-boundary case and a thermal concept. These are representative selection criteria, not a new fixed syllabus. Curate one real production path before expanding volume. Import useful existing PR350 registry content through a mapping/review, not a title-level bulk copy.

Maintain a source refresh queue, failed retrievals, licence/access changes, high-repair microtopics, duplicate candidates and disputed claims. Refresh riskier content more often: changing curricula and web banks need closer attention than stable basic equations. Do not invent a universal expiration period; record the policy and actual recheck date.

A later index can combine exact IDs, keywords and semantic retrieval. Keep the canonical records readable and exportable; implement CASE/QTI/PROV mappings only when interoperability is needed. Those standards do not supply the teaching substance, and adopting their ideas does not claim certification.

Keep student observations outside the shared content library. Store only necessary scoped evidence, avoid personal details in public Git artifacts and use synthetic profiles for public stress tests. Aggregate calibration is a separate, versioned product.

## 8. Proving that ordinary agents benefit

Compare two conditions on held-out subtopics: the current prompt/contracts alone, and the same tools/budget plus the curated library. Run several fresh instances rather than reporting the best result. Keep a reviewer-only set of source omissions, equation conditions, difficult transitions and transfer tasks. Reveal it only for evaluation.

Report the rate and severity of unsupported claims, omissions, wrong diagrams, accidental repeats, incomplete answers and unnecessary holds; time/cost to acceptable output; reviewer repairs; successful packet recovery; and later learner transfer if actually measured. An empty output is not a quality success. Include legitimate equation reuse and deeper research as positive controls against over-tightening.

Do not set a universal agent-competence or semantic-similarity percentage now. Establish a labelled pilot corpus, report disagreements and uncertainty, then choose operational thresholds by consequence. The library remains a maintained educational asset, not a one-time prompt trick.
