# 概要

ffprobe \[\<options\>\] `input_url`

# 描述

ffprobe 从多媒体流中收集信息，并以人类和机器均可读的方式打印出来。

例如，可以用它检查多媒体流所用容器的格式，以及其中每条媒体流的格式和类型。

如果在输入中指定了 url，ffprobe 会尝试打开并探测该 url 的内容。若 url 无法打开或无法识别为多媒体文件，则返回正的退出码。

如果没有通过 `o` 指定输出，ffprobe 将写入 stdout。

ffprobe 既可作为独立应用使用，也可与文本滤镜结合使用，由后者执行更复杂的处理，例如统计处理或绘图。

选项用于列出 ffprobe 支持的部分格式、指定显示哪些信息，以及设置 ffprobe 将如何显示这些信息。

ffprobe 的输出设计为易于被文本滤镜解析，由一个或多个小节组成，其形式由所选的写入器 (writer) 定义，写入器通过 `output_format` 选项指定。

小节可以包含其他嵌套的小节，每个小节由一个名称（可与其他小节共享）和一个唯一名称标识。参见 `sections` 的输出。

存储在容器或流中的元数据标签会被识别，并打印在对应的 "FORMAT"、"STREAM"、"STREAM_GROUP_STREAM" 或 "PROGRAM_STREAM" 小节中。

# 选项

## 主要选项

- **`-f format`** 强制使用的格式。

- **`-unit`** 为显示的值显示单位。

- **`-prefix`** 对显示的值使用 SI 前缀。除非使用 "-byte_binary_prefix" 选项，所有前缀均为十进制。

- **`-byte_binary_prefix`** 对字节值强制使用二进制前缀。

- **`-sexagesimal`** 时间值使用六十进制格式 HH:MM:SS.MICROSECONDS。

- **`-pretty`** 美化所显示值的格式，相当于同时使用 "-unit -prefix -byte_binary_prefix -sexagesimal" 选项。

- **`-output_format, -of, -print_format writer_name[=writer_options]`** 设置输出打印格式。

  \<writer_name\> 指定写入器的名称，\<writer_options\> 指定传给写入器的选项。

  例如要以 JSON 格式打印输出，可指定：

  ``` text
  -output_format json
  ```

  有关可用输出打印格式的更多细节，参见下文的写入器一节。

- **`-sections`** 打印小节结构和小节信息后退出。其输出并非供机器解析。

- **`-select_streams stream_specifier`** 只选择由 \<stream_specifier\> 指定的流。该选项只影响与流相关的选项（例如 `show_streams`、`show_packets` 等）。

  例如只显示音频流，可使用命令：

  ``` text
  ffprobe -show_streams -select_streams a INPUT
  ```

  只显示属于索引为 1 的视频流的视频包：

  ``` text
  ffprobe -show_packets -select_streams v:1 INPUT
  ```

- **`-show_data`** 显示载荷数据，以十六进制和 ASCII 转储的形式呈现（可用 `-data_dump_format` 选择其他格式）。与 `-show_packets` 搭配时，转储包数据；与 `-show_streams` 搭配时，转储编解码器 extradata。

  转储内容打印为 "data" 字段，其中可能包含换行。

- **`-show_data_hash algorithm`** 显示载荷数据的哈希：配合 `-show_packets` 用于包，配合 `-show_streams` 用于编解码器 extradata。

- **`-data_dump_format format`** 选择 `-show_data` 选项所启用数据转储使用的格式。默认为 `xxd`，一种与知名程序 `xxd` 兼容的十六进制转储格式。也支持 `base64`。

- **`-show_error`** 显示探测输入时发现的错误信息。

  错误信息打印在名为 "ERROR" 的小节中。

- **`-show_format`** 显示输入多媒体流容器格式的信息。

  所有容器格式信息打印在名为 "FORMAT" 的小节中。

