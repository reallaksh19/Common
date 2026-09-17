"""Capability-aware learner authoring for Mathematics Core 1A.

The Core1 plan is capability-driven. A single problem family can support several
capabilities, so a family-level exercise bank alone is not sufficient. This
module keeps the problem-family invariant while making the *lesson capability*
the instructional focus of each worked/practice instance.
"""
from __future__ import annotations

import build_math_core1a_textbook as base


CAPABILITY_TITLES = {
    "MATH-ANGLE-SUM": "Angle Sums: Build the Total Before You Infer",
    "MATH-ARITHMETIC-DIVISION": "Division as a Rate: Keep the Quantities in Order",
    "MATH-BINOMIAL-SQUARE-EXPANSION": "Squaring a Binomial Without Losing the Middle Term",
    "MATH-COLLINEARITY-BY-SLOPE": "Testing Whether Points Are Collinear",
    "MATH-COORDINATE-DISTANCE": "Distance Between Two Points",
    "MATH-COORDINATE-QUADRANT-SIGN-TRANSFORM": "Coordinates, Signs and Quadrants",
    "MATH-EQUALITY-PRESERVATION": "Keeping an Equation Balanced",
    "MATH-EQUIDISTANCE-COORDINATE-MODEL": "Turning Equal Distances into Coordinate Equations",
    "MATH-EQUIDISTANT-POINT-ON-AXIS": "A Point on an Axis at Equal Distances",
    "MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE": "Axioms and Postulates: Read the Meaning First",
    "MATH-EUCLID-PARALLEL-CONDITION": "Parallel Lines and the 180° Condition",
    "MATH-FRACTION-ARITHMETIC": "Fractions Inside Coordinate Calculations",
    "MATH-GEOMETRIC-MODELLING": "From a Geometry Statement to Equations",
    "MATH-LINE-EQUATION-FROM-SLOPE-POINT": "Building a Line from Its Slope and One Point",
    "MATH-LINE-EQUATION-FROM-TWO-POINTS": "Building a Line from Two Points",
    "MATH-LINE-Y-INTERCEPT": "Finding a y-Intercept",
    "MATH-LINEAR-EXTRAPOLATION": "Extending a Linear Trend",
    "MATH-LINEAR-PARAMETER-CONDITION": "Parameters: When Is There Enough Information?",
    "MATH-LINEAR-SYSTEM-SETUP": "Turning Two Conditions into a Linear System",
    "MATH-LINEAR-SYSTEM-SOLVE": "Solving a Linear System Without Changing Its Solutions",
    "MATH-ORDERED-PAIR-SEMANTICS": "Ordered Pairs: x First, y Second",
    "MATH-RIVER-CURRENT-MODEL": "River-Current Problems: Why the Speeds Add and Subtract",
    "MATH-SIGN-PROPAGATION": "Tracking Negative Signs Through Algebra",
    "MATH-SLOPE-AS-RATE-OF-CHANGE": "Slope as a Rate of Change",
    "MATH-SLOPE-COMPUTATION": "Computing Slope Reliably",
    "MATH-SUBSTITUTION": "Substitution: Replace the Variable, Then Recalculate",
    "MATH-UNIT-INTERPRETATION": "Reading the Units of a Rate",
    "MATH-UNORDERED-PAIR-COUNT": "Counting Pairs Without Double-Counting",
    "MATH-VARIABLE-SEMANTICS": "What Do the Variables Mean?",
    "MATH-WORD-MODELLING": "From Words to Equations",
}


def I(prompt, steps, answer, hints):
    return base.inst(prompt, steps, answer, hints)


def angle_sum_bank():
    return [
        I("Two angles on a straight line are 118° and x°. Find x.",
          ["Angles on a straight line total 180°.", "118 + x = 180.", "So x = 62."],
          "62°", ["Name the total before calculating.", "Use 180° for a straight line.", "Solve 118 + x = 180."]),
        I("The angles of a triangle are 48°, 67° and x°. Find x.",
          ["A triangle's interior angles total 180°.", "48 + 67 + x = 180.", "So x = 65."],
          "65°", ["Use the triangle angle sum.", "Add the two known angles first.", "x = 180 - 115."]),
        I("Same-side interior angles are 125° and x°. The lines are parallel. Find x.",
          ["For parallel lines, these same-side interior angles total 180°.", "125 + x = 180.", "So x = 55."],
          "55°", ["Which angle total is fixed here?", "Use 180°.", "Solve 125 + x = 180."]),
        I("Around a point, three consecutive angles are 90°, 135° and x°. Find x.",
          ["Angles around a point total 360°.", "90 + 135 + x = 360.", "So x = 135."],
          "135°", ["This is not a straight-line total.", "Angles around a point total 360°.", "Subtract 225° from 360°."]),
        I("A student writes 70° + 80° = 180° to prove two lines parallel. Identify the error.",
          ["The actual sum is 150°, not 180°.", "The parallel-line condition needs the exact required angle relation.", "The conclusion is therefore not justified."],
          "The arithmetic total is wrong; 70° + 80° = 150°.",
          ["Check the numerical sum first.", "Do not apply a theorem to an incorrect total.", "Compare the real total with 180°."]),
        I("Two same-side interior angles are (2x + 20)° and (3x + 10)°. If the lines are parallel, find x and both angles.",
          ["Their sum is 180°: 2x + 20 + 3x + 10 = 180.", "5x + 30 = 180, so x = 30.", "The angles are 80° and 100°."],
          "x = 30; angles 80° and 100°.", ["Translate parallel into an angle-sum equation.", "Collect like terms.", "Check the final two angles total 180°."]),
    ]


