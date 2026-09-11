#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text())
def schema(n): return load(ROOT/'contracts'/n)
def val(o,n): Draft202012Validator(schema(n)).validate(o)
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(o): return hashlib.sha256(canonical(o)).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); a=ap.parse_args(); out=Path(a.out)
    findings=load(out/'review_findings.resolved.json'); decisions=load(out/'revision_decisions.json'); summary=load(out/'quality_review_summary.json'); package=load(out/'review_package.json')
    for f in findings: val(f,'review-finding.schema.json')
    for d in decisions: val(d,'revision-decision.schema.json')
    val(summary,'quality-review-summary.schema.json')
    if any(f['status']!='CLOSED_FIXED' for f in findings): raise ValueError('resolved AI finding remains open')
    if any(f.get('revised_artifact_sha256')!=summary['revised_artifact_sha256'] for f in findings): raise ValueError('finding revision digest drift')
    if any(d.get('revised_artifact_sha256')!=summary['revised_artifact_sha256'] for d in decisions): raise ValueError('decision revision digest drift')
    comps={'resolved_findings_sha256':sha(findings),'revision_decisions_sha256':sha(decisions),'quality_review_summary_sha256':sha(summary)}
    if any(package[k]!=v for k,v in comps.items()) or package['package_digest']!=sha(comps): raise ValueError('review package digest drift')
    if summary['human_review_evidence']!={'SUBJECT':0,'PEDAGOGY':0,'VISUAL':0}: raise ValueError('human evidence invented')
    print('MATH-V2-06 review output validation = PASS')
if __name__=='__main__': main()
