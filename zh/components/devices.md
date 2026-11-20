# 描述

本文档描述 libavdevice 库提供的输入和输出设备。

# 设备选项

libavdevice 库提供与 libavformat 相同的接口。即，输入设备被视为解复用器，输出设备被视为复用器，接口和通用设备选项与 libavformat 提供的相同（参见 ffmpeg-formats 手册）。

此外，每个输入或输出设备还可以支持所谓的私有选项，即特定于该组件的选项。

选项可以通过在 FFmpeg 工具中指定 -\<option\> \<value\> 来设置，或通过在设备 `AVFormatContext` 选项中显式设置值，或使用 `libavutil/opt.h` API 以编程方式设置。

# 输入设备

输入设备是 FFmpeg 中的可配置元素，用于访问来自系统所连多媒体设备的数据。

配置 FFmpeg 构建时，所有支持的输入设备默认启用。可以使用 configure 选项 "–list-indevs" 列出所有可用的设备。

可以使用 configure 选项 "–disable-indevs" 禁用所有输入设备，使用选项 "–enable-indev=\<INDEV\>" 选择性启用某个输入设备，或者使用选项 "–disable-indev=\<INDEV\>" 禁用特定输入设备。

ff\* 工具的选项 "-devices" 将显示支持的输入设备列表。

以下是对当前可用输入设备的描述。

## alsa

ALSA (Advanced Linux Sound Architecture) 输入设备。

要在配置期间启用此输入设备，需要在系统上安装 libasound。

此设备允许从 ALSA 设备采集。要采集的设备名称必须是 ALSA 卡标识符。

ALSA 标识符的语法为：

``` text
hw:CARD[,DEV[,SUBDEV]]
```

其中 \<DEV\> 和 \<SUBDEV\> 部分是可选的。

三个参数（依次为 \<CARD\>、\<DEV\>、\<SUBDEV\>）指定卡号或标识符、设备号和子设备号（-1 表示任意）。

要查看系统当前识别的卡列表，请检查文件 `/proc/asound/cards` 和 `/proc/asound/devices`。

例如要用 `ffmpeg` 从卡 ID 为 0 的 ALSA 设备采集，可以运行命令：

``` text
ffmpeg -f alsa -i hw:0 alsaout.wav
```

更多信息参见：<http://www.alsa-project.org/alsa-doc/alsa-lib/pcm.html>

### 选项

| Term          | Description                                  |
|---------------|----------------------------------------------|
| `sample_rate` | 设置采样率（Hz）。默认为 48000。 |
| `channels`    | 设置声道数。默认为 2。    |

## android_camera

Android 摄像头输入设备。

此输入设备使用 Android Camera2 NDK API（API 级别 24+ 的设备可用）。android_camera 的可用性在配置期间自动检测。

此设备允许从 Android 设备上集成到 Camera2 NDK API 的所有摄像头采集。

可用的摄像头在内部进行枚举，可以用 \<camera_index\> 参数选择。输入文件字符串被丢弃。

通常后置摄像头的索引为 0，前置摄像头的索引为 1。

### 选项

- **`video_size`** 设置视频大小，以 640x480 或 hd720 等字符串给出。若请求的视频大小不可用或未指定，则回退到 Android 报告的第一个可用配置。

- **`framerate`** 设置视频帧率。若请求的帧率不可用或为默认值 (-1)，则回退到 Android 报告的第一个可用配置。

- **`camera_index`** 设置要使用的摄像头的索引。默认为 0。

- **`input_queue_size`** 设置要缓冲的最大帧数。默认为 5。

## avfoundation

AVFoundation 输入设备。

AVFoundation 是 Apple 当前推荐的用于在 OSX \>= 10.7 以及 iOS 上进行流抓取的框架。

输入文件名必须按以下语法给出：

``` text
-i "[[VIDEO]:[AUDIO]]"
```

第一个条目选择视频输入，后者选择音频输入。流必须由设备列表中显示的设备名称或设备索引指定。也可以使用 `-video_device_index <INDEX>` 和/或 `-audio_device_index <INDEX>` 按索引选择视频和/或音频输入设备，覆盖输入文件名中给出的任何设备名称或索引。

可以使用 `-list_devices true` 枚举所有可用设备，列出所有设备名称及对应索引。

有两个设备名称别名：

- **`default`** 选择对应类型的 AVFoundation 默认设备。

- **`none`** 不录制对应的媒体类型。这等价于指定空的设备名称或索引。

### 选项

AVFoundation 支持以下选项：

- **`-list_devices <TRUE|FALSE>`** 若设为 true，给出所有可用输入设备的列表，显示所有设备名称和索引。

- **`-video_device_index <INDEX>`** 按索引指定视频设备。覆盖输入文件名中给出的任何内容。

- **`-audio_device_index <INDEX>`** 按索引指定音频设备。覆盖输入文件名中给出的任何内容。

- **`-pixel_format <FORMAT>`** 请求视频设备使用特定的像素格式。如果指定的格式不受支持，将给出可用格式列表，并改用列表中的第一个。可用的像素格式有：`monob, rgb555be, rgb555le, rgb565be, rgb565le, rgb24, bgr24, 0rgb, bgr0, 0bgr, rgb0, bgr48be, uyvy422, yuva444p, yuva444p16le, yuv444p, yuv422p16, yuv422p10, yuv444p10, yuv420p, nv12, yuyv422, gray`

- **`-framerate`** 设置抓取帧率。默认值为 `ntsc`，对应帧率 `30000/1001`。

- **`-video_size`** 设置视频帧大小。

- **`-capture_cursor`** 采集鼠标指针。默认为 0。

- **`-capture_mouse_clicks`** 采集屏幕鼠标点击。默认为 0。

- **`-capture_raw_data`** 采集原始设备数据。默认为 0。使用此选项可能导致接收到交付给 AVFoundation 框架的底层数据。例如，对于向框架发送原始 DV 数据的混合设备（如基于磁带的摄像机），将此选项设为 false 会仅以指定的像素格式采集提取出的视频帧。将此选项设为 true 则会原样接收原始 DV 流。

### 示例

- 打印 AVFoundation 支持的设备列表并退出：

  ``` text
  $ ffmpeg -f avfoundation -list_devices true -i ""
  ```

- 从视频设备 0 和音频设备 0 录制视频到 out.avi：

  ``` text
  $ ffmpeg -f avfoundation -i "0:0" out.avi
  ```

- 从视频设备 2 和音频设备 1 录制视频到 out.avi：

  ``` text
  $ ffmpeg -f avfoundation -video_device_index 2 -i ":1" out.avi
  ```

- 使用像素格式 bgr0 从系统默认视频设备录制视频，不录制任何音频，输出到 out.avi：

  ``` text
  $ ffmpeg -f avfoundation -pixel_format bgr0 -i "default:none" out.avi
  ```

- 从合适的输入设备录制原始 DV 数据并写入 out.dv：

  ``` text
  $ ffmpeg -f avfoundation -capture_raw_data true -i "zr100:none" out.dv
  ```

## decklink

decklink 输入设备为 Blackmagic DeckLink 设备提供采集功能。

要启用此输入设备，需要 Blackmagic DeckLink SDK，并需要使用相应的 `--extra-cflags` 和 `--extra-ldflags` 进行配置。在 Windows 上，需要通过 `widl` 运行 IDL 文件。

DeckLink 对其支持的格式非常挑剔。输入的像素格式可以用 `raw_format` 设置。帧率和视频大小必须用 `-list_formats 1` 为您的设备确定。音频采样率始终为 48 kHz，声道数可以为 2、8 或 16。注意，所有音频声道都捆绑在单个音频轨道中。

