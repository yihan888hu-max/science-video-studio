"""Fork V2's editable renderer, keeping V2 unchanged, then add V3 components."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
text=(ROOT/'src/StockCinematicVideo.tsx').read_text(encoding='utf-8')
text=text.replace("import type referenceFilm", "import {TechRange,ShockGlass,ThunderBolt} from './StockTechEffects';\nimport type referenceFilm")
text=text.replace('StockCinematicVideo','StockTechVideo').replace('pingtan-2025-v2','pingtan-2025-v3')
text=text.replace('f-1766','f-3546').replace('age/38','age/72').replace('f-e.frame<38','f-e.frame<72').replace('f-e.frame<15','f-e.frame<24')
text=text.replace('Math.exp(-(f-e.frame)/7)','Math.exp(-(f-e.frame)/11)').replace('impact*7','impact*12').replace('impact*5','impact*9')
text=text.replace("const previousLevel=[{date:'2025-09-02',index:1,high:3.72},...film.shots]", "const previousLevel=[{date:'2025-09-02',index:1,high:3.72},...film.shots.filter(p=>p.direction==='up')]")
text=text.replace('const lastBreak=glass[glass.length-1];', "const lastBreak=glass.filter(e=>e.index===idx).slice(-1)[0];\n const downShot=shot?.direction==='down';\n const activeDown=glass.filter(e=>e.direction==='down');\n const pressure=Math.max(0,...activeDown.map(e=>Math.exp(-(f-e.frame)/30)));\n const support=film.breaks.filter(e=>e.direction==='down'&&e.frame<=f).slice(-1)[0];")
text=text.replace('<linearGradient id="cine-red">', '<linearGradient id="tech-pane"><stop stopColor="#a1efff" stopOpacity=".03"/><stop offset=".48" stopColor="#e4ffff" stopOpacity=".25"/><stop offset="1" stopColor="#70c8ff" stopOpacity=".04"/></linearGradient>\n    <linearGradient id="cine-red">')
text=text.replace('stopOpacity=".19"','stopOpacity=".10"').replace('stopOpacity=".45"','stopOpacity=".25"').replace('stopOpacity=".65"','stopOpacity=".44"').replace('stopOpacity=".35"','stopOpacity=".18"')
text=text.replace('opacity=".14" filter="url(#cine-glow)"','opacity=".29" filter="url(#cine-glow)"').replace('strokeWidth={bodyWidth+5}','strokeWidth={bodyWidth+10}').replace('fillOpacity=".28"','fillOpacity=".17"')
text=text.replace('opacity=".65"/>','opacity=".82"/>')
needle='      <path d={`M${x+bodyWidth*.2} ${t+1}V${bottom-1}`} '
at=text.index(needle)
text=text[:at]+'      <path d={`M${x+bodyWidth*.52} ${t+2}V${bottom-2}`} stroke={color} strokeWidth={bodyWidth*.24} opacity=".43" filter="url(#cine-glow)"/>\n      <path d={`M${x+bodyWidth*.63} ${t+1}V${bottom-1}`} stroke="#ecffff" strokeWidth={clamp(bodyWidth*.1,.4,2.3)} opacity=".23"/>\n'+text[at:]
start=text.index('    {shot&&state.overview>.35&&(()=>{');end=text.index('    {glass.map(e=>{',start)
text=text[:start]+'    {shot&&state.overview>.35&&<TechRange shot={shot} elapsed={state.shotElapsed} overview={state.overview} frame={f} X={X} Y={Y}/>}\n'+text[end:]
start=text.index('    {glass.map(e=>{');end=text.index('    {lightning.map(e=>{',start)
text=text[:start]+"    {glass.map(e=><ShockGlass key={e.direction+e.frame} event={e} frame={f} X={X} Y={Y}/>)}\n"+text[end:]
start=text.index('    {lightning.map(e=>{');end=text.index('    <circle cx={X(idx)}',start)
text=text[:start]+"    {lightning.map(e=><ThunderBolt key={e.frame} event={e} frame={f} x={X(e.index)} y={Y(data[e.index].low)}/>)}\n"+text[end:]
text=text.replace('    {reached.map((original,i)=>{', '    {support&&<g opacity={state.overview>.35?.18:.6}><path d={`M${Math.max(20,X(support.refIndex))} ${Y(support.level)}H1055`} stroke={DOWN} strokeWidth="2" strokeDasharray="8 10"/>{state.overview<.35&&<text x="1010" y={Y(support.level)+30} textAnchor="end" fill={DOWN} fontSize="24">前低 {support.level.toFixed(2)}</text>}</g>}\n    {reached.map((original,i)=>{')
text=text.replace('  <div style={{position:\'absolute\',left:82,right:82,top:77', '  <AbsoluteFill style={{background:\'radial-gradient(ellipse at 55% 62%,transparent 26%,#000c 78%,#000 100%)\',opacity:pressure*.8,pointerEvents:\'none\'}}/>\n  <div style={{position:\'absolute\',left:82,right:82,top:77')
text=text.replace('<span style={{marginLeft:\'auto\',fontSize:22,color:MUTED}}>前复权 · 日 K</span>','')
text=text.replace("{shot.final?'全区间最高':'阶段高点'} · 低点至高点", "{downShot?'顶部之后 · 阶段新低':(shot.final?'全区间最高':'阶段高点')} · {downShot?'高点至低点':'低点至高点'}")
text=text.replace('fontWeight:900,color:UP,lineHeight:1.2', 'fontWeight:900,color:downShot?DOWN:UP,lineHeight:1.2')
text=text.replace('+{shot.amplitude.toFixed(2)}', "{shot.amplitude>=0?'+':'−'}{Math.abs(shot.amplitude).toFixed(2)}")
text=text.replace('{shot.boards} 个涨停板', "{shot.boards} 个{downShot?'跌停':'涨停'}板")
text=text.replace('{shot.low.toFixed(2)} → {shot.high.toFixed(2)} 元 · 低高振幅，非买卖收益', "{(downShot?shot.high:shot.low).toFixed(2)} → {(downShot?shot.low:shot.high).toFixed(2)} 元 · {downShot?'高点至低点跌幅':'低高振幅'}")
text=text.replace("{lastBreak?(lastBreak.intradayOnly?'盘中突破前高':'突破前高'):market.label||'调整与蓄势'}", "{lastBreak?(lastBreak.direction==='down'?(lastBreak.intradayOnly?'盘中失守前低':'跌破前低'):(lastBreak.intradayOnly?'盘中突破前高':'突破前高')):market.label||'调整与蓄势'}")
text=text.replace("{lastBreak?`越过 ${lastBreak.level.toFixed(2)} 元${lastBreak.intradayOnly?' · 收盘回落，未守住前高':''}`:market.sub}", "{lastBreak?(lastBreak.direction==='down'?`失守 ${lastBreak.level.toFixed(2)} 元 · ${market.isDown?'跌停下挫':'下行压力延续'}`:`越过 ${lastBreak.level.toFixed(2)} 元${lastBreak.intradayOnly?' · 收盘回落，未守住前高':''}`):market.sub}")
text=text.replace('21日恢复交易 · 公司2025-069公告','21日恢复交易')
start=text.index("  <div style={{position:'absolute',left:82,right:82,top:1835")
end=text.index('  {/* Constant master',start);text=text[:start]+text[end:]
(ROOT/'src/StockTechVideo.tsx').write_text(text,encoding='utf-8')
print('Created independent StockTechVideo.tsx')
