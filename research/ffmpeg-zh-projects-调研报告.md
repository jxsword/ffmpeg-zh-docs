# FFmpeg 中文翻译项目调研报告（合并版）

> 落盘：2026-11-19｜合并自：S1《ffmpeg-zh-projects-候选搜索与分析.md》+ S2《ffmpeg-doc-体系与许可调研.md》
> 依据：`research/ffmpeg-zh-projects-调研大纲.md` v3 第 5 节；上游决策 DR-001~005
> 本报告为结论级合并；对象条目全量细节、命令出处见两份子报告。所有 URL 与数字均实测（2026-11-19，直连为主，失败处按纪律经代理重试）。

---

## 1. 调研概要

- **目标**：摸清全网已有 FFmpeg 官方文档中文翻译项目（借鉴/复用输入）；核实 FFmpeg 文档体系与许可条款（量化与合规输入）。
- **方法**：S1 全网搜索（GitHub/Gitee/GitCode/awesome/trac wiki/社区文章，7 候选 + 11 排除 + 1 机制参照）；S2 源码树级核实（n9.0.2 浅克隆 + ffmpeg-web 克隆 + trac/官网 curl）。
- **渠道结论（S1）**：GitHub 是唯一有效发现渠道；Gitee 搜索 API 应用层空结果、GitCode 无相关项目、awesome-ffmpeg（⭐1203）未收录任何中文翻译项目、trac wiki 约 290 页零命中——中文项目分散且无聚合入口。

## 2. 对象条目与优缺点（三件套模板，浓缩自 S1）

### 2.1 存活候选

#### here200/ffmpeg-doc-zh
- 官网/站点: https://here200.github.io/ffmpeg-doc-zh/ （核实: 2026-11-19 直连+代理均 200 可达）
- 官方文档/README: https://github.com/here200/ffmpeg-doc-zh#readme （核实: 2026-11-19 gh api 可达）
- 源码: https://github.com/here200/ffmpeg-doc-zh （核实: 2026-11-19 gh api 可达）
- 简介: 2026-09 的个人项目，以官方 makeinfo HTML 为底本做**同构副本式翻译**（HTML 结构不变仅换文本），18 个 `*-zh.html` 页发布于 GitHub Pages；DeepSeek + PowerShell 校验脚本链；基线 gyan.dev 2026-09-10 git 快照。
- 优点: ①同构副本法保锚点/目录/交叉引用完好；②成体系翻译工程资产——翻译说明（范围/不译清单/术语标准/校验记录四段式）、`term_pairs.json` 术语表、`split_plan.json` 分批计划、结构校验脚本；③覆盖官网 25 个核心文档页中的 18 页；④抽样质量高（5 页仅 2 处合理英文残留）；⑤底本新。
- 缺点: ①单人单发（star 0/ contributor 1），2026-09-18 后停更；②缺 7 个 libav* 库页与 -all 合集页；③无 wiki/API/Doxygen；④仓库无 LICENSE、无译作许可声明；⑤单版本快照无增量同步；⑥PowerShell 链不利于跨平台复用。
- 适用场景: 翻译说明/术语表/分批计划的模板来源；同构副本法与结构校验思路参考；质量对照样本。
- 存活判定: 最后提交 2026-09-18（gh api）→ 存活候选（单发性质）
- 保留/放弃判定与理由: **保留（机制与资产借鉴源，非内容基底）**——唯一开源可查证的现存官方文档整册中文翻译。

#### ffmpeg.net.cn
- 官网/站点: https://ffmpeg.net.cn/ （核实: 2026-11-19 直连 200/0.6s、代理 200/0.32s）
- 官方文档/README: 无独立说明页；`about.html`/`legal.html` 为官方对应页翻译（核实: 2026-11-19 直连 200）
- 源码: **未发现公开源码仓**（多路搜索无果，页面无仓库链接）——不可引用，仅记录
- 简介: ffmpeg.org 官网 1:1 中文翻译站，Wayback 最早快照 2017-05-16，运营 ≥9 年；覆盖官网整站 + 文档导航全部 25 个核心文档页（texi→makeinfo 重生成后汉化，页脚自述 makeinfo 2025-01-21 生成）+ 多版本 Doxygen 英文镜像（trunk + 33 历史版本）。基线 FFmpeg 7.1（2024-09 新闻）。
- 优点: ①覆盖面全网第一（25/25 文档页 + 整站）；②makeinfo 同源重生成路线，全文中文、选项/代码保留英文；③站点稳定、国内可达性极佳；④Doxygen 多版本目录布局（doxygen/<version>/）可参考。
- 缺点: ①无开源仓——成果/流水线不可复用、不可协作；②基线停在 7.1，滞后上游约 1 年+，无增量同步证据；③许可合规未声明；④旧新闻段落英文残留；⑤维护者署名"林建有"仅见搜索引擎摘要（存疑，不作结论）。
- 适用场景: 信息架构与 sitemap 对照清单；"整站 1:1 翻译可长期运营"的可行性佐证；Doxygen 多版本站点组织参考。
- 存活判定: 站点 last-modified 2025-08-11（HTTP header）+ Wayback 2026-08-23 快照 → 存活候选（更新停滞）
- 保留/放弃判定与理由: **保留（对标样板，非可复用资产）**——以其"无源码、无增量、无合规、无协作"四大缺口为本工程差异化空间。

