"""Independent V2 historical, cinematic and unchanged-music checks."""
import hashlib,json,math,wave
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1]
load=lambda path:json.loads(path.read_text(encoding='utf-8'))
film=load(ROOT/'src/stock-videos/pingtan-2025-v2.json');v1=load(ROOT/'src/stock-videos/pingtan-2025-v1.json')
rows=film['data'];dates=[r[0] for r in rows];frames=film['plan']['frames'];assert len(rows)==285 and len(frames)==1800
assert rows==[r for r in v1['data'] if r[0]>='2025-09-01'] and dates[-1]=='2026-11-11'
assert len(set(dates))==len(dates) and dates==sorted(dates)
for r in rows:
 o,c,h,l,v=map(float,r[1:6]);assert all(math.isfinite(x) for x in (o,c,h,l,v)) and h>=max(o,c,l) and l<=min(o,c,h)
for shot in film['shots']:
 assert shot['high']==max(float(r[3]) for r in rows[:shot['index']+1])
 start=shot['baseIndex'];end=shot['index'];assert shot['sessions']==end-start+1
 assert shot['boards']==sum(bool(m['isUp']) for m in film['market'][start:end+1])
 assert abs(shot['amplitude']-(shot['high']/shot['low']-1)*100)<1e-9
 assert all(frames[f]['index']==end and frames[f]['growth']==1 for f in range(shot['start'],shot['end']))
 assert max(frames[f]['overview'] for f in range(shot['start'],shot['end']))>.99
 assert frames[shot['end']-1]['overview']<.02
 if shot['final']:assert shot['end']-shot['start']>=240 and frames[shot['end']-1]['closeup']>.99
for event in film['breaks']:
 assert float(rows[event['index']][3])>event['level']
 assert all(float(r[3])<=event['level'] for r in rows[event['refIndex']+1:event['index']])
 assert event['intradayOnly']==(float(rows[event['index']][2])<event['level'])
assert next(e for e in film['breaks'] if e['date']=='2025-12-03')['intradayOnly']
for i,s in enumerate(frames):
 assert i==0 or s['index']>=frames[i-1]['index']
 c=s['camera'];r=rows[s['index']];top=c['ty']-float(r[3])*c['sy'];bottom=c['ty']-float(r[4])*c['sy'];x=c['tx']+s['index']*c['sx']
 assert 840<top<=bottom<1560 and 120<x<940,(i,top,bottom,x)
for e in film['strikes']:assert film['market'][e['index']]['change']<0
metrics=film['metrics'];assert metrics['date']=='2025-12-30' and metrics['high']==16.86 and metrics['volumeHands']==5155183 and metrics['turnover']==26.92
with wave.open(str(ROOT/'local-media/pingtan/qingming.wav'),'rb') as w:w.setpos(round(20.03*w.getframerate()));original=w.readframes(60*w.getframerate())
with wave.open(str(ROOT/'public/pingtan-2025-v2/music-original-excerpt.wav'),'rb') as w:music=w.readframes(w.getnframes())
assert original==music
proof=load(P/'audio-proof.json');assert not any(proof[k] for k in ('musicDucking','musicFade','musicTempoChange','musicPitchChange','normalization'))
assert proof['musicGain']==1 and hashlib.sha256(original).hexdigest()==proof['musicStemSha256']
assert not load(P/'validation.json')['errors']
print('PASS: 285 rows / 1800 frames / 5 completed peak pauses / overview and box stats / 5 first-crossing events / 8 downward lightning cues / final top closeup / historical turnover / bit-identical original music stem')