def division_bank():
    return [
        I("A boat travels 24 km in 2 h. Find its average speed.",
          ["Speed = distance ÷ time.", "24 ÷ 2 = 12.", "So the speed is 12 km/h."],
          "12 km/h", ["Write the quantity being found with its units.", "Use distance/time.", "Compute 24 ÷ 2."]),
        I("A journey covers 30 km in 3 h. What rate should enter the equation for that journey?",
          ["Rate = 30 km ÷ 3 h.", "30 ÷ 3 = 10.", "The journey rate is 10 km/h."],
          "10 km/h", ["Keep the numerator as distance.", "Time belongs in the denominator.", "30/3 = 10."]),
        I("A boat covers 45 km downstream in 2.5 h. Find the downstream effective speed.",
          ["Effective speed = 45 ÷ 2.5.", "45/2.5 = 18.", "So the downstream speed is 18 km/h."],
          "18 km/h", ["The decimal time is still a divisor.", "Write 45/2.5.", "Multiply numerator and denominator by 10 if useful."]),
        I("Which is the correct speed for 40 km in 5 h: 40/5 or 5/40? Explain.",
          ["Speed has units km/h.", "40/5 has units km per hour; 5/40 has hours per km.", "Therefore 40/5 = 8 km/h is the required speed."],
          "40/5 = 8 km/h", ["Let the units decide the order.", "You want km/h, not h/km.", "Distance is divided by time."]),
        I("A downstream trip is 36 km in 3 h and an upstream trip is 36 km in 4 h. Compute only the two effective speeds.",
          ["Downstream speed = 36/3 = 12 km/h.", "Upstream speed = 36/4 = 9 km/h."],
          "12 km/h downstream; 9 km/h upstream.", ["Do not solve for still-water speed yet.", "Calculate each journey rate separately.", "Use distance/time twice."]),
        I("A student says 15 ÷ 0.5 = 7.5 because 'division makes numbers smaller.' Correct the reasoning.",
          ["Dividing by 0.5 asks how many halves fit into 15.", "There are 30 halves in 15.", "So 15 ÷ 0.5 = 30; division does not always make a number smaller."],
          "30", ["Interpret 0.5 as one half.", "Ask how many halves make 15.", "Check by 30 × 0.5 = 15."]),
    ]


def binomial_square_bank():
    return [
        I("Expand (x - 5)² before using it in a distance equation.",
          ["Write it as (x - 5)(x - 5).", "Multiply every term: x² - 5x - 5x + 25.", "Combine the middle terms: x² - 10x + 25."],
          "x² - 10x + 25", ["A square means repeated multiplication.", "Do not square the two terms separately.", "There are two -5x cross-products."]),
        I("Expand (2x + 3)².",
          ["(2x + 3)(2x + 3).", "Products are 4x², 6x, 6x, 9.", "So 4x² + 12x + 9."],
          "4x² + 12x + 9", ["Use repeated multiplication.", "The middle term appears twice.", "2·(2x)·3 = 12x."]),
        I("In an equidistance equation you meet (x + 2)². Expand it correctly.",
          ["(x + 2)² = (x + 2)(x + 2).", "Multiply: x² + 2x + 2x + 4.", "So x² + 4x + 4."],
          "x² + 4x + 4", ["Use the product form first.", "Find both cross-terms.", "Combine 2x + 2x."]),
        I("A student writes (x - 4)² = x² + 16. What term is missing?",
          ["Expand (x - 4)(x - 4).", "The cross-products are -4x and -4x.", "The missing middle term is -8x."],
          "-8x", ["Multiply, do not distribute the square over subtraction.", "There are two cross-products.", "-4x + -4x = -8x."]),
        I("Simplify (y - 7)² - (y - 1)² without losing any middle terms.",
          ["Expand: y² - 14y + 49 - (y² - 2y + 1).", "Distribute the outer minus: y² - 14y + 49 - y² + 2y - 1.", "So the result is -12y + 48."],
          "-12y + 48", ["Expand both squares first.", "Then distribute the subtraction across the second bracket.", "The y² terms cancel."]),
        I("Explain why (a - b)² and a² - b² are different expressions.",
          ["(a - b)² means (a - b)(a - b), giving a² - 2ab + b².", "a² - b² is a difference of squares and factors as (a - b)(a + b).", "The middle cross-term distinguishes the two structures."],
          "(a - b)² = a² - 2ab + b², not a² - b².", ["Write both expressions as products.", "Compare (a-b)(a-b) with (a-b)(a+b).", "Look at the cross-term."]),
    ]


