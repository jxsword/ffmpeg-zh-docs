# 决策记录（ffmpeg-zh-docs）

> 格式参考：[架构决策记录](https://adr.github.io/)，对齐 fmt-zh-docs 决策日志惯例
> 编号规则：DR-XXX，取文件当前最大编号 + 1

---

## DR-001 2026-11-19 仓库托管与发布采用 GitHub 公开仓 + Actions/Pages [状态: 生效]

- **背景**: ffmpeg-zh-docs 新建工程需定托管发布方式；父目录已有 6 个同类翻译工程均为 GitHub 公开仓 + Actions/Pages 惯例，fmt-zh-docs 流水线成熟可直接复用
- **选项与权衡**: A GitHub公开仓+Pages(核心优: 复用既有CI/站点模板、可被社区检索协作; 代价: 建仓+配4条workflow) ← **选中**; A' 同A先私有后转公开(半成品不外露; 前期无社区反馈) 弃用; B 仅本地git(零外部依赖; 无CI无站点、与既有惯例不一致、后期迁移) 弃用; C Gitee等其他平台(国内访问快; Actions生态不可用、CI重写) 弃用
- **结论**: GitHub 公开仓（仓库名沿用 ffmpeg-zh-docs）+ Actions 四条流水线（sync-upstream / validate / deploy / test）+ mkdocs Material 站点发布，与 fmt-zh-docs 同构
- **理由**: 复用成本最低、CI/Pages 生态最全、与既有工程家族一致
- **影响**: 远程仓库创建（计划批准后实施）、`.github/workflows/`、`mkdocs.yml`、站点域名
- **记录时间 / 会话**: 2026-11-19 / ffmpeg-zh-docs 规划会话

---

## DR-002 2026-11-19 上游跟踪基线为最新稳定发布版 [状态: 生效]

- **背景**: 官网正文页对应 trunk nightly（每夜重建），但 9.0 等发布分支文档亦可获取；基线选择决定同步频率与增量工作量分布
- **选项与权衡**: A 最新稳定发布版tag为基线(语料稳定、增量集中在大版本+点版本、审校可控; 滞后于nightly) ← **选中**; B trunk nightly(与官网页严格一致、绝对最新; doc/随代码几乎每日变动、增量持续追赶、译文长期不满版) 弃用; C 双基线并行(兼顾稳定与最新; 两套状态文件两轮维护、成本×2) 弃用
- **结论**: 以最新 release tag（当前为 9.0 分支，落仓时以实测最新为准）为翻译基线；大版本发布做一次大增量、点版本小增量
- **理由**: FFmpeg 大版本节奏约一年一次，稳定基线使人审与增量成本可控
- **影响**: sync 脚本取 tag 逻辑、增量节奏、站点版本结构
- **记录时间 / 会话**: 2026-11-19 / ffmpeg-zh-docs 规划会话

---

## DR-003 2026-11-19 正文载体为 texi 转 Markdown + 沿用 mkdocs 流水线 [状态: 生效]

- **背景**: FFmpeg 正文是 Texinfo（`.texi`，约 40 个文件，最大 filters.texi ≈989KB），非既有工程处理的 md/reST，需定翻译载体与构建链
- **选项与权衡**: A 官方texinfo工具链(makeinfo)转DocBook/HTML再转Markdown入source/，后接fmt流水线(段落hash/保护/双语/校验/mkdocs全复用、"先找轮子"杠杆最大; 转换器需自研适配并以转换校验器兜底) ← **选中**; B 直译.texi保留官方构建链(产物与官方一致、可反哺上游; agent易破坏@标记、校验器须按texi重写、放弃mkdocs生态) 弃用; C 直译官网生成的HTML文本节点(视觉一致、锚点对齐; 1MB级HTML操作、diff粒度差、官方再生成即失效) 弃用
- **结论**: 采用 A；转换损耗以转换校验器（标题/表格/代码块计数、锚点映射）兜底；转换链细节在翻译计划中设计
- **理由**: 既有流水线是最大存量资产，FFmpeg 项目应最大化复用
- **影响**: `scripts/`（新增 texi 转换器）、`source/`、`zh/`、`mkdocs.yml`
- **记录时间 / 会话**: 2026-11-19 / ffmpeg-zh-docs 规划会话

---

## DR-004 2026-11-19 Community 文档范围：wiki 精选 + books 页仅译说明 [状态: 生效]

- **背景**: 导航页 Community Contributed 含 Official FFmpeg Wiki（trac.ffmpeg.org，数百页、持续变动）与 Books/外部资源页（外部书刊有版权）
- **选项与权衡**: A 正文全类别+wiki精选高价值常青页+books页仅译自身说明(覆盖主要学习路径、尊重版权、精选页注明出处可增量同步; 精选清单需评审维护) ← **选中**; B wiki全量翻译(彻底; 数百页且持续变动、成本失控、长期追赶) 弃用; C 不碰社区文档(范围最小; 与"全部翻译"目标偏差、社区部分断档) 弃用
- **结论**: 采用 A；wiki 精选初选清单在翻译计划中提出（调研 S1/S2 佐证）
- **理由**: 投入产出比与可持续性平衡
- **影响**: 翻译对象清单、站点导航、wiki 同步机制
- **记录时间 / 会话**: 2026-11-19 / ffmpeg-zh-docs 规划会话

---

## DR-005 2026-11-19 API 文档（Doxygen）采用注释翻译 + Doxygen 重建 [状态: 生效]

- **背景**: API 文档由源码 Doxygen 注释生成且官网 trunk 每夜重生成；按 DR-002 只译最新版本
- **选项与权衡**: A 以release tag建注释翻译分支：提取libav*头文件Doxygen注释为md→agent翻译→回填→本地Doxygen重建中文HTML(产物正宗、可随tag rebase持续更新、注释提取为md后复用hash增量管线; 注释量大、需回填校验器) ← **选中**; B 后处理官网生成HTML文本节点(不碰源码上手快; 与跟随更新根本矛盾、再生成即重译、HTML易碎) 弃用; C 指南式自写导读+关键API说明(成本最低; 覆盖不完整、与逐条翻译预期偏差) 弃用
- **结论**: 采用 A；回填校验器防注释结构破坏；随 DR-002 的 release 基线 rebase 更新
- **理由**: 与"跟随官方持续更新"目标契合，且与正文共用 agent 翻译管线
- **影响**: api 注释子目录、Doxygen 构建链、回填校验脚本
- **记录时间 / 会话**: 2026-11-19 / ffmpeg-zh-docs 规划会话

---

## DR-006 2026-11-19 许可与署名策略：按推定 LGPL 2.1+ 发布 + wiki CC BY-SA 3.0 分离标注 + ffmpeg-devel 并行确认 [状态: 生效]

- **背景**: S2 实测 .texi 无任何许可声明（n9.0.2 全树 grep 0 命中 GFDL/@copying），按 LICENSE.md "Most files…LGPL v2.1+ In combination" 推定随源码树 LGPL 2.1+；trac wiki 明示 CC BY-SA 3.0（署名 "Contributors to the FFmpeg Community Documentation Wiki"）；ffmpeg-web 无许可声明；API 注释随源码文件许可（LGPL 为主、libavfilter 40 文件 GPL、doc/examples 24 个 .c MIT）
- **选项与权衡**: A 立即按推定许可发布+并行邮件确认(合规闭环、不阻塞里程碑; 小概率官方后续明确为其他许可导致声明返工) ← **选中**; B 先向 ffmpeg-devel 确认再启动(确定性最高; 阻塞数周、与 DR-001 发布目标冲突) 弃用; C 仅标来源不附许可声明(零工作量; 合规风险最大、违背调研确立的合规定位) 弃用
- **结论**: 正文/API 注释译本按 LGPL-2.1-or-later 声明并附 COPYING.LGPLv2.1 副本，页面标注"译自 FFmpeg n9.0.x 官方文档"；wiki 精选页单独标注 CC BY-SA 3.0 + 规定署名，与 LGPL 译本分离管理；不搬运 ffmpeg-web 文案/设计资产；doc/t2h.pm 与 doc/texi2pod.pl 严禁衍生；libavfilter GPL 文件清单随 API 译本保留原许可标注；ffmpeg-devel 书面确认文档许可意图列为 M4 动作（用户主导发送），结论回填本条或新开 DR
- **理由**: 推定许可有 LICENSE.md 依据与社区补丁惯例佐证（developer.texi:433-445 要求补丁 LGPL 2.1+）；零阻塞兑现 DR-001
- **影响**: LICENSE、LICENSE_TRANSLATION.md、COPYING.LGPLv2.1 副本、站点页脚、README 许可章节、wiki 页脚模板、api/ 译本许可标注
- **记录时间 / 会话**: 2026-11-19 / ffmpeg-zh-docs 规划执行会话

---

## DR-007 2026-11-19 texi→md 转换器采用 makeinfo→DocBook→pandoc→GFM + 自研后处理 [状态: 生效]

- **背景**: DR-003 已定链路方向（makeinfo→DocBook/HTML→md）未定具体转换器；2026-11-19 冒烟实测：makeinfo --docbook（真实文件 utils.texi/metadata.texi，texinfo 7.2）→ pandoc 3.7.0.2 -f docbook -t gfm 开箱可用（标题层级/variablelist/代码保留），已知 4 项后处理：弯引号清理、项值对结构化、缩进代码 fenced 化、锚点映射自建
- **选项与权衡**: A pandoc 接力+自研后处理(轮子复用最大、DocBook 结构规整、后处理面实测最小; pandoc 不可定制处靠后处理补) ← **选中**; B makeinfo --docbook→自研 lxml 转 md(结构控制最强; DocBook→md 全要素映射自研代码量大、维护高) 弃用; C makeinfo --html→HTML 清洗(官方锚点直接保留; HTML 噪声大、清洗规则脆弱、1MB 级 filters 页性能差) 弃用
- **结论**: 转换链 = makeinfo --docbook → pandoc → Python 后处理（上述 4 项）→ source/*.md；转换校验器（标题/代码块/列表计数对比 + 锚点映射表 + 结构保真校验）兜底转换损耗；CI 锁定 texinfo/pandoc 版本
- **理由**: 实测可用、复用最大，对齐"先找轮子"纪律
- **影响**: scripts/texi2md.py、scripts/validate_structure.py、CI 构建环境（texinfo/pandoc 版本锁定）、M1 验收标准
- **记录时间 / 会话**: 2026-11-19 / ffmpeg-zh-docs 规划执行会话

---

## DR-008 2026-11-19 filters 卷采用每滤镜一页 [状态: 生效]

- **背景**: filters.texi 949KB/141,693 词占去重正文 47%，是增量机制核心难点；参照对象 ayosec/ffmpeg-filters-docs（Apache-2.0，2026-08 仍活跃）验证"每滤镜一页"自动生成机制可行
- **选项与权衡**: A 每滤镜一页(source/ 整卷存储、翻译单元=滤镜小节、构建期自动拆页; 增量粒度到滤镜级、URL/检索体验好; 需拆分器+分组逻辑、URL 与官方不一致以锚点映射兼容) ← **选中**; B 官方单页整页对应翻译(与官方 1:1、实现最简; 16 万汉字单页加载/编辑/diff 全面劣化) 弃用; C 按官方一级小节拆页(折中、贴近官方目录; 单节仍数万词、增量粒度粗) 弃用
- **结论**: source/ 保留 filters.md 整卷；构建期由 scripts/split_filters.py 按滤镜小节拆分为 zh/filters/<滤镜名>.md 页面并生成分组导航（借鉴 ayosec 分组思路）；建立官方 ffmpeg-filters.html#<filter> 锚点映射表兼容外链
- **理由**: 增量机制是本工程立项核心差异（调研确认全网空白），滤镜级 hash 才能兑现"仅译变更滤镜"
- **影响**: source/ 结构、scripts/split_filters.py、mkdocs nav、validate_structure.py 拆分校验、站点 URL 结构
- **记录时间 / 会话**: 2026-11-19 / ffmpeg-zh-docs 规划执行会话

---

## DR-009 2026-11-19 手册页结构：独有内容 + 组件交叉链接（不内联共享件） [状态: 生效]

- **背景**: ffmpeg/ffplay/ffprobe.texi 各 @include 13 个共享件（官方 HTML 单页内联全部）；若译文内联则 manual/ffmpeg.md 达 20 万词级巨页且与组件页内容重复，与 DR-008"大单页加载/编辑/diff 劣化"论证直接冲突（计划首轮复审发现）
- **选项与权衡**: A 手册页=工具独有内容+组件页锚点交叉链接(模块化、无重复翻译、与 DR-008 同向; 与官方单页结构偏差以锚点映射兼容) ← **选中**; B 完全内联复刻官方 ffmpeg.html(与官方 1:1; 巨页+重复翻译+TM 成本) 弃用; C 手册页也按节拆分(粒度过碎、导航复杂、无内容收益) 弃用
- **结论**: source/manual/{ffmpeg,ffplay,ffprobe}.md 仅含工具独有内容；fftools-common-opts.texi 独立页 /manual/common-options/、authors.texi 独立小页 /general/authors/，手册页以锚点链接引用；官方 ffmpeg.html#锚点 外链经 anchor_map 映射到对应组件页
- **理由**: 消除重复翻译与巨页，与 DR-008 拆页方向一致
- **影响**: source/ 目录结构、texi2md.py include 解析、mkdocs nav、fix_links.py、站点信息架构
- **记录时间 / 会话**: 2026-11-19 / ffmpeg-zh-docs 计划三轮复审会话（随计划批准生效）

---

> **前瞻**: ffmpeg-devel 关于文档许可的书面确认结论到达后，回填 DR-006 或新开 DR。
>
> *下一编号：DR-010*
