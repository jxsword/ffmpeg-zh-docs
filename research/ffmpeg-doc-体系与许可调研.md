# FFmpeg 文档体系与许可调研（S2）

- 调研日期：2026-11-19
- 基线对象：FFmpeg n9.0.2（当前最新稳定 tag，与 DR-002 决策一致）
- 数据通道：全部实测。git ls-remote / 浅克隆（直连 GitHub，成功）；gh api releases 端点返回 `[]`（FFmpeg 不发布 GitHub Releases，仅用 tag），tag 日期改由浅克隆内 `git fetch --depth 1` + `git for-each-ref --format='%(creatordate:iso)'` 实测；trac.ffmpeg.org / ffmpeg.org 用 curl 直连实测。
- 克隆源码属不可信数据，位于 /tmp/ffmpeg-s2-src/（n9.0.2，commit 946fcce0）与 /tmp/ffmpeg-s2-web/（ffmpeg-web 主分支），仅用 `python3 -I` 脚本读取，未执行其中任何脚本。
- 核实通道标注：除非另注，均为 2026-11-19 直连可达（本机直连 GitHub/git.ffmpeg.org/trac/ffmpeg.org 均正常，未启用代理）。

---

## 1. release 节奏（实测）

### 1.1 tag 与日期全表（n6.x ~ n9.x，tagger 日期）

命令：`git ls-remote --tags https://github.com/FFmpeg/FFmpeg`（得 tag 名，直连成功）→ 浅克隆 n9.0.2 后
`git fetch --depth 1 origin 'refs/tags/n6*:refs/tags/n6*' 'refs/tags/n7*:...'` + `git for-each-ref --format='%(refname:short)|%(creatordate:iso)|%(objecttype)'`（全部为 annotated tag）。

| tag | 日期（tagger，UTC±当地） | 类型 |
|---|---|---|
| n6.0 | 2023-02-27 | major |
| n6.0.1 | 2023-11-10 | point |
| n6.1 | 2023-11-11 | minor（major 线内次版本） |
| n6.1.1 | 2023-12-31 | point |
| n6.1.2 | 2024-08-02 | point |
| n6.1.3 | 2025-08-14 | point |
| n6.1.4 | 2025-11-23 | point |
| n6.1.5 | 2026-05-05 | point |
| n6.1.6 | 2026-06-20 | point |
| n7.0 | 2024-04-05 | major |
| n7.0.1 | 2024-05-26 | point |
| n7.0.2 | 2024-08-03 | point |
| n7.0.3 | 2025-08-05 | point |
| n7.1 | 2024-09-30 | minor |
| n7.1.1 | 2025-03-03 | point |
| n7.1.2 | 2025-09-14 | point |
| n7.1.3 | 2025-11-21 | point |
| n7.1.4 | 2026-05-05 | point |
| n7.1.5 | 2026-06-20 | point |
| n8.0 | 2025-08-22 | major |
| n8.0.1 | 2025-11-20 | point |
| n8.0.2 | 2026-05-04 | point |
| n8.0.3 | 2026-06-18 | point |
| n8.1 | 2026-03-16 | minor |
| n8.1.1 | 2026-05-04 | point |
| n8.1.2 | 2026-06-17 | point |
| n8.1.3 | 2026-09-21 | point |
| **n9.0** | **2026-08-03** | **major** |
| n9.0.1 | 2026-08-12 | point |
| **n9.0.2** | **2026-09-18** | **point（当前最新稳定）** |

另有开发标记 n6.1-dev / n6.2-dev / n7.1-dev / n7.2-dev / n8.1-dev / n8.2-dev / n9.1-dev（branch 切分点，非发布）。

### 1.2 量化结论

- **major 间隔**（n9.0.2 实测 checkout commit 946fcce0，2026-09-18）：
  - n6.0→n7.0：2023-02-27 → 2024-04-05 = **403 天**
  - n7.0→n8.0：2024-04-05 → 2025-08-22 = **504 天**
  - n8.0→n9.0：2025-08-22 → 2026-08-03 = **346 天**
  - 近 3 个 major 平均 **约 418 天（13.7 个月）**，即"约一年一个 major"，波动区间 11~17 个月。