### 选项

- **`list_devices`** 若设为 `true`，打印设备列表并退出。默认为 `false`。此选项已弃用，请使用 ffmpeg 的 `-sources` 选项列出可用的输入设备。

- **`list_formats`** 若设为 `true`，打印支持的格式列表并退出。默认为 `false`。

- **`format_code <FourCC>`** 此选项将输入视频格式设置为 FourCC 给定的格式。要查看您的设备支持的值，请使用 `list_formats`。注意存在 FourCC `'pal '`，也可以用作 `pal`（3 个字母）。默认行为是自动检测输入视频格式（如果硬件支持）。

- **`raw_format`** 设置采集视频的像素格式。可用值为：

  - **`auto`** 这是默认值，表示使用格式自动检测时为 8 位 YUV 422 或 8 位 ARGB，否则为 8 位 YUV 422。

  - **`uyvy422`** 8 位 YUV 422。

  - **`yuv422p10`** 10 位 YUV 422。

  - **`argb`** 8 位 RGB。

  - **`bgra`** 8 位 RGB。

  - **`rgb10`** 10 位 RGB。

- **`teletext_lines`** 若设为非零值，将从垂直辅助数据中额外采集一路图文电视流。同时支持 SD PAL (576i) 和 HD (1080i 或 1080p) 源。对于 HD 源，将解码 OP47 数据包。

  此选项是所采集的 SD PAL VBI 行的位掩码，具体为第 6 到 22 行以及第 318 到 335 行。第 6 行是掩码中的 LSB。选中的不含图文电视信息的行将被忽略。可以使用特殊常量 `all` 选择所有可能的行，或用 `standard` 跳过第 6、318 和 319 行，这些行与所有接收器不兼容。

  对于 SD 源，ffmpeg 需要以 `--enable-libzvbi` 编译。对于 HD 源，在较旧（非 4K）的 DeckLink 卡型号上必须以 10 位模式采集。

- **`channels`** 定义要采集的音频声道数。必须为 `2`、`8` 或 `16`。默认为 `2`。

- **`duplex_mode`** 设置 decklink 设备的双工/配置档 (profile) 模式。必须为 `unset`、`half`、`full`、`one_sub_device_full`、`one_sub_device_half`、`two_sub_device_full`、`four_sub_device_half`。默认为 `unset`。

  注意：DeckLink SDK 11.0 已用配置档属性取代双工属性。对于 DeckLink Duo 2 和 DeckLink Quad 2，配置档在使用相同连接器的任意 2 个子设备之间共享。对于 DeckLink 8K Pro，配置档在全部 4 个子设备之间共享，因此 DeckLink 8K Pro 支持四个配置档。

  DeckLink 8K Pro 的有效配置档模式（DeckLink SDK \>= 11.0）：`one_sub_device_full`、`one_sub_device_half`、`two_sub_device_full`、`four_sub_device_half`

  DeckLink Quad 2 和 DeckLink Duo 2 的有效配置档模式：`half`、`full`

- **`timecode_format`** 要包含在帧和视频流元数据中的时间码类型。必须为 `none`、`rp188vitc`、`rp188vitc2`、`rp188ltc`、`rp188hfr`、`rp188any`、`vitc`、`vitc2` 或 `serial`。默认为 `none`（不包含）。

  为了正确支持 50/60 fps 时间码，对于 \>30 fps 的内容，`rp188any` 查询的时间码类型顺序为 HFR、VITC1、VITC2 和 LTC。注意，这与 DeckLink API 使用的顺序（HFR、VITC1、LTC、VITC2）略有不同。

- **`video_input`** 设置视频输入源。必须为 `unset`、`sdi`、`hdmi`、`optical_sdi`、`component`、`composite` 或 `s_video`。默认为 `unset`。

- **`audio_input`** 设置音频输入源。必须为 `unset`、`embedded`、`aes_ebu`、`analog`、`analog_xlr`、`analog_rca` 或 `microphone`。默认为 `unset`。

- **`video_pts`** 设置视频包时间戳源。必须为 `video`、`audio`、`reference`、`wallclock` 或 `abs_wallclock`。默认为 `video`。

- **`audio_pts`** 设置音频包时间戳源。必须为 `video`、`audio`、`reference`、`wallclock` 或 `abs_wallclock`。默认为 `audio`。

- **`draw_bars`** 若设为 `true`，在信号丢失时绘制彩条。默认为 `true`。此选项已弃用，请使用 `signal_loss_action` 选项。

- **`signal_loss_action`** 设置信号丢失时采取的操作。接受以下值之一：

  | Term | Description |
  |----|----|
  | `1, none` | 信号丢失时不做任何操作。这通常导致黑帧。 |
  | `2, bars` | 信号丢失时绘制彩条。仅支持 8 位输入信号。 |
  | `3, repeat` | 信号丢失时重复最后一个视频帧。 |

  默认为 `bars`。

- **`queue_size`** 设置最大输入缓冲区大小（字节）。如果缓冲达到该值，传入的帧将被丢弃。默认为 `1073741824`。

- **`audio_depth`** 设置音频采样位深。必须为 `16` 或 `32`。默认为 `16`。

- **`decklink_copyts`** 若设为 `true`，时间戳按原样转发，不移除初始偏移。默认为 `false`。

- **`timestamp_align`** 采集起始时间对齐（秒）。若设为非零值，将丢弃输入帧，直到系统时间戳与配置值对齐。最多容忍一帧时长的对齐差异。这有助于在为"N 路"冗余部署的 N 个不同硬件设备之间保持输入同步。使用此选项之前，应通过 NTP 或 PTP 等协议同步不同硬件设备的系统时间。注意，此方法并非万无一失。在某些边界情况下，由于 OS 中的线程调度抖动，输入同步可能无法进行。任一方向的偏差可能为 1 帧，更罕见的情况下可能偏差 `timestamp_align` 秒。默认为 `0`。

- **`wait_for_tc (bool)`** 丢弃帧，直到收到带时间码的帧。有时串行时间码不会随第一个输入帧一起收到。如果发生这种情况，存储的流时间码将不准确。若此选项设为 `true`，将丢弃输入帧，直到收到带时间码的帧。必须指定选项 \<timecode_format\>。默认为 `false`。

- **`enable_klv(bool)`** 若设为 `true`，从 VANC 提取 KLV 数据并输出 KLV 包。KLV VANC 包基于 MID 和 PSC 字段合并，并聚合为一个 KLV 包。默认为 `false`。

### 示例

- 列出输入设备：

  ``` text
  ffmpeg -sources decklink
  ```

- 列出支持的格式：

  ``` text
  ffmpeg -f decklink -list_formats 1 -i 'Intensity Pro'
  ```

- 以 1080i50 采集视频片段：

  ``` text
  ffmpeg -format_code Hi50 -f decklink -i 'Intensity Pro' -c:a copy -c:v copy output.avi
  ```

- 以 1080i50 10 位采集视频片段：

  ``` text
  ffmpeg -raw_format yuv422p10 -format_code Hi50 -f decklink -i 'UltraStudio Mini Recorder' -c:a copy -c:v copy output.avi
  ```

- 以 1080i50 和 16 个音频声道采集视频片段：

  ``` text
  ffmpeg -channels 16 -format_code Hi50 -f decklink -i 'UltraStudio Mini Recorder' -c:a copy -c:v copy output.avi
  ```

## dshow

Windows DirectShow 输入设备。

FFmpeg 使用 mingw-w64 项目构建时启用 DirectShow 支持。当前仅支持音频和视频设备。

可以将多个设备打开为单独的输入，但也可以在同一输入上打开它们，这应当会改善它们之间的同步性。

