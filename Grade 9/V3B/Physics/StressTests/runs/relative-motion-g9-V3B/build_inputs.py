#!/usr/bin/env python3
"""Build source.json / baseline.json / plan.json for the Grade 9 CBSE Advanced
relative-motion vertical slice (V3B-Motion-Grade9-Example.md executed against
V3B-Stress-Test-Prompt-Template.md, request_id STRESS-PHY-RELATIVE-MOTION-G9-V3B).

Content is adapted from the reviewed candidate microtopic library:
  V3B-Vector-Representation-Library-Seed.json  (BUCKET-VECTOR-REPRESENTATION, MEDIUM)
  V3B-Relative-Motion-Library-Seed.json        (BUCKET-RELATIVE-MOTION, HARD)
Author-created; no independent scientific/pedagogical acceptance is claimed by
running this script. Run with:
  python3 'Grade 9/V3B/Physics/StressTests/runs/relative-motion-g9-V3B/build_inputs.py'
"""
import hashlib
import json
import sys
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
REPO_ROOT = RUN_DIR.parents[5]
sys.path.insert(0, str(REPO_ROOT / "Grade 9" / "V3B" / "Shared"))
from v3b.contracts import digest  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def atom(id_, value, unit, locator):
    return dict(id=id_, value=value, unit=unit, kind="DATUM", locator=locator)


def equation_atom(id_, mathml, locator):
    return dict(id=id_, value=mathml, kind="EQUATION", locator=locator)


EQ_VEC_SUBTRACT = ('<math display="block"><mrow><mi>P</mi><mo>-</mo><mi>Q</mi><mo>=</mo>'
                    '<mi>P</mi><mo>+</mo><mo>(</mo><mo>-</mo><mi>Q</mi><mo>)</mo></mrow></math>')
EQ_RELV = ('<math display="block"><mrow><msub><mi>v</mi><mrow><mi>A</mi><mo>/</mo><mi>B</mi></mrow></msub>'
           '<mo>=</mo><msub><mi>v</mi><mi>A</mi></msub><mo>-</mo><msub><mi>v</mi><mi>B</mi></msub></mrow></math>')


# ---------------------------------------------------------------------------
# Source atoms (AUTHOR_CREATED; every atom must be referenced by >=1 obligation)
# ---------------------------------------------------------------------------
ATOMS = [
    # BUCKET-VECTOR-REPRESENTATION
    atom("w_x", 3, "m/s", "Author-created intro vector w, x-component (east positive)"),
    atom("w_y", 4, "m/s", "Author-created intro vector w, y-component (north positive)"),
    atom("p_x", 6, "m/s", "Author-created vector P, x-component"),
    atom("p_y", 0, "m/s", "Author-created vector P, y-component"),
    atom("q_x", 0, "m/s", "Author-created vector Q, x-component"),
    atom("q_y", 8, "m/s", "Author-created vector Q, y-component"),
    atom("pq_x", 6, "m/s", "P - Q, x-component (declared result of the graphical/component construction)"),
    atom("pq_y", -8, "m/s", "P - Q, y-component (declared result of the graphical/component construction)"),
    # BUCKET-RELATIVE-MOTION -- canonical arithmetic control (matches Q-AUTHOR-REL-01 / V3B-Motion-Grade9-Example.md)
    atom("va_x", 6, "m/s", "Author-created velocity of A, x-component, common east/north frame"),
    atom("va_y", 0, "m/s", "Author-created velocity of A, y-component, common east/north frame"),
    atom("vb_x", 0, "m/s", "Author-created velocity of B, x-component, common east/north frame"),
    atom("vb_y", 8, "m/s", "Author-created velocity of B, y-component, common east/north frame"),
    atom("vab_x", 6, "m/s", "A relative to B, x-component (declared subtraction result)"),
    atom("vab_y", -8, "m/s", "A relative to B, y-component (declared subtraction result)"),
    # reversed observer
    atom("vba_x", -6, "m/s", "B relative to A, x-component (reversed observer)"),
    atom("vba_y", 8, "m/s", "B relative to A, y-component (reversed observer)"),
    # second worked/practice scenario, distinct numbers (5-12-13 triple)
    atom("vm_x", 0, "m/s", "Author-created velocity of M, x-component"),
    atom("vm_y", 13, "m/s", "Author-created velocity of M, y-component"),
    atom("vn_x", 5, "m/s", "Author-created velocity of N, x-component"),
    atom("vn_y", 1, "m/s", "Author-created velocity of N, y-component"),
    atom("vmn_x", -5, "m/s", "M relative to N, x-component (declared subtraction result)"),
    atom("vmn_y", 12, "m/s", "M relative to N, y-component (declared subtraction result)"),
    atom("vnm_x", 5, "m/s", "N relative to M, x-component (reversed observer, transfer case)"),
    atom("vnm_y", -12, "m/s", "N relative to M, y-component (reversed observer, transfer case)"),
    # labelled extension: boat/current (three-object composition, addition form)
    atom("vboat_x", 0, "m/s", "Swimmer velocity relative to water, x-component"),
    atom("vboat_y", 3, "m/s", "Swimmer velocity relative to water, y-component (straight across)"),
    atom("vcurrent_x", 4, "m/s", "Water velocity relative to ground, x-component (current)"),
    atom("vcurrent_y", 0, "m/s", "Water velocity relative to ground, y-component (current)"),
    atom("vresult_x", 4, "m/s", "Swimmer velocity relative to ground, x-component (declared composition result)"),
    atom("vresult_y", 3, "m/s", "Swimmer velocity relative to ground, y-component (declared composition result)"),
    # equations (REL-VECTOR-SUBTRACTION / REL-RELATIVE-VELOCITY from the microtopic library)
    equation_atom("eq_vec_subtract", EQ_VEC_SUBTRACT,
                  "REL-VECTOR-SUBTRACTION, V3B-Vector-Representation-Library-Seed.json"),
    equation_atom("eq_relv", EQ_RELV, "REL-RELATIVE-VELOCITY, V3B-Relative-Motion-Library-Seed.json"),
]

