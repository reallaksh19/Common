# ALG-02 - Stable Prerequisite Interface v1

Status: `FROZEN_FOR_DOWNSTREAM_CONSUMPTION`

Canonical owner: `IOQM-G9-ALG-02`.

## Downstream may assume

A learner who has completed ALG-02 can:

1. distinguish a lower bound from a minimum and an upper bound from a maximum;
2. inspect the requested domain before selecting an inequality;
3. match inequality direction to the requested extremum;
4. use AM-GM with its positivity and equality hypotheses visible;
5. use Cauchy/Engel when its reciprocal/sum structure actually reduces the target;
6. complete a square to expose a quadratic bound and equality point;
7. separate `BOUND`, `EQUALITY`, and `ATTAINMENT`;
8. reject a real equality point that is inadmissible in an integer/discrete domain;
9. apply a discrete filter only after the continuous structure is understood;
10. distinguish an inequality/optimization request from a root-existence request owned by ALG-03.

## Canonical router

`REQUEST -> DOMAIN -> BOUNDED? -> DIRECTION -> REPRESENTATION -> BOUND -> EQUALITY -> ATTAINMENT -> DISCRETE FILTER -> CHECK`

## Downstream retrieval contract

Other topics may `RECALL`, `CHECK`, `BRIDGE`, or `ROUTE_BACK` to this interface. They must not independently rebuild AM-GM/equality/attainment canon.

## Explicit non-exports

This interface does not export:
- Vieta or discriminant derivations;
- polynomial root/remainder theory;
- Diophantine reconstruction canon;
- geometry-specific feasibility canon.

## Evidence state

- historical anchors independently verified: PASS (`IOQM-2025-Q07=46`, `IOQM-2024-Q06=06`);
- authored numerical/equality cases independently checked: PASS;
- static render QA: PASS;
- classroom timing/readability: NOT_RUN;
- longitudinal retention: NOT_RUN;
- psychometrics: NOT_RUN.
