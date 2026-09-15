from pathlib import Path
import json,re,collections,hashlib,sys
R=Path(__file__).resolve().parents[1]
source=(R/'source-corpus.md').read_text(encoding='utf-8')
inv=json.loads((R/'source-inventory.json').read_text(encoding='utf-8'))
atoms=inv['atoms']
fail=[]
if hashlib.sha256((R/'source-corpus.md').read_bytes()).hexdigest()!=inv['source_corpus_sha256']: fail.append('source hash mismatch')
headers=re.findall(r'^## (Q\d{2})$',source,re.M)
if headers!=[f'Q{i:02d}' for i in range(1,13)]: fail.append(f'question headers {headers}')
def qblock(q):
 m=re.search(rf'^## {q}\n\n(.*?)(?=\n## Q\d{{2}}\n|\Z)',source,re.M|re.S); t=m.group(1).strip()
 if q=='Q12': t=t.split('\n\nQ12 is deliberately supplied exactly as written.')[0].strip()
 return t
full={a['source_ref']:a['text'] for a in atoms if a['kind']=='source_question_full'}
for q in headers:
 if full.get(q)!=qblock(q): fail.append(f'{q} full atom differs from source block')
# Independent source structure counts from original corpus.
subparts={q:max(1,len(re.findall(r'\([a-d]\)',qblock(q)))) for q in headers}
invsp=collections.Counter(a['source_ref'] for a in atoms if a['kind']=='source_subpart')
for q,n in subparts.items():
 if invsp[q]!=n: fail.append(f'{q} subparts source={n} inventory={invsp[q]}')
expected_data={'Q01':3,'Q02':5,'Q03':3,'Q04':5,'Q05':5,'Q06':5,'Q07':5,'Q08':5,'Q09':7,'Q10':4,'Q11':5,'Q12':4}
invdata=collections.Counter(a['source_ref'] for a in atoms if a['kind']=='source_datum_or_condition')
if dict(invdata)!=expected_data: fail.append(f'data/condition count mismatch {dict(invdata)}')
conv_para=re.search(r'## Conventions supplied with the corpus\n\n(.*?)\n\n## Q01',source,re.S).group(1)
convs=[a for a in atoms if a['kind']=='source_condition']
if len(convs)!=7: fail.append(f'convention atom count {len(convs)}')
def canon_conv(t):
 t=t.rstrip('.').replace('Ground frame is used','Ground frame').replace('+x is east and +y is north','+x east and +y north').replace('times are in seconds','times in seconds')
 return t
for a in convs:
 if canon_conv(a['text']) not in canon_conv(conv_para): fail.append(f'convention not reconciled: {a["atom_id"]}')
# Q02 table is independently parsed as four rows.
table_rows=re.findall(r'^\|\s*(0|2|4|6)\s*\|\s*(-?\d+)\s*\|\s*(-?\d+)\s*\|$',qblock('Q02'),re.M)
if table_rows!=[('0','0','0'),('2','6','8'),('4','12','16'),('6','12','16')]: fail.append(f'Q02 table parse {table_rows}')
kind_counts=collections.Counter(a['kind'] for a in atoms)
expected_kinds={'source_condition':7,'contract_concept':27,'equation':11,'visual_relationship':8,'research_support':4,'source_question_full':12,'source_subpart':33,'source_datum_or_condition':56,'source_quality_status':1}
if dict(kind_counts)!=expected_kinds: fail.append(f'kind denominator mismatch {dict(kind_counts)}')
if len(atoms)!=159: fail.append(f'atom total {len(atoms)}')
print(json.dumps({'status':'PASS' if not fail else 'FAIL','source_sha256':inv['source_corpus_sha256'],'question_headers':headers,'subpart_counts':subparts,'q02_table_rows':table_rows,'kind_counts':dict(kind_counts),'atom_total':len(atoms),'failures':fail},indent=2))
sys.exit(1 if fail else 0)
