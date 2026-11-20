# 描述

本文描述 libavutil 库提供的一些通用功能与实用工具。

# 语法

本节记录 FFmpeg 库和工具采用的语法与格式。

## 引号引用与转义

除非明确指定，FFmpeg 采用以下引号引用与转义机制。应用以下规则：

- `'` 和 `\` 是特殊字符（分别用于引号引用和转义）。除此之外，视引号引用与转义所用的具体语法而定，可能还有其他特殊字符。

- 特殊字符通过在其前面加 `\` 来转义。

- `''` 之间括起的所有字符都按字面包含在解析后的字符串中。引号字符 `'` 本身不能被引号引用，因此可能需要先闭合引号再对其进行转义。

- 前导和尾随空白字符（除非被转义或被引号括起）会从解析后的字符串中移除。

注意，在命令行或脚本中使用时可能需要再加一层转义，这取决于所用 shell 语言的语法。

定义在 `libavutil/avstring.h` 中的函数 `av_get_token` 可用于解析按上述规则做了引号引用或转义的 token。

FFmpeg 源码树中的工具 `tools/ffescape` 可用于在脚本中自动对字符串做引号引用或转义。

### 示例

- 转义包含 `'` 特殊字符的字符串 `Crime d'Amour`：

  ``` text
  Crime d\'Amour
  ```

- 上面的字符串包含一个引号，因此对它做引号引用时需要转义 `'`：

  ``` text
  'Crime d'\''Amour'
  ```

- 使用引号引用来包含前导或尾随空白字符：

  ``` text
  '  this string starts and ends with whitespaces  '
  ```

- 转义与引号引用可以混用：

  ``` text
  ' The string '\'string\'' is a string '
  ```

