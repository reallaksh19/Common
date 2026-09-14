from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from pypdf import PdfReader, PdfWriter
R=Path(__file__).resolve().parent; W,H=A4; M=42
INK=colors.HexColor('#17212B'); MUT=colors.HexColor('#5D6974'); B=colors.HexColor('#1F5A94'); T=colors.HexColor('#1B7F79'); O=colors.HexColor('#B36A12'); L=colors.HexColor('#F4F7F9'); P=colors.HexColor('#EAF2F8'); G=colors.HexColor('#EDF7F1'); WARM=colors.HexColor('#FFF5E8'); GRID=colors.HexColor('#CCD6DD')
def wrap(s,f='Helvetica',z=9,w=480):
 q=[]; line=''
 for a in str(s).split():
  t=a if not line else line+' '+a
  if stringWidth(t,f,z)<=w: line=t
  else: q.append(line); line=a
 if line:q.append(line)
 return q
def txt(c,s,x,y,w,z=9,lead=11,f='Helvetica',col=INK):
 c.setFillColor(col); c.setFont(f,z)
 for a in wrap(s,f,z,w): c.drawString(x,y,a); y-=lead
 return y
def head(c,title,layer,n,total,sub=''):
 c.setFillColor(colors.white); c.rect(0,0,W,H,fill=1,stroke=0); c.setFillColor(T); c.setFont('Helvetica-Bold',8.5); c.drawString(M,H-38,layer.upper()); c.setFillColor(INK); c.setFont('Helvetica-Bold',19); c.drawString(M,H-63,title)
 if sub: txt(c,sub,M,H-82,W-2*M,9.2,11,col=MUT)
 c.setStrokeColor(colors.HexColor('#D8E0E5')); c.line(M,28,W-M,28); c.setFillColor(MUT); c.setFont('Helvetica',7); c.drawString(M,16,'Review sample: projectile vertical-event / apex reasoning'); c.drawRightString(W-M,16,f'Page {n} of {total}')
def box(c,t,s,y,h=72,fill=L):
 c.setFillColor(fill); c.setStrokeColor(GRID); c.roundRect(M,y-h,W-2*M,h,7,fill=1,stroke=1); c.setFillColor(B); c.setFont('Helvetica-Bold',9.2); c.drawString(M+10,y-16,t); txt(c,s,M+10,y-32,W-2*M-20,8.9,11); return y-h-14
def linebox(c,y,n=5):
 c.setStrokeColor(GRID)
 for i in range(n): c.line(M,y-18*i,W-M,y-18*i)
def hints(c,y,hs):
 c.setFillColor(O); c.setFont('Helvetica-Bold',8); c.drawString(M,y,'SELF-GUIDED HELP - USE ONLY IF NEEDED'); y-=12
 for i,s in enumerate(hs,1):
  c.setFillColor(WARM); c.roundRect(M,y-34,W-2*M,34,5,fill=1,stroke=0); c.setFillColor(O); c.setFont('Helvetica-Bold',8); c.drawString(M+8,y-13,f'H{i}'); txt(c,s,M+42,y-12,W-2*M-54,8.2,10); y-=40
 return y
def ans(c,title,items,h=105):
 y=40; c.setFillColor(G); c.roundRect(M,y,W-2*M,h,7,fill=1,stroke=0); c.setFillColor(T); c.setFont('Helvetica-Bold',8.4); c.drawString(M+10,y+h-16,'CHECK AFTER ATTEMPT - '+title.upper()); yy=y+h-31
 for s in items: yy=txt(c,s,M+10,yy,W-2*M-20,8.3,10.3)-1
def brochure(name,layer,pages):
 c=canvas.Canvas(str(R/name),pagesize=A4); N=len(pages)
 for n,(title,sub,boxes) in enumerate(pages,1):
  if n>1:c.showPage()
  head(c,title,layer,n,N,sub); y=H-118
  for t,s,fill in boxes:y=box(c,t,s,y,82 if len(s)>150 else 68,fill)
 c.save()
def workbook(name,layer,qs):
 c=canvas.Canvas(str(R/name),pagesize=A4); N=len(qs)
 for n,(title,prompt,hs,sol) in enumerate(qs,1):
  if n>1:c.showPage()
  head(c,title,layer,n,N,'Open-ended attempt -> optional H1/H2/H3 -> same-page worked check.'); y=H-118; y=box(c,'Open-ended question',prompt,y,84,WARM); c.setFillColor(T); c.setFont('Helvetica-Bold',8); c.drawString(M,y,'YOUR RESPONSE'); linebox(c,y-14,5); y-=112; hints(c,y,hs); ans(c,title,sol)
 c.save()