输入名称应采用如下格式：

``` text
TYPE=NAME[:TYPE=NAME]
```

其中 \<TYPE\> 可以为 \<audio\> 或 \<video\>，\<NAME\> 是设备的名称或替代名称。

### 选项

如果未指定选项，则使用设备默认值。如果设备不支持所请求的选项，将无法打开。

- **`video_size`** 设置采集视频中的视频大小。

- **`framerate`** 设置采集视频中的帧率。

- **`sample_rate`** 设置采集音频的采样率（Hz）。

- **`sample_size`** 设置采集音频的采样大小（位）。

- **`channels`** 设置采集音频中的声道数。

- **`list_devices`** 若设为 `true`，打印设备列表并退出。

- **`list_options`** 若设为 `true`，打印所选设备的选项列表并退出。

- **`video_device_number`** 为同名设备设置视频设备编号（从 0 开始，默认为 0）。

- **`audio_device_number`** 为同名设备设置音频设备编号（从 0 开始，默认为 0）。

- **`pixel_format`** 选择 DirectShow 使用的像素格式。仅在视频编解码器未设置或设置为 rawvideo 时才能设置此项。

- **`audio_buffer_size`** 设置音频设备缓冲区大小（毫秒），这会直接影响延迟（取决于设备）。默认使用音频设备的默认缓冲区大小（通常为 500ms 的某个倍数）。将此值设置得过低会降低性能。另请参见 <http://msdn.microsoft.com/en-us/library/windows/desktop/dd377582(v=vs.85).aspx>

- **`video_pin_name`** 按名称或替代名称选择要使用的视频采集引脚。

- **`audio_pin_name`** 按名称或替代名称选择要使用的音频采集引脚。

- **`crossbar_video_input_pin_number`** 选择交叉开关设备的视频输入引脚编号。它将被路由到交叉开关设备的 Video Decoder 输出引脚。注意，更改此值会影响后续调用（设置新默认值），直到系统重启。

- **`crossbar_audio_input_pin_number`** 选择交叉开关设备的音频输入引脚编号。它将被路由到交叉开关设备的 Audio Decoder 输出引脚。注意，更改此值会影响后续调用（设置新默认值），直到系统重启。

- **`show_video_device_dialog`** 若设为 `true`，在采集开始前向最终用户弹出显示对话框，允许其手动更改视频滤镜属性和配置。注意，对于交叉开关设备，有时可能需要在此对话框中调整值，以便在 PAL (25 fps) 与 NTSC (29.97) 输入帧率、尺寸、隔行扫描等之间切换。更改这些值可以启用不同的扫描率/帧率，避免底部绿条、扫描线闪烁等问题。注意，对某些设备而言，更改这些属性也会影响后续调用（设置新默认值），直到系统重启。

- **`show_audio_device_dialog`** 若设为 `true`，在采集开始前向最终用户弹出显示对话框，允许其手动更改音频滤镜属性和配置。

- **`show_video_crossbar_connection_dialog`** 若设为 `true`，在打开视频设备前向最终用户弹出显示对话框，允许其手动修改交叉开关引脚路由。

- **`show_audio_crossbar_connection_dialog`** 若设为 `true`，在打开音频设备前向最终用户弹出显示对话框，允许其手动修改交叉开关引脚路由。

- **`show_analog_tv_tuner_dialog`** 若设为 `true`，在采集开始前向最终用户弹出显示对话框，允许其手动修改电视频道和频率。

- **`show_analog_tv_tuner_audio_dialog`** 若设为 `true`，在采集开始前向最终用户弹出显示对话框，允许其手动修改电视音频（如单声道与立体声、语言 A、B 或 C）。

- **`audio_device_load`** 从文件加载音频采集滤镜设备，而不是按名称搜索。如果滤镜支持将其属性序列化，也可以加载其他参数。要使用此项，必须指定音频采集源，但它可以是任何东西，即使是伪造的。

- **`audio_device_save`** 将当前使用的音频采集滤镜设备及其参数（如果滤镜支持）保存到文件。如果存在同名文件，将被覆盖。

- **`video_device_load`** 从文件加载视频采集滤镜设备，而不是按名称搜索。如果滤镜支持将其属性序列化，也可以加载其他参数。要使用此项，必须指定视频采集源，但它可以是任何东西，即使是伪造的。

- **`video_device_save`** 将当前使用的视频采集滤镜设备及其参数（如果滤镜支持）保存到文件。如果存在同名文件，将被覆盖。

- **`use_video_device_timestamps`** 若设为 `false`，视频帧的时间戳将源自墙钟 (wallclock) 而不是采集设备提供的时间戳。这允许绕过提供不可靠时间戳的设备。

### 示例

- 打印 DirectShow 支持的设备列表并退出：

  ``` text
  $ ffmpeg -list_devices true -f dshow -i dummy
  ```

- 打开视频设备 \<Camera\>：

  ``` text
  $ ffmpeg -f dshow -i video="Camera"
  ```

- 打开名为 \<Camera\> 的第二个视频设备：

  ``` text
  $ ffmpeg -f dshow -video_device_number 1 -i video="Camera"
  ```

- 打开视频设备 \<Camera\> 和音频设备 \<Microphone\>：

  ``` text
  $ ffmpeg -f dshow -i video="Camera":audio="Microphone"
  ```

- 打印所选设备支持的选项列表并退出：

  ``` text
  $ ffmpeg -list_options true -f dshow -i video="Camera"
  ```

- 按名称或替代名称指定要采集的引脚名称，并指定替代设备名称：

  ``` text
  $ ffmpeg -f dshow -audio_pin_name "Audio Out" -video_pin_name 2 -i video=video="@device_pnp_\\?\pci#ven_1a0a&dev_6200&subsys_62021461&rev_01#4&e2c7dd6&0&00e1#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\{ca465100-deb0-4d59-818f-8c477184adf6}":audio="Microphone"
  ```

- 配置交叉开关设备，指定交叉开关引脚，并允许用户在启动时调整视频采集属性：

  ``` text
  $ ffmpeg -f dshow -show_video_device_dialog true -crossbar_video_input_pin_number 0
       -crossbar_audio_input_pin_number 3 -i video="AVerMedia BDA Analog Capture":audio="AVerMedia BDA Analog Capture"
  ```

## fbdev

Linux framebuffer 输入设备。

Linux framebuffer 是一个与图形硬件无关的抽象层，用于在计算机显示器（通常在控制台上）显示图形。它通过文件设备节点访问，通常是 `/dev/fb0`。

更详细的信息请阅读 Linux 源码树中的 Documentation/fb/framebuffer.txt 文件。

另请参见 <http://linux-fbdev.sourceforge.net/> 与 fbset(1)。

要用 `ffmpeg` 从 framebuffer 设备 `/dev/fb0` 录制：

``` text
ffmpeg -f fbdev -framerate 10 -i /dev/fb0 out.avi
```

可以使用以下命令截取单张屏幕截图：

``` text
ffmpeg -f fbdev -framerate 1 -i /dev/fb0 -frames:v 1 screenshot.jpeg
```

### 选项

| Term        | Description                        |
|-------------|------------------------------------|
| `framerate` | 设置帧率。默认为 25。 |

## gdigrab

Win32 GDI 屏幕采集设备。

此设备允许您在 Windows 上采集显示器的某个区域。

输入文件名的选项包括如下元素：

``` text
desktop
```

或

``` text
title=window_title
```

或

``` text
hwnd=window_hwnd
```

第一个选项将采集整个桌面，或桌面的固定区域。第二和第三个选项则采集单个窗口的内容，无论其在屏幕上的位置如何。

