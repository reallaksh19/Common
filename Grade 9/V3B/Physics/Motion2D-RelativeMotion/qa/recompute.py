from math import sqrt,isclose
import json,sys
checks=[]
def ck(id, got, expected, tol=1e-9):
 ok=isclose(got,expected,rel_tol=tol,abs_tol=tol); checks.append({'id':id,'got':got,'expected':expected,'pass':ok}); return ok
# Frozen corpus, recomputed from givens independently of authored solution strings.
ck('Q01-distance',6+8,14); ck('Q01-displacement',sqrt(6**2+8**2),10); ck('Q01-avgspeed',14/14,1); ck('Q01-avgvelmag',sqrt((6/14)**2+(8/14)**2),5/7)
ck('Q02-vx-0-4',12/4,3); ck('Q02-vy-0-4',16/4,4); ck('Q02-distance',10+10+0,20); ck('Q02-avg-vx',12/6,2); ck('Q02-avg-vy',16/6,8/3)
ck('Q03-x6',2+3*6,20); ck('Q03-y6',5-4*6,-19); ck('Q03-distance',sqrt(3**2+(-4)**2)*6,30)
ck('Q04-rel',8-5,3); ck('Q04-catch-time',30/(8-5),10); ck('Q04-place',8*10,80)
ck('Q05-meet-time',50/(6+4),5); ck('Q05-place',6*5,30); ck('Q05-rel',6-(-4),10)
ck('Q06-relmag',sqrt(3**2+(-4)**2),5); ck('Q06-sep10',sqrt((3*10)**2+(-4*10)**2),50)
# Q07 x and y candidate times differ -> no meeting.
ck('Q07-x-time',10/2,5); ck('Q07-y-time',0/(2-1) if (2-1)!=0 else 0,0)
ck('Q08-x-time',6/2,3); ck('Q08-y-time',4/2,2); ck('Q08-min-d2',8*(2.5-2.5)**2+2,2); ck('Q08-min-sep',sqrt(2),sqrt(2))
ck('Q09-speed',sqrt(4**2+3**2),5); ck('Q09-time',60/3,20); ck('Q09-drift',4*20,80); ck('Q09-path',5*20,100)
ck('Q10-relative-mag',sqrt((-8)**2+(-6)**2),10)
ck('Q11-conversion',36*5/18,10); ck('Q11-rel',10-2,8); ck('Q11-sep20',8*20,160)
checks.append({'id':'Q12-underdetermined','got':'directions absent','expected':'no unique relative velocity; conditional examples required','pass':True})
# Generated controls and extension.
ck('2A-Q07-meeting-x',2*4,8); ck('2A-Q07-meeting-y',1*4,4); ck('2A-Q08-time',48/4,12); ck('2A-Q08-drift',2*12,24); ck('2A-Q12-required-north-speed',40/(30/2),8/3)
ck('2B-Q07-xA',1*3,3); ck('2B-Q07-xB',6-1*3,3); ck('2B-Q07-yA',2*3,6); ck('2B-Q07-yB',9-1*3,6); ck('2B-Q12-planA-drift',2*(40/(8/3)),30)
ck('EXT-Q-001-gap', (16+5*12)-(-4+5*12),20)
fail=[x for x in checks if not x['pass']]
print(json.dumps({'status':'PASS' if not fail else 'FAIL','method':'independent recomputation from givens; same author execution, not an independent reviewer','checks':checks,'failures':fail},indent=2))
sys.exit(1 if fail else 0)
