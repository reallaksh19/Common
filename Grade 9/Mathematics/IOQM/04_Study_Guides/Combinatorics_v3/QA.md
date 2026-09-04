# Combinatorics v3 — QA and Evidence Ledger

## 1. Existing baseline preserved

The existing Combinatorics v2 self-sufficiency audit records:

```text
STATIC_CONTENT_SELF_SUFFICIENCY = PASS_56_OF_56
```

That claim means each supplied Appendix A problem already has a taught recognition/execution route somewhere in v2. It does not include measured timing, retention, method selection under pressure or fresh-paper solve rate.

v3 therefore does **not** rewrite the entire core merely to make it longer. It adds stable retrieval objects, local hints, a visual audit and the 72-hour Navigator.

## 2. Wider repository signal used for priority

The validated 2023–2025 90-question reconciliation records 23/90 Combinatorics-primary items. Topic-primary counts are:

| Canonical topic | Count / 90 |
|---|---:|
| COMB-01 Basic Counting / Restrictions / Inclusion–Exclusion | 7 |
| COMB-02 Graphs / Colouring / Incidence | 6 |
| COMB-03 Recurrence / Tilings / State Evolution | 5 |
| COMB-04 Games / Invariants | 3 |
| COMB-05 Pigeonhole / Extremal | 2 |

These are used only as a recurrence/canonical-relevance signal. They are **not official IOQM weightage** and are not converted into chapter percentages.

The Q1–Q56 worksheet under-represents COMB-04 and COMB-05, so the 72-hour core deliberately includes Appendix B B19 (pigeonhole) and B20 (winning positions / invariant) rather than allowing the worksheet alone to define the curriculum.

## 3. Existing recognition assets reused

The Navigator was aligned with existing repository first-step references rather than inventing a second terminology layer:

- COMB-01 router: counted object -> order -> restrictions -> disjoint stages/cases -> direct/complement/IE -> check.
- COMB-02 router: define vertices/edges; degree sum; proper colouring; cyclic closure; static graph vs game-state distinction.
- COMB-03 router: define a sufficient state; exactly-once split; map to smaller states; meaningful base cases; reverse state when target branching is smaller.
- COMB-05 router: forced existence -> objects/boxes/capacity; or choose an extreme object and exploit what extremeness forbids.

The 12-item Recognition Scan samples these representations plus the high-transfer arrangement/symmetry methods already present in v2.

## 4. Q1–Q56 routing counts

From `Question_to_Method_Priority_Matrix.md`:

```text
QUESTION_INVENTORY = 56
MUST = 22
SHOULD = 24
IF_TIME = 10
WIDER_CANONICAL_MUST = 2   # Appendix B B19/B20
MAX_THREE_DAY_CORE = 24
```

Hint-depth allocation:

```text
NOTICE_ONLY = 16
NOTICE_RECALL = 21
NOTICE_RECALL_START = 19
TOTAL = 56
```

Appendix A hint overlay audit:

```text
NOTICE_PRESENT = PASS_56_OF_56
RECALL_PRESENT_WHERE_ASSIGNED = PASS_40_OF_40
START_PRESENT_WHERE_ASSIGNED = PASS_19_OF_19
FINAL_NUMERICAL_ANSWER_LEAKAGE = 0
```

## 5. 72-hour Navigator gates

```text
72H_NAVIGATOR_PRESENT = PASS
72H_RECOGNITION_SCAN = PASS_12_OF_12
72H_RECOGNITION_BEFORE_HINT = PASS
72H_TARGETED_EXECUTION_POOL = PASS
72H_MAX_INITIAL_EXECUTION_PROBES = 6
72H_TRAFFIC_LIGHT_MAP = PASS
72H_INTERNAL_YR_YE_SPLIT = PASS
72H_RMSEC_REPAIR_ROUTER = PASS
72H_PRIORITY_RATIONALE = PASS
72H_PERSONAL_PLAN = PASS
72H_HINT_FADING_PROTOCOL = PASS
72H_MAX_ACTIVE_RED_FAMILIES_PER_DAY = 4
72H_MAX_NEW_CORE_SKILLS_DAY3 = 0
72H_MAX_MUST_PRACTICE_ITEMS = 24
```

## 6. Priority sanity checks

Priority is not difficulty.

Examples:

- Q3 subset complement is MUST because it is foundational, high-transfer and cheap to retrieve.
- Q34 degree-2 graph decomposition is MUST because the graph representation is canonical and the orphan-method risk is high.
- Q53 cube rotations is IF TIME in a three-day rescue because it is narrower and has lower dependency value, despite being mathematically worthwhile.
- Q16 nonlinear recurrence ratio is IF TIME because it is a specialized cross-domain mechanism and should not displace core state-recognition work.

No raw duplicate count is allowed to inflate the frequency component.

## 7. Visual-pedagogy audit status

The matrix identifies strong visual candidates, but figures have not yet been integrated into the final PDF source.

Current status:

```text
VISUAL_CANDIDATE_INVENTORY = PASS
FINAL_FIGURES_INTEGRATED = NOT_RUN
FINAL_200_DPI_FIGURE_INSPECTION = NOT_RUN
```

High-value figure obligations for the PDF pass include Q8, Q12, Q20, Q31, Q33, Q34, Q41, Q46, Q49 and Q51.

## 8. PDF gate

The source-layer work in this PR is not itself the final PDF. Do not claim final PR-140 acceptance until:

```text
CORE_SKILL_HEADERS_INTEGRATED = PASS
APPENDIX_A_LOCAL_HINTS_INTEGRATED = PASS_56_OF_56
VISUAL_PEDAGOGY_GAPS = 0
PDF_PREFLIGHT = PASS
PDF_RENDER_200_DPI = PASS
EVERY_PAGE_VISUALLY_INSPECTED = PASS
SHA256_RECORDED = PASS
```

## 9. Learner metrics to record if a real student uses this mode

These are **measurement fields**, not pre-filled claims:

- unaided recognition accuracy;
- first-line accuracy;
- recognition-after-Notice gain;
- execution conditional on correct recognition;
- median hint depth by day;
- R/M/S/E/C error distribution;
- non-identical transfer success;
- recognition latency on mixed core items.

Suggested Day 1/2/3 readiness targets in the Navigator are directional routing targets, not psychometric thresholds.

## 10. Current source-layer verdict

```text
COMB_STABLE_SKILL_PROFILE = PASS
COMB_QUESTION_TO_METHOD_PRIORITY = PASS_56_OF_56
COMB_APPENDIX_A_HINT_OVERLAY = PASS_56_OF_56
COMB_72H_NAVIGATOR_SOURCE = PASS
COMB_V3_FINAL_PDF = NOT_RUN
```

The next step is integration/render QA, not another architecture redesign.