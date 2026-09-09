#!/usr/bin/env python3
"""Reconcile a frozen ExamSIDE ledger against the question-bank model it was actually
published into. check_ledger.py only proves the ledger is internally consistent
(expected_ids == recorded ids); it never checks that those records match what
grade9-physics-publication rendered. That gap let the ledger and publication model
drift apart while both independently passed (PR #155 review finding D).

Implements grade9-transfer-coverage-auditor's View 1 (subtopic -> questions) / View 2
(question -> full support chain) dual audit and its blocking-counter contract over this
ledger/model pair, instead of inventing a separate reconciliation scheme (finding F).

Also cross-checks each record's `dependency` (question-contract.md's NONE/GRAPH/DIAGRAM/TABLE/
TIMELINE/NUMBER_LINE/OPTION_FIGURES/STATEMENT_SET/MIXED classification of what the *source*
needed) against the *published* figure.dependency_class - the same vocabulary grade9-physics-
publication's Figure already carries (validate_v2.py's _DEP_CLASS_FOR_KIND). Nothing consumed
that classification across the ledger/publication boundary before; this is what makes it a real
generic contract instead of a label only grade9-physics-publication's own renderer ever reads."""
import json,sys
from pathlib import Path

_TIER_KEY={'H1':'h1','H2':'h2','H3':'h3'}

def reconcile(ledger,model):
    expected=set(ledger['expected_ids'])
    lrecords={r['id']:r for r in ledger['records']}
    qb=model['questions'];pub={q['id']:q for q in qb['anchors']+qb['core_calibrated']+qb['challenges']}
    missing=sorted(expected-pub.keys())          # ledgered but never published
    unledgered=sorted(pub.keys()-expected)        # published but not in the frozen ledger
    concept_fail=[];hint_fail=[];solution_fail=[];status_fail=[];dependency_fail=[]
    view1=[];view2=[]
    for qid in sorted(expected&pub.keys()):
        r=lrecords[qid];q=pub[qid];chain=[]
        ok_concept=r['primary_concept']==q['primary_concept_id']
        if not ok_concept:concept_fail.append(qid)
        chain.append('primary_concept '+('MATCH '+q['primary_concept_id'] if ok_concept else f"MISMATCH ledger={r['primary_concept']} published={q['primary_concept_id']}"))
        # Matched by each hint's own tier field, not by list position (hint-numbering-unification):
        # a published hints array reordered relative to the ledger's h1/h2/h3 keys is still caught.
        pub_by_tier={h['tier']:h['text'] for h in q['hints']}
        ok_hints=len(q['hints'])==3 and all(r['hints'].get(lk)==pub_by_tier.get(pk) for pk,lk in _TIER_KEY.items())
        if not ok_hints:hint_fail.append(qid)
        chain.append('hints '+('MATCH H1-H3' if ok_hints else 'MISMATCH (ledger h1/h2/h3 vs published hints[*].tier/.text diverge)'))
        ok_solution=all(q['solution'].get(k)==r['solution'].get(k) for k in ('why','method','answer','keep'))
        if not ok_solution:solution_fail.append(qid)
        chain.append('solution '+('MATCH why/method/answer/keep' if ok_solution else 'MISMATCH'))
        ok_status=(r['state']=='ORIGINAL')==(q['source_status']=='ORIGINAL')
        if not ok_status:status_fail.append(qid)
        chain.append('source_status '+('CONSISTENT' if ok_status else f"MISMATCH ledger.state={r['state']} published.source_status={q['source_status']}"))
        ledger_dep=r.get('dependency','NONE');published_dep=(q.get('figure') or {}).get('dependency_class','NONE')
        ok_dependency=ledger_dep==published_dep
        if not ok_dependency:dependency_fail.append(qid)
        chain.append('dependency '+('MATCH '+published_dep if ok_dependency else f"MISMATCH ledger.dependency={ledger_dep} published.figure.dependency_class={published_dep}"))
        complete=ok_concept and ok_hints and ok_solution and ok_status and ok_dependency
        chain.append('COMPLETE' if complete else 'DRIFTED')
        view1.append(f"{qid} {'PLACED' if complete else 'DRIFTED'}")
        view2.append({'id':qid,'chain':chain})
    for qid in missing:view1.append(f'{qid} MISSING (ledgered, never published)')
    for qid in unledgered:view1.append(f'{qid} UNLEDGERED (published, not in frozen ledger)')
    counters=dict(
        LEDGER_REQUIRED=len(expected),LEDGER_PLACED=len(expected)-len(missing),
        LEDGER_MISSING=len(missing),LEDGER_UNLEDGERED=len(unledgered),
        LEDGER_CONCEPT_LINK_FAILURES=len(concept_fail),LEDGER_HINT_FAILURES=len(hint_fail),
        LEDGER_SOLUTION_FAILURES=len(solution_fail),LEDGER_SOURCE_STATUS_FAILURES=len(status_fail),
        LEDGER_DEPENDENCY_FAILURES=len(dependency_fail),
        LEDGER_STATUS='PASS' if not(missing or unledgered or concept_fail or hint_fail or solution_fail or status_fail or dependency_fail) else 'FAIL')
    return dict(view1_subtopic_to_questions=view1,view2_question_to_support_chain=view2,counters=counters,
        missing=missing,unledgered=unledgered,concept_link_failures=concept_fail,hint_failures=hint_fail,
        solution_failures=solution_fail,source_status_failures=status_fail,dependency_failures=dependency_fail)

if __name__=='__main__':
    ledger=json.loads(Path(sys.argv[1]).read_text());model=json.loads(Path(sys.argv[2]).read_text())
    out=reconcile(ledger,model);print(json.dumps(out,indent=2))
    sys.exit(0 if out['counters']['LEDGER_STATUS']=='PASS' else 1)
