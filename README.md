# 科普动画制作工作区

以“幸存者偏差”为案例，记录从科学资料核查、知识稿审核、逐页脚本、静态样张到HyperFrames动画与运镜修订的全过程。当前成果为30秒、1280×720、30fps的本地动画；本仓库保存审核后的项目源码与文档。

![用户认可的静态风格样张](previews/style-test.png)

## 阅读入口
- [完整项目总结](docs/PROJECT_SUMMARY.md)
- [已审核科普知识稿与来源](docs/knowledge/KNOWLEDGE.md)
- [逐页演示/剪辑稿](docs/planning/SCRIPT_V3.md)
- [参考风格分析](docs/planning/REFERENCE_STYLE.md)
- [动效与运镜导演方案](docs/planning/MOTION_DIRECTION.md)
- [制作流程](docs/WORKFLOW.md)、[版本记录](docs/CHANGELOG.md)、[检查结果](docs/QA.md)
- [GitHub提交审核清单](SUBMISSION_REVIEW.md)

## 代码结构
```text
projects/survivorship-bias/    最新连续运镜工程
  index.html                 场景、音乐和效果音挂载
  compositions/journey.html   SVG世界、固定文案层与GSAP时间轴
  build_motion.py            模板生成器
  drawing.py                 矢量绘图辅助函数
  camera-keyframes.json      相机矩阵与时间
  assets/vector-definitions.svg
  local-assets.example.json  本地依赖校验清单
scripts/                     本地素材导入及提交包验证
.agents/skills/science-video/ 科普制作流程约定
previews/                    本项目代码绘制画面的预览
```

## 本地运行
需要Node、Python、Chrome与FFmpeg。原制作版本见[环境记录](docs/ENVIRONMENT.md)。
先按[素材恢复说明](docs/ASSETS.md)恢复本地依赖；没有这些文件不能直接渲染。然后：

```powershell
cd projects/survivorship-bias
npm run dev
npm run check
npm run render
```

渲染命令固定HyperFrames 0.9.23，输出render-raw.mp4。若CLI尚未安装，npx需要网络下载依赖；已有缓存时可使用npx --offline hyperframes@0.9.23。
本项目没有付费模型调用，不包含生图照片。背景音乐与效果音的复用范围、来源见[依赖记录](docs/THIRD_PARTY_NOTICES.md)。

## 当前边界
知识稿、静态风格和30秒制作分别取得过用户确认；新一次GitHub提交必须另外审核。90秒完整知识版尚未制作。声音做过信号测量，未人工试听；用户的最终观看评价仍需保留。
