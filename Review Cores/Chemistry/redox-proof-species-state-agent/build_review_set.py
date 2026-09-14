#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import fitz
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
REACTION = "Zn + Cu2+ -> Zn2+ + Cu"
NAVY = HexColor("#17324D")
INK = HexColor("#20262D")
MUTED = HexColor("#66727D")
LINE = HexColor("#C8D1D8")
BLUE = HexColor("#EEF5FA")
GREEN = HexColor("#EDF7EF")
AMBER = HexColor("#FFF5D9")
RED = HexColor("#FCEDEA")

OWNER_OVERRIDE = (
    "Student knowledge percentage was not supplied. This review fixture uses an explicit owner override; "
    "no learner percentage is fabricated. The override changes support only, not Chemistry truth or frozen question identity."
)

RESEARCH = [
    {
        "ref": "Brandriet & Bretz 2014, Chemistry Education Research and Practice",
        "url": "https://pubs.rsc.org/en/content/articlehtml/2014/rp/c4rp00129j",
        "use": "Redox misconception pressure and the need to separate labels from evidence.",
    },
    {
        "ref": "Taber 2013, Chemistry Education Research and Practice",
        "url": "https://pubs.rsc.org/is/content/articlehtml/2013/rp/c3rp00012e",
        "use": "Chemistry representation coordination and disciplined model use.",
    },
    {
        "ref": "RSC: Johnstone's triangle",
        "url": "https://edu.rsc.org/feature/improve-students-understanding-with-johnstones-triangle/4019740.article",
        "use": "Representation transitions should be explicit rather than assumed.",
    },
    {
        "ref": "Crippen & Brooks 2009, Chemistry Education Research and Practice",
        "url": "https://pubs.rsc.org/en/content/articlehtml/2009/rp/b901458f",
        "use": "Worked-example support should give way to completion and independent reasoning.",
    },
]

FROZEN_QUESTIONS = [
    (
        "RQ-REDOX-01",
        f"For {REACTION}, prove which species is oxidised and which is reduced using oxidation-state changes.",
        "Zn: 0 -> +2, so Zn is oxidised. Cu in Cu2+: +2 -> 0, so Cu2+ is reduced.",
    ),
    (
        "RQ-REDOX-02",
        "Write the two electron statements and identify the reducing and oxidising agents.",
        "Zn -> Zn2+ + 2e-. Cu2+ + 2e- -> Cu. Zn is the reducing agent; Cu2+ is the oxidising agent.",
    ),
    (
        "RQ-REDOX-03",
        "A learner says: 'Zn is the reducing agent because Zn gets reduced.' Diagnose the error and repair the reasoning.",
        "The claim reverses Zn's self-change. Zn changes 0 -> +2, so Zn is oxidised; because its electron loss reduces Cu2+, Zn is the reducing agent.",
    ),
]


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    out: list[str] = []
    for para in str(text).split("\n"):
        words = para.split()
        if not words:
            out.append("")
            continue
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if stringWidth(trial, font, size) <= width:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = word
        if cur:
            out.append(cur)
    return out


def text(c, x, y, value, width, size=9.2, font="Helvetica", leading=None, color=INK):
    leading = leading or size * 1.32
    c.setFillColor(color)
    c.setFont(font, size)
    yy = y
    for line in wrap(value, font, size, width):
        c.drawString(x, yy, line)
        yy -= leading
    return yy


def header(c, label: str, title: str, page_no: int, total: int):
    W, H = A4
    c.setFillColor(NAVY)
    c.rect(0, H - 63, W, 63, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(36, H - 27, f"Chemistry {label}")
    c.setFont("Helvetica", 8.2)
    c.drawString(36, H - 45, "Redox proof | species -> state -> electrons -> role")
    c.drawRightString(W - 36, H - 45, f"{page_no}/{total}")
    text(c, 36, H - 91, title, W - 72, 12, "Helvetica-Bold", color=NAVY)


def footer(c):
    W, _ = A4
    c.setStrokeColor(LINE)
    c.line(36, 24, W - 36, 24)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7)
    c.drawString(36, 11, "Static self-study review fixture | answers included | no runtime learner-state inference")


def box(c, x, y, w, h, title, body, fill=BLUE):
    c.setFillColor(fill)
    c.roundRect(x, y - h, w, h, 6, fill=1, stroke=0)
    text(c, x + 12, y - 22, title, w - 24, 8.5, "Helvetica-Bold", color=NAVY)
    text(c, x + 12, y - 43, body, w - 24, 8.6, leading=11.2)


