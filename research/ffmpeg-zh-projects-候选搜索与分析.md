# FFmpeg 官方文档中文翻译项目候选搜索与分析（子任务 S1）

> 落盘：2026-11-19｜执行：调研子代理 S1（会话内执行）
> 任务：全网搜索并深度分析"FFmpeg 官方文档中文翻译项目"候选，为 ffmpeg-zh-docs 翻译计划提供借鉴输入。
> 网络通道声明（对齐网络访问回退纪律）：所有可达性结论以 curl/gh api 实测为准（直连为主，直连失败处按纪律经代理 `http://192.168.33.1:10808` 重试一次后下结论）；WebSearch/WebFetch 结果仅作发现渠道。查证日期均为 2026-11-19。star/fork/提交时间等数字出处均为 `gh api`（GitHub REST API）实测输出。

---

## 1. 搜索过程记录（入口、关键词、命中路径）

### 1.1 入口一：GitHub（gh CLI，账号 jxsword）

`gh search repos` 逐组检索（默认搜索 name/description/readme）：

| 关键词 | 命中情况 |
|---|---|
| `ffmpeg 中文文档` / `ffmpeg 中文手册` / `ffmpeg 中文版` / `ffmpeg documentation 中文` / `ffmpeg文档` | 仅零散无关项目（GUI 工具、AI 视频流水线等） |
| `ffmpeg 手册 in:readme` | 无文档翻译项目；干扰项 `feixiao/learn-ffmpeg`（⭐765 学习资料）、`0voice/ffmpeg_develop_doc`（⭐2188 资源合集） |
| `ffmpeg documentation translation in:readme` | 均为无关大项目（HandBrake/jellyfin 等） |
| `ffmpeg-doc` / `ffmpeg-docs` / `ffmpeg-zh` / `ffmpeg-cn` | **`xdsnet/other-doc-cn-ffmpeg`（⭐230）**、**`here200/ffmpeg-doc-zh`**、`wdk-docs/ffmpeg-docs`、`apachecn/ffmpeg-doc-zh`、`apachecn-archive/ffmpeg-doc-zh`、`FiveYellowMice/how-to-convert-videos-with-ffmpeg-zh`（⭐274 教程翻译）、`huwan/FFmpeg-Tutorial-CN`（⭐298 教程翻译）、`chinanf-boy/ffmpeg-concat-zh`（工具 README 翻译）、`bayshier/ffmpeg-skill-zh`（Agent skill 汉化）、`cicbyte/ffmpeg-sheet-content`（速查表） |
| `ffprobe 中文` / `ffplay 中文` / `ffmpeg filters 翻译` / `ffmpeg-utils 中文` / `ffmpeg 文档翻译` / `ffmpeg manual chinese` 等 | 仅复现上述已知项目 |
| `--topic=ffmpeg --topic=chinese` / `--topic=translation` | 无文档翻译项目（字幕/配音/短视频工具为主） |
| `gh search code`（"ffmpeg 官方文档 中文翻译"等中文短语） | 0 命中（GitHub 代码检索对中文短语分词几乎无效，仅作排除证据） |

**关键命中路径**：`ffmpeg-zh` 组 → `here200/ffmpeg-doc-zh`（描述"ffmpeg官方文档中文翻译"）；`ffmpeg-cn` 组 → `xdsnet/other-doc-cn-ffmpeg`（描述"一些文档翻译项目"）。

### 1.2 入口二：Gitee / GitCode

- **Gitee API** `api/v5/search/repositories?q=...`：对 `ffmpeg`、`ffmpeg 中文`、`ffmpeg-doc` 等全部返回 `[]`（HTTP 200，应用层空结果；直连与参数组合均无效）→ Gitee 搜索 API 当前不可用（仅代表本机实测）。
- **Gitee 网页搜索**：返回 849 字节 JS 壳（`Gitee Search`），结果前端渲染，无法抓取。
- **Gitee 直探已知线索**：`gitee.com/easyhao007/ffmpeg-all-cn`（WebSearch 报告存在）→ **404 不可达**；`gitee.com/xdsnet/other-doc-cn-ffmpeg` → 404；`gitee.com/Maicss/ffmpeg`（"ffmpeg中文版"）→ 200 但为源码仓库（C/GPL），非文档翻译。
- **GitCode**：搜索页重定向至 AtomGit Search（HTTP 200，136KB SSR 数据），解析结果均为视频转码 GUI/音频工具，无文档翻译项目。

### 1.3 入口三：awesome 聚合清单