# ---------------------------------------------------------------------------
# Source questions
# ---------------------------------------------------------------------------
def q(id_, number, stem, conditions=None, verification=None):
    row = dict(id=id_, original_number=number, stem=stem, conditions=conditions or [])
    if verification:
        row["verification"] = verification
    return row


QUESTIONS = [
    q("Q-VEC-A1", "AUTHOR-VEC-01",
      "A cyclist's velocity has components 3 m/s east and 4 m/s north in a common east/north frame. "
      "Find the cyclist's speed and describe the direction in words.",
      ["Constant velocity; common east/north frame."],
      dict(validator_id="SPEED_FROM_COMPONENTS", bindings=dict(vx="w_x", vy="w_y"))),
    q("Q-VEC-A2", "AUTHOR-VEC-02",
      "A vector P has components (6, 0) m/s in an east/north frame. State its x- and y-components and "
      "explain why the y-component is zero rather than undefined.",
      ["Same east/north frame as Q-VEC-A1."]),
    q("Q-VEC-B1", "AUTHOR-VEC-03",
      "In a common east/north frame, P = (6, 0) m/s and Q = (0, 8) m/s. Construct P - Q graphically "
      "(reverse Q, then add tail-to-head) and state the resultant's components and magnitude.",
      ["Constant vectors; common east/north frame; free vectors may be translated without rotation."],
      dict(validator_id="SPEED_FROM_COMPONENTS", bindings=dict(vx="pq_x", vy="pq_y"))),
    q("Q-RELV-A1", "AUTHOR-REL-01",
      "In a common east/north frame, A moves at (6,0) m/s and B at (0,8) m/s. Find the velocity of A "
      "relative to B. State its direction and magnitude.",
      ["Constant velocities; common time and parallel nonrotating axes."],
      dict(validator_id="SPEED_FROM_COMPONENTS", bindings=dict(vx="vab_x", vy="vab_y"))),
    q("Q-RELV-A2", "AUTHOR-REL-02",
      "In a common east/north frame, M moves at (0,13) m/s and N moves at (5,1) m/s. Find the velocity "
      "of M relative to N. State its direction and magnitude.",
      ["Constant velocities; common time and parallel nonrotating axes."],
      dict(validator_id="SPEED_FROM_COMPONENTS", bindings=dict(vx="vmn_x", vy="vmn_y"))),
    q("Q-RELV-A3", "AUTHOR-REL-03",
      "Using the A/B result above (A relative to B is (6,-8) m/s), find the velocity of B relative to A. "
      "State how its magnitude and direction compare with A relative to B.",
      ["Same frame and instant as AUTHOR-REL-01."],
      dict(validator_id="SPEED_FROM_COMPONENTS", bindings=dict(vx="vba_x", vy="vba_y"))),
    q("Q-RELV-B2", "AUTHOR-REL-04",
      "A swimmer's velocity relative to the water is (0,3) m/s (straight across). The water's velocity "
      "relative to the ground (the current) is (4,0) m/s. Find the swimmer's velocity relative to the "
      "ground, and name which relation you used to combine the two given velocities.",
      ["Constant velocities; common east/north frame; classical (non-relativistic) composition.",
       "Labelled extension: three-object composition, beyond the two-object baseline scope."],
      dict(validator_id="SPEED_FROM_COMPONENTS", bindings=dict(vx="vresult_x", vy="vresult_y"))),
    q("Q-RELV-B3", "AUTHOR-REL-05",
      "Using the M/N result above (M relative to N is (-5,12) m/s), find the velocity of N relative to M "
      "without recomputing from the original velocities of M and N.",
      ["Same frame and instant as AUTHOR-REL-02."],
      dict(validator_id="SPEED_FROM_COMPONENTS", bindings=dict(vx="vnm_x", vy="vnm_y"))),
]

SOURCE = dict(id="AUTHOR", origin="AUTHOR_CREATED",
              citation="V3B relative-motion vertical slice; author-created candidate questions, not CBSE "
                       "examination items (V3B-Stress-Test-Prompt-Template.md Sec.3: BUILD_REVIEW_CORPUS). "
                       "Concept progression and arithmetic control adapted from V3B-Motion-Grade9-Example.md "
                       "and the reviewed candidate microtopic library.",
              atoms=ATOMS, questions=QUESTIONS)

