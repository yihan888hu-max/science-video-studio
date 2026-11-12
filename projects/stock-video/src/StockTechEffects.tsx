import React from 'react';
const rnd=(n:number)=>{const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x);};
const cap=(v:number)=>Math.max(0,Math.min(1,v));
const ease=(v:number)=>{v=cap(v);return v*v*(3-2*v);};
type Shot={direction:string;index:number;baseIndex:number;low:number;high:number;final:boolean};

export const TechRange:React.FC<{shot:Shot;elapsed:number;overview:number;frame:number;X:(v:number)=>number;Y:(v:number)=>number}>=({shot,elapsed,overview,frame,X,Y})=>{
 const down=shot.direction==='down',color=down?'#4affce':'#77e9ff';
 const left=X(shot.baseIndex),right=X(shot.index),top=Y(shot.high),bottom=Y(shot.low),width=right-left,height=bottom-top;
 const p=ease((elapsed-(shot.final?53:27))/28),drawY=down?top:bottom-height*p,drawH=Math.max(1,height*p),drawW=Math.max(1,width*p),scan=(frame%64)/64;
 const points=[[left,top],[right,top],[left,bottom],[right,bottom]];
 return <g opacity={Math.min(1,overview*1.4)}>
  <rect x={left} y={drawY} width={drawW} height={drawH} fill={color} fillOpacity=".055" stroke={color} strokeOpacity=".45" strokeDasharray="4 6" strokeWidth="1"/>
  {p>.98&&<>
   {Array.from({length:7},(_,i)=><path key={i} d={`M${left+width*i/6} ${top}V${bottom}`} stroke={color} strokeWidth=".6" opacity=".16"/>)}
   {Array.from({length:7},(_,i)=><path key={i} d={`M${left} ${top+height*i/6}H${right}`} stroke={color} strokeWidth=".6" opacity=".16"/>)}
   <rect x={left} y={top+height*scan} width={width} height="3" fill={color} opacity=".35"/>
  </>}
  <path d={`M${left} ${down?top:bottom}L${left+width*p} ${down?top+height*p:bottom-height*p}`} fill="none" stroke={color} strokeWidth="1" strokeDasharray="5 9" opacity=".38"/>
  {p>.8&&points.map(([x,y],i)=>{const dx=i%2?-1:1,dy=i>1?-1:1;return <g key={i}>
   <path d={`M${x+dx*23} ${y}H${x}V${y+dy*23}`} fill="none" stroke={color} strokeWidth="3.6"/>
   <circle cx={x} cy={y} r="5" fill={color}/>
  </g>;})}
  {p>.9&&[[down?left:right,top,shot.high.toFixed(2)],[down?right:left,bottom,shot.low.toFixed(2)]].map(([xx,yy,label],i)=>{const x=+xx,y=+yy;return <g key={i}>
   <circle cx={x} cy={y} r="17" fill="none" stroke={color} strokeWidth="1" opacity=".7"/>
   <path d={`M${x-25} ${y}H${x+25}M${x} ${y-25}V${y+25}`} stroke={color} opacity=".7"/>
   <rect x={x-87} y={i===0?y-61:y+19} width="100" height="34" rx="3" fill="#041317" fillOpacity=".95" stroke={color} strokeWidth=".9"/>
   <text x={x-37} y={i===0?y-37:y+43} textAnchor="middle" fontSize="25" fontFamily="Arial" fill={color}>{label}</text>
  </g>;})}
  {p>.9&&<g><rect x={left+9} y={top+10} width="150" height="29" fill="#031519" fillOpacity=".9"/><text x={left+21} y={top+31} fill={color} fontSize="17" fontFamily="Arial" letterSpacing="2">{down?'DRAWDOWN':'RANGE SCAN'}</text></g>}
 </g>;
};

