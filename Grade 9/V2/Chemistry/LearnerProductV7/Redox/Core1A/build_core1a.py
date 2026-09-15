#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
BP = ROOT / "Grade 9" / "V2" / "Chemistry" / "LearningBlueprint"
sys.path.insert(0, str(BP / "engine"))

from compile_chemistry_engineering_closure import digest, load  # noqa: E402
from compile_chemistry_product_engineering_custody import compile_product_custody  # noqa: E402
from validate_pal_engineering_ready import validate_pal_engineering_ready  # noqa: E402

AUTHORITY_REL = "golden/v7/core1a-study-note-redox-authority.json"
CCBOM_REL = "golden/v7/ccbom-redox.json"
TTU_REL = "golden/v5/core1a-hard-study-product.json"
SDU_REL = "golden/v6/sdu-hard-redox.json"
CONCEPT_TTU_REL = "golden/v6/concept-ttu-core1a-redox.json"
SELF_HELP_REL = "golden/v6/self-help-core1a-redox.json"
REQUEST_REL = "fixtures/engineering-workbench/redox-request.v1.json"
MANIFEST_REL = "fixtures/engineering-workbench/redox-manifest.v1.json"
SOURCE_SCOPE_REL = "fixtures/engineering-workbench/redox-product-source-scope.v1.json"
SOURCE_AUDIT_REL = "policies/chemistry-redox-source-audit.v1.json"
STUDY_POLICY_REL = "policies/v7-core1a-study-note-sufficiency-policy.json"

FONT = "DejaVuSans"
FONT_BOLD = "DejaVuSans-Bold"

INK = colors.HexColor("#20252B")
MUTED = colors.HexColor("#606A73")
LINE = colors.HexColor("#CBD2D8")
PANEL = colors.HexColor("#F4F6F7")
PANEL_2 = colors.HexColor("#EAEFF2")
ACCENT = colors.HexColor("#234E52")
ACCENT_LIGHT = colors.HexColor("#E8F1F1")
WARN = colors.HexColor("#6B3D2E")
WARN_BG = colors.HexColor("#F7ECE8")
PRACTICE_BG = colors.HexColor("#F3F1E8")
ANSWER_BG = colors.HexColor("#EEF2EC")


def register_fonts():
    regular = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont(FONT, str(regular)))
        pdfmetrics.registerFont(TTFont(FONT_BOLD, str(bold)))
    else:
        raise RuntimeError("DejaVu Sans fonts are required for Chemistry notation")


def jload(rel: str) -> dict:
    return json.loads((BP / rel).read_text(encoding="utf-8"))


def sha(obj: dict) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def ptxt(value) -> str:
    return escape(str(value)).replace("\n", "<br/>")


def make_styles():
    ss = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=ss["Title"], fontName=FONT_BOLD, fontSize=22, leading=26, textColor=INK, alignment=TA_LEFT, spaceAfter=5*mm),
        "subtitle": ParagraphStyle("subtitle", parent=ss["BodyText"], fontName=FONT, fontSize=10.5, leading=14, textColor=MUTED, spaceAfter=4*mm),
        "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontName=FONT_BOLD, fontSize=16, leading=20, textColor=ACCENT, spaceBefore=4*mm, spaceAfter=2.5*mm),
        "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontName=FONT_BOLD, fontSize=11.3, leading=14, textColor=INK, spaceBefore=2.5*mm, spaceAfter=1.3*mm),
        "body": ParagraphStyle("body", parent=ss["BodyText"], fontName=FONT, fontSize=9.4, leading=13.1, textColor=INK, spaceAfter=1.6*mm),
        "small": ParagraphStyle("small", parent=ss["BodyText"], fontName=FONT, fontSize=7.3, leading=9.5, textColor=MUTED),
        "eq": ParagraphStyle("eq", parent=ss["BodyText"], fontName=FONT_BOLD, fontSize=13.5, leading=17, textColor=INK, alignment=TA_CENTER),
        "practice": ParagraphStyle("practice", parent=ss["BodyText"], fontName=FONT, fontSize=9.2, leading=13, textColor=INK),
        "answer": ParagraphStyle("answer", parent=ss["BodyText"], fontName=FONT, fontSize=8.8, leading=12.2, textColor=INK),
        "badge": ParagraphStyle("badge", parent=ss["BodyText"], fontName=FONT_BOLD, fontSize=7.1, leading=8.5, textColor=ACCENT),
    }


