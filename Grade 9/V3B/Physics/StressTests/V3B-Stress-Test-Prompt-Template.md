# Reusable subtopic production stress-test prompt — V3B

Use: edit the configuration below, then give this entire file to the production agent. For a prepared invocation, use [the Grade 9 relative-motion example](V3B-Motion-Grade9-Example.md). The same structure can be used for Mathematics or Chemistry once their subject adapter and accepted contracts are identified. This is a production task, not a request to describe how production might work.

This prompt does not invoke obsolete PR-delivery or Grade 9 workflow skills. Follow the owner's current instructions. Do not merge or modify V2. The architecture and library proposals linked below are design guidance, not executable interfaces.

## 1. Editable owner configuration

```yaml
request_id: STRESS-<subject>-<subtopic>-<date>
repository: reallaksh19/Common
architecture_pr: 364
architecture_basis: VERIFY_LIVE_HEAD_AND_RECORD
subject: Physics
topic: <parent topic>
subtopics: [<one primary subtopic>, <optional related subtopic>]
grade: 9
board: CBSE
academic_year: 2026-27
curriculum_track: <STANDARD | ADVANCED | OWNER_DEFINED>
language: English
scope_mode: BOARD_PLUS_LABELLED_EXTENSION
included: [<specific capabilities / question families>]
excluded: [<topics / mathematics / models not requested>]
depth_overlay: <FOUNDATION | EXAM | ADVANCED | RESEARCH>
research_question: <required only for a RESEARCH overlay>
intrinsic_badges: {<subtopic>: HARD}  # EASY / MEDIUM / HARD, with reasons
products: [CORE1, CORE2, CORE1A, CORE1B, CORE2A, CORE2B]
practice_purpose: <SIMPLEST_FOUNDATION | BOARD_PRACTICE | COMPETITIVE_PREPARATION>
knowledge:
  percentage: null
  provenance: UNKNOWN  # DIAGNOSTIC / OWNER_ESTIMATE / SYNTHETIC_TEST / UNKNOWN
  scope: <capabilities to which the percentage actually refers>
  evidence_files: []
owner_waiver:
  enabled: false
  instruction: <when enabled, state requested demand and help; never invent mastery>
sources:
  frozen_core1: []
  frozen_core2: []
  local_references: []
  preferred_web_sources: []  # Starting points, not an allowlist
  corpus_mode: <FROZEN_SUPPLIED | BUILD_REVIEW_CORPUS>
  acquisition_allowed: true
question_targets:
  core2a: 8
  core2b: 6
  count_policy: EDITABLE_TARGET_REPORT_SOURCE_OR_PURPOSE_GAPS
delivery:
  output_root: <isolated path ending in V3B/run-id>
  formats: [HTML, PDF, STRUCTURED_SOURCE]
  audience: SELF_STUDY
  manuscript_status: REVIEW_DRAFT
stress:
  profiles: [LOW_SCOPED_EVIDENCE, HIGH_SCOPED_EVIDENCE, UNKNOWN_WITH_WAIVER]
  one_extension: <additional bucket or deeper version of existing bucket>
  cold_agent_resume: true
  run_corruption_checks: true
```

Question counts are editable production targets, not universal quality thresholds. A missing percentage plus no waiver holds personalized Core2A/2B acceptance, not Core1A/1B research. Ask only about a material unresolved owner choice; complete independent work first. Do not silently switch curriculum track or expand scope to fill a count.

## 2. Establish the actual production path

Read the live V3B [production blueprint](../Blueprint/V3B-Production-Blueprint.md), [research policy](../Blueprint/V3B-Research-and-Minimum-Criteria.md), [Core contracts](../Engineering/CORE_CONTRACTS.md), [packet contract](../Engineering/PACKET_CONTRACT.md), [runtime map](../ProductionKit/V3B-Runtime-Map.md) and [publication input](../ProductionKit/V3B-Publication-Input.md). Record the commit and implementation capabilities actually used. Compare useful parent-PR changes only where relevant; do not silently replace V3B with a different architecture.

Core0, if present, is routing infrastructure. The requested learner products remain six. A newer parent calling its architecture “seven-core” does not authorize a seventh learner book. The current V3B publisher composes A/B drafts; it does not autonomously author all six products or grant learner release.

