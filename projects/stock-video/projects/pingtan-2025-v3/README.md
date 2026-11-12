# 平潭发展120秒V3

独立Composition：`Pingtan120V3`，1080×1920、30fps、3600帧。沿用2025-09-01—2026-11-11的285条完整日线，V1与V2保留。

在`projects/stock-video`运行：

```sh
npm run dev
npm run rebuild:pingtan-v3
npm run check:pingtan-v3
npm run render:pingtan-v3
```

输出`out/pingtan-development-120s-v3.mp4`。首次安装按工程README准备依赖；当前机器直接复用已有Node/Remotion/Python/FFmpeg。

## 编辑入口

- `src/StockTechVideo.tsx`：透亮K线、红绿辉光、正文、相机、科技统计框及去除两处文字后的画面。
- `src/StockTechEffects.tsx`：TechRange扫描框、ShockGlass双向玻璃、ThunderBolt粗主干/分支/命中环。
- `scripts/stock_video/build_pingtan_v3.py`：3600帧时间轴、5个上行高点/4个下行新低、首次上下破位、涨跌停统计和真实素材音效编排。
- `src/stock-videos/pingtan-2025-v3.json`：生成后的全部数据，可直接预览；算法输入变化后重建。
- `brief.json`、`timeline.csv`：事件及精确起止帧；`research/audit.py`：独立检查。
- `research/summary.md`、`CREDITS.md`：历史口径和音效来源。

`create_pingtan_v3_renderer.py`是本次初建副本的工具，不需在日常重建时运行；直接编辑当前V3渲染器即可，避免覆盖自定义修改。

## 音频恢复

本机原音乐在`local-media/pingtan/qingming.mp3`；公开仓库不附原曲、音效原文件及独立混音。新设备先将用户原曲放到该路径，按`../../local-media.example.json`核对原曲SHA256，然后运行：

```sh
npm run prepare:pingtan
python scripts/stock_video/prepare_pingtan_v3_sfx.py
npm run rebuild:pingtan-v3
npm run check:pingtan-v3
npm run dev
npm run render:pingtan-v3
```

Mac可将`python`替换成`python3`；所有命令在`projects/stock-video`中执行。原曲解码需要FFmpeg在PATH。音效准备脚本免费恢复CC0与Mixkit缓存，不需要安装完整sound-effects技能。首次获取需要网络，之后渲染完全读取本地文件；无付费服务。预览选择`Pingtan120V3`。Mixkit独立原文件继续保持本地，来源见CREDITS.md。

配乐的连续120秒PCM保持与原曲选段一致，不变速、不变调、不随落点压低、不淡入淡出、不做响度归一化。最终音乐与音效统一固定0.7倍总输出。音效以实际录制/预制素材为核心，不再用正弦叮声。

## 下跌统计

2025-12-30最高16.86之后，1月19日、1月22日、6月29日、7月21日分别展示阶段最低11.29、9.46、6.38、4.95；最后为−70.64%，133个交易日含首尾、4个收盘跌停。低点使用日内最低，不是假称该日收盘价；标题说明“顶部之后的盘中阶段新低”。框选上行和下行的涨跌幅公式分别写在研究摘要中。

质检范围、声音测量与建议试听位置见QA.md及SOUND.md。QA中的“仅本地交付”是制作结束时的原始快照；后续按用户授权归档和更新仓库，见[版本发布记录](../../../../docs/stock-video/PINGTAN_RELEASE_2026-11-12.md)。
