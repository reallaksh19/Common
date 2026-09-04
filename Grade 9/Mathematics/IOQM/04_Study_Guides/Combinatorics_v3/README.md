# Combinatorics Study Guide v3 — 72-Hour Rescue Layer

## Status

This package upgrades the existing `Combinatorics_v2` reference book for a specific learner state:

- Grade 9;
- roughly 30–50% prior knowledge;
- exam in about three days;
- formulas may be partly remembered;
- the main bottleneck is recognizing which method/model applies and writing the first useful line.

The v2 teaching core is **not discarded**. Its static self-sufficiency audit already maps all supplied Q1–Q56 to explicitly taught methods. v3 adds the missing exam-time orchestration and local retrieval support.

## Architecture

```text
Part 0 — 72-Hour Exam Navigator
    diagnose recognition separately from execution
    build Green / Yellow / Red map
    assign R/M/S/E/C failure code
    combine global priority with personal deficit
    bound the three-day route

Existing v2 Core Reference Book
    durable teaching and worked explanations

Advanced Worked Bridges
    execution repair for non-routine methods

Appendix A
    Q1–Q56 + local Notice / Recall / Start strips

Appendix B
    transfer / wider-curriculum probes

Quick Reference
    rapid recall, not teaching
```

## Files in this v3 package

- `Part_0_72_Hour_Exam_Navigator.md` — student-facing three-day routing layer.
- `Question_to_Method_Priority_Matrix.md` — reviewer matrix for all Q1–Q56: stable skill, priority, hint depth, likely failure point and useful visual.
- `Appendix_A_Local_Hints.md` — complete answer-free local hint overlay for Q1–Q56.
- `QA.md` — data sources, counts, gates and remaining work.

The reusable builder profile is stored at:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/combinatorics-question-driven-profile-v2.md`

## Data used

This revision was not designed from the attached 56-question set alone. It also consumes existing repository evidence:

1. `Combinatorics_v2/Self_Sufficiency_Audit.md` — exact Q1–Q56 method obligations and known v1 orphan-method repairs.
2. Validated 2023–2025 90-question IOQM taxonomy reconciliation — primary-domain/topic signal for global priority; these counts are explicitly **not official weightage**.
3. `COMB-01` First-Step Reference and Recognition/First-Line Lab.
4. `COMB-02` Graphs/Colouring First-Step Reference and Recognition/First-Line Lab.
5. `COMB-03` State/Recurrence First-Step Reference and Recognition Lab.
6. `COMB-05` Pigeonhole/Extremal First-Step Reference and Recognition/First-Line Lab.
7. Existing v2 main guide, Advanced Worked Bridges, Quick Reference and Appendix B.

## Key design decisions

### Recognition is tested before full solving

The entry diagnostic uses 12 short `notice -> method -> first useful line` items. No hint is shown before the unaided response is scored.

### Priority is not difficulty

The three-day core contains 22 Appendix A items plus Appendix B B19/B20 for wider canonical Pigeonhole/Games coverage, giving a maximum 24-item route **before removing skills already Green**.

### Workload is bounded

```text
MAX_ACTIVE_RED_FAMILIES_PER_DAY = 4
MAX_NEW_CORE_SKILLS_DAY3 = 0
MAX_MUST_PRACTICE_ITEMS = 24
MAX_INITIAL_FULL_EXECUTION_PROBES = 6
```

### Errors route to different repairs

```text
R Recognize -> router / Notice
M Remember  -> Recall / skill card
S Start     -> first-line model
E Execute   -> worked bridge
C Check     -> identity / overlap / symmetry / exact-once checklist
```

### Hints fade across non-identical problems

```text
Learn: Notice + Recall + Start
-> Retrieve: max Recall
-> Transfer: max Notice
-> Exam: no hint
```

## Scope boundary

This package makes document-design claims only. It does **not** claim measured classroom timing, retention, fresh-paper solve rate, calibrated difficulty, psychometric discrimination, or probability of qualifying IOQM.

## Next production step

Integrate Part 0 and the local hint overlay into the v2 source, add the selected structural visuals from the matrix, run the PR-140 visual/orphan/hint gates, then generate and inspect the v3 PDF at 200 dpi.