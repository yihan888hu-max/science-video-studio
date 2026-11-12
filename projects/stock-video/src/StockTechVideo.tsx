import React from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame} from 'remotion';
import {TechRange,ShockGlass,ThunderBolt} from './StockTechEffects';
import type referenceFilm from './stock-videos/pingtan-2025-v3.json';
type Film=typeof referenceFilm;
const W=1080,H=1920,UP='#ff425e',DOWN='#12f5bb',GOLD='#ffd67b',WHITE='#eef6f3',MUTED='#9ab1b4';
const FONT='PingFang SC, Microsoft YaHei, Noto Sans CJK SC, sans-serif';
const clamp=(v:number,a=0,b=1)=>Math.max(a,Math.min(b,v));
const smooth=(v:number)=>{v=clamp(v);return v*v*(3-2*v);};
const rnd=(v:number)=>{const x=Math.sin(v*127.1+311.7)*43758.5453;return x-Math.floor(x);};
const dateText=(v:string)=>v.replace(/-/g,'.');

export const StockTechVideo:React.FC<{film:Film}>=({film})=>{
 const f=useCurrentFrame(),state=film.plan.frames[f],idx=state.index,settled=state.settledIndex;
 const data=film.data.map(r=>({date:r[0],open:+r[1],close:+r[2],high:+r[3],low:+r[4],volume:+r[5]}));
 const current=data[idx],quote=data[settled],market=film.market[settled];
 const shot=state.shot>=0?film.shots[state.shot]:null;
 const finalClose=!!shot?.final&&state.closeup>.3;
 const glass=film.breaks.filter(e=>f>=e.frame&&f-e.frame<72);
 const lightning=film.strikes.filter(e=>f>=e.frame&&f-e.frame<24);
 const impact=Math.max(0,...glass.map(e=>Math.exp(-(f-e.frame)/11)),...lightning.map(e=>Math.exp(-(f-e.frame)/4)));
 const shakeX=Math.sin(f*2.7)*impact*12,shakeY=Math.cos(f*3.4)*impact*9;
 const cam=state.camera,X=(i:number)=>cam.tx+i*cam.sx+shakeX,Y=(price:number)=>cam.ty-price*cam.sy+shakeY;
 const bodyWidth=clamp(cam.sx*.52,.65,40),depth=bodyWidth*.37,dz=-depth*.65;
 const previousLevel=[{date:'2025-09-02',index:1,high:3.72},...film.shots.filter(p=>p.direction==='up')].filter(p=>p.index<=settled).slice(-1)[0];
 const broken=previousLevel?film.breaks.some(e=>e.refIndex===previousLevel.index&&e.frame<=f):false;
 const quoteColor=market.change>=0?UP:DOWN;
 const end=smooth((f-3546)/22),enter=smooth((f-4)/18);
 const chartOpacity=smooth((f-7)/15);
 const activeRise=film.plan.segments.find(s=>s.index===idx);
 const completionAge=activeRise?f-activeRise.complete:100;
 const ticks=[1,2,3,4,5,6,8,10,12,14,16,18,20].filter(p=>Y(p)>820&&Y(p)<1565);
 const reached=data.slice(0,idx+1);
 const minClose=Math.min(...data.map(r=>r.close)),maxClose=Math.max(...data.map(r=>r.close));
 const mini=reached.map((r,i)=>`${i?'L':'M'}${(90+i/(data.length-1)*900).toFixed(1)} ${(1742-(r.close-minClose)/(maxClose-minClose)*92).toFixed(1)}`).join(' ');
 const overviewLabel=shot&&state.overview>.65;
 const lastBreak=glass.filter(e=>e.index===idx).slice(-1)[0];
 const downShot=shot?.direction==='down';
 const activeDown=glass.filter(e=>e.direction==='down');
 const pressure=Math.max(0,...activeDown.map(e=>Math.exp(-(f-e.frame)/30)));
 const support=film.breaks.filter(e=>e.direction==='down'&&e.frame<=f).slice(-1)[0];
 return <AbsoluteFill style={{background:'#020608',overflow:'hidden',fontFamily:FONT,color:WHITE}}>
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 60% 62%,#0a262b90,transparent 64%),linear-gradient(#020406,#030b0c)'}}/>
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 65% 59%,#d7194788,#65051b55 37%,transparent 79%)',opacity:finalClose?.95:state.red*.82}}/>
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 65% 67%,#00b67c77,#00342666 40%,transparent 78%)',opacity:state.green*.86}}/>
  <svg width={W} height={H} style={{position:'absolute',inset:0,opacity:chartOpacity}}>
   <defs>
    <clipPath id="cine-clip"><rect x="0" y="800" width="1080" height="790"/></clipPath>
    <filter id="cine-glow"><feGaussianBlur stdDeviation="5"/></filter>
    <filter id="cine-bloom" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="12"/></filter>
    <linearGradient id="tech-pane"><stop stopColor="#a1efff" stopOpacity=".03"/><stop offset=".48" stopColor="#e4ffff" stopOpacity=".25"/><stop offset="1" stopColor="#70c8ff" stopOpacity=".04"/></linearGradient>
    <linearGradient id="cine-red"><stop stopColor="#93172b" stopOpacity=".10"/><stop offset=".24" stopColor="#d72c4b" stopOpacity=".25"/><stop offset=".74" stopColor="#ff7189" stopOpacity=".44"/><stop offset="1" stopColor="#ffc5ce" stopOpacity=".18"/></linearGradient>
    <linearGradient id="cine-green"><stop stopColor="#064e40" stopOpacity=".10"/><stop offset=".24" stopColor="#04b28b" stopOpacity=".25"/><stop offset=".74" stopColor="#40efbf" stopOpacity=".44"/><stop offset="1" stopColor="#c5ffe9" stopOpacity=".18"/></linearGradient>
    <linearGradient id="cine-glass"><stop stopColor="#9eefff" stopOpacity=".03"/><stop offset=".5" stopColor="#e8feff" stopOpacity=".16"/><stop offset="1" stopColor="#a7e6ff" stopOpacity=".03"/></linearGradient>
   </defs>
   <g clipPath="url(#cine-clip)">
    {ticks.map(p=><g key={p}><path d={`M0 ${Y(p)}H1080`} stroke="#39554c" opacity=".33"/><text x="1010" y={Y(p)-12} fill="#688981" fontSize="22">{p}</text></g>)}
    {reached.filter((_,i)=>i%8===0).map((_,j)=>{const x=X(j*8);return <path key={j} d={`M${x} 800V1590`} stroke="#25433d" opacity=".20"/>;})}
    {previousLevel&&<g opacity={broken?.35:.9}>
     <path d={`M${Math.max(25,X(previousLevel.index))} ${Y(previousLevel.high)}H1055`} stroke={GOLD} strokeDasharray="9 10" strokeWidth="1.8"/>
     {state.overview<.35&&<text x="1015" y={Y(previousLevel.high)-18} textAnchor="end" fill={GOLD} fontSize="25">前高 {previousLevel.high.toFixed(2)}</text>}
    </g>}
    {support&&<g opacity={state.overview>.35?.18:.6}><path d={`M${Math.max(20,X(support.refIndex))} ${Y(support.level)}H1055`} stroke={DOWN} strokeWidth="2" strokeDasharray="8 10"/>{state.overview<.35&&<text x="1010" y={Y(support.level)+30} textAnchor="end" fill={DOWN} fontSize="24">前低 {support.level.toFixed(2)}</text>}</g>}
    {reached.map((original,i)=>{
     if(X(i)<-65||X(i)>1140)return null;
     const g=i===idx?state.growth:1,close=original.open+(original.close-original.open)*g;
     const high=Math.max(original.open,close,original.open+(original.high-original.open)*g),low=Math.min(original.open,close,original.open+(original.low-original.open)*g);
     const rise=original.close===original.open?film.market[i].change>=0:original.close>original.open,color=rise?UP:DOWN,x=X(i)-bodyWidth/2,t=Y(Math.max(original.open,close)),bottom=Math.max(t+1.6,Y(Math.min(original.open,close))),height=bottom-t;
     return <g key={i}>
      <path d={`M${X(i)} ${Y(high)}V${Y(low)}`} stroke={color} strokeWidth={bodyWidth+12} opacity=".44" filter="url(#cine-glow)"/>
      {i>idx-20&&<path d={`M${X(i)} ${bottom}V1580`} stroke={color} strokeWidth={bodyWidth*.8} opacity=".045"/>}
      <rect x={x+depth} y={t+dz} width={bodyWidth} height={height} fill="none" stroke={color} strokeWidth=".7" opacity=".32"/>
      <path d={`M${X(i)} ${Y(high)}V${Y(low)}`} stroke={color} strokeWidth={clamp(bodyWidth*.11,.8,2.4)}/>
      <path d={`M${X(i)} ${Y(high)}V${Y(low)}`} stroke="#d8ffef" strokeWidth=".55" opacity=".8"/>
      <path d={`M${x+bodyWidth} ${t}l${depth} ${dz}V${bottom+dz}L${x+bodyWidth} ${bottom}Z`} fill={color} fillOpacity=".17" stroke={color} strokeWidth=".7"/>
      <path d={`M${x} ${t}l${depth} ${dz}h${bodyWidth}l${-depth} ${-dz}Z`} fill={rise?'#ffd0d7':'#c2ffe6'} opacity=".82"/>
      <rect x={x} y={t} width={bodyWidth} height={height} fill={rise?'url(#cine-red)':'url(#cine-green)'} stroke={rise?'#ffa7b5':'#8affd7'} strokeWidth={clamp(bodyWidth*.06,.55,1.3)}/>
      <path d={`M${x+bodyWidth*.52} ${t+2}V${bottom-2}`} stroke={color} strokeWidth={bodyWidth*.3} opacity=".56" filter="url(#cine-glow)"/>
      <path d={`M${x+bodyWidth*.63} ${t+1}V${bottom-1}`} stroke="#ecffff" strokeWidth={clamp(bodyWidth*.1,.4,2.3)} opacity=".23"/>
      <path d={`M${x+bodyWidth*.2} ${t+1}V${bottom-1}`} stroke="#ffffef" opacity=".52" strokeWidth={clamp(bodyWidth*.055,.4,1.1)}/>
     </g>;
    })}
    {shot&&state.overview>.35&&<TechRange shot={shot} elapsed={state.shotElapsed} overview={state.overview} frame={f} X={X} Y={Y}/>}
    {glass.map(e=><ShockGlass key={e.direction+e.frame} event={e} frame={f} X={X} Y={Y}/>)}
    {lightning.map(e=><ThunderBolt key={e.frame} event={e} frame={f} x={X(e.index)} y={Y(data[e.index].low)}/>)}
    <circle cx={X(idx)} cy={Y(current.open+(current.close-current.open)*state.growth)} r={14+impact*12} fill={market.change>=0?UP:DOWN} opacity=".65" filter="url(#cine-bloom)"/>
    {completionAge>=0&&completionAge<17&&market.isUp&&Array.from({length:13},(_,i)=>{const t=completionAge/17,x=X(idx)+(rnd(i+idx)-.5)*55,y=Y(current.close)-t*(40+rnd(i+99)*90);return <path key={i} d={`M${x} ${y+12}V${y}`} stroke={i%4===0?GOLD:'#ffb1bf'} opacity={(1-t)*.8} strokeWidth="1.6"/>;})}
   </g>
  </svg>
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 55% 62%,transparent 26%,#000c 78%,#000 100%)',opacity:pressure*.8,pointerEvents:'none'}}/>
  <div style={{position:'absolute',left:82,right:82,top:77,color:'#55787e',fontSize:19,letterSpacing:5}}>PINGTAN / SEPT 2025 — NOV 2026</div>
  <div style={{position:'absolute',left:82,right:82,top:137,opacity:enter}}>
   <div style={{display:'flex',gap:22,alignItems:'baseline'}}><span style={{fontSize:36,fontWeight:750}}>平潭发展</span><span style={{fontSize:23,color:MUTED,letterSpacing:3}}>SZ.000592</span></div>
   <div style={{marginTop:20,color:quoteColor,fontSize:106,fontWeight:800,fontFamily:'Arial, sans-serif',lineHeight:1.1,fontVariantNumeric:'tabular-nums',textShadow:`0 0 34px ${quoteColor}44`}}>{quote.close.toFixed(2)}<span style={{fontSize:29,color:MUTED,marginLeft:25,fontWeight:400}}>元 / 收盘</span></div>
   <div style={{fontSize:47,fontWeight:700,marginTop:13,letterSpacing:1}}>{dateText(quote.date)}</div>
  </div>
  <div style={{position:'absolute',left:82,right:82,top:438}}>
   {overviewLabel&&shot?<>
    <div style={{fontSize:25,letterSpacing:3,color:GOLD}}>{downShot?'顶部之后 · 盘中阶段新低':(shot.final?'全区间最高':'阶段高点')} · {downShot?'高点至低点':'低点至高点'}</div>
    <div style={{fontSize:105,fontWeight:900,color:downShot?DOWN:UP,lineHeight:1.2,fontVariantNumeric:'tabular-nums'}}>{shot.amplitude>=0?'+':'−'}{Math.abs(shot.amplitude).toFixed(2)}<span style={{fontSize:52}}>%</span></div>
    <div style={{display:'flex',gap:35,alignItems:'baseline',marginTop:6}}><span style={{fontSize:39,fontWeight:700}}>{shot.sessions} 个交易日</span><span style={{fontSize:39,fontWeight:700,color:GOLD}}>{shot.boards} 个{downShot?'跌停':'涨停'}板</span></div>
    <div style={{fontSize:25,color:MUTED,marginTop:18}}>{dateText(shot.baseDate)} — {dateText(shot.date)} · 交易日含首尾</div>
    <div style={{fontSize:23,color:'#7f9d9b',marginTop:10}}>{(downShot?shot.high:shot.low).toFixed(2)} → {(downShot?shot.low:shot.high).toFixed(2)} 元 · {downShot?'高点至低点跌幅':'低高振幅'}</div>
   </>:finalClose?<>
    <div style={{fontSize:23,color:GOLD,letterSpacing:4}}>顶部回看 / 情绪演绎</div>
    <div style={{fontSize:78,fontWeight:850,letterSpacing:3,marginTop:12,textShadow:'0 0 40px #ff3a6380'}}>最后的狂欢</div>
    <div style={{fontSize:28,color:'#e4adb6',marginTop:8}}>贪婪，在新高处被放大</div>
    <div style={{display:'flex',justifyContent:'space-between',borderTop:'1px solid #67323d',marginTop:25,paddingTop:18}}>
     {[['最高价',film.metrics.high.toFixed(2),'元'],['当日成交量',(film.metrics.volumeHands/10000).toFixed(2),'万手'],['当日换手率',film.metrics.turnover.toFixed(2),'%']].map(([label,value,unit])=><div key={label}><div style={{fontSize:24,color:MUTED}}>{label}</div><div style={{fontSize:45,fontWeight:750,color:GOLD,marginTop:8}}>{value}<span style={{fontSize:23,marginLeft:5}}>{unit}</span></div></div>)}
    </div>
   </>:end>.05?<>
    <div style={{fontSize:25,color:GOLD}}>2025.09 — 2026.11 · 全程回看</div><div style={{fontSize:62,fontWeight:800,lineHeight:1.45,marginTop:20}}>新高并不意味着终点<br/><span style={{color:'#8fe9d0'}}>也可能是回撤的起点</span></div>
   </>:f<75?<>
    <div style={{fontSize:25,color:GOLD}}>从 2025 年 9 月开始</div><div style={{fontSize:70,fontWeight:800,lineHeight:1.4,marginTop:20}}>突破、分歧<br/><span style={{color:GOLD}}>再到最后的新高</span></div>
   </>:<>
    <div style={{fontSize:70,fontWeight:850,color:market.isDown||market.change<-.04?DOWN:(market.label?UP:WHITE)}}>{lastBreak?(lastBreak.direction==='down'?(lastBreak.intradayOnly?'盘中失守前低':'跌破前低'):(lastBreak.intradayOnly?'盘中突破前高':'突破前高')):market.label||'调整与蓄势'}</div>
    <div style={{fontSize:29,color:MUTED,lineHeight:1.5,marginTop:12}}>{lastBreak?(lastBreak.direction==='down'?`失守 ${lastBreak.level.toFixed(2)} 元 · ${market.isDown?'跌停下挫':'下行压力延续'}`:`越过 ${lastBreak.level.toFixed(2)} 元${lastBreak.intradayOnly?' · 收盘回落，未守住前高':''}`):market.sub}</div>
    {quote.date==='2025-11-21'&&<div style={{marginTop:20,borderLeft:`3px solid ${GOLD}`,paddingLeft:20,fontSize:27,lineHeight:1.6,color:'#c7dad5'}}>11月18—20日停牌核查<br/>21日恢复交易</div>}
   </>}
  </div>
  <svg width={W} height={H} style={{position:'absolute',inset:0,pointerEvents:'none'}}><path d="M90 1753H990" stroke="#23413f"/><path d={mini} fill="none" stroke="#678782" strokeWidth="1.6"/><circle cx={90+settled/(data.length-1)*900} cy={1742-(quote.close-minClose)/(maxClose-minClose)*92} r="5" fill={GOLD}/></svg>
  <div style={{position:'absolute',left:90,right:90,top:1780,display:'flex',justifyContent:'space-between',fontSize:22,color:'#7b9798'}}><span>2025.09</span><span style={{color:'#b3c7c4'}}>285 个交易日 / 历史回看</span><span>2026.11</span></div>
  {/* Constant master gain for all sound; the vocal track has no ducking or DSP. */}
  <Audio src={staticFile('pingtan-2025-v3/mix.wav')} volume={0.7}/>
 </AbsoluteFill>;
};
