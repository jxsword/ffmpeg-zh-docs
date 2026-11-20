# 描述

本文描述 libavcodec 库提供的编解码器（解码器与编码器）。

# 编解码器选项

libavcodec 提供一些通用全局选项，可设置于所有编码器和解码器。此外，每个编解码器可支持所谓的私有选项，即特定于某一编解码器的选项。

有时，某个全局选项可能只影响特定种类的编解码器，对另一类则毫无意义或被忽略，因此您需要了解所设选项的含义。还有些选项仅用于解码或编码。

可通过在 FFmpeg 工具中指定 -\<option\> \<value\> 来设置选项，或在 `AVCodecContext` 选项中显式设值，或以编程方式使用 `libavutil/opt.h` API。

支持的选项列表如下：

- **`b integer (encoding,audio,video)`** 以比特/秒为单位设置码率。默认值为 200K。

- **`ab integer (encoding,audio)`** 设置音频码率（单位为比特/秒）。默认值为 128K。

- **`bt integer (encoding,video)`** 设置视频码率容差（单位为比特/秒）。单遍模式下，码率容差指定码率控制允许偏离目标平均码率的幅度。它与最小/最大码率无关。容差降得过低会对画质产生不利影响。

- **`flags flags (decoding/encoding,audio,video,subtitles)`** 设置通用标志。

  可取的值：

  - **`mv4`** 每个宏块使用四个运动矢量（mpeg4）。

  - **`qpel`** 使用 1/4 像素运动补偿。

  - **`loop`** 使用环路滤波。

  - **`qscale`** 使用固定 qscale。

  - **`pass1`** 在第一遍模式下使用内部两遍码率控制。

  - **`pass2`** 在第二遍模式下使用内部两遍码率控制。

  - **`gray`** 仅解码/编码灰度。

  - **`psnr`** 编码期间设置 error\[?\] 变量。

  - **`truncated`** 输入比特流可能被随机截断。

  - **`drop_changed`** 不输出与流中首个已解码帧参数不同的帧。当某帧被丢弃时返回错误 AVERROR_INPUT_CHANGED。

  - **`ildct`** 使用隔行 DCT。

  - **`low_delay`** 强制低延迟。

  - **`global_header`** 将全局头放入 extradata 而非每个关键帧。

  - **`bitexact`** 仅写入与平台、构建和时间无关的数据（(I)DCT 除外）。这确保文件与数据校验和可复现且跨平台一致。其主要用途是回归测试。

  - **`aic`** 应用 H263 高级帧内编码 / mpeg4 ac 预测。

  - **`ilme`** 应用隔行运动估计。

  - **`cgop`** 使用闭合 GOP。

  - **`output_corrupt`** 连同潜在损坏的帧一并输出。

- **`time_base rational number`** 设置编解码器时间基。

  它是表示帧时间戳所用的时间基本单位（单位为秒）。对于固定帧率内容，时间基应为 `1 / frame_rate`，且时间戳增量应恒为 1。

- **`g integer (encoding,video)`** 设置图像组 (GOP) 大小。默认值为 12。

- **`ar integer (decoding/encoding,audio)`** 设置音频采样率（单位为 Hz）。

- **`ac integer (decoding/encoding,audio)`** 设置音频声道数。

- **`cutoff integer (encoding,audio)`** 设置截止带宽。（仅受部分编码器支持，参见各自文档小节。）

- **`frame_size integer (encoding,audio)`** 设置音频帧大小。

  除最后一帧外，提交的每帧每声道必须恰好包含 frame_size 个采样。当编解码器设置了 CODEC_CAP_VARIABLE_FRAME_SIZE 时可为 0，此时帧大小不受限制。部分解码器会设置它以指示恒定帧大小。

- **`frame_number integer`** 设置帧编号。

- **`delay integer`**

- **`qcomp float (encoding,video)`** 设置视频量化器缩放压缩（VBR）。它作为常数用于码率控制方程。默认 rc_eq 的推荐范围为 0.0-1.0。

- **`qblur float (encoding,video)`** 设置视频量化器缩放模糊（VBR）。

- **`qmin integer (encoding,video)`** 设置最小视频量化器缩放（VBR）。必须介于 -1 与 69 之间，默认值为 2。

- **`qmax integer (encoding,video)`** 设置最大视频量化器缩放（VBR）。必须介于 -1 与 1024 之间，默认值为 31。

- **`qdiff integer (encoding,video)`** 设置量化器缩放之间的最大差值（VBR）。

- **`bf integer (encoding,video)`** 设置非 B 帧之间 B 帧的最大数量。

  必须为 -1 至 16 之间的整数。0 表示禁用 B 帧。取 -1 时将根据编码器自动选择数值。

  默认值为 0。

- **`b_qfactor float (encoding,video)`** 设置 P 帧与 B 帧之间的 qp 因子。

- **`codec_tag integer`**

- **`bug flags (decoding,video)`** 应对未被自动检测出的编码器缺陷。

  可取的值：

  - **`autodetect`**

  - **`xvid_ilace`** Xvid 隔行缺陷（fourcc==XVIX 时自动检测）

  - **`ump4`**（fourcc==UMP4 时自动检测）

  - **`no_padding`** 填充缺陷（自动检测）

  - **`amv`**

  - **`qpel_chroma`**

  - **`std_qpel`** 旧标准 qpel（按 fourcc/版本自动检测）

  - **`qpel_chroma2`**

  - **`direct_blocksize`** direct-qpel-blocksize 缺陷（按 fourcc/版本自动检测）

  - **`edge`** 边缘填充缺陷（按 fourcc/版本自动检测）

  - **`hpel_chroma`**

  - **`dc_clip`**

  - **`ms`** 应对 microsoft 损坏解码器中的多种缺陷。

  - **`trunc`** 截断的帧

- **`strict integer (decoding/encoding,audio,video)`** 指定遵循标准的严格程度。

  可取的值：

  - **`very`** 严格符合规范的旧版更严格版本或参考软件

  - **`strict`** 无论后果如何都严格符合规范中的一切

  - **`normal`**

  - **`unofficial`** 允许非官方扩展

  - **`experimental`** 允许非标准化的实验性内容、实验性（未完成/开发中/未经充分测试）解码器与编码器。注意：实验性解码器可能带来安全风险，请勿用于解码不受信任的输入。

- **`b_qoffset float (encoding,video)`** 设置 P 帧与 B 帧之间的 QP 偏移。

- **`err_detect flags (decoding,audio,video)`** 设置错误检测标志。

  可取的值：

  - **`crccheck`** 校验内嵌 CRC

  - **`bitstream`** 检测比特流规范偏差

  - **`buffer`** 检测不正确的比特流长度

  - **`explode`** 检测到轻微错误时中止解码

  - **`ignore_err`** 忽略解码错误并继续解码。若您想分析视频内容、希望无论如何都完成解码，此选项会有用。发生错误时该选项不会产出观感良好的视频。

  - **`careful`** 将违反规范且野外未曾见过的情况视为错误

  - **`compliant`** 将所有不符合规范之处视为错误

  - **`aggressive`** 将理智的编码器不应做出的事情视为错误

- **`has_b_frames integer`**

- **`block_align integer`**

- **`rc_override_count integer`**

- **`maxrate integer (encoding,audio,video)`** 设置最大码率容差（单位为比特/秒）。需要设置 bufsize。

- **`minrate integer (encoding,audio,video)`** 设置最小码率容差（单位为比特/秒）。对建立 CBR 编码最有用，除此之外用处不大。

- **`bufsize integer (encoding,audio,video)`** 设置码率控制缓冲区大小（单位为比特）。

- **`i_qfactor float (encoding,video)`** 设置 P 帧与 I 帧之间的 QP 因子。

- **`i_qoffset float (encoding,video)`** 设置 P 帧与 I 帧之间的 QP 偏移。

- **`dct integer (encoding,video)`** 设置 DCT 算法。

  可取的值：

  - **`auto`** 自动选择一个合适的（默认）

  - **`fastint`** 快速整数

  - **`int`** 精确整数

  - **`mmx`**

  - **`altivec`**

  - **`faan`** 浮点 AAN DCT

- **`lumi_mask float (encoding,video)`** 对明亮区域的压缩强于中等区域。

- **`tcplx_mask float (encoding,video)`** 设置时间复杂度掩码。

- **`scplx_mask float (encoding,video)`** 设置空间复杂度掩码。

- **`p_mask float (encoding,video)`** 设置帧间掩码。

- **`dark_mask float (encoding,video)`** 对黑暗区域的压缩强于中等区域。

- **`idct integer (decoding/encoding,video)`** 选择 IDCT 实现。

  可取的值：

  - **`auto`**

  - **`int`**

  - **`simple`**

  - **`simplemmx`**

  - **`simpleauto`** 自动挑选一个与 simple 兼容的 IDCT

  - **`arm`**

  - **`altivec`**

  - **`sh4`**

  - **`simplearm`**

  - **`simplearmv5te`**

  - **`simplearmv6`**

  - **`simpleneon`**

  - **`xvid`**

  - **`faani`** 浮点 AAN IDCT

- **`slice_count integer`**

- **`ec flags (decoding,video)`** 设置错误隐藏策略。

  可取的值：

  | Term | Description |
  |----|----|
  | `guess_mvs` | 迭代运动矢量 (MV) 搜索（慢） |
  | `deblock` | 对受损宏块使用强去块滤波 |
  | `favor_inter` | 倾向于从前一帧而非当前帧进行预测 |

- **`bits_per_coded_sample integer`**

- **`aspect rational number (encoding,video)`** 设置采样宽高比。

- **`sar rational number (encoding,video)`** 设置采样宽高比。\<aspect\> 的别名。

- **`debug flags (decoding/encoding,audio,video,subtitles)`** 打印特定调试信息。

  可取的值：

  - **`pict`** 图像信息

  - **`rc`** 码率控制

  - **`bitstream`**

  - **`mb_type`** 宏块 (MB) 类型

  - **`qp`** 逐块量化参数 (QP)

  - **`dct_coeff`**

  - **`green_metadata`** 即将到来的帧、GoP 或给定时长的显示复杂度元数据。

  - **`skip`**

  - **`startcode`**

  - **`er`** 错误识别

  - **`mmco`** 内存管理控制操作（H.264）

  - **`bugs`**

  - **`buffers`** 图像缓冲区分配

  - **`thread_ops`** 线程操作

  - **`nomc`** 跳过运动补偿

- **`cmp integer (encoding,video)`** 设置全像素运动估计比较函数。

  可取的值：

  - **`sad`** 绝对差之和，快速（默认）

  - **`sse`** 误差平方和

  - **`satd`** 绝对 Hadamard 变换差之和

  - **`dct`** 绝对 DCT 变换差之和

  - **`psnr`** 量化误差平方和（避免使用，质量低）

  - **`bit`** 该块所需的比特数

  - **`rd`** 率失真最优，慢

  - **`zero`** 0

  - **`vsad`** 垂直绝对差之和

  - **`vsse`** 垂直误差平方和

  - **`nsse`** 噪声保留的平方差之和

  - **`w53`** 5/3 小波，仅用于 snow

  - **`w97`** 9/7 小波，仅用于 snow

  - **`dctmax`**

  - **`chroma`**

- **`subcmp integer (encoding,video)`** 设置子像素运动估计比较函数。

  可取的值：

  - **`sad`** 绝对差之和，快速（默认）

  - **`sse`** 误差平方和

  - **`satd`** 绝对 Hadamard 变换差之和

  - **`dct`** 绝对 DCT 变换差之和

  - **`psnr`** 量化误差平方和（避免使用，质量低）

  - **`bit`** 该块所需的比特数

  - **`rd`** 率失真最优，慢

  - **`zero`** 0

  - **`vsad`** 垂直绝对差之和

  - **`vsse`** 垂直误差平方和

  - **`nsse`** 噪声保留的平方差之和

  - **`w53`** 5/3 小波，仅用于 snow

  - **`w97`** 9/7 小波，仅用于 snow

  - **`dctmax`**

  - **`chroma`**

- **`mbcmp integer (encoding,video)`** 设置宏块比较函数。

  可取的值：

  - **`sad`** 绝对差之和，快速（默认）

  - **`sse`** 误差平方和

  - **`satd`** 绝对 Hadamard 变换差之和

  - **`dct`** 绝对 DCT 变换差之和

  - **`psnr`** 量化误差平方和（避免使用，质量低）

  - **`bit`** 该块所需的比特数

  - **`rd`** 率失真最优，慢

  - **`zero`** 0

  - **`vsad`** 垂直绝对差之和

  - **`vsse`** 垂直误差平方和

  - **`nsse`** 噪声保留的平方差之和

  - **`w53`** 5/3 小波，仅用于 snow

  - **`w97`** 9/7 小波，仅用于 snow

  - **`dctmax`**

  - **`chroma`**

- **`ildctcmp integer (encoding,video)`** 设置隔行 dct 比较函数。

  可取的值：

  - **`sad`** 绝对差之和，快速（默认）

  - **`sse`** 误差平方和

  - **`satd`** 绝对 Hadamard 变换差之和

  - **`dct`** 绝对 DCT 变换差之和

  - **`psnr`** 量化误差平方和（避免使用，质量低）

  - **`bit`** 该块所需的比特数

  - **`rd`** 率失真最优，慢

  - **`zero`** 0

  - **`vsad`** 垂直绝对差之和

  - **`vsse`** 垂直误差平方和

  - **`nsse`** 噪声保留的平方差之和

  - **`w53`** 5/3 小波，仅用于 snow

  - **`w97`** 9/7 小波，仅用于 snow

  - **`dctmax`**

  - **`chroma`**

- **`dia_size integer (encoding,video)`** 设置运动估计的菱形类型与大小。

  | Term                | Description                     |
  |---------------------|---------------------------------|
  | `(1024, INT_MAX)` | 完整运动估计（最慢） |
  | `(768, 1024]`     | umh 运动估计           |
  | `(512, 768]`      | hex 运动估计           |
  | `(256, 512]`      | l2s 菱形运动估计   |
  | `[2,256]`         | var 菱形运动估计   |
  | `(-1, 2)`         | 小菱形运动估计 |
  | `-1`              | 趣味菱形运动估计 |
  | `(INT_MIN, -1)`   | sab 菱形运动估计   |

- **`last_pred integer (encoding,video)`** 设置来自前一帧的运动预测器数量。

- **`precmp integer (encoding,video)`** 设置预运动估计比较函数。

  可取的值：

  - **`sad`** 绝对差之和，快速（默认）

  - **`sse`** 误差平方和

  - **`satd`** 绝对 Hadamard 变换差之和

  - **`dct`** 绝对 DCT 变换差之和

  - **`psnr`** 量化误差平方和（避免使用，质量低）

  - **`bit`** 该块所需的比特数

  - **`rd`** 率失真最优，慢

  - **`zero`** 0

  - **`vsad`** 垂直绝对差之和

  - **`vsse`** 垂直误差平方和

  - **`nsse`** 噪声保留的平方差之和

  - **`w53`** 5/3 小波，仅用于 snow

  - **`w97`** 9/7 小波，仅用于 snow

  - **`dctmax`**

  - **`chroma`**

- **`pre_dia_size integer (encoding,video)`** 设置运动估计预处理阶段的菱形类型与大小。

- **`subq integer (encoding,video)`** 设置子像素运动估计质量。

- **`me_range integer (encoding,video)`** 设置运动矢量范围限制（DivX 播放器为 1023）。

- **`global_quality integer (encoding,audio,video)`**

- **`slice_flags integer`**

- **`mbd integer (encoding,video)`** 设置宏块决策算法（高质量模式）。

  可取的值：

  | Term       | Description              |
  |------------|--------------------------|
  | `simple` | 使用 mbcmp（默认）      |
  | `bits`   | 使用最少比特          |
  | `rd`     | 使用最优率失真 |

- **`rc_init_occupancy integer (encoding,video)`** 设置在解码开始前应载入 rc 缓冲区的比特数。

- **`flags2 flags (decoding/encoding,audio,video,subtitles)`** 可取的值：

  - **`fast`** 允许不符合规范的速度优化技巧。

  - **`noout`** 跳过比特流编码。

  - **`ignorecrop`** 忽略来自 sps 的裁剪信息。

  - **`local_header`** 将全局头置于每个关键帧而非 extradata。

  - **`chunks`** 帧数据可能被拆分为多个块。

  - **`showall`** 在首个关键帧之前显示所有帧。

  - **`export_mvs`** 对支持的编解码器，将运动矢量导出到帧 side data（参见 `AV_FRAME_DATA_MOTION_VECTORS`）。另参见 `doc/examples/export_mvs.c`。

  - **`skip_manual`** 不跳过采样，并将跳过信息作为帧 side data 导出。

  - **`ass_ro_flush_noop`** 刷新时不重置 ASS ReadOrder 字段。

  - **`icc_profiles`** 从/向色度标签生成/解析内嵌 ICC 配置文件。

  - **`fixed_frame_size`** 强制音频编码器使用固定帧大小。

- **`export_side_data flags (decoding/encoding,audio,video,subtitles)`** 可取的值：

  - **`mvs`** 对支持的编解码器，将运动矢量导出到帧 side data（参见 `AV_FRAME_DATA_MOTION_VECTORS`）。另参见 `doc/examples/export_mvs.c`。

  - **`prft`** 对支持的编解码器，将编码器生产者参考时间导出到包 side data（参见 `AV_PKT_DATA_PRFT`）。

  - **`venc_params`** 对支持的编解码器，通过帧 side data 导出视频编码参数（参见 `AV_FRAME_DATA_VIDEO_ENC_PARAMS`）。目前包括 H.264 和 VP9。

  - **`film_grain`** 通过帧 side data 导出胶片颗粒参数（参见 `AV_FRAME_DATA_FILM_GRAIN_PARAMS`）。目前 AV1 解码器支持。

  - **`enhancements`** 通过帧 side data 导出图像增强元数据，例如 LCEVC（参见 `AV_FRAME_DATA_LCEVC`）。

- **`threads integer (decoding/encoding,video)`** 在所选编解码器实现支持多线程的情况下，设置要使用的线程数。

  可取的值：

  | Term        | Description                                       |
  |-------------|---------------------------------------------------|
  | `auto, 0` | 自动选择要设置的线程数 |

  默认值为 `auto`。

- **`dc integer (encoding,video)`** 设置 intra_dc_precision。

- **`nssew integer (encoding,video)`** 设置 nsse 权重。

- **`skip_top integer (decoding,video)`** 设置顶部跳过的宏块行数。

- **`skip_bottom integer (decoding,video)`** 设置底部跳过的宏块行数。

- **`profile integer (encoding,audio,video)`** 设置编码器编解码器 profile。默认值为 `unknown`。编码器特有的 profile 在相应编码器文档中说明。

- **`level integer (encoding,audio,video)`** 设置编码器 level。该 level 取决于具体编解码器，可能对应 profile level。默认设为 `unknown`。

  可取的值：

  - **`unknown`**

- **`lowres integer (decoding,audio,video)`** 以 1=1/2、2=1/4、3=1/8 分辨率解码。

- **`mblmin integer (encoding,video)`** 设置最小宏块 lagrange 因子（VBR）。

- **`mblmax integer (encoding,video)`** 设置最大宏块 lagrange 因子（VBR）。

- **`skip_loop_filter integer (decoding,video)`**

- **`skip_idct integer (decoding,video)`**

- **`skip_frame integer (decoding,video)`** 让解码器根据选项值所选的帧类型放弃处理。

  `skip_loop_filter` 跳过帧环路滤波，`skip_idct` 跳过帧 IDCT/反量化，`skip_frame` 跳过解码。

  可取的值：

  | Term        | Description                                 |
  |-------------|---------------------------------------------|
  | `none`    | 不丢弃任何帧。                           |
  | `default` | 丢弃无用帧，如 0 大小的帧。 |
  | `noref`   | 丢弃所有非参考帧。           |
  | `bidir`   | 丢弃所有双向帧。           |
  | `nokey`   | 除关键帧外丢弃所有帧。       |
  | `nointra` | 除 I 帧外丢弃所有帧。         |
  | `all`     | 丢弃所有帧。                         |

  默认值为 `default`。

- **`bidir_refine integer (encoding,video)`** 精化双向宏块使用的两个运动矢量。

- **`keyint_min integer (encoding,video)`** 设置 IDR 帧之间的最小间隔。

- **`refs integer (encoding,video)`** 设置运动补偿考虑的参考帧数。

- **`trellis integer (encoding,audio,video)`** 设置率失真最优量化。

- **`mv0_threshold integer (encoding,video)`**

- **`compression_level integer (encoding,audio,video)`**

- **`bits_per_raw_sample integer`**

- **`channel_layout integer (decoding/encoding,audio)`** 所需语法参见 `ffmpeg-utils` 中的"the Channel Layout section in the ffmpeg-utils(1) manual"（声道布局）一节。

- **`rc_max_vbv_use float (encoding,video)`**

- **`rc_min_vbv_use float (encoding,video)`**

- **`color_primaries integer (decoding/encoding,video)`** 可取的值：

  - **`bt709`** BT.709

  - **`bt470m`** BT.470 M

  - **`bt470bg`** BT.470 BG

  - **`smpte170m`** SMPTE 170 M

  - **`smpte240m`** SMPTE 240 M

  - **`film`** Film

  - **`bt2020`** BT.2020

  - **`smpte428`**

  - **`smpte428_1`** SMPTE ST 428-1

  - **`smpte431`** SMPTE 431-2

  - **`smpte432`** SMPTE 432-1

  - **`jedec-p22`** JEDEC P22

- **`color_trc integer (decoding/encoding,video)`** 可取的值：

  - **`bt709`** BT.709

  - **`gamma22`** BT.470 M

  - **`gamma28`** BT.470 BG

  - **`smpte170m`** SMPTE 170 M

  - **`smpte240m`** SMPTE 240 M

  - **`linear`** Linear

  - **`log`**

  - **`log100`** Log

  - **`log_sqrt`**

  - **`log316`** Log square root

  - **`iec61966_2_4`**

  - **`iec61966-2-4`** IEC 61966-2-4

  - **`bt1361`**

  - **`bt1361e`** BT.1361

  - **`iec61966_2_1`**

  - **`iec61966-2-1`** IEC 61966-2-1

  - **`bt2020_10`**

  - **`bt2020_10bit`** BT.2020 - 10 bit

  - **`bt2020_12`**

  - **`bt2020_12bit`** BT.2020 - 12 bit

  - **`smpte2084`** SMPTE ST 2084

  - **`smpte428`**

  - **`smpte428_1`** SMPTE ST 428-1

  - **`arib-std-b67`** ARIB STD-B67