class EquationBox(Flowable):
    def __init__(self, text: str, width=168*mm, height=18*mm):
        super().__init__(); self.text=text; self.width=width; self.height=height
    def draw(self):
        c=self.canv; c.saveState(); c.setStrokeColor(LINE); c.setFillColor(PANEL); c.roundRect(0,0,self.width,self.height,3*mm,stroke=1,fill=1)
        c.setFont(FONT_BOLD, 14); c.setFillColor(INK); c.drawCentredString(self.width/2, self.height/2-5, self.text); c.restoreState()


class StateLane(Flowable):
    def __init__(self, lane_map: dict, incomplete: bool=False, width=168*mm, height=34*mm):
        super().__init__(); self.lane_map=lane_map; self.incomplete=incomplete; self.width=width; self.height=height
    def draw(self):
        c=self.canv; c.saveState(); c.setStrokeColor(LINE); c.setFillColor(colors.white); c.roundRect(0,0,self.width,self.height,3*mm,stroke=1,fill=1)
        rows=list(self.lane_map.items()); y=self.height-11*mm
        for label, text in rows:
            c.setFont(FONT_BOLD,9); c.setFillColor(ACCENT); c.drawString(6*mm,y,label)
            c.setFont(FONT,10); c.setFillColor(INK); c.drawString(26*mm,y,text)
            y-=13*mm
        c.restoreState()


class ChainMap(Flowable):
    def __init__(self, rows: dict, width=168*mm, height=40*mm):
        super().__init__(); self.rows=rows; self.width=width; self.height=height
    def draw(self):
        c=self.canv; c.saveState(); c.setStrokeColor(LINE); c.setFillColor(PANEL); c.roundRect(0,0,self.width,self.height,3*mm,stroke=1,fill=1)
        y=self.height-12*mm
        for label, value in self.rows.items():
            c.setFillColor(ACCENT); c.setFont(FONT_BOLD,9); c.drawString(6*mm,y,label)
            c.setFillColor(INK); c.setFont(FONT,9.5); c.drawString(27*mm,y,value)
            y-=13*mm
        c.restoreState()


class BlankTTU(Flowable):
    def __init__(self, ttu: dict, width=168*mm, height=58*mm):
        super().__init__(); self.ttu=ttu; self.width=width; self.height=height
    def draw(self):
        c=self.canv; c.saveState(); c.setStrokeColor(ACCENT); c.setLineWidth(1.1); c.setFillColor(colors.white); c.roundRect(0,0,self.width,self.height,3*mm,stroke=1,fill=1)
        c.setFillColor(ACCENT); c.setFont(FONT_BOLD,9); c.drawString(5*mm,self.height-8*mm,"Reconstruct it")
        c.setFillColor(INK); c.setFont(FONT,8.5)
        action=self.ttu.get("learner_action","")
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words=action.split(); lines=[]; cur=""
        maxw=self.width-10*mm
        for w in words:
            test=(cur+" "+w).strip()
            if stringWidth(test,FONT,8.5)>maxw and cur:
                lines.append(cur); cur=w
            else: cur=test
        if cur: lines.append(cur)
        y=self.height-14*mm
        for line in lines[:3]: c.drawString(5*mm,y,line); y-=4.5*mm
        initial=self.ttu.get("initial_state",{})
        y-=2*mm; c.setFont(FONT_BOLD,9)
        for key,val in initial.items():
            if isinstance(val,list): val=" | ".join(val)
            c.setFont(FONT_BOLD,8.3); c.drawString(5*mm,y,key.replace("_"," ").title()+":")
            c.setFont(FONT,8.3); c.drawString(40*mm,y,str(val))
            y-=6*mm
        c.restoreState()


