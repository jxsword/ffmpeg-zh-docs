## 流说明符

有些选项按流生效，例如码率或编解码器。流说明符用于精确指定某个选项属于哪条（些）流。

流说明符是一个字符串，通常附加在选项名之后、以冒号与之分隔。例如 `-codec:a:1 ac3` 包含流说明符 `a:1`，匹配第二条音频流，因此会为第二条音频流选择 ac3 编解码器。

流说明符可以匹配多条流，从而该选项会应用于所有匹配的流。例如 `-b:a 128k` 中的流说明符匹配所有音频流。

空的流说明符匹配所有流。例如 `-codec copy` 或 `-codec: copy` 将不重编码地复制所有流。

流说明符的可能形式有：

- **`stream_index`** 匹配具有此索引的流。例如 `-threads:1 4` 会把第二条流的线程数设为 4。若 \<stream_index\> 作为附加流说明符使用（见下文），则从匹配的流中选取第 \<stream_index\> 条流。流编号基于 libavformat 检测到流的顺序；但同时指定了流组说明符或节目 ID 时，基于该组或该节目内流的顺序。

- **`stream_type[:additional_stream_specifier]`** \<stream_type\> 为以下之一：'v' 或 'V' 表示视频，'a' 表示音频，'s' 表示字幕，'d' 表示数据，'t' 表示附件。'v' 匹配所有视频流，'V' 只匹配非附加图片、视频缩略图或封面的视频流。若使用 \<additional_stream_specifier\>，则匹配既属于该类型又匹配 \<additional_stream_specifier\> 的流；否则，匹配该类型的所有流。

- **`g:group_specifier[:additional_stream_specifier]`** 匹配属于说明符 \<group_specifier\> 所指组的流。若使用 \<additional_stream_specifier\>，则匹配既属于该组又匹配 \<additional_stream_specifier\> 的流。\<group_specifier\> 可为以下之一：

  | Term | Description |
  |----|----|
  | `group_index` | 匹配具有该组索引的流。 |
  | `#group_id or i:group_id` | 匹配具有该组 id 的流。 |

- **`p:program_id[:additional_stream_specifier]`** 匹配属于 id 为 \<program_id\> 的节目的流。若使用 \<additional_stream_specifier\>，则匹配既属于该节目又匹配 \<additional_stream_specifier\> 的流。

- **`#stream_id or i:stream_id`** 按流 id 匹配流（例如 MPEG-TS 容器中的 PID）。

- **`m:key[:value]`** 匹配元数据标签 \<key\> 具有指定值的流。未给出 \<value\> 时，匹配包含该标签（任意值）的流。\<key\> 或 \<value\> 中的冒号字符 ':' 需要反斜杠转义。

- **`disp:dispositions[:additional_stream_specifier]`** 匹配具有给定 disposition 标志的流。\<dispositions\> 是一个或多个 disposition（由 `-dispositions` 选项打印的那些）以 '+' 连接的列表。

- **`u`** 匹配配置可用的流：编解码器必须已定义，且视频尺寸或音频采样率等关键信息必须存在。

  注意在 `ffmpeg` 中，按元数据匹配只对输入文件正常工作。

## 通用选项

这些选项为 ff\* 系列工具共用。

- **`-L, -license`** 显示许可。

- **`-h, -?, -help, --help [arg]`** 显示帮助。可指定可选参数以打印关于特定项的帮助。未指定参数时，仅显示基本（非高级）工具选项。

  \<arg\> 的可能取值如下：

  - **`long`** 除基本工具选项外还打印高级工具选项。

  - **`full`** 打印完整选项列表，包括编码器、解码器、解复用器、复用器、滤镜等的共享选项和私有选项。

  - **`decoder=decoder_name`** 打印名为 \<decoder_name\> 的解码器的详细信息。使用 `-decoders` 选项获取所有解码器列表。

  - **`encoder=encoder_name`** 打印名为 \<encoder_name\> 的编码器的详细信息。使用 `-encoders` 选项获取所有编码器列表。

  - **`demuxer=demuxer_name`** 打印名为 \<demuxer_name\> 的解复用器的详细信息。使用 `-formats` 选项获取所有解复用器和复用器列表。

  - **`muxer=muxer_name`** 打印名为 \<muxer_name\> 的复用器的详细信息。使用 `-formats` 选项获取所有复用器和解复用器列表。

  - **`filter=filter_name`** 打印名为 \<filter_name\> 的滤镜的详细信息。使用 `-filters` 选项获取所有滤镜列表。

  - **`bsf=bitstream_filter_name`** 打印名为 \<bitstream_filter_name\> 的比特流滤镜的详细信息。使用 `-bsfs` 选项获取所有比特流滤镜列表。

  - **`protocol=protocol_name`** 打印名为 \<protocol_name\> 的协议的详细信息。使用 `-protocols` 选项获取所有协议列表。

