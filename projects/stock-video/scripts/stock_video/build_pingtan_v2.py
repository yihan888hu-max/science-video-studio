"""60-second cinematic Pingtan revision; local snapshots and standard library."""
import array,csv,datetime,hashlib,json,math,random,struct,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/'projects/pingtan-2025-v2';PUBLIC=ROOT/'public/pingtan-2025-v2'
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def save(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
def cap(v,a,b):return max(a,min(b,v))
def ease(v):v=cap(v,0,1);return v*v*(3-2*v)
def mix(a,b,t):return {key:a[key]+(b[key]-a[key])*t for key in a}

def build():
 assert (PROJECT/'research/summary.md').is_file()
 v1=load(ROOT/'src/stock-videos/pingtan-2025-v1.json')
 rows=[r for r in v1['data'] if r[0]>='2025-09-01'];dates=[r[0] for r in rows];by_date={r['date']:r for r in v1['market']};market=[by_date[d] for d in dates];n=len(rows)
 assert n==285 and dates[-1]=='2026-11-11'
 start_index=dates.index('2025-10-16');low=float(rows[start_index][4])
 specs=[('2025-11-06',108),('2025-11-21',108),('2025-12-03',96),('2025-12-16',96),('2025-12-30',255)]
 blocks=[('2025-09-01','2025-10-16',66),('2025-10-17','2025-11-06',210),('2025-11-07','2025-11-21',150),('2025-11-24','2025-12-03',135),('2025-12-04','2025-12-16',135),('2025-12-17','2025-12-30',138),('2025-12-31','2026-01-21',150),('2026-01-22','2026-11-11',89)]
 holds=dict(specs);segments=[];cursor=24
 for begin,end,budget in blocks:
  indices=[i for i,d in enumerate(dates) if begin<=d<=end]
  base={i:(0 if begin>='2026-01-22' else (1 if end<='2025-10-16' else (9 if market[i]['isUp'] or market[i]['isDown'] else 6))) for i in indices}
  assert sum(base.values())<=budget
  remainder=budget-sum(base.values());carry=0
  for i in indices:
   carry+=remainder;extra=carry//len(indices);carry%=len(indices);duration=base[i]+extra
   if duration<=0:continue
   grow=1 if end<='2025-10-16' or begin>='2026-01-22' else 4
   if duration<=grow:grow=0
   s=dict(index=i,date=dates[i],start=cursor,complete=cursor+grow,growthFrames=grow,end=cursor+duration+holds.get(dates[i],0))
   segments.append(s);cursor=s['end']
 assert cursor==1760,cursor
 shots=[]
 for date,extra in specs:
  idx=dates.index(date);s=next(s for s in segments if s['index']==idx);high=float(rows[idx][3])
  assert high==max(float(r[3]) for r in rows[:idx+1])
  shots.append(dict(index=idx,date=date,start=s['complete'],end=s['end'],baseIndex=start_index,baseDate=dates[start_index],low=low,high=high,amplitude=(high/low-1)*100,sessions=idx-start_index+1,calendarDays=(datetime.date.fromisoformat(date)-datetime.date.fromisoformat(dates[start_index])).days,boards=sum(bool(m['isUp']) for m in market[start_index:idx+1]),final=date=='2025-12-30'))
 em=load(PROJECT/'research/eastmoney-dec2025.json');assert em['data']['code']=='000592'
 em_rows={v.split(',')[0]:v.split(',') for v in em['data']['klines']};top=em_rows['2025-12-30'];tencent=rows[dates.index('2025-12-30')]
 assert all(float(a)==float(b) for a,b in zip(top[1:6],tencent[1:6]))
 metrics=dict(date=top[0],high=float(top[3]),volumeHands=float(top[5]),turnover=float(top[10]),amount=float(top[6]),source='东方财富历史日线 / 腾讯OHLC与量核对')
 references=[dict(index=dates.index('2025-09-02'),date='2025-09-02',high=3.72)]+shots[:-1]
 breaks=[]
 for ref in references:
  later=next((i for i in range(ref['index']+1,n) if float(rows[i][3])>ref['high']),None)
  if later is None:continue
  s=next(s for s in segments if s['index']==later)
  breaks.append(dict(index=later,date=dates[later],refIndex=ref['index'],level=ref['high'],frame=s['complete'],intradayOnly=float(rows[later][2])<ref['high'],seed=592+later))
 strike_dates=['2025-11-06','2025-11-21','2025-11-24','2025-12-03','2025-12-17','2026-01-15','2026-01-16','2026-01-19']
 strikes=[dict(index=s['index'],date=s['date'],frame=s['complete']+5,seed=902+s['index']) for s in segments if s['date'] in strike_dates]
 frames=[];camera=None
 for f in range(1800):
  if f<24:s=segments[0];idx=0;growth=1.;settled=0
  elif f>=1760:s=segments[-1];idx=n-1;growth=1.;settled=idx
  else:
   s=next(s for s in segments if s['start']<=f<s['end']);idx=s['index'];growth=1-(1-cap((f-s['start'])/s['growthFrames'],0,1))**3 if s['growthFrames'] else 1.;settled=idx if growth>=1 else max(0,idx-1)
  r=rows[idx];recent=rows[max(0,idx-19):idx+1];lo=min(float(x[4]) for x in recent);hi=max(float(x[3]) for x in recent);span=max(hi-lo,float(r[2])*.12,.6)
  target=dict(sx=780/20,sy=600/(span*1.15),tx=850-idx*780/20,ty=1510+(lo-span*.075)*600/(span*1.15))
  camera=target if camera is None else mix(camera,target,.24)
  reached=rows[:idx+1];all_low=min(float(x[4]) for x in reached);all_high=max(float(x[3]) for x in reached);padding=max(.2,(all_high-all_low)*.08)
  global_camera=dict(sx=870/max(1,idx),sy=600/(all_high-all_low+padding*2),tx=100,ty=1530+(all_low-padding)*600/(all_high-all_low+padding*2))
  shot=next((k for k,p in enumerate(shots) if p['start']<=f<p['end']),-1);overview=0.;closeup=0.;elapsed=0
  if shot>=0:
   p=shots[shot];elapsed=f-p['start'];length=p['end']-p['start']
   if p['final']:
    overview=ease((elapsed-18)/32)*(1-ease((elapsed-116)/34));closeup=ease((elapsed-116)/34)
   else:overview=ease((elapsed-6)/22)*(1-ease((elapsed-(length-27))/24))
  rendered=mix(camera,global_camera,overview)
  if closeup:
   close_camera=dict(sx=82.,sy=180.,tx=720-idx*82.,ty=1020+float(r[3])*180.)
   rendered=mix(rendered,close_camera,closeup)
  if f>=1760:rendered=mix(rendered,global_camera,ease((f-1760)/30))
  # Keep the active candle fully framed even across compressed date jumps.
  top_y=rendered['ty']-float(r[3])*rendered['sy'];bottom_y=rendered['ty']-float(r[4])*rendered['sy']
  if top_y<850:rendered['ty']+=850-top_y
  if bottom_y>1550:rendered['ty']-=bottom_y-1550
  tip_x=rendered['tx']+idx*rendered['sx']
  if tip_x>930:rendered['tx']-=tip_x-930
  if tip_x<130:rendered['tx']+=130-tip_x
  close=float(rows[settled][2]);running_high=max(float(x[3]) for x in rows[:settled+1]);drawdown=close/running_high-1
  frames.append(dict(index=idx,settledIndex=settled,growth=growth,camera=rendered,shot=shot,shotElapsed=elapsed,overview=overview,closeup=closeup,red=cap((close/low-1)/3.5,0,1)*(1-cap((-drawdown-.08)/.25,0,1)),green=max(cap((-market[settled]['change']-.035)/.075,0,1),cap((-drawdown-.14)/.55,0,.8))))
 film=dict(meta=dict(id='pingtan-2025-v2',name='平潭发展',code='000592',exchange='SZ',fromDate=dates[0],asOf=dates[-1],fps=30,durationFrames=1800,musicOffset=20.03),data=rows,market=market,shots=shots,breaks=breaks,strikes=strikes,metrics=metrics,plan=dict(frames=frames,segments=segments,introEnd=24,playEnd=1760))
 save(ROOT/'src/stock-videos/pingtan-2025-v2.json',film);save(PROJECT/'brief.json',{k:v for k,v in film.items() if k not in ('data','market','plan')});save(PROJECT/'daily.json',rows)
 with (PROJECT/'timeline.csv').open('w',encoding='utf-8',newline='') as fd:
  out=csv.writer(fd);out.writerow(['date','start','complete','end','label','shot','glass','lightning'])
  for s in segments:out.writerow([s['date'],s['start'],s['complete'],s['end'],market[s['index']]['label'],any(p['index']==s['index'] for p in shots),any(p['index']==s['index'] for p in breaks),s['date'] in strike_dates])
 errors=[]
 for f,s in enumerate(frames):
  if f and s['index']<frames[f-1]['index']:errors.append(f'Nonmonotonic {f}')
  if not all(math.isfinite(v) for v in s['camera'].values()):errors.append(f'Camera nonfinite {f}')
  if s['growth']<1 and s['settledIndex']>=s['index'] and s['index']>0:errors.append(f'Future label {f}')
  if s['shot']>=0 and s['growth']!=1:errors.append(f'Incomplete peak {f}')
 for p in shots:
  assert all(frames[f]['index']==p['index'] and frames[f]['growth']==1 for f in range(p['start'],p['end']))
 save(PROJECT/'validation.json',dict(errors=errors,sessions=n,frames=len(frames),shots=shots,breaks=breaks,strikes=strikes,metrics=metrics));assert not errors
 audio(film)
 print(json.dumps(dict(sessions=n,segments=len(segments),shots=shots,breaks=breaks,strikes=strikes),ensure_ascii=False,indent=2))

def audio(film):
 PUBLIC.mkdir(parents=True,exist_ok=True)
 with wave.open(str(ROOT/'local-media/pingtan/qingming.wav'),'rb') as w:
  sr=w.getframerate();assert w.getnchannels()==2 and w.getsampwidth()==2;w.setpos(round(20.03*sr));music_bytes=w.readframes(60*sr)
 music=array.array('h',music_bytes);count=60*sr;fxL=array.array('f',[0.])*count;fxR=array.array('f',[0.])*count
 cues=[]
 for s in film['plan']['segments']:
  i=s['index'];m=film['market'][i]
  if m['isUp'] and s['date']>='2025-10-17' and s['date']<='2025-12-30':cues.append(dict(frame=s['complete'],kind='rise',seed=592+i))
 cues += [dict(frame=e['frame'],kind='glass',seed=e['seed']) for e in film['breaks']]
 cues += [dict(frame=e['frame'],kind='thunder',seed=e['seed']) for e in film['strikes']]
 for cue in cues:
  onset=cue['frame']/30;rng=random.Random(cue['seed']);kind=cue['kind'];duration=.65 if kind=='rise' else .8
  for j in range(round(sr*duration)):
   t=j/sr;at=round(onset*sr)+j
   if not 0<=at<count:continue
   env=min(1,t/.008)*math.exp(-t*(5 if kind=='rise' else 10))
   if kind=='rise':
    # Audible continuous low-to-high sweep plus a rising major arpeggio.
    sweep=math.sin(2*math.pi*(260*t+1250*t*t))*.35
    tones=0.
    for delay,freq in ((0,392),(.105,523.25),(.210,659.25),(.315,1046.5)):
     if t>=delay:tones+=math.sin(2*math.pi*freq*(t-delay))*math.exp(-(t-delay)*15)*.32*min(1,(t-delay)/.005)
    value=(sweep*env+tones)*.22
   elif kind=='glass':
    crack=rng.uniform(-1,1)*math.exp(-t*55)*.8
    shards=sum(math.sin(2*math.pi*p*t+math.sin(2*math.pi*p*1.37*t))*math.exp(-t*(8+k*2))*.13 for k,p in enumerate((1813,2731,3919,5311)))
    value=(crack+shards)*min(1,t/.001)*.17
   else:
    crack=rng.uniform(-1,1)*math.exp(-t*24)*.75
    rumble=math.sin(2*math.pi*(45*t+70*(1-math.exp(-t*12))/12))*math.exp(-t*8)*.8
    value=(crack+rumble)*min(1,t/.001)*.14
   fxL[at]+=value;fxR[at]+=value*.96
 applied=array.array('h');mixed=array.array('h');limited=0
 for i in range(count):
  for ch,track in ((0,fxL),(1,fxR)):
   original=music[i*2+ch];sample=round(track[i]*32768);allowed=cap(sample,-32768-original,32767-original)
   limited+=allowed!=sample;applied.append(allowed);mixed.append(original+allowed)
 def write(name,payload):
  with wave.open(str(PUBLIC/name),'wb') as w:w.setparams((2,2,sr,count,'NONE','not compressed'));w.writeframes(payload)
 write('music-original-excerpt.wav',music_bytes);write('foreground.wav',applied.tobytes());write('mix.wav',mixed.tobytes())
 proof=dict(musicSource='local-media/pingtan/qingming.wav',offsetSeconds=20.03,duration=60,sampleRate=sr,sourceExcerptSha256=hashlib.sha256(music_bytes).hexdigest(),musicStemSha256=hashlib.sha256(music_bytes).hexdigest(),musicGain=1,musicDucking=False,musicFade=False,musicTempoChange=False,musicPitchChange=False,normalization=False,headroomHandling='Only SFX contributions constrained to remaining PCM headroom; music samples unchanged',constrainedSfxSamples=limited,totalChannelSamples=count*2,cues=cues,subjectiveListening='not performed')
 save(PUBLIC/'audio-design.json',proof);save(PROJECT/'audio-proof.json',proof)

if __name__=='__main__':build()
