"""2021-now glass candles. Fast growth, then a full-bar pause before the next bar."""
import array,bisect,hashlib,json,math,random,struct,wave
from pathlib import Path
root=Path(__file__).resolve().parents[1];raw=json.loads((root/'src/shibao-2021-v4.json').read_text(encoding='utf-8'));n=len(raw)
cl=[float(r[2]) for r in raw]
ret1=[0.]+[cl[i]/cl[i-1]-1 for i in range(1,n)]
ret5=[cl[i]/cl[max(0,i-5)]-1 for i in range(n)]
hot=[i for i in range(5,n) if abs(ret1[i])>=.075 and abs(ret5[i])>=.15]
hotset=set(hot);intro=42;end=804;growth_frames=2;hold_frames=8
remaining=end-intro-len(hot)*10;ordinary=n-len(hot)
assert remaining>0
# Quiet sessions are compressed, critical bars always get 2 growth + 8 completed frames.
segments=[];events=[];f=intro;acc=0
for i in range(n):
 if i in hotset: dur=10
 else:
  acc+=remaining;dur=acc//ordinary;acc%=ordinary
 if dur:
  segments.append(dict(index=i,start=f,end=f+dur,critical=i in hotset))
  if i in hotset:events.append(dict(index=i,start=f,frame=f+growth_frames,end=f+dur,date=raw[i][0],changeDay=ret1[i],change=ret5[i]))
  f+=dur
assert f==end,(f,end)
frames=[];x=0.;cy=-cl[0]*28;sx=4.;sy=9.;anchorx=760.;bank=0.
starts=[s['start'] for s in segments]
for f in range(900):
 if f<intro:idx=0;growth=1.;critical=False;phase='intro';local=0
 elif f>=end:idx=n-1;growth=1.;critical=False;phase='outro';local=0
 else:
  seg=segments[bisect.bisect_right(starts,f)-1];idx=seg['index'];critical=seg['critical'];local=f-seg['start']
  growth=min(1.,local/growth_frames) if critical else 1.
  # One uninterrupted fast ease-out, followed by a separate completed-bar hold.
  growth=1-(1-growth)**3
  phase=('grow' if growth<1 else 'hold') if critical else 'fast'
 settled=idx if growth>=1 else max(0,idx-1)
 op=float(raw[idx][1]);price=op+(cl[idx]-op)*growth
 c5=ret5[idx];power=max(0.,min(1.,(abs(c5)-.10)/.35));power=max(power,.75 if critical else 0.)
 lookback=round(42-23*power)
 recent=raw[max(0,idx-lookback+1):idx+1];hi=max(float(r[3]) for r in recent);lo=min(float(r[4]) for r in recent)
 span=max(hi-lo,max(.45,price*.055));mid=(hi+lo)/2
 sx+=(900/(lookback*6)-sx)*.20;sy+=(600/(span*28)-sy)*.17
 x+=(idx*6-x)*.32;cy+=(-mid*28-cy)*.25
 anchorx+=(760+max(-1,min(1,c5/.25))*25-anchorx)*.16
 x=max(x,idx*6-(925-anchorx)/sx)
 bank+=(max(-1.6,min(1.6,c5*3.5))-bank)*.16
 high=float(raw[idx][3]);low=float(raw[idx][4]);sy=min(sy,650/max(.001,(high-low)*28))
 top=1170+(-high*28-cy)*sy;bottom=1170+(-low*28-cy)*sy
 if top<850:cy-=(850-top)/sy
 if bottom>1500:cy+=(bottom-1500)/sy
 impulse=max([math.exp(-(f-e['frame'])/3.0) for e in events if 0<=f-e['frame']<10] or [0.])
 frames.append(dict(index=idx,settledIndex=settled,price=price,change5=c5,changeDay=ret1[idx],growth=growth,phase=phase,critical=critical,cx=x,cy=cy,sx=sx,sy=sy,anchorX=anchorx,bank=bank,power=power,impact=impulse,lookback=lookback))
