# 常见问题

## 为什么 FFmpeg 不支持功能 \[xyz\]？

因为还没有人承担这项任务。FFmpeg 的开发由各个开发者认为重要的任务驱动。如果某项功能对您很重要，实现它的最佳方式是自己承担这项任务，或资助一位开发者。

## FFmpeg 不支持编解码器 XXX。能否加入 Windows DLL 加载器来支持它？

不。Windows DLL 不可移植、臃肿且往往缓慢。此外 FFmpeg 力求原生支持所有编解码器，DLL 加载器无助于这一目标。

## 虽然该格式似乎受 ffmpeg 支持，我仍无法读取这个文件。

即便 ffmpeg 能读取该容器格式，也可能不支持其中的所有编解码器。请查阅 ffmpeg 文档中受支持的编解码器列表。

## Windows 支持哪些编解码器？

Windows 对 MPEG 等标准格式支持不佳，除非您安装了一些额外的编解码器。

下列视频编解码器在多数 Windows 系统上应当可用：

| Term | Description |
|----|----|
| `msmpeg4v2` | .avi/.asf |
| `msmpeg4` | 仅 .asf |
| `wmv1` | 仅 .asf |
| `wmv2` | 仅 .asf |
| `mpeg4` | 仅在安装了 ffdshow 或 Xvid 之类的 MPEG-4 编解码器时。 |
| `mpeg1video` | 仅 .mpg |

注意，ASF 文件在 Windows 上常带 .wmv 或 .wma 扩展名。还应指出，Microsoft 声称对 ASF 格式持有专利，并可能起诉或威胁起诉使用非 Microsoft 软件创建 ASF 文件的用户。强烈建议尽可能避免 ASF。

下列音频编解码器在多数 Windows 系统上应当可用：

- **`adpcm_ima_wav`**

- **`adpcm_ms`**

- **`pcm_s16le`** 始终可用

- **`libmp3lame`** 若安装了 LAME 之类的 MP3 编解码器则可用。

# 编译

## `error: can't find a register in class 'GENERAL_REGS' while reloading 'asm'`

这是 gcc 的缺陷，请勿向我们报告，而应报告给 gcc 开发者。注意我们不会为 gcc 的缺陷添加变通方案。

另请注意，部分 gcc 开发者认为这不是缺陷，或不是他们应当修复的缺陷：<https://gcc.gnu.org/bugzilla/show_bug.cgi?id=11203>。话说回来，他们中有些人也分不清不可判定问题与 NP 难问题……

## 我已用发行版的包管理器安装了该库，为什么 `configure` 找不到它？

发行版通常把库拆分为多个包。主包包含运行使用该库的程序所需的文件；开发包包含构建使用该库的程序所需的文件；有时文档和/或数据也会放在单独的包中。

要构建 FFmpeg，您需要安装开发包，它通常名为 `libfoo-dev` 或 `libfoo-devel`。构建完成后可以移除它，但请务必保留主包。

## 如何让 `pkg-config` 找到我的库？

在您的库文件所在位置的某处，有一个（或几个）位于 `pkgconfig` 目录中的 `.pc` 文件。您需要设置环境变量，让 `pkg-config` 指向这些文件。

如果您需要*添加*目录到 `pkg-config` 的搜索列表（典型场景：库被单独安装），将其加入 `$PKG_CONFIG_PATH`：

``` text
export PKG_CONFIG_PATH=/opt/x264/lib/pkgconfig:/opt/opus/lib/pkgconfig
```

如果您需要*替换* `pkg-config` 的搜索列表（典型场景：交叉编译），改在 `$PKG_CONFIG_LIBDIR` 中设置：

``` text
export PKG_CONFIG_LIBDIR=/home/me/cross/usr/lib/pkgconfig:/home/me/cross/usr/local/lib/pkgconfig
```

如果您需要了解库的内部依赖（典型用途：静态链接），给 `pkg-config` 加上 `--static` 选项：

``` text
./configure --pkg-config-flags=--static
```

## 交叉编译时如何使用 `pkg-config`？

最佳做法是在您的交叉编译环境中安装 `pkg-config`，它会自动使用交叉编译的库。

您也可以显式向 `configure` 指定 `--pkg-config=pkg-config`，从而使用宿主环境的 `pkg-config`。这种情况下，您必须按上一条的说明用 `PKG_CONFIG_LIBDIR` 把 `pkg-config` 指向正确的目录。

