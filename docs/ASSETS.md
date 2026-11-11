# 本地素材恢复

首次源码包不含音乐、音效、字体、GSAP二进制、参考视频、成片MP4和重复ZIP。原因是本次先审核代码与知识文档，保留本地素材边界并控制仓库体积。
projects/survivorship-bias/local-assets.example.json记录6项本地依赖的相对路径、大小与SHA-256。所有原文件保留在制作工作区。

从已有制作工程恢复（在仓库根目录执行）：

```powershell
python scripts/prepare_assets.py --from-project "你的原始运镜工程目录" --dry-run
python scripts/prepare_assets.py --from-project "你的原始运镜工程目录"
python scripts/verify_package.py --require-assets
```

恢复工具只复制清单中的6个文件，校验哈希；路径必须留在指定工程内。若目标已经存在不同文件则拒绝覆盖。不获取凭据、不联网、不生成替代音乐。
没有原始文件时，需要提供获准使用的本地音乐、字体、运行库和效果音，再单独审核更新清单；不能把缺失的依赖当作已安装。
具体来源记录见THIRD_PARTY_NOTICES.md。素材导入后仍被.gitignore排除，不会因准备预览而自动进入提交清单。
