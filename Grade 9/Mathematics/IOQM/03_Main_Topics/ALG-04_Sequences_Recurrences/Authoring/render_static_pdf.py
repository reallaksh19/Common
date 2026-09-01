from pathlib import Path
import re, zlib, base64

ROOT = Path(__file__).resolve().parents[1]
PDFS = ROOT / "PDFs"
PDFS.mkdir(exist_ok=True)
FILES = [
    "02_Assimilation_Book.md",
    "03_First_Step_Reference.md",
    "04_Recognition_and_First_Line_Lab.md",
    "05_Practice_and_Transfer_Bank.md",
    "06_H0_Mastery_Test.md",
]


def clean(s):
    s = s.rstrip()
    s = re.sub(r"^#{1,6}\s*", "", s)
    s = s.replace("**", "").replace("__", "").replace("`", "")
    s = re.sub(r"^>\s?", "", s)
    s = re.sub(r"^[-*]\s+", "- ", s)
    return s


def wrap(s, width=112):
    if not s:
        return [""]
    m = re.match(r"^(\s*(?:\d+\.|- )\s*)", s)
    indent = " " * min(len(m.group(1)), 6) if m else ""
    out, cur = [], ""
    for word in s.split():
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= width:
            cur += " " + word
        else:
            out.append(cur)
            cur = indent + word
    if cur:
        out.append(cur)
    return out


def esc(s):
    s = s.encode("ascii", "replace").decode("ascii")
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build(out, label, fontsize=7.2, leading=8.7, lines_per_page=80):
    pages, current = [], []
    for index, filename in enumerate(FILES):
        if index and current:
            pages.append(current)
            current = []
        for raw in (ROOT / filename).read_text().splitlines():
            line = clean(raw)
            if re.fullmatch(r"-{3,}", line.strip()):
                continue
            for item in wrap(line):
                if len(current) >= lines_per_page:
                    pages.append(current)
                    current = []
                current.append(item)
        if current and len(current) > lines_per_page - 4:
            pages.append(current)
            current = []
    if current:
        pages.append(current)

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        None,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    ]
    kids = []
    for page_number, lines in enumerate(pages, 1):
        page_obj = len(objects) + 1
        content_obj = page_obj + 1
        kids.append(f"{page_obj} 0 R")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_obj} 0 R >>".encode())
        commands = ["BT", f"/F1 {fontsize:.1f} Tf", f"{leading:.1f} TL", "30 758 Td"]
        for line_number, line in enumerate(lines):
            if line_number == 0 or (line and line.upper() == line and len(line) < 90):
                commands += ["/F2 8.4 Tf", f"({esc(line)}) Tj", f"/F1 {fontsize:.1f} Tf"]
            else:
                commands.append(f"({esc(line)}) Tj")
            commands.append("T*")
        commands += ["ET", "BT", "/F1 6 Tf", f"30 18 Td ({label}) Tj", f"500 0 Td (Page {page_number}/{len(pages)}) Tj", "ET"]
        compressed = zlib.compress("\n".join(commands).encode("ascii"), 9)
        encoded = base64.a85encode(compressed, adobe=False, wrapcol=0)
        objects.append(b"<< /Filter [/ASCII85Decode /FlateDecode] /Length " + str(len(encoded)+2).encode() + b" >>\nstream\n" + encoded + b"~>\nendstream")

    objects[1] = f"<< /Type /Pages /Count {len(pages)} /Kids [{' '.join(kids)}] >>".encode()
    data = bytearray(b"%PDF-1.4\n%ASCII\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += f"{number} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref = len(data)
    size = len(objects) + 1
    data += f"xref\n0 {size}\n".encode() + b"0000000000 65535 f \n"
    for offset in offsets[1:]:
        data += f"{offset:010d} 00000 n \n".encode()
    data += f"trailer\n<< /Size {size} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    out.write_bytes(data)


build(PDFS / "ALG04_Student_Pack_v1.pdf", "ALG-04 Student Pack")
