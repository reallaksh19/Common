# V2-01 · Core1 Canonical Subject Authority

Parent roadmap: Common #175  
Implementation issue: Common #180  
Migration governance: Common #178 / PR #179

This directory implements the subject-neutral V2 Core1 boundary:

```text
canonical registry
        ↓
deterministic dependency resolver
        ↓
CanonicalKnowledgeSet
```

If required canonical semantics are unavailable, the resolver produces an explicit
`CanonicalGapCandidate`. It never invents or promotes subject truth.

## Authority

Core1 owns learner-independent subject/shared semantics. Learner evidence, learner
state, study decisions, teaching choreography, publication realization and benchmark
validation are outside this directory.

A canonical asset may describe a concept, capability, formal object, relation,
representation, misconception/error-signature semantic or diagnostic-probe semantic.
It may depend on canonical assets from another subject/shared domain.

A canonical asset must never contain learner-specific state or downstream decisions.

## Clean-lineage rule

PR #160 and PR #167 are migration evidence only. Runtime code here imports no old PR
branch and contains no old branch path. The V2-00A adoption ledger remains the
migration authority.

PR #156 / PR #157 and future mature learner artifacts are not canonical inputs.

## Contracts

- `contracts/canonical-asset.schema.json`
- `contracts/canonical-registry.schema.json`
- `contracts/canonical-knowledge-set.schema.json`
- `contracts/canonical-gap.schema.json`

## Resolver invariants

1. Only `PROMOTED` assets may enter a successful `CanonicalKnowledgeSet`.
2. Dependency closure is transitive and deduplicated.
3. Missing/unpromoted requirements become deterministic gap candidates.
4. Cycles and semantic-digest mismatches fail closed.
5. Same registry + policy + request produces byte-stable semantic output.
6. `CanonicalKnowledgeSet` binds registry version, resolver policy, exact asset digests
   and dependency reasons.
7. Learner/state/study/teaching/benchmark contamination is rejected recursively.
8. Resolver output cannot auto-promote a gap candidate.

## Synthetic fixtures only

All fixtures in this PR use IDs beginning `SYN-` and payloads explicitly marked
`fixture_only`. They prove resolver mechanics; they are not Mathematics, Physics or
Chemistry knowledge.

## CLI

```bash
python "Grade 9/V2/Core1/resolve_canonical.py" \
  --registry "Grade 9/V2/Core1/fixtures/valid/registry.json" \
  --request "Grade 9/V2/Core1/fixtures/valid/request.json"
```

A successful resolution exits `0`. A canonical gap is emitted deterministically and
the CLI exits `2`. Contract/registry corruption exits non-zero.

## Deliberate non-goals

No real subject migration, learner evidence/state, Study Synthesis, LearningDesign,
publication/PDF, longitudinal scheduling, or benchmark comparison is implemented here.