### 2.2 历史参照（仅记录）

| 项目 | 数据（gh api 实测） | 借鉴点/教训 |
|---|---|---|
| xdsnet/other-doc-cn-ffmpeg | created 2015-06、pushed 2021-01-26、⭐230、forks 71、license null；站点 https://xdsnet.github.io/other-doc-cn-ffmpeg/ 直连可达 | ffmpeg-all→44 章分章 md 粒度参考；"分离器/混合器/滤镜链图"等术语语料；教训：一次性全册翻译无维护注定过时 |
| wdk-docs/ffmpeg-docs | created 2019-06、pushed 2019-12-28、⭐0 | Sphinx 路线先例；弃用（texi 解析成本高于 md+mkdocs，与 DR-003 一致） |
| apachecn/ffmpeg-doc-zh | 2022-06 建仓仅模板占位，无实际内容 | 佐证大型翻译组织也未落地 FFmpeg 官方文档翻译 |
| easyhao007/ffmpeg-all-cn | xdsnet 的 fork（2017） | 排除（非独立项目） |

### 2.3 机制参照（非中文，1 个）

#### ayosec/ffmpeg-filters-docs
- 官网/站点: https://ayosec.github.io/ffmpeg-filters-docs/ （核实: 2026-11-19 直连+代理可达）
- 官方文档/README: https://github.com/ayosec/ffmpeg-filters-docs#readme （核实: 2026-11-19 gh api 可达）
- 源码: https://github.com/ayosec/ffmpeg-filters-docs （核实: 2026-11-19 gh api 可达；license Apache-2.0）
- 简介: 英文项目，把官方 filters 文档自动重排为"每滤镜一页"站点（按 Audio/Sources 等自动分组 + 全站搜索）；2026-08-30 仍在推送（跟随上游）。
- 优点: 自动化分组/建页机制成熟；每滤镜一页导航体验显著优于官方单页；许可清晰。
- 缺点: 仅覆盖 filters；英文；未处理文档再分发许可声明细节。
- 适用场景: filters 卷站点结构设计参考。
- 存活判定: 最后提交 2026-08-30 → 存活（参照对象）
- 保留/放弃判定与理由: **保留为机制参照**——"从官方文档源自动生成 per-filter 页"的分组推断逻辑可平移。

## 3. 选择策略矩阵

| 维度 | here200/ffmpeg-doc-zh | ffmpeg.net.cn | xdsnet（历史） | ayosec（机制参照） | 本工程 ffmpeg-zh-docs |
|---|---|---|---|---|---|
| 开源可复用 | 全仓公开 | 无源码 | 公开 | 公开（Apache-2.0） | 是 |
| 覆盖面 | 18/25 页，缺 libav* | 25/25 + 整站 + 英文 Doxygen 镜像 | ffmpeg-all 全册（4.x 基线） | 仅 filters | 全类别：正文+wiki 精选+API 注释翻译 |
| 基线新鲜度 | 2026-09（新） | 7.1 时代（滞后 1 年+） | ~4.3/4.4（滞后 5 年） | 跟随上游 | 最新稳定 release（n9.0.2）+增量跟随 |
| 增量机制 | 无 | 无 | 无 | 有（上游跟随） | 自动化增量流水线（核心差异） |
| 许可合规 | 无声明 | 无声明 | 无声明 | 仅仓库许可 | 立项明确（待 DR-006） |
| API/Doxygen | 无 | 英文镜像未译 | 无 | 无 | 注释翻译+Doxygen 重建（中文首例） |
| 站点/载体 | HTML 同构副本+Jekyll | makeinfo HTML+nginx | md+GitBook | HTML 站点 | texi→md+mkdocs Material（DR-003） |
| 国内可达性 | 直连+代理均 200 | 直连+代理均 200（0.3s 级） | 直连+代理均 200 | 直连+代理均 200 | GitHub Pages（fmt-zh-docs 同构已验证） |

