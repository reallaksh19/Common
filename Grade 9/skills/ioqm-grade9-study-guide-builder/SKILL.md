---
name: ioqm-grade9-study-guide-builder
description: Build or revise a Grade 9 IOQM study guide from existing repository material plus user-supplied questions/notes, with a configurable learner-knowledge profile (default partial knowledge), self-sufficiency audit, benchmark comparison, clean question appendices, decision-first quick reference, source/citation ledger, domain-specific authoring profiles, flexible T1-to-Tx short-horizon readiness checks, and traceable visual-pedagogy obligations.
---

# IOQM Grade 9 Study Guide Builder

## Purpose

Use this skill when the goal is not merely to collect solved questions, but to produce a **teacher-style study guide** that lets a Grade 9 learner with partial prior knowledge recognize and execute the methods needed for a supplied problem set.

This skill is deliberately different from a main-topic production package. It may synthesize several existing main topics into one revision/study guide, but it must preserve canonical topic ownership and must not silently create a new official syllabus.

## Mandatory v2 references

Before authoring or revising a production study guide, read:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2.md`

That reference is the detailed production contract for question-to-method matrices, stable skill IDs, orphan-method repair, progressive local hints, Visual Bridges, self-sufficiency gates, optional short-horizon navigation, and inspected PDF delivery.

When the user provides learner-specific topic/subtopic/skill knowledge, or when short-horizon readiness routing is requested, also read:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/learner-knowledge-profile-and-readiness-addendum.md`

That addendum defines optional learner-knowledge input, specificity precedence, personalization without pruning the durable core, and flexible `T1 ... Tx` Quick Check selection. It overrides older fixed prior-knowledge percentages and fixed Quick Check counts for those fields only.