class HintBox(Flowable):
    def __init__(self, hints: list[dict], width=168*mm):
        super().__init__(); self.hints=hints; self.width=width; self.height=max(15*mm, (len(hints)*11+8)*mm/3)
    def draw(self):
        c=self.canv; c.saveState(); c.setFillColor(ACCENT_LIGHT); c.setStrokeColor(LINE); c.roundRect(0,0,self.width,self.height,2*mm,stroke=1,fill=1)
        y=self.height-6*mm
        for i,h in enumerate(self.hints,1):
            c.setFillColor(ACCENT); c.setFont(FONT_BOLD,7.5); c.drawString(4*mm,y,f"Hint {i}")
            c.setFillColor(INK); c.setFont(FONT,7.5); c.drawString(20*mm,y,h.get("hint_text","")[:120]); y-=5.5*mm
        c.restoreState()


def box_table(title: str, body_flowables, styles, bg=PANEL, border=LINE):
    rows=[[Paragraph(ptxt(title),styles["h2"])],[body_flowables if isinstance(body_flowables,Flowable) else body_flowables]]
    t=Table(rows,colWidths=[168*mm],hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),("BOX",(0,0),(-1,-1),0.8,border),
        ("LEFTPADDING",(0,0),(-1,-1),5*mm),("RIGHTPADDING",(0,0),(-1,-1),5*mm),
        ("TOPPADDING",(0,0),(-1,-1),3*mm),("BOTTOMPADDING",(0,0),(-1,-1),3*mm),
    ]))
    return t


def bullets(items, styles):
    out=[]
    for item in items:
        out.append(Paragraph("• "+ptxt(item), styles["body"]))
    return out


def flatten_payload(payload, styles):
    if isinstance(payload,str): return [Paragraph(ptxt(payload),styles["body"])]
    if isinstance(payload,list): return bullets(payload,styles)
    if isinstance(payload,dict):
        rows=[]
        for k,v in payload.items():
            if isinstance(v,list): v="; ".join(str(x) for x in v)
            rows.append([Paragraph("<b>"+ptxt(k.replace("_"," ").title())+"</b>",styles["body"]),Paragraph(ptxt(v),styles["body"])])
        t=Table(rows,colWidths=[38*mm,124*mm],hAlign="LEFT")
        t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("GRID",(0,0),(-1,-1),0.4,LINE),("BACKGROUND",(0,0),(0,-1),PANEL_2),("LEFTPADDING",(0,0),(-1,-1),2.5*mm),("RIGHTPADDING",(0,0),(-1,-1),2.5*mm),("TOPPADDING",(0,0),(-1,-1),1.8*mm),("BOTTOMPADDING",(0,0),(-1,-1),1.8*mm)]))
        return [t]
    return [Paragraph(ptxt(payload),styles["body"])]


