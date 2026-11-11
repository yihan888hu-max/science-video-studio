from pathlib import Path
import json,re,shutil
P=Path(__file__).resolve().parent
(P/'compositions').mkdir(exist_ok=True)
import runpy
e=runpy.run_path(str(P/'drawing.py'))
D=e['DEFS'];person=e['person'];text=e['text'];G=e['group']
D=D.replace('</defs>','''<clipPath id="view"><rect x="64" y="128" width="1152" height="423"/></clipPath><filter id="lensblur" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur id="blur-kernel" stdDeviation="0 0"/></filter><linearGradient id="scan"><stop stop-color="#e9ac91" stop-opacity="0"/><stop offset=".8" stop-color="#f6c2a7" stop-opacity=".12"/><stop offset="1" stop-color="#ffcfb0" stop-opacity=".9"/></linearGradient></defs>''')
w=''
for i,(x,y) in enumerate([(130,285),(270,285),(130,405),(270,405)]):w+=person(x,y,id='unknown'+str(i))
w+=G('completed',person(600,285,True,'done0')+person(600,405,True,'done1'))
w+=G('status',G('unknown-label',text(200,355,'经历待问',24,'#a6bdce'))+G('complete-label',text(600,355,'完成打卡',24,'#9cdeeb')))
w+=G('original-scope','<path d="M70 220v-20q0-15 15-15h180M440 185h220q15 0 15 15v20M70 455v25q0 15 15 15h575q15 0 15-15v-25" fill="none" stroke="#7c9eb1" stroke-width="1.5" stroke-opacity=".6"/>'+text(352,194,'最初报名者',26,'#bad0dd'))
cal='<g stroke="#83c4d5" stroke-width="1.2" fill="none"><rect x="425" y="275" width="88" height="145" rx="5"/><path d="M425 302h88M446 267v17M492 267v17"/></g>'
for i in range(5):
 for k in range(3):cal+=f'<circle class="day" cx="{443+26*k}" cy="{320+i*16}" r="2" fill="#8fd9e3"/>'
w+=G('calendar',cal+text(469,404,'30天',15,'#b6dfeb'))
w+=G('quote','<path d="M708 308h117q14 0 14 14v40q0 14-14 14h-86l-19 17v-17h-12q-14 0-14-14v-40q0-14 14-14Z" fill="#101f2d" stroke="#d8a48e" stroke-width="1.2"/>'+text(766,353,'不难',22,'#efbea8','serif'))
for i,y in enumerate([285,405]):
 w+=f'<path id="flow{i}" d="M637 {y}H992" stroke="#9ad9e6" stroke-width="2" fill="none" stroke-dasharray="355"/><path id="flowglow{i}" d="M637 {y}H992" stroke="#8ed8e7" stroke-width="6" opacity=".15" filter="url(#fineglow)" fill="none"/>'
 w+=G('packet'+str(i),f'<circle cx="637" cy="{y}" r="3.5" fill="#d3fcff"/><ellipse cx="626" cy="{y}" rx="18" ry="2" fill="#8fdce8" opacity=".3" filter="url(#fineglow)"/>')
 w+=G('record'+str(i),f'<g transform="translate(1040 {y})" fill="none" stroke="#a2dce7" stroke-width="1.6"><path d="M-40-36h57l22 22v51h-79z" fill="#0c1928"/><path d="M17-36v22h22M-23-9H4M-23 6h44M-23 21H8"/></g>')