write_json(RUN_DIR / "inputs" / "sources" / "source.json", SOURCE)
source_path = RUN_DIR / "inputs" / "sources" / "source.json"
source_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()

# ---------------------------------------------------------------------------
# Baseline
# ---------------------------------------------------------------------------
CORES = ["CORE1A", "CORE1B", "CORE2A", "CORE2B"]

BUCKETS = [
    dict(id="B-VEC", badge="MEDIUM", prerequisites=[]),
    dict(id="B-RELV", badge="HARD", prerequisites=["B-VEC"]),
]

OBLIGATIONS = [
    dict(id="OB-VEC-CONCEPT", bucket_id="B-VEC", source_atom_ids=["w_x", "w_y"],
         required_cores=["CORE1A", "CORE1B"], required_kinds=["TEXT"]),
    dict(id="OB-VEC-SUBTRACT", bucket_id="B-VEC",
         source_atom_ids=["p_x", "p_y", "q_x", "q_y", "pq_x", "pq_y", "eq_vec_subtract"],
         required_cores=["CORE1A", "CORE1B"], required_kinds=["TEXT", "FIGURE", "EQUATION"]),
    dict(id="OB-VEC-PRACTICE", bucket_id="B-VEC", source_atom_ids=["w_x", "w_y"],
         required_cores=["CORE2A"], required_kinds=["QUESTION"]),
    dict(id="OB-VEC-TRANSFER", bucket_id="B-VEC",
         source_atom_ids=["p_x", "p_y", "q_x", "q_y", "pq_x", "pq_y"],
         required_cores=["CORE2B"], required_kinds=["QUESTION"]),
    dict(id="OB-RELV-DERIVE", bucket_id="B-RELV",
         source_atom_ids=["va_x", "va_y", "vb_x", "vb_y", "vab_x", "vab_y", "eq_relv"],
         required_cores=["CORE1A", "CORE1B"], required_kinds=["TEXT", "EQUATION", "FIGURE"]),
    dict(id="OB-RELV-REVERSAL", bucket_id="B-RELV", source_atom_ids=["vba_x", "vba_y"],
         required_cores=["CORE1A", "CORE1B"], required_kinds=["TEXT"]),
    dict(id="OB-RELV-PRACTICE-1", bucket_id="B-RELV",
         source_atom_ids=["va_x", "va_y", "vb_x", "vb_y", "vab_x", "vab_y"],
         required_cores=["CORE2A"], required_kinds=["QUESTION"]),
    dict(id="OB-RELV-PRACTICE-2", bucket_id="B-RELV",
         source_atom_ids=["vm_x", "vm_y", "vn_x", "vn_y", "vmn_x", "vmn_y"],
         required_cores=["CORE2A"], required_kinds=["QUESTION"]),
    dict(id="OB-RELV-REVERSAL-PRACTICE", bucket_id="B-RELV", source_atom_ids=["vba_x", "vba_y"],
         required_cores=["CORE2A"], required_kinds=["QUESTION"]),
    dict(id="OB-RELV-TRANSFER-N", bucket_id="B-RELV", source_atom_ids=["vnm_x", "vnm_y"],
         required_cores=["CORE2B"], required_kinds=["QUESTION"]),
    dict(id="OB-RELV-EXTENSION-BOAT", bucket_id="B-RELV",
         source_atom_ids=["vboat_x", "vboat_y", "vcurrent_x", "vcurrent_y", "vresult_x", "vresult_y"],
         required_cores=["CORE2B"], required_kinds=["TEXT", "QUESTION"]),
]

REQUIRED_QUESTIONS = [
    dict(core="CORE2A", source_id="AUTHOR", question_id="Q-VEC-A1"),
    dict(core="CORE2B", source_id="AUTHOR", question_id="Q-VEC-B1"),
    dict(core="CORE2A", source_id="AUTHOR", question_id="Q-RELV-A1"),
    dict(core="CORE2A", source_id="AUTHOR", question_id="Q-RELV-A2"),
    dict(core="CORE2A", source_id="AUTHOR", question_id="Q-RELV-A3"),
    dict(core="CORE2B", source_id="AUTHOR", question_id="Q-RELV-B2"),
    dict(core="CORE2B", source_id="AUTHOR", question_id="Q-RELV-B3"),
]

BASELINE = dict(schema_version="1.0.0", topic_id="PHY-M2D-VEC-RELV-G9", baseline_id="BASE-RELATIVE-MOTION-G9-V3B-1",
                selected_cores=CORES,
                sources=[dict(id="AUTHOR", path="sources/source.json", sha256=source_sha256)],
                buckets=BUCKETS, obligations=OBLIGATIONS, required_questions=REQUIRED_QUESTIONS)

write_json(RUN_DIR / "inputs" / "baseline.json", BASELINE)
print("Wrote source.json and baseline.json. Baseline digest:", digest(BASELINE))

# ---------------------------------------------------------------------------
# Plan (Core1A / Core1B / Core2A / Core2B content)
# ---------------------------------------------------------------------------
QUESTIONS_BY_ID = {r["id"]: r for r in QUESTIONS}
FRAME = "common east/north Cartesian frame; east positive x, north positive y"


