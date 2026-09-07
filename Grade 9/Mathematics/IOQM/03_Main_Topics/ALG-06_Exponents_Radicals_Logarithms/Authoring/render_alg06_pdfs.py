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


def _pow_convert(s: str) -> str:
    out, i = "", 0
    while i < len(s):
        if s.startswith("^(", i):
            depth, k = 1, i + 2
            while k < len(s) and depth:
                if s[k] == "(":
                    depth += 1
                elif s[k] == ")":
                    depth -= 1
                k += 1
            if depth == 0:
                out += "^{" + s[i + 2 : k - 1] + "}"
                i = k
                continue
        out += s[i]
        i += 1
    return out


def _texify(s: str) -> str:
    t = _pow_convert(_sqrt_convert(s))
    t = re.sub(r"log_\(([^)]+)\)", r"\\log_{\1}", t)
    t = re.sub(r"log_([A-Za-z0-9]+)", r"\\log_{\1}", t)
    t = t.replace("!=", r"\ne ").replace(">=", r"\ge ").replace("<=", r"\le ")
    t = t.replace("=>", r"\Rightarrow ").replace("⇔", r"\Longleftrightarrow ").replace("⇒", r"\Rightarrow ")
    t = t.replace("*", r"\cdot ")
    if re.fullmatch(r"\{[^{}]+\}=\{[^{}]+\}", t):
        t = re.sub(r"\{([^{}]+)\}", r"\\{\1\\}", t)
    elif re.fullmatch(r"\{[^{}]+\}", t):
        t = r"\{" + t[1:-1] + r"\}"
    return re.sub(r"\bbase\b", r"\\mathrm{base}", t)


def _looks_math(s: str) -> bool:
    if "IOQM-" in s or "BENCHMARK_" in s:
        return False
    if s in {"recognition", "representation", "domain_condition", "equivalence", "execution", "checking", "transfer"}:
        return False
    if re.fullmatch(r"[A-Z][A-Z _\-→>]+", s):
        return False
    return bool(re.search(r"(sqrt|log_|\^|[=<>]|\|[A-Za-z]+\||\d+\s*[+\-*/]\s*\d+)", s))


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
{{\ttfamily\small DOMAIN $\rightarrow$ NORMALIZE $\rightarrow$ REPRESENT $\rightarrow$ TRANSFORM $\rightarrow$ CHECK}}\\[22mm]
{{\sffamily\small\color{{darkgray}} {audience}}}
\vfill
{{\sffamily\footnotesize {footer}}}
\newpage
```
'''


def _combine(files, title, subtitle, audience, footer):
    parts = [_cover(title, subtitle, audience, footer)]
    for i, name in enumerate(files):
        if i:
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
\fancyhead[R]{\sffamily\footnotesize Exponents · Radicals · Logarithms}
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
        r"Exponents, Radicals \& Logarithms",
        "Strategic representation with domain and reversibility control",
        "Student learning pack · assimilation, recognition, transfer, mastery",
        "Grade 9 IOQM learning pack",
    )
    teacher = _combine(
        TEACHER_FILES,
        r"Exponents, Radicals \& Logarithms",
        "Diagnostic and benchmark teacher companion",
        "Teacher-only companion · independent answer and misconception diagnostics",
        "Grade 9 IOQM learning pack",
    )
    _render(student, PDF_DIR / "ALG06_Student_Pack_v1.pdf", "IOQM Grade 9 · Mathematics")
    _render(teacher, PDF_DIR / "ALG06_Teacher_Key_v1.pdf", "IOQM Grade 9 · ALG-06")


if __name__ == "__main__":
    main()