**按场景的选择结论**：
- **谁能直接用**：无——没有任何候选可直接作为内容基底（here200 覆盖不全且停更；ffmpeg.net.cn 无源码；xdsnet 基线过老）。
- **谁可借鉴什么**：here200 → 翻译工程资产（翻译说明模板/术语表种子/分批计划/结构校验思想）；ffmpeg.net.cn → 25/25 sitemap 对照、makeinfo 重生成路线佐证、Doxygen 多版本 URL 布局；ayosec → 每滤镜一页自动分组机制；xdsnet → 章节粒度与历史术语语料。
- **我们为何自建**：全体候选共同缺口 = 无增量同步 + 无开源协作 + 无合规声明 + 无 API 翻译；本工程 DR-001~005 的定位（开源+增量+全类别+合规+API 中文首例）恰好逐一补位，且现有候选均无跟随上游 release 节奏的能力（S2 实测 major 约年更、point 成批）。

## 4. 组件级借鉴清单

| 来源 | 组件 | 本工程用法 |
|---|---|---|
| here200 | `ffmpeg-zh-翻译说明.md`（范围/不译清单/术语标准/校验记录四段式） | 作为 `config/style-guide.md` 与翻译说明的结构模板 |
| here200 | `term_pairs.json` 术语表 | 校订后作 `config/glossary.yml` 种子 |
| here200 | `split_plan.json` 分批计划 | 迁移为 mkdocs 章节切分的批次计划模式 |
| here200 | verify/audit/remank PowerShell 校验链 | 思想下沉为 Python 结构保持校验器（AST 对比） |
| here200 | "同构副本"（结构不动只换文本）思想 | 转换校验器的"结构保真"设计原则 |
| ffmpeg.net.cn | 25/25 文档页 1:1 sitemap | 范围映射对照清单（DoD #1） |
| ffmpeg.net.cn | `doxygen/<version>/` URL 布局 | API 中文重建的站点 URL 结构 |
| ffmpeg.net.cn | makeinfo 重生成+汉化可运营 9 年 | DR-003 路线可行性佐证 |
| ayosec | 每滤镜一页 + 自动分组 + 站内搜索 | filters 卷站点结构候选方案（待决策） |
| xdsnet | 44 章分章粒度；"分离器/混合器"等译名 | 翻译单元粒度参考；术语对齐参考语料 |
| xdsnet（教训） | 一次性翻译无维护 | 论证增量机制（DR-002/003）必要性 |

## 5. FFmpeg 文档体系与许可核实结论（佐证对象，浓缩自 S2）

### 5.1 基线与节奏

- **当前最新稳定 tag：n9.0.2**（2026-09-18，annotated tag 实测；FFmpeg 无 GitHub Releases，仅 tag）。
- major 间隔近 3 次：403/504/346 天（均值 **约 13.7 个月**）；x.1 约在 major 后半年；point 成批集中在 5-6 月与 11 月维护窗口；旧线（n6.1/n7.1）在 n9.0 后仍获 point 维护 1~2 年。
- 官网 documentation.html 为 **trunk nightly 每夜重生成**（页面原文），与 release 不同步——按 DR-002 取 release 基线需自建文档构建。

### 5.2 文档体量（n9.0.2 实测）

- doc/ 下 48 个 .texi；剔除 11 个 @include 纯外壳后**去重正文 37 个文件 = 2,007,698 B ≈ 1960.6 KB / 67,133 行 / 292,805 词**。
- **filters.texi 单文件占正文 47%**（949,519 B / 141,693 词）——核心单体，必须分片/分批。
- 次大件：muxers.texi 138KB/20,436 词、ffmpeg.texi 136KB/18,303 词、encoders.texi 136KB/19,808 词、protocols.texi 75KB/11,318 词。
- 构建期生成物（源码树无）：doc/config.texi（configure 生成）、doc/avoptions_*.texi（print_options 从二进制抽取）——译前需本地 configure 补齐或占位。
- 工作量参照：ffmpeg.net.cn 实测 filters 单页 16.4 万汉字、ffmpeg-all 29 万汉字量级 → 本工程全量中文产出约 **30~35 万汉字**。

### 5.3 体系映射（官网 documentation.html → 源）

