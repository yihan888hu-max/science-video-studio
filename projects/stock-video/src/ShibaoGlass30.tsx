import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, staticFile, useCurrentFrame} from 'remotion';
import raw from './shibao-2021-v4.json';
import plan from './shibao-v4-plan.json';

const W=1080,H=1920,up='#ff425e',down='#12f5bb',gold='#ffd56a';
const ink='#edf6f5',muted='#94a9ad';
const font='PingFang SC, sans-serif';
const data=raw.map(r=>({date:r[0],open:+r[1],close:+r[2],high:+r[3],low:+r[4]}));
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const ease=Easing.bezier(.2,.8,.2,1);
const tween=(f:number,a:number[],b:number[])=>interpolate(f,a,b,clamp);
const lerp=(a:number,b:number,t:number)=>a+(b-a)*t;
const percent=(n:number)=>`${n>=0?'+':'−'}${Math.abs(n*100).toFixed(1)}%`;
const format=(s:string)=>s.replace(/-/g,'.');
const rand=(n:number)=>{const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v);};
const miniPath=data.map((r,i)=>`${i?'L':'M'}${(90+i/(data.length-1)*900).toFixed(1)} ${(1738-(r.close-3)/26*106).toFixed(1)}`).join(' ');

/** OHLC candle faces stay in price coordinates; the lens fits the local range. */
const ContinuousChart:React.FC<{frame:number}>=({frame})=>{
 const s=plan.frames[frame],idx=Math.min(data.length-1,Math.floor(s.index));
 const pull=interpolate(frame,[804,848],[0,1],{...clamp,easing:ease});
 const enter=tween(frame,[30,58],[0,1]);
 const fullSy=490/((plan.maxHigh-plan.minLow)*28);
 const sx=lerp(s.sx,900/((data.length-1)*6),pull),sy=lerp(s.sy,fullSy,pull);
 const tx=lerp(s.anchorX-s.cx*s.sx,90,pull),ty=lerp(1170-s.cy*s.sy,900+plan.maxHigh*28*fullSy,pull);
 const shock=s.impact*(1-pull),shakeX=Math.sin(frame*2.6)*shock*12,shakeY=Math.cos(frame*3.3)*shock*8;
 const X=(i:number)=>i*6*sx+tx+shakeX,Y=(p:number)=>-p*28*sy+ty+shakeY;
 const price=s.price,tipX=X(idx),tipY=Y(price),rising=data[idx].close>=data[idx].open,color=rising?up:down;
 const first=frame>=804?0:Math.max(0,idx-160);
 const candles=data.slice(first,idx+1).map((b,j)=>{
  const i=first+j;
  if(i!==idx||s.growth>=1)return {b,i};
  const close=b.open+(b.close-b.open)*s.growth;
  return {i,b:{...b,close,high:Math.max(b.open,close,b.open+(b.high-b.open)*s.growth),low:Math.min(b.open,close,b.open+(b.low-b.open)*s.growth)}};
 }).filter(({i})=>X(i)>-80&&X(i)<1130);
 const width=Math.max(.45,3.55*sx),depth=width*.42*(1-pull*.9),dz=-depth*.68;
 const visibleSpan=780/(sy*28),step=[.1,.2,.25,.5,1,2,2.5,5,10,20].find(x=>x>=visibleSpan/5)??20;
 const middle=-s.cy/28,lowTick=Math.floor((middle-visibleSpan)/step)*step;
 const ticks=Array.from({length:18},(_,k)=>lowTick+k*step).filter(p=>p>0&&Y(p)>790&&Y(p)<1555);
 let redGlow='',greenGlow='';
 for(const {b,i} of candles){const seg=`M${X(i)} ${Y(b.high)}V${Y(b.low)} `;if(b.close>=b.open)redGlow+=seg;else greenGlow+=seg;}
 const particles=Array.from({length:60},(_,i)=>{
  const life=(frame+i*5)%24/24,angle=rand(i)*Math.PI*2,v=25+rand(i+78)*(80+s.power*100);
  return {x:tipX+Math.cos(angle)*v*life,y:tipY+Math.sin(angle)*v*life+life*life*55,r:1.3+rand(i+127)*2.2,a:(1-life)*(.18+.65*s.power+.2*shock)};
 });
 return <svg width={W} height={H} style={{position:'absolute',inset:0,opacity:enter}}><defs>
 <clipPath id="candle-clip"><rect x="0" y="770" width="1080" height="810"/></clipPath>
 <filter id="candle-glow"><feGaussianBlur stdDeviation="5"/></filter>
 <filter id="candle-tip" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="12"/></filter>
 <linearGradient id="red-front" x1="0" y1="0" x2="1" y2="0"><stop stopColor="#9b1d3a" stopOpacity=".25"/><stop offset=".22" stopColor="#ed284c" stopOpacity=".48"/><stop offset=".73" stopColor="#ff657a" stopOpacity=".62"/><stop offset="1" stopColor="#ffb5bc" stopOpacity=".35"/></linearGradient>
 <linearGradient id="green-front" x1="0" y1="0" x2="1" y2="0"><stop stopColor="#075c4c" stopOpacity=".25"/><stop offset=".22" stopColor="#05b78d" stopOpacity=".48"/><stop offset=".73" stopColor="#22edb9" stopOpacity=".62"/><stop offset="1" stopColor="#a4ffe1" stopOpacity=".35"/></linearGradient>
 </defs><g clipPath="url(#candle-clip)"><g transform={`rotate(${s.bank*(1-pull)} 540 1170)`}>
 {ticks.map(p=>{const y=Y(p);return <g key={p}><path d={`M0 ${y}H1080`} stroke="#365750" strokeWidth="1" opacity=".38"/><text x="1000" y={y-13} fill="#668b83" fontSize="21" fontFamily={font}>{p.toFixed(step<1?2:0)}</text></g>;})}
 {Array.from({length:Math.floor(idx/10)+1},(_,k)=>k*10).filter(i=>X(i)>-20&&X(i)<1100).map(i=><path key={i} d={`M${X(i)} 770L${X(i)+24*(1-pull)} 1580`} stroke="#254b43" strokeWidth="1" opacity=".3"/>)}
 <path d={redGlow} fill="none" stroke={up} strokeWidth={width+7} opacity=".24" filter="url(#candle-glow)"/><path d={greenGlow} fill="none" stroke={down} strokeWidth={width+7} opacity=".24" filter="url(#candle-glow)"/>
 {candles.map(({b,i})=>{
  const x=X(i)-width/2,t=Y(Math.max(b.open,b.close)),bottom=Math.max(t+1.8,Y(Math.min(b.open,b.close))),h=bottom-t,c=b.close>=b.open?up:down,isUp=b.close>=b.open;
  return <g key={i}>
   <rect x={x+depth} y={t+dz} width={width} height={h} fill="none" stroke={c} strokeWidth=".8" opacity=".28"/>
   {i>idx-18&&<path d={`M${X(i)+depth} ${bottom}V1580`} stroke={c} strokeWidth={Math.max(1,width*.75)} opacity={.035*(1-pull)}/>}
   <line x1={X(i)} x2={X(i)} y1={Y(b.high)} y2={Y(b.low)} stroke={c} strokeWidth={Math.max(.7,Math.min(2.2,width*.12))}/>
   <line x1={X(i)} x2={X(i)} y1={Y(b.high)} y2={Y(b.low)} stroke="#c6ffe2" strokeWidth=".5" opacity=".85"/>
   <path d={`M${x+width} ${t}l${depth} ${dz}V${bottom+dz}L${x+width} ${bottom}Z`} fill={isUp?'#d82251':'#04bd91'} fillOpacity={.32} stroke={c} strokeWidth=".7"/>
   <path d={`M${x} ${t}l${depth} ${dz}h${width}l${-depth} ${-dz}Z`} fill={isUp?'#ffb4b7':'#b7ffe5'} opacity=".62"/>
   <rect x={x} y={t} width={width} height={h} fill={isUp?'url(#red-front)':'url(#green-front)'} stroke={isUp?'#ff8e9c':'#76ffd3'} strokeWidth={Math.max(.5,Math.min(1.2,width*.06))}/>
   <path d={`M${x+width*.33} ${t+2}V${bottom-2}`} stroke="#ffffff" strokeWidth={Math.max(.5,width*.12)} opacity=".17"/>
   <path d={`M${x+width*.17} ${t+1}V${bottom-1}`} stroke="#fff6e8" strokeWidth={Math.max(.4,width*.045)} opacity=".52"/>
  </g>;
 })}
 <path d={`M${tipX+width/2+depth} ${tipY}H990`} stroke={color} strokeDasharray="5 9" opacity={.40*(1-pull)}/>
 <g opacity={1-pull}>
 {particles.map((p,i)=><circle key={i} cx={p.x} cy={p.y} r={p.r} fill={i%5===0?gold:color} opacity={p.a}/>)}
 <circle cx={tipX} cy={tipY} r={18+shock*18} fill={color} opacity=".8" filter="url(#candle-tip)"/><circle cx={tipX} cy={tipY} r="4.5" fill="#fff5dc"/>
 {shock>.02&&<circle cx={tipX} cy={tipY} r={15+(1-shock)*125} fill="none" stroke={color} strokeWidth="2" opacity={shock}/>}</g>
 </g></g></svg>;
};
const Header:React.FC<{frame:number}>=({frame})=>{
 const s=plan.frames[frame],r=data[s.settledIndex],color=r.close/data[Math.max(0,s.settledIndex-5)].close>=1?up:down;
 return <div style={{position:'absolute',left:86,right:86,top:145,fontFamily:font}}>
 <div style={{display:'flex',alignItems:'baseline',gap:22}}><span style={{fontSize:34,fontWeight:700,color:ink}}>浙江世宝</span><span style={{fontSize:23,color:muted,letterSpacing:3}}>SZ.002703</span><span style={{marginLeft:'auto',fontSize:22,color:muted}}>A 股 · 前复权</span></div>
 <div style={{display:'flex',alignItems:'baseline',gap:28,marginTop:17}}><span style={{fontSize:116,lineHeight:1.1,fontWeight:850,color,fontVariantNumeric:'tabular-nums',letterSpacing:-3,textShadow:`0 0 30px ${color}44`}}>{r.close.toFixed(2)}</span><span style={{fontSize:31,color:muted}}>元 / 收盘</span></div>
 <div style={{fontSize:52,fontWeight:700,color:ink,letterSpacing:1,marginTop:9,fontVariantNumeric:'tabular-nums'}}>{format(r.date)}</div>
 <div style={{display:'flex',alignItems:'center',gap:20,marginTop:20}}><span style={{color:muted,fontSize:24}}>近 5 个交易日</span><span style={{color,fontSize:34,fontWeight:750,background:`${color}14`,padding:'3px 12px',borderRadius:3}}>{percent(r.close/data[Math.max(0,s.settledIndex-5)].close-1)}</span></div>
 </div>;
};
const Annotation:React.FC<{frame:number}>=({frame})=>{
 const s=plan.frames[frame];
 if(!s.critical||frame>=plan.playEnd)return null;
 const color=s.changeDay>0?up:down,alpha=s.growth<1?.5:1;
 return <div style={{position:'absolute',left:86,right:86,top:530,color:ink,opacity:alpha,fontFamily:font}}>
 <div style={{fontSize:44,fontWeight:750}}>{s.changeDay>0?'极速拉升 · 近景':'快速下压 · 近景'}</div>
 <div style={{display:'flex',alignItems:'baseline',gap:25,marginTop:8}}><span style={{fontSize:87,fontWeight:850,lineHeight:1.2,letterSpacing:-3,color,textShadow:`0 0 40px ${color}30`}}>{percent(s.changeDay)}</span><span style={{fontSize:24,color:muted}}>当日收盘变化</span></div>
 <div style={{fontSize:24,color:'#b5c5c5',marginTop:12}}>近 5 个交易日 {percent(s.change5)}</div>
 </div>;
};
const Progress:React.FC<{frame:number}>=({frame})=>{
 const idx=plan.frames[frame].settledIndex,p=data[Math.floor(idx)].close,x=90+idx/(data.length-1)*900,y=1738-(p-3)/26*106;
 return <div style={{position:'absolute',inset:0,fontFamily:font}}><svg width={W} height={H}><path d="M90 1750H990" stroke="#1d363b"/><path d={miniPath} fill="none" stroke="#57777d" strokeWidth="1.6"/><path d={`M${x} 1610V1750`} stroke={gold} opacity=".4" strokeDasharray="3 8"/><circle cx={x} cy={y} r="5" fill={gold}/></svg><div style={{position:'absolute',left:90,right:90,top:1770,display:'flex',justifyContent:'space-between',color:'#728b90',fontSize:23}}><span>2021</span><span style={{color:'#b7ccca'}}>全程回看 / 日 K</span><span>2026.11</span></div><div style={{position:'absolute',left:86,right:86,top:1834,color:'#607d83',fontSize:19,lineHeight:1.65}}>腾讯历史行情快照 · 2021.01.04—2026.11.11<br/>主图为日 K · 全景自适应缩放 · 非实时行情</div></div>;
};
export const ShibaoGlass30:React.FC=()=>{
 const f=useCurrentFrame(),intro=tween(f,[0,8,42,64],[0,1,1,0]),end=tween(f,[812,836],[0,1]);
 return <AbsoluteFill style={{background:'#02070a',fontFamily:font,overflow:'hidden'}}>
 <AbsoluteFill style={{background:'radial-gradient(ellipse at 52% 59%,#09272470,transparent 51%),linear-gradient(#020406,#040b0e)'}}/>
 <ContinuousChart frame={f}/><Header frame={f}/><Annotation frame={f}/><Progress frame={f}/>
 <div style={{position:'absolute',left:86,right:86,top:550,color:ink,opacity:intro}}><div style={{fontSize:24,color:gold,letterSpacing:4}}>2021 至今 · 立体日 K</div><div style={{fontSize:78,fontWeight:800,lineHeight:1.35,marginTop:24}}>急涨与急跌<br/><span style={{color:gold}}>都在同一条线上</span></div></div>
 <div style={{position:'absolute',left:86,right:86,top:535,color:ink,opacity:end}}><div style={{fontSize:49,fontWeight:750}}>从 2021，回看这段走势</div><div style={{fontSize:25,color:muted,marginTop:22}}>区间首末收盘变化</div><div style={{fontSize:107,fontWeight:850,color:plan.totalReturn>=0?up:down,lineHeight:1.2,letterSpacing:-3}}>{percent(plan.totalReturn)}</div><div style={{fontSize:26,color:'#b5c5c5',marginTop:9}}>{plan.firstClose.toFixed(2)} → {plan.lastClose.toFixed(2)} 元 · 前复权</div></div>
 <div style={{position:'absolute',left:86,right:86,top:1472,color:ink,opacity:end}}><div style={{height:1,background:'#4c7267',marginBottom:25}}/><div style={{fontSize:37,fontWeight:650}}>急涨与急跌，都在这段历史里</div><div style={{fontSize:23,color:muted,marginTop:14}}>历史走势不预示未来，区间变化不代表个人收益</div></div>
 <div style={{position:'absolute',top:85,left:86,color:'#4f7175',fontSize:19,letterSpacing:5}}>SHIBAO / 2021 TO NOW</div>
 <Audio src={staticFile('shibao-v4/mix.wav')}/>
 </AbsoluteFill>;
};