- **minor（x.1）节奏**：n6.1 落后 major 257 天、n7.1 落后 178 天、n8.1 落后 206 天；n9.1 尚未发布（截 2026-11-19 已过 78 天，仅 n9.1-dev）。可预期 **major 后约半年出现 x.1**。
- **point 频率**：每条活跃线 2~5 个 point，呈**成批集中发布**特征——n6.1.5/n7.1.4/n8.0.2/n8.1.1 全部落在 2026-05-04~05，n6.1.6/n7.1.5/n8.0.3/n8.1.2 落在 2026-06-17~20（典型的 5 月/6 月维护窗口；11 月窗口亦常见，如 n6.1.4/n7.1.3/n8.0.1）。旧线（n6.1/n7.1）在 n9.0 发布后仍持续获得 point（最近 2026-06-20），即 **2~3 条旧线并行维护 1~2 年**。
- **当前最新稳定 tag：n9.0.2**（2026-09-18，GitHub Releases 页为空、无 pre-release 标记，n9.1 未出，n9.0.2 即稳定基线；`git describe` 于 /tmp/ffmpeg-s2-src 返回 n9.0.2）。翻译基线按 DR-002 取 n9.0.2 成立。
- **对翻译的节奏含义**：若按 release tag 跟随，理论更新压力约"每年 1 次 major 级文档大更新 + 半年一次 minor + 若干 point 小修"；文档 nightly 由 trunk 重新生成（见 §5），与 release 不同步。

---

## 2. doc/ 全量清单与体量（n9.0.2 实测）

命令：`git clone --depth 1 --branch n9.0.2 https://github.com/FFmpeg/FFmpeg /tmp/ffmpeg-s2-src`（直连，10.9s）；
`wc -l -w -c *.texi`（doc/ 下）；`grep -c '@include' *.texi`；逐文件人工阅读确认存根性质。
注意：**doc/ 下共 48 个 .texi**（任务背景所引"约 40 个"为近似；filters.texi 在 n9.0.2 为 949,519 B ≈ 927KB，此前 989KB 应为更新的 trunk 快照）。

### 2.1 全量 .texi 表（按字节降序已排为字母序输出，下面为原始实测）

| 文件 | 行 | 词 | 字节 | KB | 纯外壳 | @include 数 |
|---|---:|---:|---:|---:|:---:|---:|
| authors.texi | 11 | 53 | 403 | 0.4 | 否 | 0 |
| bitstream_filters.texi | 1095 | 4858 | 32582 | 31.8 | 否 | 0 |
| codecs.texi | 1043 | 3408 | 25689 | 25.1 | 否 | 2 |
| community.texi | 182 | 1367 | 8190 | 8.0 | 否 | 0 |
| decoders.texi | 690 | 3023 | 20948 | 20.5 | 否 | 0 |
| demuxers.texi | 1231 | 6856 | 44051 | 43.0 | 否 | 0 |
| developer.texi | 1184 | 6787 | 45328 | 44.3 | 否 | 0 |
| devices.texi | 25 | 116 | 815 | 0.8 | 是 | 2 |
| drawvg-reference.texi | 2793 | 9199 | 67260 | 65.7 | 否 | 0 |
| encoders.texi | 4801 | 19808 | 139231 | 136.0 | 否 | 0 |
| faq.texi | 686 | 3880 | 25900 | 25.3 | 否 | 0 |
| fate.texi | 300 | 1452 | 9855 | 9.6 | 否 | 0 |
| ffmpeg-bitstream-filters.texi | 46 | 92 | 879 | 0.9 | 是 | 2 |
| ffmpeg-codecs.texi | 43 | 74 | 708 | 0.7 | 是 | 2 |
| ffmpeg-devices.texi | 43 | 74 | 711 | 0.7 | 是 | 2 |
| ffmpeg-filters.texi | 43 | 73 | 710 | 0.7 | 是 | 2 |
| ffmpeg-formats.texi | 43 | 75 | 726 | 0.7 | 是 | 2 |
| ffmpeg-protocols.texi | 43 | 74 | 723 | 0.7 | 是 | 2 |
| ffmpeg-resampler.texi | 45 | 95 | 883 | 0.9 | 是 | 2 |
| ffmpeg-scaler.texi | 44 | 93 | 837 | 0.8 | 是 | 2 |
| ffmpeg-utils.texi | 43 | 74 | 712 | 0.7 | 是 | 2 |
| ffmpeg.texi | 3338 | 18303 | 139582 | 136.3 | 否 | 13 |
| ffplay.texi | 352 | 1389 | 10165 | 9.9 | 否 | 13 |
| ffprobe.texi | 730 | 3045 | 21757 | 21.2 | 否 | 13 |
| fftools-common-opts.texi | 440 | 2243 | 15369 | 15.0 | 否 | 0 |
| **filters.texi** | **34370** | **141693** | **949519** | **927.3** | 否 | 0 |
| formats.texi | 293 | 1542 | 10791 | 10.5 | 否 | 3 |
| general.texi | 15 | 22 | 214 | 0.2 | 是 | 1 |
| general_contents.texi | 1600 | 9979 | 68987 | 67.4 | 否 | 0 |
| git-howto.texi | 484 | 2026 | 13442 | 13.1 | 否 | 0 |
| indevs.texi | 1596 | 7334 | 49624 | 48.5 | 否 | 0 |
| libavcodec.texi | 49 | 118 | 1130 | 1.1 | 否 | 1 |
| libavdevice.texi | 46 | 96 | 991 | 1.0 | 否 | 1 |
| libavfilter.texi | 45 | 85 | 1040 | 1.0 | 否 | 1 |
| libavformat.texi | 49 | 108 | 1089 | 1.1 | 否 | 1 |
| libavutil.texi | 63 | 168 | 1363 | 1.3 | 否 | 1 |
| libswresample.texi | 71 | 238 | 1878 | 1.8 | 否 | 1 |
| libswscale.texi | 64 | 190 | 1531 | 1.5 | 否 | 1 |
| mailing-list-faq.texi | 389 | 1924 | 13148 | 12.8 | 否 | 0 |
| metadata.texi | 89 | 375 | 2466 | 2.4 | 否 | 0 |
| muxers.texi | 4092 | 20436 | 141719 | 138.4 | 否 | 0 |
| nut.texi | 159 | 726 | 4545 | 4.4 | 否 | 0 |
| outdevs.texi | 450 | 1906 | 13121 | 12.8 | 否 | 0 |
| platform.texi | 349 | 1565 | 11679 | 11.4 | 否 | 0 |
| protocols.texi | 2408 | 11318 | 76573 | 74.8 | 否 | 0 |
| resampler.texi | 228 | 1132 | 7444 | 7.3 | 否 | 0 |
| scaler.texi | 234 | 753 | 5471 | 5.3 | 否 | 0 |
| utils.texi | 1129 | 3422 | 23837 | 23.3 | 否 | 0 |
| **合计（48 个）** | **67566** | **293667** | **2015616** | **1968.4** | | |
| 纯外壳小计（11 个） | 433 | 862 | 7918 | 7.7 | | |
| **正文小计（37 个）** | **67133** | **292805** | **2007698** | **1960.6** | | |

