# 描述

本文档介绍 libavcodec 库提供的比特流滤镜。

比特流滤镜作用于已编码的流数据，在不进行解码的情况下执行比特流级别的修改。

# 比特流滤镜

配置 FFmpeg 构建时，所有受支持的比特流滤镜默认启用。可以使用 configure 选项 `--list-bsfs` 列出全部可用项。

可以使用 configure 选项 `--disable-bsfs` 禁用全部比特流滤镜，并使用选项 `--enable-bsf=BSF` 选择性启用任意比特流滤镜，也可以使用选项 `--disable-bsf=BSF` 禁用特定的比特流滤镜。

ff\* 工具的 `-bsfs` 选项将显示你的构建中包含的全部受支持比特流滤镜的列表。

ff\* 工具具有一个按流应用的 -bsf 选项，它接受以逗号分隔的滤镜列表，滤镜参数跟在滤镜名之后，以 '=' 分隔。

``` text
ffmpeg -i INPUT -c:v copy -bsf:v filter1[=opt1=str1:opt2=str2][,filter2] OUTPUT
```

下面介绍当前可用的比特流滤镜及其参数（如有）。

## aac_adtstoasc

将 MPEG-2/4 AAC ADTS 转换为 MPEG-4 AudioSpecificConfig 比特流。

此滤镜从 MPEG-2/4 ADTS 头创建 MPEG-4 AudioSpecificConfig，并移除该 ADTS 头。

例如，将 AAC 流从原始 ADTS AAC 或 MPEG-TS 容器复制到 MP4A-LATM、FLV 文件，或 MOV/MP4 文件及 3GP、M4A 等相关格式时，就需要此滤镜。请注意，对于 MP4A-LATM 与 MOV/MP4 及相关格式，该滤镜会被自动插入。

## av1_metadata

修改嵌入在 AV1 流中的元数据。

- **`td`** 在流的全部时间单元中插入或移除时间分隔符 OBU。

  | Term | Description |
  |----|----|
  | `insert` | 在每个尚无 TD 的 TU 开头插入一个 TD。 |
  | `remove` | 从每个已有 TD 的 TU 开头移除 TD。 |

- **`color_primaries`**

- **`transfer_characteristics`**

- **`matrix_coefficients`** 设置流中的颜色描述字段（参见 AV1 规范 6.4.2 节）。

- **`color_range`** 设置流中的颜色范围（参见 AV1 规范 6.4.2 节；注意使用 BT.709 基色、sRGB 传递特性以及恒等 (RGB) 矩阵系数的流无法设置此项）。

  | Term   | Description    |
  |--------|----------------|
  | `tv` | 有限范围。 |
  | `pc` | 全范围。    |

- **`chroma_sample_position`** 设置流中的色度采样位置（参见 AV1 规范 6.4.2 节）。只能为 4:2:0 流设置。

  | Term          | Description |
  |---------------|-------------|
  | `vertical`  | 左侧位置（与 MPEG-2 和 H.264 的默认值一致）。 |
  | `colocated` | 左上位置。 |

- **`tick_rate`** 在序列头的时序信息中设置 tick 率 (*time_scale / num_units_in_display_tick*)。

- **`num_ticks_per_picture`** 设置每幅图像的 tick 数，以指示流具有固定帧率。若未同时设置 `tick_rate` 则忽略此项。

- **`delete_padding`** 删除填充 OBU。

## chomp

移除包末尾的零填充。

## dca_core

从 DCA/DTS 流中提取核心部分，丢弃 DTS-HD 等扩展。

## dovi_rpu

操作 HEVC/AV1 比特流中的杜比视界 (Dolby Vision) 元数据，可选择启用元数据压缩。

- **`strip`** 若启用，从流中剥离全部杜比视界元数据（配置记录 + RPU 数据块）。

- **`compression`** 启用哪种压缩级别。

  - **`none`** 无元数据压缩。

  - **`limited`** 受限元数据压缩方案。应与大多数设备兼容。这是默认值。

  - **`extended`** 扩展元数据压缩。设备并不要求支持此级别。注意该级别目前在 libavcodec 中的行为与 `limited` 相同。

## dovi_split

拆分杜比视界 Profile 7 多层 HEVC 比特流。Profile 7 将增强层 HEVC 比特流交织在基础层访问单元内，封装在类型为 63 (UNSPEC63) 的用户未指定 NAL 单元中，并将 RPU 元数据作为类型为 62 (UNSPEC62) 的同级用户未指定 NAL 传输。

