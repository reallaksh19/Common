#!/usr/bin/env python3
import json, sys
from pathlib import Path
WEIGHTS={"conceptual":0.25,"recognition":0.25,"reasoning_steps":0.15,"algebra":0.15,"hidden_structure":0.10,"constraints_cases":0.10}
def score(v):
    missing=[k for k in WEIGHTS if k not in v]
    if missing: raise ValueError("Missing difficulty dimensions: "+", ".join(missing))
    return sum(float(v[k])*w for k,w in WEIGHTS.items())
def main():
    if len(sys.argv)!=2: print("Usage: difficulty_check.py input.json",file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")); a,c=score(d["anchor"]),score(d["candidate"]); delta=c-a; mode=d.get("mode","same_level")
    ok=abs(delta)<=0.4 if mode=="same_level" else (0.8<=delta<=1.3 if mode=="challenge" else False)
    print(json.dumps({"anchor_score":round(a,3),"candidate_score":round(c,3),"delta":round(delta,3),"mode":mode,"scalar_screen":"PASS" if ok else "FAIL","human_review_required":True,"note":"Local heuristic only; compare cognitive profile and solution path."},indent=2)); return 0 if ok else 1
if __name__=="__main__": raise SystemExit(main())
