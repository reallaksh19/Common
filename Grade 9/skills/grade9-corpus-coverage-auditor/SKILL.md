---
name: grade9-corpus-coverage-auditor
version: 4
description: General-purpose auditor for reconciling an external source corpus or question bank against subtopic study guides, practice books, helpers, solutions, and publication artifacts. Use across subjects when a source corpus must be exhaustively classified and every eligible item must have an auditable home or explicit disposition.
---

# Grade 9 Corpus Coverage Auditor v4

## Purpose
Audit **source-to-learning coverage**, not merely whether a finished-looking PDF exists.

Use this skill when a project has:
- a bounded external corpus (question bank, past papers, workbook, textbook exercise set, source PDF, database, URL collection, etc.);
- a subtopic taxonomy;
- one or more learning artifacts (Study Guide, Practice Book, Transfer Book, Appendix, solutions, helpers);
- a requirement that eligible source items be traceably covered.

This skill is **subject-agnostic**. Domain-specific auditors may extend it with their own correctness, notation, representation, and misconception rules.

It complements, rather than replaces, a pedagogy/completeness auditor. Its central job is to prove that the source corpus has been classified, owned, linked, and reconciled without silent gaps.

---

# 1. Non-negotiable release principle
A corpus-backed learning project is complete only when all seven gates pass:

1. **SOURCE SNAPSHOT** - the source universe is frozen and identifiable.
2. **CLASSIFICATION** - every source row has one explicit disposition.
3. **OWNERSHIP** - every eligible row has one primary subtopic owner.
4. **ARTIFACT COVERAGE** - every REQUIRED row appears in the correct learning/practice artifact.
5. **SUPPORT COVERAGE** - difficult rows have the required concept/helper support.
6. **SOLUTION / ANSWER TRACEABILITY** - answers/solutions are present and verified to the level required by the project.
7. **PUBLICATION QA** - links, typography, layout, and rendered outputs remain usable.

A generated PDF is evidence of production, **not evidence of coverage**.

---

# 2. Freeze the source universe first
Before auditing subtopics, create a `source_snapshot` record.

Required fields:

```yaml
source_name:
source_type:
source_url_or_file:
snapshot_date:
source_version_or_ref:
expected_row_count:
observed_row_count:
sections:
source_access_notes:
```

Rules:
- Do not claim chapter-wide completion when `observed_row_count != expected_row_count` unless the mismatch is explicitly resolved.
- If the source is dynamic, store the snapshot date and re-audit when the source changes.
- If source rows are reordered, rely on stable source IDs/URLs/fingerprints rather than display position alone.
- Never silently substitute model knowledge for missing source content.

---

# 3. Master corpus ledger - one row per source item
Every source item gets exactly one ledger row.

## 3.1 Required identity fields
- `source_id` - stable project ID.
- `source_section` - e.g. MCQ / Numerical / Exercise / Section B.
- `source_number` - display number if present.
- `source_date_year_shift` - if applicable.
- `source_url_or_file_ref`.
- `short_fingerprint` - enough to distinguish the item without reproducing excessive source text.
- `source_status` - AVAILABLE / PARTIAL / BROKEN / FIGURE_REQUIRED / DUPLICATE_CANDIDATE.

## 3.2 Required classification fields
- `target_relevance`: CORE / HYBRID / OUT_OF_SCOPE / REVIEW.
- `primary_subtopic` - exactly one when eligible.
- `secondary_subtopics` - zero or more.
- `disposition`: REQUIRED / DEFER / EXCLUDE / REVIEW / DUPLICATE / UNCLASSIFIED.
- `disposition_reason`.
- `duplicate_of` - when applicable.
- `confidence`: HIGH / MEDIUM / LOW.

## 3.3 Required learning-link fields
- `concept_code`.
- `study_guide_artifact`.
- `study_guide_locator` - stable anchor preferred; page number is derived metadata.
- `practice_question_id`.
- `practice_artifact`.
- `practice_locator`.
- `helper_policy` - H0/H1/H2/H3 or project-specific equivalent.
- `misconception_or_failure_tag` - optional but recommended for nontrivial items.
- `solution_artifact`.
- `solution_locator`.