| 官网类别 | 源（n9.0.2） |
|---|---|
| Command Line Tools（ffmpeg/ffplay/ffprobe ± -all） | 3 个主 texi，各 @include 13 个共享件 |
| Components（9 页） | 9 个 ffmpeg-*.texi 外壳 → utils/scaler/resampler/codecs(→decoders+encoders)/bitstream_filters/formats(→demuxers+muxers+metadata)/protocols/devices(→indevs+outdevs)/filters |
| Libraries（7 页） | 7 个 libav*.texi 短页（正文主体在 Doxygen） |
| General（FAQ/General/Platform/Developer/Git/FATE） | faq/general_contents/platform/developer/git-howto/fate.texi（另有 mailing-list-faq/nut/community/drawvg-reference 可构建） |
| API Documentation | Doxyfile + 库源码注释（官网 trunk nightly） |
| Community Contributed（wiki + Books） | trac wiki（CC BY-SA 3.0） |

### 5.4 许可矩阵（关键合规输入）

| 语料 | 许可 | 依据强度 |
|---|---|---|
| doc/*.texi 正文 | **无自身声明**（全树 grep 0 命中 GFDL/@copying）；按源码树主许可**推定 LGPL 2.1+**（LICENSE.md "Most files…In combination the LGPL v2.1+ applies"） | 推定（**最大合规不确定点**） |
| 官网 ffmpeg-web 页面/文案 | **未声明**（仓库无任何许可文件） | 事实 |
| trac wiki 社区文档 | **CC BY-SA 3.0**，署名 "Contributors to the FFmpeg Community Documentation Wiki" | WikiStart 原文明示 |
| API 注释（Doxygen） | **随源码文件许可**：LGPL 2.1+ 为主（libavcodec 1695/libavformat 690 个标准头），libavfilter 40 个文件 GPL，doc/examples 24 个 .c MIT | 逐文件头实测 |
| doc/t2h.pm、doc/texi2pod.pl | **GPL（严禁衍生）** | LICENSE.md 明列 |

**注意（S1/S2 矛盾裁决）**：S1 转述 here200 README 称官方文档为 "CC-BY-SA 3.0 + GFDL 1.3 双许可"——与 S2 对 n9.0.2 全树的直接实测矛盾（0 命中），**以 S2 实测为准**；here200 的说法为其自述/第三方理解，未经源码证实。wiki 部分的 CC BY-SA 3.0 为 S2 实测确证。

### 5.5 构建链实测（对本工程的可行性输入）

- configure 要求：makeinfo 存在即可出 info/txt；**texinfo 主版本 ≥5 才启用 HTML**（configure:7621-7625）。本机 texinfo 7.2（S2 为测试安装）、doxygen 1.15.0——均满足。
- **转换链冒烟测试（2026-11-19，本会话）**：`makeinfo --docbook`（真实文件 utils.texi/metadata.texi）→ `pandoc 3.7.0.2 -f docbook -t gfm` 开箱可用：标题层级完整、variablelist 项值对保留、代码为缩进块；已知需后处理：①texinfo 弯引号 `‘’` 残留清理；②项/值对结构化；③缩进代码→fenced；④锚点映射需自建（DocBook XML 不含官方 HTML 锚点）。环境变更披露：本机新装 pandoc（apt），S2 装有 texinfo。

## 6. 对 ffmpeg-zh-docs 的差异化定位

1. **四大缺口补位**：全网候选皆缺"增量同步 / 开源协作 / 合规声明 / API 翻译"——本工程以 DR-001~005 定位逐一补位；API 注释翻译+Doxygen 中文重建将是**中文首例**。
2. **基线差异化**：唯一以最新稳定 release（n9.0.2）为基线并跟随 release 节奏（约年更 major + 半年 minor + point 批次）的中文翻译项目。
3. **规模定位**：正文 37 文件 29.3 万词（filters 47%）+ wiki 精选 + API 注释——参照 ffmpeg.net.cn 16.4 万汉字 filters 单页先例，规模可行；filters.texi 的分片策略是工程核心难点（待计划决策）。
4. **合规定位**：唯一处理译作许可声明的中文项目（LGPL 2.1+ 推定 + wiki CC BY-SA 3.0 分离标注 + t2h.pm 禁衍生），许可策略待 DR-006 用户决策。
5. **对翻译计划的输入要点**：①范围映射以 S2 §5.3 表 + ffmpeg.net.cn 25/25 sitemap 为对照；②工作量按 §5.2 体量表估算、filters 单列分批；③许可按 §5.4 矩阵；④wiki 精选清单按 DR-004 于计划中提出（约 290 页内容页中初选 30~40 页常青页）；⑤转换管线以 §5.5 实测链路为基线。

---

*查证日期：2026-11-19（S1/S2 全部实测；本会话补充 pandoc 冒烟测试）。通道：直连为主，直连失败处经代理 http://192.168.33.1:10808 重试一次后下结论；数字出处见两份子报告对应条目。*