plan=dict(fps=30,frames=frames,events=events,segments=segments,growthFrames=growth_frames,holdFrames=hold_frames,introEnd=intro,playEnd=end,start=raw[0][0],end=raw[-1][0],minLow=min(float(r[4]) for r in raw),maxHigh=max(float(r[3]) for r in raw),minClose=min(cl),maxClose=max(cl),firstClose=cl[0],lastClose=cl[-1],totalReturn=cl[-1]/cl[0]-1,sourceSha256=hashlib.sha256((root/'src/shibao-2021-v4.json').read_bytes()).hexdigest())
(root/'src/shibao-v4-plan.json').write_text(json.dumps(plan,ensure_ascii=False,separators=(',',':')), encoding='utf-8')
# New timbre: digital FM transients, rising/falling two-tone pings and sub impacts.
out=root/'public/shibao-v4';out.mkdir(exist_ok=True);sr=44100;count=sr*30;rng=random.Random(20261111)
L=array.array('f',[0.])*count;R=array.array('f',[0.])*count
for i in range(count):
 t=i/sr;fade=max(0.,min(1.,t/.7,(30-t)/1.1));base=[55.,65.406,73.416,49.][min(3,int(t/7.5))]
 phase=2*math.pi*base*t;fm=math.sin(phase+.8*math.sin(phase*2.003))
 beat=t%.5;hi=t%.25
 bed=.018*fm+.007*math.sin(phase*4+1.6*math.sin(phase*1.005))
 kick=.035*math.sin(2*math.pi*(48*beat+2*(1-math.exp(-beat*30))))*math.exp(-beat*30)
 hat=.006*(rng.random()*2-1)*math.exp(-hi*100)
 L[i]=(bed+kick+hat)*fade;R[i]=(bed+.005*math.sin(phase*2.01)+kick+hat)*fade
for e in events:
 onset=e['frame']/30;up=e['changeDay']>0;carrier=880. if up else 586.66
 phase=0.
 for j in range(int(sr*.29)):
  t=j/sr;freq=carrier*(1.+(.32 if up else -.22)*math.exp(-t*24));phase+=2*math.pi*freq/sr
  transient=.135*math.sin(phase+3.0*math.exp(-t*22)*math.sin(phase*1.414))*math.exp(-t*21)*min(1,t/.002)
  ping=.06*math.sin(2*math.pi*carrier*1.5*t)*math.exp(-max(0,t-.07)*29) if t>=.07 else 0.
  sub=.11*math.sin(2*math.pi*(51*t+2*(1-math.exp(-t*27))))*math.exp(-t*22)
  click=.026*(rng.random()*2-1)*math.exp(-t*80)
  v=transient+ping+sub+click;k=round(onset*sr)+j
  if 0<=k<count:L[k]+=v;R[k]+=v*.90
  echo=k+int(.065*sr)
  if 0<=echo<count:R[echo]+=transient*.24
 # Short electronic precharge, before completion; the strong cue is on the finished bar.
 for j in range(int(sr*.06)):
  t=j/sr;k=round((onset-.06)*sr)+j
  if 0<=k<count:
   v=.028*math.sin(2*math.pi*(900*t+4500*t*t))*(t/.06)**2
   L[k]+=v;R[k]+=v
with wave.open(str(out/'mix-raw.wav'),'wb') as w:
 w.setparams((2,2,sr,count,'NONE','not compressed'));b=bytearray()
 for l,r in zip(L,R):b.extend(struct.pack('<hh',int(max(-.92,min(.92,l))*32767),int(max(-.92,min(.92,r))*32767)))
 w.writeframes(b)
print('Range:',plan['start'],'to',plan['end'],'sessions:',n)
print('Critical bars:',len(events),'growth/hold:',growth_frames,hold_frames,'frames. Return:',round(plan['totalReturn']*100,2))
