import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import raw from './shibao-daily.json';
import {events} from './shibao-detect';

const data=raw.map(r=>({date:r[0],open:+r[1],close:+r[2],high:+r[3],low:+r[4]}));
const dates=['2022-06-17','2022-07-12','2023-07-06','2023-07-24'];
const chosen=dates.map(date=>{const e=events.find(x=>x.date===date);if(!e) throw new Error(`Missing event ${date}`);return e;});
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const mix=(f:number,a:number[],b:number[])=>interpolate(f,a,b,clamp);
const font='PingFang SC, Noto Sans CJK SC, sans-serif';
const notes=['上涨有多快？','急跌接踵而至','一年后再次冲高','涨势之后仍有回撤'];
const details=['短期涨幅不能替代风险判断','短期大涨之后，价格也可能迅速回落','不同年份都出现过剧烈波动','急涨与急跌都可能改变持有体验'];
const accent=(up:boolean)=>up?'#ff657e':'#5df4cb';
const segmentFrames=165;
const triggerFor=(index:number)=>{const start=Math.max(0,index-22),end=Math.min(data.length-1,index+2);return Math.round(110*(index-start)/(end-start));};
const Background=()=> <><AbsoluteFill style={{background:'radial-gradient(ellipse at 70% 32%, #102b3b 0%, #071622 42%, #030b12 100%)'}}/><svg style={{position:'absolute',inset:0}} width="1280" height="720"><defs><pattern id="grid30" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0H0V80" fill="none" stroke="#78e4e5" strokeOpacity=".055"/></pattern></defs><rect width="1280" height="720" fill="url(#grid30)"/></svg></>;
const Top=()=> <div style={{position:'absolute',top:35,left:70,right:70,display:'flex',justifyContent:'space-between',color:'#81d7df',fontSize:18,letterSpacing:3,fontWeight:600}}><span>浙江世宝 / 002703</span><span>DATA STORY · 日 K</span></div>;
const EventScene:React.FC<{event:typeof chosen[number],number:number}>=({event,number})=>{
 const f=useCurrentFrame(), start=Math.max(0,event.index-22), end=Math.min(data.length-1,event.index+2), bars=data.slice(start,end+1), local=event.index-start, trigger=triggerFor(event.index), age=f-trigger;
 const lo=Math.min(...bars.map(b=>b.low))*.96, hi=Math.max(...bars.map(b=>b.high))*1.04;
 const X=(i:number)=>38+i*760/(bars.length-1),Y=(n:number)=>24+(hi-n)/(hi-lo)*300;
 const revealed=mix(f,[0,110],[0,bars.length-1]), up=event.change>0, color=accent(up);
 const zoom=mix(age,[-6,4,15,53],[1,1.03,1.15,1.15]);
 const shake=age>=0&&age<14?Math.sin(age*2.65)*Math.exp(-age/4.5)*8:0;
 const focusX=X(local),focusY=Y(data[event.index].close);
 const line=bars.slice(0,Math.floor(revealed)+1).map((b,i)=>`${i?'L':'M'}${X(i).toFixed(1)} ${Y(b.close).toFixed(1)}`).join(' ');
 const ring=mix(age,[0,18],[8,42]);
 return <AbsoluteFill style={{color:'#edf9fb',fontFamily:font}}><Background/><Top/>
 <div style={{position:'absolute',top:92,left:70,fontSize:21,color:'#93aeb9',letterSpacing:2}}>历史波动样本 / {String(number+1).padStart(2,'0')}</div>
 <div style={{position:'absolute',top:128,left:68,fontSize:44,fontWeight:700}}>{notes[number]}</div>
 <div style={{position:'absolute',top:199,left:70,width:830,height:360,overflow:'hidden',border:'1px solid #244456',borderRadius:12,background:'#071521b8'}}>
 <div style={{width:830,height:360,scale:zoom,translate:`${shake}px ${shake*.4}px`,transformOrigin:`${focusX}px ${focusY}px`}}>
 <svg width="830" height="360" viewBox="0 0 830 360"><defs><filter id="neon30"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
 {[0,1,2,3].map(i=><line key={i} x1="38" x2="798" y1={25+i*100} y2={25+i*100} stroke="#32505e" strokeOpacity=".55"/>)}
 {age>=-6&&<rect x={X(local-5)-12} y="24" width={X(local)-X(local-5)+24} height="300" fill={color} opacity={mix(age,[-6,4,30],[0,.14,.08])}/>}
 {bars.map((b,i)=>i<=revealed?<g key={b.date}><line x1={X(i)} x2={X(i)} y1={Y(b.high)} y2={Y(b.low)} stroke={accent(b.close>=b.open)} strokeWidth="2"/><rect x={X(i)-6} y={Y(Math.max(b.open,b.close))} width="12" height={Math.max(2,Y(Math.min(b.open,b.close))-Y(Math.max(b.open,b.close)))} fill={accent(b.close>=b.open)}/></g>:null)}
 <path d={line} fill="none" stroke="#c5fff8" strokeOpacity=".7" strokeWidth="1.7" filter="url(#neon30)"/>
 {age>=0&&<><circle cx={focusX} cy={focusY} r={ring} fill="none" stroke={color} strokeWidth="3" opacity={mix(age,[0,18],[.95,0])}/><circle cx={focusX} cy={focusY} r="5" fill="#fff" filter="url(#neon30)"/></>}
 </svg></div></div>
 <div style={{position:'absolute',left:936,top:207,width:285}}><div style={{fontSize:19,color:'#93aeb9'}}>5 个交易日收盘变化</div><div style={{fontSize:57,fontWeight:800,color,marginTop:18,opacity:mix(age,[-8,5],[.32,1])}}>{up?'+':''}{(event.change*100).toFixed(1)}%</div><div style={{height:2,background:color,opacity:.65,margin:'23px 0'}}/><div style={{fontSize:22,lineHeight:1.65,color:'#d9eaf0'}}>{event.start}<br/>至 {event.date}</div><div style={{fontSize:19,color:'#92aeb9',marginTop:20}}>收盘 {data[event.index-5].close.toFixed(2)} → {data[event.index].close.toFixed(2)} 元</div></div>
 <div style={{position:'absolute',left:70,bottom:86,fontSize:26,fontWeight:600}}>{details[number]}</div>
 <div style={{position:'absolute',left:70,right:70,bottom:35,color:'#7795a4',fontSize:16,display:'flex',justifyContent:'space-between'}}><span>前复权日线 · 高亮区间为 5 个交易日</span><span>数据快照截至 2026-11-06</span></div>
 </AbsoluteFill>;
};
export const ShibaoStory30:React.FC=()=>{const f=useCurrentFrame();return <AbsoluteFill style={{fontFamily:font,background:'#030b12'}}>
 <Sequence from={0} durationInFrames={90}><Background/><Top/><div style={{position:'absolute',left:74,top:174,color:'#eafcff'}}><div style={{color:'#6fe6e1',fontSize:22,letterSpacing:4}}>一只股票的波动切片</div><div style={{fontSize:67,lineHeight:1.3,fontWeight:800,marginTop:23}}>浙江世宝<br/><span style={{color:'#82f9e8'}}>急涨之后，会怎样？</span></div><div style={{fontSize:23,color:'#afc8d1',marginTop:30}}>从日 K 看四段真实历史波动</div></div><svg style={{position:'absolute',right:70,top:220}} width="370" height="240" viewBox="0 0 370 240"><path d="M10 205 L55 185 L90 196 L130 135 L160 150 L205 52 L240 92 L280 20 L320 88 L360 70" fill="none" stroke="#60eadf" strokeWidth="4" strokeDasharray="650" strokeDashoffset={mix(f,[0,75],[650,0])}/></svg></Sequence>
 {chosen.map((event,i)=><Sequence key={event.date} from={90+i*segmentFrames} durationInFrames={segmentFrames}><EventScene event={event} number={i}/><Sequence from={triggerFor(event.index)} durationInFrames={24}><Audio src={staticFile('shibao-impact.wav')} volume={0.32}/></Sequence></Sequence>)}
 <Sequence from={750} durationInFrames={150}><Background/><Top/><div style={{position:'absolute',left:74,top:170,color:'#eafcff'}}><div style={{fontSize:23,color:'#72e8dd',letterSpacing:3}}>看完这四段，更重要的是</div><div style={{fontSize:54,fontWeight:800,lineHeight:1.45,marginTop:26}}>波动不是单方向的<br/><span style={{color:'#92f6e9'}}>涨得快，也可能跌得快</span></div><div style={{fontSize:23,color:'#abc2cb',marginTop:26,lineHeight:1.7}}>区间涨跌幅不等于个人收益<br/>历史走势不预示未来表现</div></div><div style={{position:'absolute',bottom:35,left:74,color:'#7894a0',fontSize:16}}>腾讯行情前复权数据快照 · 截至 2026-11-06 · 不构成投资建议</div></Sequence>
 </AbsoluteFill>;};
