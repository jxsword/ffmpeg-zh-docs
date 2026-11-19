# 概要

ffmpeg \[\<global_options\>\] {\[\<input_file_options\>\] -i `input_url`} ... {\[\<output_file_options\>\] `output_url`} ...

# 描述

`ffmpeg` 是一个通用的多媒体转换器。它可以读取多种多样的输入——包括实时采集/录制设备——进行滤镜处理，并将它们转码为大量的输出格式。

`ffmpeg` 从任意数量的输入读取数据（输入可以是常规文件、管道、网络流、采集设备等），输入由 `-i` 选项指定；并向任意数量的输出写入数据，输出由一个普通的输出 url 指定。命令行上任何无法被解释为选项的内容都会被视为输出 url。

原则上，每个输入或输出可以包含任意数量的不同类型的基本流（视频/音频/字幕/附件/数据），尽管容器格式可能限制允许的流数量和/或类型。选择哪些输入中的哪些流进入哪个输出，要么自动完成，要么用 `-map` 选项完成（参见[流选择](#流选择)章节）。

要在选项中引用输入/输出，必须使用它们的索引（从 0 开始）。例如，第一个输入是 `0`，第二个是 `1`，依此类推。类似地，输入/输出内部的流也通过索引引用。例如 `2:3` 指第三个输入或输出中的第四条流。另请参见[流说明符](#Stream-specifiers)章节。

一般而言，选项作用于其后指定的文件。因此顺序很重要，同一个选项也可以在命令行上多次出现。每次出现的选项都会作用于其后的那个输入或输出文件。此规则的例外是全局选项（例如详细程度），它们应放在最前面。

不要混用输入文件和输出文件——先指定所有输入文件，再指定所有输出文件。同样不要混用属于不同文件的选项。所有选项只对其后的那个输入或输出文件生效，并且在文件之间会重置。

下面给出一些简单示例。

- 通过对媒体流重新编码，将一个输入媒体文件转换为不同的格式：

  ``` text
  ffmpeg -i input.avi output.mp4
  ```

- 将输出文件的视频码率设置为 64 kbit/s：

  ``` text
  ffmpeg -i input.avi -b:v 64k -bufsize 64k output.mp4
  ```

- 将输出文件的帧率强制为 24 fps：

  ``` text
  ffmpeg -i input.avi -r 24 output.mp4
  ```

- 将输入文件（仅对原始格式有效）的帧率强制为 1 fps，同时将输出文件的帧率强制为 24 fps：

  ``` text
  ffmpeg -r 1 -i input.m2v -r 24 output.mp4
  ```

对于原始格式的输入文件，可能需要 format 选项。

# 详细描述

`ffmpeg` 用下面列出的组件构建出一条转码管线。程序的运行过程，就是输入数据块从源 (source) 沿着管道流向汇 (sink)，并在途中被沿途遇到的组件不断变换的过程。

可用的组件有以下几类：

- *解复用器*（"demultiplexer" 的简称）读取输入源以提取

  - 元数据、章节等全局属性；

  - 输入基本流列表及其属性

  每个 `-i` 选项会创建一个解复用器实例，它把已编码的*包* (packet) 发送给*解码器*或*复用器*。

  在其他文献中，解复用器有时也被称为 *分离器* (splitter)，因为它的主要功能是把文件拆分为基本流（尽管有些文件只包含一条基本流）。

  解复用器的示意图如下：

  ``` text
  ┌──────────┬───────────────────────┐
  │ demuxer  │                       │ packets for stream 0
  ╞══════════╡ elementary stream 0   ├──────────────────────►
  │          │                       │
  │  global  ├───────────────────────┤
  │properties│                       │ packets for stream 1
  │   and    │ elementary stream 1   ├──────────────────────►
  │ metadata │                       │
  │          ├───────────────────────┤
  │          │                       │
  │          │     ...........       │
  │          │                       │
  │          ├───────────────────────┤
  │          │                       │ packets for stream N
  │          │ elementary stream N   ├──────────────────────►
  │          │                       │
  └──────────┴───────────────────────┘
       ▲
       │
       │ read from file, network stream,
       │     grabbing device, etc.
       │
  ```

- *解码器*接收音频、视频或字幕基本流的已编码（压缩）*包*，并将其解码为原始*帧* (frame)（视频为像素数组，音频为 PCM）。解码器通常与*解复用器*中的一条基本流相关联（并从它接收输入），但有时也可以独立存在（参见[回环解码器](#回环解码器)）。

  解码器的示意图如下：

  ``` text
            ┌─────────┐
   packets  │         │ raw frames
  ─────────►│ decoder ├────────────►
            │         │
            └─────────┘
  ```

- *滤镜链图* (filtergraph) 处理并变换原始音频或视频*帧*。滤镜链图由一个或多个单独的*滤镜* (filter) 连接成图构成。滤镜链图有两种形式——*简单*和*复杂*，分别用 `-filter` 和 `-filter_complex` 选项配置。

  简单滤镜链图与一个*输出基本流*相关联；它从*解码器*接收待滤镜处理的输入，并把滤镜处理后的输出发送给该输出流的*编码器*。

  一个先做去隔行（用 `yadif` 去隔行器）、再做缩放（用 `scale` 滤镜）的简单视频滤镜链图如下所示：

  ``` text
               ┌────────────────────────┐
               │  simple filtergraph    │
   frames from ╞════════════════════════╡ frames for
   a decoder   │  ┌───────┐  ┌───────┐  │ an encoder
  ────────────►├─►│ yadif ├─►│ scale ├─►│────────────►
               │  └───────┘  └───────┘  │
               └────────────────────────┘
  ```

  复杂滤镜链图是独立的，不与任何特定流相关联。它可以有多个（或零个）输入，且类型可以不同（音频或视频），每个输入的数据既可以来自解码器，也可以来自另一个复杂滤镜链图的输出。它还有一个或多个输出，向编码器或另一个复杂滤镜链图的输入馈送数据。

  下面的示例图展示了一个有 3 个输入和 2 个输出的复杂滤镜链图（均为视频）：

  ``` text
            ┌─────────────────────────────────────────────────┐
            │               complex filtergraph               │
            ╞═════════════════════════════════════════════════╡
   frames   ├───────┐  ┌─────────┐      ┌─────────┐  ┌────────┤ frames
  ─────────►│input 0├─►│ overlay ├─────►│ overlay ├─►│output 0├────────►
            ├───────┘  │         │      │         │  └────────┤
   frames   ├───────┐╭►│         │    ╭►│         │           │
  ─────────►│input 1├╯ └─────────┘    │ └─────────┘           │
            ├───────┘                 │                       │
   frames   ├───────┐ ┌─────┐ ┌─────┬─╯              ┌────────┤ frames
  ─────────►│input 2├►│scale├►│split├───────────────►│output 1├────────►
            ├───────┘ └─────┘ └─────┘                └────────┤
            └─────────────────────────────────────────────────┘
  ```

  第二个输入的帧被叠加到第一个输入的帧之上。第三个输入的帧先被重新缩放，然后复制为两条相同的流。其中一条叠加在前两个输入合并后的画面上，结果作为滤镜链图的第一个输出；另一条复制流则成为滤镜链图的第二个输出。

- *编码器*接收原始音频、视频或字幕*帧*，并把它们编码为已编码的*包*。编码（压缩）过程通常是有损的——它会降低流质量以缩小输出体积；有些编码器是无损的，但代价是输出体积大得多。视频或音频编码器从某个滤镜链图的输出接收输入，字幕编码器从解码器接收输入（因为字幕滤镜处理尚未支持）。每个编码器都与某个复用器的*输出基本流*相关联，并把输出发送给该复用器。

  编码器的示意图如下：

  ``` text
               ┌─────────┐
   raw frames  │         │ packets
  ────────────►│ encoder ├─────────►
               │         │
               └─────────┘
  ```

- *复用器*（multiplexer 的简称）从编码器（*转码*路径）或直接从解复用器（*流复制*路径）接收其基本流的已编码*包*，把它们交错排列（当基本流多于一条时），并把结果字节写入输出文件（或管道、网络流等）。

  复用器的示意图如下：

  ``` text
                         ┌──────────────────────┬───────────┐
   packets for stream 0  │                      │   muxer   │
  ──────────────────────►│  elementary stream 0 ╞═══════════╡
                         │                      │           │
                         ├──────────────────────┤  global   │
   packets for stream 1  │                      │properties │
  ──────────────────────►│  elementary stream 1 │   and     │
                         │                      │ metadata  │
                         ├──────────────────────┤           │
                         │                      │           │
                         │     ...........      │           │
                         │                      │           │
                         ├──────────────────────┤           │
   packets for stream N  │                      │           │
  ──────────────────────►│  elementary stream N │           │
                         │                      │           │
                         └──────────────────────┴─────┬─────┘
                                                      │
                       write to file, network stream, │
                           grabbing device, etc.      │
                                                      │
                                                      ▼
  ```

## 流复制

`ffmpeg` 中最简单的管线是单流*流复制* (streamcopy)，即不解码、不滤镜处理、不编码地复制一条*输入基本流*的包。举例来说，设有一个名为 `INPUT.mkv` 的输入文件，含 3 条基本流，我们取第二条写入文件 `OUTPUT.mp4`。这样的管线示意如下：

``` text
┌──────────┬─────────────────────┐
│ demuxer  │                     │ unused
╞══════════╡ elementary stream 0 ├────────╳
│          │                     │
│INPUT.mkv ├─────────────────────┤          ┌──────────────────────┬───────────┐
│          │                     │ packets  │                      │   muxer   │
│          │ elementary stream 1 ├─────────►│  elementary stream 0 ╞═══════════╡
│          │                     │          │                      │OUTPUT.mp4 │
│          ├─────────────────────┤          └──────────────────────┴───────────┘
│          │                     │ unused
│          │ elementary stream 2 ├────────╳
│          │                     │
└──────────┴─────────────────────┘
```

上面的管线可以用下面的命令行构建：

``` text
ffmpeg -i INPUT.mkv -map 0:1 -c copy OUTPUT.mp4
```

在这条命令行中：

- 有一个输入 `INPUT.mkv`；

- 该输入没有任何输入选项；

- 有一个输出 `OUTPUT.mp4`；

- 该输出有两个输出选项：

  - `-map 0:1` 选择要使用的输入流——从索引 0 的输入（即第一个输入）中取索引 1 的流（即第二条流）；

  - `-c copy` 选择 `copy` 编码器，即不解码、不编码的流复制。

流复制适合用来改变基本流数量、更换容器格式或修改容器级元数据。由于不涉及解码和编码，它非常快且没有质量损失。但在某些情况下可能行不通，原因多种多样（例如目标容器所需的某些信息在源中不存在）。滤镜处理显然也无法进行，因为滤镜作用于解码后的帧。

还可以构建更复杂的流复制场景——例如把两个输入文件中的流合并到一个输出：

``` text
┌──────────┬────────────────────┐         ┌────────────────────┬───────────┐
│ demuxer 0│                    │ packets │                    │   muxer   │
╞══════════╡elementary stream 0 ├────────►│elementary stream 0 ╞═══════════╡
│INPUT0.mkv│                    │         │                    │OUTPUT.mp4 │
└──────────┴────────────────────┘         ├────────────────────┤           │
┌──────────┬────────────────────┐         │                    │           │
│ demuxer 1│                    │ packets │elementary stream 1 │           │
╞══════════╡elementary stream 0 ├────────►│                    │           │
│INPUT1.aac│                    │         └────────────────────┴───────────┘
└──────────┴────────────────────┘
```

它可以用下面的命令行构建：

``` text
ffmpeg -i INPUT0.mkv -i INPUT1.aac -map 0:0 -map 1:0 -c copy OUTPUT.mp4
```

这里输出选项 `-map` 用了两次，从而在输出文件中创建两条流——一条由第一个输入馈送，一条由第二个输入馈送。单次出现的 `-c` 选项为这两条流同时选择流复制。也可以把该选项的多个实例与[流说明符](#Stream-specifiers)结合使用，为每条流应用不同的值，后续小节会演示这一点。

与之相反的场景是把单个输入中的多条流拆分到多个输出：

``` text
┌──────────┬─────────────────────┐          ┌───────────────────┬───────────┐
│ demuxer  │                     │ packets  │                   │ muxer 0   │
╞══════════╡ elementary stream 0 ├─────────►│elementary stream 0╞═══════════╡
│          │                     │          │                   │OUTPUT0.mp4│
│INPUT.mkv ├─────────────────────┤          └───────────────────┴───────────┘
│          │                     │ packets  ┌───────────────────┬───────────┐
│          │ elementary stream 1 ├─────────►│                   │ muxer 1   │
│          │                     │          │elementary stream 0╞═══════════╡
└──────────┴─────────────────────┘          │                   │OUTPUT1.mp4│
                                            └───────────────────┴───────────┘
```

构建方式如下：

``` text
ffmpeg -i INPUT.mkv -map 0:0 -c copy OUTPUT0.mp4 -map 0:1 -c copy OUTPUT1.mp4
```

注意，尽管值相同，每个输出文件仍需要单独的 `-c` 选项实例。这是因为非全局选项（绝大多数选项都属此类）只在其前面所放置文件的上下文中生效。

当然，这些示例还可以进一步推广为把任意数量的输入任意重新映射到任意数量的输出。

## 转码

*转码* (transcoding) 是先对流解码、然后再次编码的过程。由于编码通常计算开销大，且多数情况下会降低流质量（即有损），因此应当只在必要时转码，其余情况用流复制。需要转码的典型原因有：

- 应用滤镜——例如对视频缩放、去隔行或叠加；对音频重采样或混音；

- 想把流馈送给无法解码原始编解码器的组件。

注意，除非为音频、视频和字幕流指定 `-c copy`，否则 `ffmpeg` 会把它们全部转码。

考虑一个示例管线：读取一个含一条音频流和一条视频流的输入文件，对视频转码、对音频流复制，写入单个输出文件。其示意如下：

``` text
┌──────────┬─────────────────────┐
│ demuxer  │                     │       audio packets
╞══════════╡ stream 0 (audio)    ├─────────────────────────────────────╮
│          │                     │                                     │
│INPUT.mkv ├─────────────────────┤ video    ┌─────────┐     raw        │
│          │                     │ packets  │  video  │ video frames   │
│          │ stream 1 (video)    ├─────────►│ decoder ├──────────────╮ │
│          │                     │          │         │              │ │
└──────────┴─────────────────────┘          └─────────┘              │ │
                                                                     ▼ ▼
                                                                     │ │
┌──────────┬─────────────────────┐ video    ┌─────────┐              │ │
│ muxer    │                     │ packets  │  video  │              │ │
╞══════════╡ stream 0 (video)    │◄─────────┤ encoder ├──────────────╯ │
│          │                     │          │(libx264)│                │
│OUTPUT.mp4├─────────────────────┤          └─────────┘                │
│          │                     │                                     │
│          │ stream 1 (audio)    │◄────────────────────────────────────╯
│          │                     │
└──────────┴─────────────────────┘
```

并用下面的命令行实现：

``` text
ffmpeg -i INPUT.mkv -map 0:v -map 0:a -c:v libx264 -c:a copy OUTPUT.mp4
```

注意它如何用流说明符 `:v` 和 `:a` 选择输入流，并为它们应用不同的 `-c` 选项值；更多细节参见[流说明符](#Stream-specifiers)小节。

## 滤镜处理

转码时，音频和视频流可以在编码前做滤镜处理，既可以用*简单*滤镜链图，也可以用*复杂*滤镜链图。

### 简单滤镜链图

简单滤镜链图指恰好有一个输入和一个输出、且两者类型相同（音频或视频）的滤镜链图。它们用每流的 `-filter` 选项配置（`-vf` 和 `-af` 分别是 `-filter:v`（视频）和 `-filter:a`（音频）的别名）。注意，简单滤镜链图与其输出流绑定，因此例如有多条音频流时，`-af` 会为每条流创建单独的滤镜链图。

沿用上文的转码示例，加入滤镜处理（为清晰起见省略音频）后如下所示：

``` text
┌──────────┬───────────────┐
│ demuxer  │               │          ┌─────────┐
╞══════════╡ video stream  │ packets  │  video  │ frames
│INPUT.mkv │               ├─────────►│ decoder ├─────►───╮
│          │               │          └─────────┘         │
└──────────┴───────────────┘                              │
                                  ╭───────────◄───────────╯
                                  │   ┌────────────────────────┐
                                  │   │  simple filtergraph    │
                                  │   ╞════════════════════════╡
                                  │   │  ┌───────┐  ┌───────┐  │
                                  ╰──►├─►│ yadif ├─►│ scale ├─►├╮
                                      │  └───────┘  └───────┘  ││
                                      └────────────────────────┘│
                                                                │
                                                                │
┌──────────┬───────────────┐ video    ┌─────────┐               │
│ muxer    │               │ packets  │  video  │               │
╞══════════╡ video stream  │◄─────────┤ encoder ├───────◄───────╯
│OUTPUT.mp4│               │          │         │
│          │               │          └─────────┘
└──────────┴───────────────┘
```

### 复杂滤镜链图

复杂滤镜链图指无法简单描述为作用于单条流的线性处理链的滤镜链图。例如，图有多个输入和/或输出，或输出流类型与输入不同时就是这种情况。复杂滤镜链图用 `-filter_complex` 选项配置。注意该选项是全局的，因为复杂滤镜链图本质上无法与单条流或单个文件明确关联。每个 `-filter_complex` 实例都会创建一个新的复杂滤镜链图，数量不限。

复杂滤镜链图的一个简单例子是 `overlay` 滤镜：它有两个视频输入和一个视频输出，把一个视频叠加在另一个之上。对应的音频滤镜是 `amix`。

## 回环解码器

解码器通常与解复用器的流相关联，但也可以创建"回环"解码器，把某个编码器的输出解码后回馈给复杂滤镜链图。这用 `-dec` 指令完成，该指令以要解码的输出流索引为参数。每个这样的指令都会创建一个新的回环解码器，索引从 0 开始依次编号。这些索引用于在复杂滤镜链图的连接标签中引用回环解码器，详见 `-filter_complex` 的文档。

解码用 AVOptions 可以像输入/输出选项一样，放在 `-dec` 之前传给回环解码器。

例如下面的示例：

``` text
ffmpeg -i INPUT                                        \
  -map 0:v:0 -c:v libx264 -crf 45 -f null -            \
  -threads 3 -dec 0:0                                  \
  -filter_complex '[0:v][dec:0]hstack[stack]'          \
  -map '[stack]' -c:v ffv1 OUTPUT
```

该命令读取一个输入视频，然后

- （第 2 行）以低质量用 `libx264` 编码；

- （第 3 行）用 3 个线程解码这条已编码流；

- （第 4 行）把解码后的视频与原始输入视频并排拼接；

- （第 5 行）拼接后的视频再经无损编码写入 `OUTPUT`。

这样的转码管线可以用下图表示：

``` text
┌──────────┬───────────────┐
│ demuxer  │               │   ┌─────────┐            ┌─────────┐    ┌────────────────────┐
╞══════════╡ video stream  │   │  video  │            │  video  │    │ null muxer         │
│   INPUT  │               ├──►│ decoder ├──┬────────►│ encoder ├─┬─►│(discards its input)│
│          │               │   └─────────┘  │         │(libx264)│ │  └────────────────────┘
└──────────┴───────────────┘                │         └─────────┘ │
                                 ╭───────◄──╯   ┌─────────┐       │
                                 │              │loopback │       │
                                 │ ╭─────◄──────┤ decoder ├────◄──╯
                                 │ │            └─────────┘
                                 │ │
                                 │ │
                                 │ │  ┌───────────────────┐
                                 │ │  │complex filtergraph│
                                 │ │  ╞═══════════════════╡
                                 │ │  │  ┌─────────────┐  │
                                 ╰─╫─►├─►│   hstack    ├─►├╮
                                   ╰─►├─►│             │  ││
                                      │  └─────────────┘  ││
                                      └───────────────────┘│
                                                           │
┌──────────┬───────────────┐  ┌─────────┐                  │
│ muxer    │               │  │  video  │                  │
╞══════════╡ video stream  │◄─┤ encoder ├───────◄──────────╯
│  OUTPUT  │               │  │ (ffv1)  │
│          │               │  └─────────┘
└──────────┴───────────────┘
```

# 流选择

`ffmpeg` 提供 `-map` 选项，用于在每个输出文件中手动控制流选择。用户也可以不用 `-map`，让 ffmpeg 按下文所述执行自动流选择。`-vn / -an / -sn / -dn` 选项可分别用于不收录视频、音频、字幕和数据流——无论它们是手动映射的还是自动选择的，但复杂滤镜链图的输出流除外。

## 描述

以下小节描述流选择涉及的各种规则。随后的示例展示这些规则在实践中如何应用。

尽管本文尽力准确反映程序的行为，但 FFmpeg 仍在持续开发中，代码可能在本文撰写之后已经变化。

### 自动流选择

当某个输出文件没有指定任何 map 选项时，ffmpeg 会检查输出格式，判断它可以收录哪些类型的流，即视频、音频和/或字幕。对每种可接受的流类型，ffmpeg 会从所有输入中挑选一条流（如果有）。

它按以下标准选择该流：

- 视频：选择分辨率最高的流，

- 音频：选择声道数最多的流，

- 字幕：选择找到的第一条字幕流，但有一个限制：输出格式的默认字幕编码器要么基于文本、要么基于图像，只会选择与其类型相同的字幕流。

当同类型的多条流不相上下时，选择索引最小的流。

数据流和附件流不会被自动选择，只能用 `-map` 收录。

### 手动流选择

使用 `-map` 时，输出文件只收录用户映射的流，唯一的例外是下文描述的滤镜链图输出。

### 复杂滤镜链图

如果存在带未标注端口的复杂滤镜链图输出流，它们会被加入第一个输出文件。如果输出格式不支持该流类型，将导致致命错误。在没有 map 选项的情况下，收录这些流会使相应类型的自动流选择被跳过。如果有 map 选项，这些滤镜链图流会与映射的流一起收录。

带标注端口的复杂滤镜链图输出流必须被映射一次且仅一次。

### 流处理

流处理独立于流选择，字幕是一个例外（见下文）。流处理用针对特定*输出*文件中各流的 `-codec` 选项设置。特别地，编解码器选项由 ffmpeg 在流选择过程之后应用，因此不影响流选择。如果某类流没有指定 `-codec` 选项，ffmpeg 会选择输出文件复用器注册的默认编码器。

字幕是个例外。如果为输出文件指定了字幕编码器，则无论文本还是图像类型，找到的第一条字幕流都会被收录。ffmpeg 不校验指定的编码器能否转换所选流，也不校验转换后的流能否被输出格式接受。一般来说也是如此：用户手动设置编码器时，流选择过程无法检查编码后的流能否复用进输出文件。如果不能，ffmpeg 会中止，且*所有*输出文件都无法处理。

## 示例

下面的示例展示 ffmpeg 流选择方法的行为、特性和局限。

这些示例假设存在以下三个输入文件。

``` text
input file 'A.avi'
      stream 0: video 640x360
      stream 1: audio 2 channels

input file 'B.mp4'
      stream 0: video 1920x1080
      stream 1: audio 2 channels
      stream 2: subtitles (text)
      stream 3: audio 5.1 channels
      stream 4: subtitles (text)

input file 'C.mkv'
      stream 0: video 1280x720
      stream 1: audio 2 channels
      stream 2: subtitles (image)
```

**示例：自动流选择**

``` text
ffmpeg -i A.avi -i B.mp4 out1.mkv out2.wav -map 1:a -c:a copy out3.mov
```

这里指定了三个输出文件，前两个没有设置 `-map` 选项，因此 ffmpeg 会为这两个文件自动选择流。

`out1.mkv` 是 Matroska 容器文件，可接受视频、音频和字幕流，因此 ffmpeg 会尝试为每种类型各选一条。视频选择 `B.mp4` 的 `stream 0`，它在所有输入视频流中分辨率最高；音频选择 `B.mp4` 的 `stream 3`，因为它的声道数最多；字幕选择 `B.mp4` 的 `stream 2`，它是 `A.avi` 和 `B.mp4` 中的第一条字幕流。

`out2.wav` 只接受音频流，因此只选择 `B.mp4` 的 `stream 3`。

对于 `out3.mov`，由于设置了 `-map` 选项，不会进行自动流选择。`-map 1:a` 选项会选择第二个输入 `B.mp4` 的所有音频流。该输出文件不会收录其他任何流。

对前两个输出，所有收录的流都会被转码。所选编码器是各输出格式注册的默认编码器，可能与所选输入流的编解码器不匹配。

对第三个输出，音频流的编解码器选项已设为 `copy`，因此不会发生解码-滤镜处理-编码操作，也*不可能*发生。所选流的包从输入文件传递过来，直接复用进输出文件。

**示例：自动字幕选择**

``` text
ffmpeg -i C.mkv out1.mkv -c:s dvdsub -an out2.mkv
```

虽然 `out1.mkv` 是可接受字幕流的 Matroska 容器文件，但只会选择视频流和音频流。`C.mkv` 的字幕流是基于图像的，而 Matroska 复用器的默认字幕编码器是基于文本的，字幕转码预期会失败，因此该流不会被选择。而在 `out2.mkv` 中，命令指定了字幕编码器，因此除视频流外字幕流也会被选择。`-an` 的存在禁用了 `out2.mkv` 的音频流选择。

**示例：未标注端口的滤镜链图输出**

``` text
ffmpeg -i A.avi -i C.mkv -i B.mp4 -filter_complex "overlay" out1.mp4 out2.srt
```

这里用 `-filter_complex` 选项建立了一个滤镜链图，由单个视频滤镜组成。`overlay` 滤镜需要恰好两个视频输入，但没有指定任何输入，于是使用前两条可用的视频流，即 `A.avi` 和 `C.mkv` 的视频流。该滤镜的输出端口没有标签，因此被送往第一个输出文件 `out1.mp4`。正因如此，视频流的自动选择被跳过——否则本来会选择 `B.mp4` 中的流。声道数最多的音频流（即 `B.mp4` 的 `stream 3`）被自动选中。但没有选择字幕流，因为 MP4 格式没有注册默认字幕编码器，用户也没有指定字幕编码器。

第二个输出文件 `out2.srt` 只接受基于文本的字幕流。因此，虽然第一条可用字幕流属于 `C.mkv`，但它是基于图像的，故被跳过。被选中的流是 `B.mp4` 的 `stream 2`，它是第一条基于文本的字幕流。

**示例：带标注端口的滤镜链图输出**

``` text
ffmpeg -i A.avi -i B.mp4 -i C.mkv -filter_complex "[1:v]hue=s=0[outv];overlay;aresample" \
       -map '[outv]' -an        out1.mp4 \
                                out2.mkv \
       -map '[outv]' -map 1:a:0 out3.mkv
```

上面的命令会失败，因为标注为 `[outv]` 的输出端口被映射了两次。所有输出文件都不会被处理。

``` text
ffmpeg -i A.avi -i B.mp4 -i C.mkv -filter_complex "[1:v]hue=s=0[outv];overlay;aresample" \
       -an        out1.mp4 \
                  out2.mkv \
       -map 1:a:0 out3.mkv
```

上面的命令同样会失败，因为 hue 滤镜的输出带有标签 `[outv]`，却没有被映射到任何地方。

应把命令修改如下：

``` text
ffmpeg -i A.avi -i B.mp4 -i C.mkv -filter_complex "[1:v]hue=s=0,split=2[outv1][outv2];overlay;aresample" \
        -map '[outv1]' -an        out1.mp4 \
                                  out2.mkv \
        -map '[outv2]' -map 1:a:0 out3.mkv
```

`B.mp4` 的视频流被送往 hue 滤镜，其输出用 split 滤镜克隆一次，两个输出都带标签。然后各取一份，分别映射到第一个和第三个输出文件。

overlay 滤镜需要两个视频输入，它使用前两条未被占用的视频流，即 `A.avi` 和 `C.mkv` 的流。overlay 的输出没有标签，因此无论 `-map` 选项是否存在，都会被送往第一个输出文件 `out1.mp4`。

aresample 滤镜接收到第一条未被占用的音频流，即 `A.avi` 的音频流。由于该滤镜的输出同样没有标签，它也被映射到第一个输出文件。`-an` 的存在只会抑制音频流的自动或手动流选择，不会抑制滤镜链图送来的输出。这两条映射进来的流在 `out1.mp4` 中将排在被映射流之前。

映射到 `out2.mkv` 的视频、音频和字幕流完全由自动流选择决定。

`out3.mkv` 由 hue 滤镜克隆出的视频输出和 `B.mp4` 的第一条音频流组成。

# 选项

## 主选项

- **`-f fmt (input/output)`** 强制指定输入或输出文件格式。输入文件的格式通常会自动检测，输出文件的格式从文件扩展名推断，因此多数情况下不需要该选项。

- **`-i url (input)`** 输入文件 url

- **`-y (global)`** 不询问，直接覆盖输出文件。

- **`-n (global)`** 不覆盖输出文件；若指定的输出文件已存在则立即退出。

- **`-stream_loop number (input)`** 设置输入流的循环次数。循环 0 表示不循环，循环 -1 表示无限循环。

- **`-recast_media (global)`** 允许强制使用与解复用器检测或指定类型不同的媒体类型解码器。用于解码被当作数据流复用的媒体数据。

- **`-c[:stream_specifier] codec (input/output,per-stream)`** 为一条或多条流选择编码器（用在输出文件之前时）或解码器（用在输入文件之前时）。\<codec\> 是解码器/编码器的名称，或特殊值 `copy`（仅限输出），表示该流不再重新编码。

  例如

  ``` text
  ffmpeg -i INPUT -map 0 -c:v libx264 -c:a copy OUTPUT
  ```

  把所有视频流用 libx264 编码，并复制所有音频流。

  对每条流，最后一个匹配的 `c` 选项生效，因此

  ``` text
  ffmpeg -i INPUT -map 0 -c copy -c:v:1 libx264 -c:a:137 libvorbis OUTPUT
  ```

  将复制所有流，但第二条视频流用 libx264 编码，第 138 条音频流用 libvorbis 编码。

- **`-t duration (input/output)`** 作为输入选项使用时（位于 `-i` 之前），限制从输入文件读取数据的 \<duration\>。

  作为输出选项使用时（位于输出 url 之前），当输出时长达到 \<duration\> 后停止写入。

  \<duration\> 必须是时长描述，参见 `ffmpeg-utils`（ffmpeg-utils(1) 手册）中的 Time duration（时长）一节。

  -to 与 -t 互斥，且 -t 优先。

- **`-to position (input/output)`** 在 \<position\> 处停止写入输出或读取输入。\<position\> 必须是时长描述，参见 `ffmpeg-utils`（ffmpeg-utils(1) 手册）中的 Time duration（时长）一节。

  -to 与 -t 互斥，且 -t 优先。

- **`-fs limit_size (output)`** 设置文件大小上限，以字节表示。超过上限后不再写入后续字节块。输出文件的实际大小会略大于请求的文件大小。

- **`-ss position (input/output)`** 作为输入选项使用时（位于 `-i` 之前），在该输入文件内定位到 \<position\>。注意多数格式无法做到精确定位，因此 `ffmpeg` 会定位到 \<position\> 之前最近的定位点。转码且 `-accurate_seek` 启用（默认）时，定位点与 \<position\> 之间的这段额外内容会被解码并丢弃。流复制或使用 `-noaccurate_seek` 时，这段内容会被保留。

  作为输出选项使用时（位于输出 url 之前），解码但丢弃输入，直到时间戳到达 \<position\>。

  \<position\> 必须是时长描述，参见 `ffmpeg-utils`（ffmpeg-utils(1) 手册）中的 Time duration（时长）一节。

- **`-sseof position (input)`** 类似 `-ss` 选项，但相对于"文件末尾"。即负值表示文件中较早的位置，0 表示位于文件末尾。

- **`-isync input_index (input)`** 把某个输入指定为同步源。

  它取目标输入与参考输入起始时间之差，并按该差值偏移目标文件的时间戳。要得到预期结果，两个输入的源时间戳应来自同一时钟源。如果设置了 `copyts`，则还必须设置 `start_at_zero`。如果任一输入没有起始时间戳，则不做同步调整。

  可接受的值是引用有效 ffmpeg 输入索引的值。如果同步参考就是目标索引本身或 \<-1\>，则不调整目标时间戳。同步参考本身不能再同步到其他任何输入。

  默认值为 \<-1\>。

- **`-itsoffset offset (input)`** 设置输入时间偏移。

  \<offset\> 必须是时长描述，参见 `ffmpeg-utils`（ffmpeg-utils(1) 手册）中的 Time duration（时长）一节。

  该偏移会加到输入文件的时间戳上。指定正偏移意味着相应的流延迟 \<offset\> 所指定的时长。

- **`-itsscale scale (input,per-stream)`** 重新缩放输入时间戳。\<scale\> 应为浮点数。

- **`-timestamp date (output)`** 设置容器中的录制时间戳。

  \<date\> 必须是日期描述，参见 `ffmpeg-utils`（ffmpeg-utils(1) 手册）中的 Date（日期）一节。

- **`-metadata[:metadata_specifier] key=value (output,per-metadata)`** 设置元数据键/值对。

  可给出可选的 \<metadata_specifier\>，为流、章节或节目设置元数据。详见 `-map_metadata` 的文档。

  该选项会覆盖用 `-map_metadata` 设置的元数据。也可以用空值删除元数据。

  例如，设置输出文件中的标题：

  ``` text
  ffmpeg -i in.avi -metadata title="my title" out.flv
  ```

  设置第一条音频流的语言：

  ``` text
  ffmpeg -i INPUT -metadata:s:a:0 language=eng OUTPUT
  ```

- **`-disposition[:stream_specifier] value (output,per-stream)`** 设置流的 disposition 标志。

  默认值：默认情况下，所有 disposition 标志从输入流复制；若该选项作用的输出流由复杂滤镜链图馈送，则默认不设置任何 disposition 标志。

  \<value\> 是以 '+' 或 '-' 分隔的 disposition 标志序列。前缀 '+' 表示添加给定的 disposition，'-' 表示移除。如果第一个标志也带 '+' 或 '-' 前缀，最终的 disposition 是默认值经 \<value\> 更新后的结果；如果第一个标志不带前缀，最终的 disposition 就是 \<value\>。也可以把 disposition 设为 0 来清除它。

  如果输出文件未指定 `-disposition` 选项，当输出文件中某种类型有多条流且尚无该类型的流被标记为默认时，ffmpeg 会自动在每种类型的第一条流上设置 'default' disposition 标志。

  `-dispositions` 选项可列出已知的 disposition 标志。

  例如，把第二条音频流设为默认流：

  ``` text
  ffmpeg -i in.mkv -c copy -disposition:a:1 default out.mkv
  ```

  把第二条字幕流设为默认流，并移除第一条字幕流的 'default' disposition：

  ``` text
  ffmpeg -i in.mkv -c copy -disposition:s:0 0 -disposition:s:1 default out.mkv
  ```

  添加内嵌封面/缩略图：

  ``` text
  ffmpeg -i in.mp4 -i IMAGE -map 0 -map 1 -c copy -c:v:1 png -disposition:v:1 attached_pic out.mp4
  ```

  为第一条音频流添加 'original' 并移除 'comment' disposition 标志，不影响其其他 disposition 标志：

  ``` text
  ffmpeg -i in.mkv -c copy -disposition:a:0 +original-comment out.mkv
  ```

  为第一条音频流移除 'original' 并添加 'comment' disposition 标志，不影响其其他 disposition 标志：

  ``` text
  ffmpeg -i in.mkv -c copy -disposition:a:0 -original+comment out.mkv
  ```

  把第一条音频流只设为 'original' 和 'comment' disposition 标志（移除其其他 disposition 标志）：

  ``` text
  ffmpeg -i in.mkv -c copy -disposition:a:0 original+comment out.mkv
  ```

  移除第一条音频流的所有 disposition 标志：

  ``` text
  ffmpeg -i in.mkv -c copy -disposition:a:0 0 out.mkv
  ```

  并非所有复用器都支持内嵌缩略图，支持的也只支持少数格式，例如 JPEG 或 PNG。

- **`-program [title=title:][program_num=program_num:]st=stream[:st=stream...] (output)`** 创建具有指定 \<title\>、\<program_num\> 的节目，并把指定的 \<stream\> 加入其中。

- **`-stream_group [map=input_file_id=stream_group][type=type:]st=stream[:st=stream][:stg=stream_group][:id=stream_group_id...] (output)`** 创建指定 \<type\> 和 \<stream_group_id\> 的流组，或通过 \<map\> 映射一个输入组，并把指定的 \<stream\> 和/或先前定义的 \<stream_group\> 加入其中。

  \<type\> 可以是以下之一：

  - **`iamf_audio_element`** 把属于同一 IAMF Audio Element 的 \<stream\> 分为一组

    对于该组 \<type\>，可用以下选项

    - **`audio_element_type`** Audio Element 类型。支持以下取值：

      | Term      | Description                           |
      |-----------|---------------------------------------|
      | `channel` | 可扩展的声道音频表示 |
      | `scene`   | Ambisonics 表示 |

    - **`demixing`** 用于重建可扩展声道音频表示的解混信息。该选项必须用 ',' 与其余部分分隔，并接受以下 key=value 选项

      | Term           | Description                                            |
      |----------------|--------------------------------------------------------|
      | `parameter_id` | 帧中参数块可引用的标识符 |
      | `dmixp_mode`   | 预定义的解混参数组合 |

    - **`recon_gain`** 用于重建可扩展声道音频表示的重建增益 (recon gain) 信息。该选项必须用 ',' 与其余部分分隔，并接受以下 key=value 选项

      | Term           | Description                                            |
      |----------------|--------------------------------------------------------|
      | `parameter_id` | 帧中参数块可引用的标识符 |

    - **`layer`** 在 Audio Element 中定义声道布局的层。该选项必须用 ',' 与其余部分分隔。可定义多个以 ',' 分隔的条目，且必须至少设置一个。

      它接受以下以 ":" 分隔的 key=value 选项

      - **`ch_layout`** 该层的声道布局

      - **`flags`** 可用标志如下：

        - **`recon_gain`** 当 recon_gain 以元数据形式出现在帧内参数块中时是否发出信号

      - **`output_gain`**

      - **`output_gain_flags`** output_gain 作用于哪些声道。可用标志如下：

        - **`FL`**

        - **`FR`**

        - **`BL`**

        - **`BR`**

        - **`TFL`**

        - **`TFR`**

      - **`ambisonics_mode`** Ambisonics 模式。当 audio_element_type 设为 channel 时无效。

        支持以下取值：

        | Term | Description |
        |----|----|
        | `mono` | 组内每个 ambisonics 声道编码为单独的单声道流 |

    - **`default_w`** 默认权重值

  - **`iamf_mix_presentation`** 把属于同一 IAMF Mix Presentation 所引用的全部 IAMF Audio Element 的 \<stream\> 分为一组

    对于该组 \<type\>，可用以下选项

    - **`submix`** Mix Presentation 中的子混音。该选项必须用 ',' 与其余部分分隔。可定义多个以 ',' 分隔的条目，且必须至少设置一个。

      它接受以下以 ":" 分隔的 key=value 选项

      - **`parameter_id`** 帧中参数块可引用的标识符，用于对混音后的音频信号做后处理，生成用于播放的音频信号

      - **`parameter_rate`** 帧中引用该 \<parameter_id\> 的参数块内采样率、时长字段所采用的表示单位

      - **`default_mix_gain`** 当某帧没有共享同一 \<parameter_id\> 的参数块时应用的默认混音增益值

      - **`element`** 引用本 Mix Presentation 所用的 Audio Element，以生成用于播放的最终输出音频信号。该选项必须用 '\|' 与其余部分分隔。可定义多个以 '\|' 分隔的条目，且必须至少设置一个。

        它接受以下以 ":" 分隔的 key=value 选项：

        - **`stg`** 本子混音引用的 Audio Element 的 \<stream_group_id\>

        - **`parameter_id`** 帧中参数块可引用的标识符，用于在与其他已处理 Audio Element 求和之前，对被引用并渲染的 Audio Element 应用处理

        - **`parameter_rate`** 帧中引用该 \<parameter_id\> 的参数块内采样率、时长字段所采用的表示单位

        - **`default_mix_gain`** 当某帧没有共享同一 \<parameter_id\> 的参数块时应用的默认混音增益值

        - **`annotations`** 描述子混音元素的 key=value 字符串，其中 "key" 是符合 BCP-47 的字符串，用于指定 "value" 字符串的语言。"key" 必须与混音的 \<annotations\> 中的相同

        - **`headphones_rendering_mode`** 指示基于声道的输入 Audio Element 在耳机上播放时，渲染为立体声扬声器，还是用双耳渲染器做空间化。如果被引用 Audio Element 的 \<audio_element_type\> 设为 channel，则无效。

          支持以下取值：

          - **`stereo`**

          - **`binaural`**

      - **`layout`** 指定本子混音测量响度信息所用的布局。该选项必须用 '\|' 与其余部分分隔。可定义多个以 '\|' 分隔的条目，且必须至少设置一个。

        它接受以下以 ":" 分隔的 key=value 选项：

        - **`layout_type`**

          | Term | Description |
          |----|----|
          | `loudspeakers` | 布局遵循 ITU-2051-3 的扬声器声系统惯例。 |
          | `binaural` | 布局为双耳。 |

        - **`sound_system`** 声道布局，匹配 ITU-2051-3 声系统 A 到 J 之一，外加 7.1.2 和 3.1.2。当 \<layout_type\> 设为 binaural 时无效。

        - **`integrated_loudness`** 节目综合响度信息，定义见 ITU-1770-4。

        - **`digital_peak`** 音频信号的数字（采样）峰值，定义见 ITU-1770-4。

        - **`true_peak`** 音频信号的真峰值，定义见 ITU-1770-4。

        - **`dialog_anchored_loudness`** 对白响度信息，定义见 ITU-1770-4。

        - **`album_anchored_loudness`** 专辑响度信息，定义见 ITU-1770-4。

    - **`annotations`** 描述混音的 key=value 字符串，其中 "key" 是符合 BCP-47 的字符串，用于指定 "value" 字符串的语言。"key" 必须与所有子混音元素的 \<annotations\> 中的相同

  例如，从多个 WAV 输入文件创建可扩展的 5.1 IAMF 文件：

  ``` text
  ffmpeg -i front.wav -i back.wav -i center.wav -i lfe.wav
  -map 0:0 -map 1:0 -map 2:0 -map 3:0 -c:a opus
  -stream_group type=iamf_audio_element:id=1:st=0:st=1:st=2:st=3,
  demixing=parameter_id=998,
  recon_gain=parameter_id=101,
  layer=ch_layout=stereo,
  layer=ch_layout=5.1(side),
  -stream_group type=iamf_mix_presentation:id=2:stg=0:annotations=en-us=Mix_Presentation,
  submix=parameter_id=100:parameter_rate=48000|element=stg=0:parameter_id=100:annotations=en-us=Scalable_Submix|layout=sound_system=stereo|layout=sound_system=5.1(side)
  -streamid 0:0 -streamid 1:1 -streamid 2:2 -streamid 3:3 output.iamf
  ```

  把有四条流的输入 IAMF 文件中的两个流组（Audio Element 与 Mix Presentation）复制到 mp4 输出：

  ``` text
  ffmpeg -i input.iamf -c:a copy -stream_group map=0=0:st=0:st=1:st=2:st=3 -stream_group map=0=1:stg=0
  -streamid 0:0 -streamid 1:1 -streamid 2:2 -streamid 3:3 output.mp4
  ```

- **`-target type (output)`** 指定目标文件类型（`vcd`、`svcd`、`dvd`、`dv`、`dv50`）。\<type\> 可加 `pal-`、`ntsc-` 或 `film-` 前缀以使用相应标准。所有格式选项（码率、编解码器、缓冲区大小）会随之自动设置。只需输入：

  ``` text
  ffmpeg -i myfile.avi -target vcd /tmp/vcd.mpg
  ```

  当然，只要确认与标准不冲突，也可以指定额外选项，例如：

  ``` text
  ffmpeg -i myfile.avi -target vcd -bf 2 /tmp/vcd.mpg
  ```

  各目标所设置的参数如下。

  **VCD**

  ``` text
  pal:
  -f vcd -muxrate 1411200 -muxpreload 0.44 -packetsize 2324
  -s 352x288 -r 25
  -codec:v mpeg1video -g 15 -b:v 1150k -maxrate:v 1150k -minrate:v 1150k -bufsize:v 327680
  -ar 44100 -ac 2
  -codec:a mp2 -b:a 224k

  ntsc:
  -f vcd -muxrate 1411200 -muxpreload 0.44 -packetsize 2324
  -s 352x240 -r 30000/1001
  -codec:v mpeg1video -g 18 -b:v 1150k -maxrate:v 1150k -minrate:v 1150k -bufsize:v 327680
  -ar 44100 -ac 2
  -codec:a mp2 -b:a 224k

  film:
  -f vcd -muxrate 1411200 -muxpreload 0.44 -packetsize 2324
  -s 352x240 -r 24000/1001
  -codec:v mpeg1video -g 18 -b:v 1150k -maxrate:v 1150k -minrate:v 1150k -bufsize:v 327680
  -ar 44100 -ac 2
  -codec:a mp2 -b:a 224k
  ```

  **SVCD**

  ``` text
  pal:
  -f svcd -packetsize 2324
  -s 480x576 -pix_fmt yuv420p -r 25
  -codec:v mpeg2video -g 15 -b:v 2040k -maxrate:v 2516k -minrate:v 0 -bufsize:v 1835008 -scan_offset 1
  -ar 44100
  -codec:a mp2 -b:a 224k

  ntsc:
  -f svcd -packetsize 2324
  -s 480x480 -pix_fmt yuv420p -r 30000/1001
  -codec:v mpeg2video -g 18 -b:v 2040k -maxrate:v 2516k -minrate:v 0 -bufsize:v 1835008 -scan_offset 1
  -ar 44100
  -codec:a mp2 -b:a 224k

  film:
  -f svcd -packetsize 2324
  -s 480x480 -pix_fmt yuv420p -r 24000/1001
  -codec:v mpeg2video -g 18 -b:v 2040k -maxrate:v 2516k -minrate:v 0 -bufsize:v 1835008 -scan_offset 1
  -ar 44100
  -codec:a mp2 -b:a 224k
  ```

  **DVD**

  ``` text
  pal:
  -f dvd -muxrate 10080k -packetsize 2048
  -s 720x576 -pix_fmt yuv420p -r 25
  -codec:v mpeg2video -g 15 -b:v 6000k -maxrate:v 9000k -minrate:v 0 -bufsize:v 1835008
  -ar 48000
  -codec:a ac3 -b:a 448k

  ntsc:
  -f dvd -muxrate 10080k -packetsize 2048
  -s 720x480 -pix_fmt yuv420p -r 30000/1001
  -codec:v mpeg2video -g 18 -b:v 6000k -maxrate:v 9000k -minrate:v 0 -bufsize:v 1835008
  -ar 48000
  -codec:a ac3 -b:a 448k

  film:
  -f dvd -muxrate 10080k -packetsize 2048
  -s 720x480 -pix_fmt yuv420p -r 24000/1001
  -codec:v mpeg2video -g 18 -b:v 6000k -maxrate:v 9000k -minrate:v 0 -bufsize:v 1835008
  -ar 48000
  -codec:a ac3 -b:a 448k
  ```

  **DV**

  ``` text
  pal:
  -f dv
  -s 720x576 -pix_fmt yuv420p -r 25
  -ar 48000 -ac 2

  ntsc:
  -f dv
  -s 720x480 -pix_fmt yuv411p -r 30000/1001
  -ar 48000 -ac 2

  film:
  -f dv
  -s 720x480 -pix_fmt yuv411p -r 24000/1001
  -ar 48000 -ac 2
  ```

  `dv50` 目标与 `dv` 目标相同，只是三种标准下设置的像素格式均为 `yuv422p`。

  用户为上述参数设置的任何值都会覆盖目标预设值。此时输出可能不符合目标标准。

- **`-dn (input/output)`** 作为输入选项使用时，阻止文件的所有数据流被滤镜处理、被自动选择或被映射到任何输出。逐流禁用请参见 `-discard` 选项。

  作为输出选项使用时，禁用数据收录，即自动选择或映射任何数据流。完全手动控制请参见 `-map` 选项。

- **`-dframes number (output)`** 设置要输出的数据帧数量。这是 `-frames:d` 的过时别名，应改用后者。

- **`-frames[:stream_specifier] framecount (output,per-stream)`** 写入 \<framecount\> 帧后停止向该流写入。

- **`-q[:stream_specifier] q (output,per-stream)`** 使用固定质量标度 (VBR)。\<q\>/\<qscale\> 的含义取决于编解码器。如果 \<qscale\> 不带 \<stream_specifier\> 使用，则只作用于视频流——这是为了与既往行为保持兼容，因为在不使用 stream_specifier 时，给音频和视频两种不同的编解码器指定相同的编解码器特定取值通常并非本意。

- **`-filter[:stream_specifier] filtergraph (output,per-stream)`** 创建 \<filtergraph\> 指定的滤镜链图，并用它对该流做滤镜处理。

  \<filtergraph\> 是要应用到该流的滤镜链图的描述，必须恰好有一个输入和一个输出，且类型与该流相同。在滤镜链图中，输入与标签 `in` 关联，输出与标签 `out` 关联。滤镜链图语法的更多信息参见 ffmpeg-filters 手册。

  若要创建有多个输入和/或输出的滤镜链图，请参见 [-filter_complex 选项](#filter_005fcomplex_005foption)。

- **`-reinit_filter[:stream_specifier] integer (input,per-stream)`** 该布尔选项决定，当输入帧参数在流中途变化时，馈送该流的滤镜链图是否重新初始化。该选项默认启用，因为大多数视频滤镜和全部音频滤镜都无法处理输入帧属性的偏差。重新初始化时，已有滤镜状态会丢失，例如某些滤镜中可用的帧计数 `n` 参考值；重新初始化时被缓冲的帧也会丢失。触发重新初始化的变化属性：视频为帧分辨率或像素格式；音频为采样格式、采样率、声道数或声道布局。

- **`-drop_changed[:stream_specifier] integer (input,per-stream)`** 该布尔选项决定，流中途帧参数不一致的帧是被丢弃，还是触发滤镜链图重新初始化（那会造成滤镜状态丢失）。通常用于避免直播输入中出现可解码但已损坏的包。默认值为 false。

- **`-filter_threads nb_threads (global)`** 定义处理滤镜管线使用的线程数。每条管线会产生一个包含这么多线程的线程池，供并行处理使用。默认值为可用 CPU 数量。

- **`-filter_buffered_frames nb_frames (global)`** 定义滤镜链图允许缓冲的最大帧数。正常情况下，滤镜链图缓冲的帧不应超过几帧，尤其是当帧以均衡方式馈入和读出时（这也是 ffmpeg 的预期行为）。该选项允许限制滤镜链图中所有链路上缓冲的帧总数。如果生成的帧更多，滤镜处理会中止并返回错误。默认值为 0，表示不限制。

- **`-pre[:stream_specifier] preset_name (output,per-stream)`** 为匹配的流指定预设。

- **`-stats (global)`** 以"info"级日志记录编码进度/统计信息（参见 `-loglevel`）。默认开启；要显式禁用，需指定 `-nostats`。

- **`-stats_period time (global)`** 设置编码进度/统计信息的更新周期。默认为 0.5 秒。

- **`-print_graphs (global)`** 按 -print_graphs_format 设置的格式，把执行图细节打印到 stderr。

- **`-print_graphs_file filename (global)`** 按 -print_graphs_format 设置的格式，把执行图细节写入指定文件。

- **`-print_graphs_format format (global)`** 设置输出格式（可用格式：default、compact、csv、flat、ini、json、xml、mermaid、mermaidhtml）。默认格式为 json。

- **`-progress url (global)`** 向 \<url\> 发送对程序友好的进度信息。

  进度信息会周期性写入，并在编码过程结束时写入。它由 "\<key\>=\<value\>" 行组成。\<key\> 只包含字母和数字。进度信息序列的最后一个键总是 "progress"，其值为 "continue" 或 "end"。

  更新周期用 `-stats_period` 设置。

  例如，把进度信息记录到 stdout：

  ``` text
  ffmpeg -progress pipe:1 -i in.mkv out.mkv
  ```

- **`-stdin`** 启用标准输入交互。默认开启，除非标准输入已被用作输入。要显式禁用交互，需指定 `-nostdin`。

  禁用标准输入交互很有用，例如 ffmpeg 处于后台进程组时。用 `ffmpeg ... < /dev/null` 可以达到大致相同的效果，但需要 shell。

- **`-debug_ts (global)`** 打印时间戳/延迟信息。默认关闭。该选项主要用于测试和调试，其输出格式可能随版本变化，因此可移植脚本不应使用它。

  另请参见选项 `-fdebug ts`。

- **`-attach filename (output)`** 向输出文件添加附件。少数格式（如 Matroska）支持此功能，例如用于渲染字幕的字体。附件实现为一种特定类型的流，因此该选项会向文件添加一条新流。之后可以按常规方式对该流使用每流选项。用该选项创建的附件流会在所有其他流（即用 `-map` 或自动映射创建的流）之后创建。

  注意，对 Matroska 还必须设置 mimetype 元数据标签：

  ``` text
  ffmpeg -i INPUT -attach DejaVuSans.ttf -metadata:s:2 mimetype=application/x-truetype-font out.mkv
  ```

  （假设附件流是输出文件中的第三条流）。

- **`-dump_attachment[:stream_specifier] filename (input,per-stream)`** 把匹配的附件流提取到名为 \<filename\> 的文件。若 \<filename\> 为空，则使用 `filename` 元数据标签的值。

  例如，把第一个附件提取到名为 'out.ttf' 的文件：

  ``` text
  ffmpeg -dump_attachment:t:0 out.ttf -i INPUT
  ```

  把所有附件提取到由 `filename` 标签确定的文件：

  ``` text
  ffmpeg -dump_attachment:t "" -i INPUT
  ```

  技术说明——附件实现为编解码器 extradata，因此该选项实际上可用于从任何流提取 extradata，而不限于附件。

## 视频选项

- **`-vframes number (output)`** 设置要输出的视频帧数量。这是 `-frames:v` 的过时别名，应改用后者。

- **`-r[:stream_specifier] fps (input/output,per-stream)`** 设置帧率（Hz 值、分数或缩写）。

  作为输入选项使用时，忽略文件中存储的任何时间戳，改为按恒定帧率 \<fps\> 生成时间戳。这与某些输入格式（如 image2 或 v4l2）使用的 `-framerate` 选项不同（在旧版 FFmpeg 中二者曾相同）。如有疑问，请用 `-framerate` 而不是输入选项 `-r`。

  作为输出选项使用时：

  - **`video encoding`** 在编码前一刻复制或丢弃帧，以达到恒定输出帧率 \<fps\>。

  - **`video streamcopy`** 告诉复用器 \<fps\> 就是该流的帧率。这种情况下不丢弃也不复制任何数据。如果 \<fps\> 与由包时间戳确定的实际流帧率不符，可能产生无效文件。另请参见 `setts` 比特流滤镜。

- **`-fpsmax[:stream_specifier] fps (output,per-stream)`** 设置最大帧率（Hz 值、分数或缩写）。

  当输出帧率被自动设置且高于该值时，将其钳制到该值。适用于批处理，或输入帧率被误检为很高的情况。不能与 `-r` 同时设置。流复制时被忽略。

- **`-s[:stream_specifier] size (input/output,per-stream)`** 设置帧尺寸。

  作为输入选项使用时，它是 `video_size` 私有选项的快捷方式，由某些解复用器识别——这些解复用器的帧尺寸要么未存储在文件中，要么可配置，例如原始视频或视频采集设备。

  作为输出选项使用时，它会把 `scale` 视频滤镜插入到相应滤镜链图的*末尾*。若要插入到开头或其他位置，请直接使用 `scale` 滤镜。

  格式为 `wxh`（默认——与源相同）。

- **`-aspect[:stream_specifier] aspect (output,per-stream)`** 设置 \<aspect\> 指定的视频显示宽高比。

  \<aspect\> 可以是浮点数字符串，也可以是 \<num\>:\<den\> 形式的字符串，其中 \<num\> 和 \<den\> 是宽高比的分子和分母。例如 "4:3"、"16:9"、"1.3333" 和 "1.7777" 都是有效的参数值。

  若与 `-vcodec copy` 一起使用，它只影响存储在容器级的宽高比，不影响编码帧中存储的宽高比（如果存在）。

- **`-display_rotation[:stream_specifier] rotation (input,per-stream)`** 设置视频旋转元数据。

  \<rotation\> 是一个十进制数，指定视频显示前应逆时针旋转的角度（单位：度）。

  该选项会覆盖文件中存储的旋转/显示变换元数据（如有）。当视频被转码（而非复制）且 `-autorotate` 启用时，视频会在滤镜处理阶段被旋转。否则，若复用器支持，该元数据会写入输出文件。

  如果同时给出 `-display_hflip` 和/或 `-display_vflip` 选项，它们会在该选项指定的旋转之后应用。

- **`-display_hflip[:stream_specifier] (input,per-stream)`** 设置显示时图像是否应水平翻转。

  更多细节参见 `-display_rotation` 选项。

- **`-display_vflip[:stream_specifier] (input,per-stream)`** 设置显示时图像是否应垂直翻转。

  更多细节参见 `-display_rotation` 选项。

- **`-mastering_display[:stream_specifier] G(%u,%u)B(%u,%u)R(%u,%u)WP(%u,%u)L(%u,%u) (input,per-stream)`** 设置视频 mastering display（母版显示）元数据。

  \<G(%u,%u)B(%u,%u)R(%u,%u)WP(%u,%u)L(%u,%u)\> 是一个字符串，以 0.00002 为单位指定 GBR 通道和白色点 (WP) 的 X,Y 显示基色，以 0.0001 坎德拉/平方米为单位指定最大-最小亮度 (L) 值。这些值是无符号整数，表示有理数的分子：GBR 和 (WP) 的隐含分母为 50000，(L) 的隐含分母为 10000。

  该选项会覆盖文件中存储的 mastering display 元数据（如有）。

- **`-content_light[:stream_specifier] %u,%u (input,per-stream)`** 设置视频内容亮度 (content light) 元数据。

  \<%u,%u\> 是一个字符串，指定最大内容亮度电平和最大画面平均亮度电平。

  该选项会覆盖文件中存储的内容亮度元数据（如有）。

- **`-vn (input/output)`** 作为输入选项使用时，阻止文件的所有视频流被滤镜处理、被自动选择或被映射到任何输出。逐流禁用请参见 `-discard` 选项。

  作为输出选项使用时，禁用视频收录，即自动选择或映射任何视频流。完全手动控制请参见 `-map` 选项。

- **`-vcodec codec (output)`** 设置视频编解码器。这是 `-codec:v` 的别名。

- **`-pass[:stream_specifier] n (output,per-stream)`** 选择编码遍数（1 或 2）。用于两遍视频编码。第一遍把视频统计信息记录到日志文件（另请参见选项 -passlogfile），第二遍用该日志文件以精确请求的码率生成视频。第一遍时可以直接停用音频并把输出设为 null，Windows 和 Unix 示例：

  ``` text
  ffmpeg -i foo.mov -c:v libxvid -pass 1 -an -f rawvideo -y NUL
  ffmpeg -i foo.mov -c:v libxvid -pass 1 -an -f rawvideo -y /dev/null
  ```

- **`-passlogfile[:stream_specifier] prefix (output,per-stream)`** 把两遍编码日志文件名前缀设为 \<prefix\>，默认文件名前缀为 "ffmpeg2pass"。完整文件名将为 `PREFIX-N.log`，其中 N 是输出流特定的数字

- **`-vf filtergraph (output)`** 创建 \<filtergraph\> 指定的滤镜链图，并用它对该流做滤镜处理。

  这是 `-filter:v` 的别名，参见 [-filter 选项](#filter_005foption)。

- **`-autorotate`** 根据文件元数据自动旋转视频。默认启用，用 `-noautorotate` 禁用。

- **`-autoscale`** 根据第一帧的分辨率自动缩放视频。默认启用，用 `-noautoscale` 禁用。禁用 autoscale 后，滤镜图的全部输出帧可能分辨率不一致，可能不适合某些编码器/复用器。因此，除非确实清楚自己在做什么，否则不建议禁用。禁用 autoscale 的风险自负。

## 高级视频选项

- **`-pix_fmt[:stream_specifier] format (input/output,per-stream)`** 设置像素格式。用 `-pix_fmts` 可显示所有支持的像素格式。如果所选像素格式无法被选中，ffmpeg 会打印警告并选择编码器支持的最佳像素格式。如果 \<pix_fmt\> 带 `+` 前缀，当请求的像素格式无法被选中时 ffmpeg 将报错退出，且滤镜链图内的自动转换被禁用。如果 \<pix_fmt\> 只是一个 `+`，ffmpeg 会选择与输入（或图输出）相同的像素格式，并禁用自动转换。

- **`-sws_flags flags (input/output)`** 设置 libswscale 库的默认标志。如果滤镜链图定义中没有覆盖，这些标志会被自动插入的 `scale` 滤镜以及简单滤镜链图中的滤镜使用。

  缩放器 (scaler) 选项列表参见 `ffmpeg-scaler` 手册相应章节。

- **`-rc_override[:stream_specifier] override (output,per-stream)`** 针对特定区间的码率控制覆盖，格式为以斜杠分隔的 "int,int,int" 列表。前两个值是起始和结束帧号；最后一个值在为正时是使用的量化器，为负时是质量因子。

- **`-vstats`** 把视频编码统计信息转储到 `vstats_HHMMSS.log`。格式描述参见 [vstats 文件格式](#vstats-文件格式)一节。

- **`-vstats_file file`** 把视频编码统计信息转储到 \<file\>。格式描述参见 [vstats 文件格式](#vstats-文件格式)一节。

- **`-vstats_version file`** 指定使用哪个版本的 vstats 格式。默认为 `2`。格式描述参见 [vstats 文件格式](#vstats-文件格式)一节。

- **`-vtag fourcc/tag (output)`** 强制视频 tag/fourcc。这是 `-tag:v` 的别名。

- **`-force_key_frames[:stream_specifier] time[,time...] (output,per-stream)`**

- **`-force_key_frames[:stream_specifier] expr:expr (output,per-stream)`**

- **`-force_key_frames[:stream_specifier] source (output,per-stream)`**

- **`-force_key_frames[:stream_specifier] scd_metadata (output,per-stream)`** \<force_key_frames\> 可以接受以下形式的参数：

  - **`time[,time...]`** 如果参数由时间戳组成，ffmpeg 会按编码器时间基把指定时间舍入到最近的输出时间戳，并在时间戳大于等于计算值的第一帧上强制关键帧。注意，如果编码器时间基太粗，关键帧可能被强制在时间戳低于指定时间的帧上。默认编码器时间基是输出帧率的倒数，但可以用 `-enc_time_base` 设置为其他值。

    如果某个时间是 "`chapters`\[\<delta\>\]"，它会展开为文件中所有章节的开始时间（按 \<delta\> 偏移），以秒为单位。该选项可用于确保输出文件的章节标记或任何其他指定位置存在定位点。

    例如，在 5 分钟处插入一个关键帧，并在每个章节开始前 0.1 秒处插入关键帧：

    ``` text
    -force_key_frames 0:05:00,chapters-0.1
    ```

  - **`expr:expr`** 如果参数带 `expr:` 前缀，字符串 \<expr\> 会被解释为表达式并对每帧求值。求值结果非零时强制关键帧。

    \<expr\> 中的表达式可以包含以下常量：

    - **`n`** 当前处理帧的编号，从 0 开始

    - **`n_forced`** 已强制帧的数量

    - **`prev_forced_n`** 上一个被强制帧的编号；尚未强制过关键帧时为 `NAN`

    - **`prev_forced_t`** 上一个被强制帧的时间；尚未强制过关键帧时为 `NAN`

    - **`t`** 当前处理帧的时间

    例如，要每 5 秒强制一个关键帧，可以指定：

    ``` text
    -force_key_frames expr:gte(t,n_forced*5)
    ```

    要从第 13 秒开始、在上次强制时间 5 秒之后强制关键帧：

    ``` text
    -force_key_frames expr:if(isnan(prev_forced_t),gte(t,13),gte(t,prev_forced_t+5))
    ```

  - **`source`** 如果参数为 `source`，当正在编码的当前帧在其源中被标记为关键帧时，ffmpeg 会强制关键帧。如果该特定源帧不得不被丢弃，则改为强制下一个可用帧成为关键帧。

  - **`scd_metadata`** 如果参数为 `scd_metadata`，当当前帧包含键为 `lavfi.scd.time` 的元数据条目时，ffmpeg 会强制关键帧。该元数据可由 `scdet` 和 `scdet_vulkan` 等滤镜添加。避免在 `scdet` 之后插入会复制帧的滤镜，否则会导致多帧出现重复元数据并重复插入关键帧。

  注意，强制过多关键帧对某些编码器的前瞻算法非常有害：使用固定 GOP 选项或类似手段会更高效。

- **`-apply_cropping[:stream_specifier] source (input,per-stream)`** 解码后根据文件元数据自动裁剪视频。默认为 *all*。

  | Term | Description |
  |----|----|
  | `none (0)` | 不应用任何裁剪元数据。 |
  | `all (1)` | 应用编解码器级和容器级裁剪。这是默认模式。 |
  | `codec (2)` | 应用编解码器级裁剪。 |
  | `container (3)` | 应用容器级裁剪。 |

- **`-copyinkf[:stream_specifier] (output,per-stream)`** 流复制时，同时复制开头出现的非关键帧。

- **`-init_hw_device type[=name][:device[,key=value...]]`** 用给定设备参数初始化一个名为 \<name\>、类型为 \<type\> 的新硬件设备。若未指定名称，将得到形如 "\<type\>%d" 的默认名称。

  \<device\> 及后续参数的含义取决于设备类型：

  - **`cuda`** \<device\> 是 CUDA 设备的编号。

    可识别以下选项：

    | Term | Description |
    |----|----|
    | `primary_ctx` | 设为 1 时，使用主设备上下文而不是新建一个。 |

    示例：

    | Term | Description |
    |----|----|
    | *-init_hw_device cuda:1* | 选择系统中的第二个设备。 |
    | *-init_hw_device cuda:0,primary_ctx=1* | 选择第一个设备并使用主设备上下文。 |

  - **`dxva2`** \<device\> 是 Direct3D 9 显示适配器的编号。

  - **`d3d11va`** \<device\> 是 Direct3D 11 显示适配器的编号。若未指定，将尝试使用默认的 Direct3D 11 显示适配器，或硬件 VendorId 与 `vendor_id` 相符的第一块 Direct3D 11 显示适配器。

    示例：

    - ***-init_hw_device d3d11va*** 在默认 Direct3D 11 显示适配器上创建 d3d11va 设备。

    - ***-init_hw_device d3d11va:1*** 在索引为 1 的 Direct3D 11 显示适配器上创建 d3d11va 设备。

    - ***-init_hw_device d3d11va:,vendor_id=0x8086*** 在硬件 VendorId 为 0x8086 的第一块 Direct3D 11 显示适配器上创建 d3d11va 设备。

  - **`vaapi`** \<device\> 可以是 X11 显示名、DRM 渲染节点或 DirectX 适配器索引。若未指定，将尝试打开默认 X11 显示（*\$DISPLAY*），然后尝试第一个 DRM 渲染节点（*/dev/dri/renderD128*）；在 Windows 上则为默认 DirectX 适配器。

    可识别以下选项：

    - **`kernel_driver`** 未指定 \<device\> 时，用该选项指定所需设备关联的内核驱动名称。该选项仅在硬件加速方法 *drm* 和 *vaapi* 启用时可用。

    - **`vendor_id`** 未指定 \<device\> 和 \<kernel_driver\> 时，用该选项指定所需设备关联的供应商 ID。该选项仅在硬件加速方法 *drm* 和 *vaapi* 启用且未指定 *kernel_driver* 时可用。

    示例：

    - ***-init_hw_device vaapi*** 在默认设备上创建 vaapi 设备。

    - ***-init_hw_device vaapi:/dev/dri/renderD129*** 在 DRM 渲染节点 `/dev/dri/renderD129` 上创建 vaapi 设备。

    - ***-init_hw_device vaapi:1*** 在 DirectX 适配器 1 上创建 vaapi 设备。

    - ***-init_hw_device vaapi:,kernel_driver=i915*** 在与内核驱动 `i915` 关联的设备上创建 vaapi 设备。

    - ***-init_hw_device vaapi:,vendor_id=0x8086*** 在与供应商 ID `0x8086` 关联的设备上创建 vaapi 设备。

  - **`vdpau`** \<device\> 是 X11 显示名。若未指定，将尝试打开默认 X11 显示（*\$DISPLAY*）。

  - **`qsv`** \<device\> 在 `MFX_IMPL_*` 中选择一个值。允许的值有：

    - **`auto`**

    - **`sw`**

    - **`hw`**

    - **`auto_any`**

    - **`hw_any`**

    - **`hw2`**

    - **`hw3`**

    - **`hw4`**

    若未指定，使用 `auto_any`。（注意，对 QSV 而言，先创建平台合适的子设备（`dxva2`、`d3d11va` 或 `vaapi`），再从它派生 QSV 设备，可能更容易达到预期效果。）

    可识别以下选项：

    - **`child_device`** 在 Linux 上指定 DRM 渲染节点，在 Windows 上指定 DirectX 适配器。

    - **`child_device_type`** 选择平台合适的子设备类型。在 Windows 上，配置时指定 `--enable-libvpl` 则默认子设备类型为 `d3d11va`，指定 `--enable-libmfx` 则默认子设备类型为 `dxva2`。在 Linux 上，用户只能用 `vaapi` 作为子设备类型。

    示例：

    - ***-init_hw_device qsv:hw,child_device=/dev/dri/renderD129*** 在 DRM 渲染节点 `/dev/dri/renderD129` 上创建使用 `MFX_IMPL_HARDWARE` 的 QSV 设备。

    - ***-init_hw_device qsv:hw,child_device=1*** 在 DirectX 适配器 1 上创建使用 `MFX_IMPL_HARDWARE` 的 QSV 设备。

    - ***-init_hw_device qsv:hw,child_device_type=d3d11va*** 选择类型为 `d3d11va` 的 GPU 子设备，并创建使用 `MFX_IMPL_HARDWARE` 的 QSV 设备。

    - ***-init_hw_device qsv:hw,child_device_type=dxva2*** 选择类型为 `dxva2` 的 GPU 子设备，并创建使用 `MFX_IMPL_HARDWARE` 的 QSV 设备。

    - ***-init_hw_device qsv:hw,child_device=1,child_device_type=d3d11va*** 在 DirectX 适配器 1 上以子设备类型 `d3d11va` 创建使用 `MFX_IMPL_HARDWARE` 的 QSV 设备。

    - ***-init_hw_device vaapi=va:/dev/dri/renderD129 -init_hw_device qsv=hw1@\<va\>*** 在 `/dev/dri/renderD129` 上创建名为 `va` 的 VAAPI 设备，然后从设备 `va` 派生名为 `hw1` 的 QSV 设备。

  - **`opencl`** \<device\> 以 *platform_index.device_index* 形式选择平台和设备。

    还可以用键值对过滤设备集合，只查找匹配特定平台或设备字符串的设备。

    可用作过滤器的字符串有：

    - **`platform_profile`**

    - **`platform_version`**

    - **`platform_name`**

    - **`platform_vendor`**

    - **`platform_extensions`**

    - **`device_name`**

    - **`device_vendor`**

    - **`driver_version`**

    - **`device_version`**

    - **`device_profile`**

    - **`device_extensions`**

    - **`device_type`**

    索引与过滤器组合起来必须能唯一选定一个设备。

    示例：

    - ***-init_hw_device opencl:0.1*** 选择第一个平台上的第二个设备。

    - ***-init_hw_device opencl:,device_name=Foo9000*** 选择名称包含字符串 *Foo9000* 的设备。

    - ***-init_hw_device opencl:1,device_type=gpu,device_extensions=cl_khr_fp16*** 选择第二个平台上支持 *cl_khr_fp16* 扩展的 GPU 设备。

  - **`vulkan`** 如果 \<device\> 是整数，则按设备在系统相关设备列表中的索引选择设备。如果 \<device\> 是其他字符串，则选择名称包含该字符串子串的第一个设备。

    可识别以下选项：

    - **`debug`** 设为 1 时，若已安装验证层则启用它。

    - **`linear_images`** 设为 1 时，hwcontext 分配的图像将是线性且可本地映射的。

    - **`instance_extensions`** 以加号分隔的额外实例扩展列表，将被启用。

    - **`device_extensions`** 以加号分隔的额外设备扩展列表，将被启用。

    示例：

    - ***-init_hw_device vulkan:1*** 选择系统中的第二个设备。

    - ***-init_hw_device vulkan:RADV*** 选择名称包含字符串 *RADV* 的第一个设备。

    - ***-init_hw_device vulkan:0,instance_extensions=VK_KHR_wayland_surface+VK_KHR_xcb_surface*** 选择第一个设备并启用 Wayland 和 XCB 实例扩展。

- **`-init_hw_device type[=name]@source`** 初始化一个名为 \<name\>、类型为 \<type\> 的新硬件设备，从名为 \<source\> 的既有设备派生。

- **`-init_hw_device list`** 列出本 ffmpeg 构建支持的所有硬件设备类型。

- **`-filter_hw_device name`** 把名为 \<name\> 的硬件设备传给所有滤镜图中的所有滤镜。可用于设置 `hwupload` 滤镜要上传到的设备，或 `hwmap` 滤镜要映射到的设备。其他滤镜在需要硬件设备时也可能使用该参数。注意，通常仅在输入还不是硬件帧时才需要它——如果已经是硬件帧，滤镜会从收到的输入帧上下文中派生所需设备。

  这是全局设置，因此所有滤镜会收到同一个设备。

- **`-hwaccel[:stream_specifier] hwaccel (input,per-stream)`** 用硬件加速解码匹配的流。\<hwaccel\> 允许的取值有：

  - **`none`** 不使用任何硬件加速（默认）。

  - **`auto`** 自动选择硬件加速方法。

  - **`vdpau`** 使用 VDPAU（Video Decode and Presentation API for Unix）硬件加速。

  - **`dxva2`** 使用 DXVA2（DirectX Video Acceleration）硬件加速。

  - **`d3d11va`** 使用 D3D11VA（DirectX Video Acceleration）硬件加速。

  - **`vaapi`** 使用 VAAPI（Video Acceleration API）硬件加速。

  - **`qsv`** 使用 Intel QuickSync Video 加速进行视频转码。

    与大多数其他取值不同，该取值启用的不是加速解码（选中 qsv 解码器时会自动使用），而是加速转码，无需把帧复制到系统内存。

    要使其生效，解码器和编码器都必须支持 QSV 加速，且不得使用滤镜。

  - **`videotoolbox`** 使用 Video Toolbox 硬件加速。

  如果所选 hwaccel 不可用或不被所选解码器支持，该选项无效。

  注意，大多数加速方法面向播放场景，在现代 CPU 上不会比软件解码更快。此外，`ffmpeg` 通常还需要把解码后的帧从 GPU 内存复制到系统内存，造成进一步的性能损失。因此该选项主要用于测试。

- **`-hwaccel_device[:stream_specifier] hwaccel_device (input,per-stream)`** 选择用于硬件加速的设备。

  该选项只在同时指定 `-hwaccel` 选项时才有意义。它既可以按名称引用用 `-init_hw_device` 创建的既有设备，也可以创建新设备，效果如同紧接着调用了 `-init_hw_device` \<type\>:\<hwaccel_device\>。

- **`-hwaccels`** 列出本 ffmpeg 构建启用的所有硬件加速组件。实际运行时可用性取决于硬件及其合适驱动是否已安装。

- **`-fix_sub_duration_heartbeat[:stream_specifier]`** 把特定输出视频流设置为心跳流：收到随机访问包时，按它拆分并推送当前进行中的字幕。

  这可以降低尚未收到结束包或下一条字幕的字幕的延迟。代价是，为了覆盖完整时长，很可能导致字幕事件重复，因此在字幕事件传递到输出的延迟无关紧要的场景中不应使用该选项。

  要使其生效，相关输入字幕流必须设置 `-fix_sub_duration`，且输入字幕流必须直接映射到心跳流所在的同一输出。

## 音频选项

- **`-aframes number (output)`** 设置要输出的音频帧数量。这是 `-frames:a` 的过时别名，应改用后者。

- **`-ar[:stream_specifier] freq (input/output,per-stream)`** 设置音频采样频率。对输出流，默认设置为对应输入流的频率。对输入流，该选项只对音频采集设备和原始解复用器有意义，并映射为相应的解复用器选项。

- **`-aq q (output)`** 设置音频质量（编解码器特定，VBR）。这是 -q:a 的别名。

- **`-ac[:stream_specifier] channels (input/output,per-stream)`** 设置音频声道数。对输出流，默认设置为输入音频声道数。对输入流，该选项只对音频采集设备和原始解复用器有意义，并映射为相应的解复用器选项。

- **`-an (input/output)`** 作为输入选项使用时，阻止文件的所有音频流被滤镜处理、被自动选择或被映射到任何输出。逐流禁用请参见 `-discard` 选项。

  作为输出选项使用时，禁用音频收录，即自动选择或映射任何音频流。完全手动控制请参见 `-map` 选项。

- **`-acodec codec (input/output)`** 设置音频编解码器。这是 `-codec:a` 的别名。

- **`-sample_fmt[:stream_specifier] sample_fmt (output,per-stream)`** 设置音频采样格式。用 `-sample_fmts` 可获取支持的采样格式列表。

- **`-af filtergraph (output)`** 创建 \<filtergraph\> 指定的滤镜链图，并用它对该流做滤镜处理。

  这是 `-filter:a` 的别名，参见 [-filter 选项](#filter_005foption)。

## 高级音频选项

- **`-atag fourcc/tag (output)`** 强制音频 tag/fourcc。这是 `-tag:a` 的别名。

- **`-ch_layout[:stream_specifier] layout (input/output,per-stream)`** `-channel_layout` 的别名。

- **`-channel_layout[:stream_specifier] layout (input/output,per-stream)`** 设置音频声道布局。对输出流，默认设置为输入声道布局。对输入流，它会覆盖输入的声道布局。并非所有解码器都遵循被覆盖的声道布局。该选项也会为音频采集设备和原始解复用器设置声道布局，并映射为相应的解复用器选项。

- **`-guess_layout_max channels (input,per-stream)`** 如果某些输入声道布局未知，只有当其对应不超过指定声道数时才尝试猜测。例如，2 告诉 `ffmpeg` 把 1 声道识别为单声道、2 声道识别为立体声，但不把 6 声道识别为 5.1。默认总是尝试猜测。设为 0 可禁用所有猜测。用 `-channel_layout` 选项显式指定输入布局也会禁用猜测。

## 字幕选项

- **`-scodec codec (input/output)`** 设置字幕编解码器。这是 `-codec:s` 的别名。

- **`-sn (input/output)`** 作为输入选项使用时，阻止文件的所有字幕流被滤镜处理、被自动选择或被映射到任何输出。逐流禁用请参见 `-discard` 选项。

  作为输出选项使用时，禁用字幕收录，即自动选择或映射任何字幕流。完全手动控制请参见 `-map` 选项。

## 高级字幕选项

- **`-fix_sub_duration`** 修正字幕时长。对每条字幕，等待同一条流中的下一个包，并调整前者的时长以避免重叠。某些字幕编解码器（尤其是 DVB 字幕）必须这样做，因为原始包中的时长只是粗略估计，真正的结束由一个空字幕帧标记。必要时不用该选项可能导致时长被夸大，或因时间戳非单调而复用失败。

  注意，该选项会推迟所有数据的输出，直到下一条字幕包被解码：这可能大幅增加内存消耗和延迟。

- **`-canvas_size size`** 设置渲染字幕所用画布的尺寸。

## 高级选项

- **`-map [-]input_file_id[:stream_specifier][:view_specifier][:?] | [linklabel] (output)`** 在输出文件中创建一条或多条流。该选项有两种指定数据源的形式：第一种从某个输入文件（用 `-i` 指定）选择一条或多条流；第二种取某个复杂滤镜链图（用 `-filter_complex` 指定）的一个输出。

  第一种形式下，会为索引为 \<input_file_id\> 的输入文件中的每条流创建输出流。如果给出了 \<stream_specifier\>，则只使用匹配该说明符的流（\<stream_specifier\> 语法参见[流说明符](#Stream-specifiers)小节）。

  流标识符前的 `-` 字符创建"负"映射：它会把匹配的流从已创建的映射中排除。

  可以在流说明符之后给出可选的 \<view_specifier\>，多视图视频时指定要使用的视图。视图说明符可以是以下格式之一：

  - **`view:view_id`** 按 ID 选择视图；\<view_id\> 可设为 'all'，把所有视图交错合入一条流；

  - **`vidx:view_idx`** 按索引选择视图；即 0 是基础视图，1 是第一个非基础视图，依此类推。

  - **`vpos:position`** 按显示位置选择视图；\<position\> 可以是 `left` 或 `right`

  转码时默认只使用基础视图，即相当于 `vidx:0`。流复制不支持视图说明符，总是复制所有视图。

  流索引后的尾随 `?` 使映射可选：如果映射没有匹配到任何流，将忽略该映射而不是失败。注意，如果使用了无效的输入文件索引（例如映射指向不存在的输入），映射仍然会失败。

  另一种 \<\[linklabel\]\> 形式把复杂滤镜图（参见 `-filter_complex` 选项）的输出映射到输出文件。\<linklabel\> 必须对应图中已定义的输出连接标签。

  该选项可以指定多次，每次向输出文件添加更多流。任何给定输入流也可以作为不同输出流的源被映射任意多次，例如为了使用不同的编码选项和/或滤镜。流在输出中创建的顺序与 `-map` 选项在命令行上给出的顺序相同。

  使用该选项会禁用该输出文件的默认映射。

  示例：

  - ***map everything*** 把第一个输入文件的所有流映射到输出

    ``` text
    ffmpeg -i INPUT -map 0 output
    ```

  - ***select specific stream*** 如果第一个输入文件中有两条音频流，这两条流由 \<0:0\> 和 \<0:1\> 标识。可以用 `-map` 选择把哪些流放入输出文件。例如：

    ``` text
    ffmpeg -i INPUT -map 0:1 out.wav
    ```

    把 `INPUT` 中的第二条输入流映射到 `out.wav` 的（唯一）输出流。

  - ***create multiple streams*** 从输入文件 `a.mov` 选择索引为 2 的流（由标识符 \<0:2\> 指定），从输入 `b.mov` 选择索引为 6 的流（由标识符 \<1:6\> 指定），并复制到输出文件 `out.mov`：

    ``` text
    ffmpeg -i a.mov -i b.mov -c copy -map 0:2 -map 1:6 out.mov
    ```

  - ***create multiple streams 2*** 从一个输入文件选择全部视频流和第三条音频流：

    ``` text
    ffmpeg -i INPUT -map 0:v -map 0:a:2 OUTPUT
    ```

  - ***negative map*** 要映射除第二条音频之外的所有流，使用负映射

    ``` text
    ffmpeg -i INPUT -map 0 -map -0:a:1 OUTPUT
    ```

  - ***optional map*** 映射第一个输入的视频和音频流，并利用尾随 `?` 在第一个输入没有音频流时忽略音频映射：

    ``` text
    ffmpeg -i INPUT -map 0:v -map 0:a? OUTPUT
    ```

  - ***map by language*** 挑选英语音频流：

    ``` text
    ffmpeg -i INPUT -map 0:m:language:eng OUTPUT
    ```

- **`-ignore_unknown`** 忽略类型未知的输入流，而不是在尝试复制此类流时失败。

- **`-copy_unknown`** 允许复制类型未知的输入流，而不是在尝试复制此类流时失败。

- **`-map_metadata[:metadata_spec_out] infile[:metadata_spec_in] (output,per-metadata)`** 用 \<infile\> 设置下一个输出文件的元数据信息。注意这些是文件索引（从 0 开始），不是文件名。可选的 \<metadata_spec_in/out\> 参数指定要复制哪些元数据。元数据说明符可以是以下形式之一：

  - **`g`** 全局元数据，即作用于整个文件的元数据

  - **`s[:stream_spec]`** 每流元数据。\<stream_spec\> 是[流说明符](#Stream-specifiers)章节所述的流说明符。作为输入元数据说明符时，从第一条匹配的流复制；作为输出元数据说明符时，复制到所有匹配的流。

  - **`c:chapter_index`** 每章节元数据。\<chapter_index\> 是从 0 开始的章节索引。

  - **`p:program_index`** 每节目元数据。\<program_index\> 是从 0 开始的节目索引。

  若省略元数据说明符，默认为全局。

  默认情况下，全局元数据从第一个输入文件复制，每流和每章节元数据随流/章节一起复制。创建任何相关类型的映射都会禁用这些默认映射。负文件索引可用于创建仅用于禁用自动复制的哑映射。

  例如，把输入文件第一条流的元数据复制到输出文件的全局元数据：

  ``` text
  ffmpeg -i in.ogg -map_metadata 0:s:0 out.mp3
  ```

  反过来，即把全局元数据复制到所有音频流：

  ``` text
  ffmpeg -i in.mkv -map_metadata:s:a 0:g out.mkv
  ```

  注意，本例中简单的 `0` 也可以，因为默认就按全局元数据处理。

- **`-map_chapters input_file_index (output)`** 把索引为 \<input_file_index\> 的输入文件的章节复制到下一个输出文件。如果未指定章节映射，则从至少含一个章节的第一个输入文件复制章节。使用负文件索引可禁用任何章节复制。

- **`-benchmark (global)`** 在编码结束时显示基准测试信息。显示实际、系统和用户时间以及最大内存消耗。并非所有系统都支持最大内存消耗统计，不支持时通常显示为 0。

- **`-benchmark_all (global)`** 在编码过程中显示基准测试信息。显示各步骤（音频/视频编码/解码）使用的实际、系统和用户时间。

- **`-timelimit duration (global)`** 当 ffmpeg 以 CPU 用户时间计运行超过 \<duration\> 秒后退出。

- **`-dump (global)`** 把每个输入包转储到 stderr。

- **`-hex (global)`** 转储包时同时转储载荷。

- **`-readrate speed (input)`** 限制输入读取速度。

  其值为正浮点数，表示每一秒墙上时钟时间内应摄取的媒体最大时长（秒）。默认值为零，表示对摄取速度不加限制。值 `1` 表示实时速度，等同于 `-re`。

  主要用于模拟采集设备或实时输入流（例如从文件读取时）。当输入是真实的采集设备或实时流时，不应使用较低的值，否则可能导致丢包。

  当输出包的流速很重要时（例如流媒体直播）很有用。

- **`-re (input)`** 以原生帧率读取输入。等同于设置 `-readrate 1`。

- **`-readrate_initial_burst seconds`** 设置初始读取突发时间（秒），此后强制执行 `-re/-readrate`。

- **`-readrate_catchup speed (input)`** 如果输入或输出被阻塞，导致实际读取速度落后于指定的 readrate，则该速率生效，直到输入追上指定 readrate。不得低于主 readrate。

- **`-fps_mode[:stream_specifier] parameter (output,per-stream)`** 设置视频同步方法/帧率模式。

  - **`passthrough`** 每帧带着来自解复用器的时间戳直接传给复用器。

  - **`cfr`** 通过复制和丢弃帧，精确达到请求的恒定帧率。

  - **`vfr`** 帧带着各自时间戳通过，或被丢弃，以避免两帧具有相同时间戳。

  - **`auto`** 根据复用器能力在 cfr 和 vfr 之间选择。这是默认方法。

  注意，此后时间戳还可能被复用器进一步修改，例如格式选项 `avoid_negative_ts` 启用时。

  用 -map 可以选择从哪条流取时间戳。可以让视频或音频之一保持不变，把其余流同步到不变的那条。

- **`-frame_drop_threshold parameter`** 丢帧阈值，指定视频帧可以落后多少才被丢弃。以帧率为单位，1.0 即一帧。默认值为 -1.1。一个可能的用途是在时间戳噪声较大时避免丢帧，或在时间戳精确时提高丢帧精度。

- **`-apad parameters (output,per-stream)`** 填充输出音频流。等同于应用 `-af apad`。参数是与 `apad` 滤镜同样构成方式的滤镜参数字符串。要使该选项生效，必须为该输出设置 `-shortest`。

- **`-copyts`** 不处理输入时间戳，保留其原值而不尝试清理。特别是，不移除初始起始时间偏移值。

  注意，取决于 `fps_mode` 选项或特定复用器处理（例如格式选项 `avoid_negative_ts` 启用时），即使选择了该选项，输出时间戳仍可能与输入时间戳不一致。

- **`-start_at_zero`** 与 `copyts` 一起使用时，平移输入时间戳使其从零开始。

  这意味着使用例如 `-ss 50` 会让输出时间戳从 50 秒开始，无论输入文件从什么时间戳开始。

- **`-copytb mode`** 指定流复制时如何设置编码器时间基。\<mode\> 是整数值，可取以下之一：

  - **`1`** 使用解复用器时间基。

    时间基从对应的输入解复用器复制到输出编码器。复制可变帧率的视频流时，有时需要这样做来避免时间戳非单调递增。

  - **`0`** 使用解码器时间基。

    时间基从对应的输入解码器复制到输出编码器。

  - **`-1`** 尝试自动选择，以生成正常的输出。

  默认值为 -1。

- **`-enc_time_base[:stream_specifier] timebase (output,per-stream)`** 设置编码器时间基。\<timebase\> 可取以下之一：

  - **`0`** 按媒体类型分配默认值。

    视频用 1/framerate，音频用 1/samplerate。

  - **`demux`** 使用解复用器的时间基。

  - **`filter`** 使用滤镜链图的时间基。

  - **`a positive number`** 使用给定数字作为时间基。

    该字段可以按两个整数之比给出（例如 1:24、1:48000），或按十进制数给出（例如 0.04166、2.0833e-5）

  默认值为 0。

- **`-bitexact (input/output)`** 为（解）复用器和（解/编）码器启用 bitexact 模式

- **`-shortest (output)`** 在最短的输出流结束时结束编码。

  注意，该选项可能需要缓冲帧，从而引入额外延迟。该延迟的最大值可用 `-shortest_buf_duration` 选项控制。

- **`-shortest_buf_duration duration (output)`** 当至少一条流比较"稀疏"时（即帧间间隔很大——字幕通常如此），`-shortest` 选项可能需要缓冲大量数据。

  该选项控制缓冲帧的最大时长（秒）。更大的值可让 `-shortest` 选项产生更精确的结果，但会增加内存使用和延迟。

  默认值为 10 秒。

- **`-dts_delta_threshold threshold`** 时间戳不连续增量阈值，以秒的十进制数表示。

  该选项启用的时间戳不连续校正只应用于接受时间戳不连续的输入格式（启用了 `AVFMT_TS_DISCONT` 标志的格式），例如 MPEG-TS 和 HLS；使用 `-copyts` 选项时自动禁用（除非检测到回绕）。

  如果检测到绝对值大于 \<threshold\> 的时间戳不连续，ffmpeg 会通过按相应增量减小/增大当前 DTS 和 PTS 来消除不连续。

  默认值为 10。

- **`-dts_error_threshold threshold`** 时间戳错误增量阈值，以秒的十进制数表示。

  该选项启用的时间戳校正只应用于不接受时间戳不连续的输入格式（未启用 `AVFMT_TS_DISCONT` 标志的格式）。

  如果检测到绝对值大于 \<threshold\> 的时间戳不连续，ffmpeg 将丢弃 PTS/DTS 时间戳值。

  默认值为 `3600*30`（30 小时），这是任意选取的，相当保守。

- **`-muxdelay seconds (output)`** 设置最大解复用-解码延迟。

- **`-muxpreload seconds (output)`** 设置初始解复用-解码延迟。

- **`-streamid output-stream-index:new-value (output)`** 为输出流指定新的 stream-id 值。该选项应在其作用的输出文件名之前指定。存在多个输出文件时，streamid 可以重新指定为不同的值。

  例如，为输出 mpegts 文件把流 0 的 PID 设为 33、流 1 的 PID 设为 36：

  ``` text
  ffmpeg -i inurl -streamid 0:33 -streamid 1:36 out.ts
  ```

- **`-bsf[:stream_specifier] bitstream_filters (input/output,per-stream)`** 对匹配的流应用比特流滤镜。作为输入选项使用时，滤镜在每个包从解复用器收到时应用；作为输出选项使用时，在包发送给复用器之前应用。

  \<bitstream_filters\> 是以逗号分隔的比特流滤镜规格列表，每条规格形如

  ``` text
  filter[=optname0=optval0:optname1=optval1:...]
  ```

  ',=:' 中任何要作为选项值一部分的字符都需要用反斜杠转义。

  用 `-bsfs` 选项可获取比特流滤镜列表。

  例如：

  ``` text
  ffmpeg -bsf:v h264_mp4toannexb -i h264.mp4 -c:v copy -an out.h264
  ```

  把 `h264_mp4toannexb` 比特流滤镜（把 MP4 封装的 H.264 流转换为 Annex B）应用到*输入*视频流。

  反过来，

  ``` text
  ffmpeg -i file.mov -an -vn -bsf:s mov2textsub -c:s copy -f rawvideo sub.txt
  ```

  把 `mov2textsub` 比特流滤镜（从 MOV 字幕提取文本）应用到*输出*字幕流。不过要注意，由于两个示例都用 `-c copy`，滤镜应用于输入还是输出差别不大——若发生转码则不然。

- **`-tag[:stream_specifier] codec_tag (input/output,per-stream)`** 为匹配的流强制 tag/fourcc。

- **`-timecode hh:mm:ssSEPff`** 指定要写入的时间码。\<SEP\> 在非 drop 时间码时为 ':'，drop 时为 ';'（或 '.'）。

  ``` text
  ffmpeg -i input.mpg -timecode 01:02:03.04 -r 30000/1001 -s ntsc output.mpg
  ```

- **`-filter_complex filtergraph (global)`** 定义复杂滤镜链图，即有任意数量输入和/或输出的滤镜链图。简单图——恰好一个输入和一个输出且类型相同——请参见 `-filter` 选项。\<filtergraph\> 是滤镜链图的描述，见 ffmpeg-filters 手册的"Filtergraph syntax（滤镜链图语法）"一节。该选项可以指定多次——每次使用都会创建一个新的复杂滤镜链图。

  复杂滤镜链图的输入可以来自不同类型的源，以相应连接标签的格式区分：

  - 连接输入流时，使用 `[file_index:stream_specifier]`（即与 `-map` 相同的语法）。如果 \<stream_specifier\> 匹配多条流，将使用第一条。多视图视频时，流说明符后可跟视图说明符，语法参见 `-map` 选项文档。

  - 连接回环解码器时，使用 \[dec:\<dec_idx\>\]，其中 \<dec_idx\> 是要连接到给定输入的回环解码器索引。多视图视频时，解码器索引后可跟视图说明符，语法参见 `-map` 选项文档。

  - 连接另一个复杂滤镜链图的输出时，使用其连接标签。例如下面的示例：

    ``` text
    ffmpeg -i input.mkv \
      -filter_complex '[0:v]scale=size=hd1080,split=outputs=2[for_enc][orig_scaled]' \
      -c:v libx264 -map '[for_enc]' output.mkv \
      -dec 0:0 \
      -filter_complex '[dec:0][orig_scaled]hstack[stacked]' \
      -map '[stacked]' -c:v ffv1 comparison.mkv
    ```

    该命令读取一个输入视频，然后

    - （第 2 行）用一个单输入双输出的复杂滤镜链图把视频缩放到 1920x1080，并把结果复制到两个输出；

    - （第 3 行）用 `libx264` 编码其中一路缩放输出，把结果写入 `output.mkv`；

    - （第 4 行）用回环解码器解码这条已编码流；

    - （第 5 行）把回环解码器的输出（即 `libx264` 编码的视频）与缩放后的原始输入并排拼接；

    - （第 6 行）拼接后的视频再经无损编码写入 `comparison.mkv`。

    注意，这两个滤镜链图不能合并为一个，否则转码管线中会出现环（滤镜链图输出进入编码，从那里进入解码，再回到同一个图），而这样的环是不允许的。

  未标注的输入会连接到匹配类型中第一条未被占用的输入流。

  输出连接标签用 `-map` 引用。未标注的输出会加入第一个输出文件。

  注意，使用该选项时可以只用 lavfi 源而不使用常规输入文件。

  例如，把一张图片叠加到视频上

  ``` text
  ffmpeg -i video.mkv -i image.png -filter_complex '[0:v][1:v]overlay[out]' -map
  '[out]' out.mkv
  ```

  这里 `[0:v]` 指第一个输入文件中的第一条视频流，它连接到 overlay 滤镜的第一个（主）输入。类似地，第二个输入中的第一条视频流连接到 overlay 的第二个（叠加）输入。

  假设每个输入文件只有一条视频流，可以省略输入标签，因此上例等价于

  ``` text
  ffmpeg -i video.mkv -i image.png -filter_complex 'overlay[out]' -map
  '[out]' out.mkv
  ```

  此外还可以省略输出标签，滤镜图的单一输出会自动加入输出文件，因此可以简写为

  ``` text
  ffmpeg -i video.mkv -i image.png -filter_complex 'overlay' out.mkv
  ```

  作为特殊例外，可以使用位图字幕流作为输入：它会被转换为与文件中最大视频同尺寸的视频，若无视频则为 720x576。注意，这是一个实验性临时方案。待 libavfilter 正式支持字幕后将移除。

  例如，把存储为 MPEG-TS 格式的 DVB-T 录制内容中的字幕硬编码烧入画面，并把字幕延迟 1 秒：

  ``` text
  ffmpeg -i input.ts -filter_complex \
    '[#0x2ef] setpts=PTS+1/TB [sub] ; [#0x2d0] [sub] overlay' \
    -sn -map '#0x2dc' output.mkv
  ```

  （0x2d0、0x2dc 和 0x2ef 分别是视频、音频和字幕流的 MPEG-TS PID；用 0:0、0:3 和 0:7 也可以）

  用 lavfi `color` 源生成 5 秒纯红视频：

  ``` text
  ffmpeg -filter_complex 'color=c=red' -t 5 out.mkv
  ```

- **`-filter_complex_threads nb_threads (global)`** 定义处理 filter_complex 图使用的线程数。与 filter_threads 类似，但只用于 `-filter_complex` 图。默认值为可用 CPU 数量。

- **`-lavfi filtergraph (global)`** 定义复杂滤镜链图，即有任意数量输入和/或输出的滤镜链图。等同于 `-filter_complex`。

- **`-accurate_seek (input)`** 该选项启用或禁用用 `-ss` 选项在输入文件中精确定位。默认启用，因此转码时定位是精确的。用 `-noaccurate_seek` 禁用；例如部分流复制、其余流转码时可能有用。

- **`-seek_timestamp (input)`** 该选项启用或禁用用 `-ss` 选项按时间戳在输入文件中定位。默认禁用。启用后，`-ss` 选项的参数被视为实际时间戳，不再按文件起始时间偏移。这只对不从时间戳 0 开始的文件（如传输流）有意义。

- **`-thread_queue_size size (input/output)`** 对输入，该选项设置从文件或设备读取时队列包的最大数量。低延迟/高速率实时流中，包若未及时读取可能被丢弃；设置该值可强制 ffmpeg 使用单独的输入线程，并在包到达时立即读取。默认情况下，只有指定了多个输入时 ffmpeg 才这样做。

  对输出，该选项指定每个复用线程可排队包的最大数量。

- **`-sdp_file file (global)`** 把输出流的 sdp 信息打印到 \<file\>。这样在至少一个输出不是 rtp 流时也能转储 sdp 信息。（要求至少一个输出格式为 rtp）。

- **`-discard (input)`** 允许丢弃特定流或流中的特定帧。任何输入流都可以用值 `all` 完全丢弃；而对流中帧的选择性丢弃发生在解复用器，并非所有解复用器都支持。

  | Term      | Description                           |
  |-----------|---------------------------------------|
  | `none`    | 不丢弃任何帧。 |
  | `default` | 默认，不丢弃帧。 |
  | `noref`   | 丢弃所有非参考帧。 |
  | `bidir`   | 丢弃所有双向帧。 |
  | `nokey`   | 丢弃关键帧以外的所有帧。 |
  | `all`     | 丢弃所有帧。 |

- **`-abort_on flags (global)`** 在各种条件下停止并中止。可用标志如下：

  | Term | Description |
  |----|----|
  | `empty_output` | 没有包传给复用器，输出为空。 |
  | `empty_output_stream` | 某些输出流没有包传给复用器。 |

- **`-max_error_rate (global)`** 设置所有输入上解码帧失败的比例阈值，超过该比例 ffmpeg 将返回退出码 69。越过该阈值不会终止处理。取值范围是 0 到 1 之间的浮点数。默认值为 2/3。

- **`-xerror (global)`** 出错时停止并退出

- **`-max_muxing_queue_size packets (output,per-stream)`** 转码音频和/或视频流时，ffmpeg 在每条此类流都各有一个包之前不会开始写入输出。等待期间，其他流的包会被缓冲。该选项为匹配的输出流设置此缓冲区的大小（以包计）。

  该选项的默认值对大多数用途应当足够，因此除非确定需要，否则不要动它。

- **`-muxing_queue_data_threshold bytes (output,per-stream)`** 这是一个最小阈值，在此之前不考虑复用队列大小。默认每流 50 MB，基于传给复用器的包总体大小。

- **`-auto_conversion_filters (global)`** 允许在所有滤镜图中自动插入格式转换滤镜，包括 `-vf`、`-af`、`-filter_complex` 和 `-lavfi` 定义的图。如果滤镜格式协商需要转换，滤镜的初始化将失败。仍可在图中插入相关转换滤镜（scale、aresample）来执行转换。默认开启；要显式禁用，需指定 `-noauto_conversion_filters`。

- **`-bits_per_raw_sample[:stream_specifier] value (output,per-stream)`** 声明给定输出流每原始样本的位数为 \<value\>。注意，该选项设置的是提供给编码器/复用器的信息，不会改变流使其符合该值。设置与流属性不符的值可能导致编码失败或输出文件无效。

- **`-stats_enc_pre[:stream_specifier] path (output,per-stream)`**

- **`-stats_enc_post[:stream_specifier] path (output,per-stream)`**

- **`-stats_mux_pre[:stream_specifier] path (output,per-stream)`** 把匹配流的每帧编码信息写入 \<path\> 给定的文件。

  `-stats_enc_pre` 在原始视频或音频帧即将送去编码之前写入其信息；`-stats_enc_post` 在从编码器收到已编码包时写入其信息；`-stats_mux_pre` 在包即将发送给复用器时写入其信息。每帧或每包在指定文件中产生一行。行格式由 `-stats_enc_pre_fmt` / `-stats_enc_post_fmt` / `-stats_mux_pre_fmt` 控制。

  当多条流的统计信息写入同一文件时，不同流的行会交错。这种交错的精确顺序未作规定，也不保证在程序的多次运行之间保持稳定，即使选项完全相同。

- **`-stats_enc_pre_fmt[:stream_specifier] format_spec (output,per-stream)`**

- **`-stats_enc_post_fmt[:stream_specifier] format_spec (output,per-stream)`**

- **`-stats_mux_pre_fmt[:stream_specifier] format_spec (output,per-stream)`** 指定用 `-stats_enc_pre` / `-stats_enc_post` / `-stats_mux_pre` 写入行的格式。

  \<format_spec\> 是一个字符串，可包含 \<{fmt}\> 形式的指令。\<format_spec\> 采用反斜杠转义——分别用 \\、\\ 和 \\ 把字面量 {、} 或 \\ 写入输出。

  \<fmt\> 给出的指令可以是以下之一：

  - **`fidx`** 输出文件的索引。

  - **`sidx`** 输出流在文件中的索引。

  - **`n`** 帧编号。编码前：迄今发送给编码器的帧数。编码后：迄今从编码器收到的包数。复用：迄今提交给该流复用器的包数。

  - **`ni`** 输入帧编号。与该输出帧或包对应的输入帧（即由解码器输出）的索引。不可用时为 -1。

  - **`tb`** 该帧/包时间戳所用的时间基，为有理数 \<num/den\>。注意编码器和复用器可能使用不同的时间基。

  - **`tbi`** \<ptsi\> 所用的时间基，为有理数 \<num/den\>。\<ptsi\> 可用时可用，否则为 \<0/1\>。

  - **`pts`** 帧或包的显示时间戳，为整数。应乘以时间基得到显示时间。

  - **`ptsi`** 输入帧的显示时间戳（见 \<ni\>），为整数。应乘以 \<tbi\> 得到显示时间。不可用时打印为 (2^63 - 1 = 9223372036854775807)。

  - **`t`** 帧或包的显示时间，为十进制数。等于 \<pts\> 乘以 \<tb\>。

  - **`ti`** 输入帧的显示时间（见 \<ni\>），为十进制数。等于 \<ptsi\> 乘以 \<tbi\>。不可用时打印为 inf。

  - **`dts (packet)`** 包的解码时间戳，为整数。应乘以时间基得到显示时间。

  - **`dt (packet)`** 帧或包的解码时间，为十进制数。等于 \<dts\> 乘以 \<tb\>。

  - **`sn (frame,audio)`** 迄今发送给编码器的音频采样数。

  - **`samp (frame,audio)`** 帧中的音频采样数。

  - **`size (packet)`** 已编码包的大小（字节）。

  - **`br (packet)`** 当前码率（bit/s）。

  - **`abr (packet)`** 迄今整条流的平均码率（bit/s）；此刻无法确定时为 -1。

  - **`key (packet)`** 包含关键帧时为字符 'K'，否则为 'N'。

  标记为 *packet* 的指令只能用于 `-stats_enc_post_fmt` 和 `-stats_mux_pre_fmt`。

  标记为 *frame* 的指令只能用于 `-stats_enc_pre_fmt`。

  标记为 *audio* 的指令只能用于音频流。

  默认格式字符串为：

  | Term            | Description           |
  |-----------------|-----------------------|
  | `pre-encoding`  | {fidx} {sidx} {n} {t} |
  | `post-encoding` | {fidx} {sidx} {n} {t} |

  未来可能会在默认格式字符串末尾添加新条目。依赖格式保持完全一致的用户应手动指定。

  注意，写入同一文件的不同流的统计信息可能采用不同格式。

## 预设文件

预设文件包含一系列 \<option\>=\<value\> 对，每行一个，指定一组在命令行上难以输入的选项。以井号（'#'）字符开头的行会被忽略，用作注释。示例参见 FFmpeg 源码树中的 `presets` 目录。

预设文件有两类：ffpreset 和 avpreset 文件。

### ffpreset 文件

ffpreset 文件用 `vpre`、`apre`、`spre` 和 `fpre` 选项指定。`fpre` 选项以预设文件名而非预设名作为输入，可用于任何类型的编解码器。对 `vpre`、`apre` 和 `spre` 选项，预设文件中指定的选项会应用到与该预设选项同类型的当前所选编解码器上。

传给 `vpre`、`apre` 和 `spre` 预设选项的参数按以下规则确定要使用的预设文件：

首先，ffmpeg 按顺序在以下目录中搜索名为 \<arg\>.ffpreset 的文件：`$FFMPEG_DATADIR`（如已设置）、`$HOME/.ffmpeg`、配置时定义的 datadir（通常为 `PREFIX/share/ffmpeg`）；win32 上还会搜索可执行文件旁的 `ffpresets` 文件夹。例如，参数为 `libvpx-1080p` 时，将搜索文件 `libvpx-1080p.ffpreset`。

如果找不到这样的文件，ffmpeg 将在上述目录中搜索名为 \<codec_name\>-\<arg\>.ffpreset 的文件，其中 \<codec_name\> 是预设文件选项将要应用到的编解码器的名称。例如，用 `-vcodec libvpx` 选择视频编解码器并使用 `-vpre 1080p` 时，将搜索文件 `libvpx-1080p.ffpreset`。

### avpreset 文件

avpreset 文件用 `pre` 选项指定。其工作方式与 ffpreset 文件类似，但只允许编码器特定选项。因此，不能使用指定编码器的 \<option\>=\<value\> 对。

指定 `pre` 选项时，ffmpeg 会按顺序在以下目录中查找后缀为 .avpreset 的文件：`$AVCONV_DATADIR`（如已设置）、`$HOME/.avconv`、配置时定义的 datadir（通常为 `PREFIX/share/ffmpeg`）。

首先，ffmpeg 在上述目录中搜索名为 \<codec_name\>-\<arg\>.avpreset 的文件，其中 \<codec_name\> 是预设文件选项将要应用到的编解码器的名称。例如，用 `-vcodec libvpx` 选择视频编解码器并使用 `-pre 1080p` 时，将搜索文件 `libvpx-1080p.avpreset`。

如果找不到这样的文件，ffmpeg 将在相同目录中搜索名为 \<arg\>.avpreset 的文件。

## vstats 文件格式

`-vstats` 和 `-vstats_file` 选项会生成一个文件，其中包含所产生的视频输出的统计信息。

`-vstats_version` 选项控制所生成文件的格式版本。

版本 `1` 的格式为：

``` text
frame= FRAME q= FRAME_QUALITY PSNR= PSNR f_size= FRAME_SIZE s_size= STREAM_SIZEkB time= TIMESTAMP br= BITRATEkbits/s avg_br= AVERAGE_BITRATEkbits/s
```

版本 `2` 的格式为：

``` text
out= OUT_FILE_INDEX st= OUT_FILE_STREAM_INDEX frame= FRAME_NUMBER q= FRAME_QUALITYf PSNR= PSNR f_size= FRAME_SIZE s_size= STREAM_SIZEkB time= TIMESTAMP br= BITRATEkbits/s avg_br= AVERAGE_BITRATEkbits/s
```

各键对应值的说明如下：

| Term     | Description                                      |
|----------|--------------------------------------------------|
| `avg_br` | 平均码率，单位 Kbits/s |
| `br`     | 码率，单位 Kbits/s |
| `frame`  | 已编码帧的编号 |
| `out`    | 输出文件索引 |
| `PSNR`   | 峰值信噪比 |
| `q`      | 帧的质量 |
| `f_size` | 已编码包的大小（字节数） |
| `s_size` | 流大小（KiB） |
| `st`     | 输出文件的流索引 |
| `time`   | 包的时间 |
| `type`   | 图像类型 |

另一种显示编码统计信息的方式参见 [-stats_enc 选项](#stats_005fenc_005foptions)。

# 示例

## 视频和音频采集

指定输入格式和设备后，ffmpeg 可以直接采集视频和音频。

``` text
ffmpeg -f oss -i /dev/dsp -f video4linux2 -i /dev/video0 /tmp/out.mpg
```

也可以不用 OSS，改用 ALSA 音频源（单声道输入，声卡 id 为 1）：

``` text
ffmpeg -f alsa -ac 1 -i hw:1 -f video4linux2 -i /dev/video0 /tmp/out.mpg
```

注意，在启动 ffmpeg 之前，必须先用任何电视查看程序（例如 Gerd Knorr 的 [xawtv](http://linux.bytesex.org/xawtv/)）激活正确的视频源和频道。还需要用标准混音器正确设置录音电平。

## X11 抓取

用 ffmpeg 抓取 X11 显示：

``` text
ffmpeg -f x11grab -video_size cif -framerate 25 -i :0.0 /tmp/out.mpg
```

0.0 是 X11 服务器的 display.screen 编号，与 DISPLAY 环境变量相同。

``` text
ffmpeg -f x11grab -video_size cif -framerate 25 -i :0.0+10,20 /tmp/out.mpg
```

0.0 是 X11 服务器的 display.screen 编号，与 DISPLAY 环境变量相同。10 是采集的 x 偏移，20 是 y 偏移。

## 视频和音频文件格式转换

任何受支持的文件格式和协议都可以作为 ffmpeg 的输入：

示例：

- 可以使用 YUV 文件作为输入：

  ``` text
  ffmpeg -i /tmp/test%d.Y /tmp/out.mpg
  ```

  它会使用以下文件：

  ``` text
  /tmp/test0.Y, /tmp/test0.U, /tmp/test0.V,
  /tmp/test1.Y, /tmp/test1.U, /tmp/test1.V, etc...
  ```

  Y 文件的分辨率是 U、V 文件的两倍。它们是原始文件，没有文件头。所有合格的视频解码器都能生成它们。如果 ffmpeg 无法推断图像尺寸，必须用 `-s` 选项指定。

- 可以从原始 YUV420P 文件读取输入：

  ``` text
  ffmpeg -i /tmp/test.yuv /tmp/out.avi
  ```

  test.yuv 是包含原始 YUV 平面数据的文件。每帧由 Y 平面以及垂直和水平分辨率减半的 U、V 平面组成。

- 可以输出到原始 YUV420P 文件：

  ``` text
  ffmpeg -i mydivx.avi hugefile.yuv
  ```

- 可以设置多个输入文件和输出文件：

  ``` text
  ffmpeg -i /tmp/a.wav -s 640x480 -i /tmp/a.yuv /tmp/a.mpg
  ```

  把音频文件 a.wav 和原始 YUV 视频文件 a.yuv 转换为 MPEG 文件 a.mpg。

- 也可以同时进行音频和视频转换：

  ``` text
  ffmpeg -i /tmp/a.wav -ar 22050 /tmp/a.mp2
  ```

  把 a.wav 转换为 22050 Hz 采样率的 MPEG 音频。

- 可以同时编码为多种格式，并定义从输入流到输出流的映射：

  ``` text
  ffmpeg -i /tmp/a.wav -map 0:a -b:a 64k /tmp/a.mp2 -map 0:a -b:a 128k /tmp/b.mp2
  ```

  把 a.wav 以 64 kbits 转换为 a.mp2，以 128 kbits 转换为 b.mp2。'-map file:index' 指定每个输出流使用哪条输入流，按输出流定义的顺序。

- 可以转码已解密的 VOB：

  ``` text
  ffmpeg -i snatch_1.vob -f avi -c:v mpeg4 -b:v 800k -g 300 -bf 2 -c:a libmp3lame -b:a 128k snatch.avi
  ```

  这是一个典型的 DVD 提取 (ripping) 示例；输入是 VOB 文件，输出是含 MPEG-4 视频和 MP3 音频的 AVI 文件。注意本命令使用 B 帧，使 MPEG-4 流与 DivX5 兼容；GOP 大小为 300，意味着对 29.97fps 的输入视频每 10 秒一个帧内帧。此外，音频流用 MP3 编码，因此需要在 configure 时传入 `--enable-libmp3lame` 以启用 LAME 支持。这种映射对 DVD 转码获取所需音频语言尤其有用。

  注意：查看支持的输入格式请使用 `ffmpeg -demuxers`。

- 可以从视频提取图像，或从多张图像创建视频：

  从视频提取图像：

  ``` text
  ffmpeg -i foo.avi -r 1 -s WxH -f image2 foo-%03d.jpeg
  ```

  这会每秒从视频中提取一帧，输出到名为 `foo-001.jpeg`、`foo-002.jpeg` 等的文件。图像会被重新缩放以适配新的 WxH 值。

  若只想提取有限数量的帧，可以把上述命令与 `-frames:v` 或 `-t` 选项组合使用，或与 -ss 组合以从某个时间点开始提取。

  从多张图像创建视频：

  ``` text
  ffmpeg -f image2 -framerate 12 -i foo-%03d.jpeg -s WxH foo.avi
  ```

  语法 `foo-%03d.jpeg` 指定用三位数字、不足补零的十进制数表示序号。它与 C printf 函数支持的语法相同，但只接受普通整数的格式才适用。

  导入图像序列时，通过选择 image2 特有的 `-pattern_type glob` 选项，-i 还支持在内部展开类似 shell 的通配符模式 (glob)。

  例如，从匹配 glob 模式 `foo-*.jpeg` 的文件名创建视频：

  ``` text
  ffmpeg -f image2 -pattern_type glob -framerate 12 -i 'foo-*.jpeg' -s WxH foo.avi
  ```

- 可以在输出中放入多条同类型的流：

  ``` text
  ffmpeg -i test1.avi -i test2.avi -map 1:1 -map 1:0 -map 0:1 -map 0:0 -c copy -y test12.nut
  ```

  得到的输出文件 `test12.nut` 将以相反顺序包含输入文件的前四条流。

- 强制 CBR 视频输出：

  ``` text
  ffmpeg -i myfile.avi -b 4000k -minrate 4000k -maxrate 4000k -bufsize 1835k out.m2v
  ```

- lmin、lmax、mblmin 和 mblmax 四个选项使用 'lambda' 单位，但可以用 QP2LAMBDA 常量轻松从 'q' 单位换算：

  ``` text
  ffmpeg -i src.ext -lmax 21*QP2LAMBDA dst.ext
  ```

# 另请参见

ffplay(1), ffprobe(1), ffmpeg-utils(1), ffmpeg-scaler(1), ffmpeg-resampler(1), ffmpeg-codecs(1), ffmpeg-bitstream-filters(1), ffmpeg-formats(1), ffmpeg-devices(1), ffmpeg-protocols(1), ffmpeg-filters(1)
