# 外部库

FFmpeg 可以挂接多种外部库以增加对更多格式的支持。它们默认都不会被使用，必须通过向 `./configure` 传入相应的标志来显式请求使用。

## Alliance for Open Media (AOM)

FFmpeg 可利用 AOM 库进行 AV1 解码与编码。

前往 <http://aomedia.org/> 并按说明安装该库。然后向 configure 传入 `--enable-libaom` 以启用它。

## AMD AMF/VCE

FFmpeg 可利用 AMD Advanced Media Framework 库，在带 Video Coding Engine (VCE) 的硬件上进行加速 H.264 与 HEVC 编码（仅限 Windows）。

要启用支持，您必须从 <https://github.com/GPUOpen-LibrariesAndSDKs/AMF.git> 获取 AMF 框架头文件（1.4.9+ 版）。

在系统头文件包含路径中创建一个 `AMF/` 目录，把 `AMF/amf/public/include/` 的内容复制到该目录。然后用 `--enable-amf` 配置 FFmpeg。

amf 编码器的初始化按以下顺序尝试：1) 尝试经 dx11 初始化（仅限 Windows）2) 尝试经 dx9 初始化（仅限 Windows）3) 尝试经 vulkan 初始化

要在 linux 上使用 h.264（AMD VCE）编码器，需要 amdgru-pro 19.20+ 版以及 amf-amdgpu-pro 包（amdgru-pro 中包含，但不会自动安装）。

该驱动可以用官方 AMD 驱动包中的 amdgpu-pro-install 脚本安装。

## AviSynth