def text_block(id_, obligations, atoms, body):
    return dict(id=id_, kind="TEXT", obligation_ids=obligations, source_atom_ids=atoms, text=body)


def equation_block(id_, obligations, atoms, mathml, meaning, symbols, conditions):
    return dict(id=id_, kind="EQUATION", obligation_ids=obligations, source_atom_ids=atoms, mathml=mathml,
                meaning=meaning, symbols=symbols, conditions=conditions)


def vector_scene(symbol, unit, x_atom, y_atom, caption):
    return dict(kind="VECTOR", symbol=symbol, unit=unit, x_atom=x_atom, y_atom=y_atom, frame=FRAME,
                x_label=f"x component ({unit})", y_label=f"y component ({unit})", caption=caption)


def figure_block(id_, obligations, atoms, scene, placement=None, question_id=None):
    row = dict(id=id_, kind="FIGURE", obligation_ids=obligations, source_atom_ids=atoms, scene=scene)
    if placement:
        row["placement"] = placement
        row["question_id"] = question_id
    return row


def question_block(id_, obligations, atoms, source_question_id, answer, hints, family, learner_action,
                    exposure_role, guidance=None):
    src = QUESTIONS_BY_ID[source_question_id]
    row = dict(id=id_, kind="QUESTION", obligation_ids=obligations, source_atom_ids=atoms,
               source_id="AUTHOR", source_question_id=source_question_id,
               original_number=src["original_number"], stem=src["stem"],
               subparts=[], options=[], conditions=src.get("conditions", []),
               answer=answer, hints=hints, family=family, learner_action=learner_action,
               exposure_role=exposure_role)
    if guidance:
        row["guidance"] = guidance
    return row


# --- CORE1A --------------------------------------------------------------
core1a_vec = [
    text_block("1A-VEC-T1", ["OB-VEC-CONCEPT"], ["w_x", "w_y"],
        "Before any number is subtracted or added, name the frame. Declare which direction along each "
        "axis counts as positive -- here, east is positive x and north is positive y -- because a signed "
        "component only means something once that choice is fixed.\n"
        "A vector w with components (3, 4) m/s is read directly off those axes: 3 m/s east and 4 m/s "
        "north. The vector and its magnitude are two different descriptions of the same physical "
        "quantity. The magnitude (speed) is obtained by treating the two perpendicular components as "
        "the legs of a right triangle: speed = sqrt(3^2 + 4^2) = sqrt(25) = 5 m/s. Squaring removes the "
        "sign from each component, so the magnitude is always taken nonnegative -- but the original "
        "signed pair (3, 4) is still required afterwards to say which way the vector points. Stating '5 "
        "m/s' alone never answers a direction question."),
    figure_block("1A-VEC-F1", ["OB-VEC-CONCEPT"], ["w_x", "w_y"],
        vector_scene("w", "m/s", "w_x", "w_y", "Vector w, drawn from the origin with its signed components.")),
    text_block("1A-VEC-T2", ["OB-VEC-SUBTRACT"], ["p_x", "p_y", "q_x", "q_y", "pq_x", "pq_y"],
        "Subtraction of two vectors is defined as addition of the reversed second vector: P - Q = "
        "P + (-Q). Reversing Q keeps its length exactly the same and flips its direction end for end; "
        "reversal also flips the sign of every one of its signed components.\n"
        "Take P = (6, 0) m/s and Q = (0, 8) m/s in the common east/north frame. Reversing Q gives "
        "-Q = (0, -8) m/s. As a free vector, -Q may be translated to the head of P without being "
        "rotated. Adding tail-to-head, the resultant is P + (-Q) = (6 + 0, 0 + (-8)) = (6, -8) m/s. This "
        "graphical route must agree with the direct component-by-component subtraction, (P_x - Q_x, "
        "P_y - Q_y) = (6 - 0, 0 - 8) = (6, -8) m/s -- and it does. Applying the right-triangle bridge, "
        "the magnitude is sqrt(6^2 + 8^2) = sqrt(100) = 10 m/s."),
    equation_block("1A-VEC-E1", ["OB-VEC-SUBTRACT"], ["eq_vec_subtract"], EQ_VEC_SUBTRACT,
        "Vector subtraction is defined as addition of the reversed second vector.",
        ["P: the first vector in the declared common frame.",
         "Q: the second vector, expressed in the same frame.",
         "-Q: Q reversed -- identical magnitude, opposite direction."],
        ["P and Q are expressed along the same declared axes.",
         "Free vectors may be translated (not rotated) for the tail-to-head construction."]),
    figure_block("1A-VEC-F2", ["OB-VEC-SUBTRACT"], ["q_x", "q_y"],
        vector_scene("Q", "m/s", "q_x", "q_y", "Q as given. This is the vector that gets reversed in the construction.")),
    figure_block("1A-VEC-F3", ["OB-VEC-SUBTRACT"], ["pq_x", "pq_y"],
        vector_scene("P-Q", "m/s", "pq_x", "pq_y",
                     "The resultant P-Q, reached by adding P and the reversed -Q tail-to-head; it agrees with the direct component subtraction.")),
]

