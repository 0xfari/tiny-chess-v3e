import json,os,sys,time,random as R,urllib.request as u
E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
ND=(-33,-31,-18,-14,14,18,31,33)
KD=(-17,-16,-15,-1,1,15,16,17)
BD=(-17,-15,15,17)
RD=(-16,-1,1,16)
MG=("","FFFFFFFFZaRYT_MDEGKLSQKBCIGJKHIAAFEHIGHAAEEDGGMD?FBACKNBFFFFFFFF","%4?<R3C17>TMKRGC=RMSW`UODIJQMTJJCGIILJJDADHHJIKC@;DEFJCB1B:?C@BA","@G6?A>GDAIBCLRJ=CMONMPMFEGJPMMGFEIIKMHHGFIIIIKJHGIIFGJMF?ECBCD>B","LNLPSHLOKLRRVSKOEJKMIORIADGKKMDB?ADFHEGA=ACCGFE?=CBDFHE8BCFIIG?A","@FLHROOOA>EFCQLQCCGHLQOQAACCFIFFDADDFEGECFDFEFIG?DHFHIEFFBDHCA@<","9KIC;?FILFBEDE>@DKFCBGJBCBDA@AC?<FA>==?<CCB==@CAFGD9=CHHCMH;H@KI")
EG=("","FFFFFFFFjifac`gkYZWSQQVWLKIGFGIIIHEEEDGFGGEFFEFDIHHHIFFEFFFFFFFF",":>C@@A92ADAFDAA<ABHHFDB>CGJJJHHBBEIKIIGBAEFIHEBB>BDEFBA=@<ACBB<9","CBDDEDCADEGDECECFDFFFGFGEHHHIHGFEGIJGHEDDEHHIGECCBEFGDCAADAEDCEC","IHJIHHHGHIIHEGHGGGGGGEEEGGIFFFFFGGHGEEDDEFEFEDDCEEFFDDDEDFGFECGB","DJJKKJHJCJLNRKLFBGHPOMJHGJKOQNQMBLJOLMNKCAIGHIHGBA@CCA?@?@B=E@B>","7?BBDIGCDIIIINKHHIKIJOOIDJKKKMKGBEJKKKHDBEHJKIGDADGIIGEC;?BD@CA=")
VM=(0,82,337,365,477,1025,0)
VE=(0,94,281,297,512,936,0)
MT=[tuple(ord(c)-70 for c in r) for r in MG]
ET=[tuple(ord(c)-70 for c in r) for r in EG]
PHV=(0,0,1,1,2,4,0)
GV=[0]*2048;HV=[0]*2048
for p in range(16):
 for q in range(128):
  t=p&7
  if 0<t<7:
   o=p*128+q;i=((q>>4) if p&8 else 7-(q>>4))*8+(q&7);x=1-(p>7)*2
   GV[o]=x*(VM[t]+5*MT[t][i]);HV[o]=x*(VE[t]+5*ET[t][i])
