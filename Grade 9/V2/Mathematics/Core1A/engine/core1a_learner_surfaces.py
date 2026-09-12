"""Student-facing prose for Core1A.

PCK records are authoring authority, not publishable prose. Their repair routes and
misconception probes may contain teacher directives (for example, "ask for..." or
"ban immediate recall"). Core1A keeps those records in trace data and realizes a
separate Grade-9 learner surface here.
"""
from __future__ import annotations

import build_math_core1a_textbook as base
import core1a_capability_authoring as cap


def S(opening, idea, notice, why, mistake, repair, verify):
    return {
        "opening": opening,
        "concept_explanation": idea,
        "what_to_notice": notice,
        "why_it_works": why,
        "common_mistake": mistake,
        "repair": repair,
        "verification": verify,
    }


SURFACES = {
    "MATH-ANGLE-SUM": S(
        "Angle problems become much easier when you decide the required total before doing any algebra.",
        "Different diagrams have different fixed totals. Angles on a straight line total 180°, angles in a triangle total 180°, and angles around a point total 360°. In parallel-line problems, a 180° same-side interior sum is an important boundary condition.",
        ["Which group of angles is being added?", "What total should that group have?", "Is the total exact, or only visually suggested by the drawing?"],
        ["Identify the angle relationship before calculating.", "Write one equation that expresses the required total.", "Solve the equation, then substitute the answer back into the angle sum.", "Use the completed angle relation to make any geometric conclusion."],
        "A diagram can look convincing even when its angle measures do not satisfy the required total. A drawing is evidence only after the angle relation is checked.",
        ["Write the required total beside the diagram.", "Add the actual angle expressions rather than estimating from appearance.", "Check the final angles add to the stated total."],
        ["Re-add the final angles.", "If a parallel-line conclusion is made, confirm the exact 180° condition that supports it."],
    ),
    "MATH-ARITHMETIC-DIVISION": S(
        "In rate problems, division answers a very specific question: how much of one quantity corresponds to one unit of another quantity?",
        "A quotient keeps the meanings of its numerator and denominator. For speed, distance is divided by time, so the units are distance per unit time. Reversing the division gives a different quantity.",
        ["What quantity is being divided?", "What quantity tells you the number of equal time or distance units?", "What units should the quotient have?"],
        ["Name the target quantity and its units.", "Write the division in the order required by those units.", "Calculate the quotient.", "Read the answer back in context instead of leaving it as a bare number."],
        "A common error is to reverse the division because both numbers appear in the question. For a speed in km/h, hours must not be placed over kilometres.",
        ["Write the desired units first, such as km/h.", "Place the matching quantity in each part of the fraction.", "Check by multiplying rate × time to see whether the original distance is recovered."],
        ["Check the units.", "Reverse the operation: rate × denominator quantity should recover the numerator quantity."],
    ),
    "MATH-BINOMIAL-SQUARE-EXPANSION": S(
        "Squaring a bracket means multiplying the whole bracket by itself. That is why a middle term appears.",
        "For (a - b)², write (a - b)(a - b). The products are a², -ab, -ab and b², so the result is a² - 2ab + b². The same repeated-product idea works for a plus sign.",
        ["A square applies to the entire bracket.", "There are two cross-products.", "The sign of the middle term comes from those cross-products."],
        ["Rewrite the square as two equal factors.", "Multiply every term in the first factor by every term in the second.", "Combine the two cross-products.", "Only then write the compact identity."],
        "Writing (a - b)² as a² + b² loses both cross-products. The square does not distribute over addition or subtraction.",
        ["For one line, ignore the memorised formula and write the repeated product.", "Mark the two cross-products explicitly.", "Combine them and check their sign before simplifying."],
        ["Multiply the final expression back from (a - b)(a - b).", "Test a simple numerical value if you are unsure about the middle sign."],
    ),
    "MATH-COLLINEARITY-BY-SLOPE": S(
        "Three points are collinear when they lie on one straight line. On a coordinate plane, that means they share one direction.",
        "For nonvertical lines, direction is measured by slope. If the slope from one reference point to the second point equals the slope from the same reference point to the third point, the three points have the same direction and are collinear.",
        ["Use a common reference point.", "Keep the point order consistent in each slope.", "Check separately for a vertical-line case before dividing by a zero horizontal change."],
        ["Choose one point as a reference.", "Compute two comparable slopes.", "Compare the simplified slopes.", "If they agree, verify that all three points satisfy the same line relation."],
        "Being on the same coordinate plane does not make points collinear. Collinear means 'on the same straight line', not merely 'drawn on the same graph'.",
        ["Use a direction test, not a visual guess.", "Compute slopes or identify the common vertical line.", "State the line relation that all three points share."],
        ["Check a third pair or substitute all three points into one line equation.", "For a vertical line, confirm all x-coordinates are equal."],
    ),
    "MATH-COORDINATE-DISTANCE": S(
        "The straight-line distance between two points comes from a right triangle: one leg is the horizontal change and the other is the vertical change.",
        "If A(x₁, y₁) and B(x₂, y₂) are two points, the horizontal and vertical changes are x₂ - x₁ and y₂ - y₁. By the Pythagorean theorem, distance = √[(x₂ - x₁)² + (y₂ - y₁)²].",
        ["Match x-coordinates with x-coordinates.", "Match y-coordinates with y-coordinates.", "Distance is non-negative."],
        ["Find the horizontal change.", "Find the vertical change using the same point order.", "Square the two changes and add them.", "Take the non-negative square root."],
        "Mixing an x-coordinate with a y-coordinate destroys the geometric meaning of the two perpendicular changes.",
        ["Write the points in aligned (x, y) columns.", "Form one x-difference and one y-difference only.", "Use the two differences as the legs of the right triangle."],
        ["Reverse the point order; the distance should stay the same.", "Check that the result is non-negative and plausible compared with the horizontal and vertical changes."],
    ),
    "MATH-COORDINATE-QUADRANT-SIGN-TRANSFORM": S(
        "A quadrant is determined by the signs of an ordered pair, and the order of the coordinates matters.",
        "The sign patterns are I: (+,+), II: (-,+), III: (-,-), IV: (+,-). A transformation such as (-x, y) or (x, -y) changes only the sign named by the expression; it does not swap coordinate roles.",
        ["First coordinate = x, second coordinate = y.", "Track sign changes one coordinate at a time.", "Points on an axis are not inside a quadrant."],
        ["Write the original sign pair.", "Apply the requested sign change to x and y separately.", "Read the new sign pair in order.", "Map that pair to a quadrant or axis."],
        "A common error is to change the wrong coordinate or to swap x and y while changing signs.",
        ["Keep the ordered pair written as (x, y).", "Mark only the coordinate whose sign changes.", "Classify the result after the transformation, not before it."],
        ["Test the rule with a simple sample point from the stated signs.", "Confirm that x still controls horizontal position and y vertical position."],
    ),
    "MATH-EQUALITY-PRESERVATION": S(
        "An equation is a balance: every legal step must keep both sides equal for exactly the same solutions.",
        "Adding, subtracting, multiplying or dividing both sides by the same allowed quantity preserves equality. This is why equation solving is not 'moving terms'; it is applying equivalent operations to both sides.",
        ["What operation is being undone?", "Was the same operation applied to both sides?", "Did any division introduce a forbidden zero divisor?"],
        ["Choose an inverse operation that simplifies the equation.", "Apply it to both sides.", "Repeat until the unknown is isolated.", "Substitute the result into the original equation."],
        "Deleting a term from one side because you want it to disappear changes the equation unless the matching operation is also applied to the other side.",
        ["Write the operation beside both sides, such as '-7' on each side.", "Simplify only after the balanced operation is shown.", "Check the solution in the original equation."],
        ["Substitute the solution into the original equation.", "Both original sides must evaluate to the same value."],
    ),
    "MATH-EQUIDISTANCE-COORDINATE-MODEL": S(
        "A geometric statement such as 'equidistant' can be turned into an equation without losing its meaning.",
        "If a point C(x, y) is equally far from A and B, then CA = CB. Because distances are non-negative, it is usually simpler to write CA² = CB² and use the coordinate-distance expressions on both sides.",
        ["Name the unknown point with coordinates.", "Translate 'equidistant' into equal distances.", "Keep every geometric side condition, including mirror possibilities."],
        ["Introduce coordinates for the unknown point.", "Write squared-distance expressions to the required fixed points.", "Equate the distances that the geometry says are equal.", "Solve the resulting equations.", "Return to the geometry and retain every valid branch."],
        "Solving one distance equation is not enough for an equilateral or multi-constraint problem. A candidate must satisfy all of the original equal-distance conditions.",
        ["Write each required distance relation before solving.", "Do not discard a plus/minus branch unless the problem gives a side condition.", "Verify every final candidate against the original distances."],
        ["Compute the required squared distances for every candidate.", "Confirm that all original geometric conditions are satisfied."],
    ),
    "MATH-EQUIDISTANT-POINT-ON-AXIS": S(
        "When a point is restricted to an axis, one of its coordinates is already known. Use that information before writing any distance equation.",
        "A point on the x-axis has form (x, 0); a point on the y-axis has form (0, y). If it is equidistant from A and B, write PA² = PB². The axis constraint and the equal-distance condition must both remain active.",
        ["Which coordinate is fixed by the axis?", "Which two distances are equal?", "Squared distances remove unnecessary square roots."],
        ["Write the unknown point using the axis-fixed coordinate.", "Form the two squared-distance expressions.", "Set them equal and simplify.", "Solve for the remaining coordinate.", "Check axis membership and both distances."],
        "Leaving both coordinates free ignores information given by the axis and can produce unnecessary or false solutions.",
        ["Write (x,0) or (0,y) immediately.", "Then form the equal-distance equation.", "Check that the final point still lies on the required axis."],
        ["Confirm the fixed coordinate is zero.", "Compare the two distances from the final point."],
    ),
    "MATH-EUCLID-CLASSIFY-AXIOM-POSTULATE": S(
        "Do not classify a foundational statement by how familiar it sounds. Classify it by what kind of mathematical claim it makes.",
        "An axiom is used as a general foundational truth, while a Euclidean postulate is a foundational assumption specific to geometry. The wording may change; the mathematical status is what matters.",
        ["Is the statement general across mathematics?", "Does it specifically concern geometric objects or constructions?", "Separate the underlying claim from its surface wording."],
        ["Restate the sentence in your own words.", "Identify the mathematical objects and scope.", "Compare that scope with the axiom/postulate distinction.", "State the classification and justify it from the scope."],
        "Recognising a sentence from memory is not a proof of its classification. Similar wording can hide different mathematical status.",
        ["Ignore familiarity for a moment.", "Ask whether the claim is general or geometry-specific.", "Use that criterion in the justification."],
        ["Your reason should still work if the statement is paraphrased.", "Check that the justification names the mathematical scope, not just the label."],
    ),
    "MATH-EUCLID-PARALLEL-CONDITION": S(
        "Euclid's parallel condition is about a precise angle sum, not about whether two drawn lines look parallel.",
        "For a transversal cutting two lines, if the same-side interior angles sum to less than 180°, the lines meet on that side. A sum of exactly 180° is the parallel boundary in this setting.",
        ["Identify the transversal and the same-side interior angles.", "Add the actual angle measures.", "Compare the result with 180° exactly."],
        ["Locate the relevant pair of interior angles.", "Calculate their sum.", "Compare the sum with 180°.", "Use the correct logical direction: given parallel lines gives an angle relation; an angle relation can justify parallelism only when the relevant converse is available."],
        "Lines that look nearly parallel in a sketch can still meet. The diagram is not a substitute for the angle condition.",
        ["Use stated or derived angle measures.", "Write the comparison with 180°.", "Make the geometric conclusion only after the condition is satisfied."],
        ["Recheck the angle sum.", "State whether you used a theorem or its converse and confirm that the direction of reasoning matches the given information."],
    ),
    "MATH-FRACTION-ARITHMETIC": S(
        "Fractions often appear naturally in slopes and coordinate calculations. Exact fraction arithmetic keeps the geometry visible and avoids rounding errors.",
        "To add or subtract fractions, use a common denominator. To divide by a fraction, multiply by its reciprocal. Always simplify the final fraction without changing its sign.",
        ["What operation is being performed?", "Do the denominators need to match?", "Can the final fraction be reduced?"],
        ["Keep the sign attached to the numerator or to the whole fraction.", "For addition/subtraction, rewrite with a common denominator.", "For division, multiply by the reciprocal.", "Reduce by common factors and interpret the result in the original calculation."],
        "Subtracting denominators or cancelling across addition changes the value of the expression.",
        ["Write one legal fraction operation per line.", "Cancel only common factors in a product, not terms separated by + or -.", "Check equivalent fractions by cross-multiplication if needed."],
        ["Convert the result back to an equivalent unsimplified form or decimal estimate to check size and sign.", "In a slope, confirm the sign agrees with the direction of the line."],
    ),
    "MATH-GEOMETRIC-MODELLING": S(
        "A coordinate model is useful only when every equation still represents a fact from the geometry.",
        "Model in two stages: first translate the geometric constraints into coordinates and distance relations; only then solve the algebra. Keeping the model and the solving stage separate makes it easier to see whether an algebraic answer still fits the original figure.",
        ["What is fixed by the geometry?", "Which point or length is unknown?", "Which equalities express the geometric condition?"],
        ["Name the unknown coordinates.", "Write each geometric constraint as a coordinate or distance statement.", "Use squared distances when equality of distance is the key relation.", "Solve the algebra after the model is complete.", "Check every candidate in the original geometry."],
        "Starting with algebra before writing all geometric constraints can solve the wrong problem perfectly.",
        ["List the geometry facts first.", "Translate each fact into one algebraic relation.", "Do not simplify away a condition before it has been represented."],
        ["Return each solution to the geometry.", "Check distances, axis conditions and all valid branches."],
    ),
    "MATH-LINE-EQUATION-FROM-SLOPE-POINT": S(
        "A slope tells you the direction of a line, but one point is needed to fix which line with that direction you mean.",
        "If a line has slope m and passes through (x₁, y₁), point-slope form y - y₁ = m(x - x₁) builds the line directly. You may then rearrange it into another equivalent form.",
        ["Identify the slope and the known point separately.", "Keep signs inside x - x₁ and y - y₁.", "Equivalent line forms should describe the same set of points."],
        ["Write point-slope form with the known slope.", "Substitute the known point coordinates.", "Simplify to the requested form.", "Check the known point in the final equation and confirm the slope."],
        "Using a visible coefficient as the slope without first identifying the equation form can select the wrong direction.",
        ["Read or calculate the slope before writing the new line.", "Use the known point to anchor that direction.", "Check both slope and point membership."],
        ["Substitute the given point into the final equation.", "Read or recompute the slope from the final form."],
    ),
    "MATH-LINE-EQUATION-FROM-TWO-POINTS": S(
        "Two distinct points determine one straight line. First use them to find its direction; then use either point to anchor the equation.",
        "For nonvertical points, calculate m = (y₂ - y₁)/(x₂ - x₁), using the same point order in numerator and denominator. Then use point-slope form. If x₁ = x₂, the line is vertical and has equation x = x₁.",
        ["Check first for a vertical line.", "Use the same point order in both coordinate differences.", "Both given points must satisfy the final equation."],
        ["Compare x-coordinates for the vertical case.", "Otherwise calculate the slope.", "Use one point in point-slope form.", "Simplify and verify the second point."],
        "A slope computed with inconsistent point order can have the wrong sign and produce a line through only one of the two points.",
        ["Write the two points in a fixed order.", "Use that order for both Δy and Δx.", "Test both points in the final equation."],
        ["Substitute both defining points.", "If the line is nonvertical, recompute its slope from the final equation."],
    ),
    "MATH-LINE-Y-INTERCEPT": S(
        "The y-intercept is not found by memorising which number to copy. It comes from the meaning of the y-axis.",
        "Every point on the y-axis has x = 0. Therefore, to find a y-intercept, substitute x = 0 into the line equation and solve for y. The intercept is the point (0, y).",
        ["The requested axis fixes one coordinate.", "For the y-axis, x = 0.", "An intercept is a point, not only a number."],
        ["Set x = 0 because the point lies on the y-axis.", "Solve the remaining one-variable equation.", "Write the result as (0, y).", "Substitute the point into the original equation."],
        "Setting y = 0 finds the x-intercept, not the y-intercept.",
        ["Say the axis name aloud.", "Write the coordinate that must be zero on that axis.", "Only then substitute and solve."],
        ["Check the first coordinate is 0.", "Substitute the full intercept point into the original line equation."],
    ),
    "MATH-LINEAR-EXTRAPOLATION": S(
        "A linear model says the same rate of change continues as the input changes. Extrapolation uses that rate beyond the given data.",
        "Find the change in output per unit change in input, then extend that same rate to the target input. The arithmetic is valid only under the stated assumption that the relationship remains linear.",
        ["Which quantity is input and which is output?", "What is the rate of output change per input unit?", "Is the target inside or outside the observed range?"],
        ["Compute the rate from two data points.", "Interpret its sign and units.", "Find the input change from a known point to the target.", "Apply the same rate to estimate the output.", "State that the estimate depends on the linearity assumption."],
        "A mathematically correct line can still be a poor real-world prediction if there is no reason to expect the linear pattern to continue.",
        ["Separate the calculation from the modelling assumption.", "State the rate and units.", "Mark an outside-range prediction as an extrapolation rather than a measured fact."],
        ["Replay the rate step from a known point to the target.", "Check units and whether the direction of change matches the sign of the rate."],
    ),
    "MATH-LINEAR-PARAMETER-CONDITION": S(
        "A parameter is not automatically a fixed number. It becomes uniquely determined only when the available conditions provide enough independent information.",
        "Substitute every given relation or point into the parameterised equation, then inspect what remains. If one equation still contains two free quantities, many values may be possible. Do not invent an extra condition to force one answer.",
        ["What is known?", "Which quantities are still free after substitution?", "How many independent conditions are available?"],
        ["Use every stated condition exactly once.", "Simplify to a relation involving the parameter and any remaining unknowns.", "Check whether that relation determines one unique parameter.", "If not, state the underdetermination rather than guessing."],
        "Choosing a convenient value for a remaining variable can create one possible parameter value, but it does not prove that value is unique.",
        ["Count the remaining degrees of freedom.", "Try two different values of the free quantity if necessary.", "Conclude 'not uniquely determined' when multiple parameter values remain possible."],
        ["Substitute any claimed parameter back with the original conditions.", "Check uniqueness, not only existence."],
    ),
    "MATH-LINEAR-SYSTEM-SETUP": S(
        "A system begins before any elimination: it begins by turning two independent conditions into two equations that use the same variable meanings.",
        "Define the unknowns, translate each condition separately, and keep the equations together. The same x and y must represent the same quantities in every equation.",
        ["What does each variable mean?", "What two independent conditions are given?", "Do both equations use the variables with the same meaning and units?"],
        ["Define the variables.", "Translate the first condition into an equation.", "Translate the second condition into another equation.", "Check that both equations refer to the same unknown quantities.", "Only then choose a solving method."],
        "Combining numbers before the two conditions are represented can hide a missing equation or change what a variable means.",
        ["Write a short variable definition first.", "Build one equation per condition.", "Read each equation back in words to see whether it matches the statement."],
        ["Check units and variable meanings term by term.", "Confirm that a candidate solution would need to satisfy both equations."],
    ),
    "MATH-LINEAR-SYSTEM-SOLVE": S(
        "Solving a system means finding values that make all of its equations true at the same time.",
        "Elimination and substitution are useful because they replace the system with equivalent equations that preserve the common solution. Every algebraic move must keep that solution set unchanged.",
        ["Look for coefficients that can cancel.", "Use equality-preserving operations.", "The final ordered pair must satisfy both original equations."],
        ["Choose elimination or substitution deliberately.", "Perform the same legal operation required to keep equations equivalent.", "Solve the resulting one-variable equation.", "Back-substitute for the second variable.", "Verify the ordered pair in both original equations."],
        "Deleting a term because it is inconvenient can remove valid solutions or create false ones.",
        ["Show the equation addition, subtraction or substitution explicitly.", "Do not change only part of an equation.", "Check the final pair in both original equations."],
        ["Substitute the pair into both originals.", "Each equation must become a true numerical statement."],
    ),
    "MATH-ORDERED-PAIR-SEMANTICS": S(
        "An ordered pair is not just two numbers in brackets. The first and second positions have different jobs.",
        "In (x, y), x gives horizontal position and y gives vertical position. Coordinate formulas work only when those roles stay attached during subtraction, transformation and interpretation.",
        ["First coordinate = x = horizontal.", "Second coordinate = y = vertical.", "Swapping entries usually changes the point."],
        ["Label x and y before calculating.", "Match first coordinates with first coordinates.", "Match second coordinates with second coordinates.", "Interpret the final pair in the same order."],
        "Subtracting an x-coordinate from a y-coordinate may produce a number, but it no longer represents a horizontal or vertical change.",
        ["Align the ordered pairs vertically if needed.", "Form x-differences only from first entries and y-differences only from second entries.", "Check the result against the graph meaning."],
        ["Swap the point order without swapping coordinate roles; the geometric relationship should remain consistent.", "Check axis cases such as x = 0 or y = 0 explicitly."],
    ),
    "MATH-RIVER-CURRENT-MODEL": S(
        "The boat and the current contribute to the same effective speed. Their effects add when they act together and subtract when they oppose each other.",
        "Let x be the boat's still-water speed and y the current speed. Downstream effective speed is x + y; upstream effective speed is x - y. Journey data then connect these expressions to distance ÷ time.",
        ["Keep still-water speed and current speed as separate quantities.", "Downstream: current assists.", "Upstream: current opposes.", "A physical solution normally needs x > y ≥ 0."],
        ["Define x and y with units.", "Convert each journey into an observed speed.", "Match downstream to x + y and upstream to x - y.", "Solve the resulting equations.", "Replay both journeys to verify the times."],
        "Treating a downstream speed such as 12 km/h as x alone ignores the current that helped produce that observed speed.",
        ["Distinguish individual speeds from compound effective speeds.", "Write x + y and x - y before inserting numbers.", "Check the solved values by recomputing both journey speeds."],
        ["Check x + y and x - y against the observed rates.", "Recompute both travel times and check x > y ≥ 0."],
    ),
    "MATH-SIGN-PROPAGATION": S(
        "A negative sign can belong to a number, an operation, or both. Parentheses keep those roles clear.",
        "When substituting or subtracting negative values, write the negative value in parentheses first. Then apply the operation. This prevents mistakes such as confusing 4 - (-3) with 4 - 3.",
        ["Is the sign part of the value or the operation?", "Use parentheses around substituted negative numbers.", "Track the sign before simplifying the magnitude."],
        ["Copy the expression before substituting.", "Insert negative values with parentheses.", "Apply exponent and multiplication rules before addition/subtraction.", "Check the final sign against a simple number-line or direction interpretation."],
        "Dropping parentheses too early can change subtraction of a negative into subtraction of a positive, or can change the meaning of a power.",
        ["Keep parentheses for one full calculation line.", "Handle double negatives deliberately.", "For powers, compare (-2)² with -2² before proceeding."],
        ["Estimate the sign before calculating fully.", "Substitute the result back into the original expression if possible."],
    ),
    "MATH-SLOPE-AS-RATE-OF-CHANGE": S(
        "Slope tells how much the output changes when the input increases by one unit.",
        "For two points (x₁, y₁) and (x₂, y₂), slope m = (y₂ - y₁)/(x₂ - x₁). In a context, its units are 'y-units per x-unit', so the sign and units are part of the meaning, not decoration.",
        ["Which variable is the input?", "Which variable is the output?", "What units should 'output change per input change' have?"],
        ["Calculate the output change.", "Calculate the input change using the same point order.", "Divide output change by input change.", "Interpret the sign and units in words."],
        "Using the reciprocal ratio can produce a neat number but answers a different question because its units are reversed.",
        ["Write the desired rate units before the calculation.", "Put the matching change in the numerator and denominator.", "Explain what one unit of input does to the output."],
        ["Check the units.", "Use the rate to predict the change over a small input interval and compare with the data."],
    ),
    "MATH-SLOPE-COMPUTATION": S(
        "Slope is a signed ratio of vertical change to horizontal change. Reliable computation depends on consistent coordinate order.",
        "Use m = Δy/Δx. Choose either point order, but use that same order in both differences. A zero Δx gives a vertical line with undefined slope; a zero Δy gives a horizontal line with slope 0.",
        ["Use y-change over x-change.", "Keep point order consistent.", "Check for Δx = 0 before dividing."],
        ["Write the two ordered pairs.", "Compute Δy.", "Compute Δx in the same order.", "Form and simplify the ratio.", "Interpret zero or undefined special cases correctly."],
        "Using Δx/Δy computes the reciprocal change ratio, not slope, and often reverses the intended units.",
        ["Remember 'rise over run'.", "Label numerator Δy and denominator Δx before inserting numbers.", "Check the result against whether the line rises or falls from left to right."],
        ["Reverse the point order; the slope should be unchanged.", "Check the sign against the graph direction."],
    ),
    "MATH-SUBSTITUTION": S(
        "Substitution means replacing a variable by a value everywhere it appears, while preserving the value's sign and grouping.",
        "Write negative substituted values in parentheses. Then follow the usual order of operations. In coordinate geometry, substitution also acts as a membership check: a point lies on a line exactly when its coordinates make the equation true.",
        ["Replace every occurrence of the variable.", "Use parentheses for negative values.", "After substitution, the result should be an ordinary numerical calculation or truth check."],
        ["Copy the original expression or equation.", "Insert the given value with clear parentheses.", "Evaluate powers and products before sums.", "If checking a point, compare the two sides of the equation."],
        "Writing x = -2 into x² as -2² changes the meaning because the negative sign is no longer grouped with the substituted value.",
        ["Treat the substituted number as one object.", "Write (-2)², not -2², when the whole value is squared.", "Check the numerical result independently."],
        ["Re-evaluate using a calculator only after the algebraic substitution is written correctly.", "For a point check, verify the original equation becomes true."],
    ),
    "MATH-UNIT-INTERPRETATION": S(
        "Units tell you what a rate actually measures, and they can expose a reversed ratio immediately.",
        "If y is measured in litres and x in minutes, slope has units litres per minute. The numerator's units belong to the dependent/output change; the denominator's units belong to the independent/input change.",
        ["Read the axis or variable units before computing.", "State the rate as 'output units per input unit'.", "Interpret the sign as increase or decrease in context."],
        ["Identify output and input quantities.", "Write their units in the slope ratio.", "Compute the numerical rate.", "State what one unit of input changes in the output."],
        "A reciprocal rate may have a reasonable number but the wrong units, such as h/km when the question asks for km/h.",
        ["Write the required units first.", "Use them to choose numerator and denominator.", "If the units come out reversed, revisit the ratio before accepting the number."],
        ["Check units algebraically.", "Describe the rate in one sentence and see whether that sentence matches the context."],
    ),
    "MATH-UNORDERED-PAIR-COUNT": S(
        "When order does not create a new outcome, AB and BA are the same pair and must be counted only once.",
        "With n objects, n(n - 1) counts ordered choices of two different objects. Every unordered pair appears twice, once as AB and once as BA, so the number of pairs is n(n - 1)/2.",
        ["Does order matter in the context?", "Are self-pairs allowed?", "Is each pair meant to be counted once?"],
        ["Decide that the objects form unordered pairs.", "Count n choices followed by n - 1 different partners.", "Divide by 2 because every pair was counted in two orders.", "Check a small case by listing pairs."],
        "Counting AB and BA as different doubles the answer in a handshake, game or complete-graph problem.",
        ["List pairs for three or four objects to see the duplication.", "Use one consistent ordering rule or divide the ordered count by 2.", "Check that no self-pair such as AA was included."],
        ["For a small n, list every pair explicitly.", "Check that the formula gives the same count."],
    ),
    "MATH-VARIABLE-SEMANTICS": S(
        "A variable is a named quantity, not just a letter. Its meaning and units must stay the same throughout a model or system.",
        "Before writing equations, define what each variable represents. Then every term can be checked: coefficients, sums and differences must combine quantities in ways that make sense in the context.",
        ["What quantity does each symbol represent?", "What units does it carry?", "Does that meaning stay unchanged in every equation?"],
        ["Write a short variable definition.", "Translate each term using that definition.", "Check that quantities being added or compared are compatible.", "Keep the same variable meaning across the entire system."],
        "Letting x mean one quantity in one equation and a different quantity in another breaks the system even if the algebra looks tidy.",
        ["Return to the variable definitions whenever a new equation is written.", "Read each equation aloud in the context.", "Use units as an extra consistency check."],
        ["Explain the final value with its quantity name and unit.", "Substitute it back into every contextual equation."],
    ),
    "MATH-WORD-MODELLING": S(
        "A word problem becomes algebra only after the relationships in the story have been identified.",
        "Define the unknown quantities first, then translate one sentence or condition at a time. Compound quantities such as downstream speed must stay compound: if x is still-water speed and y current speed, downstream is x + y and upstream is x - y.",
        ["Which quantities are unknown?", "Which statements give independent relationships?", "Does each algebraic expression still have the meaning of the sentence it represents?"],
        ["Define variables with units.", "Translate the first relationship.", "Translate the next relationship independently.", "Combine the equations only after the model is complete.", "Read the equations back in words before solving."],
        "Assigning an observed compound quantity directly to one variable can erase part of the situation. For example, downstream speed is not the still-water speed alone.",
        ["Separate basic unknowns from quantities formed from them.", "Write the verbal relationship before inserting numbers.", "Check every term's meaning and units."],
        ["Read each finished equation aloud in the original context.", "After solving, replay the original conditions with the numerical values."],
    ),
}


