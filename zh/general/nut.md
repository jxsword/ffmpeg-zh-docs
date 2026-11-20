# 描述

NUT 是一种低开销的通用容器格式。它以一种简单而高效的方式存储音频、视频、字幕和用户自定义的流。

它由一群 FFmpeg 和 MPlayer 开发者于 2003 年创建，并于 2008 年定稿。

NUT 的官方规范见 [官方 nut 规范](https://git.ffmpeg.org/gitweb/nut.git/blob/refs/heads/master:/docs/nut.txt)。若本文与官方规范之间存在任何差异，以官方规范为准。

# 模式

NUT 通过在其主头（main header）中使用 flags 字段来标记若干变体。

|           |                                         |
|-----------|-----------------------------------------|
| BROADCAST | 扩展同步点（syncpoint）以报告发送方的墙钟 |
| PIPE      | 完全省略同步点（syncpoint）              |

## BROADCAST

BROADCAST 变体提供第二时间基准，便于检测端点延迟与网络时延。它假定所有端点的时钟均已同步。适用于实时场景。

## PIPE

PIPE 变体假定 NUT 被用作不可定位的中间容器，通过不使用同步点来去除不必要的开销，并降低整体内存占用。

# 容器特定的编解码器标签

## 通用原始 YUVA 格式

由于许多特殊的平面（planar）YUVA 像素格式未被 AVI/QuickTime 的 FourCC 列表收录，因此采用以下方案来表示它们。

前两个字节可以包含以下值：Y1 = 仅 Y，Y2 = Y+A，Y3 = YUV，Y4 = YUVA。

第三个字节表示 UV 平面宽度和高度方向的色度二次采样（chroma subsampling）值，即为了求得色度宽度/高度而需要将亮度宽度/高度右移的量。

第四个字节是所使用的位数（8、16……）。

如果字节顺序颠倒，则表示每个分量都必须按大端序读取。

## 原始音频

|                                   |        |
|-----------------------------------|--------|
| ALAW                              | A-LAW  |
| ULAW                              | MU-LAW |
| P\<type\>\<interleaving\>\<bits\> | 小端序 PCM |
| \<bits\>\<interleaving\>\<type\>P | 大端序 PCM |

\<type\> 为 S 表示有符号整数，U 表示无符号整数，F 表示 IEEE 浮点数。\<interleaving\> 为 D 表示默认，P 表示平面。\<bits\> 为 8/16/24/32

``` text
PFD[32]   would for example be signed 32 bit little-endian IEEE float
```

## 字幕

|          |                  |
|----------|------------------|
| UTF8     | 原始 UTF-8       |
| SSA\[0\] | SubStation Alpha |
| DVDS     | DVD 字幕         |
| DVBS     | DVB 字幕         |

## 原始数据

|      |            |
|------|------------|
| UTF8 | 原始 UTF-8 |

## 编解码器

|      |                                                                 |
|------|-----------------------------------------------------------------|
| 3IV1 | 由旧版 3ivx 生成的非合规 MPEG-4 |
| ASV1 | Asus Video                                                      |
| ASV2 | Asus Video 2                                                    |
| CVID | Cinepak                                                         |
| CYUV | Creative YUV                                                    |
| DIVX | 由旧版 DivX 生成的非合规 MPEG-4 |
| DUCK | Truemotion 1                                                    |
| FFV1 | FFmpeg video 1                                                  |
| FFVH | FFmpeg Huffyuv                                                  |
| H261 | ITU H.261                                                       |
| H262 | ITU H.262                                                       |
| H263 | ITU H.263                                                       |
| H264 | ITU H.264                                                       |
| HFYU | Huffyuv                                                         |
| I263 | Intel H.263                                                     |
| IV31 | Indeo 3.1                                                       |
| IV32 | Indeo 3.2                                                       |
| IV50 | Indeo 5.0                                                       |
| LJPG | ITU JPEG（无损） |
| MJLS | ITU JPEG-LS                                                     |
| MJPG | ITU JPEG                                                        |
| MPG4 | MS MPEG-4v1（非 ISO MPEG-4） |
| MP42 | MS MPEG-4v2                                                     |
| MP43 | MS MPEG-4v3                                                     |
| MP4V | ISO MPEG-4 第 2 部分视频（来自旧编码器） |
| mpg1 | ISO MPEG-1 视频 |
| mpg2 | ISO MPEG-2 视频 |
| MRLE | MS RLE                                                          |
| MSVC | MS Video 1                                                      |
| RT21 | Indeo 2.1                                                       |
| RV10 | RealVideo 1.0                                                   |
| RV20 | RealVideo 2.0                                                   |
| RV30 | RealVideo 3.0                                                   |
| RV40 | RealVideo 4.0                                                   |
| SNOW | FFmpeg Snow                                                     |
| SVQ1 | Sorenson Video 1                                                |
| SVQ3 | Sorenson Video 3                                                |
| theo | Xiph Theora                                                     |
| TM20 | Truemotion 2.0                                                  |
| UMP4 | 由 UB Video MPEG-4 生成的非合规 MPEG-4 |
| VCR1 | ATI VCR1                                                        |
| VP30 | VP 3.0                                                          |
| VP31 | VP 3.1                                                          |
| VP50 | VP 5.0                                                          |
| VP60 | VP 6.0                                                          |
| VP61 | VP 6.1                                                          |
| VP62 | VP 6.2                                                          |
| VP70 | VP 7.0                                                          |
| WMV1 | MS WMV7                                                         |
| WMV2 | MS WMV8                                                         |
| WMV3 | MS WMV9                                                         |
| WV1F | 由 ? 生成的非合规 MPEG-4 |
| WVC1 | VC-1                                                            |
| XVID | 由旧版 Xvid 生成的非合规 MPEG-4 |
| XVIX | 由带隔行缺陷的旧版 Xvid 生成的非合规 MPEG-4 |