- `transitive-bullshit/awesome-ffmpeg`（⭐1203，gh api 实测）：README 中 grep `chinese|中文|translat|zh|cn` 零命中 → 主流聚合清单未收录任何中文文档翻译项目。
- 其余同名清单（awelist、MarceauKa、runningcheese 等）未检出翻译类条目。

### 1.4 入口四：FFmpeg trac wiki

- `https://trac.ffmpeg.org/wiki/TitleIndex` 实测共 **296 个 wiki 页**，grep 翻译相关（trans/chinese/zh/i18n/local）仅命中 2 个无关页（`Chinese_Font_中文版本`、`Chinese_Font_从视频中每X秒创建一个缩略图`，均为字幕字体主题）。
- 直接探测 `TranslationToChinese` / `ChineseTranslation` / `Translation` / `AboutChineseDoc` → 全部 404。
- **结论：官方 trac wiki 上没有任何"文档翻译项目"索引页**（与 S2 任务"官方无中文版"结论互证）。

### 1.5 入口五：中文社区文章（仅作发现渠道）

- BookStack 书栈网：托管《ffmpeg 翻译文档(ffmpeg中文文档)》，源即 **xdsnet/other-doc-cn-ffmpeg** 的章节 md（URL 实测 200）。全网流传的"502 页 ffmpeg 翻译文档.pdf"（quarkbook.com / CSDN gitblog 转载）均为该项目的 PDF 派生物。
- OSCHINA"FFmpeg 中文文档学习指南"等文章：只提及 GitHub 上上述已知项目与教程系列，无新项目线索。
- CSDN gitblog_09796/142890268：《FFmpeg 使用手册中文翻译》PDF 转载页（页面反爬未能提取 github 链接；按 PDF 名与页数判断为 xdsnet 派生物）。

### 1.6 补充发现：独立中文站点与域名探测

- **`ffmpeg.net.cn`**（域名探测命中，WebSearch 复核）：ffmpeg.org 官网的中文翻译站，且文档导航覆盖全部官方文档页——本次调研最重要的补充发现（详见深度分析）。
- 域名探测：`ffmpeg.org.cn`（DNS 解析超时）、`ffmpeg.com.cn`（连接超时）、`ffmpeg.net.cn`（200 命中）、`ffmpeg.cc`（无关的客户端媒体处理工具）、`ffmpeg.xyz`（无内容）。
- 关联站点：`gnu.net.cn`（GNU 官网中文版，内容跟踪 gnu.org 当前筹款活动）——ffmpeg.net.cn 的文档页脚链接指向 gnu.net.cn，推测为同一维护者的"官网翻译"系列站点。
- 日文翻译站 `ffmpeg.poyotan.jp`（训练记忆线索）：DNS 解析失败，站点已死，未纳入。

---

## 2. 候选总表

| # | 项目/站点 | 平台 | 最后提交/更新（实测出处） | 存活判定（≤24个月=存活） | 一句话简介 | 深度分析 |
|---|---|---|---|---|---|---|
| 1 | **here200/ffmpeg-doc-zh** | GitHub | 2026-09-18（gh api `pushed_at`） | **存活候选** | 官方 18 个文档页 HTML"同构副本"式中文翻译，DeepSeek+脚本流水线，GitHub Pages 在线 | **是** |
| 2 | **ffmpeg.net.cn** | 独立站 | 站点 last-modified 2025-08-11（HTTP header）；文档页脚 makeinfo 生成于 2025-01-21 | **存活候选** | ffmpeg.org 官网整站+全部 texi 文档页 1:1 中文翻译站（2017 年起持续存在，无公开源码仓） | **是** |
| 3 | xdsnet/other-doc-cn-ffmpeg | GitHub | 2021-01-26（gh api） | 历史参照 | ffmpeg-all 全册 44 章分章中文翻译（GitBook），中文区历史影响力最大的官方文档翻译 | 否（模板记录） |
| 4 | wdk-docs/ffmpeg-docs | GitHub | 2019-12-28（gh api） | 历史参照 | Sphinx 构建的官网框架+组件文档翻译，规模小 | 否（模板记录） |
| 5 | apachecn/ffmpeg-doc-zh（及 apachecn-archive 副本） | GitHub | 2022-06-02 / 2023-05-03（gh api） | 历史参照（占位仓库） | ApacheCN 模板占位仓库，README 为未填充模板，**无实际翻译内容** | 否（排除性记录） |
| 6 | easyhao007/ffmpeg-all-cn | GitHub | 2017-06-09（gh api） | 历史参照（fork） | xdsnet 项目的 fork，非独立项目；其同名 Gitee 仓库已 404 | 否 |
| 7 | ayosec/ffmpeg-filters-docs | GitHub | 2026-08-30（gh api） | 参照对象（英文，机制突出） | 从官方 filters 文档自动生成"每滤镜一页"重排版英文站（Apache-2.0） | 是（机制借鉴，简析） |