### 2.2 include 结构与口径说明

- **纯外壳（11 个，共 7.9KB）**：`ffmpeg-{utils,filters,codecs,formats,protocols,devices,bitstream-filters,scaler,resampler}.texi`（9 个）+ `devices.texi` + `general.texi`——逐个人工读确认只含 titlepage/简介一句/@include/See Also，无独有正文。如 ffmpeg-filters.texi 全文 43 行仅包 `@include filters.texi`。外壳是官网"Components Documentation"单页的载体。
- **正文文件（37 个，2,007,698 B ≈ 1.91 MiB ≈ 29.3 万英文词）**：
  - 内容件被多手册复用：ffmpeg/ffplay/ffprobe.texi 三者均 `@include` 同一批 13 个文件（fftools-common-opts、config、utils、codecs、bitstream_filters、formats、protocols、devices、resampler、scaler、filters、general_contents、authors）；codecs.texi 再包含 decoders+encoders；formats.texi 包含 demuxers+muxers+metadata；devices.texi（外壳）包含 indevs+outdevs。因此构建产物（ffmpeg-all.html 等）远大于源字节，但**源码层去重后需翻译的正文即 2.0MB**。
  - filters.texi 一个文件占正文 47%（949,519/2,007,698 B；141,693 词占 48%）——是翻译工程的核心单体，必须分片/分批处理。
  - libav*.texi 7 个是**短小的独立库介绍页**（各 1KB 左右，仅 @include authors.texi），不是存根，但 API 主体在 Doxygen（见 §4e）。
- **构建期生成、源码树中不存在的 .texi**：`doc/config.texi`（configure 生成，实测 configure:8806 `echo "@c auto-generated by configure - do not modify!" > doc/config.texi`）与 `doc/avoptions_{format,codec}.texi`（由 `doc/print_options.c` 编译后**从二进制**抽取选项表生成，doc/Makefile GENTEXI 规则；在 n9.0.2 中它们只作为构建依赖，无 .texi `@include` 引用——选项表正文已硬编码在 codecs/formats.texi 中）。翻译侧需自行补生成 config.texi 或占位。

### 2.3 doc/ 其他形态（非 .texi）