- **`-show_entries section_entries`** 设置要显示的条目列表。

  条目按以下语法指定。\<section_entries\> 包含以 `:` 分隔的小节条目列表。每个小节条目由一个小节名称（或唯一名称）组成，其后可跟以 `,` 分隔的该小节局部条目列表。

  如果指定了小节名称但后面没有 `=`，则打印该小节的所有条目及其包含的所有小节。否则只打印局部条目列表中指定的条目。特别地，如果指定了 `=` 但局部条目列表为空，则该小节不显示任何条目。

  注意，局部小节条目的指定顺序在输出中不会生效，将保持常规显示顺序。

  形式化语法如下：

  ``` text
  LOCAL_SECTION_ENTRIES ::= SECTION_ENTRY_NAME[,LOCAL_SECTION_ENTRIES]
  SECTION_ENTRY         ::= SECTION_NAME[=[LOCAL_SECTION_ENTRIES]]
  SECTION_ENTRIES       ::= SECTION_ENTRY[:SECTION_ENTRIES]
  ```

  例如，只显示每条流的 index（索引）和 type（类型），以及包的 PTS 时间、时长和流索引，可指定参数：

  ``` text
  packet=pts_time,duration_time,stream_index : stream=index,codec_type
  ```

  显示 "format" 小节的所有条目，但 "stream" 小节只显示编解码器类型，可指定参数：

  ``` text
  format : stream=codec_type
  ```

  显示 stream 和 format 小节中的所有标签：

  ``` text
  stream_tags : format_tags
  ```

  只显示 stream 小节中的 `title` 标签（如可用）：

  ``` text
  stream_tags=title
  ```

- **`-show_packets`** 显示输入多媒体流中每个包的信息。

  每个包的信息打印在名为 "PACKET" 的专用小节中。

- **`-show_frames`** 显示输入多媒体流中每帧和每条字幕的信息。

  每帧的信息打印在名为 "FRAME" 或 "SUBTITLE" 的专用小节中。

- **`-show_log loglevel`** 按 \<loglevel\> 设置的值显示解码器针对每帧输出的日志信息（参见 `-loglevel`）。该选项要求同时使用 `-show_frames`。

  每条日志消息打印在名为 "LOG" 的专用小节中。

- **`-show_streams`** 显示输入多媒体流中每条媒体流的信息。

  每条媒体流的信息打印在名为 "STREAM" 的专用小节中。

- **`-show_programs`** 显示输入多媒体流中节目及其流的信息。

  每条媒体流的信息打印在名为 "PROGRAM_STREAM" 的小节中。

- **`-show_stream_groups`** 显示输入多媒体流中流组及其流的信息。

  每条媒体流的信息打印在名为 "STREAM_GROUP_STREAM" 的小节中。

- **`-show_chapters`** 显示格式中存储的章节信息。

  每个章节打印在名为 "CHAPTER" 的专用小节中。

- **`-count_frames`** 统计每条流的帧数并在对应的流小节中报告。

- **`-count_packets`** 统计每条流的包数并在对应的流小节中报告。

- **`-read_intervals read_intervals`** 只读取指定的区间。\<read_intervals\> 必须是以 "," 分隔的区间描述序列。`ffprobe` 会定位到区间起点，并从那里继续读取。

  每个区间由以 "%" 分隔的两个可选部分指定。

  第一部分指定区间起始位置。它按绝对位置解释；若以 "+" 字符开头，则按相对当前位置的偏移解释。若未指定第一部分，读取该区间时不进行定位。

  第二部分指定区间结束位置。它按绝对位置解释；若以 "+" 字符开头，则按相对当前位置的偏移解释。若偏移描述以 "#" 开头，则解释为从区间起点开始读取的包数（不包括冲刷包）。若未指定第二部分，程序将读到输入末尾。

  注意定位并不精确，因此实际区间起点可能与指定位置不同。此外，当指定了区间时长时，绝对结束时间按定位文件找到的区间起点加时长计算，而不是加在指定的起始值上。

  形式化语法如下：

  ``` text
  INTERVAL  ::= [START|+START_OFFSET][%[END|+END_OFFSET]]
  INTERVALS ::= INTERVAL[,INTERVALS]
  ```

  下面给出几个示例。

  - 定位到时间 10，读取包直到定位点之后 20 秒，然后定位到 `01:30`（1 分 30 秒）处并读取包直到 `01:45` 处。

    ``` text
    10%+20,01:30%01:45
    ```

  - 定位到 `01:23` 处后只读取 42 个包：

    ``` text
    01:23%+#42
    ```

  - 只读取开头前 20 秒：

    ``` text
    %+20
    ```

  - 从开头读取到 `02:30` 处：

    ``` text
    %02:30
    ```

- **`-show_private_data, -private`** 显示私有数据，即依赖于所显示元素具体格式的数据。该选项默认启用，但特定用途下可能需要禁用，例如生成符合 XSD 的 XML 输出时。

