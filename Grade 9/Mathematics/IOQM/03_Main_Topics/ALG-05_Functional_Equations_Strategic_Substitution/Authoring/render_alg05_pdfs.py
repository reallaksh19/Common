from fpdf import FPDF
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / 'PDFs'
PDF_DIR.mkdir(exist_ok=True)


def clean(s):
    s = re.sub(r'`([^`]*)`', r'\1', s).replace('**', '')
    for a, b in [
        ('–', '-'), ('—', '-'), ('→', '->'), ('×', 'x'), ('√', 'sqrt'),
        ('≤', '<='), ('≥', '>='), ('•', '-'), ('π', 'pi'), ('⇒', '=>'),
        ('“', '"'), ('”', '"'), ('‘', "'"), ('’', "'"), ('…', '...')
    ]:
        s = s.replace(a, b)
    return s.encode('latin-1', 'replace').decode('latin-1')


def add_markdown(pdf, path):
    for raw in path.read_text(encoding='utf-8').splitlines():
        pdf.set_x(pdf.l_margin)
        line = clean(raw.strip())
        if not line:
            pdf.ln(1.5)
        elif line.startswith('# '):
            pdf.ln(3)
            pdf.set_font('Helvetica', 'B', 14)
            pdf.multi_cell(0, 7, line[2:])
            pdf.set_font('Helvetica', '', 8.4)
        elif line.startswith('## '):
            pdf.ln(2)
            pdf.set_font('Helvetica', 'B', 11)
            pdf.multi_cell(0, 6, line[3:])
            pdf.set_font('Helvetica', '', 8.4)
        elif line.startswith('### '):
            pdf.set_font('Helvetica', 'B', 9)
            pdf.multi_cell(0, 5, line[4:])
            pdf.set_font('Helvetica', '', 8.4)
        elif line.startswith('|') or line.startswith('```'):
            continue
        else:
            pdf.set_font('Helvetica', '', 8.4)
            pdf.multi_cell(0, 4.35, line)


def student_pdf():
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(True, margin=12)
    pdf.set_compression(True)
    pdf.set_title('Functional Equations - Strategic Substitution - Student Pack')
    pdf.set_author('IOQM Grade 9')
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.multi_cell(0, 9, 'Functional Equations - Strategic Substitution', align='C')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(
        0,
        6,
        'State the domain. Choose an input for structural payoff, pair or combine equations when the argument map closes, prove the rule for all allowed inputs, then check the original equation.'
    )
    for name in [
        '02_Assimilation_Book.md',
        '03_First_Step_Reference.md',
        '04_Recognition_and_First_Line_Lab.md',
        '05_Practice_and_Transfer_Bank.md',
        '06_H0_Mastery_Test.md',
    ]:
        add_markdown(pdf, ROOT / name)
    pdf.output(PDF_DIR / 'ALG05_Student_Pack_v1.pdf')


def teacher_companion():
    pdf = FPDF(format='A4')
    pdf.set_compression(True)
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'ALG-05 Teacher Key - Custody Companion', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.set_font('Helvetica', '', 9)
    lines = [
        'Full diagnostic solutions are in Teacher_Diagnostic_Key.md in this topic directory.',
        'Independent mathematical/source audit: PASS_STATIC_MATH_AND_SOURCE.',
        'Historical anchors independently verified: IOQM-2025-Q14=12; IOQM-2024-Q16=08.',
        'Recognition/First-Line Lab: 16 items; Practice/Transfer: 20 items; Mixed Mastery: 10 items.',
        'Mixed Mastery numeric results: 12, 45, not uniquely determined, injectivity proof, 17, 13, recurrence boundary explanation, candidate verifies, -2, proof-completeness test.',
        'Metadata: frozen 31-column schema; 48 rows = 2 historical + 46 author-created; all promoted rows independently verified.',
        'Student export excludes authoring interfaces, source-control labels, hint/wave/topic-control codes and teacher solutions.',
        'Classroom timing/readability, retention, psychometrics, calibration, qualification probability and publication approval: NOT_RUN.'
    ]
    for line in lines:
        pdf.multi_cell(0, 6, line)
        pdf.ln(1)
    pdf.output(PDF_DIR / 'ALG05_Teacher_Key_v1.pdf')


student_pdf()
teacher_companion()
