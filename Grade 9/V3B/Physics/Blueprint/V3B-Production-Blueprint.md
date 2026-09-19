# V3B Physics production blueprint: evidence in the learner product

Apply [research freedom and minimum criteria](V3B-Research-and-Minimum-Criteria.md): investigation and provisional drafts may proceed before baseline acceptance. Strict correctness/source/answer checks govern accepted learner content; advisory scores and formatting choices do not prohibit research.

Version: 1.0.0. Status: normative authoring contract; full runtime enforcement pending.

This revision governs every new Physics topic and regenerated A/B product. It strengthens the existing six-Core contracts; it does not redesign frozen Core1/Core2 or change their source bytes. The owner’s six-Core definitions take precedence over legacy four-Core runtime names. Motion is one regression corpus, not the architecture or a privileged implementation branch.

Read with [execution and relay](V3B-Agent-Execution.md), [acceptance and regression](V3B-Acceptance-and-Regression.md), and the [machine-readable rule catalogue](V3B-Production-Rules.json). The catalogue specifies obligations; it is not an executable validator or JSON Schema.

## 1. The production sequence

1. **Establish source authority.** Preserve source files, original question numbers, every subpart, figures, options, units and conditions. Independently reconcile extracted atoms against the original. Record ambiguity and errata without silently correcting frozen questions. An author-generated inventory is provisional until checked against source evidence.
2. **Build the scientific model and learning obligation graph.** Define concepts, prerequisite edges, quantities, assumptions, representations, equations and critical reasoning transitions. A question bank alone may reveal missing prerequisites; those become derived obligations with derivation provenance, not invented source quotations.
3. **Allocate teaching and exposure across Cores.** Before accepting production prose, give each obligation a primary teaching location, each Core its necessary local support, and each example an exposure role. Plan differences in learner action, not just different headings.
4. **Author bounded subtopic units.** Work in packets of 1–3 buckets; recursively split a difficult bucket at coherent conceptual boundaries. Produce actual teaching, prompts, hints, answers and bound figures. No packet is complete because its ID count is complete.
5. **Validate content, then render.** Check mathematical/scientific assertions against the model and source. Render from accepted content objects. Extract/check the final artifacts as well: a correct source model does not prove the visible answer is correct.
6. **Review academic quality and publication quality separately.** Check reasoning depth, purpose, transfer, learner fit where applicable, figure semantics and final-size pages. Expose evidence and unresolved findings on the owner board.
7. **Authorize a versioned release.** Release requires the conjunction of applicable gates and owner authorization. NOT_RUN, STALE and UNKNOWN never count as PASS. Existing legacy test passes cannot satisfy newly introduced gates.

## 2. Scientific model and learning-unit contract

The canonical unit is a subtopic learning unit, not a page template. Store these records separately so changing a diagram cannot silently redefine the problem:

| Record | Required content | Integrity rule |
|---|---|---|
| SourceAtom | Stable ID, kind, exact value/text, unit, source locator, parent question/subpart, extraction status | Keep original and normalized representation; flag any disagreement |
| Model | Applicable domain, assumptions, quantities with scalar/vector type, units, coordinate plane/frame, sign convention, equations and variable bindings | A global direction convention cannot override a local physical plane without an explicit mapping |
| Obligation | Concept, prerequisite edges, intrinsic badge and rationale, critical inference edges, expected learner capability, required representation and falsifier | Author cannot remove an obligation to improve coverage |
| Realization | Core, obligation IDs, explanation/step/prompt/answer/figure objects, actual body, source dependencies | Object existence does not establish scientific sufficiency |
| PublicationBinding | Content ID and digest, artifact digest, section/page/object locator, exported text/figure identity | A heading or answer anchor with no body fails closure |
| Evidence | Rule ID, exact scope and input digests, evaluator/version, observations, result, reviewer where required | Stale or self-asserted evidence cannot authorize release |

For each equation, show what it says in words, each symbol's meaning and unit, conditions of use and the reasoning needed to apply it. Derive a relationship when the obligation requires derivation; otherwise identify its justified prerequisite. Distinguish a vector, its component and its magnitude consistently in prose, equations and figures. Use rendered vector arrows or consistent bold mathematical notation, not bare scalar letters whose meaning changes silently.

Coverage uses **source atom → obligation → per-Core disposition → actual object → published location**. Verify links in both directions. A disposition is REALIZED, TRANSFORMED, REFERENCE, NOT_APPLICABLE or HELD. REFERENCE cannot satisfy a mandatory local worked explanation or answer. NOT_APPLICABLE needs a reviewed rationale; it cannot excuse missing source question parts or mandatory obligations. Atom preservation is global; unnecessary full repetition in every Core is not required.

