# Mathematics Core (1) - executable architecture

**Status:** draft implementation stacked on PR #160 frozen v1 Core (1) contracts  
**Scope:** Mathematics only  
**Downstream boundary:** Core (2) consumes `ResearchBundle + ResearchBundleManifest + LearnerProfile + PublicationTarget`

## 1. Ownership

Mathematics Core (1) owns the project research boundary:

```text
repository discovery
-> canonical Math authority selection
-> project ScopeGraph
-> research gaps
-> verified mathematical claims
-> representation semantics
-> formal objects / derivations
-> question-family and exam-demand evidence when applicable
-> frozen ResearchBundle + manifest
```

It does **not** own learner Bxx, learner sequencing, hint depth, appendices, page composition, or final learner publication. Those are downstream Core (2) concerns.

## 2. Agent entry point

Use `$grade9-math-core1`.

The agent must first inspect the repository for existing Mathematics authority, concept maps, source ledgers, prior Research Bundles, question evidence, and unresolved audits. It must not begin with `build_research_package.py`: that script packages already-researched structured data and does not perform mathematical research.

The agent asks only for missing intake data. It may ask the user for topic/subtopics, purpose, and a Bxx matrix, but Bxx is written to a separate `LearnerProfile` for Core (2), never into the semantic ResearchBundle.

For competitive Mathematics, the order is intentionally different:

```text
repo discovery
-> resolve exam identity/cycle
-> inspect verified samples/PYQs
-> reverse engineer actual mathematical engines
-> propose topic/subtopic map
-> ask/confirm learner Bxx
-> freeze Core (1) scope
```

For routine/generic Mathematics:

```text
repo discovery
-> propose/confirm topic/subtopics
-> ask/confirm Bxx + purpose
-> research only missing/stale evidence
-> freeze Core (1) scope
```

## 3. Math research object model

For every material concept in scope, Core (1) should establish:

```text
canonical concept reference
prerequisites / bridge nodes
invariant or mathematical engine
conditions / domain / edge cases
proof or derivation where material
required representation semantics
expert noticing / first move
nearest competing method
misconceptions / counterexamples
transfer endpoints
source-backed ResearchClaim IDs
```

A question or example may be used as evidence, but the Core (1) object is the mathematical structure, not the surface wording.

## 4. ScopeGraph rule

The project ScopeGraph references versioned canonical Math registry IDs. New ontology items are not silently minted as canonical. The only legal promotion path is:

```text
RESEARCH_CANDIDATE
-> SUBJECT_AUTHORITY_REVIEW
-> CANONICAL_PROMOTION_APPROVED
```

A `READY_FOR_PUBLISH` Math Core (1) may not contain unresolved project candidates or blocking research gaps.

## 5. Source and rights discipline

Every material ResearchClaim has explicit source lineage. Source discovery does not imply reproduction permission. The source ledger must retain authority, verification and rights/use state.

External question systems such as ExamSIDE are handled as evidence/corpus sources. Full external-question coverage requires a frozen `QuestionEvidenceLedger`; a topic ResearchBundle without that ledger must not claim complete external-corpus closure.

## 6. Mathematical verification gates

A Math ResearchBundle may be `READY_FOR_PUBLISH` only when:

```text
MATH_SUBJECT = PASS
SCOPE_REFERENCES_VERSIONED = PASS
BXX_ABSENT_FROM_RESEARCH_BUNDLE = PASS
CONCEPT_CLAIM_COVERAGE = 100%
MATERIAL_CLAIMS_VERIFIED = 100%
MATERIAL_CLAIMS_SOURCE_LINKED = 100%
CONDITIONS_AND_EDGE_CASES_CHECKED = PASS
REPRESENTATION_SEMANTICS_RESOLVED = PASS
FORMAL_OBJECT_REFS_RESOLVED = PASS
WORKED_REASONING_REFS_RESOLVED = PASS
BLOCKING_UNRESOLVED_ITEMS = 0
UNPROMOTED_PROJECT_CANDIDATES = 0
```

For competitive/external-question work add:

```text
EXAM_DEMAND_PROFILE = PASS
QUESTION_EVIDENCE_DENOMINATOR = PASS
REVIEW_ROWS = 0
SOURCE_RIGHTS_STATE = EXPLICIT
```

## 7. Core (1) package outputs

Use PR #160 v1 output names:

```text
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Research_Bundle.json
<Topic>_Research_Bundle_Manifest.json
<Topic>_Source_Ledger.json
```

Competitive/external-question projects additionally produce ExamDemand and QuestionEvidence artifacts.

`ResearchBundle.json` is canonical. MD/PDF are derived human review surfaces and must reconcile 100% of material semantic IDs.

## 8. Cold-start handoff

A clean downstream agent should need only:

```text
ResearchBundle
ResearchBundleManifest
SourceLedger
approved assets / optional evidence ledgers
LearnerProfile
PublicationTarget
shared schemas / subject skills
```

If Core (2) discovers missing mathematical truth, it returns `CORE1_RESEARCH_GAP`. It does not browse around the gap or patch the learner material.

## 9. Falsifier in this PR - Permutations

`Grade 9/Mathematics/Permutations/Core1/` is a Mathematics Core (1) falsifier built on existing repository combinatorics authority. It freezes twelve permutation reasoning engines and their representation semantics while keeping learner Bxx and publication purpose out of the ResearchBundle.

The fixture intentionally does **not** claim full ExamSIDE/JEE corpus closure. The ExamSIDE index is retained as `REFERENCE_ONLY` evidence discovery. A future JEE/ExamSIDE publication must add a complete QuestionEvidenceLedger before making source-completeness claims.

## 10. Relationship to PR #160 and PR #161

PR #160 owns and freezes the shared v1 handoff schemas. This Math layer consumes those contracts unchanged. It adds Math-specific agent behavior, semantic validation and a real topic replay; it must not fork or redefine the shared schema family.

PR #161/Core (2) starts after this boundary and consumes the frozen research package plus separate learner/purpose overlays.