例如，要用 `ffmpeg` 抓取整个桌面：

``` text
ffmpeg -f gdigrab -framerate 6 -i desktop out.mpg
```

抓取位于 `10,20` 位置的 640x480 区域：

``` text
ffmpeg -f gdigrab -framerate 6 -offset_x 10 -offset_y 20 -video_size vga -i desktop out.mpg
```

抓取名为 "Calculator" 的窗口的内容

``` text
ffmpeg -f gdigrab -framerate 6 -i title=Calculator out.mpg
```

### 选项

- **`draw_mouse`** 指定是否绘制鼠标指针。使用值 `0` 表示不绘制指针。默认值为 `1`。

- **`framerate`** 设置抓取帧率。默认值为 `ntsc`，对应帧率 `30000/1001`。

- **`show_region`** 在屏幕上显示抓取的区域。

  如果指定 \<show_region\> 为 `1`，抓取区域将在屏幕上标示。使用此选项，在仅抓取屏幕一部分时可以很容易地知道正在抓取什么。

  注意，\<show_region\> 与抓取单个窗口的内容不兼容。

  例如：

  ``` text
  ffmpeg -f gdigrab -show_region 1 -framerate 6 -video_size cif -offset_x 10 -offset_y 20 -i desktop out.mpg
  ```

- **`video_size`** 设置视频帧大小。默认情况下，若选择了 `desktop`，则采集全屏；若选择了 `title=window_title`，则采集完整窗口大小。

- **`offset_x`** 与 \<video_size\> 配合采集区域时，设置与屏幕或桌面左边缘的距离。

  注意，在 Windows 上偏移计算从主显示器的左上角开始。如果您的显示器位于主显示器左侧，则需要使用负的 \<offset_x\> 值将区域移动到该显示器。

- **`offset_y`** 与 \<video_size\> 配合采集区域时，设置与屏幕或桌面顶边缘的距离。

  注意，在 Windows 上偏移计算从主显示器的左上角开始。如果您的显示器位于主显示器上方，则需要使用负的 \<offset_y\> 值将区域移动到该显示器。

## iec61883

使用 libiec61883 的 FireWire DV/HDV 输入设备。

要启用此输入设备，需要在系统上安装 libiec61883、libraw1394 和 libavc1394。使用 configure 选项 `--enable-libiec61883` 以启用该设备进行编译。

iec61883 采集设备支持从经 IEEE1394 (FireWire) 连接的视频设备采集，使用 libiec61883 和新的 Linux FireWire 协议栈 (juju)。自旧 FireWire 协议栈被移除以来，这是 Linux Kernel 2.6.37 及以后版本中默认的 DV/HDV 输入方法。

将要使用的 FireWire 端口指定为输入文件，或指定 "auto" 以选择第一个已连接的端口。

### 选项

- **`dvtype`** 覆盖 DV/HDV 自动检测。仅应在自动检测不起作用或应禁止使用不同设备类型时使用。将 DV 设备当作 HDV 处理（或反之）不会起作用，并导致未定义的行为。支持的值为 `auto`、`dv` 和 `hdv`。

- **`dvbuffer`** 设置传入数据缓冲区的最大大小（以帧计）。对 DV 而言这是精确值。对 HDV 而言不是帧精确的，因为 HDV 没有固定的帧大小。

- **`dvguid`** 通过指定 GUID 选择采集设备。采集将仅从指定设备进行，如果未找到具有给定 GUID 的设备则失败。当同时连接多个设备时，这有助于选择输入。查看 /sys/bus/firewire/devices 以找出 GUID。

### 示例

- 抓取并显示 FireWire DV/HDV 设备的输入。

  ``` text
  ffplay -f iec61883 -i auto
  ```

- 抓取并录制 FireWire DV/HDV 设备的输入，若源为 HDV 则使用 100000 个数据包的数据包缓冲区。

  ``` text
  ffmpeg -f iec61883 -i auto -dvbuffer 100000 out.mpg
  ```

## jack

JACK 输入设备。

要在配置期间启用此输入设备，需要在系统上安装 libjack。

JACK 输入设备创建一个或多个 JACK 可写客户端，每个音频声道一个，名称为 \<client_name\>:input\_\<N\>，其中 \<client_name\> 是应用程序提供的名称，\<N\> 是标识声道的编号。每个可写客户端将获取的数据发送到 FFmpeg 输入设备。

创建一个或多个 JACK 可读客户端后，需要将它们连接到一个或多个 JACK 可写客户端。

要连接或断开 JACK 客户端，可以使用 `jack_connect` 和 `jack_disconnect` 程序，或通过图形界面完成，例如使用 `qjackctl`。

要列出 JACK 客户端及其属性，可以调用命令 `jack_lsp`。

以下示例展示如何用 `ffmpeg` 采集 JACK 可读客户端。

``` text
# Create a JACK writable client with name "ffmpeg".
$ ffmpeg -f jack -i ffmpeg -y out.wav

# Start the sample jack_metro readable client.
$ jack_metro -b 120 -d 0.2 -f 4000

# List the current JACK clients.
$ jack_lsp -c
system:capture_1
system:capture_2
system:playback_1
system:playback_2
ffmpeg:input_1
metro:120_bpm

# Connect metro to the ffmpeg writable client.
$ jack_connect metro:120_bpm ffmpeg:input_1
```

更多信息请阅读：<http://jackaudio.org/>

### 选项

| Term       | Description                               |
|------------|-------------------------------------------|
| `channels` | 设置声道数。默认为 2。 |

## kmsgrab

KMS 视频输入设备。

采集与指定 CRTC 或 plane 关联的 KMS 扫描输出帧缓冲，作为可传递给其他硬件功能的 DRM 对象。

运行需要 DRM master 或 CAP_SYS_ADMIN。

如果您不理解这些是什么意思，您可能不需要此设备。请改用 `x11grab`。

### 选项

- **`device`** 要在其上采集的 DRM 设备。默认为 `/dev/dri/card0`。

- **`format`** 帧缓冲的像素格式。如果您运行 Linux 5.7 或更高版本，可以自动检测，但更早的版本需要提供。默认为 `bgr0`，这是 Linux 控制台和 Xorg X 服务器最常用的格式。

- **`format_modifier`** 在输出帧上标记的格式修饰符 (format modifier)。某些 API 需要它才能正确导入。如果您运行 Linux 5.7 或更高版本，可以自动检测，但在更早的版本中需要时必须显式提供。可能的值参见 libdrm 文档。

- **`crtc_id`** 定义采集源的 KMS CRTC ID。将使用给定 CRTC 上的第一个活动 plane。

- **`plane_id`** 定义采集源的 KMS plane ID。若既未指定 `crtc_id` 也未指定 `plane_id`，默认为找到的第一个活动 plane。

- **`framerate`** 采集帧率。它不与任何页面翻转或帧缓冲变更同步——它只定义帧缓冲被采样的时间间隔。采样快于帧缓冲更新速率时，将生成内容相同的独立帧。默认为 `30`。

### 示例

- 从第一个活动 plane 采集，将结果下载为普通帧并编码。仅当帧缓冲既是线性又可映射时才有效——否则结果可能混乱或下载失败。

  ``` text
  ffmpeg -f kmsgrab -i - -vf 'hwdownload,format=bgr0' output.mp4
  ```

- 以 60fps 从 CRTC ID 42 采集，将结果映射到 VAAPI，转换为 NV12 并编码为 H.264。

  ``` text
  ffmpeg -crtc_id 42 -framerate 60 -f kmsgrab -i - -vf 'hwmap=derive_device=vaapi,scale_vaapi=w=1920:h=1080:format=nv12' -c:v h264_vaapi output.mp4
  ```

