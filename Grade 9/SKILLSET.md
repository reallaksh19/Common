# Grade 9 Skill Family

This folder contains the reusable Grade 9 learning-production skill family derived from the repository's shared Grade 9 workflow and subject-specific publication contracts.

## Skills

| Skill | Purpose |
|---|---|
| `grade9` | Router/orchestrator |
| `grade9-source-grounding` | Source extraction, QC, provenance, verification |
| `grade9-concept-architect` | Stable concept IDs, prerequisites, learning graph, links |
| `grade9-question-bank` | Core practice, difficulty calibration, variation, mixed tests |
| `grade9-learning-enrichment` | Helpers, hints, misconceptions, diagnostics, transfer |
| `grade9-publication` | Source-faithful educational PDF reconstruction and reconciliation |
| `grade9-subtopic-completeness-auditor` | Whole-subtopic source/pedagogy/practice/typography/layout audit |
| `grade9-transfer-coverage-auditor` | External/PYQ accounting, placement, hints, solutions and source-link coverage |
| `grade9-textbook-publisher` | Linked learner PDF production from validated canonical data |
| `grade9-math` | Mathematics reasoning/difficulty profile and concept-book routing |
| `grade9-physics` | Physics reasoning/representation profile and concept-book routing |
| `grade9-chemistry` | Chemistry macro-particle-symbolic/evidence profile and Chemistry routing |
| `grade9-chemistry-topic-builder` | **Generic Chemistry topic authoring contract:** exactly two learner PDFs per topic; Core with Appendix A Core Practice, Appendix B Core Solutions, Appendix C Printable Handout; ExamSIDE Solution & Transfer with concept segregation, badges, H0/H1-H3, links and complete solutions |
| `grade9-chemistry-publication-review` | Chemistry-wide publication/review gate for two-file delivery, Appendix A/B/C, ExamSIDE support, source/corpus reconciliation, artifact custody and fail-closed QA |
| `grade9-redox-subtopic-book-builder` | Redox-specific reasoning adapter under the generic Chemistry topic-builder contract |
| `grade9-redox-chapter-closeout-auditor` | Redox full-corpus/source closeout and unique canonical placement gate |

## Chemistry topic-production mode

For **every Chemistry topic**, invoke `$grade9-chemistry-topic-builder`.

The fixed learner-facing deliverable contract is:

```text
FILE 1 — CORE STUDY GUIDE
  teaching narrative
  Appendix A — Core Practice
  Appendix B — Core Solutions
  Appendix C — Printable Handout

FILE 2 — EXAMSIDE SOLUTION & TRANSFER
  attempt-first question
  source/date/shift badge
  difficulty badge
  transfer badge
  primary concept label
  PRIMARY vs SUPPORT concept segregation label
  Core Study Guide cross-link
  source link
  H0 + optional H1/H2/H3
  concept helper / misconception watch when needed
  complete solution
```

Appendix C is mandatory and blocking. It is the printable/detachable handout **inside the Core Study Guide**; do not create a third learner-facing handout PDF.

The subject-wide contracts live at:

- `Chemistry/CHEMISTRY_PUBLICATION_SCHEMA.md`
- `Chemistry/schema/chemistry-topic-delivery.schema.json`
- `Chemistry/schema/chemistry-publication-package.schema.json`
- `skills/grade9-chemistry-topic-builder/SKILL.md`

Redox is only an instance. When working on Redox, run `$grade9-chemistry-topic-builder` plus `$grade9-redox-subtopic-book-builder`; the Redox adapter may specialize representations/misconceptions but cannot alter the Chemistry two-file or Appendix A/B/C contract.

## Chemistry publication-review mode

After content/source/transfer audits pass, run `$grade9-chemistry-publication-review` before a Chemistry topic/chapter is declared review-ready.

The publication gate must verify:

- exactly two learner-facing topic PDFs;
- Appendix A, Appendix B and Appendix C inside every Core Study Guide;
- Appendix C is recognisably a standalone printable handout and introduces no new chemistry;
- ExamSIDE question pages carry required concept segregation, badges, progressive support and complete solutions;
- source obligations have page/region locators;
- external-corpus counters are derived from records, not trusted summaries;
- exact artifact custody/reconstruction exists;
- link/notation/layout/answer-leakage checks pass;
- technical PASS remains separate from teacher/classroom approval.

## Shared contracts

- `shared/grade9-workflow.md` — operational cross-skill workflow.
- `shared/grade9-master.schema.json` — canonical reusable master-data schema.
- Repository root `Grade9schema.md` — fuller human specification and implementation history.
- `skills/grade9-publication/references/publication-playbook.md` — source-faithful publication reconstruction manual.
- `skills/grade9-publication/references/audit-manifest-spec.md` — deterministic zero-loss/link/render audit contract.

## Source-PDF reconstruction mode

Use `$grade9-publication` when the supplied educational PDF/book itself is the reconstruction source. Preserve an immutable source, freeze stable source obligations before redesign, separate source content from value-add/editorial changes, use anti-drift checkpoints, and require render-first reconciliation before claiming completeness.

## Subtopic completeness audit mode

Run `$grade9-subtopic-completeness-auditor` after a topic/subtopic draft exists. Require source coverage, meaning-before-procedure, safe familiar context where useful, reusable helpers, explicit misconception repair, worked/guided/faded/independent practice, correct chemistry typography and collision-free rendering.

For Chemistry Core products this audit must additionally confirm Appendix A/B/C presence and Appendix C handout usability.

## Transfer coverage audit mode

When an external corpus such as ExamSIDE is part of the brief, run `$grade9-transfer-coverage-auditor` before declaring the topic complete. Require one scope status per candidate, exactly one canonical primary home for eligible items, concept links, difficulty-appropriate hints, complete solution coverage, original source links and zero missing/duplicate primary placements at final acceptance.

For Chemistry ExamSIDE products also require source/difficulty/transfer badges and visible primary-vs-support concept segregation.

## Redox closeout mode

After Redox topics are built, run `$grade9-redox-chapter-closeout-auditor` to enumerate the full frozen corpus, classify all candidates, backfill missed eligible variants, preserve unique primary homes, close source obligations and run master render QA. This is Redox-specific closeout evidence, not a replacement for the generic Chemistry publication schema.

## Deterministic checks

- `skills/grade9-question-bank/scripts/difficulty_check.py`
- `skills/grade9-question-bank/scripts/validate_bank.py`
- `skills/grade9-textbook-publisher/scripts/check_master_links.py`
- `skills/grade9-publication/scripts/check_publication_manifest.py`
- Chemistry publication tooling under `Chemistry/tools/` when present in a package branch

## Recommended invocation

```text
Use $grade9 for a multi-stage Grade 9 build.
Use $grade9-chemistry-topic-builder to build this Chemistry topic as Core + ExamSIDE.
Use $grade9-redox-subtopic-book-builder together with the Chemistry topic builder for Redox-specific reasoning.
Use $grade9-subtopic-completeness-auditor to audit the Core teaching and Appendices A-C.
Use $grade9-transfer-coverage-auditor to audit external-question placement/support.
Use $grade9-chemistry-publication-review to verify the two-file package and publication/review gates.
```

Every live skill must have `SKILL.md`, `agents/openai.yaml`, valid frontmatter and installer/router reachability where routed.
