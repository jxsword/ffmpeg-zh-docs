# 概要

ffplay \[\<options\>\] \[`input_url`\]

# 描述

FFplay 是一个非常简单、可移植的媒体播放器，使用 FFmpeg 库和 SDL 库构建。它主要用作各类 FFmpeg API 的试验平台。

# 选项

## 主要选项

- **`-x width`** 强制显示宽度。

- **`-y height`** 强制显示高度。

- **`-fs`** 以全屏模式启动。

- **`-an`** 禁用音频。

- **`-vn`** 禁用视频。

- **`-sn`** 禁用字幕。

- **`-ss pos`** 定位到 \<pos\>。注意多数格式无法做到精确定位，因此 `ffplay` 会定位到距 \<pos\> 最近的定位点。

  \<pos\> 必须是时长描述，参见 `ffmpeg-utils`（ffmpeg-utils(1) 手册）中的 Time duration（时长）一节。

- **`-t duration`** 播放 \<duration\> 秒的音频/视频。

  \<duration\> 必须是时长描述，参见 `ffmpeg-utils`（ffmpeg-utils(1) 手册）中的 Time duration（时长）一节。

- **`-bytes`** 按字节定位。

- **`-seek_interval`** 设置使用左/右方向键定位时的自定义间隔（以秒为单位）。默认为 10 秒。

- **`-nodisp`** 禁用图形显示。

- **`-noborder`** 无边框窗口。

- **`-alwaysontop`** 窗口置顶。可用平台：X11（SDL \>= 2.0.5）、Windows（SDL \>= 2.0.6）。

- **`-volume`** 设置启动音量。0 表示静音，100 表示既不降低也不放大音量。负值按 0 处理，超过 100 的值按 100 处理。

- **`-f fmt`** 强制格式。

- **`-window_title title`** 设置窗口标题（默认为输入文件名）。

- **`-left title`** 设置窗口左边缘的 x 位置（默认为窗口居中）。

- **`-top title`** 设置窗口顶部的 y 位置（默认为窗口居中）。

- **`-loop number`** 将影片播放循环 \<number\> 次。0 表示无限循环。

- **`-showmode mode`** 设置要使用的显示模式。\<mode\> 的可用取值为：

  | Term | Description |
  |----|----|
  | `0, video` | 显示视频 |
  | `1, waves` | 显示音频波形 |
  | `2, rdft` | 使用 RDFT（(逆)实数离散傅里叶变换）显示音频频带 |

  默认值为 "video"；若视频不存在或无法播放，则自动选择 "rdft"。

  按 w 键可在可用的显示模式之间交互式循环切换。

- **`-vf filtergraph`** 创建由 \<filtergraph\> 指定的滤镜链图，并用它对视频流进行滤镜处理。

  \<filtergraph\> 是要应用于该流的滤镜链图描述，必须具有单个视频输入和单个视频输出。在滤镜链图中，输入关联到标签 `in`，输出关联到标签 `out`。滤镜链图语法的更多信息参见 ffmpeg-filters 手册。

  可以多次指定该参数，按 w 键即可在指定的各个滤镜链图与显示模式之间循环切换。

- **`-af filtergraph`** \<filtergraph\> 是要应用于输入音频的滤镜链图描述。使用 "-filters" 选项可显示所有可用滤镜（包括源和汇）。

- **`-i input_url`** 读取 \<input_url\>。

## 高级选项

- **`-stats`** 打印若干播放统计信息，特别是显示流时长、编解码器参数、当前在流中的位置以及音频/视频同步漂移。默认显示，除非日志级别低于 `info`。手动指定该选项可强制显示。要禁用它，需要指定 `-nostats`。

- **`-fast`** 不完全符合规范标准的优化。

- **`-genpts`** 生成 pts。

- **`-sync type`** 将主时钟设为音频（`type=audio`）、视频（`type=video`）或外部（`type=ext`）。默认为音频。主时钟用于控制音视频同步。多数媒体播放器使用音频作为主时钟，但在某些情况下（流媒体或高质量广播）需要改变这一点。该选项主要用于调试目的。