- **`-show_program_version`** 显示与程序版本相关的信息。

  版本信息打印在名为 "PROGRAM_VERSION" 的小节中。

- **`-show_library_versions`** 显示与库版本相关的信息。

  每个库的版本信息打印在名为 "LIBRARY_VERSION" 的小节中。

- **`-show_versions`** 显示与程序和库版本相关的信息。相当于同时设置 `-show_program_version` 和 `-show_library_versions` 选项。

- **`-show_pixel_formats`** 显示 FFmpeg 支持的所有像素格式的信息。

  每个格式的像素格式信息打印在名为 "PIXEL_FORMAT" 的小节中。

- **`-show_optional_fields value`** 某些写入器（即 JSON 和 XML）会省略对无效或不适用值的字段的打印，而其他写入器总是打印它们。该选项可控制这一行为。有效值为 `always`/`1`、`never`/`0` 和 `auto`/`-1`。默认为 \<auto\>。

- **`-analyze_frames`** 分析帧和/或其 side data 直到给定的读取区间为止，提供可能在流层面有用的附加信息。必须与 `-show_streams` 选项搭配，否则无效果。

  目前，启用该选项后提供的附加字段是 `closed_captions` 和 `film_grain` 字段。

  例如，分析前 20 秒并填充这些字段：

  ``` text
  ffprobe -show_streams -analyze_frames -read_intervals "%+20" INPUT
  ```

- **`-bitexact`** 强制比特精确输出，可用于产生不依赖具体构建的输出。

- **`-i input_url`** 读取 \<input_url\>。

- **`-o output_url`** 将输出写入 \<output_url\>。未指定时，输出发送到 stdout。

- **`-c:media_specifier codec_name`** 为 \<media_specifier\> 标识的流强制指定特定的解码器实现，\<media_specifier\> 可取值 `a`（音频）、`v`（视频）、`s`（字幕）和 `d`（数据）。

# 写入器

写入器 (writer) 定义 `ffprobe` 采用的输出格式，输出的所有部分都由它打印。

写入器可接受一个或多个参数，用于指定采用的选项。选项以 \<key\>=\<value\> 对列表的形式指定，以 ":" 分隔。

所有写入器都支持以下选项：

- **`string_validation, sv`** 设置字符串校验模式。

  接受以下取值。

  - **`fail`** 一旦在输入中发现无效的字符串 (UTF-8) 序列或码点，写入器立即失败。这对校验输入元数据特别有用。

  - **`ignore`** 忽略任何校验错误。这会导致输出可能损坏，尤其是在 json 或 xml 写入器下。

  - **`replace`** 写入器会用 `string_validation_replacement` 指定的字符串替换无效的 UTF-8 序列或码点。

  默认值为 `replace`。

- **`string_validation_replacement, svr`** 设置 `string_validation` 为 `replace` 时使用的替换字符串。

  未指定该选项时，写入器将视为空字符串，即从输入字符串中删除无效序列。

下面描述当前可用的写入器。

## default

默认格式。

以如下形式打印每个小节：

``` text
[SECTION]
key1=val1
...
keyN=valN
[/SECTION]
```

元数据标签作为一行打印在对应的 FORMAT、STREAM、STREAM_GROUP_STREAM 或 PROGRAM_STREAM 小节中，并以字符串 "TAG:" 为前缀。

可接受选项的描述如下。

- **`nokey, nk`** 设为 1 时表示不打印每个字段的键。默认值为 0。

- **`noprint_wrappers, nw`** 设为 1 时表示不打印小节头和小节尾。默认值为 0。

## compact, csv

紧凑格式和 CSV 格式。

`csv` 写入器等同于 `compact`，但支持不同的默认值。

每个小节打印为单行。未指定任何选项时，输出形如：

``` text
section|key1=val1| ... |keyN=valN
```

元数据标签打印在对应的 "format" 或 "stream" 小节中。元数据标签的键（如打印）以字符串 "tag:" 为前缀。

可接受选项的描述如下。

- **`item_sep, s`** 指定输出行中分隔字段所用字符。必须是单个可打印字符，默认为 "\|"（`csv` 写入器为 ","）。

- **`nokey, nk`** 设为 1 时表示不打印每个字段的键。默认值为 0（`csv` 写入器为 1）。

