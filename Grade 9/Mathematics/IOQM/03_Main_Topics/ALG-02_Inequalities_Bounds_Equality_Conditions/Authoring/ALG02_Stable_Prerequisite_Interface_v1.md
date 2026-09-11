# ALG-02 - Stable Prerequisite Interface v1

Status: `FROZEN_FOR_DOWNSTREAM_CONSUMPTION_CONTENT_PATCH_RENDER_PENDING`

Canonical owner: `IOQM-G9-ALG-02`.

## Downstream may assume

A learner who has completed ALG-02 can:

1. distinguish a lower bound from a minimum and an upper bound from a maximum;
2. inspect the requested domain before selecting an inequality;
3. interpret absolute value as distance and translate `|u|<d`, `|u|<=d`, `|u|>d`, `|u|>=d` with the correct interval/union and endpoint discipline;
4. solve nested absolute-value inequalities from the **outermost** absolute value inward;
5. count integer solutions only after the real interval/union is established;
6. match inequality direction to the requested extremum;
7. use AM-GM with its positivity and equality hypotheses visible;
8. use Cauchy/Engel when its reciprocal/sum structure actually reduces the target;
9. complete a square to expose a quadratic bound and equality point;
10. separate `BOUND`, `EQUALITY`, and `ATTAINMENT`;
11. reject a real equality point that is inadmissible in an integer/discrete domain;
12. apply a discrete filter only after the continuous structure is understood;
13. distinguish absolute-value interval solving, inequality optimization and root-existence requests owned by ALG-03.

## Canonical router

`REQUEST -> DOMAIN -> REPRESENTATION -> [INTERVAL / BOUND] -> CONDITIONS -> ATTAINMENT / DISCRETE FILTER -> CHECK`

## Downstream retrieval contract

Other topics may `RECALL`, `CHECK`, `BRIDGE`, or `ROUTE_BACK` to this interface. They must not independently rebuild absolute-value interval canon or AM-GM/equality/attainment canon.

ALG-07 may retrieve solved real intervals before applying floor/ceiling or integer-counting machinery when that discrete-function structure becomes primary.

## Explicit non-exports

This interface does not export:
- Vieta or discriminant derivations;
- polynomial root/remainder theory;
- Diophantine reconstruction canon;
- geometry-specific feasibility canon.

## Evidence state

- historical anchors independently verified: PASS (`IOQM-2025-Q07=46`, `IOQM-2024-Q06=06`);
- authored numerical/equality cases independently checked: PASS;
- absolute-value enrichment mathematics: PASS_STATIC;
- previous rendered PDF certification: INVALIDATED_BY_LEARNER_SOURCE_CHANGE;
- recertified static render QA: PENDING;
- classroom timing/readability: NOT_RUN;
- longitudinal retention: NOT_RUN;
- psychometrics: NOT_RUN.
