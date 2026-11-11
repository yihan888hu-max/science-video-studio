import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import raw from './shibao-daily.json';
import {events} from './shibao-detect';
const d=raw.map(r=>({date:r[0],open:+r[1],close:+r[2],high:+r[3],low:+r[4]}));
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const tween=(f:number,x:number[],y:number[])=>interpolate(f,x,y,clamp);
const glow='#66fff1', dim='#98b8c8';
const Scene:React.FC<{frame:number;event:typeof events[number];number:number}>=({frame,event,number})=>{
 const start=Math.max(0,event.index-27), end=Math.min(d.length-1,event.index+5), bars=d.slice(start,end+1), eventLocal=event.index-start;
 // Timeline follows trading sessions; the visual response is tied to the detected market event.
 const reveal=tween(frame,[0,95],[0,bars.length-1]);
 const trigger=eventLocal/revealDuration(bars.length)*95;
 const age=frame-trigger;
 const z=tween(age,[-6,3,16,50],[1,1.06,1.2,1.2]);
 const shake=age>=0&&age<15?Math.sin(age*2.7)*Math.exp(-age/5)*7:0;
 const lo=Math.min(...bars.map(x=>x.low))*.95,hi=Math.max(...bars.map(x=>x.high))*1.05;
 const W=960,H=330,X=(i:number)=>45+i*W/(bars.length-1),Y=(n:number)=>25+(hi-n)/(hi-lo)*H;
 const rising=event.change>0, color=rising?'#ff637f':'#4df1bb';
 const fromX=X(Math.max(0,eventLocal-5)),toX=X(eventLocal);
 const triangle=tween(age,[-5,12],[0,1]);
 return <AbsoluteFill style={{background:'radial-gradient(ellipse at 65% 40%,#14344b,#061421 60%,#030a11)',color:'#e9f9ff',fontFamily:'PingFang SC, sans-serif'}}>
 <div style={{position:'absolute',left:65,right:65,top:35,display:'flex',justifyContent:'space-between',fontSize:19,letterSpacing:2,color:glow}}><span>浙江世宝 · 002703 / 日 K</span><span>波动事件 {String(number+1).padStart(2,'0')} / {events.length}</span></div>
 <div style={{position:'absolute',left:68,top:84,fontSize:35,fontWeight:700}}>{event.start} — {event.date}</div>
 <div style={{position:'absolute',right:70,top:84,textAlign:'right',fontSize:24,color}}>5 个交易日收盘 {event.change>0?'+':''}{(event.change*100).toFixed(1)}%</div>
 <div style={{position:'absolute',left:85,top:162,width:1110,height:380,overflow:'hidden',border:'1px solid #24495c',borderRadius:12}}>
 <div style={{width:1100,height:380,scale:z,translate:`${shake}px ${shake*.35}px`,transformOrigin:`${toX+25}px ${Y(d[event.index].close)}px`}}>
 <svg width="1100" height="380" viewBox="0 0 1100 380">
 {[0,1,2,3].map(i=><g key={i}><line x1="45" x2="1005" y1={25+i*110} y2={25+i*110} stroke="#264a5a"/></g>)}
 {age>=-4&&<rect x={fromX-10} y="25" width={toX-fromX+20} height="330" fill={color} opacity={tween(age,[-4,4,30],[0,.11,.06])}/>}
 {bars.map((r,i)=>i<=reveal?<g key={r.date}><line x1={X(i)} x2={X(i)} y1={Y(r.high)} y2={Y(r.low)} stroke={r.close>=r.open?'#ff697c':'#4df1bb'} strokeWidth="2"/><rect x={X(i)-7} y={Y(Math.max(r.open,r.close))} width="14" height={Math.max(2,Y(Math.min(r.open,r.close))-Y(Math.max(r.open,r.close)))} fill={r.close>=r.open?'#ff697c':'#4df1bb'}/></g>:null)}
 {age>=0&&<><circle cx={toX} cy={Y(d[event.index].close)} r={12+triangle*12} fill="none" stroke={color} strokeWidth="2" opacity={1-triangle*.55}/><circle cx={toX} cy={Y(d[event.index].close)} r="4" fill="#fff"/></>}
 </svg></div></div>
 <div style={{position:'absolute',left:85,top:565,color:dim,fontSize:19}}>高亮区间收盘：{d[event.index-5].close.toFixed(2)} → {d[event.index].close.toFixed(2)} 元 · 前复权</div>
 <div style={{position:'absolute',left:85,top:610,fontSize:19,color:dim}}>镜头由 5 日涨跌幅阈值触发；动画震动不改变价格数据。</div>
 <div style={{position:'absolute',right:88,top:565,fontSize:25,color,opacity:tween(age,[-3,7],[0,1]),display:'flex',alignItems:'center',gap:12}}><svg width="38" height="38" viewBox="0 0 38 38"><path d={`M 19 ${tween(triangle,[0,1],[2,rising?1:37])} L ${tween(triangle,[0,1],[35,34])} 19 L 19 ${tween(triangle,[0,1],[36,rising?24:14])} L ${tween(triangle,[0,1],[3,4])} 19 Z`} fill={color}/></svg>{rising?'快速上冲':'快速下砸'}</div>
 </AbsoluteFill>;
};
const revealDuration=(n:number)=>Math.max(1,n-1);
export const ShibaoImpact:React.FC=()=>{const f=useCurrentFrame();const intro=120, each=120; if(f<intro)return <AbsoluteFill style={{background:'#061421',color:'#e9f9ff',fontFamily:'PingFang SC,sans-serif',justifyContent:'center',paddingLeft:95}}><div style={{fontSize:22,color:glow,letterSpacing:3}}>DATA-DRIVEN MOTION / 002703</div><div style={{fontSize:67,fontWeight:700,lineHeight:1.35,marginTop:24}}>浙江世宝<br/><span style={{color:glow}}>捕捉快速波动</span></div><div style={{fontSize:24,color:dim,lineHeight:1.8,marginTop:30}}>5 个交易日收盘涨幅 ≥ 25% 或跌幅 ≤ −20%<br/>相邻同向信号合并；镜头跟随每组最强信号。</div></AbsoluteFill>;
 const current=Math.floor((f-intro)/each);if(current>=events.length)return <AbsoluteFill style={{background:'#061421',color:'#e9f9ff',fontFamily:'PingFang SC,sans-serif',justifyContent:'center',alignItems:'center',fontSize:38}}>历史波动，不代表未来走势</AbsoluteFill>;
 return <Scene frame={(f-intro)%each} event={events[current]} number={current}/>;};