## 3.4 Required verification fields
- `source_link_present` Y/N.
- `concept_backlink_present` Y/N.
- `solution_present` Y/N.
- `answer_verified` Y/N/REVIEW.
- `render_verified` Y/N.
- `audit_status`: PASS / GAP / DRIFT / VERIFY.

---

# 4. Disposition taxonomy
Use the following meanings consistently.

## REQUIRED
The item materially belongs to the current target scope and must appear in the designated practice/transfer artifact.

## DEFER
The item is relevant to the wider project but its **primary engine** belongs to another subtopic. Record the destination.

## EXCLUDE
The item is outside the target scope. State a reason; never use EXCLUDE as a convenience for unresolved classification.

## REVIEW
Ownership, source integrity, figure dependence, answer reliability, or interpretation is unresolved.

## DUPLICATE
Same meaningful source fingerprint as another row. Keep traceability, but do not inflate coverage counts.

## UNCLASSIFIED
Temporary state only. Chapter/volume status cannot be COMPLETE while any rows remain UNCLASSIFIED.

---

# 5. Ownership rules

## 5.1 One-primary-owner invariant
Every eligible source item has exactly one `primary_subtopic`.

Secondary concepts may be tagged, but only the primary owner is responsible for mandatory inclusion.

## 5.2 Primary-engine test
Ask:

> Which concept or reasoning move carries most of the cognitive load of this source item?

That is the primary owner.

Do not assign ownership based on superficial vocabulary or to increase question counts.

## 5.3 Hybrid revisit rule
A question may reappear in a later mixed/capstone set only if clearly marked `HYBRID_REVISIT`. It must not be counted twice in corpus coverage.

---

# 6. Coverage accounting
For each subtopic publish:

```text
Required: X
Covered: Y
Gaps: X-Y
Review: N
Duplicates: N
Deferred: N
Excluded: N
Unclassified: N
Coverage %: Y/X
Release gate: PASS / FAIL
```

Rules:
- `Coverage %` uses only REQUIRED rows in numerator/denominator.
- DUPLICATE rows do not inflate the denominator.
- REVIEW rows are reported separately and block final release when their outcome can affect scope.
- A subtopic passes corpus coverage only when `GAP = 0` and blocking `REVIEW = 0`.

Chapter/volume status:
- **PROVISIONAL** - any gap, blocking review, or unclassified row remains.
- **LOCALLY COMPLETE** - all current subtopics pass, but source snapshot/version remains open to change.
- **COMPLETE** - source snapshot frozen, UNCLASSIFIED=0, GAP=0, blocking REVIEW=0, and all artifact QA gates pass.

---

# 7. Helper policy - general form
Difficulty support should restore the learner's model without leaking the answer.

- **H0** - no helper needed.
- **H1 Recognition cue** - tells the learner what feature to notice; no answer setup.
- **H2 Representation / concept helper** - visual, diagram, table, map, process, contrast, worked micro-example, or domain-appropriate representation.
- **H3 Structural scaffold** - provides the reasoning skeleton or ordered steps but stops before final completion.

Use the **minimum sufficient helper**.

A hard question does not automatically need three verbose text hints. H2 must genuinely change representation or reveal structure when representation is the barrier.

---

# 8. Pedagogy-support linkage audit
For every REQUIRED row of moderate or high difficulty, verify that the learner has already been taught the necessary engine.

Minimum checks:
- concept exists in Study Guide;
- concept locator resolves;
- prerequisite concepts exist;
- at least one faithful representation/helper exists when recognition is non-obvious;
- common misconception is addressed when a plausible wrong model is predictable;
- the practice question does not require machinery intentionally deferred to another subtopic.

If a question is present but the supporting concept is absent, mark `DRIFT`, not PASS.

---

# 9. Source fidelity and source-quality gate

## 9.1 Source fidelity
When paraphrasing a source item, preserve:
- all constraints;
- quantifiers such as exactly / at least / at most / only / not all;
- units and labels;
- figure dependence;
- required answer type.

Do not simplify away the mathematical/scientific/linguistic feature that determines ownership or difficulty.

## 9.2 Source issue queue
Never propagate a suspicious source solution merely because it is published.

Use `REVIEW` for:
- ambiguous wording;
- missing figure/table;
- inconsistent answer key;
- apparent typo;
- duplicated source item with altered metadata;
- solution that seems to double-count, omit a case, misuse a rule, or conflict with the source statement.