- 要仅采集 plane 的一部分，可以对输出进行裁剪——只要窗口具有已知的绝对位置和大小，这可用于采集单个窗口。例如，采集并编码 1920x1080 plane 的中间四分之一：

  ``` text
  ffmpeg -f kmsgrab -i - -vf 'hwmap=derive_device=vaapi,crop=960:540:480:270,scale_vaapi=960:540:nv12' -c:v h264_vaapi output.mp4
  ```

## lavfi

Libavfilter 输入虚拟设备。

此输入设备从 libavfilter 滤镜链图的开放输出端口读取数据。

对于滤镜链图的每个开放输出，输入设备都会创建一个对应的流，映射到生成的输出。滤镜链图通过选项 `graph` 指定。

### 选项

- **`graph`** 指定用作输入的滤镜链图。每个视频开放输出都必须由形如 "out\<N\>" 的唯一字符串标记，其中 \<N\> 是从 0 开始的编号，对应设备生成的映射输入流。第一个未标记的输出会自动分配 "out0" 标签，但其余的都需要显式指定。

  可以在输出标签后附加后缀 "+subcc"，以创建一个额外的流，包含附着于该输出的隐藏式字幕数据包（实验性；目前仅支持 EIA-608 / CEA-708）。subcc 流在所有常规流之后创建，顺序与对应流一致。例如，如果有 "out19+subcc"、"out7+subcc" 以及直到 "out42"，则流 \#43 是流 \#7 的 subcc，流 \#44 是流 \#19 的 subcc。

  若未指定，默认为输入设备指定的文件名。

- **`graph_file`** 设置要读取并发送给其他滤镜的滤镜链图文件名。滤镜链图的语法与选项 \<graph\> 指定的相同。

- **`dumpgraph`** 将图转储到 stderr。

### 示例

- 创建彩色视频流并用 `ffplay` 播放：

  ``` text
  ffplay -f lavfi -graph "color=c=pink [out0]" dummy
  ```

- 与上一示例相同，但使用文件名指定滤镜链图描述，并省略 "out0" 标签：

  ``` text
  ffplay -f lavfi color=c=pink
  ```

- 创建三个不同的视频测试滤镜源并播放它们：

  ``` text
  ffplay -f lavfi -graph "testsrc [out0]; testsrc,hflip [out1]; testsrc,negate [out2]" test3
  ```

- 使用 amovie 源从文件读取音频流并用 `ffplay` 播放：

  ``` text
  ffplay -f lavfi "amovie=test.wav"
  ```

- 读取音频流和视频流并用 `ffplay` 播放：

  ``` text
  ffplay -f lavfi "movie=test.avi[out0];amovie=test.wav[out1]"
  ```

- 将解码帧转储为图像，并将隐藏式字幕转储为 RCWT 备份：

  ``` text
  ffmpeg -f lavfi -i "movie=test.ts[out0+subcc]" -map v frame%08d.png -map s -c copy -f rcwt subcc.bin
  ```

## libcdio

基于 libcdio 的 Audio-CD 输入设备。

要在配置期间启用此输入设备，需要在系统上安装 libcdio。它需要 configure 选项 `--enable-libcdio`。

此设备允许从 Audio-CD 播放和抓取。

例如要用 `ffmpeg` 复制 `/dev/sr0` 中的整个 Audio-CD，可以运行命令：

``` text
ffmpeg -f libcdio -i /dev/sr0 cd.wav
```

### 选项

- **`speed`** 设置驱动器读取速度。默认值为 0。

  速度以 CD-ROM 速度单位指定。速度通过 libcdio 的 `cdio_cddap_speed_set` 函数设置。在许多 CD-ROM 驱动器上，指定的值过大会导致使用最快速度。

- **`paranoia_mode`** 设置 paranoid 恢复模式标志。它接受以下值之一：

  - **`disable`**

  - **`verify`**

  - **`overlap`**

  - **`neverskip`**

  - **`full`**

  默认值为 `disable`。

  有关可用恢复模式的更多信息，请查阅 paranoia 项目文档。

## libdc1394

基于 libdc1394 和 libraw1394 的 IIDC1394 输入设备。

需要 configure 选项 `--enable-libdc1394`。

### 选项

- **`framerate`** 设置帧率。默认值为 `ntsc`，对应帧率 `30000/1001`。

- **`pixel_format`** 选择像素格式。默认值为 `uyvy422`。

- **`video_size`** 设置视频大小，以 `640x480` 或 `hd720` 等字符串给出。默认值为 `qvga`。

## openal

OpenAL 输入设备在所有具有可用 OpenAL 1.1 实现的系统上提供音频采集。

要在配置期间启用此输入设备，需要在系统上安装 OpenAL 头文件和库，并需要以 `--enable-openal` 配置 FFmpeg。

OpenAL 头文件和库应作为 OpenAL 实现的一部分提供，或作为额外的下载（SDK）提供。根据您的安装情况，您可能需要通过 `--extra-cflags` 和 `--extra-ldflags` 指定额外的标志，以让构建系统找到 OpenAL 头文件和库。

以下是 OpenAL 实现的不完整列表：

- ****Creative**** 官方 Windows 实现，在支持的设备上提供硬件加速，并有软件回退。参见 <http://openal.org/>。

- ****OpenAL Soft**** 便携的开源 (LGPL) 软件实现。包含面向 Windows、Linux、Solaris 和 BSD 操作系统上最常见声音 API 的后端。参见 <http://kcat.strangesoft.net/openal.html>。

- ****Apple**** OpenAL 是 Core Audio（Mac OS X 官方音频接口）的一部分。参见 <http://developer.apple.com/technologies/mac/audio-and-video.html>

此设备允许从经 OpenAL 处理的音频输入设备采集。

您需要在提供的文件名中指定要采集的设备名称。如果提供空字符串，设备将自动选择默认设备。可以使用选项 \<list_devices\> 获取支持的设备列表。

### 选项

- **`channels`** 设置采集音频中的声道数。当前仅支持值 `1`（单声道）和 `2`（立体声）。默认为 `2`。

- **`sample_size`** 设置采集音频的采样大小（位）。当前仅支持值 `8` 和 `16`。默认为 `16`。

- **`sample_rate`** 设置采集音频的采样率（Hz）。默认为 `44.1k`。

- **`list_devices`** 若设为 `true`，打印设备列表并退出。默认为 `false`。

### 示例

打印 OpenAL 支持的设备列表并退出：

``` text
$ ffmpeg -list_devices true -f openal -i dummy out.ogg
```

从 OpenAL 设备 `DR-BT101 via PulseAudio` 采集：

``` text
$ ffmpeg -f openal -i 'DR-BT101 via PulseAudio' out.ogg
```

从默认设备采集（注意文件名为空字符串 "）：

``` text
$ ffmpeg -f openal -i '' out.ogg
```

在同一 `ffmpeg` 命令内同时从两个设备采集，写入两个不同的文件：

``` text
$ ffmpeg -f openal -i 'DR-BT101 via PulseAudio' out1.ogg -f openal -i 'ALSA Default' out2.ogg
```

注意：并非所有 OpenAL 实现都支持多个同时采集——如果上述命令不起作用，请尝试最新的 OpenAL Soft。

## oss

Open Sound System 输入设备。

提供给输入设备的文件名是代表 OSS 输入设备的设备节点，通常设置为 `/dev/dsp`。

例如要用 `ffmpeg` 从 `/dev/dsp` 抓取，使用命令：

``` text
ffmpeg -f oss -i /dev/dsp /tmp/oss.wav
```

关于 OSS 的更多信息参见：<http://manuals.opensound.com/usersguide/dsp.html>