Produce a short owner board before the books: exact scope/year/track, available source corpus, known prerequisites, current engineering checks, products requested, implementation gaps and intended output paths. Start research with a provisional outline; a complete accepted baseline is not a prerequisite for exploration.

## 3. Ground, decompose and research

Inventory source concepts, equations, values, conditions, diagrams, examples, questions, original identifiers and answer availability. Preserve the original plus any separately justified correction. Distinguish UNKNOWN coverage from a searched, scope-bounded VERIFIED_ABSENT result. A failed download is not evidence of absence.

For each subtopic, write a usable microtopic graph: what the student can initially do, the exact inference to learn, prerequisites, equation meaning/conditions, representation, misconception/repair and an observable exit task. Split at a change of model, frame, relation, representation or difficult inference; stop when the unit is a meaningful teachable transition. Do not split merely to increase node counts. Bundles contain 1–3 subtopics; each may contain many microtopics.

Research Medium/Hard Core1A/1B to improve the teaching, not merely to attach citations. Keep the source location, what it contributes, conflicts/limitations and a reason for choosing the representation. Easy follows the owner's no-enrichment-search rule. Preferred sources may be replaced when access, quality or fit is poor; record the reason. A research overlay requires an explicit question, model boundaries, higher prerequisites and unresolved claims, not just longer prose.

For BUILD_REVIEW_CORPUS, acquire traceable questions within authorized scope and freeze a run snapshot for reproducibility. This snapshot is not an owner-approved frozen Core2 corpus. Mark Core2 and dependent products as candidates until their required source/acceptance basis exists. Authored questions may supplement allowed practice, with local IDs and truthful AUTHORED provenance; never invent an official exam/year/question number. An inaccessible required source remains an identified gap.

## 4. Build the six products with distinct learner purposes

| Product | Required experience |
|---|---|
| Core1 | Existing compact basic notes/semantic orientation. Instantiate or reference the valid upstream product; preserve already frozen material. |
| Core2 | Existing source questions and ladder hints, source identity and answers. Preserve supplied frozen wording and figures. |
| Core1A | Detailed declarative teaching by intrinsic subtopic badge: construct the concept, bridge picture → words → symbols, justify difficult steps and provide completed examples. |
| Core1B | A self-tutor for concept reconstruction: predict, explain, draw, discriminate, test a boundary, then inspect model responses and repair misconceptions. |
| Core2A | Purpose- and knowledge/waiver-adjusted practice with complete expert solution breakdowns, meaningful figures, guides and checks. Simplest questions are valid when the owner asks. |
| Core2B | Supported application and transfer: require model choice, representation or reasoning, with graduated help, full answers/rubrics and repair routes. Explain the change in demand from prior exposure. |

Core1A/1B depth must not shrink when knowledge percentage increases. Hard/Medium/Easy may need roughly up to 30/20/10 pages per subtopic as owner depth allowances; these are neither quotas nor mandatory maxima. Use the length required for clear teaching and explain large deviations. Every embedded question, diagram-completion task and “think about” prompt needs a model answer, rubric or explicit guide to judging the response. B must work without a live tutor; “discuss with your teacher” is insufficient closure.

Do not turn B into A with nouns changed or random blanks. A legitimate shared anchor may recur, but its new learner action and help/reveal state must be visible. Repeated equations need not be paraphrased to defeat similarity checks.

## 5. Demonstrate fit and differentiation

Use the same fixed intrinsic study-bucket contract across the selected practice profiles. For low/high scoped evidence, record which capabilities are supported and missing; do not infer all prerequisites from an aggregate percentage. Synthetic profiles are test inputs, not observed students. For unknown-with-waiver, retain UNKNOWN and follow the owner's requested demand/support without claiming measured fit.

Show a compact comparison of question selection, support, novelty, prerequisite bridges and expected learner actions. For efficiency, reuse unchanged study artifacts and produce profile-specific practice slices; one coherent full baseline set is still required. A high percentage with one missing critical prerequisite must trigger a bridge or scoped hold. An owner request for easier questions must remain effective even for a high estimate.