def equality_bank():
    return [
        I("Solve 3x + 7 = 22 by preserving equality at every step.",
          ["Subtract 7 from both sides: 3x = 15.", "Divide both sides by 3: x = 5.", "Check: 3(5) + 7 = 22."],
          "x = 5", ["Whatever operation you use must be applied to both sides.", "Undo +7 first.", "Then undo ×3."]),
        I("From (x - 1)² + 4 = (x - 5)² + 4, what legal first step simplifies the equation?",
          ["Subtract 4 from both sides.", "This gives (x - 1)² = (x - 5)².", "The solution set is unchanged because the same quantity was removed from both sides."],
          "Subtract 4 from both sides.", ["Look for the same term on both sides.", "Use an equality-preserving operation.", "Remove +4 from both sides."]),
        I("Is it legal to change 2x + 6 = 14 into 2x = 14 by deleting 6? Explain.",
          ["No. Deleting 6 from only one side changes the equality.", "Subtract 6 from both sides instead: 2x = 8.", "Then x = 4."],
          "No; subtract 6 from both sides.", ["An equation is a balance.", "One-sided deletion is not an operation on both sides.", "Use -6 on each side."]),
        I("Solve 5(x - 2) = 3x + 8 and show the equality-preserving moves.",
          ["Expand: 5x - 10 = 3x + 8.", "Subtract 3x from both sides: 2x - 10 = 8.", "Add 10 to both sides: 2x = 18; divide by 2: x = 9."],
          "x = 9", ["Expand first.", "Gather variable terms by doing the same subtraction on both sides.", "Check x = 9 in the original equation."]),
        I("An equidistance equation simplifies to 8x + 1 = 25. Solve it and name the invariant being preserved.",
          ["Subtract 1 from both sides: 8x = 24.", "Divide both sides by 8: x = 3.", "Each step preserves the set of values that make the equation true."],
          "x = 3", ["Use inverse operations symmetrically.", "First remove +1.", "The truth set of the equality should not change."]),
        I("Why can you add 4x to both sides of -4x + 9 = 2x - 3 without changing the solution?",
          ["Equal quantities remain equal when the same quantity is added to both.", "Adding 4x gives 9 = 6x - 3.", "This is equivalent to the original equation for every x."],
          "Because the same operation is applied to both equal sides.", ["Use the balance principle.", "The operation may contain x as long as it is applied identically to both sides.", "Equivalent equations have the same solutions."]),
    ]


def fraction_bank():
    return [
        I("Compute the slope from A(1, 2) to B(4, 7) and leave it as an exact fraction.",
          ["Δy = 7 - 2 = 5.", "Δx = 4 - 1 = 3.", "Slope = 5/3."],
          "5/3", ["Slope is Δy/Δx.", "Keep numerator and denominator roles separate.", "Do not convert to a decimal unless asked."]),
        I("Simplify the slope fraction (-6)/9.",
          ["The greatest common factor of 6 and 9 is 3.", "Divide numerator and denominator by 3.", "(-6)/9 = -2/3."],
          "-2/3", ["Reduce by a common factor.", "The negative sign can sit in the numerator or in front.", "Divide both 6 and 9 by 3."]),
        I("Compute (3/4) - (1/6).",
          ["A common denominator is 12.", "3/4 = 9/12 and 1/6 = 2/12.", "Difference = 7/12."],
          "7/12", ["Do not subtract denominators.", "Use a common denominator.", "Convert to twelfths."]),
        I("A slope calculation gives (1/2)/(3/4). Simplify it.",
          ["Dividing by 3/4 means multiplying by 4/3.", "(1/2)(4/3) = 4/6 = 2/3."],
          "2/3", ["Division by a fraction uses its reciprocal.", "Keep the outer fraction structure clear.", "Multiply 1/2 by 4/3."]),
        I("Which is larger, -2/3 or -3/4? Explain without a calculator.",
          ["Use denominator 12: -2/3 = -8/12 and -3/4 = -9/12.", "-8/12 is closer to zero.", "Therefore -2/3 is larger."],
          "-2/3", ["Use a common denominator.", "For negative numbers, the one closer to zero is larger.", "Compare -8/12 with -9/12."]),
        I("A collinearity test gives slopes 4/6 and 10/15. Are the slopes equal?",
          ["4/6 simplifies to 2/3.", "10/15 simplifies to 2/3.", "Yes, the fractions represent the same slope."],
          "Yes; both equal 2/3.", ["Simplify both fractions before comparing.", "Use common factors 2 and 5 respectively.", "Equivalent fractions can look different."]),
    ]


def two_point_line_bank():
    return [
        I("Find the equation of the line through (1, 2) and (4, 8).",
          ["Slope = (8 - 2)/(4 - 1) = 2.", "Use point-slope form: y - 2 = 2(x - 1).", "So y = 2x."],
          "y = 2x", ["Find the direction from the two points.", "Then anchor the line at either point.", "Check both points in the final equation."]),
        I("Find the line through (-2, 5) and (2, 1).",
          ["Slope = (1 - 5)/(2 - (-2)) = -4/4 = -1.", "Use y - 5 = -(x + 2).", "So y = -x + 3."],
          "y = -x + 3", ["Use the same point order in numerator and denominator.", "Slope is -1.", "Use either given point to finish the equation."]),
        I("The intersection of two lines is P(3, 2). Find the equation of the line through P and Q(1, 4).",
          ["Slope PQ = (4 - 2)/(1 - 3) = -1.", "Use y - 2 = -(x - 3).", "So y = -x + 5."],
          "y = -x + 5", ["Once P is known, this is a two-point line problem.", "Find slope between P and Q.", "Then use point-slope form."]),
        I("Do the points (0, 3) and (5, 3) determine a vertical or horizontal line? Write its equation.",
          ["Both y-coordinates are 3.", "The vertical change is 0, so the slope is 0.", "The line is horizontal: y = 3."],
          "y = 3", ["Compare the coordinates directly.", "Equal y-values mean no vertical change.", "A horizontal line has equation y = constant."]),
        I("Find the line through (4, -1) and (4, 6).",
          ["Both x-coordinates are 4.", "The line is vertical, so ordinary slope division would have denominator 0.", "Its equation is x = 4."],
          "x = 4", ["Check the x-coordinates before dividing.", "Equal x-values signal a vertical line.", "Vertical lines have x = constant."]),
        I("Why should both defining points satisfy your final line equation?",
          ["The line is constructed to contain both points.", "Substituting each point tests that the algebra preserved that requirement.", "If either check fails, the slope or rearrangement is wrong."],
          "Both point-substitution checks must be true.", ["A line equation is a membership test.", "Each defining point must be a member.", "Use substitution as an independent check."]),
    ]