core1a_relv = [
    text_block("1A-RELV-T1", ["OB-RELV-DERIVE"], ["va_x", "va_y", "vb_x", "vb_y", "vab_x", "vab_y"],
        "'A relative to B' is built from same-time positions, not memorised as a bare formula. If r_A "
        "and r_B are the positions of A and B at the same instant in one common frame, then following "
        "the path origin -> B -> A gives r_A = r_B + r_A/B, so r_A/B = r_A - r_B: the position of A "
        "measured from B.\n"
        "Writing this relation at two instants t1 and t2 and subtracting gives Delta r_A/B = Delta r_A - "
        "Delta r_B. Dividing every term by the same nonzero time interval turns each side into an "
        "average velocity; for the constant velocities used in this teaching case, v_A/B = v_A - v_B. "
        "Both displacement changes must be divided by the same shared interval -- comparing changes "
        "measured over different intervals would not describe how one simultaneous separation evolves.\n"
        "Apply this to A moving at (6, 0) m/s and B moving at (0, 8) m/s in a common east/north frame: "
        "v_A/B = (6, 0) - (0, 8) = (6, -8) m/s. By the right-triangle bridge, the magnitude is "
        "sqrt(6^2 + 8^2) = sqrt(100) = 10 m/s. The eastward component is positive and the northward "
        "component is negative, so the vector points southeast."),
    equation_block("1A-RELV-E1", ["OB-RELV-DERIVE"], ["eq_relv"], EQ_RELV,
        "For constant velocities, the relative velocity of A with respect to B is the vector difference "
        "of their common-frame velocities.",
        ["v_A: velocity of A in the common frame.", "v_B: velocity of B in the same frame, same instant.",
         "v_A/B: velocity of A relative to B, i.e. A as measured by an observer moving with B."],
        ["Use the same observation times and a common time interval.",
         "Express all vectors along parallel, nonrotating Cartesian axes.",
         "Use a classical (non-relativistic) kinematic model."]),
    figure_block("1A-RELV-F1", ["OB-RELV-DERIVE"], ["vab_x", "vab_y"],
        vector_scene("v_A/B", "m/s", "vab_x", "vab_y",
                     "The resultant relative-velocity vector A relative to B, reconciled with the component calculation above.")),
    text_block("1A-RELV-T2", ["OB-RELV-REVERSAL"], ["vba_x", "vba_y"],
        "Swapping the observer reverses the vector: v_B/A = -(v_A/B). Since A relative to B is "
        "(6, -8) m/s, B relative to A is (-6, 8) m/s -- every component changes sign. The magnitude is "
        "unchanged, because the right-triangle bridge only uses squared components, and squaring erases "
        "a sign flip: sqrt((-6)^2 + 8^2) = sqrt(100) = 10 m/s, matching the original 10 m/s. Adding the "
        "two relative vectors together gives exactly zero, which is a standing check for this reversal "
        "relation on any pair of velocities."),
]

core1a = [dict(core="CORE1A", units=[
    dict(id="U-1A-VEC", bucket_id="B-VEC", title="Vector representation and subtraction", blocks=core1a_vec),
    dict(id="U-1A-RELV", bucket_id="B-RELV", title="Relative velocity in a plane", blocks=core1a_relv),
])][0]

# --- CORE1B ----------------------------------------------------------------
core1b_vec = [
    text_block("1B-VEC-T1", ["OB-VEC-CONCEPT"], ["w_x", "w_y"],
        "Predict first: a vector has components (3, 4) m/s in an east/north frame. Before reading on, "
        "decide -- is '5 m/s' the full description of this vector, or is something still missing?\n"
        "Check your prediction: '5 m/s' is only the magnitude, obtained from sqrt(3^2 + 4^2) = 5 m/s by "
        "the right-triangle bridge. It cannot by itself say whether the vector points north-east, "
        "south-west, or anywhere else -- the squaring step that produced it threw the signs away. A "
        "common wrong idea is to treat the magnitude and the vector as interchangeable once a number "
        "has been calculated. Diagnostic: two vectors, (3,4) and (4,3) m/s, have the same magnitude (5 "
        "m/s in both cases) -- do they point the same way? They do not: comparing the signed components "
        "directly shows they are different vectors. The repair is to keep the signed pair (3,4) "
        "alongside the magnitude whenever direction is asked for."),
    figure_block("1B-VEC-F1", ["OB-VEC-CONCEPT"], ["w_x", "w_y"],
        vector_scene("w", "m/s", "w_x", "w_y", "Model drawing of w: compare it against your own sketch before reading the components off it.")),
    text_block("1B-VEC-T2", ["OB-VEC-SUBTRACT"], ["p_x", "p_y", "q_x", "q_y", "pq_x", "pq_y"],
        "Reconstruct before checking: P = (6,0) m/s and Q = (0,8) m/s in a common east/north frame. "
        "Sketch P - Q graphically on your own, using the reverse-then-add rule, before reading further.\n"
        "A frequent shortcut is to draw P and Q from the same origin and simply join their two tips in "
        "whichever order looks convenient -- this hides which observer's subtraction order is being "
        "used and is easy to reverse by accident. Diagnostic: in your sketch, which endpoint does the "
        "subtraction arrow start from -- the tip of P or the tip of Q? The correct construction reverses "
        "Q to get -Q = (0,-8) m/s, translates it to the head of P without rotating it, and draws the "
        "resultant from the tail of P to the head of the translated -Q: (6,0) + (0,-8) = (6,-8) m/s. "
        "Check your reconstruction against this and against the direct component subtraction, "
        "(6-0, 0-8) = (6,-8) m/s -- both routes must agree."),
    equation_block("1B-VEC-E1", ["OB-VEC-SUBTRACT"], ["eq_vec_subtract"], EQ_VEC_SUBTRACT,
        "Use this to check your reconstructed subtraction: it is addition of the reversed second vector, "
        "not a shortcut between two tips drawn from the same origin.",
        ["P: the first vector.", "Q: the second vector, same frame.", "-Q: Q reversed."],
        ["P and Q are expressed along the same declared axes.",
         "Free vectors may be translated (not rotated) for the construction."]),
    figure_block("1B-VEC-F2", ["OB-VEC-SUBTRACT"], ["pq_x", "pq_y"],
        vector_scene("P-Q", "m/s", "pq_x", "pq_y", "Model resultant P-Q: compare its direction with your own reconstructed sketch, not just its length.")),
]

