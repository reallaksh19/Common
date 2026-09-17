# COMB-01 - Concept and Dependency Map

Status: `STATIC_SOURCE_AUTHORING`
Canonical owner: `IOQM-G9-COMB-01`

## Governing belief

`DEFINE THE OBJECT -> ORDERED OR UNORDERED? -> RESTRICTIONS -> DISJOINT CASES OR STAGES -> DIRECT / COMPLEMENT / IE -> COUNT -> DOUBLE-COUNT CHECK`

Counting is not formula matching. A count is valid only after the counted object and its identity are fixed.

## Canonical scope

Owned here:
- addition principle with explicit disjointness;
- multiplication principle with explicit sequential-stage semantics;
- permutation and combination derived from ordered/unordered structure;
- repeated-object identity and multiset arrangements;
- restrictions and position constraints;
- complement counting;
- inclusion-exclusion for overlapping properties;
- digit-string counting when the task is to count admissible strings/numbers.

Retrieved / not duplicated:
- arithmetic digit properties, divisibility and place-value algebra belong to `IOQM-G9-NT-05` when arithmetic structure is the learning target;
- recurrence/state evolution belongs to `IOQM-G9-COMB-03`; this topic exports counting/model language to it;
- graph coloring and forbidden-subgraph canon belong to `IOQM-G9-COMB-02`;
- advanced group-action/Burnside formalism is not introduced; the 2023 dice anchor is handled by fixing a rotational frame and counting representatives.

## Dependency graph

Prerequisites: integer arithmetic, factorial notation, elementary set language.
Downstream consumers: `IOQM-G9-COMB-02`, `IOQM-G9-COMB-03`, selected NT/GEO applications.
Stable provider interface: `Authoring/COMB01_Stable_Counting_Model_Interface_v1.md`.

## Seven production microstreams

1. addition and multiplication principles;
2. permutation/combination derivation;
3. repeated objects and identity;
4. restrictions and position constraints;
5. complement and inclusion-exclusion;
6. digit-string counting and NT-05 boundary;
7. source/PYQ/misconception audit.