def system_setup_bank():
    return [
        I("Two numbers have sum 11 and difference 3. Write a system; do not solve it yet.",
          ["Let x be the larger number and y the smaller.", "'Sum 11' gives x + y = 11.", "'Difference 3' gives x - y = 3."],
          "x + y = 11, x - y = 3", ["Define the variables first.", "Translate one condition at a time.", "Keep the two conditions as two equations."]),
        I("Two lines are given by 2x + y = 8 and x - y = 1. What system must be solved to find their intersection?",
          ["An intersection must satisfy both line equations at the same time.", "So keep the equations together as the system 2x + y = 8 and x - y = 1."],
          "{2x + y = 8, x - y = 1}", ["Do not combine equations before identifying the system.", "The same x and y must satisfy both.", "Write both original equations unchanged."]),
        I("A boat's downstream speed is 14 km/h and upstream speed is 8 km/h. Let x be still-water speed and y current speed. Write the system.",
          ["Downstream adds the current: x + y = 14.", "Upstream opposes the current: x - y = 8."],
          "x + y = 14, x - y = 8", ["Keep variable meanings fixed.", "Downstream uses plus.", "Upstream uses minus."]),
        I("Adult tickets cost 8 and student tickets cost 5. Fifty tickets bring in 310. Let a and s be the numbers sold. Write the system.",
          ["Ticket count gives a + s = 50.", "Revenue gives 8a + 5s = 310."],
          "a + s = 50, 8a + 5s = 310", ["One equation counts objects; one counts money.", "Attach the correct price to each variable.", "Do not solve until both conditions are represented."]),
        I("Why is x + y = 20 alone not enough to determine x and y uniquely?",
          ["Many ordered pairs have sum 20.", "A unique intersection needs another independent condition.", "So one equation in two free variables describes a family of solutions."],
          "A second independent equation is needed.", ["Try two different pairs with sum 20.", "Both satisfy the same equation.", "Uniqueness needs another constraint."]),
        I("A word problem says one quantity is twice another and their total is 36. Write a system using x and y.",
          ["Let x be the first quantity and y the second.", "'x is twice y' gives x = 2y.", "'total 36' gives x + y = 36."],
          "x = 2y, x + y = 36", ["Translate each sentence separately.", "'Twice' is multiplication, not addition.", "Keep both conditions active."]),
    ]


def system_solve_bank():
    return [
        I("Solve x + y = 9 and x - y = 3.",
          ["Add the equations: 2x = 12.", "So x = 6.", "Substitute back: 6 + y = 9, so y = 3."],
          "x = 6, y = 3", ["Choose an operation that eliminates one variable.", "Adding eliminates y.", "Check the pair in both original equations."]),
        I("Solve 2x + y = 7 and x - y = 2.",
          ["Add equations: 3x = 9, so x = 3.", "Then 3 - y = 2, so y = 1."],
          "x = 3, y = 1", ["Elimination can be immediate here.", "Add the equations.", "Substitute x into either original equation."]),
        I("Solve x + 2y = 8 and 3x - 2y = 8.",
          ["Add the equations: 4x = 16, so x = 4.", "Then 4 + 2y = 8, so y = 2."],
          "x = 4, y = 2", ["Look for opposite coefficients.", "Adding cancels 2y and -2y.", "Verify in both equations."]),
        I("A student changes x + y = 5 into x = 5 and y = 0 without justification. Why is this invalid?",
          ["The original equation permits many pairs, such as (2,3).", "Assigning y = 0 adds a new condition that was not given.", "A system transformation must preserve the entire solution set."],
          "It silently adds a new condition and loses valid solutions.", ["Ask whether every original solution is preserved.", "Try (2,3).", "Equivalent transformations cannot invent constraints."]),
        I("Solve 3x + 2y = 12 and 3x - y = 3.",
          ["Subtract the second equation from the first: 3y = 9, so y = 3.", "Then 3x - 3 = 3, so x = 2."],
          "x = 2, y = 3", ["The x-coefficients already match.", "Subtract the equations.", "Back-substitute and check both originals."]),
        I("Why is substitution into both original equations a stronger check than checking only the final transformed equation?",
          ["A transformation or arithmetic error can produce a candidate that fits the last line but not the original system.", "Both originals are the actual constraints.", "Checking both confirms no solution condition was lost or changed."],
          "Because both original equations define the system's solution.", ["The final line is derived evidence, not the original contract.", "Return to both original equations.", "A valid pair must satisfy both."]),
    ]