## 3. Depth and purpose are different controls

| Core | Required learner experience | Reject when |
|---|---|---|
| 1A | Detailed declarative subtopic teaching: concrete setup, representation, explained equations, critical transitions, worked reasoning and checks | Formula/result fragments or headings replace a difficult inference |
| 1B | A self-contained conceptual tutor: elicit, anticipate an answer, give contingent help, reconstruct, explain and generalize | The same worked example is merely divided into questions; no repair exists after a likely wrong answer |
| 2A | Questions at the requested demand with complete solution anatomy: interpret cues, choose model, represent, solve, explain and verify | Hints contain scattered fragments but the final solution never supplies a coherent explanation |
| 2B | Questions that require conceptual choice/application, supported attempts, alternative reasoning and transfer with complete answers/rubrics | Changed numbers or story nouns are called new transfer; the model is revealed before an attempt intended to test model choice |

Core1/Core2 remain frozen inputs. If a frozen item lacks a required drawing or sufficient support, flag it and provide a clearly separate, traceable A/B support object or erratum proposal; do not rewrite the original invisibly.

For 1A/1B use intrinsic EASY/LOW, MEDIUM or HARD buckets independently of knowledge percentage. EASY needs complete steps and purposeful visuals without enrichment search. MEDIUM/HARD require documented research contribution and decomposition where needed. Research records must explain which misconception, representation or inference the source improved; a bibliography alone is insufficient. The approximate 10/20/30-page capacities are allowances, not targets or substitutes for teaching quality.

For every difficult transition record: starting understanding, the exact inference, why a novice could miss it, an explanation/representation, a likely error, targeted repair and a check that does not simply copy the demonstration. A reviewer follows the prerequisite path as a learner would. A long passage can still fail if its decisive inference is absent. No word-count threshold certifies depth.

## 4. A complete answer system

Register **every** learner request: numbered questions, embedded predictions, diagram tasks, retries, extension tasks and reflective prompts. Preserve original source numbers as visible labels; use distinct generated IDs for new tasks. Reveal whether the task is original, adapted or author-created and link the exact source. A concept source is not proof that a generated question is an official exam question.

Each prompt and subpart needs a resolvable answer record with an actual body. Numerical tasks need the result, reasoning, conditions and a verification. Open-ended tasks need expected features, a worked/model response, acceptable alternatives and misconception repair. An instruction to draw a specific scientific diagram needs a realized model drawing plus acceptance features; a textual rubric alone does not fulfill that drawing obligation. Genuinely divergent designs can use several acceptable examples with a rubric.

Hints progress from orientation to relationship selection to execution. The final answer must remain understandable if the learner skipped hints. Reveal controls must work in the actual medium: separate answer sections/pages for print, accessible reveal interactions for digital. Plain consecutive text labeled “try first” is not an implemented reveal interaction.

Compute expected numerical/symbolic results from independent source/model inputs and compare them with the **published answer representation** using declared units, tolerances and equivalent forms. Comparing a constant with itself, or recomputing without reading the candidate answer, is not answer verification. For open-ended or diagram answers, retain explicit scientific review; a numerical oracle cannot certify them.

## 5. Purposeful reuse and distinct transfer

Maintain one exposure ledger across all selected products, including worked examples, prompts, hints, diagrams and answer sections. Each entry carries source identity, normalized givens, target, model/family, constraints, solution path, representation, learner action and prior exposures. An example seen in 1A is not unseen in 2B because its ID changed.

Classify reuse as REQUIRED_RELATION, SPACED_RETRIEVAL, RECONSTRUCTION_ANCHOR, WORKED_TO_FADED, REPRESENTATION_TRANSLATION, NEW_TRANSFER or ACCIDENTAL_DUPLICATE. Recurring equations and canonical definitions are normally legitimate when their meaning and conditions remain consistent. Intentional reuse requires an instructional reason and cannot count toward new-transfer coverage.

Compare all eligible cross-Core and within-Core objects, not a handpicked list. Exact identity and normalized problem-family matching accompany lexical screening. Initial uncalibrated screening thresholds remain five-word Jaccard 0.65 candidate / 0.80 review / 0.90 high review; directional containment ≥0.80 for passages ≥50 words. Review exact nonempty short matches too. These are review triggers, not permitted copying percentages. Do not use a low score as evidence of novelty.

For NEW_TRANSFER identify which demand changes: selecting a model, changing a constraint, reasoning inversely, coordinating representations, diagnosing an invalid model, or combining prerequisites. Explain why the previous solution cannot simply be replayed. Changed numbers, nouns, diagram colors or surface wording alone fail this claim. A different learner action can make reuse valuable, but not unseen transfer. Resolve flags against the learning purpose; record decisions and keep legitimate reuse as positive controls.

