"""Fit the candle camera to observed local OHLC and drive close-ups with returns."""
import json, math
from pathlib import Path
root=Path(__file__).resolve().parents[1]
raw=json.loads((root/'src/shibao-daily.json').read_text(encoding='utf-8'));base=json.loads((root/'src/shibao-v2-plan.json').read_text(encoding='utf-8'))
frames=[];x=0.;cy=-float(raw[0][2])*28;sx=3.6;sy=8.;anchorx=760.;bank=0.
for f,s in enumerate(base['frames']):
 i=int(s['index']);price=float(raw[i][2]);ret=price/float(raw[max(0,i-5)][2])-1
 power=max(0.,min(1.,(abs(ret)-.12)/.35))
 # A readable candle is already large in quiet markets; bursts shorten the window.
 lookback=round(43-21*power)
 recent=raw[max(0,i-lookback+1):i+1];hi=max(float(r[3]) for r in recent);lo=min(float(r[4]) for r in recent)
 span=max(hi-lo,max(.45,price*.055));mid=(hi+lo)/2
 targetx=900/(lookback*6);targety=600/(span*28)
 sx+=(targetx-sx)*.16;sy+=(targety-sy)*.15
 x+=(s['index']*6-x)*.25;cy+=(-mid*28-cy)*.22
 anchorx+=(760+max(-1,min(1,ret/.25))*35-anchorx)*.15
 # Accelerated historical playback must not outrun the close-up lens.
 x=max(x,s['index']*6-(935-anchorx)/sx)
 bank+=(max(-1.6,min(1.6,ret*4))-bank)*.14
 # Keep the live candle inside the stage even when prices gap during the time-lapse.
 high=float(raw[i][3]);low=float(raw[i][4]);target_center=-((high+low)/2)*28
 max_sy=660/max(.001,(high-low)*28)
 sy=min(sy,max_sy)
 top=1170+(-high*28-cy)*sy;bottom=1170+(-low*28-cy)*sy
 if top<845:cy-= (845-top)/sy
 if bottom>1505:cy+= (bottom-1505)/sy
 frames.append(dict(**s,cx=x,cy=cy,sx=sx,sy=sy,anchorX=anchorx,bank=bank,power=power,lookback=lookback))
base['frames']=frames;base['camera']='OHLC local range fit + return-driven dolly';base['minLow']=min(float(r[4]) for r in raw);base['maxHigh']=max(float(r[3]) for r in raw)
(root/'src/shibao-v3-plan.json').write_text(json.dumps(base,ensure_ascii=False,separators=(',',':')), encoding='utf-8')
print('Built',len(frames),'frames; candle widths',round(min(s['sx'] for s in frames)*3.5,1),'to',round(max(s['sx'] for s in frames)*3.5,1),'px')
