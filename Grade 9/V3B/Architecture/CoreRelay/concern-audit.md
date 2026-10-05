# Audit of all 50 original concerns

Status: ARCHITECTURE ASSESSMENT, not implementation acceptance.

The [original checklist](inputs/original-concerns.md) marks every concern addressed and calls the remainder mainly implementation detail. This review does not accept those completion claims. The mechanisms are useful proposals, but several unresolved issues are architectural: bidirectional claim review, actual receipt meaning, packet sufficiency, learner-relative decomposition, and profile eligibility.

Numbering C01–C50 follows the exact original row order. Concern descriptions below are shortened; the original text is preserved unchanged. RETAIN means retain the proposed principle; REFINE means add a missing contract; REVISE means the original statement needs a substantive qualification; OWNER CLARIFICATION means the owner's later instruction controls. No row implies the current PRs implement or pass it.

| ID | Original concern | Original response | Assessment and required evidence |
|---|---|---|---|
| C01 | Fresh agent cannot reliably decompose difficult material | Assimilation compiler stages | REFINE: stages expose work but cannot guarantee expertise. Require difficult-connection identification, actual explanation and held-out topic evaluation. See pedagogy and E01. |
| C02 | Formula known but reasoning skipped | IC and EA packets | RETAIN + test: every nontrivial edge needs a valid rule, condition and meaning; complete-looking lines can still hide a jump. See packets, E02. |
| C03 | Wrong representation chosen | RR/RC/RD flow | REFINE: record cognitive need, alternatives, reading prerequisites and outcome in actual artifact. Selection scores alone are insufficient. E03. |
| C04 | What to notice before mathematics | notice_before_math field | RETAIN: connect this to a visible relation and explanation; a generic sentence does not satisfy it. Physics P-A2, E03. |
| C05 | Misleading figures | must_not_imply/risk fields | REFINE: inspect the rendered figure against these risks. A textual warning cannot repair a contradictory arrow. E03 and E16. |
| C06 | Vague teaching atom | Split at conceptual boundaries | REVISE: boundary changes suggest a split; not every notation change needs an atom. Require an identifiable learning transition. Pedagogy, E01. |
| C07 | No decomposition stopping rule | At most one permissible move | REVISE: useful learner-relative heuristic, not a deterministic proof of minimality. Review prerequisite knowledge and whole-concept reconstruction. E01. |
| C08 | Unknown syllabus | Adaptive Core0 routing | RETAIN: question-derived scope stays provisional and bounded. Neither question count nor confidence supplies a missing syllabus. E04. |
| C09 | Sparse questions encourage invented exam patterns | Thin/zero evidence packets | RETAIN: separate absence states from generated teaching; forbid unsupported prevalence claims. E04 and E05. |
| C10 | Zero questions leads to concept omission | Semantic importance controls teaching | RETAIN: shared scope ledger must dispatch zero-question prerequisites. Existing zero-primary policies require later explicit migration. E05. |
| C11 | Blind dependence between Cores | Shared original ground truth | REFINE: provide actual resolvable originals, including figures/options, not just the predecessor's selected summary. E06. |
| C12 | Downstream validation of upstream | Blind pass then claim comparison | REFINE: seal initial analysis and track exposure; second-role additions still need independent review. Architecture convergence; E06/E07. |
| C13 | Same instance self-certifies | Profile versus instance separation | RETAIN: fresh instance at validation boundaries; same-model independence still limited. Relay matrix, E06. |
| C14 | Who chooses reuse/profile | Deterministic Governor | REFINE: eligibility, ranking and evidence of competence are different. Record reasons and lack of calibration. E11. |
| C15 | Core0 becomes appropriate first Core | One-time transformation | RETAIN: neutral normalization may continue once; substantive claims are still subject to fresh review. Agent lifecycle. |
| C16 | Core2-first route | Inferred demands then fresh Core1 | REFINE: infer assessed slice provisionally; Core1 expands supported semantics without claiming complete syllabus. E04. |
| C17 | Core1-first route | Semantics then fresh Core2 | RETAIN: second role may report no assessment evidence while valid teaching continues. E05. |
| C18 | Placement of 1A/2A | Join before 1A; receipts before 2A | RETAIN: local dependency-cleared barriers; speculative drafts may exist but cannot be accepted early. E07/E08. |
| C19 | Core2 profile becomes Core1A | Assessment-strong fresh 1A | REVISE: assessment strength never waives subject and assimilation competence. Select only eligible profiles. E11. |
| C20 | Core1 profile becomes Core1A | Semantic-strong fresh 1A | REFINE: semantic strength also does not establish teaching skill. Require assimilation eligibility. E11. |
| C21 | Core1A becomes Core2A | Fresh assessment/transfer profile | REFINE: fresh instance mandatory; profile reuse is eligibility-based, with independent question/solution checks. Relay matrix, E14. |
| C22 | Why Core2A downstream | Depends on actual teaching | OWNER CLARIFICATION: receipts describe material support, not measured mastery. Verify exact artifact; permit explicit diagnostic/stretch exceptions. E08. |
| C23 | Reuse Core2 intelligence | Transfer envelope | RETAIN: preserve recognition, wrong chains, valid routes and conditions, not just a family label. E09. |
| C24 | Small typed handoffs | Many packet families | REFINE: related records may share a bundle; do not create an agent or file per field. Measure intellectual sufficiency and coordination cost. E06/E19. |
| C25 | References instead of long duplicated context | Stable IDs and selective lookup | REFINE: inline decisive reasoning/risks and ensure references resolve to originals. Selective retrieval must not conceal scope. E06/E10. |
| C26 | Provenance and confidence | Universal envelope | REFINE: separate origin, derivation, review and uncertainty. Agreement is not calibrated correctness. E10/E11. |
| C27 | Evidence absence explicit | Zero/thin/unknown/blocked states | RETAIN: each gap states which conclusions and operations it affects. Teaching can proceed within authorized evidence bounds. E04/E05. |
| C28 | Conflict handling | Join preserves disputes and quarantine | REFINE: preserve both claims and original keys; require scoped disposition, dependency impact and re-review. E07/E14. |
| C29 | Universal owner override | HARD/SOFT OVR | RETAIN: scope, effective version, finding, decision and final action must all persist. E12. |
| C30 | Override must not falsify truth | Finding + decision + action | RETAIN: distinguish operation from factual validation; do not relabel a disputed key confirmed. E12/E14. |
| C31 | Knowledge percentage central | Capability-expanded learner context | OWNER CLARIFICATION: retain percentage as an input; it does not decide the owner's practice requirement. E13. |
| C32 | Percentage changes pedagogy | Scaffolding/jump/fading variation | REVISE: vary support based on explicit capability assumptions and owner needs; no universal 20/50/80 rules established. E13. |
| C33 | Purpose central | First study/revision/competitive | OWNER CLARIFICATION: include elementary practice, targeted repair and flexible support/mix; the three labels are not exhaustive. E13. |
| C34 | Competitive purpose skips foundations | Prerequisite closure | RETAIN: scaffold the route while preserving the destination; distinguish supported exposure from independent readiness. Physics case, E13. |
| C35 | Same subtopic different treatment | Purpose-dependent plan/profile | RETAIN: reuse unchanged semantics but rebuild affected teaching/practice choices and bindings. E13/E17. |
| C36 | Difficulty not one label | Multidimensional demand | RETAIN: preserve specific conceptual, representational, constraint and algebraic demands; avoid uncalibrated scalar rankings. E09. |
| C37 | Readiness differs from difficulty | Intrinsic/assessment/relative difficulty | RETAIN: also separate support level and owner destination. Pedagogy, E13. |
| C38 | Question-writer intelligence | Cues, first move, wrong chains | RETAIN: walkthroughs must show these survive into actual hints/solutions. E09. |
| C39 | H1/H2/H3 not free-text evidence | Typed dependencies validated by T | REFINE: typed references are necessary but the cited explanation must actually support the hint operation. E08/E09. |
| C40 | Govern transfer beyond random creativity | Safe/conditional/forbidden axes | REFINE: independently solve each new item; combinations can be novel while semantic scope stays supported. E09/E14. |
| C41 | Generated versus observed practice | Provenance labels | REFINE: separate item origin from family basis. A new family-derived item remains new, never an observed PYQ. E05/E14. |
| C42 | Subtopic handoff max three | 1–3 subtopics | RETAIN as owner transport bound; not a researched optimal cognitive chunk. Preserve all external prerequisite refs. E15. |
| C43 | Different profiles within a bundle | Re-shard after Join | RETAIN: stable subtopic/capability IDs, explicit migration and dependency closure. E15. |
| C44 | Subtopic too large | Subtopic versus atom | REFINE: allow same-subtopic sequential segments and checkpointed continuation; atom count is not quality. E01/E15. |
| C45 | Missing prerequisites discovered | Governor inserts new bundles | REFINE: identify canonical home, cycle/order constraints and affected dependents; preserve unaffected work. E15/E17. |
| C46 | Deterministic routing | Governor input factors | REVISE: deterministic control rules are possible; content uncertainty and expert judgment remain. No invented calibrated thresholds. E11. |
| C47 | Agent chooses itself/successor | Governor-only selection | RETAIN: worker recommendations cannot write the authoritative assignment; log decision authority. E11. |
| C48 | Account for agent reliability | Confirmation/refinement/rejection rates | REVISE: use held-out task quality, error severity, exposure, sample size and assignment mix. Raw agreement can reward shared errors. E11/E19. |
| C49 | Machine QA beyond shape | Semantic/topological validators | REFINE: distinguish decidable structural checks, reproducible domain checks and substantive judgment. Exact evidence must support each claimed gate. Evaluation layers. |
| C50 | Existing tests check containers over depth | Falsifier tests | REVISE: do not generalize about all three suites without a full audit. Preserve useful existing invariants; add outcome-based pedagogical evaluation. PR evidence and E19. |