def ordered_pair_bank():
    return [
        I("For P(-3, 5), state the x-coordinate and y-coordinate.",
          ["Ordered pairs are written (x, y).", "So x = -3 and y = 5."],
          "x = -3, y = 5", ["Order carries meaning.", "First coordinate is horizontal x.", "Second coordinate is vertical y."]),
        I("Are the points (2, -4) and (-4, 2) the same point? Explain.",
          ["No. The first point has x = 2, y = -4.", "The second has x = -4, y = 2.", "Swapping entries changes their coordinate roles and therefore the location."],
          "No.", ["An ordered pair is not an unordered set.", "Compare x with x and y with y.", "Swapping entries usually changes the point."]),
        I("Point A has x = 0 and y = -6. Write its ordered pair and describe its location.",
          ["The ordered pair is (0, -6).", "x = 0 places it on the y-axis.", "The negative y-value places it below the origin."],
          "(0, -6), on the negative y-axis.", ["Write x first.", "x = 0 means y-axis.", "Then use the sign of y."]),
        I("When computing slope from A(1, 7) to B(5, 3), why must the x-difference use the x-coordinates 5 and 1 rather than 5 and 7?",
          ["The first entry of each ordered pair is an x-coordinate.", "Slope compares matched coordinate changes: Δy over Δx.", "Mixing x and y destroys the geometric meaning of the differences."],
          "Because coordinate roles must remain matched.", ["Label the entries before subtracting.", "First entries belong together.", "Second entries belong together."]),
        I("A point has coordinates (a, b). After swapping the coordinates, what point is obtained? Is it generally the same?",
          ["The swapped point is (b, a).", "It is the same only in special cases such as a = b.", "In general the horizontal and vertical roles have changed."],
          "(b, a); generally different.", ["Write the ordered roles explicitly.", "Swapping changes x from a to b and y from b to a.", "Check the special case a = b."]),
        I("Explain how ordered-pair meaning protects a collinearity slope calculation from a common error.",
          ["Each slope numerator must use y-values and each denominator x-values.", "The ordered-pair convention tells us which entries have which role.", "Respecting that order prevents cross-coordinate subtraction."],
          "It keeps y-differences over x-differences.", ["Slope has two matched differences.", "Use second entries in the numerator, first entries in the denominator.", "Do not mix axes."]),
    ]


def sign_bank():
    return [
        I("Simplify -3 - (-7).",
          ["Subtracting a negative becomes addition.", "-3 - (-7) = -3 + 7 = 4."],
          "4", ["Keep the inner negative inside parentheses.", "Minus a negative changes to plus.", "Compute -3 + 7."]),
        I("Compute the slope numerator y₂ - y₁ when y₂ = -2 and y₁ = 5.",
          ["Substitute with parentheses: (-2) - 5.", "The result is -7."],
          "-7", ["Write the negative value in parentheses.", "The subtraction sign is separate from the number's sign.", "(-2) - 5 = -7."]),
        I("Compute x₂ - x₁ when x₂ = 4 and x₁ = -3.",
          ["4 - (-3) = 4 + 3.", "So the difference is 7."],
          "7", ["Use parentheses around -3.", "Subtracting a negative adds its opposite.", "4 + 3 = 7."]),
        I("Expand (x - 4)² and identify the sign of the middle term.",
          ["(x - 4)(x - 4) gives x² - 4x - 4x + 16.", "The middle term is -8x."],
          "x² - 8x + 16", ["Both cross-products are negative.", "Add -4x and -4x.", "Do not lose the sign when combining."]),
        I("A slope has numerator -6 and denominator -3. Is the slope positive or negative?",
          ["A negative divided by a negative is positive.", "(-6)/(-3) = 2."],
          "Positive; slope = 2.", ["Track the sign separately from the magnitude.", "Same signs divide to positive.", "6/3 = 2."]),
        I("Why should negative coordinates be substituted with parentheses?",
          ["Parentheses keep the sign attached to the value being substituted.", "They distinguish, for example, (-2)² = 4 from -2² = -4 under standard order of operations.", "This prevents sign loss in powers and subtraction."],
          "Parentheses preserve the value's sign during operations.", ["Think about squaring -2.", "Compare (-2)² and -2².", "The notation changes the meaning."]),
    ]


def slope_computation_bank():
    return [
        I("Find the slope through A(1, 2) and B(5, 10).",
          ["Δy = 10 - 2 = 8.", "Δx = 5 - 1 = 4.", "Slope = 8/4 = 2."],
          "2", ["Use Δy/Δx.", "Keep the same point order in both differences.", "Simplify 8/4."]),
        I("Find the slope through (-2, 3) and (4, -5).",
          ["Δy = -5 - 3 = -8.", "Δx = 4 - (-2) = 6.", "Slope = -8/6 = -4/3."],
          "-4/3", ["Use parentheses for negative coordinates.", "Same order in numerator and denominator.", "Reduce the fraction."]),
        I("Find the slope through (3, 7) and (3, -1).",
          ["Δx = 3 - 3 = 0.", "Division by zero is undefined.", "The line is vertical and its slope is undefined."],
          "Undefined", ["Check Δx before dividing.", "A zero denominator signals a vertical line.", "Do not report 0 as the slope."]),
        I("Find the slope through (2, 5) and (8, 5).",
          ["Δy = 0 and Δx = 6.", "Slope = 0/6 = 0.", "The line is horizontal."],
          "0", ["Equal y-values mean no vertical change.", "0 divided by a nonzero number is 0.", "Horizontal lines have slope 0."]),
        I("A student computes (x₂ - x₁)/(y₂ - y₁) and gets 3/2. What has been computed instead of slope?",
          ["Slope is Δy/Δx.", "The student's ratio is Δx/Δy, the reciprocal when both changes are nonzero.", "Its units and geometric meaning are different."],
          "The reciprocal change ratio, not slope.", ["Recall the order: rise/run.", "The numerator should be y-change.", "Check the units or the slope triangle."]),
        I("Explain why reversing the point order does not change a nonvertical slope.",
          ["Reversing order changes both Δy and Δx signs.", "The ratio (-Δy)/(-Δx) equals Δy/Δx.", "So the slope is unchanged."],
          "Both signs reverse, leaving the ratio unchanged.", ["Write the ratio in both point orders.", "Both numerator and denominator are negated.", "A negative divided by a negative restores the original ratio."]),
    ]


