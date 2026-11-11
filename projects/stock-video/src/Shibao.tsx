import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import rows from './shibao-data.json';

const ink='#182b48', blue='#2259ed', red='#ef5161', green='#20a888', cream='#f6f4ea';
const data=rows.map(([date,open,close,high,low])=>({date:String(date),open:+open,close:+close,high:+high,low:+low}));
const fade=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
const Card:React.FC<{children:React.ReactNode;style?:React.CSSProperties}>=({children,style})=><div style={{background:'#fff',borderRadius:20,padding:'24px 30px',...style}}>{children}</div>;
const Chart:React.FC<{frame:number}>=({frame})=>{
 const left=52,top=30,w=920,h=310,max=30; const y=(v:number)=>top+h-v/max*h;
 const count=Math.floor(interpolate(frame,[155,410],[0,120],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}));
 return <svg width="1000" height="390" viewBox="0 0 1000 390">
 {[0,10,20,30].map(n=><g key={n}><line x1={left} x2={left+w} y1={y(n)} y2={y(n)} stroke="#dce4ec"/><text x="4" y={y(n)+6} fill="#718099" fontSize="18">{n}</text></g>)}
 {data.slice(0,count).map((d,i)=>{const x=left+(i+.5)*w/120; const c=d.close>=d.open?red:green;return <g key={d.date}><line x1={x} x2={x} y1={y(d.high)} y2={y(d.low)} stroke={c} strokeWidth="2"/><rect x={x-2.6} y={y(Math.max(d.open,d.close))} width="5.2" height={Math.max(2,Math.abs(y(d.open)-y(d.close)))} fill={c}/></g>})}
 {['2017','2019','2021','2023','2025'].map((s,i)=><text key={s} x={left+(i*24+1)*w/120} y="372" fill="#718099" fontSize="18">{s}</text>)}
 </svg>
};
export const Shibao:React.FC=()=>{const f=useCurrentFrame(); const intro=f<150, chart=f>=150&&f<570, analysis=f>=570&&f<870;return <AbsoluteFill style={{background:cream,color:ink,fontFamily:'PingFang SC, sans-serif',overflow:'hidden'}}>
 <div style={{position:'absolute',left:70,right:70,top:44,display:'flex',justifyContent:'space-between',fontSize:19,fontWeight:700,letterSpacing:2,color:blue}}><span>DATA STORIES / 数据观察</span><span>002703 · SZ</span></div>
 {intro&&<div style={{position:'absolute',left:95,top:140,opacity:fade(f,0,18)}}><div style={{fontSize:27,color:blue,fontWeight:700}}>十年行情观察  /  月 K</div><div style={{fontSize:86,fontWeight:800,marginTop:20,lineHeight:1.22}}>浙江世宝<br/><span style={{color:blue}}>十年走势</span></div><div style={{fontSize:26,marginTop:32,color:'#65758e'}}>2016.12 — 2026.11.06 · 前复权</div><div style={{position:'absolute',left:730,top:15,width:310,height:310,borderRadius:'50%',background:'#ffd34e'}}/><div style={{position:'absolute',left:805,top:68,width:160,height:190,background:blue,borderRadius:'18px 18px 70px 70px',rotate:'-12deg'}}/><div style={{position:'absolute',left:855,top:110,width:95,height:95,borderRadius:'50%',background:red}}/></div>}
 {chart&&<div style={{position:'absolute',left:70,top:100,right:70,opacity:fade(f,150,165)}}><div style={{fontSize:48,fontWeight:800}}>120 个月的<span style={{color:blue}}>价格轨迹</span></div><div style={{fontSize:21,color:'#65758e',marginTop:8}}>每根 K 线代表一个月 · 红涨绿跌 · 单位：元</div><Card style={{marginTop:22,padding:'20px 32px'}}><Chart frame={f}/></Card><div style={{fontSize:19,marginTop:14,color:'#65758e'}}>前复权价格会随后续分红等调整；2026 年 11 月为未完成月。</div></div>}
 {analysis&&<div style={{position:'absolute',left:75,top:110,right:75,opacity:fade(f,570,585)}}><div style={{fontSize:50,fontWeight:800}}>三个观察，<span style={{color:blue}}>看懂波动</span></div><div style={{display:'flex',gap:22,marginTop:45}}>
 <Card style={{width:340,opacity:fade(f,590,615)}}><div style={{fontSize:22,color:blue,fontWeight:700}}>01 / 低点</div><div style={{fontSize:57,fontWeight:800,marginTop:32}}>3.006</div><div style={{fontSize:23,lineHeight:1.6,marginTop:18}}>2018 年 10 月<br/>样本内最低月内价</div></Card>
 <Card style={{width:340,opacity:fade(f,650,675)}}><div style={{fontSize:22,color:blue,fontWeight:700}}>02 / 高点</div><div style={{fontSize:57,fontWeight:800,marginTop:32}}>28.69</div><div style={{fontSize:23,lineHeight:1.6,marginTop:18}}>2026 年 1 月<br/>样本内最高月内价</div></Card>
 <Card style={{width:340,opacity:fade(f,710,735)}}><div style={{fontSize:22,color:blue,fontWeight:700}}>03 / 近期</div><div style={{fontSize:57,fontWeight:800,marginTop:32}}>13.56</div><div style={{fontSize:23,lineHeight:1.6,marginTop:18}}>2026 年 11 月 6 日收盘<br/>较前复权年初基准约 −34%</div></Card></div><div style={{fontSize:19,color:'#65758e',marginTop:28}}>价格均为当前数据快照的前复权值；高低点为月内盘中价。</div></div>}
 {f>=870&&<div style={{position:'absolute',left:95,top:135,right:95,opacity:fade(f,870,890)}}><div style={{fontSize:26,color:blue,fontWeight:700}}>读图提示 / TAKEAWAY</div><div style={{fontSize:66,fontWeight:800,lineHeight:1.35,marginTop:28}}>十年大幅波动<br/><span style={{color:blue}}>历史不代表未来</span></div><div style={{fontSize:26,lineHeight:1.8,color:'#52637c',marginTop:28}}>K 线呈现价格变化，不能单独解释涨跌原因。<br/>分析还需结合财报、行业与风险承受能力。</div><div style={{fontSize:19,marginTop:32,color:'#7b8799'}}>资料：腾讯行情月 K；公司 2025 年报 · 截至 2026.11.06<br/>仅作历史数据展示，不构成投资建议。</div></div>}
 <div style={{position:'absolute',bottom:0,left:0,height:7,width:`${Math.min(100,f/1049*100)}%`,background:blue}}/>
 </AbsoluteFill>};
