from __future__ import annotations
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from pypdf import PdfReader

W,H=A4; M=28
NAVY=colors.HexColor('#17324D'); INK=colors.HexColor('#20262D'); MUTED=colors.HexColor('#65717C')
LINE=colors.HexColor('#CBD4DA'); BLUE=colors.HexColor('#EEF5FA'); GREEN=colors.HexColor('#EDF7EF')
AMBER=colors.HexColor('#FFF4D6'); RED=colors.HexColor('#FCEAEA'); GRAY=colors.HexColor('#F4F6F7')
TEAL=colors.HexColor('#E8F6F3'); WHITE=colors.white

def wrap(text,font='Helvetica',size=8.5,width=500):
    lines=[]
    for para in str(text).split('\n'):
        words=para.split(); cur=''
        for w in words:
            t=w if not cur else cur+' '+w
            if stringWidth(t,font,size)<=width: cur=t
            else:
                if cur: lines.append(cur)
                cur=w
        if cur: lines.append(cur)
        if not words: lines.append('')
    return lines

def draw_badges(c,badges):
    x=M; y=H-62
    for b in badges[:6]:
        w=stringWidth(b,'Helvetica-Bold',6.7)+14
        c.setFillColor(BLUE); c.setStrokeColor(LINE); c.roundRect(x,y-13,w,15,7,fill=1,stroke=1)
        c.setFillColor(NAVY); c.setFont('Helvetica-Bold',6.7); c.drawString(x+7,y-8,b); x+=w+5

def draw_table_like(c,x,y,w,h,text,fill=GRAY):
    c.setFillColor(fill); c.setStrokeColor(LINE); c.roundRect(x,y-h,w,h,6,fill=1,stroke=1)
    raw_rows=[r.strip() for r in text.split(';') if r.strip()]
    rows=[[cell.strip() for cell in r.split('|')] for r in raw_rows]
    cols=max(len(r) for r in rows) if rows else 1
    for r in rows: r += ['']*(cols-len(r))
    rh=h/max(1,len(rows)); cw=w/cols
    for ri,row in enumerate(rows):
        top=y-ri*rh
        if ri: c.line(x,top,x+w,top)
        for ci,cell in enumerate(row):
            if ci: c.line(x+ci*cw,top-rh,x+ci*cw,top)
            yy=top-12
            for line in wrap(cell,'Helvetica',7.4,cw-10)[:max(1,int((rh-10)/9))]:
                c.setFillColor(INK); c.setFont('Helvetica',7.4); c.drawString(x+ci*cw+5,yy,line); yy-=9

def draw_event(c,x,y,w,h,text):
    c.setStrokeColor(NAVY); c.setFillColor(TEAL); c.roundRect(x,y-h,w,h,6,fill=1,stroke=1)
    items=[p.strip() for p in re.split(r'->|;',text) if p.strip()]; n=max(1,len(items)); gap=w/n; cy=y-h/2
    for i,item in enumerate(items):
        cx=x+gap*(i+.5); c.setFillColor(WHITE); c.setStrokeColor(NAVY); c.circle(cx,cy,13,fill=1,stroke=1)
        c.setFillColor(INK); c.setFont('Helvetica',6.5); lines=wrap(item,'Helvetica',6.5,gap-8)[:3]; yy=cy-25
        for line in lines: c.drawCentredString(cx,yy,line); yy-=8
        if i<n-1: c.setStrokeColor(NAVY); c.line(cx+14,cy,x+gap*(i+1.5)-14,cy)

def render_product(mode,pages,outdir):
    path=outdir/f'{mode.lower()}_observation_evidence_inference.pdf'; c=canvas.Canvas(str(path),pagesize=A4)
    realization_ids=set(); page_audits=[]; usable=(W-2*M)*(H-105)
    for idx,p in enumerate(pages,1):
        c.setFillColor(NAVY); c.rect(0,H-52,W,52,fill=1,stroke=0); c.setFillColor(WHITE); c.setFont('Helvetica-Bold',14); c.drawString(M,H-25,f'{mode} - {p["title"]}')
        c.setFont('Helvetica',7.5); c.drawString(M,H-39,'Chemistry | Observation -> evidence -> inference'); draw_badges(c,p['badges'])
        y=H-88; tech_area=0; objects=0
        for block in p['blocks']:
            kind=block['kind']; text=block['text']; realization_ids.update(block.get('asset_ids',[])); objects+=1
            if kind=='TABLE': bh=78
            elif kind=='TTU': bh=150 if p['workspace'] else 82
            elif kind=='DIAGRAM': bh=90
            elif kind=='QUESTION': bh=78 if len(text)<170 else 110
            elif kind=='SOURCE': bh=28
            else: bh=max(44,min(100,20+len(wrap(text,'Helvetica',8.2,W-2*M-20))*10))
            if y-bh<42: raise RuntimeError(f'PAGE_MODEL_OVERFLOW:{mode}:{p["page_id"]}:{kind}')
            x=M; bw=W-2*M
            fill={'TTU':AMBER,'QUESTION':BLUE,'SOURCE':GRAY,'CANONICAL':GREEN,'SOLUTION':GREEN,'HELP':TEAL,'TRAP':RED,'VERIFY':TEAL,'PROMPT':AMBER}.get(kind,WHITE)
            if kind=='TABLE': draw_table_like(c,x,y,bw,bh,text,GRAY)
            elif kind=='TTU': draw_table_like(c,x,y,bw,bh,text,AMBER)
            elif kind=='DIAGRAM': draw_event(c,x,y,bw,bh,text)
            else:
                c.setFillColor(fill); c.setStrokeColor(LINE); c.roundRect(x,y-bh,bw,bh,6,fill=1,stroke=1)
                c.setFillColor(NAVY); c.setFont('Helvetica-Bold',7); c.drawString(x+8,y-14,kind)
                c.setFillColor(INK); c.setFont('Helvetica',8.2); yy=y-28
                for line in wrap(text,'Helvetica',8.2,bw-16):
                    if yy<y-bh+8: break
                    c.drawString(x+8,yy,line); yy-=10
            tech_area+=bw*bh; y-=bh+8
        frac=min(1.0,tech_area/usable)
        page_audits.append({'page_id':p['page_id'],'technical_object_count':objects,'technical_area_fraction':round(frac,3),'workspace':p['workspace'],'ttu_ids':p['ttu_ids']})
        c.setStrokeColor(LINE); c.line(M,26,W-M,26); c.setFillColor(MUTED); c.setFont('Helvetica',6.5); c.drawString(M,14,'v7 PAL-assured validation product'); c.drawRightString(W-M,14,f'{mode} | {idx}'); c.showPage()
    c.save(); return path, realization_ids, page_audits

def preflight_pdf(path):
    r=PdfReader(str(path)); assert len(r.pages)>=1
    for i,p in enumerate(r.pages,1):
        text=(p.extract_text() or '').strip()
        if len(text)<120: raise RuntimeError(f'PDF_TEXT_TOO_THIN:{path.name}:{i}:{len(text)}')
    return len(r.pages)
