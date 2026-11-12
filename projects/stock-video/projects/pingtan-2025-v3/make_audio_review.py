"""Plot five exported-MP4 waveform windows after local audio extraction."""
import array,math,wave
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
file=ROOT/'out/pingtan-v3-final-audio.wav'
with wave.open(str(file),'rb') as w:sr=w.getframerate();ch=w.getnchannels();data=array.array('h',w.readframes(w.getnframes()))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
checks=[(3.9667,'Charge to limit-up'),(21.7333,'Glass breakout'),(25.0333,'Lightning / resumed session'),(79.3,'Three lower limits / breakdown'),(109.3333,'Late down-leg / new low')]
canvas=Image.new('RGB',(1200,1050),'#081317');draw=ImageDraw.Draw(canvas)
for row,(at,title) in enumerate(checks):
 top=row*210;draw.text((24,top+15),title+' | '+str(round(at,3))+' s',font=font,fill='#d5efed')
 start=max(0,at-.95);end=at+.85;left=70;right=1160;middle=top+119
 draw.line((left,middle,right,middle),fill='#294b4a')
 for x in range(left,right):
  a=round((start+(x-left)/(right-left)*(end-start))*sr);b=max(a+1,round((start+(x+1-left)/(right-left)*(end-start))*sr));values=data[a*ch:min(b*ch,len(data))]
  rms=math.sqrt(sum(v*v for v in values)/max(1,len(values)))/32768;height=rms*120
  draw.line((x,middle-height,x,middle+height),fill='#38c6ca')
 xx=left+(at-start)/(end-start)*(right-left);draw.line((xx,top+49,xx,top+184),fill='#ff697d',width=2)
 draw.text((left,top+184),str(round(start,3))+' s',font=small,fill='#839da2');draw.text((right-70,top+184),str(round(end,3))+' s',font=small,fill='#839da2')
canvas.save(ROOT/'out/pingtan-v3-audio-review.png')
print('Saved waveform proof for five headphone review points')
