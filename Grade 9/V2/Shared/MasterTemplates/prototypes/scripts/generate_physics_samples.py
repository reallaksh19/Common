"""
Generator for Physics Sample Templates:
1. Physics_Core1_StudyGuide_Sample.pdf (2-page Landscape A4 Study Guide)
2. Physics_Core2_Practice_Sample.pdf (2-page Landscape A4 Two-Pass Practice & Check Your Method)
"""

import os, sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

sys.path.append(str(Path(__file__).resolve().parent))
from visual_primitives import (
    FONT_NAME,
    FONT_BOLD,
    FONT_OBLIQUE,
    draw_pill_badge,
    draw_number_line_1d,
    draw_vt_graph
)

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 36

def render_physics_core1(output_path):
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H))
    
    # -------------------------------------------------------------------------
    # PAGE 1: Position, Reference Frames & NAV Routines
    # -------------------------------------------------------------------------
    # Header Banner
    c.setFillColor(colors.HexColor("#0F766E"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "GRADE 9 PHYSICS  *  CORE 1 STUDY GUIDE")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "CHAPTER: MOTION IN A STRAIGHT LINE  |  Page 1 of 2")
    
    # Sub-header Badges
    draw_pill_badge(c, MARGIN, PAGE_H - 62, "NAV-1 & NAV-2", colors.HexColor("#CCFBF1"), colors.HexColor("#115E59"))
    draw_pill_badge(c, MARGIN + 105, PAGE_H - 62, "SUBTOPIC M-ST01A", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, MARGIN + 235, PAGE_H - 62, "SOURCE: Q1-Q5 BANK", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    draw_pill_badge(c, MARGIN + 375, PAGE_H - 62, "PHYSICS TRUTH FIRST", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    
    c.setFont(FONT_BOLD, 15)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 86, "{{ LESSON_TITLE: Reference Frame, Coordinate Axis, Distance & Displacement }}")
    
    c.setFont(FONT_OBLIQUE, 9)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN, PAGE_H - 100, "Core Pedagogy: SEE THE MOTION FIRST -> REALIZE THE VECTOR RELATION -> UNDERSTAND SIGN CONVENTIONS")
    
    col_w = (PAGE_W - 2 * MARGIN - 24) / 2
    col1_x = MARGIN
    col2_x = MARGIN + col_w + 24
    content_top = PAGE_H - 116
    
    # ------------------ COLUMN 1: Routine Nav & Visual Strip -----------------
    # NAV-1 & NAV-2 Routine Box
    c.setFillColor(colors.HexColor("#F0FDFA"))
    c.setStrokeColor(colors.HexColor("#99F6E4"))
    c.roundRect(col1_x, content_top - 125, col_w, 125, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(col1_x + 14, content_top - 20, "{{ NAV_ROUTINE: Every Numerical Problem  -  First 20 Seconds }}")
    
    nav_text = [
        "1. Draw a tiny coordinate line or functional sketch before touching equations.",
        "2. Choose the positive direction (+ East / + Up) explicitly: sign errors stem from unchosen frames.",
        "3. Translate hidden words into numerical physics data:",
        "   'Starts from rest' => u = 0  |  'Comes to a stop' => v = 0  |  'Highest point' => v_top = 0.",
        "4. Model Gate (NAV-2): Is acceleration constant? (Use UVATS)  |  Is velocity constant? (Use s = vt)",
        "5. Avoid formula roulette: Select the single relation that directly bypasses unneeded unknowns."
    ]
    ty = content_top - 36
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.HexColor("#134E4A"))
    for line in nav_text:
        c.drawString(col1_x + 14, ty, line)
        ty -= 14
        
    # Visual Primitive: 1D Number Line & Displacement Vector
    draw_number_line_1d(c, col1_x, content_top - 275, col_w, 140, "{{ VISUAL_PRIMITIVE: 1D Coordinate Line & Return-Path Vectors }}")
    
    # Invariant Rule Box: Distance vs Displacement
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(colors.HexColor("#93C5FD"))
    c.roundRect(col1_x, content_top - 425, col_w, 140, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(col1_x + 14, content_top - 295, "{{ PHYSICAL_INVARIANT: Path Length vs Coordinate Difference }}")
    
    inv_text = [
        "* Distance (Scalar): Total cumulative path length travelled regardless of direction.",
        "  Distance is always positive and strictly monotonically non-decreasing over time: d >= 0.",
        "* Displacement (Vector): Net change in position comparing only endpoints:",
        "  Delta x = x_final - x_initial. Displacement can be positive, negative, or zero.",
        "* The Reversal Trap: Whenever an object reverses direction, Distance > |Displacement|.",
        "* Magnitude Bound: |Displacement| <= Distance. Equality holds ONLY for unidirectional straight motion."
    ]
    ty = content_top - 312
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.HexColor("#1E293B"))
    for line in inv_text:
        c.drawString(col1_x + 14, ty, line)
        ty -= 15
        
    # ------------------ COLUMN 2: Worked Example & Guided Practice -----------
    # Worked Example with Story
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col2_x, content_top - 210, col_w, 210, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 14, content_top - 18, "PHYSICS WORKED EXAMPLE", colors.HexColor("#0F766E"), colors.white)
    c.setFont(FONT_BOLD, 9)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col2_x + 14, content_top - 34, "{{ EXAMPLE: Two-Leg Reversal Journey }}")
    
    we_text = [
        "Problem: A student starts at origin x = 0, walks 6 m East, then turns and walks 2 m West.",
        "Calculate: (a) Total Distance, (b) Final Position, (c) Net Displacement.",
        "",
        "Physics Reasoning Story (Words --> Picture --> Facts --> Target --> Relation):",
        "1. Define Frame: Let East be positive (+x direction). Origin is the school gate x = 0 m.",
        "2. Leg 1 Vector: Delta x_1 = +6 m (East). Position after Leg 1: x_1 = 0 + 6 = +6 m.",
        "3. Leg 2 Vector: Moves West => Delta x_2 = -2 m. Position after Leg 2: x_2 = +6 + (-2) = +4 m.",
        "4. Calculate Distance: d = |Delta x_1| + |Delta x_2| = 6 m + 2 m = 8 m. (Path length accumulation)",
        "5. Calculate Displacement: Delta x = x_final - x_initial = (+4 m) - (0 m) = +4 m (East).",
        "6. Verification Check: |Delta x| = 4 m < 8 m = Distance. Reversal detected and verified. [PASS]"
    ]
    ty = content_top - 48
    for line in we_text:
        if "Reasoning Story" in line:
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#0F766E"))
        elif line.startswith("6. Verification"):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#047857"))
        else:
            c.setFont(FONT_NAME, 8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 12.5
        
    # Guided Practice & Try With Me Box
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#94A3B8"))
    c.roundRect(col2_x, content_top - 425, col_w, 205, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 14, content_top - 232, "GUIDED PRACTICE * TRY WITH ME", colors.HexColor("#0284C7"), colors.white)
    
    gp_text = [
        "{{ GUIDED_PRACTICE_Q1 }}: Start at x = -2 m. Walk 5 m East, then 7 m West.",
        "* Step 1: Mark initial coordinate x_0 = ____ m.",
        "* Step 2: Displacement vector Delta x_1 = ____ m,  Delta x_2 = ____ m.",
        "* Step 3: Final coordinate x_final = x_0 + Delta x_1 + Delta x_2 = ____ m.",
        "* Step 4: Total Distance d = |____| + |____| = ____ m.",
        "* Step 5: Net Displacement Delta x = x_final - x_0 = ____ m.",
        "",
        "{{ GUIDED_PRACTICE_Q2 }}: Can an athlete complete one lap of a 400 m circular track",
        "and have a displacement of 400 m? Explain using the definition of displacement.",
        "Your physics explanation: ___________________________________________________________"
    ]
    ty = content_top - 252
    for line in gp_text:
        if line.startswith("{{ GUIDED"):
            c.setFont(FONT_BOLD, 8.5)
            c.setFillColor(colors.HexColor("#0369A1"))
        else:
            c.setFont(FONT_NAME, 8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 14.5
        
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Physics V2  |  Core (1) Motion Study Guide  |  Template ID: PHYS-CORE1-MASTER-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "Next: Kinematic Graphs & Area Integration  ->")
    
    c.showPage()
    
    # -------------------------------------------------------------------------
    # PAGE 2: Kinematic Graphs & Area Integration Spread
    # -------------------------------------------------------------------------
    c.setFillColor(colors.HexColor("#0F766E"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "GRADE 9 PHYSICS  *  CORE 1 KINEMATIC INTEGRATION")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "MODULE: VELOCITY-TIME GRAPHS & MOTION DERIVATIONS  |  Page 2 of 2")
    
    draw_pill_badge(c, MARGIN, PAGE_H - 62, "M-ST04A GRAPHS", colors.HexColor("#CCFBF1"), colors.HexColor("#115E59"))
    draw_pill_badge(c, MARGIN + 125, PAGE_H - 62, "SLOPE & AREA DECODER", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, MARGIN + 285, PAGE_H - 62, "SEE -> REALIZE -> UNDERSTAND", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    
    c.setFont(FONT_BOLD, 15)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 86, "{{ LESSON_TITLE: Velocity-Time Area as Accumulated Movement & Kinematic Derivations }}")
    
    # Left Column: v-t Graph Primitive & Derivation
    draw_vt_graph(c, col1_x, content_top - 200, col_w, 200, "{{ VISUAL_PRIMITIVE: Constant Acceleration v-t Area Decomposition }}")
    
    c.setFillColor(colors.HexColor("#F0FDFA"))
    c.setStrokeColor(colors.HexColor("#99F6E4"))
    c.roundRect(col1_x, content_top - 425, col_w, 215, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(col1_x + 14, content_top - 220, "{{ DERIVATION_WALKTHROUGH: Why s = ut + 1/2at2 Works Physically }}")
    
    deriv_text = [
        "1. Geometry of the Velocity-Time Profile:",
        "   Under constant acceleration 'a', velocity rises linearly from initial speed 'u' to 'v' in time 't'.",
        "   The region under the graph decomposes into a base rectangle and an upper triangle.",
        "",
        "2. The Base Rectangle Area (Displacement if speed never increased):",
        "   Area_rect = base x height = t x u = ut. (The distance covered at steady speed u)",
        "",
        "3. The Upper Triangle Area (Extra displacement gained from acceleration):",
        "   Area_tri = 1/2 x base x height = 1/2 x t x (v - u).",
        "   Since acceleration is defined as a = (v - u)/t => (v - u) = at.",
        "   Substitute: Area_tri = 1/2 x t x (at) = 1/2 at2.",
        "",
        "4. Total Integrated Displacement: s = Area_rect + Area_tri = ut + 1/2 at2.",
        "   Physical Meaning: Initial movement + additional speed gain = total position shift."
    ]
    ty = content_top - 238
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.HexColor("#134E4A"))
    for line in deriv_text:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4."):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#0F766E"))
        else:
            c.setFont(FONT_NAME, 7.5)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col1_x + 14, ty, line)
        ty -= 12.5
        
    # Right Column: Misconception Clinic & Link to Core 2 Practice
    c.setFillColor(colors.HexColor("#FFFBEB"))
    c.setStrokeColor(colors.HexColor("#FDE68A"))
    c.roundRect(col2_x, content_top - 200, col_w, 200, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 18, "GRAPH MISCONCEPTION CLINIC", colors.HexColor("#B45309"), colors.white)
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col2_x + 14, content_top - 36, "{{ MISCONCEPTION: Graph Height vs Graph Slope }}")
    
    misc_graph = [
        "* Misconception 1: 'Higher point on x-t graph means higher speed.'",
        "  Correction: Height on an x-t graph indicates position (distance from origin).",
        "  Speed is the SLOPE (rate of change). A flat horizontal line at x = 100 m means v = 0.",
        "",
        "* Misconception 2: 'Area below zero velocity axis is still positive distance.'",
        "  Correction: In v-t graphs, area below the v = 0 line represents NEGATIVE displacement",
        "  (travel in the negative coordinate direction).",
        "  To compute Total Distance: Add absolute areas |Area_above| + |Area_below|.",
        "  To compute Net Displacement: Take signed sum: Area_above - Area_below.",
        "",
        "* Model Validity Guardrail: The kinematic equations (s=ut+1/2at2, v2=u2+2as) are valid",
        "  ONLY when acceleration is constant. For variable acceleration, area must be integrated."
    ]
    ty = content_top - 52
    for line in misc_graph:
        if line.startswith("* Misconception") or line.startswith("* Model"):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#B45309"))
        else:
            c.setFont(FONT_NAME, 7.5)
            c.setFillColor(colors.HexColor("#1F2937"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 13
        
    # Core 1 to Core 2 Transfer Link Box
    c.setFillColor(colors.HexColor("#F0FDF4"))
    c.setStrokeColor(colors.HexColor("#86EFAC"))
    c.roundRect(col2_x, content_top - 425, col_w, 215, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 14, content_top - 222, "CORE 1 -> CORE 2 TRANSFER PIPELINE", colors.HexColor("#15803D"), colors.white)
    c.setFont(FONT_BOLD, 9.5)
    c.setFillColor(colors.HexColor("#14532D"))
    c.drawString(col2_x + 14, content_top - 245, "{{ CORE2_TRANSFER_ROADMAP: Practice Set Progression }}")
    
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.HexColor("#166534"))
    p_links = [
        "You have now mastered the conceptual representations of 1D Motion.",
        "In Core 2, you will encounter the audited PYQ & ExamSIDE transfer questions:",
        "",
        "* Assimilation Set 1: Averages, Speed vs Velocity, Harmonic Mean",
        "* Assimilation Set 2: Constant Acceleration Core (UVATS selection)",
        "* Assimilation Set 3: Polynomial motion & braking vehicle pairs",
        "* Assimilation Set 4: Free fall & vertical gravity stages",
        "* Assimilation Set 5: Relative motion & common acceleration cancellation",
        "* Assimilation Set 6: Velocity-Time & Position-Time graph interpretation",
        "",
        "Transfer Rule: Always attempt before revealing H1-H3 hints. Check methods after finishing."
    ]
    ty = content_top - 262
    for line in p_links:
        c.drawString(col2_x + 14, ty, line)
        ty -= 13.5
        
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Physics V2  |  Core (1) Motion Study Guide  |  Template ID: PHYS-CORE1-MASTER-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "Core 1 Complete  *  Proceed to Core 2 Practice Book  ->")
    
    c.save()
    print(f"Successfully generated: {output_path}")