Record:
```yaml
issue_type:
source_id:
observed_problem:
impact_on_classification:
impact_on_answer:
resolution:
status:
```

---

# 10. Answer / solution traceability
For every REQUIRED row:
- final answer/response exists where promised;
- solution is reachable from the practice item;
- solution addresses the exact source constraints;
- answer format matches the source format where relevant;
- unresolved answer concerns are flagged REVIEW, never silently patched.

Domain-specific skills should add stronger correctness checks.

---

# 11. Publication and readability gate
This gate is intentionally conservative because unreadable material is uncovered material in practice.

## Typography floor
For landscape A4 student-facing material, typical targets:
- page title: 18-24 pt;
- section heading: 13-16 pt;
- body/question text: 11-12 pt;
- helper/card prose: 10.5-11.5 pt;
- solution prose: >=11 pt;
- micro-labels may be smaller when they are navigation only.

Do not reduce instructional prose below comfortable print size merely to fit content.

## Card/page density
- one dominant instructional role per card;
- avoid more than 4 dense instructional cards per landscape page;
- if text must shrink to fit, split the page;
- whitespace must be intentional breathing room or response space.

## Render QA
Before release:
- render every page;
- inspect contact sheets plus dense pages individually;
- check clipping, overflow, box collisions, broken symbols/glyphs, and accidental dead zones;
- verify all source links and cross-artifact links;
- re-render after every material layout change.

Repair order for a failing page:
1. shorten duplication;
2. restructure information;
3. enlarge/reflow the card;
4. split the page;
5. only then make minor typography adjustments within the floor.

---

# 12. Drift detection
Re-run the audit whenever:
- the source corpus changes;
- taxonomy/subtopic boundaries change;
- a practice PDF is rebuilt;
- questions move between subtopics;
- Study Guide concept codes/pages change;
- helper or solution appendices are regenerated.

Detect at least these drift classes:
- **SOURCE_DRIFT** - source count/content/version changed.
- **OWNERSHIP_DRIFT** - source row moved or now has conflicting owners.
- **LINK_DRIFT** - source or concept link broken.
- **PEDAGOGY_DRIFT** - practice requires a concept no longer taught at that point.
- **SOLUTION_DRIFT** - solution no longer matches question/version.
- **LAYOUT_DRIFT** - rebuild damaged readability or helper rendering.

---

# 13. Required audit outputs
Produce at least:

## A. Master ledger
One row per source item.

## B. Subtopic summary
Columns:
```text
Subtopic | Required | Covered | Gaps | Review | Duplicate | Coverage % | Release Gate
```

## C. Gap + Review queue
Prioritized by:
1. blocking source ambiguity;
2. clear REQUIRED gaps;
3. broken concept support;
4. broken links/solutions;
5. duplicates/metadata cleanup.

## D. Reconciliation statement
Always state:
```text
Expected source rows:
Observed source rows:
Classified:
Unclassified:
Required:
Covered:
Gaps:
Review:
Duplicates:
Excluded/Deferred:
Corpus status:
Artifact status:
```

---

# 14. Audit anti-patterns
Never:
- infer completeness from the number of questions already included;
- classify only the obvious source rows and ignore the rest;
- count duplicate rows twice;
- use a secondary concept as the primary owner to balance subtopic sizes;
- hide unresolved source issues under EXCLUDE;
- claim PASS when concept backlinks or promised solutions are missing;
- use page count as a proxy for pedagogy or coverage;
- shrink type to rescue an overcrowded page;
- silently replace source content with outside knowledge.

---

# 15. Final release checklist

```text
[ ] Source snapshot frozen
[ ] Expected = observed row count, or discrepancy resolved
[ ] Every row classified
[ ] One primary owner per eligible row
[ ] REQUIRED rows all covered
[ ] Blocking REVIEW = 0
[ ] Duplicate handling audited
[ ] Concept links resolve
[ ] Helper policy satisfied
[ ] Solutions/answers present and traceable
[ ] Source issues resolved or explicitly retained as non-release blockers
[ ] Links verified after final export
[ ] Render/readability QA passes
[ ] Reconciliation report published
```

Final status must be one of:
- `FAIL`
- `PROVISIONAL`
- `LOCALLY_COMPLETE`
- `COMPLETE`

Do not use COMPLETE unless the ledger itself proves it.