- 要包含字面 `\`，既可以用转义也可以用引号引用：

  ``` text
  'c:\foo' can be written as c:\\foo
  ```

## 日期

可接受的语法为：

``` text
[(YYYY-MM-DD|YYYYMMDD)[T|t| ]]((HH:MM:SS[.m...]]])|(HHMMSS[.m...]]]))[Z]
now
```

若值为 "now"，则取当前时间。

除非附加 Z（此时按 UTC 解释），时间为本地时间。若未指定年-月-日部分，则取当前年-月-日。

## 时长

表达时长有两种可接受的语法。

``` text
[-][HH:]MM:SS[.m...]
```

\<HH\> 表示小时数，\<MM\> 表示分钟数（最多 2 位数字），\<SS\> 表示秒数（最多 2 位数字）。末尾的 \<m\> 表示 \<SS\> 的小数部分。

*或*

``` text
[-]S+[.m...][s|ms|us]
```

\<S\> 表示秒数，带可选的小数部分 \<m\>。可选的字面后缀 `s`、`ms` 或 `us` 分别指示把该值解释为秒、毫秒或微秒。

两种表达式中，可选的 `-` 表示负时长。

### 示例

以下均为有效的时长：

| Term         | Description                         |
|--------------|-------------------------------------|
| `55`       | 55 秒                          |
| `0.2`      | 0.2 秒                         |
| `200ms`    | 200 毫秒，即 0.2 秒       |
| `200000us` | 200000 微秒，即 0.2 秒    |
| `12:03:45` | 12 小时，03 分 45 秒 |
| `23.189`   | 23.189 秒                      |

## 视频尺寸

指定源视频的尺寸，可以是 \<width\>x\<height\> 形式的字符串，或尺寸缩写名称。

可识别以下缩写：

| Term          | Description |
|---------------|-------------|
| `ntsc`      | 720x480     |
| `pal`       | 720x576     |
| `qntsc`     | 352x240     |
| `qpal`      | 352x288     |
| `sntsc`     | 640x480     |
| `spal`      | 768x576     |
| `film`      | 352x240     |
| `ntsc-film` | 352x240     |
| `sqcif`     | 128x96      |
| `qcif`      | 176x144     |
| `cif`       | 352x288     |
| `4cif`      | 704x576     |
| `16cif`     | 1408x1152   |
| `qqvga`     | 160x120     |
| `qvga`      | 320x240     |
| `vga`       | 640x480     |
| `svga`      | 800x600     |
| `xga`       | 1024x768    |
| `uxga`      | 1600x1200   |
| `qxga`      | 2048x1536   |
| `sxga`      | 1280x1024   |
| `qsxga`     | 2560x2048   |
| `hsxga`     | 5120x4096   |
| `wvga`      | 852x480     |
| `wxga`      | 1366x768    |
| `wsxga`     | 1600x1024   |
| `wuxga`     | 1920x1200   |
| `woxga`     | 2560x1600   |
| `wqsxga`    | 3200x2048   |
| `wquxga`    | 3840x2400   |
| `whsxga`    | 6400x4096   |
| `whuxga`    | 7680x4800   |
| `cga`       | 320x200     |
| `ega`       | 640x350     |
| `hd480`     | 852x480     |
| `hd720`     | 1280x720    |
| `hd1080`    | 1920x1080   |
| `2k`        | 2048x1080   |
| `2kflat`    | 1998x1080   |
| `2kscope`   | 2048x858    |
| `4k`        | 4096x2160   |
| `4kflat`    | 3996x2160   |
| `4kscope`   | 4096x1716   |
| `nhd`       | 640x360     |
| `hqvga`     | 240x160     |
| `wqvga`     | 400x240     |
| `fwqvga`    | 432x240     |
| `hvga`      | 480x320     |
| `qhd`       | 960x540     |
| `2kdci`     | 2048x1080   |
| `4kdci`     | 4096x2160   |
| `uhd2160`   | 3840x2160   |
| `uhd4320`   | 7680x4320   |

## 视频帧率

指定视频的帧率，表示每秒生成的帧数。必须是 \<frame_rate_num\>/\<frame_rate_den\> 格式的字符串、整数、浮点数或有效的视频帧率缩写。

可识别以下缩写：

| Term          | Description |
|---------------|-------------|
| `ntsc`      | 30000/1001  |
| `pal`       | 25/1        |
| `qntsc`     | 30000/1001  |
| `qpal`      | 25/1        |
| `sntsc`     | 30000/1001  |
| `spal`      | 25/1        |
| `film`      | 24/1        |
| `ntsc-film` | 24000/1001  |

## 比率

比率可以用表达式表达，或用 \<numerator\>:\<denominator\> 的形式表达。

注意，无穷 (1/0) 或负值的比率被视为有效，因此若想排除这些值，应检查返回值。

未定义值可用字符串 "0:0" 表达。

## 颜色

可以是下文定义的颜色名称（匹配时不区分大小写），或 `[0x|#]RRGGBB[AA]` 序列，其后可跟 @ 和表示 alpha 分量的字符串。

alpha 分量可以是由 "0x" 后接十六进制数组成的字符串，或 0.0 到 1.0 之间的十进制数，表示不透明度（`0x00` 或 `0.0` 表示完全透明，`0xff` 或 `1.0` 表示完全不透明）。未指定 alpha 分量时假定为 `0xff`。

字符串 `random` 将产生随机颜色。

可识别以下颜色名称：

| Term                     | Description |
|--------------------------|-------------|
| `AliceBlue`            | 0xF0F8FF    |
| `AntiqueWhite`         | 0xFAEBD7    |
| `Aqua`                 | 0x00FFFF    |
| `Aquamarine`           | 0x7FFFD4    |
| `Azure`                | 0xF0FFFF    |
| `Beige`                | 0xF5F5DC    |
| `Bisque`               | 0xFFE4C4    |
| `Black`                | 0x000000    |
| `BlanchedAlmond`       | 0xFFEBCD    |
| `Blue`                 | 0x0000FF    |
| `BlueViolet`           | 0x8A2BE2    |
| `Brown`                | 0xA52A2A    |
| `BurlyWood`            | 0xDEB887    |
| `CadetBlue`            | 0x5F9EA0    |
| `Chartreuse`           | 0x7FFF00    |
| `Chocolate`            | 0xD2691E    |
| `Coral`                | 0xFF7F50    |
| `CornflowerBlue`       | 0x6495ED    |
| `Cornsilk`             | 0xFFF8DC    |
| `Crimson`              | 0xDC143C    |
| `Cyan`                 | 0x00FFFF    |
| `DarkBlue`             | 0x00008B    |
| `DarkCyan`             | 0x008B8B    |
| `DarkGoldenRod`        | 0xB8860B    |
| `DarkGray`             | 0xA9A9A9    |
| `DarkGreen`            | 0x006400    |
| `DarkKhaki`            | 0xBDB76B    |
| `DarkMagenta`          | 0x8B008B    |
| `DarkOliveGreen`       | 0x556B2F    |
| `Darkorange`           | 0xFF8C00    |
| `DarkOrchid`           | 0x9932CC    |
| `DarkRed`              | 0x8B0000    |
| `DarkSalmon`           | 0xE9967A    |
| `DarkSeaGreen`         | 0x8FBC8F    |
| `DarkSlateBlue`        | 0x483D8B    |
| `DarkSlateGray`        | 0x2F4F4F    |
| `DarkTurquoise`        | 0x00CED1    |
| `DarkViolet`           | 0x9400D3    |
| `DeepPink`             | 0xFF1493    |
| `DeepSkyBlue`          | 0x00BFFF    |
| `DimGray`              | 0x696969    |
| `DodgerBlue`           | 0x1E90FF    |
| `FireBrick`            | 0xB22222    |
| `FloralWhite`          | 0xFFFAF0    |
| `ForestGreen`          | 0x228B22    |
| `Fuchsia`              | 0xFF00FF    |
| `Gainsboro`            | 0xDCDCDC    |
| `GhostWhite`           | 0xF8F8FF    |
| `Gold`                 | 0xFFD700    |
| `GoldenRod`            | 0xDAA520    |
| `Gray`                 | 0x808080    |
| `Green`                | 0x008000    |
| `GreenYellow`          | 0xADFF2F    |
| `HoneyDew`             | 0xF0FFF0    |
| `HotPink`              | 0xFF69B4    |
| `IndianRed`            | 0xCD5C5C    |
| `Indigo`               | 0x4B0082    |
| `Ivory`                | 0xFFFFF0    |
| `Khaki`                | 0xF0E68C    |
| `Lavender`             | 0xE6E6FA    |
| `LavenderBlush`        | 0xFFF0F5    |
| `LawnGreen`            | 0x7CFC00    |
| `LemonChiffon`         | 0xFFFACD    |
| `LightBlue`            | 0xADD8E6    |
| `LightCoral`           | 0xF08080    |
| `LightCyan`            | 0xE0FFFF    |
| `LightGoldenRodYellow` | 0xFAFAD2    |
| `LightGreen`           | 0x90EE90    |
| `LightGrey`            | 0xD3D3D3    |
| `LightPink`            | 0xFFB6C1    |
| `LightSalmon`          | 0xFFA07A    |
| `LightSeaGreen`        | 0x20B2AA    |
| `LightSkyBlue`         | 0x87CEFA    |
| `LightSlateGray`       | 0x778899    |
| `LightSteelBlue`       | 0xB0C4DE    |
| `LightYellow`          | 0xFFFFE0    |
| `Lime`                 | 0x00FF00    |
| `LimeGreen`            | 0x32CD32    |
| `Linen`                | 0xFAF0E6    |
| `Magenta`              | 0xFF00FF    |
| `Maroon`               | 0x800000    |
| `MediumAquaMarine`     | 0x66CDAA    |
| `MediumBlue`           | 0x0000CD    |
| `MediumOrchid`         | 0xBA55D3    |
| `MediumPurple`         | 0x9370D8    |
| `MediumSeaGreen`       | 0x3CB371    |
| `MediumSlateBlue`      | 0x7B68EE    |
| `MediumSpringGreen`    | 0x00FA9A    |
| `MediumTurquoise`      | 0x48D1CC    |
| `MediumVioletRed`      | 0xC71585    |
| `MidnightBlue`         | 0x191970    |
| `MintCream`            | 0xF5FFFA    |
| `MistyRose`            | 0xFFE4E1    |
| `Moccasin`             | 0xFFE4B5    |
| `NavajoWhite`          | 0xFFDEAD    |
| `Navy`                 | 0x000080    |
| `OldLace`              | 0xFDF5E6    |
| `Olive`                | 0x808000    |
| `OliveDrab`            | 0x6B8E23    |
| `Orange`               | 0xFFA500    |
| `OrangeRed`            | 0xFF4500    |
| `Orchid`               | 0xDA70D6    |
| `PaleGoldenRod`        | 0xEEE8AA    |
| `PaleGreen`            | 0x98FB98    |
| `PaleTurquoise`        | 0xAFEEEE    |
| `PaleVioletRed`        | 0xD87093    |
| `PapayaWhip`           | 0xFFEFD5    |
| `PeachPuff`            | 0xFFDAB9    |
| `Peru`                 | 0xCD853F    |
| `Pink`                 | 0xFFC0CB    |
| `Plum`                 | 0xDDA0DD    |
| `PowderBlue`           | 0xB0E0E6    |
| `Purple`               | 0x800080    |
| `Red`                  | 0xFF0000    |
| `RosyBrown`            | 0xBC8F8F    |
| `RoyalBlue`            | 0x4169E1    |
| `SaddleBrown`          | 0x8B4513    |
| `Salmon`               | 0xFA8072    |
| `SandyBrown`           | 0xF4A460    |
| `SeaGreen`             | 0x2E8B57    |
| `SeaShell`             | 0xFFF5EE    |
| `Sienna`               | 0xA0522D    |
| `Silver`               | 0xC0C0C0    |
| `SkyBlue`              | 0x87CEEB    |
| `SlateBlue`            | 0x6A5ACD    |
| `SlateGray`            | 0x708090    |
| `Snow`                 | 0xFFFAFA    |
| `SpringGreen`          | 0x00FF7F    |
| `SteelBlue`            | 0x4682B4    |
| `Tan`                  | 0xD2B48C    |
| `Teal`                 | 0x008080    |
| `Thistle`              | 0xD8BFD8    |
| `Tomato`               | 0xFF6347    |
| `Turquoise`            | 0x40E0D0    |
| `Violet`               | 0xEE82EE    |
| `Wheat`                | 0xF5DEB3    |
| `White`                | 0xFFFFFF    |
| `WhiteSmoke`           | 0xF5F5F5    |
| `Yellow`               | 0xFFFF00    |
| `YellowGreen`          | 0x9ACD32    |

## 声道布局

声道布局指定多声道音频流中各声道的空间分布。指定声道布局时，FFmpeg 使用一种特殊语法。

单个声道由 id 标识，如下表所示：

| Term     | Description           |
|----------|-----------------------|
| `FL`   | 左前 |
| `FR`   | 右前 |
| `FC`   | 前中 |
| `LFE`  | 低频 |
| `BL`   | 左后 |
| `BR`   | 右后 |
| `FLC`  | 前中偏左  |
| `FRC`  | 前中偏右 |
| `BC`   | 后中           |
| `SL`   | 左侧             |
| `SR`   | 右侧             |
| `TC`   | 顶中             |
| `TFL`  | 顶前左        |
| `TFC`  | 顶前中      |
| `TFR`  | 顶前右       |
| `TBL`  | 顶后左         |
| `TBC`  | 顶后中       |
| `TBR`  | 顶后右        |
| `DL`   | 下混左          |
| `DR`   | 下混右         |
| `WL`   | 宽左             |
| `WR`   | 宽右            |
| `SDL`  | 环绕直接左  |
| `SDR`  | 环绕直接右 |
| `LFE2` | 低频 2       |

标准声道布局组合可用以下标识符指定：

- **`mono`** FC

- **`stereo`** FL+FR

- **`2.1`** FL+FR+LFE

- **`3.0`** FL+FR+FC

- **`3.0(back)`** FL+FR+BC

- **`4.0`** FL+FR+FC+BC

- **`quad`** FL+FR+BL+BR

- **`quad(side)`** FL+FR+SL+SR

- **`3.1`** FL+FR+FC+LFE

- **`5.0`** FL+FR+FC+BL+BR

- **`5.0(side)`** FL+FR+FC+SL+SR

- **`4.1`** FL+FR+FC+LFE+BC

- **`5.1`** FL+FR+FC+LFE+BL+BR

- **`5.1(side)`** FL+FR+FC+LFE+SL+SR

- **`6.0`** FL+FR+FC+BC+SL+SR

- **`6.0(front)`** FL+FR+FLC+FRC+SL+SR

- **`3.1.2`** FL+FR+FC+LFE+TFL+TFR

- **`hexagonal`** FL+FR+FC+BL+BR+BC

- **`6.1`** FL+FR+FC+LFE+BC+SL+SR

- **`6.1`** FL+FR+FC+LFE+BL+BR+BC

- **`6.1(front)`** FL+FR+LFE+FLC+FRC+SL+SR

- **`7.0`** FL+FR+FC+BL+BR+SL+SR

- **`7.0(front)`** FL+FR+FC+FLC+FRC+SL+SR

- **`7.1`** FL+FR+FC+LFE+BL+BR+SL+SR

- **`7.1(wide)`** FL+FR+FC+LFE+BL+BR+FLC+FRC

- **`7.1(wide-side)`** FL+FR+FC+LFE+FLC+FRC+SL+SR

- **`5.1.2`** FL+FR+FC+LFE+BL+BR+TFL+TFR

- **`octagonal`** FL+FR+FC+BL+BR+BC+SL+SR

- **`cube`** FL+FR+BL+BR+TFL+TFR+TBL+TBR

- **`5.1.4`** FL+FR+FC+LFE+BL+BR+TFL+TFR+TBL+TBR

- **`7.1.2`** FL+FR+FC+LFE+BL+BR+SL+SR+TFL+TFR

- **`7.1.4`** FL+FR+FC+LFE+BL+BR+SL+SR+TFL+TFR+TBL+TBR

- **`7.2.3`** FL+FR+FC+LFE+BL+BR+SL+SR+TFL+TFR+TBC+LFE2

- **`9.1.4`** FL+FR+FC+LFE+BL+BR+FLC+FRC+SL+SR+TFL+TFR+TBL+TBR

- **`9.1.6`** FL+FR+FC+LFE+BL+BR+FLC+FRC+SL+SR+TFL+TFR+TBL+TBR+TSL+TSR

- **`hexadecagonal`** FL+FR+FC+BL+BR+BC+SL+SR+WL+WR+TBL+TBR+TBC+TFC+TFL+TFR

- **`binaural`** BIL+BIR

- **`downmix`** DL+DR

- **`22.2`** FL+FR+FC+LFE+BL+BR+FLC+FRC+BC+SL+SR+TC+TFL+TFC+TFR+TBL+TBC+TBR+LFE2+TSL+TSR+BFC+BFL+BFR

自定义声道布局可以用以 '+' 分隔的一系列项指定。每个项可以是：

- 单个声道的名称（例如 `FL`、`FR`、`FC`、`LFE` 等），每个名称可选地在 '@' 后跟一个自定义名称（例如 `FL@Left`、`FR@Right`、`FC@Center`、`LFE@Low_Frequency` 等）

标准声道布局可由以下方式指定：

- 单个声道的名称（例如 `FL`、`FR`、`FC`、`LFE` 等）

- 标准声道布局的名称（例如 `mono`、`stereo`、`4.0`、`quad`、`5.0` 等）

- 十进制声道数后跟 'c'，产生该声道数的默认声道布局（参见函数 `av_channel_layout_default`）。注意并非所有声道数都有默认布局。

- 十进制声道数后跟 'C'，产生具有指定声道数的未知声道布局。注意并非所有声道布局描述字符串都支持未知声道布局。

- 以 "0x" 开头的十六进制声道布局掩码（参见 `libavutil/channel_layout.h` 中的 `AV_CH_*` 宏。

在 libavutil 53 版之前，指定声道数的尾部字符 "c" 是可选的，现在则是必需的；而声道布局掩码也可用十进制数指定（当且仅当其后不跟 "c" 或 "C" 时）。

另请参见定义在 `libavutil/channel_layout.h` 中的函数 `av_channel_layout_from_string`。

# 表达式求值

对算术表达式求值时，FFmpeg 使用内部公式求值器，通过 `libavutil/eval.h` 接口实现。

表达式可包含一元和二元运算符、常量以及函数。

两个表达式 \<expr1\> 和 \<expr2\> 可组合成另一表达式 "\<expr1\>;\<expr2\>"。\<expr1\> 和 \<expr2\> 依次求值，新表达式的值为 \<expr2\> 的值。

可用的二元运算符有：`+`、`-`、`*`、`/`、`^`。

可用的一元运算符有：`+`、`-`。

某些内部变量可用于存储和加载中间结果。可使用 `ld` 和 `st` 函数并带一个 0 到 9 的索引参数来访问它们，以指定访问哪个内部变量。

可用函数如下：

- **`abs(x)`** 计算 \<x\> 的绝对值。

- **`acos(x)`** 计算 \<x\> 的反余弦。

- **`asin(x)`** 计算 \<x\> 的反正弦。

- **`atan(x)`** 计算 \<x\> 的反正切。

- **`atan2(y, x)`** 计算 \<y\>/\<x\> 的反正切主值。

- **`between(x, min, max)`** 若 \<x\> 大于等于 \<min\> 且小于等于 \<max\>，返回 1，否则返回 0。

- **`bitand(x, y)`**

- **`bitor(x, y)`** 对 \<x\> 和 \<y\> 执行按位与/或运算。

  在执行按位运算前，\<x\> 和 \<y\> 的求值结果会先转换为整数。

  注意，转换为整数以及转换回浮点数都可能损失精度。对大数（通常为 2^53 及以上）要当心意外结果。

- **`ceil(expr)`** 把表达式 \<expr\> 的值向上取整到最近的整数。例如，"ceil(1.5)" 为 "2.0"。

- **`clip(x, min, max)`** 返回 \<x\> 被限制在 \<min\> 和 \<max\> 之间后的值。

- **`cos(x)`** 计算 \<x\> 的余弦。

- **`cosh(x)`** 计算 \<x\> 的双曲余弦。

- **`eq(x, y)`** 若 \<x\> 和 \<y\> 等价返回 1，否则返回 0。

- **`exp(x)`** 计算 \<x\> 的指数（以 `e` 为底，即欧拉数）。

- **`floor(expr)`** 把表达式 \<expr\> 的值向下取整到最近的整数。例如，"floor(-1.5)" 为 "-2.0"。

- **`gauss(x)`** 计算 \<x\> 的高斯函数，对应 `exp(-x*x/2) / sqrt(2*PI)`。

- **`gcd(x, y)`** 返回 \<x\> 和 \<y\> 的最大公约数。若 \<x\> 和 \<y\> 均为 0，或任一/两者小于零，则行为未定义。

- **`gt(x, y)`** 若 \<x\> 大于 \<y\> 返回 1，否则返回 0。

- **`gte(x, y)`** 若 \<x\> 大于等于 \<y\> 返回 1，否则返回 0。

- **`hypot(x, y)`** 该函数与同名 C 函数类似；返回 "sqrt(\<x\>\*\<x\> + \<y\>\*\<y\>)"，即边长为 \<x\> 和 \<y\> 的直角三角形的斜边长度，或点 (\<x\>, \<y\>) 到原点的距离。

- **`if(x, y)`** 对 \<x\> 求值，若结果非零则返回 \<y\> 的求值结果，否则返回 0。

- **`if(x, y, z)`** 对 \<x\> 求值，若结果非零则返回 \<y\> 的求值结果，否则返回 \<z\> 的求值结果。

- **`ifnot(x, y)`** 对 \<x\> 求值，若结果为零则返回 \<y\> 的求值结果，否则返回 0。

- **`ifnot(x, y, z)`** 对 \<x\> 求值，若结果为零则返回 \<y\> 的求值结果，否则返回 \<z\> 的求值结果。

- **`isinf(x)`** 若 \<x\> 为 +/-INFINITY 返回 1.0，否则返回 0.0。

- **`isnan(x)`** 若 \<x\> 为 NAN 返回 1.0，否则返回 0.0。

- **`ld(idx)`** 加载索引为 \<idx\> 的内部变量的值，该值此前用 st(\<idx\>, \<expr\>) 存入。该函数返回加载的值。

- **`lerp(x, y, z)`** 返回 \<x\> 和 \<y\> 之间按数量 \<z\> 的线性插值。

- **`log(x)`** 计算 \<x\> 的自然对数。

- **`lt(x, y)`** 若 \<x\> 小于 \<y\> 返回 1，否则返回 0。

- **`lte(x, y)`** 若 \<x\> 小于等于 \<y\> 返回 1，否则返回 0。

- **`max(x, y)`** 返回 \<x\> 和 \<y\> 中的最大值。

- **`min(x, y)`** 返回 \<x\> 和 \<y\> 中的最小值。

- **`mod(x, y)`** 计算 \<x\> 除以 \<y\> 的余数。

- **`not(expr)`** 若 \<expr\> 为零返回 1.0，否则返回 0.0。

- **`pow(x, y)`** 计算 \<x\> 的 \<y\> 次幂，相当于 "(\<x\>)^(\<y\>)"。

- **`print(t)`**

- **`print(t, l)`** 以日志级别 \<l\> 打印表达式 \<t\> 的值。未指定 \<l\> 时使用默认日志级别。返回所打印表达式的值。

- **`random(idx)`** 返回 0.0 到 1.0 之间的伪随机值。\<idx\> 是用于保存种子/状态的内部变量的索引，该种子/状态可预先用 `st(idx)` 存入。

  要初始化种子，需要把种子值作为 64 位无符号整数存入索引为 \<idx\> 的内部变量。

  例如，把值 `42` 作为种子存入索引为 `0` 的内部变量，并打印几个随机值：

  ``` c
  st(0,42); print(random(0)); print(random(0)); print(random(0))
  ```

- **`randomi(idx, min, max)`** 返回 \<min\> 和 \<max\> 区间内的伪随机值。\<idx\> 是将用于保存种子/状态的内部变量的索引，该种子/状态可预先用 `st(idx)` 存入。

  要初始化种子，需要把种子值作为 64 位无符号整数存入索引为 \<idx\> 的内部变量。

- **`root(expr, max)`** 在 0..\<max\> 区间内求一个输入值，使由 \<expr\> 表示、以 \<ld(0)\> 为参数的函数值为 0。

  \<expr\> 中的表达式必须表示连续函数，否则结果未定义。

  \<ld(0)\> 用于表示函数输入值，即给定的表达式会被以各种输入值多次求值，表达式可通过 `ld(0)` 访问这些输入值。当表达式求值为 0 时，返回对应的输入值。

- **`round(expr)`** 把表达式 \<expr\> 的值取整到最近的整数。例如，"round(1.5)" 为 "2.0"。

- **`sgn(x)`** 计算 \<x\> 的符号。

- **`sin(x)`** 计算 \<x\> 的正弦。

- **`sinh(x)`** 计算 \<x\> 的双曲正弦。

- **`sqrt(expr)`** 计算 \<expr\> 的平方根。相当于 "(\<expr\>)^.5"。

- **`squish(x)`** 计算表达式 `1/(1 + exp(4*x))`。

- **`st(idx, expr)`** 把表达式 \<expr\> 的值存入内部变量。\<idx\> 指定存储位置的变量索引，取值范围 0 到 9。该函数返回存入内部变量的值。

  存入的值可用 `ld(var)` 取回。

  注意：变量目前不在多个表达式之间共享。

- **`tan(x)`** 计算 \<x\> 的正切。

- **`tanh(x)`** 计算 \<x\> 的双曲正切。

- **`taylor(expr, x)`**

- **`taylor(expr, x, idx)`** 给定表示函数在 0 处的 `ld(idx)` 阶导数的表达式，在 \<x\> 处对泰勒级数求值。

  级数不收敛时结果未定义。

  \<ld(idx)\> 在 \<expr\> 中表示导数阶数，即给定的表达式会被以各种输入值多次求值，表达式可通过 `ld(idx)` 访问这些输入值。未指定 \<idx\> 时假定为 0。

  注意，当你拥有的是在 y 处而非 0 处的导数时，可使用 `taylor(expr, x-y)`。

- **`time(0)`** 返回当前（墙上时钟）时间，以秒为单位。

- **`trunc(expr)`** 把表达式 \<expr\> 的值朝零取整到最近的整数。例如，"trunc(-1.5)" 为 "-1.0"。

- **`while(cond, expr)`** 在表达式 \<cond\> 非零期间反复对表达式 \<expr\> 求值，返回最后一次 \<expr\> 求值的值；若 \<cond\> 始终为假，返回 NAN。

可用常量如下：

| Term  | Description                                     |
|-------|-------------------------------------------------|
| `PI`  | 单位圆盘的面积，约 3.14       |
| `E`   | exp(1)（欧拉数），约 2.718    |
| `PHI` | 黄金比率 (1+sqrt(5))/2，约 1.618 |

假定表达式值非零即为"真"，注意：

`*` 的作用如同 AND

`+` 的作用如同 OR

例如以下构造：

``` text
if (A AND B) then C
```

等价于：

``` text
if(A*B, C)
```

在你的 C 代码中，可以扩展一元和二元函数列表，并定义可识别的常量，使它们可用于你的表达式。

求值器还能识别国际单位制词头。若在前缀后附加 'i'，则使用二进制词头（基于 1024 的幂而非 1000 的幂）。'B' 后缀把值乘以 8，可附加在单位词头之后或单独使用。因此可以用 'KB'、'MiB'、'G' 和 'B' 等作为数字后缀。

可用国际单位制词头列表如下，同时标出对应的 10 的幂和 2 的幂。

| Term | Description    |
|------|----------------|
| `y`  | 10^-24 / 2^-80 |
| `z`  | 10^-21 / 2^-70 |
| `a`  | 10^-18 / 2^-60 |
| `f`  | 10^-15 / 2^-50 |
| `p`  | 10^-12 / 2^-40 |
| `n`  | 10^-9 / 2^-30  |
| `u`  | 10^-6 / 2^-20  |
| `m`  | 10^-3 / 2^-10  |
| `c`  | 10^-2          |
| `d`  | 10^-1          |
| `h`  | 10^2           |
| `k`  | 10^3 / 2^10    |
| `K`  | 10^3 / 2^10    |
| `M`  | 10^6 / 2^20    |
| `G`  | 10^9 / 2^30    |
| `T`  | 10^12 / 2^40   |
| `P`  | 10^15 / 2^50   |
| `E`  | 10^18 / 2^60   |
| `Z`  | 10^21 / 2^70   |
| `Y`  | 10^24 / 2^80   |

# 另请参见

ffmpeg(1), ffplay(1), ffprobe(1), libavutil(3)