def render_object(obj: dict, styles, answers: list, realized: set):
    realized.add(obj["object_id"])
    cls=obj["object_class"]; payload=obj["learner_payload"]
    if cls=="ANSWER":
        answers.append(obj); return []
    if cls=="EQUATION": return [EquationBox(str(payload)),Spacer(1,2*mm)]
    if cls=="REPRESENTATION":
        rtype=obj.get("representation_type")
        if rtype=="OXIDATION_STATE_LANE" and isinstance(payload,dict): return [StateLane(payload),Spacer(1,2*mm)]
        if rtype in {"SELF_OTHER_AGENT_MAP","ELECTRON_LEDGER","SPECIES_IDENTITY_MAP"} and isinstance(payload,dict): return [ChainMap(payload),Spacer(1,2*mm)]
        return flatten_payload(payload,styles)+[Spacer(1,1.5*mm)]
    if cls=="MISCONCEPTION_REPAIR" and isinstance(payload,dict):
        rows=[
            [Paragraph("Common wrong move",styles["h2"]),Paragraph(ptxt(payload.get("wrong_model","")),styles["body"])],
            [Paragraph("Repair",styles["h2"]),Paragraph(ptxt(payload.get("repair","")),styles["body"])],
        ]
        t=Table(rows,colWidths=[38*mm,124*mm],hAlign="LEFT")
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),WARN_BG),("BOX",(0,0),(-1,-1),0.7,WARN),("INNERGRID",(0,0),(-1,-1),0.35,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),3*mm),("RIGHTPADDING",(0,0),(-1,-1),3*mm),("TOPPADDING",(0,0),(-1,-1),2.2*mm),("BOTTOMPADDING",(0,0),(-1,-1),2.2*mm)]))
        return [t,Spacer(1,2*mm)]
    if cls in {"GUIDED_PRACTICE","INDEPENDENT_PRACTICE"}:
        content=flatten_payload(payload,styles)
        if obj.get("learner_source_display"):
            content.append(Spacer(1,1*mm)); content.append(Paragraph(ptxt(obj["learner_source_display"]),styles["small"]))
        return [box_table("Try it",content,styles,bg=PRACTICE_BG),Spacer(1,2.5*mm)]
    label={"MEANING":"Meaning","RULE":"Rule","REASONING_CHAIN":"How to reason","WORKED_EXAMPLE":"Worked example","VERIFICATION":"Check"}.get(cls,cls.replace("_"," ").title())
    content=flatten_payload(payload,styles)
    if cls=="WORKED_EXAMPLE": return [box_table(label,content,styles,bg=ACCENT_LIGHT),Spacer(1,2*mm)]
    if cls=="VERIFICATION": return [box_table(label,content,styles,bg=ANSWER_BG),Spacer(1,2*mm)]
    return [Paragraph(label,styles["h2"]),*content]


def page_header_footer(canvas, doc, title):
    canvas.saveState(); w,h=A4
    canvas.setStrokeColor(LINE); canvas.line(18*mm,13*mm,w-18*mm,13*mm)
    canvas.setFont(FONT,7); canvas.setFillColor(MUTED); canvas.drawString(18*mm,8*mm,"Chemistry • Core1A • Redox")
    canvas.drawRightString(w-18*mm,8*mm,f"{doc.page}")
    canvas.restoreState()


