from pathlib import Path
import re
import subprocess
import tempfile

IOQM = Path(__file__).resolve().parents[1]
TOPICS = IOQM / "03_Main_Topics"

CONFIG = {
    "NT01": {
        "root": TOPICS / "NT-01_Divisibility_GCD_LCM",
        "student_files": [
            "02_Assimilation_Book.md",
            "03_First_Step_Reference.md",
            "04_Recognition_and_First_Line_Lab.md",
            "05_Practice_and_Transfer_Bank.md",
            "06_H0_Mastery_Test.md",
        ],
        "teacher_files": ["Teacher_Diagnostic_Key.md", "Teacher_Coverage_Hardening_Addendum.md"],
        "student_pdf": "NT01_Student_Pack_v1.pdf",
        "teacher_pdf": "NT01_Teacher_Key_v1.pdf",
        "title": "Divisibility, GCD and LCM",
        "subtitle": "Structure, Euclid, reconstruction and prime-product divisibility",
        "router": "TARGET -> DIVISOR / MULTIPLE -> REDUCTION -> THEOREM CHECK -> VERIFY",
    },
    "NT02": {
        "root": TOPICS / "NT-02_Modular_Arithmetic_Residues",
        "student_files": [
            "02_Assimilation_Book.md",
            "03_First_Step_Reference.md",
            "04_Recognition_and_First_Line_Lab.md",
            "05_Practice_and_Transfer_Bank.md",
            "06_H0_Mastery_Test.md",
        ],
        "teacher_files": ["Teacher_Diagnostic_Key.md", "Teacher_Coverage_Hardening_Addendum.md"],
        "student_pdf": "NT02_Student_Pack_v1.pdf",
        "teacher_pdf": "NT02_Teacher_Key_v1.pdf",
        "title": "Modular Arithmetic, Residues and Power Cycles",
        "subtitle": "Legal residue moves, cycles, Euler bridge and theorem hypotheses",
        "router": "TARGET MODULUS -> REDUCE -> CYCLE / THEOREM -> LEGALITY -> CHECK",
    },
}


def _sqrt_convert(s: str) -> str:
    out, i = "", 0
    while i < len(s):
        if s.startswith("sqrt", i):
            j = i + 4
            while j < len(s) and s[j] == " ":
                j += 1
            if j < len(s) and s[j] == "(":
                depth, k = 1, j + 1
                while k < len(s) and depth:
                    if s[k] == "(": depth += 1
                    elif s[k] == ")": depth -= 1
                    k += 1
                if depth == 0:
                    out += r"\sqrt{" + _sqrt_convert(s[j + 1:k - 1]) + "}"
                    i = k
                    continue
            m = re.match(r"[A-Za-z0-9]+", s[j:])
            if m:
                token = m.group()
                out += r"\sqrt{" + token + "}"
                i = j + len(token)
                continue
        out += s[i]
        i += 1
    return out


def _group_convert(s: str, marker: str) -> str:
    out, i = "", 0
    needle = marker + "("
    while i < len(s):
        if s.startswith(needle, i):
            depth, k = 1, i + 2
            while k < len(s) and depth:
                if s[k] == "(": depth += 1
                elif s[k] == ")": depth -= 1
                k += 1
            if depth == 0:
                out += marker + "{" + s[i + 2:k - 1] + "}"
                i = k
                continue
        out += s[i]
        i += 1
    return out


def _power_towers(s: str) -> str:
    # Convert simple right-associated towers such as 7^7^7 to 7^{7^{7}}.
    pat = re.compile(r"\b([A-Za-z0-9]+)\^([A-Za-z0-9]+)\^([A-Za-z0-9]+)\b")
    while pat.search(s):
        s = pat.sub(lambda m: f"{m.group(1)}^{{{m.group(2)}^{{{m.group(3)}}}}}", s)
    return s


def _texify(s: str) -> str:
    t = _sqrt_convert(s)
    t = _power_towers(t)
    t = _group_convert(_group_convert(t, "^"), "_")
    t = t.replace("²", "^2").replace("³", "^3")
    t = t.replace("≡", r"\equiv ").replace("∤", r"\nmid ").replace("|", r"\mid ")
    t = t.replace("φ", r"\varphi ").replace("·", r"\cdot ")
    t = t.replace("≠", r"\ne ").replace("!=", r"\ne ")
    t = t.replace(">=", r"\ge ").replace("<=", r"\le ")
    t = t.replace("⇔", r"\Longleftrightarrow ").replace("⇒", r"\Rightarrow ").replace("=>", r"\Rightarrow ")
    t = t.replace("*", r"\cdot ")
    t = re.sub(r"\bcongruent\b", r"\\equiv", t)
    return t