作为折中方案，您可以在交叉编译环境中放置一个调用宿主 `pkg-config`（已设置 `PKG_CONFIG_LIBDIR`）的脚本。该脚本可以长这样：

``` shell
#!/bin/sh
PKG_CONFIG_LIBDIR=/path/to/cross/lib/pkgconfig
export PKG_CONFIG_LIBDIR
exec /usr/bin/pkg-config "$@"
```

# 用法

## ffmpeg 无法工作，哪里出了问题？

在构建之前，先在 ffmpeg 源码目录中尝试 `make distclean`。如果无效，参见 (<https://ffmpeg.org/bugreports.html>)。

## 如何把单张图片编码成影片？

首先，将您的图片按数字顺序重命名，例如 img1.jpg、img2.jpg、img3.jpg……然后运行：

``` text
ffmpeg -f image2 -i img%d.jpg /tmp/a.mpg
```

注意 `%d` 会被替换为图片编号。

`img%03d.jpg` 表示序列 `img001.jpg`、`img002.jpg` 等。

使用 `-start_number` 选项声明序列的起始编号。如果您的序列不是从 `img001.jpg` 开始但仍按数字顺序排列，这会很有用。下面的示例将从 `img100.jpg` 开始：

``` text
ffmpeg -f image2 -start_number 100 -i img%d.jpg /tmp/a.mpg
```

如果您有大量图片需要重命名，可以用以下命令减轻负担。该命令使用 bourne shell 语法，把当前目录中所有匹配 `*jpg` 的文件符号链接到 `/tmp` 目录，按 `img001.jpg`、`img002.jpg` 等顺序命名。

``` c
x=1; for i in *jpg; do counter=$(printf %03d $x); ln -s "$i" /tmp/img"$counter".jpg; x=$(($x+1)); done
```

如果您想按最旧修改时间优先排序，把 `$(ls -r -t *jpg)` 替换 `*jpg` 的位置即可。

然后运行：

``` text
ffmpeg -f image2 -i /tmp/img%03d.jpg /tmp/a.mpg
```

同样的逻辑适用于 ffmpeg 读取的任何图像格式。

您也可以用 `cat` 把图片通过管道送入 ffmpeg：

``` text
cat *.jpg | ffmpeg -f image2pipe -c:v mjpeg -i - output.mpg
```

## 如何把影片编码为单张图片？

使用：

``` text
ffmpeg -i movie.mpg movie%d.jpg
```

作为输入的 `movie.mpg` 将被转换为 `movie1.jpg`、`movie2.jpg` 等。

除了依赖文件格式自动识别之外，您也可以使用

- **`-c:v ppm`**

- **`-c:v png`**

- **`-c:v mjpeg`**

来强制指定编码器。

把该方案应用于上一个示例：

``` text
ffmpeg -i movie.mpg -f image2 -c:v mjpeg menu%d.jpg
```

注意并不存在 "jpeg" 编解码器，请改用 "mjpeg"。

## 为什么多线程 MPEG\* 编码会出现轻微画质下降？

对于多线程 MPEG\* 编码，已编码的小片（slice）必须相互独立，否则线程 n 实际上必须等待线程 n-1 完成，因此出现少量质量下降是合理的。这不是缺陷。

## 如何从标准输入读取或写入标准输出？

用 `-` 作为文件名。

## -f jpeg 不起作用。

试试 '-f image2 test%d.jpg'。

## 为什么无法更改帧率？

某些编解码器（如 MPEG-1/2）只允许少量固定的帧率。请用 -c:v 命令行选项选择其他编解码器。

## 如何用 ffmpeg 编码 Xvid 或 DivX 视频？

Xvid 与 DivX（4+ 版）都是 ISO MPEG-4 标准的实现（注意还有许多其他使用同一标准的编码格式）。因此，请用 '-c:v mpeg4' 编码这些格式。编码到 MPEG-4 文件时默认存储的 fourcc 为 'FMP4'。如果想要不同的 fourcc，请使用 '-vtag' 选项。例如，'-vtag xvid' 会强制把 fourcc 'xvid' 存储为视频 fourcc，而非默认值。

## 编码高质量 MPEG-4 有哪些好的参数？

'-mbd rd -flags +mv4+aic -trellis 2 -cmp 2 -subcmp 2 -g 300 -pass 1/2'，可以尝试的还有：'-bf 2'、'-mpv_flags qp_rd'、'-mpv_flags mv0'、'-mpv_flags skip_rd'。

## 编码高质量 MPEG-1/MPEG-2 有哪些好的参数？

'-mbd rd -trellis 2 -cmp 2 -subcmp 2 -g 100 -pass 1/2'，但注意 '-g 100' 可能会给某些解码器带来问题。可以尝试的还有：'-bf 2'、'-mpv_flags qp_rd'、'-mpv_flags mv0'、'-mpv_flags skip_rd'。

## 隔行视频经 ffmpeg 编码后效果很差，问题出在哪里？

对隔行素材应使用 '-flags +ilme+ildct'，或许还可加 '-flags +alt'；如果结果实在一团糟，再试试 '-top 0/1'。

## 如何读取 DirectShow 文件？

如果您在构建 FFmpeg 时带了 `./configure --enable-avisynth`（仅在 MinGW/Cygwin 平台上可行），那么 DirectShow 能读取的任何文件都可以作为输入。

只需创建一个只含下面这一行的 "input.avs" 文本文件……

``` text
DirectShowSource("C:\path to your file\yourfile.asf")
```

……然后把该文本文件喂给 ffmpeg：

``` text
ffmpeg -i input.avs
```

有关 AviSynth 的其他任何帮助，请访问 [AviSynth 主页](http://www.avisynth.org/)。

## 如何合并视频文件？

"合并"视频文件的含义相当模糊。下面列出各种"合并"的类型及其在 FFmpeg 中的处理方式。合并视频文件可能是指：

- 把它们首尾相接放在一起：这称为*拼接*（concatenate，简称 concat），[本 FAQ 中](#如何拼接视频文件)对此有专门说明。

- 把它们放进同一个文件，让用户可以在不同版本之间选择（示例：不同语言的音频）：这称为把它们*复用*在一起（multiplex，简称 mux），只需在调用 ffmpeg 时给出多个 `-i` 选项即可完成。

- 对于音频，把所有声道合到一条流中（示例：两条单声道流合成一条立体声流）：这有时称为*合并*（merge），可以用 [`amerge`](../filters/overview.md#amerge) 滤镜完成。

- 对于音频，让它们叠在一起播放：这称为*混音*（mix），可以先合并成单条流，再用 [`pan`](../filters/overview.md#pan) 滤镜按需混合各声道。

- 对于视频，把两者一起显示，或并排，或叠放于另一画面之上；可以用 [`overlay`](../filters/overview.md#overlay) 视频滤镜完成。

## 如何拼接视频文件？

有多种解决方案，取决于具体情况。

### 使用 concat *滤镜* 拼接

FFmpeg 有一个专为该用途设计的 [`concat`](../filters/overview.md#concat) 滤镜，文档中附有示例。如果您需要重新编码，推荐此操作。

### 使用 concat *解复用器* 拼接

FFmpeg 有一个 [`concat`](../components/formats.md#concat) 解复用器，当您想避免重新编码、且所用格式不支持文件级拼接时可以使用它。

### 使用 concat *协议* 拼接（文件级）

FFmpeg 有一个专为该用途设计的 [`concat`](../components/protocols.md#concat) 协议，文档中附有示例。

少数多媒体容器（MPEG-1、MPEG-2 PS、DV）允许仅通过拼接文件本身来拼接视频。

因此，您可以先把多媒体文件转码到这些特权格式，然后用朴素的 `cat` 命令（或 Windows 下同样朴素的 `copy`）把它们拼在一起，最后再转码回您选定的格式。

``` text
ffmpeg -i input1.avi -qscale:v 1 intermediate1.mpg
ffmpeg -i input2.avi -qscale:v 1 intermediate2.mpg
cat intermediate1.mpg intermediate2.mpg > intermediate_all.mpg
ffmpeg -i intermediate_all.mpg -qscale:v 2 output.avi
```

此外，您可以改用 `concat` 协议替代 `cat` 或 `copy`，从而避免生成可能非常庞大的中间文件。

``` text
ffmpeg -i input1.avi -qscale:v 1 intermediate1.mpg
ffmpeg -i input2.avi -qscale:v 1 intermediate2.mpg
ffmpeg -i concat:"intermediate1.mpg|intermediate2.mpg" -c copy intermediate_all.mpg
ffmpeg -i intermediate_all.mpg -qscale:v 2 output.avi
```

注意，您可能需要转义字符 "\|"，它对许多 shell 而言是特殊字符。

另一个选择是使用命名管道（named pipe），如果您的平台支持的话：

``` text
mkfifo intermediate1.mpg
mkfifo intermediate2.mpg
ffmpeg -i input1.avi -qscale:v 1 -y intermediate1.mpg < /dev/null &
ffmpeg -i input2.avi -qscale:v 1 -y intermediate2.mpg < /dev/null &
cat intermediate1.mpg intermediate2.mpg |\
ffmpeg -f mpeg -i - -c:v mpeg4 -c:a libmp3lame output.avi
```

### 使用裸音频与裸视频拼接

类似地，yuv4mpegpipe 格式与裸视频、裸音频编解码器也支持拼接，且转码步骤几乎无损。使用多条 yuv4mpegpipe 时，除第一条流外，其余每条流都需要丢弃首行。这可以像下文那样通过 `tail` 管道完成。注意，通过 `tail` 管道时必须使用命令分组 `{ ;}`，才能正确转入后台。

例如，假设我们要把两个 FLV 文件拼接成一个 output.flv 文件：

``` text
mkfifo temp1.a
mkfifo temp1.v
mkfifo temp2.a
mkfifo temp2.v
mkfifo all.a
mkfifo all.v
ffmpeg -i input1.flv -vn -f u16le -c:a pcm_s16le -ac 2 -ar 44100 - > temp1.a < /dev/null &
ffmpeg -i input2.flv -vn -f u16le -c:a pcm_s16le -ac 2 -ar 44100 - > temp2.a < /dev/null &
ffmpeg -i input1.flv -an -f yuv4mpegpipe - > temp1.v < /dev/null &
{ ffmpeg -i input2.flv -an -f yuv4mpegpipe - < /dev/null | tail -n +2 > temp2.v ; } &
cat temp1.a temp2.a > all.a &
cat temp1.v temp2.v > all.v &
ffmpeg -f u16le -c:a pcm_s16le -ac 2 -ar 44100 -i all.a \
       -f yuv4mpegpipe -i all.v \
       -y output.flv
rm temp[12].[av] all.[av]
```

## 使用 `-f lavfi` 时音频无缘无故变成单声道。

使用 `-dumpgraph -` 找出声道布局到底在哪里丢失。

最可能是在 `auto-inserted aresample` 处。请设法弄清楚为什么在那个位置需要这个转换滤镜。

输出之前是最可能的位置，因为 `-f lavfi` 目前只支持打包 S16。

然后在滤镜链图中显式插入正确的 `aformat`，指明确切的格式。

``` text
aformat=sample_fmts=s16:channel_layouts=stereo
```

## 为什么 FFmpeg 看不到我的 VOB 文件中的字幕？

VOB 与其他少数格式没有描述文件全部内容的全局头。应用程序应当扫描文件以查明其中有什么。由于 VOB 文件通常很大，只扫描开头部分。如果字幕恰好出现在文件靠后位置，就不会被初始扫描检测到。

包括 `ffmpeg` 命令行工具在内的一些应用程序只能处理初始扫描期间检测到的流；较晚检测到的流会被忽略。

初始扫描的大小由两个选项控制：`probesize`（默认约 5 Mo）和 `analyzeduration`（默认 5,000,000 µs = 5 秒）。要检测到字幕流，两个值都必须足够大。

## 为什么移除了 `ffmpeg` 的 `-sameq` 选项？应该用什么替代？

`-sameq` 选项意为"同一量化器"（same quantizer），只在非常有限的场景下才有意义。遗憾的是，很多人误以为它是"同质量"（same quality），在不适用的场合使用它：它产生的可见效果大致符合预期，但实现方式非常低效。

每个编码器都有自己的一组选项来设定质量与体积的平衡，请使用您所用编码器的选项，把质量调到符合您口味的水平。最常见的选项是 `-qscale` 与 `-qmax`，但您应当细读所选编码器的文档。

## 我有一个被拉伸的视频，为什么缩放修不好它？

大量视频编解码器和格式都能存储视频的*宽高比*：即整幅图像（DAR，显示宽高比）或单个像素（SAR，采样宽高比）的宽高之比。例如，640×350 分辨率的 EGA 屏幕具有 4:3 的 DAR 和 35:48 的 SAR。

多数静态图像处理都基于方形像素，即 1:1 SAR，但许多视频标准（尤其是模拟-数字过渡时代的标准）使用非方形像素。

FFmpeg 中多数处理滤镜都会处理宽高比，以避免拉伸图像：裁剪调整 DAR 以保持 SAR 不变，缩放调整 SAR 以保持 DAR 不变。

如果您想拉伸（或"反向拉伸"）图像，需要用 [`setdar or setsar filters`](../filters/overview.md#setdar_002c-setsar)覆盖该信息。

不要忘记仔细检查原始视频，确认拉伸究竟是来自图像本身，还是来自宽高比信息。

例如，要修复一段编码不良的 EGA 采集，可使用以下命令：第一条把分辨率放大到方形像素，第二条设置正确的宽高比，第三条避免转码（能否奏效视格式/编解码器/播放器/月相而定）。

``` text
ffmpeg -i ega_screen.nut -vf scale=640:480,setsar=1 ega_screen_scaled.nut
ffmpeg -i ega_screen.nut -vf setdar=4/3 ega_screen_anamorphic.nut
ffmpeg -i ega_screen.nut -aspect 4/3 -c copy ega_screen_overridden.nut
```

## 如何将 ffmpeg 作为后台任务运行？

ffmpeg 在执行操作时通常会检查控制台输入，例如检查是否有 "q"（停止）与 "?"（求助）等输入。ffmpeg 无法检测自己是否在作为后台任务运行。当它检查控制台输入时，可能导致后台运行 ffmpeg 的进程被挂起。

要阻止这些输入检查、让 ffmpeg 得以作为后台任务运行，请在调用 ffmpeg 时使用 [`-nostdin` 选项](../manual/ffmpeg.md#stdin-option)。无论您是在 shell 中运行 ffmpeg，还是经操作系统 API 在独立进程中调用 ffmpeg，这都有效。

或者，当您在 shell 中运行 ffmpeg 时，可以把标准输入重定向到 `/dev/null`（Linux 与 macOS）或 `NUL`（Windows）。重定向既可以放在 ffmpeg 调用上，也可以放在调用 ffmpeg 的 shell 脚本中。

例如：

``` text
ffmpeg -nostdin -i INPUT OUTPUT
```

或（在 Linux、macOS 及其他类 UNIX shell 中）：

``` text
ffmpeg -i INPUT OUTPUT </dev/null
```

或（在 Windows 上）：

``` text
ffmpeg -i INPUT OUTPUT <NUL
```

## 如何避免 ffmpeg 因 *suspended (tty output)* 消息而挂起？

如果您在后台运行 ffmpeg，可能会发现其进程被挂起，并可能出现 *suspended (tty output)* 之类的消息。问题在于如何防止进程被挂起。

例如：

``` text
% ffmpeg -i INPUT OUTPUT &> ~/tmp/log.txt &
[1] 93352
%
[1]  + suspended (tty output)  ffmpeg -i INPUT OUTPUT &>
```

尽管消息写着 "tty output"，这里真正的问题在于 ffmpeg 运行时通常会检查控制台输入。操作系统检测到这一点后，会挂起进程，直到您把它带到前台处理。

解决办法是用正确的手法告诉 ffmpeg 不要读取控制台输入。您可以使用 [`-nostdin` 选项](../manual/ffmpeg.md#stdin-option)，或用 `< /dev/null` 重定向标准输入。详情参见 FAQ [*如何将 ffmpeg 作为后台任务运行？*](#如何将-ffmpeg-作为后台任务运行)。

# 开发

## 有没有展示如何使用 FFmpeg 库（尤其是 libavcodec 和 libavformat）的示例？

有。请查看源码仓库中的 `doc/examples` 目录，线上也可访问：<https://github.com/FFmpeg/FFmpeg/tree/master/doc/examples>。

示例也会随默认安装装入，通常位于 `$PREFIX/share/ffmpeg/examples`。

您也可以阅读 FFmpeg 文档中的《开发者指南》。或者，研究众多已集成 FFmpeg 的开源项目之一的源码（列表见 [projects.html](https://ffmpeg.org/projects.html)）。

## 你们能支持我的 C 编译器 XXX 吗？

视情况而定。如果您的编译器符合 C99，那么支持它的补丁很可能会受到欢迎，前提是它们不会用与该编译器相关的 `#ifdef` 污染源码。

## 支持 Microsoft Visual C++ 吗？

有。请参见 FFmpeg 文档的 [Microsoft Visual C++](platform.md) 小节。

## 能否添加 automake、libtool 或 autoconf 支持？

不。这些工具过于臃肿，只会让构建复杂化。

## 为什么不用面向对象的 C++ 重写 FFmpeg？

FFmpeg 已经以高度模块化的方式组织，无需用正式的对象语言重写。此外，许多开发者偏爱纯 C，它对他们很有效。关于此话题的更多论点，请读 ["Programming Religion"](https://web.archive.org/web/20111004021423/http://kernel.org/pub/linux/docs/lkml/#s15)。

## 为什么 ffmpeg 可执行程序不带调试符号？

构建过程会生成 `ffmpeg_g`、`ffplay_g` 等，它们包含完整的调试信息。这些二进制文件随后会被剥离（strip）以生成 `ffmpeg`、`ffplay` 等。如果需要调试信息，请使用 \*\_g 版本。

## 我不喜欢 LGPL，可以改以 GPL 贡献代码吗？

可以，只要这些代码是可选的，并且能够干净利落地放进 \#if CONFIG_GPL 而不破坏任何东西。例如，新的编解码器或滤镜以 GPL 发布没有问题，而对 LGPL 代码的缺陷修复则不行。

## 我在 C 应用程序中使用 FFmpeg，但链接器报错缺少库本身的符号。

FFmpeg 默认构建静态库。静态库不处理依赖关系。这带来两个后果。第一，必须按依赖顺序指定库：`-lavdevice` 必须排在 `-lavformat` 之前，`-lavutil` 必须排在所有其他库之后，等等。第二，FFmpeg 用到的外部库也必须一并列出。

获取按依赖顺序排列的所需库完整列表的简易方法是使用 `pkg-config`。

``` text
c99 -o program program.c $(pkg-config --cflags --libs libavformat libavcodec)
```

更多细节参见 `doc/example/Makefile` 与 `doc/example/pc-uninstalled`。

## 我在 C++ 应用程序中使用 FFmpeg，但链接器报错缺少看似明明可用的符号。

FFmpeg 是纯 C 项目，因此要在 C++ 应用程序中使用这些库，您需要显式声明自己使用的是 C 库。做法是用 `extern "C"` 包住对 FFmpeg 头文件的包含。

参见 <http://www.parashift.com/c++-faq-lite/mixing-c-and-cpp.html#faq-32.3>

## 我在 C++ 应用程序中使用 libavutil，但编译器报错 'UINT64_C' was not declared in this scope

FFmpeg 是使用 C99 数学特性的纯 C 项目，要让 C++ 使用这些特性，您必须在 CXXFLAGS 中追加 -D\_\_STDC_CONSTANT_MACROS。

## 我的文件在内存中或 API 不同于 \*open/\*read/libc，如何在 libavformat 中使用它？

您需要用 `avio_alloc_context` 创建自定义 AVIOContext，参见 FFmpeg 中的 `libavformat/aviobuf.c`，以及 MPlayer 或 MPlayer2 源码中的 `libmpdemux/demux_lavf.c`。

## 关于 ffv1、msmpeg4、asv1、4xm 的文档在哪里？

参见 <https://www.ffmpeg.org/~michael/>

## 如何将 H.263-RTP（及其他 RTP 中的编解码器）送入 libavcodec？

虽然它因面向网络而显得特殊，RTP 其实与其他任何容器一样。您必须先*解复用* RTP，再把载荷送入 libavcodec。这个具体案例请查阅 RFC 4629 了解应当怎么做。

## AVStream.r_frame_rate 不对，它比帧率大得多。

`r_frame_rate` 不是平均帧率，而是能够精确表示所有时间戳的最小帧率。所以不，它大于平均值并没有错！例如，若内容混合了 25 和 30 fps，则 `r_frame_rate` 将为 150（最小公倍数）。如果您要找的是平均帧率，参见 `AVStream.avg_frame_rate`。

## 为什么 `make fate` 没有运行全部测试？

请确认您已备好 fate-suite 样本，且 `SAMPLES` Make 变量、`FATE_SAMPLES` 环境变量或 `--samples` `configure` 选项已设置为正确路径。

## 为什么 `make fate` 找不到测试样本？

您是不是在样本路径中用了 `~` 字符表示家目录？该值会在 shell 无法展开它的场景中使用，导致 FATE 找不到文件。把 `~` 换成完整路径即可。