def build(out_pdf: Path, out_manifest: Path):
    register_fonts(); styles=make_styles()
    authority=jload(AUTHORITY_REL); ccbom=jload(CCBOM_REL); ttu_doc=jload(TTU_REL); sdu=jload(SDU_REL); concept_ttu=jload(CONCEPT_TTU_REL); self_help=jload(SELF_HELP_REL); request=jload(REQUEST_REL); manifest=jload(MANIFEST_REL); scope=jload(SOURCE_SCOPE_REL); source_audit=jload(SOURCE_AUDIT_REL); study_policy=jload(STUDY_POLICY_REL)

    custody=compile_product_custody(request,manifest,ccbom,scope,authority)
    pal=validate_pal_engineering_ready(request,manifest,ccbom,scope,authority,custody)

    ttu_map={x["ttu_id"]:x for x in ttu_doc.get("reconstructable_ttus",[])}
    required_ttu_ids=authority["reconstructable_ttu_refs"]
    missing=[x for x in required_ttu_ids if x not in ttu_map]
    if missing: raise RuntimeError(f"Missing reconstructable TTU definitions: {missing}")

    out_pdf.parent.mkdir(parents=True,exist_ok=True)
    doc=BaseDocTemplate(str(out_pdf),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=17*mm,title="Core1A Redox Study Notes",author="Blueprint-derived Chemistry learner product")
    frame=Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id="main")
    doc.addPageTemplates([PageTemplate(id="page",frames=[frame],onPage=lambda c,d: page_header_footer(c,d,authority["subtopic_title"]))])

    story=[]; realized=set(); realized_ttus=[]; answers=[]; question_ids=[]; source_labels=[]
    story.append(Paragraph("Redox Reactions",styles["title"]))
    story.append(Paragraph(ptxt(authority["subtopic_title"]),styles["subtitle"]))
    badges=[f"Core1A",f"Difficulty: {authority['difficulty_badge']}",f"Grade {scope['learner_grade']} competitive foundation",f"Scope: {', '.join(scope['authorized_scope_tiers'])}"]
    badge_table=Table([[Paragraph(ptxt(x),styles["badge"]) for x in badges]],colWidths=[42*mm]*4)
    badge_table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),ACCENT_LIGHT),("BOX",(0,0),(-1,-1),0.6,LINE),("INNERGRID",(0,0),(-1,-1),0.3,LINE),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),2*mm),("RIGHTPADDING",(0,0),(-1,-1),2*mm),("TOPPADDING",(0,0),(-1,-1),2*mm),("BOTTOMPADDING",(0,0),(-1,-1),2*mm)]))
    story += [badge_table,Spacer(1,4*mm)]

    story.append(Paragraph("Study route",styles["h1"]))
    route=[]
    for i,atom in enumerate(authority["learning_atoms"],1):
        route.append([Paragraph(f"{i}",styles["h2"]),Paragraph(ptxt(atom["learner_title"]),styles["body"])])
    rt=Table(route,colWidths=[12*mm,150*mm],hAlign="LEFT")
    rt.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-2),0.35,LINE),("BACKGROUND",(0,0),(0,-1),PANEL_2),("LEFTPADDING",(0,0),(-1,-1),3*mm),("RIGHTPADDING",(0,0),(-1,-1),3*mm),("TOPPADDING",(0,0),(-1,-1),2.2*mm),("BOTTOMPADDING",(0,0),(-1,-1),2.2*mm)]))
    story += [rt,Spacer(1,3*mm),Paragraph("The route is fixed: track the same species, compare oxidation state, connect the change to electrons, then attach the agent role.",styles["body"]),Spacer(1,3*mm)]

    objects_by_atom={a["atom_id"]:[] for a in authority["learning_atoms"]}
    for obj in authority["content_objects"]: objects_by_atom[obj["learning_atom_id"]].append(obj)
    order={"MEANING":1,"RULE":2,"EQUATION":3,"REPRESENTATION":4,"REASONING_CHAIN":5,"WORKED_EXAMPLE":6,"MISCONCEPTION_REPAIR":7,"VERIFICATION":8,"GUIDED_PRACTICE":9,"INDEPENDENT_PRACTICE":10,"ANSWER":99}

    ttu_by_owner={t["owner_id"]:t for t in ttu_map.values() if t["ttu_id"] in required_ttu_ids}
    owner_alias={"LA-OS-TRACK":"LA-REDOX-STATE-CHANGE-002","LA-AGENT-ROLE":"LA-REDOX-AGENT-003"}
    ttu_by_atom={owner_alias.get(k,k):v for k,v in ttu_by_owner.items()}

    for idx,atom in enumerate(authority["learning_atoms"],1):
        story.append(CondPageBreak(65*mm))
        story.append(Paragraph(f"{idx}. {ptxt(atom['learner_title'])}",styles["h1"]))
        atom_objs=sorted(objects_by_atom[atom["atom_id"]],key=lambda o:(order.get(o["object_class"],50),o["object_id"]))
        for obj in atom_objs:
            story.extend(render_object(obj,styles,answers,realized))
            if obj.get("question_id"): question_ids.append(obj["question_id"])
            if obj.get("learner_source_display"): source_labels.append(obj["learner_source_display"])
        if atom["atom_id"] in ttu_by_atom:
            ttu=ttu_by_atom[atom["atom_id"]]; realized_ttus.append(ttu["ttu_id"])
            story.append(Paragraph("Reconstruct the model",styles["h2"]))
            story.append(BlankTTU(ttu)); story.append(Spacer(1,2*mm)); story.append(HintBox(ttu.get("hint_ladder",[]))); story.append(Spacer(1,2*mm))
            canonical=ttu.get("canonical_complete_state",{})
            story.append(box_table("Check your reconstruction",flatten_payload(canonical,styles),styles,bg=ANSWER_BG)); story.append(Spacer(1,2*mm))
            story.append(Paragraph("Verification: "+ptxt(ttu.get("verification_rule","")),styles["body"]))

    # Do not force a new page for answers. Content-first pagination lets the section
    # use remaining space and creates a new page only when the actual content requires it.
    story.append(Paragraph("Answers and checks",styles["h1"]))
    answer_map={a["object_id"]:a for a in answers}
    for practice_id in authority["practice_progression"]["answer_object_ids"]:
        ans=answer_map[practice_id]
        realized.add(ans["object_id"])
        story.append(box_table(practice_id.replace("OBJ-","").replace("-ANS","").replace("-"," ").title(),flatten_payload(ans["learner_payload"],styles),styles,bg=ANSWER_BG))
        story.append(Spacer(1,2*mm))
    story.append(Paragraph("Independent verification",styles["h2"]))
    story += bullets([concept_ttu["canonical_expert_state"]["verification"]["electron_balance"],concept_ttu["canonical_expert_state"]["verification"]["role_check"]],styles)
    story.append(Spacer(1,2*mm))
    story.append(Paragraph("Source note",styles["h2"]))
    story.append(Paragraph(ptxt(authority["scope_statement"]),styles["small"]))

    doc.build(story)

    required_ids={o["object_id"] for o in authority["content_objects"]}
    unresolved=sorted(required_ids-realized)
    if unresolved: raise RuntimeError(f"Unrealized content objects: {unresolved}")
    if sorted(realized_ttus)!=sorted(required_ttu_ids): raise RuntimeError("TTU realization mismatch")

    build_manifest={
        "schema_version":"1.0.0",
        "product":"CORE1A",
        "subtopic_id":authority["subtopic_id"],
        "authority_id":authority["authority_id"],
        "authority_digest":sha(authority),
        "ccbom_id":ccbom["ccbom_id"],
        "ccbom_digest":sha(ccbom),
        "sdu_digest":sha(sdu),
        "concept_ttu_id":concept_ttu["ttu_id"],
        "concept_ttu_digest":sha(concept_ttu),
        "self_help_closure_id":self_help["closure_id"],
        "source_scope_contract_id":scope["scope_contract_id"],
        "source_scope_digest":sha(scope),
        "source_audit_id":source_audit["audit_id"],
        "source_audit_digest":sha(source_audit),
        "study_policy_id":study_policy["policy_id"],
        "engineering_custody":custody,
        "pal_validation":pal,
        "realized_content_object_ids":sorted(realized),
        "realized_ttu_ids":sorted(realized_ttus),
        "practice_question_ids":question_ids,
        "practice_source_labels":source_labels,
        "forbidden_internal_terms":authority["learner_surface_policy"]["forbidden_internal_terms"],
        "held_scope_tiers":scope["held_scope_tiers"],
        "held_detection_tokens":[x for guard in scope["held_transformation_guards"] for x in guard["detection_tokens"]],
    }
    out_manifest.write_text(json.dumps(build_manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")


def main():
    p=argparse.ArgumentParser(); p.add_argument("--out",default=str(HERE/"out/core1a_redox_blueprint_proof.pdf")); p.add_argument("--manifest",default=str(HERE/"out/core1a_redox_blueprint_proof.manifest.json")); a=p.parse_args()
    build(Path(a.out),Path(a.manifest)); print(a.out)


if __name__=="__main__": main()