def render_physics_core2(output_path):
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H))
    
    # -------------------------------------------------------------------------
    # PAGE 1: Core 2 Student Practice Set (Attempt First + Foldable Hints)
    # -------------------------------------------------------------------------
    # Header Banner
    c.setFillColor(colors.HexColor("#0F766E"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "GRADE 9 PHYSICS  *  CORE 2 TRANSFER QUESTION BOOK")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "ASSIMILATION SET 1 / 7  |  AVERAGES & ACCELERATION CORE")
    
    # Roadmap instruction strip
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(MARGIN, PAGE_H - 58, "HOW THIS PRACTICE WORKS: 1. Attempt question in workspace  *  2. Look at hints ONLY if stuck  *  3. Verify in 'Check Your Method'")
    
    # Dual-column: Question 1 Left, Question 2 Right
    col_w = (PAGE_W - 2 * MARGIN - 24) / 2
    col1_x = MARGIN
    col2_x = MARGIN + col_w + 24
    content_top = PAGE_H - 72
    
    # ------------------ QUESTION 1 (Equal Distance Harmonic Mean) ------------
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col1_x, content_top - 475, col_w, 475, 6, fill=1, stroke=1)
    
    # Badges
    draw_pill_badge(c, col1_x + 12, content_top - 18, "Q1  EX-M2B-02", colors.HexColor("#0F766E"), colors.white)
    draw_pill_badge(c, col1_x + 105, content_top - 18, "EASY", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, col1_x + 155, content_top - 18, "JEE MAIN 2023 - 10 APR", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col1_x + 12, content_top - 36, "Concept: M-ST02B * Equal Time vs Equal Distance Averages")
    
    # Stem
    q1_stem = [
        "{{ QUESTION_STEM }}:",
        "A person travels distance x at velocity v_1 and then another equal distance x",
        "at velocity v_2 in the same direction. Relate the average velocity v to v_1 and v_2.",
        "",
        "Options:",
        "(a) v = (v_1 + v_2) / 2                          (b) v = 2v_1 v_2 / (v_1 + v_2)",
        "(c) v = sqrt(v_1 v_2)                                  (d) v = (v_1^2 + v_2^2) / 2"
    ]
    ty = content_top - 54
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.HexColor("#0F172A"))
    for line in q1_stem:
        if line.startswith("(a)"):
            c.setFont(FONT_BOLD, 8)
        else:
            c.setFont(FONT_NAME, 8)
        c.drawString(col1_x + 12, ty, line)
        ty -= 13
        
    # Attempt Workspace Box
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.roundRect(col1_x + 12, content_top - 240, col_w - 24, 130, 4, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(col1_x + 20, content_top - 122, "{{ H0_WORKSPACE: Work Here * Try Before Looking at Hints }}")
    
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.setLineStyle = 1
    for ly in range(int(content_top - 138), int(content_top - 230), -18):
        c.line(col1_x + 20, ly, col1_x + col_w - 20, ly)
        
    c.setFont(FONT_BOLD, 7.5)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(col1_x + 20, content_top - 232, "Your Attempt: Option [ _____ ]     Reason: _____________________________________________")
    
    # Foldable Hint Ladder Box
    c.setFillColor(colors.HexColor("#FFFBEB"))
    c.setStrokeColor(colors.HexColor("#FDE68A"))
    c.roundRect(col1_x + 12, content_top - 370, col_w - 24, 120, 4, fill=1, stroke=1)
    
    draw_pill_badge(c, col1_x + 20, content_top - 262, "STOP * READ ONLY IF STUCK * H1-H3 HINT LADDER", colors.HexColor("#B45309"), colors.white)
    
    q1_hints = [
        "* {{ H1_NOTICE }}: Both journey legs have the same distance x. Their travel times",
        "  are unequal: t_1 = x / v_1 and t_2 = x / v_2.",
        "* {{ H2_MODEL }}: Average velocity is defined as Total Displacement / Total Time:",
        "  v_avg = (x + x) / (t_1 + t_2) = 2x / (x/v_1 + x/v_2).",
        "* {{ H3_START }}: Factor x out of denominator: 2x / [x (1/v_1 + 1/v_2)]. Cancel x,",
        "  find common denominator v_1 v_2: 2 / [(v_1 + v_2) / v_1 v_2] = 2v_1 v_2 / (v_1 + v_2)."
    ]
    ty = content_top - 280
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#78350F"))
    for line in q1_hints:
        c.drawString(col1_x + 20, ty, line)
        ty -= 14
        
    # Navigation to Check Method
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(col1_x + 16, content_top - 460, "Check Full Method & Takeaways in 'Check Your Method' (Next Page)  ->")
    
    # ------------------ QUESTION 2 (Numerical Transfer) ----------------------
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col2_x, content_top - 475, col_w, 475, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 18, "Q2  EX-M2B-04", colors.HexColor("#0F766E"), colors.white)
    draw_pill_badge(c, col2_x + 105, content_top - 18, "EASY", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, col2_x + 155, content_top - 18, "JEE MAIN 2023 - 30 JAN", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col2_x + 12, content_top - 36, "Concept: M-ST02B * Equal Time vs Equal Distance Averages")
    
    q2_stem = [
        "{{ QUESTION_STEM }}:",
        "A vehicle travels 4 km at 3 km/h and then another 4 km at 5 km/h in the same",
        "straight line. Find the average speed of the vehicle.",
        "",
        "Options:",
        "(a) 4.0 km/h                                       (b) 3.75 km/h",
        "(c) 3.5 km/h                                       (d) 4.25 km/h"
    ]
    ty = content_top - 54
    c.setFont(FONT_NAME, 8)
    c.setFillColor(colors.HexColor("#0F172A"))
    for line in q2_stem:
        if line.startswith("(a)"):
            c.setFont(FONT_BOLD, 8)
        else:
            c.setFont(FONT_NAME, 8)
        c.drawString(col2_x + 12, ty, line)
        ty -= 13
        
    # Attempt Workspace Box
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.roundRect(col2_x + 12, content_top - 240, col_w - 24, 130, 4, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(col2_x + 20, content_top - 122, "{{ H0_WORKSPACE: Work Here * Try Before Looking at Hints }}")
    
    for ly in range(int(content_top - 138), int(content_top - 230), -18):
        c.line(col2_x + 20, ly, col2_x + col_w - 20, ly)
        
    c.setFont(FONT_BOLD, 7.5)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(col2_x + 20, content_top - 232, "Your Attempt: Option [ _____ ]     Calculation: ________________________________________")
    
    # Foldable Hint Ladder
    c.setFillColor(colors.HexColor("#FFFBEB"))
    c.setStrokeColor(colors.HexColor("#FDE68A"))
    c.roundRect(col2_x + 12, content_top - 370, col_w - 24, 120, 4, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 20, content_top - 262, "STOP * READ ONLY IF STUCK * H1-H3 HINT LADDER", colors.HexColor("#B45309"), colors.white)
    
    q2_hints = [
        "* {{ H1_NOTICE }}: Notice that the two distances are equal (d_1 = 4 km, d_2 = 4 km).",
        "  Do NOT take the arithmetic mean (3+5)/2 = 4 km/h  -  it travels longer at 3 km/h!",
        "* {{ H2_MODEL }}: Use the harmonic mean derived in Q1: v_avg = 2v_1 v_2 / (v_1 + v_2).",
        "* {{ H3_START }}: Substitute: 2(3)(5) / (3 + 5) = 30 / 8 = 3.75 km/h."
    ]
    ty = content_top - 280
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#78350F"))
    for line in q2_hints:
        c.drawString(col2_x + 20, ty, line)
        ty -= 14
        
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(col2_x + 16, content_top - 460, "Check Full Method & Takeaways in 'Check Your Method' (Next Page)  ->")
    
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Physics V2  |  Core (2) Transfer Practice  |  Template ID: PHYS-CORE2-TWOPASS-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "End of Practice Page 1  *  Turn Page for Solutions")
    
    c.showPage()
    
    # -------------------------------------------------------------------------
    # PAGE 2: CHECK YOUR METHOD (Gold Standard Solution Rhythm)
    # -------------------------------------------------------------------------
    c.setFillColor(colors.HexColor("#134E4A"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "CHECK YOUR METHOD  *  CONCEPT-ASSIMILATING SOLUTIONS")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "USE ONLY AFTER ATTEMPTING  |  ASSIMILATION SET 1 / 7")
    
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#0F766E"))
    c.drawString(MARGIN, PAGE_H - 58, "THE APPROVED METHOD RHYTHM: QUESTION RECAP --> WHY THIS WORKS --> METHOD --> ANSWER/CHECK --> CONCEPT TO KEEP")
    
    # Solution 1 (Left Column)
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col1_x, content_top - 475, col_w, 475, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col1_x + 12, content_top - 18, "SOLUTION: Q1 EX-M2B-02", colors.HexColor("#0F766E"), colors.white)
    draw_pill_badge(c, col1_x + 175, content_top - 18, "CORRECT: (b)", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    
    sol1_lines = [
        "{{ QUESTION_RECAP }}: Equal distances x travelled at v_1 and v_2. Relate v_avg to v_1, v_2.",
        "",
        "{{ WHY_THIS_WORKS }}:",
        "Average velocity must be built from total displacement divided by total time.",
        "Different speeds contribute to the average in proportion to the TIME spent at each",
        "speed, not the distance. Because time = distance/speed, the lower speed takes longer",
        "and pulls the average speed down below the arithmetic midpoint (v_1 + v_2)/2.",
        "",
        "{{ METHOD_EXECUTION }}:",
        "1. Let each leg have distance x. Total distance = x + x = 2x.",
        "2. Time for leg 1: t_1 = x / v_1.",
        "3. Time for leg 2: t_2 = x / v_2.",
        "4. Total time: t_tot = t_1 + t_2 = x/v_1 + x/v_2 = x (1/v_1 + 1/v_2) = x(v_1 + v_2) / (v_1 v_2).",
        "5. Average velocity: v_avg = Total Distance / Total Time",
        "   v_avg = 2x / [x(v_1 + v_2) / (v_1 v_2)] = 2v_1 v_2 / (v_1 + v_2).",
        "",
        "{{ ANSWER_AND_CHECK }}: Correct Option is (b) v = 2v_1 v_2 / (v_1 + v_2).",
        "* Dimensional Check: [v_1 v_2] / [v_1 + v_2] = (m/s)^2 / (m/s) = m/s. [VALID]",
        "* Limiting Case Check: If v_1 = v_2 = v_0, v_avg = 2v_0^2 / 2v_0 = v_0. [VALID]",
        "",
        "{{ CONCEPT_TO_KEEP }}:",
        "Permanent Rule: Equal-distance legs always produce the HARMONIC MEAN: 2v_1 v_2/(v_1 + v_2).",
        "Equal-time legs produce the ARITHMETIC MEAN: (v_1 + v_2)/2."
    ]
    ty = content_top - 36
    for line in sol1_lines:
        if line.startswith("{{ QUESTION") or line.startswith("{{ WHY") or line.startswith("{{ METHOD") or line.startswith("{{ ANSWER") or line.startswith("{{ CONCEPT"):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#0F766E"))
        else:
            c.setFont(FONT_NAME, 7.5)
            c.setFillColor(colors.HexColor("#1E293B"))
        c.drawString(col1_x + 12, ty, line)
        ty -= 13.5
        
    # Solution 2 (Right Column)
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col2_x, content_top - 475, col_w, 475, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 18, "SOLUTION: Q2 EX-M2B-04", colors.HexColor("#0F766E"), colors.white)
    draw_pill_badge(c, col2_x + 175, content_top - 18, "CORRECT: (b)", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    
    sol2_lines = [
        "{{ QUESTION_RECAP }}: 4 km at 3 km/h and 4 km at 5 km/h. Find average speed.",
        "",
        "{{ WHY_THIS_WORKS }}:",
        "The problem features two equal-distance legs (4 km each). The time spent travelling",
        "at 3 km/h is 4/3 h (1.33 h), while time spent at 5 km/h is only 4/5 h (0.8 h).",
        "Because 1.33 h > 0.8 h, the car spends more time at 3 km/h. The answer must be",
        "strictly less than the arithmetic mean of 4.0 km/h.",
        "",
        "{{ METHOD_EXECUTION }}:",
        "1. First-Principles Calculation:",
        "   Total distance = 4 km + 4 km = 8 km.",
        "   Total time = (4/3) + (4/5) = (20 + 12) / 15 = 32/15 h.",
        "   v_avg = 8 / (32/15) = 8 x (15/32) = 15 / 4 = 3.75 km/h.",
        "2. Direct Harmonic Mean Shortcut (from Q1):",
        "   v_avg = 2(3)(5) / (3 + 5) = 30 / 8 = 3.75 km/h.",
        "",
        "{{ ANSWER_AND_CHECK }}: Correct Option is (b) 3.75 km/h.",
        "* Sanity Check: 3.75 < 4.0 km/h. Lower speed weighted more heavily. [VALID]",
        "",
        "{{ CONCEPT_TO_KEEP }}:",
        "When distance is constant, never average speeds directly. Use the harmonic formula",
        "v = 2v_1 v_2 / (v_1 + v_2) or return to total distance over total time."
    ]
    ty = content_top - 36
    for line in sol2_lines:
        if line.startswith("{{ QUESTION") or line.startswith("{{ WHY") or line.startswith("{{ METHOD") or line.startswith("{{ ANSWER") or line.startswith("{{ CONCEPT"):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#0F766E"))
        else:
            c.setFont(FONT_NAME, 7.5)
            c.setFillColor(colors.HexColor("#1E293B"))
        c.drawString(col2_x + 12, ty, line)
        ty -= 14.5
        
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Physics V2  |  Core (2) Check Your Method  |  Template ID: PHYS-CORE2-CHECKMETHOD-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "Set 1 Complete  *  Proceed to Set 2: Constant Acceleration  ->")
    
    c.save()
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "output_samples"
    out_dir.mkdir(parents=True, exist_ok=True)
    render_physics_core1(out_dir / "Physics_Core1_StudyGuide_Sample.pdf")
    render_physics_core2(out_dir / "Physics_Core2_Practice_Sample.pdf")