**排除对象记录**（不满足"以官方文档为底本的整站/整册翻译"判定标准，仅登记备查）：

| 对象 | 性质 | 数据（gh api 实测） |
|---|---|---|
| huwan/FFmpeg-Tutorial-CN（⭐298，2026-11-04） | dranger tutorial 教程翻译，非官方文档 | 最后提交未逐项核 |
| FiveYellowMice/how-to-convert-videos-with-ffmpeg-zh（⭐274，2026-11-03） | 外部入门教程翻译 | 同上 |
| 0voice/ffmpeg_develop_doc（⭐2188，2026-11-12） | 学习资料合集（内含 xdsnet 派生 PDF） | 同上 |
| feixiao/learn-ffmpeg（⭐765，2026-11-08） | 学习笔记/资料 | 同上 |
| cicbyte/ffmpeg-sheet-content（2026-07-16） | 命令速查文档，非官方底本 | 同上 |
| bayshier/ffmpeg-skill-zh（2026-10-25） | Agent skill 汉化，非文档 | 同上 |
| MUMEI-NON906/FfmpegUnityDocs（2025-10-09） | Unity 插件文档，非官方 FFmpeg 文档 | 同上 |
| bookstack.cn《ffmpeg 翻译文档》/ quarkbook 502 页 PDF / CSDN 转载 PDF | xdsnet 项目的托管页与 PDF 派生物（bookstack URL 直连 200；quarkbook PDF HEAD 200） | 见 1.5 |
| ffmpeg.poyotan.jp（日文） | DNS 解析失败，站点已死 | 2026-11-19 直连 |
| gitee.com/easyhao007/ffmpeg-all-cn | 404，已删除/不可达 | 2026-11-19 直连 |

---

## 3. 存活候选深度分析

### here200/ffmpeg-doc-zh

- 官网/站点: https://here200.github.io/ffmpeg-doc-zh/ （核实: 2026-11-19 直连 200/0.75s；代理 200/1.33s，均可达）
- 官方文档/README: https://github.com/here200/ffmpeg-doc-zh#readme （核实: 2026-11-19 gh api 200 可达）
- 源码: https://github.com/here200/ffmpeg-doc-zh （核实: 2026-11-19 gh api 200 可达）
- 简介: 2026 年 9 月创建的个人项目，定位"ffmpeg 官方文档中文翻译"。以官方 `makeinfo` 生成的 HTML 文档为底本做**同构副本式翻译**（HTML 结构逐标签不变、仅替换可见文本），产出 18 个 `*-zh.html` 页面经 Jekyll/GitHub Pages 在线发布；自述基于 DeepSeek + harness 完成翻译，附 PowerShell 校验脚本与术语表。基线为 gyan.dev 2026-09-10 git 快照构建（README 自述）。
- 优点: ①"同构副本"翻译法保证锚点/目录/交叉引用完好，可直接替换原文件使用；②有成体系的翻译工程资产——`_guide/ffmpeg-zh-翻译说明.md`（翻译范围、明确"不译清单"、术语标准、校验结果）、`term_pairs.json` 术语表、`split_plan.json` 分批计划、`verify_doc.ps1` 等结构校验脚本；③覆盖了官方文档导航页上的 CLI 手册+组件文档+网页文档共 18 页；④抽样质量高（codecs/protocols/faq/developer/general 五页长段仅 2 处纯英文残留，均为命令示例与取值列表，属合理保留）；⑤底本版本新（2026-09 git 快照）。
- 缺点: ①单人单发（contributor=1，star=0，fork=0，无社区），2026-09-18 后无更新；②缺 7 个 `libav*` 库页（libavutil/libswscale/libswresample/libavcodec/libavformat/libavdevice/libavfilter）与全部 `-all` 合集页；③无 FAQ 之外的 wiki、无 Doxygen/API；④仓库无 LICENSE/许可声明（官方文档 CC-BY-SA 3.0+GFDL 的合规义务未处理）；⑤单版本快照，无上游同步机制；⑥PowerShell 脚本链不利于跨平台复用。
- 适用场景: ①作为"翻译说明/术语表/不译清单"的直接模板来源；②作为同构副本翻译法与结构校验思路的参考实现；③其 18 页译文可作质量对照样本。
- 存活判定: 最后提交 2026-09-18 → 存活候选（但为单发性质，活跃度极低）
- 保留/放弃判定与理由: **保留（作为机制与资产借鉴源，非内容复用源）**。理由：它是目前唯一开源、可查证的"官方文档整册中文翻译"现存项目，其翻译工程资产（术语表、不译清单、校验脚本）对本计划的流水线设计有直接组件级价值；但其内容覆盖不全且无维护，不宜作为内容基底。