- **`mode`** 输出比特流中保留哪些杜比视界组件。

  - **`bl`** 仅基础层：丢弃所有 UNSPEC63 (EL) 和所有 UNSPEC62 (RPU)。输出是不带杜比视界标记的普通 HEVC 流。这是默认值。

  - **`bl_rpu`** 保留 RPU NAL 的基础层。

  - **`el`** 仅增强层：对每个 UNSPEC63 NAL，剥去两字节的外层 NAL 头并输出内部载荷。结果是一个独立的 HEVC 比特流。UNSPEC62 (RPU) 被丢弃。

  - **`el_rpu`** 逐字保留 RPU NAL 的增强层。与 `el` 相同，但 UNSPEC62 RPU NAL 也会与解封装后的 EL NAL 一并输出。

## dump_extra

将 extradata 添加到被过滤包的开头，除非这些包本身已经恰好以要添加的 extradata 开头。

- **`freq`** 额外参数指定应过滤哪些包。它接受以下取值：

  - **`k`**

  - **`keyframe`** 为所有关键包添加 extradata

  - **`e`**

  - **`all`** 为所有包添加 extradata

若未指定，则假定为 `k`。

例如，下面的 `ffmpeg` 命令在 `libx264` 编码器生成的 H.264 包中强制使用全局头（从而禁用逐包头部），并通过将存储在 extradata 中的头部添加到关键包来修正它们：

``` text
ffmpeg -i INPUT -map 0 -flags:v +global_header -c:v libx264 -bsf:v dump_extra out.ts
```

## dv_error_marker

DV 中被标记为受损的块会被指定颜色的块替换。

- **`color`** 用于替换受损块的颜色

- **`sta`** 一个 16 位掩码，指定 16 个可能的错误状态值中哪些要被彩色块替换。默认值 0xFFFE 会替换所有非 0 的错误状态值。

  | Term | Description |
  |----|----|
  | `ok` | 无错误，无隐藏 |
  | `err` | 有错误，无隐藏 |
  | `res` | 保留 |
  | `notok` | 有错误或有隐藏 |
  | `notres` | 非保留 |
  | `Aa, Ba, Ca, Ab, Bb, Cb, A, B, C, a, b, erri, erru` | 具体的错误状态码 |

  参见 <http://web.archive.org/web/20060927044735/http://www.smpte.org/smpte_store/standards/pdf/s314m.pdf> 的第 44-46 页或 5.5 节。

## eac3_core

从 E-AC-3 流中提取核心部分，丢弃额外的声道。

## eia608_to_smpte436m

将 `EIA_608` 流转换为 `SMPTE_436M_ANC` 数据流，把隐藏式字幕封装在 CTA-708 CDP VANC 包中。

- **`line_number`** 选择生成的 VANC 包应放在哪一行。通常应选择第 9 行（默认值）或第 11 行。

- **`wrapping_type`** 选择 SMPTE 436M 封装类型，默认为 `vanc_frame`。它接受以下取值：

  - **`vanc_frame`** VANC 帧（隔行或分段逐行帧）

  - **`vanc_field_1`**

  - **`vanc_field_2`**

  - **`vanc_progressive_frame`**

- **`sample_coding`** 选择 SMPTE 436M 采样编码，默认为 `8bit_luma`。它接受以下取值：

  | Term | Description |
  |----|----|
  | `8bit_luma` | 8 位分量亮度采样 |
  | `8bit_color_diff` | 8 位分量色差采样 |
  | `8bit_luma_and_color_diff` | 8 位分量亮度和色差采样 |
  | `10bit_luma` | 10 位分量亮度采样 |
  | `10bit_color_diff` | 10 位分量色差采样 |
  | `10bit_luma_and_color_diff` | 10 位分量亮度和色差采样 |
  | `8bit_luma_parity_error` | 带奇偶校验错误的 8 位分量亮度采样 |
  | `8bit_color_diff_parity_error` | 8 位分量色差采样带奇偶校验错误 |
  | `8bit_luma_and_color_diff_parity_error` | 8 位分量亮度和色差采样带奇偶校验错误 |

- **`initial_cdp_sequence_cntr`** CDP 的 16 位无符号整数字段 `cdp_hdr_sequence_cntr` 与 `cdp_ftr_sequence_cntr` 的初始值。默认为 0。

