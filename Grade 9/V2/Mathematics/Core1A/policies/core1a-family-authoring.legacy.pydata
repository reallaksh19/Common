#!/usr/bin/env python3
"""Core 1A: turn a semantic MathCore1StudyPlan into a learner-facing textbook PDF.

Core 1 deliberately expresses instructional obligations in machine-oriented form.
Core 1A is the learner-authoring boundary. It consumes that output plus repository
instructional authority, materializes real learner problems, rewrites internal
authoring language into textbook prose, validates learner-product quality, and
emits a PDF + manuscript + audit.

Core 1A never reuses original assessment questions. It fails closed when a
problem family has no authored instance generator or when a required learner
component is not materialized.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

FULL_TREATMENTS = {"ACTIVE_STUDY", "REPAIR_BEFORE", "REPAIR_IN_UNIT"}
REQUIRED_ROLES = ("WORKED", "GUIDED", "FADED", "INDEPENDENT", "TRANSFER")
FORBIDDEN_LEARNER_TOKENS = (
    "capability_ref",
    "problem_family_ref",
    "release class",
    "pck ",
    "promotion registry",
    "author a new instance",
    "source reuse is forbidden",
    "core1 study plan",
    "treatment ",
    "reconstruction route",
    "fading dimensions",
    "candidate learner product",
    "publication engineering",
    "{rows}",
)
INTERNAL_CODE_RE = re.compile(r"\b(?:MATH-(?:PF|PCK|C1L|PAP|C1SP)-[A-Z0-9-]+)\b")

ROOT = Path(__file__).resolve().parents[2]
FONT_NAME = "Core1A-Regular"
FONT_BOLD = "Core1A-Bold"


def register_fonts() -> None:
    global FONT_NAME, FONT_BOLD
    candidates = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"),
    ]
    for regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont(FONT_NAME, regular))
            pdfmetrics.registerFont(TTFont(FONT_BOLD, bold))
            return
    FONT_NAME, FONT_BOLD = "Helvetica", "Helvetica-Bold"

DEFAULT_PCK_INDEX = ROOT / "InstructionalKnowledge" / "registry" / "math-pck-candidates.json"
DEFAULT_FAMILY_INDEX = ROOT / "ProblemSemantics" / "registry" / "math-problem-family-registry.json"

# -------------------------- deterministic helpers --------------------------
def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def load(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def humanize_code(value: str) -> str:
    text = re.sub(r"^MATH-(?:PF|PCK)-", "", str(value))
    return text.replace("_", " ").replace("-", " ").strip().title()


def sentence(text: str) -> str:
    text = str(text or "").strip()
    if not text:
        return ""
    text = text[0].upper() + text[1:]
    return text if text.endswith((".", "?", "!")) else text + "."


def public_phrase(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if re.fullmatch(r"[A-Z0-9_]+", text):
        label = text
        for prefix in ("VERIFY_", "CHECK_"):
            if label.startswith(prefix):
                label = label[len(prefix):]
                return sentence("Check " + label.replace("_", " ").lower())
        return sentence(label.replace("_", " ").lower())
    return sentence(text)


def safe_text(text: str) -> str:
    return (
        str(text or "")
        .replace("&", "&amp;")
        .replace("<=", "≤")
        .replace(">=", "≥")
        .replace("!=", "≠")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def load_pck_assets(index_path: Path) -> dict[str, dict]:
    index = load(index_path)
    out: dict[str, dict] = {}
    for row in index.get("asset_documents", []):
        asset_path = index_path.parent / row["path"]
        asset = load(asset_path)
        if asset.get("asset_id") != row.get("asset_id"):
            fail("CORE1A_PCK_INDEX_BINDING_MISMATCH", str(asset_path))
        out[asset["asset_id"]] = asset
    return out


def load_problem_families(index_path: Path) -> dict[str, dict]:
    index = load(index_path)
    out: dict[str, dict] = {}
    for shard in index.get("family_shards", []):
        body = load(index_path.parent / shard["path"])
        for family in body.get("families", []):
            out[family["family_id"]] = family
    if len(out) != index.get("family_count"):
        fail("CORE1A_PROBLEM_FAMILY_REGISTRY_INCOMPLETE")
    return out

# -------------------------- learner instance bank --------------------------
@dataclass(frozen=True)
class Instance:
    prompt: str
    steps: tuple[str, ...]
    answer: str
    hints: tuple[str, str, str]


def inst(prompt: str, steps: list[str], answer: str, hints: list[str]) -> Instance:
    if len(hints) != 3:
        raise AssertionError("all learner instances require three hints")
    return Instance(prompt, tuple(steps), answer, tuple(hints))


def distance_instances() -> list[Instance]:
    return [
        inst("Find the distance between A(1, 2) and B(4, 6).",
             ["Horizontal change = 4 - 1 = 3.", "Vertical change = 6 - 2 = 4.",
              "Distance = √(3² + 4²) = √25 = 5."],
             "5",
             ["Keep x-coordinates with x-coordinates and y-coordinates with y-coordinates.",
              "Use the horizontal and vertical changes as the legs of a right triangle.",
              "Compute √((4 - 1)² + (6 - 2)²)."]),
        inst("Find the distance between P(-2, 3) and Q(4, -5).",
             ["Horizontal change = 4 - (-2) = 6.", "Vertical change = -5 - 3 = -8.",
              "Distance = √(6² + (-8)²) = √100 = 10."],
             "10",
             ["Subtraction order may change signs, but the squares remove that sign.",
              "Find Δx and Δy first.", "Compute √(6² + (-8)²)."]),
        inst("A point R is 13 units from S(0, 0) and has coordinates R(5, y) with y > 0. Find y.",
             ["Use the distance relation: √(5² + y²) = 13.", "Square both sides: 25 + y² = 169.",
              "So y² = 144 and y = 12 because y > 0."],
             "12",
             ["Translate the distance statement into an equation first.",
              "The legs are 5 and y, and the hypotenuse is 13.", "Solve 25 + y² = 169 and use y > 0."]),
        inst("A(2, -1), B(8, 7). Without drawing, decide whether AB is longer than 9 units.",
             ["Δx = 6 and Δy = 8.", "AB² = 6² + 8² = 100, so AB = 10.", "Therefore AB is longer than 9."],
             "Yes; AB = 10.",
             ["Compare squared distances if that is quicker.", "Compute 6² + 8².", "√100 = 10."]),
        inst("Two points have horizontal separation 7 and vertical separation 24. Find their distance and explain why changing the order of the points does not change it.",
             ["Distance = √(7² + 24²) = √625 = 25.",
              "Reversing the point order changes both differences to their negatives.",
              "Squaring removes those sign changes, so the distance stays 25."],
             "25; reversing point order does not change the squared differences.",
             ["Use the right-triangle structure.", "7-24-25 is a Pythagorean triple.",
              "Explain what happens to Δx and Δy when the point order is reversed."]),
    ]


def intercept_instances() -> list[Instance]:
    return [
        inst("Find the y-intercept of 2x + 3y = 12.",
             ["A point on the y-axis has x = 0.", "Substitute x = 0: 3y = 12.", "So y = 4 and the intercept is (0, 4)."],
             "(0, 4)",
             ["Ask which coordinate is always zero on the y-axis.", "Set x = 0, not y = 0.", "Solve 3y = 12."]),
        inst("Find the y-intercept of 5x - 2y = 14.",
             ["Set x = 0.", "-2y = 14.", "So y = -7 and the intercept is (0, -7)."],
             "(0, -7)",
             ["A y-intercept lies on the y-axis.", "Use x = 0.", "Solve -2y = 14."]),
        inst("A line is written as 4y = 3x + 20. Find its y-intercept.",
             ["At the y-axis, x = 0.", "Then 4y = 20.", "So y = 5."],
             "(0, 5)",
             ["Do not rearrange more than you need to.", "At the y-axis, set x = 0.", "4y = 20."]),
        inst("Which point is the y-intercept of 7x + y = -3: (-3, 0) or (0, -3)? Explain.",
             ["The y-intercept must have x = 0.", "Substitute x = 0: y = -3.", "So (0, -3) is the y-intercept."],
             "(0, -3)",
             ["Use the meaning of the y-axis.", "A point on the y-axis has x = 0.", "Test the candidate points."]),
        inst("The y-intercept of ax + 2y = 10 is (0, 5) for every value of a. Explain why.",
             ["On the y-axis, x = 0.", "The term ax becomes a·0 = 0 for every value of a.", "The equation becomes 2y = 10, so y = 5."],
             "Because x = 0 makes the ax term vanish.",
             ["Start from the axis condition.", "What happens to ax when x = 0?", "The remaining equation is 2y = 10."]),
    ]


def slope_point_instances() -> list[Instance]:
    return [
        inst("Find the equation of the line with slope 2 through (1, 3).",
             ["Use point-slope form: y - 3 = 2(x - 1).", "Expand: y - 3 = 2x - 2.", "So y = 2x + 1."],
             "y = 2x + 1",
             ["Use the given point as the anchor.", "Write y - y₁ = m(x - x₁).", "y - 3 = 2(x - 1)."]),
        inst("Find the equation of the line with slope -1/2 through (4, 1).",
             ["Write y - 1 = -1/2(x - 4).", "Expand: y - 1 = -x/2 + 2.", "So y = -x/2 + 3."],
             "y = -x/2 + 3",
             ["Keep the negative sign attached to the slope.", "Use point-slope form.", "Substitute (4, 1) only after the form is written."]),
        inst("A line has slope 3 and passes through (-2, 5). Write an equation and check the point.",
             ["y - 5 = 3(x + 2).", "So y = 3x + 11.", "Check: 5 = 3(-2) + 11 = 5."],
             "y = 3x + 11",
             ["Be careful: x - (-2) becomes x + 2.", "Write point-slope form first.", "Substitute the point into your final equation."]),
        inst("Does y = 4x - 7 pass through (2, 1)? If it does, state its slope.",
             ["Substitute x = 2: 4(2) - 7 = 1.", "The point satisfies the equation.", "The slope in y = mx + b is 4."],
             "Yes; slope 4.",
             ["Membership can be checked by substitution.", "Test x = 2, y = 1.", "Then read m from y = mx + b."]),
        inst("A line through (3, -1) is perpendicular to a line of slope 2. Find its equation.",
             ["A perpendicular line has slope -1/2.", "Use y + 1 = -1/2(x - 3).", "So y = -x/2 + 1/2."],
             "y = -x/2 + 1/2",
             ["First determine the new slope.", "Perpendicular slopes are negative reciprocals.", "Then use the given point in point-slope form."]),
    ]


def pair_instances() -> list[Instance]:
    return [
        inst("Six students each shake hands with every other student once. How many handshakes occur?",
             ["The first student can pair with 5 others, then 4 new pairs remain, then 3, 2 and 1.",
              "5 + 4 + 3 + 2 + 1 = 15.", "Equivalently, 6·5/2 = 15."],
             "15",
             ["AB and BA are the same handshake.", "Count each unordered pair once.", "Use n(n - 1)/2 with n = 6."]),
        inst("Eight teams each play every other team once. How many games are played?",
             ["Each game is one unordered pair of teams.", "8·7/2 = 28.", "So 28 games are played."],
             "28",
             ["Do not count Team A vs Team B twice.", "Use the unordered-pair formula.", "8·7/2."]),
        inst("A graph has 10 vertices and exactly one edge joining every pair. How many edges are there?",
             ["Each edge corresponds to one pair of vertices.", "10·9/2 = 45."],
             "45",
             ["Translate 'one edge for every pair' into pair counting.", "Choose 2 objects from 10 without order.", "10·9/2."]),
        inst("There are 21 unique pairs in a group. How many objects are in the group?",
             ["Set n(n - 1)/2 = 21.", "So n(n - 1) = 42.", "n = 7 works because 7·6 = 42."],
             "7",
             ["Work backwards from the pair-count formula.", "Solve n(n - 1) = 42.", "Look for consecutive factors of 42."]),
        inst("Explain why n(n - 1) counts every unordered pair twice, and hence why the formula divides by 2.",
             ["For each ordered choice AB, the reversed choice BA is also counted in n(n - 1).",
              "Those two ordered choices represent one unordered pair.", "Therefore divide by 2."],
             "Each pair appears in two orders, AB and BA.",
             ["Think about one fixed pair.", "How many orders can its two members be written in?", "That double count is removed by dividing by 2."]),
    ]


def collinear_instances() -> list[Instance]:
    return [
        inst("Are A(1, 2), B(3, 6) and C(5, 10) collinear?",
             ["Slope AB = (6 - 2)/(3 - 1) = 2.", "Slope AC = (10 - 2)/(5 - 1) = 2.",
              "The equal slopes show a common direction, so the points are collinear."],
             "Yes.",
             ["Use the same reference point in both slopes.", "Compare slope AB with slope AC.", "Both slopes equal 2."]),
        inst("Are P(-1, 4), Q(2, 1) and R(5, -1) collinear?",
             ["Slope PQ = (1 - 4)/(2 - (-1)) = -1.", "Slope PR = (-1 - 4)/(5 - (-1)) = -5/6.",
              "The slopes are different, so the points are not collinear."],
             "No.",
             ["Equal slopes are required.", "Compute two slopes sharing P.", "Compare -1 with -5/6."]),
        inst("Find k so that (0, 1), (2, 5) and (4, k) are collinear.",
             ["Slope from (0,1) to (2,5) is 2.", "For collinearity, (k - 1)/4 = 2.", "So k = 9."],
             "k = 9",
             ["First find the known slope.", "The third point must give the same slope.", "(k - 1)/4 = 2."]),
        inst("Without plotting, show that A(-2, -2), B(3, 0) and C(8, 2) are collinear.",
             ["Slope AB = 2/5.", "Slope BC = 2/5.", "The equal directed slopes show the three points lie on one line."],
             "They are collinear.",
             ["Keep the point order consistent.", "Compute AB and BC.", "Both slopes are 2/5."]),
        inst("A student says three points are collinear because they all lie in the coordinate plane. Explain the error.",
             ["All coordinate points are coplanar by definition.", "Collinearity is stronger: the points must lie on one straight line.",
              "A valid test is equal slope between point pairs, with vertical-line cases handled separately."],
             "Coplanar does not mean collinear.",
             ["Compare the meanings of 'same plane' and 'same line'.", "Collinearity needs a common line.", "Use a direction test, not merely the fact that points are plotted."]),
    ]


def parallel_instances() -> list[Instance]:
    return [
        inst("Two same-side interior angles are 110° and 70°. What does their sum tell you about the two lines?",
             ["110° + 70° = 180°.", "A 180° same-side interior sum is the parallel boundary.", "The lines are parallel."],
             "The lines are parallel.",
             ["Add the two same-side interior angles.", "Compare the sum with 180°.", "A sum of 180° is the parallel case."]),
        inst("Two same-side interior angles are 100° and 60°. According to Euclid's condition, what happens on that side?",
             ["100° + 60° = 160°.", "160° is less than 180°.", "The lines meet on that side."],
             "They meet on that side.",
             ["Find the sum first.", "Compare it with 180°.", "Less than 180° predicts meeting on that side."]),
        inst("One same-side interior angle is 125°. Find the other angle if the lines are parallel.",
             ["Parallel lines give a same-side interior sum of 180°.", "Other angle = 180° - 125° = 55°."],
             "55°",
             ["Use the parallel-line sum.", "The two angles total 180°.", "Subtract 125° from 180°."]),
        inst("A student concludes 'parallel' because 80° + 90° is close to 180°. Is the conclusion valid?",
             ["80° + 90° = 170°.", "The condition is exact, not approximate.", "Since the sum is below 180°, the parallel conclusion is not justified."],
             "No.",
             ["'Close' is not a theorem condition.", "Calculate the exact sum.", "170° ≠ 180°."]),
        inst("Explain the difference between using a theorem and using its converse in a parallel-line angle problem.",
             ["A theorem starts from parallel lines and deduces an angle relation.",
              "A converse starts from the angle relation and deduces that the lines are parallel.",
              "The direction of the given information determines which statement is legal to use."],
             "The theorem and converse run in opposite logical directions.",
             ["Ask what information is given first.", "Parallel ⇒ angle relation is one direction.", "Angle relation ⇒ parallel is the converse direction."]),
    ]


def parameter_instances() -> list[Instance]:
    return [
        inst("The point (2, 2) lies on kx + 3y = 10. Find k.",
             ["Substitute x = 2, y = 2.", "2k + 6 = 10.", "So 2k = 4 and k = 2."],
             "k = 2",
             ["A point on a line satisfies its equation.", "Substitute both coordinates.", "Solve 2k + 6 = 10."]),
        inst("A solution of kx + y = 6 is known only to satisfy x = y. Is that enough to determine one unique value of k?",
             ["Substitute y = x: (k + 1)x = 6.", "Both k and x are still unknown.", "Different nonzero x values give different k values, so k is not uniquely determined."],
             "No; the information is insufficient.",
             ["Count the unknown quantities after using x = y.", "You still have k and x in one equation.", "One equation in two unknowns does not fix a unique pair."]),
        inst("The line (a - 1)x + 2y = 7 passes through (1, 3). Find a.",
             ["Substitute (1, 3): (a - 1) + 6 = 7.", "a + 5 = 7.", "So a = 2."],
             "a = 2",
             ["Use point membership.", "Substitute x = 1, y = 3.", "Solve a + 5 = 7."]),
        inst("For which value of p does px + 2y = 8 pass through (4, 0)?",
             ["Substitute (4, 0): 4p = 8.", "So p = 2."],
             "p = 2",
             ["Use the supplied point, not a guessed coefficient.", "Substitute x = 4, y = 0.", "4p = 8."]),
        inst("A parameter equation leaves both p and x free after every given condition is used. What should you conclude?",
             ["A unique parameter requires enough independent information to eliminate the other freedom.",
              "If p and x remain linked by one relation, many pairs may satisfy it.", "Therefore the parameter is underdetermined unless another independent condition is supplied."],
             "The parameter is not uniquely determined.",
             ["Do not silently assign a convenient value.", "Check how many independent unknowns remain.", "A remaining degree of freedom means no unique parameter."]),
    ]


def intersection_instances() -> list[Instance]:
    return [
        inst("The lines x + y = 5 and x - y = 1 meet at P. Find P, then find the line through P and (1, 4).",
             ["Add the two equations: 2x = 6, so x = 3 and y = 2.", "Thus P = (3, 2).",
              "Slope through (3,2) and (1,4) is (4 - 2)/(1 - 3) = -1.",
              "Using P: y - 2 = -(x - 3), so y = -x + 5."],
             "P = (3, 2); target line y = -x + 5.",
             ["Solve the intersection before starting the second line.", "Use the checked intersection as one of the two defining points.",
              "Then find the slope and write a line equation."]),
        inst("Find the intersection of 2x + y = 7 and x - y = 2. Then write the line through that point and the origin.",
             ["Add the equations: 3x = 9, so x = 3 and y = 1.", "The intersection is (3,1).",
              "Slope from (0,0) to (3,1) is 1/3.", "So the target line is y = x/3."],
             "(3, 1); y = x/3",
             ["Treat this as two subproblems.", "First solve both original equations simultaneously.", "Then use the origin and the intersection to make the new line."]),
        inst("The lines y = x + 1 and y = -x + 5 intersect. Find the equation of the line through their intersection and (0, 0).",
             ["Set x + 1 = -x + 5, giving 2x = 4 and x = 2.", "Then y = 3, so the intersection is (2,3).",
              "The line through (0,0) and (2,3) has slope 3/2, so y = 3x/2."],
             "y = 3x/2",
             ["At the intersection, both y expressions are equal.", "Find the point first.", "Then use the two-point slope with the origin."]),
        inst("Why must the intersection be checked in both original equations before it is reused to build a new line?",
             ["An algebra error can produce a point that satisfies only one transformed relation.",
              "The new line calculation treats the intersection as trusted data.",
              "Checking both original equations prevents an early error from contaminating the second stage."],
             "Because the second stage depends on the intersection being correct.",
             ["Think about error propagation.", "The intersection becomes input to the next calculation.", "Verify both source constraints before reuse."]),
        inst("Two source lines are parallel. Can the 'intersection then line' method continue as usual?",
             ["Parallel distinct lines have no intersection point.", "Without an intersection, the next line does not receive the required defining point.",
              "The method must stop or the problem must supply another condition."],
             "No; there is no intersection point to reuse.",
             ["Check whether the first subgoal exists.", "Parallel distinct lines do not meet.", "The second construction therefore lacks one of its required points."]),
    ]


def equidistant_axis_instances() -> list[Instance]:
    return [
        inst("P = (x, 0) lies on the x-axis and is equidistant from A(1, 2) and B(5, 2). Find P.",
             ["Use squared distances: (x - 1)² + 2² = (x - 5)² + 2².", "Cancel 4 on both sides.",
              "Expand: x² - 2x + 1 = x² - 10x + 25.", "So 8x = 24 and x = 3. Hence P = (3,0)."],
             "P = (3, 0)",
             ["Use the axis condition first: P has y = 0.", "Equate squared distances to A and B.", "The x² terms cancel after expansion."]),
        inst("P = (0, y) is on the y-axis and is equidistant from A(2, 1) and B(2, 7). Find P.",
             ["(0 - 2)² + (y - 1)² = (0 - 2)² + (y - 7)².",
              "Cancel 4, then solve (y - 1)² = (y - 7)².", "The midpoint value is y = 4, so P = (0,4)."],
             "P = (0, 4)",
             ["The axis fixes x = 0.", "Equidistance gives equal squared distances.", "Because the fixed points share x = 2, use the midpoint of their y-values."]),
        inst("Find the point on the x-axis that is equidistant from (-2, 3) and (4, 3).",
             ["Let P = (x,0).", "(x + 2)² + 9 = (x - 4)² + 9.",
              "Solve (x + 2)² = (x - 4)² to get x = 1."],
             "(1, 0)",
             ["The point on the x-axis has form (x,0).", "The fixed points have equal y-coordinates.", "The required x-value is midway between -2 and 4."]),
        inst("A student writes P = (x, y) even though P is stated to lie on the y-axis. What information has been lost?",
             ["The y-axis condition fixes x = 0.", "Writing both coordinates as free introduces an extra unknown and ignores a given constraint.",
              "The correct model is P = (0, y)."],
             "The axis constraint x = 0.",
             ["Translate the geometry before writing distances.", "What coordinate is fixed on the y-axis?", "Use P = (0, y)."]),
        inst("Explain why using squared distances is enough in an equidistance equation.",
             ["If PA = PB and both distances are nonnegative, then PA² = PB².", "Conversely, equal nonnegative squared distances give equal distances.",
              "Using squares removes square roots and keeps the same equality condition."],
             "Squaring preserves equality for nonnegative distances and simplifies the algebra.",
             ["Distances are never negative.", "Compare PA = PB with PA² = PB².", "The square-root expressions can be avoided."]),
    ]


def trend_instances() -> list[Instance]:
    return [
        inst("A linear relation passes through (2, 10) and (5, 25). Find the rate of change and estimate the output at x = 8.",
             ["Rate = (25 - 10)/(5 - 2) = 15/3 = 5.", "From x = 5 to x = 8 is an increase of 3.",
              "Output increases by 3·5 = 15, so the estimate is 25 + 15 = 40."],
             "Rate 5; output 40.",
             ["Decide which quantity is input and which is output.", "Compute change in output divided by change in input.", "Extend the same linear rate from x = 5 to x = 8."]),
        inst("At 3 hours a tank contains 50 L; at 7 hours it contains 90 L. Assuming a linear trend, find the rate in litres per hour.",
             ["Change in volume = 40 L.", "Change in time = 4 h.", "Rate = 40/4 = 10 L/h."],
             "10 L/h",
             ["Units tell you the orientation of the ratio.", "Use litres divided by hours.", "(90 - 50)/(7 - 3)."]),
        inst("A taxi cost rises from 12 to 27 as distance rises from 2 km to 7 km. Assuming linearity, predict the cost at 10 km.",
             ["Rate = (27 - 12)/(7 - 2) = 3 per km.", "From 7 km to 10 km is 3 km.",
              "Add 3·3 = 9 to 27, giving 36."],
             "36",
             ["Find the cost change per kilometre.", "Keep units as cost/km.", "Extend three more kilometres."]),
        inst("A student computes slope as change in input divided by change in output. What clue reveals the mistake?",
             ["Slope here represents output change per input change.", "The reciprocal has inverse units.",
              "Checking units exposes the reversal before any extrapolation is attempted."],
             "The units are inverted.",
             ["Name the dependent and independent variables.", "Slope units are dependent units per independent unit.", "A reciprocal rate answers a different question."]),
        inst("Why should an extrapolation answer mention the assumption of linearity?",
             ["Two data points determine a line mathematically, but a real context need not continue linearly outside the observed interval.",
              "The estimate is justified only under the stated linear-model assumption.",
              "Naming the assumption separates calculation from model validity."],
             "Because the estimate depends on the relation continuing linearly.",
             ["Distinguish arithmetic from modelling.", "What must stay true beyond the observed data?", "State the linearity assumption explicitly."]),
    ]


def river_instances() -> list[Instance]:
    return [
        inst("A boat travels 24 km downstream in 2 h and the same distance upstream in 3 h. Find the still-water speed x and current speed y.",
             ["Downstream effective speed = 24/2 = 12, so x + y = 12.",
              "Upstream effective speed = 24/3 = 8, so x - y = 8.",
              "Add the equations: 2x = 20, so x = 10. Then y = 2."],
             "Still-water speed 10 km/h; current speed 2 km/h.",
             ["Translate each journey into an effective speed.", "Downstream uses x + y; upstream uses x - y.", "Solve x + y = 12 and x - y = 8."]),
        inst("A boat covers 30 km downstream in 2 h and 30 km upstream in 3 h. Find x and y.",
             ["Downstream: x + y = 15.", "Upstream: x - y = 10.", "Add: 2x = 25, so x = 12.5 and y = 2.5."],
             "x = 12.5 km/h, y = 2.5 km/h",
             ["Compute each journey's speed first.", "Keep the plus/minus meaning attached to direction.", "Solve the two equations together."]),
        inst("Still-water speed is 14 km/h and current speed is 3 km/h. How long does 34 km take upstream?",
             ["Upstream speed = 14 - 3 = 11 km/h.", "Time = distance/speed = 34/11 h."],
             "34/11 h (about 3.09 h)",
             ["Upstream opposes the current.", "Use x - y.", "Then time = distance ÷ rate."]),
        inst("A student writes x = 12 from a downstream speed of 12 km/h. Explain the modelling error.",
             ["The observed downstream speed combines two effects.", "It equals still-water speed plus current speed: x + y = 12.",
              "Assigning 12 to x alone discards the current."],
             "Downstream speed is x + y, not x alone.",
             ["Keep variable meanings separate from effective speed.", "What contributes to downstream motion?", "Use x + y."]),
        inst("A river-current model gives x = 4 and y = 6. What should you notice before accepting it as a physical answer?",
             ["Upstream effective speed would be x - y = -2.", "For the usual boat model we require x > y ≥ 0.",
              "The algebraic pair violates the physical condition, so it is not a valid model solution."],
             "Reject it because x must be greater than y.",
             ["Check the physical constraints after solving.", "Upstream speed must remain positive.", "Test x - y."]),
    ]


def quadrant_instances() -> list[Instance]:
    return [
        inst("If x < 0 and y > 0, in which quadrant is (x, y)?",
             ["The first coordinate is negative and the second is positive.", "The sign pair (-, +) is Quadrant II."],
             "Quadrant II",
             ["Read the coordinates in order.", "Use the sign pair (-, +).", "That sign pair is Quadrant II."]),
        inst("If x > 0 and y < 0, where does the point (-x, -y) lie?",
             ["Since x > 0, -x < 0.", "Since y < 0, -y > 0.", "The transformed sign pair is (-, +), so Quadrant II."],
             "Quadrant II",
             ["Transform each coordinate separately.", "Do not swap x and y.", "The final signs are (-, +)."]),
        inst("A point is in Quadrant III. What quadrant contains its reflection in the y-axis?",
             ["Quadrant III has signs (-, -).", "Reflection in the y-axis changes only the x-sign.", "The new signs are (+, -), which is Quadrant IV."],
             "Quadrant IV",
             ["Write the original sign pair.", "A y-axis reflection negates x only.", "(+, -) is Quadrant IV."]),
        inst("A point has x = 0 and y > 0. Is it in Quadrant I or II?",
             ["Quadrants require both coordinates to be nonzero.", "x = 0 places the point on the y-axis.", "So it is in neither quadrant."],
             "Neither; it lies on the positive y-axis.",
             ["Check the boundary case.", "Points on an axis are not inside a quadrant.", "x = 0 means y-axis."]),
        inst("Explain why changing the order of coordinates can change the quadrant even when the same two numbers are used.",
             ["The first coordinate controls horizontal position and the second controls vertical position.",
              "Swapping them swaps those roles.", "For opposite signs, that can move the point to a different quadrant."],
             "Coordinate order carries meaning; x and y roles are not interchangeable.",
             ["Ordered pair means order matters.", "First = horizontal, second = vertical.", "Compare (-2, 5) with (5, -2)."]),
    ]


def euclid_classification_instances() -> list[Instance]:
    return [
        inst("Classify: 'Things equal to the same thing are equal to one another.' Is it an axiom or a geometry-specific postulate?",
             ["The statement is a general rule about equality.", "It is not restricted to geometric objects.", "So it functions as an axiom."],
             "Axiom",
             ["Ask whether the claim is general or geometry-specific.", "It talks about equality in general.", "General foundational statements are axioms."]),
        inst("Classify: 'A straight line can be drawn joining any two points.'",
             ["The statement is specifically about points and straight lines.", "Its content belongs to Euclidean geometry.", "So it is a postulate."],
             "Postulate",
             ["Look at the mathematical objects named.", "The claim is explicitly geometric.", "Geometry-specific foundational statements are postulates."]),
        inst("Why is familiar wording not enough to classify an axiom or postulate?",
             ["Classification depends on mathematical status, not whether a sentence sounds familiar.",
              "A general truth used across mathematics differs from a geometry-specific assumption.",
              "The content and scope of the statement decide the category."],
             "Because the classification depends on scope and status, not familiarity.",
             ["Ignore how familiar the wording sounds.", "Ask what kind of claim it is.", "General vs geometry-specific is the key distinction."]),
        inst("A statement mentions lengths but expresses only the general equality rule 'equals added to equals give equal wholes.' How should it be classified?",
             ["The surface context may mention geometry.", "The underlying assertion is a general rule of equality.",
              "Therefore its mathematical status is axiomatic rather than geometry-specific."],
             "Axiom",
             ["Separate the context from the logical content.", "What rule is actually being asserted?", "General equality law → axiom."]),
        inst("Create one sentence that would clearly be geometry-specific and explain why it is not merely a general axiom.",
             ["A valid response should name geometric objects and make a foundational assumption about them.",
              "For example, a postulate about drawing a straight line through points is geometry-specific.",
              "The explanation must identify the geometric scope."],
             "Answers vary; the justification must show geometry-specific scope.",
             ["Use points, lines, circles, or another geometric object.", "Make the claim foundational rather than derived.", "Explain why it is not a general law of equality or logic."]),
    ]


def equilateral_instances() -> list[Instance]:
    return [
        inst("A(-2, 0) and B(2, 0) are two vertices of an equilateral triangle. Find the possible third vertices.",
             ["The midpoint of AB is (0,0) and AB = 4.", "An equilateral altitude has length 4·√3/2 = 2√3.",
              "The third vertex lies above or below the midpoint.", "So C = (0, 2√3) or (0, -2√3)."],
             "(0, ±2√3)",
             ["Look for symmetry about the midpoint.", "An equilateral altitude is side·√3/2.", "Keep both mirror solutions unless a side is specified."]),
        inst("A(0, 0) and B(4, 0) are vertices of an equilateral triangle. Find C.",
             ["Midpoint = (2,0), side length = 4.", "Height = 2√3.", "So C = (2, 2√3) or (2, -2√3)."],
             "(2, ±2√3)",
             ["Start with the midpoint of the horizontal base.", "Use the equilateral height.", "There are two mirror positions."]),
        inst("Why is it wrong to report only the upper third vertex when a base is given with no side condition?",
             ["Reflecting an equilateral triangle across its base gives another valid equilateral triangle.",
              "Both third vertices satisfy all three equal-distance conditions.",
              "Without an 'above' or 'below' condition, both branches must be kept."],
             "Because the geometry has two valid mirror solutions.",
             ["Check whether the problem chooses a side of the base.", "Reflection preserves side lengths.", "No side condition means both branches remain valid."]),
        inst("For base endpoints (-3, 0) and (3, 0), find the y-coordinate(s) of the third vertex of an equilateral triangle.",
             ["Side length = 6.", "Height = 6√3/2 = 3√3.", "So y = ±3√3."],
             "y = ±3√3",
             ["The midpoint lies on the y-axis.", "Use side·√3/2.", "Keep both signs."]),
        inst("How can equal-distance equations verify a candidate third vertex of an equilateral triangle?",
             ["Compute the squared distances from the candidate to each base endpoint and the squared base length.",
              "All three must be equal.", "This check also catches algebra errors and lost mirror branches."],
             "Verify CA² = CB² = AB².",
             ["An equilateral triangle has three equal sides.", "Squared distances avoid unnecessary roots.", "Compare all three, not only two."]),
    ]


FAMILY_BANKS: dict[str, Callable[[], list[Instance]]] = {
    "MATH-PF-EUCLID-CLASSIFICATION": euclid_classification_instances,
    "MATH-PF-DISTANCE-FORMULA": distance_instances,
    "MATH-PF-QUADRANT-SIGN-TRANSFORM": quadrant_instances,
    "MATH-PF-LINE-INTERCEPT": intercept_instances,
    "MATH-PF-LINE-SLOPE-POINT": slope_point_instances,
    "MATH-PF-PAIR-COUNT": pair_instances,
    "MATH-PF-COLLINEARITY-SLOPE": collinear_instances,
    "MATH-PF-EUCLID-PARALLEL-EXPLANATION": parallel_instances,
    "MATH-PF-LINEAR-PARAMETER-SUFFICIENCY": parameter_instances,
    "MATH-PF-INTERSECTION-THEN-LINE": intersection_instances,
    "MATH-PF-EQUIDISTANT-AXIS-POINT": equidistant_axis_instances,
    "MATH-PF-EQUILATERAL-COORDINATE": equilateral_instances,
    "MATH-PF-LINEAR-TREND-EXTRAPOLATION": trend_instances,
    "MATH-PF-RIVER-CURRENT-SYSTEM": river_instances,
}

DISPLAY_TITLES = {
    "MATH-PF-EUCLID-CLASSIFICATION": "Axioms and Postulates: Read the Meaning First",
    "MATH-PF-DISTANCE-FORMULA": "Distance Between Two Points",
    "MATH-PF-QUADRANT-SIGN-TRANSFORM": "Coordinates, Signs and Quadrants",
    "MATH-PF-LINE-INTERCEPT": "Finding a y-Intercept",
    "MATH-PF-LINE-SLOPE-POINT": "Building the Equation of a Line",
    "MATH-PF-PAIR-COUNT": "Counting Pairs Without Double-Counting",
    "MATH-PF-COLLINEARITY-SLOPE": "Testing Whether Points Are Collinear",
    "MATH-PF-EUCLID-PARALLEL-EXPLANATION": "Parallel Lines and the 180° Condition",
    "MATH-PF-LINEAR-PARAMETER-SUFFICIENCY": "Parameters: When Is There Enough Information?",
    "MATH-PF-INTERSECTION-THEN-LINE": "Find an Intersection, Then Build a New Line",
    "MATH-PF-EQUIDISTANT-AXIS-POINT": "A Point on an Axis at Equal Distances",
    "MATH-PF-EQUILATERAL-COORDINATE": "Equilateral Triangles on the Coordinate Plane",
    "MATH-PF-LINEAR-TREND-EXTRAPOLATION": "Slope as a Rate of Change",
    "MATH-PF-RIVER-CURRENT-SYSTEM": "River-Current Problems as a Linear System",
}

EXTRA_INSTANCES: dict[str, Instance] = {
    "MATH-PF-EUCLID-CLASSIFICATION": inst(
        "A new foundational statement is about constructing a circle with any centre and radius. Classify it and justify the classification.",
        ["The statement is about a specifically geometric construction.", "Its scope is Euclidean geometry rather than a general law of equality or logic.", "So it is a postulate."],
        "Postulate",
        ["Identify the objects named.", "Ask whether the claim is general or geometry-specific.", "A circle construction is geometry-specific."]
    ),
    "MATH-PF-DISTANCE-FORMULA": inst(
        "Find all points on the x-axis that are 5 units from (3, 4).",
        ["Let the point be (x, 0).", "Use (x - 3)² + (0 - 4)² = 25.", "Then (x - 3)² = 9, so x = 0 or x = 6."],
        "(0, 0) and (6, 0)",
        ["Use the x-axis condition first.", "Set the squared distance equal to 25.", "Solve (x - 3)² = 9."]
    ),
    "MATH-PF-QUADRANT-SIGN-TRANSFORM": inst(
        "A point P lies in Quadrant II. After reflecting P in the x-axis and then the y-axis, in which quadrant does it lie?",
        ["Quadrant II has signs (-, +).", "Reflecting in the x-axis gives (-, -), Quadrant III.", "Reflecting that point in the y-axis gives (+, -), Quadrant IV."],
        "Quadrant IV",
        ["Track one reflection at a time.", "x-axis reflection changes y-sign.", "y-axis reflection then changes x-sign."]
    ),
    "MATH-PF-LINE-INTERCEPT": inst(
        "A line has equation ax + by = c with b ≠ 0. Express its y-intercept in terms of b and c.",
        ["At the y-axis, x = 0.", "Then by = c.", "So y = c/b and the intercept is (0, c/b)."],
        "(0, c/b)",
        ["Use the axis meaning before algebra.", "Set x = 0.", "Solve by = c."]
    ),
    "MATH-PF-LINE-SLOPE-POINT": inst(
        "Find the equation of the line through (2, 5) that is parallel to 3x - y = 7.",
        ["Rewrite the given line as y = 3x - 7, so its slope is 3.", "A parallel line has the same slope.", "Use y - 5 = 3(x - 2), giving y = 3x - 1."],
        "y = 3x - 1",
        ["Find the slope of the given line first.", "Parallel lines keep the same slope.", "Use the new point in point-slope form."]
    ),
    "MATH-PF-PAIR-COUNT": inst(
        "A complete graph has 66 edges. How many vertices does it have?",
        ["Use n(n - 1)/2 = 66.", "So n(n - 1) = 132.", "The consecutive factors 12 and 11 give n = 12."],
        "12",
        ["Translate edges into unordered pairs.", "Solve n(n - 1) = 132.", "Look for consecutive factors."]
    ),
    "MATH-PF-COLLINEARITY-SLOPE": inst(
        "For what value of t are A(1, 1), B(4, 7) and C(t, 11) collinear?",
        ["Slope AB = 6/3 = 2.", "For collinearity, (11 - 1)/(t - 1) = 2.", "So 10 = 2(t - 1), giving t = 6."],
        "t = 6",
        ["Find the known direction first.", "Use A as the common reference point.", "Set AC slope equal to 2."]
    ),
    "MATH-PF-EUCLID-PARALLEL-EXPLANATION": inst(
        "Two same-side interior angles are (3x + 10)° and (2x + 20)°. If the lines are parallel, find x.",
        ["Parallel lines give a sum of 180°.", "(3x + 10) + (2x + 20) = 180.", "5x + 30 = 180, so x = 30."],
        "x = 30",
        ["Use the condition that justifies parallelism.", "Set the same-side sum equal to 180°.", "Solve 5x + 30 = 180."]
    ),
    "MATH-PF-LINEAR-PARAMETER-SUFFICIENCY": inst(
        "The equation px + qy = 12 passes through (2, 2). Is that one point enough to determine both p and q uniquely?",
        ["Substitution gives 2p + 2q = 12, or p + q = 6.", "This is one equation in two unknown parameters.", "Many pairs satisfy it, so p and q are not uniquely determined."],
        "No; only p + q = 6 is determined.",
        ["Substitute the point.", "Count how many parameters remain.", "One equation cannot uniquely determine two independent parameters."]
    ),
    "MATH-PF-INTERSECTION-THEN-LINE": inst(
        "The lines 2x + y = 8 and x + y = 5 meet at P. Find the line through P parallel to y = -2x + 9.",
        ["Subtract the second equation from the first: x = 3, then y = 2, so P = (3,2).", "A parallel line has slope -2.", "Use y - 2 = -2(x - 3), giving y = -2x + 8."],
        "y = -2x + 8",
        ["Solve the intersection first.", "Read the slope of the parallel target line.", "Use the intersection in point-slope form."]
    ),
    "MATH-PF-EQUIDISTANT-AXIS-POINT": inst(
        "P lies on the x-axis and is equidistant from A(-1, 4) and B(7, 2). Find P.",
        ["Let P = (x,0).", "(x + 1)² + 16 = (x - 7)² + 4.", "Expand and simplify: 16x = 36, so x = 9/4."],
        "P = (9/4, 0)",
        ["Use P = (x,0).", "Equate squared distances.", "Expand carefully; the x² terms cancel."]
    ),
    "MATH-PF-EQUILATERAL-COORDINATE": inst(
        "The base of an equilateral triangle has endpoints (1, 2) and (5, 2). Find both possible third vertices.",
        ["The midpoint is (3,2) and the side length is 4.", "The altitude is 2√3.", "Move that distance perpendicular to the horizontal base: C = (3, 2 ± 2√3)."],
        "(3, 2 + 2√3) and (3, 2 - 2√3)",
        ["Find the midpoint of the base.", "Use the equilateral height side·√3/2.", "Keep both mirror positions."]
    ),
    "MATH-PF-LINEAR-TREND-EXTRAPOLATION": inst(
        "A linear model has output 18 at input 4 and output 30 at input 10. Find the input at which the model predicts output 42.",
        ["Rate = (30 - 18)/(10 - 4) = 2.", "From output 30 to 42 is an increase of 12, requiring 12/2 = 6 more input units.", "So the input is 10 + 6 = 16."],
        "16",
        ["Find the rate first.", "Work backwards from the required output change.", "Divide the output increase by the rate."]
    ),
    "MATH-PF-RIVER-CURRENT-SYSTEM": inst(
        "A boat's downstream speed is 18 km/h and upstream speed is 10 km/h. Find its still-water speed and the current speed.",
        ["Let x be still-water speed and y current speed.", "x + y = 18 and x - y = 10.", "Adding gives 2x = 28, so x = 14 and y = 4."],
        "Still-water speed 14 km/h; current speed 4 km/h.",
        ["Translate the two effective speeds.", "Use x + y and x - y.", "Add the equations first."]
    ),
}


def family_bank(family_id: str) -> list[Instance]:
    if family_id not in FAMILY_BANKS:
        fail("CORE1A_FAMILY_GENERATOR_MISSING", family_id)
    rows = list(FAMILY_BANKS[family_id]())
    extra = EXTRA_INSTANCES.get(family_id)
    if extra:
        rows.append(extra)
    if len(rows) < 6:
        fail("CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED", family_id + ":need_six_distinct_instances")
    return rows

# -------------------------- manuscript authoring --------------------------
def choose_family(lesson: dict) -> str | None:
    plans = lesson.get("problem_authoring_plans") or []
    if plans:
        return plans[0].get("problem_family_ref")
    return None


def choose_asset(lesson: dict, assets: dict[str, dict]) -> dict | None:
    for ref in lesson.get("pck_asset_refs", []):
        if ref in assets:
            return assets[ref]
    return None


def public_route(asset: dict | None, family: dict | None) -> list[str]:
    if asset and asset.get("reconstruction_route"):
        return [sentence(x) for x in asset["reconstruction_route"]]
    if family:
        return [sentence(x.get("semantic_job", "")) for x in family.get("reasoning_route_template", [])]
    return []


def materialize_practice(bank: list[Instance], lesson: dict) -> dict[str, dict]:
    index_for = {"WORKED": 0, "GUIDED": 2, "FADED": 3, "INDEPENDENT": 4, "TRANSFER": 5, "VERIFY": 4}
    needed = [p["instance_role"] for p in lesson.get("problem_authoring_plans", [])]
    out = {}
    for role in needed:
        if role not in index_for:
            fail("CORE1A_UNKNOWN_INSTANCE_ROLE", role)
        i = index_for[role]
        if i >= len(bank):
            fail("CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED", role)
        item = bank[i]
        out[role] = {
            "prompt": item.prompt,
            "solution_steps": list(item.steps),
            "answer": item.answer,
            "hints": list(item.hints),
            "source_class": "NEW_AUTHORED_CORE1A",
        }
    return out


def authored_lesson(lesson: dict, assets: dict[str, dict], families: dict[str, dict]) -> dict:
    family_id = choose_family(lesson)
    asset = choose_asset(lesson, assets)
    family = families.get(family_id) if family_id else None
    full = lesson["treatment"] in FULL_TREATMENTS

    if full and not family_id:
        fail("CORE1A_PROBLEM_FAMILY_REQUIRED", lesson["lesson_id"])
    if full and family_id not in FAMILY_BANKS:
        fail("CORE1A_FAMILY_GENERATOR_MISSING", family_id or lesson["lesson_id"])

    if family_id in FAMILY_BANKS:
        bank = family_bank(family_id)
        practice = materialize_practice(bank, lesson)
    else:
        bank = []
        practice = {}

    title = DISPLAY_TITLES.get(family_id, lesson.get("learner_title") or "Mathematics")
    recognition = []
    if family:
        recognition = [sentence(x) for x in family.get("problem_signature", {}).get("recognition_cues", [])]

    ordinary = sentence(asset.get("ordinary_language_bridge", "")) if asset else ""
    anchor = sentence(asset.get("anchor", "")) if asset else ""
    route = public_route(asset, family)
    mistake = ""
    repair = []
    if asset:
        wrong = asset.get("misconception_discriminator", {}).get("candidate_wrong_model", "")
        probe = asset.get("misconception_discriminator", {}).get("probe", "")
        if wrong:
            mistake = sentence(wrong) + (" " + sentence(probe) if probe else "")
        repair = [sentence(x) for x in asset.get("repair_route", [])]
    elif family and family.get("common_invalid_mechanisms"):
        row = family["common_invalid_mechanisms"][0]
        mistake = sentence(row.get("invalid_move", "")) + " " + sentence(row.get("why_invalid", ""))

    verification = []
    if asset:
        verification.extend(sentence(x) for x in asset.get("verification_method", []))
    verification.extend(public_phrase(x) for x in lesson.get("verification_requirements", []))
    verification = list(dict.fromkeys(x for x in verification if x))

    return {
        "lesson_id": lesson["lesson_id"],
        "title": title,
        "treatment": lesson["treatment"],
        "family_ref": family_id,
        "opening": ordinary or "Begin by identifying what the question is asking you to preserve, compare or determine.",
        "concept_explanation": anchor or (sentence(family.get("problem_signature", {}).get("target_job", "")) if family else ""),
        "what_to_notice": recognition,
        "why_it_works": route,
        "common_mistake": mistake,
        "repair": repair,
        "worked_examples": (
            [
                {"prompt": bank[0].prompt, "steps": list(bank[0].steps), "answer": bank[0].answer},
                {"prompt": bank[1].prompt, "steps": list(bank[1].steps), "answer": bank[1].answer},
            ]
            if full and len(bank) >= 2
            else []
        ),
        "practice": practice,
        "verification": verification,
        "source_trace": {
            "core1_lesson_ref": lesson["lesson_id"],
            "assessment_question_refs": list(lesson.get("assessment_question_refs", [])),
            "pck_asset_refs": list(lesson.get("pck_asset_refs", [])),
        },
    }


def manuscript(core1: dict, assets: dict[str, dict], families: dict[str, dict]) -> dict:
    lessons = [authored_lesson(x, assets, families) for x in core1["lessons"]]
    out = {
        "core1a_book_id": "MATH-C1A-" + digest({"core1": core1["core1_study_plan_id"], "plan_digest": core1["plan_digest"]})[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "source_core1_study_plan_ref": core1["core1_study_plan_id"],
        "source_core1_plan_digest": core1["plan_digest"],
        "release_class": core1["release_class"],
        "lessons": lessons,
        "quality_audit": {},
        "book_digest": "",
    }
    out["quality_audit"] = validate_manuscript(out)
    out["book_digest"] = digest(out, "book_digest")
    return out


def learner_texts(book: dict) -> list[str]:
    texts: list[str] = []
    for lesson in book["lessons"]:
        for key in ("title", "opening", "concept_explanation", "common_mistake"):
            texts.append(str(lesson.get(key, "")))
        texts.extend(lesson.get("what_to_notice", []))
        texts.extend(lesson.get("why_it_works", []))
        texts.extend(lesson.get("repair", []))
        texts.extend(lesson.get("verification", []))
        for ex in lesson.get("worked_examples", []):
            texts.append(ex["prompt"])
            texts.extend(ex["steps"])
            texts.append(ex["answer"])
        for item in lesson.get("practice", {}).values():
            texts.append(item["prompt"])
            texts.extend(item["hints"])
    return texts


def validate_manuscript(book: dict) -> dict:
    failures: list[str] = []
    full_count = 0
    actual_problem_count = 0

    for lesson in book["lessons"]:
        full = lesson["treatment"] in FULL_TREATMENTS
        if full:
            full_count += 1
            if len(lesson["worked_examples"]) < 2:
                failures.append(f"CORE1A_WORKED_EXAMPLE_DEPTH_MISSING:{lesson['lesson_id']}")
            required = set(REQUIRED_ROLES)
            got = set(lesson["practice"])
            missing = sorted(required - got)
            if missing:
                failures.append(f"CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED:{lesson['lesson_id']}:{','.join(missing)}")
            if not lesson["concept_explanation"] or len(lesson["why_it_works"]) < 2:
                failures.append(f"CORE1A_CONCEPT_EXPLANATION_UNDERREALIZED:{lesson['lesson_id']}")
            if not lesson["common_mistake"] or not lesson["repair"]:
                failures.append(f"CORE1_MISCONCEPTION_REPAIR_NOT_MATERIALIZED:{lesson['lesson_id']}")
        for item in lesson.get("practice", {}).values():
            if item.get("source_class") == "NEW_AUTHORED_CORE1A":
                actual_problem_count += 1

    for text in learner_texts(book):
        lower = text.lower()
        for token in FORBIDDEN_LEARNER_TOKENS:
            if token in lower:
                failures.append(f"CORE1A_INTERNAL_JARGON_LEAK:{token}")
        if INTERNAL_CODE_RE.search(text):
            failures.append("CORE1A_INTERNAL_IDENTIFIER_LEAK")

    if failures:
        fail("CORE1A_QUALITY_GATE_FAILED", "|".join(sorted(set(failures))))

    return {
        "status": "PASS",
        "full_teaching_lessons": full_count,
        "actual_problem_instances": actual_problem_count,
        "checks": [
            "NO_INTERNAL_AUTHORING_JARGON",
            "FULL_TEACHING_HAS_TWO_WORKED_EXAMPLES",
            "REQUIRED_PRACTICE_ROLES_MATERIALIZED",
            "MISCONCEPTION_REPAIR_MATERIALIZED",
            "CONCEPT_EXPLANATION_MATERIALIZED",
            "NO_UNRESOLVED_TEMPLATE_TOKENS",
        ],
    }

# -------------------------- textbook PDF --------------------------
def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "BookTitle", parent=base["Title"], fontName=FONT_BOLD,
            fontSize=25, leading=29, textColor=colors.HexColor("#16324F"),
            alignment=TA_CENTER, spaceAfter=10,
        ),
        "chapter": ParagraphStyle(
            "Chapter", parent=base["Heading1"], fontName=FONT_BOLD,
            fontSize=19, leading=23, textColor=colors.HexColor("#16324F"),
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName=FONT_BOLD,
            fontSize=13.5, leading=17, textColor=colors.HexColor("#1E5A7A"),
            spaceBefore=5, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=10.2, leading=14.2, textColor=colors.HexColor("#20262E"),
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=8.8, leading=11.5, textColor=colors.HexColor("#425466"),
        ),
        "example": ParagraphStyle(
            "Example", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=9.8, leading=13.5, leftIndent=4, rightIndent=4,
            textColor=colors.HexColor("#20262E"),
        ),
    }


def card(title: str, body_parts: list[Any], color: str, st: dict) -> Table:
    title_p = Paragraph(f"<b>{safe_text(title)}</b>", ParagraphStyle(
        f"card-{hash(title)}", parent=st["small"], textColor=colors.white, fontName=FONT_BOLD
    ))
    rows = [[title_p]]
    for part in body_parts:
        if isinstance(part, Paragraph):
            rows.append([part])
        else:
            rows.append([Paragraph(safe_text(str(part)), st["example"])])
    t = Table(rows, colWidths=[174 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor(color)),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F9FBFD")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor(color)),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def bullet_paragraphs(items: list[str], st: dict) -> list[Paragraph]:
    return [Paragraph("• " + safe_text(x), st["body"]) for x in items if x]


def example_box(number: int, ex: dict, st: dict) -> Table:
    body: list[Any] = [Paragraph(f"<b>{safe_text(ex['prompt'])}</b>", st["example"])]
    for i, step in enumerate(ex["steps"], 1):
        body.append(Paragraph(f"<b>{i}.</b> {safe_text(step)}", st["example"]))
    body.append(Paragraph(f"<b>Answer:</b> {safe_text(ex['answer'])}", st["example"]))
    return card(f"Worked example {number}", body, "#2E8B57", st)


def practice_box(title: str, item: dict, st: dict, show_hints: int) -> Table:
    parts: list[Any] = [Paragraph(f"<b>{safe_text(item['prompt'])}</b>", st["example"])]
    for i in range(show_hints):
        parts.append(Paragraph(f"<b>Hint {i+1}:</b> {safe_text(item['hints'][i])}", st["example"]))
    return card(title, parts, "#B7791F", st)


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NAME, 8)
    canvas.setFillColor(colors.HexColor("#667788"))
    canvas.drawString(18 * mm, 10 * mm, "Mathematics | Core 1A")
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def render_pdf(book: dict, path: Path) -> dict:
    register_fonts()
    st = styles()
    doc = SimpleDocTemplate(
        str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title="Mathematics Core 1A Student Textbook",
        author="Grade 9 V2 Mathematics",
    )
    story: list[Any] = []
    story.append(Spacer(1, 18))
    story.append(Paragraph("Mathematics", st["title"]))
    story.append(Paragraph("Core 1A — Student Textbook", st["title"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This book develops each idea through examples, explanation, guided practice and independent checks. "
        "Internal authoring and review metadata are intentionally kept out of the learner pages.",
        ParagraphStyle("cover", parent=st["body"], alignment=TA_CENTER, fontSize=11, leading=15)
    ))
    story.append(Spacer(1, 12))
    story.append(card(
        "How to study a lesson",
        [
            "Read the opening example before memorising a rule.",
            "Follow the worked examples line by line and check why each step is legal.",
            "Use hints only when you are stuck; later questions deliberately remove support.",
            "Always perform the final check before accepting an answer.",
        ],
        "#16324F", st
    ))
    story.append(PageBreak())

    for li, lesson in enumerate(book["lessons"], 1):
        story.append(Paragraph(f"{li}. {safe_text(lesson['title'])}", st["chapter"]))
        story.append(Paragraph(safe_text(lesson["opening"]), st["body"]))

        if lesson["what_to_notice"]:
            story.append(Paragraph("What should you notice?", st["h2"]))
            story.extend(bullet_paragraphs(lesson["what_to_notice"], st))

        if lesson["concept_explanation"]:
            story.append(Paragraph("The idea", st["h2"]))
            story.append(Paragraph(safe_text(lesson["concept_explanation"]), st["body"]))

        if lesson["why_it_works"]:
            story.append(Paragraph("Why the method works", st["h2"]))
            for i, step in enumerate(lesson["why_it_works"], 1):
                story.append(Paragraph(f"<b>{i}.</b> {safe_text(step)}", st["body"]))

        for ei, ex in enumerate(lesson["worked_examples"], 1):
            story.append(Spacer(1, 4))
            story.append(example_box(ei, ex, st))
            story.append(Spacer(1, 7))

        if lesson["common_mistake"]:
            story.append(card(
                "Common mistake",
                [lesson["common_mistake"]] + lesson.get("repair", []),
                "#B03A2E", st
            ))
            story.append(Spacer(1, 8))

        practice = lesson["practice"]
        if "GUIDED" in practice:
            story.append(Paragraph("Try it with help", st["h2"]))
            story.append(practice_box("Guided practice", practice["GUIDED"], st, 2))
            story.append(Spacer(1, 6))
        if "FADED" in practice:
            story.append(practice_box("Now with less help", practice["FADED"], st, 1))
            story.append(Spacer(1, 6))
        if "INDEPENDENT" in practice:
            story.append(practice_box("Your turn", practice["INDEPENDENT"], st, 0))
            story.append(Spacer(1, 6))
        if "TRANSFER" in practice:
            story.append(practice_box("Challenge", practice["TRANSFER"], st, 0))
            story.append(Spacer(1, 6))
        if "VERIFY" in practice and lesson["treatment"] not in FULL_TREATMENTS:
            story.append(practice_box("Quick check", practice["VERIFY"], st, 0))
            story.append(Spacer(1, 6))

        if lesson["verification"]:
            story.append(Paragraph("Check your work", st["h2"]))
            story.extend(bullet_paragraphs(lesson["verification"], st))

        if li != len(book["lessons"]):
            story.append(PageBreak())

    story.append(PageBreak())
    story.append(Paragraph("Answer check", st["chapter"]))
    story.append(Paragraph(
        "Use this section after you have attempted the practice. If your answer differs, return to the worked example and identify the first step where your reasoning changed.",
        st["body"],
    ))
    for li, lesson in enumerate(book["lessons"], 1):
        practice = lesson.get("practice", {})
        if not practice:
            continue
        story.append(Paragraph(f"{li}. {safe_text(lesson['title'])}", st["h2"]))
        for role in ("GUIDED", "FADED", "INDEPENDENT", "TRANSFER", "VERIFY"):
            if role not in practice:
                continue
            label = {
                "GUIDED": "Guided practice",
                "FADED": "Less-help practice",
                "INDEPENDENT": "Your turn",
                "TRANSFER": "Challenge",
                "VERIFY": "Quick check",
            }[role]
            story.append(Paragraph(
                f"<b>{label}:</b> {safe_text(practice[role]['answer'])}",
                st["body"],
            ))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    pdf_bytes = path.read_bytes()
    return {
        "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
        "pdf_size_bytes": len(pdf_bytes),
    }

# -------------------------- CLI --------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core1-plan", required=True)
    ap.add_argument("--pck-index", default=str(DEFAULT_PCK_INDEX))
    ap.add_argument("--problem-family-index", default=str(DEFAULT_FAMILY_INDEX))
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    core1 = load(args.core1_plan)
    if core1.get("subject") != "MATHEMATICS":
        fail("CORE1A_NON_MATH_INPUT")
    if core1.get("plan_digest") != digest(core1, "plan_digest"):
        fail("CORE1A_CORE1_PLAN_DIGEST_MISMATCH")

    assets = load_pck_assets(Path(args.pck_index))
    families = load_problem_families(Path(args.problem_family_index))
    book = manuscript(core1, assets, families)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manuscript_path = out / "core1a_textbook_manuscript.json"
    manuscript_path.write_text(json.dumps(book, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    pdf_path = out / "core1a_student_textbook.pdf"
    pdf_meta = render_pdf(book, pdf_path)

    audit = {
        "core1a_book_id": book["core1a_book_id"],
        "source_core1_plan_digest": book["source_core1_plan_digest"],
        "book_digest": book["book_digest"],
        "quality_audit": book["quality_audit"],
        "artifact": {"path": pdf_path.name, **pdf_meta},
        "release_class": book["release_class"],
    }
    (out / "core1a_quality_audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