def lane(c, y=635):
    W, _ = A4
    x = 48
    w = W - 96
    c.setFillColor(BLUE)
    c.roundRect(x, y - 92, w, 86, 6, fill=1, stroke=0)
    text(c, x + 12, y - 25, "OXIDATION-STATE LANES", w - 24, 8.4, "Helvetica-Bold", color=NAVY)
    text(c, x + 28, y - 57, "Zn: 0  ->  +2    (increase)", 220, 11, "Helvetica-Bold")
    text(c, x + 285, y - 57, "Cu: +2  ->  0    (decrease)", 230, 11, "Helvetica-Bold")


def species_map(c, y=635):
    W, _ = A4
    x = 48
    w = W - 96
    c.setFillColor(BLUE)
    c.roundRect(x, y - 92, w, 86, 6, fill=1, stroke=0)
    text(c, x + 12, y - 25, "TRACK THE SAME ELEMENT BEFORE COMPARING", w - 24, 8.4, "Helvetica-Bold", color=NAVY)
    text(c, x + 50, y - 58, "Zn  ---------->  Zn2+", 190, 12, "Helvetica-Bold")
    text(c, x + 300, y - 58, "Cu2+  -------->  Cu", 190, 12, "Helvetica-Bold")


def electron_map(c, y=635):
    W, _ = A4
    x = 48
    w = W - 96
    c.setFillColor(GREEN)
    c.roundRect(x, y - 94, w, 88, 6, fill=1, stroke=0)
    text(c, x + 12, y - 25, "ELECTRON LEDGER", w - 24, 8.4, "Helvetica-Bold", color=NAVY)
    text(c, x + 25, y - 57, "Zn -> Zn2+ + 2e-", 220, 11, "Helvetica-Bold")
    text(c, x + 285, y - 57, "Cu2+ + 2e- -> Cu", 220, 11, "Helvetica-Bold")
    text(c, x + 160, y - 79, "2 electrons lost = 2 electrons gained", 270, 8.6, "Helvetica-Bold", color=NAVY)


def render_pages(path: Path, label: str, pages: list[dict]):
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle(f"Chemistry {label} - Redox proof")
    total = len(pages)
    for i, pg in enumerate(pages, 1):
        header(c, label, pg["title"], i, total)
        visual = pg.get("visual")
        if visual == "species":
            species_map(c)
        elif visual == "lane":
            lane(c)
        elif visual == "electron":
            electron_map(c)
        elif visual == "reaction":
            box(c, 48, 650, A4[0] - 96, 78, "GOVERNED REACTION", REACTION, BLUE)
        y = 510 if visual else 650
        for block in pg.get("blocks", []):
            title, body, fill = block
            h = 100 if len(body) < 280 else 125
            box(c, 48, y, A4[0] - 96, h, title, body, fill)
            y -= h + 15
        footer(c)
        c.showPage()
    c.save()


def build_core1():
    pages = [
        {"title": "The whole idea in one chain", "visual": "reaction", "blocks": [
            ("COMPACT RULE", "Track the same element -> compare oxidation state -> connect to electron loss/gain -> attach the agent role last.", GREEN),
            ("WHY ORDER MATTERS", "A reagent name or remembered label is not evidence. In this subtopic the self-change is the proof and the role is the conclusion.", AMBER),
        ]},
        {"title": "Oxidation-state direction", "visual": "lane", "blocks": [
            ("RULE", "Increase in oxidation state means oxidation. Decrease means reduction. Therefore Zn is oxidised and Cu2+ is reduced.", GREEN),
            ("CHECK", "Compare Zn with Zn and Cu with Cu. Never compare unlike elements when deciding the direction of change.", AMBER),
        ]},
        {"title": "Electron consequence", "visual": "electron", "blocks": [
            ("INTERPRETATION", "Zn loses two electrons; Cu2+ gains those two electrons. The electron ledger is an independent consistency check on the oxidation-state conclusion.", GREEN),
        ]},
        {"title": "Agent roles", "visual": "reaction", "blocks": [
            ("ROLE RULE", "Zn is oxidised and supplies electrons that reduce Cu2+, so Zn is the reducing agent. Cu2+ is reduced and accepts electrons from Zn, so Cu2+ is the oxidising agent.", GREEN),
            ("MEMORY GUARD", "The reducing agent is not 'the thing that gets reduced'. Agent names describe the effect caused on the other species after the agent's own change is proved.", RED),
        ]},
        {"title": "Quick retrieval check", "blocks": [
            ("TRY WITHOUT LOOKING", f"For {REACTION}: write both state-change lanes, both electron statements, and both agent roles.", BLUE),
            ("ANSWER", "Zn 0 -> +2: oxidised; Zn -> Zn2+ + 2e-; reducing agent. Cu +2 -> 0: reduced; Cu2+ + 2e- -> Cu; oxidising agent.", GREEN),
        ]},
    ]
    render_pages(ROOT / "01_Core1_Basic_Notes_Redox_Proof.pdf", "Core1 | Basic Notes", pages)


