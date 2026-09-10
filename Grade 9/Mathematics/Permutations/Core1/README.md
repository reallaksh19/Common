# Permutations - Math Core (1) falsifier

This folder is **not** a learner Study Guide and is **not** the old ST01/ST07 publication pilot.

It demonstrates the PR #160 two-core boundary for a real Mathematics topic:

```text
existing repository Math authority
-> permutation ScopeGraph
-> verified research claims
-> representation semantics
-> formal identities
-> worked reasoning records
-> frozen learner-neutral ResearchBundle
-> Core (2) handoff
```

## Scope

The ResearchBundle freezes twelve permutation reasoning engines:

`ST01 ordered slots`, `ST02 multiset`, `ST03 positional restrictions`, `ST04 block`, `ST05 complement`, `ST06 gaps`, `ST07 number formation`, `ST08 lexicographic rank`, `ST09 circular`, `ST10 derangements`, `ST11 forbidden strings / inclusion-exclusion`, and `ST12 hybrid structures`.

These IDs are grounded in the existing repository permutation ownership taxonomy and its version is recorded in the ScopeGraph.

## Deliberate exclusions

- no Bxx or learner profile;
- no Core (2) sequencing, hints, appendices or page composition;
- no claim of complete ExamSIDE/JEE question coverage;
- no reproduction of ExamSIDE question text.

The external ExamSIDE index is retained only as `REFERENCE_ONLY` discovery evidence. A future JEE/ExamSIDE publication must add a frozen QuestionEvidenceLedger before claiming external-corpus completeness.

## Files

- `research_input.json` - already-researched structured input to the shared PR #160 package builder.
- `Permutations_Core1_Research_Bundle.json` - canonical machine handoff.
- `Permutations_Core1_Research_Bundle_Manifest.json` - evidence/package identity and artifact hashes.
- `Permutations_Core1_Source_Ledger.json` - source/rights custody.
- `Permutations_Core1_Research_Core.md` / `.pdf` - human review surfaces derived from the bundle.

The Math-specific validators in `$grade9-math-core1` require 100% concept-claim coverage, source-reference closure, no unpromoted project candidates, no blocking unresolved items and no learner-state leakage before `READY_FOR_PUBLISH`.