MVV=[[VM[v]*10-VM[a]//10 for a in range(7)] for v in range(7)]
SQ=tuple(s for s in range(128) if not s&136)
B=[0]*128
S=[0,15,-1,0,4,116]
rep={};TT={};KL=[0]*1024;H=[0]*98304;nodes=0;NODES=60000;RB=0;ZK=0;MG=0;EG=0;PH=24;BW=2;BB=2;CT=0
CM=[0]*128
for a,b in((4,3),(116,12),(0,2),(7,1),(112,8),(119,4)):CM[a]=b
PD=((-15,-17),(15,17))
R.seed(1);ZR=[R.getrandbits(64) for _ in range(2048)]
def att(s,w):
 b=B
 for D,v in((PD[w>>3],1),(ND,2),(KD,6),(BD,3),(RD,4)):
  for d in D:
   t=s+d
   while not t&136:
    q=b[t]
    if q:
     if q==v+w or v>2 and q==5+w:return 1
     break
    if v%5<3:break
    t+=d
 return 0
def gen(c=0):
 b=B;w=S[0];ms=[];ap=ms.append
 for s in SQ:
  p=b[s]
  if not p or p&8!=w:continue
  t=p&7
  if t==1:
   d=16 if w==0 else -16
   t1=s+d
   if not t1&136 and not b[t1]:
    r=t1>>4
    if r==0 or r==7:
     for q in (5,4,3,2):ap(s|t1<<7|q<<14)
    elif not c:
     ap(s|t1<<7)
     if (s>>4)==(1 if w==0 else 6):
      t2=s+2*d
      if not b[t2]:ap(s|t2<<7)
   for dd in (d-1,d+1):
    t1=s+dd
    if t1&136:continue
    q=b[t1]
    if q and q&8!=w or t1==S[2]:
     r=t1>>4
     if r==0 or r==7:
      for x in (5,4,3,2):ap(s|t1<<7|x<<14)
     else:ap(s|t1<<7)
  elif t==2 or t==6:
   D=ND if t==2 else KD
   for d in D:
    t1=s+d
    if t1&136:continue
    q=b[t1]
    if not q and not c or q and q&8!=w:ap(s|t1<<7)
   if t==6 and not c:
    for K,C,E,R,T,A in((4,1,(5,6),7,6,(4,5,6)),(4,2,(3,2,1),0,2,(4,3,2)),(116,4,(117,118),119,118,(116,117,118)),(116,8,(115,114,113),112,114,(116,115,114))):
     if s==K and S[1]&C and b[R]==4+w and not any(b[e] for e in E) and not any(att(a,w^8) for a in A):ap(K|T<<7)
  else:
   D=BD if t==3 else RD if t==4 else BD+RD
   for d in D:
    t1=s+d
    while not t1&136:
     q=b[t1]
     if q:
      if q&8!=w:ap(s|t1<<7)
      break
     if not c:ap(s|t1<<7)
     t1+=d
 return ms
def make(m):
 global ZK,MG,EG,PH,BW,BB
 b=B;s=S;f=m&127;t=m>>7&127;pr=m>>14
 p=b[f];un=(m,b[t],s[1],s[2],s[3],s[4],s[5],ZK)
 o=p*128;dmg=GV[o+t]-GV[o+f];deg=HV[o+t]-HV[o+f];dph=0;dbw=0;dbb=0
 if un[1]:
  c=un[1];u2=c*128;dmg-=GV[u2+t];deg-=HV[u2+t];dph-=PHV[c&7]
  if c&7==3:
   if c&8:dbb-=1
   else:dbw-=1
 ZK^=ZR[p*128+f]^ZR[p*128+t]^ZR[1817]
 if un[1]:ZK^=ZR[un[1]*128+t]
 b[t]=p;b[f]=0
 if pr:
  np=pr|(p&8);ZK^=ZR[p*128+t]^ZR[np*128+t];b[t]=np
  dmg+=GV[np*128+t]-GV[o+t];deg+=HV[np*128+t]-HV[o+t];dph+=PHV[pr]
  if pr==3:
   if p&8:dbb+=1
   else:dbw+=1
 if p&7==1 and t==s[2] and not un[1]:
  e=t+(-16 if p&8==0 else 16);ZK^=ZR[b[e]*128+e];dmg-=GV[b[e]*128+e];deg-=HV[b[e]*128+e];b[e]=0
 if p&7==6:
  if p&8==0:s[4]=t
  else:s[5]=t
  if abs(t-f)==2:
   if t>f:
    rk=b[f+3];dmg+=GV[rk*128+f+1]-GV[rk*128+f+3];deg+=HV[rk*128+f+1]-HV[rk*128+f+3]
    ZK^=ZR[b[f+3]*128+f+3]^ZR[b[f+3]*128+f+1];b[f+1]=b[f+3];b[f+3]=0
   else:
    rk=b[f-4];dmg+=GV[rk*128+f-1]-GV[rk*128+f-4];deg+=HV[rk*128+f-1]-HV[rk*128+f-4]
    ZK^=ZR[b[f-4]*128+f-4]^ZR[b[f-4]*128+f-1];b[f-1]=b[f-4];b[f-4]=0
 oc=s[1];s[1]&=~CM[f]&~CM[t]
 if s[1]!=oc:ZK^=ZR[1792+oc]^ZR[1792+s[1]]
 oe=s[2];s[2]=f+(16 if p&8==0 else -16) if p&7==1 and abs(t-f)==32 else -1
 if oe!=s[2]:ZK^=ZR[1808+(oe&7)+1 if oe!=-1 else 1808]^ZR[1808+(s[2]&7)+1 if s[2]!=-1 else 1808]
 s[3]=0 if p&7==1 or un[1] else s[3]+1
 s[0]^=8
 rep[ZK]=rep.get(ZK,0)+1
 MG+=dmg;EG+=deg;PH+=dph;BW+=dbw;BB+=dbb
 return un+(dmg,deg,dph,dbw,dbb)
def unmake(un):
 global ZK,MG,EG,PH,BW,BB
 b=B;s=S;m,cap,c,e,h,kw,kb,zk,dmg,deg,dph,dbw,dbb=un
 f=m&127;t=m>>7&127;pr=m>>14
 p=b[t]
 rep[ZK]-=1
 b[t]=cap
 b[f]=(1 if pr else p&7)|(p&8)
 if p&7==6 and abs(t-f)==2:
  if t>f:b[f+3]=b[f+1];b[f+1]=0
  else:b[f-4]=b[f-1];b[f-1]=0
 if p&7==1 and t==e and not cap:b[t+(-16 if p&8==0 else 16)]=9 if p&8==0 else 1
 s[1]=c;s[2]=e;s[3]=h;s[4]=kw;s[5]=kb;s[0]^=8;ZK=zk;MG-=dmg;EG-=deg;PH-=dph;BW-=dbw;BB-=dbb
def ev():
 mg=MG;eg=EG;kw=S[4];kb=S[5]
 for k,v,s in((kw,1,1),(kb,9,-1)):
  for dd in(15,16,17):
   t=k+s*dd
   if not t&136 and B[t]==v:mg+=15*s;eg+=15*s
 if BW>1:mg+=25;eg+=25
 if BB>1:mg-=25;eg-=25
 if PH>=24:return mg
 return (mg*PH+eg*(24-PH))//24
def order(ms,tt,ply):
 k=KL[ply]
 o=[(1e5 if m==tt else 1e4+MVV[t&7][B[m&127]&7] if (t:=B[m>>7&127]) else 9000 if m==k else H[m],m) for m in ms]
 o.sort(reverse=True)
 return [m for _,m in o]
class AB(Exception):pass
def qs(al,be,ply):
 global nodes
 nodes+=1
 if nodes>NODES:raise AB
 w=S[0]
 if S[3]>=100:return 0
 chk=att(S[4] if w==0 else S[5],w^8)
 if not chk:
  s=ev()*(1 if w==0 else -1)+10
  if s>=be:return be
  if s>al:al=s
  ms=order(gen(1),0,ply)
 else:ms=order(gen(),0,ply)
 best=-1e5
 for mv in ms:
  un=make(mv)
  if not att(S[4] if w==0 else S[5],w^8):
   sc=-qs(-be,-al,ply+1)
   if sc>best:best=sc
   if sc>al:al=sc
   if al>=be:unmake(un);return be
  unmake(un)
 if chk:
  return -2e4+ply if best==-1e5 else best
 return al
def sr(d,al,be,ply):
 global nodes,RB,ZK
 nodes+=1
 if nodes>NODES:raise AB
 w=S[0]
 if S[3]>=100:return 0
 if rep.get(ZK,0)>1:return CT
 chk=att(S[4] if w==0 else S[5],w^8)
 if chk:d+=1
 if d<=0:return qs(al,be,ply)
 e=TT.get(ZK)
 if e and e[0]>=d:
  s,f,mv=e[1],e[2],e[3]
  if f==0:return s
  if f==1 and s>=be:return s
  if f==2 and s<=al:return s
 if d>=3 and not chk:
  s=ev()*(1 if w==0 else -1)
  if s>=be and PH>=5:
   ep=S[2];z=ZR[1808+(ep&7)+1]^ZR[1808] if ep!=-1 else 0;S[0]^=8;S[2]=-1;ZK^=ZR[1817]^z
   sc=-sr(d-3,-be,-be+1,ply+1)
   S[0]^=8;S[2]=ep;ZK^=ZR[1817]^z
   if sc>=be:return be
 ms=order(gen(),e[3] if e else 0,ply)
 best=-1e5;bestm=0;fl=2;i=0
 for mv in ms:
  un=make(mv)
  if att(S[4] if w==0 else S[5],w^8):
   unmake(un);continue
  if i:
   r=2 if i>2 and d>2 and not chk and not un[1] and not mv>>14 else 1
   sc=-sr(d-r,-al-1,-al,ply+1)
   if r>1 and sc>al:sc=-sr(d-1,-al-1,-al,ply+1)
   if al<sc<be:sc=-sr(d-1,-be,-al,ply+1)
  else:sc=-sr(d-1,-be,-al,ply+1)
  if sc>best:best,bestm=sc,mv
  if sc>al:al=sc;fl=0
  if al>=be:
   fl=1
   if not un[1] and not mv>>14:
    KL[ply]=mv;H[mv]+=d*d
   unmake(un);break
  unmake(un);i+=1
 if best==-1e5:
  return -2e4+ply if chk else 0
 TT[ZK]=(d,best,fl,bestm)
 if ply==0:RB=bestm
 return best
def start():
 b=[0]*128;bk=(4,2,3,5,6,3,2,4)
 for f,k in enumerate(bk):b[f]=k;b[f+112]=k+8;b[f+16]=1;b[f+96]=9
 return b
def u2m(a):
 pr='  nbrq'.find(a[4:])
 return (ord(a[0])-97+(ord(a[1])-49)*16)|(ord(a[2])-97+(ord(a[3])-49)*16)<<7|pr<<14
def m2u(m):
 f=m&127;t=m>>7&127;pr=m>>14
 s=chr(97+(f&7))+str(1+(f>>4))+chr(97+(t&7))+str(1+(t>>4))
 return s+('  nbrq'[pr] if pr else '')
def zinit():
 global ZK
 z=0
 for q in SQ:
  p=B[q]
  if p:z^=ZR[p*128+q]
 z^=ZR[1792+S[1]]
 if S[2]!=-1:z^=ZR[1808+(S[2]&7)+1]
 ZK=z
def decide(g):
 global B,S,rep,nodes,RB,MG,EG,PH,BW,BB,CT,NODES,H
 B=start();S=[0,15,-1,0,4,116];rep={};zinit();rep[ZK]=1;MG=0;EG=0;PH=24;BW=2;BB=2
 for a in g["moves"]:
  make(u2m(a))
 legal=g["legal_moves"]
 if len(legal)==1:return legal[0]
 if len(rep)<11 or len(TT)>4e5:TT.clear();H=[0]*98304
 if g.get("game"):
  NODES,CT=((4e4,0),(4e4,0),(15e4,0),(15e4,25),(12e4,35),(6e4,45),(4e4,45),(4e4,45))[g["game"]-1]
 nodes=0;best=legal[0]
 try:
  for d in range(1,13):
   sr(d,-1e6,1e6,0)
   if RB:best=m2u(RB)
 except AB:pass
 return best if best in legal else legal[0]
OP=u.build_opener(u.ProxyHandler({}))
def post(p,d):
 for _ in range(3):
  try:
   r=OP.open(u.Request(E+p,data=json.dumps(d).encode()),timeout=5)
   if r.status==200:return json.load(r)
  except Exception as e:print(e,file=sys.stderr)
  time.sleep(.3)
 raise IOError
def main():
 while 1:
  try:g=post("/game",{})
  except Exception as e:print(e,file=sys.stderr);time.sleep(1);continue
  if g.get("status")=="done":break
  while g.get("status")=="your_move":
   try:mv=decide(g)
   except Exception as e:
    print(e,file=sys.stderr);mv=(g.get("legal_moves") or [None])[0]
   if not mv:break
   try:g=post("/move",{"game":g["game"],"move":mv})
   except Exception as e:
    print(e,file=sys.stderr)
    try:g=post("/game",{})
    except Exception:time.sleep(1)
    break
if __name__=="__main__":main()