def substitution_bank():
    return [
        I("Evaluate 2x + 3 when x = -4.",
          ["Substitute with parentheses: 2(-4) + 3.", "-8 + 3 = -5."],
          "-5", ["Replace every x with the given value.", "Use parentheses for a negative input.", "Then follow order of operations."]),
        I("Does (2, 3) lie on 3x + y = 9?",
          ["Substitute x = 2 and y = 3.", "3(2) + 3 = 9.", "The equality is true, so the point lies on the line."],
          "Yes.", ["A point lies on a line exactly when its coordinates satisfy the equation.", "Substitute both coordinates.", "Check whether both sides are equal."]),
        I("Find the y-intercept of 4x + 2y = 10 by substitution.",
          ["At the y-axis, substitute x = 0.", "2y = 10.", "So y = 5 and the intercept is (0,5)."],
          "(0, 5)", ["The y-axis tells you what to substitute for x.", "Use x = 0.", "Solve the remaining equation."]),
        I("Evaluate x² - 2x at x = -3.",
          ["Substitute: (-3)² - 2(-3).", "9 + 6 = 15."],
          "15", ["Parentheses matter when squaring a negative value.", "Compute the square before subtraction.", "-2(-3) is +6."]),
        I("A student substitutes x = -2 into x² as -2² and writes -4. Explain the error.",
          ["The substituted value is the whole number -2.", "It must be written (-2)².", "That equals 4; without parentheses -2² means -(2²)."],
          "The correct substitution is (-2)² = 4.", ["Treat the negative input as one value.", "Use parentheses.", "Compare (-2)² with -2²."]),
        I("Why is substitution a useful verification method for a line equation you have just derived?",
          ["The defining point should satisfy the final equation.", "Substitution tests that membership directly.", "A failed equality reveals an algebra or construction error."],
          "It checks that the known point is actually on the derived line.", ["A line equation is a membership test.", "Return to the original known point.", "The equation should become a true statement."]),
    ]


def unit_bank():
    return [
        I("Distance is measured in kilometres and time in hours. What are the units of distance/time?",
          ["The ratio is kilometres divided by hours.", "So the units are km/h."],
          "km/h", ["Carry units through the division.", "Numerator unit goes on top.", "Denominator unit goes below."]),
        I("Cost is in rials and distance in km. A slope of 0.8 has what units and meaning?",
          ["Slope = change in cost / change in distance.", "Its units are rials per km.", "It means cost rises by 0.8 rial for each additional kilometre under the linear model."],
          "0.8 rial/km", ["Name dependent per independent units.", "Cost is the output here.", "Interpret one unit of distance."]),
        I("Temperature changes by -6°C over 3 h. State the rate with units and interpret the sign.",
          ["Rate = -6/3 = -2 °C/h.", "The negative sign means temperature decreases by 2°C each hour on average."],
          "-2 °C/h; decreasing.", ["Keep the sign with the change.", "Divide output change by time change.", "Interpret the sign in words."]),
        I("A student reports a speed as 5 h/km. What quantity do those units describe?",
          ["h/km is time per unit distance.", "That is a pace, the reciprocal of km/h speed.", "The units reveal that the ratio was inverted for a speed question."],
          "Pace (time per distance), not speed in km/h.", ["Read units literally.", "h/km means hours for each kilometre.", "Compare with required km/h."]),
        I("A graph has y in litres and x in minutes. What are slope units?",
          ["Slope is change in y divided by change in x.", "So units are litres per minute."],
          "L/min", ["Use y-units over x-units.", "Do not ignore axis labels.", "State the rate as 'litres per minute'."]),
        I("Why can units be used as a check on a slope or rate calculation?",
          ["A correctly oriented ratio has dependent units over independent units.", "If the units appear reversed, the numerator and denominator were likely swapped.", "This check catches a structural error even before the numerical result is judged."],
          "Correct units verify the orientation of the rate ratio.", ["Treat units as algebraic labels.", "Ask which quantity changes per which other quantity.", "Reversed units signal a reversed ratio."]),
    ]


def variable_semantics_bank():
    return [
        I("In a river problem, let x be still-water speed and y current speed. What do x + y and x - y mean?",
          ["x + y combines the boat's still-water speed with the assisting current, so it is downstream speed.", "x - y is the opposing-current case, so it is upstream speed."],
          "x + y = downstream speed; x - y = upstream speed.", ["Keep each symbol tied to its meaning.", "Current helps downstream and opposes upstream.", "Do not treat x + y as a new unrelated variable."]),
        I("In a ticket problem, a is adult tickets and s is student tickets. What does 8a + 5s represent if prices are 8 and 5?",
          ["8a is revenue from adult tickets.", "5s is revenue from student tickets.", "Their sum is total ticket revenue."],
          "Total revenue.", ["Attach each coefficient to the variable's meaning.", "Price × number gives revenue.", "Then add the two revenue parts."]),
        I("Two equations use x and y. Can x mean distance in one equation and speed in the other within the same system?",
          ["No. A system requires the same variable to represent the same quantity across all its equations.", "Changing meaning mid-system breaks the shared unknown structure."],
          "No; variable identity must stay consistent across the system.", ["A symbol is not just a placeholder shape.", "Track its meaning across every equation.", "Shared variables are what link system equations."]),
        I("If P = (x, 0), what does x represent?",
          ["The second coordinate 0 says P lies on the x-axis.", "x is the unknown horizontal coordinate of P."],
          "The unknown horizontal coordinate of P.", ["Read the ordered pair semantically.", "First coordinate = horizontal position.", "The zero already fixes the vertical position."]),
        I("A word problem uses t for time in hours. Why is the equation t + 60 = d suspicious if d is distance in km?",
          ["The terms t and 60 must have compatible meanings to be added, but t is time and 60 has no stated time unit here.", "The equation also equates a time-like expression to distance.", "Variable meanings and units expose a modelling mismatch."],
          "It mixes incompatible quantities unless the constants/variables are redefined.", ["Ask what every symbol and constant means.", "Only like quantities can be added meaningfully.", "Check units on both sides."]),
        I("Explain why writing variable definitions before forming equations reduces modelling errors.",
          ["Definitions give each symbol a stable quantity and unit.", "Every later term can then be checked against that meaning.", "This prevents role swaps and equations that combine incompatible quantities."],
          "Definitions keep symbols tied to consistent quantities and units.", ["Think of definitions as a contract.", "Each equation should respect the contract.", "Stable meanings make errors visible."]),
    ]


