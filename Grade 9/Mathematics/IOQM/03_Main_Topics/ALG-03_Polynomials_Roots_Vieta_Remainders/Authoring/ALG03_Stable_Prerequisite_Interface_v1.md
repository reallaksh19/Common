# ALG-03 - Stable Prerequisite Interface v1

Status: `FROZEN_FOR_DOWNSTREAM_CONSUMPTION`

Canonical owner: `IOQM-G9-ALG-03`.

## Downstream may assume

A learner who has completed ALG-03 can:

1. choose among coefficient, factor, root, symmetric-invariant, and remainder representations from the requested information;
2. use root-factor correspondence;
3. reconstruct Vieta from `a(x-alpha)(x-beta)` rather than treating it as an unexplained formula list;
4. use Vieta when symmetric root information is requested without unnecessarily solving individual roots;
5. use the discriminant for quadratic real-root behavior and route minimum/maximum questions to ALG-02;
6. transform root sets correctly: desired root shift `+c` corresponds to input shift `P(x-c)`;
7. use remainder and factor theorems through evaluation;
8. reduce high powers modulo a low-degree polynomial relation;
9. eliminate leading terms to find candidate common roots and then check candidates in the originals.

## Canonical router

`REQUESTED INFORMATION -> REPRESENTATION -> FIRST MOVE -> CONDITIONS -> CHECK`

## Downstream retrieval contract

Other topics may `RECALL`, `CHECK`, `BRIDGE`, or `ROUTE_BACK` to this interface. They must not independently rederive Vieta, discriminant, or polynomial-remainder canon.

## Explicit non-exports

This interface does not export:
- general inequality/equality/attainment doctrine (ALG-02);
- general sequence/recurrence doctrine (ALG-04);
- Diophantine integer reconstruction canon (NT-04).

## Evidence state

Historical anchors independently verified: `22`, `53`, `50`, `18` for the four validated anchors. Canonical derivations and authored numerical reductions independently checked: PASS. Static render QA: PASS. Classroom timing/readability, retention, and psychometrics: NOT_RUN.
