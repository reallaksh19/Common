from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "PDFs"
PDF_DIR.mkdir(exist_ok=True)

STUDENT_FILES = [
    "02_Assimilation_Book.md",
    "03_First_Step_Reference.md",
    "04_Recognition_and_First_Line_Lab.md",
    "05_Practice_and_Transfer_Bank.md",
    "07_Benchmark_Assimilation_Lab.md",
    "06_H0_Mastery_Test.md",
]
TEACHER_FILES = ["Teacher_Diagnostic_Key.md", "Teacher_Benchmark_Assimilation_Key.md"]


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
                    if s[k] == "(":
                        depth += 1
                    elif s[k] == ")":
                        depth -= 1
                    k += 1
                if depth == 0:
                    out += r"\sqrt{" + _sqrt_convert(s[j + 1 : k - 1]) + "}"
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
                if s[k] == "(":
                    depth += 1
                elif s[k] == ")":
                    depth -= 1
                k += 1
            if depth == 0:
                out += marker + "{" + s[i + 2 : k - 1] + "}"
                i = k
                continue
        out += s[i]
        i += 1
    return out


def _texify(s: str) -> str:
    t = _sqrt_convert(s)
    t = _group_convert(_group_convert(t, "^"), "_")
    t = t.replace("²", "^2").replace("³", "^3")
    t = t.replace("∠", r"\angle ").replace("⟂", r"\perp ")
    t = t.replace("°", r"^{\circ}")
    t = t.replace("·", r"\cdot ")
    t = t.replace("≠", r"\ne ").replace("!=", r"\ne ")
    t = t.replace(">=", r"\ge ").replace("<=", r"\le ")
    t = t.replace("=>", r"\Rightarrow ").replace("⇔", r"\Longleftrightarrow ").replace("⇒", r"\Rightarrow ")
    t = t.replace("*", r"\cdot ")
    return t


def _looks_math(s: str) -> bool:
    if "IOQM-" in s or "BENCHMARK_" in s:
        return False
    if s in {
        "recognition", "representation", "execution", "checking", "transfer",
        "CYCLICITY_ASSUMED_FROM_PICTURE", "GENERIC_QUAD_RULE_USED",
        "TANGENCY_NOT_PROVED", "TANGENT_CHORD_CONFUSED", "POWER_POINT_MISMATCH",
        "WRONG_PRODUCT_SEGMENTS", "SYNTHETIC_CHAIN_NOT_RECOGNIZED", "COORDINATE_OVERKILL",
    }:
        return False
    if re.fullmatch(r"[A-Z][A-Z _\-→>]+", s):
        return False
    # Workflow prose inside code ticks must stay prose, not collapsed math.
    if re.search(r"[A-Za-z]{4,}\s+[A-Za-z]{4,}", s) and not re.search(r"[=∠⟂°²³·]", s):
        return False
    return bool(re.search(r"(sqrt|\^|_[A-Za-z0-9(]|[=<>]|∠|⟂|°|²|³|·|\d+\s*[+\-*/]\s*\d+|\([A-Z]{2}/[A-Z]{2}\))", s))


def _preprocess(md: str) -> str:
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)

    def repl(m):
        s = m.group(1)
        return "$" + _texify(s) + "$" if _looks_math(s) else "`" + s + "`"

    return re.sub(r"`([^`\n]+)`", repl, md)


def _cover(title: str, subtitle: str, audience: str, footer: str) -> str:
    return rf'''```{{=latex}}
\thispagestyle{{empty}}
\vspace*{{27mm}}
{{\sffamily\bfseries\small IOQM · GRADE 9 MATHEMATICS}}\\[18mm]
{{\sffamily\bfseries\fontsize{{27}}{{31}}\selectfont {title}}}\\[8mm]
{{\sffamily\fontsize{{14}}{{18}}\selectfont\color{{darkgray}} {subtitle}}}\\[12mm]
\rule{{38mm}}{{1.1pt}}\\[8mm]
{{\ttfamily\small STRUCTURE $\rightarrow$ JUSTIFY $\rightarrow$ LOCAL RELATION $\rightarrow$ ROUTE $\rightarrow$ CHECK}}\\[22mm]
{{\sffamily\small\color{{darkgray}} {audience}}}
\vfill
{{\sffamily\footnotesize {footer}}}
\newpage
```
'''


def _combine(files, title, subtitle, audience, footer, force_breaks=True):
    parts = [_cover(title, subtitle, audience, footer)]
    for i, name in enumerate(files):
        if i and force_breaks:
            parts.append(r"\newpage")
        parts.append(_preprocess((ROOT / name).read_text(encoding="utf-8")))
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
\renewcommand{\arraystretch}{1.22}
\AtBeginEnvironment{longtable}{\small}
\widowpenalty=10000
\clubpenalty=10000
\hyphenpenalty=10000
\exhyphenpenalty=10000
\raggedbottom
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\sffamily\footnotesize HEADER_LEFT}
\fancyhead[R]{\sffamily\footnotesize Circles · Cyclicity · Tangency}
\fancyfoot[C]{\sffamily\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\setlength{\headheight}{14pt}
'''


def _render(md_text: str, output: Path, header_left: str):
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        md_path = td / "combined.md"
        header_path = td / "header.tex"
        md_path.write_text(md_text, encoding="utf-8")
        header_path.write_text(HEADER.replace("HEADER_LEFT", header_left), encoding="utf-8")
        cmd = [
            "pandoc", str(md_path), "-f", "markdown+raw_tex", "--pdf-engine=xelatex",
            "--include-in-header", str(header_path),
            "-V", "papersize:a4",
            "-V", "geometry:top=17mm,bottom=18mm,left=17mm,right=17mm",
            "-V", "fontsize=10pt",
            "-V", "mainfont=DejaVu Sans",
            "-V", "sansfont=DejaVu Sans",
            "-V", "monofont=DejaVu Sans Mono",
            "-V", "mathfont=DejaVu Math TeX Gyre",
            "-o", str(output),
        ]
        subprocess.run(cmd, check=True)


def main():
    student = _combine(
        STUDENT_FILES,
        r"Circles, Cyclicity \& Tangency",
        "Recognition chains before theorem selection",
        "Student learning pack · assimilation, recognition, transfer, mastery",
        "Grade 9 IOQM learning pack",
        force_breaks=True,
    )
    teacher = _combine(
        TEACHER_FILES,
        r"Circles, Cyclicity \& Tangency",
        "Diagnostic and benchmark teacher companion",
        "Teacher-only companion · independent answer and misconception diagnostics",
        "Grade 9 IOQM learning pack",
        force_breaks=False,
    )
    _render(student, PDF_DIR / "GEO04_Student_Pack_v1.pdf", "IOQM Grade 9 · Mathematics")
    _render(teacher, PDF_DIR / "GEO04_Teacher_Key_v1.pdf", "IOQM Grade 9 · GEO-04")


if __name__ == "__main__":
    main()