def word_modelling_bank():
    return [
        I("A boat travels downstream with still-water speed x and current y. Write the downstream effective speed.",
          ["The current assists the boat downstream.", "So the effects add: downstream speed = x + y."],
          "x + y", ["Identify whether the current helps or opposes.", "Downstream means same direction.", "Helping rates add."]),
        I("Write the upstream effective speed using x for still-water speed and y for current speed.",
          ["Upstream motion opposes the current.", "So current reduces effective speed: x - y."],
          "x - y", ["Upstream means against the current.", "The current reduces progress.", "Use x - y."]),
        I("A 24 km downstream trip takes 2 h. Using x and y as above, write an equation.",
          ["The observed journey speed is 24/2 = 12 km/h.", "Downstream effective speed is x + y.", "So x + y = 12."],
          "x + y = 12", ["Convert the journey data into a rate first.", "Match that rate to the downstream expression.", "Use x + y = distance/time."]),
        I("A 24 km upstream trip takes 3 h. Write the corresponding equation.",
          ["Upstream journey speed = 24/3 = 8 km/h.", "Upstream effective speed is x - y.", "So x - y = 8."],
          "x - y = 8", ["Find distance/time.", "Upstream uses the difference.", "Set x - y equal to the observed rate."]),
        I("A student writes x = 12 and y = 8 from downstream/upstream rates 12 and 8. Explain the modelling error.",
          ["The observed rates are effective combinations, not the individual unknown speeds.", "They give x + y = 12 and x - y = 8.", "Treating them as x and y discards the physical relationships."],
          "The journey rates correspond to x + y and x - y, not x and y separately.", ["Separate unknown quantities from observed compound quantities.", "Ask what each journey measures.", "Translate before solving."]),
        I("Generalise the river model to an aircraft with still-air speed v and wind speed w. Write ground speeds with and against the wind.",
          ["With the wind, the effects combine: v + w.", "Against the wind, the wind opposes motion: v - w.", "The same relative-rate structure transfers to the new context."],
          "v + w with the wind; v - w against it.", ["Look past the river surface context.", "Identify assisting versus opposing rate.", "Keep the compound-speed invariant."]),
    ]


def geometric_modelling_bank():
    return [
        I("A third vertex C(x, y) must be equidistant from A(0, 0) and B(4, 0). Write the equal-distance equation before solving.",
          ["CA² = x² + y².", "CB² = (x - 4)² + y².", "Equidistance gives x² + y² = (x - 4)² + y²."],
          "x² + y² = (x - 4)² + y²", ["Translate the word 'equidistant'.", "Use squared distances.", "Keep both coordinates of C active."]),
        I("A point P lies on the x-axis and is equidistant from A and B. What two constraints should your model preserve?",
          ["The axis condition gives P = (x, 0).", "The equidistance condition gives PA² = PB².", "Both constraints must remain active in the algebra."],
          "P = (x,0) and PA² = PB².", ["Extract geometry before algebra.", "One condition fixes a coordinate.", "The other equates distances."]),
        I("For an equilateral triangle ABC with C(x,y), what distance equations express the geometry?",
          ["Equilateral means all three sides have the same length.", "A useful model is CA² = AB² and CB² = AB².", "These equations preserve the equal-side condition while avoiding square roots."],
          "CA² = AB² and CB² = AB².", ["Translate 'equilateral' into equal side lengths.", "Use squared distances.", "Choose equations that compare C to both fixed vertices."]),
        I("Why is introducing C = (x, y) a modelling step rather than merely notation?",
          ["It converts an unknown geometric location into two algebraic quantities with coordinate meaning.", "Distance and symmetry constraints can then be expressed as equations in x and y.", "The representation opens a legal route from geometry to algebra."],
          "It turns a geometric unknown into algebraic variables while preserving coordinate meaning.", ["Ask what becomes possible after naming coordinates.", "Geometry constraints can now become equations.", "The coordinates still represent a location, not arbitrary symbols."]),
        I("A model for a point on the y-axis uses P = (x, y). What constraint is missing?",
          ["Every point on the y-axis has x = 0.", "The model should be P = (0, y).", "Leaving x free weakens the original geometry and may create false solutions."],
          "The missing constraint is x = 0.", ["Translate the axis literally.", "Which coordinate is zero on the y-axis?", "Build that into the representation immediately."]),
        I("Explain why a final algebraic solution must be checked against the original geometry.",
          ["Algebraic transformations can produce candidates that violate a side condition, axis condition, or branch requirement.", "The original geometry is the governing model.", "Checking distances, location and branch completeness confirms the candidate still represents the stated object."],
          "Because algebraic candidates must still satisfy every original geometric constraint.", ["Return from symbols to the diagram/statement.", "Check axis, distances and side conditions.", "A solved equation is necessary but not always sufficient."]),
    ]


