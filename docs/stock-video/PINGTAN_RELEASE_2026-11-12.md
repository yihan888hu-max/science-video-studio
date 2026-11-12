# 平潭发展120秒V3 · 仓库更新记录

2026-11-12，用户明确授权将项目更新至`yihan888hu-max/science-video-studio`，并保留仓库上一版。仓库保持公开属性，普通快进更新，不重写历史。

## 版本保留

| 版本 | Composition / 标签 | 固定成片 | 主要区别 |
|---|---|---|---|
| 30秒V1 | `Pingtan2025`，随V2快照归档 | [MP4](../../previews/stock-video/pingtan-development-30s-v1.mp4) | 2025年至今回看，代码电子音效 |
| 60秒V2 | `Pingtan60V2` / `pingtan-v2-60s` | [MP4](../../previews/stock-video/pingtan-development-60s-v2.mp4) | 从9月开始，五次高点框选、突破、闪电、顶部详情 |
| 120秒V3 | `Pingtan120V3` / `pingtan-v3-120s` | [MP4](../../previews/stock-video/pingtan-development-120s-v3.mp4) | 双向玻璃、连续下破、科技扫描框、红绿透亮K线、真实充能与重击 |

先建立V1/V2独立归档提交，再在其之上添加V3。`archive-pre-pingtan-20261112`标签保留本次更新前的`53fc41b0434bc9d00790a7c7c22a6d403ca29d8f`，包含原有股票与科普工程。所有历史Composition和旧版源码继续留在最新分支中，不只依赖标签才能查看。

V1/V2归档提交为[`ab2a5ee4f12362c970c0296f905b27499d124ccc`](https://github.com/yihan888hu-max/science-video-studio/commit/ab2a5ee4f12362c970c0296f905b27499d124ccc)。从其暂存树导出独立源码目录，TypeScript编译通过，188个文件的包级完整性验证通过；归档入口没有注册V3，能够独立保留上一版工程结构。

在独立目录恢复旧版，可在GitHub选择`pingtan-v2-60s`下载源码，或从该标签新建自己的分支；已有工作目录包含改动时先保存，不必覆盖现有目录。

## V3上传内容

- `StockTechVideo.tsx`与`StockTechEffects.tsx`：发光透明蜡烛、科技框选、上扬/下坠玻璃、粗主干及分叉闪电、命中环、压迫暗角与镜头震动。
- `build_pingtan_v3.py`、生成JSON和timeline.csv：3600帧、5次上行/4次下行统计停留、31个下行破位、18个闪电节点；最高点11.6秒全局后拉近。
- 研究、导演稿、来源清单、原曲采样一致性证明、独立核验脚本、最终MP4技术检查与16张关键帧。
- 声音使用真实免费素材；sound-effects技能的方法与来源在CREDITS中署名，技能安装目录本身不上传。准备脚本可免费恢复音效缓存。
- 原曲连续使用20.03—140.03秒，不动态压低、变速、变调、淡入淡出或归一化；最终固定0.7倍总输出。原曲及独立音轨不公开。

数据截止2026-11-11，未引入盘中未完成日线。16.86至4.95为顶部之后的盘中阶段低点跌幅−70.64%，133个交易日含首尾、4个收盘跌停。动画并非逐笔回放，情绪文案属于演绎。详见[研究摘要](../../projects/stock-video/projects/pingtan-2025-v3/research/summary.md)。

## 检查与范围

原片交付前已完成整片渲染、最终MP4抽帧和电平测量；V3为120.000秒、1080×1920、恒定30fps、H.264/AAC、BT.709，−10.9LUFS、−2.2dBTP。10项PASS、1项WARN、0项FAIL；WARN为无独立字幕轨，文字已入画。没有把信号检测写成人工试听。[原始QA](../../projects/stock-video/projects/pingtan-2025-v3/QA.md)保留制作时的本地交付状态；本记录描述后续仓库更新。

仓库更新另检查TypeScript、三版数据断言、素材恢复脚本、旧版注册、发布成片哈希、Git历史、敏感路径与凭据排除，以及FILE_MANIFEST逐文件完整性。`validation-report.json`记录包级检查，不等于重新人工看完整片。

发布记录中的机器路径仅将工具安装目录替换为`ffmpeg`等可移植名称；未修改技术检测的数值、PASS/WARN状态、时刻或影片哈希。原本机检查和源ZIP仍保留在用户设备。`.gitattributes`统一Git文本LF；验证脚本兼容旧Windows工作目录的CRLF，二进制哈希逐字节校验。

根FILE_MANIFEST按实际暂存内容生成，排除自身及自引用的validation-report；固定成片、帧图和波形图校验值见`previews/stock-video/pingtan-release-manifest.json`。依赖、字体、浏览器缓存、日志、原曲、完整第三方网页、原音效及私人工作笔记不上传。此次未增装npm依赖，也未使用付费服务。