| 类别 | 内容 |
|---|---|
| API 文档生成 | `Doxyfile`（103,212 B，PROJECT_NUMBER=9.0.2，INPUT 留空由 doxy-wrapper.sh 注入）、`doxy-wrapper.sh`、`doxy/`（空目录，构建产物目标 doc/doxy/html） |
| 手册构建工具 | `Makefile`（HTML=makeinfo --html + t2h.pm；man=texi2pod.pl→pod2man；txt=makeinfo --no-headers；仅 fate.txt 走 TXTPAGES）、`t2h.init`/`t2h.pm`（**t2h.pm 与 texi2pod.pl 为 GPL 文件**，见 §4b）、`texi2pod.pl`、`texidep.pl`、`print_options.c`（LGPL）、`htmlxref.cnf` |
| 代码示例 | `examples/`：24 个 .c + Makefile + Makefile.example + README（.c 头部为 **MIT 许可**，例：decode_audio.c "Copyright (c) 2001 Fabrice Bellard … Permission is hereby granted, free of charge…"） |
| 设计笔记（纯文本） | build_system.txt、filter_design.txt、infra.txt、issue_tracker.txt、mips.txt、multithreading.txt、optimization.txt、rate_distortion.txt、snow.txt、swresample.txt、swscale.txt、swscale-v2.txt、tablegen.txt、`transforms.md`（31,387 B）、CVSS.txt |
| 变更记录 | `APIchanges`（179,886 B——API 变更日志，API 文档翻译的重要语料） |
| 其他 | ffprobe.xsd（26,213 B，ffprobe XML schema）、errno.txt、lexicon、patchwork、fate_config.sh.template、default.css + bootstrap.min.css/style.min.css（源自 ffmpeg-web，见 §4c） |

---

## 3. 构建链与版本要求（实测）

### 3.1 makeinfo / texinfo

- **官方要求**（configure 实测摘录，configure:7621-7625）：
  ```sh
  $makeinfo --version > /dev/null 2>&1 && enable makeinfo_command || disable makeinfo_command makeinfo_html
  if enabled makeinfo_command; then
    [ 0$($makeinfo --version | grep "texinfo" | sed 's/.*texinfo[^0-9]*\([0-9]*\)\..*/\1/') -ge 5 ] \
      && enable makeinfo_html || disable makeinfo_html
  ```
  即：**仅要求 makeinfo 存在即可出 info/txt；主版本号 ≥5 才启用 HTML 输出**（否则回退 texi2html）。无 texinfo 上限要求。doc/Makefile:72/76 实际命令：`makeinfo --html -I doc --no-split -D config-not-all --init-file=doc/t2h.pm --output $@ $<`。
- **本机实测**：初始未装 makeinfo；经 `sudo -n apt-get install -y texinfo` 安装后 `makeinfo --version` → `texi2any (GNU texinfo) 7.2`（满足 ≥5）。已注：该安装为本机环境变更，如需卸载 `sudo apt-get remove texinfo`。
- **输出格式实测**（对 doc/metadata.texi，产物在 /tmp/ffmpeg-s2-tmp/makeinfo-test/）：
  - `makeinfo --html --no-split` → metadata.html（4,277 B，成功）
  - `makeinfo --docbook` → metadata.xml（成功）
  - `makeinfo`（默认）→ metadata.info（成功）
  - txt 由 doc/Makefile:57 `makeinfo --force --no-headers` 生成（官方仅对 fate.txt 使用）。
  - man 页路径：texi2pod.pl（perl）→ pod2man；本机 `/usr/bin/pod2man` 存在。

### 3.2 Doxygen

- **官方要求**：Doxyfile 未设版本约束；configure 仅做存在性检查（configure:5083-5085：`if test "$doxygen" != "$doxygen_default" && ! $doxygen --version >/dev/null 2>&1; then warn "Specified doxygen … will fail to build."`）。Doxyfile 关键项（n9.0.2 实测）：PROJECT_NUMBER=9.0.2、OUTPUT_DIRECTORY=doc/doxy、INPUT 空（由 doc/doxy-wrapper.sh 以命令行注入 `INPUT=$@`，版本号取 VERSION 文件或 `git describe`）、GENERATE_HTML=YES。
- **本机实测**：`doxygen --version` → **1.15.0**（/usr/bin/doxygen），满足一般使用（FFmpeg 无最低版本声明）。

---

## 4. 许可核实（核心，逐项摘录原文）

