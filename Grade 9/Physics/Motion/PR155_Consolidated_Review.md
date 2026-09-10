# PR #156 review consolidation and structural gap analysis

## Scope

This document consolidates seven submitted reviews and 43 inline threads on PR #156 into 21 unique findings. Repeated comments are grouped by failure boundary, not counted as separate defects.

The PR is a two-topic Motion publication pilot. It is not a completed 68-question chapter, a verified ExamSIDE corpus, an adaptive student-remediation system, or a classroom-validated release.

## Structural diagnosis

The recurring failure was promotion of component checks into end-to-end claims:

```text
chapter authority
  → raw source extraction
  → immutable source ledger
  → publication model
  → learner render
  → PDF audit
  → package summaries and manifest
  → release claim
```

Before this repair, several stages passed independently while adjacent stages were not bound to each other. Examples included a ledger that checked its own IDs but not raw source identity, mixed-test metadata that was never rendered, a study-guide profile that rendered but crashed in audit, and package summaries that retained old model/PDF hashes while still reporting PASS.

The repair principle is therefore: a stage may report only what it directly proves, and a final package PASS requires every machine-checkable boundary in the chain to agree.

## Consolidated findings and disposition

| # | Consolidated finding | Structural cause | Implemented disposition |
|---|---|---|---|
| 1 | Installed skill family failed its own package validator; the inventory was stale. | Install-copy success was treated as package conformance. | Added missing `agents/openai.yaml` files, corrected interface prompts/frontmatter, updated `SKILLSET.md`, and retained install and family validation as separate checks. |
| 2 | Motion canonical crosswalk was presence-checked rather than authority-checked. | A local string was accepted without binding it to the chapter map. | Added a canonical registry with the source-map SHA-256 and exact allowed IDs; validation checks the current map hash, derives its `CB0..CB12` keys, requires exact set equality, and rejects unknown concept parents. |
| 3 | Source status, provenance, transcription, and adaptation were conflated. | One editorial state was used to infer unrelated source authority. | Kept each axis independent. Original and external combinations are typed, but no one-to-one provenance map exists. |
| 4 | Ledger reconciliation could false-pass and did not bind the rendered artifact. | Non-original states were collapsed to one bit and the ledger carried too little source identity. | Expanded the ledger contract to raw document/hash/page/stem/answer/options/figure semantics/URL/locator/adaptation/targets. `reconcile.py` compares exact state axes and source identity and optionally requires the audit to name the exact model hash and a concrete PDF hash. Eleven induced drift cases cover the boundary. |
| 5 | `mixed_tests[]` existed only as metadata. | The renderer consumed the ordinary question list only. | Mixed sets now carry stable `test_id`/`set_id`, `study_mode=MIXED_TRANSFER`, and `concept_hidden=true`; the renderer uses set order, hides task/concept cues on attempt pages, uses item-demand pagination, and reveals diagnosis only after solutions. |
| 6 | `study_guide` and `transfer_book` were not end-to-end product profiles. | Validation rules, render ownership, audit assumptions, repair navigation, and pair identity disagreed. | The canonical profiles now pass validate → render → audit and must pass reciprocal pair reconciliation. A Study Guide carries Core practice plus Appendices A–C; an ExamSIDE Solution Book carries externally grounded questions, badges, hints, transfer diagnosis and Appendix A solutions. Legacy pilot profiles cannot claim pair completion. |
| 7 | Chapter-scale closure was claimed from a 72-item clone. | Item-count capacity was confused with batch consolidation semantics. | The generic closeout skill now delegates AD-22..AD-29 mechanics to `grade9-publication/references/batch-production.md` and verifies their evidence. The 72-item test is described only as renderer capacity. A complete 68-question Motion chapter remains not authored. |
| 8 | The Redox closeout profile still duplicated the generic workflow. | Declared ownership changed but the old copied sections remained. | Reduced Redox to a thin chemistry-specific dependency and typography profile over the generic closeout owner. |
| 9 | Difficulty vectors were mechanically derived from task type. | A renamed heuristic was presented as multidimensional calibration. | Removed ungrounded numeric vectors from the pilot. `task_type` remains descriptive; `difficulty_source=AUTHOR_HEURISTIC` and `qa.difficulty_checked=false` remain explicit until source analysis, expert calibration, or empirical data exists. |
| 10 | Committed PDFs, audits, summaries, and manifest disagreed. | Artifact generation had no package-level identity gate. | All three model/PDF/layout/audit pairs are regenerated together. `verify_review_package.py` checks model/PDF hashes, exact summary copies, render blockers, complete manifest scope, byte counts, and hashes. |
| 11 | B80-L4 omitted the instantaneous-transition modelling condition. | Support compression removed a physical idealisation note while preserving the discontinuous graph. | Added the zero-duration idealisation cue; no numerical method or answer changed. |
| 12 | Transfer-book repair targets were dead semantic references. | Local lesson validation was disabled without defining an external route. | Added typed `LOCAL_LESSON`, `EXTERNAL_COMPANION`, and `SELF_CONTAINED` repair modes. External repair requires a valid companion title, URL, and locator and is rendered as a working link. |
| 13 | Master-schema conformance was a one-off command. | Compatibility evidence lived outside the normal test chain. | `test_v2.py` validates all three committed models against `grade9-master.schema.json` on every run. |
| 14 | “A–O closed” was blurred with completion of weak-topic remediation. | Review-finding closure and product-capability closure were treated as the same status. | The claim is narrowed: the reviewed publication/packaging gaps are repaired, while per-student concept mastery, diagnostic event capture, retry/promotion logic, and learner-outcome storage remain explicitly outside this PR. |
| 15 | The installed `$grade9` router advertised Redox builders that the default installer omitted. | Router capability and installer closure were maintained independently. | Added both routed Redox skills to the installer and made `validate_skills.py` derive advertised live-skill dependencies from the router, rejecting any future omission. |
| 16 | Package summaries hard-coded PASS and fixed test counts. | Narrative summaries were treated as evidence producers. | Added `run_review_checks.py`; summaries now project statuses only from captured real commands, exit codes, output hashes, dependency hashes, and artifact hashes. |
| 17 | A visual PASS survived changes to the PDFs. | Human review text had no artifact identity. | Added `visual_review_evidence.json` and `record_visual_review.py`; PASS requires at least 200 DPI, every audited page, and exact hashes for all three PDFs. Stale evidence projects as `PENDING`. |
| 18 | The cold-start sequence skipped summary refresh. | Regeneration order did not model evidence dependencies. | `REPRODUCE.md` now orders render/audit/reconcile → machine evidence → visual evidence → summaries → manifest → package verification. |
| 19 | Manifest scope omitted live router, shared, schema, and publication dependencies. | A hand-picked producer list stood in for dependency closure. | Manifest scope now covers the live `Grade 9/skills` tree, `Grade 9/shared`, router/install validators, and the complete Motion package. |
| 20 | Mixed-test diagnosis rows still had a one-page ceiling. | Attempt pagination and diagnosis pagination used different layout models. | Diagnosis rows now paginate four per page with stable destinations and global question numbering; an eight-item executable case requires two diagnosis pages after all solutions. |
| 21 | External MCQ options and unsupported statement-like dependencies could exist only in citation metadata. | Source capture capability was mistaken for learner-render capability. | The Motion validator now hard-routes external items with choices, or dependency classes outside `NONE`, `GRAPH`, and `NUMBER_LINE`, to `grade9-publication` instead of silently producing incomplete learner pages. |