## Later owner corrections and additional architectural requirements

| ID | Source/status | Required treatment |
|---|---|---|
| C51 | Later owner: architecture first | Subject PRs provide pinned architecture context; line-by-line code reviews remain a separate phase. |
| C52 | Later owner: Core1A assimilation | Real explanations, pictures, examples and equation simplification must be demonstrated in material, not merely enumerated in schema. |
| C53 | Later owner: Core2A need chosen by owner | Practice brief independently controls destination, difficulty/support and selection; knowledge percentage cannot substitute. |
| C54 | Later owner: packet relay crucial | Audit producer-to-consumer sufficiency, source access, dependency preservation and loss during reshards. |
| C55 | Later owner: reuse/new agent critical | Treat profile reuse, instance continuation and artifact reuse separately; evaluate costs and error propagation. |
| C56 | Review recommendation | Add global syllabus/scope reconciliation above local bundles so undispatched subtopics cannot disappear. |
| C57 | Review recommendation | Define retry, stale-version invalidation and single canonical acceptance for duplicate attempts. |
| C58 | Review recommendation | Separate content receipts from learner mastery and independent-task inclusion from actual learner performance. |
| C59 | Review recommendation | Distinguish source integrity inventory from the owner's selected worksheet contents. |
| C60 | Latest owner authorization | Accumulate research/design details in a draft PR; no merge or production migration implied. |

## Overall disposition

The concern set is captured and mapped to proposed contracts and falsifiers. It is not closed as implemented or pedagogically validated. Exact routing calibration, packet sufficiency under cold execution, independent review effectiveness and learner suitability remain evaluation questions. See [decisions](decisions.md) and [acceptance/evaluation](acceptance-and-evaluation.md).