**维度①~⑩补充小节**

① **活跃度**（gh api 实测）：created 2026-09-12、pushed 2026-09-18、stargazers 0、forks 0、contributors 1。约 6 天内完成的一批发布，此后无活动。
② **覆盖范围**：`zh-cn/` 下 18 个译文页 = 12 个 texi 组件文档（ffmpeg/ffplay/ffprobe/utils/scaler/resampler/codecs/bitstream-filters/formats/protocols/devices/filters）+ 6 个网页文档（faq/general/platform/developer/git-howto/fate）；基线 gyan.dev git 2026-09-10（README 自述）；`_guide/ffmpeg-zh-翻译说明.md` 自述 ffmpeg.html 底本为 Texinfo 6.7 生成（2719 行），并提示官方已有 Texinfo 7.2 生成的 4001 行新版需重新翻译/核对。对应官网文档导航 25 个核心文档中的 18 个，缺 7 个 `libav*` 库页。
③ **翻译完整性与质量口碑**：抽样 5 页中文密度 14%~52%（codecs 31%/protocols 40%/faq 35%/developer 52%/general 14%，general 偏低系外部库表格页特性）；长段纯英文残留仅 2 处（命令示例、取值列表）。无社区口碑数据（star 0）。翻译说明自述"命令、代码、图解不翻译"纪律并全篇列出。
④ **上游对齐与增量机制**：无上游变更监测、无自动同步；翻译按 `split_plan.json` 分批（batch1 已见），校验靠 `_guide/verify_*.ps1`、`audit_chunks.ps1`、`remap_chunks.ps1` 等脚本人工触发。属"LLM 翻译 + 脚本结构校验"的半自动流水线，无增量更新能力。
⑤ **技术实现**：载体=官方 texi→makeinfo HTML 产物原位汉化；站点=Jekyll 3.10 + GitHub Pages（页面实测含 Jekyll SEO tag v2.8.0）；构建=PowerShell 脚本链（无 Makefile/CI）。
⑥ **许可合规声明**：仓库无 LICENSE 文件（gh api `license: null`）；README 未声明翻译作品许可；官方文档为 CC-BY-SA 3.0（网页）与 GFDL 1.3（手册）双许可约束——**合规缺口明显**。
⑦ **多版本/历史版本处理**：仅单版本（2026-09 基线）；翻译说明明确提示新版底本需重译/重校。
⑧ **API/Doxygen**：完全未覆盖。
⑨ **站点可达性**：直连 200（0.75s）、代理 200（1.33s），github.io 在国内网络双通道均可用（2026-11-19 实测）。
⑩ **对本计划的组件级可借鉴/可复用点**：
   - 可直接借用其 `ffmpeg-zh-翻译说明.md` 的**翻译约定结构**（翻译范围/不译清单/术语标准/校验记录四段式）；
   - `term_pairs.json` 术语表可作本工程术语库的种子（可对照校订后复用）；
   - `split_plan.json` 分批翻译计划模式可迁移到 mkdocs 章节切分；
   - "同构副本"思想（HTML 结构不动只换文本）可下沉为本工程 texi→md 流水线的"结构保持校验"环节（脚本需重写为 Python/node）；
   - 反面教训：无许可声明、无增量同步、单点维护——本工程立项时需补齐（对应 DR-001~005 已定决策）。

---

### ffmpeg.net.cn

