# PR #155 — Consolidated Review

Source: [PR #155](https://github.com/reallaksh19/Common/pull/155) ("Physics: rebuild Motion B30/B80 teaching, skills and PDF schema for review"), 4 review passes, 20 inline comments, all self-authored on `2026-09-09`. This document does two things:

1. **Consolidates** the 20 inline comments + 4 review summaries into one deduplicated, prioritized list, checked against the canonical Grade 9 architecture actually present on `main` (not just against the reviews' own prose).
2. **Adds a lens the four reviews never asked for**: read as a teacher preparing students for competitive exams, where the schema's job is to find out *which specific topics* a given student is weak in and route them to material that closes exactly that gap — not just to publish a uniform book.

The second lens changes the priority order of the first list more than it adds new items: most of what "weak-topic remediation" needs turns out to already exist somewhere in the canonical `Grade 9/skills/` family and simply isn't wired into PR #155's new schema.

## 1. What's already true on `main` that the reviews under-cite

The four reviews correctly diagnose symptoms ("not discoverable," "second ontology," "difficulty is really task-type") but mostly argue from first principles. Checking against `main` directly:

- `Grade 9/install_skills.py` `SKILLS` list (lines 18–29) does **not** contain `grade9-physics-publication` or `grade9-physics-examside`. Confirmed, not just claimed.
- `Grade 9/skills/grade9/SKILL.md` (the router) never mentions either new skill, and its "Route by task" section already sends *any* "subtopic-by-subtopic Physics build... Study Guide + ExamSIDE/PYQ transfer book" to `grade9-physics-subtopic-book-builder` (see `grade9-physics/SKILL.md:120-139`). PR #155 ships a second, overlapping route for the same job.
- `Grade 9/Physics/Motion/Motion_Source_Coverage_Map.md` already defines the concept taxonomy `CB1..CB12` over `Q1..Q68` with a `SEE -> REALIZE -> UNDERSTAND` focus column per question. PR #155's `CONCEPT_REVIEW_MAP.md` introduces `PHY-MOT-DIST-01` / `PHY-MOT-DISP-01` / `PHY-MOT-VTAREA-01` / `PHY-MOT-VTDIST-01` with zero crosswalk field to `CB1`/`CB12`.
- `Grade 9/skills/grade9-concept-architect/SKILL.md` already types the canonical concept object with `prerequisites`, `same_level_question_ids`, `challenge_question_ids`, `misconception_ids`, and **`mastery_path`**. PR #155's `validate_v2.py` `Model.concepts` is `list[dict]` — open, untyped, and does not populate any of these.
- `Grade 9/skills/grade9-learning-enrichment/SKILL.md` already specifies a 4–5 level percentage-scored hint ladder (H1 ~10% ... H5 ~90%) and an explicit **"Mastery evidence"** concept: *"Hint use can reduce strength of mastery evidence... keep this as analytics metadata."* PR #155's `validate_v2.py` hard-codes exactly 3 hints (`Field(min_length=3, max_length=3)`) and records no mastery-evidence field at all.
- `Grade 9/skills/grade9-question-bank/SKILL.md` already specifies "Mixed mastery": *"Reuse validated Core questions in mixed tests that hide concept labels before the attempt. After marking, map each error back to an exact concept and recommended retake."* PR #155's `render_v2.py` paginates with a hard-coded `range(..., 2)` and no `set_id`/`study_mode`/concept-visibility metadata (matches inline finding on `render_v2.py:238`).
- `Grade 9/skills/grade9/SKILL.md` non-negotiable rule #3: *"Treat difficulty as a cognitive profile, not an Easy/Medium/Hard label."* `Grade 9/skills/grade9-physics/SKILL.md` defines a 7-dimension 0–10 difficulty vector (`physical_model_selection`, `conceptual_reasoning`, `representation_translation`, `vector_spatial_reasoning`, `equation_construction`, `experimental_data_reasoning`, `constraints_cases`) plus separately tracked algebra/arithmetic/unit-conversion burden. PR #155's `validate_v2.py` field named `difficulty` is `Literal['Apply','Explain','Connect','Transfer','Compare']` — a task-type badge wearing the difficulty field's name (matches inline finding on `validate_v2.py:57`).
- A `grade9-math-assimilation` skill already exists as a sibling of `grade9-math` — a plausible reuse target for the weak method-assimilation gate finding below, parallel to how `grade9-physics-examside` should sit under the canonical corpus/coverage auditors instead of re-owning that responsibility.

None of this makes the four reviews wrong. It means the fix in most cases is **"route to / type against the existing canonical shape,"** not **"design a new mechanism."**

## 2. Consolidated findings (deduplicated)

Severity as marked by the reviews (Blocker / Major); grouped by root cause, not by which of the 4 passes raised it.

| # | Theme | Raised | Grounding | Requested fix |
|---|---|---|---|---|
| A | **Routing/install invisible.** `grade9-physics-publication` / `grade9-physics-examside` are unreachable from `$grade9`. | 3× (`SKILL.md:14` ×2, `SKILL.md:14` again) | Confirmed: absent from `install_skills.py` and `grade9/SKILL.md`. Also overlaps `grade9-physics-subtopic-book-builder`, already routed for this exact job. | Add routing entries + install-list membership, **and** state precedence vs. `grade9-physics-subtopic-book-builder`/`grade9-publication` — or mark the new skills experimental/chapter-local in their own frontmatter. |
| B | **Second concept ontology.** `PHY-MOT-*` has no crosswalk to `CB1..CB12`/`Q1-Q68`. | 2× (`CONCEPT_REVIEW_MAP.md:7` ×2) | Confirmed against `Motion_Source_Coverage_Map.md`. `CB1` = Position/Distance/Displacement, `CB12` = graphs — so `PHY-MOT-DIST-01`/`DISP-01` → `CB1`, `PHY-MOT-VTAREA-01`/`VTDIST-01` → `CB12` is the natural mapping, as reviewers proposed. | Add `canonical_concept_id` (parent) field; also conform `concepts:list[dict]` to `grade9-concept-architect`'s typed object instead of an open dict. |
| C | **`difficulty` stores task type, not difficulty.** | Blocker | Confirmed in code (`validate_v2.py:57`). Conflicts with router rule #3 and `grade9-physics`'s difficulty vector. | Rename to `task_type`; add typed `source_difficulty` (physics vector) and derived `learner_badge` (Easy/Medium/Hard/Challenge). |
| D | **Zero-loss claim unverifiable.** `frozen_questions:int` freezes a count, not a source-obligation ledger; `check_ledger.py` proves only `expected_ids == ledger_ids`; ledger and publication JSON can each pass while drifting apart from each other. | Blocker ×2 (`validate_v2.py:68`, `check_ledger.py:8`) + reproducibility gap (`REPRODUCE.md:38`) | Confirmed: `question-contract.md` defines a rich extraction record (source hash/page, raw stem, values/units, options, dependency class, adaptation state, target IDs) that the ledger shape doesn't carry through. | Add source-obligation ledger with preservation class/status; one reconciliation command binding frozen ledger ⇄ publication model ⇄ render manifest on exact ID + concept + source-status + dependency + hint + solution + target closure, not ID-set equality alone. |
| E | **Rigid product profile.** Appendix A/B, hints, and end solutions are mandatory inside every Core book. | Major | Conflicts with `grade9/SKILL.md`: *"keep Concept Book, First-Step Reference, and Question Bank as distinct companion products,"* and `grade9-publication`'s `CORE_SOURCE`/`PRESENTATION_SOURCE`/`VALUE_ADD`/`EDITORIAL_CHANGE` separation. | Make `core_with_appendices` a selectable product profile; allow audit/self-check content to live outside the learner Core. |
| F | **Corpus/coverage re-owned.** `grade9-physics-examside` independently owns corpus freezing, concept mapping, hints, solutions, completeness. | Major | `grade9-corpus-coverage-auditor` and `grade9-transfer-coverage-auditor` already exist as the canonical engines. | Express as a Physics profile consuming the canonical coverage authority — "one denominator/ownership contract across subjects," as the reviewer put it. |
| G | **No chapter-scale batch protocol.** Two-topic pilot has no path to the 68-question chapter. | Blocker | — | Contiguous source batches, approved-page immutability, cumulative denominator reconciliation, cross-batch links, cumulative render regression, final TOC/bookmarks/global numbering. |
| H | **Figure types too narrow.** `Figure.kind` supports only `numberline\|vt\|tiles\|compare\|blank`. | Major | Confirmed against `question-contract.md`'s dependency classes: `NONE, GRAPH, DIAGRAM, TABLE, TIMELINE, NUMBER_LINE, OPTION_FIGURES, STATEMENT_SET, MIXED`. | Typed support (incl. source-image/crop) for the declared classes, or hard-route unsupported ones to the generic publication engine. |
| I | **Method-assimilation gate too weak.** | Major | Confirmed: the only check is `method != answer` plus `min_length=10` — passes near-duplicates and formula-only routes. | Reuse/port the canonical assimilation check (cf. `grade9-math-assimilation`) or add near-duplicate/terse/formula-only gates with per-question failure counters. |
| J | **No study-mode/mixed-transfer metadata; pagination hard-coded to 2/page.** | Blocker | Confirmed (`render_v2.py:238`). Directly duplicates `grade9-question-bank`'s already-specified "Mixed mastery" behavior. | Model `set_id`, `study_mode` (`ASSIMILATION`/`MIXED_TRANSFER`), concept visibility; paginate from item demand. |
| K | **SRU concept-book contract not executable.** `concepts`, `grade_scope`, `placement` are open dicts; no SEE/REALIZE/UNDERSTAND acceptance fields. | Major | Confirmed against `grade9-physics/references/concept-book-see-realize-understand.md`'s `SRU-01` ("No Naked Equation") through `SRU-09` ("Source Traceability") and beyond. | Type/validate the critical fields, or explicitly delegate pedagogical certification to the canonical SRU audit and say so in the schema doc. |
| L | **B80-L2 drops an idealisation note that B30-L4 states for the same instantaneous velocity jump.** | Physics/model-condition | `motion_B80_v2.json:147` | Retain the idealisation note (also check B80-L4's vertical jumps) or render a finite transition. |
| M | **Color-only semantic distinction (`blue return arrow` / `red arrow`) fails the review guide's own grayscale requirement.** | Publication/accessibility | `motion_B30_v2.json:210` | Make the distinction redundant via shape/label ("journey/return leg" vs. "start-to-finish displacement arrow"). |
| N | **Missing First-Step Reference product.** B30 fading + H1-H3 is not a substitute for "how do I start?" as its own product. | Raised in review #3 | `grade9/SKILL.md` and the IOQM builder's Wave 3 ("Integrated First-Step Reference": recognition atlas, decision router, first-step cards) both treat this as a distinct, required layer. | Name it as an explicit product/profile or explicit delegation, not folded into Core. |
| O | **No cold-start reproducibility reviewer role.** | 2× (`REVIEW_GUIDE.md:16`, review summaries) | — | Add the role/test: can a fresh agent, from brief + source authority + repo only, reproduce the same obligations/artifacts/audit without chat history? |

## 3. The competitive-exam-teacher lens

Read the schema as the tool a teacher uses to get students ready for a competitive exam (the repo's own `ioqm-grade9-*` skills and `grade9-physics-examside`'s ExamSIDE/PYQ framing confirm this is already the intended use case elsewhere in the repo, not a reframing being imposed from outside it). That teacher's actual job is never "publish a book" — it's:

1. find out **which specific concepts** a given student is weak in (not "which subject," not "which band");
2. put that student in front of material that closes **exactly that gap**, at the depth they need, without re-teaching what they already have;
3. verify the gap actually closed before moving on;
4. build genuine exam readiness — which means the student can solve the concept when it's *not* labeled, mixed in with others, under the representation variety a real paper uses.

Checked against that job, four things in the current schema block it — three of them are re-statements of findings above once you ask "does this support diagnosis-and-remediation," and one is new:

**3.1 Band is book-level, not concept-level (extends Finding B/E).** `Model.band: Literal['B30','B80','B90']` is one value for the *whole book*. A real student is rarely uniformly weak — they might need B30-depth support on `CB1` (distance/displacement) and be solidly B80 on `CB12` (graphs). Today the only way to serve that is to hand them two entire separate books and have a human decide which one to assign, cover to cover. The schema has no unit smaller than "book" that carries a support level. This is the single highest-leverage gap for the stated goal: **move support level onto the concept, not the book** — e.g. a per-`(cohort_or_student, concept_id)` `mastery_state` that reuses `grade9-concept-architect`'s existing `mastery_path` field, so B30-depth and B80-depth material for the *same* concept pool can be assembled per student instead of shipped as two static products.

**3.2 No diagnostic signal, no mastery evidence (extends Finding C/J).** `grade9-learning-enrichment` already defines a "Diagnostic / repair" stage and treats hint depth as mastery evidence ("a learner solving without hints or after H1 demonstrates stronger independent recognition than one requiring H4/H5... keep this as analytics metadata"). PR #155's schema has no diagnostic question type and no mastery-evidence field — the fixed 3-hint ladder (H1 Notice → H2 Model → H3 Start) records *that* a hint was shown, in the PDF, to every reader; it doesn't record *which* hint depth a specific student actually needed, so there's no data path from "student attempted this" to "student is weak here." Without this, the tool can publish material but can't detect who needs it.

**3.3 `repair_target` doesn't close the loop.** Today a wrong answer routes to exactly one lesson ID — "if wrong, re-read this." There's no retry question at the same concept, no promotion rule (repair → retry → correct → advance; retry → still wrong → escalate support), and no logged outcome. A gap-closing tool needs the loop to close, not just point back at the material that (by definition) didn't land the first time.

**3.4 Mixed/concept-hidden transfer is absent (Finding J), and this is the actual definition of exam readiness.** `grade9-question-bank`'s "Mixed mastery" section is explicit that concept-grouped practice "can leak the intended method" and that real assessment requires hiding concept labels and mapping errors back after marking. A student is not exam-ready on a concept until they can recognize it unlabeled, mixed with others, in whatever representation a real paper throws at it (`GRAPH`/`DIAGRAM`/`TABLE`/etc. — Finding H). `render_v2.py`'s hard-coded 2-per-page pagination with no `study_mode` makes this structurally impossible to build today, not just unbuilt.

**Sketch of the field additions this implies** (illustrative shape, not a final schema — for the next drafting pass to formalize):

```jsonc
// On the concept object (conform to grade9-concept-architect's typed shape):
{
  "concept_id": "PHY-MOT-DIST-01",
  "canonical_concept_id": "CB1",              // Finding B
  "mastery_path": []                           // already canonical, currently unused here
}

// On Question, replacing the misnamed `difficulty`:
{
  "task_type": "Apply",                        // was `difficulty`      — Finding C
  "source_difficulty": { "conceptual_reasoning": 6, "representation_translation": 7, "..." : "..." },
  "learner_badge": "Medium",
  "diagnostic": false,                         // true = pre-instruction weak-topic probe
  "mastery_evidence": { "hint_depth_used": null, "attempts": 0, "outcome": null },
  "set_id": "CB1-MIXED-03",                     // Finding J
  "study_mode": "MIXED_TRANSFER",
  "concept_hidden": true
}

// Closing the repair loop:
{
  "repair_target": "B30-L2",     // existing: points at the lesson
  "retry_question_id": "C-CB1-014",             // new: same-concept retry, not just re-teaching
  "on_retry_pass": "PROMOTE_TO_MIXED_TRANSFER",
  "on_retry_fail": "ESCALATE_SUPPORT_BAND"
}
```

## 4. Prioritized action plan

**P0 — blocks any reuse of this as infrastructure (do first, small/mechanical):**
- A (routing/install wiring + state precedence), C (rename `difficulty` → `task_type`, add `source_difficulty`), B (concept-ID crosswalk to `CB1..CB12`).

**P1 — blocks the weak-topic/remediation claim (the competitive-exam lens):**
- 3.1 concept-level `mastery_state` (not book-level band), 3.2 diagnostic question type + mastery-evidence field (reuse `grade9-learning-enrichment`), 3.3 repair-loop closure (retry + promotion rule), D (ledger ⇄ publication ⇄ render reconciliation).

**P2 — blocks scaling past the 2-topic pilot / blocks real competitive-readiness depth:**
- J (mixed/concept-hidden transfer sets — reuse `grade9-question-bank`'s "Mixed mastery"), I (assimilation gate), G (chapter-scale batch protocol), E (selectable product profile), H (wider figure/representation types), F (corpus-ownership consolidation onto canonical auditors).

**P3 — content-level and process fixes (independent of the above, safe to do anytime):**
- L (B80-L2/L4 idealisation note), M (B30-L2 grayscale redundancy), K (type the SRU fields or explicitly delegate), N (name the First-Step Reference product), O (cold-start reproducibility reviewer role).

Note for whoever picks this up: P0 and P1 share a root cause — both are "use the concept/mastery infrastructure that `grade9-concept-architect` and `grade9-learning-enrichment` already define, instead of the parallel simplified version this PR built." Doing P0's crosswalk and rename first makes P1's concept-level mastery state a natural extension rather than a second migration.

## 5. Status and revised plan for the remaining findings (max-reuse)

**Closed and pushed** (verified against the real pipeline, not just documented): A (routing/install), B (concept-ID crosswalk, machine-checked), C (`difficulty`→`task_type` + `source_difficulty` vector — a derived `learner_badge` was drafted and then removed, since `core-teaching.md:60` explicitly forbids inventing exam-difficulty badges without empirical calibration), L (B80-L2 idealisation note), M (B30-L2 grayscale fix, backed by an actual dashed-arrow render change).

**Still open:** D, E, F, G, H, I, J, K, N, O. Before planning these, two things surfaced by re-reading the actual canonical skill files (not just their names) materially change the P1-P3 order above:

1. `grade9-corpus-coverage-auditor` is now a **deprecated redirect** to `grade9-math-corpus-coverage-auditor` ("do not maintain a second independent set of corpus-audit rules") — it is Math/JEE-specific, not the subject-agnostic engine Finding F assumed.
2. `grade9-physics-subtopic-book-builder` — already installed and routed, unlike PR #155's two new skills — already specifies almost everything findings D, E, G, I, J and N ask for: a D1-D5 anchor-difficulty → H1-H3 support mapping, a paired `STUDY_GUIDE` + `TRANSFER_BOOK` product split (not one mandatory merged "core"), a full external/ExamSIDE audit with an exact per-question field list and a **View A / View B** reconciliation (subtopic→questions, and question→full support chain: scope → primary subtopic → concept taught → representation taught → first move taught → hints present → visual QA → solution present → source link valid → `COMPLETE`), blocking counters (`SUBTOPIC_MISSING=0`, `SUBTOPIC_DUPLICATE_PRIMARY=0`, ...), and a complete per-subtopic build sequence (§14).

So `grade9-physics-publication`/`grade9-physics-examside` did not need to invent most of this — they need to become the **typed-schema/renderer layer executing `grade9-physics-subtopic-book-builder`'s already-correct contract**, not a second, weaker pedagogy system beside it.

| Finding | Revised plan | Reuses |
|---|---|---|
| D + F | Merge into one fix: implement `check_ledger.py`'s reconciliation as View A/View B + the blocking counters, backed by `grade9-transfer-coverage-auditor` (not the deprecated corpus auditor) | subtopic-book-builder §11-13 (exact field list), `grade9-transfer-coverage-auditor` |
| E | Split `product` into `STUDY_GUIDE`/`TRANSFER_BOOK` instead of one mandatory `core` object with baked-in Appendix A/B | subtopic-book-builder's existing paired product |
| G | Subtopic-level batch protocol already exists (§14). The real gap is chapter closeout — add a new `grade9-physics-chapter-closeout-auditor` | `grade9-redox-chapter-closeout-auditor` (direct template: freeze corpus, backfill, `CHAPTER_DUPLICATE_PRIMARY_PLACEMENTS=0`) |
| I + N | New sibling skill `grade9-physics-assimilation`; its independent-audit step grounds in `grade9-physics`'s own 10-step solution structure instead of Math's algebra checks | `grade9-math-assimilation`, ported almost directly — it already targets the "~50%-knowledge weak learner," including a First-Step Reference (its step 9) that resolves N |
| J | Implement verbatim: concept-hidden mixed tests, errors routed back to concept IDs after marking | `grade9-textbook-publisher`'s existing "Learning mode vs testing mode" spec (written, just unused here) |
| K | Type `concepts`/`grade_scope`/lesson blocks against the named tests | `grade9-physics/references/concept-book-see-realize-understand.md` (`SRU-01`..) |
| O | Reuse the exact wording/test | IOQM builder's Wave 5 + "if another agent cannot continue without chat history, the handoff is incomplete" |
| H | No existing richer figure/diagram engine to delegate to (checked `grade9-textbook-publisher` — no typed figure system there either). Stays local; defer until a real multi-representation need arises from an actual chapter-scale build | — |

Aside (not a new finding, flagged for later): three different hint-numbering conventions coexist in the repo — `grade9-learning-enrichment` (H1=10%→H5=90%), `grade9-physics-subtopic-book-builder` (H1 NOTICE→H3 START), `grade9-math-assimilation` (H3 EXECUTION→H0 INDEPENDENT, reversed). Worth a unification pass outside this batch.

Suggested next sequence: **D+F → E → J → K** (schema/mechanical, same shape as the closed batch) **→ I+N → G** (two new sibling skills, larger) **→ O** (doc-only) **→ H stays deferred.**

## 6. Master-schema conformance (done, ahead of D/E/F/I/J)

A cross-cutting instruction — build this generically for any Physics topic and reusably across subjects, not just for Motion — surfaced a root cause bigger than any single finding above: `validate_v2.py`'s `Model` was never a compatible extension of `../../../shared/grade9-master.schema.json`, despite `grade9-workflow.md` S12 requiring exactly that ("generated from ... grade9-master.schema.json or a compatible extension"). It had its own incompatible field names throughout (`Question.prompt` vs the master's `question`, `source_status` vs `provenance_class`, concept `id` vs `concept_id`, a flat `questions` array vs the master's `{anchors, core_calibrated, challenges}`), and was missing objects the master schema already defines generically (`project`, `qa`, `misconceptions`, `mixed_tests`).

Fixed, and **empirically verified** — not just asserted — by validating the regenerated `motion_B30_v2.json`/`motion_B80_v2.json`/`motion_question_bank_v2.json` against `grade9-master.schema.json` directly with `jsonschema.Draft202012Validator`: **0 errors on all three.**

What changed in `validate_v2.py`/`make_motion_models.py`/`render_v2.py`:
- `Question.prompt` → `question` (matches master field name); `Question.difficulty` is now the cognitive-profile vector itself (previously misnamed `source_difficulty` after the P0 rename — see S2 finding C), matching master's deliberately-open `question.difficulty: {type: object}`.
- Added `Question.provenance_class`, kept in lockstep with the existing Physics-specific `source_status` by a model validator (`_PROVENANCE_MAP`) so the two cannot drift.
- Added top-level `Question.answer`, validated equal to `solution.answer` (mirrored, not independently authored, for the same reason).
- `concepts[].id` → `concept_id`, added required `title`, populated real `prerequisites` (VTAREA/VTDIST depend on DIST/DISP) and `misconception_ids`.
- `sources[].id` → `source_id`, added `title`/`provenance_class`.
- Added `project` (grade/subject/chapter) and `qa` (source_qc_complete/answers_verified/concept_links_verified/notes) objects — both required by the master schema, both absent before. `qa.answers_verified` is honestly `false` with a note: numeric answers are independently recomputed by `validate_v2.py`, qualitative ones are not, so a blanket `true` would overclaim.
- Added `misconceptions[]`, populated with 2 real, grounded Motion misconceptions (distance≠displacement, graph-height≠distance — both already named in `grade9-physics-subtopic-book-builder`'s own misconception list), in the exact object shape `grade9-learning-enrichment` already uses.
- `questions` restructured from a flat list into the master's `{anchors, core_calibrated, challenges}` buckets. This pilot has no external anchors and no next-level appendix, so those two are honestly empty lists (not omitted — the master schema requires the keys present); all 8 questions per book are `core_calibrated`. `render_v2.py`/`audit_v2.py`/`test_v2.py` updated to flatten the buckets where they page/paginate/mutate.
- Re-ran the full verification chain after every change: `validate_v2.py` on all 3 models, `render_v2.py` (21p/16p unchanged), `audit_v2.py` (zero broken links/overlaps/outside-page on both — one intermediate label-collision regression was caught by `audit_v2.py` itself and fixed), `test_v2.py` (13/13 negative cases, 3 boundary cases, citation fixture), and finally the direct `grade9-master.schema.json` validation above.

`Figure`/`band`/`lessons`/`handout`/`guided_solutions` remain Physics-Core-specific extensions with no master-schema equivalent (a "lesson" with a figure/caption/takeaway isn't a concept in a question-bank schema) — riding alongside the conformant core via the master schema's `additionalProperties: true`, not forced into a shape that doesn't fit. `Figure.kind` (`numberline`/`vt`/`tiles`) is still Motion-flavored; broadening it to the already-generic dependency-class vocabulary (`GRAPH`/`DIAGRAM`/`TABLE`/...) is finding H, still queued next.

---
*This document is a review consolidation only — no code or schema changes are made here. It is intended to be read alongside PR #155 by whoever drives its next revision.*