### 选项

| Term          | Description                                  |
|---------------|----------------------------------------------|
| `sample_rate` | 设置采样率（Hz）。默认为 48000。 |
| `channels`    | 设置声道数。默认为 2。    |

## pulse

PulseAudio 输入设备。

要启用此输出设备，需要以 `--enable-libpulse` 配置 FFmpeg。

提供给输入设备的文件名是一个源设备或字符串 "default"

要列出 PulseAudio 源设备及其属性，可以调用命令 `pactl list sources`。

关于 PulseAudio 的更多信息参见 <http://www.pulseaudio.org>。

### 选项

- **`server`** 连接到特定的 PulseAudio 服务器，由 IP 地址指定。未提供时使用默认服务器。

- **`name`** 指定 PulseAudio 显示活动客户端时使用的应用程序名称，默认为 `LIBAVFORMAT_IDENT` 字符串。

- **`stream_name`** 指定 PulseAudio 显示活动流时使用的流名称，默认为 "record"。

- **`sample_rate`** 以 Hz 指定采样率，默认使用 48kHz。

- **`channels`** 指定使用的声道，默认为 2（立体声）。

- **`frame_size`** 此选项无任何作用，已弃用。

- **`fragment_size`** 以字节指定 PulseAudio 中最小缓冲分片的大小，它会影响音频延迟。默认设置为 50 ms 的数据量。

- **`wallclock`** 使用当前时间设置初始 PTS。默认为 1。

### 示例

从默认设备录制流：

``` text
ffmpeg -f pulse -i default /tmp/pulse.wav
```

## sndio

sndio 输入设备。

要在配置期间启用此输入设备，需要在系统上安装 libsndio。

提供给输入设备的文件名是代表 sndio 输入设备的设备节点，通常设置为 `/dev/audio0`。

例如要用 `ffmpeg` 从 `/dev/audio0` 抓取，使用命令：

``` text
ffmpeg -f sndio -i /dev/audio0 /tmp/oss.wav
```

### 选项

| Term          | Description                                  |
|---------------|----------------------------------------------|
| `sample_rate` | 设置采样率（Hz）。默认为 48000。 |
| `channels`    | 设置声道数。默认为 2。    |

## video4linux2, v4l2

Video4Linux2 输入视频设备。

"v4l2" 可以用作 "video4linux2" 的别名。

如果 FFmpeg 构建时带有 v4l-utils 支持（通过使用 `--enable-libv4l2` configure 选项），可以将它与 `-use_libv4l2` 输入设备选项一起使用。

要抓取的设备名称是文件设备节点，Linux 系统通常在设备（例如 USB 摄像头）插入系统时自动创建此类节点，名称形如 `/dev/videoN`，其中 \<N\> 是与设备关联的编号。

Video4Linux2 设备通常支持有限的 \<width\>x\<height\> 尺寸和帧率集合。可以使用 `-list_formats all` 检查 Video4Linux2 设备支持哪些。某些设备（如电视卡）支持一种或多种制式。可以使用 `-list_standards all` 列出所有支持的制式。

时间戳的时间基为 1 微秒。根据内核版本和配置，时间戳可能源自实时时钟（起点为 Unix 纪元）或单调时钟（起点通常为启动时间，不受 NTP 或手动时钟更改影响）。`-timestamps abs` 或 `-ts abs` 选项可用于强制转换为实时时钟。

video4linux2 设备与 `ffmpeg` 和 `ffplay` 的一些用法示例：

- 列出 video4linux2 设备支持的格式：

  ``` text
  ffplay -f video4linux2 -list_formats all /dev/video0
  ```

- 抓取并显示 video4linux2 设备的输入：

  ``` text
  ffplay -f video4linux2 -framerate 30 -video_size hd720 /dev/video0
  ```

- 抓取并录制 video4linux2 设备的输入，保留先前设置的帧率和尺寸：

  ``` text
  ffmpeg -f video4linux2 -input_format mjpeg -i /dev/video0 out.mpeg
  ```

关于 Video4Linux 的更多信息，请查看 <http://linuxtv.org/>。

### 选项

- **`standard`** 设置制式。必须是受支持制式的名称。要获取支持的制式列表，使用 `list_standards` 选项。

- **`channel`** 设置输入声道编号。默认为 -1，表示使用先前选择的声道。

- **`video_size`** 设置视频帧大小。参数必须是 \<WIDTH\>x\<HEIGHT\> 形式的字符串或有效的尺寸缩写。

- **`pixel_format`** 选择像素格式（仅对原始视频输入有效）。

- **`input_format`** 设置首选像素格式（针对原始视频）或编解码器名称。当有多个可用格式时，此选项允许选择输入格式。

- **`framerate`** 设置首选视频帧率。

- **`list_formats`** 列出可用格式（支持的像素格式、编解码器和帧尺寸）并退出。

  可用值有：

  | Term | Description |
  |----|----|
  | `all` | 显示所有可用（压缩与非压缩）格式。 |
  | `raw` | 仅显示原始视频（非压缩）格式。 |
  | `compressed` | 仅显示压缩格式。 |

- **`list_standards`** 列出支持的制式并退出。

  可用值有：

  | Term    | Description                   |
  |---------|-------------------------------|
  | `all` | 显示所有支持的制式。 |

- **`timestamps, ts`** 设置抓取帧的时间戳类型。

  可用值有：

  | Term         | Description                                             |
  |--------------|---------------------------------------------------------|
  | `default`  | 使用来自内核的时间戳。                         |
  | `abs`      | 使用绝对时间戳（墙钟）。                   |
  | `mono2abs` | 强制从单调时钟转换为绝对时间戳。 |

  默认值为 `default`。

- **`use_libv4l2`** 使用 libv4l2 (v4l-utils) 转换函数。默认为 0。

## vfwcap

VfW (Video for Windows) 采集输入设备。

作为输入传递的文件名是采集驱动器编号，范围为 0 到 9。可以使用 "list" 作为文件名以打印驱动器列表。任何其他文件名将被解释为设备编号 0。

### 选项

- **`video_size`** 设置视频帧大小。

- **`framerate`** 设置抓取帧率。默认值为 `ntsc`，对应帧率 `30000/1001`。

## x11grab

X11 视频输入设备。

要在配置期间启用此输入设备，需要在系统上安装 libxcb。它会在配置期间自动检测。

此设备允许采集 X11 显示器的某个区域。

作为输入传递的文件名具有如下语法：

``` text
[hostname]:display_number.screen_number[+x_offset,y_offset]
```

\<hostname\>:\<display_number\>.\<screen_number\> 指定要抓取的屏幕的 X11 显示名称。\<hostname\> 可以省略，默认为 "localhost"。环境变量 `DISPLAY` 包含默认显示名称。

\<x_offset\> 和 \<y_offset\> 指定抓取区域相对于 X11 屏幕左上边框的偏移量。它们默认为 0。

详细信息请查看 X11 文档（例如 `man X`）。

使用 `xdpyinfo` 程序获取 X11 显示器属性的基本信息（例如 grep "name" 或 "dimensions"）。

例如要用 `ffmpeg` 从 `:0.0` 抓取：

``` text
ffmpeg -f x11grab -framerate 25 -video_size cif -i :0.0 out.mpg
```

在位置 `10,20` 抓取：

``` text
ffmpeg -f x11grab -framerate 25 -video_size cif -i :0.0+10,20 out.mpg
```

### 选项

- **`select_region`** 指定是否使用指针以图形方式选择抓取区域。值为 `1` 时提示用户通过点击并拖动以图形方式选择抓取区域。单击且不拖动将选择整个屏幕。宽度或高度为零的区域也将选择整个屏幕。此选项会覆盖 \<video_size\>、\<grab_x\> 和 \<grab_y\> 选项。默认值为 `0`。

