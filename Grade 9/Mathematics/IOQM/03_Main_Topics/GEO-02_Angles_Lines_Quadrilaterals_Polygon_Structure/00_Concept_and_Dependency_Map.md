# GEO-02 - Concept and Dependency Map

Main topic: Angles, Lines, Quadrilaterals & Polygon Structure

## Governing learner router

**PROVE THE STRUCTURE -> choose LOCAL or GLOBAL angle accounting -> use a diagonal only when it reduces unknowns -> use symmetry only after proof -> switch representation only when cheaper.**

## Boundary and ownership

### Canonical teaching here
- angle chasing on lines and at vertices;
- parallel-line angle structure and converses;
- quadrilateral angle structure;
- regular-polygon interior/exterior angles;
- diagonal counting and diagonal-based decomposition;
- symmetry recognition with proof obligations.

### Retrieval/application only
- basic triangle angle sum and elementary Euclidean facts: prerequisite retrieval;
- coordinate/vector calculations: alternate representation only; canonical representation teaching belongs to GEO-05;
- triangle-feasibility inequalities in the trapezium anchor: minimum bridge only; canonical teaching belongs to GEO-01.

### Explicitly excluded
- cyclic quadrilateral theorems;
- tangent, chord, power-of-a-point and circle-angle canon;
- full coordinate/vector doctrine.

## Learner-state map

| Node | Likely learner state | Missing bridge | Ownership target |
|---|---|---|---|
| Straight-line and vertical angles | partly familiar | chain without losing orientation | local angle accounting |
| Parallel lines | remembers angle names | theorem vs converse | proof discipline |
| Quadrilateral sum | remembers 360 degrees | reconstruct and choose when useful | structural use |
| Regular polygons | may remember formula | exterior-turn derivation | local/global switch |
| Diagonals | sees clutter | use as decomposition/counting tool | split/reassemble |
| Symmetry | trusts drawing | prove before use | visual-assumption discipline |
| Coordinates | fallback reflex | compare method cost | representation boundary |

## Dependency graph

```text
elementary angles -> line/vertical relations -> parallel theorem/converse
-> triangle-angle retrieval -> quadrilateral decomposition
-> regular-polygon turn structure -> diagonals/proved symmetry -> mixed selection
```

## Method-selection map

| Surface | Route | Competing route | Boundary question |
|---|---|---|---|
| few labelled angles | local chase | polygon formula | Can two or three local relations close it? |
| regular n-gon | global turn formula | vertex-by-vertex chase | Does regularity make every turn identical? |
| quadrilateral plus diagonal | split into triangles | coordinates | Does the split expose known angles immediately? |
| lengths plus fixed directions | coordinate/vector application | synthetic chase | Is angular information too weak for a short chase? |
| symmetric-looking sketch | prove symmetry first | visual assumption | What stated fact forces the symmetry? |
| trapezium side set | feasibility before counting | enumerate drawings | Can the legs span the base difference with positive height? |

## Transfer map
- local chase -> polygon vertex reasoning;
- quadrilateral split -> polygon triangulation;
- exterior turn -> integer/divisibility filtering;
- proved symmetry -> diagonal incidence counting;
- synthetic network <-> coordinate direction computation;
- trapezium geometry -> discrete counting only after feasibility.

## Contrast inventory
1. local chase vs global polygon formula;
2. theorem vs converse for parallels;
3. generic quadrilateral vs special quadrilateral;
4. regular polygon vs merely equiangular polygon;
5. useful diagonal vs needless diagonal;
6. synthetic vs coordinate/vector representation;
7. visually apparent symmetry vs proved symmetry;
8. reflection vs rotational symmetry;
9. all chord pairs vs diagonal pairs;
10. geometry feasibility first vs integer enumeration first.

## Source custody
Validated anchors: IOQM-2025-Q13, IOQM-2024-Q04, IOQM-2023-Q06, IOQM-2023-Q24, IOQM-2023-Q25. All five have independently verified answers and `figure_required=false` in the production package.
