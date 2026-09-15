from pathlib import Path
import re,json,sys
R=Path(__file__).resolve().parents[1]
s=(R/'source-corpus.md').read_text(encoding='utf-8'); c=(R/'Core2.md').read_text(encoding='utf-8')
results=[]; fail=[]
for i in range(1,13):
 q=f'Q{i:02d}'
 m=re.search(rf'^## {q}\n\n(.*?)(?=\n## Q\d{{2}}\n|\Z)',s,re.M|re.S); src=m.group(1).strip()
 if q=='Q12': src=src.split('\n\nQ12 is deliberately supplied exactly as written.')[0].strip()
 m2=re.search(rf'<!-- FROZEN_SOURCE_START:{q} -->\n(.*?)\n<!-- FROZEN_SOURCE_END:{q} -->',c,re.S)
 exact=bool(m2) and m2.group(1).strip()==src
 attr='Author-created test fixture; not an official CBSE or past-exam question.' in c[c.find(f'<a id="{q.lower()}"></a>'):c.find(f'<a id="{q.lower()}-answer"></a>')]
 hints_ok=all(x in c[c.find(f'<a id="{q.lower()}"></a>'):c.find(f'<a id="{q.lower()}-answer"></a>')] for x in ['### H1','### H2','### H3'])
 ans=f'<a id="{q.lower()}-answer"></a>' in c
 if not (exact and attr and hints_ok and ans): fail.append(q)
 results.append({'question':q,'source_exact':exact,'attribution_present':attr,'hint_ladder_present':hints_ok,'answer_anchor_present':ans,'q02_table_in_immutable_block':('| 2 | 6 | 8 |' in m2.group(1)) if q=='Q02' and m2 else None})
q12_ok='underdetermined' in c[c.find('<a id="q12-answer"></a>'):].lower() and 'both east' in c[c.find('<a id="q12-answer"></a>'):].lower()
if not q12_ok: fail.append('Q12 scientific hold')
print(json.dumps({'status':'PASS' if not fail else 'FAIL','questions':results,'q12_scientific_hold':q12_ok,'failures':fail},indent=2))
sys.exit(1 if fail else 0)