- **`draw_mouse`** 指定是否绘制鼠标指针。值为 `0` 表示不绘制指针。默认值为 `1`。

- **`follow_mouse`** 让抓取区域跟随鼠标。参数可以是 `centered` 或像素数 \<PIXELS\>。

  当指定为 "centered" 时，抓取区域跟随鼠标指针，并将指针保持在区域中心；否则，仅当鼠标指针到达距区域边缘 \<PIXELS\>（大于零）以内时区域才跟随。

  例如：

  ``` text
  ffmpeg -f x11grab -follow_mouse centered -framerate 25 -video_size cif -i :0.0 out.mpg
  ```

  仅当鼠标指针到达距边缘 100 像素以内时才跟随：

  ``` text
  ffmpeg -f x11grab -follow_mouse 100 -framerate 25 -video_size cif -i :0.0 out.mpg
  ```

- **`framerate`** 设置抓取帧率。默认值为 `ntsc`，对应帧率 `30000/1001`。

- **`show_region`** 在屏幕上显示抓取的区域。

  如果指定 \<show_region\> 为 `1`，抓取区域将在屏幕上标示。使用此选项，在仅抓取屏幕一部分时可以很容易地知道正在抓取什么。

- **`region_border`** 使用 `-show_region 1` 时设置区域边框厚度。范围为 1 到 128，默认为 3（仅限基于 XCB 的 x11grab）。

  例如：

  ``` text
  ffmpeg -f x11grab -show_region 1 -framerate 25 -video_size cif -i :0.0+10,20 out.mpg
  ```

  配合 \<follow_mouse\>：

  ``` text
  ffmpeg -f x11grab -follow_mouse centered -show_region 1 -framerate 25 -video_size cif -i :0.0 out.mpg
  ```

- **`window_id`** 抓取此窗口，而不是整个屏幕。默认值为 0，映射到整个屏幕（根窗口）。

  可以使用 `xwininfo` 程序（可能配合 -tree 和 -root 选项）找到窗口的 id。

  如果窗口随后被放大，新区域不会被录制。视频在窗口关闭、取消映射（即最小化）或缩小到视频尺寸以下（默认为初始窗口尺寸）时结束。

  此选项会禁用 `follow_mouse` 和 `select_region` 选项。

- **`video_size`** 设置视频帧大小。默认为整个桌面或窗口。

- **`grab_x`**

- **`grab_y`** 设置抓取区域坐标。它们表示为相对于 X11 窗口左上角的偏移量，对应设备名称中的 \<x_offset\> 和 \<y_offset\> 参数。两个选项的默认值均为 0。

# 输出设备

输出设备是 FFmpeg 中的可配置元素，可将多媒体数据写入系统所连的输出设备。

配置 FFmpeg 构建时，所有支持的输出设备默认启用。可以使用 configure 选项 "–list-outdevs" 列出所有可用的设备。

可以使用 configure 选项 "–disable-outdevs" 禁用所有输出设备，使用选项 "–enable-outdev=\<OUTDEV\>" 选择性启用某个输出设备，或者使用选项 "–disable-outdev=\<OUTDEV\>" 禁用特定输入设备。

ff\* 工具的选项 "-devices" 将显示已启用的输出设备列表。

以下是对当前可用输出设备的描述。

## alsa

ALSA (Advanced Linux Sound Architecture) 输出设备。

### 示例

- 在默认 ALSA 设备上播放文件：

  ``` text
  ffmpeg -i INPUT -f alsa default
  ```

- 在声卡 1 的音频设备 7 上播放文件：

  ``` text
  ffmpeg -i INPUT -f alsa hw:1,7
  ```

## AudioToolbox

AudioToolbox 输出设备。

允许在 OSX 上对 CoreAudio 设备进行原生输出。

输出文件名可以为空（或 `-`）以指代默认系统输出设备，或为一个数字，指代使用 `-list_devices true` 显示的设备索引。

也可以使用 `-audio_device_index <INDEX>` 按索引选择音频输入设备，覆盖输出文件名中给出的任何设备名称或索引。

可以使用 `-list_devices true` 枚举所有可用设备，列出所有设备名称、UID 及对应索引。

### 选项

AudioToolbox 支持以下选项：

- **`-audio_device_index <INDEX>`** 按索引指定音频设备。覆盖输出文件名中给出的任何内容。

### 示例

- 打印支持的设备列表并向默认设备输出正弦波：

  ``` text
  $ ffmpeg -f lavfi -i sine=r=44100 -f audiotoolbox -list_devices true -
  ```

- 向索引为 2 的设备输出正弦波，覆盖任何输出文件名：

  ``` text
  $ ffmpeg -f lavfi -i sine=r=44100 -f audiotoolbox -audio_device_index 2 -
  ```

## caca

CACA 输出设备。

此输出设备允许在 CACA 窗口中显示视频流。每个应用程序只允许一个 CACA 窗口，因此一个应用程序中只能有此输出设备的一个实例。

要启用此输出设备，需要以 `--enable-libcaca` 配置 FFmpeg。libcaca 是一个输出文本而非像素的图形库。

关于 libcaca 的更多信息，请查看：<http://caca.zoy.org/wiki/libcaca>

### 选项

- **`window_title`** 设置 CACA 窗口标题，若未指定，默认为输出设备指定的文件名。

- **`window_size`** 设置 CACA 窗口大小，可以是 \<width\>x\<height\> 形式的字符串或视频尺寸缩写。若未指定，默认为输入视频的尺寸。

- **`driver`** 设置显示驱动器。

- **`algorithm`** 设置抖动算法。抖动是必要的，因为被渲染的图片通常包含的颜色远多于可用调色板。可接受的值用 `-list_dither algorithms` 列出。

- **`antialias`** 设置抗锯齿方法。抗锯齿使渲染的图像更平滑，避免常见的阶梯效应。可接受的值用 `-list_dither antialiases` 列出。

- **`charset`** 设置渲染文本时使用的字符。可接受的值用 `-list_dither charsets` 列出。

- **`color`** 设置渲染文本时使用的颜色。可接受的值用 `-list_dither colors` 列出。

- **`list_drivers`** 若设为 `true`，打印可用驱动器列表并退出。

- **`list_dither`** 列出与参数相关的可用抖动选项。参数必须是 `algorithms`、`antialiases`、`charsets`、`colors` 之一。

### 示例

- 以下命令显示 `ffmpeg` 输出到一个 CACA 窗口，强制其尺寸为 80x25：

  ``` text
  ffmpeg -i INPUT -c:v rawvideo -pix_fmt rgb24 -window_size 80x25 -f caca -
  ```

- 显示可用驱动器列表并退出：

  ``` text
  ffmpeg -i INPUT -pix_fmt rgb24 -f caca -list_drivers true -
  ```

- 显示可用抖动颜色列表并退出：

  ``` text
  ffmpeg -i INPUT -pix_fmt rgb24 -f caca -list_dither colors -
  ```

## decklink

decklink 输出设备为 Blackmagic DeckLink 设备提供播放功能。

要启用此输出设备，需要 Blackmagic DeckLink SDK，并需要使用相应的 `--extra-cflags` 和 `--extra-ldflags` 进行配置。在 Windows 上，需要通过 `widl` 运行 IDL 文件。

DeckLink 对其支持的格式非常挑剔。像素格式始终为 uyvy422，帧率、场序和视频尺寸必须用 `-list_formats 1` 为您的设备确定。音频采样率始终为 48 kHz。

### 选项

