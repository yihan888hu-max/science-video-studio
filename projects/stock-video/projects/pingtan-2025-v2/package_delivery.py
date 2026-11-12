"""Package local V2 media, editable source and source checksums."""
import argparse,hashlib,json,os,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];P=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('output',type=Path);a=parser.parse_args();a.output.mkdir(parents=True,exist_ok=True)
video=ROOT/'out/pingtan-development-60s-v2.mp4';assert video.is_file()
for source,target in [(video,'平潭发展-60秒-V2.mp4'),(P/'QA.md','质量检查.md'),(ROOT/'out/pingtan-v2-final-contact.jpg','关键帧.jpg')]:shutil.copy2(source,a.output/target)
items=[]
with zipfile.ZipFile(a.output/'平潭发展-60秒-可编辑源工程-V2.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 files=[]
 for folder in [ROOT,REPO/'.agents/skills/stock-video',REPO/'docs/stock-video']:
  for current,dirs,names in os.walk(folder,followlinks=False):
   dirs[:]=[d for d in dirs if d not in ('node_modules','out','.git','.cache','.remotion','__pycache__')]
   for name in names:
    file=Path(current)/name
    if file.suffix=='.log' or name=='mix-raw.wav' or (file.suffix=='.wav' and 'local-media' in file.parts):continue
    files.append(file)
 for file in sorted(set(files)):
  relative=file.relative_to(REPO).as_posix();z.write(file,relative);items.append(dict(path=relative,sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
 z.writestr('README.md','# 平潭发展60秒 V2 · 可编辑工程\n\n进入projects/stock-video，准备Node/Python/FFmpeg和锁定依赖；已有本地环境可复用。预览npm run dev，选择Pingtan60V2。重建依次npm run prepare:pingtan、npm run rebuild:pingtan-v2、npm run check:pingtan-v2、npm run render:pingtan-v2。\n\n制作规范、音乐保持方式、资料摘要与质量检查位于projects/stock-video/projects/pingtan-2025-v2。原曲MP3随本地工程提供，解码WAV由prepare命令恢复；已生成音轨位于public/pingtan-2025-v2。V1保留。依赖、浏览器缓存和最终MP4未打入源码ZIP，MP4单独交付。本次未上传GitHub。\n')
 z.writestr('DELIVERY-MANIFEST.json',json.dumps(items,ensure_ascii=False,indent=2))
receipt=dict(videoSha256=hashlib.sha256(video.read_bytes()).hexdigest(),videoBytes=video.stat().st_size,sourceFiles=len(items),videoFrames=1800,baseCommit='53fc41b0434bc9d00790a7c7c22a6d403ca29d8f')
(a.output/'交付清单.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');print(receipt)