w+=G('record-label',text(1040,210,'访谈记录',25,'#b5d4df'))
w+=G('record-frame','<rect id="sample-frame" x="976" y="227" width="130" height="228" rx="9" fill="none" stroke="#e4ad95" stroke-opacity=".7" stroke-width="1.5"/>')
w+=G('gate','<path d="M796 235v-12q0-10 10-10h36q10 0 10 10v12M796 455v12q0 10 10 10h36q10 0 10-10v-12" stroke="#e2a78b" stroke-width="1.4" fill="none"/>'+text(824,191,'只采访完成者',24,'#eab298'))
w+='<rect id="scanner" x="60" y="220" width="92" height="255" fill="url(#scan)"/>'
for i,(x,y) in enumerate([(130,285),(270,285),(130,405),(270,405)]):w+=G('absence'+str(i),f'<circle cx="{x}" cy="{y}" r="42" stroke="#e1ad98" fill="none" stroke-width="1.7" stroke-dasharray="4 8"/>')
w+=G('comparison','<path id="project-top" d="M976 238L692 204M976 447L692 484" stroke="#91b6c9" stroke-opacity=".55" stroke-width="1.4" stroke-dasharray="5 8" fill="none"/>'+text(823,364,'≠',67,'#e7af95','serif'))
form='<path d="M936 239h170v219H936z" stroke="#96bacf" stroke-width="1.5" fill="#0c1725"/>'+text(1021,213,'待补查的记录',23,'#bdd1dc')+text(1021,282,'何时中断打卡？',20,'#c0cfd7')+text(1021,345,'未完成原因？',20,'#c0cfd7')+text(1021,410,'?',30,'#e9af95')
for y in [302,365,431]:form+=f'<path d="M951 {y}h137" stroke="#668397" stroke-width="1.1"/>'
w+=G('follow-form',form)+G('query-routes','<path id="route0" d="M130 245V229Q130 217 145 217H868Q900 217 900 249v46h34M270 445v35q0 16 17 16h575q38 0 38-38v-69h34" stroke="#e4b099" stroke-width="1.5" fill="none" stroke-dasharray="8 8"/>')+G('query-packet','<circle cx="145" cy="217" r="3.5" fill="#efb89a"/><circle cx="145" cy="217" r="10" fill="#efb89a" opacity=".3" filter="url(#fineglow)"/>')
svg=D+'''<rect width="1280" height="720" fill="url(#bg)"/><ellipse id="light" cx="960" cy="345" rx="310" ry="225" fill="url(#bluefog)"/><ellipse id="warmlight" cx="760" cy="345" rx="180" ry="195" fill="url(#warmfog)"/><g clip-path="url(#view)" data-layout-allow-overflow="true"><g id="lens" filter="url(#lensblur)"><g id="camera" data-layout-allow-overflow="true">'''+w+'''</g></g></g><g id="end-question">'''+text(640,410,'谁没有被看见？',58,'#f1f5f5','serif')+'''<path id="end-rule" d="M432 459H848" stroke="#e5af96" stroke-width="2"/><circle cx="432" cy="459" r="4" fill="#eab49a"/></g>'''
for v in sorted(set(re.findall(r'\bid="([^"]+)"',svg)),key=len,reverse=True):svg=svg.replace(f'id="{v}"',f'id="motion-{v}"').replace(f'url(#{v})',f'url(#motion-{v})').replace(f'href="#{v}"',f'href="#motion-{v}"')
copy=[(0,4,'30天打卡，很容易？','只问打卡到最后的人，','就能了解所有人的体验？'),(4,5,'先看，最初有哪些人','完成者只是其中一部分。','其他人的经历，也属于这批人。'),(9,6,'只采访完成者，会漏掉谁？','完成者的经历被听见，','未被采访者，没有进入这份记录。'),(15,5,'幸存者偏差','把留下来的样本，','当成最初的全部。'),(20,5,'把调查范围补回来','从最初名单追踪，','停止打卡 ≠ 停止跑步。'),(25,5,'幸存者偏差','成功经验可以参考。','先检查样本，再判断结论。')]
hud=''
for i,(s,d,h,a,b) in enumerate(copy):hud+=f'<div id="copy-{i}" class="clip copy-track" data-start="{s}" data-duration="{d}" data-track-index="2" data-track-kind="captions"><div id="copy-inner-{i}" class="copy"><h1>{h}</h1><div class="bottom"><p>{a}</p><p>{b}</p></div></div></div>'
js='''const tl=gsap.timeline({paused:true});
tl.set('#motion-camera',{attr:{transform:'matrix(2 0 0 2 -560 -350)'}},0);
tl.set('#motion-status,#motion-original-scope,#motion-gate,#motion-record-label,#motion-record0,#motion-record1,#motion-flow0,#motion-flow1,#motion-flowglow0,#motion-flowglow1,#motion-packet0,#motion-packet1,#motion-record-frame,#motion-comparison,#motion-follow-form,#motion-query-routes,#motion-query-packet,#motion-scanner,#motion-absence0,#motion-absence1,#motion-absence2,#motion-absence3,#motion-end-question',{opacity:0},0);
tl.fromTo('#motion-calendar .day',{opacity:.2},{opacity:1,duration:.18,stagger:.035},.1);
tl.fromTo('#motion-quote',{scale:.85,transformOrigin:'center',opacity:0},{scale:1,opacity:1,duration:.7,ease:'power4.out'},.25);
// Reveal the same original population with a dolly-out, not a dissolve.
tl.to('#motion-camera',{attr:{transform:'matrix(1 0 0 1 0 0)'},duration:1.55,ease:'power3.inOut'},3.25);
tl.to('#motion-calendar',{scale:.65,opacity:0,transformOrigin:'center',duration:.6,ease:'power3.in'},3.35);
tl.to('#motion-quote',{x:250,scale:.6,opacity:0,transformOrigin:'center',duration:.65,ease:'power3.in'},3.65);
tl.to('#motion-original-scope,#motion-status',{opacity:1,duration:.5},4.45);
tl.fromTo('#motion-scanner',{x:0,opacity:0},{x:540,opacity:1,duration:1.35,ease:'power2.inOut'},6.1);
tl.to('#motion-scanner',{opacity:0,duration:.2},7.46);
tl.to('#motion-gate',{opacity:1,duration:.45},7.15);
tl.fromTo('#motion-flow0,#motion-flow1',{strokeDashoffset:355,opacity:0},{strokeDashoffset:0,opacity:1,stagger:.22,duration:.85,ease:'power2.inOut'},7.45);
tl.to('#motion-flowglow0,#motion-flowglow1',{opacity:.12,duration:.4},7.5);
tl.to('#motion-record-label',{opacity:1,duration:.4},8.35);
tl.fromTo('#motion-record0,#motion-record1',{scale:.65,transformOrigin:'center',opacity:0},{scale:1,opacity:1,stagger:.2,duration:.6,ease:'power4.out'},8.3);
tl.to('#motion-original-scope',{opacity:0,duration:.25},8.4);
tl.to('#motion-original-scope',{opacity:1,duration:.35},14.8);
tl.to('#motion-gate',{opacity:0,duration:.25},10.2);
// Track the evidence along its route. Human identities never duplicate.
tl.fromTo('#motion-packet0',{x:0,opacity:0},{x:355,opacity:1,duration:1.2,ease:'power2.inOut'},8.4);
tl.fromTo('#motion-packet1',{x:0,opacity:0},{x:355,opacity:1,duration:1.2,ease:'power2.inOut'},8.65);
tl.to('#motion-camera',{attr:{transform:'matrix(1.35 0 0 1.35 -350 -90)'},duration:1.15,ease:'power3.inOut'},8.45);
tl.to('#motion-camera',{attr:{transform:'matrix(1.75 0 0 1.75 -1110 -260)'},duration:1.05,ease:'power3.inOut'},10.25);
tl.to('#motion-record-frame',{opacity:1,duration:.5},10.65);
tl.to('#motion-complete-label',{opacity:0,duration:.2},12.5);
tl.to('#motion-complete-label',{opacity:1,duration:.3},14.85);
// A return pan points out people excluded from that field of view.
tl.to('#motion-camera',{attr:{transform:'matrix(1.6 0 0 1.6 320 -220)'},duration:1.15,ease:'power3.inOut'},12.55);
tl.to('#motion-blur-kernel',{attr:{stdDeviation:'4 0'},duration:.22,ease:'power2.in'},12.75);
tl.to('#motion-blur-kernel',{attr:{stdDeviation:'0 0'},duration:.35,ease:'power2.out'},13.05);
tl.to('#motion-light',{attr:{cx:380},duration:1.15,ease:'power2.inOut'},12.55);
tl.to('#motion-warmlight',{attr:{cx:560},duration:1.15,ease:'power2.inOut'},12.55);
tl.fromTo('#motion-absence0,#motion-absence1,#motion-absence2,#motion-absence3',{opacity:0,scale:.7,transformOrigin:'center'},{opacity:.7,scale:1,duration:.5,stagger:.08,ease:'power4.out'},13.25);
tl.to('#motion-camera',{attr:{transform:'matrix(1 0 0 1 0 0)'},duration:1.05,ease:'power3.inOut'},14.45);
tl.to('#motion-light',{attr:{cx:920},duration:1},14.45);
tl.to('#motion-absence0,#motion-absence1,#motion-absence2,#motion-absence3',{opacity:0,duration:.4},15.2);
tl.to('#motion-comparison',{opacity:1,duration:.6},15.7);
tl.fromTo('#motion-project-top',{strokeDashoffset:90},{strokeDashoffset:0,duration:1.05},15.7);
tl.to('#motion-sample-frame',{attr:{x:70,y:185,width:605,height:310,rx:14},duration:1.1,ease:'power3.inOut'},16.2);
tl.to('#motion-sample-frame',{opacity:.25,duration:.45},17.1);
tl.to('#motion-flow0,#motion-flow1,#motion-flowglow0,#motion-flowglow1,#motion-packet0,#motion-packet1,#motion-gate',{opacity:.18,duration:.6},16.8);
// Follow-up form grows out of the record. Unknown states stay unknown.
tl.to('#motion-camera',{attr:{transform:'matrix(1.08 0 0 1.08 -10 -25)'},duration:.9,ease:'power3.inOut'},19.35);
tl.to('#motion-comparison,#motion-record0,#motion-record1,#motion-record-label,#motion-record-frame,#motion-gate,#motion-flow0,#motion-flow1,#motion-flowglow0,#motion-flowglow1,#motion-packet0,#motion-packet1',{opacity:0,duration:.4},19.55);
tl.fromTo('#motion-follow-form',{opacity:0,scale:.7,transformOrigin:'center'},{opacity:1,scale:1,duration:.8,ease:'power4.out'},19.75);
tl.to('#motion-query-routes',{opacity:.8,duration:.5},20.35);
tl.fromTo('#motion-route0',{strokeDashoffset:100},{strokeDashoffset:0,duration:2,ease:'none'},20.35);
tl.fromTo('#motion-query-packet',{x:0,opacity:0},{x:700,opacity:1,duration:1.6,ease:'power2.inOut'},20.7);
tl.to('#motion-query-packet',{opacity:0,duration:.3},22.35);
tl.to('#motion-camera',{attr:{transform:'matrix(.72 0 0 .72 180 -30)'},duration:1.45,ease:'power3.inOut'},24.4);
tl.to('#motion-lens',{opacity:.22,duration:1.1},25.25);
tl.to('#motion-end-question',{opacity:1,duration:.7},25.65);
tl.fromTo('#motion-end-rule',{strokeDasharray:416,strokeDashoffset:416},{strokeDashoffset:0,duration:.8,ease:'power4.out'},25.85);
'''
for i,(s,d,h,a,b) in enumerate(copy):
 if i>0:js+=f"tl.fromTo('#copy-inner-{i}',{{opacity:0}},{{opacity:1,duration:.3,ease:'power2.out'}},{s});\n"
