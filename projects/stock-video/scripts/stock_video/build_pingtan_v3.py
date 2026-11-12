"""120-second Pingtan: real SFX, up/down ranges and cinematic deterministic frames."""
import array,csv,datetime,hashlib,json,math,wave
from pathlib import Path
from build_pingtan_v2 import load,save,cap,ease,mix
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'projects/pingtan-2025-v3';PUBLIC=ROOT/'public/pingtan-2025-v3'

def build():
 assert (P/'research/summary.md').exists()
 v2=load(ROOT/'src/stock-videos/pingtan-2025-v2.json');rows=v2['data'];market=v2['market'];dates=[r[0] for r in rows];n=len(rows)
 top_index=dates.index('2025-12-30');top=float(rows[top_index][3]);origin=dates.index('2025-10-16');origin_low=float(rows[origin][4])
 up_specs=[('2025-11-06',132),('2025-11-21',132),('2025-12-03',132),('2025-12-16',132),('2025-12-30',330)]
 down_specs=[('2026-01-19',150),('2026-01-22',135),('2026-06-29',120),('2026-07-21',150)]
 blocks=[('2025-09-01','2025-10-16',90,'fast'),('2025-10-17','2025-11-06',285,'normal'),('2025-11-07','2025-11-21',240,'normal'),('2025-11-24','2025-12-03',210,'normal'),('2025-12-04','2025-12-16',210,'normal'),('2025-12-17','2025-12-30',225,'normal'),('2025-12-31','2026-01-19',255,'normal'),('2026-01-20','2026-01-22',80,'normal'),('2026-01-23','2026-05-26',150,'fast'),('2026-05-27','2026-07-21',260,'crash'),('2026-07-22','2026-11-11',98,'fast')]
 holds=dict(up_specs+down_specs);segments=[];cursor=24
 for begin,end,budget,tempo in blocks:
  ix=[i for i,d in enumerate(dates) if begin<=d<=end]
  base={i:0 if tempo=='fast' else (5 if tempo=='crash' else (10 if market[i]['isUp'] or market[i]['isDown'] else 8)) for i in ix}
  assert sum(base.values())<=budget,(begin,sum(base.values()),budget)
  carry=0;left=budget-sum(base.values())
  for i in ix:
   carry+=left;duration=base[i]+carry//len(ix);carry%=len(ix)
   if not duration:continue
   grow=0 if tempo=='fast' else (2 if tempo=='crash' else 5)
   segments.append(dict(index=i,date=dates[i],start=cursor,complete=cursor+grow,end=cursor+duration+holds.get(dates[i],0),growthFrames=grow));cursor=segments[-1]['end']
 assert cursor==3540,cursor
 by_index={s['index']:s for s in segments};shots=[]
 for direction,specs in [('up',up_specs),('down',down_specs)]:
  for date,hold in specs:
   idx=dates.index(date);start=origin if direction=='up' else top_index;high=float(rows[idx][3]) if direction=='up' else top;low=origin_low if direction=='up' else float(rows[idx][4]);seg=by_index[idx]
   if direction=='up':assert high==max(float(r[3]) for r in rows[:idx+1])
   else:assert low==min(float(r[4]) for r in rows[top_index+1:idx+1])
   shots.append(dict(direction=direction,index=idx,date=date,start=seg['complete'],end=seg['end'],baseIndex=start,baseDate=dates[start],high=high,low=low,amplitude=(high/low-1)*100 if direction=='up' else (low/high-1)*100,sessions=idx-start+1,calendarDays=(datetime.date.fromisoformat(date)-datetime.date.fromisoformat(dates[start])).days,boards=sum(bool(m['isUp'] if direction=='up' else m['isDown']) for m in market[start:idx+1]),final=date=='2025-12-30'))
 shots.sort(key=lambda p:p['start'])
 breaks=[]
 for old in v2['breaks']:
  s=by_index[old['index']];breaks.append(dict(**{k:v for k,v in old.items() if k!='frame'},frame=s['complete'],direction='up',kind='breakout'))
 early={'2025-11-06':('2025-11-05',8.90),'2025-11-21':('2025-11-17',11.97),'2025-11-24':('2025-11-21',10.77),'2025-12-03':('2025-12-02',11.43),'2025-12-17':('2025-12-16',14.10)}
 low_level=float(rows[top_index][4]);low_date=dates[top_index]
 for i,r in enumerate(rows):
  date=r[0];candidate=None
  if date in early:candidate=early[date]
  if i>top_index and float(r[4])<low_level:
   if market[i]['change']<0 and i in by_index:candidate=(low_date,low_level)
   low_level=float(r[4]);low_date=date
  if candidate and i in by_index:
   ref_date,level=candidate;assert float(r[4])<level
   breaks.append(dict(index=i,date=date,refIndex=dates.index(ref_date),level=level,frame=by_index[i]['complete'],intradayOnly=float(r[2])>level,seed=1592+i,direction='down',kind='continuation' if market[i]['isDown'] else 'breakdown'))
 strikes=[dict(index=e['index'],date=e['date'],frame=e['frame']+6,seed=e['seed']) for e in breaks if e['direction']=='down' and (market[e['index']]['isDown'] or market[e['index']]['change']<-.04)]
 frames=[];camera=None
 for f in range(3600):
  if f<24:idx=0;growth=1.;settled=0
  elif f>=3540:idx=n-1;growth=1.;settled=idx
  else:
   s=next(s for s in segments if s['start']<=f<s['end']);idx=s['index'];growth=1-(1-cap((f-s['start'])/s['growthFrames'],0,1))**3 if s['growthFrames'] else 1.;settled=idx if growth>=1 else max(0,idx-1)
  r=rows[idx];recent=rows[max(0,idx-18):idx+1];lo=min(float(x[4]) for x in recent);hi=max(float(x[3]) for x in recent);span=max(hi-lo,float(r[2])*.12,.6)
  target=dict(sx=780/19,sy=600/(span*1.15),tx=830-idx*780/19,ty=1510+(lo-span*.075)*600/(span*1.15));camera=target if camera is None else mix(camera,target,.2)
  reached=rows[:idx+1];all_lo=min(float(x[4]) for x in reached);all_hi=max(float(x[3]) for x in reached);pad=max(.2,(all_hi-all_lo)*.08)
  global_cam=dict(sx=870/max(1,idx),sy=600/(all_hi-all_lo+pad*2),tx=100,ty=1530+(all_lo-pad)*600/(all_hi-all_lo+pad*2))
  shot=next((k for k,p in enumerate(shots) if p['start']<=f<p['end']),-1);overview=0.;closeup=0.;elapsed=0
  if shot>=0:
   p=shots[shot];elapsed=f-p['start'];length=p['end']-p['start']
   if p['final']:overview=ease((elapsed-18)/35)*(1-ease((elapsed-153)/35));closeup=ease((elapsed-153)/35)
   else:overview=ease((elapsed-8)/26)*(1-ease((elapsed-(length-31))/28))
  rendered=mix(camera,global_cam,overview)
  if closeup:rendered=mix(rendered,dict(sx=86.,sy=180.,tx=720-idx*86.,ty=1020+float(r[3])*180.),closeup)
  if f>=3540:rendered=mix(rendered,global_cam,ease((f-3540)/35))
  top_y=rendered['ty']-float(r[3])*rendered['sy'];bottom_y=rendered['ty']-float(r[4])*rendered['sy']
  if top_y<850:rendered['ty']+=850-top_y
  if bottom_y>1550:rendered['ty']-=bottom_y-1550
  tip_x=rendered['tx']+idx*rendered['sx']
  if tip_x>930:rendered['tx']-=tip_x-930
  if tip_x<130:rendered['tx']+=130-tip_x
  close=float(rows[settled][2]);running_hi=max(float(x[3]) for x in rows[:settled+1]);dd=close/running_hi-1
  frames.append(dict(index=idx,settledIndex=settled,growth=growth,camera=rendered,shot=shot,shotElapsed=elapsed,overview=overview,closeup=closeup,red=cap((close/origin_low-1)/3.5,0,1)*(1-cap((-dd-.08)/.25,0,1)),green=max(cap((-market[settled]['change']-.035)/.075,0,1),cap((-dd-.14)/.55,0,.85))))
 film=dict(meta=dict(id='pingtan-2025-v3',name='平潭发展',code='000592',exchange='SZ',fromDate=dates[0],asOf=dates[-1],fps=30,durationFrames=3600,musicOffset=20.03),data=rows,market=market,metrics=v2['metrics'],shots=shots,breaks=sorted(breaks,key=lambda e:e['frame']),strikes=strikes,plan=dict(frames=frames,segments=segments,introEnd=24,playEnd=3540))
 save(ROOT/'src/stock-videos/pingtan-2025-v3.json',film);save(P/'daily.json',rows);save(P/'brief.json',{k:v for k,v in film.items() if k not in ('data','market','plan')})
 with (P/'timeline.csv').open('w',encoding='utf-8',newline='') as fd:
  w=csv.writer(fd);w.writerow(['date','start','complete','end','shot','break direction'])
  for s in segments:w.writerow([s['date'],s['start'],s['complete'],s['end'],' | '.join(p['direction'] for p in shots if p['index']==s['index']),' | '.join(e['direction'] for e in breaks if e['index']==s['index'])])
 errors=[]
 for f,s in enumerate(frames):
  if f and s['index']<frames[f-1]['index']:errors.append(f'Nonmonotonic {f}')
  if s['shot']>=0 and s['growth']!=1:errors.append(f'Incomplete shot {f}')
 save(P/'validation.json',dict(errors=errors,frames=len(frames),sessions=n,shots=shots,breaks=breaks,strikes=strikes));assert not errors
 audio(film)
 print(json.dumps(dict(frames=3600,shots=shots,upBreaks=sum(e['direction']=='up' for e in breaks),downBreaks=sum(e['direction']=='down' for e in breaks),lightning=len(strikes)),ensure_ascii=False,indent=2))

