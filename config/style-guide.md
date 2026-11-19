# FFmpeg 中文文档翻译风格指南

> 结构对齐 here200 翻译说明四段式（翻译范围/不译清单/术语标准/校验记录），
> 核心原则沿用 fmt-zh-docs 惯例；本指南冻结于 M1，M2 批次 B1 完成后随
> glossary v1 一并复审。

## 一、翻译范围

| 内容 | 位置 | 范围 | 优先级 |
|---|---|---|---|
| CLI 手册 | `zh/manual/` | ffmpeg/ffplay/ffprobe 独有内容 + 公共选项 | P0 |
| 组件文档 | `zh/components/` | 官方 Components 页粒度 | P0 |
| 滤镜 | `zh/filters/` | 每滤镜一页（构建期由整卷拆分） | P0 |
| 库页 | `zh/libraries/` | 7 个 lib* 短页 | P0 |
| General | `zh/general/` | FAQ/平台/开发者/git/FATE/作者等 | P0 |
| P2 补充 | `zh/general/` | mailing-list-faq/nut/community/drawvg-reference | P2 |
| API 注释 | `api/zh/` | 公开头文件 Doxygen 注释（M2 后期批） | — |
| wiki 精选 | `zh/wiki/` | P0 32 页（预处理分级预检通过者） | P0 |
| 变更日志 | `general/APIchanges.md` | **不翻译**（英文占位页，fmt DR-014 口径） | 豁免 |

段落状态口径（`.translation-state.json`）：`pending`=待翻译；`skipped`=不译豁免
（分母=可译段数，豁免段不计入覆盖率）。

## 二、不译清单

以下内容**原样保留英文**，任何情况下不得翻译或改写：

1. **代码块**（``` 围栏整块）：命令行示例、C 代码、配置片段；
2. **内联代码**（`` ` `` 包裹）：选项名、滤镜名、协议名、函数名、常量名、
   文件路径、`-vf`/`-af`/`-filter_complex` 等参数；
3. **专有名词**：`ffmpeg`/`ffprobe`/`libavutil` 等工具与库名、`AVCodecID`
   等类型名、`YUV`/`RGB`/`H.264`/`AAC` 等标准名、`VAAPI`/`NVDEC` 等硬件名；
4. **URL 与邮箱**；
5. **表格中的 Term 列**（选项/值名）；
6. **命令行示例中的参数值**（`-vf scale=640:480` 整体保留）。

**易错点**：滤镜名与滤镜选项名同名异义（如 `scale` 滤镜名 vs "scaling"
动词语义）——名字不译，语义按术语表翻译。

## 三、术语标准

- 术语表：`config/glossary.yml`（128 条，M1 初版；**B1 批完成后冻结 v1**）；
- 首次出现可括注原文：`滤镜链图 (filtergraph)`；此后统一用中文译名；
- 术语表未收录的术语：首次使用时在 PR 中讨论并加入术语表；
- **高频基线**：filter=滤镜、filtergraph=滤镜链图、muxer=复用器、
  demuxer=解复用器、bitstream filter=比特流滤镜、codec=编解码器、
  encoder=编码器、decoder=解码器、packet=包、frame=帧、sample=采样；
- 上下文消歇（fmt DR-003 惯例）：同一术语在不同文件语境下如有必要区分，
  以 glossary 的 context 字段为准。

### 语气与标点

| 场景 | 推荐 | 避免 |
|---|---|---|
| 指令 | 使用 `ffmpeg -i in.mp4 out.mp4` 转码。 | 你可以用 ffmpeg 来转码 |
| 陈述 | 该滤镜接受以下选项。 | 这个滤镜有很多选项啦 |
| 您/用户 | 您可以通过... | 你可以通过... |

- 中文句子用中文标点；夹杂代码时逗号句号用中文，引号内代码内容原样；
- 括号内纯英文用英文标点：`支持 C++20 (C++20)`；
- 数字与单位间不译：`128 kbps`、`30 fps` 原样。

## 四、校验记录

自动化校验（CI 强制，`validate_translation.py` M2 上线后执行）：

| 校验项 | 目标 | 工具 |
|---|---|---|
| 术语一致性 | ≥99% | glossary 注入 + 校验器 |
| 代码块完整性 | 100%（hash 一致） | validate_translation.py |
| 内联代码完整性 | 100% | validate_translation.py |
| 结构完整性（标题/列表/表格 AST 对比） | 100% | validate_translation.py |
| 占位符还原 | 100% | protect_untranslatable 惯例 |
| 中文标点 | 告警级 | validate_translation.py |

人工抽检：每版本发布前随机 50 段，通过率 ≥95%（quality-metrics.yml）。

### 滤镜页特别约定（DR-008）

- 翻译单元=滤镜小节：译文写入 `zh/components/filters.md` 整卷对应位置，
  站点拆页由构建期完成；
- 每滤镜页内的 `### Options` / `### Examples` / `### Commands` 小节标题
  **统一译法**：选项 / 示例 / 运行时命令；
- 示例代码块整块保留，示例前的引导句翻译。

### wiki 页特别约定（DR-004/DR-006）

- 页脚署名块**不可删改**（CC BY-SA 3.0 合规要求）；
- Trac 宏（`[[Image]]`/`[[Include]]`）按预处理分级处理：plain/macro-light
  直译，macro-heavy 宏输出占位保护，degrade 级不翻译仅外链。