**总体关键事实先行**：FFmpeg 官方文档 .texi **不存在** @copying 块、**不存在** 任何 GFDL/许可授予文本（与常见假设相反）：
- `grep -l 'GNU Free Documentation License' doc/*.texi` → **空**（48 个文件 0 命中）
- `grep -l '@copying' doc/*.texi` → 空；`grep -n 'Permission is granted\|Copyright (C)' *.texi` → 仅 4 个文件在**正文**中提及许可主题（developer/encoders/general_contents/fftools-common-opts，均为内容性提及而非声明）
- 即：**文档源文件没有任何自身许可声明**，许可结论只能从整仓许可文件与官网声明推断（见 4.4 综合结论）。

### 4a. .texi 头部声明核查（逐项）

- ffmpeg.texi 头部（head -50 实测）：`\input texinfo` → `@settitle ffmpeg Documentation` 后直接进 Synopsis，无版权/许可段。
- filters.texi / ffprobe.texi / faq.texi：同样无 @copying、无许可文本。
- 正文中的许可性提及仅两处值得注意（内容性，非声明）：
  - developer.texi:27-29（指导语）："For more detailed legal information about the use of FFmpeg in external programs read the `LICENSE` file in the source tree and consult https://ffmpeg.org/legal.html."
  - developer.texi:433-445（补丁许可要求）："Licenses for patches must be compatible with FFmpeg. Contributions should be licensed under the LGPL 2.1, including an 'or any later version' clause, or, if you prefer a gift-style license, the ISC or MIT license. GPL 2 including an 'or any later version' clause is also acceptable, but LGPL is preferred. If you add a new file, give it a proper license header."
  - general_contents.texi 中大段是外部库（x264/libdavs2/Apache 2.0 等）与 FFmpeg 组合时的许可升级说明（与 LICENSE.md 同源）。
- 构建模板也不注入许可：doc/t2h.init 的 `FFMPEG_FOOTER` 缺省模板（t2h.init:28-33）仅为 `</div></body></html>` 收尾 + "makeinfo 程序串"，无许可脚注；ffmpeg-web 的 src/template_footer1 亦只有托管方致谢（"Hosting provided by telepoint.bg"）。
- **结论：官方文档（texi 及其生成的 HTML/man/txt）不带任何许可页脚/封面声明；其许可状态完全依附于源码树的 LGPL 2.1+ 主许可（见 4b），但这是一个"未明示"状态，属本项目最大的合规不确定点。**

### 4b. LICENSE.md / COPYING.*（n9.0.2 实测，仓库根）

文件：`LICENSE.md`（127 行）+ COPYING.GPLv2 / COPYING.GPLv3 / COPYING.LGPLv2.1 / COPYING.LGPLv3（标准 FSF 全文）。

LICENSE.md 关键原文摘录：

> Most files in FFmpeg are under the GNU Lesser General Public License version 2.1 or later (LGPL v2.1+). Read the file `COPYING.LGPLv2.1` for details. Some other files have MIT/X11/BSD-style licenses. In combination the LGPL v2.1+ applies to FFmpeg.
>
> Some optional parts of FFmpeg are licensed under the GNU General Public License version 2 or later (GPL v2+). See the file `COPYING.GPLv2` for details. None of these parts are used by default, you have to explicitly pass `--enable-gpl` to configure to activate them. In this case, FFmpeg's license changes to GPL v2+.
>
> Specifically, the GPL parts of FFmpeg are: … - the following building and testing tools - `compat/solaris/make_sunver.pl` - **`doc/t2h.pm`** - **`doc/texi2pod.pl`** - `libswresample/tests/swresample.c` - `tests/checkasm/*` - `tests/tiny_ssim.c` - the following filters in libavfilter: - `signature_lookup.c` - `vf_blackframe.c` …（28 个 libavfilter 文件，其中 vf_lensfun.c 为 GPL v3+）
>
> Should you, for whatever reason, prefer to use version 3 of the (L)GPL, then the configure parameter `--enable-version3` will activate this licensing option for you.
>
> There are a handful of files under other licensing terms, namely: * The files `libavcodec/jfdctfst.c`, `libavcodec/jfdctint_template.c` and `libavcodec/jrevdct.c` are taken from libjpeg … Specifically note that you must credit the IJG in the documentation accompanying your program if you only distribute executables. You must also indicate any changes … to those three files in the documentation. * `tests/reference.pnm` is under the expat license.

README.md「## License」节原文：

> FFmpeg codebase is mainly LGPL-licensed with optional components licensed under GPL. Please refer to the LICENSE file for detailed information.

