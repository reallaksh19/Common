# Graph and Signed-Area QA

Use this checkpoint set whenever a student-facing batch contains graphs whose geometry carries physics meaning, especially motion graphs.

## AD-30 GRAPH SEMANTIC FIDELITY

A graph is not preserved merely because axes and a line are present. Verify that the rendered figure preserves the source semantics:

- axis identity and direction;
- origin/zero line placement where relevant;
- endpoint values and labels;
- straight versus curved shape;
- slope sign and whether slope is constant;
- zero crossings;
- shaded regions and what each region represents;
- time ordering;
- any midpoint, intercept, tangent, or stage boundary used by the explanation.

For reconstructed/redrawn graphs, create a semantic manifest before drawing. Example:

```text
figure: v-t constant-acceleration area
x-axis: time

y-axis: velocity
line: straight from u to v
rectangle region: ut
triangle region: 1/2 at^2
meaning of total signed area: displacement
```

Fail the batch if a graph is visually attractive but changes any of these relationships.

## AD-31 SIGNED-AREA / REVERSAL INTEGRITY

When velocity can cross zero, the learner must be able to distinguish displacement from distance.

Check that:

- the zero-velocity line is visually identifiable;
- area above zero and below zero are distinguishable;
- negative area is not accidentally shown as positive displacement;
- a displacement result is not labelled total distance;
- if distance is asked, the page instructs the learner to split at the zero crossing and combine absolute path/area contributions;
- any midpoint-average shortcut is not presented as a distance shortcut across reversal.

If the source intentionally asks the learner to draw the graph, preserve that omission in independent transfer. A neutral axis frame may be added only if it does not reveal the answer.

## AD-32 GRAPH-TO-EQUATION LINKAGE

Whenever a formula is being justified by a graph, the corresponding visual quantity must be visibly connected to the mathematical term.

Examples:

- rectangle area ↔ `ut`;
- triangle area ↔ `1/2 at^2`;
- straight v-t ramp ↔ `(u+v)/2` average;
- curved v-t graph ↔ warning that endpoint midpoint is not generally the true time-average;
- equal displacement blocks ↔ equal changes in `v^2` under constant acceleration.

Fail if the formula is shown but the graph does not make the claimed term/relationship visible, or if the graph labels are too small to read at normal viewing size.

## Required review sequence

1. Render every graph-heavy page.
2. Compare each graph against its semantic manifest.
3. Inspect zero crossings and signed regions at 100%.
4. Check graph labels at normal student viewing size.
5. Confirm any graph-derived equation is visually linked to the relevant region/slope/endpoint relationship.
6. Record `graph_semantic_findings = 0` and `signed_area_findings = 0` before release.
