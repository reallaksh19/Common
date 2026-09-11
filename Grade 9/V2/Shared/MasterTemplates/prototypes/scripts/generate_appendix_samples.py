"""
Generator for Appendix A, B, and C Master Sample Templates:
1. Appendix_A_CorePractice_Sample.pdf (Landscape A4: Tiered Core Practice  -  Guided, Faded, Independent, Probe)
2. Appendix_B_CoreSolutions_Sample.pdf (Landscape A4: Complete Multi-Step Reasoning Solutions & Verification)
3. Appendix_C_PrintableHandout_Sample.pdf (Landscape A4: Answer-Free, Grayscale-Safe Quick Reference Handout)
"""

import os, sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from primitives import (
    draw_pill_badge,
    FONT_NAME,
    FONT_BOLD
)

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 36

# ==============================================================================
# APPENDIX A: CORE PRACTICE (GUIDED -> FADED -> INDEPENDENT -> PROBE)
# ==============================================================================
def render_appendix_a(output_path):
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H))
    
    # Header Banner
    c.setFillColor(colors.HexColor("#0F172A"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "{{ SUBJECT_NAME }}  *  APPENDIX A: CORE PRACTICE")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "TIERED PRACTICE: GUIDED * FADED * INDEPENDENT * PROBE")
    
    # Badges
    draw_pill_badge(c, MARGIN, PAGE_H - 62, "APPENDIX A  -  CORE PRACTICE", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    draw_pill_badge(c, MARGIN + 185, PAGE_H - 62, "TIERED SCAFFOLDING", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, MARGIN + 335, PAGE_H - 62, "SOLUTIONS IN APPENDIX B", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    
    c.setFont(FONT_BOLD, 14)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 86, "{{ CHAPTER_TITLE: Comprehensive Topic Mastery & Practice Items }}")
    
    col_w = (PAGE_W - 2 * MARGIN - 24) / 2
    col1_x = MARGIN
    col2_x = MARGIN + col_w + 24
    content_top = PAGE_H - 104
    
    # ------------------ COLUMN 1: Tier 1 (Guided) & Tier 2 (Faded) -----------
    # Tier 1: Guided Practice Item
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col1_x, content_top - 180, col_w, 180, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col1_x + 12, content_top - 18, "TIER 1: GUIDED PRACTICE", colors.HexColor("#0284C7"), colors.white)
    draw_pill_badge(c, col1_x + 160, content_top - 18, "ITEM: {{ ITEM_ID: PRAC-01 }}", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col1_x + 12, content_top - 36, "{{ CAPABILITY_REF: CAP-ASSIGN-OXIDATION-NUMBER-CORE }}")
    
    p1_lines = [
        "{{ PROMPT }}: Determine the oxidation state of Phosphorus in H3PO4.",
        "Representation Spec: FORMULA_ANATOMY_VIEW",
        "",
        "Step-by-Step Guided Scaffolding:",
        "1. Identify fixed-rule elements: Hydrogen is in non-metal compound => H = +1.",
        "   Three Hydrogen atoms contribute: 3 x (+1) = +3.",
        "2. Identify Oxygen default: No peroxide bond present => O = -2.",
        "   Four Oxygen atoms contribute: 4 x (-2) = -8.",
        "3. Set up the Sum Invariant (Net charge = 0):",
        "   (+3) + P + (-8) = 0 => P - 5 = 0 => P = [ _____ ].",
        "Solution Reference: [See Appendix B --> SOL-PRAC-01]"
    ]
    ty = content_top - 54
    for line in p1_lines:
        if "Guided Scaffolding" in line:
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#0284C7"))
        elif line.startswith("Solution Reference"):
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#64748B"))
        else:
            c.setFont(FONT_NAME, 8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col1_x + 12, ty, line)
        ty -= 12.5
        
    # Tier 2: Faded Practice Item
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col1_x, content_top - 380, col_w, 190, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col1_x + 12, content_top - 198, "TIER 2: FADED PRACTICE", colors.HexColor("#D97706"), colors.white)
    draw_pill_badge(c, col1_x + 155, content_top - 198, "ITEM: {{ ITEM_ID: PRAC-02 }}", colors.HexColor("#FEF3C7"), colors.HexColor("#92400E"))
    
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col1_x + 12, content_top - 216, "{{ CAPABILITY_REF: CAP-TRACK-ELEMENT-CHARGE-CHANGE }}")
    
    p2_lines = [
        "{{ PROMPT }}: For the reaction: Zn(s) + 2HCl(aq) --> ZnCl2(aq) + H2(g),",
        "identify which element undergoes oxidation and which undergoes reduction.",
        "",
        "Faded Support Steps:",
        "1. Write ON above each atom in reactants: Zn = [ ___ ], H in HCl = [ ___ ], Cl in HCl = [ ___ ].",
        "2. Write ON above each atom in products: Zn in ZnCl2 = [ ___ ], Cl = [ ___ ], H in H2 = [ ___ ].",
        "3. Track direction of change:",
        "   * Zn changes from ___ to ___ => (Increase/Decrease) => [ __________________ ].",
        "   * H changes from ___ to ___ => (Increase/Decrease) => [ __________________ ].",
        "Solution Reference: [See Appendix B --> SOL-PRAC-02]"
    ]
    ty = content_top - 234
    for line in p2_lines:
        if "Faded Support" in line:
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#D97706"))
        elif line.startswith("Solution Reference"):
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#64748B"))
        else:
            c.setFont(FONT_NAME, 8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col1_x + 12, ty, line)
        ty -= 13.5
        
    # ------------------ COLUMN 2: Tier 3 (Independent) & Tier 4 (Probe) ------
    # Tier 3: Independent Practice Item
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col2_x, content_top - 180, col_w, 180, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 18, "TIER 3: INDEPENDENT PRACTICE", colors.HexColor("#059669"), colors.white)
    draw_pill_badge(c, col2_x + 185, content_top - 18, "ITEM: {{ ITEM_ID: PRAC-03 }}", colors.HexColor("#ECFDF5"), colors.HexColor("#065F46"))
    
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(col2_x + 12, content_top - 36, "{{ CAPABILITY_REF: CAP-ATTACH-REDOX-ROLES }}")
    
    p3_lines = [
        "{{ PROMPT }}: In the industrial reaction: Fe2O3(s) + 3CO(g) --> 2Fe(s) + 3CO2(g):",
        "(a) Name the oxidising agent and reducing agent.",
        "(b) Calculate the total moles of electrons transferred per mole of Fe2O3 reacted.",
        "",
        "Instructions: Complete without hints. Show your work clearly.",
        "Your Working Area:",
        "* Oxidising Agent: ____________________    Reducing Agent: ____________________",
        "* Electron Transfer Calculation: _______________________________________________",
        "Solution Reference: [See Appendix B --> SOL-PRAC-03]"
    ]
    ty = content_top - 54
    for line in p3_lines:
        if line.startswith("Instructions"):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#059669"))
        elif line.startswith("Solution Reference"):
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#64748B"))
        else:
            c.setFont(FONT_NAME, 8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col2_x + 12, ty, line)
        ty -= 14
        
    # Tier 4: Diagnostic Probe Item (Scored & Misconception Sensitive)
    c.setFillColor(colors.HexColor("#FFF1F2"))
    c.setStrokeColor(colors.HexColor("#FECDD3"))
    c.roundRect(col2_x, content_top - 380, col_w, 190, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 198, "TIER 4: DIAGNOSTIC PROBE (TRAP DETECTOR)", colors.HexColor("#DC2626"), colors.white)
    draw_pill_badge(c, col2_x + 235, content_top - 198, "ITEM: {{ ITEM_ID: PRAC-04 }}", colors.HexColor("#FEE2E2"), colors.HexColor("#991B1B"))
    
    c.setFont(FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#991B1B"))
    c.drawString(col2_x + 12, content_top - 216, "{{ CAPABILITY_REF: CAP-DISCRIMINATE-PEROXIDE-EXCEPTION }}")
    
    p4_lines = [
        "{{ PROMPT }}: A student calculates the oxidation state of Oxygen in BaO2 by applying",
        "the standard rule (O = -2), concluding Ba = +4. Evaluate this claim.",
        "",
        "Diagnostic Evaluation Questions:",
        "1. Is Ba = +4 physically permissible for an Alkaline Earth metal (Group 2)? [ YES / NO ]",
        "2. Which rule takes priority: Group 2 fixed charge (+2) OR default Oxygen (-2)?",
        "   Priority Rule: _________________________________________________________________",
        "3. Deduce the correct oxidation state of Oxygen in barium peroxide (BaO2):",
        "   Correct ON of Oxygen = [ _____ ].",
        "Solution Reference: [See Appendix B --> SOL-PRAC-04]"
    ]
    ty = content_top - 234
    for line in p4_lines:
        if line.startswith("Diagnostic"):
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor("#B91C1C"))
        elif line.startswith("Solution Reference"):
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#64748B"))
        else:
            c.setFont(FONT_NAME, 8)
            c.setFillColor(colors.HexColor("#881337"))
        c.drawString(col2_x + 12, ty, line)
        ty -= 13.5
        
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 V2 Architecture  |  Appendix A: Tiered Core Practice  |  Template ID: SHARED-APP-A-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "Full Solutions Available in Appendix B  ->")
    
    c.save()
    print(f"Successfully generated: {output_path}")