- 官网/站点: https://ffmpeg.net.cn/ （核实: 2026-11-19 直连 200/~0.6s；代理 200/0.32s，均可达）
- 官方文档/README: 无独立 README；站点自述性页面 `about.html`（核实: 2026-11-19 直连 200）与 `legal.html`（核实: 2026-11-19 直连 200）为官方对应页的翻译，未发现"翻译项目说明"页
- 源码: **未发现公开源码仓库**（gh 搜索 `linjianyou`/`林建有`/`ffmpeg.net.cn` 无果；页面内无 github/gitee 链接）——不可引用，仅记录搜索过程
- 简介: ffmpeg.org 官网的 1:1 中文翻译站，最早 Wayback 快照 2017-05-16，持续存活至今（Wayback 近年快照 2025-11/2026-01/2026-02/2026-08）。覆盖官网整站页面 + 官方文档导航全部 25 个核心文档页（texi 由维护者经 makeinfo 重生成后汉化，文档页脚自述"2025 年 1 月 21 日 makeinfo 生成"）+ 多版本 Doxygen 英文镜像（trunk + 33 个历史版本）。内容基线为 FFmpeg 7.1（首页最新新闻 2024-09-30 FFmpeg 7.1 "Péter"）。搜索引擎摘要显示"网站翻译由林建有提供支持"，但未能在我方抓取的页面内实测到该署名（存疑，不作为结论）。
- 优点: ①覆盖面全网第一：官网整站 + 全部 texi 文档页（含 7 个 `libav*` 库页）+ FAQ/legal 等网页文档；②文档经 makeinfo 从 texi 源重生成（与官方同源构建路线），抽样 ffmpeg-filters（16.4 万汉字）、ffmpeg-all（29 万汉字）、faq、libavcodec、about/legal 均为全文中文；③选项名/参数/代码保留英文，正文中文，风格与官方一致；④站点稳定运营 ≥9 年，国内可达性极佳（nginx + HTTP/2/h3，直连 0.3~0.6s）；⑤Doxygen 多版本镜像布局（trunk + 33 历史版本）可直接参考。
- 缺点: ①无公开源码/翻译资产仓库——全部工作不可复用、不可审校、不可协作；②内容基线停在 7.1（2024-09），落后上游约 1 年+（官网已有 FFmpeg 8.x），无增量同步证据；③部分旧新闻正文残留英文（首页尾部 2014 年新闻段未译）；④翻译许可合规未声明（页面仅转载官方 legal 内容，未声明译作本身的许可）；⑤无多语切换/无开源协作入口；⑥"林建有"署名仅见于搜索引擎摘要，站内未实测到。
- 适用场景: ①作为"覆盖面与信息架构"的对标样板（官网 1:1 映射方案已被验证可运营 9 年）；②作为国内可达的中文文档站体验参照；③Doxygen 多版本站点的目录组织参考。
- 存活判定: 站点内容 last-modified 2025-08-11（HTTP header 实测）+ Wayback 2026-08-23 仍有快照 → 存活候选（站点存活；但更新停滞于 2025-08）
- 保留/放弃判定与理由: **保留（作为对标样板与运营参照，非可复用资产）**。理由：它是中文区覆盖最全、运营最久的官方文档中文站，验证了整站 1:1 翻译的可行性与长期维护成本；但因无开源仓库，其翻译成果与流水线均不可复用，本工程应以"开源 + 增量"差异化超越。

**维度①~⑩补充小节**