def audio(film):
 PUBLIC.mkdir(parents=True,exist_ok=True);sr=44100;count=120*sr
 with wave.open(str(ROOT/'local-media/pingtan/qingming.wav'),'rb') as w:
  assert w.getframerate()==sr and w.getsampwidth()==2 and w.getnchannels()==2;w.setpos(round(20.03*sr));music_bytes=w.readframes(count)
 music=array.array('h',music_bytes);assert len(music)==count*2
 cache={};measures=[]
 for name in ('charge','charge-alt','surge','heavy','sub','hit','glass','plasma','thunder'):
  file=ROOT/f'local-media/pingtan-v3-sfx/{name}.wav'
  with wave.open(str(file),'rb') as w:
   rate=w.getframerate();ch=w.getnchannels();assert w.getsampwidth()==2;samples=array.array('h',w.readframes(w.getnframes()))
  mono=[sum(samples[i:i+ch])/ch/32768 for i in range(0,len(samples),ch)]
  converted=[]
  for j in range(int(len(mono)*sr/rate)):
   pos=j*rate/sr;k=min(len(mono)-2,int(pos));q=pos-k;converted.append(mono[k]*(1-q)+mono[k+1]*q)
  cache[name]=converted;hop=round(sr*.02);energies=[sum(x*x for x in converted[i:i+hop]) for i in range(0,len(converted),hop)];peak_time=max(range(len(energies)),key=lambda i:energies[i])*.02
  measures.append(dict(name=name,duration=len(converted)/sr,peak=max(map(abs,converted)),energyPeakSeconds=peak_time))
 fxL=array.array('f',[0.])*count;fxR=array.array('f',[0.])*count;cues=[]
 def place(name,frame,gain=0.35,lead=0,tail=None,offset=0):
  source=cache[name][round(offset*sr):];source=source[:round(tail*sr)] if tail else source;start=round((frame/30-lead)*sr)
  for j,v in enumerate(source):
   at=start+j
   if 0<=at<count:fxL[at]+=v*gain;fxR[at]+=v*gain*.96
  cues.append(dict(name=name,frame=frame,onsetSeconds=start/sr,gain=gain,duration=len(source)/sr,sourceOffset=offset))
 for s in film['plan']['segments']:
  m=film['market'][s['index']]
  if m['isUp'] and '2025-10-17'<=s['date']<='2025-12-30':
   place('charge-alt',s['complete'],.48,lead=.78,tail=.86)
   place('plasma',s['complete'],.30,lead=.06,tail=.45)
 for e in film['breaks']:
  place('glass',e['frame'],.40 if e['direction']=='up' else .56,tail=1.5)
  if e['direction']=='down':place('heavy',e['frame'],.36,tail=1.1,offset=2.94);place('sub',e['frame']+3,.24,tail=1.8)
  else:place('surge',e['frame'],.36,lead=.12,tail=.8)
 for e in film['strikes']:place('thunder',e['frame'],.28,tail=1.8,offset=.90)
 peak=max(max(map(abs,fxL)),max(map(abs,fxR)));sfx_gain=min(1,.65/max(peak,1e-9))
 applied=array.array('h');mixed=array.array('h');limited=0
 for i in range(count):
  for ch,track in ((0,fxL),(1,fxR)):
   original=music[2*i+ch];v=round(track[i]*sfx_gain*32768);bounded=cap(v,-32768-original,32767-original);limited+=v!=bounded;applied.append(bounded);mixed.append(original+bounded)
 def write(file,payload):
  with wave.open(str(PUBLIC/file),'wb') as w:w.setparams((2,2,sr,count,'NONE','not compressed'));w.writeframes(payload)
 write('music-original-excerpt.wav',music_bytes);write('foreground.wav',applied.tobytes());write('mix.wav',mixed.tobytes())
 proof=dict(musicOffset=20.03,duration=120,musicStemSha256=hashlib.sha256(music_bytes).hexdigest(),sourceExcerptSha256=hashlib.sha256(music_bytes).hexdigest(),musicGain=1,masterGain=.7,musicDucking=False,musicTempoChange=False,musicPitchChange=False,musicFade=False,normalization=False,sfxMethod='Real CC0 and runtime Mixkit recordings; no oscillator synthesis',sfxOnlyGain=sfx_gain,constrainedSfxSamples=limited,totalChannelSamples=count*2,measurements=measures,cues=cues,subjectiveListening='not performed')
 save(P/'audio-proof.json',proof);save(PUBLIC/'audio-design.json',proof)

if __name__=='__main__':build()