- **覆盖范围判断**：LICENSE.md 是"源码树总体声明"，按"Most files in FFmpeg"表述，doc/ 下 .texi 作为源码树一部分**默认落入 LGPL v2.1+ 组合许可**，但没有任何一句明示"文档按 LGPL 发布"或单独的文档许可（无 FDL、无 CC）。COPYING.* 均为标准 GPL/LGPL 全文，不含文档特别条款。
- **注意**：doc/ 内两个构建工具 t2h.pm、texi2pod.pl 被 LICENSE.md 明列为 **GPL v2+ 文件**（t2h.pm 头部实测自述 "GNU General Public License … version 3 or later"，作者含 Free Software Foundation/Andreas Cadhalpun/Timothy Gu）。翻译项目**不得衍生/修改这两个工具文件**（衍生需整体 GPL），但以其原样构建文档无碍。
- **doc/examples/*.c 头部为 MIT**（实测 decode_audio.c："Permission is hereby granted, free of charge, to any person obtaining a copy …"），print_options.c 为标准 LGPL 2.1+ 头。

### 4c. ffmpeg-web.git（网站源码）

- 存在性：`git clone --depth 1 https://git.ffmpeg.org/ffmpeg-web.git /tmp/ffmpeg-s2-web`（**直连成功，3.6s**；另有 GitHub 镜像 FFmpeg/ffmpeg-web）。仓库结构：README、Makefile、bower.json、generate-doc.sh、src/（每页一个无扩展名源文件 + _js/_title）、htdocs/（css/js 静态资源）。
- **许可核查**：仓库**没有任何 COPYING/LICENSE 文件**；README 全文只讲构建方法（lessc/clean-css、make），无许可声明。`grep -rn -i 'creative commons|licensed under|CC-BY|GFDL|GNU Free' src/ htdocs/` 仅命中第三方资产：htdocs/js/respond.min.js（MIT）、bootstrap.min.js/css（MIT）。generate-doc.sh 显示官网文档页由 `./generate-doc.sh <ffmpeg-src>` 从 FFmpeg 源码树 texi 生成（README 原文："None of the generated versions of the website contain the documentation. To generate the documentation pages, just `./generate-doc.sh <ffmpeg-src>`."）。
- src/legal（官网 legal.html 源）关于 FFmpeg 软件许可的原文（非网站内容许可）：

  > FFmpeg is licensed under the GNU Lesser General Public License (LGPL) version 2.1 or later. However, FFmpeg incorporates several optional parts and optimizations that are covered by the GNU General Public License (GPL) version 2 or later. If those parts get used the GPL applies to all of FFmpeg.
  >
  > Note that FFmpeg is not available under any other licensing terms, especially not proprietary/commercial ones, not even in exchange for payment.

- **结论：ffmpeg-web 网站源码无显式许可授予**（页面文案、布局、CSS 设计均处于无声明状态）。对翻译项目的含义：**不要搬运官网页面文案/导航/设计资产**；翻译语料应以源码树 .texi 为准（我们本来就要从源码生成中文站，这一点可满足）。

### 4d. trac wiki（trac.ffmpeg.org）

- 实测：curl https://trac.ffmpeg.org/wiki/WikiStart（直连，25,862 B，页面版本 243，最后修改 2026-10-02）。
- WikiStart「About this Wiki → License」节原文（完整摘录）：

  > The materials within the Community Contributed Documentation section of the FFmpeg Wiki are released under the Creative Commons Attribution-ShareAlike 3.0 License. This allows anyone to share, adapt, and build upon this work, even for commercial purposes, as long as the same or compatible license is used and that credit is properly attributed to the author(s). Credit should be attributed to "Contributors to the FFmpeg Community Documentation Wiki".

- **范围限定**：声明只覆盖 wiki 的 **Community Contributed Documentation 部分**；Trac 软件自带文档（TracGuide 等）与 bug tracker 不在其列。
- **结论：wiki 社区文档 = CC BY-SA 3.0**——翻译/引用可行，但必须署名 "Contributors to the FFmpeg Community Documentation Wiki" 并以相同/兼容许可（BY-SA 3.0 或后续兼容版本）共享。documentation.html 将 wiki（含 BooksAndOtherExternalResources）归入 "Community Contributed Documentation"（见 §5），即官网导航指向的 wiki 内容大体都按此许可理解。

### 4e. API（Doxygen）注释的许可分布

- **机制事实**：Doxygen 注释（/** … @file @brief @param … */）写在库源码文件内部，随文件许可走，无独立文档许可。Doxyfile INPUT 为全库源码（含 .h），生成 doc/doxy/html。
- **标准头实测摘录**（libavutil/utils.c、libavcodec/avcodec.c 等一致）：

  > This file is part of FFmpeg.
  > FFmpeg is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.