- **`cdp_frame_rate`** 设置 CDP 的 `cdp_frame_rate` 字段。这并不会真正改变数据流的时序，只是改变生成的 CDP 包中该字段插入的值。默认为 `30000/1001`。

## extract_extradata

提取带内 (in-band) extradata。

某些编解码器允许长期头信息（如 MPEG-2 序列头，或 H.264/HEVC 的 (VPS/)SPS/PPS）以"带内"方式（即作为包含已编码帧的比特流的一部分）或"带外"方式（如在容器层面）传输。后一种形式在 FFmpeg 术语中称为 extradata。

此比特流滤镜检测带内头信息并使其作为 extradata 可用。

- **`remove`** 启用此选项后，长期头信息会在提取后从比特流中移除。

## filter_units

从流中移除类型属于或不属于给定集合的单元。

- **`pass_types`** 要放行的单元类型或类型范围列表，同时移除所有其他单元。以 '\|' 分隔的单元类型值列表或用 '-' 表示的值范围列表形式指定。

- **`remove_types`** 与 `pass_types` 相同，区别在于给定集合中的单元被移除，所有其他单元被放行。

pass_types 与 remove_types 所用的类型对应 H.264、HEVC 和 H.266 中的 NAL 单元类型 (nal_unit_type)（参见 H.264 和 HEVC 规范的表 7-1 或 H.266 规范的表 5）、JPEG 的标记值（不含 0xFF 前缀），以及 MPEG-2 的起始码（不含起始码前缀，即 0x000001 之后的字节）。对 VP8 和 VP9，每个单元的类型均为零。

extradata 不会被此变换改变，但请注意，如果流中包含内联参数集，则移除它们后输出可能不可用。

例如，从 H.264 流中移除所有非 VCL NAL 单元：

``` text
ffmpeg -i INPUT -c:v copy -bsf:v 'filter_units=pass_types=1-5' OUTPUT
```

从 H.265 流中移除所有 AUD、SEI 和填充数据：

``` text
ffmpeg -i INPUT -c:v copy -bsf:v 'filter_units=remove_types=35|38-40' OUTPUT
```

从 MPEG-2 流中移除所有用户数据（包括隐藏式字幕）：

``` text
ffmpeg -i INPUT -c:v copy -bsf:v 'filter_units=remove_types=178' OUTPUT
```

从 H264 流中移除所有 SEI（包括隐藏式字幕）：

``` text
ffmpeg -i INPUT -c:v copy -bsf:v 'filter_units=remove_types=6' OUTPUT
```

从 HEVC 流中移除所有前缀和后缀 SEI（包括隐藏式字幕和动态 HDR）：

``` text
ffmpeg -i INPUT -c:v copy -bsf:v 'filter_units=remove_types=39|40' OUTPUT
```

## hapqa_extract

从 HAPQA 文件中提取 RGB 或 Alpha 部分，无需重新压缩，从而创建 HAPQ 或 HAPAlphaOnly 文件。

- **`texture`** 指定要保留的纹理。

  - **`color`**

  - **`alpha`**

将 HAPQA 转换为 HAPQ

``` text
ffmpeg -i hapqa_inputfile.mov -c copy -bsf:v hapqa_extract=texture=color -tag:v HapY -metadata:s:v:0 encoder="HAPQ" hapq_file.mov
```

将 HAPQA 转换为 HAPAlphaOnly

``` text
ffmpeg -i hapqa_inputfile.mov -c copy -bsf:v hapqa_extract=texture=alpha -tag:v HapA -metadata:s:v:0 encoder="HAPAlpha Only" hapalphaonly_file.mov
```

## h264_metadata

修改嵌入在 H.264 流中的元数据。

- **`aud`** 在流的全部访问单元中插入或移除 AUD NAL 单元。

  - **`pass`**

  - **`insert`**

  - **`remove`**

  默认值为 pass。

- **`sample_aspect_ratio`** 在 VUI 参数中设置流的采样宽高比。参见 H.264 表 E-1。

- **`overscan_appropriate_flag`** 设置该流是否适合使用过扫描 (overscan) 显示（参见 H.264 规范 E.2.1 节）。

- **`video_format`**

- **`video_full_range_flag`** 设置流中的视频格式（参见 H.264 规范 E.2.1 节和表 E-2）。

