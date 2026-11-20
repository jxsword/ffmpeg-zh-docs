# 描述

FFmpeg 重采样器为 libswresample 库的音频重采样工具提供高层接口。特别是它可以执行音频重采样、音频声道布局重矩阵化 (rematrixing)，以及转换音频格式与打包布局。

# 重采样器选项

音频重采样器支持以下命名选项。

可通过在 FFmpeg 工具中指定 -\<option\> \<value\>、对 aresample 滤镜指定 \<option\>=\<value\>、在 `SwrContext` 选项中显式设值，或以编程方式使用 `libavutil/opt.h` API 来设置选项。

- **`uchl, used_chlayout`** 设置使用中的输入声道布局。默认未设置。该选项仅用于特殊重映射。

- **`isr, in_sample_rate`** 设置输入采样率。默认值为 0。

- **`osr, out_sample_rate`** 设置输出采样率。默认值为 0。

- **`isf, in_sample_fmt`** 指定输入采样格式。默认设为 `none`。

- **`osf, out_sample_fmt`** 指定输出采样格式。默认设为 `none`。

- **`tsf, internal_sample_fmt`** 设置内部采样格式。默认值为 `none`。未显式设置时会自动选择。

- **`ichl, in_chlayout`**

- **`ochl, out_chlayout`** 设置输入/输出声道布局。

  所需语法参见 `ffmpeg-utils` 中的"the Channel Layout section in the ffmpeg-utils(1) manual"（声道布局）一节。

- **`clev, center_mix_level`** 设置中置混音电平。该值以分贝表示，必须处于区间 \[-32,32\]。

- **`slev, surround_mix_level`** 设置环绕混音电平。该值以分贝表示，必须处于区间 \[-32,32\]。

- **`lfe_mix_level`** 设置 LFE 混入非 LFE 的电平。存在 LFE 输入而无 LFE 输出时使用。该值以分贝表示，必须处于区间 \[-32,32\]。

- **`rmvol, rematrix_volume`** 设置重矩阵化音量。默认值为 1.0。

- **`rematrix_maxval`** 设置重矩阵化的最大输出值。它可用于在防止削波与防止音量降低之间权衡。取 1.0 时防止削波。

- **`flags, swr_flags`** 设置转换器使用的标志。默认值为 0。

  它支持以下单独标志：

  - **`res`** 强制重采样，即使输入与输出采样率一致也强制使用重采样。

- **`dither_scale`** 设置抖动缩放。默认值为 1。

- **`dither_method`** 设置抖动方法。默认值为 0。

  支持的值：

  | Term                    | Description                                     |
  |-------------------------|-------------------------------------------------|
  | `rectangular`         | 选择矩形抖动                       |
  | `triangular`          | 选择三角抖动                        |
  | `triangular_hp`       | 选择带高通的三角抖动         |
  | `lipshitz`            | 选择 Lipshitz 噪声整形抖动。           |
  | `shibata`             | 选择 Shibata 噪声整形抖动。            |
  | `low_shibata`         | 选择低 Shibata 噪声整形抖动。        |
  | `high_shibata`        | 选择高 Shibata 噪声整形抖动。        |
  | `f_weighted`          | 选择 f 加权噪声整形抖动          |
  | `modified_e_weighted` | 选择改良 e 加权噪声整形抖动 |
  | `improved_e_weighted` | 选择改进 e 加权噪声整形抖动 |

- **`resampler`** 设置重采样引擎。默认值为 swr。

  支持的值：

  - **`swr`** 选择原生 SW 重采样器；滤镜选项 precision 与 cheby 在此情况下不适用。

  - **`soxr`** 选择 SoX 重采样器（在可用处）；compensation 与滤镜选项 filter_size、phase_shift、exact_rational、filter_type & kaiser_beta 在此情况下不适用。

- **`filter_size`** 仅限 swr：设置重采样滤镜大小，默认值为 32。

