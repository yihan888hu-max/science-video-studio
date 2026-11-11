"""Build a source-audited, reusable OHLC film. Standard library + existing FFmpeg only."""
import argparse,array,bisect,csv,datetime,json,math,random,struct,subprocess,wave
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def save(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n', encoding='utf-8')
def cap(v,a,b):return max(a,min(b,v))
def allocate(indices,base,budget):
 used=sum(base.get(i,0) for i in indices);assert used<=budget,f'Hold budget {used} exceeds {budget}; extend duration or reduce holds'
 left=budget-used;acc=0;result={}
 for i in indices:
  acc+=left;extra=acc//len(indices);acc%=len(indices);result[i]=base.get(i,0)+extra
 return result

def build(path):
 path=path.resolve();folder=path.parent;c=json.loads(path.read_text(encoding='utf-8'))
 assert (folder/'research/summary.md').exists(),'Research summary is required before production'
 identity_path=folder/'research/data-sources.json'
 if identity_path.exists():
  identity=json.loads(identity_path.read_text(encoding='utf-8')).get('identity');assert not identity or identity['symbol']==c['exchange'].lower()+c['code'],'Stock identity mismatch'

 raw=json.loads((folder/c['dataFile']).read_text(encoding='utf-8'));un=json.loads((folder/c['unadjustedFile']).read_text(encoding='utf-8'));actual={r[0]:r for r in un}
 assert raw and all(raw[i][0]<raw[i+1][0] for i in range(len(raw)-1));assert raw[-1][0]==c['asOf']
 dates=[r[0] for r in raw];n=len(raw);cl=[float(r[2]) for r in raw];prior_dates=[r[0] for r in un if r[0]<dates[0]]
 assert prior_dates,'Need previous completed trading day for first-day price limit'
 previous=actual[max(prior_dates)];market=[];streak=0;last=-100;cluster_start=0;count=0
 for i,r in enumerate(raw):
  a=actual[r[0]];o,close,hi,lo,vol=map(float,a[1:6]);assert hi>=max(o,close)>=lo and hi>=min(o,close)>=lo
  prev=Decimal(previous[2]);up_limit=(prev*(1+Decimal(str(c['defaultLimitPct']))/100)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP);dn_limit=(prev*(1-Decimal(str(c['defaultLimitPct']))/100)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
  if r[0] in c.get('limits',{}):
   special=c['limits'][r[0]];up_limit=Decimal(str(special['upper'])) if special['upper'] is not None else None;dn_limit=Decimal(str(special['lower'])) if special['lower'] is not None else None
  isup=up_limit is not None and Decimal(a[2])==up_limit;isdown=dn_limit is not None and Decimal(a[2])==dn_limit
  failed=up_limit is not None and Decimal(a[3])==up_limit and not isup
  prior=streak;streak=streak+1 if isup else 0;change=float(Decimal(a[2])/prev-1)
  if isup:
   if i-last>3:cluster_start=i;count=0
   count+=1;last=i
  span=i-cluster_start+1
  label=f'{streak}连板' if streak>=2 else (f'{span}天{count}板' if isup and count>=3 else ('首板涨停' if isup else ('跌停' if isdown else ('断板' if prior>=2 else ''))))
  if not label and failed:label='炸板回落'
  if not label and change<=-.06:label='长阴调整'
  if not label and change>=.06:label='强势上行'
  item=dict(date=r[0],isUp=isup,isDown=isdown,change=change,streak=streak,label=label,sub='',volume=vol)
  override=c.get('overrides',{}).get(r[0])
  if override:
   assert override.get('evidence'),f'Missing caption evidence: {r[0]}'
   item.update(override)
  market.append(item);previous=a
 for msg in c['catalysts']:
  assert msg['from']>=msg['published'] and msg['from']<=msg['to'] and msg['url']
 peaks=[]
 for spec in c['peaks']:
  a=dates.index(spec['start']);b=dates.index(spec['date']);assert b>=a
  lo=float(raw[a][4]);hi=float(raw[b][3]);assert hi==max(float(r[3]) for r in raw[a:b+1]),'Peak is not wave high'
  peaks.append(dict(**spec,index=b,low=lo,high=hi,amplitudePct=(hi/lo-1)*100,tradingSessions=b-a+1,calendarDays=(datetime.date.fromisoformat(dates[b])-datetime.date.fromisoformat(dates[a])).days))
 intro=c['introEnd'];end=c['playEnd'];total=c['durationFrames'];focus=set();dur={}
 ret5=[cl[i]/cl[max(0,i-5)]-1 for i in range(n)]
 critical={i for i,m in enumerate(market) if m['isUp'] or m['isDown'] or dates[i] in c['overrides']}
 for w in c['focus']:
  ix=[i for i in range(n) if w['from']<=dates[i]<=w['to']];assert not focus.intersection(ix);focus.update(ix)
  base={i:(8 if i in critical else 4)+c['extraHolds'].get(dates[i],0) for i in ix};dur.update(allocate(ix,base,w['frames']))
 outside=[i for i in range(n) if i not in focus];outside_budget=end-intro-sum(dur.values())
 rare=sorted([i for i in outside if abs(market[i]['change'])>.09],key=lambda i:abs(market[i]['change']*ret5[i]),reverse=True)[:8]
 dur.update(allocate(outside,{i:6 for i in rare},outside_budget))
 segments=[];events=[];f=intro
 for i in range(n):
  length=dur[i]
  if not length:continue
  slow=i in focus or i in rare;seg=dict(index=i,start=f,end=f+length,critical=slow);segments.append(seg)
  if slow and (i in critical or i in rare):events.append(dict(index=i,date=dates[i],start=f,frame=f+2,end=f+length,changeDay=market[i]['change'],label=market[i]['label'],peak=any(p['index']==i for p in peaks)))
  f+=length
 assert f==end
 for p in peaks:
  seg=next(s for s in segments if s['index']==p['index']);p.update(frame=seg['start']+2,end=seg['end'])
 frames=[];x=0.;cy=-cl[0]*28;sx=4.;sy=9.;anchor=760.;bank=0.;red=0.;green=0.;starts=[s['start'] for s in segments];running_hi=float(raw[0][3]);wave_low=peaks[0]['low'];wave_start=peaks[0]['start']
 for f in range(total):
  if f<intro:idx=0;growth=1.;slow=False;phase='intro';local=0
  elif f>=end:idx=n-1;growth=1.;slow=False;phase='outro';local=0
  else:
   seg=segments[bisect.bisect_right(starts,f)-1];idx=seg['index'];slow=seg['critical'];local=f-seg['start'];growth=1-(1-min(1,local/2))**3 if slow else 1.;phase=('grow' if growth<1 else 'hold') if slow else 'fast'
  settled=idx if growth>=1 else max(0,idx-1);o=float(raw[idx][1]);price=o+(cl[idx]-o)*growth;change5=ret5[idx]
  power=max(cap((abs(change5)-.08)/.35,0,1),.8 if slow and abs(market[idx]['change'])>.075 else 0)
  lookback=round(36-19*power);recent=raw[max(0,idx-lookback+1):idx+1];hi=max(float(r[3]) for r in recent);lo=min(float(r[4]) for r in recent);span=max(hi-lo,max(.45,price*.06));mid=(hi+lo)/2
  # Damping stops during a completed-bar hold, rather than dragging a candle mid-growth.
  damping=.21 if phase!='hold' or local<10 else (.08 if local<17 else 0)
  sx+=(900/(lookback*6)-sx)*damping;sy+=(605/(span*28)-sy)*damping;x+=(idx*6-x)*min(.38,damping*1.7);cy+=(-mid*28-cy)*min(.3,damping*1.4)
  anchor+=(760+cap(change5/.25,-1,1)*24-anchor)*damping;x=max(x,idx*6-(920-anchor)/sx);bank+=(cap(change5*3.8,-1.65,1.65)-bank)*damping
  bh=float(raw[idx][3]);bl=float(raw[idx][4]);sy=min(sy,640/max(.001,(bh-bl)*28));top=1170+(-bh*28-cy)*sy;bottom=1170+(-bl*28-cy)*sy
  if top<850:cy-=(850-top)/sy
  if bottom>1490:cy+=(bottom-1490)/sy
  impulse=max([math.exp(-(f-e['frame'])/3.4)*(1.25 if e['peak'] else 1.) for e in events if 0<=f-e['frame']<13] or [0.])
  running_hi=max(running_hi,float(raw[settled][3]));drawdown=cl[settled]/running_hi-1
  # Atmosphere uses only prices reached so far; no future peak drives early colour.
  expansion=cap(math.log(max(1,cl[settled]/wave_low))/math.log(5),0,1) if dates[settled]>=wave_start else 0
  target_green=max(cap((-market[settled]['change']-.04)/.06,0,1),cap((-change5-.04)/.3,0,1),cap((-drawdown-.12)/.50,0,.85) if dates[settled]>=wave_start else 0)
  target_red=expansion*(1-target_green)*(.9 if change5>=-.03 else .35)
  red+=(target_red-red)*.12;green+=(target_green-green)*.16
  frames.append(dict(index=idx,settledIndex=settled,price=price,growth=growth,phase=phase,cx=x,cy=cy,sx=sx,sy=sy,anchorX=anchor,bank=bank,power=power,impact=impulse,red=red,green=green,change5=change5))
 plan=dict(frames=frames,events=events,segments=segments,introEnd=intro,playEnd=end,minLow=min(float(r[4]) for r in raw),maxHigh=max(float(r[3]) for r in raw))
 film=dict(meta=c,data=raw,market=market,catalysts=c['catalysts'],peaks=peaks,plan=plan)
 save(ROOT/f'src/stock-videos/{c["id"]}.json',film)
 with (folder/'timeline.csv').open('w', encoding='utf-8', newline='') as fd:
  out=csv.writer(fd);out.writerow(['date','start_frame','completion_frame','end_frame','hold_frames','label','message'])
  for s in segments:
   i=s['index'];out.writerow([dates[i],s['start'],s['start']+(2 if s['critical'] else 0),s['end'],s['end']-s['start']-(2 if s['critical'] else 0),market[i]['label'],' | '.join(m['title'] for m in c['catalysts'] if m['from']<=dates[i]<=m['to'])])
 # Every frame: monotonic history, OHLC containment, bounded active candle, message dates.
 errors=[]
 for j,s in enumerate(frames):
  if j and s['index']<frames[j-1]['index']:errors.append(f'Non-monotonic {j}')
  if intro<=j<end:
   i=s['index'];top=1170+(-float(raw[i][3])*28-s['cy'])*s['sy'];bottom=1170+(-float(raw[i][4])*28-s['cy'])*s['sy'];tip=s['anchorX']+(i*6-s['cx'])*s['sx']
   if not (849<=top<=bottom<=1491 and tip<=921):errors.append(f'Camera bounds {j}')
  if s['growth']<1 and s['settledIndex']>=s['index'] and s['index']>0:errors.append(f'Premature completed label {j}')
 save(folder/'validation.json',dict(errors=errors,sessions=n,first=dates[0],last=dates[-1],frames=total,visibleSegments=len(segments),events=len(events),peaks=peaks,checks=['OHLC order','previous close','message publication','caption evidence','monotonic timeline','completed candle labels','active candle fit','peak calculations']))
 assert not errors,errors[:10]
 audio(ROOT/f'public/{c["id"]}',events,total/c['fps'],c['fps'])
 print(json.dumps(dict(film=c['id'],sessions=n,segments=len(segments),events=len(events),peaks=peaks),ensure_ascii=False,indent=2))

def audio(folder,events,duration,fps):
 folder.mkdir(parents=True,exist_ok=True);sr=48000;count=round(sr*duration);rng=random.Random(5472025);L=array.array('f',[0])*count;R=array.array('f',[0])*count;duck=array.array('f',[1])*count
 for e in events:
  for j in range(int(sr*.36)):
   k=round(e['frame']/fps*sr)+j
   if 0<=k<count:duck[k]=min(duck[k],.18+.82*(j/(sr*.36))**2)
 for i in range(count):
  t=i/sr;fade=cap(min(t/.5,(duration-t)/.9),0,1);base=[55,65.406,49,73.416][min(3,int(t/(duration/4)))];phase=2*math.pi*base*t;beat=t%.5
  # Quiet electro pulse, with deep automatic space for the foreground signal.
  bed=.018*math.sin(phase+.7*math.sin(phase*2.01))+.008*math.sin(phase*4.005)
  kick=.025*math.sin(2*math.pi*(47*beat+1.5*(1-math.exp(-beat*38))))*math.exp(-beat*35)
  v=(bed+kick)*fade*duck[i];L[i]=v;R[i]=v+.003*math.sin(phase*2.003)*fade*duck[i]
 for e in events:
  onset=e['frame']/fps;peak=e['peak'];up=e['changeDay']>=0 or peak;carrier=1760 if peak else (1320 if up else 660);amp=1.25 if peak else 1
  for j in range(round(sr*.40)):
   t=j/sr;k=round(onset*sr)+j
   if not 0<=k<count:continue
   # Sharp metal/FM front, bitlike overtone and tight pitched sub: deliberately unlike V5's soft ping.
   attack=min(1,t/.0008);env=math.exp(-t*31)*attack
   phase=2*math.pi*carrier*(t+(.006 if up else -.004)*(1-math.exp(-t*35)))
   metal=.24*math.sin(phase+4.2*math.exp(-t*40)*math.sin(phase*1.4142))*env
   click=.09*(rng.random()*2-1)*math.exp(-t*160)*attack
   sub=.19*math.sin(2*math.pi*(48*t+2.2*(1-math.exp(-t*45))))*math.exp(-t*22)
   ping=0
   for delay,pitch in ((.075,1.5 if up else .75),(.145,2 if up else .5)):
    if t>=delay:ping+=.12*math.sin(2*math.pi*carrier*pitch*(t-delay))*math.exp(-(t-delay)*45)*min(1,(t-delay)/.001)
   v=(metal+click+sub+ping)*amp;L[k]+=v;R[k]+=v*.94
  for j in range(round(sr*.045)):
   t=j/sr;k=round((onset-.045)*sr)+j
   if 0<=k<count:
    v=.045*math.sin(2*math.pi*(700*t+9000*t*t))*(t/.045)**2;L[k]+=v;R[k]+=v
 maximum=max(max(map(abs,L)),max(map(abs,R)));gain=min(1,.92/maximum)
 with wave.open(str(folder/'mix-raw.wav'),'wb') as w:
  w.setparams((2,2,sr,count,'NONE','not compressed'));b=bytearray()
  for l,r in zip(L,R):b.extend(struct.pack('<hh',round(l*gain*32767),round(r*gain*32767)))
  w.writeframes(b)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(folder/'mix-raw.wav'),'-af','loudnorm=I=-15:TP=-1.2:LRA=9','-ar',str(sr),'-y',str(folder/'mix.wav')],check=True)
 save(folder/'audio-design.json',dict(originalSynthesis=True,sampleRate=sr,foregroundToBed='Layered metal/FM + digital double-ping + sub; bed duck to 18% at cue',cueFrames=[e['frame'] for e in events],normalization='I=-15 LUFS TP=-1.2 dBTP',rawPeak=maximum))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('brief',type=Path);args=parser.parse_args();build(args.brief)