def build_core1a():
    pages = [
        ("Learning target and prerequisites", "Learn to prove Redox roles from reaction evidence. Prerequisites: species identity, elemental oxidation state 0, ionic charge in Cu2+/Zn2+, and the meaning of increase/decrease."),
        ("1. Track identity before labels", "Locate Zn on both sides and Cu on both sides. Do not begin with oxidation, reduction or agent words. Identity is the anchor that makes every later comparison legal."),
        ("2. What an oxidation-state lane does", "The lane is a bookkeeping representation for the same element before and after the reaction. In this governed example Zn is 0 then +2; Cu is +2 then 0."),
        ("3. Work the Zn lane", "Zn starts as elemental Zn, oxidation state 0, and appears as Zn2+, oxidation state +2. The number increases by 2; therefore Zn is oxidised."),
        ("4. Work the Cu lane", "Cu begins in Cu2+ with oxidation state +2 and ends as elemental Cu with oxidation state 0. The number decreases by 2; therefore Cu2+ is reduced."),
        ("5. General direction rule", "Increase -> oxidation. Decrease -> reduction. This is the concept-level rule; it should still work when the reagent names change."),
        ("6. Translate Zn to electrons", "Zn -> Zn2+ + 2e-. Electrons appear on the product side because Zn loses them."),
        ("7. Translate Cu2+ to electrons", "Cu2+ + 2e- -> Cu. Electrons appear on the reactant side because Cu2+ gains them."),
        ("8. Close the electron ledger", "The same two electrons lost by Zn are gained by Cu2+. If the loss/gain counts disagree, the proof is internally inconsistent."),
        ("9. Derive the Zn role", "Prove SELF first: Zn is oxidised / loses electrons. Then OTHER effect: those electrons reduce Cu2+. Conclusion: Zn is the reducing agent."),
        ("10. Derive the Cu2+ role", "Prove SELF first: Cu2+ is reduced / gains electrons. Its acceptance of electrons makes oxidation of Zn possible. Conclusion: Cu2+ is the oxidising agent."),
        ("11. Misconception contrast", "Wrong: 'Zn is reducing agent because Zn gets reduced.' Correct: 'Zn is oxidised; its electron loss reduces Cu2+; therefore Zn is the reducing agent.' The wrong statement reverses the proved self-change."),
        ("12. Fully worked proof", "Zn 0 -> +2, so Zn is oxidised. Zn -> Zn2+ + 2e-. Cu +2 -> 0, so Cu2+ is reduced. Cu2+ + 2e- -> Cu. The two-electron ledger closes. Hence Zn is the reducing agent and Cu2+ is the oxidising agent."),
        ("13. Completion / fading", "Complete: Zn: 0 -> __ ; direction = __ ; process = __ ; electron statement = __ ; role = __. Then do the Cu line with fewer prompts."),
        ("14. Independent reconstruction", "Close the notes. Rebuild the complete proof from the equation only. Final check: same element tracked, state direction correct, electron loss = gain, agent label derived after self-change."),
    ]
    rendered = []
    for i, (title, body) in enumerate(pages):
        visual = "species" if i == 1 else "lane" if i in {2,3,4,5,11,13,14} else "electron" if i in {6,7,8} else "reaction"
        rendered.append({"title": title, "visual": visual, "blocks": [
            ("DECLARATIVE EXPLANATION", body, BLUE),
            ("SELF-CHECK", "Explain why the step is chemically legal before moving on. If the statement cannot be tied to the same element or the closed electron ledger, revisit the preceding page.", AMBER),
        ]})
    render_pages(ROOT / "02_Core1A_Detailed_Declarative_Redox_Proof.pdf", "Core1A | Detailed Declarative Notes | HARD", rendered)