core1b_relv = [
    text_block("1B-RELV-T1", ["OB-RELV-DERIVE"], ["va_x", "va_y", "vb_x", "vb_y", "vab_x", "vab_y"],
        "Predict and reconstruct: A moves at (6,0) m/s and B moves at (0,8) m/s in a common east/north "
        "frame. Which displacement carries you from B to A -- and does that mean you compute v_A - v_B "
        "or v_B - v_A for 'A relative to B'? Decide before reading on.\n"
        "A common wrong route is to subtract whichever velocity is written first in the question. The "
        "repair is to reconstruct the path explicitly: draw origin -> B -> A, giving r_A = r_B + r_A/B, "
        "so r_A/B = r_A - r_B -- the same order carries through to velocities, v_A/B = v_A - v_B. "
        "Applying this: v_A/B = (6,0) - (0,8) = (6,-8) m/s, magnitude sqrt(36+64) = 10 m/s. Now explain "
        "in your own words why reversing the observer -- asking for B relative to A instead -- reverses "
        "the sign of every component, before checking the next block."),
    equation_block("1B-RELV-E1", ["OB-RELV-DERIVE"], ["eq_relv"], EQ_RELV,
        "Check your reconstructed subtraction order against this relation.",
        ["v_A: velocity of A in the common frame.", "v_B: velocity of B, same frame.",
         "v_A/B: velocity of A relative to B."],
        ["Same observation times and a common interval.", "Parallel, nonrotating Cartesian axes.",
         "Classical (non-relativistic) model."]),
    figure_block("1B-RELV-F1", ["OB-RELV-DERIVE"], ["vab_x", "vab_y"],
        vector_scene("v_A/B", "m/s", "vab_x", "vab_y", "Model resultant v_A/B: compare its direction with your own reconstruction.")),
    text_block("1B-RELV-T2", ["OB-RELV-REVERSAL"], ["vba_x", "vba_y"],
        "Diagnose this arrow: a classmate reverses the observer and draws B relative to A with the "
        "correct length (10 m/s) but pointing northeast instead of northwest. Is the length being "
        "correct enough to accept the answer? It is not: v_B/A = -(v_A/B) = -(6,-8) = (-6,8) m/s, which "
        "points northwest, not northeast -- a correct magnitude does not certify a correct vector. Name "
        "the observer, label both signed components, and inspect the direction before ever taking a "
        "magnitude. As a standing check, v_A/B + v_B/A must equal exactly zero for any pair of "
        "velocities."),
]

core1b = dict(core="CORE1B", units=[
    dict(id="U-1B-VEC", bucket_id="B-VEC", title="Vector representation and subtraction", blocks=core1b_vec),
    dict(id="U-1B-RELV", bucket_id="B-RELV", title="Relative velocity in a plane", blocks=core1b_relv),
])

# --- CORE2A (worked practice, full solutions, purpose- and waiver-adjusted) ----
core2a_vec = [
    question_block("2A-VEC-Q1", ["OB-VEC-PRACTICE"], ["w_x", "w_y"], "Q-VEC-A1",
        answer=dict(summary="Speed 5 m/s; the velocity points into the north-east quadrant.",
                    steps=["Read the signed components from the declared east/north axes: 3 m/s east, 4 m/s north.",
                           "Apply the right-triangle bridge: speed = sqrt(3^2+4^2) = sqrt(25) = 5 m/s.",
                           "Keep the original signed pair (3,4) for the direction statement; the magnitude alone cannot supply it."],
                    check="Both components are positive, so the vector must lie in the north-east quadrant, consistent with the stated direction.",
                    numeric=dict(value=5, unit="m/s")),
        hints=["Name the frame and read the two signed components first.",
               "Apply the right-triangle bridge to the component magnitudes for the speed.",
               "Direction needs the signed pair, not the magnitude alone."],
        family="vector_magnitude", learner_action="solve", exposure_role="WORKED_EXAMPLE"),
    figure_block("2A-VEC-F1", ["OB-VEC-PRACTICE"], ["w_x", "w_y"],
        vector_scene("w", "m/s", "w_x", "w_y", "The cyclist's velocity vector, matching the worked answer."),
        placement="ANSWER", question_id="2A-VEC-Q1"),
]