core1=[('Semantic core','What is true, under what conditions?',[('Stable claim','With negligible air resistance and constant g, vertical velocity changes uniformly: v_y=u_y+a_y t; with upward positive, a_y=-g.',P),('Apex boundary','At the apex v_y=0 but a_y=-g; horizontal velocity may remain nonzero.',G),('Authority boundary','Core1 does not choose pedagogy, infer mastery, or authorize transfer.',WARM)]),('Representation invariants','Same meaning across forms.',[('Story','Gravity changes v_y by the same signed amount each second.',L),('Table/graph','Equal time steps give equal Delta v_y; the v_y-t graph is a straight line whose slope is a_y.',P),('Misconceptions','Downward acceleration does not mean downward motion; a v_y-t graph is not the trajectory.',WARM)]),('Core1 handoff','Stable semantics only.',[('Downstream','Core1A teaches; Core1B gathers learner evidence; Core2 describes challenge structure; Core2A authorizes transfer; Core2B runs transfer.',G)])]
core1a=[('Teaching target','What must be built and repaired?',[('Capability','Track v_y through flight; distinguish velocity/acceleration; recognise apex; connect story, table, graph and equation.',P),('Difficulty','Learners confuse negative acceleration with downward motion and apex with zero acceleration.',WARM)]),('Meaning before formula','Build the physical idea first.',[('Phenomenon','A projectile may move upward while acceleration points downward.',L),('Bridge','story -> signed change -> table -> v_y-t graph -> v_y=u_y+a_y t.',G)]),('Progression','Fade support deliberately.',[('Worked','t=1 s, v_y=12, a_y=-10 -> u_y=22 m/s.',P),('Faded','t=2 s, v_y=6, a_y=-9 -> learner completes rearrangement.',L),('Independent','t=3 s, v_y=3, a_y=-9 -> learner chooses model, solves, explains applicability and checks.',G)]),('Core1A handoff','Teaching authority, not mastery.',[('Invariant','One clock; signed vertical velocity; constant downward acceleration; apex v_y=0.',G),('Boundary','Publication never proves learner mastery.',WARM)])]
q1b=[('Prediction','v_y=+2 m/s, a_y=-10 m/s^2. Predict v_y one second later and explain.',('Acceleration tells change, not motion direction now.','One second changes v_y by -10.','Add +2 and -10.'),('v_y=-8 m/s.','The projectile is then moving downward.')),('Read the pattern','time 0,1,2,3 s; v_y +22,+12,+2,-8. Find a_y and when direction changes.',('Compare equal one-second intervals.','Velocity drops by the same amount each second.','Use a=Delta v/Delta t; direction changes at v_y=0.'),('a_y=-10 m/s^2.','Direction changes between 2 and 3 s.')),('Worked reconstruction','At t=1 s, v_y=+12, a_y=-10. Find u_y.',('Use one clock.','Take upward positive.','12=u_y-10.'),('u_y=22 m/s upward.','Check: 22-10=12.')),('Independent use','At t=3 s, v_y=+3, a_y=-9. Find u_y, state applicability, check.',('Recognise the event-clock structure.','Use signed constant acceleration.','3=u_y-27.'),('u_y=30 m/s upward.','Model applies because vertical acceleration is constant and time is from launch.')),('Apex integrity','At the highest point, what are v_y and a_y, and why does the projectile fall afterward?',('Separate velocity from acceleration.','Zero velocity at an instant does not imply zero acceleration.','Gravity remains downward.'),('At apex v_y=0 and a_y=-g.','Gravity drives v_y negative immediately afterward.'))]
core2=[('Challenge semantics','What hidden structure does the problem demand?',[('Anchor demand','Given v_y at a stated elapsed time, infer another event variable using one global clock and signed constant-acceleration reasoning.',P),('Hidden structure','recognise family -> choose sign -> place event on clock -> select equation -> solve target -> verify.',G)]),('Transfer envelope','Surface may change while structure stays.',[('Variations','Near transfer, reversed target, event identification, representation shift, multi-step bridge.',L),('Demand dimensions','Structural distance, representation change, model discrimination, multi-step bridge, synthesis, competitive mixing.',P),('Boundary','A scalar T0-T8 label cannot be the sole authorizer.',WARM)]),('Core2 handoff','Challenge semantics only.',[('Contribution','Problem-family identity, first-step reference, hint semantics, solution/verification requirements and transfer dimensions.',G)])]
core2a=[('Legal pool input','What transfer is permissible?',[('Receipt','Projectile vertical-event teaching complete; learner evidence unknown.',P),('Rule','Teaching completion permits compilation only for supported families/purposes; it does not prove transfer.',WARM)]),('Legal candidates','Generated transfer under exact custody.',[('Near','v_y=6 at t=2 s, a_y=-9 -> find u_y. Expected 24 m/s.',G),('Reversed target','u_y=30, v_y=3, a_y=-9 -> find t. Expected 3 s.',G)]),('Fail-closed boundary','No silent expansion.',[('Legal','Direct, near transfer, reversed target.',G),('Not in pool','New representation, synthesis or competitive mixing without supporting authority/evidence.',WARM)])]
q2b=[('Direct recognition','v_y=+12 at t=1 s, a_y=-10. Find u_y.',('Place launch and event on one clock.','Use signed vertical constant acceleration.','12=u_y-10.'),('u_y=22 m/s upward.','This is direct recognition of the taught structure.')),('Near transfer','v_y=+6 at t=2 s, a_y=-9. Find u_y.',('Do not invent a new model because numbers changed.','Keep the same sign and clock.','6=u_y-18.'),('u_y=24 m/s upward.','Surface numbers changed; hidden structure did not.')),('Reversed target','u_y=30, later v_y=+3, a_y=-9. Find t.',('Target changed; physics did not.','Use the same relation for a different unknown.','3=30-9t.'),('t=3 s.','Same invariant, different target.')),('Model selection','Which needs this model: horizontal range; infer u_y from later v_y and t; centripetal acceleration?',('Look for stated vertical velocity at stated time.','This capability is signed one-dimensional vertical velocity under constant acceleration.','The second option matches.'),('The vertical-event option is the match.','Core2B tests recognition and selection, not only algebra.')),('Exit robustness','u_y=36, v_y=0, a_y=-9. What event is this and when?',('What event has v_y=0?','Use the same one-clock signed model.','0=36-9t.'),('Apex event; t=4 s.','Event recognition + model selection + changed target.'))]
val=[('Six-layer distinction','Each layer answers a different question.',[('Core1','What is true?',P),('Core1A','What must be taught?',L),('Core1B','Can learner reconstruct/use it?',G),('Core2','What challenge structure exists?',P),('Core2A','What transfer is legal?',L),('Core2B','Can learner recognise/select/transfer?',G)]),('Authority leakage audit','Downstream cannot create upstream authority.',[('PASS','Core1A publication does not prove mastery; Core1B cannot create legality; Core2A does not prove mastery; Core2B cannot expand the legal pool.',G)]),('Verdict','Process-golden validation.',[('PASS','Architecture is coherent and operational.',G),('LIMIT','This does not prove real learner efficacy.',WARM),('NEXT','Pilot with real responses; record hint use, failure dimension and repair success on a different transfer item.',P)])]
def main():
 files=[('SAMPLE-Projectile-Vertical-Event-Core1-v1.pdf',lambda p:brochure(p,'Core1 - source-grounded semantics',core1)),('SAMPLE-Projectile-Vertical-Event-Core1A-v1.pdf',lambda p:brochure(p,'Core1A - teaching authority',core1a)),('SAMPLE-Projectile-Vertical-Event-Core1B-v1.pdf',lambda p:workbook(p,'Core1B - self-guided reconstruction',q1b)),('SAMPLE-Projectile-Vertical-Event-Core2-v1.pdf',lambda p:brochure(p,'Core2 - source-grounded challenge model',core2)),('SAMPLE-Projectile-Vertical-Event-Core2A-v1.pdf',lambda p:brochure(p,'Core2A - transfer legality',core2a)),('SAMPLE-Projectile-Vertical-Event-Core2B-v1.pdf',lambda p:workbook(p,'Core2B - self-guided transfer',q2b)),('SAMPLE-Projectile-Vertical-Event-Process-Validation-v1.pdf',lambda p:brochure(p,'Process validation',val))]
 for n,f in files:f(R/n)
 w=PdfWriter()
 for n,_ in files:
  for p in PdfReader(str(R/n)).pages:w.add_page(p)
 with open(R/'SAMPLE-Projectile-Vertical-Event-Full-Six-Layer-Process-v1.pdf','wb') as f:w.write(f)
if __name__=='__main__':main()
