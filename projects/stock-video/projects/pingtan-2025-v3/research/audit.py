"""Independent 120s data, downward-range, event and unchanged-music checks."""
import datetime,hashlib,json,math,wave
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1]
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
f=load(ROOT/'src/stock-videos/pingtan-2025-v3.json');v2=load(ROOT/'src/stock-videos/pingtan-2025-v2.json');d=f['data'];frames=f['plan']['frames']
assert d==v2['data'] and len(d)==285 and len(frames)==3600
assert len(f['shots'])==9 and sum(s['direction']=='down' for s in f['shots'])==4
peak=next(i for i,r in enumerate(d) if r[0]=='2025-12-30');assert float(d[peak][3])==16.86
for p in f['shots']:
 start=p['baseIndex'];end=p['index'];down=p['direction']=='down'
 assert p['sessions']==end-start+1
 assert p['boards']==sum(bool(m['isDown'] if down else m['isUp']) for m in f['market'][start:end+1])
 assert p['calendarDays']==(datetime.date.fromisoformat(p['date'])-datetime.date.fromisoformat(p['baseDate'])).days
 if down:
  assert start==peak and p['low']==min(float(r[4]) for r in d[peak+1:end+1])
  assert abs(p['amplitude']-(p['low']/16.86-1)*100)<1e-9
 else:assert p['high']==max(float(r[3]) for r in d[:end+1])
 assert all(frames[i]['index']==end and frames[i]['growth']==1 for i in range(p['start'],p['end']))
 assert max(frames[i]['overview'] for i in range(p['start'],p['end']))>.99
 if p['final']:assert p['end']-p['start']>=330 and frames[p['end']-1]['closeup']==1
last=[p for p in f['shots'] if p['direction']=='down'][-1]
assert last['date']=='2026-07-21' and last['low']==4.95 and round(last['amplitude'],2)==-70.64 and last['sessions']==133 and last['boards']==4
for e in f['breaks']:
 assert e['refIndex']<e['index']
 if e['direction']=='down':
  assert float(d[e['index']][4])<e['level'] and f['market'][e['index']]['change']<0
  assert e['intradayOnly']==(float(d[e['index']][2])>e['level'])
 else:
  assert float(d[e['index']][3])>e['level']
  assert all(float(r[3])<=e['level'] for r in d[e['refIndex']+1:e['index']])
for i,s in enumerate(frames):
 assert i==0 or s['index']>=frames[i-1]['index']
 c=s['camera'];r=d[s['index']];y0=c['ty']-float(r[3])*c['sy'];y1=c['ty']-float(r[4])*c['sy'];x=c['tx']+s['index']*c['sx']
 assert 840<y0<=y1<1560 and 120<x<940,(i,y0,y1,x)
source=(ROOT/'src/StockTechVideo.tsx').read_text(encoding='utf-8')
assert '前复权 · 日 K' not in source and '腾讯历史日 K' not in source and 'top:1835' not in source
assert 'TechRange' in source and 'ShockGlass' in source and 'ThunderBolt' in source
with wave.open(str(ROOT/'local-media/pingtan/qingming.wav'),'rb') as w:w.setpos(round(20.03*w.getframerate()));original=w.readframes(120*w.getframerate())
with wave.open(str(ROOT/'public/pingtan-2025-v3/music-original-excerpt.wav'),'rb') as w:music=w.readframes(w.getnframes())
assert music==original
proof=load(P/'audio-proof.json');assert proof['musicStemSha256']==hashlib.sha256(original).hexdigest()
assert not any(proof[k] for k in ('musicDucking','musicTempoChange','musicPitchChange','musicFade','normalization'))
assert proof['musicGain']==1 and proof['masterGain']==.7
assert 'no oscillator synthesis' in proof['sfxMethod'] and any(c['name']=='charge-alt' and c['onsetSeconds']<c['frame']/30 for c in proof['cues'])
assert not load(P/'validation.json')['errors']
print('PASS: 3600 frames, 285 OHLC rows, 5 upside/4 downside pauses, high-to-low drawdowns, boards and dates, 31 downward breaks, 18 lightning cues, active framing, removed labels, real SFX and unchanged original vocal music stem')