core2a_relv = [
    question_block("2A-RELV-Q1", ["OB-RELV-PRACTICE-1"], ["va_x", "va_y", "vb_x", "vb_y", "vab_x", "vab_y"],
        "Q-RELV-A1",
        answer=dict(summary="(6,-8) m/s, southeast; magnitude 10 m/s.",
                    steps=["Subtract B's velocity from A's: (6,0) - (0,8) = (6,-8) m/s.",
                           "The eastward component is +6 m/s and the northward component is -8 m/s (i.e. 8 m/s south).",
                           "Right-triangle bridge: magnitude = sqrt(6^2+8^2) = sqrt(100) = 10 m/s."],
                    check="Reversing the observer gives (-6,8) m/s, the same magnitude, opposite direction.",
                    numeric=dict(value=10, unit="m/s")),
        hints=["Name the frame; subtract B's components from A's, in that order.",
               "Keep the signs through the subtraction before taking any magnitude.",
               "Apply the right-triangle bridge only once the signed components are found."],
        family="relative_velocity", learner_action="solve", exposure_role="WORKED_EXAMPLE"),
    figure_block("2A-RELV-F1", ["OB-RELV-PRACTICE-1"], ["vab_x", "vab_y"],
        vector_scene("v_A/B", "m/s", "vab_x", "vab_y", "A relative to B, matching the worked answer."),
        placement="ANSWER", question_id="2A-RELV-Q1"),
    question_block("2A-RELV-Q2", ["OB-RELV-PRACTICE-2"], ["vm_x", "vm_y", "vn_x", "vn_y", "vmn_x", "vmn_y"],
        "Q-RELV-A2",
        answer=dict(summary="(-5,12) m/s, north-west of the frame's axes; magnitude 13 m/s.",
                    steps=["Subtract N's velocity from M's: (0,13) - (5,1) = (-5,12) m/s.",
                           "The eastward component is -5 m/s (i.e. 5 m/s west) and the northward component is +12 m/s.",
                           "Right-triangle bridge: magnitude = sqrt(5^2+12^2) = sqrt(169) = 13 m/s."],
                    check="Reversing the observer gives N relative to M = (5,-12) m/s, the same magnitude.",
                    numeric=dict(value=13, unit="m/s")),
        hints=["Same subtraction order as the worked A/B example, with M and N in place of A and B.",
               "5-12-13 is a right-triangle triple; check the arithmetic against it."],
        family="relative_velocity", learner_action="solve", exposure_role="PRACTICE"),
    figure_block("2A-RELV-F2", ["OB-RELV-PRACTICE-2"], ["vmn_x", "vmn_y"],
        vector_scene("v_M/N", "m/s", "vmn_x", "vmn_y", "M relative to N, matching the worked answer."),
        placement="ANSWER", question_id="2A-RELV-Q2"),
    question_block("2A-RELV-Q3", ["OB-RELV-REVERSAL-PRACTICE"], ["vba_x", "vba_y"], "Q-RELV-A3",
        answer=dict(summary="(-6,8) m/s; same magnitude (10 m/s), opposite direction to A relative to B.",
                    steps=["Apply v_B/A = -(v_A/B): negate every component of (6,-8), giving (-6,8) m/s.",
                           "Magnitude is unchanged because the right-triangle bridge squares both components: sqrt((-6)^2+8^2) = 10 m/s."],
                    check="Adding v_A/B and v_B/A gives exactly (0,0) m/s -- a standing check for any reversal.",
                    numeric=dict(value=10, unit="m/s")),
        hints=["Reversal negates every signed component; it does not change the magnitude.",
               "Add your answer to the original vector as a check -- the sum must be zero."],
        family="relative_velocity_reversal", learner_action="solve", exposure_role="WORKED_TO_FADED"),
]

core2a = dict(core="CORE2A", units=[
    dict(id="U-2A-VEC", bucket_id="B-VEC", title="Vector representation and subtraction: practice", blocks=core2a_vec),
    dict(id="U-2A-RELV", bucket_id="B-RELV", title="Relative velocity in a plane: practice", blocks=core2a_relv),
])

# --- CORE2B (transfer: model choice, representation, graduated help) -----------
core2b_vec = [
    question_block("2B-VEC-Q1", ["OB-VEC-TRANSFER"], ["p_x", "p_y", "q_x", "q_y", "pq_x", "pq_y"], "Q-VEC-B1",
        answer=dict(summary="P-Q = (6,-8) m/s; magnitude 10 m/s.",
                    steps=["Reverse Q = (0,8) to get -Q = (0,-8) m/s.",
                           "Translate -Q to the head of P without rotating it, and add tail-to-head: (6,0)+(0,-8) = (6,-8) m/s.",
                           "Cross-check against direct component subtraction: (6-0, 0-8) = (6,-8) m/s -- both routes must agree.",
                           "Right-triangle bridge for the magnitude: sqrt(6^2+8^2) = 10 m/s."],
                    check="The graphical and component routes produced the same (6,-8) m/s.",
                    numeric=dict(value=10, unit="m/s")),
        hints=["State which vector is being reversed before drawing anything.",
               "Translate, do not rotate, the reversed vector.",
               "Cross-check the graphical resultant against direct component subtraction."],
        family="vector_magnitude", learner_action="reconstruct", exposure_role="RECONSTRUCTION_ANCHOR"),
]

