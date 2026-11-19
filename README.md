# ffmpeg-zh-docs · FFmpeg 官方文档中文翻译

> 译自 [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)（官方无任何中文版本），基线 **n9.0.2**（2026-09-18 tag）。
> 跟随上游 release 节奏的**增量翻译体系**：段落级 hash 对比 + 每滤镜一页，上游出新版本只译变更内容。

## 站点

- 在线阅读：https://jxsword.github.io/ffmpeg-zh-docs/（M4 上线）
- 版本策略：`latest` 指向当前基线；每个翻译基线 tag 独立版本目录；在线保留最近 2 个 major 线

## 覆盖范围

| 类别 | 内容 | 说明 |
|---|---|---|
| CLI 手册 | ffmpeg / ffplay / ffprobe + 公共选项 | 独有内容 + 组件交叉链接（DR-009） |
| 组件 | utils/codecs/formats/protocols/devices 等 | 官方 Components 页粒度 |
| 滤镜 | **每滤镜一页**（video/audio/multimedia 分组） | 增量粒度到滤镜级（DR-008） |
| 库页 | libavutil 等 7 库 | |
| General | FAQ/平台/开发者/git/FATE 等 | |
| wiki 精选 | Trac 社区 wiki 常青页（CC BY-SA 3.0 分离标注） | |
| API | 公开头文件 Doxygen 注释翻译 + Doxygen 中文重建 | 中文首例 |

## 仓库结构

```
scripts/    转换/同步/校验/构建脚本（MIT）
source/     英文 md（texi→md 转换产物，只读；UPSTREAM.json 记录基线与工具版本）
zh/         中文翻译（站点内容）
api/        API 注释（en/ 提取、zh/ 翻译、meta/ 范围）
wiki/       wiki 精选（en/ 快照、zh/ 翻译、meta/）
config/     glossary.yml 术语表、style-guide.md 风格指南、quality-metrics.yml
tests/      脚本单测（pytest）
docs/       决策记录、翻译看板、交接文档
```

## 本地构建

```bash
pip install -r requirements.txt
# 校验
python scripts/validate_structure.py
pytest tests/
# 站点
mkdocs serve
```

工具链版本锁定：texinfo（基线 7.2）、pandoc（3.7.0.2）、doxygen（1.15.0）——与 `source/UPSTREAM.json` 比对，CI 不一致即失败。

## 贡献

见 [CONTRIBUTING_TRANSLATION.md](CONTRIBUTING_TRANSLATION.md) 与 [翻译任务看板](docs/translation-board.md)。

## 许可

- 工程代码（scripts/tests/CI）：[MIT](LICENSE)
- 正文与 API 译本：LGPL-2.1-or-later（推定，见 [LICENSE_TRANSLATION.md](LICENSE_TRANSLATION.md) 与 [COPYING.LGPLv2.1](COPYING.LGPLv2.1)）
- wiki 精选页：CC BY-SA 3.0，署名 "Contributors to the FFmpeg Community Documentation Wiki"
- 未搬运 ffmpeg-web 网站资产；未衍生 FFmpeg 的 GPL 文件（doc/t2h.pm、doc/texi2pod.pl）

## 致谢

[fmtlib/fmt](https://github.com/fmtlib/fmt) 中文翻译工程（fmt-zh-docs）的流水线惯例、[here200/ffmpeg-doc-zh](https://github.com/here200/ffmpeg-doc-zh) 的翻译工程资产、[ayosec/ffmpeg-filters-docs](https://github.com/ayosec/ffmpeg-filters-docs) 的每滤镜一页机制。
