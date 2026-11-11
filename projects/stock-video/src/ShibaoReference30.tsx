import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, staticFile, useCurrentFrame} from 'remotion';
import raw from './shibao-daily.json';
import plan from './shibao-v2-plan.json';

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

/** Data space, camera space, and fixed screen text are kept independent. */
const ContinuousChart:React.FC<{frame:number}>=({frame})=>{
 const s=plan.frames[frame],cursor=s.index,idx=Math.min(data.length-1,Math.floor(cursor));
 const pull=interpolate(frame,[795,839],[0,1],{...clamp,easing:ease});
 const enter=tween(frame,[30,58],[0,1]);
 const sx=lerp(s.zoom,900/((data.length-1)*6),pull),sy=lerp(s.zoom,430/((plan.maxClose-plan.minClose)*28),pull);
 const tx=lerp(640-s.x*s.zoom,90,pull),ty=lerp(1090-s.y*s.zoom,950+plan.maxClose*28*(430/((plan.maxClose-plan.minClose)*28)),pull);
 const shock=s.impact*(1-pull),shakeX=Math.sin(frame*2.6)*shock*12,shakeY=Math.cos(frame*3.3)*shock*7;
 const X=(i:number)=>i*6*sx+tx+shakeX,Y=(p:number)=>-p*28*sy+ty+shakeY;
 const price=s.price,tipX=X(cursor),tipY=Y(price),rising=idx===0||data[idx].close>=data[idx-1].close,color=rising?up:down;
 const first=frame>=795?0:Math.max(0,idx-320);
 let all='',red='',green='';
 for(let i=Math.max(1,first);i<=idx;i++){
  const a=data[i-1],b=data[i],seg=`M${X(i-1).toFixed(2)},${Y(a.close).toFixed(2)}L${X(i).toFixed(2)},${Y(b.close).toFixed(2)} `;
  all+=seg;if(b.close>=a.close)red+=seg;else green+=seg;
 }
 if(cursor>idx&&idx<data.length-1){const seg=`M${X(idx)},${Y(data[idx].close)}L${tipX},${tipY}`;all+=seg;if(data[idx+1].close>=data[idx].close)red+=seg;else green+=seg;}
 const particles=Array.from({length:72},(_,i)=>{
  const life=(frame+i*5)%28/28,angle=rand(i)*Math.PI*2,v=40+rand(i+78)*170;
  return {x:tipX+Math.cos(angle)*v*life,y:tipY+Math.sin(angle)*v*life+life*life*70,r:1.5+rand(i+127)*2.3,a:(1-life)*(.2+.8*Math.min(1,Math.abs(s.change5)*2+shock))};
 });
 return <svg width={W} height={H} style={{position:'absolute',inset:0,opacity:enter}}><defs>
 <clipPath id="chart-clip-v2"><rect x="0" y="790" width="1080" height="770"/></clipPath>
 <filter id="line-glow-v2" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
 <filter id="tip-glow-v2" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="11"/></filter>
 <linearGradient id="fall-v2" x1="0" y1="0" x2="0" y2="1"><stop stopColor={color} stopOpacity=".19"/><stop offset="1" stopColor={color} stopOpacity="0"/></linearGradient>
 </defs><g clipPath="url(#chart-clip-v2)">
 {[5,10,15,20,25,30].map(p=>{const y=Y(p);return <g key={p} opacity={.32}><path d={`M0 ${y}H1080`} stroke="#315350" strokeWidth="1"/><text x="1005" y={y-12} fill="#7d9694" fontSize="20" fontFamily={font}>{p.toFixed(0)}</text></g>;})}
 {Array.from({length:Math.floor(idx/30)+1},(_,k)=>k*30).filter(i=>i>=first).map(i=><path key={i} d={`M${X(i)} 790V1560`} stroke="#294743" strokeWidth="1" opacity=".25"/>)}
 {data.slice(Math.max(first,idx-60),idx+1).map((b,j)=>{const i=Math.max(first,idx-60)+j;return <path key={i} d={`M${X(i)} ${Y(b.close)}V1560`} stroke={b.close>=b.open?up:down} strokeWidth={Math.max(1,sx*2)} opacity={.06*(1-pull)}/>;})}
 {data.slice(Math.max(first,idx-105),idx+1).map((b,j)=>{const i=Math.max(first,idx-105)+j,c=b.close>=b.open?up:down;return <g key={i} opacity={.5*(1-pull)}><line x1={X(i)} x2={X(i)} y1={Y(b.high)} y2={Y(b.low)} stroke={c} strokeWidth="1.3"/><rect x={X(i)-1.5*sx} width={3*sx} y={Y(Math.max(b.open,b.close))} height={Math.max(1,(Math.abs(b.close-b.open))*28*sy)} fill={c}/></g>;})}
 <path d={red} fill="none" stroke={up} strokeWidth="13" opacity=".55" filter="url(#line-glow-v2)"/><path d={green} fill="none" stroke={down} strokeWidth="13" opacity=".55" filter="url(#line-glow-v2)"/>
 <path d={red} fill="none" stroke={up} strokeWidth="4.3" strokeLinejoin="round"/><path d={green} fill="none" stroke={down} strokeWidth="4.3" strokeLinejoin="round"/>
 <path d={all} fill="none" stroke="#faffef" strokeWidth="1.2" strokeOpacity=".9"/>
 <path d={`M${tipX} ${tipY}H1000`} stroke={color} strokeDasharray="5 9" opacity={.36*(1-pull)}/>
 <path d={`M${tipX} ${tipY}V1560`} stroke={color} strokeWidth="24" opacity={.10*(1-pull)}/>
 <g opacity={1-pull}>{particles.map((p,i)=><circle key={i} cx={p.x} cy={p.y} r={p.r} fill={i%5===0?gold:color} opacity={p.a}/>)}
 <circle cx={tipX} cy={tipY} r={19+shock*15} fill={color} opacity=".65" filter="url(#tip-glow-v2)"/><circle cx={tipX} cy={tipY} r="6" fill="#fff8df"/>
 {shock>.02&&<circle cx={tipX} cy={tipY} r={16+(1-shock)*110} fill="none" stroke={color} strokeWidth="2" opacity={shock}/>}</g>
 </g></svg>;
};
const Header:React.FC<{frame:number}>=({frame})=>{
 const s=plan.frames[frame],r=data[Math.floor(s.index)],color=s.change5>=0?up:down;
 return <div style={{position:'absolute',left:86,right:86,top:145,fontFamily:font}}>
 <div style={{display:'flex',alignItems:'baseline',gap:22}}><span style={{fontSize:34,fontWeight:700,color:ink}}>浙江世宝</span><span style={{fontSize:23,color:muted,letterSpacing:3}}>SZ.002703</span><span style={{marginLeft:'auto',fontSize:22,color:muted}}>A 股 · 前复权</span></div>
 <div style={{display:'flex',alignItems:'baseline',gap:28,marginTop:17}}><span style={{fontSize:116,lineHeight:1.1,fontWeight:850,color,fontVariantNumeric:'tabular-nums',letterSpacing:-3,textShadow:`0 0 30px ${color}44`}}>{r.close.toFixed(2)}</span><span style={{fontSize:31,color:muted}}>元 / 收盘</span></div>
 <div style={{fontSize:52,fontWeight:700,color:ink,letterSpacing:1,marginTop:9,fontVariantNumeric:'tabular-nums'}}>{format(r.date)}</div>
 <div style={{display:'flex',alignItems:'center',gap:20,marginTop:20}}><span style={{color:muted,fontSize:24}}>近 5 个交易日</span><span style={{color,fontSize:34,fontWeight:750,background:`${color}14`,padding:'3px 12px',borderRadius:3}}>{percent(r.close/data[Math.max(0,Math.floor(s.index)-5)].close-1)}</span></div>
 </div>;
};
const Annotation:React.FC<{frame:number}>=({frame})=>{
 const matches=plan.annotations.filter(a=>a.frame<=frame),a=matches[matches.length-1];
 if(!a||frame>=790)return null;
 const next=plan.annotations.find(b=>b.frame>a.frame),duration=Math.min(69,(next?.frame??795)-a.frame),age=frame-a.frame;
 if(age>=duration)return null;
 const alpha=tween(age,[0,5,duration-8,duration],[0,1,1,0]),color=a.change>0?up:down;
 return <div style={{position:'absolute',left:86,right:86,top:535,color:ink,opacity:alpha,translate:`0 ${tween(age,[0,9],[15,0])}px`,fontFamily:font}}>
 <div style={{fontSize:47,fontWeight:750,letterSpacing:1}}>{a.title}</div><div style={{display:'flex',alignItems:'baseline',gap:25,marginTop:8}}><span style={{fontSize:103,fontWeight:850,lineHeight:1.2,letterSpacing:-3,color,textShadow:`0 0 40px ${color}30`}}>{percent(a.change)}</span><span style={{fontSize:23,color:muted}}>5 日收盘</span></div>
 <div style={{fontSize:25,color:'#b5c5c5',marginTop:8}}>{format(a.start)} — {format(a.date)}</div>
 </div>;
};
const Progress:React.FC<{frame:number}>=({frame})=>{
 const idx=plan.frames[frame].index,p=data[Math.floor(idx)].close,x=90+idx/(data.length-1)*900,y=1738-(p-3)/26*106;
 return <div style={{position:'absolute',inset:0,fontFamily:font}}><svg width={W} height={H}><path d="M90 1750H990" stroke="#1d363b"/><path d={miniPath} fill="none" stroke="#57777d" strokeWidth="1.6"/><path d={`M${x} 1610V1750`} stroke={gold} opacity=".4" strokeDasharray="3 8"/><circle cx={x} cy={y} r="5" fill={gold}/></svg><div style={{position:'absolute',left:90,right:90,top:1770,display:'flex',justifyContent:'space-between',color:'#728b90',fontSize:23}}><span>2016</span><span style={{color:'#b7ccca'}}>十年全景 / 日线</span><span>2026</span></div><div style={{position:'absolute',left:86,right:86,top:1834,color:'#607d83',fontSize:19,lineHeight:1.65}}>腾讯历史行情快照 · 2016.11.08—2026.11.06<br/>主线为每日收盘价，局部叠加日 K · 非实时行情</div></div>;
};
export const ShibaoReference30:React.FC=()=>{
 const f=useCurrentFrame(),intro=tween(f,[0,8,42,64],[0,1,1,0]),end=tween(f,[800,824],[0,1]);
 return <AbsoluteFill style={{background:'#02070a',fontFamily:font,overflow:'hidden'}}>
 <AbsoluteFill style={{background:'radial-gradient(ellipse at 52% 59%,#09272470,transparent 51%),linear-gradient(#020406,#040b0e)'}}/>
 <ContinuousChart frame={f}/><Header frame={f}/><Annotation frame={f}/><Progress frame={f}/>
 <div style={{position:'absolute',left:86,right:86,top:550,color:ink,opacity:intro}}><div style={{fontSize:24,color:gold,letterSpacing:4}}>十年日 K · 连续回放</div><div style={{fontSize:78,fontWeight:800,lineHeight:1.35,marginTop:24}}>急涨与急跌<br/><span style={{color:gold}}>都在同一条线上</span></div></div>
 <div style={{position:'absolute',left:86,right:86,top:535,color:ink,opacity:end}}><div style={{fontSize:49,fontWeight:750}}>十年走完，回看全局</div><div style={{fontSize:25,color:muted,marginTop:22}}>区间首末收盘变化</div><div style={{fontSize:107,fontWeight:850,color:down,lineHeight:1.2,letterSpacing:-3}}>{percent(plan.totalReturn)}</div><div style={{fontSize:26,color:'#b5c5c5',marginTop:9}}>19.82 → 13.56 元 · 前复权</div></div>
 <div style={{position:'absolute',left:86,right:86,top:1472,color:ink,opacity:end}}><div style={{height:1,background:'#4c7267',marginBottom:25}}/><div style={{fontSize:37,fontWeight:650}}>短期急涨 ≠ 长期收益</div><div style={{fontSize:23,color:muted,marginTop:14}}>首末变化不含分红现金流，不代表个人收益</div></div>
 <div style={{position:'absolute',top:85,left:86,color:'#4f7175',fontSize:19,letterSpacing:5}}>SHIBAO / A DECADE IN MOTION</div>
 <Audio src={staticFile('shibao-v2/mix.wav')}/>
 </AbsoluteFill>;
};
