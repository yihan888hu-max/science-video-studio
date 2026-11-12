"""Independent Pingtan data, timeline and source assertions. No network."""
import datetime,json,math
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
p=Path(__file__).resolve().parents[1];root=p.parents[1]
load=lambda path:json.loads(path.read_text(encoding='utf-8'))
film=load(root/'src/stock-videos/pingtan-2025-v1.json');raw=load(p/'daily.json');un=load(p/'unadjusted.json')
assert film['data']==raw and len(raw)==446
assert raw[0][0]=='2025-01-02' and raw[-1][0]=='2026-11-11'
assert load(p/'research/data-sources.json')['identity']['symbol']=='sz000592'
assert len({r[0] for r in raw})==len(raw)
for rows in (raw,un):
 assert all(rows[i][0]<rows[i+1][0] for i in range(len(rows)-1))
 for r in rows:
  datetime.date.fromisoformat(r[0]);o,c,h,l,v=map(float,r[1:6])
  assert all(math.isfinite(x) for x in (o,c,h,l,v)) and h>=max(o,c,l) and l<=min(o,c,h) and v>=0
previous=None;limits={}
for r in un:
 if previous is not None:limits[r[0]]=((Decimal(previous[2])*Decimal('1.1')).quantize(Decimal('.01'),rounding=ROUND_HALF_UP),(Decimal(previous[2])*Decimal('.9')).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
 previous=r
d={r[0]:r for r in raw};m={r['date']:r for r in film['market']}
assert all(m[date]['isUp']==(Decimal(d[date][2])==limits[date][0]) for date in d)
cluster=[r for r in raw if '2025-10-17'<=r[0]<='2025-11-17']
assert len(cluster)==22 and sum(Decimal(r[2])==limits[r[0]][0] for r in cluster)==14
assert m['2025-10-29']['streak']==5 and m['2025-11-05']['streak']==4
assert m['2025-11-17']['streak']==3 and len(set(d['2025-11-17'][1:5]))==1
assert round((1-float(d['2025-10-28'][5])/float(d['2025-10-27'][5]))*100,1)==82.0
assert Decimal(d['2025-10-30'][3])==limits['2025-10-30'][0] and not m['2025-10-30']['isUp']
assert not any(date in d for date in ('2025-11-18','2025-11-19','2025-11-20'))
assert all(m[date]['isDown'] for date in ('2025-11-21','2025-11-24','2026-01-15','2026-01-16','2026-01-19'))
assert len(set(d['2026-01-19'][1:5]))==1
top=max(raw,key=lambda r:float(r[3]));assert top[0]=='2025-12-30' and float(top[3])==16.86
start=next(i for i,r in enumerate(raw) if r[0]=='2025-10-16');peak=next(i for i,r in enumerate(raw) if r[0]==top[0])
assert all(float(raw[start][4])<float(raw[i][4]) for i in (start-2,start-1,start+1,start+2))
assert round((float(top[3])/float(raw[start][4])-1)*100,2)==403.28 and peak-start+1==51
for card in film['peaks']:
 assert card['end']-card['frame']>=45
for s in film['plan']['segments']:
 if s['critical']:
  frames=film['plan']['frames'];assert frames[s['start']]['growth']==0
  assert all(x['growth']==1 for x in frames[s['start']+2:s['end']])
  assert s['end']-s['start']>=6
assert len(film['plan']['frames'])==900
assert not load(p/'validation.json')['errors']
for msg in film['catalysts']:assert msg['from']>=msg['published']
for message in film['market']+film['catalysts']:assert all(word not in str(message) for word in ('航天发展','商业航天','流动性枯竭','卡异动'))
print('PASS: 446 OHLC rows, 22 sessions/14 boards, 5/4/3 consecutive boards, halt gap, two peaks, 3 lower limits, timing holds, message dates, safe camera, no inherited aerospace captions')