- **`-ast audio_stream_specifier`** 使用给定的流说明符选择所需的音频流。流说明符在[流说明符](#Stream-specifiers)章节中描述。未指定该选项时，会在已选视频流所在节目中选择"最佳"音频流。

- **`-vst video_stream_specifier`** 使用给定的流说明符选择所需的视频流。流说明符在[流说明符](#Stream-specifiers)章节中描述。未指定该选项时，会选择"最佳"视频流。

- **`-sst subtitle_stream_specifier`** 使用给定的流说明符选择所需的字幕流。流说明符在[流说明符](#Stream-specifiers)章节中描述。未指定该选项时，会在已选视频或音频流所在节目中选择"最佳"字幕流。

- **`-autoexit`** 视频播放完毕后退出。

- **`-exitonkeydown`** 按下任意键时退出。

- **`-exitonmousedown`** 按下任意鼠标键时退出。

- **`-codec:media_specifier codec_name`** 为 \<media_specifier\> 标识的流强制指定特定的解码器实现，\<media_specifier\> 可取值 `a`（音频）、`v`（视频）和 `s`（字幕）。

- **`-acodec codec_name`** 强制使用特定的音频解码器。

- **`-vcodec codec_name`** 强制使用特定的视频解码器。

- **`-scodec codec_name`** 强制使用特定的字幕解码器。

- **`-autorotate`** 根据文件元数据自动旋转视频。默认启用，使用 `-noautorotate` 可禁用。

- **`-framedrop`** 视频失去同步时丢弃视频帧。主时钟未设为视频时默认启用。使用该选项可对所有主时钟来源启用丢帧，使用 `-noframedrop` 可禁用。

- **`-infbuf`** 不限制输入缓冲区大小，尽快从输入读取尽可能多的数据。对实时流默认启用（若不及时读取，数据可能被丢弃）。使用该选项可为所有输入启用无限缓冲，使用 `-noinfbuf` 可禁用。

- **`-filter_threads nb_threads`** 定义处理滤镜管线使用多少线程。每条管线都会创建一个包含这么多线程的线程池供并行处理使用。默认值为 0，表示线程数由可用 CPU 数量决定。

- **`-enable_vulkan`** 使用 vulkan 渲染器而非 SDL 内置渲染器。依赖 libplacebo。

- **`-vulkan_params`** 通过以 ":" 分隔的 \<key\>=\<value\> 对列表配置 Vulkan。

- **`-hwaccel`** 使用硬件加速解码。启用该选项会自动启用 vulkan 渲染器。

- **`-video_bg pattern`** 设置透明视频使用的视频背景图案。纯色图案可使用颜色名称或颜色代码，参见 `ffmpeg-utils`（ffmpeg-utils(1) 手册）中的 Color（颜色）一节。还可使用特殊关键字 `tiles` 表示棋盘格样式图案，这也是默认值。`none` 图案在渲染时不做 alpha 混合，相当于忽略透明通道。

## 播放期间

- **q, ESC** 退出。

- **f** 切换全屏。

- **p, SPC** 暂停。

- **m** 切换静音。

- **9, 0**

- **/, \*** 分别减小和增大音量。

- **a** 在当前节目中循环切换音频声道。

- **v** 循环切换视频声道。

- **t** 在当前节目中循环切换字幕声道。

- **c** 循环切换节目。

- **w** 循环切换视频滤镜或显示模式。

- **s** 步进到下一帧。

  若流尚未暂停则先暂停，步进到下一个视频帧，然后暂停。

- **left/right** 向后/向前定位 10 秒；若设置了 -seek_interval 则按自定义间隔定位。

- **down/up** 向后/向前定位 1 分钟。

- **page down/page up** 定位到上一个/下一个章节；若无章节则向后/向前 10 分钟。

- **right mouse click** 按点击位置相对窗口宽度的比例定位到文件中的对应百分比处。

- **left mouse double-click** 切换全屏。

# 另请参见

ffmpeg(1), ffprobe(1), ffmpeg-utils(1), ffmpeg-scaler(1), ffmpeg-resampler(1), ffmpeg-codecs(1), ffmpeg-bitstream-filters(1), ffmpeg-formats(1), ffmpeg-devices(1), ffmpeg-protocols(1), ffmpeg-filters(1)