CUSTOM_BANKS = {
    "MATH-ANGLE-SUM": angle_sum_bank,
    "MATH-ARITHMETIC-DIVISION": division_bank,
    "MATH-BINOMIAL-SQUARE-EXPANSION": binomial_square_bank,
    "MATH-EQUALITY-PRESERVATION": equality_bank,
    "MATH-FRACTION-ARITHMETIC": fraction_bank,
    "MATH-GEOMETRIC-MODELLING": geometric_modelling_bank,
    "MATH-LINE-EQUATION-FROM-TWO-POINTS": two_point_line_bank,
    "MATH-LINEAR-SYSTEM-SETUP": system_setup_bank,
    "MATH-LINEAR-SYSTEM-SOLVE": system_solve_bank,
    "MATH-ORDERED-PAIR-SEMANTICS": ordered_pair_bank,
    "MATH-SIGN-PROPAGATION": sign_bank,
    "MATH-SLOPE-COMPUTATION": slope_computation_bank,
    "MATH-SUBSTITUTION": substitution_bank,
    "MATH-UNIT-INTERPRETATION": unit_bank,
    "MATH-VARIABLE-SEMANTICS": variable_semantics_bank,
    "MATH-WORD-MODELLING": word_modelling_bank,
}


def capability_bank(capability_ref: str, family_ref: str):
    if capability_ref in CUSTOM_BANKS:
        rows = CUSTOM_BANKS[capability_ref]()
    else:
        rows = base.family_bank(family_ref)
    if len(rows) < 6:
        base.fail("CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED", capability_ref + ":need_six_instances")
    return rows


def choose_asset_for_capability(lesson, assets):
    capability = lesson["capability_ref"]
    candidates = [assets[x] for x in lesson.get("pck_asset_refs", []) if x in assets]
    for asset in candidates:
        if capability in asset.get("capability_refs", []):
            return asset
    return candidates[0] if candidates else None


def authored_lesson(lesson, assets, families):
    family_id = base.choose_family(lesson)
    capability = lesson["capability_ref"]
    asset = choose_asset_for_capability(lesson, assets)
    family = families.get(family_id) if family_id else None
    full = lesson["treatment"] in base.FULL_TREATMENTS

    if full and not family_id:
        base.fail("CORE1A_PROBLEM_FAMILY_REQUIRED", lesson["lesson_id"])
    if full and family_id not in base.FAMILY_BANKS:
        base.fail("CORE1A_FAMILY_GENERATOR_MISSING", family_id or lesson["lesson_id"])

    bank = capability_bank(capability, family_id) if family_id else []
    practice = base.materialize_practice(bank, lesson) if bank else {}
    title = CAPABILITY_TITLES.get(capability, lesson.get("learner_title") or base.humanize_code(capability))

    recognition = []
    if family:
        recognition = [base.sentence(x) for x in family.get("problem_signature", {}).get("recognition_cues", [])]

    ordinary = base.sentence(asset.get("ordinary_language_bridge", "")) if asset else ""
    anchor = base.sentence(asset.get("anchor", "")) if asset else ""
    route = base.public_route(asset, family)

    mistake = ""
    repair = []
    if asset:
        wrong = asset.get("misconception_discriminator", {}).get("candidate_wrong_model", "")
        probe = asset.get("misconception_discriminator", {}).get("probe", "")
        if wrong:
            mistake = base.sentence(wrong) + (" " + base.sentence(probe) if probe else "")
        repair = [base.sentence(x) for x in asset.get("repair_route", [])]
    elif family and family.get("common_invalid_mechanisms"):
        row = family["common_invalid_mechanisms"][0]
        mistake = base.sentence(row.get("invalid_move", "")) + " " + base.sentence(row.get("why_invalid", ""))

    verification = []
    if asset:
        verification.extend(base.sentence(x) for x in asset.get("verification_method", []))
    verification.extend(base.public_phrase(x) for x in lesson.get("verification_requirements", []))
    verification = list(dict.fromkeys(x for x in verification if x))

    return {
        "lesson_id": lesson["lesson_id"],
        "title": title,
        "treatment": lesson["treatment"],
        "family_ref": family_id,
        "opening": ordinary or "Begin by identifying the mathematical roles before calculating.",
        "concept_explanation": anchor or (base.sentence(family.get("problem_signature", {}).get("target_job", "")) if family else ""),
        "what_to_notice": recognition,
        "why_it_works": route,
        "common_mistake": mistake,
        "repair": repair,
        "worked_examples": (
            [
                {"prompt": bank[0].prompt, "steps": list(bank[0].steps), "answer": bank[0].answer},
                {"prompt": bank[1].prompt, "steps": list(bank[1].steps), "answer": bank[1].answer},
            ] if full else []
        ),
        "practice": practice,
        "verification": verification,
        "source_trace": {
            "core1_lesson_ref": lesson["lesson_id"],
            "assessment_question_refs": list(lesson.get("assessment_question_refs", [])),
            "pck_asset_refs": list(lesson.get("pck_asset_refs", [])),
        },
    }


def install():
    """Install capability-aware authoring into the shared Core1A infrastructure."""
    base.authored_lesson = authored_lesson
    return base
