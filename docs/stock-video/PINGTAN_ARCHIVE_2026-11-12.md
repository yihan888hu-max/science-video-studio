# 平潭发展V1/V2保留记录

用户在120秒V3交付后要求：“将项目更新到对应仓库中。保持记录，仓库中上一版也保留”。仓库为`yihan888hu-max/science-video-studio`。

此次首先归档已在本机制作的30秒V1及60秒V2，单独提交并建立`pingtan-v2-60s`标签。该快照保留两版完整源码、生成数据、行情原始快照、研究摘要、逐帧时间轴、导演说明及当时的质量检查。根入口注册`Pingtan2025`和`Pingtan60V2`，命令保留`rebuild/check/render:pingtan`及`rebuild/check/render:pingtan-v2`；此前所有Composition继续注册。

固定成片和关键帧：

- `previews/stock-video/pingtan-development-30s-v1.mp4`与`pingtan-v1-contact.jpg`
- `previews/stock-video/pingtan-development-60s-v2.mp4`与`pingtan-v2-contact.jpg`

V1为900帧，覆盖2025-01-02至2026-11-11；V2为1800帧，从2025年9月开始，加入5次高点框选、玻璃突破、8次闪电及顶部长镜头。两版1080×1920、30fps；音效为代码合成，V1曾有音乐闪避，V2按用户要求改为连续原曲、固定0.7倍总输出。历史差异原样记录，不能将V3的真实音效设计追记到旧版。

先前QA内的“本次未提交GitHub”描述的是制作阶段。此次仓库归档另立本记录，不改写原QA的验收范围或人工试听状态。版本成片的SHA256见`previews/stock-video/pingtan-release-manifest.json`，归档后的Git提交和标签是恢复旧版的依据。

原曲MP3、解码WAV、独立分轨/混音、参考视频和依赖不公开；重新渲染先按`projects/stock-video/local-media.example.json`恢复用户自己的音乐，再运行素材准备与重建。原来的航天发展、浙江世宝和幸存者偏差项目继续保留。
