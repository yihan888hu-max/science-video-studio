"""Select real CC0 skill-library audio and a runtime-only recorded glass crash."""
import hashlib,json,shutil,urllib.request,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1]
P=ROOT/'projects/pingtan-2025-v3/research';DEST=ROOT/'local-media/pingtan-v3-sfx';DEST.mkdir(parents=True,exist_ok=True);P.mkdir(parents=True,exist_ok=True)
SKILL=REPO/'.agents/skills/sound-effects'
library=[('charge', 'sfx/riser/kenney-digital-powerup1.ogg'),('charge-alt','sfx/riser/kenney-digital-powerup3.ogg'),('surge','sfx/riser/kenney-digital-phaserup1.ogg'),('heavy','sfx/impact/fs-177242-cinematic-impact.ogg'),('sub','sfx/impact/kenney-sci-lowfrequency-explosion-000.ogg'),('hit','sfx/impact/kenney-impact-impactpunch-heavy-000.ogg')]
manifest_path=SKILL/'sfx/manifest.json'
if not manifest_path.exists():manifest_path=P/'skill-manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'));(P/'skill-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
ledger=[]
for name,path in library:
 file=SKILL/path;target=DEST/(name+'.ogg')
 if file.exists():shutil.copy2(file,target)
 elif not target.exists():
  request=urllib.request.Request('https://raw.githubusercontent.com/barty-bart/motion-graphics/main/skills/sound-effects/'+path,headers={'User-Agent':'Mozilla/5.0'})
  target.write_bytes(urllib.request.urlopen(request,timeout=35).read())
 ledger.append(dict(name=name,file=target.relative_to(ROOT).as_posix(),license='CC0 1.0 (skill source manifest)',source='https://github.com/barty-bart/motion-graphics/blob/main/skills/sound-effects/'+path,sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
def get(url):return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
# Exact asset URLs were checked during research; restoring a cache does not
# depend on parsing changing catalog pages or printing their HTML.
(P/'sfx-sources.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
for name,title,url in [('glass','Glass break with hammer thud','https://assets.mixkit.co/active_storage/sfx/759/759-preview.mp3'),('plasma','Sci fi plasma gun power up','https://assets.mixkit.co/active_storage/sfx/1679/1679-preview.mp3'),('thunder','Cinematic laser gun thunder','https://assets.mixkit.co/active_storage/sfx/1287/1287-preview.mp3')]:
 target=DEST/(name+'.mp3')
 if not target.exists():target.write_bytes(get(url))
 ledger.append(dict(name=name,title=title,file=target.relative_to(ROOT).as_posix(),license='Mixkit Sound Effects Free License, synchronized video only; raw file not redistributed',source=url,page='https://mixkit.co/free-sound-effects/'+('glass/' if name=='glass' else 'sci-fi/'),licenseUrl='https://mixkit.co/license/#sfxFree',sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
for entry in ledger:
 source=ROOT/entry['file'];output=source.with_suffix('.wav')
 if not output.exists():
  helper=Path.home()/'.codex/skills/ffmpeg-skill/scripts/audio.py'
  if helper.exists():subprocess.run([sys.executable,str(helper),str(source),'-o',str(output),'--stereo','--json-brief'],check=True)
  else:subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-i',str(source),'-ac','2','-c:a','pcm_s16le',str(output)],check=True)
(P/'sfx-sources.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