## 6. Figures generated from scientific meaning

Separate a reusable diagram **template** from its per-question **instance**. Each instance binds the model, source/task IDs, quantities, units, directions, coordinate frame, time/state and answer stage. Exact image reuse is allowed only when those bindings match or when it is explicitly a generic schematic with no conflicting values. Figures in answer sections must not leak into an attempt that assesses construction.

The renderer consumes a typed scene: vectors, points, axes, graph series, rays, forces or other approved primitives. Each vector has origin, components/direction, magnitude label and quantity type. Each graph has variable/unit labels, scale, domain, data/model function and relevant piecewise intervals. Validate geometry against model values, including orientation, arrowhead, subtraction construction, endpoint and axis alignment. A generic arrow diagram cannot validate an arbitrary numerical instance.

Declare QUANTITATIVE or SCHEMATIC. Quantitative diagrams use a consistent relevant scale; schematics are visibly labeled “not to scale” and still preserve qualitative direction, topology and physical relationships. A label cannot excuse a wrong sign or wrong graph trend. Bind the final rendered asset digest to the scene and publication location, then visually inspect it. An SVG that parses can still teach incorrect physics.

## 7. Layout as a publication contract

Declare the intended medium and final page/viewport dimensions before composition. Choose and record a style profile for text measure, margins, math size, diagram labels, answer separation and pagination. Evaluate both outer page margins and empty space **inside** illustration view boxes; adjusting page margins cannot fix a mostly empty SVG.

The publisher must report page size, occupied text/figure bounds, overflow/clipping, smallest labels, unused diagram canvas and broken page relationships. These metrics trigger inspection; maximizing occupied area is not the goal. Preserve writing space where it serves an explicit student task. Do not shrink text to fill a page or inflate examples to reach a page count.

Inspect final-size pages covering every template and diagram family, every flagged outlier, dense equations, long solutions and answer transitions. Record page-specific findings. Markdown alone cannot establish PDF margin quality. No committed final PDF/HTML means publication review is NOT_RUN. Re-rendering invalidates visual receipts for changed pages and their dependent layout.

## 8. Fit, badges and visible engineering

Only 2A/2B require a scoped knowledge percentage with evidence/date or an explicit owner waiver. Record purpose separately: starter, practice, revision or competition. Unknown knowledge plus a waiver is OWNER_ROUTED_NOT_KNOWLEDGE_VALIDATED. Without either, produce at most a labeled design preview and keep learner-fit acceptance blocked.

Use a prerequisite/subtopic skill profile where available; a single aggregate percentage cannot determine every question's demand. Map item prerequisite demands, inference depth, representation burden, support and transfer demand to the learner profile using a versioned policy. Include a rationale and uncertainty. Validate predictions using independent attempts, error types, hint use and delayed/transfer performance when available. Pre-use design review is predicted fit, not measured learning. Do not relabel hard concepts as easy to fit a score.

Learner badges should help navigation: bucket/subtopic, intrinsic difficulty or question demand explicitly distinguished, purpose, prerequisite/help link, representation, source and optional estimated effort. Defer concept/model badges until reveal when recognition is assessed. Keep source digests, gate IDs and reviewer receipts in the owner view.

The owner board must show, per bucket and product: scope/baseline version; missing prerequisites; source reconciliation; academic depth; Core differentiation; answer/figure correctness; reuse decisions; learner fit; publication inspection; release status. Each status links evidence and the next blocking action. Never compress all columns into one “passed” count.

## 9. Scope growth and release discipline

Start a new topic by selecting reusable scientific gates and proposing missing ones **before authoring**. Gates define obligations and failure conditions; topic bindings supply actual concepts and values. Do not encode topic names or individual question IDs into universal production logic.

An extension declares its parent baseline, added/changed subtopics, depth/exam-scope impact, prerequisite closure and intended products. Verify that a claimed addition is actually absent from the parent. Create a successor baseline; preserve the old one. Invalidate affected teaching, example exposures, questions, figures, answers, calibration and publication evidence transitively. Unaffected evidence may survive only with compatible dependency digests.

A research-level bucket needs a distinct depth profile, mathematical prerequisites, research sources, uncertainty/model limits and qualified review. Owner research ambition does not silently expand the student's exam syllabus or confer reviewer expertise. Missing prerequisites remain visible; bridge them or hold that branch.

See the acceptance document for implementation boundaries. This blueprint changes required authoring behavior and acceptance design. It does not claim that the current four-Core runtime, engineering proof checker, or an unreviewed agent now enforces these contracts automatically.
