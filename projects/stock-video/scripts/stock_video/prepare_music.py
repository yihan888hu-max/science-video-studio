"""Decode a user-provided local music file; preserve the original."""
import argparse,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=ROOT/'local-media/pingtan/qingming.mp3');p.add_argument('--output',type=Path,default=ROOT/'local-media/pingtan/qingming.wav');p.add_argument('--overwrite',action='store_true');a=p.parse_args()
assert a.source.is_file(),'Restore the supplied music to local-media/pingtan/qingming.mp3 first'
if a.output.exists() and not a.overwrite:
 print('Using existing decoded music:',a.output)
else:
 a.output.parent.mkdir(parents=True,exist_ok=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y' if a.overwrite else '-n','-i',str(a.source),'-ac','2','-c:a','pcm_s16le',str(a.output)],check=True)
 print('Decoded:',a.output)
