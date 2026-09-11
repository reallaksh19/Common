#!/usr/bin/env python3
import argparse
from pathlib import Path
import pypdfium2 as pdfium
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pdf',required=True); ap.add_argument('--out-dir',required=True); ap.add_argument('--expected-pages',type=int,required=True); a=ap.parse_args()
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); pdf=pdfium.PdfDocument(a.pdf)
    if len(pdf)!=a.expected_pages: raise ValueError(f'expected {a.expected_pages} pages, got {len(pdf)}')
    for n,page in enumerate(pdf):
        img=page.render(scale=1.4).to_pil().convert('L'); extrema=img.getextrema()
        if extrema==(255,255): raise ValueError(f'blank page {n+1}')
        img.save(out/f'page-{n+1:02d}.png')
    print(f'PHY-V2-05 render preflight = PASS ({len(pdf)} nonblank pages)')
if __name__=='__main__': main()
