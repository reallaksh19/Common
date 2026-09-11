# IOQM Grade 9 — Canonical Overlap Ownership v1

Status: `FROZEN_FOR_MAIN_TOPIC_PRODUCTION`

Purpose: prevent duplicate teaching, inconsistent terminology and prerequisite inversion when a mechanism appears in several domains.

## Rule

Every reusable mechanism has exactly one **canonical teaching owner**. Other topics may retrieve, bridge or apply it, but must not independently rebuild the full teaching sequence unless the ownership file is explicitly revised.

## Core ownership matrix

| Mechanism / overlap | Canonical owner | Other topics may do | Other topics must not do |
|---|---|---|---|
| divisibility / gcd / lcm / Euclidean algorithm | `NT-01` | retrieve, apply to Diophantine/digit/game problems | reteach full gcd/lcm theory |
| modular arithmetic / residue legality / power cycles | `NT-02` | apply residues/cycles in digits and games | create separate canonical congruence chapter |
| prime factorisation / divisor count / perfect powers | `NT-03` | use exponent patterns in Diophantine/counting | duplicate FTA/divisor-count derivation |
| integer reconstruction / Diophantine filtering | `NT-04` | use as bridge in geometry/algebra | treat every integer constraint as separate ad hoc casework doctrine |
| place value / digit divisibility / carrying / concatenation | `NT-05` | COMB-01 may count strings once the arithmetic constraint is formed | duplicate place-value/divisibility derivation in counting |
| strategic algebraic transformation / equivalence discipline | `ALG-01` | all algebra/NT topics may retrieve | reteach general manipulation principles from scratch |
| AM-GM / inequality direction / equality / attainment | `ALG-02` | geometry/NT may apply | independently teach optimization doctrine |
| Vieta / discriminant / roots / polynomial remainder/reduction | `ALG-03` | geometry/NT may retrieve or apply | create another canonical Vieta/discriminant derivation |
| AP/GP / algebraic sequence notation / recurrence transformation | `ALG-04` | COMB-03 may use a minimal bridge | turn counting-state recurrences into a second sequence textbook |
| strategic functional-equation substitution | `ALG-05` | ALG-01 principles may be retrieved | import abstract function theory not required by IOQM mechanisms |
| exponent/radical/log reversible transforms + domain | `ALG-06` | other topics may use verified identities | duplicate principal-root/domain doctrine |
| floor/ceiling interval translation / discrete filtering | `ALG-07` | NT/COMB may use as final filter | reteach floor theory locally |
| triangle feasibility / metric relations / cevians | `GEO-01` | NT may apply integer filtering; ALG may support algebra | duplicate triangle-metric canon elsewhere |
| angle chasing / polygon structure | `GEO-02` | GEO-04 may retrieve angle facts | rebuild basic angle/polygon doctrine in circle book |
| similarity / ratio / area / centroid | `GEO-03` | GEO-01/GEO-04 may apply | duplicate similarity/area canon |
| circles / cyclicity / tangency / power of point | `GEO-04` | GEO-01/GEO-05 may use as transfer surface | build independent circle theorem set elsewhere |
| coordinate/vector/mensuration as representation choice | `GEO-05` | other geometry topics may offer it as alternate route | force coordinates as universal first method |
| basic counting / restrictions / complement / IE | `COMB-01` | digit/graph/state topics may retrieve | duplicate basic counting canon |
| graphs / colouring / incidence / handshaking | `COMB-02` | games/extremal may use graph models | independently reteach graph basics |
| counting recurrences / tilings / deterministic state evolution | `COMB-03` | ALG-04 bridge for recurrence notation | conflate deterministic state counting with adversarial games |
| adversarial games / invariants / monovariants | `COMB-04` | use NT residues/parity as invariant material | reteach modular arithmetic as if owned here |
| pigeonhole / extremal selection | `COMB-05` | geometry/NT may use as transfer surfaces | bury pigeonhole as an incidental trick inside another topic |

## Cross-domain decision rules from the 90-question reconciliation

### Integer geometry

Geometry owns when feasibility/metric structure is decisive. `NT-04` supplies integer/factor filtering as a bridge.

### Digit counting

`COMB-01` owns when the decisive task is counting admissible strings. `NT-05` owns when place value/divisibility/carry structure is decisive.

### Polynomial + recurrence

`ALG-03` owns quotient/coefficient/root algebra. `COMB-03` owns counting-state recurrence. `ALG-04` owns algebraic sequence/recurrence teaching.

### Inequalities in geometry

Geometry owns when the inequality merely proves a geometric feasibility/metric fact. `ALG-02` owns when bound/equality/attainment is the learning target.

### Vieta in geometry

Geometry may own the historical problem if geometry reconstructs the quantities and Vieta only packages symmetric data. Canonical Vieta teaching remains `ALG-03`.

### Modular digit problems

`NT-05` owns decimal/place-value structure; `NT-02` owns pure residue-cycle structure.

### State search vs games

`COMB-03` owns deterministic shortest-path/state evolution. `COMB-04` owns adversarial optimal-play or invariant-game reasoning.

### Extremal geometry/combinatorics

`COMB-05` owns when the extremal selection principle is decisive. Geometry owns when metric/incidence feasibility is decisive.

## Retrieval contract

When a topic uses another owner's mechanism, the student-facing material should do one of:

- `RECALL`: state the needed fact in one line;
- `CHECK`: ask a retrieval question before use;
- `BRIDGE`: give the minimum missing connection;
- `ROUTE_BACK`: point to the canonical topic if the learner cannot reconstruct the prerequisite.

Do not repeat a full concept map, derivation, hint ladder and mastery cycle for the borrowed mechanism.

## Historical question ownership

Primary historical `main_topic_id` remains a **counting/coverage owner**, not a prohibition against cross-domain teaching. Secondary tags can support transfer maps and contrast sets but cannot inflate recurrence denominators.

## Medium-confidence ownership set

The 41 medium-confidence items remain eligible for second-route review during each topic's Wave 0/1. A topic lead may propose a primary-owner change only with:

1. exact source ID;
2. independent solution route;
3. decisive mechanism argument;
4. impact on both old and new topic coverage;
5. no denominator inflation.

Until accepted, the current reconciliation owner remains authoritative.

## Gate

`CANONICAL_OVERLAP_OWNERSHIP_FROZEN__SECOND_ROUTE_REVIEW_ALLOWED_WITH_CHANGE_CONTROL`