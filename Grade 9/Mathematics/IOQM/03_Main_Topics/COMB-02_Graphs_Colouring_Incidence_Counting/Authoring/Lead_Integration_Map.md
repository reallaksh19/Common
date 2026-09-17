# COMB-02 Topic-Lead Integration Map

Status: `INTERFACES_COMPLETE_READY_FOR_INTEGRATED_PROSE`

## Learner promise
The learner should first ask whether a graph is the cheapest representation, then reason from adjacency/incidence rather than accumulate terminology:

`DEFINE OBJECTS -> DRAW/MODEL RELATIONS -> CHOOSE DEGREE/COLOR/INCIDENCE VIEW -> COUNT/PROVE -> CHECK DOUBLE COUNT`.

## Integrated order
1. **Reconnect: representation before vocabulary** — turn people/points/positions into vertices and relations into edges only when that loses no needed information.
2. **Degree and handshaking** — every edge contributes two incidences; direct edge count vs degree sum.
3. **Proper vertex colouring** — restricted assignments, local adjacency constraints, sequential choices only after the graph is defined.
4. **Cyclic/local-distance colouring** — graph powers and wrap-around constraints; linear sequence vs cyclic closure.
5. **Grid and knight graphs** — encode legal moves as edges; directed move count then halve only when each unordered edge is counted twice.
6. **Incidence double counting** — regions/intersections/cevians or point-line incidences; define the incidence object before counting it two ways.
7. **Edge colouring and Ramsey-style inevitability** — local degree forcing, monochromatic triangle avoidance, structural inevitability rather than raw enumeration.
8. **Mixed transfer** — decide whether the surface is counting, colouring, incidence, or game/state; route game strategy away from COMB-02.

## Teach once globally
- vertex/edge/degree meaning;
- graph modelling is optional representation, not mandatory jargon;
- handshaking `sum degrees = 2|E|`;
- proper colouring means adjacent vertices receive different colours;
- every double count must name the same set of incidences twice.

## Retrieve, do not reteach
From COMB-01: define the counted object, disjoint/exhaustive cases, multiplication/addition principles, ordered-vs-unordered distinction, complement/IE boundary, state/restriction vocabulary.

## Mandatory contrast placements
- unrestricted colour assignments vs proper colouring: first colouring lesson;
- direct edge enumeration vs degree sum: handshaking lesson;
- ordered moves vs unordered knight pairs: grid/knight lesson;
- linear string colouring vs cyclic closure: before 2025-Q29;
- graph state vs adversarial game: transfer boundary;
- brute-force `2^10` edge colourings vs Ramsey forcing: before 2024-Q19.

## Historical anchor placement
### IOQM-2025-Q08 = 48
Early proper-colouring anchor. Model the quadrilateral plus diagonal as `K4` minus one edge; colour sequentially using adjacency constraints, not unrestricted `4^4` assignments.

### IOQM-2024-Q09 = 48
Handshaking/grid anchor. Count directed knight moves on the 5x5 grid by displacement classes, then halve because each unordered legal pair is counted from both endpoints.

### IOQM-2024-Q19 = 12
Ramsey-style edge-colouring anchor. Fix colours incident to one vertex; triangle avoidance forces the remaining pattern toward a 5-cycle structure. Use inevitability, not raw `2^10` search.

### IOQM-2023-Q16 = 94
Forbidden-subgraph colouring anchor. Red polygon sides constrain which diagonal edges may be blue; count colourings by identifying the forbidden all-blue triangles in the diagonal graph.

### IOQM-2023-Q22 = 77
Incidence anchor. Convert “exactly nine regions” into the required interior-intersection/concurrency pattern among cevians; count peg choices after the incidence condition is characterized.

### IOQM-2025-Q29 = 19
Late cyclic-colouring transfer. Model the local distance-four restriction as a colouring of `C_n^4`; cyclic closure is the key distinction from a linear word.

## Recognition Lab targets
- identify when a graph model removes irrelevant geometry;
- choose direct edge count vs degree sum;
- distinguish unrestricted assignment from proper colouring;
- detect ordered-vs-unordered move counting;
- identify one incidence set that can be counted in two ways;
- distinguish static graph constraint from adversarial game state.

## First-Line Lab targets
- “vertices = ..., edges = ...” modelling sentence;
- `sum_v deg(v)=2|E|`;
- write adjacency restrictions before colour counting;
- define the directed move count before halving;
- define the incidence pair `(object, relation)` before double counting;
- fix one vertex and apply pigeonhole/degree forcing in Ramsey surfaces.

## F0 -> F4 ladder
- F0: identify vertices/edges and compute degrees.
- F1: proper colouring on paths/cycles/small graphs.
- F2: handshaking and grid/knight pair counts.
- F3: incidence and edge-colouring arguments with reduced scaffolding.
- F4: cyclic graph powers, forbidden-subgraph and changed-surface inevitability problems.

## H0 mastery design
First attempt unlabelled/unhinted. Include:
- one modelling-only item;
- one degree/handshaking item;
- one proper-colouring count;
- one grid/knight incidence item;
- one incidence double count;
- one Ramsey/forbidden-subgraph explanation;
- one WHY-NOT item contrasting graph state with game strategy.

## Teacher diagnostic codes
- `MODEL_LOSES_CONSTRAINT`
- `UNRESTRICTED_ASSIGNMENT_USED`
- `EDGE_DOUBLE_COUNT_MISSED`
- `ORDERED_UNORDERED_CONFUSED`
- `CYCLIC_CLOSURE_MISSED`
- `INCIDENCE_SET_NOT_DEFINED`
- `RAMSEY_BRUTE_FORCE`
- `GAME_STATE_MISROUTED`

## Source and publication gates
Historical mathematics: 6/6 PASS. Stable source IDs and independent numerical traces are recorded. Before ready-for-review: exact source/figure custody where a historical geometry surface is promoted, authored-item key verification, frozen metadata, integrated prose, practice/mastery, teacher key, canonical PDFs with hash/blob/page count and page-by-page visual QA. Classroom timing/retention/psychometrics remain `NOT_RUN`.
