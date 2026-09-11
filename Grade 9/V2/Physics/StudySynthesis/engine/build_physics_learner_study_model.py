#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from study_common import *
from study_scope import derive_study_scope
from study_treatment import *

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scope-bindings",required=True)
    ap.add_argument("--scope-authority",required=True)
    ap.add_argument("--problem-semantics",required=True)
    ap.add_argument("--learner-snapshot",required=True)
    ap.add_argument("--treatment-policy",required=True)
    ap.add_argument("--scope-out",required=True)
    ap.add_argument("--model-out",required=True)
    a=ap.parse_args()
    s=derive_study_scope(load(a.scope_bindings),load(a.scope_authority),load(a.problem_semantics))
    m=build_model(s,load(a.learner_snapshot),load(a.treatment_policy))
    Path(a.scope_out).write_text(json.dumps(s,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    Path(a.model_out).write_text(json.dumps(m,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
if __name__=="__main__": main()
