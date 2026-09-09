# Historical concept note — extracted text

Original attachment; superseded as the implementation proposal by the executable skills in this PR. Paragraph text is extracted for review; the DOCX preserves original formatting. This is not a new concept note.

GRADE 9 SKILL ARCHITECTURE

Concept Note for Approval

Repository: reallaksh19/Common · Grade 9

Status: Draft for architecture approval

Date: 8 September 2026

Core proposalEvolve the Grade 9 repository from a flat list of peer skills into a governed production architecture: authorities own reusable rules, services create learning objects, workflows compose authorities, auditors verify, publishers render/reconstruct, and program tracks remain specialized. Introduce one canonical skill registry as the control plane and generate documentation, install profiles and distributions from it.

Approval requested on architecture, migration sequence and ownership rules—not on immediate folder relocation.

Approval Snapshot

Decision area

Recommendation

Approval sought

Architecture

Adopt layered production model with one canonical owner per reusable concern.

Approve

Repository metadata

Create skill-registry.yaml as the architecture control plane.

Approve

Physical folders

Keep current flat installable folders during Phase 1; do not move yet.

Approve

Auditors

Make corpus auditor canonical; convert overlapping transfer coverage into compatibility/profile semantics.

Approve

Math

Keep grade9-math as authority; treat math-assimilation as a product workflow.

Approve

Publishing

Keep source-PDF reconstruction and master-data publishing as separate engines.

Approve

Distribution

Generate SKILLSET, installer profiles and ChatGPT distribution from registry.

Approve

Compatibility

Use ACTIVE → COMPATIBILITY → DEPRECATED → REMOVED lifecycle; avoid abrupt deletion.

Approve

1. Purpose of this concept note

This note proposes a controlled refactor of the Grade 9 skill family so that another agent can discover, route, compose, validate and install the right capabilities without relying on chat history or tribal knowledge. The objective is not to rewrite successful skills. It is to make ownership, composition, compatibility, installation and quality assurance explicit and machine-governed.

2. Why a refactor is now needed

The repository has matured from a small set of reusable Grade 9 skills into a production system containing generic capabilities, subject authorities, builders, auditors, publication engines and competition-specific programs. These are still presented largely as peers in a single skills namespace. That creates routing ambiguity and encourages duplication of contracts such as source status, stable IDs, hints, difficulty labels, corpus ownership and render QA.

Observed registry driftThe live Grade 9/skills tree contains 20 skill folders. SKILLSET.md documents a smaller set, install_skills.py installs only 10, and the separately maintained ChatGPT package documents 9. This means the filesystem, documentation, installer and distribution package are already different inventories.

2.1 Current inventory

Current skill

Current functional role

grade9

Router / orchestrator

grade9-source-grounding

Source extraction, provenance and QC

grade9-concept-architect

Stable concept IDs and dependency graph

grade9-math

Mathematics authority

grade9-physics

Physics authority

grade9-chemistry

Chemistry authority

grade9-question-bank

Question authoring / calibration

grade9-learning-enrichment

Hints, misconceptions, diagnostics, transfer

grade9-math-assimilation

Mathematics assimilation workflow

grade9-physics-subtopic-book-builder

Physics subtopic product workflow

grade9-redox-subtopic-book-builder

Redox subtopic product workflow

grade9-corpus-coverage-auditor

General corpus coverage audit

grade9-transfer-coverage-auditor

External/PYQ transfer coverage audit

grade9-math-corpus-coverage-auditor

Mathematics coverage extension

grade9-subtopic-completeness-auditor

Pedagogical subtopic release audit

grade9-redox-chapter-closeout-auditor

Redox chapter-wide closeout workflow

grade9-publication

Source-PDF reconstruction

grade9-textbook-publisher

Master-data publishing

ioqm-grade9-main-topic-builder

IOQM integrated topic workflow

ioqm-grade9-model-exam-builder

IOQM model-exam workflow

3. Architectural objective

The proposed architecture separates reusable semantic authority from operational composition. A skill should not own a rule merely because it needs that rule. Instead, it should reference the canonical owner.

Governing rule: one reusable rule → one canonical ownerAuthorities own reusable semantics. Services create reusable learning objects. Workflows compose authorities and services. Profiles specialize behavior. Auditors verify; they do not silently author. Publishers reconstruct or render; they do not redefine subject content.

4. Proposed production layers

Layer

Name

Canonical contents

Role

00

Orchestration

grade9

Interpret request, select pipeline, invoke specialists, enforce completion gates