- **`phase_shift`** 仅限 swr：设置重采样相移，默认值为 10，必须处于区间 \[0,30\]。

- **`linear_interp`** 启用（默认）时使用线性插值。当 exact_rational 失败时，若想以速度优先于质量可禁用它。

- **`exact_rational`** 仅限 swr：启用时尝试使用基于输入与输出采样率的精确 phase_count。但若它大于 `1 << phase_shift`，将以 `1 << phase_shift` 作为 phase_count 兜底。默认启用。

- **`cutoff`** 设置截止频率比（swr：6dB 点；soxr：0dB 点）；必须是 0 与 1 之间的浮点值。swr 默认值为 0.97，soxr 默认值为 0.91（soxr 在 44100 采样率下可把整个音频频带保留到 20kHz）。

- **`precision`** 仅限 soxr：重采样信号的计算精度（以比特计）。默认值 20（配合适当抖动，适合目标位深 16）给出 SoX 的'High Quality'；取 28 给出 SoX 的'Very High Quality'。

- **`cheby`** 仅限 soxr：选择无通带滚降 (Chebyshev) 与'无理'比例的更高精度近似。默认值为 0。

- **`async`** 仅限 swr：单参数音频与时间戳同步，使用拉伸、压缩、填充与修剪。设为 1 将启用填充与修剪，更大的值表示数据每秒可被拉伸或压缩的最大采样量。默认值为 0，即不做任何补偿来使采样匹配音频时间戳。

- **`first_pts`** 仅限 swr：假定首个 pts 应为此值。时间单位为 1 / 采样率。这允许在流开始处填充/修剪。默认不对首帧预期 pts 做任何假定，因此不做填充或修剪。例如，音频流晚于视频流开始时可将它设为 0 以静音填充开头，或修剪因编码器延迟而具有负 pts 的采样。

- **`min_comp`** 仅限 swr：设置触发数据拉伸/压缩/填充或修剪以匹配时间戳的时间戳与音频数据最小差（单位为秒）。默认禁用拉伸/压缩/填充与修剪（`min_comp` = `FLT_MAX`）。

- **`min_hard_comp`** 仅限 swr：设置触发增删采样以匹配时间戳的时间戳与音频数据最小差（单位为秒）。该选项实际上是在硬补偿（修剪/填充）与软补偿（压缩/拉伸）之间选择的阈值。注意所有补偿默认经 `min_comp` 禁用。默认值为 0.1。

- **`comp_duration`** 仅限 swr：设置数据被拉伸/压缩以匹配时间戳的持续时长（单位为秒）。必须是非负双精度浮点值，默认值为 1.0。

- **`max_soft_comp`** 仅限 swr：设置数据为匹配时间戳而被拉伸/压缩的最大因子。必须是非负双精度浮点值，默认值为 0。

- **`matrix_encoding`** 选择矩阵化立体声编码。

  它接受以下取值：

  | Term      | Description               |
  |-----------|---------------------------|
  | `none`  | 选择 none               |
  | `dolby` | 选择 Dolby              |
  | `dplii` | 选择 Dolby Pro Logic II |

  默认值为 `none`。

- **`filter_type`** 仅限 swr：选择重采样滤镜类型。它只影响重采样操作。

  它接受以下取值：

  | Term                 | Description                           |
  |----------------------|---------------------------------------|
  | `cubic`            | 选择 cubic                          |
  | `blackman_nuttall` | 选择 Blackman Nuttall 加窗 sinc |
  | `kaiser`           | 选择 Kaiser 加窗 sinc           |

- **`kaiser_beta`** 仅限 swr：设置 Kaiser 窗 beta 值。必须是 \[2,16\] 区间内的双精度浮点值，默认值为 9。

- **`output_sample_bits`** 仅限 swr：设置用于抖动的输出采样位数。必须是 \[0,64\] 区间内的整数，默认值为 0，表示不使用。

# 另请参见

ffmpeg(1), ffplay(1), ffprobe(1), libswresample(3)