- **`-version`** 显示版本。

- **`-buildconf`** 显示构建配置，每行一个选项。

- **`-formats`** 显示可用格式（包括设备）。

- **`-demuxers`** 显示可用解复用器。

- **`-muxers`** 显示可用复用器。

- **`-devices`** 显示可用设备。

- **`-codecs`** 显示 libavcodec 已知的所有编解码器。

  注意，本档通篇将 'codec' 一词用作简称，其更准确的说法是媒体比特流格式。

- **`-decoders`** 显示可用解码器。

- **`-encoders`** 显示所有可用编码器。

- **`-bsfs`** 显示可用比特流滤镜。

- **`-protocols`** 显示可用协议。

- **`-filters`** 显示 libavfilter 可用滤镜。

- **`-pix_fmts`** 显示可用像素格式。

- **`-sample_fmts`** 显示可用采样格式。

- **`-layouts`** 显示声道名称和标准声道布局。

- **`-dispositions`** 显示流的 disposition 标志。

- **`-colors`** 显示已识别的颜色名称。

- **`-sources device[,opt1=val1[,opt2=val2]...]`** 显示输入设备的自动探测源。某些设备可能提供无法自动探测的、依赖系统的源名称。返回的列表不能假定总是完整。

  ``` text
  ffmpeg -sources pulse,server=192.168.0.4
  ```

- **`-sinks device[,opt1=val1[,opt2=val2]...]`** 显示输出设备的自动探测汇。某些设备可能提供无法自动探测的、依赖系统的汇名称。返回的列表不能假定总是完整。

  ``` text
  ffmpeg -sinks pulse,server=192.168.0.4
  ```

- **`-loglevel [flags+]loglevel | -v [flags+]loglevel`** 设置库使用的日志级别和标志。

  可选的 \<flags\> 前缀可由以下值组成：

  - **`repeat`** 表示重复的日志输出不压缩至第一行，并且省略 "Last message repeated n times" 一行。

  - **`level`** 表示日志输出为每条消息行添加 `[level]` 前缀。可用作日志着色的替代，例如把日志转储到文件时。

  - **`time`** 表示日志行加时间信息前缀。

  - **`datetime`** 表示日志行加日期和时间信息前缀。

  标志也可以单独使用：加 '+'/'-' 前缀设置/重置单个标志，不影响其他 \<flags\>，也不改变 \<loglevel\>。同时设置 \<flags\> 和 \<loglevel\> 时，最后一个 \<flags\> 值与 \<loglevel\> 之间应有一个 '+' 分隔符。

  \<loglevel\> 是包含以下取值之一的字符串或数字：

  - **`quiet, -8`** 什么都不显示；保持静默。

  - **`panic, 0`** 只显示可能导致进程崩溃的致命错误，例如断言失败。目前不用于任何用途。

  - **`fatal, 8`** 只显示致命错误。这些是进程绝对无法再继续的错误。

  - **`error, 16`** 显示所有错误，包括可从中恢复的错误。

  - **`warning, 24`** 显示所有警告和错误。任何与可能不正确或意外事件相关的消息都会显示。

  - **`info, 32`** 显示处理过程中的提示信息。这是警告和错误之外的补充。这是默认值。

  - **`verbose, 40`** 与 `info` 相同，但更详细。

  - **`debug, 48`** 显示一切，包括调试信息。

  - **`trace, 56`**

  例如：启用重复日志输出、添加 `level` 前缀，并将 \<loglevel\> 设为 `verbose`：

  ``` text
  ffmpeg -loglevel repeat+level+verbose -i input output
  ```

  另一个示例：启用重复日志输出，但不影响 `level` 前缀标志的当前状态或 \<loglevel\>：

  ``` text
  ffmpeg [...] -loglevel +repeat
  ```

  默认情况下程序将日志记录到 stderr。若终端支持着色，会用颜色标记错误和警告。可通过设置环境变量 `AV_LOG_FORCE_NOCOLOR` 禁用日志着色，或设置环境变量 `AV_LOG_FORCE_COLOR` 强制启用。