① **活跃度**：无代码仓故无提交数据；站点级实测——HTTP header `last-modified: Mon, 11 Aug 2025 16:14:34 GMT`（ffmpeg.net.cn 与 ffmpeg-all.html 一致）；Wayback CDX：2025-11-08、2026-01-13、2026-02-04、2026-08-23 均 200 快照；最早快照 2017-05-16。
② **覆盖范围**：官网整站（about/news/download/documentation/community/contact/security/legal/consulting 等全部页面）+ 文档导航页列出的全部文档：3 个 CLI 手册、3 个 `-all` 合集、10 个组件文档（utils/scaler/resampler/codecs/bitstream-filters/formats/protocols/devices/filters）、7 个 `libav*` 库页（libavcodec.html 实测为已译完整短页）、faq/general/platform/developer/git-howto/fate；另镜像多版本 Doxygen（trunk + 33 个历史版本，英文原样）并外链 trac wiki。基线 FFmpeg 7.1（首页新闻最新条目 2024-09-30；文档页脚 makeinfo 2025-01-21 生成）。
③ **翻译完整性与质量口碑**：抽样 6 页均全文中文（中文字符密度：filters 16.4 万/37.5 万、all 29 万/72 万、faq 5269/13887 等）；命令与代码保留英文；官网旧新闻（2013–2014）部分段落英文残留；选项名/滤镜名/协议名术语统一。无公开渠道口碑数据。
④ **上游对齐与增量机制**：无自动化证据。文档采用 makeinfo 重生成（技术路线与官方一致，利于后续重生成），但近一年无内容更新（新闻止于 7.1、文档页 makeinfo 2025-01），上游对齐滞后。
⑤ **技术实现**：自托管 nginx（HTTP/2 + h3、CDN 缓存特征、CSP `frame-ancestors 'self' net.cn *.net.cn`）；站点框架=官方 bootstrap 模板（与 ffmpeg-web 同源）汉化；文档=texi→makeinfo 生成后嵌入翻译；无静态站生成器、无 CI。
⑥ **许可合规声明**：未发现翻译作品许可声明；legal.html 为官方许可页翻译；页脚保留官方"托管由 telepoint.bg 提供"字样（原样照搬）。
⑦ **多版本/历史版本处理**：texi 文档单版本（7.1 时代）；Doxygen 英文镜像含 trunk + 33 个历史版本（多版本处理仅限英文镜像）。
⑧ **API/Doxygen**：有完整 Doxygen 站点（https://ffmpeg.net.cn/doxygen/trunk/index.html 实测 200，英文字符，中文 0）——即 API 文档**只镜像未翻译**。全网未发现任何中文 API/Doxygen 翻译。
⑨ **站点可达性**：直连 200（0.3~0.6s）、代理 200（0.32s），国内可达性优；ffmpeg-all.html 全量抓取 1.62MB 时出现一次 HTTP/2 stream early-close（curl err 2），重试策略可解，属服务端流式行为而非不可达。
⑩ **对本计划的组件级可借鉴/可复用点**：
   - 信息架构：官网导航页 1:1 映射 + 全部 25 个核心文档页逐页对应——可直接作为本工程 sitemap 的对照清单；
   - 技术路线佐证：texi→makeinfo 重生成再翻译的路线可运营（与本工程 DR-003"texi→md+mkdocs"同源不同载体，其"从 texi 源重生成"思想可平移为"从 texi 源重解析"）；
   - Doxygen 多版本目录布局（doxygen/<version>/）可复用为本工程 API 重建的 URL 结构；
   - 差异化机会点：其"无源码、无增量、无合规、无协作"四大缺口正是本工程立项价值所在。

---

## 4. 历史参照（仅按模板记录，不深析）

### xdsnet/other-doc-cn-ffmpeg
- 官网/站点: https://xdsnet.github.io/other-doc-cn-ffmpeg/ （核实: 2026-11-19 直连 200/0.86s；代理 200/0.50s 可达；首页为"杂食菜熊的Blog"Wiki-in-box 动态目录页）
- 官方文档/README: https://github.com/xdsnet/other-doc-cn-ffmpeg#readme （核实: 2026-11-19 gh api 200）
- 源码: https://github.com/xdsnet/other-doc-cn-ffmpeg （核实: 2026-11-19 gh api 200）
- 简介: 2015-06 创建的"ffmpeg-all 全册"分章中文翻译，44 个分章 md（01–43 + 06x），GitBook（book.json/SUMMARY.md）构建，覆盖命令语法、解码器/编码器、滤镜、协议、设备、重采样、缩放等 ffmpeg-all 全部重要组件。中文区历史影响力最大的 FFmpeg 官方文档翻译（bookstack 托管版与全网 502 页 PDF 均源自它）。
- 优点: 全册覆盖 ffmpeg-all；分章 md 结构清晰；bookstack 提供了持续可访问的阅读入口。
- 缺点: 停更于 2021-01-26（基线约 FFmpeg 4.3/4.4 时代），后续 3 个大版本的滤镜/编解码器/协议增量全部缺失；无许可证声明；无上游同步。
- 适用场景: 旧版本（≤4.4）的中文参考阅读；分章切分粒度（ffmpeg-all→44 章）的章节数量级参考。
- 存活判定: 最后提交 2021-01-26 → 历史参照
- 保留/放弃判定与理由: 保留为历史参照。经验教训：①"一次性全册翻译+无人维护"注定过时——本工程的增量机制（DR-004）正是针对此缺口；②其 44 章切分与术语（"分离器/混合器/滤镜链图"等）可作为术语对齐的参考语料。

**补充数据（gh api 实测）**：created 2015-06-12、pushed 2021-01-26、⭐230、forks 71、contributors 1、license null。Gitee 无镜像（gitee.com/xdsnet/... 404）。派生物：easyhao007/ffmpeg-all-cn fork（2017-06-09 停更）、bookstack 托管书（直连 200）、quarkbook/CSDN 502 页 PDF。