js+="window.__timelines=window.__timelines||{};window.__timelines.journey=tl;"
css='''@font-face{font-family:VideoSans;src:url('assets/fonts/msyh.ttc')}@font-face{font-family:VideoSong;src:url('assets/fonts/simsun.ttc')}#root{position:absolute;inset:0;overflow:hidden}.sans{font-family:VideoSans,sans-serif}.serif{font-family:VideoSong,serif}svg{position:absolute;inset:0}.copy-track{position:absolute;inset:0;pointer-events:none;z-index:5}.copy h1{position:absolute;top:62px;left:80px;width:1120px;margin:0;color:#f0f4f6;text-align:center;font:700 37px/1.3 VideoSong,serif;letter-spacing:1px}.bottom{position:absolute;top:570px;left:100px;width:1080px;text-align:center;color:#eaf2f5;font:33px/1.45 VideoSong,serif}.bottom p{margin:0}.note{position:absolute;right:64px;bottom:25px;color:#92aabd;font:20px VideoSans,sans-serif;z-index:8}'''
(P/'compositions/journey.html').write_text(f'<template><style>{css}</style><div id="root" data-composition-id="journey" data-width="1280" data-height="720"><svg id="world" class="clip" data-start="0" data-duration="30" data-track-index="1" viewBox="0 0 1280 720" width="1280" height="720">{svg}</svg>{hud}<div class="note">教学示意，非调查数据</div></div><script>{js}</script></template>',encoding='utf-8')
audio='<audio id="music-bed" class="clip" src="assets/audio/We Never vibebgm.mp3" data-timeline-role="music" data-start="0" data-duration="30" data-media-start="24.07" data-volume="0.4" data-fade-in="0.5" data-fade-out="1.6" data-track-index="3"></audio>'
for i,(name,t,v) in enumerate([('pop',.35,.12),('whoosh-short',3.55,.16),('whoosh-short',6.25,.08),('pop',8.45,.17),('whoosh-short',10.5,.13),('whoosh-short',12.8,.16),('whoosh-short',14.7,.13),('pop',16.6,.14),('whoosh-short',19.6,.12),('pop',21.9,.14),('whoosh-short',24.75,.12)]):audio+=f'<audio id="fx-{i}" class="clip" src="assets/audio/{name}.mp3" data-start="{t}" data-duration="{.57 if name.startswith("whoosh") else .72}" data-volume="{v}" data-track-index="{4+i%2}"></audio>'
(P/'index.html').write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>幸存者偏差 · 运镜修订版</title><script src="assets/js/gsap.min.js"></script><style>body{{margin:0;background:#040812}}#root{{position:relative;width:1280px;height:720px;overflow:hidden}}.clip{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="30" data-width="1280" data-height="720" data-fps="30"><div id="journey" class="clip" data-composition-id="journey" data-composition-src="compositions/journey.html" data-start="0" data-duration="30" data-width="1280" data-height="720" data-track-index="1" data-track-kind="graphics"></div>{audio}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}});</script></body></html>',encoding='utf-8')
(P/'meta.json').write_text(json.dumps({'id':'survivorship-bias-30s-motion-v3','name':'幸存者偏差 · 运镜修订版'},ensure_ascii=False),encoding='utf-8')
print('Built continuous camera composition')