- **`-report`** 把完整命令行和日志输出转储到当前目录下名为 `program-YYYYMMDD-HHMMSS.log` 的文件。该文件对缺陷报告很有用。它还意味着 `-loglevel debug`。

  把环境变量 `FFREPORT` 设为任意值有同样效果。若值为以 ':' 分隔的 key=value 序列，这些选项会影响报告；选项值含特殊字符或选项分隔符 ':' 时必须转义（参见 ffmpeg-utils 手册中的 "Quoting and escaping"（引号引用与转义）一节）。

  可识别以下选项：

  - **`file`** 设置报告所用文件名；`%p` 展开为程序名，`%t` 展开为时间戳，`%%` 展开为普通 `%`

  - **`level`** 用数值设置日志详细程度（参见 `-loglevel`）。

  例如，把报告输出到名为 `ffreport.log` 的文件，日志级别用 `32`（日志级别 `info` 的别名）：

  ``` text
  FFREPORT=file=ffreport.log:level=32 ffmpeg -i input output
  ```

  解析环境变量出错不是致命的，也不会出现在报告中。

- **`-hide_banner`** 不打印横幅。

  FFmpeg 各工具通常会显示版权声明、构建选项和库版本。该选项可用于不打印这些信息。

- **`-cpuflags flags (global)`** 允许设置和清除 CPU 标志。该选项用于测试。不了解其后果请勿使用。

  ``` text
  ffmpeg -cpuflags -sse+mmx ...
  ffmpeg -cpuflags mmx ...
  ffmpeg -cpuflags 0 ...
  ```

  该选项可用的标志如下：

- **`x86`**

  - **`mmx`**

  - **`mmxext`**

  - **`sse`**

  - **`sse2`**

  - **`sse2slow`**

  - **`sse3`**

  - **`sse3slow`**

  - **`ssse3`**

  - **`atom`**

  - **`sse4.1`**

  - **`sse4.2`**

  - **`avx`**

  - **`avx2`**

  - **`xop`**

  - **`fma3`**

  - **`fma4`**

  - **`3dnow`**

  - **`3dnowext`**

  - **`bmi1`**

  - **`bmi2`**

  - **`cmov`**

- **`ARM`**

  - **`armv5te`**

  - **`armv6`**

  - **`armv6t2`**

  - **`vfp`**

  - **`vfpv3`**

  - **`neon`**

  - **`setend`**

- **`AArch64`**

  - **`armv8`**

  - **`vfp`**

  - **`neon`**

- **`PowerPC`**

  - **`altivec`**

- **`Specific Processors`**

  - **`pentium2`**

  - **`pentium3`**

  - **`pentium4`**

  - **`k6`**

  - **`k62`**

  - **`athlon`**

  - **`athlonxp`**

  - **`k8`**

- **`-cpucount count (global)`** 覆盖 CPU 数量探测。该选项用于测试。不了解其后果请勿使用。

  ``` text
  ffmpeg -cpucount 2
  ```

- **`-max_alloc bytes`** 设置 ffmpeg 的 malloc 函数族在堆上分配内存块的大小上限。使用该选项时务必**极其谨慎**。若不了解其全部后果请勿使用。默认值为 INT_MAX。

## AVOptions

这些选项由 libavformat、libavdevice 和 libavcodec 库直接提供。要查看可用 AVOptions 列表，使用 `-help` 选项。它们分为两类：

- **`generic`** 这些选项可设置于任何容器、编解码器或设备。通用选项在容器/设备下列于 AVFormatContext 选项，在编解码器下列于 AVCodecContext 选项。

- **`private`** 这些选项特定于给定容器、设备或编解码器。私有选项列于对应的容器/设备/编解码器之下。

例如，向 MP3 文件写入 ID3v2.3 头而非默认的 ID3v2.4，使用 MP3 复用器的 `id3v2_version` 私有选项：

``` text
ffmpeg -i input.flac -id3v2_version 3 out.mp3
```

所有编解码器 AVOptions 均按流生效，因此应附加流说明符：

``` text
ffmpeg -i multichannel.mxf -map 0:v:0 -map 0:a:0 -map 0:a:0 -c:a:0 ac3 -b:a:0 640k -ac:a:1 2 -c:a:1 aac -b:2 128k out.mp4
```

上例中，一条多声道音频流被映射两次用于输出。第一个实例用 ac3 编解码器以 640k 码率编码。第二个实例被下混到 2 声道并用 aac 编解码器编码。其码率 128k 通过输出流的绝对索引指定。

注意：`-nooption` 语法不能用于布尔 AVOptions，请使用 `-option 0`/`-option 1`。

注意：通过在选项名前加 v/a/s 前缀来指定逐流 AVOptions 的旧式做法（未成文档）现已废弃，即将移除。