def _looks_math(s: str) -> bool:
    if "/" in s or re.search(r"\.(md|csv|py|pdf)$", s, re.I): return False
    if re.fullmatch(r"[A-Z][A-Z0-9 _\-]+", s): return False
    if re.search(r"[A-Za-z]{4,}\s+[A-Za-z]{4,}", s) and not re.search(r"[=<>≡∤φ²³·^]", s): return False
    return bool(re.search(r"(sqrt|\^|_[A-Za-z0-9(]|[=<>]|≡|∤|φ|²|³|·|\bmod\b|\bgcd\b|\blcm\b|\bphi\b|\bcongruent\b|\d+\s*[+\-*/]\s*\d+|[A-Za-z]\|[A-Za-z0-9(])", s))


def _preprocess(md: str) -> str:
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = md.replace("→", "->").replace("—", "-").replace("–", "-")
    def repl(m):
        s = m.group(1)
        return "$" + _texify(s) + "$" if _looks_math(s) else "`" + s + "`"
    return re.sub(r"`([^`\n]+)`", repl, md)


def _cover(title, subtitle, audience, footer, router):
    esc = lambda x: x.replace("&", r"\&")
    safe_router = esc(router).replace("->", r"$\rightarrow$")
    return rf'''```{{=latex}}
\thispagestyle{{empty}}
\vspace*{{22mm}}
{{\sffamily\bfseries\small IOQM · GRADE 9 MATHEMATICS}}\\[16mm]
{{\sffamily\bfseries\fontsize{{25}}{{29}}\selectfont {esc(title)}}}\\[7mm]
{{\sffamily\fontsize{{13}}{{17}}\selectfont\color{{darkgray}} {esc(subtitle)}}}\\[10mm]
\rule{{38mm}}{{1.1pt}}\\[8mm]
{{\ttfamily\small {safe_router}}}\\[20mm]
{{\sffamily\small\color{{darkgray}} {esc(audience)}}}
\vfill
{{\sffamily\footnotesize {esc(footer)}}}
\newpage
```
'''


def _combine(root, files, title, subtitle, audience, footer, router, breaks=True):
    parts = [_cover(title, subtitle, audience, footer, router)]
    for i, name in enumerate(files):
        if i and breaks: parts.append(r"\newpage")
        parts.append(_preprocess((root / name).read_text(encoding="utf-8")))
    return "\n\n".join(parts)


HEADER = r'''\usepackage{xcolor}
\usepackage{microtype}
\usepackage{enumitem}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{fancyhdr}
\usepackage{etoolbox}
\setlist[itemize]{leftmargin=*,topsep=3pt,itemsep=2pt}
\setlist[enumerate]{leftmargin=*,topsep=3pt,itemsep=2.4pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\renewcommand{\arraystretch}{1.20}
\AtBeginEnvironment{longtable}{\small}
\widowpenalty=10000
\clubpenalty=10000
\hyphenpenalty=10000
\exhyphenpenalty=10000
\raggedbottom
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\sffamily\footnotesize HEADER_LEFT}
\fancyhead[R]{\sffamily\footnotesize HEADER_RIGHT}
\fancyfoot[C]{\sffamily\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\setlength{\headheight}{14pt}
'''


def _render(md_text, output, header_left, header_right):
    output.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        md_path, header_path = td / "combined.md", td / "header.tex"
        md_path.write_text(md_text, encoding="utf-8")
        header_path.write_text(HEADER.replace("HEADER_LEFT", header_left).replace("HEADER_RIGHT", header_right), encoding="utf-8")
        subprocess.run([
            "pandoc", str(md_path), "-f", "markdown+raw_tex", "--pdf-engine=xelatex",
            "--include-in-header", str(header_path), "-V", "papersize:letter",
            "-V", "geometry:top=0.66in,bottom=0.67in,left=0.67in,right=0.67in",
            "-V", "fontsize=9pt", "-V", "mainfont=DejaVu Sans", "-V", "sansfont=DejaVu Sans",
            "-V", "monofont=DejaVu Sans Mono", "-V", "mathfont=DejaVu Math TeX Gyre",
            "-o", str(output)
        ], check=True)


def render_topic(code):
    cfg = CONFIG[code]; root = cfg["root"]; pdf_dir = root / "PDFs"
    student = _combine(root, cfg["student_files"], cfg["title"], cfg["subtitle"], "Student learning pack - assimilation, recognition, transfer and mastery", "Grade 9 IOQM learning pack", cfg["router"], True)
    teacher = _combine(root, cfg["teacher_files"], cfg["title"], "Diagnostic and coverage-hardening companion", "Teacher-only companion - answer diagnostics and theorem-hypothesis checks", "Grade 9 IOQM teacher companion", cfg["router"], False)
    _render(student, pdf_dir / cfg["student_pdf"], "IOQM Grade 9 · Mathematics", cfg["title"])
    _render(teacher, pdf_dir / cfg["teacher_pdf"], "IOQM Grade 9 · Teacher", cfg["title"])


def main():
    render_topic("NT01")
    render_topic("NT02")

if __name__ == "__main__": main()