10

Source & Knowledge Architecture

source-grounding, concept-architect

Establish source truth, provenance, stable IDs, dependencies

20

Subject Authorities

math, physics, chemistry

Own subject correctness, models, representations, misconceptions, subject difficulty

30

Learning Object Authoring

question-bank, learning-enrichment

Create/calibrate questions, hints, diagnostics, worked support, transfer

40

Product Workflows

math-assimilation, physics builder, redox builder

Compose authorities/services into finished learning products

50

Assurance & Audit

corpus auditor, subtopic completeness

Prove coverage and learning completeness; specialized profiles extend checks

60

Publication

publication, textbook-publisher

Reconstruct source PDFs or render validated master data

70

Programs / Tracks

IOQM workflows

Highly opinionated program-specific production

90

Compatibility

transfer-coverage wrapper and future aliases

Preserve old invocations while canonical ownership migrates

5. Proposed skill object types

Type

Definition

Examples

Allowed behavior

ROUTER

Selects the correct pipeline.

grade9

Routes and gates; should not become a giant duplicate spec.

AUTHORITY

Owns reusable domain truth or semantics.

source-grounding, math, physics, chemistry

Defines canonical rules for its concern.

SERVICE

Performs a reusable operation.

question-bank, learning-enrichment

Consumes authorities and emits reusable objects.

WORKFLOW

Coordinates several skills to produce a product.

math-assimilation, physics builder, Redox builder

Sequences steps; should reference, not duplicate, canonical rules.

AUDITOR

Verifies independent completion criteria.

corpus auditor, completeness auditor

Measures and blocks; does not repair by redefining source/scope.

PROFILE

Specializes another skill without owning the whole workflow.

external-transfer, math-corpus rules

Overrides/adds schema/checks only.

PUBLISHER

Creates a publication artifact.

publication, textbook-publisher

Reconstructs or renders; must preserve authority boundaries.

PROGRAM

Opinionated multi-stage track.

IOQM main-topic/model-exam

May compose many skills under a track-specific contract.

COMPATIBILITY

Temporary invocation shim.

transfer-coverage legacy wrapper

Delegates to canonical replacement; no new independent rules.

6. Canonical authority matrix

Reusable concern

Canonical owner

Boundary

Source transcription/status/provenance

grade9-source-grounding

All others consume its source records.

Stable concept IDs / prerequisites / learning graph

grade9-concept-architect

Rendered page numbers are never canonical identity.

Mathematical correctness and Math reasoning

grade9-math

Assimilation workflow consumes this authority.

Physics correctness/model validity/representation semantics

grade9-physics

Builders/publication may not redefine model validity.

Chemistry correctness/representation semantics

grade9-chemistry

Chemistry typography profile can extend publication QA.

Question generation / same-level calibration / challenge creation

grade9-question-bank

Subject authorities supply difficulty semantics.

Generic hints/misconceptions/diagnostics/transfer objects

grade9-learning-enrichment

Subject workflows specialize language and representations.

Corpus accounting / ownership / coverage denominator

grade9-corpus-coverage-auditor

Transfer and math variants become profiles/extensions.

Pedagogical subtopic completeness

grade9-subtopic-completeness-auditor

Delegates source/corpus/render checks to their owners.

Source-PDF reconstruction

grade9-publication

Authority model = source_document.

Validated-master publication

grade9-textbook-publisher

Authority model = canonical_master.

7. Key refactor decisions by skill family

7.1 Mathematics: authority vs assimilation workflow

grade9-math should remain the authority for mathematical mechanisms, invariants, representation choice, decision boundaries, difficulty fingerprinting and correctness. grade9-math-assimilation should become explicitly a product workflow: it turns validated mathematical authority into a partial-knowledge Assimilation Book, First-Step Reference, transfer/mastery layer, diagnostic key and rendered QA package.

Boundarygrade9-math = WHAT must be mathematically true and cognitively recognized. grade9-math-assimilation = HOW to produce a partial-knowledge learning product from that authority.

7.2 Auditor family

grade9-corpus-coverage-auditor should become the canonical subject-agnostic accounting engine. It already owns source snapshots, classification, one-primary-owner rules, placement, support, solution traceability and publication QA. grade9-transfer-coverage-auditor should migrate to a thin compatibility wrapper/profile for EXTERNAL_TRANSFER. grade9-math-corpus-coverage-auditor should remain a mathematics extension/profile. grade9-redox-chapter-closeout-auditor should remain a workflow because it performs a chapter-wide freeze → reverse comparison → backfill → re-audit sequence, rather than merely changing a few checks.