- **`escape, e`** 设置使用的转义模式，默认为 "c"（`csv` 写入器为 "csv"）。

  可取以下值之一：

  - **`c`** 执行类 C 转义。包含换行（`\n`）、回车（`\r`）、制表符（`\t`）、换页符（`\f`）、转义字符（`\`）或字段分隔符 \<SEP\> 的字符串按类 C 方式转义：换行转换为序列 `\n`，回车转换为 `\r`，`\` 转换为 `\\`，分隔符 \<SEP\> 转换为 `\SEP`。

  - **`csv`** 执行类 CSV 转义，如 RFC4180 所述。包含换行（`\n`）、回车（`\r`）、双引号（`"`）或 \<SEP\> 的字符串用双引号括起。

  - **`none`** 不执行转义。

- **`print_section, p`** 值为 `1` 时在每行开头打印小节名称，设为 `0` 禁用。默认值为 `1`。

## flat

扁平格式。

自由格式输出，每行包含显式的 key=value，例如 "streams.stream.3.tags.foo=bar"。输出经过 shell 转义，因此只要分隔符是字母数字字符或下划线（参见 \<sep_char\> 选项），就可以直接嵌入 sh 脚本。

可接受选项的描述如下。

- **`sep_char, s`** 在打印的字段键中分隔章节、小节名称、ID 和可能的标签所用分隔符。

  默认值为 `.`。

- **`hierarchical, h`** 指定小节名称是否按层级给出。设为 1 且当前章节中有多个小节时，小节名称将加上章节名称前缀。值为 0 时禁用该行为。

  默认值为 1。

## ini

INI 格式输出。

以基于 INI 的格式打印输出。

采用以下约定：

- 所有键和值均为 UTF-8

- `.` 是子组分隔符

- 换行、`\t`、`\f`、`\b` 和以下字符会被转义

- `\` 是转义字符

- `#` 是注释指示符

- `=` 是键/值分隔符

- `:` 不使用，但通常被解析为键/值分隔符

该写入器以 \<key\>=\<value\> 对列表的形式接受选项，以 `:` 分隔。

可接受选项的描述如下。

- **`hierarchical, h`** 指定小节名称是否按层级给出。设为 1 且当前章节中有多个小节时，小节名称将加上章节名称前缀。值为 0 时禁用该行为。

  默认值为 1。

## json

基于 JSON 的格式。

每个小节以 JSON 记法打印。

可接受选项的描述如下。

- **`compact, c`** 设为 1 时启用紧凑输出，即每个小节打印为单行。默认值为 0。

有关 JSON 的更多信息，参见 <http://www.json.org/>。

## xml

基于 XML 的格式。

XML 输出由随 FFmpeg datadir 安装的 XML schema 描述文件 `ffprobe.xsd` 描述。

更新版本的 schema 可从 url <http://www.ffmpeg.org/schema/ffprobe.xsd> 获取，该 url 重定向到提交进 FFmpeg 开发源码树的最新 schema。

注意，只有在未指定特殊全局输出选项（`unit`、`prefix`、`byte_binary_prefix`、`sexagesimal` 等）时，发出的输出才会符合 `ffprobe.xsd` schema。

可接受选项的描述如下。

- **`fully_qualified, q`** 设为 1 时指定输出应为完全限定 (fully qualified)。默认值为 0。生成可通过 XSD 文件校验的 XML 文件时需要此项。

- **`xsd_strict, x`** 设为 1 时执行更多检查以确保输出符合 XSD。默认值为 0。该选项会自动将 `fully_qualified` 设为 1。

有关 XML 格式的更多信息，参见 <https://www.w3.org/XML/>。

# 时间码

`ffprobe` 支持时间码提取：

- MPEG1/2 时间码从 GOP 中提取，可在视频流详情（`-show_streams`，参见 \<timecode\>）中获得。

- MOV 时间码从 tmcd 轨道中提取，因此可在 tmcd 流的元数据（`-show_streams`，参见 \<TAG:timecode\>）中获得。

- DV、GXF 和 AVI 时间码可在格式元数据（`-show_format`，参见 \<TAG:timecode\>）中获得。

# 另请参见

ffmpeg(1), ffplay(1), ffmpeg-utils(1), ffmpeg-scaler(1), ffmpeg-resampler(1), ffmpeg-codecs(1), ffmpeg-bitstream-filters(1), ffmpeg-formats(1), ffmpeg-devices(1), ffmpeg-protocols(1), ffmpeg-filters(1)