- **分布统计**（n9.0.2，`grep -l 'version 2.1 of the License, or (at your option) any later version'` 计 LGPL 2.1+ 标准头；`grep -l 'under the terms of the GNU General Public License'` 计 GPL 头；文件含 .c/.h）：

  | 库 | LGPL 2.1+ 头文件数 | GPL 头文件数 | ISC/MIT 样式 |
  |---|---:|---:|---:|
  | libavutil | 262 | 2 | 0 |
  | libavcodec | 1695 | 0 | 6 |
  | libavformat | 690 | 0 | 0 |
  | libavfilter | 566 | **40** | 1 |
  | libswscale | 52 | 0 | 0 |
  | libswresample | 19 | 0 | 0 |
  | libavdevice | 61 | 0 | 1 |

  （libavfilter 的 40 个 GPL 文件与 LICENSE.md 所列 28+ 个 GPL filter 及 x86/asm GPL 文件吻合；libavutil 的 2 个 GPL 命中为相关文件提及。）
- **结论：API 文档 = 头文件/源码内注释，许可随文件——绝大多数 LGPL 2.1+，少数（主要是 libavfilter 若干 filter 与构建工具）GPL 2+/GPL 3+，极少数 MIT/ISC。翻译并再发布 API 文档属于派生作品，需按 LGPL 2.1+（GPL 部分保持其原许可）发布并附许可声明与变更说明。**

### 4.4 综合结论（对"翻译再发布"的约束）

