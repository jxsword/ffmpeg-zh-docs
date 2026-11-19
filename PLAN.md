# FFmpeg 中文文档翻译项目 - 完整实施计划（PLAN.md v2）

> 制定时间：2026-11-19｜**v2：三轮复审修订版**｜状态：**已批准（2026-11-19 用户确认，DR-009 一并生效），待新会话实施 M1**
> 修订记录：R1 完整性与一致性复审、R2 技术可行性细化复审、R3 风险/合规/终审复审（详见文末"三轮复审修订记录"）
> 依据：`research/ffmpeg-zh-projects-调研报告.md`（S1+S2 合并）、`docs/decision_log.md` DR-001~009、fmt-zh-docs 既有惯例（DR-011~014 只读借鉴）
> 纪律：长任务/内存不可预估脚本一律 `memgate [上限MB] <cmd>` 包裹；URL 引用须实测可达并标注日期通道

---

## 📋 目录

1. [项目概览](#项目概览)
2. [决策记录汇总](#决策记录汇总)
3. [范围映射（DoD 1）](#范围映射dod-1)
4. [texi→md 转换管线设计（DoD 2）](#teximd-转换管线设计dod-2)
5. [API 注释翻译管线](#api-注释翻译管线)
6. [wiki 精选翻译与同步](#wiki-精选翻译与同步)
7. [仓库结构与 git 管理（DoD 3）](#仓库结构与-git-管理dod-3)
8. [CI/CD 流水线](#cicd-流水线)
9. [配置文件规范](#配置文件规范)
10. [里程碑与交付计划（DoD 4）](#里程碑与交付计划dod-4)
11. [质量校验（DoD 5）](#质量校验dod-5)
12. [许可与署名（DoD 6）](#许可与署名dod-6)
13. [站点发布（DoD 7）](#站点发布dod-7)
14. [风险与对策（DoD 8）](#风险与对策dod-8)
15. [执行顺序与依赖（DoD 9）](#执行顺序与依赖dod-9)
16. [三轮复审修订记录](#三轮复审修订记录)

**DoD 对照**：1→§3｜2→§4/§5/§6｜3→§7｜4→§10｜5→§11｜6→§12｜7→§13｜8→§14｜9→§15

---

## 项目概览

### 目标

将 [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)（官方无任何中文版本，S2 已核实）全类别译为中文，建立**跟随上游 release 节奏的增量翻译体系**，与 fmt-zh-docs 同构的 GitHub 公开仓 + Actions/Pages 工程家族成员。

### 核心特性

- **增量翻译**：段落级 hash 对比 + 滤镜级拆页（DR-008），仅译变更内容
- **转换链实测可用**：makeinfo→DocBook→pandoc→GFM（DR-007，2026-11-19 冒烟实测）
- **术语一致性**：上下文感知术语表（fmt 惯例）+ here200 术语表种子校订
- **代码保护**：占位符替换法（fmt DR-004 惯例），命令行示例/选项名绝不误译
- **API 中文首例**：注释翻译 + Doxygen 重建（DR-005；调研确认全网为零）
- **合规先行**：LGPL 2.1+ 推定声明 + wiki CC BY-SA 3.0 分离标注（DR-006）

### 上游文档源

| 源 | URL | 核实日期 | 说明 |
|----|-----|----------|------|
| 文档源码仓 | https://git.ffmpeg.org/ffmpeg.git | 2026-11-19（交接文档，直连+代理双通道） | 正文 .texi 在源码树 doc/ |
| GitHub 镜像 | https://github.com/FFmpeg/FFmpeg | 2026-11-19（S2 浅克隆实测，10.9s 直连） | sync 优先走镜像（HEAD 与官方一致） |
| 网站源码仓 | https://git.ffmpeg.org/ffmpeg-web.git | 2026-11-19（S2 克隆实测） | **无许可声明，不搬运其文案/设计（DR-006）** |
| trac wiki | https://trac.ffmpeg.org/wiki | 2026-11-19（S2/S1 curl 实测） | CC BY-SA 3.0，精选翻译 |
| 文档导航页 | https://ffmpeg.org/documentation.html | 2026-11-19（S2 curl 实测） | trunk nightly 重生成，非 release 版 |

### 翻译基线

**n9.0.2**（2026-09-18 tag，S2 实测当前最新稳定；DR-002）。release 节奏实测：major 约年更（403/504/346 天）、x.1 约 major 后半年、point 成批集中 5-6 月/11 月维护窗口 → 理论增量压力 ≈ 每年 1 次 major 大增量 + 半年 1 次 minor + 若干 point 小修。

### 现有项目调研结论（详见调研报告）

- 全网无"持续跟进上游"的中文翻译项目（两个存活候选分别停更 2026-09/2025-08），**增量机制是全网空白**
- 无候选可直接作内容基底；可借鉴：here200 翻译工程资产（术语表/不译清单/分批计划）、ffmpeg.net.cn 25/25 sitemap 与 Doxygen 目录布局、ayosec 每滤镜一页机制、xdsnet 章节粒度与术语语料
- **API/Doxygen 中文翻译全网为零**——本工程将成中文首例
- 体量实测：去重正文 37 文件 = 2,007,698 B / **292,805 词**；filters.texi 占 47%（141,693 词）

---

## 决策记录汇总

| DR | 标题 | 状态 | 关键决策 |
|----|------|------|----------|
| DR-001 | 仓库托管与发布 | 生效 | GitHub 公开仓 + Actions 四条流水线 + mkdocs Material |
| DR-002 | 上游跟踪基线 | 生效 | 最新稳定 release tag（当前 n9.0.2） |
| DR-003 | 正文载体 | 生效 | texi→md（makeinfo→DocBook/HTML→md）+ mkdocs 流水线 |
| DR-004 | Community 范围 | 生效 | wiki 精选高价值常青页 + books 页仅译自身说明 |
| DR-005 | API 文档 | 生效 | 注释提取翻译 + Doxygen 重建，只译最新版本 |
| DR-006 | 许可与署名 | 生效 | 按推定 LGPL 2.1+ 发布 + wiki CC BY-SA 3.0 分离标注 + ffmpeg-devel 并行确认 |
| DR-007 | 转换器选型 | 生效 | makeinfo→DocBook→pandoc→GFM + 自研后处理/校验器 |
| DR-008 | filters 粒度 | 生效 | 每滤镜一页（source 整卷 + 构建期拆页 + 锚点映射） |
| DR-009 | 手册页结构 | 生效（随计划批准） | 手册页=独有内容+组件交叉链接，不内联共享件 |

翻译执行方式沿用 fmt-zh-docs 既定约定：**M2 会话内 agent 翻译（零 key）、M3 CI 增量用英伟达 provider `z-ai/glm-5.3-flash`（OpenAI 兼容）、凭据走 `NVIDIA_API_KEY` 环境变量/GitHub Secrets、config/llm.yml 只存非敏感项**（fmt DR-012/013）。

---

## 范围映射（DoD 1）

### 3.1 正文映射表（官网类别 → texi → source/ → zh/）

去重正文 **37 个 .texi**（S2 体量表为准，词数为 n9.0.2 实测）：

| 官网类别 | texi（词数） | source/ | zh/ 站点页 | 优先级 |
|---|---|---|---|---|
| CLI 手册（DR-009） | ffmpeg.texi (18,303)、ffplay.texi (1,389)、ffprobe.texi (3,045) **仅独有内容** | source/manual/{ffmpeg,ffplay,ffprobe}.md | /manual/*/ | P0 |
| 手册共享件 | fftools-common-opts.texi (2,243) | source/manual/fftools-common-opts.md | /manual/common-options/（3 手册交叉链接） | P0 |
| 组件正文 | utils (3,422)、codecs+decoders+encoders (3,408+3,023+19,808)、bitstream_filters (4,858)、formats+demuxers+muxers+metadata (1,542+6,856+20,436+375)、protocols (11,318)、devices→indevs+outdevs (7,334+1,906)、resampler (1,132)、scaler (753) | source/components/*.md（官方 Components 页粒度） | /components/*/ | P0 |
| 滤镜卷（DR-008） | filters.texi (141,693) | source/components/filters.md 整卷 | /filters/{video,audio,multimedia}/<滤镜名>/ 拆页 | P0 |
| 库页 | libavutil (168)、libswscale (190)、libswresample (238)、libavcodec (118)、libavformat (108)、libavdevice (96)、libavfilter (85) | source/libraries/*.md | /libraries/*/ | P0 |
| General | faq (3,880)、general_contents (9,979)（经 general 外壳）、platform (1,565)、developer (6,787)、git-howto (2,026)、fate (1,452)、authors (53) | source/general/*.md | /general/*/ | P0 |
| 官网未列但可构建 | mailing-list-faq (1,924)、nut (726)、community (1,367)、drawvg-reference (9,199) | source/general/ | /general/*/ | P2（M2 后期批） |
| 变更日志 | doc/APIchanges（179,886 B 纯文本） | source/general/APIchanges.md | /general/APIchanges/ **英文占位页**（fmt DR-014 口径，nav 标注"英文原文"；M2 余量充足时再评估翻译） | P2 |

> **11 个 @include 纯外壳**（ffmpeg-{utils,...}.texi 等 9 个 + general/devices 外壳）不进入翻译队列——转换时解析 include、正文归入对应内容件（对齐 S2 §2.2 口径）。
> **构建期生成物**：仅 doc/config.texi 需补齐（`./configure` 不 make 即生成，见 §4.1）；doc/avoptions_*.texi 经 S2 实测**无任何 @include 引用**（选项表已硬编码在 codecs/formats.texi），无需生成。
> **严禁触碰**：doc/t2h.pm、doc/texi2pod.pl（GPL 文件，LICENSE.md 明列；原样构建无碍，不翻译不修改）。
> **-all 合集页不构建**（R1 复审修正）：内容为主手册+组件页并集，单页体量（约 29 万词）与 DR-008"大单页劣化"论证矛盾；官方 ffmpeg-all.html 外链保留在导航"官方参考"区。

**codecs/formats 拆分预案**（不实施，仅登记）：codecs.md（约 2.6 万词）、formats.md（约 2.9 万词）如站点体验不佳，可沿天然 include 缝合线拆为 codecs/{decoders,encoders}、formats/{demuxers,muxers} 子页——届时按轻量决策执行，不动 DR-008。

### 3.2 wiki 精选初选清单（DR-004，DoD 1 必备）

trac wiki 实测约 290 页（TitleIndex 2026-11-19），剔除 Trac 系统页/GSoC 历史页/沙盒后内容页约 150 页；初选清单如下（翻译前每页以 CC BY-SA 3.0 页脚 + 署名 + 快照日期标注，见第 12 节）：

**P0 首批（32 页，M2 主批）**：

| 主题组 | 页面 |
|---|---|
| 编码指南（7） | EncodingGuide、Encode/H.264、Encode/H.265、Encode/AV1、Encode/VP9、Encode/AAC、Encode/MP3 |
| 编译指南（7） | CompilationGuide、CompilationGuide/Ubuntu、CompilationGuide/Generic、CompilationGuide/macOS、CompilationGuide/MinGW、CompilationGuide/MSVC、CrossCompilingForWindows |
| 滤镜/剪辑实操（8） | FilteringGuide、Scaling、CroppingVideo、Concatenate、AudioVolume、FancyFilteringExamples、Slideshow、AfadeCurves |
| 工具/选项（4） | FFprobeTips、How to use -map option、Seeking、Creating multiple outputs |
| 硬件加速（4） | HWAccelIntro、Hardware/VAAPI、Hardware/QuickSync、Hardware/AMF |
| 流媒体/字幕（2） | StreamingGuide、How to burn subtitles into the video |

**P1 次批（27 页，M2 机动/M4 前完成）**：denoise、Blend、Xfade、AudioChannelManipulation、Chroma Subsampling、colorspace、Histogram、Vectorscope、Waveform、Capture/PulseAudio、Capture/Webcam、Capture/Desktop、DirectShow、EncodingForStreamingSites、EncodeforYouTube、GuidelinesHighQualityAudio、Encode/HighQualityAudio、ExtractSubtitles、HowToConvertSubtitleToASS、ChangingFrameRate、Debug/MacroblocksAndMotionVectors、Using libav*、Including FFmpeg headers in a C++ application、MaintainingFFmpeg、MailingListEtiquette、Errors、Windows_Tips

**特殊处理**：BooksAndOtherExternalResources 按 DR-004 **仅译页面自身说明段**（书刊列表不译，外链保留）。
**预处理分级（R2 补充）**：M2 批次规划前逐页预检 TracWiki 标记复杂度——纯文本/基础标记页直译；宏密集页（[[Image]]/[[Include]]/模板/动态列表）宏输出占位保护、模板段跳过；宏占比过高且常青价值低的页降级到 P1 外清单（不翻译，仅外链），预检结果随批次计划落盘。
**清单维护**：P0/P1 为初选，M4 后按用户反馈增删；增删走 CONTRIBUTING 评审，不触发新 DR。

### 3.3 API 范围（DR-005）

- 对象：n9.0.2 基线 `libav*/`、`libswscale/`、`libswresample/` 公开头文件（.h）中的 Doxygen 注释（公开 API）；.c 内部注释不译（保留英文，Doxygen 输出原样）
- 产出：`api/en/*.md`（提取）→ `api/zh/*.md`（翻译）→ 回填 → 本地 doxygen 重建中文 HTML → 站点 /api/
- 许可标注：随文件许可（LGPL 2.1+ 为主；libavfilter 40 个 GPL 文件清单在 api/ 许可页列明，DR-006）

---

## texi→md 转换管线设计（DoD 2）

### 4.1 转换链（DR-007）

```
FFmpeg tag n9.0.x（GitHub 镜像浅克隆）
  → doc/*.texi + ./configure（不 make，仅生成 doc/config.texi；avoptions_*.texi 无需，S2 实测无引用）
  → makeinfo --docbook -I doc --no-split（逐文件；configure 要求 texinfo 主版本 ≥5，本机 7.2 实测满足）
  → pandoc -f docbook -t gfm
  → scripts/texi2md.py 后处理（实测已知 4 项）：
      ① texinfo 弯引号 ‘…’ 残留清理（保留代码 span 内容）
      ② variablelist 项/值对结构化（转为 "term" 加粗 + 值列表，选项表格化）
      ③ 缩进代码块 → fenced code（保留缩进层级，标注语言）
      ④ 标题层级规整（@chapter→# 页标题偏移、@section→##）+ 锚点 slug 生成
  → source/<域>/<文件>.md + source/UPSTREAM.json（记录 tag/commit/转换工具版本）
```

- **include 解析（DR-009）**：转换器按 doc/Makefile 的 include 依赖拆解——手册页只取工具独有内容；共享件各归其位（components/manual-common/general）；11 个外壳不产出独立 md。
- **锚点映射**：构建 `config/anchor_map.yml`（双向：中文标题 slug ↔ 官方 HTML 锚点如 `#Video-size`）；mkdocs `toc.slugify: python-markdown-nonorm`（保留大小写）+ fix_links.py 兜底，兼容官方外链（fmt 惯例）。
- **-all 视图**：不构建（R1 修正，见 §3.1 注记）。

### 4.2 转换校验器（scripts/validate_structure.py）

DR-003 要求的兜底，校验项：

1. **结构计数对比**：转换前后标题数/代码块数/列表项数/表格数逐级对比（阈值 0 差异，DocBook XML 为中间基准）
2. **锚点完备**：每个 @node/@anchor 在 anchor_map.yml 有映射
3. **include 完备**：手册页/外壳引用的每个内容件均有对应 source md，且手册页不含内联共享内容（DR-009 校验）
4. **占位符保护**：@code/@option/@var 等原文标记内容未被转换破坏（fmt protect_untranslatable 惯例前置）
5. **命令示例静态校验（R2 补充）**：CLI 示例中 `-vf/-af/-filter` 后的滤镜名与拆页滤镜清单比对（未知名告警）；**不做运行时执行验证**——fmt DR-009 编译验证不适用于本工程（示例依赖媒体文件/编码器环境），以结构保护+静态清单替代，此差异已在计划中显式确认
6. **失败行为**：任一项失败阻断入库，输出差异报告（文件/行号/类型）

### 4.3 filters 拆页（DR-008）

- `source/components/filters.md` 整卷存储（翻译单元=滤镜小节，段落 hash 到滤镜级）
- `scripts/split_filters.py` 构建期拆分：按 `@section <滤镜名>` 切分 → `zh/filters/{video,audio,multimedia,...}/<滤镜名>.md`
- 分组导航按官方 chapter（Video/Audio/Multimedia Filters 等）自动生成（借鉴 ayosec 分组推断）
- 官方锚点兼容：`ffmpeg-filters.html#<filter>` → 新 URL 映射表 + 404 兜底跳转页

### 4.4 增量同步流程（scripts/sync_docs.py，fmt 同名脚本改造）

```
检测最新稳定 tag：git ls-remote --tags GitHub 镜像 → 过滤 -dev 后缀
  → annotated tag 日期校验（for-each-ref creatordate，S2 同款方法）→ 确认最新稳定
  → 有新 tag：浅克隆 → ./configure（仅取 config.texi）→ 全量转换 source/
  → 与旧 source/ 段落 hash diff → .translation-state.json 标记 pending/changed/deleted
  → 输出变更摘要（文件/新增段/修改段/删除段）→ 自动创建 Sync PR
```

M3 演练数据源：GitHub 镜像 trunk 的 doc/ 目录与 n9.0.2 基线做真实 diff 模拟一次增量（不等真实新 tag）。

---

## API 注释翻译管线

```
n9.0.2 checkout（api 分支：api-baseline/n9.0.2）
  → scripts/extract_api_comments.py：解析 libav*/*.h Doxygen 注释块 → api/en/<库>/<头文件>.md
     （保序保留 @param/@return/@note 结构，代码片段占位保护）
  → M2 会话内 agent 翻译 / M3 CI translate_batch（共用 fmt 管线）
  → scripts/backfill_api_comments.py 回填源文件（结构逐字段还原）
  → scripts/validate_backfill.py 回填校验：@param 数量与顺序一致、@return/@brief 存在、非注释代码区零改动
  → 本地 doxygen（1.15.0 实测满足）重建中文 HTML → 站点 /api/
  → 随基线 tag rebase 持续更新（DR-005）
```

M1 验证项：实测 Doxyfile 的 EXTRACT_ALL/INPUT 配置（doxy-wrapper.sh 注入机制），确定公开 API 提取范围清单（预计 libav* 公共头百余个文件）并落盘 `api/meta/scope.md`。

---

## wiki 精选翻译与同步

- 快照获取：`curl https://trac.ffmpeg.org/wiki/<页面>`；**限速抓取（每请求间隔 ≥2s）+ 本地缓存**，避免对 trac 施压（R3 风险对策）；README 版本号 + 修改日期入 `wiki/meta/<页面>.json`
- TracWiki 语法 → md 转换器 `scripts/wiki2md.py`（子集：标题/表格/链接/粗斜体/代码块）；宏与模板输出占位保护；页面按 §3.2 预处理分级后进入批次
- 每页页脚固定块（DR-006）：
  > 本文译自 [FFmpeg Community Documentation Wiki – <页面>](原文 URL)（快照于 YYYY-MM-DD，版本 N），以 [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) 授权，署名 "Contributors to the FFmpeg Community Documentation Wiki"。
- 同步：M4 起 sync-upstream 每季度抽查 P0 页 diff（页面版本号变化即告警），变更走增量翻译；P1 页仅按需更新

---

## 仓库结构与 git 管理（DoD 3）

### 7.1 仓库结构（单仓，与 fmt-zh-docs 同构）

```
ffmpeg-zh-docs/
├── .github/workflows/
│   ├── sync-upstream.yml          # 每周一 cron + 手动 --tag：检测新 tag → Sync PR
│   ├── validate.yml               # PR + 每日：全量校验（结构/翻译/回填）+ 质量报告
│   ├── deploy.yml                 # main 推送 + 基线 tag：mkdocs + mike 部署 Pages
│   ├── translate-incremental.yml  # M3 启用：pending 段 → glm-5.3-flash 翻译 → 校验 → 提交
│   └── test.yml                   # pytest（scripts 单测）
├── scripts/
│   ├── sync_docs.py               # tag 检测/克隆/configure/转换调度/diff（fmt 版改造）
│   ├── texi2md.py                 # makeinfo→pandoc→后处理（DR-007）
│   ├── split_filters.py           # filters 拆页（DR-008）
│   ├── wiki2md.py                 # trac wiki → md
│   ├── extract_api_comments.py    # API 注释提取（DR-005）
│   ├── backfill_api_comments.py   # 注释回填
│   ├── protect_untranslatable.py  # 占位符保护（fmt 移植）
│   ├── generate_bilingual.py      # 双语对照（fmt 移植）
│   ├── translate_batch.py         # M3 接 API 适配器（fmt 移植改造）
│   ├── validate_structure.py      # 转换校验器（DR-007/003/009）
│   ├── validate_translation.py    # 翻译校验（fmt 移植扩展）
│   ├── validate_backfill.py       # 回填校验（DR-005）
│   ├── fix_links.py               # 链接/锚点修复（fmt 移植 + anchor_map 双向映射）
│   ├── build_site.py              # filters 拆页调度 + mkdocs nav 生成
│   ├── rollback_translation.py    # 回滚（fmt 移植）
│   └── prompts/translate.md.j2    # Prompt 模板
├── source/                        # 英文 md（转换产物，只读，sync 更新）
│   ├── UPSTREAM.json              # 基线 tag/commit/转换工具版本
│   ├── manual/ components/ libraries/ general/
├── api/                           # API 注释（en/ 提取、zh/ 翻译、meta/ 范围与许可清单）
├── wiki/                          # wiki 精选（en/ 快照转 md、zh/、meta/）
├── zh/                            # 中文翻译（站点 docs_dir；manual/ components/ filters/ libraries/ general/ wiki/）
├── config/
│   ├── glossary.yml               # 术语表（here200 term_pairs 种子校订 + xdsnet 术语语料参考）
│   ├── style-guide.md             # 风格指南（here200 四段式模板 + fmt 惯例）
│   ├── quality-metrics.yml        # 质量指标
│   ├── anchor_map.yml             # 锚点映射（构建期生成，双向）
│   └── llm.yml                    # M3 创建：provider/base_url/model/api_key_env（fmt DR-013 惯例）
├── tests/                         # 各脚本单测（texi2md/split_filters/wiki2md 固样测试）
├── docs/                          # decision_log.md、translation-board.md、handoff
├── LICENSE                        # 工程代码 MIT（fmt 惯例）
├── LICENSE_TRANSLATION.md         # 译本许可声明（DR-006）
├── COPYING.LGPLv2.1               # FSF 标准全文副本（DR-006）
├── CONTRIBUTING_TRANSLATION.md / AUTHORS_TRANSLATION.md
├── mkdocs.yml                     # docs_dir: zh；nav 含 filters 分组动态生成
├── .translation-state.json        # 段落级翻译状态
└── PLAN.md / README.md
```

### 7.2 git 管理与上游快照

- **单仓单分支主线**（main）+ 功能分支 PR；基线 tag 对应 `translation/n9.0.2` 标签；API 翻译在 `api-baseline/n9.0.2` 分支隔离
- **原始 .texi 不入库**：source/ 只存转换后 md；UPSTREAM.json 记录 tag/commit 使任意历史可重建（`sync_docs.py --rebuild-tag n9.0.2`）
- **增量机制**：sync-upstream 定时检测最新稳定 tag；新 tag → 全量转换 + 段落 hash diff → state 标记 → Sync PR → 合并后触发增量翻译（M3）；major 大版本触发 L1/L2/L3 分级响应（沿用 fmt DR-007 惯例：结构变化 <10% 自动迁移 / 10-30% 半自动 / >30% 冻结+冲刺）
- **filters 粒度**：hash 单元=滤镜小节 → 大版本时仅变更滤镜进入 pending（DR-008 兑现"仅译变更滤镜"）

---

## CI/CD 流水线

| workflow | 触发 | 流程要点 |
|---|---|---|
| sync-upstream.yml | 每周一 02:00 + 手动(指定 tag) | 检测最新稳定 tag → sync_docs.py → 变更则创建 Sync PR（附变更统计） |
| translate-incremental.yml（M3） | Sync PR 合并 + 手动 | 读 state pending 段 → 按文件/滤镜分批 → translate_batch.py（英伟达 `z-ai/glm-5.3-flash`，Secret `NVIDIA_API_KEY`）→ validate → 通过自动提交/失败标记人工复核 |
| validate.yml | 所有 PR + 每日 | validate_structure（转换层）+ validate_translation（译文层）+ validate_backfill（API 层）+ 单测 + 质量报告 Artifact |
| deploy.yml | main 推送（zh/ 变更）+ 基线 tag | mkdocs build（filters 拆页）→ mike deploy latest/<tag> → Pages |
| test.yml | PR + main | pytest --cov=scripts --cov-fail-under=80 |

**工具链锁定（R3 补充）**：CI 安装 texinfo 与 pandoc 后将版本写入 job 输出并比对 UPSTREAM.json 记录，不一致即失败（防止 makeinfo/pandoc 版本漂移改变转换输出）；版本升级为显式人工变更（更新 UPSTREAM.json + 全量转换重放校验）。

凭据纪律对齐 fmt DR-013：仅环境变量/Secrets，config/llm.yml 无凭据字面量。

---

## 配置文件规范

- **glossary.yml**（fmt DR-003 上下文消歇惯例）：种子 = here200 `term_pairs.json`（校订后入库）+ xdsnet 语料仅作对齐参考不作默认。**首批核心术语定稿基线（R3 明确，M1 落盘 ≥100 条，M2 批次 B1 完成后冻结 v1，此后增补走评审）**：

| en | zh（初选） | 备注 |
|---|---|---|
| filter | 滤镜 | |
| filtergraph | 滤镜链图 | 对齐 xdsnet 语料 |
| muxer | 复用器 | 社区主流技术译法 |
| demuxer | 解复用器 | 与"复用器"对应 |
| bitstream filter | 比特流滤镜 | |
| codec / coder / decoder | 编解码器 / 编码器 / 解码器 | |
| protocol | 协议 | |
| sample / frame / packet | 采样 / 帧 / 包 | |
| scale / resample | 缩放 / 重采样 | |
| device | 设备 | |
| stream / format | 流 / 格式 | |
| hardware acceleration | 硬件加速 | |

- **style-guide.md**：here200 四段式结构（翻译范围/不译清单/术语标准/校验记录）+ fmt 核心原则（代码不译/术语统一/专业语气/结构保持）；FFmpeg 特有：命令行示例整块保护、选项名/滤镜名/协议名保留英文、`@option` 项值对表格化规则、`-vf/-af` 等参数在示例中保留原样
- **quality-metrics.yml**：见第 11 节指标表
- **llm.yml**（M3 创建）：`provider: nvidia / base_url: https://integrate.api.nvidia.com/v1 / model: z-ai/glm-5.3-flash / api_key_env: NVIDIA_API_KEY`（fmt DR-012/013 同款，2026-11-19 fmt 工程实测可达）

---

## 里程碑与交付计划（DoD 4）

| 阶段 | 任务 | 交付物 | 验收标准 |
|---|---|---|---|
| **M1 基建**（预计 3~5 个工作会话，R1 修正） | git init + 远程仓 + 仓库结构 + LICENSE 系列 + CONTRIBUTING/AUTHORS 骨架 + texi2md.py/split_filters.py/validate_structure.py + sync_docs.py 改造 + ./configure 补 config.texi + 全量转换 n9.0.2 + wiki2md 骨架 + mkdocs 骨架 + CI 四条 + glossary/style 初版 + Doxyfile 提取范围实测 + wiki P0 页预处理分级预检 | 可运行的"同步→转换→校验→构建"链路，source/ 全量入库 | ① 37 个正文文件转换成功且 validate_structure 0 错误 ② filters 拆页抽检 20 个滤镜页结构正确 ③ 手册页不含内联共享内容（DR-009 校验通过）④ mkdocs 本地构建成功 ⑤ sync_docs.py --tag n9.0.2 可重放 ⑥ CI 首跑全绿 ⑦ 段落总数与翻译批次计划落盘 translation-board.md |
| **M2 全量翻译**（预计 15~25 个翻译会话，按段数定） | 会话内 agent 分批翻译（fmt DR-012 方式，零 key）：正文 P0 批 → wiki P0 批 → API 注释 → P2 批（含 APIChanges 占位页落地）；每批 validate + 人工抽检 | zh/ 全量 + api/zh + wiki P0/P1 | ① 可译段 100% 覆盖（分母=去重段数，不译/占位段 skipped 豁免，参照 fmt DR-014 口径） ② 术语一致性 ≥99%（glossary v1 冻结后） ③ 代码块/结构完整性 100% ④ 站点内容完整可预览 |
| **M3 CI 增量** | translate-incremental.yml 上线 + 真实 diff 演练（trunk doc/ vs n9.0.2，§4.4） | 自动化增量翻译闭环 | ① 演练增量 sync 检测/标记正确 ② CI 增量翻译仅处理 pending 段 ③ 校验通过自动提交、失败标记复核 ④ Secrets 凭据无泄露（repo 扫描） |
| **M4 发布** | Pages 上线 + mike 版本部署 + 双语对照 + ffmpeg-devel 许可确认邮件（用户主导）+ 季度质量报告 | 正式站点 | ① 线上可达（HTTP 200 实测）+ 版本切换正常 ② DR-006 确认结论回填决策日志 ③ 质量指标达标表落盘 |

### M2 工作量估算（M1 段落切分后校准）

- 正文 292,805 词 ≈ 中文产出 30~35 万汉字（ffmpeg.net.cn 实测 filters 16.4 万汉字、ffmpeg-all 29 万汉字佐证）
- 预估段落 5,000~7,500 段（按 40~60 词/段）；会话内 agent 按 300~500 段/会话 → **约 15~25 个翻译会话**；filters 141,693 词单列约 8~10 个子批（按 chapter 分组）
- 批次计划在 M1 结束时按实际段数写入 `docs/translation-board.md`（fmt 惯例），批次粒度=单会话可完成（约 300~500 段）
- **M2 跨会话纪律（R2 补充）**：每批完成即 git 提交 + 看板勾销 + 交接文档随更新；上下文过半或批次完成即按全局「会话连续性」约定收尾交接，不以"快完了"硬撑新批

---

## 质量校验（DoD 5）

沿用 fmt-zh-docs 全套惯例 + 本工程新增两层校验器：

| 层 | 校验器 | 校验项 |
|---|---|---|
| 转换层（新增） | validate_structure.py | 标题/代码块/列表/表格计数对比、锚点映射完备、include 完备性与手册页无内联（DR-009）、占位符保护、命令示例滤镜名静态校验 |
| 翻译层（fmt 移植） | validate_translation.py | 术语一致性（上下文消歇）、代码块 hash 一致、结构 AST 对比、内联代码未译、链接可解析、占位符还原、中文标点 |
| API 层（新增） | validate_backfill.py | @param 数量/顺序一致、@return/@brief 存在、非注释区零改动 |
| 拆分层（新增） | split_filters 内建校验 | 滤镜页集合 = 整卷小节集合（无丢失/重复） |
| wiki 层（新增） | wiki2md 内建校验 | 宏占位无遗漏、页脚署名块完整、原文版本号记录 |

**质量指标**（quality-metrics.yml）：首轮全量覆盖率 100%（可译段，R3 补充）｜术语一致性 ≥99%｜代码块完整性 100%｜结构完整性 100%｜转换校验器 0 错误｜回填校验器 0 错误｜人工抽检通过率 ≥95%｜增量翻译覆盖率 ≥90%（M3）

**保护机制**：protect_untranslatable 占位符（fmt DR-004 格式 `{{PROTECTED_<TYPE>_<HASH>}}`）前置到转换后、翻译前；命令行示例/选项表/代码块/API 名全保护。

**双语对照**：generate_bilingual.py 悬浮原文 + 独立对照页（fmt DR-005 模式），M4 上线。

---

## 许可与署名（DoD 6）

依 DR-006 落地（全部文件在 M1 建仓时创建）：

1. **LICENSE**（工程代码）：MIT（fmt 惯例；scripts/tests 均为本工程原创）
2. **LICENSE_TRANSLATION.md**（译本声明）：
   - 正文/API 注释译本：基于 FFmpeg n9.0.2 官方文档（官方 .texi 无单独许可声明，按源码树主许可推定 LGPL 2.1+），本译本按 **LGPL-2.1-or-later** 提供；随仓库附 `COPYING.LGPLv2.1` 全文副本；显著标注"译自 FFmpeg n9.0.2 官方文档，并注明翻译状态"
   - wiki 精选页：**CC BY-SA 3.0**，署名 "Contributors to the FFmpeg Community Documentation Wiki"（每页页脚固定块 + wiki 首页集中声明），与 LGPL 译本分区标注不混许可
   - API 译本许可页：列明 libavfilter 40 个 GPL 文件清单与 doc/examples MIT 清单，各文件保留原许可
   - 禁止项声明：不搬运 ffmpeg-web 文案/设计（无许可声明）；doc/t2h.pm、doc/texi2pod.pl 未衍生未修改
   - APIChanges 占位页：标注"英文原文"（fmt DR-014 口径）
3. **COPYING.LGPLv2.1**：FSF 标准全文副本入库
4. **站点页脚**（mkdocs copyright）：`除 wiki 精选页（CC BY-SA 3.0）外，译文基于 FFmpeg 官方文档（LGPL 2.1+）以 LGPL-2.1-or-later 提供 · 译自 n9.0.2`
5. **ffmpeg-devel 确认动作（M4）**：由用户主导向 ffmpeg-devel 邮件列表书面询问官方文档许可意图；结论到达后回填 DR-006（如有变更新开 DR）——这是推定许可的唯一开放项
6. **README 许可章节**：汇总上述声明

---

## 站点发布（DoD 7）

- **引擎**：mkdocs Material（fmt 同款：zh 分词搜索/导航分组/代码复制/深浅色）+ **mike** 版本插件
- **URL 结构**：

```
/latest/                    → 指向当前基线 tag 版本（mike alias）
  manual/{ffmpeg,ffplay,ffprobe,common-options}/   ← DR-009 手册页=独有内容+交叉链接
  components/{utils,scaler,resampler,codecs,bitstream-filters,formats,protocols,devices}/
  filters/{video,audio,multimedia}/<滤镜名>/        ← DR-008 每滤镜一页
  libraries/{libavutil,...}/
  general/{faq,general,platform,developer,git-howto,fate,authors,mailing-list-faq,nut,community,...}/
  api/                       ← Doxygen 中文重建
  wiki/<精选页>/
  bilingual/                 ← 双语对照
  （官方参考外链区：ffmpeg-all.html 等 -all 页与 trac 原文）
/n9.0.2/ /n8.1/ ...         ← mike 版本目录
```

- **版本策略**（轻量决策，随本计划批准）：`latest` alias + 每个翻译基线 tag 一个版本目录；**在线保留最近 2 个 major 线**（约 2 年窗口，FFmpeg major 年更），更早版本打包 GitHub Releases 附件；域名/仓库名沿用 `jxsword.github.io/ffmpeg-zh-docs`（DR-001）
- **部署**：deploy.yml → mike deploy --push → GitHub Pages；badge 对齐 fmt README 惯例

---

## 风险与对策（DoD 8）

| 风险 | 可能性 | 影响 | 对策 |
|---|---|---|---|
| filters.texi 转换/拆页质量（14 万词、variablelist 密集） | 中 | 高 | split_filters + validate_structure 固样单测；每滤镜页集合完备性校验；M1 抽检 20 页 |
| makeinfo/pandoc 版本漂移致转换输出变化 | 中 | 中 | CI 工具链版本锁定比对（§8）；UPSTREAM.json 记录工具版本；转换校验器拦截 |
| CI 环境工具链安装差异（apt 版本与本地不一致） | 中 | 中 | workflow 内安装后立即版本比对（R3 补充）；必要时自建容器镜像固化工具链 |
| 许可推定被官方后续否认（DR-006 开放项） | 低 | 中 | 声明集中在 LICENSE_TRANSLATION.md 单点修改；M4 邮件确认前置化解；最坏情况=改声明不改内容 |
| API 注释回填破坏源码结构 | 中 | 高 | validate_backfill 逐字段校验 + api 翻译在独立分支（api-baseline/n9.0.2）隔离 + git revert 兜底 |
| wiki 页漂移（CC BY-SA 3.0 持续变动） | 中 | 低 | 精选常青页 + 快照版本记录 + 季度 diff 抽查；仅 P0 保证跟随 |
| trac wiki 抓取限流/反爬 | 中 | 低 | 抓取限速（≥2s 间隔）+ 本地缓存 + 快照入库后不再重复抓取（R3 补充） |
| wiki 宏/模板转换损耗 | 中 | 中 | 预处理分级（§3.2）+ 宏占位保护 + 宏密集页降级排除机制（R2/R3 补充） |
| M2 跨会话批次衔接断裂 | 中 | 中 | 批次粒度=单会话可完成 + 每批提交/看板/交接文档三件套（R3 补充） |
| 官方 major 时 filters 大 diff（预期年更） | 高 | 中 | 滤镜级 hash 增量（DR-008）+ L1/L2/L3 分级响应（fmt DR-007 惯例）+ major 冻结冲刺窗口 |
| LLM 术语漂移/成本 | 中 | 中 | glossary 注入 prompt + CI 强制校验 + TM 复用（fmt DR-006 惯例）；M3 flash 档 + 日/月预算告警 |
| 长任务内存失控（fmt OOM 事故教训） | 低 | 高 | 一律 memgate 包裹（DR-011 纪律）+ earlyoom 常驻 |
| git.ffmpeg.org 直连超时 | 中 | 低 | sync 走 GitHub 镜像（HEAD 与官方一致，S2 实测）；代理回退纪律 |
| GitHub Pages 国内可达性波动 | 低 | 低 | fmt-zh-docs 同构已实测可达；必要时补国内镜像（后议） |
| 单人维护可持续性（xdsnet 教训） | 中 | 中 | CONTRIBUTING 协作规范 + 翻译看板 + 增量机制降低维护边际成本 |

---

## 执行顺序与依赖（DoD 9）

```
[计划批准] ← 当前节点（批准前零实施）
   ↓
① git init + 首提交（docs/research/PLAN）+ gh repo create + 目录骨架 + LICENSE 系列 + CONTRIBUTING/AUTHORS 骨架
   ↓（并行：②③）
② scripts/texi2md.py + validate_structure.py（依赖：本地 ./configure 补 config.texi）
③ scripts/split_filters.py（依赖：② 的 filters.md 产出）
   ↓
④ sync_docs.py --tag n9.0.2 全量转换 → source/ 入库 → 段落切分与批次计划（translation-board）
   ↓
⑤ mkdocs 骨架 + CI 四条 workflow + glossary/style 初版 + wiki 预处理分级预检 → M1 验收
   ↓
⑥ M2 分批翻译（正文 P0 → wiki P0 → API 注释 → P2；每批 validate+提交，跨会话接续按交接纪律）
   ↓
⑦ M3 translate-incremental.yml（依赖：M2 管线稳定 + NVIDIA_API_KEY Secrets 配置 + trunk diff 演练）
   ↓
⑧ M4 Pages/mike 发布 + ffmpeg-devel 确认 + 质量报告
```

依赖要点：② 阻塞 ③④；M2 各批内互相独立；M3 依赖 M2 的 state 结构与校验器稳定；M4 依赖 M3 增量演练通过。

### 启动清单（批准后 M1 第一步）

```bash
cd /home/ssy/soft-tech-docs-translate/ffmpeg-zh-docs
git init && git add docs/ research/ PLAN.md && git commit -m "docs: planning artifacts (DR-001~009, research, plan)"
gh repo create jxsword/ffmpeg-zh-docs --public --source . --push   # DR-001
# 随后按第 7.1 节结构落 scripts/config/tests 骨架 → M1 任务单
```

---

## 三轮复审修订记录（v1 → v2）

**R1 完整性与一致性复审**：
1. 移除"-all 拼接视图"——与 DR-008"大单页劣化"论证自相矛盾（29 万词单页 > filters 16 万汉字单页）；改为组件页 + 官方 -all 外链
2. 手册页 include 处理缺失 → 新增 **DR-009**（手册页=独有内容+组件交叉链接）
3. fftools-common-opts/authors.texi 归属缺失 → 独立页 /manual/common-options/、/general/authors/
4. wiki P0/P1 清单计数修正（实际 P0=32、P1=27，与正文一致）
5. APIChanges 处置明确：默认英文占位页（fmt DR-014 口径）
6. M1 会话估算 2~3 → 3~5（含 configure 生成物、拆页器、CI 等 heavier 工作量）

**R2 技术可行性细化复审**：
1. config.texi 生成具体化：`./configure`（不 make）即产出；avoptions_*.texi 实测无引用、无需生成
2. 锚点 slugify 具体化：mkdocs `toc.slugify: python-markdown-nonorm`（保留大小写）+ anchor_map 双向映射
3. wiki 预处理分级：纯文本直译 / 宏密集页占位保护 / 宏占比过高页降级排除
4. sync 检测逻辑具体化：ls-remote 过滤 -dev + annotated tag 日期校验（S2 同款方法）；M3 演练改用 trunk doc/ 真实 diff
5. 命令示例校验显式化：滤镜名静态清单校验 + 明确"不做运行时执行验证"及理由（fmt DR-009 编译验证不适用的差异确认）
6. M2 跨会话纪律显式化（每批提交+看板+交接三件套）
7. codecs/formats 拆分预案登记（不实施，天然 include 缝合线备用）

**R3 风险/合规/终审复审**：
1. 风险表 +4 项：CI 工具链安装差异、trac 限流、wiki 宏损耗、M2 跨会话衔接
2. 质量指标补"首轮全量覆盖率 100%（可译段）"；校验层表补 wiki 层
3. 术语表种子明确化（muxer=复用器/demuxer=解复用器等 12 条基线；xdsnet 语料降为参考；v1 冻结点=B1 批后）
4. DoD 9 项对照表加入目录区（1→§3 … 9→§15）
5. 启动清单/M1 交付物补 CONTRIBUTING/AUTHORS 骨架；CI 工具链版本锁定比对机制落 §8

---

## 待用户批准事项

1. ~~本计划 v2 整体~~ → **已于 2026-11-19 获用户批准**（含 DR-009 手册页结构、wiki P0/P1 初选清单、-all 不构建、APIChanges 英文占位、版本保留策略）
2. 批准后按"启动清单"开始 M1（新会话执行）
