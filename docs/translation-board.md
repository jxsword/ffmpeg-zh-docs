# 翻译任务看板（translation-board）

> 基线：n9.0.2（2026-09-18）· 段落总数：19046 · 状态口径：pending=待翻译 / skipped=不译豁免（fmt DR-014）
> 生成：scripts/gen_board.py（M1 收尾）· 批次粒度 ≈ 500 段/会话

## 总览

| 文件 | 段落 | 待译 | 豁免 | 优先级 |
|---|---|---|---|---|
| manual/ffmpeg.md | 805 | 805 | 0 | P0 |
| manual/ffplay.md | 80 | 80 | 0 | P0 |
| manual/ffprobe.md | 183 | 183 | 0 | P0 |
| manual/common-options.md | 146 | 146 | 0 | P0 |
| components/utils.md | 203 | 203 | 0 | P0 |
| components/scaler.md | 66 | 66 | 0 | P0 |
| components/resampler.md | 54 | 54 | 0 | P0 |
| components/codecs.md | 1983 | 1983 | 0 | P0 |
| components/bitstream-filters.md | 356 | 356 | 0 | P0 |
| components/formats.md | 1573 | 1573 | 0 | P0 |
| components/protocols.md | 677 | 677 | 0 | P0 |
| components/devices.md | 570 | 570 | 0 | P0 |
| libraries/libavutil.md | 13 | 13 | 0 | P0 |
| libraries/libavcodec.md | 9 | 9 | 0 | P0 |
| libraries/libavformat.md | 9 | 9 | 0 | P0 |
| libraries/libavdevice.md | 8 | 8 | 0 | P0 |
| libraries/libavfilter.md | 8 | 8 | 0 | P0 |
| libraries/libswscale.md | 12 | 12 | 0 | P0 |
| libraries/libswresample.md | 13 | 13 | 0 | P0 |
| general/faq.md | 193 | 193 | 0 | P0 |
| general/general.md | 166 | 166 | 0 | P0 |
| general/platform.md | 100 | 100 | 0 | P0 |
| general/developer.md | 287 | 287 | 0 | P0 |
| general/git-howto.md | 139 | 139 | 0 | P0 |
| general/fate.md | 0 | 0 | 0 | P0 |
| general/authors.md | 4 | 4 | 0 | P0 |
| general/mailing-list-faq.md | 114 | 114 | 0 | P2 |
| general/nut.md | 28 | 28 | 0 | P2 |
| general/community.md | 73 | 73 | 0 | P2 |
| general/drawvg-reference.md | 929 | 929 | 0 | P2 |
| general/APIchanges.md | 4 | 0 | 4 | 豁免（英文占位页，fmt DR-014） |

## 批次（正文 B 系列，按优先级排序）

| 批次 | 范围 | 段数 | 状态 |
|---|---|---|---|
| B1 | manual/ffmpeg.md | 805 | 未开始 |
| B2 | manual/ffplay.md + manual/ffprobe.md + manual/common-options.md + components/utils.md | 612 | 未开始 |
| B3 | components/scaler.md + components/resampler.md + components/codecs.md | 2103 | 未开始 |
| B4 | components/bitstream-filters.md + components/formats.md | 1929 | 未开始 |
| B5 | components/protocols.md | 677 | 未开始 |
| B6 | components/devices.md | 570 | 未开始 |
| B7 | libraries/libavutil.md + libraries/libavcodec.md + libraries/libavformat.md + libraries/libavdevice.md + libraries/libavfilter.md + libraries/libswscale.md + libraries/libswresample.md + general/faq.md + general/general.md + general/platform.md | 531 | 未开始 |
| B8 | general/developer.md + general/git-howto.md + general/fate.md + general/authors.md + general/mailing-list-faq.md | 544 | 未开始 |
| B9 | general/nut.md + general/community.md + general/drawvg-reference.md | 1030 | 未开始 |

## 批次（filters 卷 F 系列，按章节分组，DR-008）

| 批次 | 章节 | 滤镜数 | 段数 | 状态 |
|---|---|---|---|---|
| F1 | Filtering Introduction | - | 10 | 未开始 |
| F2 | graph2dot | - | 12 | 未开始 |
| F3 | Filtergraph description | - | 49 | 未开始 |
| F4 | Timeline editing | - | 12 | 未开始 |
| F5 | Changing options at runtime with a command | - | 1 | 未开始 |
| F6 | Options for filters with several inputs (framesync) | - | 8 | 未开始 |
| F7 | Audio Filters | - | 2067 | 未开始 |
| F8 | Audio Sources | - | 181 | 未开始 |
| F9 | Audio Sinks | - | 7 | 未开始 |
| F10 | Video Filters | - | 5684 | 未开始 |
| F11 | CUDA Video Filters | - | 151 | 未开始 |
| F12 | OpenCL Video Filters | - | 326 | 未开始 |
| F13 | VAAPI Video Filters | - | 135 | 未开始 |
| F14 | VideoToolbox Video Filters | - | 23 | 未开始 |
| F15 | Vulkan Video Filters | - | 104 | 未开始 |
| F16 | QSV Video Filters | - | 28 | 未开始 |
| F17 | Video Sources | - | 422 | 未开始 |
| F18 | Video Sinks | - | 7 | 未开始 |
| F19 | Multimedia Filters | - | 946 | 未开始 |
| F20 | Multimedia Sources | - | 48 | 未开始 |

## 纪律（M2 跨会话，R2 补充）

- 每批完成即 git 提交 + 本看板勾销 + 交接文档随更新
- 上下文过半或批次完成即收尾交接，不以"快完了"硬撑新批
- 术语冻结点：B1 批完成后 glossary v1 冻结（PLAN §9）