core2b_relv = [
    text_block("2B-RELV-T-EXT", ["OB-RELV-EXTENSION-BOAT"],
        ["vboat_x", "vboat_y", "vcurrent_x", "vcurrent_y", "vresult_x", "vresult_y"],
        "Labelled extension, beyond the two-object baseline scope: a swimmer's velocity relative to the "
        "water and the water's velocity relative to the ground are both given. Finding the swimmer's "
        "velocity relative to the ground needs the same relation used throughout this unit, rearranged: "
        "if v_A/C = v_A/B - v_C/B and the current is described as water relative to ground rather than "
        "ground relative to water, then v_swimmer/ground = v_swimmer/water + v_water/ground. This is "
        "addition, not the subtraction drilled above, and it involves three objects (swimmer, water, "
        "ground) instead of two -- decide which relation applies before calculating; do not assume every "
        "relative-motion question is a subtraction."),
    question_block("2B-RELV-Q1", ["OB-RELV-EXTENSION-BOAT"],
        ["vboat_x", "vboat_y", "vcurrent_x", "vcurrent_y", "vresult_x", "vresult_y"], "Q-RELV-B2",
        answer=dict(summary="(4,3) m/s; magnitude 5 m/s.",
                    steps=["Identify the relation: swimmer relative to ground = swimmer relative to water + water relative to ground (addition, not subtraction, because the current is already given as water-relative-to-ground).",
                           "Add the components: (0,3) + (4,0) = (4,3) m/s.",
                           "Right-triangle bridge: magnitude = sqrt(4^2+3^2) = sqrt(25) = 5 m/s."],
                    check="If the current were zero, the result would reduce to the swimmer's own (0,3) m/s, as it should.",
                    numeric=dict(value=5, unit="m/s")),
        hints=["First decide: does this situation add or subtract the two given velocities? Justify the choice before calculating.",
               "Write out which object each velocity is measured relative to before combining them."],
        family="relative_velocity_composition", learner_action="judge_model_choice", exposure_role="NEW_TRANSFER"),
    question_block("2B-RELV-Q2", ["OB-RELV-TRANSFER-N"], ["vnm_x", "vnm_y"], "Q-RELV-B3",
        answer=dict(summary="(5,-12) m/s; same magnitude (13 m/s) as M relative to N.",
                    steps=["Apply the reversal relation directly to the already-known result: v_N/M = -(v_M/N) = -(-5,12) = (5,-12) m/s.",
                           "No need to return to M and N's original velocities -- the reversal principle applies to any relative-velocity result."],
                    check="Adding v_M/N and v_N/M gives (0,0) m/s.",
                    numeric=dict(value=13, unit="m/s")),
        hints=["The reversal principle proved for A/B applies to any pair -- it does not need to be re-derived from scratch for M and N."],
        family="relative_velocity_reversal", learner_action="apply_principle_to_new_case", exposure_role="NEW_TRANSFER"),
]

core2b = dict(core="CORE2B", units=[
    dict(id="U-2B-VEC", bucket_id="B-VEC", title="Vector representation and subtraction: transfer", blocks=core2b_vec),
    dict(id="U-2B-RELV", bucket_id="B-RELV", title="Relative velocity in a plane: transfer", blocks=core2b_relv),
])

PRACTICE_CONTROL = dict(
    mode="OWNER_WAIVER", purpose="COMPETITION",
    authorization_ref="V3B-Motion-Grade9-Example.md#owner_waiver (enabled: true; instruction: start from "
                       "prerequisite bridges and simple cases, then offer clearly labelled "
                       "competitive-foundation transfer; no measured-mastery claim)",
    support_plan="Bridge signed-coordinate subtraction and right-triangle magnitude "
                 "(CAP-SIGNED-PAIR-BRIDGE, CAP-RIGHT-TRIANGLE-BRIDGE) before independent use; keep "
                 "UNKNOWN knowledge visible throughout; this run makes no personalised-readiness claim.")

PLAN = dict(schema_version="1.0.0", subject="Physics", topic_id=BASELINE["topic_id"],
            title="Motion in two dimensions: vector representation and subtraction; relative velocity in a plane",
            baseline_digest=digest(BASELINE), practice_control=PRACTICE_CONTROL,
            products=[core1a, core1b, core2a, core2b])

write_json(RUN_DIR / "inputs" / "plan.json", PLAN)
print("Wrote plan.json.")
print("CORE2A questions:", sum(1 for u in core2a["units"] for b in u["blocks"] if b["kind"] == "QUESTION"),
      "(target 8)")
print("CORE2B questions:", sum(1 for u in core2b["units"] for b in u["blocks"] if b["kind"] == "QUESTION"),
      "(target 6)")