- **`colour_primaries`**

- **`transfer_characteristics`**

- **`matrix_coefficients`** 设置流中的颜色描述（参见 H.264 规范 E.2.1 节和表 E-3、E-4、E-5）。

- **`chroma_sample_loc_type`** 设置流中的色度采样位置（参见 H.264 规范 E.2.1 节和图 E-1）。

- **`tick_rate`** 在 VUI 参数中设置 tick 率 (time_scale / num_units_in_tick)。这是流中可表示的最小时间单位，在许多情况下表示流的场率（帧率的两倍）。

- **`fixed_frame_rate_flag`** 设置流是否具有固定帧率——通常这表示帧率恰好是 tick 率的一半，但确切含义取决于隔行方式和图像结构（参见 H.264 规范 E.2.1 节和表 E-6）。

- **`zero_new_constraint_set_flags`** 将 SPS 中的 constraint_set4_flag 和 constraint_set5_flag 置零。这些位在 H.264 规范的先前版本中是保留位，因此某些硬件解码器要求它们为零。置零后的结果仍是有效的比特流。

- **`crop_left`**

- **`crop_right`**

- **`crop_top`**

- **`crop_bottom`** 在 SPS 中设置帧裁剪偏移。如果流已被裁剪，这些值将替换当前值。

  这些字段以像素为单位设置。注意，如果色度被子采样或流为隔行，某些尺寸可能无法表示（参见 H.264 规范 7.4.2.1.1 节）。

- **`sei_user_data`** 插入一个字符串作为 SEI 未注册用户数据。参数必须采用 *UUID+string* 形式，其中 UUID 为十六进制数字（可含连字符分隔），字符串可以是任意内容。

  例如，`086f3693-b7b3-4f2c-9653-21492feee5b8+hello` 将插入与给定 UUID 关联的字符串 "hello"。

- **`delete_filler`** 同时删除填充 NAL 单元和填充 SEI 消息。

- **`display_orientation`** 插入、提取或移除显示方向 (Display orientation) SEI 消息。语法与语义参见 H.264 规范 D.1.27 和 D.2.27 节。

  - **`pass`**

  - **`insert`**

  - **`remove`**

  - **`extract`**

  默认值为 pass。

  插入模式与 `rotate` 和 `flip` 选项配合使用。在插入或移除模式下，任何已存在的显示方向消息都会被移除。提取模式会将显示矩阵作为 side data 附加到包上。

- **`rotate`** 在显示方向 SEI 中设置旋转（逆时针角度，单位为度）。范围为 -360 到 +360。默认值为 NaN。

- **`flip`** 在显示方向 SEI 中设置翻转。

  - **`horizontal`**

  - **`vertical`**

  默认为未设置。

- **`level`** 在 SPS 中设置级别。参见 H.264 规范 A.3 节和表 A-1 至 A-5。

  参数必须是级别名称（例如 `4.2`）、level_idc 值（例如 `42`），或特殊名称 `auto`，后者表示滤镜应尝试根据输入流属性猜测级别。

## h264_mp4toannexb

将 H.264 比特流从长度前缀模式转换为起始码前缀模式（如 ITU-T H.264 规范附录 B 所定义）。

某些流媒体格式需要此转换，通常是 MPEG-2 传输流格式（复用器 `mpegts`）。

例如，使用 `ffmpeg` 将包含 H.264 流的 MP4 文件重新封装为 mpegts 格式，可以使用以下命令：

``` text
ffmpeg -i INPUT.mp4 -codec copy -bsf:v h264_mp4toannexb OUTPUT.ts
```

请注意，对于 MPEG-TS（复用器 `mpegts`）和原始 H.264（复用器 `h264`）输出格式，此滤镜会被自动插入。

## h264_redundant_pps

这对某些包含冗余 PPS 的 Blu-ray BDMV H264 流应用特定的修正。这些 PPS 会修改流中无关的参数，干扰需要正确 extradata 的其他变换。

用于这些受影响流的编码器会在整个流中添加额外的 PPS，改变初始 QP 以及是否启用加权预测。这会在将流复制到全局头容器后引发问题，因为起始的 PPS 不适合流的其余部分。例如，一个副作用是定位 (seek) 会返回乱码输出，直到新的 PPS 出现。