| 语料 | 许可 | 依据强度 |
|---|---|---|
| doc/*.texi 正文（手册/FAQ/组件页） | **无自身声明；按源码树主许可推定为 LGPL 2.1+**（组合中部分内容 MIT/BSD 风格） | 推定（LICENSE.md "Most files…In combination the LGPL v2.1+ applies"；无逐文件头） |
| 官网 ffmpeg.org 页面外壳/文案 | **未声明**（ffmpeg-web 无许可文件） | 事实 |
| trac wiki（社区文档/Books 列表） | **CC BY-SA 3.0**（署名 "Contributors to the FFmpeg Community Documentation Wiki"） | WikiStart 原文明示 |
| API 文档（Doxygen 生成） | **随源码文件许可**：LGPL 2.1+ 为主，libavfilter 少数 GPL，examples 为 MIT | 逐文件头实测 |
| 构建工具 doc/t2h.pm、doc/texi2pod.pl | **GPL（不得衍生）** | LICENSE.md 明列 |

---

## 5. 文档体系映射（官网 documentation.html 实测）

核实：curl https://ffmpeg.org/documentation.html（直连，10,006 B，2026-11-19 可达）。页面说明原文："The following documentation is regenerated nightly, and corresponds to the newest FFmpeg revision. Consult your locally installed documentation for older versions."（即**官网文档页随 trunk nightly 重新生成**，非 release 固定版——翻译基线需自建 release 版文档，与官网版本存在时间差。）

| 官网类别 | 页面 | 源（n9.0.2 源码树） |
|---|---|---|
| Command Line Tools Documentation | ffmpeg.html / **ffmpeg-all.html**；ffplay(.html)/ffplay-all；ffprobe(.html)/ffprobe-all | ffmpeg.texi / ffplay.texi / ffprobe.texi（-all 版将 13 个 @include 全展开为单页） |
| Components Documentation | Utilities(ffmpeg-utils)、Scaler(ffmpeg-scaler)、Resampler(ffmpeg-resampler)、Codecs(ffmpeg-codecs)、Bitstream filters(ffmpeg-bitstream-filters)、Formats(ffmpeg-formats)、Protocols(ffmpeg-protocols)、Devices(ffmpeg-devices)、Filters(ffmpeg-filters) | 9 个 ffmpeg-*.texi 外壳 → 各自 @include 的 utils/scaler/resampler/codecs(→decoders+encoders)/bitstream_filters/formats(→demuxers+muxers+metadata)/protocols/devices(→indevs+outdevs)/filters.texi |
| Libraries Documentation | libavutil / libswscale / libswresample / libavcodec / libavformat / libavdevice / libavfilter | 7 个 libav*.texi 短页（正文主体在 Doxygen API 文档） |
| General Documentation | FAQ(faq.html)、Supported External Libraries…(general.html)、Platform Specific Information(platform.html)、Developer Documentation(developer.html)、Git How-To(git-howto.html)、FATE(fate.html) | faq.texi、general.texi→general_contents.texi、platform.texi、developer.texi、git-howto.texi、fate.texi（另有官网页未列的 mailing-list-faq.texi、nut.texi、community.texi、drawvg-reference.texi 亦可构建） |
| API Documentation | doxygen/trunk/index.html（nightly）+ 历史版本存档（9.0/8.1/8.0/7.1/7.0/6.1/…/0.5） | Doxyfile + 库源码注释（doc/doxy/html 构建目标） |
| Community Contributed Documentation | Official FFmpeg Wiki（trac.ffmpeg.org/wiki）、Books and other external resources（trac wiki BooksAndOtherExternalResources 页） | trac wiki（CC BY-SA 3.0），非源码树内容 |
| （官网其他相关页） | Download（含 doxygen 历史链）、Bug Reports→bugreports.html（源码树无对应 texi，为 web 仓库 src/bugreports）、Legal→legal.html（web 仓库 src/legal） | ffmpeg-web/src/*（无许可声明） |

---

## 6. 对翻译计划的合规提示清单

1. **文档许可无明示是最大不确定点**：.texi 无任何许可头/授予文本，只能推定随源码树 LGPL 2.1+。建议：(a) 中文译本按 LGPL 2.1+ 发布，附 LICENSE 副本、显著标注"译自 FFmpeg n9.0.2 官方文档（LGPL 2.1+），并注明译本修改/翻译状态"；(b) 更稳妥的做法是通过 ffmpeg-devel 邮件列表书面确认文档许可意图（社区一贯要求补丁 LGPL 2.1+，developer.texi:433-445 为佐证），确认结论回填本项目决策记录。
2. **严禁衍生 doc/t2h.pm 与 doc/texi2pod.pl**（LICENSE.md 明列 GPL 文件）；原样使用其构建产物没有问题。翻译流水线应把这两个文件排除在"可翻译/可改"清单外。
3. **wiki 内容（CC BY-SA 3.0）单独管理**：若翻译 wiki 页（含 Books and other external resources），必须署名 "Contributors to the FFmpeg Community Documentation Wiki" 并以 BY-SA 3.0+ 兼容许可共享，且与 LGPL 的手册译本**分开标注许可**，避免混许可。
4. **不要搬运官网（ffmpeg-web）页面文案与设计**：该仓库无任何许可声明；中文站应仅基于源码树 .texi 生成内容（可复用其构建思路 generate-doc.sh，但不抄其无许可的文案/样式资产；bootstrap CSS 等 MIT 资产保留其许可头即可）。
5. **API 文档翻译的许可碎片化**：API 注释随文件许可（LGPL 2.1+ 为主，libavfilter 40 个 GPL 文件、examples MIT）；若做 API 文档中文版，需按文件清单保留各文件原许可并整包附 COPYING.LGPLv2.1 等副本；Doxygen 生成物本身无版权注入，许可声明需自行附加。
6. **版本漂移管理**：major 间隔约 11~17 个月（均值 ~13.7 个月），x.1 约在 major 后半年，point 成批出现在 5-6 月/11 月维护窗口；官网文档 nightly 随 trunk 变化。建议译本页面固定标注基线 tag（如 "基于 n9.0.2，译于 2026-xx"），并预期 filters.texi（927KB、14.2 万词）在每次 major 时有实质 diff，需建立 texi→中文的 diff 同步机制而非按页重译。
7. **构建期文件**：doc/config.texi 与 doc/avoptions_*.texi 为 configure/print_options 生成物（源码树无），译前需在本地 configure 后补齐，或以占位说明处理。

---

## 附：本调研实测命令与产物索引

- tag/日期：`git ls-remote --tags https://github.com/FFmpeg/FFmpeg`；`git -C /tmp/ffmpeg-s2-src fetch --depth 1 origin 'refs/tags/n6*:…'`；`git for-each-ref --format='%(refname:short)|%(creatordate:iso)' refs/tags/n6* …`
- 体量：`wc -l -w -c /tmp/ffmpeg-s2-src/doc/*.texi`；`grep -c '@include' …`；逐文件 head/sed 阅读判存根
- 构建链：configure:7621-7625/5083-5085、doc/Makefile:57-76、doc/Doxyfile；本机 `makeinfo --version`（texi2any 7.2）、`doxygen --version`（1.15.0）；格式试验产物 /tmp/ffmpeg-s2-tmp/makeinfo-test/
- 许可：LICENSE.md/COPYING.*/README.md 全文；grep 统计 .texi 与库文件头；ffmpeg-web 于 /tmp/ffmpeg-s2-web；trac WikiStart 存档 /tmp/ffmpeg-s2-tmp/wikistart.html；documentation.html 存档 /tmp/ffmpeg-s2-tmp/documentation.html
- 全部 URL 于 2026-11-19 直连实测可达（未使用代理）。