7.3 Subtopic builders

Physics and Redox builders are product workflows, not subject authorities. A future generic subtopic-package-builder may extract the common lifecycle shell, but it must not flatten subject pedagogy. The generic layer should own workflow order; Physics/Redox profiles should continue to own their distinctive representations, misconceptions and subject-specific teaching grammar.

7.4 Publication engines

Decision question

grade9-publication

grade9-textbook-publisher

What is the source of truth?

Existing PDF/book/source document

Validated canonical master data

Primary operation

Reconstruct + reconcile

Render + link + preflight

May repaginate?

Yes, with zero-loss source obligation reconciliation

Yes, generated from master data

Core risk

Silent loss/rewrite of source

Render/link drift from canonical master

Proposed display name

Source-PDF Reconstructor

Master-Data Publisher

7.5 Program tracks

IOQM should be classified as a program layer because it has its own architecture freeze, topic ownership, source contracts, integrated Assimilation/First-Step/mastery outputs and timed-exam conventions. It consumes Math and other reusable services; it should not be conceptually peer to the Math authority.

8. Shared difficulty and hint contracts

The repository currently contains several legitimate difficulty and hint systems. The refactor should centralize the data model and naming, not force a single psychometric scale across subjects.

Field

Purpose

Example

difficulty_profile_schema

Names the subject/workflow scoring schema.

PHYSICS_V1 / MATH_RMCEV_V1

difficulty_profile

Stores multidimensional difficulty values.

{recognition: 7, modelling: 6, execution: 4}

difficulty_band

Local band used by the workflow.

D3

learner_badge

Student-facing label only.

Hard

hint_profile

Named ladder semantics.

TRANSFER_H1_H3

hint_depth_required

Required support depth under the named profile.

H2

8.1 Named hint profiles

Profile

Semantics

Use

TRANSFER_H1_H3

H1 Notice → H2 Model → H3 Start

Static transfer/PYQ support

ASSIMILATION_H0_H3

H0 Independent → H1 Recognition → H2 Structure → H3 Execution

Partial-knowledge fading

TUTORING_H1_H5

Progressively deeper interactive reveal

Interactive tutoring / diagnostic help

9. skill-registry.yaml as the control plane

The registry should become the single architecture inventory. SKILL.md remains the runtime behavioral contract; the registry holds repository-level metadata such as grouping, object type, dependencies, authority ownership, profiles, install sets and lifecycle state.

Illustrative registry entry

skills:  grade9-physics:    group: subject-authority    kind: authority    domain: physics    authority:      - physics_correctness      - model_validity      - representation_semantics      - physics_difficulty    requires:      - grade9-source-grounding    install_profiles:      - physics      - publication      - full    status: active  grade9-transfer-coverage-auditor:    group: assurance    kind: compatibility-wrapper    canonical_owner: grade9-corpus-coverage-auditor    profile: EXTERNAL_TRANSFER    status: compatibility    replacement: grade9-corpus-coverage-auditor

9.1 Registry fields

Field

Meaning

group

Logical production layer.

kind

router / authority / service / workflow / auditor / profile / publisher / program / compatibility-wrapper.

domain

cross-subject / mathematics / physics / chemistry / program-specific.

authority

Canonical concern keys owned by this skill.

requires

Hard dependencies.

optional_requires

Conditional dependencies.

extends / profile

Specialization relationship.

authority_model

source_document / canonical_master / external_corpus / other.

install_profiles

Named installation bundles.

status

active / compatibility / deprecated / removed.

replacement

Migration target when not active.

version

Repository version metadata without changing Agent Skill frontmatter.

10. Installation profiles

Profile

Contents (conceptual)

Purpose

platform-core

grade9; source-grounding; concept-architect; question-bank; learning-enrichment

Generic multi-stage work

subjects

math; physics; chemistry

Subject authority pack

assurance

corpus auditor; subtopic completeness auditor

Coverage and learning release

publication

publication; textbook-publisher; assurance dependencies

Reconstruction/render workflows

mathematics

platform-core + math + math-assimilation + math coverage profile

Mathematics learning products

physics

platform-core + physics + physics subtopic workflow + assurance/publication as needed

Physics packages

chemistry

platform-core + chemistry + Redox workflow + assurance/publication as needed

Chemistry/Redox packages

ioqm

mathematics + IOQM program workflows

IOQM topic/exam production

full

