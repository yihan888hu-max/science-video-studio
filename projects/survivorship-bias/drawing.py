from pathlib import Path
DEFS=(Path(__file__).parent/'assets/vector-definitions.svg').read_text(encoding='utf-8')
def text(x,y,s,size=25,color='#a9c0cc',cls='sans',anchor='middle',extra=''):
 return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}" {extra}>{s}</text>'
def group(id,html):return f'<g id="{id}">{html}</g>'
def person(x,y,active=False,id=''):
 a=f'<g id="{id}">' if id else '<g>'
 if active:a+=f'<circle cx="{x}" cy="{y}" r="32" fill="#6bc9df" opacity=".2" filter="url(#glow)"/><circle cx="{x}" cy="{y}" r="33" fill="#0c202e" stroke="#8cd8e9" stroke-opacity=".48" stroke-width="1.3"/><use href="#person" x="{x}" y="{y}" stroke="#b1eaf0" stroke-width="2.1"/><circle cx="{x+27}" cy="{y+24}" r="10" fill="#182d3a" stroke="#8bd5df" stroke-width="1.2"/><use href="#check" x="{x+27}" y="{y+24}" stroke="#b8eef0" stroke-width="1.6"/>'
 else:a+=f'<circle cx="{x}" cy="{y}" r="33" fill="none" stroke="#657e94" stroke-opacity=".65" stroke-dasharray="3 5"/><use href="#person" x="{x}" y="{y}" stroke="#92aabd" stroke-width="1.8"/>'+text(x+28,y+27,'?',20,'#91a8bb')
 return a+'</g>'
def population():
 return group('known',person(520,283,True,'known1')+person(520,413,True,'known2'))+group('unknown',person(235,283,id='unknown1')+person(375,283,id='unknown2')+person(235,413,id='unknown3')+person(375,413,id='unknown4'))
def boundary(label='最初报名者'):
 return group('boundary','<path id="boundary-line" d="M155 212v-14q0-19 19-19h118M437 179h147q19 0 19 19v14M155 446v18q0 19 19 19h410q19 0 19-19v-18" fill="none" stroke="#6b91a3" stroke-opacity=".5" stroke-width="1.3"/>'+text(365,188,label))
def records():
 a=text(1000,215,'访谈记录')
 for j,y in enumerate([283,413]):a+=group('record'+str(j),f'<g transform="translate(1000 {y})" stroke="#8cd7e6" stroke-width="1.6"><rect x="-45" y="-40" width="90" height="81" fill="url(#record)" stroke="none"/><use href="#doc"/></g>')
 return group('records',a)
def connectors():
 a=''
 for j,y in enumerate([283,413]):
  a+=f'<path id="wire{j}" d="M553 {y}H950" fill="none" stroke="#92c4d3" stroke-opacity=".62" stroke-width="1.8" stroke-dasharray="397"/>'
  a+=f'<circle id="packet{j}" cx="553" cy="{y}" r="3.5" fill="#b9f2f6"/><circle id="packetglow{j}" cx="553" cy="{y}" r="11" fill="#a9eaf2" opacity=".3" filter="url(#fineglow)"/>'
 return group('wires',a)
def gate():
 a='<path id="gate-line" d="M715 231V208q0-12 12-12h60q12 0 12 12v23M715 466v15q0 12 12 12h60q12 0 12-12v-15" fill="none" stroke="#d99d87" stroke-opacity=".65" stroke-width="1.5"/>'+text(756,171,'只采访完成者',25,'#e6ad98')
 for y in [283,413]:a+=f'<circle cx="756" cy="{y}" r="12" stroke="#e0a38d" stroke-width="1.3" fill="#0d1725"/><use href="#check" x="756" y="{y}" stroke="#efc1ac" stroke-width="1.7"/>'
 return group('gate',a)
def cap(a,b):return group('caption',text(640,600,a,33,'#edf3f5','serif caption')+text(640,648,b,33,'#edf3f5','serif caption'))
def head(s):return text(640,100,s,37,'#f2f4f5','serif heading',extra='id="title" data-var-text="headline"')
def bg():return '<rect width="1280" height="720" fill="url(#bg)"/><ellipse cx="960" cy="345" rx="320" ry="240" fill="url(#bluefog)"/><ellipse cx="748" cy="337" rx="145" ry="180" fill="url(#warmfog)"/>'
def commonlabels():return group('status',text(305,350,'未被采访',23,'#b2c2ce')+text(520,350,'完成打卡',23,'#9cdeeb'))
