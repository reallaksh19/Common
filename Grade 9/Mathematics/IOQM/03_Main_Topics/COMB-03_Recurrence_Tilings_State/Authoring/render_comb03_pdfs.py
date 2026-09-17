from fpdf import FPDF
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / 'PDFs'
PDF_DIR.mkdir(exist_ok=True)


def clean(s):
    s = re.sub(r'`([^`]*)`', r'\1', s).replace('**', '')
    for a, b in [('–','-'),('—','-'),('→','->'),('×','x'),('√','sqrt'),('≤','<='),('≥','>='),('•','-')]:
        s = s.replace(a, b)
    return s.encode('latin-1', 'replace').decode('latin-1')


def add_markdown(pdf, path):
    for raw in path.read_text().splitlines():
        pdf.set_x(pdf.l_margin)
        line = clean(raw.strip())
        if not line:
            pdf.ln(1.5)
        elif line.startswith('# '):
            pdf.ln(3); pdf.set_font('Helvetica','B',14); pdf.multi_cell(0,7,line[2:]); pdf.set_font('Helvetica','',8.4)
        elif line.startswith('## '):
            pdf.ln(2); pdf.set_font('Helvetica','B',11); pdf.multi_cell(0,6,line[3:]); pdf.set_font('Helvetica','',8.4)
        elif line.startswith('### '):
            pdf.set_font('Helvetica','B',9); pdf.multi_cell(0,5,line[4:]); pdf.set_font('Helvetica','',8.4)
        elif line.startswith('|') or line.startswith('```'):
            continue
        else:
            pdf.set_font('Helvetica','',8.4); pdf.multi_cell(0,4.35,line)


def student_pdf():
    pdf = FPDF(format='A4'); pdf.set_auto_page_break(True, margin=12); pdf.set_compression(True)
    pdf.set_title('Recurrence, Tilings & State Evolution - Student Pack'); pdf.set_author('IOQM Grade 9')
    pdf.add_page(); pdf.set_font('Helvetica','B',18)
    pdf.multi_cell(0,9,'Recurrence, Tilings & State Evolution - Student Pack',align='C')
    pdf.set_font('Helvetica','',10)
    pdf.multi_cell(0,6,'State before recurrence. Define the object/state, prove exactly-once transitions, give meaningful bases, then compute or choose a smaller representation.')
    for name in ['02_Assimilation_Book.md','03_First_Step_Reference.md','04_Recognition_Lab.md','05_First_Line_Lab.md','06_Practice_and_Transfer_Bank.md','07_H0_Mastery_Test.md']:
        add_markdown(pdf, ROOT / name)
    pdf.output(PDF_DIR / 'COMB03_Student_Pack_v1.pdf')


def teacher_companion():
    pdf = FPDF(format='A4'); pdf.set_compression(True); pdf.add_page(); pdf.set_font('Helvetica','B',16)
    pdf.cell(0,10,'COMB-03 Teacher Key - Custody Companion',new_x='LMARGIN',new_y='NEXT',align='C'); pdf.set_font('Helvetica','',9)
    lines = [
        'Full diagnostic solutions are in Teacher_Diagnostic_Key.md in this topic directory.',
        'Final independent audit status: PASS_STATIC_MATH_AFTER_CORRECTION.',
        'Pre-custody correction: Mixed Mastery item 1 = 55 (not 89).',
        'Practice answers 1-20: 13,13,8,21,9,48,21,34,19,11,26,52,8,8,6,5,28,27,5,10.',
        'Mastery answers 1-8: 55,55,28,43,17,10,10,7.',
        'Mastery 9 state: (position,last bit,parity of ones).',
        'Mastery 10 boundary: adversarial game requires an opponent with an opposing strategic objective.',
        'Historical anchors independently verified: 2024-Q14=80, 2024-Q20=10, 2023-Q08=59, 2023-Q21=15, 2023-Q26=19.',
        'Classroom timing/readability, retention, psychometrics and publication approval: NOT_RUN.'
    ]
    for line in lines:
        pdf.multi_cell(0,6,line); pdf.ln(1)
    pdf.output(PDF_DIR / 'COMB03_Teacher_Key_v1.pdf')


student_pdf()
teacher_companion()