- **`colorspace integer (decoding/encoding,video)`** 可取的值：

  - **`rgb`** RGB

  - **`bt709`** BT.709

  - **`fcc`** FCC

  - **`bt470bg`** BT.470 BG

  - **`smpte170m`** SMPTE 170 M

  - **`smpte240m`** SMPTE 240 M

  - **`ycocg`** YCOCG

  - **`bt2020nc`**

  - **`bt2020_ncl`** BT.2020 NCL

  - **`bt2020c`**

  - **`bt2020_cl`** BT.2020 CL

  - **`smpte2085`** SMPTE 2085

  - **`chroma-derived-nc`** Chroma-derived NCL

  - **`chroma-derived-c`** Chroma-derived CL

  - **`ictcp`** ICtCp

- **`color_range integer (decoding/encoding,video)`** 作为输入参数使用时，它作为提示告知解码器输入具有的 color_range。可取的值：

  - **`tv`**

  - **`mpeg`**

  - **`limited`** MPEG (219\*2^(n-8))

  - **`pc`**

  - **`jpeg`**

  - **`full`** JPEG (2^n-1)

- **`chroma_sample_location integer (decoding/encoding,video)`** 可取的值：

  - **`left`**

  - **`center`**

  - **`topleft`**

  - **`top`**

  - **`bottomleft`**

  - **`bottom`**

- **`alpha_mode integer (decoding/encoding,video)`** 可取的值：

  - **`premultiplied`**

  - **`straight`**

- **`log_level_offset integer`** 设置日志级别偏移。

- **`slices integer (encoding,video)`** 小片数量，用于并行化编码。

- **`thread_type flags (decoding/encoding,video)`** 选择使用哪种多线程方法。

  使用 `frame` 会令解码延迟每线程增加一帧，因此无法提前提供后续帧的客户端不应使用它。

  可取的值：

  - **`slice`** 一次解码单帧的多个部分。

    基于小片的多线程仅在视频以小片编码时有效。

  - **`frame`** 一次解码多帧。

  默认值为 `slice+frame`。

- **`audio_service_type integer (encoding,audio)`** 设置音频服务类型。

  可取的值：

  | Term   | Description        |
  |--------|--------------------|
  | `ma` | 主音频服务 |
  | `ef` | 效果            |
  | `vi` | 视障辅助  |
  | `hi` | 听障辅助   |
  | `di` | 对话           |
  | `co` | 评论         |
  | `em` | 紧急          |
  | `vo` | 画外音         |
  | `ka` | 卡拉 OK            |

- **`request_sample_fmt sample_fmt (decoding,audio)`** 设置音频解码器应优先使用的采样格式。默认值为 `none`。

- **`pkt_timebase rational number`**

- **`sub_charenc encoding (decoding,subtitles)`** 设置输入字幕的字符编码。

- **`field_order field_order (video)`** 设置/覆盖视频的场序。可取的值：

  | Term            | Description                                               |
  |-----------------|-----------------------------------------------------------|
  | `progressive` | 逐行视频                                         |
  | `tt`          | 隔行视频，顶场先编码先显示     |
  | `bb`          | 隔行视频，底场先编码先显示  |
  | `tb`          | 隔行视频，顶场先编码，底场先显示 |
  | `bt`          | 隔行视频，底场先编码，顶场先显示 |

- **`skip_alpha bool (decoding,video)`** 设为 1 禁用透明 (alpha) 处理。其作用类似 `flags` 选项中的 `gray` 标志，只是跳过的是 alpha 信息而非色度信息。默认为 0。

- **`codec_whitelist list (input)`** 以","分隔的允许解码器列表。默认全部允许。

- **`dump_separator string (input)`** 用于分隔命令行上打印的流参数各字段的分隔符。例如以换行和缩进分隔字段：

  ``` text
  ffprobe -dump_separator "
                            "  -i ~/videos/matrixbench_mpeg2.mpg
  ```

- **`max_pixels integer (decoding/encoding,video)`** 每幅图像的最大像素数。该值可用于避免大图像导致的内存耗尽故障。

- **`apply_cropping bool (decoding,video)`** 当裁剪参数是 left 和 top 参数所需对齐的倍数时启用裁剪。若不满足对齐要求，将部分应用裁剪以维持对齐。默认为 1（启用）。注意：所需对齐取决于是否设置了 `AV_CODEC_FLAG_UNALIGNED` 以及 CPU。`AV_CODEC_FLAG_UNALIGNED` 无法从命令行更改。此外，硬件解码器不会应用 left/top 裁剪。

# 解码器

解码器是 FFmpeg 中的已配置组件，用于解码多媒体流。

配置 FFmpeg 构建时，所有受支持的原生解码器默认启用。需要外部库的解码器必须通过相应的 `--enable-lib` 选项手动启用。可使用 configure 选项 `--list-decoders` 列出全部可用解码器。

可用 configure 选项 `--disable-decoders` 禁用全部解码器，并用选项 `--enable-decoder=DECODER` / `--disable-decoder=DECODER` 选择性地启用/禁用单个解码器。

ff\* 工具的 `-decoders` 选项会显示已启用的解码器列表。

# 视频解码器

以下描述部分当前可用的视频解码器。

## av1

AOMedia Video 1 (AV1) 解码器。

### 选项

| Term | Description |
|----|----|
| `operating_point` | 选择可分级 AV1 比特流的一个操作点 (operating point)（0 - 31）。默认为 0。 |

## hevc

HEVC（又称 ITU-T H.265 或 ISO/IEC 23008-2）解码器。

该解码器支持最多两个视图的 MV-HEVC 多视图流。要输出的视图通过向解码器提供视图 ID 列表来选择（`view_ids` 选项）。该选项既可在解码器初始化之前静态设置，也可从 `get_format()` 回调中设置——后者适用于视图数量或 ID 在解码期间动态变化的情形。

默认仅解码基本层。

注意：如果您使用 `ffmpeg` 命令行工具，应使用其手册中记载的视图说明符 (view specifier)，而非此处记载的选项。

### 选项

- **`view_ids (MV-HEVC)`** 指定应输出的视图 ID 列表。该选项也可设为单个 '-1'，这将解码并输出 VPS 中定义的所有视图。

- **`view_ids_available (MV-HEVC)`** 调用方可读取该选项以获取活动 VPS 中可用视图 ID 的数组。单层视频时该数组为空。

  从 `get_format()` 回调中读取该值可保证准确。在其他时刻（如打开解码器之后）也可能读取到该值，但它仅供参考且可能不正确（如流中包含多个不同 VPS NALU 时）。

- **`view_pos_available (MV-HEVC)`** 调用方可读取该选项以获取活动 VPS 中可用视图位置（左、右或未指定）的数组，表示为 `AVStereo3DView` 值。数组可用时，其元素与 `view_ids_available` 的对应元素配对，即 `view_pos_available[i]` 包含 ID 为 `view_ids_available[i]` 的视图的位置。

  适用于 `view_ids_available` 的有效性限制同样适用于本选项。

## rawvideo

原始视频解码器。

该解码器解码 rawvideo 流。

### 选项

- **`top top_field_first`** 指定输入视频的假定场类型。

  | Term | Description                                      |
  |------|--------------------------------------------------|
  | `-1` | 假定视频为逐行（默认） |
  | `0`  | 假定为底场在前                    |
  | `1`  | 假定为顶场在前                       |

## libdav1d

dav1d AV1 解码器。

libdav1d 允许 libavcodec 解码 AOMedia Video 1 (AV1) 编解码器。配置期间需要 libdav1d 头文件与库。需要以 `--enable-libdav1d` 显式配置构建。

### 选项

libdav1d 封装器支持以下选项。

- **`max_frame_delay`** 设置解码器内部可缓冲的最大帧数。默认值为 0（自动检测）。

- **`filmgrain`** 若比特流中存在胶片颗粒，则将其应用到解码后的视频。默认使用库的内部默认值。该选项已弃用，将来会被移除。请改用全局选项 `export_side_data` 导出胶片颗粒参数而非应用它。

- **`oppoint`** 选择可分级 AV1 比特流的一个操作点（0 - 31）。默认使用库的内部默认值。

- **`alllayers`** 输出可分级 AV1 比特流的所有空间层。默认值为 false。

## libdavs2

AVS2-P2/IEEE1857.4 视频解码器封装器。

该解码器允许 libavcodec 借助 davs2 库解码 AVS2 流。

## libuavs3d

AVS3-P2/IEEE1857.10 视频解码器。

libuavs3d 允许 libavcodec 解码 AVS3 流。配置期间需要 libuavs3d 头文件与库。需要以 `--enable-libuavs3d` 显式配置构建。

### 选项

libuavs3d 封装器支持以下选项。

- **`frame_threads`** 设置解码期间使用的帧线程数量。默认值为 0（自动检测）。

## libxevd

eXtra-fast Essential Video Decoder (XEVD) MPEG-5 EVC 解码器封装器。

该解码器要求配置期间存在 libxevd 头文件与库。需要以 `--enable-libxevd` 显式配置构建。

xevd 项目网站位于 <https://github.com/mpeg5/xevd>。

### 选项

libxevd 封装器支持以下选项。为便于迁移，括号中列出 xevd 等价的选项或值。

要获得更准确、更全面的 libxevd 选项文档，请执行命令 `xevd_app --help` 或查阅 libxevd 文档。

| Term                | Description                               |
|---------------------|-------------------------------------------|
| `threads (threads)` | 强制使用指定的线程数 |

## QSV 解码器

Intel QuickSync Video 解码器家族（VC1、MPEG-2、H.264、HEVC、JPEG/MJPEG、VP8、VP9、AV1、VVC）。

### 通用选项

所有 qsv 解码器均支持以下选项。

- **`async_depth`** 内部并行化深度，值越大延迟越高。

- **`gpu_copy`** 视频内存与系统内存之间的 GPU 加速拷贝

  - **`default`**

  - **`on`**

  - **`off`**

### HEVC 选项

hevc_qsv 的额外选项。

- **`load_plugin`** 在内部会话中加载的用户插件

  - **`none`**

  - **`hevc_sw`**

  - **`hevc_hw`**

- **`load_plugins`** 以":"分隔的十六进制插件 UID 列表，将在内部会话中加载

## v210

无压缩 4:2:2 10 比特解码器。

### 选项

- **`custom_stride`** 以字节为单位设置 v210 数据的行大小。默认值为 0（自动检测）。可使用特殊值 -1 表示无步长的 v210，如 BOXX 文件中所示。

# 音频解码器

以下描述部分当前可用的音频解码器。

## ac3

AC-3 音频解码器。

该解码器实现 ATSC A/52:2010 与 ETSI TS 102 366 的一部分，以及未见于文档的 RealAudio 3（又称 dnet）。

### AC-3 解码器选项

- **`-drc_scale value`** 动态范围缩放因子。应用到 AC-3 流中动态范围值的因子。该因子按指数方式应用。默认值为 1。有三个值得注意的缩放因子范围：

  - **`drc_scale == 0`** 禁用 DRC。产出全范围音频。

  - **`0 < drc_scale <= 1`** 启用 DRC。应用流 DRC 值的一部分。音频再现介于全范围与全压缩之间。

  - **`drc_scale > 1`** 启用 DRC。非对称地应用 drc_scale。响亮声音被完全压缩，柔和声音被增强。

## flac

FLAC 音频解码器。

该解码器力求实现 Xiph 的完整 FLAC 规范。

### FLAC 解码器选项

- **`-use_buggy_lpc`** lavc FLAC 编码器过去在高 lpc 值（如默认值）下会产生有缺陷的流。该选项通过在解码时使用 lavc 旧的有缺陷的 lpc 逻辑，使正确解码此类流成为可能。

## ffwavesynth

内部波形合成器。

该解码器按预定义序列生成波形模式。其用途纯属内部，其接受的数据格式未公开记载。

## libgsm

libgsm 解码器封装器。

libgsm 允许 libavcodec 解码 GSM 全速率音频编解码器。配置期间需要 libgsm 头文件与库。需要以 `--enable-libgsm` 显式配置构建。

该解码器同时支持普通 GSM 与 Microsoft 变体。

## libilbc

libilbc 解码器封装器。

libilbc 允许 libavcodec 解码 Internet Low Bitrate Codec (iLBC) 音频编解码器。配置期间需要 libilbc 头文件与库。需要以 `--enable-libilbc` 显式配置构建。

### 选项

libilbc 封装器支持以下选项。

- **`enhance`** 设为 1 时启用对解码后音频的增强。默认值为 0（禁用）。

## libmpeghdec

libmpeghdec 解码器封装器。

libmpeghdec 允许 libmpeghdec 解码 MPEG-H 3D 音频编解码器。配置期间需要 libmpeghdec 头文件与库。需要以 `--enable-libmpeghdec --enable-nonfree` 显式配置构建。

## libopencore-amrnb

libopencore-amrnb 解码器封装器。

libopencore-amrnb 允许 libavcodec 解码 Adaptive Multi-Rate Narrowband 音频编解码器。使用它要求配置期间存在 libopencore-amrnb 头文件与库。需要以 `--enable-libopencore-amrnb` 显式配置构建。

AMR-NB 已有 FFmpeg 原生解码器，因此用户无需此库即可解码 AMR-NB。

## libopencore-amrwb

libopencore-amrwb 解码器封装器。

libopencore-amrwb 允许 libavcodec 解码 Adaptive Multi-Rate Wideband 音频编解码器。使用它要求配置期间存在 libopencore-amrwb 头文件与库。需要以 `--enable-libopencore-amrwb` 显式配置构建。

AMR-WB 已有 FFmpeg 原生解码器，因此用户无需此库即可解码 AMR-WB。

## libopus

libopus 解码器封装器。

libopus 允许 libavcodec 解码 Opus Interactive Audio Codec。配置期间需要 libopus 头文件与库。需要以 `--enable-libopus` 显式配置构建。

Opus 已有 FFmpeg 原生解码器，因此用户无需此库即可解码 Opus。

# 字幕解码器

## libaribb24

ARIB STD-B24 字幕解码器。

实现 ARIB STD-B24 标准的 profile A 与 profile C。

### libaribb24 解码器选项

- **`-aribb24-base-path path`** 设置 libaribb24 库的基路径。用于读取配置文件（用于自定义 unicode 转换），以及将非文本符号以图像形式转储到该位置之下。

  默认未设置。

- **`-aribb24-skip-ruby-text boolean`** 告知解码器封装器跳过包含半高 ruby 文本（注音文本）的文本块。

  默认启用。

## libaribcaption

另一个使用外部 libaribcaption 库的 ARIB STD-B24 字幕解码器。

实现日本 ARIB STD-B24 标准的 profile A 与 profile C、巴西 ABNT NBR 15606-1，以及菲律宾版 ISDB-T。

要求配置期间存在 libaribcaption 头文件与库（<https://github.com/xqq/libaribcaption>）。需要以 `--enable-libaribcaption` 显式配置构建。若 libaribb24 与 libaribcaption 均已启用，libaribcaption 解码器优先。

### libaribcaption 解码器选项

- **`-sub_type subtitle_type`** 指定解码后字幕的格式。

  | Term       | Description                                  |
  |------------|----------------------------------------------|
  | `bitmap` | 图形图像。                             |
  | `ass`    | ASS 格式化文本。                          |
  | `text`   | 不带格式的简单文本输出。 |

  默认为 ass，与 libaribb24 解码器相同。一些现有播放器（如 mpv）期望 ARIB 字幕为 ASS 格式。

- **`-caption_encoding encoding_scheme`** 指定输入字幕文本的编码方案。

  - **`auto`** 自动检测文本编码（默认）。

  - **`jis`** ARIB STD B24 定义的 8bit-char JIS 编码。该编码在日本用于 ISDB 字幕。

  - **`utf8`** ARIB STD B24 定义的 UTF-8 编码。该编码在菲律宾用于 ISDB-T 字幕。

  - **`latin`** ABNT NBR 15606-1 定义的拉丁字符编码。该编码在南美洲用于 SBTVD / ISDB-Tb 字幕。

- **`-font font_name[,font_name2,...]`** 指定以逗号分隔的字体族名称列表，用于 bitmap 或 ass 类型字幕的渲染。ass 类型字幕只使用第一个字体名称。

  未指定时使用内部定义的默认字体族。

- **`-ass_single_rect boolean`** ARIB STD-B24 规定某些字幕可能同时显示在不同位置（多矩形字幕）。由于部分播放器（如旧版 mpv）无法处理单个 AVSubtitle 中的多个 ASS 矩形，或无法处理起始时间戳相同但时长不定的多个 ASS 矩形，该选项可改变行为，使所有文本显示在单个 ASS 矩形中。

  默认为 \<false\>。

  如果您的播放器无法正确处理带多个 ASS 矩形的 AVSubtitle，可将该选项设为 \<true\>，或在编译时定义 `ASS_SINGLE_RECT=1` 以改变默认行为。

- **`-force_outline_text boolean`** 指定是否始终为所有字符渲染描边文本，而不管字符样式如何指示。

  默认为 \<false\>。

- **`-outline_width number (0.0 - 3.0)`** 指定描边文本的宽度，以点为单位（相对值）。

  默认为 \<1.5\>。

- **`-ignore_background boolean`** 指定是否忽略背景色渲染。

  默认为 \<false\>。

- **`-ignore_ruby boolean`** 指定是否忽略 ruby 类（注音）字符的渲染。

  默认为 \<false\>。

- **`-replace_drcs boolean`** 指定是否将被替换的 DRCS 字符渲染为 Unicode 字符。

  默认为 \<true\>。

- **`-replace_msz_ascii boolean`** 指定是否将 MSZ（中等大小；半宽）全角字母数字替换为半角字母数字。

  默认为 \<true\>。

- **`-replace_msz_japanese boolean`** 指定是否将某些 MSZ（中等大小；半宽）全角日文特殊字符替换为半角字符。

  默认为 \<true\>。

- **`-replace_msz_glyph boolean`** 指定在字体支持时是否将 MSZ（中等大小；半宽）字符替换为半宽字形。该选项在使用 FreeType 或 DirectWrite 渲染器并配合 Adobe-Japan1 兼容字体时生效，如 IBM Plex Sans JP、Morisawa BIZ UDGothic、Morisawa BIZ UDMincho、Yu Gothic、Yu Mincho 和 Meiryo。

  默认为 \<true\>。

- **`-canvas_size image_size`** 指定字幕渲染目标画布的分辨率；通常应为输入视频的帧大小。该选项仅在 `-subtitle_type` 设为 \<bitmap\> 时适用。

  libaribcaption 解码器假定 bitmap 渲染的输入帧大小如下：

  1.  PROFILE_A：1440 x 1080，SAR (PAR) 4:3

  2.  PROFILE_C：320 x 180，SAR (PAR) 1:1

  若输入视频的实际帧大小与上述假定不符，渲染的字幕可能变形。要使字幕不变形，请添加 `-canvas_size` 选项以指定实际输入视频大小。

  注意：对于尺寸不同但宽高比相同的视频，无需 `-canvas_size` 选项。此时若未指定 `-canvas_size`，字幕将被拉伸或收缩到实际视频大小。若 `-canvas_size` 指定了不同大小，字幕将按指定大小并以计算出的 SAR 拉伸或收缩。

### libaribcaption 解码器使用示例

用 `ffplay` 工具显示带 ARIB 字幕的 MPEG-TS 文件：

``` text
ffplay -sub_type bitmap MPEG.TS
```

用 `ffplay` 工具显示输入帧大小为 1920x1080 的 MPEG-TS 文件：

``` text
ffplay -sub_type bitmap -canvas_size 1920x1080 MPEG.TS
```

在转码后的视频中嵌入 ARIB 字幕：

``` text
ffmpeg -sub_type bitmap -i src.m2t -filter_complex "[0:v][0:s]overlay" -vcodec h264 dest.mp4
```

## dvbsub

### 选项

- **`compute_clut`**

  | Term | Description                                                      |
  |------|------------------------------------------------------------------|
  | `-2` | 若流中无匹配的 CLUT，则计算一次 clut。          |
  | `-1` | 若流中无匹配的 CLUT，则计算 clut。               |
  | `0`  | 从不计算 CLUT                                               |
  | `1`  | 始终计算 CLUT 并覆盖流中提供的 CLUT。 |

- **`dvb_substream`** 选择 dvb 子流，为 -1 时选择全部子流（默认）。

## dvdsub

该编解码器解码 DVD 使用的位图字幕；同样的字幕也见于 VobSub 文件对和一些 Matroska 文件中。

### 选项

- **`palette`** 指定位图使用的全局调色板。存储于 VobSub 时，调色板通常在索引文件中指定；在 Matroska 中，调色板以与 VobSub 相同的格式存储在编解码器额外数据 (extradata) 中。在 DVD 中，调色板存储在 IFO 文件中，因此从转储的 VOB 文件读取时不可用。

  该选项的格式是一个包含 16 个 24 位十六进制数（不带 0x 前缀）的字符串，各数以逗号分隔，例如 `0d00ee, ee450d, 101010, eaeaea, 0ce60b, ec14ed, ebff0b, 0d617a, 7b7b7b, d1d1d1, 7b2a0e, 0d950c, 0f007b, cf0dec, cfa80c, 7c127b`。

- **`ifo_palette`** 指定从中获取全局调色板的 IFO 文件。（实验性）

- **`forced_subs_only`** 仅解码标记为强制的字幕条目。有些标题在同一轨道中同时含有强制与非强制字幕。将该标志设为 `1` 将只保留强制字幕。默认值为 `0`。

## libzvbi-teletext

Libzvbi 允许 libavcodec 解码 DVB 图文电视页和 DVB 图文电视字幕。配置期间需要 libzvbi 头文件与库。需要以 `--enable-libzvbi` 显式配置构建。

### 选项

