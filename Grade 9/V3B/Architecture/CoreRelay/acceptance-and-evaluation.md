# Acceptance layers and evaluation design

Status: PROPOSED SCENARIOS, NOT EXECUTED. The documentation checks actually performed are recorded separately in validation.md. This file does not report runtime tests, multi-agent experiments, human review or learner outcomes.

## Evidence layers

| Layer | Suitable checks | What passing cannot establish |
|---|---|---|
| Structural and custody | Required fields, enums, reference resolution, exact versions, dependency closure, bundle size, single acceptance and source inventory accounting | Scientific truth, teaching sufficiency or learner understanding |
| Reproducible domain checks | Algebraic equivalence under domain assumptions, dimensions, numerical solutions, atom/charge accounting where applicable, independent answer reconstruction | Suitability of explanation or all conceptual edge cases |
| Subject/content review | Valid assumptions, completeness of reasoning, correct causal/model account, alternate routes, transfer constraints and ambiguity | Measured learner assimilation |
| Pedagogical review | Intended conceptual change, suitable granularity, reading prerequisites, representation function, misconception repair and recomposition | Guaranteed effectiveness for all children |
| Rendered artifact review | Actual diagram/prose/notation, reading order, caption, legibility, hint/solution placement and locator integrity | Correct hidden source assumptions without content review |
| Owner product-fit review | Requested scope, level, support, provenance policy and deliverable mix | Factual correctness by preference |
| Learner evidence, if separately authorized | Understanding, explanation, near/far transfer, retention and usability with appropriate design | Generalization beyond the tested learners/tasks |

Machine validators should state the predicate they evaluated. A language-model judgment is a model-based review result, not a deterministic proof because it returns a boolean.

## Falsifier scenarios

| ID | Setup / injected defect | Expected behavior and reviewable evidence |
|---|---|---|
| E01 | Complex equation has ten listed atoms but hides a sign/frame decision; alternatively a simple relation is split into many meaningless fragments | IC exposes the hidden decision; the plan adds or consolidates meaningful transitions; reviewer explains adequacy and checks whole-concept reconstruction |
| E02 | Every derivation line is present, but one uses an unstated condition or divides by a possibly zero quantity | Reject or qualify the edge; preserve lost solutions/domain condition; dependent explanation and answer rechecked |
| E03 | A visually attractive apex diagram omits acceleration or compares velocity/acceleration arrow lengths as if same units | RD/visual review identifies the exact false implication; actual artwork and explanation corrected |
| E04 | No syllabus; two ambiguous questions and an absent figure | Record scope/evidence gap, no invented complete syllabus or exam pattern; continue only a defensible authorized slice or request necessary source |
| E05 | Clear syllabus contains a prerequisite with zero questions | Include semantic teaching obligation; Core2 records no observed assessment evidence; generated practice clearly new and not frequency-backed |
| E06 | Upstream packet contains a plausible wrong answer; fresh receiver is given originals separately | Seal a source-only analysis before exposure, then produce claim-level disposition with independent reasoning; exposure contamination invalidates the blind label |
| E07 | Second Core introduces a new law/condition that first Core never reviewed | Join holds impacted obligations until a fresh competent reviewer resolves the new claim; unaffected obligations can proceed |
| E08 | T says pre-taught but only a heading/plan exists, or an H2 needs an unexplained operation | Core2A ordinary support check fails; add realized teaching and review or use explicit permitted diagnostic/stretch mode; no mastery claim |
| E09 | New problem uses the same family label but introduces a new representation, hidden constraint or unsafe transfer axis | Recompute actual demands and solution; require named conditional support or reject; preserve useful D intelligence |
| E10 | A crucial source crop is inaccessible, original options lost, or an accepted ref silently moves to a new version | Emit G; block affected claim; repair source binding and invalidate descendants instead of trusting ID presence |
| E11 | Assessment-strong profile lacks subject pedagogy; raw agreement score favors it | Eligibility excludes or marks competence unverified; Governor records evidence basis and selects only under explicit supported policy |
| E12 | Owner requests elementary output, a deferred prerequisite, or use of a disputed key | Preserve system finding + owner decision + final action; honor product choice without falsifying factual status or hiding consequence |
| E13 | 80% knowledge + elementary goal; 20% knowledge + competitive goal; same goal with differing capability assumptions | Goal survives unchanged; support changes explicitly where appropriate; no percentage-derived override or invented capability diagnosis |
| E14 | New item ambiguously admits two answers, key conflicts, or a generated item is labelled as an observed exam question | Independent solution/ambiguity review corrects or quarantines; provenance corrected; original key/source preserved |
| E15 | Three-subtopic bundle splits and one shared prerequisite is hosted elsewhere; a fourth prerequisite is discovered | Stable IDs/edges preserved; new task respects bound; blocked dependents held; accepted unaffected content reused; cycles surfaced |
| E16 | Accepted teaching text survives but diagram/notation/rendering changes | Revalidate actual artifact and rebind T; an old hash/locator cannot certify the new representation |
| E17 | Owner brief or semantic assumption changes after X generation | Recompute affected dependency closure; preserve unrelated K/D; reject stale acceptance and assemble only a coherent manifest |
| E18 | Worker crashes after writing output; duplicate attempts finish; old worker returns after custody changes | Durable state resumes correctly; one canonical acceptance per version; obsolete epoch cannot accept; rejected outputs remain auditable |
| E19 | Compare same-instance continuation, fresh-role packet relay and full-context baseline on unseen subtopics | Report correctness, preserved reasoning, seeded-error detection, teaching quality, goal fidelity, cost/latency and rework using comparable budgets |
| E20 | All dispatched bundles pass, but a syllabus item was never dispatched | Global scope reconciliation catches missing required item and blocks a claim of complete authorized coverage |
| E21 | Chemistry balancing diagram presents a particle-count equation as an actual simultaneous collision mechanism | Subject review rejects unsupported mechanism; clarify representational scope; invalidate dependent causal claims |
| E22 | Mathematics root-to-factor path cancels a potentially zero factor | Review preserves the excluded case and complete solution set; formula shape alone cannot pass |
| E23 | New competitive question combines already supported ideas without copying a worked example | Allow after demand/solution review if semantic scope and owner brief fit; do not require pre-teaching the exact held-out answer |
| E24 | Finite budget is exhausted with unresolved critical disagreement | Preserve uncertainty and restrict/block affected output; no confidence inflation, repeated self-agreement or unbounded retry |

