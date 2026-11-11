"""Professional market captions, sourced catalysts, and tiered post-candle holds."""
import array,bisect,hashlib,json,math,random,struct,wave
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
root=Path(__file__).resolve().parents[1];raw=json.loads((root/'src/shibao-2021-v4.json').read_text(encoding='utf-8'));n=len(raw)
cl=[float(r[2]) for r in raw];lookup={}
for year in range(2021,2027):
 for r in json.loads((root/f'reference-analysis/v5/tencent-unadjusted-{year}.json').read_text(encoding='utf-8'))['data']['sz002703']['day']:lookup[r[0]]=r
actual=[lookup[r[0]] for r in raw];market=[];streak=0;last=-100;cluster_start=0;count=0
for i,r in enumerate(actual):
 prev=Decimal(actual[i-1][2]) if i else Decimal(r[2]);c=Decimal(r[2]);u=(prev*Decimal('1.1')).quantize(Decimal('.01'),rounding=ROUND_HALF_UP);dn=(prev*Decimal('.9')).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
 up=i>0 and c==u;down=i>0 and c==dn;prior=streak;streak=streak+1 if up else 0
 if up:
  if i-last>3:cluster_start=i;count=0
  count+=1;last=i
 span=i-cluster_start+1
 label=f'{streak}连板' if streak>=2 else (f'{span}天{count}板' if up and count>=3 else ('首板涨停' if up else ('跌停' if down else ('断板' if prior>=2 else ''))))
 change=float(c/prev-1) if i else 0.
 if not label and change<=-.06:label='长阴调整'
 if not label and change>=.06:label='放量上行' if i>=5 and float(r[5])>sum(float(x[5]) for x in actual[i-5:i])/5*1.5 else '强势上行'
 reported=r[0]=='2022-06-28'
 if reported:label='12天11板' # Contemporaneous report convention; see source note on 0.01 quote gap.
 market.append(dict(date=r[0],open=float(r[1]),close=float(r[2]),high=float(r[3]),low=float(r[4]),isUp=up,isDown=down,streak=streak,label=label,change=change,reported=reported))
(root/'src/shibao-v5-market.json').write_text(json.dumps(market,ensure_ascii=False,separators=(',',':')), encoding='utf-8')
ret1=[m['change'] for m in market];ret5=[cl[i]/cl[max(0,i-5)]-1 for i in range(n)]
windows=[('2022-06-13','2022-07-12'),('2023-06-30','2023-07-11'),('2025-12-16','2025-12-26')]
hot={i for i in range(5,n) if abs(ret1[i])>=.075 and abs(ret5[i])>=.15}
for i,m in enumerate(market):
 if any(a<=m['date']<=b for a,b in windows) and (m['isUp'] or m['isDown'] or m['label']=='断板' or m['reported']):hot.add(i)
extra={'2022-06-24':20,'2022-06-28':16,'2022-07-06':12,'2023-07-06':20,'2023-07-11':12,'2025-12-19':10,'2025-12-26':24}
intro=42;end=804;growth_frames=2;hold_frames=6
critical_durations={i:growth_frames+hold_frames+extra.get(raw[i][0],0) for i in hot}
remaining=end-intro-sum(critical_durations.values());ordinary=n-len(hot);assert remaining>0
segments=[];events=[];f=intro;acc=0
for i in range(n):
 if i in hot:dur=critical_durations[i]
 else:acc+=remaining;dur=acc//ordinary;acc%=ordinary
 if dur:
  segments.append(dict(index=i,start=f,end=f+dur,critical=i in hot))
  if i in hot:events.append(dict(index=i,start=f,frame=f+growth_frames,end=f+dur,date=raw[i][0],changeDay=ret1[i],change=ret5[i],label=market[i]['label']))
  f+=dur
assert f==end
frames=[];x=0.;cy=-cl[0]*28;sx=4.;sy=9.;anchorx=760.;bank=0.;starts=[s['start'] for s in segments]
for f in range(900):
 if f<intro:idx=0;growth=1.;critical=False;phase='intro';local=0
 elif f>=end:idx=n-1;growth=1.;critical=False;phase='outro';local=0
 else:
  seg=segments[bisect.bisect_right(starts,f)-1];idx=seg['index'];critical=seg['critical'];local=f-seg['start'];growth=min(1.,local/growth_frames) if critical else 1.;growth=1-(1-growth)**3;phase=('grow' if growth<1 else 'hold') if critical else 'fast'
 settled=idx if growth>=1 else max(0,idx-1);op=float(raw[idx][1]);price=op+(cl[idx]-op)*growth;c5=ret5[idx]
 power=max(0.,min(1.,(abs(c5)-.10)/.35));power=max(power,.75 if critical else 0.);lookback=round(42-23*power)
 recent=raw[max(0,idx-lookback+1):idx+1];hi=max(float(r[3]) for r in recent);lo=min(float(r[4]) for r in recent);span=max(hi-lo,max(.45,price*.055));mid=(hi+lo)/2
 # Settle the camera during the completed-candle pause, instead of indefinite drift.
 damping=.17 if phase!='hold' or local<9 else (.07 if local<16 else 0.)
 sx+=(900/(lookback*6)-sx)*damping;sy+=(600/(span*28)-sy)*damping
 x+=(idx*6-x)*min(.32,damping*1.7);cy+=(-mid*28-cy)*min(.25,damping*1.4)
 anchorx+=(760+max(-1,min(1,c5/.25))*25-anchorx)*damping;x=max(x,idx*6-(925-anchorx)/sx)
 bank+=(max(-1.6,min(1.6,c5*3.5))-bank)*damping
 high=float(raw[idx][3]);low=float(raw[idx][4]);sy=min(sy,650/max(.001,(high-low)*28));top=1170+(-high*28-cy)*sy;bottom=1170+(-low*28-cy)*sy
 if top<850:cy-=(850-top)/sy
 if bottom>1500:cy+=(bottom-1500)/sy
 impulse=max([math.exp(-(f-e['frame'])/3.) for e in events if 0<=f-e['frame']<10] or [0.])
 frames.append(dict(index=idx,settledIndex=settled,price=price,change5=c5,changeDay=ret1[idx],growth=growth,phase=phase,critical=critical,cx=x,cy=cy,sx=sx,sy=sy,anchorX=anchorx,bank=bank,power=power,impact=impulse,lookback=lookback))
plan=dict(fps=30,frames=frames,events=events,segments=segments,growthFrames=2,holdFrames=6,introEnd=intro,playEnd=end,start=raw[0][0],end=raw[-1][0],minLow=min(float(r[4]) for r in raw),maxHigh=max(float(r[3]) for r in raw),minClose=min(cl),maxClose=max(cl),firstClose=cl[0],lastClose=cl[-1],totalReturn=cl[-1]/cl[0]-1)
(root/'src/shibao-v5-plan.json').write_text(json.dumps(plan,ensure_ascii=False,separators=(',',':')), encoding='utf-8')
print('Critical bars',len(hot),'ordinary frames',remaining,'milestone holds',extra)
# New timbre: digital FM transients, rising/falling two-tone pings and sub impacts.
out=root/'public/shibao-v5';out.mkdir(exist_ok=True);sr=44100;count=sr*30;rng=random.Random(20261111)
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