此 BSF 移除多余的 PPS 并重写小片 (slice) 头，使流在全局头中使用单一的前导 PPS，从而解决该问题。

## hevc_metadata

修改嵌入在 HEVC 流中的元数据。

- **`aud`** 在流的全部访问单元中插入或移除 AUD NAL 单元。

  - **`insert`**

  - **`remove`**

- **`sample_aspect_ratio`** 在 VUI 参数中设置流的采样宽高比。

- **`video_format`**

- **`video_full_range_flag`** 设置流中的视频格式（参见 H.265 规范 E.3.1 节和表 E.2）。

- **`colour_primaries`**

- **`transfer_characteristics`**

- **`matrix_coefficients`** 设置流中的颜色描述（参见 H.265 规范 E.3.1 节和表 E.3、E.4、E.5）。

- **`chroma_sample_loc_type`** 设置流中的色度采样位置（参见 H.265 规范 E.3.1 节和图 E.1）。

- **`tick_rate`** 在 VPS 和 VUI 参数中设置 tick 率 (time_scale / num_units_in_tick)。与 `num_ticks_poc_diff_one` 组合可在流中设置恒定帧率。注意当流位于容器中时，此项很可能被容器参数覆盖。

- **`num_ticks_poc_diff_one`** 在 VPS 和 VUI 中设置 poc_proportional_to_timing_flag，并使用此值设置 num_ticks_poc_diff_one_minus1（参见 H.265 规范 7.4.3.1 和 E.3.1 节）。若未同时设置 `tick_rate` 则忽略此项。

- **`crop_left`**

- **`crop_right`**

- **`crop_top`**

- **`crop_bottom`** 在 SPS 中设置一致性窗口 (conformance window) 裁剪偏移。如果流已被裁剪，这些值将替换当前值。

  这些字段以像素为单位设置。注意，如果色度被子采样，某些尺寸可能无法表示（H.265 规范 7.4.3.2.1 节）。

- **`width`**

- **`height`** 设置裁剪后的宽度和高度。

- **`level`** 在 VPS 和 SPS 中设置级别。参见 H.265 规范 A.4 节和表 A.6、A.7。

  参数必须是级别名称（例如 `5.1`）、*general_level_idc* 值（例如 5.1 级对应 `153`），或特殊名称 `auto`，后者表示滤镜应尝试根据输入流属性猜测级别。

## hevc_mp4toannexb

将 HEVC/H.265 比特流从长度前缀模式转换为起始码前缀模式（如 ITU-T H.265 规范附录 B 所定义）。

某些流媒体格式需要此转换，通常是 MPEG-2 传输流格式（复用器 `mpegts`）。

例如，使用 `ffmpeg` 将包含 HEVC 流的 MP4 文件重新封装为 mpegts 格式，可以使用以下命令：

``` text
ffmpeg -i INPUT.mp4 -codec copy -bsf:v hevc_mp4toannexb OUTPUT.ts
```

请注意，对于 MPEG-TS（复用器 `mpegts`）和原始 HEVC/H.265（复用器 `h265` 或 `hevc`）输出格式，此滤镜会被自动插入。

## imxdump

修改比特流以适配 MOV 并使其可被 Final Cut Pro 解码器使用。此滤镜仅适用于 mpeg2video 编解码器，对于配有适当 `-tag:v` 的 Final Cut Pro 7 及更新版本，很可能不需要此滤镜。

例如，将 30 MB/秒的 NTSC IMX 重新封装为 MOV：

``` text
ffmpeg -i input.mxf -c copy -bsf:v imxdump -tag:v mx3n output.mov
```

## mjpeg2jpeg

将 MJPEG/AVI1 包转换为完整的 JPEG/JFIF 包。

MJPEG 是一种视频编解码器，其中每个视频帧本质上都是一幅 JPEG 图像。各个帧可以无损提取，例如：

``` text
ffmpeg -i ../some_mjpeg.avi -c:v copy frames_%d.jpg
```

遗憾的是，这些数据块是不完整的 JPEG 图像，因为它们缺少解码所需的 DHT 段。引用 <http://www.digitalpreservation.gov/formats/fdd/fdd000063.shtml> 的话：

