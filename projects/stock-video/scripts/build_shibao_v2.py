"""Build a deterministic data-driven camera, annotations, and original sound mix."""
import array, bisect, hashlib, json, math, random, struct, wave
from pathlib import Path
root=Path(__file__).resolve().parents[1]
raw=json.loads((root/'src/shibao-daily.json').read_text(encoding='utf-8'))
cl=[float(r[2]) for r in raw]; n=len(cl)
# Time remapping controls pacing only. Zoom and shock come from market data.
anchors=[[0,0],[54,0],[150,308],[216,590],[302,1255],[331,1329],[392,1363],[436,1375],[505,1614],[548,1626],[606,1976],[665,2212],[704,2226],[751,2296],[798,n-1],[899,n-1]]
signals=[]
for i in range(5,n):
 c=cl[i]/cl[i-5]-1
 if -.2<c<.25: continue
 if signals and i-signals[-1]['last']<=5 and (c>0)==(signals[-1]['change']>0):
  signals[-1]['last']=i
  if abs(c)>abs(signals[-1]['change']): signals[-1].update(index=i,date=raw[i][0],change=c)
 else: signals.append(dict(index=i,last=i,date=raw[i][0],change=c))
def frame_of(idx):
 for (f0,i0),(f1,i1) in zip(anchors,anchors[1:]):
  if i0<=idx<=i1 and i0!=i1:return round(f0+(idx-i0)/(i1-i0)*(f1-f0))
 return 798
for s in signals:s['frame']=frame_of(s['index'])
labels={
'2018-02-06':('下跌，来得很快','五个交易日收盘变化'),
'2019-04-10':('反弹，也会很急','五个交易日收盘变化'),
'2022-06-17':('向上加速','五个交易日收盘变化'),
'2022-07-12':('随后出现回撤','另一段五个交易日'),
'2023-07-06':('又一次快速拉升','五个交易日收盘变化'),
'2023-07-24':('上涨之后仍有急跌','另一段五个交易日'),
'2025-12-22':('新的波动区间','五个交易日收盘变化')}
annotations=[]
for s in signals:
 if s['date'] in labels:
  i=s['index'];title,sub=labels[s['date']]
  annotations.append(dict(frame=s['frame'],date=s['date'],start=raw[i-5][0],title=title,subtitle=sub,change=s['change'],before=cl[i-5],after=cl[i]))
frames=[]; camx=0.; camy=-cl[0]*28; zoom=1.
for f in range(900):
 k=min(len(anchors)-2,max(0,bisect.bisect_right([a[0] for a in anchors],f)-1))
 f0,i0=anchors[k];f1,i1=anchors[k+1];cursor=i0+(i1-i0)*(f-f0)/(f1-f0)
 i=min(n-1,int(cursor));p=cl[i]+(cl[min(n-1,i+1)]-cl[i])*(cursor-i)
 c5=p/cl[max(0,i-5)]-1
 # Target zoom uses current trailing return, with no future prices.
 power=max(0,min(1.0,(abs(c5)-.12)/.40));target=1.+.65*power
 zoom+=(target-zoom)*.18;camx+=(cursor*6-camx)*.22;camy+=(-p*28-camy)*.18
 hits=[(f-s['frame'],abs(s['change'])) for s in signals if 0<=f-s['frame']<15]
 impact=max([min(1,a/.6)*math.exp(-age/4) for age,a in hits] or [0.])
 frames.append(dict(index=round(cursor,5),price=p,change5=c5,x=camx,y=camy,zoom=zoom,impact=impact))
plan=dict(fps=30,frames=frames,signals=signals,annotations=annotations,anchors=anchors,sourceSha256=hashlib.sha256((root/'src/shibao-daily.json').read_bytes()).hexdigest(),start=raw[0][0],end=raw[-1][0],minClose=min(cl),maxClose=max(cl),totalReturn=cl[-1]/cl[0]-1)
(root/'src/shibao-v2-plan.json').write_text(json.dumps(plan,ensure_ascii=False,separators=(',',':')), encoding='utf-8')
# Original instrumental bed and action sounds. No reference soundtrack is copied.
sr=44100; length=30; audio=array.array('f',[0.])*(sr*length);rng=random.Random(703)
notes=[55.,65.406,49.,58.270]
for i in range(len(audio)):
 t=i/sr;fade=min(1,t/1.4,(30-t)/1.5);freq=notes[min(3,int(t/7.5))]
 pad=.022*(math.sin(2*math.pi*freq*t)+.45*math.sin(2*math.pi*freq*2.005*t)+.25*math.sin(2*math.pi*freq*3*t))
 pulse=(t%(.625))
 kick=.045*math.sin(2*math.pi*(45*pulse+2.8*(1-math.exp(-pulse*25))))*math.exp(-pulse*25)
 tick=.009*(rng.random()*2-1)*math.exp(-((t%.3125)*85))
 audio[i]=(pad+kick+tick)*max(0,fade)
for s in signals:
 t0=s['frame']/30
 for j in range(int(sr*.8)):
  t=j/sr;k=int(t0*sr)+j
  if k>=len(audio):break
  hit=.17*math.sin(2*math.pi*(47*t+2.2*(1-math.exp(-t*18))))*math.exp(-t*11)
  noise=.036*(rng.random()*2-1)*math.exp(-t*20)
  audio[k]+=hit+noise
 # The pre-hit whoosh follows the same detected event, starting 0.18 s earlier.
 for j in range(int(sr*.18)):
  t=j/sr;k=int((t0-.18)*sr)+j
  if 0<=k<len(audio): audio[k]+=.025*(rng.random()*2-1)*(t/.18)**2
with wave.open(str(root/'public/shibao-v2/mix-raw.wav'),'wb') as w:
 w.setparams((2,2,sr,len(audio),'NONE','not compressed'))
 chunk=bytearray()
 for v in audio:
  sample=int(max(-.9,min(.9,v))*32767);chunk.extend(struct.pack('<hh',sample,sample))
 w.writeframes(chunk)
print('Built',len(frames),'camera frames;',len(signals),'data events;',len(annotations),'annotations')
print('Return:',round(plan['totalReturn']*100,2),'Min/max close',min(cl),max(cl))
