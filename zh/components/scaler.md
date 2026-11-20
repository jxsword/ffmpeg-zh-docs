# 描述

FFmpeg 缩放器为 libswscale 库的图像转换工具提供高层接口。特别是它可以执行图像缩放 (rescaling) 与像素格式转换。

# 缩放器选项

视频缩放器支持以下命名选项。

可通过在 FFmpeg 工具中指定 -\<option\> \<value\> 来设置选项，少数仅 API 的例外在下文说明。以编程方式使用时，可在 `SwsContext` 选项中显式设值，或通过 `libavutil/opt.h` API。

- **`scaler, scaler_sub`** 选择要使用的缩放算法。两者默认值均为 `auto`。它接受以下取值：

  - **`auto`** 自动选择。对 `scaler_sub`，意味着与 `scaler` 相同的算法。对 `scaler`，默认为 `sws_flags` 所选的缩放标志。

  - **`bilinear`** 双线性滤波器。（又称三角滤波器）

  - **`bicubic`** 2 抽头三次 BC 样条（又称 Mitchell-Netravali 样条）。B 与 C 参数可通过设置 `param0` 与 `param1` 配置，分别默认 0.0 与 0.6。

  - **`point, neighbor`** 点采样（又称最近邻）。

  - **`area`** 区域平均。上采样时等价于 `bilinear`。

  - **`gaussian`** 2 抽头高斯滤波器近似。锐度参数可通过设置 `param0` 配置，默认 3.0。

  - **`sinc`** 无窗 sinc 滤波器。

  - **`lanczos`** Lanczos 重采样（sinc 加窗 sinc）。滤波器抽头数可通过设置 `param0` 配置，默认 3。

  - **`spline`** 无窗自然三次样条。

- **`sws_flags`** 设置缩放器标志。它也用于设置缩放算法，但这种用法已弃用，建议改设 `scaler`。只能选择单一算法。默认值为 `bicubic`。

  它接受以下取值：

  - **`fast_bilinear`** 选择快速双线性缩放算法。（已弃用）

  - **`bilinear`** 选择双线性缩放算法。（已弃用）

  - **`bicubic`** 选择三次缩放算法。（已弃用）

  - **`experimental`** 选择实验性缩放算法。（已弃用）

  - **`neighbor`** 选择最近邻重采样算法。（已弃用）

  - **`area`** 选择平均区域重采样算法。（已弃用）

  - **`bicublin`** 对亮度分量选择三次缩放算法，对色度分量选择双线性。（已弃用）

  - **`gauss`** 选择高斯重采样算法。（已弃用）

  - **`sinc`** 选择 sinc 重采样算法。（已弃用）

  - **`lanczos`** 选择 Lanczos 重采样算法。默认宽度 (alpha) 为 3，可通过设置 `param0` 更改。（已弃用）

  - **`spline`** 选择自然三次样条重采样算法。（已弃用）

  - **`print_info`** 启用打印/调试日志。

  - **`accurate_rnd`** 启用精确舍入。

  - **`full_chroma_int`** 启用完整色度插值。

  - **`full_chroma_inp`** 选择完整色度输入。

  - **`bitexact`** 启用比特精确输出。

  - **`unstable`** 允许使用实验性新代码。可能轻微影响输出甚至产出错误结果。仅用于测试。

- **`srcw (API only)`** 设置源宽度。

- **`srch (API only)`** 设置源高度。

- **`dstw (API only)`** 设置目标宽度。

- **`dsth (API only)`** 设置目标高度。

- **`src_format (API only)`** 设置源像素格式（必须以整数表示）。

- **`dst_format (API only)`** 设置目标像素格式（必须以整数表示）。

- **`src_range (boolean)`** 值设为 `1` 时表示源为全范围 (full range)。默认值为 `0`，即源为受限范围 (limited range)。

- **`dst_range (boolean)`** 值设为 `1` 时为目标启用全范围。默认值为 `0`，即目标为受限范围。

- **`gamma (boolean)`** 值设为 `1` 时启用伽马校正缩放。默认值为 `0`。

- **`param0, param1`** 设置缩放算法参数。所设值仅对某些缩放算法有意义，其余算法会忽略。所设值为浮点数值。

- **`sws_dither`** 设置抖动算法。接受以下值之一。默认值为 `auto`。

  - **`auto`** 自动选择

  - **`none`** 不抖动

  - **`bayer`** bayer 抖动

  - **`ed`** 误差扩散抖动

  - **`a_dither`** 基于加法的算术抖动

  - **`x_dither`** 基于异或的算术抖动（比 a_dither 更随机、图案更不明显）。

- **`alphablend`** 设置输入含 alpha 而输出不含时使用的 alpha 混合方式。默认值为 `none`。

  | Term              | Description                           |
  |-------------------|---------------------------------------|
  | `uniform_color` | 混合到均匀背景色 |
  | `checkerboard`  | 混合到棋盘格             |
  | `none`          | 不混合                           |

- **`sws_backends`** 设置允许的 swscale 后端。这是一个标志选项，可组合多个后端。

  - **`auto`** 自动选择。依 `unstable` 标志是否设置而等价于 `stable` 或 `all`。这是默认值。

  - **`stable`** 所有稳定后端。

  - **`unstable`** 所有不稳定后端。

  - **`all`** 所有可用后端。

  - **`legacy`** 旧版 swscale 代码。

  - **`c`** 基于模板的参考代码。

  - **`memcpy`** 使用 libc `memcpy` 的快速路径。

  - **`x86`** x86 SIMD 内核。

  - **`aarch64`** AArch64 NEON 内核。

  - **`spirv`** Vulkan SPIR-V 后端。

# 另请参见

ffmpeg(1), ffplay(1), ffprobe(1), libswscale(3)