All active canonical capabilities + compatibility wrappers as configured

Development / complete environment

11. Generated documentation and distributions

The repository should stop manually maintaining multiple independent skill inventories. The registry should generate the human and machine-facing views.

SKILLSET.md: generated human-readable catalog grouped by architecture layer.

Installer profile manifests: generated from install_profiles and dependency closure.

Router catalog: generated task-to-skill summary used by grade9.

ChatGPT distribution manifest: generated from active/installable skills.

Agent Skills distribution: generated from the same source folders.

Dependency report: generated graph showing hard, optional and compatibility edges.

Compatibility report: active wrappers, replacements and planned removals.

Author once, package twiceGrade 9/skills should remain the canonical skill source. The current separately maintained ChatGPT skill family should become a generated distribution under dist/chatgpt-skills rather than a second manually edited source of truth.

12. Router simplification

grade9 should remain the public entry point for complex work, but become smaller. It should select workflows using registry metadata instead of embedding increasing amounts of Redox-, Math-, audit- and publication-specific detail.

Request signature

Primary route

Source PDF/book reconstruction

source-grounding → subject authority → publication → assurance

Validated master JSON to PDF

subject authority as needed → textbook-publisher → assurance

Same-level/challenge questions

source-grounding → subject authority → question-bank → enrichment

Math partial-knowledge concept product

source-grounding → math → math-assimilation → assurance → publication

Physics subtopic Study Guide + transfer

source-grounding → physics → physics workflow → assurance → publication

Redox subtopic/chapter

source-grounding → chemistry → Redox workflow → assurance; closeout workflow at chapter end

IOQM main topic/model exam

math + IOQM program workflow + assurance/publication

13. Validation and CI gates

The current validator primarily checks folder/frontmatter/interface shape. The refactor should add architecture-level checks.

Gate

Failure blocked

REGISTRY ↔ FILESYSTEM

Active registry entry without SKILL.md; skill folder without registry entry.

DEPENDENCY EXISTENCE

requires/extends points to missing skill.

DEPENDENCY CLOSURE

Install profile omits a transitive hard dependency.

AUTHORITY UNIQUENESS

Two active skills claim the same canonical authority key.

NO ACTIVE→DEPRECATED DEP

New active workflow depends on deprecated wrapper instead of replacement.

CYCLE CHECK

Circular workflow/authority dependency.

DISTRIBUTION PARITY

ChatGPT/Agent distribution differs from selected registry profile.

ROUTER PARITY

Router references a skill not available in its declared profile.

FRONTMATTER CONTRACT

Installable Agent Skill violates name/description contract.

INTERFACE CONTRACT

Callable skill missing agents/openai.yaml unless explicitly non-installable profile/reference.

14. Migration strategy

Pass 1 — Inventory and control plane

Create skill-registry.yaml and register all 20 existing skill folders.

Classify each as router, authority, service, workflow, auditor, profile, publisher, program or compatibility wrapper.

Record canonical authority keys and dependency relationships.

Define install profiles without moving skill folders.

Update validation so registry ↔ filesystem parity is checked.

Reconcile the 20/14/10/9 inventory drift and generate an authoritative inventory report.

Pass 2 — Ownership and deduplication

Make corpus-coverage-auditor the canonical coverage engine.

Convert transfer-coverage-auditor to compatibility/profile semantics.

Thin grade9-math operational duplication and point to math-assimilation for the execution workflow.

Reduce duplicated transfer/corpus/render contracts inside subtopic-completeness-auditor by delegation.

Centralize hint-profile and difficulty metadata contracts.

Assign one canonical owner to stable IDs, source statuses, coverage accounting, publication QA and similar cross-cutting rules.

Pass 3 — Generated distribution

Generate SKILLSET.md from registry.

Generate install profile manifests and dependency closure.

Generate ChatGPT distribution/manifest from canonical skill source.

Generate router catalog from registry.

Add distribution parity validation and CI.

Keep current skill IDs stable to avoid breaking existing invocations.

Pass 4 — Optional workflow extraction after evidence

Observe repeated lifecycle patterns across Physics, Redox and Mathematics builds.

Extract a generic subtopic-package workflow shell only where behavior is genuinely common.

Keep subject representations and pedagogy inside subject-specific profiles/workflows.

Consider physical folder reorganization only after tooling no longer assumes a flat skills directory.

15. Compatibility and deprecation policy

LifecycleACTIVE → COMPATIBILITY → DEPRECATED → REMOVED

