# Paired-Launch Endpoint and Tower-Time QA

Use this checkpoint set when two vertical launches begin from the same level with equal speed magnitude but opposite directions, especially same-impact-speed and paired tower-time questions.

These checks are additive to source fidelity, gravity/sign QA, model-gate checks, and artifact separation.

## AD-73 ENDPOINT-SPEED MAGNITUDE INTEGRITY

When the ideal constant-g model compares two bodies launched from the same level with equal initial speed magnitude `|u|` and observed at one common lower level, preserve the source distinction:

- the journeys and travel times can differ;
- the final **speed magnitudes** can match;
- the equality follows from the no-time relation because `(+u)^2 = (-u)^2` and the net vertical displacement to the common endpoint is the same;
- do not publish the result as equal velocity unless direction/sign is also established;
- keep the negligible-air-resistance / constant-g model gate visible when the source relies on it.

Fail if the page implies that equal impact speed means equal path length, equal time, or identical velocity vectors.

## AD-74 PATH-LENGTH VS NET-DISPLACEMENT GATE

For endpoint speed under ideal constant acceleration, the no-time relation uses net displacement, not total path length.

Required checks:

- identify the common endpoint height difference explicitly;
- do not replace the vertical displacement term with the longer travelled path of the upward-launched body;
- if a teacher-added figure shows different routes, label them as different histories while keeping the endpoint relation separate;
- if air resistance or dissipation is introduced, mark the model change before claiming path independence.

Fail if a longer route is presented as a reason for a larger final speed in the ideal no-resistance model.

## AD-75 SAME-STATE TIME-SHIFT INTEGRITY

For equal-magnitude upward and downward launches from the same tower level, the upward-launched body contains two extra symmetric legs before it matches the downward launch's initial state:

1. rise to the top: `u/g`;
2. return to the launch level: `u/g`;
3. at return, same position and downward speed magnitude `u`;
4. therefore the later trajectory is a time-shifted copy of the downward-launched trajectory;
5. extra time = `2u/g`.

Fail if the publication counts only the ascent and states an extra time of `u/g`.

## AD-76 PAIRED-TIME SHORTCUT DOMAIN

The geometric-mean result `t0 = sqrt(t1 t2)` is a conditional shortcut, not a universal tower formula.

Publish it only when the source/setup supports all of the following:

- same launch point / tower height;
- same final endpoint;
- equal launch-speed magnitudes used once upward and once downward;
- same constant gravitational acceleration;
- ideal vertical motion under the same model assumptions;
- `t0` is explicitly defined as the drop-from-rest time from the same point to the same endpoint.

Use true radical typography in the student PDF. Do not silently apply the result to unequal launch speeds, different endpoints, or a changed acceleration model.

## Required review sequence

1. Freeze the two launch directions, equal `|u|`, common start, and common endpoint.
2. Verify that the endpoint-speed relation uses net displacement, not path length.
3. Verify the state-matching timeline contains both `u/g` legs.
4. Check that the `2u/g` result is visually tied to the matched state.
5. For `t0 = sqrt(t1 t2)`, state the shortcut domain near the relation or in an adjacent model gate.
6. Inspect speed-vs-velocity wording and all radicals at normal viewing size.
7. Record `endpoint_speed_magnitude_findings = 0`, `path_displacement_findings = 0`, `same_state_shift_findings = 0`, and `paired_time_domain_findings = 0` before release.
