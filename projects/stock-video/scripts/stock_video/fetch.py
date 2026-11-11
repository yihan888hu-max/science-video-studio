"""Download Tencent yearly adjusted/raw snapshots without project dependencies.
Existing raw files are reused unless --refresh is explicit. No credentials needed.
"""
import argparse,datetime,json,re,subprocess
from pathlib import Path
from urllib.parse import urlencode
p=argparse.ArgumentParser();p.add_argument('--symbol',required=True);p.add_argument('--from',dest='start',required=True);p.add_argument('--to',dest='end',required=True);p.add_argument('--project',type=Path,required=True);p.add_argument('--refresh',action='store_true');a=p.parse_args()
assert re.fullmatch(r'(sz|sh)\d{6}',a.symbol),'Use exchange prefix, e.g. sz000547'
start=datetime.date.fromisoformat(a.start);end=datetime.date.fromisoformat(a.end);assert start<=end
folder=a.project;rawdir=folder/'research/raw';rawdir.mkdir(parents=True,exist_ok=True);rows={'qfq':{},'bfq':{}};ledger=[];identity=None
for year in range(start.year-1,end.year+1):
 for mode in ('qfq','bfq'):
  param=f'{a.symbol},day,{year}-01-01,{year}-12-31,320,{"qfq" if mode=="qfq" else ""}'
  url='https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?'+urlencode({'param':param},safe=',')
  file=rawdir/f'tencent-{year}-{mode}.json'
  reused=file.exists() and not a.refresh
  if not reused:
   result=subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','35',url],capture_output=True,text=True,check=True);obj=json.loads(result.stdout)
   assert a.symbol in obj.get('data',{}),'Missing symbol in provider response';file.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':')), encoding='utf-8')
  obj=json.loads(file.read_text(encoding='utf-8'))['data'][a.symbol];data=obj.get('qfqday' if mode=='qfq' else 'day',obj.get('day',[]));assert data,f'No daily prices {year} {mode}'
  quote=obj.get('qt',{}).get(a.symbol,[])
  if quote:
   assert quote[2]==a.symbol[2:];identity={'symbol':a.symbol,'name':quote[1],'quoteTimestamp':quote[30] if len(quote)>30 else None}
  for r in data:rows[mode][r[0]]=r
  ledger.append({'path':str(file),'url':url,'cacheReused':reused})
daily=[r for date,r in sorted(rows['qfq'].items()) if a.start<=date<=a.end];assert daily,'Empty requested interval'
unadjusted=[r for date,r in sorted(rows['bfq'].items()) if date<=a.end];assert any(r[0]<daily[0][0] for r in unadjusted),'Need prior session'
for name,value in [('daily.json',daily),('unadjusted.json',unadjusted),('research/data-sources.json',{'requestedStart':a.start,'requestedEnd':a.end,'actualLast':daily[-1][0],'identity':identity,'requests':ledger})]:
 file=folder/name;file.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
print(json.dumps({'identity':identity,'sessions':len(daily),'actualLast':daily[-1][0]},ensure_ascii=False))
