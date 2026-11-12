"""Local RMS-onset grid estimate. Measures rhythm; does not claim listening."""
import array,json,math,sys,wave
from pathlib import Path
path=Path(sys.argv[1]);out=Path(sys.argv[2])
with wave.open(str(path),'rb') as w:
 sr=w.getframerate();ch=w.getnchannels();assert w.getsampwidth()==2
 samples=array.array('h',w.readframes(w.getnframes()))
step=.01;hop=round(sr*step);energy=[]
for i in range(0,len(samples)//ch-hop,hop):
 values=samples[i*ch:(i+hop)*ch:ch];energy.append(math.sqrt(sum(v*v for v in values)/len(values))/32768)
flux=[max(0,energy[i]-energy[max(0,i-2)]) for i in range(len(energy))]
scores=[]
for lag in range(30,101):
 score=sum(flux[i]*flux[i-lag] for i in range(lag,len(flux)))/max(1,len(flux)-lag)
 scores.append((score,lag))
score,lag=max(scores);period=lag*step
phase=max(range(lag),key=lambda p:sum(flux[i] for i in range(p,len(flux),lag)))
beats=[round((phase+k*lag)*step,3) for k in range(len(flux)//lag) if (phase+k*lag)<len(flux)]
value={'method':'positive RMS onset autocorrelation; estimated grid, no subjective listening','bpm':60/period,'period':period,'phase':phase*step,'beats':beats,'duration':len(samples)/ch/sr,'windowRms':[round(sum(energy[s*100:(s+30)*100])/3000,5) for s in range(0,151,10)]}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8');print({k:v for k,v in value.items() if k!='beats'})