FFmpeg 可以读取 AviSynth 脚本作为输入。要启用支持，请在安装 [AviSynth+](https://github.com/AviSynth/AviSynthPlus) 提供的头文件后，向 configure 传入 `--enable-avisynth`。AviSynth+ 可以配置为仅安装头文件：既可在常规的 CMake 构建系统中传入 `-DHEADERS_ONLY:bool=on`，也可使用其提供的 `GNUmakefile`。

对 Windows，受支持的 AviSynth 变体是 [AviSynth 2.6 RC1 或更高版本](http://avisynth.nl)（32 位构建）以及 [AviSynth+ r1718 或更高版本](http://avisynth.nl/index.php/AviSynth+)（32 位与 64 位构建）。

对 Linux、macOS 与 BSD，唯一受支持的 AviSynth 变体是 [AviSynth+](https://github.com/AviSynth/AviSynthPlus)，自 3.5 版起。

2016 年，AviSynth+ 增加了对 GCC 构建的支持。然而，由于 Windows 调用约定的特殊性，AviSynth+ 的 32 位 GCC 构建与典型的 32 位 FFmpeg 构建不兼容。

默认情况下，FFmpeg 假定与 AviSynth+ 的 32 位 MSVC 构建兼容，因为这是使用最广、根基最深的构建配置。用户可以改变这一点：在配置 FFmpeg 时向 `--extra-cflags` 传入 `-DAVSC_WIN32_GCC32`，以启用对 AviSynth+ 32 位 GCC 构建的支持。

64 位构建的 FFmpeg 不受影响，无需任何特殊标志即可使用 MSVC 或 GCC 构建的 AviSynth+。

AviSynth(+) 是动态加载的。发行打包者可以让 FFmpeg 以 `--enable-avisynth` 构建，此时即便最终用户没有安装 AviSynth，二进制文件也能正常工作。当最终用户想使用 AviSynth 脚本时，安装 AviSynth(+) 后 FFmpeg 即可找到并使用它来打开脚本。

## Chromaprint

FFmpeg 可利用 Chromaprint 库生成音频指纹。向 configure 传入 `--enable-chromaprint` 以启用它。参见 <https://acoustid.org/chromaprint>。

## codec2

FFmpeg 可利用 codec2 库进行 codec2 解码与编码。目前尚无原生解码器，因此解码必须使用 libcodec2。

前往 <http://freedv.org/>，下载 "Codec 2 source archive"。使用 CMake 构建并安装。Debian 用户也可以改为安装 libcodec2-dev 包。libcodec2 安装好后，向 configure 传入 `--enable-libcodec2` 以启用它。

使用 codec2 最简单的方式是通过 .c2 文件，其中含有解码所需的模式信息。要编码此类文件，请使用 .c2 扩展名并给 libcodec2 编码器 -mode 选项：`ffmpeg -i input.wav -mode 700C output.c2`。播放很简单：`ffplay output.c2`。要查看支持的模式列表，请运行 `ffmpeg -h encoder=libcodec2`。裸 codec2 文件也受支持；要正确解析它们，需要以格式选项的形式指定所用模式：`ffmpeg -f codec2raw -mode 1300 -i input.raw output.wav`。

## dav1d

FFmpeg 可利用 dav1d 库进行 AV1 视频解码。

前往 <https://code.videolan.org/videolan/dav1d> 并按说明安装该库。然后向 configure 传入 `--enable-libdav1d` 以启用它。

## davs2

FFmpeg 可利用 davs2 库进行 AVS2-P2/IEEE1857.4 视频解码。

前往 <https://github.com/pkuvcl/davs2> 并按说明安装该库。然后向 configure 传入 `--enable-libdavs2` 以启用它。

libdavs2 采用 GNU 通用公共许可证第 2 版或更高版本（详情参见 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>），使用它必须把 FFmpeg 的许可升级为 GPL。

## uavs3d

FFmpeg 可利用 uavs3d 库进行 AVS3-P2/IEEE1857.10 视频解码。

前往 <https://github.com/uavs3/uavs3d> 并按说明安装该库。然后向 configure 传入 `--enable-libuavs3d` 以启用它。

## Game Music Emu

FFmpeg 可利用 Game Music Emu 库读取受支持的游戏音乐文件格式中的音频。向 configure 传入 `--enable-libgme` 以启用它。参见 <https://bitbucket.org/mpyne/game-music-emu/overview>。

## Intel QuickSync Video

FFmpeg 可利用 Intel QuickSync Video (QSV) 对多种编解码器进行加速解码与编码。要使用 QSV，FFmpeg 必须链接 `libmfx` 分发器（dispatcher），由它加载实际的解码库。

该分发器是开源的，可从 <https://github.com/lu-zero/mfx_dispatch.git> 下载。FFmpeg 需要以 `--enable-libmfx` 选项配置，且 `pkg-config` 需要能定位分发器的 `.pc` 文件。

## Kvazaar

FFmpeg 可利用 Kvazaar 库进行 HEVC 编码。

前往 <https://github.com/ultravideo/kvazaar> 并按说明安装该库。然后向 configure 传入 `--enable-libkvazaar` 以启用它。

## LAME

FFmpeg 可利用 LAME 库进行 MP3 编码。

前往 <http://lame.sourceforge.net/> 并按说明安装该库。然后向 configure 传入 `--enable-libmp3lame` 以启用它。

## LCEVCdec

FFmpeg 可利用 liblcevc_dec 库在受支持的比特流上解码 LCEVC 增强层。

前往 <https://github.com/v-novaltd/LCEVCdec> 并按说明安装该库。然后向 configure 传入 `--enable-liblcevc-dec` 以启用它。

LCEVCdec 采用 BSD-3-Clause-Clear 许可证。

## libilbc

iLBC 是 Google 作为 WebRTC 项目的一部分而自由开放的一款窄带语音编解码器。libilbc 是对 iLBC 编解码器的一种便于打包的副本。FFmpeg 可利用 libilbc 库进行 iLBC 解码与编码。

前往 <https://github.com/TimothyGu/libilbc> 并按说明安装该库。然后向 configure 传入 `--enable-libilbc` 以启用它。

## libjxl

JPEG XL 是一种意在长期内完全取代传统 JPEG 的图像格式。更多信息参见 <https://jpegxl.info/>，库源码参见 <https://github.com/libjxl/libjxl>。您可以向 configure 传入 `--enable-libjxl` 以启用 libjxl 封装器。

## libvpx

FFmpeg 可利用 libvpx 库进行 VP8/VP9 解码与编码。

前往 <http://www.webmproject.org/> 并按说明安装该库。然后向 configure 传入 `--enable-libvpx` 以启用它。

## ModPlug

FFmpeg 可利用这款源自 Modplug-XMMS 的库读取 MOD 类音乐文件。参见 <https://github.com/Konstanty/libmodplug>。向 configure 传入 `--enable-libmodplug` 以启用它。

## ONNX Runtime

FFmpeg 可利用 ONNX Runtime 库作为基于 DNN 的滤镜的后端。

前往 <https://onnxruntime.ai/> 并按说明安装该库。针对各种平台都有预构建包可用。

配置 FFmpeg 以支持 ONNX Runtime：

``` text
./configure \
    --enable-libonnxruntime \
    --extra-cflags="-I/path/to/onnxruntime/include" \
    --extra-ldflags="-L/path/to/onnxruntime/lib"
```

在基于 ELF 的系统（Linux、BSD）上，您可能还想嵌入库搜索路径，使安装的 `ffmpeg` 二进制文件在运行时无需设置 `LD_LIBRARY_PATH` 即可找到共享库：

``` text
./configure \
    --enable-libonnxruntime \
    --extra-cflags="-I/path/to/onnxruntime/include" \
    --extra-ldflags="-L/path/to/onnxruntime/lib -Wl,-rpath,/path/to/onnxruntime/lib"
```

`-Wl,-rpath` 标志是 ELF 特有的，在其他平台（Windows、macOS）上应省略。

对 MinGW GCC 构建，为兼容 ONNX Runtime 头文件，请添加 `-D_stdcall=__stdcall` 标志。

## OpenCORE、VisualOn 与 Fraunhofer 库

这些库从 Google Android 源码分离而来，为多种音频编解码器提供编码器。

OpenCORE 与 VisualOn 库采用 Apache 许可证 2.0（详情参见 <http://www.apache.org/licenses/LICENSE-2.0>），与 LGPL 2.1 和 GPL 2 不兼容。您必须通过向 configure 传入 `--enable-version3` 把 FFmpeg 的许可升级为 LGPL 第 3 版（若已启用 GPL 组件则为 GPL 第 3 版）才能使用它。

Fraunhofer AAC 库的许可证与 GPL 不兼容。因此，对 GPL 构建，您必须向 configure 传入 `--enable-nonfree` 才能使用它。据我们所知，它与 LGPL 兼容。

### OpenCORE AMR

FFmpeg 可利用 OpenCORE 库进行 AMR-NB 解码/编码与 AMR-WB 解码。

前往 <http://sourceforge.net/projects/opencore-amr/> 并按说明安装这些库。然后向 configure 传入 `--enable-libopencore-amrnb` 和/或 `--enable-libopencore-amrwb` 以启用它们。

### VisualOn AMR-WB 编码器库

FFmpeg 可利用 VisualOn AMR-WBenc 库进行 AMR-WB 编码。

前往 <http://sourceforge.net/projects/opencore-amr/> 并按说明安装该库。然后向 configure 传入 `--enable-libvo-amrwbenc` 以启用它。

### Fraunhofer AAC 库

FFmpeg 可利用 Fraunhofer AAC 库进行 AAC 解码与编码。

前往 <http://sourceforge.net/projects/opencore-amr/> 并按说明安装该库。然后向 configure 传入 `--enable-libfdk-aac` 以启用它。

### Fraunhofer MPEG-H 3D Audio 解码器库

FFmpeg 可利用 Fraunhofer MPEG-H 解码器库进行 MPEG-H 3DA 解码。

前往 <https://github.com/Fraunhofer-IIS/mpeghdec> 并按说明安装该库。然后向 configure 传入 `--enable-libmpeghdec --enable-nonfree` 以启用它。

### LC3 库

FFmpeg 可利用 Google LC3 库进行 LC3 解码与编码。

前往 <https://github.com/google/liblc3/> 并按说明安装该库。然后向 configure 传入 `--enable-liblc3` 以启用它。

## OpenH264

FFmpeg 可利用 OpenH264 库进行 H.264 解码与编码。

前往 <http://www.openh264.org/> 并按说明安装该库。然后向 configure 传入 `--enable-libopenh264` 以启用它。

在解码方面，该库比 libavcodec 内置的解码器受限得多；目前它不支持解码 B 帧 (B-frames) 及其他一些 main/high profile 特性。（目前它仅支持 constrained baseline profile 与 CABAC。）使用它主要用于测试，以及利用 Cisco 的专利池许可 (<http://www.openh264.org/BINARY_LICENSE.txt>)。

## OpenJPEG

FFmpeg 可利用 OpenJPEG 库进行 J2K 视频的解码/编码。前往 <http://www.openjpeg.org/> 获取这些库并按说明安装。要在 FFmpeg 中启用 OpenJPEG，向 `./configure` 传入 `--enable-libopenjpeg`。

## rav1e

FFmpeg 可经其 C 绑定利用 rav1e（Rust AV1 编码器）编码视频。前往 <https://github.com/xiph/rav1e/> 并按说明构建 C 库。要在 FFmpeg 中启用 rav1e，向 `./configure` 传入 `--enable-librav1e`。

## SVT-AV1

FFmpeg 可利用 Scalable Video Technology for AV1 库进行 AV1 编码。

前往 <https://gitlab.com/AOMediaCodec/SVT-AV1/> 并按说明安装该库。然后向 configure 传入 `--enable-libsvtav1` 以启用它。

## SVT-JPEG-XS

FFmpeg 可利用 Scalable Video Technology for JPEG-XS 库进行 JPEG-XS 解码与编码。

前往 <https://github.com/OpenVisualCloud/SVT-JPEG-XS> 并按说明安装该库。然后向 configure 传入 `--enable-libsvtjpegxs` 以启用它。

## TwoLAME

FFmpeg 可利用 TwoLAME 库进行 MP2 编码。

前往 <http://www.twolame.org/> 并按说明安装该库。然后向 configure 传入 `--enable-libtwolame` 以启用它。

## VapourSynth

FFmpeg 可以读取 VapourSynth 脚本作为输入。要启用支持，向 configure 传入 `--enable-vapoursynth`。VapourSynth 经 `pkg-config` 检测。支持 42 或更高版本。参见 <http://www.vapoursynth.com/>。

出于安全考虑，VapourSynth 脚本不会被自动检测，因此必须强制指定输入格式。对 ff* CLI 工具，在输入 `-i yourscript.vpy` 之前添加 `-f vapoursynth`。

## x264

FFmpeg 可利用 x264 库进行 H.264 编码。

前往 <http://www.videolan.org/developers/x264.html> 并按说明安装该库。然后向 configure 传入 `--enable-libx264` 以启用它。

x264 采用 GNU 通用公共许可证第 2 版或更高版本（详情参见 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>），使用它必须把 FFmpeg 的许可升级为 GPL。

## x265

FFmpeg 可利用 x265 库进行 HEVC 编码。

前往 <http://x265.org/developers.html> 并按说明安装该库。然后向 configure 传入 `--enable-libx265` 以启用它。

x265 采用 GNU 通用公共许可证第 2 版或更高版本（详情参见 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>），使用它必须把 FFmpeg 的许可升级为 GPL。

## xavs

FFmpeg 可利用 xavs 库进行 AVS 编码。

前往 <http://xavs.sf.net/> 并按说明安装该库。然后向 configure 传入 `--enable-libxavs` 以启用它。

## xavs2

FFmpeg 可利用 xavs2 库进行 AVS2-P2/IEEE1857.4 视频编码。

前往 <https://github.com/pkuvcl/xavs2> 并按说明安装该库。然后向 configure 传入 `--enable-libxavs2` 以启用它。

libxavs2 采用 GNU 通用公共许可证第 2 版或更高版本（详情参见 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>），使用它必须把 FFmpeg 的许可升级为 GPL。

## eXtra-fast Essential Video Encoder (XEVE)

FFmpeg 可利用 XEVE 库进行 EVC 视频编码。

前往 <https://github.com/mpeg5/xeve> 并按说明安装 XEVE 库。然后向 configure 传入 `--enable-libxeve` 以启用它。

## eXtra-fast Essential Video Decoder (XEVD)

FFmpeg 可利用 XEVD 库进行 EVC 视频解码。

前往 <https://github.com/mpeg5/xevd> 并按说明安装 XEVD 库。然后向 configure 传入 `--enable-libxevd` 以启用它。

## ZVBI

ZVBI 是一款 VBI 解码库，FFmpeg 可用它解码 DVB 图文电视页面和 DVB 图文电视字幕。

前往 <http://sourceforge.net/projects/zapping/> 并按说明安装该库。然后向 configure 传入 `--enable-libzvbi` 以启用它。

# 支持的文件格式、编解码器或特性

您可以使用 `-formats` 与 `-codecs` 选项获取完整列表。

## 文件格式

FFmpeg 经由 `libavformat` 库支持以下文件格式：

|  |  |  |  |
|----|----|----|----|
| Name | Encoding | Decoding | Comments |
| 3dostr |  | X |  |
| 4xm |  | X | 4X Technologies 格式，用于某些游戏。 |
| 8088flex TMV |  | X |  |
| AAX |  | X | Audible Enhanced Audio 格式，用于有声书。 |
| AA |  | X | Audible Format 2、3 与 4，用于有声书。 |
| ACT Voice |  | X | 含 G.729 音频 |
| Adobe Filmstrip | X | X |  |
| Audio IFF (AIFF) | X | X |  |
| American Laser Games MM |  | X | 用于 Mad Dog McCree 等游戏的多媒体格式。 |
| 3GPP AMR | X | X |  |
| Amazing Studio Packed Animation File |  | X | 用于游戏 Heart Of Darkness 的多媒体格式。 |
| Apple HTTP Live Streaming |  | X |  |
| Artworx Data Format |  | X |  |
| Interplay ACM |  | X | 部分 Interplay 游戏使用的纯音频格式。 |
| ADP |  | X | Nintendo Gamecube 上使用的音频格式。 |
| AFC |  | X | Nintendo Gamecube 上使用的音频格式。 |
| ADS/SS2 |  | X | PS2 上使用的音频格式。 |
| APNG | X | X |  |
| ASF | X | X | Advanced / Active Streaming Format。 |
| AST | X | X | Nintendo Wii 上使用的音频格式。 |
| AVI | X | X |  |
| AviSynth |  | X |  |
| AVR |  | X | Mac 上使用的音频格式。 |
| AVS |  | X | Creature Shock 游戏使用的多媒体格式。 |
| Beam Software SIFF |  | X | Beam Software 部分游戏使用的音视频格式。 |
| Bethesda Softworks VID |  | X | 用于 Bethesda Softworks 的部分游戏。 |
| Binary text |  | X |  |
| Bink |  | X | 许多游戏使用的多媒体格式。 |
| Bink Audio |  | X | 部分游戏使用的纯音频多媒体格式。 |
| Bitmap Brothers JV |  | X | 用于 Z 与 Z95 游戏。 |
| BRP |  | X | Argonaut Games 格式。 |
| Brute Force & Ignorance |  | X | 用于游戏 Flash Traffic: City of Angels。 |
| BFSTM |  | X | Nintendo WiiU 上使用的音频格式（基于 BRSTM）。 |
| BRSTM |  | X | Nintendo Wii 上使用的音频格式。 |
| BW64 |  | X | Broadcast Wave 64bit。 |
| BWF | X | X |  |
| codec2 (raw) | X | X | 必须给定 -mode 格式选项才能正确解码。 |
| codec2 (.c2 files) | X | X | 含有版本与模式信息的头，简化播放。 |
| CRI ADX | X | X | 主机游戏使用的纯音频格式。 |
| CRI AIX |  | X |  |
| CRI HCA |  | X | 主机游戏使用的纯音频格式。 |
| Discworld II BMV |  | X |  |
| Interplay C93 |  | X | 用于 Interplay 的游戏 Cyberia。 |
| Delphine Software International CIN |  | X | Delphine Software 游戏使用的多媒体格式。 |
| Digital Speech Standard (DSS) |  | X |  |
| CD+G |  | X | CD+G 卡拉 OK 光盘使用的视频格式 |
| Phantom Cine |  | X |  |
| Commodore CDXL |  | X | Amiga CD 视频格式 |
| Core Audio Format | X | X | Apple Core Audio Format |
| CRC testing format | X |  |  |
| Creative Voice | X | X | 为 Sound Blaster Pro 而设计。 |
| CRYO APC |  | X | CRYO Interactive Entertainment 部分游戏使用的音频格式。 |
| D-Cinema audio | X | X |  |
| Deluxe Paint Animation |  | X |  |
| DCSTR |  | X |  |
| DFA |  | X | 该格式用于 Chronomaster 游戏 |
| DirectDraw Surface |  | X |  |
| DSD Stream File (DSF) |  | X |  |
| DV video | X | X |  |
| DXA |  | X | 该格式用于 Feeble Files 游戏的非 Windows 版本，以及为配合 ScummVM 重新打包的不同游戏过场动画。 |
| Electronic Arts cdata |  | X |  |
| Electronic Arts Multimedia |  | X | 用于多款 EA 游戏；文件扩展名如 WVE 和 UV2。 |
| Ensoniq Paris Audio File |  | X |  |
| FFM (FFserver live feed) | X | X |  |
| Flash (SWF) | X | X |  |
| Flash 9 (AVM2) | X | X | 仅解码内嵌音频。 |
| FLI/FLC/FLX animation |  | X | .fli/.flc 文件 |
| Flash Video (FLV) | X | X | Macromedia Flash 视频文件 |
| framecrc testing format | X |  |  |
| FunCom ISS |  | X | FunCom 的 The Longest Journey 等游戏使用的音频格式。 |
| G.723.1 | X | X |  |
| G.726 |  | X | 左对齐与右对齐均可。 |
| G.729 BIT | X | X |  |
| G.729 raw |  | X |  |
| GENH |  | X | 供各类游戏使用的音频格式。 |
| GIF Animation | X | X |  |
| GXF | X | X | 通用交换格式 SMPTE 360M，用于 Thomson Grass Valley 播出服务器。 |
| HNM |  | X | 仅支持第 4 版，用于 Cryo Interactive 的部分游戏 |
| iCEDraw File |  | X |  |
| ICO | X | X | Microsoft Windows ICO |
| id Quake II CIN video |  | X |  |
| id RoQ | X | X | 用于 Quake III、Jedi Knight 2 及其他电脑游戏。 |
| IEC61937 encapsulation | X | X |  |
| IFF |  | X | Interchange File Format |
| IFV |  | X | 一些老式 CCTV DVR 使用的格式。 |
| iLBC | X | X |  |
| Interplay MVE |  | X | 多款 Interplay 电脑游戏使用的格式。 |
| Iterated Systems ClearVideo |  | X | 仅 I 帧 (I-frames) |
| IV8 |  | X | IndigoVision 8000 视频服务器生成的格式。 |
| IVF (On2) | X | X | libvpx 使用的格式 |
| Internet Video Recording |  | X |  |
| IRCAM | X | X |  |
| LAF |  | X | Limitless Audio Format |
| LATM | X | X |  |
| LMLM4 |  | X | 用于 Linux Media Labs MPEG-4 PCI 板卡 |
| LOAS |  | X | 含经 LATM 复用的 AAC 音频 |
| LRC | X | X |  |
| LVF |  | X |  |
| LXF |  | X | VR 原生流格式，用于 Leitch/Harris 的视频服务器。 |
| Magic Lantern Video (MLV) |  | X |  |
| Matroska | X | X |  |
| Matroska audio | X |  |  |
| FFmpeg metadata | X | X | 文本格式的元数据。 |
| MAXIS XA |  | X | 用于 Sim City 3000；文件扩展名 .xa。 |
| MCA |  | X | 用于 Capcom 的部分游戏；文件扩展名 .mca。 |
| MD Studio |  | X |  |
| Metal Gear Solid: The Twin Snakes |  | X |  |
| Megalux Frame |  | X | Megalux Ultimate Paint 所用 |
| MobiClip MODS |  | X |  |
| MobiClip MOFLEX |  | X |  |
| Mobotix .mxg |  | X |  |
| Monkey's Audio |  | X |  |
| Motion Pixels MVI |  | X |  |
| MOV/QuickTime/MP4 | X | X | 支持 3GP、3GP2、PSP、iPod 变体 |
| MP2 | X | X |  |
| MP3 | X | X |  |
| MPEG-1 System | X | X | 音视频复用流，支持 VCD 格式 |
| MPEG-PS (program stream) | X | X | 亦称 `VOB` 文件，支持 SVCD 与 DVD 格式 |
| MPEG-TS (transport stream) | X | X | 亦称 DVB Transport Stream |
| MPEG-4 | X | X | MPEG-4 是 QuickTime 的一个变体。 |
| MSF |  | X | PS3 上使用的音频格式。 |
| Mirillis FIC video |  | X | 不渲染光标。 |
| MIDI Sample Dump Standard |  | X |  |
| MIME multipart JPEG | X |  |  |
| MSN TCP webcam |  | X | MSN Messenger 网络摄像头流使用。 |
| MTV |  | X |  |
| Musepack |  | X |  |
| Musepack SV8 |  | X |  |
| Material eXchange Format (MXF) | X | X | SMPTE 377M，用于数字影院与广播行业。 |
| Material eXchange Format (MXF), D-10 Mapping | X | X | SMPTE 386M，D-10/IMX 映射。 |
| NC camera feed |  | X | NC (AVIP NC4600) 摄像机流 |
| NIST SPeech HEader REsources |  | X |  |
| Computerized Speech Lab NSP |  | X |  |
| NTT TwinVQ (VQF) |  | X | Nippon Telegraph and Telephone Corporation 的 TwinVQ。 |
| Nullsoft Streaming Video |  | X |  |
| NuppelVideo |  | X |  |
| NUT | X | X | NUT 开放容器格式 |
| Ogg | X | X |  |
| Playstation Portable PMP |  | X |  |
| Portable Voice Format |  | X |  |
| RK Audio (RKA) |  | X |  |
| TechnoTrend PVA |  | X | 用于 TechnoTrend DVB PCI 板卡。 |
| QCP |  | X |  |
| raw ADTS (AAC) | X | X |  |
| raw AC-3 | X | X |  |
| raw AMR-NB |  | X |  |
| raw AMR-WB |  | X |  |
| raw APAC |  | X |  |
| raw APV | X | X |  |
| raw aptX | X | X |  |
| raw aptX HD | X | X |  |
| raw Bonk |  | X |  |
| raw Chinese AVS video | X | X |  |
| raw DFPWM | X | X |  |
| raw Dirac | X | X |  |
| raw DNxHD | X | X |  |
| raw DTS | X | X |  |
| raw DTS-HD |  | X |  |
| raw E-AC-3 | X | X |  |
| raw EVC | X | X |  |
| raw FLAC | X | X |  |
| raw G.728 |  | X |  |
| raw GSM |  | X |  |
| raw H.261 | X | X |  |
| raw H.263 | X | X |  |
| raw H.264 | X | X |  |
| raw HEVC | X | X |  |
| raw Ingenient MJPEG |  | X |  |
| raw MJPEG | X | X |  |
| raw MLP |  | X |  |
| raw MPEG |  | X |  |
| raw MPEG-1 |  | X |  |
| raw MPEG-2 |  | X |  |
| raw MPEG-4 | X | X |  |
| raw NULL | X |  |  |
| raw video | X | X |  |
| raw id RoQ | X |  |  |
| raw OBU | X | X |  |
| raw OSQ |  | X |  |
| raw SBC | X | X |  |
| raw Shorten |  | X |  |
| raw TAK |  | X |  |
| raw TrueHD | X | X |  |
| raw VC-1 | X | X |  |
| raw PCM A-law | X | X |  |
| raw PCM mu-law | X | X |  |
| raw PCM Archimedes VIDC | X | X |  |
| raw PCM signed 8 bit | X | X |  |
| raw PCM signed 16 bit big-endian | X | X |  |
| raw PCM signed 16 bit little-endian | X | X |  |
| raw PCM signed 24 bit big-endian | X | X |  |
| raw PCM signed 24 bit little-endian | X | X |  |
| raw PCM signed 32 bit big-endian | X | X |  |
| raw PCM signed 32 bit little-endian | X | X |  |
| raw PCM signed 64 bit big-endian | X | X |  |
| raw PCM signed 64 bit little-endian | X | X |  |
| raw PCM unsigned 8 bit | X | X |  |
| raw PCM unsigned 16 bit big-endian | X | X |  |
| raw PCM unsigned 16 bit little-endian | X | X |  |
| raw PCM unsigned 24 bit big-endian | X | X |  |
| raw PCM unsigned 24 bit little-endian | X | X |  |
| raw PCM unsigned 32 bit big-endian | X | X |  |
| raw PCM unsigned 32 bit little-endian | X | X |  |
| raw PCM 16.8 floating point little-endian |  | X |  |
| raw PCM 24.0 floating point little-endian |  | X |  |
| raw PCM floating-point 32 bit big-endian | X | X |  |
| raw PCM floating-point 32 bit little-endian | X | X |  |
| raw PCM floating-point 64 bit big-endian | X | X |  |
| raw PCM floating-point 64 bit little-endian | X | X |  |
| RDT |  | X |  |
| REDCODE R3D |  | X | RED Digital 摄像机使用的文件格式，含 JPEG 2000 帧与 PCM 音频。 |
| RealMedia | X | X |  |
| Redirector |  | X |  |
| RedSpark |  | X |  |
| Renderware TeXture Dictionary |  | X |  |
| Resolume DXV | X | X | 仅 DXT1（普通质量，无透明通道）纹理格式支持编码。 |
| RF64 |  | X |  |
| RL2 |  | X | Entertainment Software Partners 部分游戏使用的音视频格式。 |
| RPL/ARMovie |  | X |  |
| Lego Mindstorms RSO | X | X |  |
| RSD |  | X |  |
| RTMP | X | X | 输出通过向 RTMP 服务器发布流实现 |
| RTP | X | X |  |
| RTSP | X | X |  |
| Sample Dump eXchange |  | X |  |
| SAP | X | X |  |
| SBG |  | X |  |
| SDNS |  | X |  |
| SDP |  | X |  |
| SER |  | X |  |
| Digital Pictures SGA |  | X |  |
| Sega FILM/CPK | X | X | 用于多款 Sega Saturn 主机游戏。 |
| Silicon Graphics Movie |  | X |  |
| Sierra SOL |  | X | Sierra Online 游戏使用的 .sol 文件。 |
| Sierra VMD |  | X | 用于 Sierra CD-ROM 游戏。 |
| Smacker |  | X | 许多游戏使用的多媒体格式。 |
| SMJPEG | X | X | 用于某些 Loki 游戏移植版。 |
| SMPTE 337M encapsulation |  | X |  |
| Smush |  | X | 部分 LucasArts 游戏使用的多媒体格式。 |
| Sony OpenMG (OMA) | X | X | Sony Sonic Stage 与 Sony Vegas 使用的音频格式。 |
| Sony PlayStation STR |  | X |  |
| Sony Wave64 (W64) | X | X |  |
| SoX native format | X | X |  |
| SUN AU format | X | X |  |
| SUP raw PGS subtitles | X | X |  |
| SVAG |  | X | Konami PS2 游戏使用的音频格式。 |
| TDSC |  | X |  |
| Text files |  | X |  |
| THP |  | X | 用于 Nintendo GameCube。 |
| Tiertex Limited SEQ |  | X | DOS CD-ROM 版游戏 Flashback 使用的 Tiertex .seq 文件。 |
| True Audio | X | X |  |
| VAG |  | X | 多款 Sony PS2 游戏使用的音频格式。 |
| VC-1 test bitstream | X | X |  |
| Vidvox Hap | X | X |  |
| Vivo |  | X |  |
| VPK |  | X | Sony PS 游戏使用的音频格式。 |
| Marble WADY |  | X |  |
| WAV | X | X |  |
| Waveform Archiver |  | X |  |
| WavPack | X | X |  |
| WebM | X | X |  |
| Windows Televison (WTV) | X | X |  |
| Wing Commander III movie |  | X | Origin 的 Wing Commander III 电脑游戏使用的多媒体格式。 |
| Westwood Studios audio | X | X | Westwood Studios 游戏使用的多媒体格式。 |
| Westwood Studios VQA |  | X | Westwood Studios 游戏使用的多媒体格式。 |
| Wideband Single-bit Data (WSD) |  | X |  |
| WVE |  | X |  |
| Konami XMD |  | X |  |
| XMV |  | X | Xbox 游戏使用的 Microsoft 视频容器。 |
| XVAG |  | X | PS3 上使用的音频格式。 |
| xWMA |  | X | XAudio 2 使用的 Microsoft 音频容器。 |
| eXtended BINary text (XBIN) |  | X |  |
| YUV4MPEG pipe | X | X |  |
| Psygnosis YOP |  | X |  |

`X` 表示该列（编码 / 解码）所对应的特性受支持。

## 图像格式

FFmpeg 可读取和写入视频序列每一帧的图像。支持以下图像格式：

|  |  |  |  |
|----|----|----|----|
| Name | Encoding | Decoding | Comments |
| .Y.U.V | X | X | 每分量一个裸文件 |
| Alias PIX | X | X | Alias/Wavefront PIX 图像格式 |
| animated GIF | X | X |  |
| APNG | X | X | 动画便携式网络图形 (APNG) |
| BMP | X | X | Microsoft BMP 图像 |
| BRender PIX |  | X | Argonaut BRender 3D 引擎图像格式。 |
| CRI |  | X | Cintel RAW |
| DPX | X | X | Digital Picture Exchange |
| EXR |  | X | OpenEXR |
| FITS | X | X | 灵活图像传输系统 (FITS) |
| HDR | X | X | Radiance HDR RGBE 图像格式 |
| IMG |  | X | GEM 光栅图像 |
| JPEG | X | X | 不支持渐进式 JPEG。 |
| JPEG 2000 | X | X |  |
| JPEG-LS | X | X |  |
| JPEG-XS | E | E | 经外部库 libsvtjpegxs 支持 |
| LJPEG | X |  | 无损 JPEG |
| Media 100 |  | X |  |
| MSP |  | X | Microsoft 画图图像 |
| PAM | X | X | PAM 是带透明支持的 PNM 扩展。 |
| PBM | X | X | 便携位图 (Portable BitMap) 图像 |
| PCD |  | X | PhotoCD |
| PCX | X | X | PC Paintbrush |
| PFM | X | X | 便携浮点图 (Portable FloatMap) 图像 |
| PGM | X | X | 便携灰度图 (Portable GrayMap) 图像 |
| PGMYUV | X | X | YUV 4:2:0 中带 U 与 V 分量的 PGM |
| PGX |  | X | PGX 文件解码器 |
| PHM | X | X | 便携半浮点图 (Portable HalfFloatMap) 图像 |
| PIC |  | X | Pictor/PC Paint |
| PNG | X | X | 便携式网络图形 (PNG) 图像 |
| PPM | X | X | 便携像素图 (Portable PixelMap) 图像 |
| PSD |  | X | Photoshop |
| PTX |  | X | V.Flash PTX 格式 |
| QOI | X | X | Quite OK Image 格式 |
| SGI | X | X | SGI RGB 图像格式 |
| Sun Rasterfile | X | X | Sun RAS 图像格式 |
| TIFF | X | X | 尚不支持 YUV、JPEG 及部分扩展。 |
| Truevision Targa | X | X | Targa (.TGA) 图像格式 |
| VBN | X | X | Vizrt 二进制图像格式 |
| WBMP | X | X | 无线应用协议位图图像格式 |
| WebP | E | X | WebP 图像格式，编码经外部库 libwebp 支持 |
| XBM | X | X | X 位图 (X BitMap) 图像格式 |
| XFace | X | X | X-Face 图像格式 |
| XPM |  | X | X 像素图 (X PixMap) 图像格式 |
| XWD | X | X | X Window 转储图像格式 |

`X` 表示该列（编码 / 解码）所对应的特性受支持。

`E` 表示该支持经由外部库提供。

## 视频编解码器

|  |  |  |  |
|----|----|----|----|
| Name | Encoding | Decoding | Comments |
| 4X Movie |  | X | 用于某些电脑游戏。 |
| 8088flex TMV |  | X |  |
| A64 multicolor | X |  | 生成适合在 commodore 64 上播放的视频（多色模式）。 |
| Amazing Studio PAF Video |  | X |  |
| American Laser Games MM |  | X | 用于 Mad Dog McCree 等游戏。 |
| Amuse Graphics Movie |  | X |  |
| AMV Video | X | X | 用于中国的 MP3 播放器。 |
| ANSI/ASCII art |  | X |  |
| Apple Intermediate Codec |  | X |  |
| Apple MJPEG-B |  | X |  |
| Apple Pixlet |  | X |  |
| Apple ProRes | X | X | fourcc: apch,apcn,apcs,apco,ap4h,ap4x |
| Apple QuickDraw |  | X | fourcc: qdrw |
| APV |  | X |  |
| Argonaut Video |  | X | 用于部分 Argonaut 游戏。 |
| Asus v1 | X | X | fourcc: ASV1 |
| Asus v2 | X | X | fourcc: ASV2 |
| ATI VCR1 |  | X | fourcc: VCR1 |
| ATI VCR2 |  | X | fourcc: VCR2 |
| Auravision Aura |  | X |  |
| Auravision Aura 2 |  | X |  |
| Autodesk Animator Flic video |  | X |  |
| Autodesk RLE |  | X | fourcc: AASC |
| AV1 | E | E | 经外部库 libaom、libdav1d、librav1e 与 libsvtav1 支持 |
| Avid 1:1 10-bit RGB Packer | X | X | fourcc: AVrp |
| AVS (Audio Video Standard) video |  | X | Creature Shock 游戏使用的视频编码。 |
| AVS2-P2/IEEE1857.4 | E | E | 经外部库 libxavs2 与 libdavs2 支持 |
| AVS3-P2/IEEE1857.10 |  | E | 经外部库 libuavs3d 支持 |
| AYUV | X | X | Microsoft 无压缩打包 4:4:4:4 |
| Beam Software VB |  | X |  |
| Bethesda VID video |  | X | 用于 Bethesda Softworks 的部分游戏。 |
| Bink Video |  | X |  |
| BitJazz SheerVideo |  | X |  |
| Bitmap Brothers JV video |  | X |  |
| y41p Brooktree uncompressed 4:1:1 12-bit | X | X |  |
| Brooktree ProSumer Video |  | X | fourcc: BT20 |
| Brute Force & Ignorance |  | X | 用于游戏 Flash Traffic: City of Angels。 |
| C93 video |  | X | Cyberia 游戏使用的编解码器。 |
| CamStudio |  | X | fourcc: CSCD |
| CD+G |  | X | CD+G 卡拉 OK 光盘使用的视频编解码器 |
| CDXL |  | X | Amiga CD 视频编解码器 |
| Chinese AVS video | E | X | AVS1-P2，JiZhun 配置档，编码经外部库 libxavs |
| Delphine Software International CIN video |  | X | Delphine Software International 游戏使用的编解码器。 |
| Discworld II BMV Video |  | X |  |
| CineForm HD | X | X |  |
| Canopus HQ |  | X |  |
| Canopus HQA |  | X |  |
| Canopus HQX |  | X |  |
| Canopus Lossless Codec |  | X |  |
| CDToons |  | X | 多款 Broderbund 游戏使用的编解码器。 |
| Cinepak |  | X |  |
| Cirrus Logic AccuPak | X | X | fourcc: CLJR |
| CPiA Video Format |  | X |  |
| Creative YUV (CYUV) |  | X |  |
| DFA |  | X | Chronomaster 游戏使用的编解码器。 |
| Dirac | E | X | 经原生 vc2 (Dirac Pro) 编码器支持 |
| Deluxe Paint Animation |  | X |  |
| DNxHD | X | X | 又称 SMPTE VC3 |
| Duck TrueMotion 1.0 |  | X | fourcc: DUCK |
| Duck TrueMotion 2.0 |  | X | fourcc: TM20 |
| Duck TrueMotion 2.0 RT |  | X | fourcc: TR20 |
| DV (Digital Video) | X | X |  |
| Dxtory capture format |  | X |  |
| Feeble Files/ScummVM DXA |  | X | 最初用于 Feeble Files 游戏的编解码器。 |
| Electronic Arts CMV video |  | X | 用于游戏 NHL 95。 |
| Electronic Arts Madcow video |  | X |  |
| Electronic Arts TGV video |  | X |  |
| Electronic Arts TGQ video |  | X |  |
| Electronic Arts TQI video |  | X |  |
| Escape 124 |  | X |  |
| Escape 130 |  | X |  |
| EVC / MPEG-5 Part 1 | E | E | 编码与解码经外部库 libxeve 与 libxevd 支持 |
| FFmpeg video codec \#1 | X | X | 无损编解码器（fourcc: FFV1） |
| Flash Screen Video v1 | X | X | fourcc: FSV1 |
| Flash Screen Video v2 | X | X |  |
| Flash Video (FLV) | X | X | Flash 中使用的 Sorenson H.263 |
| FM Screen Capture Codec |  | X |  |
| Forward Uncompressed |  | X |  |
| Fraps |  | X |  |
| Go2Meeting |  | X | fourcc: G2M2, G2M3 |
| Go2Webinar |  | X | fourcc: G2M4 |
| Gremlin Digital Video |  | X |  |
| H.261 | X | X |  |
| H.263 / H.263-1996 | X | X |  |
| H.263+ / H.263-1998 / H.263 version 2 | X | X |  |
| H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 | E | X | 编码经外部库 libx264 与 OpenH264 支持 |
| HEVC | X | X | 编码经外部库 libx265 与 libkvazaar 支持 |
| HNM version 4 |  | X |  |
| HuffYUV | X | X |  |
| HuffYUV FFmpeg variant | X | X |  |
| IBM Ultimotion |  | X | fourcc: ULTI |
| id Cinematic video |  | X | 用于 Quake II。 |
| id RoQ video | X | X | 用于 Quake III、Jedi Knight 2 及其他电脑游戏。 |
| IFF ILBM |  | X | IFF 交错位图 |
| IFF ByteRun1 |  | X | IFF 行程编码位图 |
| Infinity IMM4 |  | X |  |
| Intel H.263 |  | X |  |
| Intel Indeo 2 |  | X |  |
| Intel Indeo 3 |  | X |  |
| Intel Indeo 4 |  | X |  |
| Intel Indeo 5 |  | X |  |
| Interplay C93 |  | X | 用于 Interplay 的游戏 Cyberia。 |
| Interplay MVE video |  | X | 用于 Interplay .MVE 文件。 |
| J2K | X | X |  |
| Karl Morton's video codec |  | X | Worms 游戏使用的编解码器。 |
| Kega Game Video (KGV1) |  | X | Kega 模拟器屏幕抓取编解码器。 |
| Lagarith |  | X |  |
| LCEVC / MPEG-5 LCEVC / MPEG-5 Part 2 |  | E | 解码经外部库 liblcevc-dec 支持 |
| LCL (LossLess Codec Library) MSZH |  | X |  |
| LCL (LossLess Codec Library) ZLIB | E | E |  |
| LEAD MCMP |  | X |  |
| LOCO |  | X |  |
| LucasArts SANM/Smush |  | X | 用于 LucasArts 游戏 / SMUSH 动画。 |
| lossless MJPEG | X | X |  |
| MagicYUV Video | X | X |  |
| Mandsoft Screen Capture Codec |  | X |  |
| Microsoft ATC Screen |  | X | 亦称 Microsoft Screen 3。 |
| Microsoft Expression Encoder Screen |  | X | 亦称 Microsoft Titanium Screen 2。 |
| Microsoft RLE | X | X |  |
| Microsoft Screen 1 |  | X | 亦称 Windows Media Video V7 Screen。 |
| Microsoft Screen 2 |  | X | 亦称 Windows Media Video V9 Screen。 |
| Microsoft Video 1 |  | X |  |
| Mimic |  | X | 用于 MSN Messenger 网络摄像头流。 |
| Miro VideoXL |  | X | fourcc: VIXL |
| MJPEG (Motion JPEG) | X | X |  |
| Mobotix MxPEG video |  | X |  |
| Motion Pixels video |  | X |  |
| MPEG-1 video | X | X |  |
| MPEG-2 video | X | X |  |
| MPEG-4 part 2 | X | X | 编码亦可改用 libxvidcore。 |
| MPEG-4 part 2 Microsoft variant version 1 |  | X |  |
| MPEG-4 part 2 Microsoft variant version 2 | X | X |  |
| MPEG-4 part 2 Microsoft variant version 3 | X | X |  |
| Newtek SpeedHQ | X | X |  |
| Nintendo Gamecube THP video |  | X |  |
| NotchLC |  | X |  |
| NuppelVideo/RTjpeg |  | X | NuppelVideo 文件使用的视频编码。 |
| On2 VP3 |  | X | 仍为实验性 |
| On2 VP4 |  | X | fourcc: VP40 |
| On2 VP5 |  | X | fourcc: VP50 |
| On2 VP6 |  | X | fourcc: VP60,VP61,VP62 |
| On2 VP7 |  | X | fourcc: VP70,VP71 |
| VP8 | E | X | fourcc: VP80，编码经外部库 libvpx 支持 |
| VP9 | E | X | 编码经外部库 libvpx 支持 |
| Pinnacle TARGA CineWave YUV16 |  | X | fourcc: Y216 |
| Q-team QPEG |  | X | fourccs: QPEG, Q1.0, Q1.1 |
| QuickTime 8BPS video |  | X |  |
| QuickTime Animation (RLE) video | X | X | fourcc: 'rle ' |
| QuickTime Graphics (SMC) | X | X | fourcc: 'smc ' |
| QuickTime video (RPZA) | X | X | fourcc: rpza |
| R10K AJA Kona 10-bit RGB Codec | X | X |  |
| R210 Quicktime Uncompressed RGB 10-bit | X | X |  |
| Raw Video | X | X |  |
| RealVideo 1.0 | X | X |  |
| RealVideo 2.0 | X | X |  |
| RealVideo 3.0 |  | X | 距离理想还很远 |
| RealVideo 4.0 |  | X |  |
| RealVideo 6.0 |  | X |  |
| Renderware TXD (TeXture Dictionary) |  | X | Renderware 引擎使用的纹理字典。 |
| RivaTuner Video |  | X | fourcc: 'RTV1' |
| RL2 video |  | X | 用于 Entertainment Software Partners 的部分游戏 |
| ScreenPressor |  | X |  |
| Screenpresso |  | X |  |
| Screen Recorder Gold Codec |  | X |  |
| Sierra VMD video |  | X | 用于 Sierra VMD 文件。 |
| Silicon Graphics Motion Video Compressor 1 (MVC1) |  | X |  |
| Silicon Graphics Motion Video Compressor 2 (MVC2) |  | X |  |
| Silicon Graphics RLE 8-bit video |  | X |  |
| Smacker video |  | X | Smacker 使用的视频编码。 |
| SMPTE VC-1 |  | X |  |
| Snow | X | X | 实验性小波编解码器（fourcc: SNOW） |
| Sony PlayStation MDEC (Motion DECoder) |  | X |  |
| Sorenson Vector Quantizer 1 | X | X | fourcc: SVQ1 |
| Sorenson Vector Quantizer 3 |  | X | fourcc: SVQ3 |
| Sunplus JPEG (SP5X) |  | X | fourcc: SP5X |
| TechSmith Screen Capture Codec |  | X | fourcc: TSCC |
| TechSmith Screen Capture Codec 2 |  | X | fourcc: TSC2 |
| Theora | E | X | 编码经外部库 libtheora 支持 |
| Tiertex Limited SEQ video |  | X | DOS CD-ROM 版游戏 FlashBack 使用的编解码器。 |
| Ut Video | X | X |  |
| v210 QuickTime uncompressed 4:2:2 10-bit | X | X |  |
| v308 QuickTime uncompressed 4:4:4 | X | X |  |
| v408 QuickTime uncompressed 4:4:4:4 | X | X |  |
| v410 QuickTime uncompressed 4:4:4 10-bit | X | X |  |
| VBLE Lossless Codec |  | X |  |
| vMix Video |  | X | fourcc: 'VMX1' |
| VMware Screen Codec / VMware Video |  | X | VMware 录制视频所用的编解码器。 |
| Westwood Studios VQA (Vector Quantized Animation) video |  | X |  |
| Windows Media Image |  | X |  |
| Windows Media Video 7 | X | X |  |
| Windows Media Video 8 | X | X |  |
| Windows Media Video 9 |  | X | 尚未完全可用 |
| Wing Commander III / Xan |  | X | 用于 Wing Commander III .MVE 文件。 |
| Wing Commander IV / Xan |  | X | 用于 Wing Commander IV。 |
| Winnov WNV1 |  | X |  |
| WMV7 | X | X |  |
| YAMAHA SMAF | X | X |  |
| Psygnosis YOP Video |  | X |  |
| yuv4 | X | X | libquicktime 无压缩打包 4:2:0 |
| ZeroCodec Lossless Video |  | X |  |
| ZLIB | X | X | LCL 的一部分，编码器为实验性 |
| Zip Motion Blocks Video | X | X | 编码器仅在 PAL8 下工作。 |

`X` 表示该列（编码 / 解码）所对应的特性受支持。

`E` 表示该支持经由外部库提供。

## 音频编解码器

|  |  |  |  |
|----|----|----|----|
| Name | Encoding | Decoding | Comments |
| 8SVX exponential |  | X |  |
| 8SVX fibonacci |  | X |  |
| AAC | EX | X | 编码经内部编码器与外部库 libfdk-aac 支持 |
| AAC+ | E | IX | 编码经外部库 libfdk-aac 支持 |
| AC-3 | IX | IX |  |
| ACELP.KELVIN |  | X |  |
| ADPCM 4X Movie |  | X |  |
| ADPCM Yamaha AICA |  | X |  |
| ADPCM AmuseGraphics Movie |  | X |  |
| ADPCM Argonaut Games | X | X |  |
| ADPCM CDROM XA |  | X |  |
| ADPCM Creative Technology |  | X | 16 -\> 4, 8 -\> 4, 8 -\> 3, 8 -\> 2 |
| ADPCM Electronic Arts |  | X | 用于多款 EA 作品。 |
| ADPCM Electronic Arts Maxis CDROM XS |  | X | 用于 Sim City 3000。 |
| ADPCM Electronic Arts R1 |  | X |  |
| ADPCM Electronic Arts R2 |  | X |  |
| ADPCM Electronic Arts R3 |  | X |  |
| ADPCM Electronic Arts XAS |  | X |  |
| ADPCM G.722 | X | X |  |
| ADPCM G.726 | X | X |  |
| ADPCM IMA Acorn Replay |  | X |  |
| ADPCM IMA AMV | X | X | 用于 AMV 文件 |
| ADPCM IMA Cunning Developments |  | X |  |
| ADPCM IMA Electronic Arts EACS |  | X |  |
| ADPCM IMA Electronic Arts SEAD |  | X |  |
| ADPCM IMA Funcom |  | X |  |
| ADPCM IMA High Voltage Software ALP | X | X |  |
| ADPCM IMA Mobiclip MOFLEX |  | X |  |
| ADPCM IMA QuickTime | X | X |  |
| ADPCM IMA Simon & Schuster Interactive | X | X |  |
| ADPCM IMA Ubisoft APM | X | X |  |
| ADPCM IMA Loki SDL MJPEG |  | X |  |
| ADPCM IMA WAV | X | X |  |
| ADPCM IMA Westwood |  | X |  |
| ADPCM ISS IMA |  | X | 用于 FunCom 游戏。 |
| ADPCM IMA Dialogic |  | X |  |
| ADPCM IMA Duck DK3 |  | X | 用于部分 Sega Saturn 主机游戏。 |
| ADPCM IMA Duck DK4 |  | X | 用于部分 Sega Saturn 主机游戏。 |
| ADPCM IMA Radical |  | X |  |
| ADPCM IMA Xbox |  | X |  |
| ADPCM Microsoft | X | X |  |
| ADPCM MS IMA | X | X |  |
| ADPCM Nintendo Gamecube AFC |  | X |  |
| ADPCM Nintendo Gamecube DTK |  | X |  |
| ADPCM Nintendo THP |  | X |  |
| ADPCM Playstation |  | X |  |
| ADPCM QT IMA | X | X |  |
| ADPCM Sanyo |  | X |  |
| ADPCM SEGA CRI ADX | X | X | 用于 Sega Dreamcast 游戏。 |
| ADPCM Shockwave Flash | X | X |  |
| ADPCM Sound Blaster Pro 2-bit |  | X |  |
| ADPCM Sound Blaster Pro 2.6-bit |  | X |  |
| ADPCM Sound Blaster Pro 4-bit |  | X |  |
| ADPCM VIMA |  | X | 用于 LucasArts SMUSH 动画。 |
| ADPCM Konami XMD |  | X |  |
| ADPCM Westwood Studios IMA | X | X | 用于 Command and Conquer 等 Westwood Studios 游戏。 |
| ADPCM Yamaha | X | X |  |
| ADPCM Zork |  | X |  |
| AMR-NB | E | X | 编码经外部库 libopencore-amrnb 支持 |
| AMR-WB | E | X | 编码经外部库 libvo-amrwbenc 支持 |
| Amazing Studio PAF Audio |  | X |  |
| Apple lossless audio | X | X | QuickTime fourcc 'alac' |
| aptX | X | X | 用于蓝牙 A2DP |
| aptX HD | X | X | 用于蓝牙 A2DP |
| ATRAC1 |  | X |  |
| ATRAC3 |  | X |  |
| ATRAC3+ |  | X |  |
| ATRAC9 |  | X |  |
| Bink Audio |  | X | 用于许多游戏的 Bink 与 Smacker 文件。 |
| Bonk audio |  | X |  |
| codec2 | E | E | 编码/解码经外部库 libcodec2 支持 |
| CRI HCA |  | X |  |
| Delphine Software International CIN audio |  | X | Delphine Software International 游戏使用的编解码器。 |
| DFPWM | X | X |  |
| Digital Speech Standard - Standard Play mode (DSS SP) |  | X |  |
| Discworld II BMV Audio |  | X |  |
| COOK |  | X | 除 5.1 外的所有版本均受支持。 |
| DCA (DTS Coherent Acoustics) | X | X | 受支持的扩展：XCh、XXCH、X96、XBR、XLL、LBR（部分） |
| Dolby E |  | X |  |
| DPCM Cuberoot-Delta-Exact |  | X | 用于少数游戏。 |
| DPCM Gremlin |  | X |  |
| DPCM id RoQ | X | X | 用于 Quake III、Jedi Knight 2 及其他电脑游戏。 |
| DPCM Marble WADY |  | X |  |
| DPCM Interplay |  | X | 用于多款 Interplay 电脑游戏。 |
| DPCM Squareroot-Delta-Exact |  | X | 用于多款游戏。 |
| DPCM Sierra Online |  | X | 用于 Sierra Online 游戏音频文件。 |
| DPCM Sol |  | X |  |
| DPCM Xan |  | X | 用于 Origin 的 Wing Commander IV AVI 文件。 |
| DPCM Xilam DERF |  | X |  |
| DSD (Direct Stream Digital), least significant bit first |  | X |  |
| DSD (Direct Stream Digital), most significant bit first |  | X |  |
| DSD (Direct Stream Digital), least significant bit first, planar |  | X |  |
| DSD (Direct Stream Digital), most significant bit first, planar |  | X |  |
| DSP Group TrueSpeech |  | X |  |
| DST (Direct Stream Transfer) |  | X |  |
| DV audio |  | X |  |
| Enhanced AC-3 | X | X |  |
| EVRC (Enhanced Variable Rate Codec) |  | X |  |
| FLAC (Free Lossless Audio Codec) | X | IX |  |
| FTR Voice |  | X |  |
| G.723.1 | X | X |  |
| G.728 |  | X |  |
| G.729 |  | X |  |
| GSM | E | X | 编码经外部库 libgsm 支持 |
| GSM Microsoft variant | E | X | 编码经外部库 libgsm 支持 |
| IAC (Indeo Audio Coder) |  | X |  |
| iLBC (Internet Low Bitrate Codec) | E | EX | 编码与解码经外部库 libilbc 支持 |
| IMC (Intel Music Coder) |  | X |  |
| Interplay ACM |  | X |  |
| LC3 | E | E | 经外部库 liblc3 支持 |
| MACE (Macintosh Audio Compression/Expansion) 6:1 |  | X |  |
| Marian's A-pac audio |  | X |  |
| MI-SC4 (Micronas SC-4 Audio) |  | X |  |
| MLP (Meridian Lossless Packing) | X | X | 用于 DVD-Audio 光盘。 |
| Monkey's Audio |  | X |  |
| MP1 (MPEG audio layer 1) |  | IX |  |
| MP2 (MPEG audio layer 2) | IX | IX | 编码亦可经外部库 TwoLAME 支持 |
| MP3 (MPEG audio layer 3) | E | IX | 编码经外部库 LAME 支持，ADU MP3 与 MP3onMP4 亦受支持 |
| MPEG-4 Audio Lossless Coding (ALS) |  | X |  |
| MPEG-H 3D Audio |  | E | 解码经外部库 libmpeghdec 支持 |
| MobiClip FastAudio |  | X |  |
| Musepack SV7 |  | X |  |
| Musepack SV8 |  | X |  |
| Nellymoser Asao | X | X |  |
| On2 AVC (Audio for Video Codec) |  | X |  |
| Opus | E | X | 编码经外部库 libopus 支持 |
| OSQ (Original Sound Quality) |  | X |  |
| PCM A-law | X | X |  |
| PCM mu-law | X | X |  |
| PCM Archimedes VIDC | X | X |  |
| PCM signed 8-bit planar | X | X |  |
| PCM signed 16-bit big-endian planar | X | X |  |
| PCM signed 16-bit little-endian planar | X | X |  |
| PCM signed 24-bit little-endian planar | X | X |  |
| PCM signed 32-bit little-endian planar | X | X |  |
| PCM 32-bit floating point big-endian | X | X |  |
| PCM 32-bit floating point little-endian | X | X |  |
| PCM 64-bit floating point big-endian | X | X |  |
| PCM 64-bit floating point little-endian | X | X |  |
| PCM D-Cinema audio signed 24-bit | X | X |  |
| PCM signed 8-bit | X | X |  |
| PCM signed 16-bit big-endian | X | X |  |
| PCM signed 16-bit little-endian | X | X |  |
| PCM signed 24-bit big-endian | X | X |  |
| PCM signed 24-bit little-endian | X | X |  |
| PCM signed 32-bit big-endian | X | X |  |
| PCM signed 32-bit little-endian | X | X |  |
| PCM signed 16/20/24-bit big-endian in MPEG-TS |  | X |  |
| PCM unsigned 8-bit | X | X |  |
| PCM unsigned 16-bit big-endian | X | X |  |
| PCM unsigned 16-bit little-endian | X | X |  |
| PCM unsigned 24-bit big-endian | X | X |  |
| PCM unsigned 24-bit little-endian | X | X |  |
| PCM unsigned 32-bit big-endian | X | X |  |
| PCM unsigned 32-bit little-endian | X | X |  |
| PCM SGA |  | X |  |
| QCELP / PureVoice |  | X |  |
| QDesign Music Codec 1 |  | X |  |
| QDesign Music Codec 2 |  | X | 仍存在一些失真。 |
| RealAudio 1.0 (14.4K) | X | X | Real 14400 bit/s 编解码器 |
| RealAudio 2.0 (28.8K) |  | X | Real 28800 bit/s 编解码器 |
| RealAudio 3.0 (dnet) | IX | X | Real 低码率 AC-3 编解码器 |
| RealAudio Lossless |  | X |  |
| RealAudio SIPR / ACELP.NET |  | X |  |
| RK Audio (RKA) |  | X |  |
| SBC (low-complexity subband codec) | X | X | 用于蓝牙 A2DP |
| Shorten |  | X |  |
| Sierra VMD audio |  | X | 用于 Sierra VMD 文件。 |
| Smacker audio |  | X |  |
| SMPTE 302M AES3 audio | X | X |  |
| Sonic | X | X | 实验性编解码器 |
| Sonic lossless | X | X | 实验性编解码器 |
| Speex | E | EX | 经外部库 libspeex 支持 |
| TAK (Tom's lossless Audio Kompressor) |  | X |  |
| True Audio (TTA) | X | X |  |
| TrueHD | X | X | 用于 HD-DVD 与 Blu-Ray 光盘。 |
| TwinVQ (VQF flavor) |  | X |  |
| VIMA |  | X | 用于 LucasArts SMUSH 动画。 |
| ViewQuest VQC |  | X |  |
| Vorbis | E | X | 已有一个原生但非常简陋的编码器。 |
| Voxware MetaSound |  | X |  |
| Waveform Archiver |  | X |  |
| WavPack | X | X |  |
| Westwood Audio (SND1) |  | X |  |
| Windows Media Audio 1 | X | X |  |
| Windows Media Audio 2 | X | X |  |
| Windows Media Audio Lossless |  | X |  |
| Windows Media Audio Pro |  | X |  |
| Windows Media Audio Voice |  | X |  |
| Xbox Media Audio 1 |  | X |  |
| Xbox Media Audio 2 |  | X |  |

`X` 表示该列（编码 / 解码）所对应的特性受支持。

`E` 表示该支持经由外部库提供。

`I` 表示也存在仅整数版本（确保在没有硬件浮点支持的系统上获得高性能）。

## 字幕格式

|                     |        |          |          |          |
|---------------------|--------|----------|----------|----------|
| Name                | Muxing | Demuxing | Encoding | Decoding |
| 3GPP Timed Text     |        |          | X        | X        |
| AQTitle             |        | X        |          | X        |
| DVB                 | X      | X        | X        | X        |
| DVB teletext        |        | X        |          | E        |
| DVD                 | X      | X        | X        | X        |
| JACOsub             | X      | X        |          | X        |
| MicroDVD            | X      | X        |          | X        |
| MPL2                |        | X        |          | X        |
| MPsub (MPlayer)     |        | X        |          | X        |
| PGS                 |        |          |          | X        |
| PJS (Phoenix)       |        | X        |          | X        |
| RealText            |        | X        |          | X        |
| SAMI                |        | X        |          | X        |
| Spruce format (STL) |        | X        |          | X        |
| SSA/ASS             | X      | X        | X        | X        |
| SubRip (SRT)        | X      | X        | X        | X        |
| SubViewer v1        |        | X        |          | X        |
| SubViewer           |        | X        |          | X        |
| TED Talks captions  |        | X        |          | X        |
| TTML                | X      |          | X        |          |
| VobSub (IDX+SUB)    |        | X        |          | X        |
| VPlayer             |        | X        |          | X        |
| WebVTT              | X      | X        | X        | X        |
| XSUB                |        |          | X        | X        |

`X` 表示该特性受支持。

`E` 表示该支持经由外部库提供。

## 网络协议

|              |         |
|--------------|---------|
| Name         | Support |
| AMQP         | E       |
| file         | X       |
| FTP          | X       |
| Gopher       | X       |
| Gophers      | X       |
| HLS          | X       |
| HTTP         | X       |
| HTTPS        | X       |
| Icecast      | X       |
| MMSH         | X       |
| MMST         | X       |
| pipe         | X       |
| Pro-MPEG FEC | X       |
| RTMP         | X       |
| RTMPE        | X       |
| RTMPS        | X       |
| RTMPT        | X       |
| RTMPTE       | X       |
| RTMPTS       | X       |
| RTP          | X       |
| SAMBA        | E       |
| SCTP         | X       |
| SFTP         | E       |
| TCP          | X       |
| TLS          | X       |
| UDP          | X       |
| ZMQ          | E       |

`X` 表示该协议受支持。

`E` 表示该支持经由外部库提供。

## 输入/输出设备

|                      |       |        |
|----------------------|-------|--------|
| Name                 | Input | Output |
| ALSA                 | X     | X      |
| BKTR                 | X     |        |
| caca                 |       | X      |
| DV1394               | X     |        |
| Lavfi virtual device | X     |        |
| Linux framebuffer    | X     | X      |
| JACK                 | X     |        |
| LIBCDIO              | X     |        |
| LIBDC1394            | X     |        |
| OpenAL               | X     |        |
| OpenGL               |       | X      |
| OSS                  | X     | X      |
| PulseAudio           | X     | X      |
| SDL                  |       | X      |
| Video4Linux2         | X     | X      |
| VfW capture          | X     |        |
| X11 grabbing         | X     |        |
| Win32 grabbing       | X     |        |

`X` 表示支持该输入/输出。

## 时间码

|              |      |       |
|--------------|------|-------|
| Codec/format | Read | Write |
| AVI          | X    | X     |
| DV           | X    | X     |
| GXF          | X    | X     |
| MOV          | X    | X     |
| MPEG1/2      | X    | X     |
| MXF          | X    | X     |
