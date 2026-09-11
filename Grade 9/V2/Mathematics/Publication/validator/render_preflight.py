#!/usr/bin/env python3
import argparse
from pathlib import Path
import pypdfium2 as pdfium
from PIL import ImageStat

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pdf',required=True); ap.add_argument('--out-dir',required=True); ap.add_argument('--expected-pages',type=int,required=True); a=ap.parse_args()
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); pdf=pdfium.PdfDocument(a.pdf)
    if len(pdf)!=a.expected_pages: raise SystemExit(f'expected {a.expected_pages} pages, got {len(pdf)}')
    for i,page in enumerate(pdf):
        img=page.render(scale=1.25).to_pil().convert('L'); path=out/f'page-{i+1:02d}.png'; img.save(path)
        if ImageStat.Stat(img).mean[0]>253.5 or path.stat().st_size<5000: raise SystemExit(f'page {i+1} appears empty')
    print(f'MATH-V2-05 render preflight = PASS ({len(pdf)} pages)')
if __name__=='__main__': main()
