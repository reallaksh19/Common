"""
Generator for Chemistry Sample Templates:
1. Chemistry_Core1_MasterGuide_Sample.pdf (2-page Landscape A4 Study Guide)
2. Chemistry_Core2_Transfer_Sample.pdf (1-page Landscape A4 ExamSIDE Transfer Question Page)
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
    draw_particle_model,
    draw_formula_anatomy,
    draw_oxidation_state_lane
)

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 36

def render_chemistry_core1(output_path):
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H))
    
    # -------------------------------------------------------------------------
    # PAGE 1: Bookkeeping Charge & Particle Conservation
    # -------------------------------------------------------------------------
    # Header Banner
    c.setFillColor(colors.HexColor("#065F46"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "GRADE 9 CHEMISTRY  *  CORE 1 MASTER STUDY GUIDE")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "CHAPTER: REDOX REACTIONS  |  Page 1 of 2")
    
    # Sub-header Badges
    draw_pill_badge(c, MARGIN, PAGE_H - 62, "SUBTOPIC RX-ST01", colors.HexColor("#ECFDF5"), colors.HexColor("#065F46"))
    draw_pill_badge(c, MARGIN + 130, PAGE_H - 62, "OXIDATION NUMBER", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, MARGIN + 270, PAGE_H - 62, "OBLIGATIONS: RX-S01..S06", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    draw_pill_badge(c, MARGIN + 440, PAGE_H - 62, "HARD BOUNDARY: NO TITRATION", colors.HexColor("#FEF2F2"), colors.HexColor("#991B1B"))
    
    c.setFont(FONT_BOLD, 14)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 86, "{{ LESSON_TITLE: What is an Oxidation Number? Understand the Bookkeeping Idea Before Rules }}")
    
    c.setFont(FONT_OBLIQUE, 8.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN, PAGE_H - 100, "Cognitive Job: Master the bookkeeping definition before memorizing arbitrary rules. Elements have variable oxidation states.")
    
    col_w = (PAGE_W - 2 * MARGIN - 24) / 2
    col1_x = MARGIN
    col2_x = MARGIN + col_w + 24
    content_top = PAGE_H - 114
    
    # ------------------ COLUMN 1: Tripartite View & Particle Conservation ----
    # 1. Concept Foundation Box
    c.setFillColor(colors.HexColor("#ECFDF5"))
    c.setStrokeColor(colors.HexColor("#A7F3D0"))
    c.roundRect(col1_x, content_top - 120, col_w, 120, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 9.5)
    c.setFillColor(colors.HexColor("#065F46"))
    c.drawString(col1_x + 14, content_top - 20, "{{ CONCEPT_FOUNDATION: The Bookkeeping Contract }}")
    
    fnd_text = [
        "An oxidation number is NOT an actual physical charge located on an atom.",
        "It is a hypothetical bookkeeping charge an atom would carry if all shared bonds were",
        "treated as 100% ionic, assigning electrons completely to the more electronegative atom.",
        "* In elemental O2: Neither atom is more electronegative => ON = 0.",
        "* In H2O: Oxygen is more electronegative than Hydrogen => H = +1, O = -2.",
        "* In H2O2 (Peroxide): The O-O bond shares electrons equally => H = +1, O = -1.",
        "* The Invariant: The algebraic sum of oxidation numbers must equal the net charge of the species."
    ]
    ty = content_top - 36
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#064E3B"))
    for line in fnd_text:
        c.drawString(col1_x + 14, ty, line)
        ty -= 13.0
        
    # 2. Particulate Model Primitive
    draw_particle_model(c, col1_x, content_top - 265, col_w, 135, "{{ VISUAL_PRIMITIVE: Particulate View of Atom & Charge Conservation }}")
    
    # 3. Formula Anatomy Strip Primitive
    draw_formula_anatomy(c, col1_x, content_top - 425, col_w, 150, "{{ VISUAL_PRIMITIVE: Notation Anatomy - Distinguishing Position Meaning }}")
    
    # ------------------ COLUMN 2: Misconception Clinic & Worked Example ------
    # Misconception Clinic (Height = 140 pt)
    c.setFillColor(colors.HexColor("#FFF1F2"))
    c.setStrokeColor(colors.HexColor("#FECDD3"))
    c.roundRect(col2_x, content_top - 140, col_w, 140, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 18, "MISCONCEPTION CLINIC", colors.HexColor("#991B1B"), colors.white)
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#991B1B"))
    c.drawString(col2_x + 150, content_top - 16, "{{ CLINIC: Subscript vs Charge vs Oxidation Number }}")
    
    misc_lines = [
        "* Misconception 1: 'Oxidation number is the same as valence.'",
        "  Correction: Valence is combining capacity and is always a positive integer (e.g. Carbon valence = 4).",
        "  Oxidation number is signed and can be positive, negative, zero, or fractional (e.g. CH4: C = -4; CO2: C = +4).",
        "* Misconception 2: 'In SO4^2-, each oxygen atom carries a 2- charge.'",
        "  Correction: The 2- superscript is the NET CHARGE of the whole sulfate ion, not oxygen alone!",
        "  Each oxygen is assigned -2. Total oxygen charge = 4 x (-2) = -8. Sulfur is +6.",
        "  Check: +6 + (-8) = -2 = Net Ionic Charge.",
        "* Misconception 3: 'Oxygen is always -2.'",
        "  Correction: In peroxides (H2O2, Na2O2), O = -1. In superoxides (KO2), O = -1/2. In OF2, O = +2."
    ]
    ty = content_top - 34
    for line in misc_lines:
        if line.startswith("* Misconception"):
            c.setFont(FONT_BOLD, 7.2)
            c.setFillColor(colors.HexColor("#991B1B"))
        else:
            c.setFont(FONT_NAME, 7.0)
            c.setFillColor(colors.HexColor("#881337"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 11.2
        
    # Worked Example with Rule-Priority Verification (Starts at content_top - 152, Height = 273 pt)
    we_top = content_top - 152
    we_h = 273
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col2_x, we_top - we_h, col_w, we_h, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, we_top - 16, "WORKED EXAMPLE WITH STEP-BY-STEP AUDIT", colors.HexColor("#065F46"), colors.white)
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col2_x + 14, we_top - 34, "{{ EXAMPLE: Assigning ON in K2Cr2O7 and CrO5 }}")
    
    we_chem = [
        "Problem: Determine the oxidation state of Chromium in (a) K2Cr2O7 and (b) CrO5.",
        "",
        "Reasoning Story (Apply Fixed Rules Before Sum Rule):",
        "Part (a) Potassium Dichromate (K2Cr2O7):",
        "1. Step 1 (Fixed Rules): Group 1 metal (K) has invariant ON = +1. Potassium contribution = 2(+1) = +2.",
        "2. Step 2 (Oxygen Rule): No peroxide linkage indicated. Standard oxygen ON = -2. 7(-2) = -14.",
        "3. Step 3 (Sum Rule): Net charge = 0. Let Chromium ON = x. Formula has 2 Cr atoms:",
        "   (+2) + 2x + (-14) = 0 => 2x - 12 = 0 => 2x = +12 => x = +6.",
        "   Conclusion: In K2Cr2O7, Cr = +6. [VERIFIED & AUDITED]",
        "",
        "Part (b) Butterfly Compound (CrO5) - The Structure-Sensitive Exception:",
        "1. Naive Algebra (Wrong): If all O = -2 => x + 5(-2) = 0 => x = +10. (IMPOSSIBLE: Cr max ON = +6).",
        "2. Structural Truth: CrO5 contains ONE oxo oxygen (=O) and TWO peroxo linkages (-O-O-).",
        "   * 1 oxo oxygen with ON = -2.",
        "   * 4 peroxo oxygens with ON = -1 each (total -4).",
        "3. Correct Sum: x + (-2) + 4(-1) = 0 => x - 6 = 0 => Cr = +6. [STRUCTURE-GROUNDED TRUTH]"
    ]
    ty = we_top - 50
    for line in we_chem:
        if line.startswith("Part (") or "Reasoning Story" in line:
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#065F46"))
        elif "Wrong" in line:
            c.setFont(FONT_BOLD, 7.2)
            c.setFillColor(colors.HexColor("#DC2626"))
        elif line.startswith("   Conclusion") or line.startswith("3. Correct"):
            c.setFont(FONT_BOLD, 7.2)
            c.setFillColor(colors.HexColor("#047857"))
        else:
            c.setFont(FONT_NAME, 7.0)
            c.setFillColor(colors.HexColor("#1E293B"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 11.5
        
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Chemistry V2  |  Core (1) Redox Master Study Guide  |  Template ID: CHEM-CORE1-MASTER-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "Next: Redox Processes & Agent Roles (Self vs Other)  ->")
    
    c.showPage()
    
    # -------------------------------------------------------------------------
    # PAGE 2: Oxidation, Reduction, and Agent Role Attachment
    # -------------------------------------------------------------------------
    c.setFillColor(colors.HexColor("#065F46"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "GRADE 9 CHEMISTRY  *  CORE 1 PROCESSES & AGENT ROLES")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "SUBTOPIC RX-ST02 & RX-ST03: SELF VS OTHER FRAME  |  Page 2 of 2")
    
    draw_pill_badge(c, MARGIN, PAGE_H - 62, "PROCESS VS AGENT", colors.HexColor("#ECFDF5"), colors.HexColor("#065F46"))
    draw_pill_badge(c, MARGIN + 140, PAGE_H - 62, "SELF / OTHER FRAME", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, MARGIN + 290, PAGE_H - 62, "REACTANT ROLE ATTACHMENT", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    
    c.setFont(FONT_BOLD, 14)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 86, "{{ LESSON_TITLE: Oxidation, Reduction & the SELF vs OTHER Agent Attachment Frame }}")
    
    # Left Column: Oxidation State Lane Primitive & Rule Ladder
    draw_oxidation_state_lane(
        c, col1_x, content_top - 120, col_w, 120,
        title="{{ VISUAL_PRIMITIVE: Electron Transfer & Oxidation State Progression }}",
        reactant_label="Fe^2+ (aq)", reactant_on="+2",
        product_label="Fe^3+ (aq)", product_on="+3",
        delta_text="Delta ON = +1 (Oxidation)",
        electron_text="Loss of 1e- --> Fe^2+ is REDUCING AGENT"
    )
    
    c.setFillColor(colors.HexColor("#ECFDF5"))
    c.setStrokeColor(colors.HexColor("#A7F3D0"))
    c.roundRect(col1_x, content_top - 425, col_w, 295, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 9.5)
    c.setFillColor(colors.HexColor("#065F46"))
    c.drawString(col1_x + 14, content_top - 138, "{{ RULE_PRIORITY_LADDER: The Ironclad Order of Precedence }}")
    
    ladder_text = [
        "Consult rules in this strict order. NEVER override an earlier rule with a later rule:",
        "",
        "1. Priority 1 - Free Elemental State: Any uncombined element has ON = 0.",
        "   Examples: O2, P4, S8, Fe, Cu, Cl2 => all have ON = 0.",
        "",
        "2. Priority 2 - Alkali & Alkaline Earth Metals:",
        "   Group 1 (Li, Na, K, Rb) is ALWAYS +1 in compounds. Group 2 (Be, Mg, Ca, Ba) is ALWAYS +2.",
        "",
        "3. Priority 3 - Fluorine: The most electronegative element. In compounds, F is ALWAYS -1.",
        "",
        "4. Priority 4 - Hydrogen: Usually +1. Exception: in metal hydrides (NaH, CaH2), H = -1.",
        "",
        "5. Priority 5 - Oxygen: Usually -2. Exceptions: in peroxides (H2O2), O = -1; in OF2, O = +2.",
        "",
        "6. Priority 6 - Halogens: Usually -1. Exception: when bonded to more electronegative atoms (O, F).",
        "",
        "7. Priority 7 - The Sum Rule (Final Step):",
        "   Sum of all ONs = Net Charge of the molecule or polyatomic ion. Solve for unknown element."
    ]
    ty = content_top - 156
    for line in ladder_text:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5.") or line.startswith("6.") or line.startswith("7."):
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#065F46"))
        else:
            c.setFont(FONT_NAME, 7.2)
            c.setFillColor(colors.HexColor("#1E293B"))
        c.drawString(col1_x + 14, ty, line)
        ty -= 12.0
        
    # Right Column: SELF vs OTHER Agent Frame & Core 2 Link
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(colors.HexColor("#BFDBFE"))
    c.roundRect(col2_x, content_top - 180, col_w, 180, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 16, "SELF VS OTHER REASONING FRAME", colors.HexColor("#1D4ED8"), colors.white)
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#1E40AF"))
    c.drawString(col2_x + 12, content_top - 32, "{{ FRAME: What It Undergoes vs What It Causes }}")
    
    frame_text = [
        "The central pedagogical barrier in Redox is confounding the PROCESS with the AGENT.",
        "Remember: Agent name describes what it does to the OTHER reactant!",
        "",
        "* OXIDATION (Process): Loss of electrons => Oxidation Number INCREASES (UP).",
        "* REDUCTION (Process): Gain of electrons => Oxidation Number DECREASES (DOWN).",
        "",
        "THE AGENT ATTACHMENT CONTRACT:",
        "1. The species that UNDERGOES OXIDATION loses electrons and donates them to the other.",
        "   Therefore, it CAUSES the other species to be reduced => It is the REDUCING AGENT.",
        "2. The species that UNDERGOES REDUCTION gains electrons by taking them from the other.",
        "   Therefore, it CAUSES the other species to be oxidised => It is the OXIDISING AGENT.",
        "3. Critical Scope Gate: The role belongs to the ENTIRE REACTANT SPECIES, never product!",
        "   Example: In 2Fe^2+ + Cl2 --> 2Fe^3+ + 2Cl^-, Fe^2+ is reducing agent; Cl2 is oxidising agent."
    ]
    ty = content_top - 46
    for line in frame_text:
        if line.startswith("* OXIDATION") or line.startswith("* REDUCTION") or "THE AGENT ATTACHMENT" in line:
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#1E40AF"))
        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            c.setFont(FONT_NAME, 7.2)
            c.setFillColor(colors.HexColor("#1E3A8A"))
        else:
            c.setFont(FONT_NAME, 7.2)
            c.setFillColor(colors.HexColor("#1E293B"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 10.8
        
    # Guided Drill & Core 2 Link
    c.setFillColor(colors.HexColor("#F0FDF4"))
    c.setStrokeColor(colors.HexColor("#86EFAC"))
    c.roundRect(col2_x, content_top - 425, col_w, 235, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 198, "GUIDED DRILL & CORE 2 TRANSFER LINK", colors.HexColor("#166534"), colors.white)
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#14532D"))
    c.drawString(col2_x + 14, content_top - 220, "{{ GUIDED_DRILL: MnO2 + 4HCl --> MnCl2 + Cl2 + 2H2O }}")
    
    drill_text = [
        "Analyze the reaction step-by-step:",
        "* Mn in MnO2: ON = +4  -->  Mn in MnCl2: ON = +2. (Change: -2, Reduction).",
        "* Cl in HCl: ON = -1  -->  Cl in Cl2: ON = 0. (Change: +1, Oxidation).",
        "* The Oxidised Atom is: Cl^-. The Changing Reactant Species is: HCl.",
        "* Therefore, the REDUCING AGENT is: HCl. The OXIDISING AGENT is: MnO2.",
        "",
        "CORE 2 TRANSFER PIPELINE LINK:",
        "You are now qualified for the full ExamSIDE Core 2 Transfer Suite.",
        "Target Modules: RX-C2-01 through RX-C2-24 (JEE Main 2019-2023 audited items).",
        "Features: Primary/Supporting concept badges, H0-H3 hint ladders, verified solutions.",
        "Next: Open Chemistry Core 2 Transfer Book."
    ]
    ty = content_top - 236
    for line in drill_text:
        if line.startswith("* The") or line.startswith("* Therefore") or "CORE 2" in line:
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#166534"))
        else:
            c.setFont(FONT_NAME, 7.2)
            c.setFillColor(colors.HexColor("#1F2937"))
        c.drawString(col2_x + 14, ty, line)
        ty -= 13.0
        
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Chemistry V2  |  Core (1) Redox Master Study Guide  |  Template ID: CHEM-CORE1-MASTER-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "Core 1 Complete  *  Proceed to Core 2 Transfer Book  ->")
    
    c.save()
    print(f"Successfully generated: {output_path}")

def render_chemistry_core2(output_path):
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H))
    
    # -------------------------------------------------------------------------
    # PAGE 1: ExamSIDE C-I Core 2 Transfer Question Page (Single Page Layout)
    # -------------------------------------------------------------------------
    # Header Banner
    c.setFillColor(colors.HexColor("#065F46"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "GRADE 9 CHEMISTRY  *  CORE 2 TRANSFER BOOK (EXAMSIDE)")
    c.setFont(FONT_NAME, 8.5)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "C-I COMPLIANT: PRIMARY/SUPPORTS CONCEPTS + H0-H3 HINTS + VERIFIED SOLUTION")
    
    # 2-Tier Metadata Badges (Strict C-I Standard - Zero Truncation)
    # Row 1 (y = PAGE_H - 58)
    b_x = MARGIN
    b_x += draw_pill_badge(c, b_x, PAGE_H - 58, "ITEM: {{ QUESTION_ID: RX-C2-04 }}", colors.HexColor("#065F46"), colors.white) + 8
    b_x += draw_pill_badge(c, b_x, PAGE_H - 58, "DEMAND: {{ DIFFICULTY_BADGE: STANDARD }}", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F")) + 8
    draw_pill_badge(c, b_x, PAGE_H - 58, "TARGET GRADE: GRADE 9 ADVANCED", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    
    # Row 2 (y = PAGE_H - 76)
    b_x = MARGIN
    b_x += draw_pill_badge(c, b_x, PAGE_H - 76, "PRIMARY: {{ PRIMARY_CONCEPT: RX-S03 Oxidising vs Reducing Agents }}", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF")) + 8
    b_x += draw_pill_badge(c, b_x, PAGE_H - 76, "SUPPORTS: {{ SUPPORTING_CONCEPTS: [RX-S01, RX-S02] }}", colors.HexColor("#F1F5F9"), colors.HexColor("#475569")) + 8
    draw_pill_badge(c, b_x, PAGE_H - 76, "SRC: {{ SOURCE: JEE MAIN 2022 - 27 JUL SHIFT 1 }}", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    
    c.setFont(FONT_BOLD, 13)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 96, "{{ QUESTION_TITLE: Reducing Agent Identification & Electron Transfer in Acidic Permanganate-Oxalate Reaction }}")
    
    col_w = (PAGE_W - 2 * MARGIN - 24) / 2
    col1_x = MARGIN
    col2_x = MARGIN + col_w + 24
    content_top = PAGE_H - 110
    
    # ------------------ LEFT COLUMN: Question & Workspace --------------------
    # Question Stem Box
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#94A3B8"))
    c.roundRect(col1_x, content_top - 140, col_w, 140, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col1_x + 12, content_top - 18, "ORIGINAL EXAMSIDE ITEM", colors.HexColor("#0F172A"), colors.white)
    
    stem_chem = [
        "{{ QUESTION_STEM }}:",
        "In the acidic aqueous redox reaction:",
        "   2 MnO4^-(aq) + 5 C2O4^2-(aq) + 16 H+(aq) --> 2 Mn^2+(aq) + 10 CO2(g) + 8 H2O(l)",
        "identify the reducing agent, the oxidation state change of the reducing element,",
        "and the total moles of electrons transferred per mole of reducing agent.",
        "",
        "Options:",
        "(a) MnO4^-, Mn changes from +7 to +2, 5 electrons",
        "(b) C2O4^2-, C changes from +4 to +3, 1 electron",
        "(c) C2O4^2-, C changes from +3 to +4, 2 electrons",
        "(d) H+, H changes from +1 to 0, 1 electron"
    ]
    ty = content_top - 32
    for line in stem_chem:
        if line.startswith("(c)"):
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#065F46"))
        elif line.startswith("(a)") or line.startswith("(b)") or line.startswith("(d)"):
            c.setFont(FONT_NAME, 7.5)
            c.setFillColor(colors.HexColor("#334155"))
        elif "2 MnO4^-" in line:
            c.setFont(FONT_BOLD, 7.8)
            c.setFillColor(colors.HexColor("#0F172A"))
        else:
            c.setFont(FONT_NAME, 7.8)
            c.setFillColor(colors.HexColor("#0F172A"))
        c.drawString(col1_x + 12, ty, line)
        ty -= 9.8
        
    # Visual Vector Primitive: Oxidation State Lane (Oxalate to CO2)
    draw_oxidation_state_lane(
        c, col1_x, content_top - 258, col_w, 110,
        title="{{ VISUAL_PRIMITIVE: Carbon Oxidation & Role Assignment Lane }}",
        reactant_label="C2O4^2- (aq)", reactant_on="+3",
        product_label="2 CO2 (g)", product_on="+4",
        delta_text="Delta ON = +1 per C (Oxidation)",
        electron_text="Loss of 2e- per unit --> C2O4^2- is REDUCING AGENT"
    )
    
    # Attempt Workspace (Ends at content_top - 425)
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col1_x, content_top - 425, col_w, 159, 6, fill=1, stroke=1)
    
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(col1_x + 14, content_top - 280, "{{ H0_ATTEMPT_WORKSPACE: Work Here * Try Before Looking at Hints }}")
    
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    for ly in range(int(content_top - 298), int(content_top - 400), -18):
        c.line(col1_x + 14, ly, col1_x + col_w - 14, ly)
        
    c.setFont(FONT_BOLD, 7.8)
    c.setFillColor(colors.HexColor("#065F46"))
    c.drawString(col1_x + 14, content_top - 416, "Your Attempt: Option [ _____ ]     Oxidant: ___________  Reductant: ___________")
    
    # ------------------ RIGHT COLUMN: Hints, Route & Solution ----------------
    # Faded Hint Ladder (H1 -> H2 -> H3)
    c.setFillColor(colors.HexColor("#FFFBEB"))
    c.setStrokeColor(colors.HexColor("#FDE68A"))
    c.roundRect(col2_x, content_top - 115, col_w, 115, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 18, "H1-H3 HINT LADDER (READ ONLY IF STUCK)", colors.HexColor("#B45309"), colors.white)
    
    hints_chem = [
        "* {{ H1_NOTICE }}: Assign oxidation numbers to Carbon in reactant C2O4^2- and product CO2.",
        "* {{ H2_MODEL }}: The reducing agent is the REACTANT that is OXIDISED (increases ON).",
        "  Calculate ON jump per Carbon atom, then multiply by 2 Carbon atoms per C2O4^2-.",
        "* {{ H3_START }}: In C2O4^2-: 2C + 4(-2) = -2 => 2C = +6 => C = +3.",
        "  In CO2: C + 2(-2) = 0 => C = +4. Delta ON = +1 per C. Two carbons => 2 electrons lost."
    ]
    ty = content_top - 34
    c.setFont(FONT_NAME, 7.2)
    c.setFillColor(colors.HexColor("#78350F"))
    for line in hints_chem:
        c.drawString(col2_x + 12, ty, line)
        ty -= 14.5
        
    # Reasoning Route (Height = 100 pt)
    rr_top = content_top - 123
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(colors.HexColor("#BFDBFE"))
    c.roundRect(col2_x, rr_top - 100, col_w, 100, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, rr_top - 16, "CHEMISTRY REASONING ROUTE", colors.HexColor("#1D4ED8"), colors.white)
    
    route_chem = [
        "Step 1 [PARSE & BIND]: Identify reactants and spectator ions. H+ acts as medium carrier.",
        "Step 2 [TRACK ON]: Mn in MnO4^- (+7) --> Mn^2+ (+2) [Gain of 5e-, Reduction].",
        "Step 3 [TRACK REDUCTANT]: C in C2O4^2- (+3) --> C in CO2 (+4) [Loss of 1e- per C, Oxidation].",
        "Step 4 [ATTACH ROLE]: Oxalate ion C2O4^2- undergoes oxidation => It is the REDUCING AGENT.",
        "Step 5 [COUNT ELECTRONS]: 1 formula unit of C2O4^2- contains 2 C atoms => 2 x 1e- = 2e- transferred."
    ]
    ty = rr_top - 32
    c.setFont(FONT_BOLD, 7.2)
    c.setFillColor(colors.HexColor("#1E40AF"))
    for line in route_chem:
        c.drawString(col2_x + 12, ty, line)
        ty -= 13.0
        
    # Verified Solution & Verification Check (Height = 194 pt, Ends at content_top - 425)
    sol_top = rr_top - 108
    sol_h = 194
    c.setFillColor(colors.HexColor("#F0FDF4"))
    c.setStrokeColor(colors.HexColor("#86EFAC"))
    c.roundRect(col2_x, sol_top - sol_h, col_w, sol_h, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, sol_top - 16, "VERIFIED SOLUTION & SYSTEM VERIFICATION", colors.HexColor("#15803D"), colors.white)
    
    sol_chem = [
        "{{ SOLUTION_FINAL_ANSWER }}: Correct Option is (c).",
        "Chemical Language Response: The reducing agent is oxalate ion C2O4^2-.",
        "Carbon changes from oxidation state +3 to +4, releasing 2 moles of electrons per mole of C2O4^2-.",
        "",
        "{{ VERIFICATION_ROUTE }}:",
        "1. Total Electron Balance Check:",
        "   Total electrons lost by 5 moles of C2O4^2- = 5 x 2e- = 10 moles of electrons.",
        "   Total electrons gained by 2 moles of MnO4^- = 2 x 5e- = 10 moles of electrons.",
        "   Electrons lost = Electrons gained = 10e-. [100% ELECTRON CONSERVATION PASS]",
        "2. Atom Conservation Check: 2 Mn, 10 C, 24 O, 16 H on both sides. [ATOM CONSERVATION PASS]",
        "3. Charge Conservation Check: 2(-1) + 5(-2) + 16(+1) = +4 = 2(+2). [CHARGE BALANCE PASS]",
        "4. {{ CONDITION_EXCEPTION_CHECK }}: Reaction is recorded in acidic solution; product is Mn^2+. [PASS]",
        "Linkage: Traceable to Core1 Lesson RX-ST03 (Agent Roles & Electron Conservation)."
    ]
    ty = sol_top - 32
    for line in sol_chem:
        if line.startswith("{{ SOLUTION") or line.startswith("{{ VERIFICATION"):
            c.setFont(FONT_BOLD, 7.8)
            c.setFillColor(colors.HexColor("#14532D"))
        elif line.startswith("Linkage:"):
            c.setFont(FONT_OBLIQUE, 7)
            c.setFillColor(colors.HexColor("#065F46"))
        else:
            c.setFont(FONT_NAME, 6.8)
            c.setFillColor(colors.HexColor("#1F2937"))
        c.drawString(col2_x + 12, ty, line)
        ty -= 11.2
        
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 Chemistry V2  |  Core (2) ExamSIDE Transfer Sheet  |  Template ID: CHEM-CORE2-SINGLE-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "End of Transfer Item  *  Traceable to Core1 Lesson RX-ST03")
    
    c.save()
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "output_samples"
    out_dir.mkdir(parents=True, exist_ok=True)
    render_chemistry_core1(out_dir / "Chemistry_Core1_MasterGuide_Sample.pdf")
    render_chemistry_core2(out_dir / "Chemistry_Core2_Transfer_Sample.pdf")
