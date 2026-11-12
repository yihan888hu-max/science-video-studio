"""Package this local delivery, excluding dependencies, caches and decoded music."""
import argparse,hashlib,json,os,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];PROJECT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('output',type=Path);a=parser.parse_args();a.output.mkdir(parents=True,exist_ok=True)
video=ROOT/'out/pingtan-development-2025-now-v1-final.mp4';assert video.is_file()
shutil.copy2(video,a.output/'平潭发展-2025至今-30秒-V1.mp4')
shutil.copy2(PROJECT/'QA.md',a.output/'质量检查.md')
shutil.copy2(ROOT/'out/pingtan-final-contact-sheet.jpg',a.output/'关键帧.jpg')
manifest=[]
with zipfile.ZipFile(a.output/'平潭发展-可编辑源工程-V1.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 paths=[]
 for folder in [ROOT,REPO/'.agents/skills/stock-video',REPO/'docs/stock-video']:
  for current,dirs,files in os.walk(folder,followlinks=False):
   dirs[:]=[d for d in dirs if d not in ('node_modules','out','.git','.cache','.remotion','__pycache__')]
   for filename in files:
    file=Path(current)/filename
    if file.suffix=='.log' or filename=='mix-raw.wav' or (file.suffix=='.wav' and 'local-media' in file.parts):continue
    paths.append(file)
 for file in sorted(set(paths)):
  relative=file.relative_to(REPO).as_posix();z.write(file,relative);manifest.append({'path':relative,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
 z.writestr('README.md','# 平潭发展30秒 · 可编辑源工程\n\n基线53fc41b，新增平潭发展项目、资料和用户配乐。\n\n进入projects/stock-video：首次npm ci，然后npm run dev选择Pingtan2025。完整重建：npm run prepare:pingtan、npm run rebuild:pingtan、npm run check:pingtan、npm run render:pingtan。需要Node、Python 3、FFmpeg和Remotion浏览器；当前机器已装环境可直接复用。\n\n用户提供的原音乐位于local-media/pingtan/qingming.mp3，仅随本地交付包提供；解码WAV可由prepare命令恢复。已生成混音在public/pingtan-2025-v1。研究与质量检查见projects/stock-video/projects/pingtan-2025。\n\n依赖、浏览器缓存和最终MP4不包含在源码压缩包中；MP4单独交付。此次没有提交GitHub。\n')
 z.writestr('DELIVERY-MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
receipt={'video':{'name':'平潭发展-2025至今-30秒-V1.mp4','sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'bytes':video.stat().st_size},'sourceFiles':len(manifest),'baseCommit':'53fc41b0434bc9d00790a7c7c22a6d403ca29d8f'}
(a.output/'交付清单.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