- **`list_devices`** 若设为 `true`，打印设备列表并退出。默认为 `false`。此选项已弃用，请使用 ffmpeg 的 `-sinks` 选项列出可用的输出设备。

- **`list_formats`** 若设为 `true`，打印支持的格式列表并退出。默认为 `false`。

- **`preroll`** 视频预卷时间量（秒）。默认为 `0.5`。

- **`duplex_mode`** 设置 decklink 设备的双工/配置档 (profile) 模式。必须为 `unset`、`half`、`full`、`one_sub_device_full`、`one_sub_device_half`、`two_sub_device_full`、`four_sub_device_half`。默认为 `unset`。

  注意：DeckLink SDK 11.0 已用配置档属性取代双工属性。对于 DeckLink Duo 2 和 DeckLink Quad 2，配置档在使用相同连接器的任意 2 个子设备之间共享。对于 DeckLink 8K Pro，配置档在全部 4 个子设备之间共享，因此 DeckLink 8K Pro 支持四个配置档。

  DeckLink 8K Pro 的有效配置档模式（DeckLink SDK \>= 11.0）：`one_sub_device_full`、`one_sub_device_half`、`two_sub_device_full`、`four_sub_device_half`

  DeckLink Quad 2 和 DeckLink Duo 2 的有效配置档模式：`half`、`full`

- **`timing_offset`** 在所用输出上设置 genlock 时序像素偏移。默认为 `unset`。

- **`link`** 在所用输出上设置 SDI 视频链路配置。必须为 `unset`、`single` link SDI、`dual` link SDI 或 `quad` link SDI。默认为 `unset`。

- **`sqd`** 为四链路 SDI 输出启用方形分割四路拆分 (Square Division Quad Split) 模式。必须为 `unset`、`true` 或 `false`。默认为 `unset`。

- **`level_a`** 在所用输出上启用 SMPTE Level A 模式。必须为 `unset`、`true` 或 `false`。默认为 `unset`。

- **`vanc_queue_size`** 设置 VANC 数据的最大输出缓冲区大小（字节）。如果缓冲达到该值，传出的 VANC 数据将被丢弃。默认为 `1048576`。

### 示例

- 列出输出设备：

  ``` text
  ffmpeg -sinks decklink
  ```

- 列出支持的格式：

  ``` text
  ffmpeg -i test.avi -f decklink -list_formats 1 'DeckLink Mini Monitor'
  ```

- 播放视频片段：

  ``` text
  ffmpeg -i test.avi -f decklink -pix_fmt uyvy422 'DeckLink Mini Monitor'
  ```

- 以非标准帧率或视频尺寸播放视频片段：

  ``` text
  ffmpeg -i test.avi -f decklink -pix_fmt uyvy422 -s 720x486 -r 24000/1001 'DeckLink Mini Monitor'
  ```

## fbdev

Linux framebuffer 输出设备。

Linux framebuffer 是一个与图形硬件无关的抽象层，用于在计算机显示器（通常在控制台上）显示图形。它通过文件设备节点访问，通常是 `/dev/fb0`。

更详细的信息请阅读 Linux 源码树中的 `Documentation/fb/framebuffer.txt` 文件。

### 选项

- **`xoffset`**

- **`yoffset`** 设置左上角的 x/y 坐标。默认为 0。

### 示例

在 framebuffer 设备 `/dev/fb0` 上播放文件。所需的像素格式取决于当前 framebuffer 设置。

``` text
ffmpeg -re -i INPUT -c:v rawvideo -pix_fmt bgra -f fbdev /dev/fb0
```

另请参见 <http://linux-fbdev.sourceforge.net/> 与 fbset(1)。

## oss

OSS (Open Sound System) 输出设备。

## pulse

PulseAudio 输出设备。

要启用此输出设备，需要以 `--enable-libpulse` 配置 FFmpeg。

关于 PulseAudio 的更多信息参见 <http://www.pulseaudio.org>

### 选项

- **`server`** 连接到特定的 PulseAudio 服务器，由 IP 地址指定。未提供时使用默认服务器。

- **`name`** 指定 PulseAudio 显示活动客户端时使用的应用程序名称，默认为 `LIBAVFORMAT_IDENT` 字符串。

- **`stream_name`** 指定 PulseAudio 显示活动流时使用的流名称，默认设置为指定的输出名称。

- **`device`** 指定要使用的设备。未提供时使用默认设备。输出设备列表可用命令 `pactl list sinks` 获得。

- **`buffer_size`**

- **`buffer_duration`** 控制 PulseAudio 缓冲区的大小和持续时间。小缓冲区提供更多控制，但需要更频繁的更新。

  `buffer_size` 以字节指定大小，而 `buffer_duration` 以毫秒指定持续时间。

  同时提供两个选项时使用较大值（时长会使用流参数换算为字节）。若它们被设为 0（默认值），设备将使用默认的 PulseAudio 时长值。PulseAudio 默认将缓冲时长设为约 2 秒。

- **`prebuf`** 以字节指定预缓冲大小。在缓冲区中至少有 `prebuf` 字节可用之前，服务器不会开始播放。默认情况下，此选项初始化为与 `buffer_size` 或 `buffer_duration`（取较大者）相同的值。

- **`minreq`** 以字节指定最小请求大小。服务器向客户端请求的字节数不会少于 `minreq`，而是等待缓冲区空闲到足以一次请求更多字节。建议不设置此选项，它将初始化为服务器认为合理的值。

### 示例

在默认服务器的默认设备上播放文件：

``` text
ffmpeg  -i INPUT -f pulse "stream name"
```

## sndio

sndio 音频输出设备。

## v4l2

Video4Linux2 输出设备。

## xv

XV (XVideo) 输出设备。

此输出设备允许在 X Window System 窗口中显示视频流。

### 选项

- **`display_name`** 指定硬件显示名称，它决定要使用的显示器和通信域。

  显示名称或 DISPLAY 环境变量可以是 \<hostname\>\[:\<number\>\[.\<screen_number\>\]\] 格式的字符串。

  \<hostname\> 指定显示器物理连接的主机名。\<number\> 指定该主机上显示服务器的编号。\<screen_number\> 指定该服务器上要使用的屏幕。

  若未指定，默认为 DISPLAY 环境变量的值。

  例如，`dual-headed:0.1` 表示名为 "dual-headed" 的机器上显示器 0 的屏幕 1。

  有关显示名称格式的更详细信息，请查看 X11 规范。

- **`window_id`** 设为非零值时，设备不创建新窗口，而是使用提供的 \<window_id\> 对应的现有窗口。默认情况下此选项设为零，设备创建自己的窗口。

- **`window_size`** 设置创建的窗口大小，可以是 \<width\>x\<height\> 形式的字符串或视频尺寸缩写。若未指定，默认为输入视频的尺寸。设置 \<window_id\> 时忽略。

- **`window_x`**

- **`window_y`** 设置创建窗口的 X 和 Y 偏移。两者默认均为 0。这些值可能被窗口管理器忽略。设置 \<window_id\> 时忽略。

- **`window_title`** 设置窗口标题，若未指定，默认为输出设备指定的文件名。设置 \<window_id\> 时忽略。

关于 XVideo 的更多信息参见 <http://www.x.org/>。

### 示例

- 用 `ffmpeg` 同时解码、显示和编码视频输入：

  ``` text
  ffmpeg -i INPUT OUTPUT -f xv display
  ```

- 将输入视频解码并显示到多个 X11 窗口：

  ``` text
  ffmpeg -i INPUT -f xv normal -vf negate -f xv negated
  ```

# 另请参见

ffmpeg(1), ffplay(1), ffprobe(1), libavdevice(3)