- **`txt_page`** 要解码的图文电视页号列表。不匹配指定列表的页将被丢弃。可使用特殊字符串 `*` 匹配所有页，或 `subtitle` 匹配所有字幕页。默认值为 \*。

- **`txt_default_region`** 设置解码使用的默认字符集，取值介于 0 与 87 之间（参见 ETS 300 706 第 15 节表 32）。默认值为 -1，即不覆盖 libzvbi 默认值。某些无法指示正确字符集的老旧 1.0 级传输需要该选项。

- **`txt_chop_top`** 丢弃顶部图文电视行。默认值为 1。

- **`txt_format`** 指定解码后字幕的格式。

  - **`bitmap`** 默认格式，图文电视页应使用它，因为某些图形和颜色无法用简单文本甚至 ASS 表达。

  - **`text`** 不带格式的简单文本输出。

  - **`ass`** 格式化的 ASS 输出，字幕页与图文电视页以不同样式返回，字幕页被精简为文本，但会尽量保持文本对齐与格式。

- **`txt_left`** 生成位图的 X 偏移，默认为 0。

- **`txt_top`** 生成位图的 Y 偏移，默认为 0。

- **`txt_chop_spaces`** 去除生成文本的首尾空格并删除空行。该选项对基于图文电视的字幕很有用，因为由于双倍大小的图文电视字符，行首或行尾可能出现空白，字幕行之间可能出现空行。默认值为 1。

- **`txt_duration`** 以毫秒为单位设置解码后的图文电视页或字幕的显示时长。默认值为 -1，表示无限或持续到下一个字幕事件到来。

- **`txt_transparent`** 强制生成的图文电视位图使用透明背景。默认值为 0，即不透明背景。

- **`txt_opacity`** 设置图文电视背景的不透明度 (0-255)。未设置 `txt_transparent` 时，它只影响起始框与结束框之间的字符（通常是字幕）。设置 `txt_transparent` 时默认值为 0，否则为 255。

# 编码器

编码器是 FFmpeg 中的已配置组件，用于编码多媒体流。

配置 FFmpeg 构建时，所有受支持的原生编码器默认启用。需要外部库的编码器必须通过相应的 `--enable-lib` 选项手动启用。可使用 configure 选项 `--list-encoders` 列出全部可用编码器。

可用 configure 选项 `--disable-encoders` 禁用全部编码器，并用选项 `--enable-encoder=ENCODER` / `--disable-encoder=ENCODER` 选择性地启用/禁用单个编码器。

ff\* 工具的 `-encoders` 选项会显示已启用的编码器列表。

# 音频编码器

以下描述部分当前可用的音频编码器。

## aac

Advanced Audio Coding (AAC) 编码器。

该编码器是默认的 AAC 编码器，由 FFmpeg 原生实现。

### 选项

- **`b`** 以比特/秒为单位设置码率。设置它会自动激活恒定码率 (CBR) 模式。未指定该选项时设为 128kbps。

- **`q`** 设置可变码率 (VBR) 模式的质量。该选项仅在使用 `ffmpeg` 命令行工具时有效。库接口用户请使用 `global_quality`。

- **`cutoff`** 设置截止频率。未指定时将允许编码器动态调整截止值，以提升低码率下的清晰度。

- **`aac_coder`** 设置 AAC 编码器编码方法。可取的值：

  - **`twoloop`** 双循环搜索 (TLS) 方法。这是默认方法。

    该方法先根据频带阈值设置量化器，然后尝试通过为所有量化器加减一个特定值并微调某些单独量化器来寻找最优组合。会依据 `aac_is`、`aac_ms` 与 `aac_pns` 是否启用而自行调整。

  - **`anmr`** 掩蔽比平均噪声 (ANMR) 基于网格的解法。

    这是一个实验性编码器，目前质量较低、更不稳定且比默认的 twoloop 编码器慢，但具有潜力。目前不支持 `aac_is` 或 `aac_pns` 选项。当前不推荐使用。

  - **`fast`** 恒定量化器方法。

    使用 twoloop 算法的廉价版本，不做那么多巧妙的调整。低码率（低于 64kbps）时表现较差，但高码率时更好且快得多。

- **`aac_ms`** 设置中/侧 (mid/side) 编码模式。默认值 "auto" 会自动对能从中受益的频带使用 M/S。可用值 "enable" 对所有频带强制启用（主要用于调试），或用 "disable" 禁用。

- **`aac_is`** 设置强度立体声编码工具的使用。默认启用，若有益会自动对相似的立体声频带对切换 IS。调试时可将值设为 "disable" 以禁用。

- **`aac_pns`** 在解码过程中使用感知噪声替换，将低熵高频带替换为不可感知的白噪声。默认启用，调试时可用 "disable" 禁用。

- **`aac_tns`** 启用跨越高频带的多抽头 FIR 滤波器，在编码过程中隐藏量化噪声，并由解码器还原。这不仅能减少高频段令人不快的伪影，还能降低高频带的熵，让中低频带使用更多比特。默认启用，调试时可将该选项设为 "disable" 禁用。

- **`aac_ltp`** 启用长期预测扩展，它通过在帧间各频带延展恒定谐波峰值，提升极低带宽情形（如语音或独奏钢琴音乐编码）下的编码效率。profile:a aac_low 隐含该选项。配合 `-ar` 使用可降低采样率。

- **`profile`** 设置编码 profile，可取的值：

  - **`aac_low`** 默认值，AAC "低复杂度" profile。兼容性最好，质量尚可。

  - **`mpeg2_aac_low`** 等价于 `-profile:a aac_low -aac_pns 0`。PNS 随 MPEG4 规范引入。

  - **`aac_ltp`** 长期预测 profile，由它启用并会启用 `aac_ltp` 选项。随 MPEG4 引入。

  未指定该选项时设为 `aac_low`。

## ac3 and ac3_fixed

AC-3 音频编码器。

这些编码器实现 ATSC A/52:2010 与 ETSI TS 102 366 的一部分。

\<ac3\> 编码器使用浮点数学，而 \<ac3_fixed\> 编码器只使用定点整数数学。这并不意味着谁总是更快，只是二者中某一方可能更适合特定系统。\<ac3_fixed\> 编码器不是任何输出格式的默认编解码器，因此必须通过选项 `-acodec ac3_fixed` 显式指定才能使用。

### AC-3 元数据

AC-3 元数据选项用于设置描述音频的参数，但在多数情况下不影响音频编码本身。其中一些选项会直接影响或左右最终比特流的解码与播放，另一些仅作信息用途。少数选项会向输出流添加本可用于音频数据的比特，从而影响输出质量。这类选项会在下面的选项列表中相应标注。

这些参数在多份公开文档中有详细描述。

