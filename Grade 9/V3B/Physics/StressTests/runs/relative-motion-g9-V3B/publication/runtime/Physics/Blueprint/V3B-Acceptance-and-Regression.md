# V3B acceptance and regression contract

Severity and stage refinement: [research freedom and minimum criteria](V3B-Research-and-Minimum-Criteria.md) distinguishes exploratory work, review drafts and learner-ready acceptance. Advisory flags are not automatically required PASS gates. Consequential scientific uncertainty permits marked drafts but must be resolved for learner-ready use.

Implementation update: the [Physics publication host](../ProductionKit/V3B-Runtime-Map.md) now enforces a bounded subset against real exported HTML/SVG and source bytes. Its test results are separate from this full acceptance specification. Full six-Core authoring/release integration remains pending.

This is a topic-independent specification of evidence required for acceptance, not a report that these tests have executed. The [rule catalogue](V3B-Production-Rules.json) assigns stable IDs. Existing JavaScript proof checks remain prerequisites within their documented scope; they do not implement this complete suite. The older four-Core Python runtime is not certified by this revision.

## Evidence and gate computation

Allowed evidence states: PASS, FAIL, NOT_RUN, STALE, UNKNOWN, NOT_APPLICABLE. NOT_APPLICABLE needs an authorized applicability decision; it cannot bypass a mandatory rule. Compute required rules from the requested products, scientific families and publication medium **before** evaluating results. Check both missing expected evidence and unexpected unsupported claims.

Each result binds rule/version, topic/bucket/Core, source/model/baseline/policy digests, exact content/artifact digests, evaluator/version, command or review method, observed comparison, result and reviewer authority where applicable. Expected values must not come from the author's displayed solution. Host verification is required for digest and executable-run claims.

Conceptual release algorithm:

```text
required = applicable_minimum_acceptance(selected_products, accepted_baseline, medium, learner_mode)
advisories = findings_requiring_triage_but_not_automatic_rejection
for each requirement:
    resolve current source -> model -> content -> publication dependencies
    reject missing, stale, inapplicable or unsupported evidence
    accept only the evaluator permitted for that requirement
candidate_ready = every required requirement has accepted PASS evidence
release_authorized = candidate_ready AND exact-version owner authorization
```

This pseudocode is normative design, not an installed release hook. Until an execution host implements it, the owner board must expose enforcement gaps; an agent may not claim an automated production pass.

## Required rule and falsifier matrix

Mutation tests run on isolated copies. Establish a valid control first, introduce one defect, execute the real validator, and require the specific expected failure. Record the changed bytes and detailed output. A missing script, validator crash or unrelated failure is not successful detection. Restore and revalidate the control. Reviewer-based tests need a blinded second review, not a fabricated machine PASS.

| Rule | Required observation | Deliberate corruption that must be detected | Acceptance method |
|---|---|---|---|
| SRC-01 | Every source datum, equation, condition, figure and question/subpart is reconciled | Change a unit/value or omit a subpart while keeping IDs | Source comparison plus independent extraction review |
| COV-01 | Mandatory obligations resolve to substantive published objects | Keep an anchor but delete its explanation/answer body | Structural object/body check and publication extraction |
| SEM-01 | Equations and claims match source/model meaning and conditions | Reverse an operation/sign or change applicability while keeping the same equation ID | Family-specific oracle plus scientific review |
| DEP-01 | Every required difficult inference has explained prerequisites, repair and a check | Remove the decisive reasoning transition while retaining headings and word count | Independent academic review against obligation graph |
| CORE-01 | Each Core realizes its distinct learner action | Rename a 1A explanation as 1B; scatter hints in place of a full 2A solution | Core-specific academic review of actual tasks and answers |
| ANS-01 | Every prompt/subpart/retry resolves to a complete answer or appropriate model/rubric | Add an unregistered embedded prompt; retain an empty answer anchor | Prompt registry reconciliation plus academic answer review |
| ANS-02 | Published results agree with independently computed expectations | Corrupt the visible answer but leave recomputation code untouched | Read candidate answer, normalize units/forms and compare with independent oracle |
| FIG-01 | Each figure is bound to the actual problem/model state | Substitute a valid-looking figure with different quantities, signs or time | Scene/model comparison, artifact identity and scientific visual review |
| FIG-02 | Geometry, graph data and vector notation preserve scientific meaning | Reverse a vector, distort a quantitative scale or change a graph slope | Primitive/data geometry checks and rendered inspection |
| REUSE-01 | All eligible pairs and prior exposures are considered | Omit a pair from a supplied comparison list while repeating an example | Inventory-derived pair generation and exposure-ledger reconciliation |
| TRANSFER-01 | Claimed fresh transfer changes reasoning demand | Alter only numbers/nouns and count it as unseen transfer | Family/action comparison plus independent adjudication |
| FIT-01 | 2A/2B have scoped knowledge evidence or actual owner waiver and purpose | Remove waiver/evidence; label owner-routed output knowledge-validated | Input/provenance checks and calibration-policy review |
| FIT-02 | Claimed measured fit has learner performance evidence | Use aggregate percentage to assert every subtopic mastered | Skill-demand review and real performance evidence for measured claims |
| LAYOUT-01 | Final medium is legible and serves its learning purpose | Introduce excessive empty illustration canvas, clipping or tiny math labels | Bounds/overflow checks plus final-size visual inspection |
| RELAY-01 | A receiver can recover the required state from the declared bundle | Omit a source stem, required asset or current exposure history | Isolated recovery exercise and host digest/access verification |
| EXT-01 | Scope changes create a genuine delta and invalidate dependencies | Call existing content a new gate; retain receipts after a shared model change | Baseline delta/dependency-closure comparison |
| RELEASE-01 | Missing/stale evidence blocks affected acceptance; authorization is exact-version | Mark absent validators as PASS, mix baselines or reuse old owner approval | Host evidence validation and state-transition tests |