Audit all actual examples, questions and figures across products using identity, normalized text, solution structure, model assumptions, representation and prior exposure. Use the current versioned similarity policy. Its 5-word-shingle Jaccard triggers (0.65 candidate, 0.80 review, 0.90 high review) and containment trigger (0.80 with a 50-word minimum) are uncalibrated review aids, not a universal pass mark. Low similarity is not proof of transfer. For every flagged pair record purpose, changed demand, learner action and disposition. Do not claim these scores were computed if the available tool only checks source/family identity.

## 6. Scientific figures and final layout

Create exact diagrams with a quantitative drawing/plotting tool where geometry matters. For vectors specify frame, axes, direction, tail/head, units, scale and equation bindings; distinguish vector from magnitude. Graphs need variable names, units, domains and meaningful scales. A figure template may be reused; an incompatible instance may not.

Inspect exported final-size pages, not only source code or standalone images. Check equations, arrowheads, label size, figure-to-working adjacency, clipping, broken page flow and unused left/right space. Keep justified response space and readable line lengths. Record measured margins and the worst offending pages; do not use page occupancy alone as a quality score. PDFs need actual PDF inspection. If a browser/renderer is unavailable, deliver the editable draft, state what is uninspected and keep publication acceptance pending.

## 7. Stress the system, including positive controls

Run these on isolated copies; never corrupt the accepted source or soften an oracle to obtain a pass. Use the real available validators/review workflow. If no detector exists, report the gap rather than writing a test that merely echoes this table.

| Probe | Expected observation |
|---|---|
| Remove a required inference while leaving its heading/ID | Coverage/content review identifies the missing teaching. |
| Delete an answer or retain only its anchor | Actual output closure fails. |
| Reverse a vector; swap a plausible but incompatible diagram | Scientific/instance checks or review identify the mismatch. |
| Change a frozen value, condition, option or question number | Source-custody acceptance fails. |
| Rename a worked example and call it unseen transfer | Exposure/semantic review disputes the claim. |
| Reuse a necessary equation with a different valid teaching purpose | No automatic rejection solely for similarity. |
| Rearrange an equation with recorded source, steps and conditions | Review draft permitted; semantic approval not fabricated. |
| Use an unsupported evaluator | Clearly unverified review draft permitted; no numerical PASS. |
| Provide complete help with one hint or no separate hints | No fixed-three-hints rejection; substantive help remains reviewable. |
| Remove knowledge and owner waiver | Personalized practice acceptance held; study work continues. |
| Give high aggregate knowledge but missing critical prerequisite | Practice route does not assert prerequisite mastery. |
| Reuse a source after it changes or an old packet after an extension | Affected acceptance becomes stale; unrelated content can remain reusable. |
| Introduce optional extra research or a harmless wording change | No blanket global research stop. |
| Widen margins or shrink labels severely | Final-medium review records the usability failure. |
| Request an extension outside the declared syllabus | Label it, record new prerequisites and keep it outside board claims. |

Report two independent outcomes: **architecture behaviour** and **learner-product quality**. Correctly holding missing evidence may pass a particular negative probe while leaving the requested books incomplete. “Everything held safely” is not a successful full production stress test.

## 8. Recovery and one extension

Package sources or accessible exact references, content, figures, accepted/candidate state, policies, input versions, evidence, unresolved issues and the next action. A second agent should resume one chosen bucket from that package without this chat. Independent review must use a separate instance and inspect originals; a reused specialist profile is fine, self-review is not independent evidence. If no second agent is available, mark cold-agent recovery NOT_RUN and do a separate process rebuild only if possible.

Then add the configured extension. Show new prerequisites, affected consumers and retained artifacts. Do not rebuild unrelated pages merely because a new bucket exists. Do not reuse acceptance for changed science, scope or figures. If automated invalidation is unavailable, provide the exact manual impact list and name the missing implementation.

## 9. Required handback

Deliver actual learner artifacts plus editable sources, the owner board, source/answer/coverage index, research contributions, microtopic map, cross-Core exposure decisions, profile comparison, extension impact, executed stress results and a restart packet. The documentation may share files; no artificial file-count target.

For every product state: produced / candidate / held / not run; exact paths; source and scope basis; academic/visual review status; remaining limitation. Include a short record of difficult teaching decisions with evidence. Do not claim universal topic support, independent review, empirical mastery or publication readiness from metadata or successful rendering alone. Preserve V2 and existing frozen products. No merge.