- [A/52:2010 - 数字音频压缩 (AC-3) (E-AC-3) 标准](http://www.atsc.org/cms/standards/a_52-2010.pdf)

- [A/54 - ATSC 数字电视标准使用指南](http://www.atsc.org/cms/standards/a_54a_with_corr_1.pdf)

- [Dolby 元数据指南](http://www.dolby.com/uploadedFiles/zz-_Shared_Assets/English_PDFs/Professional/18_Metadata.Guide.pdf)

- [Dolby Digital 专业编码指南](http://www.dolby.com/uploadedFiles/zz-_Shared_Assets/English_PDFs/Professional/46_DDEncodingGuidelines.pdf)

#### 元数据控制选项

- **`-per_frame_metadata boolean`** 允许逐帧元数据。指定编码器是否应逐帧检查元数据变化。

  - **`0`** 初始化时设置的元数据值将用于流中的每一帧。（默认）

  - **`1`** 编码每帧之前可更改元数据值。

#### 下混电平

- **`-center_mixlev level`** 中置混音电平。下混到立体声时解码器应应用到中置声道的增益量。仅当存在中置声道时该字段才会写入比特流。值以缩放因子指定。有 3 个有效值：

  | Term    | Description                 |
  |---------|-----------------------------|
  | `0.707` | 应用 -3dB 增益             |
  | `0.595` | 应用 -4.5dB 增益（默认） |
  | `0.500` | 应用 -6dB 增益             |

- **`-surround_mixlev level`** 环绕混音电平。下混到立体声时解码器应应用到环绕声道（一个或多个）的增益量。仅当存在一个或多个环绕声道时该字段才会写入比特流。值以缩放因子指定。有 3 个有效值：

  | Term    | Description                 |
  |---------|-----------------------------|
  | `0.707` | 应用 -3dB 增益             |
  | `0.500` | 应用 -6dB 增益（默认）   |
  | `0.000` | 静音环绕声道 |

#### 音频制作信息

音频制作信息是描述混音环境的可选信息。两个字段要么都不写入比特流，要么都写入。

- **`-mixing_level number`** 混音电平。指定混音母带制作时生产环境的峰值声压级 (SPL)。有效值为 80 到 111，或 -1 表示未知/未指示。默认值为 -1，但若音频制作信息写入比特流则不能使用该值。因此，若 `room_type` 选项不是默认值，`mixing_level` 选项不得为 -1。

- **`-room_type type`** 房间类型。描述在录音室或配音棚进行最终混音时使用的均衡。大房间指采用行业标准 X 曲线均衡的配音棚；小房间采用平坦均衡。若 `mixing_level` 选项与 `room_type` 选项均为默认值，该字段不会写入比特流。

  - **`0`** 未指示（默认）

  - **`1`** 大房间

  - **`2`** 小房间

#### 其他元数据选项

- **`-copyright boolean`** 版权指示。指定此音频是否存在版权。

  - **`0`** 无版权（默认）

  - **`1`** 有版权

- **`-dialnorm value`** 对话归一化。指示节目的平均对话电平低于数字 100% 满刻度 (0 dBFS) 多少。该参数决定音频再现期间的一个电平偏移，将对话的平均音量设到预定电平。目标是匹配不同节目源之间的音量。取 -31dB 时，音频再现期间相对源音量不发生音量变化。有效值为 -31 到 -1 范围内的整数，默认 -31。

- **`-dsur_mode mode`** Dolby Surround 模式。指定立体声信号是否使用 Dolby Surround (Pro Logic)。仅当音频流为立体声时该字段才会写入比特流。使用该选项**并不**意味着编码器会真正应用 Dolby Surround 处理。

  - **`0`** 未指示（默认）

  - **`1`** 未以 Dolby Surround 编码

  - **`2`** 以 Dolby Surround 编码

- **`-original boolean`** 原始比特流指示。指定此音频是否来自原始源而非副本。

  - **`0`** 非原始源

  - **`1`** 原始源（默认）

### 扩展比特流信息

扩展比特流选项是 A/52:2010 标准附录 D 规定的替代比特流语法 (Alternate Bit Stream Syntax) 的一部分。它分为两部分。若组内任一参数被指定，该组中的全部值都会写入比特流。已写入但未指定的值使用默认值。若写入了混音电平，支持替代比特流语法的解码器将使用这些值，而非 `center_mixlev` 和 `surround_mixlev` 选项中指定的值。

#### 扩展比特流信息 - 第 1 部分

- **`-dmix_mode mode`** 首选立体声下混模式。允许用户选择 Lt/Rt（Dolby Surround）或 Lo/Ro（普通立体声）作为首选立体声下混模式。

  - **`0`** 未指示（默认）

  - **`1`** 首选 Lt/Rt 下混

  - **`2`** 首选 Lo/Ro 下混

- **`-ltrt_cmixlev level`** Lt/Rt 中置混音电平。Lt/Rt 模式下混到立体声时解码器应应用到中置声道的增益量。

  | Term    | Description                 |
  |---------|-----------------------------|
  | `1.414` | 应用 +3dB 增益             |
  | `1.189` | 应用 +1.5dB 增益           |
  | `1.000` | 应用 0dB 增益              |
  | `0.841` | 应用 -1.5dB 增益           |
  | `0.707` | 应用 -3.0dB 增益           |
  | `0.595` | 应用 -4.5dB 增益（默认） |
  | `0.500` | 应用 -6.0dB 增益           |
  | `0.000` | 静音中置声道      |

- **`-ltrt_surmixlev level`** Lt/Rt 环绕混音电平。Lt/Rt 模式下混到立体声时解码器应应用到环绕声道（一个或多个）的增益量。

  | Term    | Description                 |
  |---------|-----------------------------|
  | `0.841` | 应用 -1.5dB 增益           |
  | `0.707` | 应用 -3.0dB 增益           |
  | `0.595` | 应用 -4.5dB 增益           |
  | `0.500` | 应用 -6.0dB 增益（默认） |
  | `0.000` | 静音环绕声道 |

- **`-loro_cmixlev level`** Lo/Ro 中置混音电平。Lo/Ro 模式下混到立体声时解码器应应用到中置声道的增益量。

  | Term    | Description                 |
  |---------|-----------------------------|
  | `1.414` | 应用 +3dB 增益             |
  | `1.189` | 应用 +1.5dB 增益           |
  | `1.000` | 应用 0dB 增益              |
  | `0.841` | 应用 -1.5dB 增益           |
  | `0.707` | 应用 -3.0dB 增益           |
  | `0.595` | 应用 -4.5dB 增益（默认） |
  | `0.500` | 应用 -6.0dB 增益           |
  | `0.000` | 静音中置声道      |

- **`-loro_surmixlev level`** Lo/Ro 环绕混音电平。Lo/Ro 模式下混到立体声时解码器应应用到环绕声道（一个或多个）的增益量。

  | Term    | Description                 |
  |---------|-----------------------------|
  | `0.841` | 应用 -1.5dB 增益           |
  | `0.707` | 应用 -3.0dB 增益           |
  | `0.595` | 应用 -4.5dB 增益           |
  | `0.500` | 应用 -6.0dB 增益（默认） |
  | `0.000` | 静音环绕声道 |

#### 扩展比特流信息 - 第 2 部分

- **`-dsurex_mode mode`** Dolby Surround EX 模式。指示流是否使用 Dolby Surround EX（7.1 矩阵化到 5.1）。使用该选项**并不**意味着编码器会真正应用 Dolby Surround EX 处理。

  - **`0`** 未指示（默认）

  - **`1`** Dolby Surround EX 关

  - **`2`** Dolby Surround EX 开

- **`-dheadphone_mode mode`** Dolby Headphone 模式。指示流是否使用 Dolby Headphone 编码（多声道矩阵化到 2.0 供耳机使用）。使用该选项**并不**意味着编码器会真正应用 Dolby Headphone 处理。

  - **`0`** 未指示（默认）

  - **`1`** Dolby Headphone 关

  - **`2`** Dolby Headphone 开

- **`-ad_conv_type type`** A/D 转换器类型。指示音频是否经过了 HDCD A/D 转换。

  - **`0`** 标准 A/D 转换器（默认）

  - **`1`** HDCD A/D 转换器

### 其他 AC-3 编码选项

- **`-stereo_rematrixing boolean`** 立体声重矩阵化。启用/禁用对立体声输入使用重矩阵化。这是一项可选的 AC-3 特性，通过选择性地将左/右声道编码为中/侧来提升质量。该选项默认启用，强烈建议保持启用，除非用于测试。

- **`cutoff frequency`** 设置低通截止频率。未指定时，编码器会依据其他编码参数选择默认值。

### 仅浮点 AC-3 编码选项

这些选项仅对浮点编码器有效，定点编码器不存在这些选项，因为相应特性未在定点实现中实现。

- **`-channel_coupling boolean`** 启用/禁用声道耦合，这是一项可选的 AC-3 特性，通过把多个声道的高频信息合并到单一声道来提升质量。各声道的高频信息在频域和时域都以较低精度发送。这让更多比特可用于较低频率，同时保留足够信息以重建高频。该选项对浮点编码器默认启用，一般应保持启用，除非用于测试或需要提高编码速度。

  - **`-1`** 由编码器选择（默认）

  - **`0`** 禁用声道耦合

  - **`1`** 启用声道耦合

- **`-cpl_start_band number`** 耦合起始频带。设置声道耦合起始频带，取值 1 到 15。若使用的值高于带宽，将被减为耦合结束频带减 1。使用 \<auto\> 时，起始频带由编码器依据码率、采样率和声道布局确定。声道耦合被禁用时该选项无效。

  - **`-1`** 由编码器选择（默认）

## flac

FLAC (Free Lossless Audio Codec) 编码器

### 选项

FFmpeg 的 flac 编码器支持以下选项。

- **`compression_level`** 设置压缩级别，若其他选项未显式设置，它将为许多其他选项选择默认值。有效值为 0 到 12，默认 5。

- **`frame_size`** 以每声道采样数为单位设置帧大小。

- **`lpc_coeff_precision`** 设置 LPC 系数精度，有效值为 1 到 15，默认 15。

- **`lpc_type`** 设置第一级 LPC 算法

  - **`none`** 不使用 LPC

  - **`fixed`** 固定 LPC 系数

  - **`levinson`**

  - **`cholesky`**

- **`lpc_passes`** LPC 分析期间 Cholesky 分解使用的遍数

- **`min_partition_order`** 最小分区阶数

- **`max_partition_order`** 最大分区阶数

- **`prediction_order_method`**

  - **`estimation`**

  - **`2level`**

  - **`4level`**

  - **`8level`**

  - **`search`** 暴力搜索

  - **`log`**

- **`ch_mode`** 声道模式

  - **`auto`** 每帧自动选择模式

  - **`indep`** 各声道独立编码

  - **`left_side`**

  - **`right_side`**

  - **`mid_side`**

- **`exact_rice_parameters`** 选择 rice 参数按精确方式还是近似方式计算。设为 1 时精确选择，会略微降低速度并略微提升压缩率。

- **`multi_dim_quant`** 多维量化。设为 1 时在第一级之后应用第二级 LPC 算法来微调系数。相当慢，但略微提升压缩率。

## opus

Opus 编码器。

这是 FFmpeg 针对 Opus 格式的原生编码器。目前仍在开发中，只实现了该编解码器的 CELT 部分。其质量通常较差，最好情况下与 libopus 编码器持平。

### 选项

- **`b`** 以比特/秒为单位设置码率。未指定时依据声道数和布局作出较优估计。

- **`opus_delay`** 以毫秒为单位设置最大延迟。低于 20ms 的延迟会非常快地降低质量。

## libfdk_aac

libfdk-aac AAC (Advanced Audio Coding) 编码器封装器。

libfdk-aac 库基于 Android 项目的 Fraunhofer FDK AAC 代码。

要求配置期间存在 libfdk-aac 头文件与库。需要以 `--enable-libfdk-aac` 显式配置构建。该库与 GPL 不兼容，因此若允许使用 GPL，应以 `--enable-gpl --enable-nonfree --enable-libfdk-aac` 配置。

该编码器支持 AAC-HE profile。

通过 `vbr` 或 `flags +qscale` 选项启用的 VBR 编码是实验性的，仅在某些参数组合下有效。

仅 libfdk-aac 0.1.3 及更高版本支持编码 7.1 音频。

更多信息参见 fdk-aac 项目：<http://sourceforge.net/p/opencore-amr/fdk-aac/>。

### 选项

以下选项映射到 FFmpeg 共享编解码器选项。

- **`b`** 以比特/秒为单位设置码率。未显式指定码率时，会依据所选 profile 自动设为合适的值。

  VBR 模式启用时该选项被忽略。

- **`ar`** 设置音频采样率（单位为 Hz）。

- **`channels`** 设置音频声道数。

- **`flags +qscale`** 启用固定质量 VBR（可变码率）模式。注意 `vbr` 值为正时 VBR 已隐式启用。

- **`cutoff`** 设置截止频率。未指定（或显式设为 0）时将使用库自动计算的值。默认值为 0。

- **`profile`** 设置音频 profile。

  可识别以下 profile：

  | Term          | Description                              |
  |---------------|------------------------------------------|
  | `aac_low`   | 低复杂度 AAC (LC)                  |
  | `aac_he`    | 高效率 AAC (HE-AAC)             |
  | `aac_he_v2` | 高效率 AAC 第 2 版 (HE-AACv2) |
  | `aac_ld`    | 低延迟 AAC (LD)                       |
  | `aac_eld`   | 增强低延迟 AAC (ELD)             |

  未指定时设为 `aac_low`。

以下是 libfdk_aac 编码器的私有选项。

- **`afterburner`** 设为 1 启用 afterburner 特性，设为 0 禁用。它提升质量，但也提升所需处理能力。

  默认值为 1。

- **`eld_sbr`** 设为 1 为 ELD 启用 SBR（频带复制），设为 0 禁用。

  默认值为 0。

- **`eld_v2`** 设为 1 为 ELDv2 启用（ELD 立体声信号的 LD-MPS 扩展），设为 0 禁用。

  注意该选项仅在 fdk-aac 版本 (AACENCODER_LIB_VL0.AACENCODER_LIB_VL1.AACENCODER_LIB_VL2) \> (4.0.0) 时可用。

  默认值为 0。

- **`signaling`** 设置 SBR/PS 信号传递方式。

  可取以下值之一：

  - **`default`** 隐式选择信号传递方式（默认为显式分层式，全局头被禁用时为隐式）

  - **`implicit`** 隐式向后兼容的信号传递

  - **`explicit_sbr`** 显式 SBR，隐式 PS 信号传递

  - **`explicit_hierarchical`** 显式分层信号传递

  默认值为 `default`。

- **`latm`** 设为 1 输出 LATM/LOAS 封装数据，设为 0 禁用。

  默认值为 0。

- **`header_period`** 设置 StreamMuxConfig 与 PCE 的重复周期（以帧为单位），用于在 LATM/LOAS 传输层内发送带内配置缓冲区。

  必须是 16 位非负整数。

  默认值为 0。

- **`vbr`** 设置 VBR 模式，取值 1 到 5。1 是最低质量（尽管仍相当好），5 是最高质量。取 0 将禁用 VBR，启用 CBR（恒定码率）。

  目前仅 `aac_low` profile 支持 VBR 编码。

  VBR 模式 1-5 大致对应以下平均码率：

  | Term  | Description              |
  |-------|--------------------------|
  | `1` | 32 kbps/声道          |
  | `2` | 40 kbps/声道          |
  | `3` | 48-56 kbps/声道       |
  | `4` | 64 kbps/声道          |
  | `5` | 约 80-96 kbps/声道 |

  默认值为 0。

- **`frame_length`** 以采样数为单位设置音频帧长度。默认值为库的内部默认值。支持的取值请查阅库文档。

### 示例

- 用 `ffmpeg` 将音频文件转换为 M4A (MP4) 容器中的 VBR AAC：

  ``` text
  ffmpeg -i input.wav -codec:a libfdk_aac -vbr 3 output.m4a
  ```

- 用 `ffmpeg` 将音频文件转换为 CBR 64k kbps AAC，使用高效率 AAC profile：

  ``` text
  ffmpeg -i input.wav -c:a libfdk_aac -profile:a aac_he -b:a 64k output.m4a
  ```

## liblc3

liblc3 LC3 (Low Complexity Communication Codec) 编码器封装器。

要求配置期间存在 liblc3 头文件与库。需要以 `--enable-liblc3` 显式配置构建。

该编码器支持用于 LE Audio 协议的 Bluetooth SIG LC3 编解码器，以及 LC3plus 的以下特性：

- 2.5 与 5ms 帧时长。

- 高分辨率模式，48 KHz 与 96 kHz 采样率。

更多信息参见 liblc3 项目：<https://github.com/google/liblc3>。

### 选项

以下选项映射到 FFmpeg 共享编解码器选项。

- **`b bitrate`** 以比特/秒为单位设置码率。对选定的帧时长，这将决定编码帧的固定大小。

- **`ar frequency`** 设置音频采样率（单位为 Hz）。

- **`channels`** 设置音频声道数。

- **`frame_duration`** 以毫秒为单位设置音频帧时长。默认值为 10ms。允许的帧时长为 2.5ms、5ms、7.5ms 和 10ms。LC3（Bluetooth LE Audio）允许 7.5ms 与 10ms；LC3plus 为 2.5ms、5ms 与 10ms。

  10ms 帧时长在 LC3 与 LC3plus 标准中都可用。此模式下产出的比特流既可称为 LC3 也可称为 LC3plus。

- **`high_resolution boolean`** 设为 1 启用高分辨率模式。高分辨率模式适用于所有 LC3plus 帧时长，以及 48 KHz 与 96 KHz 采样率。

  编码器在较低采样率下自动关闭该模式，并在 96 KHz 时激活它。

  高码率下应优先使用该模式。此模式下音频带宽始终达到奈奎斯特频率，而 48 KHz 的 LC3 将带宽限制在 20 KHz。

## libmp3lame

LAME (Lame Ain't an MP3 Encoder) MP3 编码器封装器。

要求配置期间存在 libmp3lame 头文件与库。需要以 `--enable-libmp3lame` 显式配置构建。

定点 MP3 编码器参见 [libshine](#libshine)，但质量较低。

### 选项

libmp3lame 封装器支持以下选项。括号中列出 `lame` 等价选项。

- **`b (-b)`** 以比特/秒为单位设置 CBR 或 ABR 的码率。LAME 的 `bitrate` 以千比特/秒表示。

- **`q (-V)`** 为 VBR 设置恒定质量。该选项仅在使用 `ffmpeg` 命令行工具时有效。库接口用户请使用 `global_quality`。

- **`compression_level (-q)`** 设置算法质量。有效参数为 0-9 范围内的整数，0 表示质量最高但最慢，9 表示最快但质量最差。

- **`cutoff (--lowpass)`** 设置低通截止频率。未指定时编码器动态调整截止值。

- **`reservoir`** 设为 1 启用比特储备池。默认值为 1。LAME 默认启用它，但可用 `--nores` 选项覆盖。

- **`joint_stereo (-m j)`** 允许编码器（逐帧）使用 L/R 立体声或中/侧立体声。默认值为 1。

- **`abr (--abr)`** 设为 1 允许编码器使用 ABR。`lame` 的 `--abr` 设置目标码率，而该选项只告知 FFmpeg 使用 ABR，码率仍依赖 `b` 设置。

- **`copyright (-c)`** 设为 1 时设置 MPEG 音频版权标志。默认值为 0（禁用）。

- **`original (-o)`** 设为 1 时设置 MPEG 音频原始标志。默认值为 1（启用）。

## libopencore-amrnb

OpenCORE Adaptive Multi-Rate Narrowband 编码器。

要求配置期间存在 libopencore-amrnb 头文件与库。需要以 `--enable-libopencore-amrnb --enable-version3` 显式配置构建。

这是仅支持单声道的编码器。官方仅支持 8000Hz 采样率，但可通过将 `strict` 设为 `unofficial` 或更低来覆盖。

### 选项

- **`b`** 以比特/秒为单位设置码率。仅支持以下码率，否则 libavcodec 将就近取整到最近的有效码率。

  - **`4750`**

  - **`5150`**

  - **`5900`**

  - **`6700`**

  - **`7400`**

  - **`7950`**

  - **`10200`**

  - **`12200`**

- **`dtx`** 设为 1 允许非连续传输（生成舒适噪声）。默认值为 0（禁用）。

## libopus

libopus Opus Interactive Audio Codec 编码器封装器。

要求配置期间存在 libopus 头文件与库。需要以 `--enable-libopus` 显式配置构建。

### 选项映射

多数 libopus 选项仿照 opus-tools 的 `opusenc` 工具。下面是选项映射表，描述 libopus 封装器支持的选项及其 `opusenc` 等价选项（括注）。

- **`b (bitrate)`** 以比特/秒为单位设置码率。FFmpeg 的 `b` 选项以比特/秒表示，而 `opusenc` 的 `bitrate` 以千比特/秒表示。

- **`vbr (vbr, hard-cbr, and cvbr)`** 设置 VBR 模式。FFmpeg `vbr` 选项的有效参数如下，括注 `opusenc` 等价选项：

  | Term                   | Description                                   |
  |------------------------|-----------------------------------------------|
  | `off (hard-cbr)`     | 使用恒定码率编码。               |
  | `on (vbr)`           | 使用可变码率编码（默认）。 |
  | `constrained (cvbr)` | 使用受约束的可变码率编码。   |

- **`compression_level (comp)`** 设置编码算法复杂度。有效选项为 0-10 范围内的整数。0 编码最快但质量较低，10 质量最高但编码最慢。默认值为 10。

- **`frame_duration (framesize)`** 设置最大帧大小，即帧的毫秒时长。参数必须恰好为以下之一：2.5、5、10、20、40、60。更小的帧大小实现更低延迟，但在给定码率下质量更低。大于 20ms 的大小仅在相当低的码率下有意义。默认值为 20ms。

- **`packet_loss (expect-loss)`** 设置预期的丢包百分比。默认值为 0。

- **`fec (n/a)`** 启用带内前向纠错。`packet_loss` 必须非零才能生效——FEC 'side data' 的频率与预期丢包率成正比。默认禁用。

- **`application (N.A.)`** 设置目标应用类型。有效选项如下所列：

  | Term | Description |
  |----|----|
  | `voip` | 偏重提升语音可懂度。 |
  | `audio` | 偏重忠实于输入（默认）。 |
  | `lowdelay` | 通过禁用语音优化模式，限制为仅最低延迟模式。 |

- **`cutoff (N.A.)`** 以 Hz 为单位设置截止带宽。参数必须恰好为以下之一：4000、6000、8000、12000 或 20000，分别对应窄带、中带、宽带、超宽带与全带。默认值为 0（禁用截止）。注意 libopus 对码率 \< 15 kbps 强制宽带截止，除非使用仅 CELT 模式（`application` 设为 `lowdelay`）。

- **`mapping_family (mapping_family)`** 设置编码器使用的声道映射族。默认值 -1 对单声道和立体声输入使用映射族 0，其他输入使用映射族 1。该默认值还会禁用 libopus 的环绕掩蔽与 LFE 带宽优化，并要求输入不超过 8 声道。

  其他取值包括：0 用于单声道和立体声，1 用于带掩蔽与 LFE 带宽优化的环绕声，255 用于声道布局未指定的独立流。

- **`dtx (N.A.)`** 设为 1 允许非连续传输。默认值为 0（禁用）。

- **`apply_phase_inv (N.A.) (requires libopus >= 1.2)`** 设为 0 时禁用强度立体声的相位反转，提升单声道下混的质量，但略微降低普通立体声质量。默认值为 1（启用相位反转）。

## libshine

Shine 定点 MP3 编码器封装器。

Shine 是定点 MP3 编码器。它在没有 FPU 的平台（如 armel CPU、部分手机与平板）上性能好得多。但它更注重性能而非质量，质量上不及 LAME 等生产级编码器。此外，据项目主页所述，该编码器可能并非没有缺陷——代码编写于很久以前，项目已死至少 5 年。

该编码器仅支持立体声与单声道输入，且仅支持 CBR。

原始项目（最后更新于 2007 年初）位于 <http://sourceforge.net/projects/libshine-fxp/>。我们仅支持 Savonet/Liquidsoap 项目维护的更新分支：<https://github.com/savonet/shine>。

要求配置期间存在 libshine 头文件与库。需要以 `--enable-libshine` 显式配置构建。

另请参见 [libmp3lame](#libmp3lame)。

### 选项

libshine 封装器支持以下选项。括号中列出 `shineenc` 等价选项。

- **`b (-b)`** 以比特/秒为单位设置 CBR 码率。`shineenc` 的 `-b` 选项以千比特/秒表示。

## libtwolame

TwoLAME MP2 编码器封装器。

要求配置期间存在 libtwolame 头文件与库。需要以 `--enable-libtwolame` 显式配置构建。

### 选项

libtwolame 封装器支持以下选项。`twolame` 等价选项跟随 FFmpeg 选项之后，括注于括号中。

- **`b (-b)`** 以比特/秒为单位设置 CBR 码率。`twolame` 的 `b` 选项以千比特/秒表示。默认值为 128k。

- **`q (-V)`** 为实验性 VBR 支持设置质量。最大取值范围 -50 到 50，实用范围 -10 到 10。值越高质量越好。该选项仅在使用 `ffmpeg` 命令行工具时有效。库接口用户请使用 `global_quality`。

- **`mode (--mode)`** 设置产出音频的模式。可取的值：

  | Term | Description |
  |----|----|
  | `auto` | 依据输入自动选择模式。这是默认值。 |
  | `stereo` | 立体声 |
  | `joint_stereo` | 联合立体声 |
  | `dual_channel` | 双声道 |
  | `mono` | 单声道 |

- **`psymodel (--psyc-mode)`** 设置编码使用的心理声学模型。参数必须是 -1 到 4（含）之间的整数。值越高质量越好。默认值为 3。

- **`energy_levels (--energy)`** 设为 1 启用能量级别扩展。默认值为 0（禁用）。

- **`error_protection (--protect)`** 设为 1 启用 CRC 错误保护。默认值为 0（禁用）。

- **`copyright (--copyright)`** 设为 1 时设置 MPEG 音频版权标志。默认值为 0（禁用）。

- **`original (--original)`** 设为 1 时设置 MPEG 音频原始标志。默认值为 0（禁用）。

## libvo-amrwbenc

VisualOn Adaptive Multi-Rate Wideband 编码器。

要求配置期间存在 libvo-amrwbenc 头文件与库。需要以 `--enable-libvo-amrwbenc --enable-version3` 显式配置构建。

这是仅支持单声道的编码器。官方仅支持 16000Hz 采样率，但可通过将 `strict` 设为 `unofficial` 或更低来覆盖。

### 选项

- **`b`** 以比特/秒为单位设置码率。仅支持以下码率，否则 libavcodec 将就近取整到最近的有效码率。

  - **`6600`**

  - **`8850`**

  - **`12650`**

  - **`14250`**

  - **`15850`**

  - **`18250`**

  - **`19850`**

  - **`23050`**

  - **`23850`**

- **`dtx`** 设为 1 允许非连续传输（生成舒适噪声）。默认值为 0（禁用）。

## libvorbis

libvorbis 编码器封装器。

要求配置期间存在 libvorbisenc 头文件与库。需要以 `--enable-libvorbis` 显式配置构建。

### 选项

libvorbis 封装器支持以下选项。括号中列出 `oggenc` 等价选项。

要获得更准确、更全面的 libvorbis 选项文档，请查阅 libvorbisenc 与 `oggenc` 的文档。参见 <http://xiph.org/vorbis/>、<http://wiki.xiph.org/Vorbis-tools> 与 oggenc(1)。

- **`b (-b)`** 以比特/秒为单位设置 ABR 码率。`oggenc` 的 `-b` 以千比特/秒表示。

- **`q (-q)`** 为 VBR 设置恒定质量。值应为 -1.0 到 10.0 范围内的浮点数。值越高质量越好。默认值为 `3.0`。

  该选项仅在使用 `ffmpeg` 命令行工具时有效。库接口用户请使用 `global_quality`。

- **`cutoff (--advanced-encode-option lowpass_frequency=N)`** 以 Hz 为单位设置截止带宽，取 0 禁用截止。`oggenc` 的相应选项以 kHz 表示。默认值为 `0`（禁用截止）。

- **`minrate (-m)`** 以比特/秒为单位设置最小码率。`oggenc` 的 `-m` 以千比特/秒表示。

- **`maxrate (-M)`** 以比特/秒为单位设置最大码率。`oggenc` 的 `-M` 以千比特/秒表示。它仅对 ABR 模式生效。

- **`iblock (--advanced-encode-option impulse_noisetune=N)`** 为冲击块设置噪声底偏置。值为 -15.0 到 0.0 的浮点数。负偏置指示编码器特别关注编码音频中瞬态的清晰度。更好瞬态响应的代价是更高的码率。

## mjpeg

Motion JPEG 编码器。

### 选项

- **`huffman`** 设置 huffman 编码策略。可取的值：

  | Term        | Description                                                   |
  |-------------|---------------------------------------------------------------|
  | `default` | 使用默认 huffman 表。这是默认策略。 |
  | `optimal` | 计算并使用最优 huffman 表。                       |

## wavpack

WavPack 无损音频编码器。

### 选项

括号中列出 `wavpack` 命令行工具的等价选项。

#### 共享选项

以下共享选项对该编码器生效。此处仅记录该编码器特有的注意事项。选项的一般含义参见[编解码器选项](#codec_002doptions)章节。

- **`frame_size (--blocksize)`** 对该编码器，该选项的取值范围为 128 到 131072。默认值依据采样率和声道数自动决定。

  默认值的完整计算公式参见 `libavcodec/wavpackenc.c`。

- **`compression_level (-f, -h, -hh, and -x)`**

#### 私有选项

- **`joint_stereo (-j)`** 设置是否启用联合立体声。有效值：

  | Term        | Description                           |
  |-------------|---------------------------------------|
  | `on (1)`  | 强制中/侧音频编码。        |
  | `off (0)` | 强制左/右音频编码。      |
  | `auto`    | 由编码器自动决定。 |

- **`optimize_mono`** 设置是否启用单声道优化。该选项仅对非单声道流生效。可用值：

  | Term    | Description |
  |---------|-------------|
  | `on`  | 启用     |
  | `off` | 禁用    |

# 视频编码器

以下描述部分当前可用的视频编码器。

## a64_multi, a64_multi5

A64 / Commodore 64 多彩字符集编码器。`a64_multi5` 扩展了第 5 种颜色 (colram)。

## Cinepak

Cinepak（又称 CVID）编码器。兼容 Windows 3.1 与早期 MacOS。

### 选项

- **`g integer`** 关键帧间隔。每 `-g` 帧至少插入一个关键帧，有时更早。

- **`q:v integer`** 质量因子。越低越好。越高码率越低。下表列出以 `-g 100` 编码 akiyo_cif.y4m 时不同 `-q:v` 值的码率：

  - **`-q:v 1 1918 kb/s`**

  - **`-q:v 2 1735 kb/s`**

  - **`-q:v 4 1500 kb/s`**

  - **`-q:v 10 1041 kb/s`**

  - **`-q:v 20 826 kb/s`**

  - **`-q:v 40 553 kb/s`**

  - **`-q:v 100 394 kb/s`**

  - **`-q:v 200 312 kb/s`**

  - **`-q:v 400 266 kb/s`**

  - **`-q:v 1000 237 kb/s`**

- **`max_extra_cb_iterations integer`** 额外码书重算遍数的最大值，越多越好但越慢。

- **`skip_empty_cb boolean`** 避免浪费字节，忽略早期 MacOS 解码器。

- **`max_strips integer`** 使用的条带最小与最大数量。更宽的范围有时能提升质量。条带越多通常质量越好但消耗更多比特。条带越少往往产生更多关键帧。兼容早期版本为 1..3。

- **`strip_number_adaptivity integer`** 帧间允许条带数量变化的幅度。越高越好但越慢。

## ffv1

FFv1 编码器

### 选项

FFmpeg 的 FFv1 编码器支持以下选项。

- **`context`** 设置上下文大小，0（默认）为小，1 为大。

- **`coder`** 设置编码器，

  | Term          | Description                    |
  |---------------|--------------------------------|
  | `rice`      | Golomb rice 编码器              |
  | `range_def` | 使用默认表的范围编码器 |
  | `range_tab` | 使用自定义表的范围编码器  |

- **`slicecrc`** -1（默认，自动），1 使用初始与终止状态均为零的 crc，2 使用初始与终止状态非零的 crc

- **`qtable`**

  | Term            | Description        |
  |-----------------|--------------------|
  | `default`     | 默认，自动 |
  | `8bit`        | 使用 8bit 默认   |
  | `greater8bit` | 使用 \>8bit 默认 |

- **`remap_optimizer`** 0 - 5，默认 3，编码器在优化重映射表上投入的精力。

## GIF

GIF 图像/动画编码器。

### 选项

- **`gifflags integer`** 设置 GIF 编码使用的标志。

  - **`offsetting`** 启用图像偏移。

    默认启用。

  - **`transdiff`** 启用帧间透明检测。

    默认启用。

- **`gifimage integer`** 启用每帧编码一幅完整 GIF 图像，而非动画 GIF。

  默认值为 `0`。

- **`global_palette integer`** 在可行时向全局 GIF 头写入调色板。

  禁用时每帧都会写入调色板，即使已提供全局调色板。

  默认值为 `1`。

## Hap

Vidvox Hap 视频编码器。

### 选项

- **`format integer`** 指定要编码的 Hap 格式。

  - **`hap`**

  - **`hap_alpha`**

  - **`hap_q`**

  默认值为 `hap`。

- **`chunks integer`** 指定帧拆分成的块数，取值 1 到 64。这允许大帧的多线程解码，但可能以数据率为代价。编码器可能修改该值以均匀划分帧。

  默认值为 \<1\>。

- **`compressor integer`** 指定使用的第二级压缩器。设为 `none` 时 `chunks` 被限制为 1，因为分块的非压缩帧毫无益处。

  - **`none`**

  - **`snappy`**

  默认值为 `snappy`。

## jpeg2000

原生 jpeg 2000 编码器默认为有损，`-q:v` 选项可用于设置编码质量。可用 `-pred 1` 选择无损编码。

### 选项

- **`format integer`** 可设为 `j2k` 或 `jp2`（默认），后者可存储非 rgb 像素格式。

- **`tile_width integer`** 设置瓦片宽度。范围 1 到 1073741824。默认为 256。

- **`tile_height integer`** 设置瓦片高度。范围 1 到 1073741824。默认为 256。

- **`pred integer`** 允许设置离散小波变换 (DWT) 类型

  - **`dwt97int (Lossy)`**

  - **`dwt53 (Lossless)`**

  默认为 `dwt97int`

- **`sop boolean`** 启用后在每个包开头添加 SOP 标记。默认禁用。

- **`eph boolean`** 启用后在每个包头末尾添加 EPH 标记。默认禁用。

- **`prog integer`** 设置编码器使用的渐进顺序。可取的值：

  - **`lrcp`**

  - **`rlcp`**

  - **`rpcl`**

  - **`pcrl`**

  - **`cprl`**

  默认设为 `lrcp`。

- **`layer_rates string`** 默认不使用该选项时，以质量指标进行压缩。该选项允许按压缩比压缩。可为每一层指定压缩比。层 `l` 的压缩比指前 `l` 层所含文件总大小的比例。

  示例用法：

  ``` text
  ffmpeg -i input.bmp -c:v jpeg2000 -layer_rates "100,10,1" output.j2k
  ```

  这会将图像压缩为含 3 层：第一层数据压缩 1000 倍，前两层压缩 100 倍，使用全部 3 层时包含所有数据。

## librav1e

rav1e AV1 编码器封装器。

要求配置期间存在 rav1e 头文件与库。需要以 `--enable-librav1e` 显式配置构建。

### 选项

- **`qmax`** 设置码率模式下使用的最大量化器。

- **`qmin`** 设置码率模式下使用的最小量化器。

- **`qp`** 使用量化器模式以给定量化器 (0-255) 编码。

- **`speed`** 选择编码的速度预设 (0-10)。

- **`tiles`** 选择编码使用的瓦片数。

- **`tile-rows`** 选择编码使用的瓦片行数。

- **`tile-columns`** 选择编码使用的瓦片列数。

- **`rav1e-params`** 使用以":"分隔的 \<key\>=\<value\> 对列表设置 rav1e 选项。选项列表参见 `rav1e --help`。

  例如用 `-rav1e-params` 指定 librav1e 编码选项：

  ``` text
  ffmpeg -i input -c:v librav1e -b:v 500K -rav1e-params speed=5:low_latency=true output.mp4
  ```

## libaom-av1

libaom AV1 编码器封装器。

要求配置期间存在 libaom 头文件与库。需要以 `--enable-libaom` 显式配置构建。

### 选项

该封装器支持以下标准 libavcodec 选项：

- **`b`** 以比特/秒为单位设置码率目标。默认使用可变码率模式。若 `maxrate` 与 `minrate` 也设为相同值，则使用恒定码率模式；若同时设置了 `crf`，则使用受约束质量模式。

- **`g keyint_min`** 设置关键帧布置。GOP 大小设置关键帧之间的最大距离；为零时输出流将仅含帧内帧。除非最小距离与 GOP 大小相同——此时关键帧总是以固定间隔出现——否则最小距离被忽略。默认不设置，因此没有该选项时库对关键帧位置有完全自由的选择。

- **`qmin qmax`** 设置最小/最大量化值。有效范围 0 到 63（警告：这与 AV1 实际使用的量化值不匹配——实际量化值除以四才映射到该范围）。默认为 min/max（无约束）。

- **`minrate maxrate bufsize rc_init_occupancy`** 设置码率控制缓冲参数。不设置时不使用——默认为无约束可变码率。

- **`threads`** 设置编码使用的线程数。可能还需要设置 `tiles` 或 `row-mt` 选项才能真正用满指定数量的线程。默认为主机支持的硬件线程数。

- **`profile`** 设置编码 profile。默认使用与输入位深和色度二次采样匹配的 profile。

该封装器还有一些专属选项：

- **`cpu-used`** 设置质量/编码速度权衡。有效范围 0 到 8，数字越大速度越快、质量越低。默认值为 1，速度慢且质量高。

- **`auto-alt-ref`** 启用交替参考帧。默认使用库的内部默认值。

- **`arnr-max-frames (frames)`** 设置 altref 降噪最大帧数。默认为 -1。

- **`arnr-strength (strength)`** 设置 altref 降噪滤波强度。范围 -1 到 6。默认为 -1。

- **`aq-mode (aq-mode)`** 设置自适应量化模式。可取的值：

  | Term               | Description       |
  |--------------------|-------------------|
  | `none (0)`       | 禁用。         |
  | `variance (1)`   | 基于方差。   |
  | `complexity (2)` | 基于复杂度。 |
  | `cyclic (3)`     | 循环刷新。   |

- **`tune (tune)`** 设置编码器调优所用的失真度量。默认为 `psnr`。

  - **`psnr (0)`**

  - **`ssim (1)`**

- **`lag-in-frames`** 设置编码器为前瞻目的任一时刻可保持在途的最大帧数。默认使用库的内部默认值。

- **`error-resilience`** 启用错误恢复特性：

  | Term      | Description                                        |
  |-----------|----------------------------------------------------|
  | `default` | 提升对整帧丢失的恢复能力。 |

  默认不启用。

- **`crf`** 为恒定质量（无码率目标）与受约束质量（有最大码率目标）模式设置质量/大小权衡。有效范围 0 到 63，数字越大质量越低、输出越小。仅在设置时使用；默认只使用码率目标。

- **`static-thresh`** 为块设置变化阈值，低于它的块将被编码器跳过。以任意单位定义为非负整数，默认为零（不跳过任何块）。

- **`drop-threshold`** 设置接近码率控制边界时丢帧的阈值。定义为目标缓冲区的百分比——当码率控制缓冲区低于该百分比时，将丢帧直到缓冲区重新填充到阈值之上。默认为零（不丢帧）。

- **`denoise-noise-level (level)`** 胶片颗粒合成要去除的噪声量。该选项未设置或设为 0 时禁用颗粒合成。

- **`denoise-block-size (pixels)`** 胶片颗粒合成降噪使用的块大小。未设置时 AV1 编解码器使用默认值 32。

- **`undershoot-pct (pct)`** 设置数据率低于目标码率的（最小）百分比。范围 -1 到 100。默认为 -1。

- **`overshoot-pct (pct)`** 设置数据率超出目标码率的（最大）百分比。范围 -1 到 1000。默认为 -1。

- **`minsection-pct (pct)`** GOP 码率相对目标码率的最小百分比变化。未设置 minsection-pct 时，libaomenc 封装器按 `(minrate * 100 / bitrate)` 计算。范围 -1 到 100。默认为 -1（未设置）。

- **`maxsection-pct (pct)`** GOP 码率相对目标码率的最大百分比变化。未设置 maxsection-pct 时，libaomenc 封装器按 `(maxrate * 100 / bitrate)` 计算。范围 -1 到 5000。默认为 -1（未设置）。

- **`frame-parallel (boolean)`** 启用帧并行可解码特性。默认为 true。

- **`tiles`** 设置编码输入视频使用的瓦片数，格式为 列 x 行。更大的数字允许编码与解码更大的并行度，但可能降低编码效率。默认为输入视频大小所需的最少瓦片数（对不超过 4K 的尺寸这是 1x1，即单瓦片）。

- **`tile-columns tile-rows`** 以瓦片行数与列数的 log2 设置瓦片数。提供它是为了与 libvpx/VP9 兼容。

- **`row-mt (Requires libaom >= 1.0.0-759-g90a15f4f2)`** 启用基于行的多线程。默认禁用。

- **`enable-cdef (boolean)`** 启用受约束方向增强滤波器 (CDEF)。libaom-av1 编码器默认启用 CDEF。

- **`enable-restoration (boolean)`** 启用环路恢复滤波器。libaom-av1 默认为 true。

- **`enable-global-motion (boolean)`** 启用全局运动用于块预测。默认为 true。

- **`enable-intrabc (boolean)`** 启用帧内块预测的块复制模式。该模式对屏幕内容有用。默认为 true。

- **`enable-rect-partitions (boolean) (Requires libaom >= v2.0.0)`** 启用矩形分区。默认为 true。

- **`enable-1to4-partitions (boolean) (Requires libaom >= v2.0.0)`** 启用 1:4/4:1 分区。默认为 true。

- **`enable-ab-partitions (boolean) (Requires libaom >= v2.0.0)`** 启用 AB 形状分区。默认为 true。

- **`enable-angle-delta (boolean) (Requires libaom >= v2.0.0)`** 启用角度增量帧内预测。默认为 true。

- **`enable-cfl-intra (boolean) (Requires libaom >= v2.0.0)`** 启用由亮度预测色度的帧内预测。默认为 true。

- **`enable-filter-intra (boolean) (Requires libaom >= v2.0.0)`** 启用滤波帧内预测器。默认为 true。

- **`enable-intra-edge-filter (boolean) (Requires libaom >= v2.0.0)`** 启用帧内边缘滤波。默认为 true。

- **`enable-smooth-intra (boolean) (Requires libaom >= v2.0.0)`** 启用平滑帧内预测模式。默认为 true。

- **`enable-paeth-intra (boolean) (Requires libaom >= v2.0.0)`** 启用帧内预测中的 paeth 预测器。默认为 true。

- **`enable-palette (boolean) (Requires libaom >= v2.0.0)`** 启用调色板预测模式。默认为 true。

- **`enable-flip-idtx (boolean) (Requires libaom >= v2.0.0)`** 启用扩展变换类型，包括 FLIPADST_DCT、DCT_FLIPADST、FLIPADST_FLIPADST、ADST_FLIPADST、FLIPADST_ADST、IDTX、V_DCT、H_DCT、V_ADST、H_ADST、V_FLIPADST、H_FLIPADST。默认为 true。

- **`enable-tx64 (boolean) (Requires libaom >= v2.0.0)`** 启用 64 点变换。默认为 true。

- **`reduced-tx-type-set (boolean) (Requires libaom >= v2.0.0)`** 使用缩减的变换类型集合。默认为 false。

- **`use-intra-dct-only (boolean) (Requires libaom >= v2.0.0)`** 仅对 INTRA 模式使用 DCT。默认为 false。

- **`use-inter-dct-only (boolean) (Requires libaom >= v2.0.0)`** 仅对 INTER 模式使用 DCT。默认为 false。

- **`use-intra-default-tx-only (boolean) (Requires libaom >= v2.0.0)`** 仅对 INTRA 模式使用默认变换。默认为 false。

- **`enable-ref-frame-mvs (boolean) (Requires libaom >= v2.0.0)`** 启用时域 mv 预测。默认为 true。

- **`enable-reduced-reference-set (boolean) (Requires libaom >= v2.0.0)`** 使用缩减的单参考与复合参考集合。默认为 false。

- **`enable-obmc (boolean) (Requires libaom >= v2.0.0)`** 启用 obmc。默认为 true。

- **`enable-dual-filter (boolean) (Requires libaom >= v2.0.0)`** 启用双重滤波。默认为 true。

- **`enable-diff-wtd-comp (boolean) (Requires libaom >= v2.0.0)`** 启用差值加权复合。默认为 true。

- **`enable-dist-wtd-comp (boolean) (Requires libaom >= v2.0.0)`** 启用距离加权复合。默认为 true。

- **`enable-onesided-comp (boolean) (Requires libaom >= v2.0.0)`** 启用单侧复合。默认为 true。

- **`enable-interinter-wedge (boolean) (Requires libaom >= v2.0.0)`** 启用帧间-帧间楔形复合。默认为 true。

- **`enable-interintra-wedge (boolean) (Requires libaom >= v2.0.0)`** 启用帧间-帧内楔形复合。默认为 true。

- **`enable-masked-comp (boolean) (Requires libaom >= v2.0.0)`** 启用掩蔽复合。默认为 true。

- **`enable-interintra-comp (boolean) (Requires libaom >= v2.0.0)`** 启用帧间-帧内复合。默认为 true。

- **`enable-smooth-interintra (boolean) (Requires libaom >= v2.0.0)`** 启用平滑帧间-帧内模式。默认为 true。

- **`aom-params`** 使用以":"分隔的 \<key\>=\<value\> 对列表设置 libaom 选项。支持的选项列表参见 `aomenc --help` 的"AV1 Specific Options"一节。

  例如用 `-aom-params` 指定 libaom 编码选项：

  ``` text
  ffmpeg -i input -c:v libaom-av1 -b:v 500K -aom-params tune=psnr:enable-tpl-model=1 output.mp4
  ```

## liboapv

Advanced Professional Video 编解码器编码器封装器。

该编码器要求配置期间存在 liboapv 头文件与库。需要以 `--enable-liboapv` 显式配置构建。

许多 liboapv 编码器选项映射到 FFmpeg 全局编解码器选项，而独有的编码器选项通过私有选项提供。

apv 项目网站位于 <https://github.com/AcademySoftwareFoundation/openapv>。

### 选项

liboapv 封装器支持以下选项。

要获得更全面的 liboapv 选项文档，请查阅 liboapv 文档。

- **`preset`** 设置质量-速度权衡 \[fastest, fast, medium, slow, placebo, default\]

- **`qp`** 为 CQP 码率控制模式设置量化参数值。

- **`oapv-params (parse_apv_params)`** 使用以":"分隔的 \<key\>=\<value\> 对列表设置 liboapvenc 选项。接受的参数列表参见 liboapv 编码器用户指南。

## libsvtav1

SVT-AV1 编码器封装器。

要求配置期间存在 SVT-AV1 头文件与库。需要以 `--enable-libsvtav1` 显式配置构建。

### 选项

- **`profile`** 设置编码 profile。

  - **`main`**

  - **`high`**

  - **`professional`**

- **`level`** 设置操作点级别。例如：'4.0'

- **`hielevel`** 设置分层预测级别。

  - **`3level`**

  - **`4level`** 这是默认值。

- **`tier`** 设置操作点层。

  - **`main`** 这是默认值。

  - **`high`**

- **`qmax`** 设置码率模式下使用的最大量化器。

- **`qmin`** 设置码率模式下使用的最小量化器。

- **`crf`** crf 码率控制模式使用的恒定码率因子值 (0-63)。

- **`qp`** 设置 cqp 码率控制模式使用的量化器 (0-63)。

- **`sc_detection`** 启用场景切换检测。

- **`la_depth`** 设置前瞻帧数 (0-120)。

- **`preset`** 设置质量-速度权衡，范围 0 到 13。值越大越快但质量越低。

- **`tile_rows`** 设置使用的瓦片行数的 log2 (0-6)。

- **`tile_columns`** 设置使用的瓦片列数的 log2 (0-4)。

- **`svtav1-params`** 使用以":"分隔的 \<key\>=\<value\> 对列表设置 SVT-AV1 选项。接受的参数列表参见 SVT-AV1 编码器用户指南。

## libsvtjpegxs

SVT-JPEG-XS 编码器封装器。

要求配置期间存在 SVT-JPEG-XS 头文件与库。需要以 `--enable-libsvtjpegxs` 显式配置构建。

### 选项

- **`decomp_v`** 设置垂直分解级别

- **`decomp_h`** 设置水平分解级别

- **`quantization`** 设置量化算法。

  - **`deadzone`**

  - **`uniform`**

- **`coding-signs`** 启用符号处理策略

  - **`disable`**

  - **`fast`**

  - **`full`**

- **`coding-sigf`** 启用显著性编码

- **`coding-vpred`** 启用垂直预测编码

  - **`disable`**

  - **`no_residuals`**

  - **`no_coeffs`**

## libjxl

libjxl JPEG XL 编码器封装器。

要求配置期间存在 libjxl 头文件与库。需要以 `--enable-libjxl` 显式配置构建。

### 选项

libjxl 封装器支持以下选项：

- **`distance`** 设置目标 Butteraugli 距离。这是一项质量设置：距离越低质量越高，对摄影内容而言 distance=1.0 大致相当于 libjpeg Quality 90。设 distance=0.0 可实现真正的无损编码。有效值范围 0.0 到 15.0，合理取值很少超过 5.0。设 distance=0.1 对多数输入通常即可达到视觉透明。默认值为 1.0。

- **`effort`** 设置使用的编码投入。更高的投入值产出更稳定的质量，通常带来更好的质量/bpp 曲线，代价是所需 CPU 时间更多。有效值范围 1 到 9，默认值为 7。

- **`modular`** 强制编码器使用 Modular 模式而非自动选择。默认对有损编码使用 VarDCT，对无损使用 Modular。VarDCT 在有损编码上通常优于 Modular，但不支持无损编码。

## libkvazaar

Kvazaar H.265/HEVC 编码器。

要求配置期间存在 libkvazaar 头文件与库。需要以 `--enable-libkvazaar` 显式配置构建。

### 选项

- **`b`** 以比特/秒为单位设置目标视频码率并启用码率控制。

- **`kvazaar-params`** 以逗号 (,) 分隔的 \<name\>=\<value\> 对列表设置 kvazaar 参数。选项列表参见 kvazaar 文档。

## libopenh264

Cisco libopenh264 H.264/MPEG-4 AVC 编码器封装器。

该编码器要求配置期间存在 libopenh264 头文件与库。需要以 `--enable-libopenh264` 显式配置构建。库通过 `pkg-config` 检测。

关于该库的更多信息参见 <http://www.openh264.org>。

### 选项

以下 FFmpeg 全局选项影响 libopenh264 编码器的配置。

- **`b`** 设置码率（以每秒比特数为单位）。

- **`g`** 设置 GOP 大小。

- **`maxrate`** 设置最大码率（以每秒比特数为单位）。

- **`flags +global_header`** 在比特流中设置全局头。

- **`slices`** 设置小片数量，用于并行化编码。默认值为 0。仅在 `slice_mode` 设为 `fixed` 时使用。

- **`loopfilter`** 启用环路滤波（设为 1 时自动启用）。设为 0 禁用。

- **`profile`** 设置 profile 限制。设为 `main` 时启用 CABAC（将 `SEncParamExt.iEntropyCodingModeFlag` 标志设为 1）。

- **`max_nal_size`** 以字节为单位设置最大 NAL 大小。

- **`allow_skip_frames`** 设为 1 时允许跳帧以达到目标码率。

## libtheora

libtheora Theora 编码器封装器。

要求配置期间存在 libtheora 头文件与库。需要以 `--enable-libtheora` 显式配置构建。

关于 libtheora 项目的更多信息参见 <http://www.theora.org/>。

### 选项

以下全局选项映射到内部 libtheora 选项，影响编码流的质量与码率。

- **`b`** 为 CBR（恒定码率）模式设置视频码率（单位为比特/秒）。VBR（可变码率）模式启用时该选项被忽略。

- **`flags`** 用于通过 `qscale` 标志启用恒定质量 (VBR) 编码，以及启用 `pass1` 与 `pass2` 模式。

- **`g`** 设置 GOP 大小。

- **`global_quality`** 以 lambda 单位的整数设置全局质量。

  仅在用 `flags +qscale` 启用 VBR 模式时相关。该值除以 `FF_QP2LAMBDA` 转换为 QP 单位，截取到 \[0 - 10\] 范围，再乘以 6.3 得到 libtheora 原生范围 \[0-63\] 内的值。值越高质量越高。

- **`q`** 设为非负值时启用 VBR 模式，并以 QP 单位的双精度浮点值设置恒定质量。

  该值截取到 \[0-10\] 范围，再乘以 6.3 得到 libtheora 原生范围 \[0-63\] 内的值。

  该选项仅在使用 `ffmpeg` 命令行工具时有效。库接口用户请使用 `global_quality`。

### 示例

- 用 `ffmpeg` 设置最大恒定质量 (VBR) 编码：

  ``` text
  ffmpeg -i INPUT -codec:v libtheora -q:v 10 OUTPUT.ogg
  ```

- 用 `ffmpeg` 转换 CBR 1000 kbps Theora 视频流：

  ``` text
  ffmpeg -i INPUT -codec:v libtheora -b:v 1000k OUTPUT.ogg
  ```

## libvpx

通过 libvpx 支持 VP8/VP9 格式。

要求配置期间存在 libvpx 头文件与库。需要以 `--enable-libvpx` 显式配置构建。

### 选项

libvpx 封装器支持以下选项。为便于迁移，括号中列出 `vpxenc` 等价的选项或值。

为减少文档重复，这里只记录私有选项及少数需要特别注意的选项。未记载的通用选项文档参见[编解码器选项](#codec_002doptions)章节。

要获得 libvpx 选项的更多文档，请执行命令 `ffmpeg -h encoder=libvpx`、`ffmpeg -h encoder=libvpx-vp9` 或 `vpxenc --help`。更多信息见 libvpx API 文档。

- **`b (target-bitrate)`** 以比特/秒为单位设置码率。注意 FFmpeg 的 `b` 选项以比特/秒表示，而 `vpxenc` 的 `target-bitrate` 以千比特/秒表示。

- **`g (kf-max-dist)`**

- **`keyint_min (kf-min-dist)`**

- **`qmin (min-q)`** 最小（最佳质量）量化器。

- **`qmax (max-q)`** 最大（最差质量）量化器。可逐帧更改。

- **`bufsize (buf-sz, buf-optimal-sz)`** 设置码率控制缓冲区大小（单位为比特）。注意 `vpxenc` 的选项以毫秒指定，libvpx 封装器按如下方式转换该值：`buf-sz = bufsize * 1000 / bitrate`、`buf-optimal-sz = bufsize * 1000 / bitrate * 5 / 6`。

- **`rc_init_occupancy (buf-initial-sz)`** 设置解码开始前应载入 rc 缓冲区的比特数。注意 `vpxenc` 的选项以毫秒指定，libvpx 封装器按如下方式转换该值：`rc_init_occupancy * 1000 / bitrate`。

- **`undershoot-pct`** 设置数据率低于目标码率的（最小）百分比。

- **`overshoot-pct`** 设置数据率超出目标码率的（最大）百分比。

- **`skip_threshold (drop-frame)`**

- **`qcomp (bias-pct)`**

- **`maxrate (maxsection-pct)`** 以比特/秒为单位设置 GOP 最大码率。注意 `vpxenc` 的选项以目标码率的百分比指定，libvpx 封装器按如下方式转换该值：`(maxrate * 100 / bitrate)`。

- **`minrate (minsection-pct)`** 以比特/秒为单位设置 GOP 最小码率。注意 `vpxenc` 的选项以目标码率的百分比指定，libvpx 封装器按如下方式转换该值：`(minrate * 100 / bitrate)`。

- **`minrate, maxrate, b end-usage=cbr`** `(minrate == maxrate == bitrate)`。

- **`crf (end-usage=cq, cq-level)`**

- **`tune (tune)`**

  - **`psnr (psnr)`**

  - **`ssim (ssim)`**

- **`quality, deadline (deadline)`**

  - **`best`** 使用最佳质量 deadline。命名欠佳且相当慢，应避免使用该选项，因为它可能产出比 good 更差的质量。

  - **`good`** 使用良好质量 deadline。配合 `cpu-used` 选项使用时是速度与质量的良好折中。

  - **`realtime`** 使用实时质量 deadline。

- **`speed, cpu-used (cpu-used)`** 设置质量/速度比调节器。更高的值以质量为代价加快编码。

- **`nr (noise-sensitivity)`**

- **`static-thresh`** 为块设置变化阈值，低于它的块将被编码器跳过。

- **`slices (token-parts)`** 注意 FFmpeg 的 `slices` 选项给出分区总数，而 `vpxenc` 的 `token-parts` 以 `log2(partitions)` 给出。

- **`max-intra-rate`** 以目标码率的百分比设置最大 I 帧码率。取 0 表示不限。

- **`force_key_frames`** `VPX_EFLAG_FORCE_KF`

- **`Alternate reference frame related`**

  - **`auto-alt-ref`** 启用交替参考帧（仅两遍模式）。大于 1 的值启用多层交替参考帧（仅 VP9）。

  - **`arnr-maxframes`** 设置 altref 降噪最大帧数。

  - **`arnr-type`** 设置 altref 降噪滤波类型：backward、forward、centered。

  - **`arnr-strength`** 设置 altref 降噪滤波强度。

  - **`rc-lookahead, lag-in-frames (lag-in-frames)`** 设置为帧类型判定和码率控制前瞻的帧数。

  - **`min-gf-interval`** 设置 golden/交替参考帧最小间隔（仅 VP9）。

- **`error-resilient`** 启用错误恢复特性。

- **`sharpness integer`** 以更低 PSNR 为代价提升锐度。有效范围 \[0, 7\]。

- **`ts-parameters`** 使用以":"分隔的 key=value 对列表设置时间可分级配置。例如用 `ffmpeg` 指定时间可分级参数：

  ``` text
  ffmpeg -i INPUT -c:v libvpx -ts-parameters ts_number_layers=3:\
  ts_target_bitrate=250,500,1000:ts_rate_decimator=4,2,1:\
  ts_periodicity=4:ts_layer_id=0,2,1,2:ts_layering_mode=3 OUTPUT
  ```

  以下简要解释各参数，更多细节请参阅 `vpx/vpx_encoder.h` 中的 `struct vpx_codec_enc_cfg`。

  - **`ts_number_layers`** 时间编码层数。

  - **`ts_target_bitrate`** 每个时间层的目标码率（单位为 kbps）。（码率应包含更低的时间层。）

  - **`ts_rate_decimator`** 每个时间层的帧率抽取因子。

  - **`ts_periodicity`** 定义帧时间层归属的序列长度。

  - **`ts_layer_id`** 定义帧到时间层归属的模板。

  - **`ts_layering_mode`** （可选）从一组预定义的时间分层模式中选择时间结构。目前支持以下选项。

    - **`0`** 内部不提供时间分层标志，依赖通过 `AVFrame` 的 `metadata` 字段以下列键传入的标志。

      - **`vp8-flags`** 设置传入编码器的标志，指示当前帧的参考方案。更多细节请参阅 `vpx/vpx_encoder.h` 中的函数 `vpx_codec_encode`。

      - **`temporal_id`** 显式设置当前要编码帧的时间 id。

    - **`2`** 两个时间层。0-1...

    - **`3`** 三个时间层。0-2-1-2...；使用单参考帧。

    - **`4`** 与选项 "3" 相同，但时间周期内的两个时间层 2 帧之间存在依赖。

- **`VP8-specific options`**

  - **`screen-content-mode`** 屏幕内容模式，取值之一：0（关）、1（屏幕）、2（屏幕，更激进的码率控制）。

- **`VP9-specific options`**

  - **`lossless`** 启用无损模式。

  - **`tile-columns`** 设置使用的瓦片列数。注意以 `log2(tile_columns)` 给出。例如设置 `tile-columns` 选项为 3 即请求 8 个瓦片列。

  - **`tile-rows`** 设置使用的瓦片行数。注意以 `log2(tile_rows)` 给出。例如设置 `tile-rows` 选项为 2 即请求 4 个瓦片行。

  - **`frame-parallel`** 启用帧并行可解码特性。

  - **`aq-mode`** 设置自适应量化模式（0：关（默认）、1：方差、2：复杂度、3：循环刷新、4：equator360）。

  - **`colorspace color-space`** 设置输入色彩空间。VP9 比特流支持传递下列色彩空间信号：

    - **`'rgb' sRGB`**

    - **`'bt709' bt709`**

    - **`'unspecified' unknown`**

    - **`'bt470bg' bt601`**

    - **`'smpte170m' smpte170`**

    - **`'smpte240m' smpte240`**

    - **`'bt2020_ncl' bt2020`**

  - **`row-mt boolean`** 启用基于行的多线程。

  - **`tune-content`** 设置内容类型：default (0)、screen (1)、film (2)。

  - **`corpus-complexity`** 语料库 VBR 模式是标准 VBR 的变体，其中复杂度分布中点以传入方式给出，而非针对特定剪辑或数据块计算。

    有效范围 \[0, 10000\]。0（默认）使用标准 VBR。

  - **`enable-tpl boolean`** 启用时域依赖模型。

  - **`ref-frame-config`** 使用逐帧元数据设置 `vpx/vp8cx.h` 中结构 `vpx_svc_ref_frame_config_t` 的成员，以细控参考方案与帧缓冲管理。使用以":"分隔的 key=value 对列表。例如，

    ``` c
    av_dict_set(&av_frame->metadata, "ref-frame-config", \
    "rfc_update_buffer_slot=7:rfc_lst_fb_idx=0:rfc_gld_fb_idx=1:rfc_alt_fb_idx=2:rfc_reference_last=0:rfc_reference_golden=0:rfc_reference_alt_ref=0");
    ```

    | Term                     | Description                                  |
    |--------------------------|----------------------------------------------|
    | `rfc_update_buffer_slot` | 指示要更新的缓冲槽编号   |
    | `rfc_update_last`        | 指示是否更新 LAST 帧   |
    | `rfc_update_golden`      | 指示是否更新 GOLDEN 帧     |
    | `rfc_update_alt_ref`     | 指示是否更新 ALT_REF 帧    |
    | `rfc_lst_fb_idx`         | LAST 帧缓冲索引                      |
    | `rfc_gld_fb_idx`         | GOLDEN 帧缓冲索引                    |
    | `rfc_alt_fb_idx`         | ALT_REF 帧缓冲索引                   |
    | `rfc_reference_last`     | 指示是否参考 LAST 帧    |
    | `rfc_reference_golden`   | 指示是否参考 GOLDEN 帧  |
    | `rfc_reference_alt_ref`  | 指示是否参考 ALT_REF 帧 |
    | `rfc_reference_duration` | 指示帧时长                     |

关于 libvpx 的更多信息参见：<http://www.webmproject.org/>

## libvvenc

VVenC H.266/VVC 编码器封装器。

该编码器要求配置期间存在 libvvenc 头文件与库。需要以 `--enable-libvvenc` 显式配置构建。

VVenC 项目网站位于 <https://github.com/fraunhoferhhi/vvenc>。

### 支持的像素格式

VVenC 仅支持 10 位色彩空间作为输入。但内部（编码）位深可在运行时设为 8 位或 10 位。

### 选项

- **`b`** 设置目标视频码率。

- **`g`** 设置 GOP 大小。目前支持 g=1（仅帧内）或默认值。

- **`preset`** 设置 VVenC 预设。

- **`levelidc`** 设置 level idc。

- **`tier`** 设置 vvc 层。

- **`qp`** 设置恒定量化参数。

- **`subopt boolean`** 设置主观（感知动机的）优化。默认为 1（开）。

- **`bitdepth8 boolean`** 设为 8 位编码模式而非 10 位。默认为 0（关）。

- **`period`** 设置（帧内）刷新周期（单位为秒）。

- **`vvenc-params`** 使用以":"分隔的 \<key\>=\<value\> 对列表设置 vvenc 选项。选项列表参见 `vvencapp --fullhelp` 或 `vvencFFapp --fullhelp`。

  例如，选项可以这样提供：

  ``` text
  intraperiod=64:decodingrefreshtype=idr:poc0idr=1:internalbitdepth=8
  ```

  例如编码选项可以用 `-vvenc-params` 提供：

  ``` text
  ffmpeg -i input -c:v libvvenc -b 1M -vvenc-params intraperiod=64:decodingrefreshtype=idr:poc0idr=1:internalbitdepth=8 output.mp4
  ```

## libwebp

libwebp WebP 图像编码器封装器

libwebp 是 Google 官方的 WebP 图像编码器。它能以有损或无损模式编码。有损图像本质上是 VP8 帧的一层封装。无损图像是 Google 开发的独立编解码器。

### 像素格式

受格式与 libwebp 限制，目前 libwebp 有损仅支持 YUV420，无损仅支持 RGB。两种模式都支持 alpha。由于 API 限制，若有损编码传入 RGB 或无损编码传入 YUV，像素格式将使用 libwebp 的函数自动转换。这并不理想，仅为方便起见。

### 选项

- **`-lossless boolean`** 启用/禁用无损模式。默认为 0。

- **`-compression_level integer`** 有损时这是质量/速度权衡。更高的值在给定大小下给出更好质量，代价是编码时间增加。无损时这是大小/速度权衡。更高的值给出更小大小，代价是编码时间增加。更具体地说，它控制使用的额外算法与压缩工具的数量，并改变这些工具的组合。它映射到 libwebp 的 \<method\> 选项。有效范围 0 到 6。默认为 4。

- **`-quality float`** 有损编码时控制图像质量；无损编码时控制投入压缩的精力与时间。范围 0 到 100。默认为 75。

- **`-preset type`** 配置预设。它依据图像的大致类型做一些自动设置。

  | Term      | Description                                      |
  |-----------|--------------------------------------------------|
  | `none`    | 不使用预设。                             |
  | `default` | 使用编码器默认值。                         |
  | `picture` | 数字图像，如肖像、内景照       |
  | `photo`   | 自然光照下的户外照片        |
  | `drawing` | 手绘或线稿，高对比度细节 |
  | `icon`    | 小尺寸多彩图像                      |
  | `text`    | 类文本                                    |

## libx264, libx264rgb

x264 H.264/MPEG-4 AVC 编码器封装器。

该编码器要求配置期间存在 libx264 头文件与库。需要以 `--enable-libx264` 显式配置构建。

libx264 支持数量可观的功能，包括 8x8 与 4x4 自适应空间变换、自适应 B 帧布置、CAVLC/CABAC 熵编码、隔行 (MBAFF)、无损模式、面向细节保留的心理视觉优化（自适应量化、psy-RD、psy-trellis）。

许多 libx264 编码器选项映射到 FFmpeg 全局编解码器选项，而独有的编码器选项通过私有选项提供。此外，`x264opts` 与 `x264-params` 私有选项允许传入 libx264 `x264_param_parse` 函数接受的 key=value 元组列表。

x264 项目网站位于 <http://www.videolan.org/developers/x264.html>。

libx264rgb 编码器与 libx264 相同，只是它接受打包 RGB 像素格式而非 YUV 作为输入。

### 支持的像素格式

x264 支持 8 至 10 位色彩空间。确切位深在 x264 配置时控制。

### 选项

libx264 封装器支持以下选项。为便于迁移，括号中列出 `x264` 等价的选项或值。

为减少文档重复，这里只记录私有选项及少数需要特别注意的选项。未记载的通用选项文档参见[编解码器选项](#codec_002doptions)章节。

要获得更准确、更全面的 libx264 选项文档，请执行命令 `x264 --fullhelp` 或查阅 libx264 文档。

在下面的列表中，注意存在直接映射时，`x264` 选项名会以括号形式显示在 libavcodec 对应名称之后。

- **`b (bitrate)`** 以比特/秒为单位设置码率。注意 FFmpeg 的 `b` 选项以比特/秒表示，而 `x264` 的 `bitrate` 以千比特/秒表示。

- **`bf (bframes)`** I 帧与 P 帧之间 B 帧的数量

- **`g (keyint)`** 最大 GOP 大小

- **`qmin (qpmin)`** 最小量化器缩放

- **`qmax (qpmax)`** 最大量化器缩放

- **`qdiff (qpstep)`** 量化器缩放之间的最大差值

- **`qblur (qblur)`** 量化器曲线模糊

- **`qcomp (qcomp)`** 量化器曲线压缩因子

- **`refs (ref)`** 每个 P 帧可用的参考帧数。范围 \<0-16\>。

- **`level (level)`** 设置 `x264_param_t.i_level_idc` 值；值为正时生效，否则被忽略。

  该值可用 `AVCodecContext` API 设置（如直接设置 `AVCodecContext` 值），并以映射到相应 level 的整数指定（如值 31 映射到 `x264_levels` 表中定义的 H.264 level IDC "3.1"）。设为非正值时被忽略。

  或者可将其设为私有选项，覆盖 `AVCodecContext` 中设置的值；此时必须以 H.264 附录 A 定义的 level IDC 标识符（如 "3.1"）指定。

- **`sc_threshold (scenecut)`** 设置场景切换检测阈值。

- **`trellis (trellis)`** 执行 Trellis 量化以提升效率。默认启用。

- **`nr (nr)`** 降噪

- **`me_range (merange)`** 以像素为单位的运动搜索最大范围。

- **`me_method (me)`** 设置运动估计方法。按速度降序排列的可取值：

  - **`dia (dia)`**

  - **`epzs (dia)`** 半径 1 的菱形搜索（最快）。`epzs` 是 `dia` 的别名。

  - **`hex (hex)`** 半径 2 的六边形搜索。

  - **`umh (umh)`** 不均匀多六边形搜索。

  - **`esa (esa)`** 穷举搜索。

  - **`tesa (tesa)`** Hadamard 穷举搜索（最慢）。

- **`forced-idr`** 通常在强制 I 帧类型时，编码器可选择任何 I 帧类型。该选项强制其选择 IDR 帧。

- **`subq (subme)`** 子像素运动估计方法。

- **`b_strategy (b-adapt)`** 自适应 B 帧布置决策算法。仅在第一遍使用。

- **`keyint_min (min-keyint)`** 最小 GOP 大小。

- **`coder`** 设置熵编码器。可取的值：

  - **`ac`** 启用 CABAC。

  - **`vlc`** 启用 CAVLC 并禁用 CABAC。效果与 `x264` 的 `--no-cabac` 选项相同。

- **`cmp`** 设置全像素运动估计比较算法。可取的值：

  - **`chroma`** 运动估计启用色度。

  - **`sad`** 运动估计忽略色度。效果与 `x264` 的 `--no-chroma-me` 选项相同。

- **`threads (threads)`** 编码线程数。

- **`thread_type`** 设置多线程技术。可取的值：

  - **`slice`** 基于小片的多线程。效果与 `x264` 的 `--sliced-threads` 选项相同。

  - **`frame`** 基于帧的多线程。

- **`flags`** 设置编码标志。可将其设为 `-cgop` 以禁用闭合 GOP、启用开放 GOP。结果类似 `x264` 的 `--open-gop` 选项行为。

- **`rc_init_occupancy (vbv-init)`** 初始 VBV 缓冲区占用

- **`preset (preset)`** 设置编码预设。

- **`tune (tune)`** 设置编码参数调优。

- **`profile (profile)`** 设置 profile 限制。

- **`fastfirstpass`** 设为 1 时在编码第一遍启用快速设置。设为 0 时效果与 `x264` 的 `--slow-firstpass` 选项相同。

- **`crf (crf)`** 设置恒定质量模式的质量。

- **`crf_max (crf-max)`** CRF 模式下阻止 VBV 把质量降到此点之下。

- **`qp (qp)`** 设置恒定量化码率控制方法参数。

- **`aq-mode (aq-mode)`** 设置 AQ 方法。可取的值：

  | Term                 | Description                      |
  |----------------------|----------------------------------|
  | `none (0)`         | 禁用。                        |
  | `variance (1)`     | 方差 AQ（复杂度掩码）。   |
  | `autovariance (2)` | 自动方差 AQ（实验性）。 |

- **`aq-strength (aq-strength)`** 设置 AQ 强度，减少平坦与纹理区域的块效应与模糊。

- **`psy`** 设为 1 使用心理视觉优化。设为 0 时效果与 `x264` 的 `--no-psy` 选项相同。

- **`psy-rd (psy-rd)`** 设置心理视觉优化强度，格式为 \<psy-rd\>:\<psy-trellis\>。

- **`rc-lookahead (rc-lookahead)`** 设置为帧类型判定和码率控制前瞻的帧数。

- **`weightb`** 设为 1 为 B 帧启用加权预测。设为 0 时效果与 `x264` 的 `--no-weightb` 选项相同。

- **`weightp (weightp)`** 设置 P 帧加权预测方法。可取的值：

  | Term           | Description                              |
  |----------------|------------------------------------------|
  | `none (0)`   | 禁用                                 |
  | `simple (1)` | 仅启用加权参考                |
  | `smart (2)`  | 同时启用加权参考与重复 |

- **`ssim (ssim)`** 启用编码后计算并打印 SSIM 统计。

- **`intra-refresh (intra-refresh)`** 设为 1 时启用周期性帧内刷新取代 IDR 帧。

- **`avcintra-class (class)`** 配置编码器生成 AVC-Intra。有效值为 50、100 与 200

- **`bluray-compat (bluray-compat)`** 配置编码器兼容蓝光标准。它是设置 "bluray-compat=1 force-cfr=1" 的简写。

- **`b-bias (b-bias)`** 设置对 B 帧使用频率的影响。

- **`b-pyramid (b-pyramid)`** 设置保留部分 B 帧作为参考的方法。可取的值：

  | Term                | Description                          |
  |---------------------|--------------------------------------|
  | `none (none)`     | 禁用。                            |
  | `strict (strict)` | 严格分层金字塔。       |
  | `normal (normal)` | 非严格（不兼容蓝光）。 |

- **`mixed-refs`** 设为 1 启用每分区一个参考，而非每宏块一个参考。设为 0 时效果与 `x264` 的 `--no-mixed-refs` 选项相同。

- **`8x8dct`** 设为 1 启用自适应空间变换（high profile 8x8 变换）。设为 0 时效果与 `x264` 的 `--no-8x8dct` 选项相同。

- **`fast-pskip`** 设为 1 启用 P 帧早期 SKIP 检测。设为 0 时效果与 `x264` 的 `--no-fast-pskip` 选项相同。

- **`aud (aud)`** 设为 1 启用访问单元分隔符。

- **`mbtree`** 设为 1 启用宏块树码率控制。设为 0 时效果与 `x264` 的 `--no-mbtree` 选项相同。

- **`deblock (deblock)`** 设置环路滤波参数，格式为 \<alpha\>:\<beta\>。

- **`cplxblur (cplxblur)`** 设置 QP 的波动削减（曲线压缩之前）。

- **`partitions (partitions)`** 以逗号分隔的值列表设置要考虑的分区。列表中的可取值：

  - **`p8x8`** 8x8 P 帧分区。

  - **`p4x4`** 4x4 P 帧分区。

  - **`b8x8`** 4x4 B 帧分区。

  - **`i8x8`** 8x8 I 帧分区。

  - **`i4x4`** 4x4 I 帧分区。（启用 `p4x4` 要求启用 `p8x8`。启用 `i8x8` 要求启用自适应空间变换（`8x8dct` 选项）。）

  - **`none (none)`** 不考虑任何分区。

  - **`all (all)`** 考虑每个分区。

- **`direct-pred (direct)`** 设置直接 MV 预测模式。可取的值：

  | Term                    | Description                 |
  |-------------------------|-----------------------------|
  | `none (none)`         | 禁用 MV 预测。      |
  | `spatial (spatial)`   | 启用空间预测。  |
  | `temporal (temporal)` | 启用时域预测。 |
  | `auto (auto)`         | 自动决定。      |

- **`slice-max-size (slice-max-size)`** 以字节为单位设置每个小片大小的限制。未指定但指定了 RTP 载荷大小 (`ps`) 时使用后者。

- **`stats (stats)`** 设置多遍统计的文件名。

- **`nal-hrd (nal-hrd)`** 设置 HRD 信息信号传递（要求设置 `vbv-bufsize`）。可取的值：

  | Term            | Description                                       |
  |-----------------|---------------------------------------------------|
  | `none (none)` | 禁用 HRD 信息信号传递。                |
  | `vbr (vbr)`   | 可变码率。                                |
  | `cbr (cbr)`   | 恒定码率（MP4 容器中不允许）。 |

- **`x264opts opts`**

- **`x264-params opts`** 使用以":"分隔的 key=value 选项列表覆盖 x264 配置。

  两个选项的参数都是以":"分隔的 \<key\>=\<value\> 对列表。使用 `x264opts` 时值可以省略，此时假定值为 `1`。

  对于 \<filter\> 与 \<psy-rd\> 这类自身以":"作分隔符的选项值，请改用","。它们其实早已接受","，但出于某种原因一直未见于文档。

  例如，选项可以这样提供：

  ``` text
  level=30:bframes=0:weightp=0:cabac=0:ref=1:vbv-maxrate=768:vbv-bufsize=2000:analyse=all:me=umh:no-fast-pskip=1:subq=6:8x8dct=0:trellis=0
  ```

  例如用 `ffmpeg` 指定 libx264 编码选项：

  ``` text
  ffmpeg -i foo.mpg -c:v libx264 -x264opts keyint=123:min-keyint=20 -an out.mkv
  ```

  要获得 libx264 选项的完整列表，请执行命令 `x264 --fullhelp` 或查阅 libx264 文档。

- **`a53cc boolean`** 将隐藏式字幕（必须为 ATSC 兼容格式）导入输出。仅 mpeg2 与 h264 解码器提供这些。默认为 1（开）。

- **`udu_sei boolean`** 将用户数据非注册 SEI（若可用）导入输出。默认为 0（关）。

- **`mb_info boolean`** 通过 AVFrameSideData 设置 mb_info 数据，仅从 API 使用时有用。默认为 0（关）。

提供了常见用法的编码 ffpresets，以便它们可与通用预设系统一起使用（如传入 `pre` 选项）。

## libx265

x265 H.265/HEVC 编码器封装器。

该编码器要求配置期间存在 libx265 头文件与库。需要以 `--enable-libx265` 显式配置构建。

### 选项

- **`b`** 设置目标视频码率。

- **`bf`**

- **`g`** 设置 GOP 大小。

- **`keyint_min`** 最小 GOP 大小。

- **`refs`** 每个 P 帧可用的参考帧数。范围 \<1-16\>。

- **`preset`** 设置 x265 预设。

- **`tune`** 设置 x265 tune 参数。

- **`profile`** 设置 profile 限制。

- **`crf`** 设置恒定质量模式的质量。

- **`qp`** 设置恒定量化码率控制方法参数。

- **`qmin`** 最小量化器缩放。

- **`qmax`** 最大量化器缩放。

- **`qdiff`** 量化器缩放之间的最大差值。

- **`qblur`** 量化器曲线模糊

- **`qcomp`** 量化器曲线压缩因子

- **`i_qfactor`**

- **`b_qfactor`**

- **`forced-idr`** 通常在强制 I 帧类型时，编码器可选择任何 I 帧类型。该选项强制其选择 IDR 帧。

- **`x265-stats`** 指定两遍统计的文件名。使用 `-passlogfile` 选项时自动设置。

- **`udu_sei boolean`** 将用户数据非注册 SEI（若可用）导入输出。默认为 0（关）。

- **`x265-params`** 使用以":"分隔的 \<key\>=\<value\> 对列表设置 x265 选项。选项列表参见 `x265 --help`。

  例如用 `-x265-params` 指定 libx265 编码选项：

  ``` text
  ffmpeg -i input -c:v libx265 -x265-params crf=26:psy-rd=1 output.mp4
  ```

## libxavs2

xavs2 AVS2-P2/IEEE1857.4 编码器封装器。

该编码器要求配置期间存在 libxavs2 头文件与库。需要以 `--enable-libxavs2` 显式配置构建。

使用以下标准 libavcodec 选项：

- `b` / `bit_rate`

- `g` / `gop_size`

- `bf` / `max_b_frames`

该编码器还有自己的专属选项：

### 选项

- **`lcu_row_threads`** 设置行并行线程数，取值 1 到 8（默认 5）。

- **`initial_qp`** 设置 xavs2 量化参数，取值 1 到 63（默认 34）。用于设置第一帧的初始 qp。

- **`qp`** 设置 xavs2 量化参数，取值 1 到 63（默认 34）。用于恒定 QP 模式下设置 qp 值。

- **`max_qp`** 设置码率控制最大 qp，取值 1 到 63（默认 55）。

- **`min_qp`** 设置码率控制最小 qp，取值 1 到 63（默认 20）。

- **`speed_level`** 设置速度级别，取值 0 到 9（默认 0）。越高越好但越慢。

- **`log_level`** 设置日志级别，取值 -1 到 3（默认 0）。-1：无、0：错误、1：警告、2：信息、3：调试。

- **`xavs2-params`** 使用以":"分隔的 \<key\>=\<value\> 对列表设置 xavs2 选项。

  例如用 `-xavs2-params` 指定 libxavs2 编码选项：

  ``` text
  ffmpeg -i input -c:v libxavs2 -xavs2-params RdoqLevel=0 output.avs2
  ```

## libxeve

eXtra-fast Essential Video Encoder (XEVE) MPEG-5 EVC 编码器封装器。为便于迁移，括号中列出 xeve 等价的选项或值。

该编码器要求配置期间存在 libxeve 头文件与库。需要以 `--enable-libxeve` 显式配置构建。

许多 libxeve 编码器选项映射到 FFmpeg 全局编解码器选项，而独有的编码器选项通过私有选项提供。此外，xeve-params 私有选项允许传入 libxeve `parse_xeve_params` 函数接受的 key=value 元组列表。

xeve 项目网站位于 <https://github.com/mpeg5/xeve>。

### 选项

libxeve 封装器支持以下选项。为便于迁移，括号中列出 xeve 等价的选项或值。

为减少文档重复，这里只记录私有选项及少数需要特别注意的选项。未记载的通用选项文档参见[编解码器选项](#codec_002doptions)章节。

要获得更准确、更全面的 libxeve 选项文档，请执行命令 `xeve_app --help` 或查阅 libxeve 文档。

- **`b (bitrate)`** 以比特/秒为单位设置目标视频码率。注意 FFmpeg 的 b 选项以比特/秒表示，而 xeve 的 bitrate 以千比特/秒表示。

- **`bf (bframes)`** 设置 B 帧最大数量 (1,3,7,15)。

- **`g (keyint)`** 设置 GOP 大小（I 图像周期）。

- **`preset (preset)`** 设置 xeve 预设。设置编码器预设值以决定编码速度 \[fast, medium, slow, placebo\]

- **`tune (tune)`** 设置编码器 tune 参数 \[psnr, zerolatency\]

- **`profile (profile)`** 设置编码器 profile \[0: baseline; 1: main\]

- **`crf (crf)`** 设置恒定质量模式的质量。恒定码率因子 \<10..49\> \[default: 32\]

- **`qp (qp)`** 设置恒定量化码率控制方法参数。量化参数 qp \<0..51\> \[default: 32\]

- **`threads (threads)`** 强制使用指定的线程数

## libxvid

Xvid MPEG-4 Part 2 编码器封装器。

该编码器要求配置期间存在 libxvidcore 头文件与库。需要以 `--enable-libxvid --enable-gpl` 显式配置构建。

原生 `mpeg4` 编码器支持 MPEG-4 Part 2 格式，因此用户无需此库即可编码到该格式。

### 选项

libxvid 封装器支持以下选项。下列部分选项已列出但未在此处记载，它们对应共享编解码器选项，其文档参见[编解码器选项](#codec_002doptions)章节。未列出的其他共享选项对 libxvid 编码器无效。

- **`b`**

- **`g`**

- **`qmin`**

- **`qmax`**

- **`mpeg_quant`**

- **`threads`**

- **`bf`**

- **`b_qfactor`**

- **`b_qoffset`**

- **`flags`** 设置特定编码标志。可取的值：

  | Term | Description |
  |----|----|
  | `mv4` | 每个宏块使用四个运动矢量。 |
  | `aic` | 启用高质量 AC 预测。 |
  | `gray` | 仅编码灰度。 |
  | `qpel` | 启用四分之一像素运动补偿。 |
  | `cgop` | 启用闭合 GOP。 |
  | `global_header` | 将全局头放入 extradata 而非每个关键帧。 |

- **`gmc`** 启用全局运动补偿 (GMC)。默认为 0（禁用）。

- **`me_quality`** 设置运动估计质量级别。按速度降序、质量升序排列的可取值：

  - **`0`** 不使用运动估计（默认）。

  - **`1, 2`** 为 16x16 块启用高级菱形区域搜索与半像素精化。

  - **`3, 4`** 启用上述全部，并为 8x8 块启用高级菱形区域搜索与半像素精化，还为 P 帧和 B 帧在色度平面上启用运动估计。

  - **`5, 6`** 启用上述全部，并扩展 16x16 与 8x8 块搜索。

- **`mbd`** 设置宏块决策算法。按质量升序排列的可取值：

  - **`simple`** 使用宏块比较函数算法（默认）。

  - **`bits`** 为 16x16 块启用基于率失真的半像素与四分之一像素精化。

  - **`rd`** 启用上述全部，并为 8x8 块启用基于率失真的半像素与四分之一像素精化，以及基于率失真的方形模式搜索。

- **`lumi_aq`** 设为 1 启用亮度掩蔽自适应量化。默认为 0（禁用）。

- **`variance_aq`** 设为 1 启用方差自适应量化。默认为 0（禁用）。

  与 `lumi_aq` 组合使用时，所得质量不会优于二者单独使用中的任何一种。换言之，最终质量是两种效果中较差的一个。

- **`trellis`** 设置率失真最优量化。

- **`ssim`** 设置结构相似性 (SSIM) 显示方法。可取的值：

  - **`off`** 禁用 SSIM 信息显示。

  - **`avg`** 编码结束时向 stdout 输出平均 SSIM。平均 SSIM 的显示格式为：

    ``` text
    Average SSIM: %f
    ```

    对不熟悉 C 的用户，%f 表示一个浮点数，即小数（如 0.939232）。

  - **`frame`** 编码期间向 stdout 输出逐帧 SSIM 数据，并在编码结束时输出平均 SSIM。逐帧信息的格式为：

    ``` text
           SSIM: avg: %1.3f min: %1.3f max: %1.3f
    ```

    对不熟悉 C 的用户，%1.3f 表示一个四舍五入到小数点后 3 位的浮点数（如 0.932）。

- **`ssim_acc`** 设置 SSIM 精度。有效选项为 0-4 范围内的整数，0 给出最精确的结果，4 计算最快。

## MediaCodec

MediaCodec 编码器封装器在 Android 设备上启用硬件加速视频编码。它支持 H.264、H.265 (HEVC)、VP8、VP9、MPEG-4 与 AV1 编码（是否可用取决于设备）。

Android 提供两套 API：Java MediaCodec 与 NDK MediaCodec。MediaCodec 编码器封装器两者都支持。注意 NDK MediaCodec API 无需 JVM 即可运行，但由于依赖系统框架服务，在 JVM 环境之外可能无法正常工作，Android 15 之后尤其如此。

- **`ndk_codec boolean`** 使用基于 NDK 的 MediaCodec API 而非 Java API。`av_jni_get_java_vm()` 返回 NULL 时默认启用。

- **`ndk_async boolean`** 以异步模式使用 NDK MediaCodec。异步模式比同步模式的循环轮询开销更小。异步模式的缺点是 AV_CODEC_FLAG_GLOBAL_HEADER 不起作用（必要时使用 extract_extradata bsf）。在低于 Android 8.0 的设备上不起作用并将自动禁用。

- **`codec_name string`** 同一编解码器类型在单一设备上可能有多个实现，该选项指定使用哪个后端（经 MediaCodec createCodecByName API）。默认为 NULL，编码器由 createEncoderByType 创建。

- **`bitrate_mode integer`** 可取的值：

  | Term       | Description                            |
  |------------|----------------------------------------|
  | `cq`     | 恒定质量模式                  |
  | `vbr`    | 可变码率模式                  |
  | `cbr`    | 恒定码率模式                  |
  | `cbr_fd` | 带丢帧的恒定码率模式 |

- **`pts_as_dts boolean`** 使用 PTS 作为 DTS。这是 MediaCodec API 不提供解码时间戳的一种变通。B 帧为 0 时自动启用。

- **`operating_rate integer`** 编解码器需要以何种期望运行率工作，零表示未指定。用于高速/慢动作视频采集等场景：视频编码器格式包含目标播放率（如 30fps），但组件必须能处理高运行采集率（如 240fps）。编解码器将使用该速率做资源规划与设置运行点。

- **`qp_i_min integer`** I 帧最小量化参数。

- **`qp_p_min integer`** P 帧最小量化参数。

- **`qp_b_min integer`** B 帧最小量化参数。

- **`qp_i_max integer`** I 帧最大量化参数。

- **`qp_p_max integer`** P 帧最大量化参数。

- **`qp_b_max integer`** B 帧最大量化参数。

## MediaFoundation

MediaFoundation 框架中的编码器提供以下封装器：

- h264_mf

- hevc_mf

- av1_mf

它们同时支持软件与硬件编码。

视频编码器可接受 nv12 或 yuv420p 形式的输入（部分编码器两者都支持，部分只支持其一——实践中 nv12 是更安全的选择，硬件编码器尤其如此）。

硬件加速编码需要 D3D11，包括通过 scale_d3d11 滤镜的硬件缩放能力。

要列出 MediaFoundation 编码器的全部可用选项，使用：`ffmpeg -h encoder=<encoder>`，如 `ffmpeg -h encoder=h264_mf`

### 选项

- **`rate_control`** 选择码率控制模式。可用模式：

  | Term        | Description                                     |
  |-------------|-------------------------------------------------|
  | `default` | 默认模式                                    |
  | `cbr`     | CBR 模式                                        |
  | `pc_vbr`  | 峰值受约束 VBR 模式                       |
  | `u_vbr`   | 无约束 VBR 模式                          |
  | `quality` | 质量模式                                    |
  | `ld_vbr`  | 低延迟 VBR 模式（要求 Windows 8+）        |
  | `g_vbr`   | 全局 VBR 模式（要求 Windows 8+）           |
  | `gld_vbr` | 全局低延迟 VBR 模式（要求 Windows 8+） |

- **`scenario`** 选择使用场景。可用场景：

  | Term | Description |
  |----|----|
  | `default` | 默认场景 |
  | `display_remoting` | 显示远程化场景 |
  | `video_conference` | 视频会议场景 |
  | `archive` | 归档场景 |
  | `live_streaming` | 直播场景 |
  | `camera_record` | 相机录制场景 |
  | `display_remoting_with_feature_map` | 带特征图的显示远程化场景 |

- **`quality`** 设置编码质量 (0-100)。-1 表示默认质量。

- **`hw_encoding`** 强制硬件编码 (0-1)。默认为 0（禁用）。

### 示例

硬件编码：

``` text
ffmpeg -i input.mp4 -c:v h264_mf -hw_encoding 1 output.mp4
```

硬件加速解码配合硬件编码：

``` text
ffmpeg -hwaccel d3d11va -i input.mp4 -c:v h264_mf -hw_encoding 1 output.mp4
```

硬件加速解码、硬件缩放与编码并设置质量：

``` text
ffmpeg -hwaccel d3d11va -hwaccel_output_format d3d11 -i input.mp4 -vf scale_d3d11=1920:1080 -c:v hevc_mf -hw_encoding 1 -quality 80 output.mp4
```

## Microsoft RLE

Microsoft RLE（又称 MSRLE）编码器。仅支持 8 位调色板模式。兼容 Windows 3.1 与 Windows 95。

### 选项

- **`g integer`** 关键帧间隔。每 `-g` 帧至少插入一个关键帧，有时更早。

## mpeg2

MPEG-2 视频编码器。

### 选项

- **`profile`** 选择要编码的 mpeg2 profile：

  - **`422`**

  - **`high`**

  - **`ss`** 空间可分级

  - **`snr`** SNR 可分级

  - **`main`**

  - **`simple`**

- **`level`** 选择要编码的 mpeg2 level：

  - **`high`**

  - **`high1440`**

  - **`main`**

  - **`low`**

- **`seq_disp_ext integer`** 指定编码器是否应向输出写入 sequence_display_extension。

  - **`-1`** 通过检查要写入的数据是否不同于默认或未指定值，自动决定是否写入（这是默认值）。

  - **`0`** 从不写入。

  - **`1`** 总是写入。

- **`video_format integer`** 指定写入序列显示扩展的 video_format，指示视频图像的来源。默认为 `unspecified`，可为 `component`、`pal`、`ntsc`、`secam` 或 `mac`。为最大兼容性请使用 `component`。

- **`a53cc boolean`** 将隐藏式字幕（必须为 ATSC 兼容格式）导入输出。默认为 1（开）。

## png

PNG 图像编码器。

### 选项

| Term                | Description                                      |
|---------------------|--------------------------------------------------|
| `compression_level` | 设置压缩级别，从 0 到 9（默认） |

### 私有选项

| Term | Description |
|----|----|
| `dpi integer` | 设置像素物理密度，单位为点/英寸，默认未设置 |
| `dpm integer` | 设置像素物理密度，单位为点/米，默认未设置 |
| `pred method` | 设置预测方法（none、sub、up、avg、paeth、mixed），默认为 paeth |

## ProRes

Apple ProRes 编码器。

FFmpeg 包含 2 个 ProRes 编码器：prores-aw 与 prores-ks 编码器。可用 `-vcodec` 选项选择所用编码器。

### prores-ks 的私有选项

- **`profile integer`** 选择要编码的 ProRes profile

  - **`proxy`**

  - **`lt`**

  - **`standard`**

  - **`hq`**

  - **`4444`**

  - **`4444xq`**

- **`quant_mat integer`** 选择量化矩阵。

  - **`auto`**

  - **`default`**

  - **`proxy`**

  - **`lt`**

  - **`standard`**

  - **`hq`**

  设为 \<auto\> 时将挑选与 profile 匹配的矩阵。未设置时挑选质量最高的矩阵 \<default\>。

- **`bits_per_mb integer`** 为编码一个宏块分配多少比特。不同 profile 每宏块使用 200 到 2400 比特，最大为 8000。

- **`mbs_per_slice integer`** 每个小片中的宏块数 (1-8)；默认值 (8) 在几乎所有情形下都合适。

- **`vendor string`** 覆盖 4 字节厂商 ID。自定义厂商 ID 如 \<apl0\> 会声称该流由 Apple 编码器产出。

- **`alpha_bits integer`** 指定 alpha 分量的比特数。可取值为 \<0\>、\<8\> 与 \<16\>。使用 \<0\> 禁用 alpha 平面编码。

### 速度考量

在默认运行模式下，编码器必须遵守帧约束（即不产出大于请求大小的帧），同时尽量让输出图像尽可能好。包含大量小细节的帧更难压缩，编码器会花更多时间为每个小片搜索合适的量化器。

设置更高的 `bits_per_mb` 限制会提升速度。

要获得最快的编码速度，设置 `qscale` 参数（推荐值为 4）且不要设置大小约束。

## QSV 编码器

Intel QuickSync Video 编码器家族（MPEG-2、H.264、HEVC、JPEG/MJPEG、VP9、AV1）

### 码率控制方法

码率控制方法按如下方式选择：

- 指定 `global_quality` 时，使用基于质量的模式。具体而言即下列之一

  - − \<CQP\> - 恒定量化器缩放，同时设置 `qscale` 编解码器标志时（即 `-qscale` ffmpeg 选项）。

  - − \<LA_ICQ\> - 带前瞻的智能恒定质量，同时设置 `look_ahead` 选项时。

  - − \<ICQ\> – 其他情况为智能恒定质量。ICQ 模式的全局质量范围为 1 到 51，1 为最佳质量。

- 否则当用 `b` 选项指定期望的平均码率时，使用基于码率的模式。

  - − \<LA\> - 带前瞻的 VBR，指定 `look_ahead` 选项时。

  - − \<VCM\> - 视频会议模式，设置 `vcm` 选项时。

  - − \<CBR\> - 恒定码率，指定 `maxrate` 且等于平均码率时。

  - − \<VBR\> - 可变码率，指定 `maxrate` 但高于平均码率时。

  - − \<AVBR\> - 平均 VBR 模式，未指定 `maxrate` 且 `avbr_accuracy` 与 `avbr_convergence` 均设为非零时。该模式在 Windows 上可用于 H264 与 HEVC。

- 否则使用默认码率控制方法 \<CQP\>。

注意，依据系统情况，编码器可能选择与您指定不同的模式。将详细级别设为 \<verbose\> 或更高可查看 QSV 运行时实际使用的设置。

### 全局选项 -\> MSDK 选项

额外的 libavcodec 全局选项按如下方式映射到 MSDK 选项：

- `g/gop_size` -\> `GopPicSize`

- `bf/max_b_frames`+1 -\> `GopRefDist`

- `rc_init_occupancy/rc_initial_buffer_occupancy` -\> `InitialDelayInKB`

- `slices` -\> `NumSlice`

- `refs` -\> `NumRefFrame`

- `b_strategy/b_frame_strategy` -\> `BRefType`

- `cgop/CLOSED_GOP` 编解码器标志 -\> `GopOptFlag`

- 对 \<CQP\> 模式，`i_qfactor/i_qoffset` 与 `b_qfactor/b_qoffset` 分别设置 \<QPP\> 与 \<QPI\>、\<QPP\> 与 \<QPB\> 之间的差值。

- 将 `coder` 选项设为值 \<vlc\> 会使 H.264 编码器使用 CAVLC 而非 CABAC。

### 通用选项

以下选项为所有 qsv 编码器所用。

- **`async_depth`** 指定应用在显式同步结果之前执行的异步操作数。为零时表示未指定该值。

- **`preset`** 该选项列出从 veryfast（最快速度）到 veryslow（最佳质量）的一系列选择。

  - **`veryfast`**

  - **`faster`**

  - **`fast`**

  - **`medium`**

  - **`slow`**

  - **`slower`**

  - **`veryslow`**

- **`forced_idr`** 强制将 I 帧作为 IDR 帧。

- **`low_power`** 对编码器将此标志设为 ON 以降低功耗与 GPU 占用。

### 运行时选项

以下选项可在 qsv 编码期间使用。

- **`global_quality`**

- **`i_quant_factor`**

- **`i_quant_offset`**

- **`b_quant_factor`**

- **`b_quant_offset`** 在 h264_qsv 与 hevc_qsv 中支持。更改这些值将重置 qsv 编解码器的 qp 配置。

- **`max_frame_size`** 在 h264_qsv 与 hevc_qsv 中支持。更改该值将重置 qsv 编解码器的 MaxFrameSize 配置。

- **`gop_size`** 更改该值将重置 qsv 编解码器的 gop 配置。

- **`int_ref_type`**

- **`int_ref_cycle_size`**

- **`int_ref_qp_delta`**

- **`int_ref_cycle_dist`** 在 h264_qsv 与 hevc_qsv 中支持。更改这些值将重置 qsv 编解码器的 Intra Refresh 配置。

- **`qmax`**

- **`qmin`**

- **`max_qp_i`**

- **`min_qp_i`**

- **`max_qp_p`**

- **`min_qp_p`**

- **`max_qp_b`**

- **`min_qp_b`** 在 h264_qsv 中支持。更改这些值将重置 qsv 编解码器的 max/min qp 配置。

- **`low_delay_brc`** 在 h264_qsv、hevc_qsv 与 av1_qsv 中支持。更改该值将重置 qsv 编解码器的 low_delay_brc 配置。

- **`framerate`** 更改该值将重置 qsv 编解码器的帧率配置。

- **`bit_rate`**

- **`rc_buffer_size`**

- **`rc_initial_buffer_occupancy`**

- **`rc_max_rate`** 更改这些值将重置 qsv 编解码器的码率控制配置。

- **`pic_timing_sei`** 在 h264_qsv 与 hevc_qsv 中支持。更改该值将重置 qsv 编解码器的 pic_timing_sei 配置。

- **`qsv_params`** 以冒号分隔的键值对列表设置 QSV 编码器参数。

  `qsv_params` 的格式应为 `key1=value1:key2=value2:...`。

  这些参数通过 MFXSetParameter 函数直接传递给底层 Intel Quick Sync Video (QSV) 编码器。

  示例：

  ``` text
  ffmpeg -i input.mp4 -c:v h264_qsv -qsv_params "CodingOption1=1:CodingOption2=2" output.mp4
  ```

  该选项允许对 QSV 编码器提供的各种编码器专属设置进行细粒度控制。

### H264 选项

以下选项为 h264_qsv 所用

- **`extbrc`** 扩展码率控制。

- **`recovery_point_sei`** 设置此标志以在每个帧内刷新周期开始处插入恢复点 SEI 消息。

- **`rdo`** 启用率失真优化。

- **`max_frame_size`** 以字节为单位的最大编码帧大小。

- **`max_frame_size_i`** 以字节为单位的 I 帧最大编码帧大小。该值设为大于零时，I 帧将忽略 max_frame_size 设置的值。

- **`max_frame_size_p`** 以字节为单位的 P 帧最大编码帧大小。该值设为大于零时，P 帧将忽略 max_frame_size 设置的值。

- **`max_slice_size`** 以字节为单位的最大编码小片大小。

- **`bitrate_limit`** 切换码率限制。将码率修改为 QSV 编码器强制的范围内。关闭此标志可能违反 HRD 一致性。注意将码率指定在 QSV 编码器范围以下可能显著影响质量。开启时该选项在非 CQP 模式下生效：若码率不在 QSV 编码器强制的范围内，将被改为落在该范围内。

- **`mbbrc`** 设置此标志启用宏块级码率控制，通常提升主观视觉质量。启用此标志可能对性能与客观视觉质量指标产生负面影响。

- **`low_delay_brc`** 设置此标志开启或关闭 qsv 插件中的 LowDelayBRC 特性，它提供更精确的码率控制以逐帧最小化比特流大小的方差。取值：-1-默认 0-关 1-开

- **`adaptive_i`** 此标志控制 QSV 编码器插入 I 帧。开启此标志允许把帧类型从 P 和 B 改为 I。

- **`adaptive_b`** 此标志控制把帧类型从 B 改为 P。

- **`p_strategy`** 启用 P 金字塔：0-默认 1-简单 2-金字塔（bf 需设为 0）。

- **`b_strategy`** 该选项控制 B 帧作为参考的使用。

- **`dblk_idc`** 该选项禁用去块。取值范围 0~2。

- **`cavlc`** 设置时使用 CAVLC；未设置时使用 CABAC 编码。

- **`vcm`** 视频会议模式，参见码率控制方法。

- **`idr_interval`** IDR 帧之间的距离（以 I 帧计）。

- **`pic_timing_sei`** 插入带 pic_struct_syntax 元素的图像计时 SEI。

- **`single_sei_nal_unit`** 将所有 SEI 消息放入一个 NALU。

- **`max_dec_frame_buffering`** DPB 中缓冲的最大帧数。

- **`look_ahead`** 使用带前瞻的 VBR 算法。

- **`look_ahead_depth`** 前瞻深度，以帧数计。

- **`look_ahead_downsampling`** 为前瞻分析保存的帧的降采样因子。

  - **`unknown`**

  - **`auto`**

  - **`off`**

  - **`2x`**

  - **`4x`**

- **`int_ref_type`** 指定帧内刷新类型。帧内刷新的主要目标是提升错误恢复能力，同时不显著增加 I 帧造成的编码比特流大小。SDK 编码器通过在刷新周期内使用帧内宏块编码每帧的一部分来实现。\<none\> 表示不刷新。\<vertical\> 表示垂直刷新，按宏块列。\<horizontal\> 表示水平刷新，按宏块行。\<slice\> 表示按小片的水平刷新，无重叠。\<slice\> 情况下 in_ref_cycle_size 被忽略。要启用帧内刷新，B 帧应设为 0。

- **`int_ref_cycle_size`** 指定刷新周期内的图像数，从 2 开始。0 和 1 是无效值。

- **`int_ref_qp_delta`** 指定插入帧内宏块的 QP 差值。这是带符号值：亮度样本目标编码位深为 8 时范围 \[-51, 51\]，10 位深时为 \[-63, 63\]，12 位深时为 \[-75, 75\]。

- **`int_ref_cycle_dist`** 帧内刷新周期起点之间的距离（以帧计）。

- **`profile`**

  - **`unknown`**

  - **`baseline`**

  - **`main`**

  - **`high`**

- **`a53cc`** 使用 A53 隐藏式字幕（若可用）。

- **`aud`** 插入访问单元分隔符 NAL。

- **`mfmode`** 多帧模式。

  - **`off`**

  - **`auto`**

- **`repeat_pps`** 每帧重复 pps。

- **`max_qp_i`** I 帧最大视频量化器缩放。

- **`min_qp_i`** I 帧最小视频量化器缩放。

- **`max_qp_p`** P 帧最大视频量化器缩放。

- **`min_qp_p`** P 帧最小视频量化器缩放。

- **`max_qp_b`** B 帧最大视频量化器缩放。

- **`min_qp_b`** B 帧最小视频量化器缩放。

- **`scenario`** 向编码器提示编码会话的场景。

  - **`unknown`**

  - **`displayremoting`**

  - **`videoconference`**

  - **`archive`**

  - **`livestreaming`**

  - **`cameracapture`**

  - **`videosurveillance`**

  - **`gamestreaming`**

  - **`remotegaming`**

- **`avbr_accuracy`** AVBR 码率控制的精度（单位为十分之一百分点）。

- **`avbr_convergence`** AVBR 码率控制的收敛（单位为 100 帧）

  参数 \<avbr_accuracy\> 与 \<avbr_convergence\> 用于平均可变码率控制 (AVBR) 算法。该算法在满足指定码率 \<target_bitrate\>（精度范围 \<avbr_accuracy\> 内）的前提下，经过 \<avbr_Convergence\> 周期后关注整体编码质量。该方法不遵循 HRD，即时码率不封顶也不填充。

- **`skip_frame`** 编码时使用逐帧元数据 "qsv_skip_frame" 跳帧。该选项定义此元数据的用法。

  - **`no_skip`** 禁用跳帧。

  - **`insert_dummy`** 编码器向比特流插入一个所有宏块都编码为跳过的帧。

  - **`insert_nothing`** 类似 insert_dummy，但编码器不向比特流插入任何内容。跳过的帧仍参与码率控制。例如 gop 仍包含跳过的帧，且跳过帧之后的帧会更大。

  - **`brc_only`** skip_frame 元数据指示当前帧之前错过的帧数。

### HEVC 选项

以下选项为 hevc_qsv 所用

- **`extbrc`** 扩展码率控制。

- **`recovery_point_sei`** 设置此标志以在每个帧内刷新周期开始处插入恢复点 SEI 消息。

- **`rdo`** 启用率失真优化。

- **`max_frame_size`** 以字节为单位的最大编码帧大小。

- **`max_frame_size_i`** 以字节为单位的 I 帧最大编码帧大小。该值设为大于零时，I 帧将忽略 max_frame_size 设置的值。

- **`max_frame_size_p`** 以字节为单位的 P 帧最大编码帧大小。该值设为大于零时，P 帧将忽略 max_frame_size 设置的值。

- **`max_slice_size`** 以字节为单位的最大编码小片大小。

- **`mbbrc`** 设置此标志启用宏块级码率控制，通常提升主观视觉质量。启用此标志可能对性能与客观视觉质量指标产生负面影响。

- **`low_delay_brc`** 设置此标志开启或关闭 qsv 插件中的 LowDelayBRC 特性，它提供更精确的码率控制以逐帧最小化比特流大小的方差。取值：-1-默认 0-关 1-开

- **`adaptive_i`** 此标志控制 QSV 编码器插入 I 帧。开启此标志允许把帧类型从 P 和 B 改为 I。

- **`adaptive_b`** 此标志控制把帧类型从 B 改为 P。

- **`p_strategy`** 启用 P 金字塔：0-默认 1-简单 2-金字塔（bf 需设为 0）。

- **`b_strategy`** 该选项控制 B 帧作为参考的使用。

- **`dblk_idc`** 该选项禁用去块。取值范围 0~2。

- **`idr_interval`** IDR 帧之间的距离（以 I 帧计）。

  | Term           | Description                                              |
  |----------------|----------------------------------------------------------|
  | `begin_only` | 仅在流开始处输出一个 IDR 帧。 |

- **`load_plugin`** 在内部会话中加载的用户插件。

  - **`none`**

  - **`hevc_sw`**

  - **`hevc_hw`**

- **`load_plugins`** 以":"分隔的十六进制插件 UID 列表，将在内部会话中加载。

- **`look_ahead_depth`** 前瞻深度，以帧数计，extbrc 选项启用时可用。

- **`profile`** 设置编码 profile（scc 要求 libmfx \>= 1.32）。

  - **`unknown`**

  - **`main`**

  - **`main10`**

  - **`mainsp`**

  - **`rext`**

  - **`scc`**

- **`tier`** 设置编码层（仅 level \>= 4 支持 high 层）。该选项仅在指定 level 选项时生效。

  - **`main`**

  - **`high`**

- **`gpb`** 1：GPB（广义 P/B 帧）

  0：常规 P 帧。

- **`tile_cols`** 瓦片编码的列数。

- **`tile_rows`** 瓦片编码的行数。

- **`aud`** 插入访问单元分隔符 NAL。

- **`pic_timing_sei`** 插入带 pic_struct_syntax 元素的图像计时 SEI。

- **`transform_skip`** 开启该选项启用 transformskip。ICL 及更新平台支持。

- **`int_ref_type`** 指定帧内刷新类型。帧内刷新的主要目标是提升错误恢复能力，同时不显著增加 I 帧造成的编码比特流大小。SDK 编码器通过在刷新周期内使用帧内宏块编码每帧的一部分来实现。\<none\> 表示不刷新。\<vertical\> 表示垂直刷新，按宏块列。\<horizontal\> 表示水平刷新，按宏块行。\<slice\> 表示按小片的水平刷新，无重叠。\<slice\> 情况下 in_ref_cycle_size 被忽略。要启用帧内刷新，B 帧应设为 0。

- **`int_ref_cycle_size`** 指定刷新周期内的图像数，从 2 开始。0 和 1 是无效值。

- **`int_ref_qp_delta`** 指定插入帧内宏块的 QP 差值。这是带符号值：亮度样本目标编码位深为 8 时范围 \[-51, 51\]，10 位深时为 \[-63, 63\]，12 位深时为 \[-75, 75\]。

- **`int_ref_cycle_dist`** 帧内刷新周期起点之间的距离（以帧计）。

- **`max_qp_i`** I 帧最大视频量化器缩放。

- **`min_qp_i`** I 帧最小视频量化器缩放。

- **`max_qp_p`** P 帧最大视频量化器缩放。

- **`min_qp_p`** P 帧最小视频量化器缩放。

- **`max_qp_b`** B 帧最大视频量化器缩放。

- **`min_qp_b`** B 帧最小视频量化器缩放。

- **`scenario`** 向编码器提示编码会话的场景。

  - **`unknown`**

  - **`displayremoting`**

  - **`videoconference`**

  - **`archive`**

  - **`livestreaming`**

  - **`cameracapture`**

  - **`videosurveillance`**

  - **`gamestreaming`**

  - **`remotegaming`**

- **`avbr_accuracy`** AVBR 码率控制的精度（单位为十分之一百分点）。

- **`avbr_convergence`** AVBR 码率控制的收敛（单位为 100 帧）

  参数 \<avbr_accuracy\> 与 \<avbr_convergence\> 用于平均可变码率控制 (AVBR) 算法。该算法在满足指定码率 \<target_bitrate\>（精度范围 \<avbr_accuracy\> 内）的前提下，经过 \<avbr_Convergence\> 周期后关注整体编码质量。该方法不遵循 HRD，即时码率不封顶也不填充。

- **`skip_frame`** 编码时使用逐帧元数据 "qsv_skip_frame" 跳帧。该选项定义此元数据的用法。

  - **`no_skip`** 禁用跳帧。

  - **`insert_dummy`** 编码器向比特流插入一个所有宏块都编码为跳过的帧。

  - **`insert_nothing`** 类似 insert_dummy，但编码器不向比特流插入任何内容。跳过的帧仍参与码率控制。例如 gop 仍包含跳过的帧，且跳过帧之后的帧会更大。

  - **`brc_only`** skip_frame 元数据指示当前帧之前错过的帧数。

### MPEG2 选项

以下选项为 mpeg2_qsv 所用

- **`profile`**

  - **`unknown`**

  - **`simple`**

  - **`main`**

  - **`high`**

### VP9 选项

以下选项为 vp9_qsv 所用

- **`profile`**

  - **`unknown`**

  - **`profile0`**

  - **`profile1`**

  - **`profile2`**

  - **`profile3`**

- **`tile_cols`** 瓦片编码的列数（要求 libmfx \>= 1.29）。

- **`tile_rows`** 瓦片编码的行数（要求 libmfx \>= 1.29）。

### AV1 选项

以下选项为 av1_qsv 所用（要求 libvpl）。

- **`profile`**

  - **`unknown`**

  - **`main`**

- **`tile_cols`** 瓦片编码的列数。

- **`tile_rows`** 瓦片编码的行数。

- **`adaptive_i`** 此标志控制 QSV 编码器插入 I 帧。开启此标志允许把帧类型从 P 和 B 改为 I。

- **`adaptive_b`** 此标志控制把帧类型从 B 改为 P。

- **`b_strategy`** 该选项控制 B 帧作为参考的使用。

- **`extbrc`** 扩展码率控制。

- **`look_ahead_depth`** 前瞻深度，以帧数计，extbrc 选项启用时可用。

- **`low_delay_brc`** 设置此标志开启或关闭 qsv 插件中的 LowDelayBRC 特性，它提供更精确的码率控制以逐帧最小化比特流大小的方差。取值：-1-默认 0-关 1-开

- **`max_frame_size`** 设置每帧允许的最大字节大小。帧大小超出限制时，编码器将调整 QP 值以控制帧大小。CQP 码率控制模式下无效。

- **`max_frame_size_i`** 以字节为单位的 I 帧最大编码帧大小。该值设为大于零时，I 帧将忽略 max_frame_size 设置的值。

- **`max_frame_size_p`** 以字节为单位的 P 帧最大编码帧大小。该值设为大于零时，P 帧将忽略 max_frame_size 设置的值。

## snow

### 选项

| Term                 | Description                                  |
|----------------------|----------------------------------------------|
| `iterative_dia_size` | 迭代运动估计的 dia 大小 |

## VAAPI 编码器

可通过 VAAPI 访问的硬件编码器封装器。

这些编码器只接受 VAAPI 硬件表面的输入。若输入为软件帧，请使用 `hwupload` 滤镜将其上传到 GPU。

使用以下标准 libavcodec 选项：

- `g` / `gop_size`

- `bf` / `max_b_frames`

- `profile`

  未设置时将依据输入帧格式与驱动支持的 profile 自动确定。

- `level`

- `b` / `bit_rate`

- `maxrate` / `rc_max_rate`

- `bufsize` / `rc_buffer_size`

- `rc_init_occupancy` / `rc_initial_buffer_occupancy`

- `compression_level`

  速度/质量权衡：值越大越快/质量越差。

- `q` / `global_quality`

  大小/质量权衡：值越大越小/质量越差。

- `qmin`

- `qmax`

- `i_qfactor` / `i_quant_factor`

- `i_qoffset` / `i_quant_offset`

- `b_qfactor` / `b_quant_factor`

- `b_qoffset` / `b_quant_offset`

- `slices`

所有编码器均支持以下选项：

- **`low_power`** 部分驱动/平台为某些编解码器提供第二种编码器，其功耗低于默认编码器；设置该选项将尝试使用那个编码器。注意它可能只支持精简特性集，因此该模式下某些其他选项可能不可用。

- **`idr_interval`** 在开放 GOP 模式下设置全刷新 (IDR) 帧之间普通帧内帧的数量。这些帧内帧仍是 IRAP，但不包含全局头，且可能带有不可解码的引导图像。

- **`b_depth`** 设置 B 帧参考深度。设为 1（默认）时，所有 B 帧只参考 P 帧或 I 帧。设为更大值时将出现多层 B 帧，每层中的帧只参考更高层中的帧。

- **`async_depth`** 最大处理并行度。增大它可提升单通道性能。驱动未实现 vaSyncBuffer 函数时该选项无效。使用大量 async_depth 时请确保分配了足够的 hw_frames。

- **`max_frame_size`** 设置每帧允许的最大字节大小。帧大小超出限制时，编码器将调整 QP 值以控制帧大小。CQP 码率控制模式下无效。

- **`rc_mode`** 设置要使用的码率控制模式。给定驱动可能只支持模式的一个子集。

  可能的模式：

  - **`auto`** 依据驱动支持与其他选项自动选择模式。这是默认值。

  - **`CQP`** 恒定质量。

  - **`CBR`** 恒定码率。

  - **`VBR`** 可变码率。

  - **`ICQ`** 智能恒定质量。

  - **`QVBR`** 质量定义的可变码率。

  - **`AVBR`** 平均可变码率。

- **`blbrc`** 启用块级码率控制，逐块分配不同码率。CQP 模式下无效。

每个编码器还有自己的专属选项：

- **`av1_vaapi`** `profile` 设置 *seq_profile* 的值。`tier` 设置 *seq_tier* 的值。`level` 设置 *seq_level_idx* 的值。

  - **`tiles`** 设置编码输入视频使用的瓦片数，格式为 列 x 行。（默认为 auto，即使用最少的瓦片列/行数）。

  - **`tile_groups`** 设置瓦片组数。所有瓦片将尽可能均匀地分配到每个瓦片组。（默认为 1）。

- **`h264_vaapi`** `profile` 设置 *profile_idc* 与 *constraint_set\*\_flag*s 的值。`level` 设置 *level_idc* 的值。

  - **`coder`** 设置熵编码器（默认为 *cabac*）。可取的值：

    - **`ac`**

    - **`cabac`** 使用 CABAC。

    - **`vlc`**

    - **`cavlc`** 使用 CAVLC。

  - **`aud`** 在流中包含访问单元分隔符（默认不包含）。

  - **`sei`** 设置要包含的 SEI 消息类型。以下值的某种组合：

    - **`identifier`** 包含 *user_data_unregistered* 消息，内含编码器相关信息。

    - **`timing`** 包含图像计时参数（*buffering_period* 与 *pic_timing* 消息）。

    - **`recovery_point`** 在适当处包含恢复点（*recovery_point* 消息）。

- **`hevc_vaapi`** `profile` 与 `level` 分别设置 *general_profile_idc* 与 *general_level_idc* 的值。

  - **`aud`** 在流中包含访问单元分隔符（默认不包含）。

  - **`tier`** 设置 *general_tier_flag*。未显式指定时可能影响为流选择的 level。

  - **`sei`** 设置要包含的 SEI 消息类型。以下值的某种组合：

    - **`hdr`** 输入帧带有 HDR 元数据时包含它（*mastering_display_colour_volume* 与 *content_light_level* 消息）。

  - **`tiles`** 设置编码输入视频使用的瓦片数，格式为 列 x 行。更大的数字允许编码与解码更大的并行度，但可能降低编码效率。

- **`mjpeg_vaapi`** 仅支持基线 DCT 编码。编码器总是使用标准量化与 huffman 表——`global_quality` 缩放标准量化表（范围 1-100）。

  对 YUV，支持 4:2:0、4:2:2 与 4:4:4 二次采样模式。也支持 RGB，将创建 RGB JPEG。

  - **`jfif`** 每帧包含 JFIF 头（默认不包含）。

  - **`huffman`** 包含标准 huffman 表（默认开）。关闭它可在每个输出帧中节省几百字节，但可能失去与某些不能完整处理 MJPEG 的 JPEG 解码器的兼容性。

- **`mpeg2_vaapi`** `profile` 与 `level` 设置 *profile_and_level_indication* 的值。

- **`vp8_vaapi`** 不支持 B 帧。

  `global_quality` 设置非关键帧使用的 *q_idx*（范围 0-127）。

  - **`loop_filter_level`**

  - **`loop_filter_sharpness`** 手动设置环路滤波参数。

- **`vp9_vaapi`** `global_quality` 设置 P 帧使用的 *q_idx*（范围 0-255）。

  - **`loop_filter_level`**

  - **`loop_filter_sharpness`** 手动设置环路滤波参数。

  支持 B 帧，但输出流总是编码顺序而非显示顺序。启用 B 帧时，可能需要使用 `vp9_raw_reorder` 比特流滤镜修改输出流，使帧按正确顺序显示。

  只产出普通帧——可能需要 `vp9_superframe` 比特流滤镜才能产出可用于所有解码器的流。

## vbn

Vizrt Binary Image 编码器。

广播厂商 Vizrt 使用该格式进行快速纹理串流。该格式的高级特性（如纹理数据的 LZW 压缩或 mipmap 生成）不受支持。

### 选项

- **`format string`** 设置 VBN 文件使用的纹理压缩。可为 \<dxt1\>、\<dxt5\> 或 \<raw\>。默认为 \<dxt5\>。

## vc2

SMPTE VC-2（先前称 BBC Dirac Pro）。该编解码器主要面向专业广播，但由于它支持 8（受限范围或全范围）、10 或 12 位的 yuv420、yuv422 与 yuv444，也适合其他需要低开销与低压缩比的任务（如屏幕录制）。

### 选项

- **`b`** 设置目标视频码率。通常约为未压缩视频码率的 1:6（如 1920x1080 50fps yuv422p10 约为 400Mbps）。更高的值（接近未压缩码率）开启无损压缩模式。

- **`field_order`** 隔行输入设置它（如 tt——顶场在前）时启用场编码。它会拆分各场并分别编码，因此对隔行内容应能提升压缩率。

- **`wavelet_depth`** 设置应用的小波变换总层数，取值 1 到 5（默认）。更低的值降低压缩率与质量。能力较弱的解码器可能无法处理超过 3 的 `wavelet_depth` 值。

- **`wavelet_type`** 设置变换类型。目前仅实现 \<5_3\> (LeGall) 与 \<9_7\> (Deslauriers-Dubuc)，其中 9_7 压缩更好，因此为默认。

- **`slice_width`**

- **`slice_height`** 设置每个小片的大小。更大的值带来更好的压缩。为与其他能力较弱的解码器兼容，使用 `slice_width` 32 与 `slice_height` 8。

- **`tolerance`** 以百分比设置码率控制系统的欠冲容差。这是为了避免运行昂贵的搜索。

- **`qm`** 设置默认使用或 `wavelet_depth` 设为 5 时使用的量化矩阵预设

  - − \<default\> 使用规范中的默认量化矩阵，并扩展第五级的值。这能在保留细节与省略伪影之间取得良好平衡。

  - − \<flat\> 使用完全置零的量化矩阵。这提升 PSNR 但可能降低观感。适合用在无意义的基准测试中。

  - − \<color\> 减少细节，但在极低码率下尽量保留颜色。

# 字幕编码器

## dvbsub

该编解码器编码 DVB 广播与录制中使用的位图字幕格式。位图通常作为独立的流嵌入 MPEG-TS 等容器中。

### 选项

- **`min_bpp integer (2, 4, or 8)`** 为字幕颜色查找表设置最小每像素比特值。

  DVB 支持 2、4 与 8 每像素比特的颜色查找表。该选项允许无论颜色数量多少都强制特定每像素比特值。由于并非所有播放器都支持或正确支持 2 每像素比特，该值默认为 4。

## dvdsub

该编解码器编码 DVD 中使用的位图字幕格式。它们通常存储于 VOBSUB 文件对（\*.idx + \*.sub），也可用于 Matroska 文件。

### 选项

- **`palette`** 指定位图使用的全局调色板。

  该选项的格式是一个包含 16 个 24 位十六进制数（不带 0x 前缀）的字符串，各数以逗号分隔，例如 `0d00ee, ee450d, 101010, eaeaea, 0ce60b, ec14ed, ebff0b, 0d617a, 7b7b7b, d1d1d1, 7b2a0e, 0d950c, 0f007b, cf0dec, cfa80c, 7c127b`。

- **`even_rows_fix`** 设为 1 时启用一种变通，使所有字幕的像素行数为偶数。这修复部分播放器在行数为奇数时切掉底部行的问题。该变通只是在需要时添加一个完全透明的行。开销很低，平均每个字幕通常一个字节。

  默认禁用该变通。

## lrc

该编解码器编码 LRC 歌词格式。

### 选项

- **`precision`** 指定时间戳小数部分的精度。时间基依据该值确定。

  默认为 2，即百分之一秒。

# 另请参见

ffmpeg(1), ffplay(1), ffprobe(1), libavcodec(3)