## Positive controls and limits

The suite must also accept legitimate cases: repeated fundamental equations with consistent meaning; an explicitly declared reconstruction anchor; mathematically equivalent answer forms and converted units; a correctly labeled schematic; an owner waiver that makes no knowledge-validation claim; an independent subtopic addition that leaves unrelated valid evidence intact. Report false blocks as well as missed defects.

No lexical similarity threshold proves novelty or pedagogy. Before treating scores as calibrated decisions, build independently labeled duplicate/reuse/transfer cases, adjudicate disagreement, split by scientific family/topic, and report precision, recall and false-block rates with sample sizes. Keep the numerical screening values provisional until this is done.

No minimum number of pages, examples or diagrams establishes assimilation. Conversely, a short and correct final answer does not fulfill a required detailed solution. Acceptance is against the inference/representation obligations and intended learner action.

## Generalization qualification

Use the reviewed Motion snapshot `dc885f969abbfe2d2455aa22edb68adb52c91343` as one external regression corpus. Its four reported undetected mutations motivate SRC-01, COV-01, SEM-01 and ANS-02; diagram/example findings motivate FIG and REUSE rules. These are prior audit observations, not results from a newly implemented validator.

Before claiming topic-independent runtime reliability, qualify at least these structurally different families: vector/component reasoning; scalar conservation or thermal relationships with units and sign conventions; graph/piecewise interpretation; and a predominantly conceptual/drawing explanation. These are test families, not a requirement to publish new books or a claim that all are Grade 9 syllabus content. Choose owner-approved grade-appropriate bindings or explicitly separate advanced fixtures. Use an unseen binding for each implemented family to test that passing did not depend on memorized question IDs.

Gate creation precedes lesson generation. A family without a qualified evaluator remains researchable and draftable, and may be accepted through qualified scientific review; it cannot claim automated answer/figure verification. A successful motion example cannot certify thermodynamics or optics. A research extension needs a qualified depth-specific reviewer as well as expanded obligations.

## Implementation ledger at this revision

| Layer | Delivered in this revision | Still required before a production claim |
|---|---|---|
| Universal authoring contract | Detailed typed records, depth, Core action, reuse, figure, answer, fit and layout requirements | Consistent application and academic review on generated material |
| Entry points | Existing Physics contracts and new-topic entry now require this blueprint | Host refusal to bypass it |
| Machine-readable rules | IDs, applicability, evidence method and falsifier catalogue | Executable adapters; catalogue is not a validator/schema |
| Existing proof runtime | Preserved without altered numerical authority | Bind real files/artifacts and six-Core transitions; run new falsifiers |
| Publication | Final-medium inspection and content/asset binding requirements | Actual export integration and visual inspection |
| Relay | Complete portable bundle and current-state requirements | Demonstrated restart with host verification |
| Release | Explicit separate readiness and authorization logic | Trusted host enforcement and exact-version owner decision |

Documentation/JSON/link validation only supports the first three delivered entries. It must not be reported as scientific, pedagogical, learner-fit or textbook-publication acceptance.