If **any** question, chapter, Worked Bridge, Appendix A/B item, Appendix C method family, or Navigator element has a visual requirement other than `VISUAL_NONE`, also read and apply:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2-visual-production-addendum.md`

The visual addendum is mandatory when triggered. A required visual is a teaching obligation, not optional polish.

When a domain profile exists, read it after the generalized contract. A domain profile specializes the generalized rules; it does not weaken them. Learner-profile/readiness overrides may then specialize only learner knowledge and Quick Check selection.

Current profile example:

`Grade 9/skills/ioqm-grade9-study-guide-builder/references/algebra-question-driven-profile-v2.md`

## Core student standard

If no learner-specific knowledge is supplied, assume the learner knows roughly 30–50% of the school-level background:

- familiar formulas may be remembered;
- routine exercises may be solvable;
- method recognition is inconsistent;
- nearby methods are confused;
- advanced Olympiad moves cannot be assumed.

If the user provides topic/subtopic/skill-wise knowledge, **do not flatten it into one global percentage**. Use the most specific relevant information for routing. Accept categorical, approximate-percentage, or natural-language input. Treat stated percentages as planning estimates unless they come from measured evidence.

Examples:

```text
Quadratics = strong
Polynomials / Vieta = strong
Polynomials / repeated roots = weak
Recurrences = 20%
ALG-EQ-04 = unknown
```

The durable guide should still remain self-sufficient for a partial-knowledge learner unless the user explicitly requests a personally pruned edition. Personalization changes the Navigator route, Quick Check selection, practice priority, and starting support level; it does not silently delete core teaching.

The guide must therefore teach **enough to recognize, start, execute, and check**, not merely name methods.

The learner path is:

**problem wording → recognized structure → legal method choice → first useful line → execution → checking.**

## Source roles

Classify every input before authoring.

### Authority source

Official/validated contest papers, frozen repository source maps, correction overlays, stable interfaces.

Use these for exact historical claims, answer custody and official-source statements.

### Comparison/practice source

User notes, coaching handouts, videos, DPP compilations, preparation routines, external question lists.

Use these to discover methods, teaching cues and practice coverage. Do not upgrade them to official authority.

### Internal quality benchmark

For Grade 9 mathematics, inspect:

`Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`

Use it as a quality comparator for:

- explanation completeness;
- missing-link repair;
- method contrast;
- attempt before answers;
- independence in starting unfamiliar problems;
- source/citation discipline;
- visual pedagogy;
- cover/index usability;
- final PDF quality.

Do not copy its wording, layout, exercises, typography, or diagrams.

## Required pre-authoring audit

Before writing the guide, create a question inventory / question-to-method matrix.

For every supplied question record at minimum:

- stable local question number;
- mathematical surface;
- primary method;
- secondary prerequisite;
- recognition cue;
- first useful line;
- enough execution detail to finish;
- difficulty of recognition;
- likely half-knowledge misconception;
- legality/reversibility/admissibility checks where relevant;
- whether the current guide explicitly teaches the method;
- whether the current guide gives enough execution detail;
- planned teaching location;
- initial hint depth where hints are allowed;
- visual requirement.

When learner-specific input exists, also maintain enough internal mapping to know which topic/subtopic/skill is `UNKNOWN`, `NONE`, `WEAK`, `PARTIAL`, `STRONG`, or `SECURE`, and what evidence/source produced that state.

### Visual requirement fields

When a visual may matter, do not use only a loose note such as “diagram useful.” Apply the visual addendum and record:

- `visual_level = NONE / OPTIONAL / REQUIRED / SOURCE_REQUIRED`;
- visual teaching job;
- stable visual asset ID;
- visual form;
- what the learner should notice;
- placement layer(s);
- leakage risk;
- visual status.

A `REQUIRED` or `SOURCE_REQUIRED` visual must be traceable through:

**question/skill → visual obligation → asset → placement → rendered page → QA pass.**

### Orphan-method test

A method is **orphaned** if a student must already know a trick that the guide only names.

Examples:

- “use derangements” without defining/counting derangements;
- “use Burnside” without a small-symmetry path or Burnside explanation;
- “degree 2 means cycles” without the labeled cycle-count formula;
- “use generating functions” without explaining coefficient extraction;
- “alternate inequalities” without showing how to count a small alternating pattern.

No supplied question may retain an orphan method.

## Static self-sufficiency gate

A question passes only if the guide contains all required support:

1. **Prerequisite refresh** — the minimum background is stated or recalled.
2. **Recognition cue** — what in the wording/structure should trigger the method.
3. **First useful step** — an executable first mathematical line, construction, or representation.
4. **Execution bridge** — enough explanation to finish the method without an unnamed trick.
5. **Legality/common-error check** — the nearby wrong move is identified where relevant.
6. **Practice isolation** — the question itself does not leak the method or answer beyond the requested support level.
7. **Required visual support** — if `visual_level` is `REQUIRED` or `SOURCE_REQUIRED`, the visual must exist, be correctly placed, and pass final-size rendered QA.

Record:

`STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n`

only when every supplied question passes.

This gate evaluates the durable document, not the learner's stated percentage. A personalized route may skip secure topics in short-horizon mode without weakening the underlying core.

This is not classroom evidence. Keep actual learner success, timing, retention and psychometrics unclaimed unless observed.

## Subtopic grouping rule

Do not group by the source document's lot/order unless that order is pedagogically strong.

Group by dependency:

1. fundamentals;
2. direct applications;
3. restricted/conditional variants;
4. representation changes;
5. advanced structures;
6. mixed method selection.

For combinatorics, a strong default progression is:

- counting foundations;
- selections and logical restrictions;
- distributions/multisets;
- linear arrangements;
- relative order/rank;
- circular symmetry;
- graphs/matchings/colorings;
- recurrence/state;
- number-theoretic counting;
- pigeonhole/extremal;
- invariants/games.

For other domains, derive a comparable dependency order from the repository topic map and the domain profile.

## Learner-facing style

Write like a strong teacher, not like an internal production system.

Prefer:

- “What should I notice?”
- “Why this works”
- “Try this first”
- “Common mistake”
- “When this method is not appropriate”
- “Check”
- short worked examples

For progressive hints, learner-facing labels may be:

- **Notice**;
- **Recall**;
- **Start**.

Internal QA may call these H1/H2/H3, but do not make opaque `H1/H2/H3` codes the main learner-facing language.

Avoid learner-facing internal terms such as:

- wave;
- microstream;
- RMSEC;
- transfer gate;
- control plane;
- interface owner;
- raw priority equations;
- psychometric-sounding readiness percentages unless actually measured.

Internal QA documents may use technical production terminology when necessary.

## Worked-example rule

For every non-routine method needed by the supplied questions, include at least one **non-identical worked example**.

The example should reveal the mechanism without becoming a disguised copy of the appendix question.

If the representation itself is the hidden method, the worked example must include the corresponding required visual at the point where the representation is introduced.

## Visual pedagogy rule

Figures are teaching tools, not decoration.

Use visuals when they materially reduce cognitive load or expose a structure that prose hides: graphs, constructions, blocks/gaps, state diagrams, number lines, exponent grids, symmetry/orbit models, case-overlap schematics, tables, or other exact mathematical representations.

When visuals are triggered:

1. create a Visual Obligation Register before final layout;
2. write an asset brief for every required visual;
3. prefer deterministic/vector/programmatic construction when exact mathematical relationships matter;
4. do not use generative illustration as authority for exact geometry, graph topology, coordinate intersections, mathematical labels/equations, or source-required contest figures;
5. place the first useful visual where the representation is first taught, not only in a later gallery;
6. use quieter variants in Appendix A when they help recognition without leaking the solution;
7. preserve transfer integrity in Appendix B — method-revealing visuals normally belong after the attempt unless the problem itself requires the figure;
8. use retrieval micro-models in Appendix C for high-value visually driven method families;
9. do not show method-revealing routers before an unaided short-horizon diagnostic;
10. render and inspect every required visual at final size.

A decorative image never satisfies a required visual obligation.

## Appendix contract

### Appendix A — supplied questions

If the user explicitly asks for **strict questions-only**, that instruction overrides the default local-hint presentation:

- reproduce every supplied question;
- remove solutions, tips, source commentary, local hints, and module-position notes from the appendix;
- preserve all mathematical conditions and source-required figures needed to solve the question;
- place the answer key only after the final question.

Otherwise, for the partial-knowledge learner profile, use the detailed v2 contract's adaptive local hint model where appropriate:

- **Notice** — recognition clue;
- **Recall** — readable prior skill + stable ID;
- **Start** — first executable move without solution leakage.

Required local visuals may sit with the question/Notice strip when they reduce recognition load, but must not reveal more than the assigned support depth.

Maintain source/provenance in a separate citation ledger.

### Appendix B — audit / mixed transfer

Create a fresh mixed mock set when requested or required by the domain profile.

Rules:

- label author-created items as author-created;
- model method balance on verified historical repository patterns;
- do not claim an official Grade-9-only IOQM paper exists;
- include methods underrepresented by the supplied attachment but present in the canonical curriculum;
- hide topic labels where transfer is being tested;
- answers only after the final mock question;
- independently recompute every answer;
- include a problem-essential figure with the problem when necessary;
- keep method-revealing rescue visuals out of the pre-attempt page unless explicitly requested.

## Quick-reference handout / Appendix C

Create a compact decision-first memory helper, usually 1–3 pages depending on the domain.

Start with:

**What do I see? → What should I draw/write first? → What must I check?**

Then include only material worth recalling quickly:

- compact method triggers;
- core formulas after method choice;
- common legality/equality conditions;
- high-value transforms;
- final pre-submit checklist;
- stable IDs in secondary type where useful.

If the domain contains high-value visually driven method families, Appendix C must include small retrieval micro-models where they beat another sentence: gaps, blocks, circle identity, graph, state arrows, residue cycle, exponent grid, root/tangency sketch, similarity/cyclicity configuration, etc.

Do not put full worked solutions in the handout.

## Optional short-horizon Navigator

When the learner has only a few days, apply the detailed v2 Navigator rules and the learner-profile/readiness addendum when applicable.

The student-facing interface should remain simple:

- Quick Check uses `T1`, `T2`, ... `Tx` rather than colliding with corpus `Q1`, `Q2`, ...;
- `x` is derived from the learner profile, high-value unknown/weak/partial families, time budget, page fit, and any explicit user count;
- if no learner profile is supplied, use the domain's default Quick Check bank/count;
- score recognition before exposing method cues or visual routers;
- use readable `DO FIRST / DO NEXT / QUICK RETEST / ONLY IF TIME` routing;
- use plain-language `Notice / Recall / Start` repair;
- keep internal diagnostic codes and priority equations out of the child-facing pages;
- do not waste T-slots repeatedly testing explicitly secure families unless a mixed spot-check is useful;
- no major new core skill on Day 3;
- protect normal sleep rather than prescribing late-night new theory.

The governing architecture remains:

**Navigator = where to go. Core = how to do it.**

## Citation and provenance rule

Provide citations wherever useful, but do not contaminate a strict questions-only appendix.

Preferred locations:

- source/citation ledger;
- chapter endnotes;
- teacher/reviewer manifest;
- stable historical ID references.

For a comparison source, preserve its uncertainty. Never turn “identified practice problem” into “confirmed official lecture question.”

## Independent cross-check

Before finalizing:

1. every supplied question appears exactly once in Appendix A;
2. no inline answers appear before the Appendix A answer key;
3. every Appendix A question maps to a taught method;
4. every non-routine method has an execution bridge;
5. every `REQUIRED`/`SOURCE_REQUIRED` visual has an asset, placement, and rendered QA pass;
6. no decorative figure is counted as pedagogical visual coverage;
7. Appendix B answer count matches question count;
8. every Appendix B answer is independently recomputed;
9. broader canonical curriculum gaps exposed by the source set are repaired or explicitly listed;
10. citations/source roles are recorded;
11. quick-reference content matches the main guide and carries micro-models for visually driven core families where appropriate;
12. no unsupported classroom-effectiveness claim is made;
13. when learner knowledge is supplied, the most specific topic/subtopic/skill evidence controls routing without pruning the durable core;
14. when a short-horizon Quick Check is used, its `T1 ... Tx` count and family coverage are justified by the selected scope/profile rather than copied blindly from a default edition.

## Hard visual gate

If any required visual remains only `PLANNED`, missing, broken, misplaced, unreadable at final size, mathematically incorrect, or too solution-revealing:

`PDF_GENERATION_ALLOWED = FALSE`

for a first final build, or:

`STATUS = VISUAL_REBUILD_REQUIRED`

for a rendered draft.

Use contact sheets for whole-book scanning, but inspect every critical required visual on its actual rendered page at final reading size.

Recommended visual gates when triggered:

```text
VISUAL_OBLIGATION_REGISTER = COMPLETE
VISUAL_OBLIGATIONS = PASS_n_OF_n
VISUAL_REQUIRED_ASSETS = PASS_n_OF_n
VISUAL_PLACEMENT = PASS_n_OF_n
CRITICAL_VISUAL_FINAL_SIZE_QA = PASS_n_OF_n
SOURCE_REQUIRED_FIGURE_CUSTODY = PASS_n_OF_n
ANSWER_FREE_VISUAL_LEAKAGE = 0
BROKEN_OR_MISSING_FIGURES = 0
VISUAL_ASSET_ORPHANS = 0
DECORATIVE_FIGURES_COUNTED_AS_COVERAGE = 0
```

## Required output set

A practical study-guide package should contain:

```text
README.md
<Subject>_Study_Guide_vN.md
Quick_Reference_or_Appendix_C.md
Appendix_A_<supplied-question-set>.md
Appendix_B_<mixed-transfer-set>.md
Self_Sufficiency_Audit.md
Sources_and_Citations.md
QA.md
```

When meaningful visual obligations exist, also create:

```text
Visual_Obligation_Register.md or .csv
Visual_Manifest.md or .csv
Visual_Pedagogy_Audit.md
visuals/
```

For reusable agent operation create or maintain:

```text
Grade 9/skills/ioqm-grade9-study-guide-builder/SKILL.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/learner-knowledge-profile-and-readiness-addendum.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/question-driven-self-sufficient-study-guide-skill-v2-visual-production-addendum.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/domain-prompt-examples.md
Grade 9/skills/ioqm-grade9-study-guide-builder/references/self-sufficiency-audit-template.md
```

Read any available domain profile as part of the reusable authoring context.

## Completion language

Use:

`STATIC_CONTENT_SELF_SUFFICIENCY = PASS`

only for document-level coverage.

When visual obligations exist, do not call the final PDF visually complete until the visual addendum gates pass.

Keep these separate unless measured:

- classroom readability/timing;
- learner solve rate;
- retention;
- recognition accuracy;
- hint dependency;
- transfer success;
- psychometric calibration;
- qualification/pass-mark prediction.

## Final rule

A guide is not self-sufficient because it lists every formula, contains many pages, or looks professional.

It is self-sufficient only when the target learner can move from:

**problem wording → recognized structure → legal first step → executable method → correct check**

without needing an unnamed trick that exists only in the teacher's head.

If learner-specific knowledge is unavailable, use the partial-knowledge baseline. If it is available, personalize the route rather than pretending one global “50%” describes every topic.

When a representation is part of the method, the learner must also be able to **see the representation at the point of need**.
