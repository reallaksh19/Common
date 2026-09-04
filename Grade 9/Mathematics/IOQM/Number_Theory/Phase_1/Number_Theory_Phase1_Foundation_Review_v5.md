---
title: "Number Theory v5 - Phase 1 Foundation Review"
subtitle: "PR #140 question-driven rebuild"
date: "September 2026"
toc: true
toc-depth: 2
geometry: margin=18mm
fontsize: 10pt
header-includes:
  - |
    \usepackage{longtable}
    \usepackage{booktabs}
    \usepackage{array}
---

# Phase 1 decision

**Status: COMPLETE - FOUNDATION / CUSTODY ONLY**

Phase 1 freezes the 90 Appendix A stems, the 20 Appendix B stems, stable
Number Theory skill/bridge IDs, badge vocabulary, the PR140 matrix schema, and
the rule that production deliverables must also appear in the final PDF.

It does **not** claim that the final self-sufficiency gates have passed.

# Final PDF inclusion map

The final book will contain two clearly separated layers.

## Student Book

1. teaching units;
2. mixed method-selection lab;
3. Advanced Worked Bridges;
4. quick reference;
5. Appendix A;
6. Appendix B;
7. Appendix C.

## Reviewer / Build Dossier

1. Number Theory Question-Driven Profile;
2. full 90-row Appendix A Question-to-Method Matrix;
3. full 20-row Appendix B Method-Coverage Matrix;
4. corpus/source custody ledger;
5. self-sufficiency gate report;
6. visual/figure manifest;
7. final QA record and SHA-256.

# Frozen corpus

- Appendix A stems frozen: **90/90**
- Appendix B stems frozen: **20/20**
- Total frozen practice stems: **110/110**

A stem hash is recorded for every item. Badges, hints, layout and helpful
structural figures may change; the mathematical stem may change only for a
separately documented source correction.

# Badge contract

Appendix A:

`[CORE|BRIDGE|CHALLENGE] [BROAD FAMILY] [TRANSFER|MIXED|ADVANCED BRIDGE]`

Appendix B adds:

`[PYQ]`

Badges orient the learner. They must not reveal the decisive trick.

# Phase 1 acceptance checks

| Gate | Result |
|---|---|
| Appendix A stems inventoried | PASS 90/90 |
| Appendix B stems inventoried | PASS 20/20 |
| Stem hashes recorded | PASS 110/110 |
| Stable skill IDs defined | PASS |
| Stable bridge IDs defined | PASS |
| Badge vocabulary frozen | PASS |
| A matrix schema upgraded | PASS 90/90 rows |
| B matrix schema created | PASS 20/20 rows |
| Final-PDF deliverable inclusion rule | PASS |
| Final orphan-method audit | NOT RUN - Phase 2 |
| Final hint audit | NOT RUN - Phase 3 |
| Final self-sufficiency audit | NOT RUN - Phase 4 |
| Final PDF generation | BLOCKED until Phase 4 |

# Next phase

**Phase 2 - Teaching and visual rebuild.**

The next work item is to audit every stable skill against the 90-question
matrix, split any remaining broad skill, repair orphan methods, and define the
visual teaching object for each question where a diagram materially reduces
cognitive load.