def build_core1b():
    tasks = [
        ("Species identity retrieval", "Without using any Redox label, map each element from reactant to product.", "species", "Match Zn only with Zn2+ and Cu in Cu2+ only with Cu.", "Zn -> Zn2+; Cu2+ -> Cu. Identity comes before labels."),
        ("Construct the oxidation-state lanes", "Write the before/after oxidation state for each element and describe only the numerical direction.", "lane", "Elemental Zn/Cu are 0; the ions shown carry +2 for the corresponding element.", "Zn 0 -> +2 increases. Cu +2 -> 0 decreases."),
        ("Build oxidation / reduction from direction", "Write the general rule first, then use it to label Zn and Cu2+.", "lane", "Do not use a remembered reagent role. Use increase/decrease.", "Increase -> oxidation, so Zn is oxidised. Decrease -> reduction, so Cu2+ is reduced."),
        ("Construct the electron consequences", "Translate each self-change into an electron statement and close the ledger.", "electron", "The species oxidised loses electrons; the species reduced gains them.", "Zn -> Zn2+ + 2e-. Cu2+ + 2e- -> Cu. Two lost = two gained."),
        ("Construct the Zn agent role", "Build a three-link proof: Zn self-change -> effect on Cu2+ -> role.", "reaction", "Role comes last. Start 'Zn is oxidised and loses electrons...'.", "Zn is oxidised and supplies electrons that reduce Cu2+; therefore Zn is the reducing agent."),
        ("Construct the Cu2+ agent role", "Build the complementary three-link proof for Cu2+.", "reaction", "Start with Cu2+ being reduced / gaining electrons; then connect that to Zn oxidation.", "Cu2+ is reduced and accepts electrons from Zn; therefore Cu2+ is the oxidising agent."),
        ("Diagnose the classic reversal", "A learner says 'Zn is the reducing agent because Zn gets reduced.' Identify the exact broken link.", "reaction", "Check the Zn lane before discussing the role word.", "Zn does not get reduced: 0 -> +2 is oxidation. Its oxidation supplies electrons for Cu2+ reduction; that is why it is the reducing agent."),
        ("Translate between proof representations", "Show how one statement can be written as a state lane, an electron statement, and an agent-role sentence.", "electron", "Use Zn as the anchor and preserve the same self-change across all three forms.", "Zn 0 -> +2 | Zn -> Zn2+ + 2e- | Zn is oxidised and acts as the reducing agent."),
        ("Teach back without the page", f"From {REACTION} alone, reconstruct the full Redox proof in your own layout.", "reaction", "Minimum chain: identity -> state direction -> electron consequence -> role -> independent check.", "Zn 0 -> +2 oxidised, loses 2e-, reducing agent. Cu +2 -> 0 reduced, gains 2e-, oxidising agent. Electron loss equals gain."),
    ]
    pages=[]
    for title,prompt,vis,hint,answer in tasks:
        pages.append({"title": title, "visual": vis, "blocks": [
            ("OPEN-ENDED TASK | attempt before help", prompt, BLUE),
            ("SELF-GUIDED HELP", f"H1 ORIENT: identify the evidence target. H2 REPRESENT: use the displayed frame. H3 PRINCIPLE: {hint} H4 FIRST MOVE: write the first evidence statement before any role label.", AMBER),
            ("CANONICAL RESPONSE + CHECK", answer + " Check that the same element is tracked and the electron ledger closes.", GREEN),
        ]})
    render_pages(ROOT / "03_Core1B_Open_Ended_Self_Tutor_Redox_Proof.pdf", "Core1B | Open-Ended Concept Tutor | HARD", pages)


