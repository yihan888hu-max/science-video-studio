"""Film-specific historical assertions, independent of render frame effects."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1];root=p.parents[1];film=json.loads((root/'src/stock-videos/aerospace-2025-v1.json').read_text(encoding='utf-8'));d={r[0]:list(map(float,r[1:])) for r in film['data']};m={r['date']:r for r in film['market']}
assert m['2025-11-17']['streak']==2 and len(set(d['2025-11-17'][:4]))==1
assert round((1-d['2025-11-17'][4]/d['2025-11-14'][4])*100,1)==92.1
assert m['2025-11-20']['streak']==5 and d['2025-11-20'][0]==d['2025-11-20'][1]==d['2025-11-20'][2]>d['2025-11-20'][3]
assert m['2025-11-21']['isDown'] and not m['2025-11-21']['isUp']
cluster=[r for r in film['market'] if '2025-11-14'<=r['date']<='2025-12-01'];assert len(cluster)==12 and sum(r['isUp'] for r in cluster)==8
assert d['2025-12-04'][2]==18.92 and d['2025-12-04'][1]<18.92
for peak in film['peaks']:
 assert round(peak['amplitudePct'],2)==(310.17 if peak['date']=='2025-12-30' else 392.13)
 assert peak['end']-peak['frame']>=45
for s in film['plan']['segments']:
 if s['critical']:
  f=film['plan']['frames'];assert f[s['start']]['growth']==0 and f[s['start']+1]['growth']<1
  assert all(x['growth']==1 for x in f[s['start']+2:s['end']])
  assert s['end']-s['start']>=6
for date in ('2025-11-21','2026-01-13'):
 s=next(s for s in film['plan']['segments'] if film['data'][s['index']][0]==date)
 assert film['plan']['frames'][s['end']-1]['green']>.9
assert not any('流动性枯竭' in str(x) for x in film['market']+film['catalysts'])
assert not json.loads((p/'validation.json').read_text(encoding='utf-8'))['errors']
print('PASS: historical boards, T candle, volume, 12-day cluster, peak statistics, completion-then-hold, green sell-off, caption evidence boundaries')
