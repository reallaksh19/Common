"""
Generator for Mathematics Sample Templates:
1. Math_Core1_Mature_Sample.pdf (2-page Landscape A4 Study Guide)
2. Math_Core2_Transfer_Sample.pdf (1-page Landscape A4 Transfer Question Page)
"""

import os, sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from primitives import (
    FONT_NAME,
    FONT_BOLD,
    FONT_OBLIQUE,
    draw_pill_badge,
    CartesianPlotter2D,
    CombinatorialSlotDiagram,
    VisualSemanticValidator
)

PAGE_W, PAGE_H = landscape(A4) # 841.89 x 595.28 pt
MARGIN = 36 # 0.5 inch

def render_math_core1(output_path):
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H))
    
    # -------------------------------------------------------------------------
    # PAGE 1: Foundation & Visual Model
    # -------------------------------------------------------------------------
    # Top Header Banner
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "GRADE 9 MATHEMATICS  *  CORE 1 STUDY GUIDE")
    
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "MODULE: COORDINATE GEOMETRY & ALGEBRAIC INVARIANTS  |  Page 1 of 2")
    
    # Sub-header Strip
    draw_pill_badge(c, MARGIN, PAGE_H - 62, "AXIOM A1", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    draw_pill_badge(c, MARGIN + 75, PAGE_H - 62, "PT-2 GROUNDED", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, MARGIN + 185, PAGE_H - 62, "SOURCE: [PT2-Q10, Q14]", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    draw_pill_badge(c, MARGIN + 335, PAGE_H - 62, "EVIDENCE: [SW-Q10, Q14]", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    
    c.setFont(FONT_BOLD, 15)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 86, "{{ LESSON_TITLE: Equality is a Promise  -  Legal Coordinate & Algebraic Transformations }}")
    
    c.setFont(FONT_OBLIQUE, 9)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN, PAGE_H - 100, "Cognitive Job: Master the invariant preservation principle before memorizing formulas. The '=' sign is a promise.")
    
    # Dual-Column Layout
    col_w = (PAGE_W - 2 * MARGIN - 24) / 2
    col1_x = MARGIN
    col2_x = MARGIN + col_w + 24
    content_top = PAGE_H - 116
    
    # ------------------ COLUMN 1: Invariant & Visual Anchor ------------------
    # 1. Axiomatic Invariant Box
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(colors.HexColor("#93C5FD"))
    c.setLineWidth(1)
    c.roundRect(col1_x, content_top - 120, col_w, 120, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(col1_x + 14, content_top - 20, "{{ AXIOMATIC_INVARIANT: Equality is an Unbroken Contract }}")
    
    c.setFont(FONT_NAME, 8.5)
    c.setFillColor(colors.HexColor("#1E293B"))
    inv_text = [
        "The equals sign does not signify 'now compute the next line'.",
        "It asserts that the expression on the left and the expression on the right evaluate",
        "to the exact same mathematical value or geometric point.",
        "* Legal Rule 1: Applying any bijection f(x) to both sides preserves equality: A = B => f(A) = f(B).",
        "* Legal Rule 2: Compound terms (such as x + y) must be bracketed before transformation.",
        "* Invariant Check: If a candidate step produces unequal evaluations, the step is ILLEGAL."
    ]
    ty = content_top - 36
    for line in inv_text:
        c.drawString(col1_x + 14, ty, line)
        ty -= 14
        
    # 2. Misconception Clinic: Why the Learner Route Failed
    c.setFillColor(colors.HexColor("#FFF1F2"))
    c.setStrokeColor(colors.HexColor("#FECDD3"))
    c.roundRect(col1_x, content_top - 235, col_w, 105, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 9.5)
    c.setFillColor(colors.HexColor("#991B1B"))
    c.drawString(col1_x + 14, content_top - 144, "{{ MISCONCEPTION_CLINIC: Why the Learner's Q14 Route Failed }}")
    
    misc_text = [
        "* The Error: Student computed sqrt(x_1^2 + y_1^2) without grouping differences,",
        "  missing the true distance invariant: d = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2).",
        "* Root Cause: Misapplied square root across addition: sqrt(a + b) != sqrta + sqrtb.",
        "* Causal Repair: Distance is the hypotenuse of a right-angled slope triangle.",
        "  You must calculate the horizontal run Delta x and vertical rise Delta y first,",
        "  then apply Pythagoras to the components: d2 = (Delta x)2 + (Delta y)2."
    ]
    ty = content_top - 158
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.HexColor("#881337"))
    for line in misc_text:
        c.drawString(col1_x + 14, ty, line)
        ty -= 12
        
    # Visual Primitive: 2D Coordinate Grid with Slope Triangle
    CartesianPlotter2D.draw_slope_bridge(
        c, col1_x, content_top - 425, col_w, 180,
        title="{{ VISUAL_PRIMITIVE: 2D Cartesian Frame & Slope-Distance Bridge }}",
        p1=(1, 2), p2=(4, 6)
    )
    
    # ------------------ COLUMN 2: Worked Example & Faded Practice ------------
    # 1. Worked Example with Reasoning Story
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col2_x, content_top - 200, col_w, 200, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 14, content_top - 18, "WORKED EXAMPLE", colors.HexColor("#1E3A8A"), colors.white)
    c.setFont(FONT_BOLD, 9)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col2_x + 14, content_top - 34, "{{ WORKED_EXAMPLE_TITLE: Line Passing Through (4, -1) with Slope 2/3 }}")
    
    we_text = [
        "Problem: Find the equation of the line passing through A(4, -1) with slope m = 2/3,",
        "and determine its y-intercept.",
        "",
        "Reasoning Story (Step-by-Step Invariant Preservation):",
        "1. State the Definition: Slope is constant for every point (x, y) on the line:",
        "   (y - y_1) / (x - x_1) = m => (y - (-1)) / (x - 4) = 2/3",
        "2. Preserve Compound Equality (Multiply both sides by 3(x - 4)):",
        "   3(y + 1) = 2(x - 4)",
        "   3y + 3 = 2x - 8",
        "3. Canonical Standard Form: 2x - 3y - 11 = 0",
        "4. Invariant Check (Substitute x = 4, y = -1): 2(4) - 3(-1) - 11 = 8 + 3 - 11 = 0. [VALIDATED]",
        "5. Intercept: Set x = 0 => 3y = -11 => y = -11/3."
    ]
    ty = content_top - 48
    for line in we_text:
        if "Reasoning Story" in line:
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#1E3A8A"))
        elif line.startswith("4. Invariant Check"):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#047857"))
        else:
            c.setFont(FONT_NAME, 8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 12
        
    # 2. Guided / Faded Practice
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#94A3B8"))
    c.roundRect(col2_x, content_top - 425, col_w, 215, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 14, content_top - 222, "TRY WITH ME * FADED PRACTICE", colors.HexColor("#0284C7"), colors.white)
    
    faded_text = [
        "{{ FADED_PRACTICE_Q1 }}: The line passes through P(-2, 3) and Q(4, -1).",
        "Step 1: Compute Rise and Run:  Delta y = (-1) - 3 = ____   |   Delta x = 4 - (-2) = ____",
        "Step 2: Slope m = Delta y / Delta x = ____ / ____ = ____",
        "Step 3: Point-Slope Form: y - (____) = m(x - (____))",
        "Step 4: Check your answer by testing whether point Q(4, -1) satisfies your equation.",
        "",
        "{{ FADED_PRACTICE_Q2 }}: State Euclid's Common Notion 1 in terms of legal algebra:",
        "'Things which are equal to the same thing are equal to one another.'",
        "If A = C and B = C, prove why A = B using a single substitution step.",
        "Your deduction: ____________________________________________________________________"
    ]
    ty = content_top - 242
    c.setFont(FONT_NAME, 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    for line in faded_text:
        if line.startswith("{{ FADED_PRACTICE"):
            c.setFont(FONT_BOLD, 8.5)
            c.setFillColor(colors.HexColor("#0369A1"))
        else:
            c.setFont(FONT_NAME, 8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 15
        
    # Bottom Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Mathematics V2  |  Core (1) Instructional Material  |  Template ID: MATH-CORE1-MASTER-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "Next: Core 2 Practice Sets  ->")
    
    c.showPage()
    
    # -------------------------------------------------------------------------
    # PAGE 2: Combinatorial & Advanced Representations Spread
    # -------------------------------------------------------------------------
    # Top Header Banner
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "GRADE 9 MATHEMATICS  *  CORE 1 ADVANCED VISUAL MODELS")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "MODULE: COMBINATORIAL SLOTS & REASONING  |  Page 2 of 2")
    
    draw_pill_badge(c, MARGIN, PAGE_H - 62, "DISCRETE MATH", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    draw_pill_badge(c, MARGIN + 110, PAGE_H - 62, "COUNTING ENGINE", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, MARGIN + 230, PAGE_H - 62, "ST01-ST12 COVERAGE", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    
    c.setFont(FONT_BOLD, 15)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 86, "{{ LESSON_TITLE: The Multiplication Principle as Independent Decision Slots }}")
    
    # Left Column: Combinatorial Slots Primitive & Rules
    CombinatorialSlotDiagram.draw_slots(c, col1_x, content_top - 180, col_w, 180,
                                        title="{{ VISUAL_PRIMITIVE: 4-Digit Number Formation Slot Model }}")
    
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(colors.HexColor("#93C5FD"))
    c.roundRect(col1_x, content_top - 425, col_w, 235, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(col1_x + 14, content_top - 200, "{{ COMBINATORIAL_RULES: Slot Restrictions & Priority Order }}")
    
    rules_text = [
        "1. The Severest Restriction Goes First:",
        "   If a slot has special conditions (e.g. 'Units digit must be even', 'Thousands != 0'),",
        "   fill that decisive slot FIRST before unconstrained positions.",
        "",
        "2. Distinguish With vs Without Repetition:",
        "   * With Repetition: Previous choices do not reduce subsequent options: n x n x n.",
        "   * Without Repetition: Each filled slot consumes 1 object: n x (n - 1) x (n - 2).",
        "",
        "3. Independent Decisions Rule (Rule of Product):",
        "   If task 1 can be done in p ways, and for each way task 2 can be done in q ways,",
        "   the combined sequence occurs in p x q ways.",
        "",
        "4. Fail-Safe Overcounting Check: Check whether indistinguishable objects were",
        "   ordered as if distinguishable. Divide by k! to remove unwanted symmetry."
    ]
    ty = content_top - 220
    c.setFont(FONT_NAME, 8.5)
    c.setFillColor(colors.HexColor("#1E293B"))
    for line in rules_text:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4."):
            c.setFont(FONT_BOLD, 8.5)
            c.setFillColor(colors.HexColor("#1E40AF"))
        else:
            c.setFont(FONT_NAME, 8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col1_x + 14, ty, line)
        ty -= 14
        
    # Right Column: Comprehensive Worked Example & Core 2 Link
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col2_x, content_top - 280, col_w, 280, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 14, content_top - 18, "COMBINATORICS WORKED EXAMPLE", colors.HexColor("#1E3A8A"), colors.white)
    c.setFont(FONT_BOLD, 9)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col2_x + 14, content_top - 34, "{{ EXAMPLE: 4-Digit Even Numbers Without Repetition }}")
    
    comb_we = [
        "Problem: How many 4-digit even numbers can be formed using digits {0, 1, 2, 3, 4, 5}",
        "if no digit may be repeated?",
        "",
        "Reasoning Story (Split by Conflicting Restriction):",
        "The digit '0' creates a conflict: it makes a number even (units slot), but cannot",
        "be in the thousands slot. Therefore, split into 2 mutually exclusive cases:",
        "",
        "Case 1: Units digit is 0 (Units = {0} => 1 way):",
        "  * Thousands: Any non-zero remaining digit {1,2,3,4,5} => 5 choices.",
        "  * Hundreds: Any remaining digit => 4 choices.",
        "  * Tens: Any remaining digit => 3 choices.",
        "  * Subtotal Case 1 = 5 x 4 x 3 x 1 = 60 numbers.",
        "",
        "Case 2: Units digit is non-zero even (Units = {2, 4} => 2 ways):",
        "  * Thousands: Cannot be 0, cannot be the units digit => (6 - 2) = 4 choices.",
        "  * Hundreds: Remaining digits (including 0 now allowed) => 4 choices.",
        "  * Tens: Remaining digits => 3 choices.",
        "  * Subtotal Case 2 = 4 x 4 x 3 x 2 = 96 numbers.",
        "",
        "Total = Case 1 + Case 2 = 60 + 96 = 156 even numbers. [CHECKED & VERIFIED]"
    ]
    ty = content_top - 48
    for line in comb_we:
        if "Reasoning Story" in line or line.startswith("Case 1") or line.startswith("Case 2") or line.startswith("Total ="):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#1E3A8A") if not line.startswith("Total =") else colors.HexColor("#047857"))
        else:
            c.setFont(FONT_NAME, 7.5)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 12.0
        
    # Core 1 to Core 2 Linkage Banner
    c.setFillColor(colors.HexColor("#F0FDF4"))
    c.setStrokeColor(colors.HexColor("#86EFAC"))
    c.roundRect(col2_x, content_top - 425, col_w, 135, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 14, content_top - 302, "CORE 1 -> CORE 2 TRANSFER CONTRACT", colors.HexColor("#166534"), colors.white)
    c.setFont(FONT_BOLD, 9)
    c.setFillColor(colors.HexColor("#14532D"))
    c.drawString(col2_x + 14, content_top - 325, "{{ CORE2_TRANSFER_AUTHORITY }}")
    
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.HexColor("#166534"))
    link_text = [
        "* Core 1 establishes the mental models, invariants, and failure clinics.",
        "* Core 2 puts you in full test conditions with untouched external items.",
        "* When stuck in Core 2, use the H1-H3 Hint Ladder before checking solutions.",
        "* Every Core 2 question explicitly cites its foundational Core 1 lesson.",
        "Linked Target: Core 2 Set ST01  -  Elementary Slot Permutations (Questions 1-15)"
    ]
    ty = content_top - 340
    for line in link_text:
        c.drawString(col2_x + 14, ty, line)
        ty -= 13
        
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Mathematics V2  |  Core (1) Instructional Material  |  Template ID: MATH-CORE1-MASTER-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "Core 1 Complete  *  Proceed to Core 2 Transfer Book  ->")
    
    c.save()
    print(f"Successfully generated: {output_path}")