### wdk-docs/ffmpeg-docs
- 官网/站点: https://wdk-docs.github.io/ffmpeg-docs （核实: 2026-11-19 直连 200/0.78s）
- 官方文档/README: https://github.com/wdk-docs/ffmpeg-docs#readme （核实: 2026-11-19 gh api 200）
- 源码: https://github.com/wdk-docs/ffmpeg-docs （核实: 2026-11-19 gh api 200）
- 简介: 2019 年的 Sphinx 构建中文翻译站（标题"ffmpeg-docs v2019.06.09 文档"），覆盖官网框架页 + 组件文档（bitstream-filters/codecs/devices/filters/formats/protocols/resampler/scaler/utils 的 doctree 可见），规模小、停在 2019-12-28。
- 优点: Sphinx 中文文档工程结构可参考（gettext 产物树）。
- 缺点: 内容规模小、停更 6 年+、无许可声明、无上游同步。
- 适用场景: 无（仅佐证 Sphinx 路线的先例）。
- 存活判定: 最后提交 2019-12-28 → 历史参照
- 保留/放弃判定与理由: 保留为历史参照；弃用其路线（Sphinx+texi 解析成本高，不如 md+mkdocs，与 DR-003 一致）。

**补充数据（gh api 实测）**：created 2019-06-02、pushed 2019-12-28、⭐0、forks 0、license null。

### apachecn/ffmpeg-doc-zh（含 apachecn-archive 副本）
- 官网/站点: 无（未发布有效站点）
- 官方文档/README: https://github.com/apachecn/ffmpeg-doc-zh#readme （核实: 2026-11-19 gh api 200；内容为未填充的 ApacheCN 模板占位符）
- 源码: https://github.com/apachecn/ffmpeg-doc-zh （核实: 2026-11-19 gh api 200）
- 简介: ApacheCN 2022-06 建仓后仅推送模板（docsify 资产 + 占位 README），**无任何实际翻译内容**；apachecn-archive/ffmpeg-doc-zh（2023-05-03）为其归档副本。
- 优点: 无。
- 缺点: 空仓库；佐证"ApacheCN 体系曾计划翻译 FFmpeg 官方文档但未落地"。
- 适用场景: 无。
- 存活判定: 最后提交 2022-06-02 → 历史参照（占位）
- 保留/放弃判定与理由: 排除性记录。说明大型翻译组织（ApacheCN）也未产出 FFmpeg 官方文档译本——中文区空白属实。

### easyhao007/ffmpeg-all-cn
- 官网/站点: 无
- 官方文档/README: https://github.com/easyhao007/ffmpeg-all-cn （核实: 2026-11-19 gh api 200，`fork:true`，parent=xdsnet/other-doc-cn-ffmpeg）
- 源码: 同上
- 简介: xdsnet 项目 2017 年的 fork，无独立改动（首提交 2015-07 book.json，pushed 2017-06-09）；其同名 Gitee 仓库现已 404。
- 优点/缺点/适用场景: 均同 xdsnet（fork 无独立价值）。
- 存活判定: 最后提交 2017-06-09 → 历史参照（fork）
- 保留/放弃判定与理由: 排除（fork 非独立项目）。

---

## 5. 参照对象（非中文，机制特别突出，最多 2 个——本次纳入 1 个）

### ayosec/ffmpeg-filters-docs
- 官网/站点: https://ayosec.github.io/ffmpeg-filters-docs/ （核实: 2026-11-19 直连 200/0.78s；代理 200/1.14s）
- 官方文档/README: https://github.com/ayosec/ffmpeg-filters-docs#readme （核实: 2026-11-19 gh api 200）
- 源码: https://github.com/ayosec/ffmpeg-filters-docs （核实: 2026-11-19 gh api 200）
- 简介: 英文项目，用仓库内工具链把官方 filters 文档重排为"每个滤镜一页"的站内文档：按 Filters/Audio、Sources/Multimedia 等自动分组、全局搜索框（`/` 快捷键 + 上下选择）、代码语法高亮、差异说明页。非中文翻译项目，纳入理由是其"从官方文档源自动生成 per-filter 页面"的机制对本工程 mkdocs 站点结构有直接参考价值。
- 优点: 机制自动化程度高（解析官方文档自动分组/建页）；Apache-2.0 许可清晰；2026-08-30 仍在推送（跟随上游维护）；每滤镜一页的导航体验显著优于官方单页。
- 缺点: 仅覆盖 filters 一个文档；英文；未处理文档许可再分发的声明细节（仅仓库许可）。
- 适用场景: filters 站点化阅读体验设计参考。
- 存活判定: 最后提交 2026-08-30 → 存活（参照对象）
- 保留/放弃判定与理由: 保留为机制参照。组件级借鉴点：①每滤镜一页 + 分组 + 站内搜索的 URL/导航结构可平移到本工程 filters 卷；②"从官方文档源码自动生成站点"的脚本思想与 DR-003 流水线同构，其分组推断逻辑（从官方文档章节头猜组）可参考。