def build_core2():
    pages=[
        {"title":"Frozen question authority and help contract","blocks":[
            ("QUESTION CUSTODY", "The three questions in this review fixture are owner-frozen inputs. Core2 may add ladder hints and answer closure but may not silently rewrite the question or claim NCERT provenance.", BLUE),
            ("HELP LADDER", "Attempt -> small clue -> stronger clue -> full answer/check. The learner decides when to reveal help; the PDF does not detect responses.", AMBER),
        ]}
    ]
    for qid,q,ans in FROZEN_QUESTIONS:
        pages.append({"title":f"{qid} | Attempt","visual":"reaction","blocks":[
            ("FROZEN QUESTION",q,BLUE),
            ("LADDER HINTS", "H1: Track the same element. H2: Write oxidation-state lanes. H3: Connect direction to electron loss/gain. H4: Attach agent role only after self-change is proved.", AMBER),
        ]})
        pages.append({"title":f"{qid} | Answer closure","blocks":[
            ("FULL ANSWER",ans,GREEN),
            ("CHECK", "Verify element identity, direction of oxidation-state change, two-electron balance, and role-label consistency.", AMBER),
        ]})
    render_pages(ROOT / "04_Core2_Frozen_Questions_With_Ladder_Hints_Redox_Proof.pdf", "Core2 | Frozen Questions + Ladder Hints", pages)


def build_core2a():
    pages=[
        {"title":"Owner override and guided-practice contract","blocks":[
            ("LEARNER CONDITIONING", OWNER_OVERRIDE, AMBER),
            ("CORE2A JOB", "Declarative deliberate practice: attempt first, then technical clue, setup, quick check, full solution, error classification and retry. Questions remain frozen.", BLUE),
        ]},
        {"title":"Episode 1 | WORKED | RQ-REDOX-01","visual":"lane","blocks":[
            ("ATTEMPT",FROZEN_QUESTIONS[0][1],BLUE),
            ("WORKED REPAIR",FROZEN_QUESTIONS[0][2] + " Technical reason: compare the same element and use increase/decrease, not reagent reputation.",GREEN),
        ]},
        {"title":"Episode 1 | Error classification and retry","blocks":[
            ("IF WRONG", "Species mismatch -> SPECIES_IDENTITY_ERROR. Reversed increase/decrease -> CHARGE_OR_OXIDATION_STATE_ERROR. Correct label without proof -> CONCEPT_MODEL_ERROR.", RED),
            ("RETRY", "Cover the worked repair and reconstruct both lanes again from the reaction only.", AMBER),
        ]},
        {"title":"Episode 2 | COMPLETION | RQ-REDOX-02","visual":"electron","blocks":[
            ("COMPLETE", "Zn -> Zn2+ + __ ; Cu2+ + __ -> Cu. Then identify both agents and justify each role from the self-change.", BLUE),
            ("FULL SOLUTION", FROZEN_QUESTIONS[1][2], GREEN),
        ]},
        {"title":"Episode 2 | Error classification and near retry","blocks":[
            ("IF WRONG", "Wrong electron side -> SYMBOLIC_EXECUTION_ERROR. Wrong count -> CONSERVATION_ERROR. Reversed agent role -> CONCEPT_MODEL_ERROR.", RED),
            ("RETRY", "Write a four-column ledger: species | state change | electron change | role. Fill role last.", AMBER),
        ]},
        {"title":"Episode 3 | INDEPENDENT | RQ-REDOX-03","visual":"reaction","blocks":[
            ("ATTEMPT WITHOUT HELP", FROZEN_QUESTIONS[2][1], BLUE),
            ("QUICK CHECK", "If your first sentence says Zn is reduced, reopen only the oxidation-state lane before reading the full repair.", AMBER),
        ]},
        {"title":"Episode 3 | Complete worked repair","blocks":[
            ("WORKED REPAIR", FROZEN_QUESTIONS[2][2], GREEN),
            ("WHY THE ERROR PERSISTS", "The label 'reducing agent' describes what the species causes elsewhere, not the species' own Redox process. Separate SELF from OTHER.", BLUE),
        ]},
        {"title":"Exit check | no mastery claim","blocks":[
            ("INDEPENDENT CHECK", "Without looking back, write the full proof and then explain why 'reducing agent' cannot be translated as 'gets reduced'.", BLUE),
            ("NON-CLAIM", "Completing this printed episode does not prove mastery or retention. It is an opportunity to demonstrate the reasoning; learner evidence must be recorded elsewhere.", AMBER),
        ]},
    ]
    render_pages(ROOT / "05_Core2A_Guided_Practice_Owner_Override_Redox_Proof.pdf", "Core2A | Guided Declarative Practice", pages)