type BreakEvent={frame:number;index:number;level:number;seed:number;direction:string};
export const ShockGlass:React.FC<{event:BreakEvent;frame:number;X:(v:number)=>number;Y:(v:number)=>number}>=({event:e,frame:f,X,Y})=>{
 const age=f-e.frame,down=e.direction==='down',life=down?72:60,p=cap(age/life),cx=X(e.index),cy=Y(e.level),ice=down?'#9cffe9':'#d0f9ff';
 const paneX=Math.max(20,cx-640),paneW=Math.min(1010,1080-paneX-20);
 return <g>
  {age<13&&<g opacity={Math.max(0,1-age/13)}>
   <rect x={paneX} y={cy-95} width={paneW} height="190" fill="url(#tech-pane)" stroke={ice} strokeOpacity=".75" strokeWidth="2"/>
   <path d={`M${paneX+12} ${cy-83}H${paneX+paneW-12}`} stroke="white" strokeWidth="2.5" opacity=".7"/>
   {Array.from({length:20},(_,i)=>{const a=i*Math.PI*2/20,d=160+rnd(i+e.seed)*280;return <path key={i} d={`M${cx} ${cy}l${Math.cos(a)*d*.3} ${Math.sin(a)*50}l${Math.cos(a+.1)*d*.7} ${Math.sin(a)*55}`} fill="none" stroke={ice} strokeWidth={i%3===0?2.5:1.2}/>;})}
   {down&&<rect x={paneX} y={cy-95} width={paneW} height="190" fill="#00100d" opacity=".28"/>}
  </g>}
  {age>=4&&Array.from({length:down?86:72},(_,i)=>{
   const dt=age-4,side=rnd(e.seed+i*5)-.5,speed=down?11:15,vx=side*speed,vy=down?1+rnd(e.seed+i*5+1)*6:-3-rnd(e.seed+i*5+1)*9;
   const size=9+rnd(e.seed+i*5+2)*(down?37:25),x=cx+side*245+vx*dt,y=cy+(rnd(i+e.seed)-.5)*120+vy*dt+(down?.22:.11)*dt*dt;
   const points=`${-size},${size*.4} ${-size*.6},${-size} ${size*.9},${-size*.25} ${size*.3},${size*.75}`;
   return <g key={i} transform={`translate(${x} ${y}) rotate(${dt*(rnd(i+95)-.5)*13})`} opacity={(1-p)**1.15}>
    <polygon points={points} transform="translate(2 3)" fill={down?'#003d32':'#135b73'} stroke="#021013" strokeWidth="2"/>
    <polygon points={points} fill={i%3===0?'#f2ffff':ice} fillOpacity={i%3===0?.35:.12} stroke={ice} strokeWidth="1.5"/>
    <path d={`M${-size*.6} ${-size}L${size*.9} ${-size*.25}L${size*.3} ${size*.75}`} stroke="white" fill="none" strokeWidth="1.9" opacity=".9"/>
    <path d={`M${-size} ${size*.4}L${size*.9} ${-size*.25}`} stroke="white" opacity=".4" strokeWidth=".7"/>
   </g>;
  })}
  {down&&age<42&&Array.from({length:17},(_,i)=>{const x=cx+(rnd(i+e.seed)-.5)*700,y=cy+age*9;return <path key={i} d={`M${x} ${y}v${30+rnd(i+7)*100}`} stroke="#70ffd9" strokeWidth="1.5" opacity={.30*(1-p)}/>;})}
  <ellipse cx={cx} cy={cy} rx={35+age*7} ry={down?15+age*1.7:35+age*4} fill="none" stroke={ice} opacity={Math.exp(-age/13)} strokeWidth="2.4"/>
  <circle cx={cx} cy={cy} r={age<8?55:24} fill={ice} opacity={Math.exp(-age/6)*.8} filter="url(#cine-bloom)"/>
 </g>;
};

export const ThunderBolt:React.FC<{event:{frame:number;seed:number};frame:number;x:number;y:number}>=({event:e,frame:f,x,y})=>{
 const age=f-e.frame,seed=e.seed+Math.floor(age/2)*19,a=Math.max(Math.exp(-age/9),age>=8&&age<12?.8:0),startY=805;
 const points=Array.from({length:13},(_,i)=>{const p=i/12;return [x+(1-p)*140+(i===12?0:(rnd(seed+i)-.5)*125),startY+(y-startY)*p];});
 const path=points.map((p,i)=>`${i?'L':'M'}${p[0]} ${p[1]}`).join(' ');
 return <g opacity={a}>
  <path d={path} stroke="#38baff" strokeWidth="36" fill="none" filter="url(#cine-glow)"/>
  <path d={path} stroke="#74dfff" strokeWidth="13" fill="none"/><path d={path} stroke="#ecffff" strokeWidth="4.1" fill="none"/>
  {[2,4,6,8,10].map((k,i)=>{const s=i%2?1:-1;return <g key={k}>
   <path d={`M${points[k][0]} ${points[k][1]}l${s*(70+i*10)} 21l${s*24} 48l${s*36} 27`} stroke="#4ccfff" strokeWidth="6" fill="none" opacity=".7"/>
   <path d={`M${points[k][0]} ${points[k][1]}l${s*(70+i*10)} 21l${s*24} 48l${s*36} 27`} stroke="#eaffff" strokeWidth="1.8" fill="none"/>
  </g>;})}
  <ellipse cx={x} cy={y} rx={55+age*6} ry={18+age*1.6} fill="none" stroke="#b7ffee" strokeWidth="3.4"/>
  <ellipse cx={x} cy={y} rx={80+age*6} ry={9+age*.7} fill="none" stroke="#35ffd6" strokeWidth="1.2" opacity=".6"/>
  <circle cx={x} cy={y} r="48" fill="#75ffe0" filter="url(#cine-bloom)"/><circle cx={x} cy={y} r="8" fill="white"/>
  {Array.from({length:18},(_,i)=>{const angle=rnd(e.seed+i)*Math.PI*2,dt=age;return <path key={i} d={`M${x+Math.cos(angle)*dt*7} ${y+Math.sin(angle)*dt*3}l${Math.cos(angle)*15} ${Math.sin(angle)*8}`} stroke="#c5fff0" strokeWidth="2" opacity={Math.exp(-dt/12)}/>;})}
 </g>;
};