def clean(text):
    return (
        str(text or "")
        .replace("^2", "²")
        .replace("^3", "³")
        .replace(" degrees", "°")
    )


def clean_list(items):
    return [clean(x) for x in (items or [])]


def authored_lesson(lesson, assets, families):
    out = cap.authored_lesson(lesson, assets, families)
    surface = SURFACES.get(lesson["capability_ref"])
    if surface:
        for key in ("opening", "concept_explanation", "common_mistake"):
            out[key] = clean(surface[key])
        for key in ("what_to_notice", "why_it_works", "repair", "verification"):
            out[key] = clean_list(surface[key])
    else:
        for key in ("opening", "concept_explanation", "common_mistake"):
            out[key] = clean(out.get(key, ""))
        for key in ("what_to_notice", "why_it_works", "repair", "verification"):
            out[key] = clean_list(out.get(key, []))
    for ex in out.get("worked_examples", []):
        ex["prompt"] = clean(ex["prompt"])
        ex["steps"] = clean_list(ex["steps"])
        ex["answer"] = clean(ex["answer"])
    for item in out.get("practice", {}).values():
        item["prompt"] = clean(item["prompt"])
        item["solution_steps"] = clean_list(item["solution_steps"])
        item["answer"] = clean(item["answer"])
        item["hints"] = clean_list(item["hints"])
    return out


def install():
    base.authored_lesson = authored_lesson
    return base