def render_math_core2(output_path):
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H))
    
    # -------------------------------------------------------------------------
    # PAGE 1: 1-Page Modular Transfer Question Layout
    # -------------------------------------------------------------------------
    # Top Header Banner
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "GRADE 9 MATHEMATICS  *  CORE 2 TRANSFER BOOK")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "H1/H2/H3 HINTS  +  SEMANTIC REASONING ROUTE  +  VERIFIED SOLUTION")
    
    # 2-Tier Metadata Badges (Zero Truncation)
    # Row 1 (y = PAGE_H - 58)
    b_x = MARGIN
    b_x += draw_pill_badge(c, b_x, PAGE_H - 58, "ITEM: {{ QUESTION_ID: PT2-Q05 }}", colors.HexColor("#1E3A8A"), colors.white) + 8
    b_x += draw_pill_badge(c, b_x, PAGE_H - 58, "DEMAND: {{ DIFFICULTY_BADGE: MEDIUM }}", colors.HexColor("#E1EFFE"), colors.HexColor("#1E429F")) + 8
    draw_pill_badge(c, b_x, PAGE_H - 58, "TARGET GRADE: GRADE 9 MATH", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    
    # Row 2 (y = PAGE_H - 76)
    b_x = MARGIN
    b_x += draw_pill_badge(c, b_x, PAGE_H - 76, "CONCEPT: {{ PRIMARY_CONCEPT: Coordinate Transformations }}", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F")) + 8
    b_x += draw_pill_badge(c, b_x, PAGE_H - 76, "LINK: {{ CORE1_LINK: Core1 Lesson A1 }}", colors.HexColor("#F3F4F6"), colors.HexColor("#374151")) + 8
    draw_pill_badge(c, b_x, PAGE_H - 76, "SRC: {{ SOURCE_REF: PT2-2023-TERM2 }}", colors.HexColor("#F3F4F6"), colors.HexColor("#374151"))
    
    c.setFont(FONT_BOLD, 13)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 96, "{{ QUESTION_TITLE: Line with Slope 2/3 Passing Through Point (4, -1) }}")
    
    # Split Layout (Left: Question & Attempt Workspace; Right: Hints, Route & Solution)
    col_w = (PAGE_W - 2 * MARGIN - 24) / 2
    col1_x = MARGIN
    col2_x = MARGIN + col_w + 24
    content_top = PAGE_H - 110
    
    # ------------------ LEFT COLUMN: Question & Workspace --------------------
    # Question Stem Box
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#94A3B8"))
    c.setLineWidth(1)
    c.roundRect(col1_x, content_top - 120, col_w, 120, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col1_x + 12, content_top - 18, "ORIGINAL EXAM QUESTION / ATTEMPT", colors.HexColor("#0F172A"), colors.white)
    
    stem_lines = [
        "{{ QUESTION_STEM }}:",
        "A straight line L passes through point A(4, -1) with slope m = 2/3.",
        "Which of the following points also lies on line L, and what is the y-intercept of L?",
        "",
        "Options:",
        "(a) Point (-2, -5) and y-intercept = -11/3      (b) Point (1, -3) and y-intercept = -11/3",
        "(c) Point (7, 1) and y-intercept = 11/3          (d) Point (2, -2) and y-intercept = -8/3"
    ]
    ty = content_top - 34
    c.setFont(FONT_NAME, 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    for line in stem_lines:
        if line.startswith("(a)"):
            c.setFont(FONT_BOLD, 8)
        else:
            c.setFont(FONT_NAME, 8.5)
        c.drawString(col1_x + 14, ty, line)
        ty -= 13
        
    # Visual Vector Figure in Left Column
    CartesianPlotter2D.draw_slope_bridge(c, col1_x, content_top - 280, col_w, 150,
                                         title="{{ RECONSTRUCTED_SOURCE_FIGURE: 2D Line L on Cartesian Grid }}",
                                         p1=(1, 2), p2=(4, 6))
    
    # Student Attempt Workspace
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col1_x, content_top - 440, col_w, 150, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(col1_x + 14, content_top - 296, "{{ H0_ATTEMPT_WORKSPACE: Work Here * Try Before Looking at Hints }}")
    
    # Guided dotted lines for student working
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.setLineWidth(0.8)
    c.setDash(2, 2)
    for ly in range(int(content_top - 315), int(content_top - 425), -20):
        c.line(col1_x + 14, ly, col1_x + col_w - 14, ly)
    c.setDash()
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(col1_x + 14, content_top - 430, "Your Final Choice: [ _____ ]      Reason: ___________________________")
    
    # ------------------ RIGHT COLUMN: Hints, Route & Solution ----------------
    # 1. Faded Hint Ladder (H1 -> H2 -> H3)
    c.setFillColor(colors.HexColor("#FFFBEB"))
    c.setStrokeColor(colors.HexColor("#FDE68A"))
    c.roundRect(col2_x, content_top - 120, col_w, 120, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 18, "H1-H3 HINT LADDER (READ ONE AT A TIME ONLY IF STUCK)", colors.HexColor("#B45309"), colors.white)
    
    hints_text = [
        "* {{ H1_NOTICE }}: The slope m = (y - y_1) / (x - x_1) is identical for ALL points on the line.",
        "* {{ H2_MODEL }}: Use point-slope form: (y - (-1)) = 2/3 (x - 4) => 3(y + 1) = 2(x - 4).",
        "  Rearrange into standard linear equation form: 2x - 3y - 11 = 0.",
        "* {{ H3_START }}: Substitute candidate points into 2x - 3y - 11 = 0 to see which gives 0.",
        "  For y-intercept, evaluate at x = 0: 2(0) - 3y - 11 = 0 => y = -11/3."
    ]
    ty = content_top - 34
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.HexColor("#78350F"))
    for line in hints_text:
        c.drawString(col2_x + 14, ty, line)
        ty -= 15
        
    # 2. Semantic Reasoning Route
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(colors.HexColor("#BFDBFE"))
    c.roundRect(col2_x, content_top - 240, col_w, 110, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 138, "SEMANTIC REASONING ROUTE", colors.HexColor("#1D4ED8"), colors.white)
    
    route_steps = [
        "Step 1 [INTERPRET]: Identify given geometric parameters: point (4, -1), slope m = 2/3.",
        "Step 2 [MODEL & BIND]: Convert to algebraic form using point-slope invariant: 2x - 3y - 11 = 0.",
        "Step 3 [DISCRIMINATE]: Test options: (-2, -5) => 2(-2) - 3(-5) - 11 = -4 + 15 - 11 = 0. [VALID]",
        "Step 4 [VERIFY INTERCEPT]: Set x = 0 => y = -11/3. Select matching option (a)."
    ]
    ty = content_top - 156
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#1E40AF"))
    for line in route_steps:
        c.drawString(col2_x + 14, ty, line)
        ty -= 18
        
    # 3. Verified Solution & Check Box
    c.setFillColor(colors.HexColor("#F0FDF4"))
    c.setStrokeColor(colors.HexColor("#86EFAC"))
    c.roundRect(col2_x, content_top - 440, col_w, 190, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 258, "VERIFIED SOLUTION & CHECK", colors.HexColor("#15803D"), colors.white)
    
    sol_text = [
        "{{ SOLUTION_FINAL_ANSWER }}: Correct Option is (a).",
        "",
        "Execution Walkthrough:",
        "1. Standard Equation: 2x - 3y - 11 = 0.",
        "2. Option (a) Point Check: Substitute (-2, -5):",
        "   LHS = 2(-2) - 3(-5) - 11 = -4 + 15 - 11 = 0 = RHS. (Satisfies L)",
        "3. Intercept Determination:",
        "   L crosses y-axis where x = 0 => 2(0) - 3y - 11 = 0 => -3y = 11 => y = -11/3.",
        "",
        "{{ VERIFICATION_CHECK }}:",
        "Compute slope between given point A(4, -1) and discovered point B(-2, -5):",
        "m_calc = (-1 - (-5)) / (4 - (-2)) = 4 / 6 = 2/3. Exactly matches problem statement.",
        "",
        "Permanent Invariant: Points lie on a line if and only if they satisfy its equation."
    ]
    ty = content_top - 276
    for line in sol_text:
        if line.startswith("{{ SOLUTION") or line.startswith("{{ VERIFICATION"):
            c.setFont(FONT_BOLD, 8.5)
            c.setFillColor(colors.HexColor("#14532D"))
        elif line.startswith("Permanent"):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#065F46"))
        else:
            c.setFont(FONT_NAME, 7.5)
            c.setFillColor(colors.HexColor("#1F2937"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 12.5
        
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Mathematics V2  |  Core (2) Transfer Question Sheet  |  Template ID: MATH-CORE2-SINGLE-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "End of Transfer Sheet  *  Traceable to Core1 Lesson A1")
    
    c.save()
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "output_samples"
    out_dir.mkdir(parents=True, exist_ok=True)
    render_math_core1(out_dir / "Math_Core1_Mature_Sample.pdf")
    render_math_core2(out_dir / "Math_Core2_Transfer_Sample.pdf")
