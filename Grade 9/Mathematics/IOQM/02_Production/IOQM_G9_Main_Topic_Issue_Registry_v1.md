# IOQM Grade 9 — Main-Topic Issue Registry v1

Status: `22_OF_22_PRODUCTION_ISSUES_CREATED`

Control rule: one main topic = one production issue. Internal microstreams stay inside that issue and do not create child issues.

## Wave 1 — canonical primitives, parallel

| Topic | Issue |
|---|---:|
| NT-01 Divisibility / GCD / LCM | #68 |
| ALG-01 Identities / Transformations | #69 |
| ALG-04 Sequences / Progressions / Recurrences | #70 |
| ALG-07 Floor / Ceiling / Discrete Functions | #71 |
| GEO-02 Angles / Lines / Quadrilaterals / Polygons | #72 |
| GEO-03 Similarity / Ratio / Area / Centroid | #73 |
| GEO-05 Coordinate / Vector / Mensuration | #74 |
| COMB-01 Basic Counting / Restrictions / IE | #75 |
| COMB-05 Pigeonhole / Extremal | #76 |

## Wave 2 — starts after named prerequisite interfaces freeze

| Topic | Issue | Required interface |
|---|---:|---|
| NT-02 Modular Arithmetic / Residues / Cycles | #77 | NT-01 |
| NT-03 Prime Factorisation / Divisors / Perfect Powers | #78 | NT-01 |
| ALG-02 Inequalities / Bounds / Equality | #79 | ALG-01 |
| ALG-03 Polynomials / Roots / Vieta / Remainders | #80 | ALG-01 |
| ALG-05 Functional Equations | #81 | ALG-01 bridge |
| ALG-06 Exponents / Radicals / Logs | #82 | ALG-01 |
| GEO-01 Triangle Feasibility / Metric / Cevians | #83 | GEO-03; G9 angle core |
| GEO-04 Circles / Cyclicity / Tangency | #84 | GEO-02 |
| COMB-02 Graphs / Colouring / Incidence | #85 | COMB-01 |
| COMB-03 Recurrence / Tilings / State | #86 | COMB-01; ALG-04 bridge |

## Wave 3 — composite / cross-domain

| Topic | Issue | Required interface |
|---|---:|---|
| NT-04 Diophantine / Integer Restrictions | #87 | NT-03 + ALG-01; ALG-03 bridge |
| NT-05 Digits / Place Value / Bases | #88 | NT-02 for advanced residue/cycle work |
| COMB-04 Games / Invariants | #89 | NT-01/NT-02 bridge + F1 proof habits |

## Issue execution authority

Every issue must read:

- `Grade 9/skills/ioqm-grade9-main-topic-builder/SKILL.md`;
- `00_Architecture/*`;
- `01_Corpus/*`, including answer-verification and metadata-correction overlays;
- `02_Production/IOQM_G9_Main_Topic_Production_Waves_v1.md`;
- `02_Production/IOQM_G9_Canonical_Overlap_Ownership_v1.md`;
- `02_Production/IOQM_G9_Main_Topic_Prompt_Pack_v1.md`.

The issue body is a standalone execution prompt; the prompt pack is the shared detailed authority.

## Start rule

Wave-1 issues may proceed in parallel immediately after the architecture/corpus PR is available.

Wave-2/3 agents may perform source/prework early, but **integrated student prose must wait for required prerequisite interfaces**, not for the final upstream PDF.

## Evidence rule

The 90 validated historical answers are independently verified. This does not imply classroom timing, psychometric difficulty, retention or qualification probability; those remain `NOT_RUN` until observed.

## Current control state

`PROGRAM_ISSUE_CONTROL_PLANE_READY`