Avery Lee 在 2001 年于 rec.video.desktop 新闻组的发言中评论道："MJPEG，或者至少是 AVI 中带有 MJPG fourcc 的 MJPEG，是一种受限的 JPEG，使用固定——且被 \*省略\* 的——霍夫曼表。JPEG 必须是 YCbCr 色彩空间，必须是 4:2:2，并且必须使用基本霍夫曼编码，而非算术编码或渐进式编码。……你确实可以提取 MJPEG 帧并用常规 JPEG 解码器解码，但必须在它们前面加上 DHT 段，否则解码器将完全不知道如何解压这些数据。所需的确切表格在 OpenDML 规范中给出。"

此比特流滤镜修补从 MJPEG 流中提取的帧的头部（这些帧携带 AVI1 头 ID 且缺少 DHT 段），以生成完全合格的 JPEG 图像。

``` text
ffmpeg -i mjpeg-movie.avi -c:v copy -bsf:v mjpeg2jpeg frame_%d.jpg
exiftran -i -9 frame*.jpg
ffmpeg -i frame_%d.jpg -c:v copy rotated.avi
```

## mjpegadump

在比特流中添加一个 MJPEG A 头，以启用 QuickTime 解码。

## mov2textsub

从 MOV 字幕中提取可表示的文本文件，并从每个字幕包中剥离元数据头。

