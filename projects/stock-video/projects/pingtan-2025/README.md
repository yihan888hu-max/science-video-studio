# 平潭发展 · 2025年至今 · V1

源工程基于GitHub `53fc41b` 的Remotion通用股票组件。1080×1920，30fps，900帧。行情截止2026-11-11；制作时11月12日盘中，不采用未完成日K。

先读[研究摘要与来源](research/summary.md)，剪辑节奏见[timeline.csv](timeline.csv)，输入为[brief.json](brief.json)、daily.json和unadjusted.json。时间轴和音轨由共用build.py生成；`src/ProjectRoot.tsx`新增Pingtan2025，原有Root及历史项目保留。

在工程根目录运行：

```sh
npm run check:pingtan
npm run dev
npm run prepare:pingtan
npm run rebuild:pingtan
npm run render:pingtan
```

生成输出为`out/pingtan-development-2025-now-v1-final.mp4`，PNG逐帧生成、BT.709、8位YUV420P，确保颜色转换和播放兼容性。首次运行按工程README准备锁定依赖；Windows制作复用了本地已有的同版本Remotion依赖，未重复安装。

配乐为用户提供《01 清明上河图.mp3》，总长204秒，选20.03—50.03秒。原曲解码成PCM16双声道后放在`local-media/pingtan/qingming.wav`供生成器读取；该目录及本片混音WAV保留本地。换设备需要恢复音源；现有混音位于`public/pingtan-2025-v1/mix.wav`。原始音频不覆盖。选段、采样、事件落点、音乐闪避见brief及audio-design.json。音效是共用标准库生成的原创电子提示音；有独立foreground.wav和music-bed.wav供调整。

本片沿用玻璃2.5D蜡烛、局部动态取景、屏幕固定HUD、完成后停顿与事件粒子。数据/时间被压缩，生长是OHLC视觉插值，不重现真实分时先后；画面涨幅明确为低高振幅。主要统计卡为停牌前节点及全区间高点。已公开消息从对应日期开始显示，停牌日期不补造K线。

质量检查见QA.md。当前只本地交付；远程仓库未提交本次改动。