These scenarios are acceptance targets for a future implementation/evaluation. A prose walkthrough illustrates expected behavior but does not count as executing any scenario.

## Packet and agent evaluation

Use representative subtopics with meaningful contrasts:
- Physics: components/apex, a sign/frame dependency, and an unseen multi-representation topic.
- Mathematics: roots/factors/domain constraints plus a withheld different concept family.
- Chemistry: coefficients/subscripts, an equation-versus-mechanism trap and a different symbolic/model transition.

Use the same source set and owner briefs across comparisons. Include clean packets, deliberately incomplete packets and planted errors. Keep the answer/review oracle independent of the production authors. Reserve held-out topics; do not tune only on the three examples in this PR.

Suggested variants:
1. Strong single-instance baseline with the complete task and source set.
2. Fresh roles with full-context handoff.
3. Fresh roles with typed packets and source retrieval.
4. Same eligible profile reused in fresh instances.
5. Different eligible profiles with the same source and packet protocol.

These are experimental variants, not permission to run agents now. A baseline that violates a proposed production independence rule can still be used as a labelled comparator.

Hold task information and approximate inference/tool budgets comparable, then report actual costs. Where budgets differ materially, provide both a fixed-budget comparison and quality/cost tradeoff instead of attributing all improvement to architecture.

## Outcomes to measure

Measure subject correctness and condition preservation; omitted necessary bridges; representation misinterpretations; source/claim fidelity; recognition/transfer intelligence retained; owner-goal fidelity; unsupported teaching claims; stale-state/duplicate acceptance; recovery correctness; and cost, latency and rework volume.

Pedagogical judges should rate actual explanations with examples of accepted/rejected reasoning, ideally blinded to architecture variant. Report disagreement and task-level examples rather than only an average score. Machine and model-based scores stay separately labelled. Do not treat agreement between related agents as an independent correctness oracle.

Choose numerical thresholds after a pilot with explicit severity criteria; this review does not invent calibrated values. Critical errors such as false law, lost solution, unsafe species interpretation, invented provenance or unsupported required prerequisite must be visible individually, even if average scores are high.

## Staged adoption

1. Owner reviews meanings, relay boundaries, packet semantics and examples in this draft.
2. Implement a minimal vertical slice in a later authorized engineering task: one subtopic, both first-role routes, one receipt-to-practice transition, targeted correction and recovery.
3. Run structural/domain falsifiers and independently review actual teaching/question artifacts.
4. Evaluate unseen topics and compare relay variants before choosing reliability thresholds or scaling the agent count.
5. Migrate subject contracts explicitly, preserving their existing source/answer/artifact safeguards.
6. Conduct learner evaluation only as a separately scoped activity if efficacy claims are desired.

No current source inspection or document validation establishes completion of these adoption gates.