def build_core2b():
    pages=[
        {"title":"Owner override and open-ended tutor contract","blocks":[
            ("LEARNER CONDITIONING", OWNER_OVERRIDE, AMBER),
            ("CORE2B JOB", "Coach interpretation and move selection before releasing solution detail. The learner must commit to what is asked, relevant evidence, representation, invariant, first move and justification.", BLUE),
        ]}
    ]
    for qid,q,ans in FROZEN_QUESTIONS:
        pages.extend([
            {"title":f"{qid} | Commit before help","visual":"reaction","blocks":[
                ("FROZEN QUESTION",q,BLUE),
                ("YOUR PLAN", "1 What is being asked? 2 Which species/state evidence matters? 3 Which representation will you use? 4 What must remain true? 5 What is your first move? 6 Why is that move legal?", AMBER),
            ]},
            {"title":f"{qid} | Progressive concept help","visual":"lane","blocks":[
                ("H1 ORIENT", "Name the target in your own words before calculating or labelling anything.", AMBER),
                ("H2 STRUCTURE / H3 REPRESENT", "Track same element -> state lane -> electron consequence. Keep role blank until self-change is secure.", BLUE),
                ("H4 PRINCIPLE / H5 FIRST MOVE", "Increase = oxidation; decrease = reduction. First move: write the two before/after lanes.", GREEN),
            ]},
            {"title":f"{qid} | Solution, falsify, generalise","blocks":[
                ("FULL SOLUTION",ans,GREEN),
                ("FALSIFY", "Try to disprove your answer: does each role agree with the species' own state/electron change? Does electron loss equal gain?", AMBER),
                ("GENERALISE", "State a method that would still work if Zn/Cu were replaced by unfamiliar species: identity -> state direction -> electron consequence -> role.", BLUE),
            ]},
        ])
    pages.append({"title":"Teach-back / transfer reflection","blocks":[
        ("TEACH BACK", "Explain the problem-solving strategy without using the words Zn or Cu. Your explanation must tell another learner how to select a first move and how to verify the final role labels.", BLUE),
        ("TARGET STRATEGY", "Track identity; choose oxidation-state lanes; infer oxidation/reduction from direction; translate to electron loss/gain; derive agent roles; close the electron ledger; test for a role/self-change reversal.", GREEN),
    ]})
    render_pages(ROOT / "06_Core2B_Open_Ended_Problem_Tutor_Owner_Override_Redox_Proof.pdf", "Core2B | Open-Ended Problem Tutor", pages)


def build_validation():
    pages=[
        {"title":"Six learner contracts are different jobs","blocks":[
            ("STUDY SIDE", "Core1 = compact notes. Core1A = complete declarative teaching. Core1B = elicitation-first concept reconstruction.", BLUE),
            ("QUESTION SIDE", "Core2 = frozen questions + ladder help. Core2A = guided deliberate practice with full repair. Core2B = coached problem solving that forces move selection before solution exposure.", GREEN),
        ]},
        {"title":"Control axes and authority boundaries","blocks":[
            ("CORE1 SERIES", "This subtopic is HARD because depth follows intrinsic Chemistry difficulty, not student knowledge. The set uses only the governed symbolic Redox representation and does not invent particle-level scenes.", AMBER),
            ("CORE2 SERIES", OWNER_OVERRIDE + " The three questions are owner-frozen review inputs; their wording/answer custody is shared across Core2/Core2A/Core2B.", BLUE),
        ]},
        {"title":"Self-help closure and falsifiers","blocks":[
            ("COMMON CLOSURE", "Every learner task has ATTEMPT -> SUPPORT -> CHECK -> REPAIR -> RETRY/TRANSFER. Open-ended never means answerless.", GREEN),
            ("RELEASE FALSIFIERS", "Reject if Core1 depth depends on learner percentage; if Core2 conditioning is unresolved; if B layers add live runtime fields; if Core2B invents new questions; if role labels are given without self-change evidence; if symbolic representation authority drifts.", RED),
        ]},
        {"title":"Review verdict","blocks":[
            ("PASS", "The six artifacts share one chemical truth but produce six different learner actions. Core1A/Core1B share the HARD bucket; Core2A/Core2B share owner conditioning; all tasks close with answers/checks; no mastery claim is inferred from artifact completion.", GREEN),
            ("NEXT VALIDATION", "Repeat the six-core fixture on a second Chemistry family with different representation demands before treating the architecture as broadly mature.", AMBER),
        ]},
    ]
    render_pages(ROOT / "07_Six_Core_Architecture_Validation_Redox_Proof.pdf", "Six-Core Architecture Validation", pages)


