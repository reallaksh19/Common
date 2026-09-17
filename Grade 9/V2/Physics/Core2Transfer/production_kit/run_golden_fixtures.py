#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_transfer_representation import build
from validate_transfer_representation import validate
def main():
    files=sorted((ROOT/'fixtures'/'golden').glob('*.json')); assert len(files)==3, f'expected 3 golden fixtures, found {len(files)}'
    out=[]
    for p in files:
        f=json.loads(p.read_text(encoding='utf-8')); rep=build(f); out.append({'fixture':p.name,**validate(rep,f)})
    print(json.dumps({'status':'PASS','fixture_count':len(out),'results':out},indent=2))
if __name__=='__main__': main()