另请参见 [text2movsub](#text2movsub) 滤镜。

## mpeg2_metadata

修改嵌入在 MPEG-2 流中的元数据。

- **`display_aspect_ratio`** 设置流中的显示宽高比。

  支持以下固定值：

  - **`4/3`**

  - **`16/9`**

  - **`221/100`**

  任何其他值都会改为用方像素 (square pixels) 标识（参见 H.262 规范 6.3.3 节和表 6-3）。

- **`frame_rate`** 设置流中的帧率。它由已知值表结合一个小的乘数和除数构成——如果提供的值无法精确表示，将使用最接近的可表示值（参见 H.262 规范 6.3.3 节和表 6-4）。

- **`video_format`** 设置流中的视频格式（参见 H.262 规范 6.3.6 节和表 6-6）。

- **`colour_primaries`**

- **`transfer_characteristics`**

- **`matrix_coefficients`** 设置流中的颜色描述（参见 H.262 规范 6.3.6 节和表 6-7、6-8、6-9）。

## mpeg4_unpack_bframes

解包 DivX 风格的打包 B 帧 (packed B-frames)。

DivX 风格的打包 B 帧不是有效的 MPEG-4，只是对有缺陷的 Video for Windows 子系统的权宜之计。它们占用更多空间，可能导致轻微的音视频同步问题，需要更多 CPU 算力来解码（除非播放器有某种已解码图像队列来补偿每包 2,0,2,0 帧的模式），并且复制到 mp4 或 mpeg-ps/ts 等标准容器时会引起麻烦，因为 MPEG-4 解码器可能无法解码它们——它们不是有效的 MPEG-4。

例如，使用 `ffmpeg` 修复包含 DivX 风格打包 B 帧的 MPEG-4 流的 AVI 文件，可以使用以下命令：

``` text
ffmpeg -i INPUT.avi -codec copy -bsf:v mpeg4_unpack_bframes OUTPUT.avi
```

## noise

破坏包的内容或直接丢弃包，而不损坏容器。可用于模糊测试 (fuzzing) 或测试错误恢复/错误隐藏能力。

参数：

- **`amount`** 接受一个表达式，对每个包求值，其结果决定该包中的字节被修改的频率。低于 0 的值将产生可变频率。默认值为 0，表示不修改。但是，如果既未指定 amount 也未指定 drop，则 amount 将被设置为 \<-1\>。可用变量见下文。

- **`drop`** 接受一个对每个包求值的表达式，其值决定是否丢弃该包。求值为正数会导致该包被丢弃。求值为负数会导致该包有可变的丢弃概率，大致与值的幅度成反比。默认值为 0，表示不丢弃。可用变量见下文。

- **`dropamount`** 接受一个非负整数，指定可变的丢弃概率，大致与该值成反比。默认值为 0，表示不丢弃。保留此选项是为了向后兼容，等效于将 drop 设为幅值相同的负值，即 `dropamount=4` 等同于 `drop=-4`。若同时指定了 drop 则忽略此项。

`amount` 和 `drop` 均接受包含以下变量的表达式：

- **`n`** 包的索引，从零开始。

- **`tb`** 包时间戳的时间基。

- **`pts`** 包呈现时间戳。

- **`dts`** 包解码时间戳。

- **`nopts`** 表示 AV_NOPTS_VALUE 的常量。

- **`startpts`** 流中见到的首个非 AV_NOPTS_VALUE 的 PTS。

- **`startdts`** 流中见到的首个非 AV_NOPTS_VALUE 的 DTS。

- **`duration`** 包时长，以时间基单位计。

- **`pos`** 包在输入中的位置；未知或未设置时可能为 -1。

- **`size`** 包大小，以字节计。

- **`key`** 包是否被标记为关键帧。

- **`state`** 一个伪随机整数，主要源自包载荷内容。

### 示例

修改每个字节但不丢弃任何包。

``` text
ffmpeg -i INPUT -c copy -bsf noise=1 output.mkv
```

丢弃时间戳 30 秒之后所有未标记为关键帧的视频包，但不修改其余任何包。

``` text
ffmpeg -i INPUT -c copy -bsf:v noise=drop='gt(pts*tb\,30)*not(key)' output.mkv
```

每 10 秒丢弃一秒的音频，并为其余部分添加一些随机噪声。

``` text
ffmpeg -i INPUT -c copy -bsf:a noise=amount=-1:drop='between(mod(pts*tb\,10)\,9\,10)' output.mkv
```

## null

此比特流滤镜原样传递包。

## pcm_rechunk

将 PCM 音频重新打包为每包固定采样数或每秒固定包率。这类似于 `ffmpeg-filters` 中"asetnsamples 音频滤镜"一节，但它作用于音频包而非音频帧。

- **`nb_out_samples, n`** 设置每个输出音频包的采样数。该数字指*每个声道*的采样数。默认值为 1024。

- **`pad, p`** 若设为 1，滤镜会用静音填充最后一个音频包，使其包含与前几个包相同数量的采样（或大致相同的数量，参见 `frame_rate`）。默认值为 1。

- **`frame_rate, r`** 此选项使滤镜每秒输出固定数量的包，而不是每包固定数量的采样。如果音频采样率不能被帧率整除，则采样数将不恒定，而是略有变化，使每个包尽可能靠近帧边界开始。此选项的优先级高于 `nb_out_samples`。

可以使用 `frame_rate` 选项生成 NTSC 帧率下广为人知的 48kHz 音频 1602-1601-1602-1601-1602 模式。

``` text
ffmpeg -f lavfi -i sine=r=48000:d=1 -c pcm_s16le -bsf pcm_rechunk=r=30000/1001 -f framecrc -
```

## pgs_frame_merge

将以"显示集结束"段收尾的 PGS 字幕段序列合并为单个包。

某些支持 PGS 字幕的容器（复用器 `matroska`）需要此操作。

## prores_metadata

修改嵌入在 prores 流中的颜色属性元数据。

- **`color_primaries`** 设置基色 (color primaries)。可用值为：

  - **`auto`** 保持相同的基色属性（默认）。

  - **`unknown`**

  - **`bt709`**

  - **`bt470bg`** BT601 625

  - **`smpte170m`** BT601 525

  - **`bt2020`**

  - **`smpte431`** DCI P3

  - **`smpte432`** P3 D65

- **`transfer_characteristics`** 设置颜色传递 (color transfer)。可用值为：

  - **`auto`** 保持相同的传递特性属性（默认）。

  - **`unknown`**

  - **`bt709`** BT 601, BT 709, BT 2020

  - **`smpte2084`** SMPTE ST 2084

  - **`arib-std-b67`** ARIB STD-B67

- **`matrix_coefficients`** 设置矩阵系数。可用值为：

  - **`auto`** 保持相同的色彩空间属性（默认）。

  - **`unknown`**

  - **`bt709`**

  - **`smpte170m`** BT 601

  - **`bt2020nc`**

为文件的每一帧设置 Rec709 色彩空间

``` text
ffmpeg -i INPUT -c copy -bsf:v prores_metadata=color_primaries=bt709:color_trc=bt709:colorspace=bt709 output.mov
```

为文件的每一帧设置 Hybrid Log-Gamma 参数

``` text
ffmpeg -i INPUT -c copy -bsf:v prores_metadata=color_primaries=bt2020:color_trc=arib-std-b67:colorspace=bt2020nc output.mov
```

## remove_extra

从包中移除 extradata。

它接受以下参数：

- **`freq`** 设置从哪些帧类型移除 extradata。

  | Term         | Description |
  |--------------|-------------|
  | `k`        | 仅从非关键帧移除 extradata。 |
  | `keyframe` | 仅从关键帧移除 extradata。 |
  | `e, all`   | 从所有帧移除 extradata。 |

## setts

设置包中的 PTS 和 DTS。

它接受以下参数：

- **`ts`**

- **`pts`**

- **`dts`** 设置 PTS、DTS 或两者的表达式。

- **`duration`** 设置时长的表达式。

- **`time_base`** 设置输出时间基。

- **`prescale`** 设置是否在表达式求值之前将时间字段转换为用户设置的输出时间基。默认值为 0。

表达式通过 eval API 求值，可以包含以下常量：

- **`N`** 输入包的计数。从 0 开始。

- **`TS`** 使用 `ts` 或 `dts` 选项时为输入的解复用时间戳，使用 `pts` 选项时为呈现时间戳。

- **`POS`** 包在文件中的原始位置，对当前包未定义时为未定义。

- **`DTS`** 输入的解复用时间戳。

- **`PTS`** 输入的呈现时间戳。

- **`DURATION`** 输入的时长。

- **`STARTDTS`** 第一个包的 DTS。

- **`STARTPTS`** 第一个包的 PTS。

- **`PREV_INDTS`** 前一个输入 DTS。

- **`PREV_INPTS`** 前一个输入 PTS。

- **`PREV_INDURATION`** 前一个输入时长。

- **`PREV_OUTDTS`** 前一个输出 DTS。

- **`PREV_OUTPTS`** 前一个输出 PTS。

- **`PREV_OUTDURATION`** 前一个输出时长。

- **`NEXT_DTS`** 下一个输入 DTS。

- **`NEXT_PTS`** 下一个输入 PTS。

- **`NEXT_DURATION`** 下一个输入时长。

- **`TB`** 时间字段所采用的时间基。启用 prescale 时为用户设置的输出时间基，否则为输入时间基。

- **`TB_OUT`** 输出时间基。

- **`SR`** 包所属流的采样率。

- **`NOPTS`** AV_NOPTS_VALUE 常量。

例如，将 PTS 设为等于 DTS（如果涉及 B 帧则不建议）：

``` text
ffmpeg -i INPUT -c:a copy -bsf:a setts=pts=DTS out.mkv
```

## showinfo

记录包的基本信息。主要用于测试、调试和开发。

## smpte436m_to_eia608

将 `SMPTE_436M_ANC` 数据流转换为 `EIA_608` 流，从 CTA-708 CDP VANC 包中提取隐藏式字幕，并忽略所有其他数据。

## text2movsub

将文本字幕转换为带元数据头的 MOV 字幕（如 `mov_text` 编解码器所用）。

另请参见 [mov2textsub](#mov2textsub) 滤镜。

## trace_headers

记录包含已编码流头中全部语法元素（即高于单个已编码块层级的所有内容）的跟踪输出。这对调试底层流问题很有用。

支持 AV1、H.264、H.265、(M)JPEG、MPEG-2 和 VP9，但视构建情况，可能只有其中一部分可用。

## truehd_core

从 TrueHD 流中提取核心部分，丢弃 ATMOS 数据。

## vp9_metadata

修改嵌入在 VP9 流中的元数据。

- **`color_space`** 在帧头中设置色彩空间值。注意任何设为 RGB 的帧都会被隐式设为 PC 范围，且 RGB 与 profile 0 和 2 不兼容。

  - **`unknown`**

  - **`bt601`**

  - **`bt709`**

  - **`smpte170`**

  - **`smpte240`**

  - **`bt2020`**

  - **`rgb`**

- **`color_range`** 在帧头中设置颜色范围值。注意色彩空间施加的任何值都将优先于此值。

  - **`tv`**

  - **`pc`**

## vp9_superframe

将 VP9 不可见 (alt-ref) 帧合并回 VP9 超级帧 (superframe)。这修复了拆分/分段 VP9 流的合并问题——其中 alt-ref 帧与其可见对应帧被拆开。

## vp9_superframe_split

将 VP9 超级帧拆分为单帧。

## vp9_raw_reorder

给定时间戳正确但顺序可能错乱的 VP9 流，插入额外的 show-existing-frame 包以修正顺序。

# 另请参见

ffmpeg(1), ffplay(1), ffprobe(1), libavcodec(3)
