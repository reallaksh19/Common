# Core1 — compact notes (Motion in two dimensions: vector representation and subtraction; relative velocity in a plane)

Status: **CANDIDATE**. Core1 is defined as "existing compact basic notes; preserve existing/frozen material" (V3B-Pending-Activity-Handover.md). No frozen Core1 for this topic exists in the repository, so this is a condensed instantiation drawn directly from the reviewed Core1A content produced in this run (`publication/CORE1A.html`), not a separate research effort. It carries the same review status as Core1A: author-created, scientific/pedagogical review pending.

## Vector representation and subtraction (MEDIUM)

- Declare axis directions before reading any signed component; a component's sign only means something once positive directions are stated (e.g. east positive x, north positive y).
- A vector's **magnitude** (nonnegative) and its **signed components** are two different descriptions of the same quantity. Magnitude = sqrt(x² + y²) (right-triangle bridge). Magnitude alone never answers a direction question.
- Vector subtraction is addition of the reversed second vector: **P − Q = P + (−Q)**. Reversing a vector keeps its length and flips both signed components. Free vectors may be translated (not rotated) for the tail-to-head construction.
- Worked anchor: P = (6,0) m/s, Q = (0,8) m/s → P − Q = (6,−8) m/s, magnitude 10 m/s. The graphical and component routes must agree.

## Relative velocity in a plane (HARD)

- "A relative to B" comes from same-time positions: r_A/B = r_A − r_B (path origin → B → A, then subtract r_B from both sides).
- For constant velocities over a common interval: **v_A/B = v_A − v_B**. Conditions: same observation times and interval; parallel, nonrotating axes; classical (non-relativistic) model.
- Worked anchor: A at (6,0) m/s, B at (0,8) m/s → v_A/B = (6,−8) m/s, magnitude 10 m/s, direction southeast.
- Reversal: v_B/A = −(v_A/B). Same magnitude, opposite direction; v_A/B + v_B/A = 0 is a standing check.
- Labelled extension (beyond baseline scope): a three-object composition (e.g. swimmer relative to water + water relative to ground) uses **addition**, not the subtraction drilled above — identify which relation applies before calculating.
- Explicitly out of scope here (research-boundary note only, not assessed): rotating reference frames (Coriolis terms) and relativistic velocity addition — see `MIC-FRAME-QUALIFICATION-BOUNDARY` in the microtopic library.

## Curriculum status

CBSE 2026–27 Advanced track: background context only (Chapter 2, sections 2.2–2.4). No exact CBSE curriculum-authority binding exists for quantitative two-dimensional relative velocity; it is carried as `OWNER_EXTENSION`, not confirmed prescribed board content. See `registry/physics-curriculum-scope-bindings.v1.json` (PR #350 lineage) for the same fail-closed posture on the parallel track.