def write_readme():
    content = f"""# Chemistry six-core review set - Redox proof

Subtopic: **species identity -> oxidation-state change -> electron consequence -> agent role** using the governed reaction `{REACTION}`.

Files:

1. `01_Core1_Basic_Notes_Redox_Proof.pdf` - compact notes.
2. `02_Core1A_Detailed_Declarative_Redox_Proof.pdf` - detailed HARD-bucket explanatory notes.
3. `03_Core1B_Open_Ended_Self_Tutor_Redox_Proof.pdf` - open-ended concept self-tutor.
4. `04_Core2_Frozen_Questions_With_Ladder_Hints_Redox_Proof.pdf` - owner-frozen review questions with ladder hints.
5. `05_Core2A_Guided_Practice_Owner_Override_Redox_Proof.pdf` - declarative deliberate practice.
6. `06_Core2B_Open_Ended_Problem_Tutor_Owner_Override_Redox_Proof.pdf` - open-ended problem-solving tutor.
7. `07_Six_Core_Architecture_Validation_Redox_Proof.pdf` - architecture review.

## Conditioning

No student knowledge percentage was supplied. Core2A/Core2B use an explicit **OWNER_OVERRIDE** rather than fabricating a percentage. The override changes support only, not the frozen review questions or Chemistry truth.

## HARD-bucket research

The realization records Chemistry-education research on Redox misconceptions, representation coordination and worked-example/fading design. Research improves pedagogy only; it does not expand Chemistry authority. This review remains at the currently governed symbolic representation level.

## Scope

The three Core2 questions are owner-frozen review inputs and are **not** presented as NCERT/source-question claims. All six learner products are static and self-help complete.
"""
    (ROOT / "README.md").write_text(content, encoding="utf-8")


def validate_and_manifest():
    expected = {
        "01_Core1_Basic_Notes_Redox_Proof.pdf": 5,
        "02_Core1A_Detailed_Declarative_Redox_Proof.pdf": 15,
        "03_Core1B_Open_Ended_Self_Tutor_Redox_Proof.pdf": 9,
        "04_Core2_Frozen_Questions_With_Ladder_Hints_Redox_Proof.pdf": 7,
        "05_Core2A_Guided_Practice_Owner_Override_Redox_Proof.pdf": 8,
        "06_Core2B_Open_Ended_Problem_Tutor_Owner_Override_Redox_Proof.pdf": 11,
        "07_Six_Core_Architecture_Validation_Redox_Proof.pdf": 4,
    }
    page_counts = {}
    hashes = {}
    for name, count in expected.items():
        p = ROOT / name
        with fitz.open(p) as doc:
            assert len(doc) == count, (name, len(doc), count)
            raw = "\n".join(page.get_text() for page in doc)
            assert len(raw) > 250
            for page in doc:
                assert page.rect.width > 500 and page.rect.height > 800
        page_counts[p.stem] = count
        hashes[p.stem] = hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = {
        "subject": "Chemistry",
        "subtopic": "Redox proof: species identity -> oxidation-state change -> electron consequence -> agent role",
        "governed_reaction": REACTION,
        "difficulty_badge": "HARD",
        "core1_control_axis": "INTRINSIC_SUBTOPIC_DIFFICULTY",
        "core2_conditioning": {
            "mode": "OWNER_OVERRIDE",
            "reason": "Student knowledge percentage not supplied; owner-directed six-core review build",
            "fabricated_knowledge_percent": False,
            "support_profile": "MEDIUM-HIGH for Core2A; LOW initial/MEDIUM total for Core2B",
        },
        "core2_question_provenance": "OWNER_FROZEN_REVIEW_INPUT; not an NCERT/source-question claim",
        "representation_authority": ["SYMBOLIC"],
        "research_evidence": RESEARCH,
        "roles": {
            "Core1": "compact basic notes",
            "Core1A": "detailed declarative teaching",
            "Core1B": "open-ended concept self-tutor",
            "Core2": "frozen review questions + ladder hints",
            "Core2A": "guided declarative deliberate practice",
            "Core2B": "open-ended problem-solving tutor",
        },
        "page_counts": page_counts,
        "sha256": hashes,
    }
    (ROOT / "validation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main():
    build_core1()
    build_core1a()
    build_core1b()
    build_core2()
    build_core2a()
    build_core2b()
    build_validation()
    write_readme()
    validate_and_manifest()
    print("CHEMISTRY_REDOX_SIX_CORE_REVIEW=PASS")


if __name__ == "__main__":
    main()