## Additional checks retained from the earlier review

- Solution methods reject terse, formula-only, and near-answer copies.
- Figure dependency classes are validated and reconciled across the ledger/publication boundary; the drawing implementations themselves remain Motion-specific.
- SRU-01..15 fields are typed and release-gated, but no authored concept receives self-attested pedagogical acceptance.
- The B30 grayscale route uses redundant line styling, not colour alone.
- The cold-start reviewer role remains in the review guide.
- The First-Step Reference remains a named shared learning-enrichment product; it is not duplicated into another Physics-only skill.

## Truthful validation boundary

The committed package may report automated PASS only for:

- skill-family metadata and scratch installation;
- publication schema and shared master-schema conformance;
- model invariants and numerical recomputation covered by the executable checks;
- supported product-profile rendering and PDF link/layout checks;
- ledger/model reconciliation for the original-question pilot;
- exact model/PDF/audit/summary/manifest identity.

The following remain `NOT_RUN`, `PENDING`, or out of scope and must not be promoted by those automated results:

- real external ExamSIDE/PYQ source-page fidelity: `NOT_RUN` because no qualified external-corpus fixture is included;
- complete 68-question Motion chapter authorship and chapter-closeout execution: `NOT_RUN`;
- per-student weak-topic diagnosis → repair → retry → promotion workflow: out of scope;
- independent SRU/pedagogy review: `PENDING`;
- classroom and psychometric testing: `NOT_RUN`;
- accessible tagged-PDF conformance and syllabus approval: `NOT_RUN`.
- source-owned difficulty-code normalization and learner-badge mapping: `NOT_RUN`; no qualified source difficulty data exists in this original-question pilot, so a `D1`–`D4` mapping is not guessed.

## Reproduction order

Run the package in this order:

1. validate and scratch-install the Grade 9 skill family;
2. regenerate the three models and exported schema;
3. run publication and reconciliation tests;
4. render and audit all three PDFs;
5. reconcile the question-bank ledger with the final audit;
6. run `run_review_checks.py` to bind real command outputs to current dependency/artifact hashes;
7. render every PDF page for visual inspection and record `visual_review_evidence.json` against the exact PDF hashes;
8. refresh package summaries and `FILE_MANIFEST.json`;
9. run `verify_review_package.py`.

This ordering prevents stale component evidence from being mistaken for a coherent release package.