**补充数据（gh api 实测）**：pushed 2026-08-30、⭐18、forks 0、license Apache-2.0、homepage=https://ayosec.github.io/ffmpeg-filters-docs/。

---

## 6. 选择策略矩阵（存活候选对比 + 对本计划的定位）

| 维度 | here200/ffmpeg-doc-zh | ffmpeg.net.cn | 本工程（ffmpeg-zh-docs，DR-001~005） |
|---|---|---|---|
| 开源可复用 | 是（全仓公开） | 否（无源码仓） | 是 |
| 覆盖面 | 18/25 核心文档页，缺 libav* 7 页 | 25/25 + 整站 + Doxygen 英文镜像 | 目标全类别（含 libav*、wiki 精选、API 注释翻译） |
| 内容新鲜度 | 2026-09 git 快照（新） | 7.1 时代（2024-09~2025-01），滞后 1 年+ | 基线=最新稳定 release，增量跟随 |
| 翻译工程资产 | 术语表/不译清单/校验脚本（可借鉴） | 无公开 | 自建（可借 here200 资产为种子） |
| 上游对齐机制 | 无 | 无（人工偶发） | 自动化增量流水线（立项核心差异） |
| 许可合规 | 无声明 | 无声明 | 立项时明确（普遍缺口=机会点） |
| API/Doxygen | 无 | 英文镜像未译 | 注释翻译+Doxygen 重建（中文区首例） |
| 可达性（国内） | 直连+代理均 200 | 直连+代理均 200（0.3s 级） | GitHub Pages + 可选国内镜像 |
| 定位 | 机制/资产借鉴源 | 对标样板/信息架构参照 | 差异化：开源+增量+全类别+合规 |

---

## 7. 关键发现汇总

1. **中文区不存在"持续跟进上游"的 FFmpeg 官方文档中文翻译项目**：现存 2 个存活候选分别是单发个人项目（here200，2026-09 后停更）与更新停滞的独立站（ffmpeg.net.cn，2025-08 后停更）；历史项目 xdsnet（2021 停更）、wdk-docs（2019 停更）均无上游同步。增量同步机制是全网空白，与本工程 DR-004 决策吻合。
2. **官方文档中文整册翻译的可行路线已被验证**：xdsnet（ffmpeg-all→44 章 md）、here200（官方 HTML 同构副本）、ffmpeg.net.cn（texi→makeinfo 重生成+汉化）三条路线均有可运营产出；其中 ffmpeg.net.cn 的 1:1 覆盖（25/25 文档页+整站）证明全类别翻译在体量上可行（filters 单页 16.4 万汉字、ffmpeg-all 29 万汉字量级）。
3. **API/Doxygen 中文翻译全网为零**：ffmpeg.net.cn 仅做英文多版本镜像，here200 未覆盖——本工程"API=注释翻译+Doxygen 重建"将是中文首例。
4. **翻译工程资产可直接借鉴**：here200 的 `_guide/ffmpeg-zh-翻译说明.md`（翻译范围/不译清单/术语标准/校验结果四段式）、`term_pairs.json` 术语表、`split_plan.json` 分批计划是现成的流水线设计参考；ayosec 的"每滤镜一页自动生成"机制可平移到 filters 卷的站点结构。
5. **许可合规是全体候选的共同缺口**（均无译作许可声明），官方文档 CC-BY-SA 3.0 + GFDL 1.3 的合规处理应在本工程许可声明中明确（与 S2 许可条款核实任务衔接）。
6. **搜索渠道结论**：GitHub 是唯一有效项目发现渠道；Gitee 搜索 API 不可用（应用层空结果）且网页搜索 JS 渲染、GitCode/AtomGit 无相关项目、awesome 清单与 trac wiki 均未收录任何中文翻译项目（trac wiki 296 页零命中）——说明中文项目分散且无聚合入口，进一步支持本工程的聚合价值。

---

*附：本次调研所有实测数据出处均为 gh api（GitHub REST）/ curl 直连 / curl 代理（192.168.33.1:10808）输出，查证日期 2026-11-19；唯一无法实测确认的信息为 ffmpeg.net.cn 维护者署名"林建有"（仅搜索引擎摘要提及，已在正文标注存疑）。临时文件位于 /tmp/ffmpeg-s1-tmp/。*