Do not delete old skill IDs in the first refactor.

Compatibility wrappers must delegate to the canonical replacement and must not acquire new independent rules.

New active workflows may not depend on deprecated wrappers.

Each compatibility entry records replacement, migration note and earliest removal version.

Removal occurs only after router/install/distribution references are clean.

16. Risks and mitigations

Risk

Failure mode

Mitigation

Over-consolidation

Generic workflow flattens subject-specific pedagogy.

Extract lifecycle only; retain subject representations/teaching grammar.

Breaking existing invocations

Renames/folder moves disrupt agents.

Keep stable skill IDs and flat folders in initial phases.

Registry becomes another duplicate source

Manual docs continue beside registry.

Generate SKILLSET/install/distribution from registry; validate parity.

Authority ambiguity

Two skills continue redefining one contract.

Machine-check authority keys and reject duplicate active owners.

Profile explosion

Too many tiny profiles become hard to use.

Profiles only when they specialize a canonical engine; workflows remain for ordered operations.

Difficulty scale confusion

D3/H2 semantics mix across subjects.

Central schema + named profile; local subject scales remain explicit.

Compatibility never removed

Legacy wrappers accumulate.

Lifecycle status, replacement metadata and release-based removal policy.

17. Success criteria

Measure

Target

Inventory parity

Filesystem active skills = registry active skills = generated catalog = selected distribution.

Installer integrity

Every install profile contains complete transitive hard dependencies.

Router integrity

Every router target is registered and installable in the applicable profile.

Authority conflicts

0 duplicate active authority owners.

Coverage engine duplication

One canonical corpus accounting model; specializations reference it.

Compatibility drift

No new workflow depends on compatibility/deprecated aliases.

Distribution drift

0 manually divergent ChatGPT/Agent skill copies.

Discoverability

An agent can identify skill type, authority, dependencies and replacement from registry alone.

Handoff quality

A new agent can continue without reading prior chat history.

18. Explicit non-goals

Do not rewrite subject pedagogy merely to make skills look uniform.

Do not merge grade9-publication with grade9-textbook-publisher.

Do not physically move all skill folders in the first implementation pass.

Do not change stable skill IDs unless a separate migration is approved.

Do not force Mathematics, Physics and Chemistry onto one numeric difficulty scale.

Do not make auditors silently repair source/scope simply to pass counters.

Do not treat program-specific IOQM logic as generic Grade 9 authority.

19. Approval decisions requested

ID

Approval item

Decision

A1

Adopt the 00–90 layered architecture.

YES / NO

A2

Adopt one-canonical-owner-per-reusable-rule as a machine-enforced principle.

YES / NO

A3

Create skill-registry.yaml as the architecture control plane.

YES / NO

A4

Keep current flat skill folders during Pass 1.

YES / NO

A5

Make corpus-coverage-auditor the canonical coverage engine.

YES / NO

A6

Migrate transfer-coverage-auditor to compatibility/profile semantics.

YES / NO

A7

Treat math-assimilation as a workflow under grade9-math authority.

YES / NO

A8

Keep the two publication engines separate and clarify display names.

YES / NO

A9

Move IOQM conceptually under Programs/Tracks.

YES / NO

A10

Generate SKILLSET/install/distribution artifacts from the registry.

YES / NO

A11

Adopt named difficulty/hint profile schema without collapsing subject scales.

YES / NO

A12

Adopt four-pass migration sequence.

YES / NO

20. Recommended approval statement

Proposed approvalApproved in principle to refactor the Grade 9 skill family using the layered architecture, canonical authority ownership, skill-registry control plane, generated distributions, compatibility lifecycle and four-pass migration sequence described in this note. Pass 1 may proceed without renaming or physically relocating existing skill folders. Any removal of legacy skill IDs or material change to subject pedagogy requires separate approval.

Appendix A — Proposed classification of all 20 current skills

Skill

Proposed layer

Kind

Status

grade9

00 Orchestration

ROUTER

Canonical

grade9-source-grounding

10 Source & Knowledge

AUTHORITY

Canonical

grade9-concept-architect

10 Source & Knowledge

AUTHORITY

Canonical

grade9-math

20 Subject Authorities

AUTHORITY

Canonical

grade9-physics

20 Subject Authorities

AUTHORITY

Canonical

grade9-chemistry

20 Subject Authorities

AUTHORITY

Canonical

grade9-question-bank

30 Learning Object Authoring

SERVICE

Canonical

grade9-learning-enrichment

30 Learning Object Authoring