# ==============================================================================
# APPENDIX B: CORE SOLUTIONS & VERIFICATION
# ==============================================================================
def render_appendix_b(output_path):
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H))
    
    # Header Banner
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "{{ SUBJECT_NAME }}  *  APPENDIX B: CORE SOLUTIONS")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "REASONING ROUTES * VERIFICATION CHECKS * AUDITS")
    
    draw_pill_badge(c, MARGIN, PAGE_H - 62, "APPENDIX B  -  CORE SOLUTIONS", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    draw_pill_badge(c, MARGIN + 195, PAGE_H - 62, "VERIFIED PROOFS", colors.HexColor("#DEF7EC"), colors.HexColor("#03543F"))
    draw_pill_badge(c, MARGIN + 325, PAGE_H - 62, "FAIL-CLOSED AUDITS", colors.HexColor("#F1F5F9"), colors.HexColor("#475569"))
    
    c.setFont(FONT_BOLD, 14)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 86, "{{ SOLUTIONS_DIRECTORY: Complete Verified Solutions for Appendix A Practice Items }}")
    
    col_w = (PAGE_W - 2 * MARGIN - 24) / 2
    col1_x = MARGIN
    col2_x = MARGIN + col_w + 24
    content_top = PAGE_H - 104
    
    # ------------------ COLUMN 1: Solutions PRAC-01 & PRAC-02 ----------------
    # Solution PRAC-01
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col1_x, content_top - 180, col_w, 180, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col1_x + 12, content_top - 18, "SOLUTION: SOL-PRAC-01", colors.HexColor("#1E3A8A"), colors.white)
    draw_pill_badge(c, col1_x + 160, content_top - 18, "TARGET: PRAC-01", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    
    s1_lines = [
        "{{ PRIMARY_CAPABILITY: CAP-ASSIGN-OXIDATION-NUMBER-CORE }}",
        "",
        "Reasoning Steps:",
        "1. Identify compound type: Phosphoric acid (H3PO4) is a neutral molecule (Net charge = 0).",
        "2. Apply Rule Priority 4 (Hydrogen): Hydrogen is bonded to non-metals => H = +1.",
        "   Total H contribution = 3 x (+1) = +3.",
        "3. Apply Rule Priority 5 (Oxygen): Standard oxide bonding => O = -2. Total O = 4 x (-2) = -8.",
        "4. Apply Priority 7 (Sum Rule): Let ON of P = x.",
        "   (+3) + x + (-8) = 0 => x - 5 = 0 => x = +5.",
        "",
        "{{ FINAL_RESPONSE }}: The oxidation state of Phosphorus in H3PO4 is +5.",
        "{{ VERIFICATION_STEP }}: (+3) + (+5) + (-8) = 0. Charge balance is exactly satisfied.",
        "{{ CONDITION_NOTE }}: Phosphorus uses all 5 valence electrons in bonding; +5 is its maximum state."
    ]
    ty = content_top - 34
    for line in s1_lines:
        if line.startswith("{{ FINAL") or line.startswith("{{ VERIFICATION"):
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(colors.HexColor("#047857"))
        elif line.startswith("Reasoning"):
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(colors.HexColor("#1E3A8A"))
        else:
            c.setFont(FONT_NAME, 7)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col1_x + 12, ty, line)
        ty -= 10.5
        
    # Solution PRAC-02
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col1_x, content_top - 390, col_w, 200, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col1_x + 12, content_top - 198, "SOLUTION: SOL-PRAC-02", colors.HexColor("#1E3A8A"), colors.white)
    draw_pill_badge(c, col1_x + 160, content_top - 198, "TARGET: PRAC-02", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    
    s2_lines = [
        "{{ PRIMARY_CAPABILITY: CAP-TRACK-ELEMENT-CHARGE-CHANGE }}",
        "",
        "Reasoning Steps:",
        "1. Assign ON to every reactant species:",
        "   * Free Zinc metal Zn(s): Elemental state => ON = 0.",
        "   * In HCl(aq): H = +1, Cl = -1.",
        "2. Assign ON to every product species:",
        "   * In ZnCl2(aq): Group 12 metal Zn = +2; two chloride ions each Cl = -1.",
        "   * In H2(g): Free elemental diatomic hydrogen gas => ON = 0.",
        "3. Track direction of electron transfer:",
        "   * Zinc: Changes from 0 to +2 => Loss of 2e- => UNDERGOES OXIDATION.",
        "   * Hydrogen: Changes from +1 to 0 => Gain of 1e- per atom => UNDERGOES REDUCTION.",
        "   * Chloride: Stays at -1 => Spectator ion (unchanged).",
        "",
        "{{ FINAL_RESPONSE }}: Zinc is oxidised (0 -> +2); Hydrogen is reduced (+1 -> 0).",
        "{{ VERIFICATION_STEP }}: 1 mole Zn loses 2e-; 2 moles H+ gain 2(1e-) = 2e-. 100% conserved."
    ]
    ty = content_top - 214
    for line in s2_lines:
        if line.startswith("{{ FINAL") or line.startswith("{{ VERIFICATION"):
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(colors.HexColor("#047857"))
        elif line.startswith("Reasoning"):
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(colors.HexColor("#1E3A8A"))
        else:
            c.setFont(FONT_NAME, 6.8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col1_x + 12, ty, line)
        ty -= 10.5
        
    # ------------------ COLUMN 2: Solutions PRAC-03 & PRAC-04 ----------------
    # Solution PRAC-03
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col2_x, content_top - 185, col_w, 185, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 18, "SOLUTION: SOL-PRAC-03", colors.HexColor("#1E3A8A"), colors.white)
    draw_pill_badge(c, col2_x + 160, content_top - 18, "TARGET: PRAC-03", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF"))
    
    s3_lines = [
        "{{ PRIMARY_CAPABILITY: CAP-ATTACH-REDOX-ROLES }}",
        "",
        "Reasoning Steps:",
        "1. Identify reacting species and changes in Fe2O3 + 3CO -> 2Fe + 3CO2:",
        "   * Iron in Fe2O3: 2Fe + 3(-2) = 0 => Fe = +3. In product Fe(s): Fe = 0.",
        "     Fe decreases from +3 to 0 => Reduction. Therefore, Fe2O3 is the OXIDISING AGENT.",
        "   * Carbon in CO: C + (-2) = 0 => C = +2. In product CO2: C + 2(-2) = 0 => C = +4.",
        "     C increases from +2 to +4 => Oxidation. Therefore, CO is the REDUCING AGENT.",
        "2. Calculate electron count per formula unit of Fe2O3:",
        "   Each Iron atom decreases by 3 units: Fe3+ + 3e- -> Fe0.",
        "   1 formula unit of Fe2O3 contains 2 Iron atoms => 2 x 3e- = 6 electrons accepted.",
        "   Check: 3 moles of CO each lose 2e- => 3 x 2e- = 6 electrons donated. (Matches exactly).",
        "",
        "{{ FINAL_RESPONSE }}: Oxidising Agent = Fe2O3; Reducing Agent = CO; 6 moles e- transferred.",
        "{{ VERIFICATION_STEP }}: Agent names attached to ENTIRE reactant species, not isolated atoms."
    ]
    ty = content_top - 34
    for line in s3_lines:
        if line.startswith("{{ FINAL") or line.startswith("{{ VERIFICATION"):
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(colors.HexColor("#047857"))
        elif line.startswith("Reasoning"):
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(colors.HexColor("#1E3A8A"))
        else:
            c.setFont(FONT_NAME, 6.8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col2_x + 12, ty, line)
        ty -= 10.2
        
    # Solution PRAC-04 (Diagnostic Probe)
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(col2_x, content_top - 395, col_w, 195, 6, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 12, content_top - 200, "SOLUTION: SOL-PRAC-04", colors.HexColor("#DC2626"), colors.white)
    draw_pill_badge(c, col2_x + 160, content_top - 200, "TARGET: PRAC-04", colors.HexColor("#FEE2E2"), colors.HexColor("#991B1B"))
    
    s4_lines = [
        "{{ PRIMARY_CAPABILITY: CAP-DISCRIMINATE-PEROXIDE-EXCEPTION }}",
        "",
        "Reasoning Steps (Causal Misconception Repair):",
        "1. Physical impossibility check: Barium is an alkaline earth metal (Group 2, [Xe] 6s2).",
        "   Its ionization energies allow only a +2 oxidation state (loss of two 6s electrons).",
        "   Ba = +4 would require breaking into the stable closed noble-gas shell of Xenon (impossible).",
        "2. Rule Priority Hierarchy: Priority 2 (Group 2 metal is ALWAYS +2) overrides Priority 5 (Oxygen).",
        "   Therefore, Ba MUST be assigned +2 fixed.",
        "3. Evaluate Oxygen via Sum Rule:",
        "   (+2) + 2(ON_O) = 0 => 2(ON_O) = -2 => ON of Oxygen = -1.",
        "4. Structural Confirmation: BaO2 contains the peroxide linkage [O-O]2-.",
        "",
        "{{ FINAL_RESPONSE }}: Student claim is FALSE. Ba is fixed at +2; Oxygen is -1 (Peroxide).",
        "{{ CONDITION_NOTE }}: Group 1 and 2 metal fixed rules strictly precede the Oxygen default rule."
    ]
    ty = content_top - 216
    for line in s4_lines:
        if line.startswith("{{ FINAL") or line.startswith("{{ CONDITION"):
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(colors.HexColor("#991B1B"))
        elif line.startswith("Reasoning"):
            c.setFont(FONT_BOLD, 7)
            c.setFillColor(colors.HexColor("#1E3A8A"))
        else:
            c.setFont(FONT_NAME, 6.8)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col2_x + 12, ty, line)
        ty -= 10.5
        
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(MARGIN, 18, "Grade 9 V2 Architecture  |  Appendix B: Verified Core Solutions  |  Template ID: SHARED-APP-B-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "End of Appendix B  *  Next: Appendix C Printable Handout  ->")
    
    c.save()
    print(f"Successfully generated: {output_path}")

# ==============================================================================
# APPENDIX C: STANDALONE PRINTABLE HANDOUT (ANSWER-FREE & GRAYSCALE SAFE)
# ==============================================================================
def render_appendix_c(output_path):
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_W, PAGE_H))
    
    # Header Banner (Grayscale-safe slate dark)
    c.setFillColor(colors.HexColor("#1E293B"))
    c.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)
    
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(colors.white)
    c.drawString(MARGIN, PAGE_H - 26, "{{ SUBJECT_NAME }}  *  APPENDIX C: QUICK REFERENCE HANDOUT")
    c.setFont(FONT_NAME, 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, "ANSWER-FREE  *  GRAYSCALE-SAFE  *  STANDALONE")
    
    draw_pill_badge(c, MARGIN, PAGE_H - 62, "APPENDIX C  -  QUICK REFERENCE", colors.HexColor("#F1F5F9"), colors.HexColor("#0F172A"))
    draw_pill_badge(c, MARGIN + 215, PAGE_H - 62, "PRINT CONSTRAINT: ANSWER_FREE", colors.HexColor("#F1F5F9"), colors.HexColor("#0F172A"))
    draw_pill_badge(c, MARGIN + 430, PAGE_H - 62, "PRINT CONSTRAINT: GRAYSCALE_SAFE", colors.HexColor("#F1F5F9"), colors.HexColor("#0F172A"))
    
    c.setFont(FONT_BOLD, 14)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(MARGIN, PAGE_H - 86, "{{ HANDOUT_TITLE: Essential First Moves, Decision Flowcharts & Verification Cues }}")
    
    # 3-Column Grid for Handout
    col_w = (PAGE_W - 2 * MARGIN - 32) / 3
    col1_x = MARGIN
    col2_x = MARGIN + col_w + 16
    col3_x = MARGIN + 2 * (col_w + 16)
    content_top = PAGE_H - 104
    
    # Card 1: Capability 1 (Oxidation State Assignment)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#334155"))
    c.setLineWidth(1)
    c.roundRect(col1_x, content_top - 345, col_w, 345, 4, fill=1, stroke=1)
    
    draw_pill_badge(c, col1_x + 10, content_top - 18, "CAPABILITY 01: OXIDATION STATE", colors.HexColor("#334155"), colors.white)
    
    c1_lines = [
        "{{ FIRST_MOVE }}:",
        "* Check if element is uncombined => ON = 0.",
        "* Otherwise, write fixed rules above metals:",
        "  Group 1 = +1, Group 2 = +2, Fluorine = -1.",
        "* Check Hydrogen: Non-metal compound = +1,",
        "  metal hydride = -1.",
        "* Check Oxygen: Standard = -2, peroxide = -1.",
        "",
        "{{ RULE_OR_DECISION_CUE }}:",
        "Decision Ladder Order:",
        "1. Element alone? => 0",
        "2. Group 1 / 2 metal present? => +1 / +2",
        "3. Fluorine present? => -1",
        "4. Hydrogen? => +1 (or -1 with metal)",
        "5. Oxygen? => -2 (or -1 in peroxide)",
        "6. Sum of all ONs = Net Charge of species.",
        "   Solve algebraically for the unknown.",
        "",
        "{{ VERIFICATION_CUE }}:",
        "* Multiply assigned ON by atom count.",
        "* Add all contributions algebraically.",
        "* Sum MUST equal overall molecule/ion charge.",
        "* Check that metal does not exceed max valence."
    ]
    ty = content_top - 36
    for line in c1_lines:
        if line.startswith("{{ FIRST") or line.startswith("{{ RULE") or line.startswith("{{ VERIFICATION"):
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#0F172A"))
        else:
            c.setFont(FONT_NAME, 7)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col1_x + 10, ty, line)
        ty -= 13.5
        
    # Card 2: Capability 2 (Redox Roles: Self vs Other)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#334155"))
    c.roundRect(col2_x, content_top - 345, col_w, 345, 4, fill=1, stroke=1)
    
    draw_pill_badge(c, col2_x + 10, content_top - 18, "CAPABILITY 02: AGENT ROLES", colors.HexColor("#334155"), colors.white)
    
    c2_lines = [
        "{{ FIRST_MOVE }}:",
        "* Connect identical elements from reactants to",
        "  products with an arrow.",
        "* Calculate Delta ON = ON_product - ON_reactant.",
        "* If Delta ON is positive => Element is OXIDISED.",
        "* If Delta ON is negative => Element is REDUCED.",
        "",
        "{{ RULE_OR_DECISION_CUE }}:",
        "SELF vs OTHER Decision Matrix:",
        "* What it undergoes (SELF) vs What it acts as (OTHER):",
        "  Undergoes Oxidation => Acts as REDUCING AGENT.",
        "  Undergoes Reduction => Acts as OXIDISING AGENT.",
        "",
        "Crucial Role Attachment Rule:",
        "* The agent role belongs to the ENTIRE REACTANT",
        "  species, never an isolated element or product!",
        "  Example: If C in C2O4^2- oxidises, the reducing",
        "  agent is the whole C2O4^2- ion.",
        "",
        "{{ VERIFICATION_CUE }}:",
        "* Total electrons lost by reducing agent MUST",
        "  equal total electrons gained by oxidising agent."
    ]
    ty = content_top - 36
    for line in c2_lines:
        if line.startswith("{{ FIRST") or line.startswith("{{ RULE") or line.startswith("{{ VERIFICATION"):
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#0F172A"))
        else:
            c.setFont(FONT_NAME, 7)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col2_x + 10, ty, line)
        ty -= 13.5
        
    # Card 3: Capability 3 (Kinematics / Physical Model Selection)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#334155"))
    c.roundRect(col3_x, content_top - 345, col_w, 345, 4, fill=1, stroke=1)
    
    draw_pill_badge(c, col3_x + 10, content_top - 18, "CAPABILITY 03: PHYSICAL MODEL GATE", colors.HexColor("#334155"), colors.white)
    
    c3_lines = [
        "{{ FIRST_MOVE }}:",
        "* Draw 1D axis and choose positive direction (+).",
        "* Translate keywords:",
        "  'From rest' => u = 0.",
        "  'Stops / Braking' => v = 0.",
        "  'Highest point' => v_top = 0.",
        "",
        "{{ RULE_OR_DECISION_CUE }}:",
        "Model Gate Decision Tree:",
        "* Constant Velocity? (a = 0) => Use s = vt.",
        "* Constant Acceleration? (a != 0, const):",
        "  1. If time 't' is unknown and not needed:",
        "     Use v^2 = u^2 + 2as.",
        "  2. If final velocity 'v' is not needed:",
        "     Use s = ut + 1/2 at^2.",
        "  3. If displacement 's' is not needed:",
        "     Use v = u + at.",
        "* Free Fall? Set a = -g (if up is positive).",
        "",
        "{{ VERIFICATION_CUE }}:",
        "* Units check: [m/s], [m/s2], [m], [s].",
        "* Direction check: Does displacement sign match",
        "  the final coordinate relative to start?"
    ]
    ty = content_top - 36
    for line in c3_lines:
        if line.startswith("{{ FIRST") or line.startswith("{{ RULE") or line.startswith("{{ VERIFICATION"):
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor("#0F172A"))
        else:
            c.setFont(FONT_NAME, 7)
            c.setFillColor(colors.HexColor("#334155"))
        c.drawString(col3_x + 10, ty, line)
        ty -= 13.5
        
    # Footer
    c.setFont(FONT_NAME, 7.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(MARGIN, 18, "Grade 9 V2 Architecture  |  Appendix C: Standalone Printable Handout (Answer-Free)  |  Template ID: SHARED-APP-C-v1")
    c.drawRightString(PAGE_W - MARGIN, 18, "Authorized for Classroom & Student Exam Reference Use")
    
    c.save()
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "output_samples"
    out_dir.mkdir(parents=True, exist_ok=True)
    render_appendix_a(out_dir / "Appendix_A_CorePractice_Sample.pdf")
    render_appendix_b(out_dir / "Appendix_B_CoreSolutions_Sample.pdf")
    render_appendix_c(out_dir / "Appendix_C_PrintableHandout_Sample.pdf")
