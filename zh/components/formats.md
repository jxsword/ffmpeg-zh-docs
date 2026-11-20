# 描述

本文档介绍 libavformat 库所支持的格式（复用器与解复用器）。

# 格式选项

libavformat 库提供一些通用全局选项，可为所有复用器和解复用器设置。此外，每个复用器或解复用器还可以支持所谓的私有选项，即特定于该组件的选项。

选项可通过在 FFmpeg 工具中指定 -\<option\> \<value\> 来设置，或通过在 `AVFormatContext` 选项中显式设值来设置；以编程方式使用时，可使用 `libavutil/opt.h` API。

受支持选项的列表如下：

- **`avioflags flags (input/output)`** 可能的取值：

  | Term       | Description       |
  |------------|-------------------|
  | `direct` | 减少缓冲。 |

- **`probesize integer (input)`** 设置探测大小（字节），即为了获取流信息而分析的数据大小。较大的值能够在信息分散到流中的情况下检测到更多信息，但会增加延迟。必须是不小于 32 的整数。默认为 5000000。

- **`max_probe_packets integer (input)`** 设置探测编解码器时缓冲包的最大数量。默认为 2500 个包。

- **`packetsize integer (output)`** 设置包大小。

- **`fflags flags`** 设置格式标志。部分标志仅对有限数量的格式实现。

  输入文件的可能取值：

  - **`discardcorrupt`** 丢弃损坏的包。

  - **`fastseek`** 为某些格式启用快速但不精确的定位。

  - **`genpts`** 若存在 DTS 则生成缺失的 PTS。

  - **`igndts`** 若 PTS 也已设置则忽略 DTS。当 PTS 已设置时，DTS 值被设为 NOPTS。设置 `nofillin` 标志时此项被忽略。

  - **`ignidx`** 忽略索引。

  - **`nobuffer`** 减少初始输入流分析期间缓冲引入的延迟。

  - **`nofillin`** 不填充包字段中缺失的、可精确计算的值。

  - **`noparse`** 禁用 AVParser，这还需要 `+nofillin`。

  - **`sortdts`** 尝试按 DTS 交错输出包。目前仅对带索引的 AVI 可用。

  输出文件的可能取值：

  - **`autobsf`** 按输出格式的要求自动应用比特流滤镜。默认启用。

  - **`bitexact`** 只写入与平台、构建和时间无关的数据。这确保文件和数据校验和可复现且跨平台一致。其主要用途是回归测试。

  - **`flush_packets`** 立即写出包。

  - **`shortest`** 在最短流结束时停止复用。可能需要增大 max_interleave_delta 以避免在 EOF 之前刷新较长的流。

- **`seek2any integer (input)`** 若设为 1，则允许在解复用器层面定位到非关键帧（在受支持时）。默认值为 0。

- **`analyzeduration integer (input)`** 指定探测输入时分析多少微秒。较大的值能够检测到更精确的信息，但会增加延迟。默认值为 5,000,000 微秒 = 5 秒。

- **`cryptokey hexadecimal string (input)`** 设置解密密钥。

- **`indexmem integer (input)`** 设置时间戳索引（每流）可用的最大内存。

- **`rtbufsize integer (input)`** 设置缓冲实时帧可用的最大内存。

- **`fdebug flags (input/output)`** 打印特定的调试信息。

  可能的取值：

  | Term | Description |
  |----|----|
  | `ts` | 打印时间戳信息。 |
  | `id3v2` | 解复用含 ID3v2 标签的文件时打印 ID3v2 帧数据。 |

- **`max_delay integer (input/output)`** 设置复用或解复用的最大延迟（微秒）。

- **`fpsprobesize integer (input)`** 设置用于探测 fps 的帧数。

- **`audio_preload integer (output)`** 设置音频包提前交错的时间（微秒）。

- **`chunk_duration integer (output)`** 设置每个 chunk 的时长（微秒）。

- **`chunk_size integer (output)`** 设置每个 chunk 的大小（字节）。

- **`err_detect, f_err_detect flags (input)`** 设置错误检测标志。`f_err_detect` 已弃用，只能通过 `ffmpeg` 工具使用。

  可能的取值：

  - **`crccheck`** 校验内嵌的 CRC。

  - **`bitstream`** 检测比特流规范偏差。

  - **`buffer`** 检测不正确的比特流长度。

  - **`explode`** 检测到轻微错误时中止解码。

  - **`careful`** 将违反规范且现实中未见过的情况视为错误。

  - **`compliant`** 将所有不符合规范的情况视为错误。

  - **`aggressive`** 将正常编码器不应做出的行为视为错误。

- **`max_interleave_delta integer (output)`** 设置交错的最大缓冲时长。该时长以微秒表示，默认为 10000000（10 秒）。

  为确保所有流正确交错，libavformat 会等到每个流都至少有一个包之后才真正向输出文件写入任何包。当某些流"稀疏"（即连续包之间存在大段空隙）时，这可能造成过度缓冲。

  此字段指定复用队列中第一个包与最后一个包时间戳之间的最大差值，超过该差值时，libavformat 将输出一个包，而不管它是否已为所有流排入了包。

  若设为 0，libavformat 将持续缓冲包，直到每个流都有一个包，而不考虑缓冲包之间的最大时间戳差值。

- **`use_wallclock_as_timestamps integer (input)`** 若设为 1，使用墙上时钟作为时间戳。默认值为 0。

- **`avoid_negative_ts integer (output)`** 可能的取值：

  - **`make_non_negative`** 平移时间戳使其非负。另请注意，此项只影响开头的负时间戳，不影响非单调的负时间戳。

  - **`make_zero`** 平移时间戳，使第一个时间戳为 0。

  - **`auto (default)`** 在目标格式需要时启用平移。

  - **`disabled`** 禁用时间戳平移。

  启用平移时，所有输出时间戳平移相同的量。与不平移相比，音频、视频和字幕的失步以及相对时间戳差异都会保持不变。

- **`skip_initial_bytes integer (input)`** 若设为 1，设置读取头和帧之前要跳过的字节数。默认值为 0。

- **`correct_ts_overflow integer (input)`** 若设为 1，修正单个时间戳溢出。默认值为 1。

- **`flush_packets integer (output)`** 在每个包之后刷新底层 I/O 流。默认值为 -1（自动），即由底层协议决定；1 启用它，具有降低延迟的效果；0 禁用它，在某些情况下可能提高 I/O 吞吐量。

- **`output_ts_offset offset (output)`** 设置输出时间偏移。

  \<offset\> 必须是时长描述 (time duration specification)，参见 `ffmpeg-utils` 中"the Time duration section in the ffmpeg-utils(1) manual"（时长）一节。

  该偏移由复用器加到输出时间戳上。

  指定正的偏移意味着相应的流延迟 \<offset\> 中指定的时长。默认值为 `0`（即不应用偏移）。

- **`format_whitelist list (input)`** 以 "," 分隔的允许解复用器列表。默认全部允许。

- **`dump_separator string (input)`** 用于分隔命令行上打印的流参数字段的分隔符。例如，用换行和缩进分隔字段：

  ``` text
  ffprobe -dump_separator "
                            "  -i ~/videos/matrixbench_mpeg2.mpg
  ```

- **`max_streams integer (input)`** 指定流的最大数量。可用于拒绝因流数量过大而需要过多资源的文件。

- **`skip_estimate_duration_from_pts bool (input)`** 如果估计输入时长需要对文件末尾的 PTS 进行额外探测，则跳过该估计。目前适用于 MPEG-PS 和 MPEG-TS。

- **`duration_probesize integer (input)`** 设置输入时长估计实际需要对文件末尾 PTS 进行额外探测时（当前：MPEG-PS 和 MPEG-TS）的探测大小（字节）。此选项面向希望获得更准确时长探测结果的用户，或例如使用 concat 解复用器而间接需要的用户。典型场景是高码率、高视频缓冲、结尾清理后视频与音频 PTS 相近的 MPEG-TS CBR：在这种场景下，最后一个视频包与最后一个音频包之间的大段物理间隔使得必须读取大量字节才能获得视频流时长。另一个场景是默认探测行为由于帧重排只到达流中非最后一帧的单个视频帧，导致时长不准确。设置此选项会带来性能影响，即使是小文件也是如此，因为探测大小是固定的。默认行为是通用性的权衡，在很大程度上自适应，但不会不惜代价地扩展探测大小来获取流时长。必须是不小于 1 的整数，或 0 表示默认行为。

- **`strict, f_strict integer (input/output)`** 指定遵循标准的严格程度。`f_strict` 已弃用，只能通过 `ffmpeg` 工具使用。

  可能的取值：

  - **`very`** 严格遵循规范的更旧更严格版本或参考软件

  - **`strict`** 无论如何都严格遵循规范中的所有内容

  - **`normal`**

  - **`unofficial`** 允许非官方扩展

  - **`experimental`** 允许非标准化的实验性内容、实验性（未完成/开发中/未经充分测试）解码器和编码器。注意：实验性解码器可能带来安全风险，请勿将其用于解码不受信任的输入。

## 格式流说明符

格式流说明符允许选择匹配特定属性的一个或多个流。

流说明符的确切语义由 `libavformat/avformat.h` 头文件中声明的 `avformat_match_stream_specifier()` 函数定义，并在 `ffmpeg` 中"Stream specifiers section in the ffmpeg(1) manual"（流说明符）一节有文档说明。

# 解复用器

解复用器是 FFmpeg 中的配置元素，可以从特定类型的文件读取多媒体流。

配置 FFmpeg 构建时，所有受支持的解复用器默认启用。可以使用 configure 选项 `--list-demuxers` 列出全部可用项。

可以使用 configure 选项 `--disable-demuxers` 禁用全部解复用器，并使用选项 `--enable-demuxer=DEMUXER` 选择性启用单个解复用器，或使用选项 `--disable-demuxer=DEMUXER` 禁用它。

ff\* 工具的 `-demuxers` 选项将显示已启用解复用器的列表。使用 `-formats` 查看已启用解复用器和复用器的合并列表。

下面介绍部分当前可用的解复用器。

## aa

Audible Format 2、3 和 4 解复用器。

此解复用器用于解复用 Audible Format 2、3 和 4 (.aa) 文件。

## aac

Raw Audio Data Transport Stream AAC 解复用器。

此解复用器用于解复用包含单个 AAC 流以及其中任何 ID3v1/2 或 APE 标签的 ADTS 输入。

## apng

动图便携式网络图形 (Animated Portable Network Graphics) 解复用器。

此解复用器用于解复用 APNG 文件。除 PNG 签名外，直到（但不包含）第一个 fcTL chunk 的所有头信息都作为 extradata 传输。随后，帧被拆分为两个 fcTL chunk 之间、或最后一个 fcTL 与 IEND chunk 之间的所有 chunk。

- **`-ignore_loop bool`** 若设置，忽略文件中的循环变量。默认启用。

- **`-max_fps int`** 最大帧率（每秒帧数）。默认值 0 表示不限制。

- **`-default_fps int`** 文件中未指定时的默认帧率（每秒帧数）（0 表示尽可能快）。默认值为 15。

## asf

Advanced Systems Format 解复用器。

此解复用器用于解复用 ASF 文件和 MMS 网络流。

| Term | Description |
|----|----|
| `-no_resync_search bool` | 不尝试通过查找某个可选起始码来重新同步。 |

## concat

虚拟拼接脚本 (virtual concatenation script) 解复用器。

此解复用器从文本文件读取文件列表和其他指令，并依次解复用它们，就像所有包被一起复用一样。

文件中的时间戳会被调整，使第一个文件从 0 开始，每个后续文件从前一个文件结束之处开始。注意这是全局进行的，如果所有流的长度不完全相同，可能产生空隙。

所有文件必须具有相同的流（相同的编解码器、相同的时间基等）。

每个文件的时长用于调整下一个文件的时间戳：如果时长不正确（例如因为它是用码率计算的，或因为文件被截断），可能造成伪影。可以使用 `duration` 指令覆盖存储在每个文件中的时长。

### 语法

脚本是扩展 ASCII 编码的文本文件，每行一条指令。空行、前导空格和以 '#' 开头的行会被忽略。可识别以下指令：

- **`file path`** 要读取的文件的路径；特殊字符和空格必须用反斜杠或单引号转义。

  所有后续与文件相关的指令都作用于该文件。

- **`ffconcat version 1.0`** 标识脚本类型和版本。

  为了让 FFmpeg 自动识别该格式，此指令必须原样出现在脚本的第一行（不能有额外空格或字节序标记）。

- **`duration dur`** 文件的时长。此信息可从文件中指定；在此指定可能更高效，或在文件中的信息不可用或不准确时有所帮助。

  如果为所有文件都设置了时长，则可以在整个拼接视频中定位。

- **`inpoint timestamp`** 文件的入点。解复用器打开文件时会立即定位到指定的时间戳。定位的方式是使所有流都能在入点处成功呈现。

  此指令对帧内编解码器效果最佳，因为对非帧内编解码器，通常会在实际入点之前得到额外的包，且解码内容很可能也包含入点之前的帧。

  对每个文件，文件入点之前的包的时间戳会小于该文件计算出的起始时间戳（第一个文件时为负），且文件时长（若未通过 `duration` 指令指定）会根据其指定的入点缩减。

  由于指定入点之前可能存在包，两个拼接文件的包时间戳可能重叠。

- **`outpoint timestamp`** 文件的出点。当解复用器在任何流中到达指定的解码时间戳时，将其作为文件结束条件处理，并跳过当前流及所有流的剩余所有包。

  出点是排他的，即解复用器不会输出解码时间戳大于或等于出点的包。

  此指令对帧内编解码器以及所有流紧密交错的格式效果最佳。对非帧内编解码器，通常会在出点之后得到带有呈现时间戳的额外包，因此解码内容很可能也包含出点之后的帧。如果流未紧密交错，可能得不到出点之前所有流的全部包，且只能解码最早的流直到出点。

  文件时长（若未通过 `duration` 指令指定）会根据其指定的出点缩减。

- **`file_packet_metadata key=value`** 文件包的元数据。指定的元数据会为每个文件包设置。可多次指定此指令以添加多个元数据条目。此指令已弃用，请改用 `file_packet_meta`。

- **`file_packet_meta key value`** 文件包的元数据。指定的元数据会为每个文件包设置。可多次指定此指令以添加多个元数据条目。

- **`option key value`** 用于访问、打开和探测文件的选项。可出现多次。

- **`stream`** 在虚拟文件中引入一个流。所有后续与流相关的指令都作用于最后引入的流。必须设置某些流属性，才能在子文件中识别匹配的流。如果脚本中未定义流，则复制第一个文件的流。

- **`exact_stream_id id`** 设置流的 id。若给出此指令，将使用子文件中具有相应 id 的字符串。这对 MPEG-PS (VOB) 文件尤其有用，因为其流顺序不可靠。

- **`stream_meta key value`** 流的元数据。可出现多次。

- **`stream_codec value`** 流的编解码器。

- **`stream_extradata hex_string`** 流的 extradata，以十六进制编码。

- **`chapter id start end`** 添加一个章节。\<id\> 是唯一标识符，可以是较小且连续的数字。

### 选项

此解复用器接受以下选项：

- **`safe`** 若设为 1，拒绝不安全的文件路径和指令。文件路径被视为安全的条件是：不包含协议规范、为相对路径、所有组件只包含可移植字符集中的字符（字母、数字、句点、下划线和连字符），且组件开头没有句点。

  若设为 0，接受任何文件名。

  默认值为 1。

- **`auto_convert`** 若设为 1，尝试对包数据执行自动转换，使流可拼接。默认值为 1。

  目前，唯一的转换是为 MP4 格式的 H.264 流添加 h264_mp4toannexb 比特流滤镜。在存在分辨率变化时尤其必要。

- **`segment_time_metadata`** 若设为 1，每个包将包含 \<lavf.concat.start_time\> 和 \<lavf.concat.duration\> 包元数据值，即拼接输出中相应文件分段的 start_time 和 duration（以微秒表示）。仅在基于 concat 文件可知时才设置 duration 元数据。默认值为 0。

### 示例

- 使用绝对文件名并包含一些注释：

  ``` text
  # my first filename
  file /mnt/share/file-1.wav
  # my second filename including whitespace
  file '/mnt/share/file 2.wav'
  # my third filename including whitespace plus single quote
  file '/mnt/share/file 3'\''.wav'
  ```

- 允许自动探测输入格式，使用安全文件名并设置第一个文件的时长：

  ``` text
  ffconcat version 1.0

  file file-1.wav
  duration 20.0

  file subdir/file-2.wav
  ```

## dash

基于 HTTP 的动态自适应流媒体 (Dynamic Adaptive Streaming over HTTP) 解复用器。

此解复用器呈现清单 (manifest) 中找到的所有 AVStream。通过对 AVStream 设置 discard 标志，调用方可以决定实际接收哪些流。每个流镜像 `<Representation>` 中的 `id` 和 `bandwidth` 属性，分别作为名为 "id" 和 "variant_bitrate" 的元数据键。

### 选项

此解复用器接受以下选项：

- **`cenc_decryption_key`** 默认的 16 字节密钥（十六进制），用于解密使用 ISO 通用加密 (CENC/AES-128 CTR; ISO/IEC 23001-7) 加密的文件。

- **`cenc_decryption_keys`** 16 字节密钥 ID =\> 16 字节密钥的字典（均为十六进制），用于解密使用 ISO 通用加密 (CENC/AES-128 CTR; ISO/IEC 23001-7) 加密的文件。

## dvdvideo

DVD-Video 解复用器，由 libdvdnav 和 libdvdread 驱动。

可将 DVD 标题（具体为顺序 PGC）直接送入转换管线。菜单资产（如背景视频或音频）也可以在给定菜单坐标的情况下解复用（尽力而为）。

接受块设备（DVD 光驱）、ISO 文件和目录结构。在这些输入之前使用 `-f dvdvideo` 激活。

此解复用器不具备任何形式的解密代码。处理加密 DVD 需自行设法，不应期待这方面的支持。

底层播放由 libdvdnav 处理，结构解析由 libdvdread 处理。FFmpeg 构建时必须提供 GPL 库支持，以及 configure 开关 `--enable-libdvdnav` 和 `--enable-libdvdread`。

需要提供所需的"标题编号"或精确的 PGC/PG 坐标。许多开源 DVD 播放器和工具可帮助提供此信息。若未指定，解复用器默认为标题 1，这对许多光盘有效。但由于格式的灵活性，建议手动检查。有些光盘的编排很奇怪或带有无效头。

如果输入是真实 DVD 光驱，请注意有些光驱在读取光盘坏扇区时可能静默失败，返回随机比特，这实际上是损坏的数据。这在老化或霉变的光盘上尤为突出。需要二次读取和完整性检查才能检测出损坏。这不是 FFmpeg 的问题。

### 背景

DVD-Video 不是传统意义上可直接访问的线性容器格式。相反，它允许对精心复用的、存储在无头 VOB 文件中的 MPEG-PS 流进行复杂的程序化播放。对最终用户而言，这些流简单地称为"标题"，而实际的逻辑播放顺序由标题内的一个或多个"PGC"（Program Group Chain，节目组链）定义。PGC 又由多个"PG"（Program，节目）组成，PG 是实际的视频分段（对典型的视频作品而言按顺序排列）。PGC 结构连同流布局和元数据一起存储在需要解析的 IFO 文件中。简单来说，可以把 PGC 看作播放列表。

真实的 DVD 播放器依靠用户通过菜单的 GUI 交互以及内部 VM 来驱动解复用的方向。通常，用户要么（通过菜单）导航，要么自动跳转到其选择的 PGC。在此过程和随后的播放期间，DVD 播放器的内部 VM 还会维护状态并执行可在播放期间创建到不同扇区跳转的指令。这就是需要 libdvdnav 的原因，因为仅线性读取光盘上的 MPEG-PS 数据块（VOB）在许多情况下不足以产生正确的顺序。

还有许多其他 DVD 结构（一个很长的主题）此处不作讨论。特别是 NAV 包，由该解复用器处理以构建精确的时序，但不作为流输出。要获得良好的高层理解，请参阅：<https://code.videolan.org/videolan/libdvdnav/-/blob/master/doc/dvd_structures>

### 选项

此解复用器接受以下选项：

- **`title int`** 要播放的标题编号。若未设置 `pgc` 和 `pg` 则必须设置。不适用于菜单。默认值为 0（自动），目前只选择第一个可用标题（标题 1），并通知用户其影响。

- **`chapter_start int`** 开始的章节（或 PTT (part-of-title)）编号。不适用于菜单。默认值为 1。

- **`chapter_end int`** 结束的章节（或 PTT (part-of-title)）编号。不适用于菜单。默认值为 0，这是一个特殊值，表示在最后一个可能的章节结束。

- **`angle int`** 视频角度编号，指本质上是由 VOB 中交织的替代帧构成的附加视频流。不适用于菜单。默认值为 1。

- **`region int`** 用于播放的区域码。某些光盘可能用它来在不同区域默认以特定角度播放。若使用真实 DVD 光驱作为输入，此选项不会影响其区域码。不适用于菜单。默认值为 0，即"世界"。

- **`menu bool`** 解复用菜单资产而不是导航标题。需要菜单的精确坐标（`menu_lu`、`menu_vts`、`pgc`、`pg`）。默认为 false。

- **`menu_lu int`** 要解复用的菜单语言。DVD 中菜单按语言分组。默认值为 1，即第一个语言单元。

- **`menu_vts int`** 菜单所在的 VTS，若是 VMG 菜单（根级）则为 0。默认值为 1，即第一个 VTS 的菜单。

- **`pgc int`** 开始播放的入口 PGC，与 `pg` 配合使用。也可通过设置 `title` 实现。目前不支持章节标记。菜单必须显式设置。默认值为 0，自动从 `title` 的值解析。

- **`pg int`** 开始播放的入口 PG，与 `pgc` 配合使用。也可通过设置 `title` 实现。目前不支持章节标记。默认值为 1，即 PGC 的第一个 PG。

- **`preindex bool`** 启用后可获得准确的章节 (PTT) 标记和时长测量，但需要缓慢的二次读取，以便从 NAV 包索引章节标记时间戳。对真实光驱而言这是不理想的额外工作。建议对存储在硬盘上的 DVD 结构备份使用此选项，更快。与 `pgc` 和 `pg` 不兼容。默认值为 0，即 false。

- **`trim bool`** 跳过开头的填充单元（即短于 1 秒的单元）。许多光盘在 PGC 开头带有填充段，通常含有用于控制真实 DVD 播放器缓冲速度的垃圾数据，没有其他实质内容。不适用于菜单。默认值为 1，即 true。

### 示例

- 打开给定 DVD 结构中的标题 3：

  ``` text
  ffmpeg -f dvdvideo -title 3 -i <path to DVD> ...
  ```

- 打开给定 DVD 结构中标题 1 的第 3-6 章：

  ``` text
  ffmpeg -f dvdvideo -chapter_start 3 -chapter_end 6 -title 1 -i <path to DVD> ...
  ```