SERVICE

Canonical

grade9-math-assimilation

40 Product Workflows

WORKFLOW

Active

grade9-physics-subtopic-book-builder

40 Product Workflows

WORKFLOW

Active

grade9-redox-subtopic-book-builder

40 Product Workflows

WORKFLOW

Active

grade9-corpus-coverage-auditor

50 Assurance

AUDITOR

Canonical

grade9-subtopic-completeness-auditor

50 Assurance

AUDITOR

Canonical

grade9-math-corpus-coverage-auditor

50 Assurance

PROFILE/EXTENSION

Active

grade9-redox-chapter-closeout-auditor

50 Assurance

WORKFLOW

Active

grade9-transfer-coverage-auditor

90 Compatibility

COMPATIBILITY

Migrate

grade9-publication

60 Publication

PUBLISHER/CONTROL

Canonical

grade9-textbook-publisher

60 Publication

PUBLISHER

Canonical

ioqm-grade9-main-topic-builder

70 Programs

PROGRAM WORKFLOW

Active

ioqm-grade9-model-exam-builder

70 Programs

PROGRAM WORKFLOW

Active

Appendix B — Evidence basis from the current repository

Repository source

Architectural evidence

Grade 9/skills/grade9/SKILL.md

Current router already sequences source grounding, subject skills, builders, audits and publication, indicating the latent layered architecture.

Grade 9/skills/grade9-source-grounding/SKILL.md

Defines source transcription/QC/provenance statuses; suitable source authority.

Grade 9/skills/grade9-concept-architect/SKILL.md

Defines stable IDs, prerequisites and page-independent concept linkage.

Grade 9/skills/grade9-question-bank/SKILL.md

Owns difficulty-calibrated question generation and mixed mastery.

Grade 9/skills/grade9-learning-enrichment/SKILL.md

Owns generic recognition, hints, misconceptions, diagnostics and transfer objects.

Grade 9/skills/grade9-corpus-coverage-auditor/SKILL.md

Subject-agnostic coverage/accounting model with source snapshots, dispositions and one-primary-owner invariant.

Grade 9/skills/grade9-transfer-coverage-auditor/SKILL.md

Overlaps corpus accounting but specializes external/PYQ transfer placement/support.

Grade 9/skills/grade9-math-corpus-coverage-auditor/SKILL.md

Already declares itself an extension of the general corpus auditor.

Grade 9/skills/grade9-subtopic-completeness-auditor/SKILL.md

Checks whole learning experience rather than only source-row coverage.

Grade 9/skills/grade9-publication/SKILL.md

Treats existing source PDF/book as immutable source authority for reconstruction.

Grade 9/skills/grade9-textbook-publisher/SKILL.md

Treats PDF as rendered output from validated canonical master data.

Grade 9/skills/ioqm-grade9-main-topic-builder/SKILL.md

Program-specific integrated topic architecture; not a generic Math authority.

Grade 9/skills/ioqm-grade9-model-exam-builder/SKILL.md

Program-specific complete timed-exam workflow.

Grade 9/install_skills.py

Hard-coded installer currently installs only ten skill folders.

Grade 9/validate_skills.py

Validator assumes immediate skill folders and strict Agent Skill shape; physical nesting should therefore wait.

Grade 9/chatgpt-skills/README.md

Separately maintained ChatGPT distribution documents nine skills, creating a second inventory surface.

Appendix C — First implementation deliverables after approval

skill-registry.yaml v1 covering all 20 existing skills.

Registry schema/readme with kind, group, authority, requires, profile, install-profile and lifecycle semantics.

Inventory reconciliation report: filesystem vs SKILLSET vs installer vs ChatGPT distribution.

Updated validator with registry/filesystem/dependency/authority checks.

Generated SKILLSET.md proof-of-concept.

Install profiles: platform-core, subjects, assurance, publication, mathematics, physics, chemistry, ioqm, full.

Compatibility entry for grade9-transfer-coverage-auditor.

Migration notes for math-assimilation duplication and completeness-auditor delegation.

No folder moves and no skill-ID renames in Pass 1.

Appendix D — Architecture principle summary

Skills should represent reusable authorities or services.

Workflows should compose those authorities.

Profiles should specialize canonical engines.

Auditors should verify rather than author.

Publishers should reconstruct/render rather than redefine source or subject truth.

Programs may be opinionated but must consume—not duplicate—canonical Grade 9 authorities.

One architecture registry should control inventory, dependencies, installation and distribution.
