# 平潭发展60秒V2

1080×1920，30fps，1800帧。2025-09-01—2026-11-11共285条完整日线。V1源码与成片保留，V2是独立Composition `Pingtan60V2`。

## 运行与编辑

在`projects/stock-video`目录：

```sh
npm run dev
npm run rebuild:pingtan-v2
npm run check:pingtan-v2
npm run render:pingtan-v2
```

输出：`out/pingtan-development-60s-v2.mp4`。首次安装按工程README准备锁定版本依赖；本次直接复用Windows已有依赖。原音乐解码路径由`npm run prepare:pingtan`恢复。

- `scripts/stock_video/build_pingtan_v2.py`：截取行情、分配时间、阶段高点/突破/闪电事件、镜头轨迹、分轨声音和数据校验。
- `src/StockCinematicVideo.tsx`：沿用原项目玻璃K线材质，加入框选、虚线、碎玻璃、闪电与顶部信息。
- `src/stock-videos/pingtan-2025-v2.json`：可编辑生成数据；改算法或输入后重建此文件。
- 本目录`timeline.csv`、`brief.json`、`DIRECTOR.md`：精确帧表及本次导演要求。
- `research/summary.md`、`research/audit.py`：新增价量换手来源、统计和独立断言。
- `public/pingtan-2025-v2/music-original-excerpt.wav`：与原曲20.03秒起连续60秒PCM完全一致的独立音乐轨。
- `public/pingtan-2025-v2/foreground.wav`：上行音阶、玻璃、雷击音效；`mix.wav`为合轨。`audio-proof.json`记录原音乐哈希及无动态处理。

最终播放总母线固定0.7倍，同时作用于音乐和音效，留出编码余量；不变速、不变调、不压低人声、不随落点改变音乐音量，也不作响度归一化。单独音乐轨可与原曲选段逐采样比较。

## 镜头分配

|视频时间|内容|
|---|---|
|0—3秒|9月进入，快速扫至启动前|
|3—13.6秒|连板加速、9.62阶段高位，暂停、全局框选|
|13.6—22.2秒|突破9.62、后续上冲、复牌分歧与12.68框选|
|22.2—29.9秒|回撤修复、盘中越过12.68、13.27框选|
|29.9—37.6秒|再调整、突破13.27、15.97框选|
|37.6—50.7秒|调整后突破15.97、16.86最终顶部，先远后近长停留|
|50.7—58.7秒|随后急跌和2026后续行情|
|58.7—60秒|全局收束|

主要阶段高点统一自10月16日3.35元“启动低点”计算；不是从9月样本最小值随意挑选。框中交易日含首尾，涨停数按未复权收盘价限统计。突破若仅在最高价发生而收盘未守住，明确标注盘中突破。最高价16.86、当日成交量515.52万手、当日换手26.92%，不宣称为最高价瞬间的分时量。

本次只做本地交付，未提交GitHub。主观听感与连续观感由用户审核，自动和抽样检查范围见QA.md。