- 只打开给定 DVD 结构中标题 1 的第 5 章：

  ``` text
  ffmpeg -f dvdvideo -chapter_start 5 -chapter_end 5 -title 1 -i <path to DVD> ...
  ```

- 从 VTS 1、PGC 1 解复用语言 1 的菜单，从 PG 1 开始：

  ``` text
  ffmpeg -f dvdvideo -menu 1 -menu_lu 1 -menu_vts 1 -pgc 1 -pg 1 -i <path to DVD> ...
  ```

## ea

Electronic Arts 多媒体格式解复用器。

此格式被多款 Electronic Arts 游戏使用。

### 选项

- **`merge_alpha bool`** 通常，VP6 透明通道（如果存在）会作为辅助视频流返回；设置此选项后，解复用器将返回单一视频流，其中除普通视频外还包含透明通道。

## imf

可互操作母版格式 (Interoperable Master Format) 解复用器。

此解复用器呈现 IMF Composition 中找到的音频和视频流，如 [SMPTE ST 2067-2](https://doi.org/10.5594/SMPTE.ST2067-2.2020) 所规定。

``` text
ffmpeg [-assetmaps <path of ASSETMAP1>,<path of ASSETMAP2>,...] -i <path of CPL> ...
```

若未指定 `-assetmaps`，解复用器会在 CPL 所在目录中查找名为 `ASSETMAP.xml` 的文件。

## flv, live_flv, kux

Adobe Flash Video 格式解复用器。

此解复用器用于解复用 FLV 文件和 RTMP 网络流。对于直播网络流，如果强制指定格式，可以使用 live_flv 选项代替 flv，以应对时间戳不连续。KUX 是优酷平台使用的 flv 变体。

``` text
ffmpeg -f flv -i myfile.flv ...
ffmpeg -f live_flv -i rtmp://<any.server>/anything/key ....
```

| Term | Description |
|----|----|
| `-flv_metadata bool` | 根据 onMetaData 数组内容分配流。 |
| `-flv_ignore_prevtag bool` | 忽略前一个 tag 值的大小。 |
| `-flv_full_metadata bool` | 输出 onMetadata 的全部上下文。 |

## gif

动图 GIF (Animated GIF) 解复用器。

它接受以下选项：

- **`min_delay`** 设置帧间最小有效延迟（单位为百分之一秒）。范围为 0 到 6000。默认值为 2。

- **`max_gif_delay`** 设置帧间最大有效延迟（单位为百分之一秒）。范围为 0 到 65535。默认值为 65535（接近十一分钟），即规范允许的最大值。

- **`default_delay`** 设置帧间默认延迟（单位为百分之一秒）。范围为 0 到 6000。默认值为 10。

- **`ignore_loop`** GIF 文件可包含按一定次数（或无限次）循环的信息。若 `ignore_loop` 设为 1，则忽略输入中的循环设置，不进行循环。若设为 0，则进行循环，并按 GIF 的设置循环相应次数。默认值为 1。

例如，借助 overlay 滤镜，将无限循环的 GIF 叠加在另一个视频上：

``` text
ffmpeg -i input.mp4 -ignore_loop 0 -i input.gif -filter_complex overlay=shortest=1 out.mkv
```

注意，上例使用 overlay 滤镜的 shortest 选项使输出视频在最短输入文件的长度处结束，在本例中即 `input.mp4`，因为示例中的 GIF 无限循环。

## hls

HLS 解复用器

Apple HTTP Live Streaming 解复用器。

此解复用器呈现来自所有变体流 (variant stream) 的全部 AVStream。id 字段设为码率变体的索引号。通过对 AVStream 设置 discard 标志（在 ffplay 中按 'a' 或 'v'），调用方可以决定实际接收哪些变体流。流所属变体的总码率可在名为 "variant_bitrate" 的元数据键中获得。

它接受以下选项：

- **`live_start_index`** 直播流起始的分段索引（负值表示从末尾计）。

- **`prefer_x_start`** 若播放列表中存在 \#EXT-X-START，则优先使用它而不是 live_start_index。

- **`allowed_extensions`** 以 ',' 分隔的、允许 hls 访问的文件扩展名列表。

- **`extension_picky`** 阻止不允许的扩展名参与探测。它还要求所有可用分段的扩展名与格式匹配（mpegts 除外，mpegts 始终被允许）。建议正确设置白名单而不是依赖扩展名。默认启用。

- **`max_reload`** 尝试重新加载不完整列表的最大次数。默认值为 1000。

- **`m3u8_hold_counters`** m3u8 刷新但没有新分段时的最大加载次数。默认值为 1000。

- **`http_persistent`** 使用持久 HTTP 连接。仅适用于 HTTP 流。默认启用。

- **`http_multiple`** 使用多个 HTTP 连接下载 HTTP 分段。对 HTTP/1.1 服务器默认启用。

- **`http_seekable`** 使用 HTTP 部分请求下载 HTTP 分段。0 = 禁用，1 = 启用，-1 = 自动。默认为自动。

- **`seg_format_options`** 使用以 `:` 分隔的 key=value 对列表设置媒体分段解复用器的选项。

- **`seg_max_retry`** 出错时重新加载分段的最大次数，在不希望因网络错误跳过分段时有用。默认值为 0。

## image2

图像文件解复用器。

此解复用器从模式 (pattern) 指定的图像文件列表读取。模式的语法与含义由选项 \<pattern_type\> 指定。

模式可以包含一个后缀，用于自动确定文件中所含图像的格式。

序列中所有文件的每个图像的大小、像素格式和格式必须相同。

此解复用器接受以下选项：

- **`framerate`** 设置视频流的帧率。默认为 25。

- **`loop`** 若设为 1，循环读取输入。默认值为 0。

- **`pattern_type`** 选择用于解释所提供文件名的模式类型。

  \<pattern_type\> 接受以下取值之一。

  - **`none`** 禁用模式匹配，因此视频将只包含指定的图像。如果不想从多幅图像创建序列，且文件名可能包含特殊模式字符，应使用此选项。

  - **`sequence`** 选择序列模式类型，用于指定以顺序编号索引的文件序列。

    序列模式可包含字符串 "%d" 或 "%0\<N\>d"，它指定每个匹配文件名中表示顺序编号的字符的位置。若使用 "%d0\<N\>d" 形式，每个文件名中表示编号的字符串以 0 填充，\<N\> 是表示编号的 0 填充位数的总数。模式中可用字符串 "%%" 指定字面字符 '%'。

    若序列模式包含 "%d" 或 "%0\<N\>d"，则模式指定的文件列表的第一个文件名必须包含介于 \<start_number\> 与 \<start_number\>+\<start_number_range\>-1 之间（含边界）的编号，且后续所有编号必须连续。

    例如，模式 "img-%03d.bmp" 将匹配 `img-001.bmp`、`img-002.bmp`、……、`img-010.bmp` 等形式的文件名序列；模式 "i%%m%%g-%d.jpg" 将匹配 `i%m%g-1.jpg`、`i%m%g-2.jpg`、……、`i%m%g-10.jpg` 等形式的文件名序列。

    注意，模式不一定必须包含 "%d" 或 "%0\<N\>d"，例如转换单个图像文件 `img.jpeg` 可以使用命令：

    ``` text
    ffmpeg -i img.jpeg img.png
    ```

  - **`glob`** 选择 glob 通配符模式类型。

    模式按 `glob()` 模式解释。仅当 libavformat 编译时带有 glob 支持才可选择此项。

  默认值为 \<sequence\>。

- **`pixel_format`** 设置要读取图像的像素格式。若未指定，则从序列中第一幅图像文件猜测。

- **`start_number`** 设置图像文件模式匹配的文件中开始读取的索引。默认值为 0。

- **`start_number_range`** 设置查找序列中第一幅图像文件时检查的索引区间范围，从 \<start_number\> 开始。默认值为 5。

- **`ts_from_file`** 若设为 1，将帧时间戳设为图像文件的修改时间。注意这不保证时间戳单调：图像顺序与不使用此选项时相同。默认值为 0。若设为 2，将帧时间戳设为图像文件的修改时间（纳秒精度）。

- **`video_size`** 设置要读取图像的视频尺寸。若未指定，则从序列中第一幅图像文件猜测。

- **`export_path_metadata`** 若设为 1，将在输入中发现的元数据基础上增加两个额外字段，使其也可供其他滤镜使用（示例参见 \<drawtext\> 滤镜）。默认值为 0。额外字段说明如下：

  | Term | Description |
  |----|----|
  | `lavf.image2dec.source_path` | 对应被读取输入文件的完整路径。 |
  | `lavf.image2dec.source_basename` | 对应被读取文件的名称。 |

### 示例

- 使用 `ffmpeg` 从文件序列 `img-001.jpeg`、`img-002.jpeg`、……的图像创建视频，假设输入帧率为每秒 10 帧：

  ``` text
  ffmpeg -framerate 10 -i 'img-%03d.jpeg' out.mkv
  ```

- 同上，但从序列中索引为 100 的文件开始读取：

  ``` text
  ffmpeg -framerate 10 -start_number 100 -i 'img-%03d.jpeg' out.mkv
  ```

- 读取匹配 "\*.png" glob 模式的图像，即所有以 ".png" 后缀结尾的文件：

  ``` text
  ffmpeg -framerate 10 -pattern_type glob -i "*.png" out.mkv
  ```

## libgme

Game Music Emu 库是视频游戏音乐文件模拟器的集合。

更多信息参见 <https://bitbucket.org/mpyne/game-music-emu/overview>。

它接受以下选项：

- **`track_index`** 设置要解复用的音轨索引。该解复用器只能导出一条音轨。音轨索引从 0 开始。默认选取第一条音轨。音轨数作为 \<tracks\> 元数据条目导出。

- **`sample_rate`** 设置导出音轨的采样率。范围为 1000 到 999999。默认值为 44100。

- **`max_size (bytes)`** 该解复用器将整个文件缓冲进内存。调整此值以设置最大缓冲大小，它同时构成可读文件大小的上限。默认为 50 MiB。

## libmodplug

基于 ModPlug 的模块 (module) 解复用器

参见 <https://github.com/Konstanty/libmodplug>

它将导出一条 2 声道 16 位 44.1 kHz 音频流。可选地，还可导出一条 `pal8` 16 色视频流（可带或不带打印的元数据）。

它接受以下选项：

- **`noise_reduction`** 应用简单的低通滤镜。可为 1（开）或 0（关）。默认值为 0。

- **`reverb_depth`** 设置混响量。范围 0-100。默认值为 0。

- **`reverb_delay`** 设置延迟（毫秒），限制在 40-250 ms。默认值为 0。

- **`bass_amount`** 应用低音扩展，又称 XBass 或 megabass。范围为 0（安静）到 100（响亮）。默认值为 0。

- **`bass_range`** 设置低音频率的截止频率（即上限）。范围为 10-100 Hz。默认值为 0。

- **`surround_depth`** 应用 Dolby Pro-Logic 环绕声效果。范围为 0（安静）到 100（浓重）。默认值为 0。

- **`surround_delay`** 设置环绕延迟（毫秒），限制在 5-40 ms。默认值为 0。

- **`max_size`** 该解复用器将整个文件缓冲进内存。调整此值以设置最大缓冲大小，它同时构成可读文件大小的上限。范围为 0 到 100 MiB。0 表示移除缓冲大小限制（不推荐）。默认为 5 MiB。

- **`video_stream_expr`** 通过 eval API 求值的字符串，用于为生成的视频流指定颜色。可用变量为 `x`、`y`、`w`、`h`、`t`、`speed`、`tempo`、`order`、`pattern` 和 `row`。

- **`video_stream`** 生成视频流。可为 1（开）或 0（关）。默认值为 0。

- **`video_stream_w`** 设置视频帧宽度（以"字符"为单位，一个字符表示 8 像素）。范围为 20-512。默认值为 30。

- **`video_stream_h`** 设置视频帧高度（以"字符"为单位，一个字符表示 8 像素）。范围为 20-512。默认值为 30。

- **`video_stream_ptxt`** 在视频流上打印元数据。包括 `speed`、`tempo`、`order`、`pattern`、`row` 和 `ts`（时间，毫秒）。可为 1（开）或 0（关）。默认值为 1。

## libopenmpt

基于 libopenmpt 的模块 (module) 解复用器

更多信息参见 <https://lib.openmpt.org/libopenmpt/>。

某些文件包含多个子歌曲 (subsongs/音轨)，可通过 `subsong` 选项设置。

它接受以下选项：

- **`subsong`** 设置子歌曲索引。可为 'all'、'auto' 或子歌曲的索引。子歌曲索引从 0 开始。默认值为 'auto'。

  默认值是让 libopenmpt 自行选择。

- **`layout`** 设置声道布局。有效值为 1、2 和 4 声道布局。默认值为 STEREO。

- **`sample_rate`** 设置 libopenmpt 输出的采样率。范围为 1000 到 INT_MAX。默认值为 48000。

## mcc

MacCaption MCC 文件解复用器，支持 MCC 版本 1.0 和 2.0。MCC 文件存储 VANC 数据，其中可包含隐藏式字幕（EIA-608 和 CEA-708）、辅助时间码、摇移 (pan-scan) 数据等。默认情况下，出于向后兼容，MCC 解复用器只提取 EIA-608 和 CEA-708 隐藏式字幕并返回 `EIA_608` 流，忽略所有其他 VANC 数据。可通过设置 `-eia608_extract 0` 将其改为返回包含全部 VANC 数据的 `SMPTE_436M_ANC` 数据流

### 示例

- 将 MCC 文件转换为 Scenarist (SCC) 格式：

  ``` text
  ffmpeg -i CC.mcc -c:s copy CC.scc
  ```

  注意 SCC 格式只支持 EIA-608，因此会丢弃所有其他数据（如 CEA-708 扩展）。

- 将 MCC 文件合并进 MXF 文件：

  ``` text
  ffmpeg -i video_and_audio.mxf -eia608_extract 0 -i CC.mcc -c copy -map 0 -map 1 out.mxf
  ```

  这样会保留全部 VANC 数据，并将其作为 `SMPTE_436M_ANC` 数据流插入输出的 MXF 文件。

## mov/mp4/3gp

QuickTime 文件格式与 ISO/IEC 基础媒体文件格式 (ISO/IEC 14496-12 或 MPEG-4 Part 12、ISO/IEC 15444-12 或 JPEG 2000 Part 12) 解复用器。

注册的扩展名：mov、mp4、m4a、3gp、3g2、mj2、psp、m4b、ism、ismv、isma、f4v

### 选项

此解复用器接受以下选项：

- **`enable_drefs`** 启用外部轨道 (external track) 的加载，默认禁用。在某些使用场景下启用它理论上可能泄露信息。

- **`use_absolute_path`** 允许通过绝对路径加载外部轨道，默认禁用。启用会带来安全风险。仅在确认来源无恶意时才应启用。

- **`seek_streams_individually`** 定位时逐流单独寻找最近点，并从该点开始解复用该流的包。与从头线性解复用相比，这可能导致不同的包序列。默认值为 true。

- **`ignore_editlist`** 忽略任何 edit list atom。默认情况下，解复用器会修改流索引以反映 edit list 描述的时间线。默认值为 false。

- **`advanced_editlist`** 修改流索引以反映 edit list 描述的时间线。此选项生效要求 `ignore_editlist` 设为 false。若 `ignore_editlist` 与此选项都设为 false，则只修改流索引的开头，以反映 edit list 描述的初始停留时间或起始时间戳。默认值为 true。

- **`ignore_chapters`** 不解析章节。包括 GoPro 'HiLight' 标签/时刻。注意只有输入可定位时才会解析章节。默认值为 false。

- **`use_mfra_for`** 对可定位的分片输入，从媒体分片随机访问 box（如果存在）设置分片的起始时间戳。

  可用选项如下：

  - **`auto`** 自动检测将 mfra 时间戳设为 PTS 还是 DTS *(默认)*

  - **`dts`** 将 mfra 时间戳设为 DTS

  - **`pts`** 将 mfra 时间戳设为 PTS

  - **`0`** 不使用 mfra box 设置时间戳

- **`use_tfdt`** 对分片输入，将分片起始时间戳设为 `tfdt` box 中的 `baseMediaDecodeTime`。默认启用，即优先使用 `tfdt` box 设置 DTS。禁用以使用 `sidx` box 中的 `earliest_presentation_time`。无论哪种情况，若 mfra box 可用且 `use_mfra_for` 设为 pts 或 dts，都会使用 `mfra` box 中的时间戳。

- **`export_all`** 将 \<udta\> box 内未识别的 box 导出为元数据条目。box 类型的前四个字符作为键。默认值为 false。

- **`export_xmp`** 将 \<XMP\_\> box 和 \<uuid\> box 的全部内容导出为键为 `xmp` 的字符串。注意若设置了 `export_all` 而未设置此选项，\<XMP\_\> box 的内容仍会导出，但键为 `XMP_`。默认值为 false。

- **`activation_bytes`** 解密 Audible AAX 与 AAX+ 文件所需的 4 字节密钥。参见下文 Audible AAX 小节。

- **`audible_fixed_key`** 处理 Audible AAX/AAX+ 文件使用的固定密钥。已预先设置，无需指定。

- **`decryption_key`** 默认的 16 字节密钥（十六进制），用于解密使用 ISO 通用加密 (CENC/AES-128 CTR; ISO/IEC 23001-7) 加密的文件。

- **`decryption_keys`** 16 字节密钥 ID =\> 16 字节密钥的字典（均为十六进制），用于解密使用 ISO 通用加密 (CENC/AES-128 CTR; ISO/IEC 23001-7) 加密的文件。

- **`max_stts_delta`** 写入 trak 的 stts box 的极高采样增量偶尔是有意为之，但通常是错误写入，或用于在被当作有符号 32 位整数时存储负值以修正 dts。此选项允许用户设置上限，超过上限的增量会被限制为 1。超出上限的值若转换为 int32 后为负，则用于调整后续 dts。

  单位为轨道时间基 (track time scale)。范围为 0 到 UINT_MAX。默认值为 `UINT_MAX - 48000*10`，它允许 48 kHz 音频流最多 10 秒的 dts 修正，同时覆盖 99.9% 的 `uint32` 范围。

- **`interleaved_read`** 在解复用器层面交错来自多条轨道的包。对交错不良的文件，这可避免不同轨道的包之间的大段空隙引起的播放问题（MOV/MP4 对包位置没有要求）。但这对交错极其糟糕的文件可能造成过度定位（轨道间来回寻道），因此禁用它可能避免 I/O 问题，但牺牲播放质量。

### Audible AAX

Audible AAX 文件是加密的 M4B 文件，可通过指定 4 字节激活密钥解密。

``` text
ffmpeg -activation_bytes 1CEB00DA -i test.aax -vn -c:a copy output.mp4
```

## mpegts

MPEG-2 传输流解复用器。

此解复用器接受以下选项：

- **`resync_size`** 设置查找新同步的大小限制。默认值为 65536。

- **`skip_unknown_pmt`** 跳过未在 PAT 中定义的节目的 PMT。默认值为 0。

- **`fix_teletext_pts`** 用图文电视流所属且未被丢弃的第一个节目的 PCR 计算出的时间戳，覆盖图文电视包的 PTS 和 DTS 值。默认值为 1；若想保持图文电视包的 PTS 与 DTS 原样，将此选项设为 0。

- **`ts_packetsize`** 输出选项，携带以字节为单位的原始包大小。显示检测到的原始包大小，用户无法设置。

- **`scan_all_pmts`** 扫描并合并所有 PMT。取值为 -1 到 1 的整数（-1 表示自动设置，1 表示启用，0 表示禁用）。默认值为 -1。

- **`merge_pmt_versions`** 当 PMT 版本更新且基本流移动到不同 PID 时复用现有流。默认值为 0。

- **`max_packet_size`** 设置解复用器输出包的最大大小（字节）。超过此大小的载荷会被拆分到多个包。范围为 184 到 INT_MAX/2。默认值为 204800 字节。

## mpjpeg

多部分 MIME 封装的 MJPEG 解复用器。

此解复用器允许读取 MJPEG，其中每帧表示为 multipart/x-mixed-replace 流的一部分。

- **`strict_mime_boundary`** 默认实现对多部分 MIME 边界检测采用宽松标准，以避免与大量未生成规范 MIME MJPEG 流的现有端点产生回归。将此选项设为 1 开启后将进行更严格的边界值检查。

## rawvideo

原始视频 (raw video) 解复用器。

此解复用器允许读取原始视频数据。由于没有指定视频参数的头信息，用户必须显式指定它们才能正确解码数据。

此解复用器接受以下选项：

- **`framerate`** 设置输入视频帧率。默认值为 25。

- **`pixel_format`** 设置输入视频像素格式。默认值为 `yuv420p`。

- **`stride`** 设置帧行大小（字节），仅在存在额外填充时需要。对多平面格式，`stride` 是每个平面行大小的列表。

- **`video_size`** 设置输入视频尺寸。此值必须显式指定。

例如，使用 `ffplay` 读取 rawvideo 文件 `input.raw`，假设像素格式为 `rgb24`、视频尺寸为 `320x240`、帧率为每秒 10 幅图像，使用命令：

``` text
ffplay -f rawvideo -pixel_format rgb24 -video_size 320x240 -framerate 10 input.raw
```

使用 `ffplay` 读取 rawvideo，假设像素格式为 `yuv420p`、视频尺寸为 `1080x1920`，Y 平面每行有 8 字节填充，UV 平面有 4 字节填充，

``` text
ffplay -f rawvideo -pixel_format yuv420p -video_size 1080x1920 -stride 1088,544,544 input.raw
```

## rcwt

RCWT (Raw Captions With Time) 是 ccextractor 原生的格式，ccextractor 是处理 608/708 隐藏式字幕 (CC) 源的常用开源工具。关于该格式的更多信息，参见 `ffmpeg-formats` 中的"rcwtenc"。

此解复用器实现 2024 年 3 月版的规范，该规范自 2014 年 4 月以来保持稳定未变。

### 示例

- 使用内置解码器将 CC 渲染为 ASS：

  ``` text
  ffmpeg -i CC.rcwt.bin CC.ass
  ```

  注意如果输出为空，可能需要手动设置解码器的 `data_field` 选项以选择所需的 CC 子流。

- 将 RCWT 备份转换为 Scenarist (SCC) 格式：

  ``` text
  ffmpeg -i CC.rcwt.bin -c:s copy CC.scc
  ```

  注意 SCC 格式不支持 RCWT 中可存储的全部 CC 扩展（如 EIA-708）。

## sbg

SBaGen 脚本解复用器。

此解复用器读取 SBaGen <http://uazu.net/sbagen/> 用来生成双耳节拍 (binaural beats) 会话的脚本语言。SBG 脚本形如：

``` text
-SE
a: 300-2.5/3 440+4.5/0
b: 300-2.5/0 440+4.5/3
off: -
NOW      == a
+0:07:00 == b
+0:14:00 == a
+0:21:00 == b
+0:30:00    off
```

SBG 脚本可混合绝对与相对时间戳。如果脚本只使用绝对时间戳（包括脚本起始时间）或只使用相对时间戳，其布局是固定的，转换很直接。反之，如果脚本混合了两种时间戳，则相对时间戳的 \<NOW\> 参考将取自读取脚本时的当前时刻，脚本布局会根据该参考冻结。这意味着直接播放脚本时，实际时间将与绝对时间戳一致（误差为声音控制器的时钟精度），但如果用户暂停播放或定位，所有时间都会相应偏移。

## tedcaptions

[TED Talks](http://www.ted.com/) 使用的 JSON 字幕。

TED 不提供字幕链接，但可以从页面猜出。FFmpeg 源码树中的文件 `tools/bookmarklets.html` 包含一个用于展示字幕链接的书签脚本 (bookmarklet)。

此解复用器接受以下选项：

- **`start_time`** 设置 TED 演讲的起始时间（毫秒）。默认为 15000（15 秒）。它用于将字幕与可下载视频同步，因为视频包含 15 秒的开场。

示例：将字幕转换为大多数播放器都能理解的格式：

``` text
ffmpeg -i http://www.ted.com/talks/subtitles/id/1/lang/en talk1-en.srt
```

## vapoursynth

VapourSynth 包装器。

出于安全考虑，VapourSynth 脚本不会被自动检测，因此必须强制指定输入格式。对 ff\* 命令行工具，在输入 `-i yourscript.vpy` 之前添加 `-f vapoursynth`。

此解复用器接受以下选项：

- **`max_script_size`** 该解复用器将整个脚本缓冲进内存。调整此值以设置最大缓冲大小，它同时构成可读脚本大小的上限。默认为 1 MiB。

## w64

Sony Wave64 音频解复用器。

此解复用器接受以下选项：

- **`max_size`** 参见 [wav](#wav) 解复用器的同名选项。

## wav

RIFF Wave 音频解复用器。

此解复用器接受以下选项：

- **`ignore_length bool`** 若设置，忽略 `data` chunk 的大小并持续读取到文件末尾。对头信息未正确更新的损坏或不完整文件可能有用，但会误读 `data` chunk 之后带有非音频 chunk 的文件。默认禁用。

- **`max_size`** 指定解复用包的最大包大小（字节）。默认设为 0，表示根据输入格式选择合适的值。

## webp

动图 WebP (Animated WebP) 解复用器。

它接受以下选项：

- **`-min_delay int`** 设置帧间最小有效延迟（毫秒）。范围为 0 到 60000。默认值为 10。

- **`-max_webp_delay int`** 设置帧间最大有效延迟（毫秒）。范围为 0 到 16777215。默认值为 16777215（超过四小时），即规范允许的最大值。

- **`-default_delay int`** 设置帧间默认延迟（毫秒）。范围为 0 到 60000。默认值为 100。

- **`-ignore_loop bool`** WebP 文件可包含按一定次数（或无限次）循环的信息。若 `ignore_loop` 设为 true，则忽略输入中的循环设置，不进行循环。若设为 false，则进行循环，并按 WebP 的设置循环相应次数。默认值为 true。

- **`usebgcolor bool`** WebP 文件在 ANIM chunk 中包含背景颜色提示，但 WebP 规范说明查看器应用不要求使用它。若 `usebgcolor` 设为 true，则使用背景颜色提示，否则背景使用透明黑。默认值为 false。

# 复用器

复用器是 FFmpeg 中的配置元素，用于将多媒体流写入特定类型的文件。

配置 FFmpeg 构建时，所有受支持的复用器默认启用。可以使用 configure 选项 `--list-muxers` 列出全部可用复用器。

可以使用 configure 选项 `--disable-muxers` 禁用全部复用器，并使用选项 `--enable-muxer=MUXER` / `--disable-muxer=MUXER` 选择性启用/禁用单个复用器。

ff\* 工具的 `-muxers` 选项将显示已启用复用器的列表。使用 `-formats` 查看已启用解复用器和复用器的合并列表。

下面介绍部分当前可用的复用器。

## Raw 复用器

本节介绍 raw 复用器。它们接受匹配指定编解码器的单一流。它们不存储时间戳或元数据。可识别的扩展名与复用器名相同，除非另有说明。

它包含以下复用器。表中同时列出媒体类型以及用于根据输出扩展名自动选择复用器的扩展名（如有）。

- **`ac3 audio`** Dolby Digital，又称 AC-3。

- **`adx audio`** CRI Middleware ADX 音频。

  当输出可定位且总数能以 32 位存储时，此复用器会在第一个包开头的附近写出采样总数。

- **`aptx audio`** aptX (Audio Processing Technology for Bluetooth)

- **`aptx_hd audio (aptxdh)`** aptX HD (Audio Processing Technology for Bluetooth) 音频

- **`avs2 video (avs, avs2)`** AVS2-P2 (Audio Video Standard - Second generation - Part 2) / IEEE 1857.4 视频

- **`avs3 video (avs3)`** AVS3-P2 (Audio Video Standard - Third generation - Part 2) / IEEE 1857.10 视频

- **`cavsvideo video (cavs)`** 中国 AVS (Audio Video Standard - First generation)

- **`codec2raw audio`** Codec 2 音频。

  未注册扩展名，因此必须提供格式名，例如通过 ffmpeg 命令行工具的 `-f codec2raw`。

- **`data any`** 通用数据复用器。

  此复用器接受任意类型、任意编解码器的单一流。使用 `ffmpeg` 命令行工具时，必须通过 `-map` 选项选择输入流。

  未注册扩展名，因此必须提供格式名，例如通过 `ffmpeg` 命令行工具的 `-f data`。

- **`dfpwm audio (dfpwm)`** Raw DFPWM1a (Dynamic Filter Pulse With Modulation) 音频复用器。

- **`dirac video (drc, vc2)`** BBC Dirac 视频。

  Dirac Pro 编解码器是其子集，已标准化为 SMPTE VC-2。

- **`dnxhd video (dnxhd, dnxhr)`** Avid DNxHD 视频。

  已标准化为 SMPTE VC-3。接受 DNxHR 流。

- **`dts audio`** DTS Coherent Acoustics (DCA) 音频

- **`eac3 audio`** Dolby Digital Plus，又称 Enhanced AC-3

- **`evc video (evc)`** MPEG-5 Essential Video Coding (EVC) / EVC / MPEG-5 Part 1 EVC 视频

- **`g722 audio`** ITU-T G.722 音频

- **`g723_1 audio (tco, rco)`** ITU-T G.723.1 音频

- **`g726 audio`** ITU-T G.726 大端序（"left-justified"）音频。

  未注册扩展名，因此必须提供格式名，例如通过 `ffmpeg` 命令行工具的 `-f g726`。

- **`g726le audio`** ITU-T G.726 小端序（"right-justified"）音频。

  未注册扩展名，因此必须提供格式名，例如通过 `ffmpeg` 命令行工具的 `-f g726le`。

- **`gsm audio`** 全球移动通信系统 (GSM) 音频

- **`h261 video`** ITU-T H.261 视频

- **`h263 video`** ITU-T H.263 / H.263-1996、H.263+ / H.263-1998 / H.263 version 2 视频

- **`h264 video (h264, 264)`** ITU-T H.264 / MPEG-4 Part 10 AVC 视频。比特流若为长度前缀模式，须转换为 Annex B 语法。

- **`hevc video (hevc, h265, 265)`** ITU-T H.265 / MPEG-H Part 2 HEVC 视频。比特流若为长度前缀模式，须转换为 Annex B 语法。

- **`m4v video`** MPEG-4 Part 2 视频

- **`mjpeg video (mjpg, mjpeg)`** Motion JPEG 视频

- **`mlp audio`** Meridian Lossless Packing，又称 Packed PCM

- **`mp2 audio (mp2, m2a, mpa)`** MPEG-1 Audio Layer II 音频

- **`mpeg1video video (mpg, mpeg, m1v)`** MPEG-1 Part 2 视频。

- **`mpeg2video video (m2v)`** ITU-T H.262 / MPEG-2 Part 2 视频

- **`obu video`** AV1 低开销开放比特流单元 (Open Bitstream Units) 复用器。

  时间分隔符 OBU 会插入流的所有时间单元中。

- **`rawvideo video (yuv, rgb)`** 原始未压缩视频。

- **`sbc audio (sbc, msbc)`** Bluetooth SIG 低复杂度子带编解码器音频

- **`truehd audio (thd)`** Dolby TrueHD 音频

- **`vc1 video`** SMPTE 421M / VC-1 视频

### 示例

- 使用 `ffmpeg` 以 `rawvideo` 复用器存储原始视频帧：

  ``` text
  ffmpeg -f lavfi -i testsrc -t 10 -s hd1080p testsrc.yuv
  ```

  由于 rawvideo 复用器不存储尺寸与格式相关信息，解复用该文件时必须提供这些信息：

  ``` text
  ffplay -video_size 1920x1080 -pixel_format rgb24 -f rawvideo testsrc.rgb
  ```

## Raw PCM 复用器

本节介绍 raw PCM（脉冲编码调制）音频复用器。

它们接受匹配指定编解码器的单一流。它们不存储时间戳或元数据。可识别的扩展名与复用器名相同。

它包含以下复用器。括号中同时列出用于根据输出扩展名自动选择复用器的附加扩展名（如有）。

| Term           | Description                             |
|----------------|-----------------------------------------|
| `alaw (al)`  | PCM A-law（A 律）                               |
| `f32be`      | PCM 32 位浮点大端序    |
| `f32le`      | PCM 32 位浮点小端序 |
| `f64be`      | PCM 64 位浮点大端序    |
| `f64le`      | PCM 64 位浮点小端序 |
| `mulaw (ul)` | PCM mu-law（μ 律）                              |
| `s16be`      | PCM 有符号 16 位大端序            |
| `s16le`      | PCM 有符号 16 位小端序         |
| `s24be`      | PCM 有符号 24 位大端序            |
| `s24le`      | PCM 有符号 24 位小端序         |
| `s32be`      | PCM 有符号 32 位大端序            |
| `s32le`      | PCM 有符号 32 位小端序         |
| `s8 (sb)`    | PCM 有符号 8 位                        |
| `u16be`      | PCM 无符号 16 位大端序          |
| `u16le`      | PCM 无符号 16 位小端序       |
| `u24be`      | PCM 无符号 24 位大端序          |
| `u24le`      | PCM 无符号 24 位小端序       |
| `u32be`      | PCM 无符号 32 位大端序          |
| `u32le`      | PCM 无符号 32 位小端序       |
| `u8 (ub)`    | PCM 无符号 8 位                      |
| `vidc`       | PCM Archimedes VIDC                     |

## MPEG-1/MPEG-2 节目流复用器

本节介绍属于 MPEG-1 与 MPEG-2 Systems 家族的格式。

MPEG-1 Systems 格式（又称 ISO/IEEC 11172-1 或 MPEG-1 节目流）被用作 VCD (Video Compact Disc) 中存储的媒体轨道格式。

MPEG-2 Systems 标准（又称 ISO/IEEC 13818-1）涵盖两种容器格式：一种称为传输流，一种称为节目流；此处只介绍后者。

MPEG-2 节目流格式（因相应文件扩展名又称 VOB）是 MPEG-1 节目流的扩展：除支持为音频流和视频流使用不同编解码器外，它还存储字幕和导航元数据。MPEG-2 节目流被用于 SVCD 和 DVD 存储设备中的媒体流存储。

本节包含以下复用器。

- **`mpeg (mpg,mpeg)`** MPEG-1 Systems / MPEG-1 节目流复用器。

- **`vcd`** MPEG-1 Systems / MPEG-1 节目流 (VCD) 复用器。

  此复用器可用于生成 VCD (Video Compact Disc) 存储设备所接受格式的轨道。

  它与 `mpeg` 复用器相同，仅有少量差异。

- **`vob`** MPEG-2 节目流 (VOB) 复用器。

- **`dvd`** MPEG-2 节目流 (DVD VOB) 复用器。

  此复用器可用于生成 DVD (Digital Versatile Disc) 存储设备所接受格式的轨道。

  它与 `vob` 复用器相同，仅有少量差异。

- **`svcd (vob)`** MPEG-2 节目流 (SVCD VOB) 复用器。

  此复用器可用于生成 SVCD (Super Video Compact Disc) 存储设备所接受格式的轨道。

  它与 `vob` 复用器相同，仅有少量差异。

### 选项

- **`muxrate rate`** 设置用户自定义复用率（单位为比特/秒）。若未指定，则采用自动计算的复用率。默认值为 `0`。

- **`preload delay`** 设置初始解复用-解码延迟（微秒）。默认值为 `500000`。

## MOV/MPEG-4/ISOMBFF 复用器

本节介绍属于 QuickTime / MOV 家族的格式，包括 MPEG-4 Part 14 格式与 ISO 基础媒体文件格式 (ISOBMFF)。这些格式共享基于 ISO 基础媒体文件格式 (ISOBMFF) 的共同结构。

MOV 格式最初为 Apple QuickTime 开发。后来它被用作 MPEG-4 Part 1（后为 Part 14）格式（又称 ISO/IEC 14496-1）的基础。该格式随后被泛化为 ISOBMFF，又称 MPEG-4 Part 12 格式、ISO/IEC 14496-12 或 ISO/IEC 15444-12。

它包含以下复用器。

- **`3gp`** 第三代合作伙伴项目 (3GPP) 用于 3G UMTS 多媒体服务的格式

- **`3g2`** 第三代合作伙伴项目 2 (3GP2 或 3GPP2) 用于 3G CDMA2000 多媒体服务的格式，与 `3gp` 相似，但有扩展与限制

- **`f4v`** Adobe Flash Video 格式

- **`ipod`** MPEG-4 音频文件格式，如同 MOV/MP4 但仅限音频流，通常用 Apple ipod 设备播放

- **`ismv`** Microsoft IIS (Internet Information Services) Smooth Streaming 音频/视频 (ISMV 或 ISMA) 格式。基于 MPEG-4 Part 14 格式，带有少量不兼容变体，用于为 Microsoft IIS 服务器流式传输媒体文件。

- **`mov`** 由 `.mov` 扩展名标识的 QuickTime 播放器格式

- **`mp4`** MP4 或 MPEG-4 Part 14 格式

- **`psp`** PlayStation Portable MP4/MPEG-4 Part 14 格式变体。基于 MPEG-4 Part 14 格式，带有少量不兼容变体，用于在 PlayStation 设备上播放文件。

### 分片

`mov`、`mp4` 和 `ismv` 复用器支持分片 (fragmentation)。通常，MOV/MP4 文件将关于所有包的全部元数据存储在一个位置。

这些数据通常写在文件末尾，但为了更好的播放体验，可以通过向 `-movflags` 添加 `+faststart`（或使用 `qt-faststart` 工具）将其移到文件开头。

分片文件由若干分片 (fragment) 组成，包与关于这些包的元数据存储在一起。写入分片文件的优点是：即使写入被中断，文件也可解码（而普通 MOV/MP4 若未正常结束则不可解码）；并且在写入超长文件时占用更少内存（因为写入普通 MOV/MP4 文件时，关于每个包的信息都会保存在内存中直到文件关闭）。缺点是与其他应用的兼容性较差。

通过设置以下定义如何将文件切分为分片的选项之一来启用分片：

- **`frag_duration`**

- **`frag_size`**

- **`min_frag_duration`**

- **`movflags +frag_keyframe`**

- **`movflags +frag_custom`**

若指定了多个条件，则在满足任一指定条件时切分分片。例外是选项 `min_frag_duration`，它必须满足，其他条件才适用。

### 选项

- **`brand brand_string`** 覆盖主品牌 (major brand)。

- **`empty_hdlr_name bool`** 启用后跳过写入 `hdlr` box 内的名称。默认值为 `false`。

- **`encryption_key key`** 以十六进制格式设置媒体加密密钥

- **`encryption_kid kid`** 以十六进制格式设置媒体加密密钥标识符

- **`encryption_scheme scheme`** 配置加密方案，允许的值为 `none` 与 `cenc-aes-ctr`

- **`frag_duration duration`** 创建时长为 \<duration\> 微秒的分片。

- **`frag_interleave number`** 在分片内交错采样（最大连续采样数；数值越小交错越紧密，但开销越大）。默认设为 `0`。

- **`frag_size size`** 创建最多包含 \<size\> 字节载荷数据的分片

- **`iods_audio_profile profile`** 指定音频 profile atom 的 iods 编号（从 -1 到 255），默认值为 `-1`

- **`iods_video_profile profile`** 指定视频 profile atom 的 iods 编号（从 -1 到 255），默认值为 `-1`

- **`ism_lookahead num_entries`** 指定 ISM 文件的前瞻 (lookahead) 条目数（从 0 到 255），默认值为 `0`

- **`min_frag_duration duration`** 不创建短于 \<duration\> 微秒的分片

- **`moov_size bytes`** 在文件开头为 moov atom 预留空间，而不是把 moov atom 放在文件末尾。若预留空间不足，复用将失败。

- **`mov_gamma gamma`** 指定 gama atom 的 gamma 值（0 到 10 的十进制数），默认值为 `0.0`，必须与 `+ movflags` 一起设置

- **`movflags flags`** 设置各种复用开关。可用标志如下：

  - **`cmaf`** 写入 CMAF (Common Media Application Format) 兼容的分片 MP4 输出

  - **`dash`** 写入 DASH (Dynamic Adaptive Streaming over HTTP) 兼容的分片 MP4 输出

  - **`default_base_moof`** 与 `omit_tfhd_offset` 标志类似，此标志避免在 tfhd atom 中写入绝对 base_data_offset 字段，但改用新的 default-base-is-moof 标志实现。此标志来自 14496-12:2012。在某些情况下可让分片更易解析（避免将轨道分片位置计算基于前一个轨道分片的隐式结尾）。

  - **`delay_moov`** 延迟写入初始 moov，直到切出第一个分片或第一次刷新分片

  - **`disable_chpl`** 禁用 Nero 章节标记 (chpl atom)。通常，Nero 章节与 QuickTime 章节轨道都会写入文件。设置此选项后只写 QuickTime 章节轨道。用某些打标程序（如 mp3Tag 2.61a 与 iTunes 11.3，很可能其他版本也受影响）重新处理文件时，Nero 章节可能导致失败。

  - **`faststart`** 执行第二遍处理，将索引 (moov atom) 移到文件开头。此操作可能耗时，且在分片输出等多种情况下不可用，因此默认不启用。

  - **`frag_custom`** 允许调用方通过调用 `av_write_frame(ctx, NULL)` 手动选择何时切分分片，以写出迄今写入的包组成的一个分片。（这只对集成 libavformat 的其他应用有用，不适用于 `ffmpeg`。）

  - **`frag_discont`** 表示下一个分片与之前的分片不连续

  - **`frag_every_frame`** 每帧切分一个分片

  - **`frag_keyframe`** 在每个视频关键帧处开始新分片

  - **`global_sidx`** 在文件开头写入全局 sidx 索引

  - **`isml`** 创建直播平滑流媒体推送源（用于推流到发布点）

  - **`negative_cts_offsets`** 启用 CTTS box 版本 1，其中 CTS 偏移可为负。这使得初始采样的 DTS/CTS 可以为零，并减少了某些情况（如带 B 帧的视频轨道）对 edit list 的需求。此外，更易符合 DASH-IF 互操作性指南。

    写入 `ismv` (Smooth Streaming) 文件时隐式设置此选项。

  - **`omit_tfhd_offset`** 不在 tfhd atom 中写入任何绝对 base_data_offset。这可避免将分片绑定到文件/流中的绝对字节位置。

  - **`prefer_icc`** 写入 colr atom 时，若流包 side data 中存在 ICC profile，则优先使用它。

  - **`rtphint`** 向输出文件添加 RTP 提示 (hinting) 轨道

  - **`separate_moof`** 为每条轨道写一个独立的 moof (movie fragment) atom。通常，所有轨道的包写在一个 moof atom 中（效率略高），但设置此选项后，复用器为每条轨道写一对 moof/mdat，使轨道更易分离。

  - **`skip_sidx`** 跳过 sidx atom 的写入。当 sidx atom 带来的码率开销较高时，可在 sidx atom 非必需的场景使用此选项。启用 `global_sidx` 标志时忽略此选项。

  - **`skip_trailer`** 跳过为分片文件写 mfra/tfra/mfro 尾部

  - **`use_metadata_tags`** 使用 mdta atom 存储元数据

  - **`write_colr`** 即使颜色信息未指定也写入 colr atom。此标志是实验性的，可能被重命名或更改，请勿在脚本中使用。

  - **`write_gama`** 写入已弃用的 gama atom

  - **`hybrid_fragmented`** 出于可恢复性考虑，将输出文件写成分片文件。这使得中间文件在写入过程中即可被读取（特别是当写入进程不干净地中止时）。写入完成后，文件被转换为常规的非分片文件，兼容性更好，且定位更轻松快速。

    若写入被中止，可手动将中间文件重新封装，从未完成的文件中得到已写入内容的常规非分片文件。

- **`movie_timescale scale`** 设置写入电影头 box (`mvhd`) 的 timescale。范围为 1 到 INT_MAX。默认值为 `1000`。

- **`rtpflags flags`** 向输出文件添加 RTP 提示轨道。

  可用标志如下：

  | Term | Description |
  |----|----|
  | `h264_mode0` | 对 RTP 中的 H.264 使用 mode 0 |
  | `latm` | 对 AAC 使用 MP4A-LATM 封包而不是 MPEG4-GENERIC |
  | `rfc2190` | 对 H.263 使用 RFC 2190 封包而不是 RFC 4629 |
  | `send_bye` | 结束时发送 RTCP BYE 包 |
  | `skip_rtcp` | 不发送 RTCP 发送方报告 |

- **`skip_iods bool`** 跳过 iods atom 的写入（默认值为 `true`）

- **`use_editlist bool`** 使用 edit list（默认值为 `auto`）

- **`use_stream_ids_as_track_ids bool`** 使用流 id 作为轨道 id（默认值为 `false`）

- **`video_track_timescale scale`** 设置视频轨道使用的 timescale。范围为 `0` 到 INT_MAX。若设为 `0`，timescale 将根据原生流时间基自动设置。默认值为 `0`。

- **`write_btrt bool`** 强制或禁用在轨道的 stsd box 内写入码率 box。该 box 包含轨道的解码缓冲大小（字节）、最大码率与平均码率。若这些值都无法计算，将跳过该 box。默认值为 `-1` 或 `auto`，即仅在 MP4 模式下写入。

- **`write_prft option`** 写入带指定时间源的生成者时间参考 box (PRFT)，用于 PRFT box 中的 NTP 字段。设为 `wallclock` 表示时间源为墙上时钟，设为 `pts` 表示时间源为输入包的 PTS 值。

- **`write_tmcd bool`** 设为 `on` 强制写入时间码轨道，`off` 禁用它，`auto` 表示仅为 mov 与 mp4 输出写入时间码轨道（默认）。

  设为 `pts` 仅适用于直播编码场景，其中 PTS 值在源头即按墙上时钟设置。例如使用 decklink 采集源且 `video_pts` 与 `audio_pts` 设为 `abs_wallclock` 的编码场景。

### 示例

- 使用 `ffmpeg` 与 `ismv` 复用器将 Smooth Streaming 内容实时推送到 IIS 上的发布点：

  ``` text
  ffmpeg -re <normal input/transcoding options> -movflags isml+frag_keyframe -f ismv http://server/publishingpoint.isml/Streams(Encoder1)
  ```

## a64

A64 Commodore 64 视频复用器。

此复用器接受单条 `a64_multi` 或 `a64_multi5` 编解码器视频流。

## ac4

Raw AC-4 音频复用器。

此复用器接受单条 `ac4` 音频流。

### 选项

- **`write_crc bool`** 启用后为每个包向输出写入 CRC 校验和，默认值为 `false`

## adts

Audio Data Transport Stream 复用器。

它接受单条 AAC 流。

### 选项

- **`write_id3v2 bool`** 启用后在流开头写入 ID3v2.4 标签。默认禁用。

- **`write_apetag bool`** 启用后在流末尾写入 APE 标签。默认禁用。

- **`write_mpeg2 bool`** 启用后将 ADTS 帧头中的 MPEG 版本位设为 1，表示 MPEG-2。默认值为 0，表示 MPEG-4。

## aea

MD STUDIO 音频复用器。

此复用器接受单条 ATRAC1 音频流，声道数为 1 或 2，采样率为 44100Hz。

由于 AEA 支持存储音轨标题，此复用器还会将流元数据中的标题写入容器。

## aiff

Audio Interchange File Format 复用器。

### 选项

- **`write_id3v2 bool`** 设为 1 时启用 ID3v2 标签写入。默认值为 0（禁用）。

- **`id3v2_version bool`** 选择要写入的 ID3v2 版本。目前仅支持版本 3 与 4（即 ID3v2.3 与 ID3v2.4）。默认为版本 4。

## alp

High Voltage Software 的 Lego Racers 游戏音频复用器。

它接受单条不超过 2 声道、采样率不高于 44100 Hz 的 ADPCM_IMA_ALP 流。

扩展名：`tun`、`pcm`

### 选项

- **`type type`** 设置文件类型。

  \<type\> 接受以下取值：

  - **`tun`** 将文件类型设为音乐。采样率必须为 22050 Hz。

  - **`pcm`** 将文件类型设为音效 (sfx)。

  - **`auto`** 按输出文件扩展名设置文件类型。`.pcm` 得到类型 `pcm`，否则设为类型 `tun`。\<(default)\>

## amr

3GPP AMR (Adaptive Multi-Rate) 音频复用器。

它接受单条包含 AMR NB 流的音频流。

## amv

AMV (Actions Media Video) 格式复用器。

## apm

Ubisoft Rayman 2 APM 音频复用器。

它接受单条 ADPCM IMA APM 音频流。

## apng

动图便携式网络图形 (Animated Portable Network Graphics) 复用器。

它接受单条 APNG 视频流。

### 选项

- **`final_delay delay`** 强制在每次重复的最后一帧之后加上以秒表示的延迟。默认值为 `0.0`。

- **`plays repetitions`** 指定内容播放次数，`0` 表示无限循环，`1` 表示不循环

### 示例

- 使用 `ffmpeg` 生成重复 2 次、且第一次重复后延迟半秒的 APNG 输出：

  ``` text
  ffmpeg -i INPUT -final_delay 0.5 -plays 2 out.apng
  ```

## argo_asf

Argonaut Games ASF 音频复用器。

它接受单条 ADPCM 音频流。

### 选项

- **`version_major version`** 覆盖文件主版本号，以整数指定，默认值为 `2`

- **`version_minor version`** 覆盖文件次版本号，以整数指定，默认值为 `1`

- **`name name`** 将文件名嵌入文件，若未指定则使用输出文件名。名称会截断为 8 个字符。

## argo_cvg

Argonaut Games CVG 音频复用器。

它接受单条单声道 22050Hz ADPCM 音频流。

`loop` 与 `reverb` 选项设置头中相应的标志，之后可检索这些标志来相应处理音频流。

### 选项

- **`skip_rate_check bool`** 跳过采样率检查（默认值为 `false`）

- **`loop bool`** 设置循环标志（默认值为 `false`）

- **`reverb boolean`** 设置混响标志（默认值为 `true`）

## asf, asf_stream

Advanced / Active Systems (or Streaming) Format 音频复用器。

流式传输时应选择 `asf_stream` 变体。

注意 Windows Media Audio (wma) 与 Windows Media Video (wmv) 也使用此复用器。

### 选项

- **`packet_size size`** 设置复用器包大小（字节）。根据源的不同，调整此设置可减少数据碎片或复用器开销。默认值为 `3200`，最小为 `100`，最大为 `64Ki`。

## ass

ASS/SSA (SubStation Alpha) 字幕复用器。

它接受单条 ASS 字幕流。

### 选项

- **`ignore_readorder bool`** 立即写入对话事件（即使乱序），默认值为 `false`；否则会缓存它们，直到找到预期时间的事件。

## ast

AST (Audio Stream) 复用器。

此格式用于在某些 Nintendo Wii 游戏中播放音频。

它接受单条音频流。

`loopstart` 与 `loopend` 选项可用于定义文件中循环的区段，供支持这些选项的播放器使用。

### 选项

- **`loopstart start`** 指定循环起始位置（毫秒），范围 `-1` 到 `INT_MAX`；若设为 `-1` 则不指定循环（默认 -1），且 `loopend` 值被忽略。

- **`loopend end`** 指定循环结束位置（毫秒），范围 `0` 到 `INT_MAX`，默认值为 `0`；若设为 `0` 则视为总流时长。

## au

SUN AU 音频复用器。

它接受单条音频流。

## avi

Audio Video Interleaved 复用器。

AVI 是 Microsoft 开发的专有格式，后来通过 Open DML 规范正式定案。

由于各播放器实现存在差异，可能需要设置一些选项，以确保生成的输出能被目标播放器正确播放。

### 选项

- **`flipped_raw_rgb bool`** 若设为 `true`，为 raw RGB 位图存储正的高度值，表示位图自底向上存储。注意此选项不会翻转位图，翻转须事先手动完成，例如使用 `vflip` 滤镜。默认值为 `false`，表示位图自顶向下存储。

- **`reserve_index_space size`** 在文件头中为每条流的 OpenDML 主索引预留指定的字节数。默认情况下，若第一个主索引没有剩余空间，额外的主索引会嵌入数据包中并链接成索引链。这种索引结构在某些使用场景下会造成问题，例如严格依赖 OpenDML 索引规范的第三方软件，或文件定位缓慢时。在文件头中预留足够的索引空间可避免这些问题。

  所需的索引空间取决于输出文件大小，每吉字节约 16 字节。省略此选项或设为零时会猜测必要的索引空间。

  默认值为 `0`。

- **`write_channel_mask bool`** 将声道布局掩码写入音频流头。

  此选项默认启用。禁用声道掩码在特定场景下有用，例如将多条音频流合并为一条以兼容只支持 AVI 中单条音频流的软件（参见 `ffmpeg-filters` 中"the "amerge" section in the ffmpeg-filters manual"（amerge）一节）。

## avif

AV1 (Alliance for Open Media Video codec 1) 图像格式复用器。

此复用器存储使用 AV1 编解码器编码的图像。

它接受一条或两条视频流。若提供两条视频流，第二条应包含存储透明掩码的单一平面。

若提供多幅图像，生成的输出视为动画 AVIF，循环次数可用 `loop` 选项指定。

这基于 Alliance for Open Media 的规范，网址为 <https://aomediacodec.github.io/av1-avif>。

### 选项

- **`loop count`** 动画 AVIF 的循环次数，`0` 表示无限循环，默认值为 `0`

- **`movie_timescale timescale`** 设置写入电影头 box (`mvhd`) 的 timescale。范围为 1 到 INT_MAX。默认值为 `1000`。

## avm2

ShockWave Flash (SWF) / ActionScript Virtual Machine 2 (AVM2) 格式复用器。

它接受一条音频流、一条视频流或两者兼有。

## bit

G.729 (.bit) 文件格式复用器。

它接受单条 G.729 音频流。

## caf

Apple CAF (Core Audio Format) 复用器。

它接受单条音频流。

## codec2

Codec2 音频复用器。

它接受单条 codec2 音频流。

## chromaprint

Chromaprint 指纹器 (fingerprinter) 复用器。

要启用此滤镜的编译，需要以 `--enable-chromaprint` 配置 FFmpeg。

此复用器将音频数据馈送给 Chromaprint 库，由它为提供的音频数据生成指纹。参见：<https://acoustid.org/chromaprint>

它接受单条至多 2 声道的有符号本机字节序 16 位 raw 音频流。

### 选项

- **`algorithm version`** 选择用于生成指纹的算法版本。范围为 `0` 到 `4`。版本 `3` 启用静音检测。默认值为 `1`。

- **`fp_format format`** 指纹的输出格式。接受以下选项：

  - **`base64`** Base64 压缩指纹 *(默认)*

  - **`compressed`** 二进制压缩指纹

  - **`raw`** 二进制原始指纹

- **`silence_threshold threshold`** 静音检测阈值。范围从 `-1` 到 `32767`，其中 `-1` 禁用静音检测。静音检测只能配合算法版本 `3` 使用。

  使用 AcoustID 服务时必须禁用静音检测。默认值为 `-1`。

## crc

CRC (Cyclic Redundancy Check，循环冗余校验) 复用器。

此复用器计算并打印全部输入音频与视频帧的 Adler-32 CRC。默认情况下，计算 CRC 前音频帧被转换为有符号 16 位 raw 音频，视频帧被转换为 raw 视频。

复用器的输出由单行组成，形如 CRC=0x\<CRC\>，其中 \<CRC\> 是以 0 填充到 8 位的十六进制数，包含全部已解码输入帧的 CRC。

另请参见 [framecrc](#framecrc) 复用器。

### 示例

- 使用 `ffmpeg` 计算输入的 CRC 并存储到文件 `out.crc`：

  ``` text
  ffmpeg -i INPUT -f crc out.crc
  ```

- 使用 `ffmpeg` 将 CRC 打印到标准输出：

  ``` text
  ffmpeg -i INPUT -f crc -
  ```

- 可以通过指定音频与视频编解码器及格式，用 `ffmpeg` 选择每帧的输出格式。例如，计算转换为 PCM 无符号 8 位的输入音频与转换为 MPEG-2 视频的输入视频的 CRC，使用命令：

  ``` text
  ffmpeg -i INPUT -c:a pcm_u8 -c:v mpeg2video -f crc -
  ```

## dash

基于 HTTP 的动态自适应流媒体 (Dynamic Adaptive Streaming over HTTP, DASH) 复用器。

此复用器按照 MPEG-DASH 标准 ISO/IEC 23009-1:2014 及后续标准更新创建分段与清单文件。

更多信息参见：

- ISO DASH 规范：<http://standards.iso.org/ittf/PubliclyAvailableStandards/c065274_ISO_IEC_23009-1_2014.zip>

- WebM DASH 规范：<https://sites.google.com/a/webmproject.org/wiki/adaptive-streaming/webm-dash-specification>

此复用器为每条流创建一个 MPD (Media Presentation Description) 清单文件和分段文件。分段文件与 MPD 清单文件放在同一目录。

分段文件名可以包含预定义标识符，这些标识符在清单 `SegmentTemplate` 小节中使用，如标准 5.3.9.4.4 节所定义。

可用标识符为 `$RepresentationID$`、`$Number$`、`$Bandwidth$` 与 `$Time$`。除标准标识符外，还支持 ffmpeg 特有的 `$ext$` 标识符。指定时，`ffmpeg` 会将文件名中的 `$ext$` 替换为复用格式的扩展名，如 `mp4`、`webm` 等。

### 选项

- **`adaptation_sets adaptation_sets`** 将流分配到适配集 (adaptation set)，在 MPD 清单的 `AdaptationSets` 小节中指定。

  适配集包含一组作为单一子集访问的一条或多条流，例如用户根据可用带宽选择的不同尺寸编码的相应流，或不同语言的多条音频流。

  每个适配集按以下语法指定：

  ``` text
  id=index,streams=streams
  ```

  其中 \<index\> 必须是数值索引，\<streams\> 是以 `,` 分隔的流索引序列。可指定多个适配集，以空格分隔。

  要将全部视频（或音频）流映射到一个适配集，可用 `v`（或 `a`）作为流标识符代替 ID。

  未定义分配时，默认为每条流一个适配集。

  还可指定以下可选字段：

  - **`descriptor`** 按 ISO/IEC 23009-1:2014/Amd.2:2015 的定义指定描述符 (descriptor)。

    例如：

    ``` text
    <SupplementalProperty schemeIdUri=\"urn:mpeg:dash:srd:2014\" value=\"0,0,0,1,1,2,2\"/>
    ```

    描述符字符串应是自闭合的 XML 标签。

  - **`frag_duration`** 覆盖用 `frag_duration` 选项指定的全局分片时长。

  - **`frag_type`** 覆盖用 `frag_type` 选项指定的全局分片类型。

  - **`seg_duration`** 覆盖用 `seg_duration` 选项指定的全局分段时长。

  - **`trick_id`** 将适配集标记为包含用于所引用适配集特技模式 (Trick Mode) 的流。

  下面是 `adaptation_sets` 选项的一些可能取值示例：

  ``` text
  id=0,seg_duration=2,frag_duration=1,frag_type=duration,streams=v id=1,seg_duration=2,frag_type=none,streams=a
  ```

  ``` text
  id=0,seg_duration=2,frag_type=none,streams=0 id=1,seg_duration=10,frag_type=none,trick_id=0,streams=1
  ```

- **`dash_segment_type type`** 设置 DASH 分段文件类型。

  可能的取值：

  - **`auto`** DASH 分段文件格式根据流编解码器选择。这是默认模式。

  - **`mp4`** DASH 分段文件为 ISOBMFF/MP4 格式

  - **`webm`** DASH 分段文件为 WebM 格式

- **`extra_window_size size`** 设置从磁盘移除前保留在清单之外的最大分段数。

- **`format_options options_list`** 使用以 `:` 分隔的 key=value 参数列表设置容器格式 (mp4/webm) 选项。包含 `:` 特殊字符的值必须转义。

- **`frag_duration duration`** 设置分段的分片长度（秒），可设置小数值。

- **`frag_type type`** 设置分片化 (fragmentation) 的间隔类型。

  可能的取值：

  - **`auto`** 每个分段一个分片

  - **`every_frame`** 每帧切分一个分片

  - **`duration`** 按特定时间间隔切分分片

  - **`pframes`** 在关键帧及后续 P 帧重排处切分分片（仅视频，实验性）

- **`global_sidx bool`** 写入全局 `SIDX` atom。仅适用于单文件、mp4 输出、非流式模式。

- **`hls_master_name file_name`** HLS 主播放列表名称。默认为 `master.m3u8`。

- **`hls_playlist bool`** 生成 HLS 播放列表文件。主播放列表按 `hls_master_name` 选项指定的文件名生成。每条流生成一个媒体播放列表文件，文件名为 `media_0.m3u8`、`media_1.m3u8` 等。

- **`http_opts http_opts`** 指定以 `:` 分隔的 key=value 选项列表，传给底层 HTTP 协议。仅适用于 HTTP 输出。

- **`http_persistent bool`** 使用持久 HTTP 连接。仅适用于 HTTP 输出。

- **`http_user_agent user_agent`** 覆盖 HTTP 头中的 User-Agent 字段。仅适用于 HTTP 输出。

- **`ignore_io_errors bool`** 忽略打开和写入期间的 I/O 错误。对网络输出的长时间运行有用。默认禁用。

- **`index_correction bool`** 启用或禁用分段索引修正逻辑。仅在启用 `use_template` 且禁用 `use_timeline` 时适用。默认禁用。

  启用后，该逻辑监测分段索引的流动。若某流的分段索引值不在预期的实时位置，逻辑会修正该索引值。

  直播场景通常需要此逻辑。长时间流式传输期间网络带宽波动很常见，每次波动都可能使分段索引落后于预期的实时位置。

- **`init_seg_name init_name`** 用于初始化分段的 DASH 模板名。默认为 `init-stream$RepresentationID$.$ext$`。`$ext$` 会替换为分段格式特有的文件扩展名。

- **`ldash bool`** 通过约束某些元素的存在与取值启用低延迟 Dash (Low-latency Dash)。默认禁用。

- **`lhls bool`** 启用低延迟 HLS (LHLS)。添加带当前分段 URI 的 `#EXT-X-PREFETCH` 标签。hls.js 播放器社区正尝试标准化开放的 LHLS 规范，草案见 <https://github.com/video-dev/hlsjs-rfcs/blob/lhls-spec/proposals/0001-lhls.md>。

  此选项尽量符合上述开放规范。它会自动启用 `streaming` 与 `hls_playlist` 选项。这是实验性功能。

  注意：这不是 Apple 版本的 LHLS。参见 <https://datatracker.ietf.org/doc/html/draft-pantos-hls-rfc8216bis>

- **`master_m3u8_publish_rate segment_intervals_count`** 每隔指定数量的分段间隔重复发布主播放列表。

- **`max_playback_rate rate`** 设置指示的最大播放速率，供客户端在正常播放期间自动调整播放延迟与缓冲占用。

- **`media_seg_name segment_name`** 用于媒体分段的 DASH 模板名。默认为 `chunk-stream$RepresentationID$-$Number%05d$.$ext$`。`$ext$` 会替换为分段格式特有的文件扩展名。

- **`method method`** 使用给定的 HTTP 方法创建输出文件。通常设为 `PUT` 或 `POST`。

- **`min_playback_rate rate`** 设置指示的最小播放速率，供客户端在正常播放期间自动调整播放延迟与缓冲占用。

- **`mpd_profile flags`** 设置一个或多个 MPD 清单 profile。

  可能的取值：

  | Term         | Description                                       |
  |--------------|---------------------------------------------------|
  | `dash`     | MPEG-DASH ISO 基础媒体文件格式直播 profile |
  | `dvb_dash` | DVB-DASH profile                                  |

  默认值为 `dash`。

- **`remove_at_exit bool`** 启用或禁用完成时移除全部分段。默认禁用。

- **`seg_duration duration`** 设置分段长度（秒，可设小数值）。启用 `use_template` 且禁用 `use_timeline` 时该值作为平均分段时长，其他所有场景下作为最小分段时长。

  默认值为 `5`。

- **`single_file bool`** 启用或禁用将全部分段存储在一个文件中（通过字节范围访问）。默认禁用。

  单文件的名称可用 `single_file_name` 选项指定；未指定时假定为清单文件的基本名加输出格式扩展名。

- **`single_file_name file_name`** 用于清单 `baseURL` 元素的 DASH 模板名。隐含 `single_file` 选项设为 \<true\>。模板中 `$ext$` 会替换为分段格式特有的文件扩展名。

- **`availability_start_time_ms milliseconds`** 将 MPD `availabilityStartTime` 属性设为以毫秒为单位的 Unix 纪元时间。设为 `0` 时，写入第一个包时使用墙上时钟。这对需要在重启间保持稳定可用起始时间的直播输出很有用。

- **`streaming bool`** 启用或禁用输出的分块流式传输模式 (chunk streaming)。此模式下每帧都是一个构成 chunk 的 `moof` 分片。默认禁用。

- **`suggested_presentation_delay duration`** 设置 MPD `suggestedPresentationDelay` 属性。设为 `0` 时使用最后一个分段的时长。

- **`target_latency target_latency`** 设置服务端的预期目标延迟（秒，可设小数值）。仅在启用 `streaming` 与 `write_prft` 选项时适用。这是供客户端测量服务延迟的提示性字段。

- **`timeout timeout`** 设置套接字 I/O 操作超时（秒，可设小数值）。仅适用于 HTTP 输出。

- **`update_period period`** 设置动态内容的 MPD 更新周期。单位为秒。设为 `0` 时自动计算周期。

  默认值为 `0`。

- **`use_template bool`** 启用或禁用在清单中使用 `SegmentTemplate` 而非 `SegmentList`。默认启用。

- **`use_timeline bool`** 启用或禁用在 `SegmentTemplate` 清单小节中使用 `SegmentTimeline`。默认启用。

- **`utc_timing_url url`** 返回 ISO 格式 UTC 时间戳的页面 URL，例如 `https://time.akamai.com/?iso`

- **`window_size size`** 设置清单中保留的最大分段数，丢弃最旧的。对直播有用。

  值为 `0` 时保留清单中的全部分段。默认值为 `0`。

- **`write_prft write_prft`** 在受支持的流上写入生成者参考时间 (Producer Reference Time) 元素。这也会启用底层复用器中的 prft box 写入。仅在启用 \<utc_url\> 选项时适用。默认为 \<auto\>，此时复用器只在需要的模式下尝试启用它。

### 示例

使用 `ffmpeg` 从实时输入源生成 DASH 输出。

从输入文件生成两条多媒体流，均包含经 `libx264` 编码的视频流和以 `libfdk_aac` 编码的音频流。第一条多媒体流包含 800k 码率的视频与默认码率的音频；第二条包含缩放至 320x170 像素、300k 码率的视频与重采样到 22050 Hz 的音频。

`window_size` 选项只保留最近 5 个分段（默认时长 5 秒）。

``` text
ffmpeg -re -i <input> -map 0 -map 0 -c:a libfdk_aac -c:v libx264 \
-b:v:0 800k -profile:v:0 main \
-b:v:1 300k -s:v:1 320x170 -profile:v:1 baseline -ar:a:1 22050 \
-bf 1 -keyint_min 120 -g 120 -sc_threshold 0 -b_strategy 0 \
-use_timeline 1 -use_template 1 -window_size 5 \
-adaptation_sets "id=0,streams=v id=1,streams=a" \
-f dash /path/to/out.mpd
```

## daud

D-Cinema 音频复用器。

它接受单条 6 声道、重采样至 96000 Hz、以 `pcm_24daud` 编解码器编码的音频流。

### 示例

使用 `ffmpeg` 将输入音频复用为重采样至 96000Hz 的 `5.1` 声道布局：

``` text
ffmpeg -i INPUT -af aresample=96000,pan=5.1 slow.302
```

对 7.0 之前的 ffmpeg 版本，可能需要使用 `asetnsamples` 滤镜限制复用包大小，因为此格式不支持复用大于 65535 字节（3640 个采样）的包。对较新的 ffmpeg 版本，音频会自动打包成 36000 字节（2000 个采样）的包。

## dv

DV (Digital Video) 复用器。

它恰好接受一条 `dvvideo` 视频流和至多两条 `pcm_s16` 音频流。更多约束由视频属性（必须对应受支持的 DV 视频 profile）以及帧率定义。

### 示例

使用 `ffmpeg` 转换输入：

``` text
ffmpeg -i INPUT -s:v 720x480 -pix_fmt yuv411p -r 29.97 -ac 2 -ar 48000 -y out.dv
```

## ffmetadata

FFmpeg 元数据复用器。

此复用器以 `ffmetadata` 格式写入流元数据。

格式信息参见 `ffmpeg-formats` 中"the Metadata chapter"（元数据）一章。

### 示例

使用 `ffmpeg` 将输入文件的元数据提取为 `ffmetadata` 格式的 `metadata.ffmeta` 文件：

``` text
ffmpeg -i INPUT -f ffmetadata metadata.ffmeta
```

## fifo

FIFO (First-In First-Out，先进先出) 复用器。

`fifo` 伪复用器 (pseudo-muxer) 通过使用先进先出队列并在独立线程中运行实际复用器，实现编码与复用的分离。

它与 [tee](#tee) 复用器结合使用尤其有用，可用于向多个目标发送数据，各目标具有不同的可靠性/写入速度/延迟。

目标复用器从输出名中选择，或通过 `fifo_format` 选项指定。

当队列填满或输出失败（例如包无法写入输出）时，`fifo` 复用器的行为可以选择：

- 输出可以透明重启，重试之间的延迟可配置（基于实时或被处理流的时间）。

- 临时故障期间可阻塞编码，或在 FIFO 队列填满时透明地继续丢弃包。

API 用户应注意，其 `AVFormatContext` 内使用的回调函数（`interrupt_callback`、`io_open` 与 `io_close`）必须是线程安全的。

### 选项

- **`attempt_recovery bool`** 发生故障时尝试恢复输出。与网络输出配合使用时尤其有用，可以透明地重启流式传输。此选项默认设为 `false`。

- **`drop_pkts_on_overflow bool`** 若设为 `true`，当 fifo 队列填满时将丢弃包而不是阻塞编码器。这使流式传输得以继续而不延迟输入，代价是省略部分流。此选项默认设为 `false`，此时编码器会被阻塞，直到复用器处理掉部分包，且没有包丢失。

- **`fifo_format format_name`** 指定格式名。当无法从输出名后缀猜出格式时有用。

- **`format_opts options`** 指定底层复用器的格式选项。复用器选项可以以 ':' 分隔的 \<key\>=\<value\> 对列表指定。

- **`max_recovery_attempts count`** 设置连续恢复尝试失败的最大次数，超过后输出永久失败。此选项默认设为 `0`（无限）。

- **`queue_size size`** 以包数指定队列大小。默认值为 `60`。

- **`recover_any_error bool`** 若设为 `true`，无论导致故障的错误类型如何都会尝试恢复。此选项默认设为 `false`；发生某些（通常是永久性的）错误时，即使 `attempt_recovery` 选项设为 `true` 也不会尝试恢复。

- **`recovery_wait_streamtime bool`** 若设为 `false`，等待恢复尝试时使用实时（即在 `recovery_wait_time` 选项指定的时间后尝试恢复）。

  若设为 `true`，则改为考虑被处理流的时间（即在丢弃与 `recovery_wait_time` 选项对应的包之后尝试恢复）。

  此选项默认设为 `false`。

- **`recovery_wait_time duration`** 指定上一次恢复尝试失败后到下一次恢复尝试前的等待时间（秒）。默认值为 `5`。

- **`restart_with_keyframe bool`** 指定从队列溢出或故障恢复后是否等待关键帧。此选项默认设为 `false`。

- **`timeshift duration`** 缓冲指定数量的包并延迟写出输出。注意 `queue_size` 选项的值必须大到足以存储时移 (timeshift) 所需的包。输入结束时，fifo 缓冲以实时速度刷新。

### 示例

使用 `ffmpeg` 向 RTMP 服务器推流，在临时故障（网络中断）时仍以实时速率继续处理流，并每秒尝试恢复推流，无限重试：

``` text
ffmpeg -re -i ... -c:v libx264 -c:a aac -f fifo -fifo_format flv \
  -drop_pkts_on_overflow 1 -attempt_recovery 1 -recovery_wait_time 1 \
  -map 0:v -map 0:a rtmp://example.com/live/stream_name
```

## film_cpk

Sega film (.cpk) 复用器。

此格式曾被多款 Sega 游戏用作内部格式。

关于 Sega film 文件格式的更多信息，访问 <http://wiki.multimedia.cx/index.php?title=Sega_FILM>。

它最多接受一条 `cinepak` 或 raw 视频流，以及最多一条音频流。

## filmstrip

Adobe Filmstrip 复用器。

多款 Adobe 工具用此格式存储生成的胶片条 (filmstrip) 导出。它接受单条 raw 视频流。

## fits

灵活图像传输系统 (Flexible Image Transport System, FITS) 复用器。

此图像格式用于存储天文数据。

关于该格式的更多信息，访问 <https://fits.gsfc.nasa.gov>。

## flac

Raw FLAC 音频复用器。

此复用器恰好接受一条 FLAC 音频流。此外，可以添加带 `attached_pic` disposition 的图像。

### 选项

- **`write_header bool`** 设为 `true` 时写文件头，默认值为 `true`

### 示例

使用 `ffmpeg` 存储输入文件的音频流，以及若干配合 `attached_pic` disposition 使用的图片：

``` text
ffmpeg -i INPUT -i pic1.png -i pic2.jpg -map 0:a -map 1 -map 2 -disposition:v attached_pic OUTPUT
```

## flv

Adobe Flash Video Format 复用器。

### 选项

- **`flvflags flags`** 可能的取值：

  - **`aac_seq_header_detect`** 基于音频流数据放置 AAC 序列头。

  - **`no_sequence_end`** 禁用序列结束标签。

  - **`no_metadata`** 禁用元数据标签。

  - **`no_duration_filesize`** 当流末尾的时长与文件大小为零时，禁用元数据中的时长与文件大小。（用于不可定位的直播流）。

  - **`add_keyframe_index`** 用于辅助定位，对 HTTP 伪流 (pseudo streaming) 尤其有用。

## framecrc

逐包 CRC (Cyclic Redundancy Check) 测试格式。

此复用器为每个音频与视频包计算并打印 Adler-32 CRC。默认情况下，计算 CRC 前音频帧被转换为有符号 16 位 raw 音频，视频帧被转换为 raw 视频。

复用器的输出为每个音频与视频包一行，形如：

``` text
stream_index, packet_dts, packet_pts, packet_duration, packet_size, 0xCRC
```

\<CRC\> 是以 0 填充到 8 位的十六进制数，包含该包的 CRC。

### 示例

例如，计算 `INPUT` 中转换为 raw 音频与视频包的音频和视频帧的 CRC，并存储到文件 `out.crc`：

``` text
ffmpeg -i INPUT -f framecrc out.crc
```

将信息打印到标准输出，使用命令：

``` text
ffmpeg -i INPUT -f framecrc -
```

使用 `ffmpeg` 时，可以通过指定音频与视频编解码器，选择在计算每个包的 CRC 前音频与视频帧编码到的输出格式。例如，计算转换为 PCM 无符号 8 位的每个已解码输入音频帧与转换为 MPEG-2 视频的每个已解码输入视频帧的 CRC，使用命令：

``` text
ffmpeg -i INPUT -c:a pcm_u8 -c:v mpeg2video -f framecrc -
```

另请参见 [crc](#crc) 复用器。

## framehash

逐包哈希 (hash) 测试格式。

此复用器为每个音频与视频包计算并打印加密哈希。可用于逐包相等性检查，无需对每个包单独做二进制比较。

默认情况下，计算哈希前音频帧被转换为有符号 16 位 raw 音频，视频帧被转换为 raw 视频，但也可使用显式转换为其他编解码器后的输出。默认使用 SHA-256 加密哈希函数，但也支持若干其他算法。

复用器的输出为每个音频与视频包一行，形如：

``` text
stream_index, packet_dts, packet_pts, packet_duration, packet_size, hash
```

\<hash\> 是表示该包计算所得哈希的十六进制数。

- **`hash algorithm`** 使用字符串 \<algorithm\> 指定的加密哈希函数。支持的值包括 `MD5`、`murmur3`、`RIPEMD128`、`RIPEMD160`、`RIPEMD256`、`RIPEMD320`、`SHA160`、`SHA224`、`SHA256`（默认）、`SHA512/224`、`SHA512/256`、`SHA384`、`SHA512`、`CRC32` 与 `adler32`。

### 示例

计算 `INPUT` 中转换为 raw 音频与视频包的音频和视频帧的 SHA-256 哈希，并存储到文件 `out.sha256`：

``` text
ffmpeg -i INPUT -f framehash out.sha256
```

以 MD5 哈希函数将信息打印到标准输出，使用命令：

``` text
ffmpeg -i INPUT -f framehash -hash md5 -
```

另请参见 [hash](#hash) 复用器。

## framemd5

逐包 MD5 测试格式。

这是 [framehash](#framehash) 复用器的变体。与该复用器不同，它默认使用 MD5 哈希函数。

### 示例

计算 `INPUT` 中转换为 raw 音频与视频包的音频和视频帧的 MD5 哈希，并存储到文件 `out.md5`：

``` text
ffmpeg -i INPUT -f framemd5 out.md5
```

将信息打印到标准输出，使用命令：

``` text
ffmpeg -i INPUT -f framemd5 -
```

另请参见 [framehash](#framehash) 与 [md5](#md5) 复用器。

## gif

动图 GIF (Animated GIF) 复用器。

注意 GIF 格式的时间基非常大：两帧之间的延迟因此不能小于一百分之一秒。

### 选项

- **`loop bool`** 设置输出循环次数。`-1` 表示不循环，`0` 表示无限循环（默认）。

- **`final_delay delay`** 强制最后一帧之后的延迟（以百分之一秒表示）。每帧以到下一帧的延迟结尾。默认值为 `-1`，这是一个特殊值，告诉复用器复用上一个延迟。循环时可能需要自定义此值，例如用于标记停顿。

### 示例

编码循环 10 次、循环间延迟 5 秒的 GIF：

``` text
ffmpeg -i INPUT -loop 10 -final_delay 500 out.gif
```

注意 1：若希望将帧提取为单独的 GIF 文件，需要强制使用 [image2](#image2) 复用器：

``` text
ffmpeg -i INPUT -c:v gif -f image2 "out%d.gif"
```

## gxf

通用交换格式 (General eXchange Format, GXF) 复用器。

GXF 由 Grass Valley Group 开发，后由 SMPTE 标准化为 SMPTE 360M，并在 SMPTE RDD 14-2007 中扩展以支持高清视频分辨率。

它最多接受一条编解码器为 `mjpeg`、`mpeg1video`、`mpeg2video`，或分辨率为 `512x480` 或 `608x576` 的 `dvvideo` 视频流，以及若干采样率 48000Hz、编解码器为 `pcm16_le` 的音频流。

## hash

哈希 (hash) 测试格式。

此复用器计算并打印全部输入音频与视频帧的加密哈希。可用于相等性检查，无需做完整的二进制比较。

默认情况下，计算哈希前音频帧被转换为有符号 16 位 raw 音频，视频帧被转换为 raw 视频，但也可使用显式转换为其他编解码器后的输出。时间戳被忽略。默认使用 SHA-256 加密哈希函数，但也支持若干其他算法。

复用器的输出由单行组成，形如 \<algo\>=\<hash\>，其中 \<algo\> 是表示所用哈希函数的短字符串，\<hash\> 是表示计算所得哈希的十六进制数。

- **`hash algorithm`** 使用字符串 \<algorithm\> 指定的加密哈希函数。支持的值包括 `MD5`、`murmur3`、`RIPEMD128`、`RIPEMD160`、`RIPEMD256`、`RIPEMD320`、`SHA160`、`SHA224`、`SHA256`（默认）、`SHA512/224`、`SHA512/256`、`SHA384`、`SHA512`、`CRC32` 与 `adler32`。

### 示例

计算转换为 raw 音频与视频的输入的 SHA-256 哈希，并存储到文件 `out.sha256`：

``` text
ffmpeg -i INPUT -f hash out.sha256
```

将 MD5 哈希打印到标准输出，使用命令：

``` text
ffmpeg -i INPUT -f hash -hash md5 -
```

另请参见 [framehash](#framehash) 复用器。

## hds

HTTP 动态流媒体 (HTTP Dynamic Streaming, HDS) 复用器。

HTTP 动态流媒体（HDS）是 Adobe 开发的自适应码率流媒体方法。HDS 通过 HTTP 连接交付 MP4 视频内容。HDS 可用于点播流或直播流。

此复用器在指定为输出的目录中创建一个 .f4m (Adobe Flash Media Manifest File) 清单、每条流一个 .abst (Adobe Bootstrap File)，以及分段文件。

HDS 播放器需要通过 HTTPS 访问这些文件，才能对生成的流进行播放。

### 选项

- **`extra_window_size int`** 从磁盘移除前保留在清单之外的分片数

- **`min_frag_duration microseconds`** 最小分片时长（微秒），默认值为 1 秒 (`10000000`)

- **`remove_at_exit bool`** 设为 `true` 时完成时移除全部分片

- **`window_size int`** 清单中保留的分片数（若设为非 `0` 值）。默认情况下全部分段都保留在输出目录中。

### 示例

使用 `ffmpeg` 以实时速率向 `output.hds` 目录生成 HDS 文件：

``` text
ffmpeg -re -i INPUT -f hds -b:v 200k output.hds
```

## hls

Apple HTTP Live Streaming 复用器，按 HTTP Live Streaming (HLS) 规范对 MPEG-TS 分段。

它创建一个播放列表文件和一个或多个分段文件。输出文件名即播放列表文件名。

默认情况下，复用器为每个生成的分段创建一个文件。这些文件与播放列表同名，后接顺序编号和 .ts 扩展名。

编码时务必要求封闭 GOP (closed GOP)，并将 GOP 大小设为符合分段时长约束。

例如，使用 `ffmpeg` 转换输入文件：

``` text
ffmpeg -i in.mkv -c:v h264 -flags +cgop -g 30 -hls_time 1 out.m3u8
```

此示例将生成播放列表 `out.m3u8` 和分段文件：`out0.ts`、`out1.ts`、`out2.ts` 等。

另请参见 [segment](#segment) 复用器，它提供了更通用灵活的分段器实现，可用于执行 HLS 分段。

### 选项

- **`hls_init_time duration`** 设置初始目标分段长度。默认值为 \<0\>。

  \<duration\> 必须是时长描述 (time duration specification)，参见 `ffmpeg-utils` 中"the Time duration section in the ffmpeg-utils(1) manual"（时长）一节。

  在第一个 m3u8 列表上经过该时间后，将在下一个关键帧处切分分段。初始播放列表填满后，`ffmpeg` 将按等于 `hls_time` 的时长切分分段。

- **`hls_time duration`** 设置目标分段长度。默认值为 2。

  \<duration\> 必须是时长描述 (time duration specification)，参见 `ffmpeg-utils` 中"the Time duration section in the ffmpeg-utils(1) manual"（时长）一节。经过该时间后将在下一个关键帧处切分分段。

- **`hls_list_size size`** 设置播放列表条目的最大数量。设为 0 时列表文件将包含全部分段。默认值为 5。

- **`hls_delete_threshold size`** 设置在 `hls_flags delete_segments` 删除前，磁盘上保留的未被引用分段的数量。增大此值可让客户端继续下载播放列表中最近引用过的分段。默认值为 1，即早于 `hls_list_size+1` 的分段会被删除。

- **`hls_start_number_source source`** 按指定来源开始播放列表序号 (`#EXT-X-MEDIA-SEQUENCE`)。除非设置了 `hls_flags single_file`，它还指定分段与字幕文件名起始序号的来源。无论如何，若设置了 `hls_flags append_list` 且读取到的播放列表序号大于指定的起始序号，则使用该值作为起始值。

  它接受以下取值：

  - **`generic (default)`** 根据 `start_number` 选项的值设置起始编号。

  - **`epoch`** 将起始编号设为自纪元 (1970-01-01 00:00:00) 以来的秒数。

  - **`epoch_us`** 将起始编号设为自纪元 (1970-01-01 00:00:00) 以来的微秒数。

  - **`datetime`** 基于当前日期/时间（格式 YYYYmmddHHMMSS）设置起始编号，例如 20161231235759。

- **`start_number number`** 当 `hls_start_number_source` 值为 \<generic\> 时（这是默认情况），从指定的 \<number\> 开始播放列表序号 (`#EXT-X-MEDIA-SEQUENCE`)。除非设置了 `hls_flags single_file`，它还指定分段与字幕文件名的起始序号。默认值为 0。

- **`hls_allow_cache bool`** 显式设置客户端是否可以 (1) 或不得 (0) 缓存媒体分段。

- **`hls_base_url baseurl`** 将 \<baseurl\> 追加到播放列表的每个条目。用于生成带绝对路径的播放列表。

  注意播放列表序号对每个分段必须唯一，不要与分段文件名序号混淆——后者可以是循环的，例如指定了 `wrap` 选项时。

- **`hls_segment_filename filename`** 设置分段文件名。除非 `hls_flags` 选项设为 `single_file`，\<filename\> 将作为字符串格式使用，后接分段编号。

  例如：

  ``` text
  ffmpeg -i in.nut -hls_segment_filename 'file%03d.ts' out.m3u8
  ```

  将生成播放列表 `out.m3u8` 和分段文件：`file000.ts`、`file001.ts`、`file002.ts` 等。

  \<filename\> 可包含完整路径或相对路径说明，但 m3u8 分段列表中只包含不带任何路径的文件名部分。若指定相对路径，创建的分段文件的路径将相对于当前工作目录。设置 `strftime_mkdir` 时，\<filename\> 展开后的完整值会写入 m3u8 分段列表。

  当 `var_stream_map` 设置了两个或更多变体流时，\<filename\> 模式必须包含字符串 "%v"，该字符串会展开为变体流索引在生成的分段文件名中的位置。

  例如：

  ``` text
  ffmpeg -i in.ts -b:v:0 1000k -b:v:1 256k -b:a:0 64k -b:a:1 32k \
    -map 0:v -map 0:a -map 0:v -map 0:a -f hls -var_stream_map "v:0,a:0 v:1,a:1" \
    -hls_segment_filename 'file_%v_%03d.ts' out_%v.m3u8
  ```

  将生成播放列表分段文件集：`file_0_000.ts`、`file_0_001.ts`、`file_0_002.ts` 等，以及 `file_1_000.ts`、`file_1_001.ts`、`file_1_002.ts` 等。

  字符串 "%v" 可出现在文件名或包含该文件的最后一级目录名中，但只能出现在其中之一。（此外，%v 可在最后一级子目录或文件名中出现多次。）若 %v 出现在目录名中，则会在展开目录名模式后创建子目录。这使得可以在子目录中创建对应不同变体流的分段。

  例如：

  ``` text
  ffmpeg -i in.ts -b:v:0 1000k -b:v:1 256k -b:a:0 64k -b:a:1 32k \
    -map 0:v -map 0:a -map 0:v -map 0:a -f hls -var_stream_map "v:0,a:0 v:1,a:1" \
    -hls_segment_filename 'vs%v/file_%03d.ts' vs%v/out.m3u8
  ```

  将生成播放列表分段文件集：`vs0/file_000.ts`、`vs0/file_001.ts`、`vs0/file_002.ts` 等，以及 `vs1/file_000.ts`、`vs1/file_001.ts`、`vs1/file_002.ts` 等。

- **`strftime bool`** 对 \<filename\> 使用 `strftime()` 以本地时间展开分段文件名。此模式下分段编号同样可用，但使用它需要在 `hls_flag` 中设置 `second_level_segment_index`，且以 %%d 作为说明符。

  例如：

  ``` text
  ffmpeg -i in.nut -strftime 1 -hls_segment_filename 'file-%Y%m%d-%s.ts' out.m3u8
  ```

  将生成播放列表 `out.m3u8` 和分段文件：`file-20160215-1455569023.ts`、`file-20160215-1455569024.ts` 等。注意：在某些系统/环境中，`%s` 说明符不可用。参见 `strftime()` 文档。

  例如：

  ``` text
  ffmpeg -i in.nut -strftime 1 -hls_flags second_level_segment_index -hls_segment_filename 'file-%Y%m%d-%%04d.ts' out.m3u8
  ```

  将生成播放列表 `out.m3u8` 和分段文件：`file-20160215-0001.ts`、`file-20160215-0002.ts` 等。

- **`strftime_mkdir bool`** 与 `strftime` 配合使用，它将创建选项 `hls_segment_filename` 展开值中出现的所有子目录。

  例如：

  ``` text
  ffmpeg -i in.nut -strftime 1 -strftime_mkdir 1 -hls_segment_filename '%Y%m%d/file-%Y%m%d-%s.ts' out.m3u8
  ```

  将创建目录 `201560215`（如果不存在），然后生成播放列表 `out.m3u8` 和分段文件：`20160215/file-20160215-1455569023.ts`、`20160215/file-20160215-1455569024.ts` 等。

  例如：

  ``` text
  ffmpeg -i in.nut -strftime 1 -strftime_mkdir 1 -hls_segment_filename '%Y/%m/%d/file-%Y%m%d-%s.ts' out.m3u8
  ```

  将创建目录层级 `2016/02/15`（如果任一层不存在），然后生成播放列表 `out.m3u8` 和分段文件：`2016/02/15/file-20160215-1455569023.ts`、`2016/02/15/file-20160215-1455569024.ts` 等。

- **`hls_segment_options options_list`** 使用以 :-分隔的 key=value 参数列表设置输出格式选项。包含 `:` 特殊字符的值必须转义。

- **`hls_key_info_file key_info_file`** 使用 \<key_info_file\> 中的信息进行分段加密。\<key_info_file\> 的第一行指定写入播放列表的密钥 URI。密钥 URL 用于播放期间访问加密密钥。第二行指定加密过程中获取密钥的密钥文件路径。密钥文件按二进制格式的 16 个八位组的单一打包数组读取。可选的第三行指定初始化向量 (IV)（十六进制字符串），代替默认的分段序号用于加密。若启用 `hls_flags periodic_rekey`，对 \<key_info_file\> 的更改将导致用新密钥/IV 进行分段加密，并在播放列表中添加新密钥 URI/IV 的条目。

  密钥信息文件格式：

  ``` text
  key URI
  key file path
  IV (optional)
  ```

  密钥 URI 示例：

  ``` text
  http://server/file.key
  /path/to/file.key
  file.key
  ```

  密钥文件路径示例：

  ``` text
  file.key
  /path/to/file.key
  ```

  IV 示例：

  ``` text
  0123456789ABCDEF0123456789ABCDEF
  ```

  密钥信息文件示例：

  ``` text
  http://server/file.key
  /path/to/file.key
  0123456789ABCDEF0123456789ABCDEF
  ```

  Shell 脚本示例：

  ``` shell
  #!/bin/sh
  BASE_URL=${1:-'.'}
  openssl rand 16 > file.key
  echo $BASE_URL/file.key > file.keyinfo
  echo file.key >> file.keyinfo
  echo $(openssl rand -hex 16) >> file.keyinfo
  ffmpeg -f lavfi -re -i testsrc -c:v h264 -hls_flags delete_segments \
    -hls_key_info_file file.keyinfo out.m3u8
  ```

- **`hls_enc bool`** 启用 (1) 或禁用 (0) AES128 加密。启用后每个生成的分段都会被加密，加密密钥保存为 \<playlist name\>.key。

- **`hls_enc_key key`** 指定用于加密分段的 16 八位组密钥，默认随机生成。

- **`hls_enc_key_url keyurl`** 若设置，播放列表中的密钥文件名前附加 \<keyurl\> 而不是 \<baseurl\>。

- **`hls_enc_iv iv`** 为每个分段指定 16 八位组初始化向量，代替自动生成的。

- **`hls_segment_type flags`** 可能的取值：

  - **`mpegts`** 以 MPEG-2 传输流格式输出分段文件。与所有 HLS 版本兼容。

  - **`fmp4`** 以分片 MP4 格式输出分段文件，类似 MPEG-DASH。fmp4 文件可用于 HLS 版本 7 及以上。

- **`hls_fmp4_init_filename filename`** 设置分片文件头文件的文件名，默认文件名为 `init.mp4`。

  启用 `strftime` 时，\<filename\> 会按本地时间展开为分段文件名。

  例如：

  ``` text
  ffmpeg -i in.nut -hls_segment_type fmp4 -strftime 1 -hls_fmp4_init_filename "%s_init.mp4" out.m3u8
  ```

  将生成形如 `1602678741_init.mp4` 的 init 文件。

- **`hls_fmp4_init_resend bool`** 每次刷新 m3u8 文件后重发 init 文件，默认为 \<0\>。

  当 `var_stream_map` 设置了两个或更多变体流时，\<filename\> 模式必须包含字符串 "%v"，该字符串指定变体流索引在生成的 init 文件名中的位置。字符串 "%v" 可出现在文件名或包含该文件的最后一级目录名中。若字符串出现在目录名中，则会在展开目录名模式后创建子目录。这使得可以在子目录中创建对应不同变体流的 init 文件。

- **`hls_flags flags`** 可能的取值：

  - **`single_file`** 若设置此标志，复用器将全部分段存储在单个 MPEG-TS 文件中，并在播放列表中使用字节范围。以此方式生成的 HLS 播放列表版本号为 4。

    例如：

    ``` text
    ffmpeg -i in.nut -hls_flags single_file out.m3u8
    ```

    将生成播放列表 `out.m3u8` 和单个分段文件 `out.ts`。

  - **`delete_segments`** 从播放列表移除的分段文件在等于分段时长加播放列表时长的期间过后被删除。

  - **`append_list`** 将新分段追加到旧分段列表末尾，并从旧分段列表移除 `#EXT-X-ENDLIST`。

  - **`round_durations`** 将播放列表文件分段信息中的时长取整为整数，而不是使用浮点数。若没有其他需要更高 HLS 版本的特性，这将允许 `ffmpeg` 输出 HLS 版本 2 的 m3u8。

  - **`discont_start`** 在第一个分段信息之前向播放列表添加 `#EXT-X-DISCONTINUITY` 标签。

  - **`omit_endlist`** 不在播放列表末尾追加 `EXT-X-ENDLIST` 标签。

  - **`periodic_rekey`** 定期检查 `hls_key_info_file` 指定的文件并检测加密信息的更新。务必原子性地替换该文件，包括包含 AES 加密密钥的文件。

  - **`independent_segments`** 对含视频分段、且其全部分段保证以关键帧开始的播放列表添加 `#EXT-X-INDEPENDENT-SEGMENTS` 标签。

  - **`iframes_only`** 对含视频分段、且可在 `#EXT-X-BYTERANGE` 模式下只播放 I 帧的播放列表添加 `#EXT-X-I-FRAMES-ONLY` 标签。

  - **`split_by_time`** 允许分段在非关键帧处开始。这改善了关键帧间隔不一致时某些播放器的行为，但可能使另一些播放器变差，并可能在定位时引起一些怪异现象。此标志应与 `hls_time` 选项配合使用。

  - **`program_date_time`** 生成 `EXT-X-PROGRAM-DATE-TIME` 标签。

  - **`second_level_segment_index`** 当 `strftime` 选项开启时，使分段编号可作为 %%d 用于 `hls_segment_filename` 选项表达式中的日期/时间值之外。要获得带尾零的定宽数字，可使用 %%0xd 格式，其中 x 为所需宽度。

  - **`second_level_segment_size`** 当 strftime 开启时，使分段大小（以字节计）可作为 %%s 用于 `hls_segment_filename` 选项表达式中的日期/时间值之外。要获得带尾零的定宽数字，可使用 %%0xs 格式，其中 x 为所需宽度。

  - **`second_level_segment_duration`** 当 strftime 开启时，使分段时长（以微秒计）可作为 %%t 用于 `hls_segment_filename` 选项表达式中的日期/时间值之外。要获得带尾零的定宽数字，可使用 %%0xt 格式，其中 x 为所需宽度。

    例如：

    ``` text
    ffmpeg -i sample.mpeg \
       -f hls -hls_time 3 -hls_list_size 5 \
       -hls_flags second_level_segment_index+second_level_segment_size+second_level_segment_duration \
       -strftime 1 -strftime_mkdir 1 -hls_segment_filename "segment_%Y%m%d%H%M%S_%%04d_%%08s_%%013t.ts" stream.m3u8
    ```

    将生成形如 `segment_20170102194334_0003_00122200_0000003000000.ts`、`segment_20170102194334_0004_00120072_0000003000000.ts` 等的分段。

  - **`temp_file`** 将分段数据写入 `filename.tmp`，仅在分段完成后才重命名为 filename。

    提供分段的 web 服务器可配置为拒绝 \*.tmp 请求，以防止在分段加入 m3u8 播放列表之前访问进行中的分段。

    此标志还影响 m3u8 播放列表文件的创建方式。设置此标志后，所有播放列表文件都会先写入临时文件，完成后重命名，与分段的处理方式类似。但使用 `file` 协议且 `hls_playlist_type` 非 `vod` 的播放列表，无论此标志如何，总是写入临时文件。

    用 `master_pl_name` 指定的主播放列表文件（如有），使用 `file` 协议时，若 `master_pl_publish_rate` 值非零，无论此标志如何总是写入临时文件。

- **`hls_playlist_type type`** 若 type 为 `event`，在 m3u8 头中输出 `#EXT-X-PLAYLIST-TYPE:EVENT`。这强制 `hls_list_size` 为 0；播放列表只能追加。

  若 type 为 `vod`，在 m3u8 头中输出 `#EXT-X-PLAYLIST-TYPE:VOD`。这强制 `hls_list_size` 为 0；播放列表不得改变。

- **`method method`** 使用给定的 HTTP 方法创建 hls 文件。

  例如：

  ``` text
  ffmpeg -re -i in.ts -f hls -method PUT http://example.com/live/out.m3u8
  ```

  将用 HTTP PUT 方法上传所有 mpegts 分段文件到 HTTP 服务器，并每 `refresh` 次用相同方法更新 m3u8 文件。注意 HTTP 服务器必须支持该上传方法。

- **`http_user_agent agent`** 覆盖 HTTP 头中的 User-Agent 字段。仅适用于 HTTP 输出。

- **`var_stream_map stream_map`** 指定映射字符串，定义如何将音频、视频和字幕流分组为不同变体流。变体流组以空格分隔。

  预期字符串格式形如 "a:0,v:0 a:1,v:1 ...."。其中 a:、v:、s: 分别是指定音频、视频和字幕流的键。允许的值为 0 到 9（仅基于实际用量的限制）。

  有两个或更多变体流时，输出文件名模式必须包含字符串 "%v"：该字符串指定变体流索引在输出媒体播放列表文件名中的位置。字符串 "%v" 可出现在文件名或包含该文件的最后一级目录名中。若字符串出现在目录名中，则会在展开目录名模式后创建子目录。这使得可以在子目录中创建变体流。

  举几例说明。

  - 创建两个 hls 变体流。第一个变体流包含 1000k 码率的视频流与 64k 码率的音频流，第二个变体流包含 256k 码率的视频流与 32k 码率的音频流。这里将创建文件名为 `out_0.m3u8` 与 `out_1.m3u8` 的两个媒体播放列表。

    ``` text
    ffmpeg -re -i in.ts -b:v:0 1000k -b:v:1 256k -b:a:0 64k -b:a:1 32k \
      -map 0:v -map 0:a -map 0:v -map 0:a -f hls -var_stream_map "v:0,a:0 v:1,a:1" \
      http://example.com/live/out_%v.m3u8
    ```

  - 若希望结果名称中出现有意义的文本而不是索引，可为每个或部分变体指定名称。下例创建与前例相同的两个 hls 变体流。但这里将创建文件名为 `out_my_hd.m3u8` 与 `out_my_sd.m3u8` 的两个媒体播放列表。

    ``` text
    ffmpeg -re -i in.ts -b:v:0 1000k -b:v:1 256k -b:a:0 64k -b:a:1 32k \
      -map 0:v -map 0:a -map 0:v -map 0:a -f hls -var_stream_map "v:0,a:0,name:my_hd v:1,a:1,name:my_sd" \
      http://example.com/live/out_%v.m3u8
    ```

  - 创建三个 hls 变体流。第一个变体流是 1000k 码率的纯视频流，第二个变体流是 64k 码率的纯音频流，第三个变体流是 256k 码率的纯视频流。这里将创建文件名为 `out_0.m3u8`、`out_1.m3u8` 与 `out_2.m3u8` 的三个媒体播放列表。

    ``` text
    ffmpeg -re -i in.ts -b:v:0 1000k -b:v:1 256k -b:a:0 64k \
      -map 0:v -map 0:a -map 0:v -f hls -var_stream_map "v:0 a:0 v:1" \
      http://example.com/live/out_%v.m3u8
    ```

  - 在子目录中创建变体流。这里，第一个媒体播放列表创建于 `http://example.com/live/vs_0/out.m3u8`，第二个创建于 `http://example.com/live/vs_1/out.m3u8`。

    ``` text
    ffmpeg -re -i in.ts -b:v:0 1000k -b:v:1 256k -b:a:0 64k -b:a:1 32k \
      -map 0:v -map 0:a -map 0:v -map 0:a -f hls -var_stream_map "v:0,a:0 v:1,a:1" \
      http://example.com/live/vs_%v/out.m3u8
    ```

  - 创建两条纯音频与两条纯视频变体流。除主播放列表中每个变体流的 `#EXT-X-STREAM-INF` 标签外，还会为两条纯音频变体流添加 `#EXT-X-MEDIA` 标签，并用音频组名 'aud_low' 与 'aud_high' 将它们映射到两条纯视频变体流。默认情况下会创建包含全部已编码流的单个 hls 变体。

    ``` text
    ffmpeg -re -i in.ts -b:a:0 32k -b:a:1 64k -b:v:0 1000k -b:v:1 3000k  \
      -map 0:a -map 0:a -map 0:v -map 0:v -f hls \
      -var_stream_map "a:0,agroup:aud_low a:1,agroup:aud_high v:0,agroup:aud_low v:1,agroup:aud_high" \
      -master_pl_name master.m3u8 \
      http://example.com/live/out_%v.m3u8
    ```

  - 创建两条纯音频与一条纯视频变体流。除主播放列表中每个变体流的 `#EXT-X-STREAM-INF` 标签外，还会为两条纯音频变体流添加 `#EXT-X-MEDIA` 标签，并用音频组名 'aud_low' 将它们映射到那条纯视频变体流，音频组的默认状态为 NO 或 YES。默认情况下会创建包含全部已编码流的单个 hls 变体。

    ``` text
    ffmpeg -re -i in.ts -b:a:0 32k -b:a:1 64k -b:v:0 1000k \
      -map 0:a -map 0:a -map 0:v -f hls \
      -var_stream_map "a:0,agroup:aud_low,default:yes a:1,agroup:aud_low v:0,agroup:aud_low" \
      -master_pl_name master.m3u8 \
      http://example.com/live/out_%v.m3u8
    ```

  - 创建两条纯音频与一条纯视频变体流。除主播放列表中每个变体流的 `#EXT-X-STREAM-INF` 标签外，还会为两条纯音频变体流添加 `#EXT-X-MEDIA` 标签，并用音频组名 'aud_low' 将它们映射到那条纯视频变体流，音频组的默认状态为 NO 或 YES，且一条音频的语言名为 ENG，另一条音频的语言名为 CHN。默认情况下会创建包含全部已编码流的单个 hls 变体。

    ``` text
    ffmpeg -re -i in.ts -b:a:0 32k -b:a:1 64k -b:v:0 1000k \
      -map 0:a -map 0:a -map 0:v -f hls \
      -var_stream_map "a:0,agroup:aud_low,default:yes,language:ENG a:1,agroup:aud_low,language:CHN v:0,agroup:aud_low" \
      -master_pl_name master.m3u8 \
      http://example.com/live/out_%v.m3u8
    ```

  - 创建单条变体流。在主播放列表中添加带 `TYPE=SUBTITLES` 的 `#EXT-X-MEDIA` 标签，webvtt 字幕组名为 'subtitle'，可选字幕名如 'English'。确保输入文件至少有一条文本字幕流。

    ``` text
    ffmpeg -y -i input_with_subtitle.mkv \
     -b:v:0 5250k -c:v h264 -pix_fmt yuv420p -profile:v main -level 4.1 \
     -b:a:0 256k \
     -c:s webvtt -c:a mp2 -ar 48000 -ac 2 -map 0:v -map 0:a:0 -map 0:s:0 \
     -f hls -var_stream_map "v:0,a:0,s:0,sgroup:subtitle,sname:English" \
     -master_pl_name master.m3u8 -t 300 -hls_time 10 -hls_init_time 4 -hls_list_size \
     10 -master_pl_publish_rate 10 -hls_flags \
     delete_segments+discont_start+split_by_time ./tmp/video.m3u8
    ```

- **`cc_stream_map cc_stream_map`** 映射字符串，指定不同的隐藏式字幕组及其属性。隐藏式字幕流组以空格分隔。

  预期字符串格式形如 "ccgroup:\<group name\>,instreamid:\<INSTREAM-ID\>,language:\<language code\> ...."。'ccgroup' 与 'instreamid' 是必需属性。'language' 是可选属性。

  用此选项配置的隐藏式字幕组，通过在 `var_stream_map` 字符串中提供相同的 'ccgroup' 名称映射到不同变体流。

  例如：

  ``` text
  ffmpeg -re -i in.ts -b:v:0 1000k -b:v:1 256k -b:a:0 64k -b:a:1 32k \
    -a53cc:0 1 -a53cc:1 1 \
    -map 0:v -map 0:a -map 0:v -map 0:a -f hls \
    -cc_stream_map "ccgroup:cc,instreamid:CC1,language:en ccgroup:cc,instreamid:CC2,language:sp" \
    -var_stream_map "v:0,a:0,ccgroup:cc v:1,a:1,ccgroup:cc" \
    -master_pl_name master.m3u8 \
    http://example.com/live/out_%v.m3u8
  ```

  将在主播放列表中为 INSTREAM-ID 'CC1' 与 'CC2' 添加两个带 `TYPE=CLOSED-CAPTIONS` 的 `#EXT-X-MEDIA` 标签。此外，还会为两条输出变体流添加组名为 'cc' 的 `CLOSED-CAPTIONS` 属性。

  若未设置 `var_stream_map`，则 `cc_stream_map` 中第一个可用的 ccgroup 映射到输出变体流。

  例如：

  ``` text
  ffmpeg -re -i in.ts -b:v 1000k -b:a 64k -a53cc 1 -f hls \
    -cc_stream_map "ccgroup:cc,instreamid:CC1,language:en" \
    -master_pl_name master.m3u8 \
    http://example.com/live/out.m3u8
  ```

  这将在主播放列表中添加带 `TYPE=CLOSED-CAPTIONS` 的 `#EXT-X-MEDIA` 标签，组名为 'cc'、语言为 'en'（英语）、INSTREAM-ID 为 'CC1'。此外，还会为输出变体流添加组名为 'cc' 的 `CLOSED-CAPTIONS` 属性。

- **`master_pl_name name`** 用给定名称创建 HLS 主播放列表。

  例如：

  ``` text
  ffmpeg -re -i in.ts -f hls -master_pl_name master.m3u8 http://example.com/live/out.m3u8
  ```

  创建名为 `master.m3u8` 的 HLS 主播放列表，发布于 <http://example.com/live/>。

- **`master_pl_publish_rate count`** 每隔指定数量的分段间隔重复发布主播放列表。

  例如：

  ``` text
  ffmpeg -re -i in.ts -f hls -master_pl_name master.m3u8 \
  -hls_time 2 -master_pl_publish_rate 30 http://example.com/live/out.m3u8
  ```

  创建名为 `master.m3u8` 的 HLS 主播放列表，并每 30 个分段（即每 60 秒）重复发布。

- **`http_persistent bool`** 使用持久 HTTP 连接。仅适用于 HTTP 输出。

- **`timeout timeout`** 设置套接字 I/O 操作超时。仅适用于 HTTP 输出。

- **`ignore_io_errors bool`** 忽略打开、写入和删除期间的 I/O 错误。对网络输出的长时间运行有用。

- **`headers headers`** 设置自定义 HTTP 头，可覆盖内置默认头。仅适用于 HTTP 输出。

## iamf

沉浸式音频模型与格式 (Immersive Audio Model and Formats, IAMF) 复用器。

IAMF 用于为流式与离线应用中广泛设备上的呈现提供沉浸式音频内容。这些应用包括互联网音频流、组播/广播服务、文件下载、游戏、通信、虚拟与增强现实等。在这些应用中，音频可在多种设备上播放，如耳机、手机、平板电脑、电视、条形音箱、家庭影院系统和大屏幕。

此格式由 Alliance for Open Media 推动并设计。

关于此格式的更多信息，参见 <https://aomedia.org/iamf/>。

## ico

ICO 文件复用器。

Microsoft 的图标文件格式 (ICO) 有一些值得注意的严格限制：

- 任意维度不得超过 256 像素

- 只能存储 BMP 与 PNG 图像

- 若使用 BMP 图像，必须是以下像素格式之一：

  ``` text
  BMP Bit Depth      FFmpeg Pixel Format
  1bit               pal8
  4bit               pal8
  8bit               pal8
  16bit              rgb555le
  24bit              bgr24
  32bit              bgra
  ```

- 若使用 BMP 图像，必须使用 BITMAPINFOHEADER DIB 头

- 若使用 PNG 图像，必须使用 rgba 像素格式

## ilbc

Internet Low Bitrate Codec (iLBC) raw 复用器。

它接受单条 `ilbc` 音频流。

## image2, image2pipe

图像文件复用器。

`image2` 复用器将视频帧写入图像文件。

输出文件名由模式 (pattern) 指定，模式可用于生成按顺序编号的文件系列。模式可包含字符串 "%d" 或 "%0\<N\>d"，该字符串指定文件名中表示编号的字符的位置。若使用 "%0\<N\>d" 形式，每个文件名中表示编号的字符串以 0 填充到 \<N\> 位。模式中可用字符串 "%%" 指定字面字符 '%'。

若模式包含 "%d" 或 "%0\<N\>d"，指定文件列表的第一个文件名将包含编号 1，后续编号依次连续。

模式可包含一个后缀，用于自动确定要写入图像文件的格式。

例如，模式 "img-%03d.bmp" 将指定 `img-001.bmp`、`img-002.bmp`、……、`img-010.bmp` 等形式的文件名序列。模式 "img%%-%d.jpg" 将指定 `img%-1.jpg`、`img%-2.jpg`、……、`img%-10.jpg` 等形式的文件名序列。

图像复用器支持 .Y.U.V 图像文件格式。此格式比较特殊：每幅图像帧由三个文件组成，对应 YUV420P 的各个分量。读取或写入此图像文件格式时，指定 '.Y' 文件名。复用器会按需自动打开 '.U' 与 '.V' 文件。

`image2pipe` 复用器接受与 `image2` 复用器相同的选项，但忽略模式校验与展开，因为它写入的是命令输出而非实际存储的文件。

### 选项

- **`frame_pts bool`** 若设为 1，用包 PTS (presentation time stamp) 展开文件名。默认值为 0。

- **`start_number count`** 从指定编号开始序列。默认值为 1。

- **`update bool`** 若设为 1，文件名将始终只按文件名解释（而不是模式），相应文件会被新图像持续覆盖。默认值为 0。

- **`strftime bool`** 若设为 1，用 `strftime()` 的日期与时间信息展开文件名。默认值为 0。

- **`atomic_writing bool`** 将输出写入临时文件，写入完成后重命名为目标文件名。默认禁用。

- **`protocol_opts options_list`** 以 :-分隔的 key=value 参数列表设置协议选项。包含 `:` 特殊字符的值必须转义。

### 示例

- 使用 `ffmpeg` 创建文件序列 `img-001.jpeg`、`img-002.jpeg`、……，每秒从输入视频取一幅图像：

  ``` text
  ffmpeg -i in.avi -fps_mode cfr -r 1 -f image2 'img-%03d.jpeg'
  ```

  注意使用 `ffmpeg` 时，若未用 `-f` 选项指定格式且输出文件名指明图像文件格式，会自动选择 image2 复用器，因此上一命令可写为：

  ``` text
  ffmpeg -i in.avi -fps_mode cfr -r 1 'img-%03d.jpeg'
  ```

  另外注意模式不一定必须包含 "%d" 或 "%0\<N\>d"，例如从输入视频开头创建单个图像文件 `img.jpeg` 可使用命令：

  ``` text
  ffmpeg -i in.avi -f image2 -frames:v 1 img.jpeg
  ```

- `strftime` 选项允许用日期与时间信息展开文件名。语法参见 `strftime()` 函数的文档。

  要按 `strftime()` 的 "%Y-%m-%d\_%H-%M-%S" 模式生成图像文件，可用以下 `ffmpeg` 命令：

  ``` text
  ffmpeg -f v4l2 -r 1 -i /dev/video0 -f image2 -strftime 1 "%Y-%m-%d_%H-%M-%S.jpg"
  ```

- 用当前帧的 PTS 设置文件名：

  ``` text
  ffmpeg -f v4l2 -r 1 -i /dev/video0 -copyts -f image2 -frame_pts true %d.jpg
  ```

- 每秒将桌面内容直接发布到 WebDAV 服务器：

  ``` text
  ffmpeg -f x11grab -framerate 1 -i :0.0 -q:v 6 -update 1 -protocol_opts method=PUT http://example.com/desktop.jpg
  ```

## ircam

Berkeley / IRCAM / CARL Sound Filesystem (BICSF) 格式复用器。

Berkeley/IRCAM/CARL 声音格式诞生于 20 世纪 80 年代，是多个早期声音文件格式与系统合并的结果，包括 UC San Diego 计算机音频研究实验室 (CARL) 的 Gareth Loy 博士开发的 csound 系统、巴黎声学与音乐研究协调研究所 (Institut de Recherche et Coordination Acoustique / Musique) 的 Rob Gross 与 Dan Timis 开发的 IRCAM 声音文件系统，以及 Berkeley 快速文件系统。

它最初作为 Berkeley/IRCAM/CARL Sound Filesystem 的一部分开发，这是一套为运行于 Berkeley UNIX 下的音频应用实现文件系统的程序。它在学术音乐研究中心尤为流行，曾数次用于早期计算机生成作品的创作。

此复用器接受单条包含 PCM 数据的音频流。

## ivf

On2 IVF 复用器。

IVF 由 On2 Technologies（前称 Duck Corporation）开发，用于存储其内部开发的编解码器。

此复用器接受单条 `vp8`、`vp9` 或 `av1` 视频流。

## jacosub

JACOsub 字幕格式复用器。

此复用器接受单条 `jacosub` 字幕流。

关于该格式的更多信息，参见 <http://unicorn.us.com/jacosub/jscripts.html>。

## kvag

Simon & Schuster Interactive VAG 复用器。

此自定义 VAG 容器被一些 Simon & Schuster Interactive 游戏使用，如 "Real War" 与 "Real War: Rogue States"。

此复用器接受单条 `adpcm_ima_ssi` 音频流。

## lc3

Bluetooth SIG 低复杂度通信编解码器音频 (LC3)，或 ETSI TS 103 634 低复杂度通信编解码器增强版 (LC3plus)。

此复用器接受单条 `lc3` 音频流。

## lrc

LRC 歌词文件格式复用器。

LRC（LyRiCs 的缩写）是一种将歌曲歌词与音频文件（如 MP3、Vorbis 或 MIDI）同步的计算机文件格式。

此复用器接受单条 `subrip` 或 `text` 字幕流。

### 选项

- **`precision number`** 设置时间戳小数（亚秒）部分使用的十进制位数。范围为 `1` 到 `6`。默认值为 `2`，即百分之一秒。

### 元数据

以下元数据标签会转换为格式对应的元数据：

- **`title`**

- **`album`**

- **`artist`**

- **`author`**

- **`creator`**

- **`encoder`**

- **`encoder_version`**

若未显式设置 `encoder_version`，它会自动设为 libavformat 版本。

## matroska

Matroska 容器复用器。

此复用器实现 matroska 与 webm 容器规范。

### 元数据

此复用器识别的元数据设置如下：

- **`title`** 设置提供给单条轨道的标题名。对作为附件写入的流，它会映射到 FileDescription 元素。

- **`language`** 以 Matroska 语言形式指定轨道的语言。

  语言可以是 3 字母文献型 ISO-639-2 (ISO 639-2/B) 形式（如法语为 "fre"），也可以是混合国家代码以表示语言特例的语言代码（如加拿大法语为 "fre-ca"）。

- **`stereo_mode`** 设置单条视频轨道中两个视图的立体 3D 视频布局。

  可识别以下取值：

  - **`mono`** 视频不是立体声

  - **`left_right`** 两个视图并排排列，左眼视图在左

  - **`bottom_top`** 两个视图上下排列，左眼视图在下

  - **`top_bottom`** 两个视图上下排列，左眼视图在上

  - **`checkerboard_rl`** 每个视图以棋盘交织模式排列，左眼视图在前

  - **`checkerboard_lr`** 每个视图以棋盘交织模式排列，右眼视图在前

  - **`row_interleaved_rl`** 每个视图由基于行的交织构成，右眼视图为第一行

  - **`row_interleaved_lr`** 每个视图由基于行的交织构成，左眼视图为第一行

  - **`col_interleaved_rl`** 两个视图按基于列的交织方式排列，右眼视图为第一列

  - **`col_interleaved_lr`** 两个视图按基于列的交织方式排列，左眼视图为第一列

  - **`anaglyph_cyan_red`** 全部帧为红青滤光镜可观看的双色立体 (anaglyph) 格式

  - **`right_left`** 两个视图并排排列，右眼视图在左

  - **`anaglyph_green_magenta`** 全部帧为绿品红滤光镜可观看的双色立体 (anaglyph) 格式

  - **`block_lr`** 双眼编入同一 Block，左眼视图在前

  - **`block_rl`** 双眼编入同一 Block，右眼视图在前

例如，可用以下命令行创建 3D WebM 片段：

``` text
ffmpeg -i sample_left_right_clip.mpg -an -c:v libvpx -metadata stereo_mode=left_right -y stereo_clip.webm
```

### 选项

- **`reserve_index_space size`** 默认情况下，此复用器把用于定位的索引（Matroska 术语称 cues）写在文件末尾，因为它无法预先知道应在文件开头为索引留多少空间。但对某些使用场景——例如定位可行但缓慢的流式传输——把索引放在文件开头是有用的。

  若此选项设为非零值，复用器将在文件头中预留 \<size\> 字节空间，并在复用完成后尝试将 cues 写在那里。若预留空间不足，则不写 cues，文件完成定稿，写尾部时返回错误。对大多数场景，每小时视频约 50kB 是安全的大小。

  注意只有输出可定位时才写 cues；不可定位时此选项无效。

- **`cues_to_front bool`** 若设置，复用器会通过必要时平移主数据将索引写在文件开头。这可与 reserve_index_space 结合使用，此时只在最初预留的空间不足时才平移数据。

  输出不可定位时忽略此选项。

- **`cluster_size_limit size`** 每个 cluster 至多存储指定的字节数。

  未指定时，限制自动设为合理的硬编码固定值。

- **`cluster_time_limit duration`** 每个 cluster 至多存储指定的毫秒数。

  未指定时，限制自动设为合理的硬编码固定值。

- **`dash bool`** 创建符合 WebM DASH 规范的 WebM 文件。默认设为 `false`。

- **`dash_track_number index`** DASH 流的轨道编号。默认设为 `1`。

- **`live bool`** 以直播流假设写入文件。默认设为 `false`。

- **`allow_raw_vfw bool`** 允许 raw VFW 模式。默认设为 `false`。

- **`flipped_raw_rgb bool`** 若设为 `true`，为 raw RGB 位图存储正的高度值，表示位图自底向上存储。注意此选项不会翻转位图，翻转须事先手动完成，例如使用 `vflip` 滤镜。默认值为 `false`，表示位图自顶向下存储。

- **`write_crc32 bool`** 在每个 Level 1 元素内写入 CRC32 元素。默认设为 `true`。对 WebM 忽略此选项。

- **`default_mode mode`** 控制输出轨道的 FlagDefault 如何设置。它影响播放器默认应播放哪些轨道。默认模式为 `passthrough`。

  - **`infer`** 每条带 default disposition 的轨道都会设置 FlagDefault。此外，对每类轨道（音频、视频或字幕），若该类不存在带 default disposition 的轨道，则该类的第一条轨道会被标记为默认（如存在）。这确保即使输入来自缺少默认轨道概念的容器，默认标志也以合理方式设置。

  - **`infer_no_subs`** 此模式与 infer 相同，区别是若不存在带 default disposition 的字幕轨道，则不将任何字幕轨道标记为默认。

  - **`passthrough`** 此模式下，当且仅当相应流的 disposition 中设置了 AV_DISPOSITION_DEFAULT 标志时才设置 FlagDefault。

## md5

MD5 测试格式。

这是 [hash](#hash) 复用器的变体。与该复用器不同，它默认使用 MD5 哈希函数。

另请参见 [hash](#hash) 与 [framemd5](#framemd5) 复用器。

### 示例

- 计算转换为 raw 音频与视频的输入的 MD5 哈希，并存储到文件 `out.md5`：

  ``` text
  ffmpeg -i INPUT -f md5 out.md5
  ```

- 将 MD5 哈希打印到标准输出：

  ``` text
  ffmpeg -i INPUT -f md5 -
  ```

## mcc

MacCaption MCC 文件复用器，支持 MCC 版本 1.0 和 2.0。MCC 文件存储 VANC 数据，其中可包含隐藏式字幕（EIA-608 和 CEA-708）、辅助时间码、摇移 (pan-scan) 数据等。

### 选项

复用器选项如下：

- **`override_time_code_rate`** 覆盖输出中的 `Time Code Rate` 值。默认尝试从流的 `time_base` 推断，但通常推断不出来。

- **`use_u_alias`** 对字节序列 `E1h 00h 00h 00h` 使用 `U` 别名。默认禁用，因为部分 `.mcc` 文件对它是 2 个还是 3 个零字节存在分歧。

- **`mcc_version`** MCC 文件格式版本。必须是 1 或 2，默认为 2。

- **`creation_program`** 创建程序。默认为本版本的 FFmpeg。

- **`creation_time`** 创建时间。默认为当前时间。

### 示例

- 从 MXF 文件提取 MXF `SMPTE_436M_ANC` 流并写入 30 fps 的 MCC 文件。

  ``` text
  ffmpeg -i input.mxf -c copy -map 0:d -override_time_code_rate 30 out.mcc
  ```

- 从 `.mp4` 文件提取 EIA-608/CTA-708 隐藏式字幕并写入 29.97 fps 的 MCC 文件。

  ``` text
  ffmpeg -f lavfi -i "movie=input.mp4[out+subcc]" -c:s copy -map 0:s -override_time_code_rate 30000/1001 out.mcc
  ```

## microdvd

MicroDVD 字幕格式复用器。

此复用器接受单条 `microdvd` 字幕流。

## mmf

合成音乐移动应用格式 (Synthetic music Mobile Application Format, SMAF) 复用器。

SMAF 是 Yamaha 为手机和个人数字助理等便携电子设备指定的音乐数据格式。

此复用器接受单条 `adpcm_yamaha` 音频流。

## mp3

MP3 复用器写入带以下可选特性的 raw MP3 流：

- 开头的 ID3v2 元数据头（默认启用）。支持版本 2.3 与 2.4，私有选项 `id3v2_version` 控制使用哪一个（3 或 4）。将 `id3v2_version` 设为 0 可完全禁用 ID3v2 头。

  复用器支持向 ID3v2 头写入附图 (APIC 帧)。图片以含单个包的视频流形式提供给复用器。可以有任意多条这样的流，每条对应一个 APIC 帧。流元数据标签 \<title\> 与 \<comment\> 分别映射到 APIC 的 \<description\> 与 \<picture type\>。允许的图片类型参见 <http://id3.org/id3v2.4.0-frames>。

  注意 APIC 帧必须写在开头，因此复用器会缓冲音频帧直到收到全部图片。因此建议尽早提供图片，避免过度缓冲。

- ID3v2 头（如果存在）之后的 Xing/LAME 帧。默认启用，但只在输出可定位时写入。私有选项 `write_xing` 可禁用它。该帧包含对解码器可能有用的各种信息，如音频时长或编码器延迟。

- 文件末尾的旧式 ID3v1 标签（默认禁用）。可用私有选项 `write_id3v1` 启用，但其能力非常有限，不建议使用。

示例：

写入带 ID3v2.3 头与 ID3v1 尾的 mp3：

``` text
ffmpeg -i INPUT -id3v2_version 3 -write_id3v1 1 out.mp3
```

用 `map` 同时选择音频流与图片流，将图片附加到 mp3 文件：

``` text
ffmpeg -i input.mp3 -i cover.png -c copy -map 0 -map 1
-metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" out.mp3
```

写入不带任何额外特性的"干净"MP3：

``` text
ffmpeg -i input.wav -write_xing 0 -id3v2_version 0 out.mp3
```

## mpegts

MPEG 传输流复用器。

此复用器实现 ISO 13818-1 与 ETSI EN 300 468 的部分内容。

mpegts 复用器识别的元数据设置为 `service_provider` 与 `service_name`。未设置时，`service_provider` 默认为 `FFmpeg`，`service_name` 默认为 `Service01`。

### 选项

复用器选项如下：

- **`mpegts_transport_stream_id integer`** 设置 `transport_stream_id`。它在 DVB 中标识一个转发器 (transponder)。默认为 `0x0001`。

- **`mpegts_original_network_id integer`** 设置 `original_network_id`。它是 DVB 中网络的唯一标识符，主要用于通过路径 `Original_Network_ID, Transport_Stream_ID` 唯一标识一个服务。默认为 `0xff01`。

- **`mpegts_service_id integer`** 设置 `service_id`，在 DVB 中也称节目 (program)。默认为 `0x0001`。

- **`mpegts_service_type integer`** 设置节目 `service_type`。默认为 `digital_tv`。接受以下选项：

  - **`hex_value`** `0x01` 到 `0xff` 之间的任意十六进制值，按 ETSI 300 468 定义。

  - **`digital_tv`** 数字电视服务。

  - **`digital_radio`** 数字广播服务。

  - **`teletext`** 图文电视服务。

  - **`advanced_codec_digital_radio`** 高级编解码器数字广播服务。

  - **`mpeg2_digital_hdtv`** MPEG2 数字 HDTV 服务。

  - **`advanced_codec_digital_sdtv`** 高级编解码器数字 SDTV 服务。

  - **`advanced_codec_digital_hdtv`** 高级编解码器数字 HDTV 服务。

  - **`hevc_digital_hdtv`** HEVC 数字电视服务。

- **`mpegts_pmt_start_pid integer`** 设置 PMT 的首个 PID。默认为 `0x1000`，最小为 `0x0020`，最大为 `0x1ffa`。在 m2ts 模式下此选项无效，PMT PID 固定为 `0x0100`。

- **`mpegts_start_pid integer`** 设置基本流的首个 PID。默认为 `0x0100`，最小为 `0x0020`，最大为 `0x1ffa`。在 m2ts 模式下此选项无效，基本流 PID 固定。

- **`mpegts_m2ts_mode boolean`** 设为 `1` 时启用 m2ts 模式。默认值为 `-1`，即禁用 m2ts 模式。

- **`muxrate integer`** 设置恒定复用率。默认为 VBR。

- **`pes_payload_size integer`** 设置最小 PES 包载荷（字节）。默认值为 `2930`。

- **`mpegts_flags flags`** 设置 mpegts 标志。接受以下选项：

  | Term | Description |
  |----|----|
  | `resend_headers` | 写下一个包之前重发 PAT/PMT。 |
  | `latm` | 对 AAC 使用 LATM 封包。 |
  | `pat_pmt_at_frames` | 在每个视频帧重发 PAT 与 PMT。 |
  | `system_b` | 遵循 System B (DVB) 而不是 System A (ATSC)。 |
  | `initial_discontinuity` | 将每条流的初始包标记为不连续。 |
  | `nit` | 输出 NIT 表。 |
  | `omit_rai` | 禁用随机访问指示符 (random access indicator) 的写入。 |

- **`mpegts_copyts boolean`** 值设为 `1` 时保留原始时间戳。默认值为 `-1`，即平移时间戳使其从 0 开始。

- **`omit_video_pes_length boolean`** 省略视频包的 PES 包长度。默认值为 `1`（true）。

- **`pcr_period integer`** 覆盖默认的 PCR 重传时间（毫秒）。默认为 `-1`，表示 PCR 间隔自动确定：CBR 流使用 20 ms，VBR 流使用小于 100 ms 的帧时长最大整数倍。

- **`pat_period duration`** PAT/PMT 表之间的最大间隔时间（秒）。默认值为 `0.1`。

- **`sdt_period duration`** SDT 表之间的最大间隔时间（秒）。默认值为 `0.5`。

- **`nit_period duration`** NIT 表之间的最大间隔时间（秒）。默认值为 `0.5`。

- **`tables_version integer`** 设置 PAT、PMT、SDT 与 NIT 版本（默认 `0`，有效值为 0 到 31，含边界）。此选项允许更新流结构，使标准消费端能检测到变化。为此需重新打开输出 `AVFormatContext`（API 用法）或重启 `ffmpeg` 实例，循环变更 `tables_version` 值：

  ``` text
  ffmpeg -i source1.ts -codec copy -f mpegts -tables_version 0 udp://1.1.1.1:1111
  ffmpeg -i source2.ts -codec copy -f mpegts -tables_version 1 udp://1.1.1.1:1111
  ...
  ffmpeg -i source3.ts -codec copy -f mpegts -tables_version 31 udp://1.1.1.1:1111
  ffmpeg -i source1.ts -codec copy -f mpegts -tables_version 0 udp://1.1.1.1:1111
  ffmpeg -i source2.ts -codec copy -f mpegts -tables_version 1 udp://1.1.1.1:1111
  ...
  ```

### 示例

``` text
ffmpeg -i file.mpg -c copy \
     -mpegts_original_network_id 0x1122 \
     -mpegts_transport_stream_id 0x3344 \
     -mpegts_service_id 0x5566 \
     -mpegts_pmt_start_pid 0x1500 \
     -mpegts_start_pid 0x150 \
     -metadata service_provider="Some provider" \
     -metadata service_name="Some Channel" \
     out.ts
```

## mxf, mxf_d10, mxf_opatom

MXF 复用器。

### 选项

复用器选项如下：

- **`store_user_comments bool`** 设置是否存储用户注释（如有）。IRT D-10 不允许用户注释，因此默认为 mxf 与 mxf_opatom 写注释，mxf_d10 不写

## null

Null 复用器。

此复用器不生成任何输出文件，主要用于测试或基准测试。

例如，用 `ffmpeg` 做解码基准测试可使用命令：

``` text
ffmpeg -benchmark -i INPUT -f null out.null
```

注意上述命令不读写 `out.null` 文件，但 `ffmpeg` 语法要求指定输出文件。

也可以将命令写为：

``` text
ffmpeg -benchmark -i INPUT -f null -
```

## nut

- **`-syncpoints flags`** 更改 nut 中同步点 (syncpoint) 的使用方式：

  - **`default use the normal low-overhead seeking aids.`**

  - **`none do not use the syncpoints at all, reducing the overhead but making the stream non-seekable;`** 不建议使用此选项，因为生成的文件对损坏非常敏感且无法定位。此外一般来说同步点的开销可忽略。注意，-`write_index` 0 可用于禁用所有增长型数据表，从而在有限内存下复用无限流且没有这些缺点。

  - **`timestamped extend the syncpoint with a wallclock field.`**

  \<none\> 与 \<timestamped\> 标志是实验性的。

- **`-write_index bool`** 在末尾写索引，默认写索引。

``` text
ffmpeg -i INPUT -f_strict experimental -syncpoints none - | processor
```

## ogg

Ogg 容器复用器。

- **`-page_duration duration`** 首选页时长（微秒）。复用器会尝试创建约 \<duration\> 微秒长的页。这让用户在定位粒度与容器开销之间权衡。默认为 1 秒。值 0 会填满所有分段，使页尽可能大。值 1 在多数情况下相当于每页一个包，以额外容器开销换取较小的定位粒度。

- **`-serial_offset value`** 用于设置流序列号的起始序列值。设为不同且足够大的值可确保生成的 ogg 文件可安全串联。

## pdv

Playdate 视频复用器。

此复用器写入 Panic 的 Playdate SDK 使用的 Playdate 视频容器。它要求输出可定位，以及单条 PDV 视频流。

- **`max_frames frames`** 在文件头中为至多 \<frames\> 个视频帧预留空间。此选项是必需的。

## rcwt

RCWT (Raw Captions With Time) 是 ccextractor 原生的格式，ccextractor 是处理 608/708 隐藏式字幕 (CC) 源的常用开源工具。它可用于存档提取的原始 CC 比特流，并生成供后续处理或转换的源文件。该格式支持 ccextractor 与 FFmpeg 之间的互操作，解析简单，可用于创建 CC 呈现的备份。

此复用器实现 2024 年 3 月版的规范，该规范自 2014 年 4 月以来保持稳定未变。

此复用器与 ccextractor 复用 RCWT 的方式存在一些细微差异。迄今未观察到处理输出与 ccextractor 的兼容性问题，但情况可能各异，输出不会逐位完全一致。

RCWT 的自由规范见：<https://github.com/CCExtractor/ccextractor/blob/master/docs/BINARY_FILE_FORMAT.TXT>

### 示例

- 使用 lavfi 提取隐藏式字幕到 RCWT：

  ``` text
  ffmpeg -f lavfi -i "movie=INPUT.mkv[out+subcc]" -map 0:s:0 -c:s copy -f rcwt CC.rcwt.bin
  ```

## segment, stream_segment, ssegment

基础流分段器 (stream segmenter)。

此复用器将流输出到若干时长接近固定的独立文件。输出文件名模式可按类似 [image2](#image2) 的方式设置，或在启用 `strftime` 选项时使用 `strftime` 模板。

`stream_segment` 是该复用器的变体，用于写入不需要全局头的流式输出格式，推荐用于输出到 MPEG 传输流分段等。`ssegment` 是 `stream_segment` 的简写别名。

每个分段从所选参考流的一个关键帧开始，参考流通过 `reference_stream` 选项设置。

注意，若想对视频文件进行精确切分，需要让输入关键帧对应分段器预期的精确切分时间，否则分段复用器会从指定起始时间之后找到的下一个关键帧开始新分段。

分段复用器与单一恒定帧率视频配合效果最佳。

可选地，它可以通过设置选项 \<segment_list\> 生成已创建分段的列表。列表类型由 \<segment_list_type\> 选项指定。分段列表中的条目文件名默认为相应分段文件的基本名。

另请参见 [hls](#hls) 复用器，它提供了针对 HLS 分段的更具体实现。

### 选项

分段复用器支持以下选项：

- **`increment_tc 1|0`** 若设为 `1`，在每个分段之间递增时间码。选择此项时，输入的第一条视频流需要有时间码。默认值为 `0`。

- **`reference_stream specifier`** 设置参考流，由字符串 \<specifier\> 指定。\<specifier\> 设为 `auto` 时自动选择参考。否则它必须是流说明符（参见 ffmpeg 手册的"Stream specifiers"一章），用以指定参考流。默认值为 `auto`。

- **`segment_format format`** 覆盖内部容器格式，默认由文件名扩展名猜出。

- **`segment_format_options options_list`** 使用以 :-分隔的 key=value 参数列表设置输出格式选项。包含 `:` 特殊字符的值必须转义。

- **`segment_list name`** 同时生成名为 \<name\> 的列表文件。未指定时不生成列表文件。

- **`segment_list_flags flags`** 设置影响分段列表生成的标志。

  目前支持以下标志：

  | Term      | Description                                   |
  |-----------|-----------------------------------------------|
  | `cache` | 允许缓存（只影响 M3U8 列表文件）。 |
  | `live`  | 允许生成对直播友好的文件。          |

- **`segment_list_size size`** 更新列表文件使其至多包含 \<size\> 个分段。若为 0，列表文件将包含全部分段。默认值为 0。

- **`segment_list_entry_prefix prefix`** 为每个条目前加 \<prefix\>。用于生成绝对路径。默认不加前缀。

- **`segment_list_type type`** 选择列表格式。

  可识别以下取值：

  - **`flat`** 为已创建分段生成平面列表，每行一个分段。

  - **`csv, ext`** 为已创建分段生成列表，每行一个分段，每行匹配以下格式（逗号分隔值）：

    ``` text
    segment_filename,segment_start_time,segment_end_time
    ```

    \<segment_filename\> 是复用器按给定模式生成的输出文件名。必要时应用 CSV 转义（按 RFC4180）。

    \<segment_start_time\> 与 \<segment_end_time\> 指定分段的开始与结束时间（秒）。

    后缀为 `".csv"` 或 `".ext"` 的列表文件会自动选择此格式。

    `ext` 已弃用，建议改用 `csv`。

  - **`ffconcat`** 为已创建分段生成 ffconcat 文件。结果文件可用 FFmpeg [concat](#concat) 解复用器读取。

    后缀为 `".ffcat"` 或 `".ffconcat"` 的列表文件会自动选择此格式。

  - **`m3u8`** 生成扩展 M3U8 文件（版本 3），符合 <http://tools.ietf.org/id/draft-pantos-http-live-streaming>。

    后缀为 `".m3u8"` 的列表文件会自动选择此格式。

  未指定时，类型由列表文件名后缀猜出。

- **`segment_time time`** 将分段时长设为 \<time\>，值必须是时长描述。默认值为 "2"。另请参见 `segment_times` 选项。

  注意切分可能不精确，除非你在给定时间强制参考流关键帧。参见开头说明与下文示例。

- **`min_seg_duration time`** 将最小分段时长设为 \<time\>，值必须是时长描述。它防止复用器在低于该值的时长处结束分段。仅与 `segment_time` 配合有效。默认值为 "0"。

- **`segment_atclocktime 1|0`** 若设为 "1"，按从 00:00 起的常规时钟时间间隔切分。`segment_time` 中指定的 \<time\> 值用于设置切分间隔的长度。

  例如，`segment_time` 设为 "900" 时，可以在 12:00、12:15、12:30 等时刻创建文件。

  默认值为 "0"。

- **`segment_clocktime_offset duration`** 使用 `segment_atclocktime` 时，用指定时长延迟分段切分时刻。

  例如，`segment_time` 设为 "900"、`segment_clocktime_offset` 设为 "300" 时，可以在 12:05、12:20、12:35 等时刻创建文件。

  默认值为 "0"。

- **`segment_clocktime_wrap_duration duration`** 强制分段器只在分段时钟时间之后的指定时长内有包到达复用器时才开始新分段。这样可让分段器对本地时间回拨（如闰秒或从夏令时切换回标准时间）更有韧性。

  默认为最大可能时长，即无论距上一个时钟时间过了多久都开始新分段。

- **`segment_time_delta delta`** 指定选择分段起始时间时的容差时间，以时长描述表示。默认值为 "0"。

  指定 delta 后，若关键帧的 PTS 满足以下关系，则会开始新分段：

  ``` text
  PTS >= start_time - time_delta
  ```

  此选项在切分视频内容（总是在 GOP 边界切分）时有用，以防在指定切分时间之前刚好有关键帧。

  特别地，可与 `ffmpeg` 选项 \<force_key_frames\> 组合使用。\<force_key_frames\> 指定的关键帧时间可能因舍入问题无法精确设置，导致关键帧时间恰好设在指定时间之前。对恒定帧率视频，值 1/(2\*\<frame_rate\>) 应能解决指定时间与 \<force_key_frames\> 所设时间的最坏失配。

- **`segment_times times`** 指定切分点列表。\<times\> 包含以逗号分隔、按升序排列的时长描述列表。另请参见 `segment_time` 选项。

- **`segment_frames frames`** 指定切分视频帧编号列表。\<frames\> 包含以逗号分隔、按升序排列的整数列表。

  此选项指定：每当发现参考流关键帧且帧的顺序编号（从 0 起）大于或等于列表中下一个值时，开始新分段。

- **`segment_wrap limit`** 分段索引达到 \<limit\> 后循环回绕。

- **`segment_start_number number`** 设置第一个分段的序号。默认为 `0`。

- **`strftime 1|0`** 使用 `strftime` 函数定义要写入的新分段名。选择此项时，输出分段名必须包含 `strftime` 函数模板。默认值为 `0`。

- **`break_non_keyframes 1|0`** 若启用，允许分段在非关键帧处开始。这改善了关键帧间隔不一致时某些播放器的行为，但可能使另一些播放器变差，并可能在定位时引起一些怪异现象。默认为 `0`。

- **`reset_timestamps 1|0`** 在每个分段开头重置时间戳，使每个分段以接近零的时间戳开始。旨在方便播放生成的分段。可能与某些复用器/编解码器组合不兼容。默认设为 `0`。

- **`initial_offset offset`** 指定应用于输出包时间戳的时间戳偏移。参数必须是时长描述，默认为 0。

- **`write_empty_segments 1|0`** 若启用，当分段通常跨越的期间内没有任何包时写一个空分段。否则分段将由下一个写入的包填充。默认为 `0`。

编码时务必要求封闭 GOP (closed GOP)，并将 GOP 大小设为符合分段时长约束。

### 示例

- 将文件 `in.mkv` 的内容重新封装为分段列表 `out-000.nut`、`out-001.nut` 等，并将生成的分段列表写入 `out.list`：

  ``` text
  ffmpeg -i in.mkv -codec hevc -flags +cgop -g 60 -map 0 -f segment -segment_list out.list out%03d.nut
  ```

- 对输入分段并为输出分段设置输出格式选项：

  ``` text
  ffmpeg -i in.mkv -f segment -segment_time 10 -segment_format_options movflags=+faststart out%03d.mp4
  ```

- 按 \<segment_times\> 选项指定的切分点对输入文件分段：

  ``` text
  ffmpeg -i in.mkv -codec copy -map 0 -f segment -segment_list out.csv -segment_times 1,2,3,5,8,13,21 out%03d.nut
  ```

- 使用 `ffmpeg` 的 `force_key_frames` 选项在输入的指定位置强制关键帧，并配合分段选项 `segment_time_delta` 来考虑设置关键帧时间时可能进行的舍入。

  ``` text
  ffmpeg -i in.mkv -force_key_frames 1,2,3,5,8,13,21 -codec:v mpeg4 -codec:a pcm_s16le -map 0 \
  -f segment -segment_list out.csv -segment_times 1,2,3,5,8,13,21 -segment_time_delta 0.05 out%03d.nut
  ```

  为了在输入文件上强制关键帧，需要转码。

- 按 `segment_frames` 选项指定的帧编号序列切分输入文件：

  ``` text
  ffmpeg -i in.mkv -codec copy -map 0 -f segment -segment_list out.csv -segment_frames 100,200,300,500,800 out%03d.nut
  ```

- 使用 `libx264` 与 `aac` 编码器将 `in.mkv` 转换为 TS 分段：

  ``` text
  ffmpeg -i in.mkv -map 0 -codec:v libx264 -codec:a aac -f ssegment -segment_list out.list out%03d.ts
  ```

- 对输入文件分段并创建 M3U8 直播播放列表（可用作直播 HLS 源）：

  ``` text
  ffmpeg -re -i in.mkv -codec copy -map 0 -f segment -segment_list playlist.m3u8 \
  -segment_list_flags +live -segment_time 10 out%03d.mkv
  ```

## smoothstreaming

Smooth Streaming 复用器生成一组适合用常规 web 服务器提供的文件（清单、chunk）。

- **`window_size`** 指定清单中保留的分片数。默认 0（全部保留）。

- **`extra_window_size`** 指定从磁盘移除前保留在清单之外的分片数。默认 5。

- **`lookahead_count`** 指定前瞻 (lookahead) 分片数。默认 2。

- **`min_frag_duration`** 指定最小分片时长（微秒）。默认 5000000。

- **`remove_at_exit`** 指定完成时是否移除全部分片。默认 0（不移除）。

## streamhash

逐流哈希 (hash) 测试格式。

此复用器按流计算并打印全部输入帧的加密哈希。可用于相等性检查，无需做完整的二进制比较。

默认情况下，计算哈希前音频帧被转换为有符号 16 位 raw 音频，视频帧被转换为 raw 视频，但也可使用显式转换为其他编解码器后的输出。时间戳被忽略。默认使用 SHA-256 加密哈希函数，但也支持若干其他算法。

复用器的输出为每条流一行，形如 \<streamindex\>,\<streamtype\>,\<algo\>=\<hash\>，其中 \<streamindex\> 是被映射流的索引，\<streamtype\> 是表示流类型的单个字符，\<algo\> 是表示所用哈希函数的短字符串，\<hash\> 是表示计算所得哈希的十六进制数。

- **`hash algorithm`** 使用字符串 \<algorithm\> 指定的加密哈希函数。支持的值包括 `MD5`、`murmur3`、`RIPEMD128`、`RIPEMD160`、`RIPEMD256`、`RIPEMD320`、`SHA160`、`SHA224`、`SHA256`（默认）、`SHA512/224`、`SHA512/256`、`SHA384`、`SHA512`、`CRC32` 与 `adler32`。

### 示例

计算转换为 raw 音频与视频的输入的 SHA-256 哈希，并存储到文件 `out.sha256`：

``` text
ffmpeg -i INPUT -f streamhash out.sha256
```

将 MD5 哈希打印到标准输出，使用命令：

``` text
ffmpeg -i INPUT -f streamhash -hash md5 -
```

另请参见 [hash](#hash) 与 [framehash](#framehash) 复用器。

## tee

tee 复用器可用于将相同数据写到多个输出，如文件或流。例如可用于在网络上传输视频的同时保存到磁盘。

它与向 `ffmpeg` 命令行工具指定多个输出不同。使用 tee 复用器时，音频与视频数据只编码一次。使用常规多输出时，会启动多个并行编码操作，代价可能很高。直接使用 libavformat API 时 tee 复用器没有用处，因为那时可以直接把相同的包馈送给多个复用器。

由于 tee 复用器不代表任何特定输出格式，ffmpeg 无法自动选择输出流。因此所有要输出的流都必须用 `-map` 指定。参见下文示例。

某些编码器可能因输出格式不同而需要不同选项；tee 复用器无法自动检测这一点，因此需要显式指定。主要例子是 `global_header` 标志。

从属输出 (slave output) 在给复用器的文件名中指定，以 '\|' 分隔。若任何从属名称包含 '\|' 分隔符、前导或尾随空格或任何特殊字符，必须转义（参见 `ffmpeg-utils` 中"the "Quoting and escaping" section in the ffmpeg-utils(1) manual"（引号与转义）一节）。

### 选项

- **`use_fifo bool`** 若设为 1，从属输出将用 [fifo](#fifo) 复用器在独立线程中处理。这可以补偿不同输出的速度/延迟/可靠性差异，并设置透明恢复。默认关闭此功能。

- **`fifo_options`** 传给 fifo 伪复用器实例的选项。参见 [fifo](#fifo)。

可为每个从属指定复用器选项，方法是在方括号内前缀一组以 ':' 分隔的 \<key\>=\<value\> 对。若选项值包含特殊字符或 ':' 分隔符，必须转义；注意这是第二层转义。

还识别以下特殊选项：

- **`f`** 指定格式名。无法从输出 URL 猜出时必需。

- **`bsfs[/spec]`** 指定应用于指定输出的比特流滤镜列表。

  可以通过在选项后附加以 `/` 分隔的流说明符，指定给定的比特流滤镜应用于哪些流。\<spec\> 必须是流说明符（参见 [格式流说明符](#Format-stream-specifiers)）。

  未指定流说明符时，比特流滤镜将应用于输出中的所有流。若输出包含无法应用该比特流滤镜的流（例如对包含音频流的输出应用 `h264_mp4toannexb`），该输出操作将失败。

  比特流滤镜的选项必须以 `opt=value` 形式指定。

  可指定多个比特流滤镜，以 "," 分隔。

- **`use_fifo bool`** 允许为单个从属复用器覆盖 tee 复用器的 use_fifo 选项。

- **`fifo_options`** 允许为单个从属复用器覆盖 tee 复用器的 fifo_options。参见 [fifo](#fifo)。

- **`select`** 选择应映射到从属输出的流，由流说明符指定。未指定时默认为全部已映射流。若输出格式不接受全部已映射流，该输出操作将失败。

  可以使用以逗号 (`,`) 分隔的多个流说明符，例如：`a:0,v`

- **`onfail`** 指定输出失败时的行为。可设为 `abort`（默认）或 `ignore`。`abort` 会使整个进程在此从属输出失败时失败。`ignore` 会忽略此输出的失败，其他输出继续不受影响。

### 示例

- 编码内容并同时存档为 WebM 文件、以 MPEG-TS 经 UDP 推流：

  ``` text
  ffmpeg -i ... -c:v libx264 -c:a mp2 -f tee -map 0:v -map 0:a
    "archive-20121107.mkv|[f=mpegts]udp://10.0.1.255:1234/"
  ```

- 同上，但即使输出到本地文件失败（例如本地磁盘写满）也继续推流：

  ``` text
  ffmpeg -i ... -c:v libx264 -c:a mp2 -f tee -map 0:v -map 0:a
    "[onfail=ignore]archive-20121107.mkv|[f=mpegts]udp://10.0.1.255:1234/"
  ```

- 使用 `ffmpeg` 编码输入，并将输出发送到三个不同目标。`dump_extra` 比特流滤镜用于向全部输出视频关键帧包添加 extradata 信息（MPEG-TS 格式要求）。select 选项应用于 `out.aac`，使其只包含音频包。

  ``` text
  ffmpeg -i ... -map 0 -flags +global_header -c:v libx264 -c:a aac
         -f tee "[bsfs/v=dump_extra=freq=keyframe]out.ts|[movflags=+faststart]out.mp4|[select=a]out.aac"
  ```

- 同上，但音频输出只选择流 `a:1`。注意必须进行第二层转义，因为 ":" 是用于分隔选项的特殊字符。

  ``` text
  ffmpeg -i ... -map 0 -flags +global_header -c:v libx264 -c:a aac
         -f tee "[bsfs/v=dump_extra=freq=keyframe]out.ts|[movflags=+faststart]out.mp4|[select=\'a:1\']out.aac"
  ```

## wav

RIFF Wave 音频复用器。

### 选项

- **`rf64 mode`** 选择是否用 RF64 文件格式代替 RIFF。RF64 允许大于 4 GB 的文件，但 RF64 支持不如 RIFF 普遍。

  可识别以下模式：

  - **`auto`** 先写标准 RIFF 文件以保持与非 RF64 感知软件的兼容性，但若输出文件超过 4 GB 则切换到 RF64。会用 `JUNK` chunk 在头中预留少量额外空间，所有合规的 RIFF 读取器都应忽略它，但一些极其简化的 WAV 读取器可能因此混淆。

  - **`always`** 无论文件大小都使用 RF64 格式。输出文件只能被 RF64 兼容软件读取，不再是标准 RIFF WAVE 文件。

  - **`never`** 总是使用普通 RIFF，绝不使用 RF64。此模式对旧软件兼容性最好，但若输出文件超过 4 GB，`data` chunk 中的 32 位大小字段将无法正确表示大小，多数音频软件将无法读取部分或全部数据。（[wav](#wav) 解复用器的 `ignore_length` 选项可用于恢复此类文件。）这是默认模式。

- **`write_bext bool`** 启用后添加包含扩展音频元数据的 Broadcast Wave Format `BEXT` chunk。默认为 false。

- **`write_peak mode`** 启用后添加峰值包络 chunk (Peak Envelope chunk, EBU Tech 3285 Supplement 3)。默认关闭。

  - **`off`** 不添加峰值包络 chunk。

  - **`on`** 添加峰值包络 chunk，基于 `peak_block_size`、`peak_format` 与 `peak_ppv` 选项计算峰值。

  - **`only`** 类似 `on`，但跳过实际音频数据写入（文件不写 `data` chunk；只写峰值包络与其他元数据 chunk）。

- **`peak_block_size int`** 用于生成每个峰值帧的音频采样数，最大 65536。默认为 256。

- **`peak_format format`** 峰值包络数据的格式（1: uint8，2: uint16）。默认为 2 (uint16)。

- **`peak_ppv int`** 每个峰值值的峰值点数（1 或 2）。默认为 2。

## webm_chunk

WebM 直播分块 (Live Chunk) 复用器。

此复用器将 WebM 头与 chunk 写为独立文件，供支持经 DASH 的 WebM 直播流的客户端使用。

### 选项

此复用器支持以下选项：

| Term | Description |
|----|----|
| `chunk_start_index` | 第一个 chunk 的索引（默认为 0）。 |
| `header` | 写入初始化数据的头的文件名。 |
| `audio_chunk_duration` | 每个音频 chunk 的时长（毫秒）（默认为 5000）。 |

### 示例

``` text
ffmpeg -f v4l2 -i /dev/video0 \
       -f alsa -i hw:0 \
       -map 0:0 \
       -c:v libvpx-vp9 \
       -s 640x360 -keyint_min 30 -g 30 \
       -f webm_chunk \
       -header webm_live_video_360.hdr \
       -chunk_start_index 1 \
       webm_live_video_360_%d.chk \
       -map 1:0 \
       -c:a libvorbis \
       -b:a 128k \
       -f webm_chunk \
       -header webm_live_audio_128.hdr \
       -chunk_start_index 1 \
       -audio_chunk_duration 1000 \
       webm_live_audio_128_%d.chk
```

## webm_dash_manifest

WebM DASH 清单复用器。

此复用器实现 WebM DASH 清单规范以生成 DASH 清单 XML。它也支持为 DASH 直播流生成清单。

更多信息参见：

- WebM DASH 规范：<https://sites.google.com/a/webmproject.org/wiki/adaptive-streaming/webm-dash-specification>

- ISO DASH 规范：<http://standards.iso.org/ittf/PubliclyAvailableStandards/c065274_ISO_IEC_23009-1_2014.zip>

### 选项

此复用器支持以下选项：

- **`adaptation_sets`** 此选项语法为："id=x,streams=a,b,c id=y,streams=d,e"，其中 x 与 y 是适配集的唯一标识符，a、b、c、d、e 是相应音频与视频流的索引。可用此选项添加任意数量的适配集。

- **`live`** 设为 1 以创建直播流 DASH 清单。默认：0。

- **`chunk_start_index`** 第一个 chunk 的起始索引。它进入清单中 `SegmentTemplate` 元素的 `startNumber` 属性。默认：0。

- **`chunk_duration_ms`** 每个 chunk 的时长（毫秒）。它进入清单中 `SegmentTemplate` 元素的 `duration` 属性。默认：1000。

- **`utc_timing_url`** 返回 ISO 格式 UTC 时间戳的页面 URL。它进入清单中 `UTCTiming` 元素的 `value` 属性。默认：无。

- **`time_shift_buffer_depth`** 保证任何 Representation 可用的最小时移缓冲时间（秒）。它进入清单中 `MPD` 元素的 `timeShiftBufferDepth` 属性。默认：60。

- **`minimum_update_period`** 清单的最小更新周期（秒）。它进入清单中 `MPD` 元素的 `minimumUpdatePeriod` 属性。默认：0。

### 示例

``` text
ffmpeg -f webm_dash_manifest -i video1.webm \
       -f webm_dash_manifest -i video2.webm \
       -f webm_dash_manifest -i audio1.webm \
       -f webm_dash_manifest -i audio2.webm \
       -map 0 -map 1 -map 2 -map 3 \
       -c copy \
       -f webm_dash_manifest \
       -adaptation_sets "id=0,streams=0,1 id=1,streams=2,3" \
       manifest.xml
```

## whip

支持按 WHIP (WebRTC-HTTP ingestion protocol) 规范进行亚秒级延迟流式传输的 WebRTC (Real-Time Communication) 复用器。

这是实验性功能。

它使用 HTTP 作为信令协议交换 SDP 能力与 ICE lite 候选。随后使用 STUN 绑定请求与响应在 UDP 上建立会话。接着发起 DTLS 握手以交换 SRTP 加密密钥。最后将视频与音频帧拆分为 RTP 包并用 SRTP 加密。

请确保视频使用不带 B 帧的 H.264，音频编解码器使用 Opus。例如，用 `ffmpeg` 将输入文件转换为 WebRTC：

``` text
ffmpeg -re -i input.mp4 -acodec libopus -ar 48000 -ac 2 \
  -vcodec libx264 -profile:v baseline -tune zerolatency -threads 1 -bf 0 \
  -f whip "http://localhost:1985/rtc/v1/whip/?app=live&stream=livestream"
```

在此示例中我们采用了低延迟选项，端到端延迟约为 150ms。

### 选项

此复用器支持以下选项：

- **`handshake_timeout integer`** 设置 ICE 与 DTLS 握手的超时（毫秒）。默认值为 5000。

- **`timeout integer`** 设置套接字 I/O 操作超时（秒）。仅适用于 HTTP 输出。默认值为 -1。

- **`pkt_size integer`** 设置发出的 RTP 包的最大大小（字节）。默认值为 1200。

- **`ts_buffer_size integer`** 设置底层协议的缓冲大小（字节）。默认值为 -1（自动）。UDP 自动选择合理的值。

- **`whip_flags flags`** 可能的取值：

  | Term | Description |
  |----|----|
  | `dtls_active` | 复用器将尝试设置 dtls 主动角色并发送第一个 client hello。 |

- **`rtp_history integer`** 设置要存储的 RTP 历史条目数。默认值为 512。

- **`authorization string`** WHIP 授权的可选 Bearer 令牌。

- **`cert_file string`** DTLS 的可选证书文件路径。

- **`key_file string`** DTLS 的可选私钥文件路径。

# 元数据

FFmpeg 可以将媒体文件中的元数据转储到简单的 UTF-8 编码、类 INI 的文本文件中，然后再用元数据复用器/解复用器加载回来。

文件格式如下：

1.  文件由头和若干分为小节 (section) 的元数据标签组成，各占一行。

2.  头是一个 `;FFMETADATA` 字符串，后跟版本号（当前为 1）。

3.  元数据标签形如 `key=value`

4.  头之后紧跟全局元数据

5.  全局元数据之后可以有带每流/每章节元数据的小节。

6.  小节以括号（`[`、`]`）中的大写小节名（即 STREAM 或 CHAPTER）开始，到下一个小节或文件末尾结束。

7.  章节小节开头可以有可选的 timebase，用于 start/end 值。它必须形如 `TIMEBASE=num/den`，其中 \<num\> 与 \<den\> 是整数。若缺少 timebase，则 start/end 时间按纳秒假定。

    接着，章节小节必须包含形如 `START=num`、`END=num` 的章节开始与结束时间，其中 \<num\> 是正整数。

8.  空行以及以 `;` 或 `#` 开头的行被忽略。

9.  包含特殊字符（`=`、`;`、`#`、`\` 和换行）的元数据键或值必须用反斜杠 `\` 转义。

10. 注意元数据中的空白（如 `foo = bar`）被视为标签的一部分（上例中键为 `foo`，值为 `bar`）。

ffmetadata 文件可能形如：

``` text
;FFMETADATA1
title=bike\\shed
;this is a comment
artist=FFmpeg troll team

[CHAPTER]
TIMEBASE=1/1000
START=0
#chapter ends at 0:01:00
END=60000
title=chapter \#1
[STREAM]
title=multi\
line
```

通过配合使用 ffmetadata 复用器与解复用器，可以把输入文件的元数据提取到 ffmetadata 文件，然后用编辑后的 ffmetadata 文件把该文件转码为输出文件。

用 `ffmpeg` 提取 ffmetadata 文件如下：

``` text
ffmpeg -i INPUT -f ffmetadata FFMETADATAFILE
```

从 FFMETADATAFILE 文件重新插入编辑后的元数据信息可这样做：

``` text
ffmpeg -i INPUT -i FFMETADATAFILE -map_metadata 1 -codec copy OUTPUT
```

# 另请参见

ffmpeg(1), ffplay(1), ffprobe(1), libavformat(3)
