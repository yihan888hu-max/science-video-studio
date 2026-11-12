"""Package editable V3 source, while omitting standalone licensed SFX caches."""
import argparse
import hashlib
import json
import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[1]
P = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('output', type=Path)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
video = ROOT/'out/pingtan-development-120s-v3.mp4'
assert video.is_file()

deliverables = [
    (video, '平潭发展-120秒-V3.mp4'),
    (P/'QA.md', '质量检查.md'),
    (P/'SOUND.md', '声音试听位置.md'),
    (ROOT/'out/pingtan-v3-final-contact.jpg', '关键帧.jpg'),
    (ROOT/'out/pingtan-v3-audio-review.png', '声音落点波形.png'),
]
for source, target in deliverables:
    shutil.copy2(source, args.output/target)

def allowed(file):
    if file.suffix == '.log' or file.name == 'mix-raw.wav':
        return False
    if file.suffix == '.wav' and 'local-media' in file.parts:
        return False
    if 'pingtan-v3-sfx' in file.parts and file.suffix not in ('.ogg', '.json', '.md'):
        return False
    if 'public' in file.parts and 'pingtan-2025-v3' in file.parts and file.suffix == '.wav':
        return False
    if file.name.startswith('mixkit-') and file.suffix == '.html':
        return False
    return True

files = []
for folder in [ROOT, REPO/'.agents/skills/stock-video', REPO/'docs/stock-video']:
    for current, dirs, names in os.walk(folder, followlinks=False):
        dirs[:] = [d for d in dirs if d not in ('node_modules', 'out', '.git', '.cache', '.remotion', '__pycache__')]
        files.extend(Path(current)/name for name in names if allowed(Path(current)/name))

manifest = []
archive = args.output/'平潭发展-120秒-可编辑源工程-V3.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for file in sorted(set(files)):
        relative = file.relative_to(REPO).as_posix()
        z.write(file, relative)
        manifest.append(dict(path=relative, sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
    z.writestr('README.md', '''# 平潭发展120秒 V3 · 可编辑工程

进入 projects/stock-video，安装锁定的 Node 依赖，并准备 Python / FFmpeg。当前本机可直接使用现有环境。

```sh
npm ci
npm run prepare:pingtan
python scripts/stock_video/prepare_pingtan_v3_sfx.py
npm run rebuild:pingtan-v3
npm run check:pingtan-v3
npm run dev
npm run render:pingtan-v3
```

预览选择 Pingtan120V3。源代码入口是 src/StockTechVideo.tsx 和 src/StockTechEffects.tsx；时间轴由 scripts/stock_video/build_pingtan_v3.py 生成。V1、V2保留。

制作说明、研究、质量检查和音效来源位于 projects/stock-video/projects/pingtan-2025-v3。
用户原曲MP3及已选CC0 OGG随本地源包提供；解码WAV、Mixkit原素材、V3合成音轨、依赖、浏览器缓存与最终MP4未收入ZIP。首次准备素材需要联网免费获取，之后本地重建与渲染。具体来源和许可在CREDITS.md及research/sfx-sources.json，准备脚本可恢复所需缓存。原曲使用权由用户提供。

音乐原选段动态保持，仅总输出固定0.7倍；不做动态闪避、变速、变调、淡入淡出和归一化。本次未上传GitHub。
''')
    z.writestr('DELIVERY-MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))

receipt = dict(videoSha256=hashlib.sha256(video.read_bytes()).hexdigest(),
               videoBytes=video.stat().st_size, sourceFiles=len(manifest),
               videoFrames=3600, baseCommit='53fc41b0434bc9d00790a7c7c22a6d403ca29d8f',
               sourceZipSha256=hashlib.sha256(archive.read_bytes()).hexdigest())
(args.output/'交付清单.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=False))
