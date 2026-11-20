# 引言

drawvg（draw vector graphics，绘制矢量图形）是一种在视频帧之上绘制二维图形的语言。它并非作为通用语言而设计。由于其作用范围有限，它优先追求简洁与易用。

例如，使用 [Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)，我们可以在 Web 浏览器中运行以下代码来渲染一个三角形：

``` c
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

ctx.beginPath();
ctx.moveTo(125, 50);
ctx.lineTo(100, 100);
ctx.lineTo(150, 100);
ctx.closePath();
ctx.stroke();
```

同样的三角形也可以用下面这个 drawvg 脚本来绘制：

``` text
moveto 125 50
lineto 100 100 150 100
closepath
stroke
```

可以利用 [`moveto`](#m-moveto)、[`lineto`](#l-lineto) 和 [`closepath`](#z-z-closepath) 的别名将其缩短：

``` text
M 125 50
L 100 100 150 100
Z
stroke
```

换行符（`U+000A`）和空格（`U+0020`）可以互换使用作为分隔符，因此多条命令可以出现在同一行上：

``` text
M 125 50 L 100 100 150 100 Z
stroke
```

最后，drawvg 可以使用 `ffmpeg-utils` 中"FFmpeg 表达式"小节的内容，以及在命令参数中使用帧元数据。在本例中，我们使用变量 \<w\>（帧宽度）和 \<h\>（帧高度）在帧中央创建一个圆。

``` text
circle (w / 2) (h / 2) (w / 3)
stroke
```

许多命令与 [Cairo 图形库](https://www.cairographics.org/)中的函数直接等价。对于这类命令，下方的参考提供了指向相关 Cairo 文档的链接。

# 语法

该语法的灵感大量来自 [Magick Vector Graphics](https://imagemagick.org/script/magick-vector-graphics.php) 和 [SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path) 等语言。许多命令名取自 [PostScript](https://en.wikipedia.org/wiki/PostScript)。

## 结构

drawvg 脚本由一系列描述 2D 图形的命令组成。

命令是一个标识符（如 [`setcolor`](#setcolor) 或 [`lineto`](#l-lineto)），后跟其参数。代码中的每个项（命令名、参数等）由以下任一字符分隔：

- 空格（`' '`）

- 逗号（`','`）

- 换行符（`'\n'`）

- 制表符（`'\t'`）

- 回车符（`'\r'`）

项的开头字符决定它将如何被解释：

| 项   | 描述                             |
|------|----------------------------------|
| `//` | 注释                             |
| `0`, …, `9`, `+`, `-` | 数字字面量       |
| `(`  | 表达式                           |
| `{`, `}` | 块分隔符                      |
| 其他 | 命令名、颜色名等                 |

## 注释

注释以两个斜杠（`//`）开始，并在行尾结束（`\n` 或脚本结尾）。

``` text
circle 100 100 50 // this is ignored
fill

// this is also ignored
```

`//` 必须出现在空格之后或行首。如果 `//` 前面有任何非空白字符，解析器会把 `//` 视为前一项的一部分。

例如，在这个脚本中：

``` text
circle 10 10 50// something
```

解析器抛出错误，因为它试图把 `50//` 解析为数字字面量。

## 命令

命令的解析方式灵感来自 [SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path)：

- 脚本中的每条命令都以其名称开始，后跟零个或多个参数。

- 命令之间或参数之间没有显式分隔符。

  大多数编程语言期望用括号、逗号或分号等字符来分隔各项。例如：

  ``` c
  moveto(10, 10); lineto(20, 30);
  ```

  drawvg 中的等价写法是：

  ``` text
  moveto 10 10 lineto 20 30
  ```

- 如果命令没有参数（如 [`closepath`](#z-z-closepath) 或 [`stroke`](#stroke)），下一条命令将从下一项开始。

<div class="sidebar">

<div class="title">

示例

</div>

在下一个脚本中有 4 条不同的命令：

``` text
newpath rect 10 20 30 40 setcolor teal fill
```

1.  [`newpath`](#newpath) 不需要参数。

2.  [`rect`](#rect) 需要 4 个参数，因此它取接下来的 4 个数字。

3.  [`setcolor`](#setcolor) 需要 1 个参数，因此它取单词 `teal`。

4.  [`fill`](#fill-eofill) 不需要参数。

</div>

### 单字母别名

[SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path) 中的大多数命令在 drawvg 中也存在。对于其中一部分命令，存在指向更长名称的别名：

- [`curveto`](#c-curveto) 对应 [`C`](#c-curveto)。

- [`rcurveto`](#c-rcurveto) 对应 [`c`](#c-rcurveto)。

- [`lineto`](#l-lineto) 对应 [`L`](#l-lineto)。

- [`rlineto`](#l-rlineto) 对应 [`l`](#l-rlineto)。

- [`moveto`](#m-moveto) 对应 [`M`](#m-moveto)。

- [`rmoveto`](#m-rmoveto) 对应 [`m`](#m-rmoveto)。

- [`closepath`](#z-z-closepath) 对应 [`Z`](#z-z-closepath)、[`z`](#z-z-closepath)。

其他命令只以单字母形式存在：

- [`H`](#h-h), [`h`](#h-h)

- [`Q`](#q), [`q`](#q)

- [`S`](#s-s), [`s`](#s-s)

- [`V`](#v-v), [`v`](#v-v)

- [`T`](#t-t), [`t`](#t-t)

这使得可以用 SVG 的路径在 drawvg 脚本中创建相同的形状。

### 隐式命令

对于许多命令，在连续调用中多次使用时可以省略其名称。

在下文的命令参考中，这类命令的签名处标有 *可为隐式* 注记。

<div class="sidebar">

<div class="title">

示例

</div>

例如，在这个脚本中：

``` text
M 50 50
l 10 10
l 10 -10
l 10 10
l 10 -10
l 10 10
stroke
```

在第一次调用 [`l`](#l-rlineto)（[`rlineto`](#l-rlineto) 的别名）之后，该命令可以不带名称执行，因此可以写作：

``` text
M 50 50
l 10 10 10 -10 10 10 10 -10 10 10
stroke
```

</div>

要复用同一条命令（上例中的 [`l`](#l-rlineto)），解析器会检查最后一个参数之后的项是否为数值，比如数字字面量或 FFmpeg 表达式。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中：

``` text
l 10 20 30 40 stroke
```

[`l`](#l-rlineto) 需要 2 个参数，并且可为隐式，因此解析器执行以下操作：

1.  取接下来的两项（`10` 和 `20`）并发出第一条指令。

2.  检查 `20` 之后的项是否为数值。由于它是 `30`，于是取 `30` 和 `40` 并发出第二条指令（`l 30 40`）。

3.  检查 `40` 之后的下一项是否为数值，但它是一条命令（[`stroke`](#stroke)），因此停止复用 [`l`](#l-rlineto)。

</div>

这是另一个取自 [SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path) 的特性。与 SVG 的一个重要区别是：各项之间的分隔符始终是必需的。在 SVG 中，某些情况下可以省略它。例如，表达式 `m1-2` 在 SVG 中等价于 `m 1 -2`，但在 drawvg 中是语法错误。

## 参数

大多数命令接受数字参数，比如数字字面量、变量名或表达式。

[`setcolor`](#setcolor) 和 [`colorstop`](#colorstop) 接受一个颜色。

[`setlinecap`](#setlinecap) 和 [`setlinejoin`](#setlinejoin) 接受一个常量值。

### 数字字面量

数字字面量是脚本中表示常量值的项。任何以十进制数字（`0` 到 `9` 之间）、`-` 或 `+` 开头的项都会被解释为数字字面量。

该值用 [`av_strtod`](https://ffmpeg.org/doxygen/trunk/eval_8c.html#a7d21905c92ee5af0bb529d2daf8cb7c3) 解析。它支持 `0x` 前缀来书写十六进制值，并支持[许多单位](https://ffmpeg.org/ffmpeg-utils.html#:~:text=The%20evaluator%20also%20recognizes%20the%20International%20System%20unit%20prefixes)（如 `K` 或 `GiB`）。

在下一个例子中，所有字面量都表示同一个值：

``` text
10000
1e4
10K
0x2710
```

### 表达式

`ffmpeg-utils` 中"FFmpeg 表达式"小节的内容可用作任何接受数字参数的命令的参数。表达式必须用括号括起。

<div class="sidebar">

<div class="title">

示例

</div>

变量 \<w\> 和 \<h\> 表示帧的宽度和高度。我们可以把它们除以 `2` 来计算帧的中心：

``` text
M (w / 2) (h / 2)
```

它们还可以包含括号（用于分组运算、调用函数等）：

``` text
moveto
    ((w + 10) / 2)      // x
    (h / (2 * cos(t)))  // y
```

</div>

变量 \<n\> 和 \<t\> 可用于计算随时间变化的值。

<div class="sidebar">

<div class="title">

示例

</div>

要绘制一个从左向右振荡的圆，我们可以对 `x` 坐标使用基于 `sin(t)` 的表达式：

``` text
circle
    (w / 2 + sin(2 * t) * w / 4)  // x
    (h / 2)                       // y
    (w / 5)                       // radius

stroke
```

</div>

表达式可以分写成多行，但其内部不能包含注释。

``` text
moveto   // This is a comment.
    (w   // This is part of the expression, not a comment.
     + h)
```

### 变量名

当表达式只是对变量的引用时，括号可以省略，此时该项就是变量名。

<div class="sidebar">

<div class="title">

示例

</div>

接下来的 3 个表达式是等价的：在所有情况下，它们都会创建一个覆盖整帧的矩形。

``` text
rect (0) (0) (w) (h)

rect 0 0 w h

rect (0) 0 (w) h
```

</div>

可以创建与命令同名的变量，然后将其用作参数。在上一个例子中，项 \<h\> 是对变量（帧高度）的引用，但在其他上下文中它可能是一条命令（[`h`](#h-h)）。

对于[隐式命令](#隐式命令)，当解析器需要判断命令是否被复用时，命令优先于变量名。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，变量 \<c\> 在两次调用 [`l`](#l-rlineto) 时被用作第一个参数。然而只有第一次是有效的，因为在第二次调用中解析器将 [`c`](#c-rcurveto) 识别为命令。

``` text
setvar c 5
l c 10 c 15
```

这个问题可以通过给第二次调用的开头加上括号来解决：

``` text
setvar c 5
l c 10 (c) 15
```

</div>

### 颜色

描边和填充路径所用的颜色可以用 [`setcolor`](#setcolor) 设置。其参数与 FFmpeg 中的颜色语法相同：

- `ffmpeg-utils` 中"预定义颜色名"小节中的名称。

- `#RRGGBB` 格式。

- 可以添加 `@a` 后缀来设置 alpha 值（可选），其中 `a` 是 `0` 到 `1` 之间的数字。

``` text
circle 70 70 60
setcolor #FF0000
fill

circle 170 170 60
setcolor blue@0.5
fill
```

颜色可以是变量名。在这种情况下，必须先用 [`defrgba`](#defrgba)、[`defhsla`](#defhsla) 或 [`setvar`](#setvar) 配合一个颜色为其赋值。

``` text
circle 70 70 60
setvar CustomGreen #22FF44
setcolor CustomGreen
fill

circle 170 170 60
defhsla CustomBlue 200 0.7 0.5 1
setcolor CustomBlue
fill
```

命令 [`setrgba`](#setrgba) 和 [`sethsla`](#sethsla) 允许用表达式设置颜色。它们类似于 [`defrgba`](#defrgba) 和 [`defhsla`](#defhsla)，但没有中间变量。

### 常量

[`setlinecap`](#setlinecap) 和 [`setlinejoin`](#setlinejoin) 的参数是引用常量值的标识符。

``` text
setlinecap round
```

# 指南

## 路径

路径是一种复杂形状，由直线和曲线组成，可用于填充区域、描边轮廓或建立裁剪区域。

要在视频帧之上绘制任何内容，首先必须定义一个路径，然后使用 [`stroke`](#stroke) 或 [`fill`](#fill-eofill)。

[MDN 上的路径教程](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths)是该主题很好的入门材料。它聚焦于 [SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path)，但相同的概念也适用于 drawvg。

### 当前点

一些命令需要*当前点*。初始时，*当前点*被设为 [`NaN`](https://en.wikipedia.org/wiki/NaN)。它由 [`M`](#m-moveto) 或 [`moveto`](#m-moveto) 初始化。其他命令（如 [`lineto`](#l-lineto) 或 [`curveto`](#c-curveto)）会把*当前点*更新为形状的新终点。

*当前点*可以用 [`newpath`](#newpath) 清除。清除路径的命令（如 [`stroke`](#stroke) 或 [`fill`](#fill-eofill)）也会清除*当前点*。

<div class="sidebar">

<div class="title">

示例

</div>

[`rlineto`](#l-rlineto) 使用相对于*当前点*的坐标。

给定这个脚本：

``` text
moveto 20 100
rlineto 150 -90
rlineto -50 200
closepath
stroke
```

这些是执行每条命令后*当前点*的坐标：

| 命令              | 当前点        |
|-------------------|---------------|
| `moveto 20 100`   | `20, 100`     |
| `rlineto 150 -90` | `170, 10`     |
| `rlineto -10 50`  | `140, 210`    |
| `closepath`       | `20, 100`     |

同一脚本也可以用单字母别名书写：

``` text
M 20 100 l 150 -90 -50 200 z stroke
```

</div>

### 定义形状

路径通过添加直线、曲线或基本形状来定义。

- 基本形状

  - [`circle`](#circle)

  - [`ellipse`](#ellipse)

  - [`rect`](#rect)

  - [`roundedrect`](#roundedrect)

- 直线

  - [`M`](#m-moveto), [`moveto`](#m-moveto)

  - [`m`](#m-rmoveto), [`rmoveto`](#m-rmoveto)

  - [`H`](#h-h), [`h`](#h-h)

  - [`V`](#v-v), [`v`](#v-v)

  - [`L`](#l-lineto), [`lineto`](#l-lineto)

  - [`l`](#l-rlineto), [`rlineto`](#l-rlineto)

  - [`Z`](#z-z-closepath), [`z`](#z-z-closepath), [`closepath`](#z-z-closepath)

- 曲线

  - [`arc`](#arc), [`arcn`](#arcn)

  - [`C`](#c-curveto), [`curveto`](#c-curveto),

  - [`c`](#c-rcurveto), [`rcurveto`](#c-rcurveto)

  - [`Q`](#q), [`q`](#q)

  - [`S`](#s-s), [`s`](#s-s)

  - [`T`](#t-t), [`t`](#t-t)

单字母命令取自 [SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path)。

### 填充

由路径定义的形状内部区域可以用 [`fill`](#fill-eofill) 或 [`eofill`](#fill-eofill) 填充。每条命令使用不同的[填充规则](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-fill-rule-t)：

- [`fill`](#fill-eofill) 使用[环绕规则](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-WINDING:CAPS)（亦称[非零规则](https://en.wikipedia.org/wiki/Nonzero-rule)）。

- [`eofill`](#fill-eofill) 使用[奇偶规则](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS)。

<div class="sidebar">

<div class="title">

示例

</div>

这个脚本展示了[环绕规则](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-WINDING:CAPS)与[奇偶规则](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS)之间的区别：

``` text
rect 50 10 100 60
circle 150 70 40
setcolor seagreen
fill

rect 50 130 100 60
circle 150 190 40
setcolor skyblue
eofill
```

</div>

### 描边

[`stroke`](#stroke) 沿路径定义的形状周围绘制线条。描边可以用以下命令配置：

- [`setdash`](#setdash)

- [`setdashoffset`](#setdashoffset)

- [`setlinecap`](#setlinecap)

- [`setlinejoin`](#setlinejoin)

- [`setlinewidth`](#setlinewidth)

- [`resetdash`](#resetdash)

<div class="sidebar">

<div class="title">

示例

</div>

这个例子使用 [`setdashoffset`](#setdashoffset) 来制作描边动画：

``` text
moveto 0 0
lineto w h

setlinecap round
setdash 50 50
setlinewidth 20
setdashoffset (hypot(w, h) * t / -3)
setcolor seagreen

stroke
```

</div>

### 裁剪

可以用 [`clip`](#clip-eoclip) 和 [`eoclip`](#clip-eoclip) 建立[裁剪区域](https://en.wikipedia.org/wiki/Clipping_(computer_graphics))。

如果已存在活动的裁剪区域，新的裁剪区域将是现有区域与路径的交集。[`resetclip`](#resetclip) 将裁剪区域重置为整帧。

[`eoclip`](#clip-eoclip) 使用[奇偶规则](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS)来计算裁剪区域。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
rect 50 50 100 200
clip

circle 30 30 150
setcolor seagreen
fill

// Draw outside the clip region.
resetclip
circle 30 30 150
setlinewidth 3
setcolor skyblue
stroke
```

</div>

### 保留路径

路径在任何作用于它的操作（如 [`fill`](#fill-eofill) 或 [`stroke`](#stroke)）之后都会被清除。要在多个操作中复用同一路径，必须在这些操作之前调用 [`preserve`](#preserve)。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，每个路径被使用了两次。

``` text
circle 120 120 50
setcolor seagreen
preserve stroke
clip

circle 100 100 50
setcolor skyblue
preserve fill
setcolor tomato
stroke
```

</div>

## 变量

drawvg 可以使用解释器提供的一些变量，在 `ffmpeg-utils` 中"FFmpeg 表达式"小节的语法中计算值：

- **\<cx\>** [当前点](#当前点) 的 X 坐标。

- **\<cy\>** [当前点](#当前点) 的 Y 坐标。

- **\<w\>** 帧的宽度（像素）。

- **\<h\>** 帧的高度（像素）。

- **\<i\>** repeat 块中的循环计数器。

- **\<n\>** 帧序号。

- **\<t\>** 时间戳（秒）。

- **\<ts\>** 第一帧的时间戳（秒）。

- **\<duration\>** 帧的时长（秒）。

### 用户变量

可以用 [`setvar`](#setvar) 命令创建新变量。它将一个名称与一个数值关联起来。

名称必须遵循以下规则：

- 必须以 ASCII 字母或下划线（`_`）开头。

- 只能包含 ASCII 字母、下划线和数字。

- 不得与解释器提供的变量名（如 \<w\> 或 \<t\>）同名。

同一个变量可以被多次赋值。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，一个表达式的结果被存储在名为 \<progress\> 的变量中。然后它被用作 [`rect`](#rect) 的 \<x\> 和 \<width\> 参数。

``` text
setvar progress (w * (pow(mod(t / 2 + 0.5, 1), 2.5)))

rect ((w - progress) / 2) 0 progress h

setcolor darkblue
fill
```

</div>

目前，一个脚本最多只能包含 20 个不同的变量名，但这一限制将来可能会修改。

## 图案

填充和描边操作所用的图案可以是纯色，也可以是渐变。

- 纯色。

  - [`setcolor`](#setcolor)

  - [`sethsla`](#sethsla)

  - [`setrgba`](#setrgba)

- 渐变。

  - [`lineargrad`](#lineargrad)

  - [`radialgrad`](#radialgrad)

图案在填充或描边操作中使用后不会被清除，但会被任何设置新图案的命令替换。

### 渐变

要配置渐变，首先调用 [`lineargrad`](#lineargrad) 或 [`radialgrad`](#radialgrad)，然后为每个停靠点调用 [`colorstop`](#colorstop) 添加色标（color stop）。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，整个帧被一个线性渐变填充：

``` text
lineargrad 0 0 w h
colorstop 0 skyblue
colorstop 1 darkblue

rect 0 0 w h
fill
```

在这个例子中，一个径向渐变被用来模拟一个球体：

``` text
radialgrad 90 90 5 120 120 100
colorstop 0.0 #90DDFF
colorstop 0.9 #000030
colorstop 1.0 #000000

rect 0 0 w h
fill
```

</div>

### 变量

[`setcolor`](#setcolor) 和 [`colorstop`](#colorstop) 接受变量名作为参数。该变量必须先用 [`defrgba`](#defrgba)、[`defhsla`](#defhsla) 或 [`setvar`](#setvar) 配合一个颜色赋值。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
// Use color #1020FF, alpha = 50%
setvar someblue #1020FF@0.5

setcolor someblue

rect 30 30 120 120
fill

rect 90 90 120 120
fill
```

</div>

如果变量与 `ffmpeg-utils` 中"已知颜色"小节中的名称相同，则变量优先，将使用该变量而非预定义颜色。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
setcolor teal
rect 30 30 120 120
fill

setvar teal #70AAAA
setcolor teal         // Use the new color for `teal`.
rect 90 90 120 120
fill
```

</div>

[`defrgba`](#defrgba) 和 [`defhsla`](#defhsla) 通过为每个颜色分量提供一个表达式，将颜色赋给变量：

- 对于 [`defrgba`](#defrgba)：*红*、*绿*、*蓝*和 *alpha*。

- 对于 [`defhsla`](#defhsla)：*色相*、*饱和度*、*亮度*和 *alpha*。

每个颜色分量必须在 `0` 到 `1` 之间，*色相*除外，它为 `0` 到 `360`。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
defrgba colorA 1 0.5 0.25 1     // colorA = RGB(255, 127, 63)
defhsla colorB 200 0.75 0.25 1  // colorB = HSL(200, 75%, 25%)

rect 0 0 (w / 2) h
setcolor colorA
fill

rect (w / 2) 0 (w / 2) h
setcolor colorB
fill
```

</div>

## 变换

每条命令的坐标可以通过以下命令进行缩放、旋转和平移：

- [`rotate`](#rotate)

- [`scale`](#scale)

- [`scalexy`](#scalexy)

- [`translate`](#translate)

变换在命令执行时生效。它们对现有路径没有影响，只影响添加到其中的新线段。

它们通过更新 Cairo 上下文中的[当前变换矩阵](https://www.cairographics.org/manual/cairo-Transformations.html)来完成。要将矩阵重置为进行任何变换之前的原始状态，请使用 [`resetmatrix`](#resetmatrix)。

缩放和旋转的变换原点初始位于 `0, 0`，但可以用 [`translate`](#translate) 调整。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
// Map (0, 0) as the center of the frame.
translate (w / 2) (h / 2)

// Scale the space as if the frame is 1x1 pixel.
scalexy w h

// Draw multiple lines with the same arguments,
// but each one on a different rotation.
repeat 10 {
    rotate (PI / 10)
    M -0.25 0
    H 0.25
}

// Reset transformations, so the scale does not
// affect stroke.
resetmatrix

stroke
```

</div>

## 状态栈

drawvg 脚本的状态包含绘制操作所用的所有参数，如当前颜色、变换矩阵、描边配置等。

[`save`](#save) 命令将状态快照压入内部栈。之后，[`restore`](#restore) 从栈中弹出最近的快照，并将其用作新的状态。

可以保存和恢复的参数有：

- 描边和填充操作的图案。

  - [`lineargrad`](#lineargrad)

  - [`radialgrad`](#radialgrad)

  - [`setrgba`](#setrgba)

  - [`setcolor`](#setcolor)

  - [`sethsla`](#sethsla)

- 变换矩阵。

  - [`resetmatrix`](#resetmatrix)

  - [`rotate`](#rotate)

  - [`scale`](#scale)

  - [`scalexy`](#scalexy)

  - [`translate`](#translate)

- 描边配置。

  - [`setdash`](#setdash)

  - [`setdashoffset`](#setdashoffset)

  - [`setlinecap`](#setlinecap)

  - [`setlinejoin`](#setlinejoin)

  - [`setlinewidth`](#setlinewidth)

- 裁剪区域

  - [`clip`](#clip-eoclip)

  - [`resetclip`](#resetclip)

## 帧元数据

一些 FFmpeg 滤镜会向帧添加元数据。命令 [`getmetadata`](#getmetadata) 可以读取包含数值的元数据项，并将其存储到可用于命令参数的变量中。

<div class="sidebar">

<div class="title">

示例

</div>

`cropdetect` 滤镜计算用于去除视频四周空白区域的参数。这些参数可以通过帧元数据的 `lavfi.cropdetect` 键访问。

``` text
// Get metadata from cropdetect filter and store it
// in `cd*` variables.
getmetadata cdx lavfi.cropdetect.x
getmetadata cdy lavfi.cropdetect.y
getmetadata cdw lavfi.cropdetect.w
getmetadata cdh lavfi.cropdetect.h

rect cdx cdy cdw cdh
setcolor yellow@0.5
setlinewidth 10
stroke
```

要测试该脚本，请将其复制到一个 `drawcropdetect.vgs` 文件，然后执行如下命令：

``` text
ffplay -i example-video.webm -vf 'cropdetect, drawvg=file=drawcropdetect.vgs'
```

</div>

## `if` / `repeat` 语句

对控制流语句的支持有限：只有 [`if`](#if) 和 [`repeat`](#repeat)。

两条命令都接受两个参数：一个表达式和一个块。

``` text
if (condition) {
    // commands
}

repeat (count) {
    // commands
}
```

[`if`](#if) 在 `(condition)` 的结果非零时执行其块。

[`repeat`](#repeat) 按 `(count)` 指定的次数执行其块。在每次迭代中，变量 \<i\> 被用作[循环计数器](https://en.wikipedia.org/wiki/For_loop#Loop_counters)。

如果表达式的结果不是有限数（如 [`NaN`](https://en.wikipedia.org/wiki/NaN)），则不会执行该块。

### 比较与逻辑运算符

`ffmpeg-utils` 中"FFmpeg 表达式"小节只支持算术运算符（如表示加法的 `+`）。比较运算符（如 `!=`）通过函数支持，而逻辑运算符（如表示 `AND` 的 `&&`）可以用算术运算模拟。

| 表达式      | FFmpeg 等价写法    |
|-------------|--------------------|
| `x = y`     | `eq(x, y)`         |
| `x < y`     | `lt(x, y)`         |
| `x > y`     | `gt(x, y)`         |
| `x ≤ y`     | `lte(x, y)`        |
| `x ≥ y`     | `gte(x, y)`        |
| `a ≤ x ≤ b` | `between(x, a, b)` |

逻辑运算符可以用乘法（对应 `AND`）或加法（对应 `OR`）来模拟：

| 表达式     | FFmpeg 等价写法   |
|------------|-------------------|
| `x OR y`   | `x + y`           |
| `x AND y`  | `x * y`           |

<div class="sidebar">

<div class="title">

示例

</div>

在其他编程语言中，如下代码：

``` text
if (x > y && z != 1) {
    // …
}
```

在 drawvg 中可以这样写：

``` text
if (gt(x, y) * not(eq(z, 1))) {
    // …
}
```

</div>

### 提前退出

[`break`](#break) 会使 [`repeat`](#repeat) 循环立即终止。

如果在 [`repeat`](#repeat) 块之外执行，它会终止整个脚本或当前过程。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，我们使用 [`randomg`](#函数-randomg) 函数绘制一条由随机线段组成的线。

循环可以执行 `500` 次，但如果[当前点](#当前点)（\<cx\>）的 X 坐标超过帧宽度（\<w\>）就会中断。每次调用 [`rlineto`](#l-rlineto) 之后都会更新[当前点](#当前点)。

``` text
moveto 0 0

repeat 500 {
    rlineto
        (randomg(0) * 15)
        (randomg(0) * 20)

    if (gt(cx, w)) {
        break
    }
}

stroke
```

</div>

## 过程

过程是与一个块关联的名称，可以多次执行。它可以接受 0 到 6 个参数。

[`proc`](#proc) 用于设置过程的参数名和块：

``` text
proc p0 {
    // …
}

proc p1 param1 param2 {
    // …
}
```

在块内，参数可以作为普通变量访问：

``` text
proc square center_x center_y side {
    rect
        (center_x - side / 2) (center_y - side / 2)
        side side
}
```

[`call`](#call) 执行分配给过程名的块。它要求提供过程名，以及 [`proc`](#proc) 调用中定义的每个参数的值。

``` text
call p0

call p1 1 2

call square (w / 2) (h / 2) (w / t)
```

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，过程 `zigzag` 从[当前点](#当前点)绘制多条线。

``` text
setvar len (w / 10)
setlinewidth 5

proc zigzag {
    repeat 10 {
        l len len len (-len)
    }

    stroke
}

setcolor #40C0FF
M 0 60
call zigzag

setcolor #00AABB
M 0 120
call zigzag

setcolor #20F0B7
M 0 180
call zigzag
```

起点的颜色和 Y 坐标可以作为过程参数传入：

``` text
setvar len (w / 10)
setlinewidth 5

proc zigzag color y {
    setcolor color

    M 0 y
    repeat 10 {
        l len len len (-len)
    }

    stroke
}

call zigzag #40C0FF 60
call zigzag #00AABB 120
call zigzag #20F0B7 180
```

</div>

当过程返回时，每个参数对应的变量值会恢复为调用过程之前的值。对其他变量的修改（通过 [`setvar`](#setvar)、[`getmetadata`](#getmetadata)、[`defhsla`](#defhsla) 和 [`defrgba`](#defrgba)）会被保留。

<div class="sidebar">

<div class="title">

示例

</div>

在下一个例子中，变量 \<A\> 在调用过程 \<P\> 之前的值为 `0`。在 \<P\> 执行期间，`A` 为 `1`；执行结束后，\<A\> 又变回 `0`。

``` text
setvar A 0

proc P A {
    print A
}

print A
call P 1
print A
```

它会写出以下消息：

``` text
[7:7] A = 0.000
[4:8] A = 1.000
[9:7] A = 0.000
```

</div>

[`break`](#break) 会使脚本退出当前过程，类似于其他编程语言中的 [`return` 语句](https://en.wikipedia.org/wiki/Return_statement)，除非它是在 [`repeat`](#repeat) 循环内被调用。

过程体必须在使用 [`call`](#call) *之前*用 [`proc`](#proc) 定义。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，当过程 `notyet` 被调用时，其过程体尚未定义，因此执行失败并报错 `Missing body for procedure 'notyet'`。

``` text
call notyet

proc notyet {
    // ...
}
```

</div>

过程可以通过其他使用同名 [`proc`](#proc) 的调用重新定义。在这种情况下，[`call`](#call) 会调用最后分配的块。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，过程 `example` 有两个不同的块。

``` text
proc example {
    // block1
}

call example    // executes block1

proc example {
    // block2
}

call example    // executes block2
```

</div>

## 表达式中的函数

`ffmpeg-utils` 中"FFmpeg 表达式"小节中有一些 drawvg 特有的函数可用。

### 函数 `p`

`p(x, y)` 返回坐标 `x, y` 处像素的颜色，表示为 `0xRRGGBBAA` 值。它可以赋给一个变量，使该颜色可供 [`setcolor`](#setcolor) 和 [`colorstop`](#colorstop) 命令使用。

如果单个表达式包含多次对该函数的调用，则必须返回最后一次调用的值，才能将其用作颜色。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，第一次调用 `p(0, 0)` 的结果存储在表达式的变量 \<0\> 中。然后同一表达式进行第二次调用 `p(1, 1)`，最后返回变量 \<0\> 中的值。

``` c
setvar pixel (st(0, p(0, 0)); p(1, 1); ld(0))
```

由于表达式的结果不是最后一次对 `p` 的调用，变量 \<pixel\> 不能用作颜色，但仍可用作数值型的 `0xRRGGBBAA` 值。

</div>

如果坐标在帧之外，或任一参数不是有限数（如 [`NaN`](https://en.wikipedia.org/wiki/NaN)），该函数返回 `NaN`。

[变换矩阵](#变换)会作用于这些参数。要使用原始帧坐标，请在 [`save`](#save) 和 [`restore`](#restore) 之间调用 [`resetmatrix`](#resetmatrix)：

``` text
save
resetmatrix
setvar pixel (p(0, 0))    // top-left pixel of the frame.
restore

setcolor pixel
```

可以使用按位运算来提取各个颜色分量：

``` text
setvar pixel (p(x, y))

if (not(isnan(pixel))) {
    setvar px_red   (pixel / 0x1000000)
    setvar px_green (bitand(pixel / 0x10000, 0xFF))
    setvar px_blue  (bitand(pixel / 0x100, 0xFF))
    setvar px_alpha (bitand(pixel, 0xFF))
}
```

### 函数 `pathlen`

`pathlen(n)` 通过累加 [`cairo_copy_path_flat`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-copy-path-flat) 返回的每条线段的长度来计算当前路径的长度。

该函数接受一个参数 \<n\>，作为要累加到长度中的线段数上限，或 `0` 表示累加所有线段。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，`pathlen` 被用于在 5 秒循环中制作螺旋线描边的动画。

``` text
M (w / 2) (h / 2)

setvar a -1
repeat 16 {
    rcurveto
        (a * 2 / 3) 0
        (a * 2 / 3) (a)
        0 (a)

    setvar a (-sgn(a) * (abs(a) + 10))
}

setlinewidth 3
setdash
    (pathlen(0) * (1 - mod(t / 5, 1)))
    1e6

setcolor teal
stroke
```

</div>

### 函数 `randomg`

`randomg(idx)` 类似于 `ffmpeg-utils` 中"FFmpeg 表达式"小节提供的 `random(idx)` 函数，但它的状态对整帧是全局的，而不是每个表达式各自持有。

要理解它们的区别，我们需要深入了解 `random(idx)` 在 drawvg 脚本中的工作方式。

首先，FFmpeg 中的每个表达式都有一组 10 个内部变量，可用 `st(idx, value)` 写入，用 `ld(idx)` 读取。\<idx\> 是 `0` 到 `9` 之间的值。这些变量被初始化为 `0`。

当 drawvg 脚本被解析时，每个表达式都会用 [`av_expr_parse`](https://ffmpeg.org/doxygen/8.0/eval_8h.html#ad3bf8f3330d1fd139de2ca156c313f34)（来自 [libavutil](https://ffmpeg.org/libavutil.html)）编译，并且这些编译后的表达式会在每一帧中复用。内部变量的变化（通过 `st(idx, value)`）在各帧之间可见，但不会在表达式之间共享。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，X 坐标的表达式在每一帧都更新其内部变量 `0`：

``` text
circle
    (st(0, mod(ld(0) + 15, w))) // X
    120                         // Y
    (ld(0) + 20)                // radius

fill
```

`st(idx, value)` 返回更新后的值，因此可以用作表达式的结果。

半径不受影响，因为它的内部变量（来自 `ld(0)`）没有被另一个表达式更新。

另请注意，这个例子只是为了展示内部变量如何在各帧之间保留。创建这种动画的更好方法是使用变量 n 或 t：

``` text
circle (mod(n * 15, w)) 120 20
fill
```

</div>

函数 `random(idx)` 返回一个介于 `0` 和 `1` 之间的[伪随机](https://en.wikipedia.org/wiki/Pseudorandom_number_generator)值。\<idx\> 是内部变量，既用作种子，也用于保存数字生成器的状态。

<div class="sidebar">

<div class="title">

示例

</div>

下一个例子使用 `random(0)` 为圆心生成一个随机值：

``` text
circle
    (random(0) * w)
    (random(0) * h)
    10

fill
```

每一帧的圆都位于不同的位置，但总是在帧的对角线上。这是因为 X 和 Y 坐标的值相同——两个数字生成器使用了相同的种子。

要让圆分布到整个帧上，我们需要为每个表达式使用不同的种子。这可以通过向其中一个表达式的内部变量写入一个非零值（如 `0xF0F0`）来实现，但仅在其值为 `0` 时写入：

``` c
circle
    (random(0) * w)
    (st(0, if(ld(0), ld(0), 0xF0F0)); random(0) * h)
    10

fill
```

这种方法只在需要每帧完全不同的位置时才有用。在下一个例子中，随机值用于将许多圆分布到帧上，但位置是固定的。唯一随时间变化的是填充颜色：

``` c
repeat 20 {
    circle
        (st(0, i + 1e5); random(0) * w)
        (st(0, i + 1e10); random(0) * h)
        10
}

sethsla (t * 60) 0.5 0.5 1
preserve fill

setcolor black@0.5
setlinewidth 1
stroke
```

这是通过在调用 `random(0)` 之前使用一个预计算的状态实现的。变量 \<i\>（由 [`repeat`](#repeat) 更新）用于在每次迭代中计算不同的状态。

</div>

`randomg(idx)` 函数是 drawvg 脚本特有的，类似于 `random(idx)`，但旨在解决前面的问题：

- 所有帧都使用相同的种子。

- 状态在表达式之间共享。

参数 \<idx\> 有两个用途：

- 最后两个比特是内部状态的索引，因此可以有 4 个不同的数字生成器。

- 对特定索引首次调用 `randomg` 时，参数将用作该索引处数字生成器的种子。

在这样的脚本中：

``` text
M (randomg(0xFF1)) (randomg(0xFF0))
l (randomg(0xAA1)) (randomg(0xFF0))
```

有 4 次对 `randomg` 的调用：

1.  第一次调用的参数为 `0xFF1`，使用索引 `1` 处的内部状态（因为 `0xFF1` 对 `4` 取模为 `1`）。

    由于这是该索引的首次使用，数字生成器以种子 `0xFF1` 初始化。

2.  第二次调用行为相同：它用值 `0xFF0` 初始化索引 `0` 处的状态。

3.  第三次调用的参数为 `0xAA1`，使用索引 `1`。由于该状态已经初始化（种子为 `0xFF1`），值 `0xAA1` 被忽略，它返回下一个数字。

<div class="sidebar">

<div class="title">

示例

</div>

这个例子渲染了一个简单的下雨动画，让线条从上到下移动。

`randomg` 用于将线条分布到帧上，并为每条线赋予不同的速度。

``` text
rect 0 0 w h
setcolor midnightblue
fill

setcolor white

repeat 50 {
    setvar offset (t * (randomg(0) + 1))

    moveto
        (mod(randomg(0) + offset / 6, 1) * w)
        (mod(randomg(0) + offset, 1) * h)

    rlineto 6 36

    setlinewidth (randomg(1) / 2 + 0.2)
    stroke
}
```

</div>

## 使用 `print` 跟踪

可以通过 [`print`](#print) 命令或 print 函数打印表达式的值，来跟踪 drawvg 脚本的执行。

在这两种情况下，值都会写入 FFmpeg 日志。

打印表达式可能会对性能产生明显影响，因此最好只在必要时使用。

### 函数 print

函数 `print(t)` 写出 t 的值，并返回其参数。

<div class="sidebar">

<div class="title">

示例

</div>

给定这样一行：

``` text
M (sin(2 * PI * t) * w) 0
```

我们可以通过用 `print()` 调用将 `sin(2 * PI * t)` 包起来，观察它的值：

``` text
M (print(sin(2 * PI * t)) * w) 0
```

以 1 秒 / 8 FPS 的视频执行此脚本，会显示正弦函数的预期值。

``` text
$ ffmpeg \
    -f lavfi \
    -i 'color=r=8:d=1, drawvg=M (print(sin(2 * PI * t)) * w) 0' \
    -f null /dev/null \
  |& grep 'Eval @'

[Eval @ 0x7f500f502d20] 0.000000
[Eval @ 0x7f4ff784b420] 0.707107
[Eval @ 0x7f4ff784ba20] 1.000000
[Eval @ 0x7f4ff784c020] 0.707107
[Eval @ 0x7f4ff784c620] 0.000000
[Eval @ 0x7f4ff784cc20] -0.707107
[Eval @ 0x7f4ff784d220] -1.000000
[Eval @ 0x7f4ff784d820] -0.707107
```

</div>

### 命令 `print`

命令 [`print`](#print) 接受任意数量的参数，并对每个参数写出：

- 源码位置（行和列）。

- 表达式的源代码。

- 表达式求值的结果。

当有多个表达式时，它们用 `|` 字符分隔。

<div class="sidebar">

<div class="title">

示例

</div>

下一个脚本在 [`l`](#l-rlineto) 命令之后打印[当前点](#当前点)的位置：

``` text
M 10 20
l 100 100
print cx cy
stroke
```

对于每一帧，它产生如下输出：

``` text
[3:7] cx = 110.000000 | [3:10] cy = 120.000000
```

下一个例子打印 `random(0)` 的值：

``` text
$ ffmpeg \
    -f lavfi \
    -i 'color=r=8:d=1, drawvg=print (random(0))' \
    -f null /dev/null \
  |& grep 'drawvg @'

[drawvg @ 0x50a000000180] [1:7] (random(0)) = 0.229731
[drawvg @ 0x50a000000180] [1:7] (random(0)) = 0.959813
[drawvg @ 0x50a000000180] [1:7] (random(0)) = 0.071676
[drawvg @ 0x50a000000180] [1:7] (random(0)) = 0.044600
[drawvg @ 0x50a000000180] [1:7] (random(0)) = 0.134127
[drawvg @ 0x50a000000180] [1:7] (random(0)) = 0.320513
[drawvg @ 0x50a000000180] [1:7] (random(0)) = 0.857675
[drawvg @ 0x50a000000180] [1:7] (random(0)) = 0.562456
```

</div>

# 命令

## `arc`

**`arc xc yc radius angle1 angle2`**    — [*可为隐式*](#隐式命令)

向当前路径添加一段给定 \<radius\> 的圆弧。圆弧以 \<xc, yc\> 为圆心，从 \<angle1\> 开始，沿角度增大的方向行进，到 \<angle2\> 结束。

如果存在[当前点](#当前点)，会从它向圆弧起点添加一条线。如果不希望如此，请在 [`arc`](#arc) 之前使用 [`newpath`](#newpath) 来清除[当前点](#当前点)。

详见 [`cairo_arc`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-arc) 函数的文档，了解更多细节。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
arc 120 120 60 0 (3 * PI / 2)
stroke
```

</div>

## `arcn`

**`arcn xc yc radius angle1 angle2`**    — [*可为隐式*](#隐式命令)

与 [`arc`](#arc) 类似，但两条角度之间的圆弧方向不同。

详见 [`cairo_arc_negative`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-arc-negative) 函数的文档，了解更多细节。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，[`arc`](#arc) 与 [`arcn`](#arcn) 使用相同的角度，但渲染出不同的弧：

``` text
arc  120  90 60 (PI / 2) 0

newpath
arcn 120 150 60 (PI / 2) 0

stroke
```

</div>

需要用 [`newpath`](#newpath) 来避免在两条弧之间连线。

## `break`

**`break`**

[`break`](#break) 终止最内层块的执行，可以是 [`repeat`](#repeat) 循环或过程。

如果在 [`repeat`](#repeat) / [`proc`](#proc) 块之外使用，它会终止当前帧的脚本。

## `call`

**`call name args*`**

调用由 [`proc`](#proc) 定义的过程。

详见上文的 [过程](#过程) 小节，了解更多细节。

## `circle`

**`circle xc yc radius`**    — [*可为隐式*](#隐式命令)

向当前路径添加一个给定 \<radius\> 的圆。圆以 \<xc, yc\> 为圆心。添加圆之前和之后，[当前点](#当前点)都会被清除。

这是 [`arc`](#arc) 的便捷封装。调用 [`circle`](#circle) 等价于：

``` text
newpath
arc xc yc radius (0) (2 * PI)
newpath
```

## `clip`, `eoclip`

**`clip, eoclip`**

将当前裁剪区域与当前路径（按 [`fill`](#fill-eofill) 或 [`eofill`](#fill-eofill) 填充它的方式）求交集，建立新的裁剪区域。

[`eoclip`](#clip-eoclip) 使用[奇偶规则](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS)。详见[填充规则](#填充)。

在更新裁剪区域后路径会被清除，除非在 [`clip`](#clip-eoclip) 或 [`eoclip`](#clip-eoclip) 之前使用了 [`preserve`](#preserve) 命令。

详见 [`cairo_clip`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-clip) 函数的文档，了解更多细节。

## `Z`, `z`, `closepath`

**`Z, z, closepath`**

向路径添加一条从[当前点](#当前点)到当前子路径起点的线段，并闭合该子路径。起点由任何*移动*命令设置（[`M`](#m-moveto)、[`m`](#m-rmoveto)、[`moveto`](#m-moveto)、[`rmoveto`](#m-rmoveto)）。

详见 [`cairo_close_path`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-close-path) 函数的文档，了解更多细节。

## `colorstop`

**`colorstop offset color`**    — [*可为隐式*](#隐式命令)

向渐变图案添加一个色标。

\<offset\> 是 `0` 到 `1` 之间的值，它指定沿渐变控制向量的位置。

此命令必须在 [`lineargrad`](#lineargrad) 或 [`radialgrad`](#radialgrad) 之后执行。

色标可以在多次调用 [`colorstop`](#colorstop) 中添加。在下一个例子中，3 个块定义了相同的渐变：

``` text
// 1
colorstop 0.0 red
colorstop 0.5 green
colorstop 1.0 blue

// 2
colorstop 0 red 0.5 green
colorstop 1 blue

// 3
colorstop 0 red 0.5 green 1 blue
```

详见 [`cairo_pattern_add_color_stop_rgba`](https://www.cairographics.org/manual/cairo-cairo-pattern-t.html#cairo-pattern-add-color-stop-rgba) 函数的文档，了解更多细节。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，色标在一个 [`repeat`](#repeat) 循环中添加。

``` text
lineargrad 0 0 w h

repeat 6 {
    defhsla s (i * 60) 0.8 0.5 1
    colorstop (i / 5) s
}

rect 0 0 w h
fill
```

可以通过在两个色标中重复使用相同颜色来避免色标之间的过渡：

``` text
lineargrad 0 0 w h

repeat 6 {
    defhsla s (i * 60) 0.8 0.5 1
    colorstop (i / 5) s
    colorstop ((i + 1) / 5) s
}

rect 0 0 w h
fill
```

</div>

## `C`, `curveto`

**`C, curveto x1 y1 x2 y2 x y`**    — [*可为隐式*](#隐式命令)

从[当前点](#当前点)向 \<x, y\> 指定的*终点*绘制三次贝塞尔曲线。*起始控制点*由 \<x1, y1\> 指定，*终止控制点*由 \<x2, y2\> 指定。

其行为与 [SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path) 中的 [`C`](#c-curveto) 命令完全相同。更多细节请参阅 [MDN 上的三次贝塞尔曲线](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d#cubic_b%C3%A9zier_curve)以及 [MDN 路径教程的曲线命令小节](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths#curve_commands)。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
moveto 20 20

curveto
    0 (h / 2)           // start control point
    w (h / 2)           // end control point
    (w - 20) (h - 20)   // end point

stroke
```

</div>

## `c`, `rcurveto`

**`c, rcurveto dx1 dy1 dx2 dy2 dx dy`**    — [*可为隐式*](#隐式命令)

与 [`curveto`](#c-curveto) 类似，但坐标相对于[当前点](#当前点)。

## `defhsla`

**`defhsla varname h s l a`**

与 [`sethsla`](#sethsla) 类似，但它不设置描边和填充操作所用的颜色，而是将计算出的颜色赋给变量 \<varname\>。

\<varname\> 之后可以用作 [`setcolor`](#setcolor) 和 [`colorstop`](#colorstop) 的颜色。

有关颜色如何计算的更多细节，请参见 [`sethsla`](#sethsla)。

## `defrgba`

**`defrgba varname r g b a`**

根据*红*、*绿*、*蓝*和 *alpha* 分量计算出一个颜色，并将其赋给变量 \<varname\>。

所有分量都是 `0` 到 `1` 之间的值。超出该范围的值会被钳制到该范围内。

## `ellipse`

**`ellipse cx cy rx ry`**    — [*可为隐式*](#隐式命令)

向当前路径添加一个椭圆。与 [`circle`](#circle) 类似，但两个轴可以使用不同的半径。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
ellipse 120 120 75 50
stroke
```

</div>

## `fill`, `eofill`

**`fill, eofill`**

使用[当前图案](#图案)（纯色或渐变）填充当前路径。

[`eofill`](#fill-eofill) 使用[奇偶规则](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS)。详见[填充规则](#填充)。

操作完成后路径会被清除，除非在 [`fill`](#fill-eofill) 或 [`eofill`](#fill-eofill) 之前使用了 [`preserve`](#preserve) 命令。

详见 [`cairo_fill`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-fill) 函数的文档，了解更多细节。

## `getmetadata`

**`getmetadata varname key`**

获取由其他滤镜创建的元数据项的值，并将其赋给变量 \<varname\>。

如果不存在 \<key\> 对应的元数据项，或其值不是数字，则 \<varname\> 被设为 [`NaN`](https://en.wikipedia.org/wiki/NaN)。

例子见上文的[帧元数据](#帧元数据)小节。

## `H`, `h`

**`H, h x`**    — [*可为隐式*](#隐式命令)

从[当前点](#当前点)向 x 绘制一条水平线。

[`H`](#h-h) 的坐标是绝对的，而 [`h`](#h-h) 的坐标相对于[当前点](#当前点)。

## `if`

**`if condition { block }`**

当 \<condition\> 的值非零且为有限数（与 [`NaN`](https://en.wikipedia.org/wiki/NaN) 不同）时，执行一个块。

如何书写条件表达式的更多细节，请参见上文的[比较与逻辑运算符](#比较与逻辑运算符)小节。

## `lineargrad`

**`lineargrad x0 y0 x1 y1`**

将[当前图案](#图案)设为一个新的线性渐变，沿从坐标 \<x0, y0\> 到 \<x1, y1\> 的直线。

此渐变可用于描边和填充操作。

使用 [`colorstop`](#colorstop) 为渐变中的每个位置设置颜色。

## `L`, `lineto`

**`L, lineto x y`**    — [*可为隐式*](#隐式命令)

从[当前点](#当前点)向 \<x, y\> 坐标绘制一条直线。

详见 [`cairo_line_to`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-line-to) 函数的文档，了解更多细节。

## `l`, `rlineto`

**`l, rlineto dx dy`**    — [*可为隐式*](#隐式命令)

与 [`lineto`](#l-lineto) 类似，但坐标相对于[当前点](#当前点)。

## `M`, `moveto`

**`M, moveto x y`**    — [*可为隐式*](#隐式命令)

开始一个新的子路径，并将[当前点](#当前点)设为 \<x, y\>。

## `m`, `rmoveto`

**`m, rmoveto dx dy`**    — [*可为隐式*](#隐式命令)

与 [`moveto`](#m-moveto) 类似，但坐标相对于[当前点](#当前点)。

## `newpath`

**`newpath`**

开始一个新的子路径。与 [`moveto`](#m-moveto) 类似，但之后没有[当前点](#当前点)。

<div class="sidebar">

<div class="title">

示例

</div>

在下一个例子中，右侧的路径使用了 [`newpath`](#newpath)，以避免连接两条弧的线段。

``` text
setlinewidth 3

setcolor skyblue
arcn 70 90 20 0 (PI)
arc 70 150 20 0 (PI)
stroke

setcolor seagreen
arcn 170 90 20 0 (PI)
newpath
arc 170 150 20 0 (PI)
stroke
```

</div>

## `preserve`

**`preserve`**

指示接下来的填充、描边或裁剪操作必须保留路径，以便同一路径可用于多个操作。

它对以下命令有效：

- [`clip`](#clip-eoclip)

- [`eoclip`](#clip-eoclip)

- [`eofill`](#fill-eofill)

- [`fill`](#fill-eofill)

- [`stroke`](#stroke)

脚本可以在 [`preserve`](#preserve) 与相关操作之间包含任意命令。这允许修改其他属性，如当前颜色。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，同一路径既用于 [`fill`](#fill-eofill) 又用于 [`stroke`](#stroke)，但颜色不同。

``` text
circle (w / 2) (h / 2) (w / 3)

setcolor skyblue
preserve fill

setlinewidth 10
setcolor seagreen
stroke
```

</div>

如果同一路径要在 3 个或更多操作中使用，[`preserve`](#preserve) 可以调用多次。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中，[`circle`](#circle) 创建的路径被 [`fill`](#fill-eofill)、[`stroke`](#stroke) 和 [`clip`](#clip-eoclip) 使用。在 [`clip`](#clip-eoclip) 之后，路径被清除。

``` text
circle 100 100 50

preserve fill
preserve stroke
clip
```

</div>

## `print`

**`print expr`**    — [*可为隐式*](#隐式命令)

将其参数打印到 FFmpeg 日志。

详见上文的 [命令 print](#命令-print) 小节，了解更多细节。

## `proc`

**`proc name params* { block }`**

为过程 \<name\> 分配块和参数。该过程可以用 [`call`](#call) 命令多次调用。

详见上文的 [过程](#过程) 小节，了解更多细节。

## `Q`

**`Q x1 y1 x y`**

从[当前点](#当前点)向 \<x, y\> 指定的*终点*绘制二次贝塞尔曲线。*控制点*由 \<x1, y1\> 指定。

其行为与 [SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path) 中的 `Q` 命令完全相同。更多细节请参阅 [MDN 上的二次贝塞尔曲线](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d#quadratic_b%C3%A9zier_curve)以及 [MDN 路径教程的曲线命令小节](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths#curve_commands)。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
moveto 20 20

Q
    0 h                 // control point
    (w - 20) (h - 20)   // end point

stroke
```

</div>

## `q`

**`q dx1 dy1 dx dy`**

与 [`Q`](#q) 类似，但坐标相对于[当前点](#当前点)。

## `radialgrad`

**`radialgrad cx0 cy0 radius0 cx1 cy1 radius1`**

创建一个径向渐变，介于由 \<cx0 cy0 radius0\> 和 \<cx1 cy1 radius1\> 定义的两个圆之间。每组参数分别是圆心坐标和半径。

此渐变可用于描边和填充操作。

使用 [`colorstop`](#colorstop) 为渐变中的每个位置设置颜色。

<div class="sidebar">

<div class="title">

示例

</div>

下一个例子中的动画展示了 [`radialgrad`](#radialgrad) 参数定义的两个圆如何相互作用。

红色圆表示 \<cx0 cy0 radius0\> 参数对应的圆，黄色圆是 \<cx1 cy1 radius1\> 参数对应的圆。

``` text
setvar cx0 (mod(t * 30, w))
setvar cy0 120
setvar radius0 20

setvar cx1 120
setvar cy1 120
setvar radius1 70

radialgrad
    cx0 cy0 radius0
    cx1 cy1 radius1

colorstop
    0 lightblue
    1 darkblue

// Fill the frame with the gradient.
rect 0 0 w h
fill

// Draw inner circle.
circle cx0 cy0 radius0
setcolor red
stroke

// Draw outer circle.
circle cx1 cy1 radius1
setcolor yellow
stroke
```

</div>

## `rect`

**`rect x y width height`**

向当前路径添加一个给定尺寸（\<width\> × \<height\>）、位于 \<x, y\> 位置的矩形。添加矩形之前和之后，[当前点](#当前点)都会被清除。

详见 [`cairo_rectangle`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-rectangle) 函数的文档，了解更多细节。

## `repeat`

**`repeat count { block }`**

按 \<count\> 指示的次数执行一个块。

在每次迭代中，变量 \<i\> 被用作[循环计数器](https://en.wikipedia.org/wiki/For_loop#Loop_counters)。它取 `0` 到 `count - 1` 的值。循环终止后，该变量恢复为循环开始前的值。

如果 \<count\> 小于 `1`，或不是有限数（如 [`NaN`](https://en.wikipedia.org/wiki/NaN)），则不会执行该块。

## `resetclip`

**`resetclip`**

将当前裁剪区域重置为其原始状态，覆盖整帧。

详见 [`cairo_reset_clip`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-reset-clip) 函数的文档，了解更多细节。

## `resetdash`

**`resetdash`**

禁用 [`stroke`](#stroke) 将使用的虚线图案。这会撤销 [`setdash`](#setdash) 和 [`setdashoffset`](#setdashoffset) 所做的任何更改。

它以 `num_dashes` 设为 `0` 调用 [`cairo_set_dash`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-dash)。

## `resetmatrix`

**`resetmatrix`**

重置当前的[变换矩阵](#变换)。

## `restore`

**`restore`**

恢复之前调用 [`save`](#save) 保存的状态。

更多细节请参见上文的[状态栈](#状态栈)小节，以及 [`cairo_restore`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-restore) 函数。

## `rotate`

**`rotate angle`**

通过将用户空间轴旋转 \<angle\> 弧度来修改当前的[变换矩阵](#变换)。

详见 [`cairo_rotate`](https://www.cairographics.org/manual/cairo-Transformations.html#cairo-rotate) 函数的文档，了解更多细节。

<div class="sidebar">

<div class="title">

示例

</div>

在这个例子中：

- [`scalexy`](#scalexy) 将坐标映射到 1x1 的帧。

- [`translate`](#translate) 把 `0, 0` 放在帧中心。

- [`rotate`](#rotate) 旋转 45°。

- [`resetmatrix`](#resetmatrix) 在 [`stroke`](#stroke) 之前撤销变换，使线宽不受缩放影响。

``` text
scalexy w h
translate 0.5 0.5
rotate (PI / 4)
rect -0.25 -0.25 0.5 0.5
resetmatrix
stroke
```

</div>

## `roundedrect`

**`roundedrect x y width height radius`**    — [*可为隐式*](#隐式命令)

与 [`rect`](#rect) 类似，但角部使用圆弧。

<div class="sidebar">

<div class="title">

示例

</div>

下一个例子展示了同一个矩形使用不同圆角半径的效果。

半径通过 \<i\>（[循环计数器](https://en.wikipedia.org/wiki/For_loop#Loop_counters)）乘以 `4.5` 计算。选择这个数字是为了让最后一个形状成为正圆。

``` text
repeat 9 {
    roundedrect
        (mod(i, 3) * 80 + 5)     // x
        (floor(i / 3) * 80 + 5)  // y
        70 70                    // size
        (i * 4.5)                // radius
}

stroke
```

</div>

## `save`

**`save`**

将当前状态的副本保存到内部栈上。之后可以用 [`restore`](#restore) 恢复该副本。

更多细节请参见上文的[状态栈](#状态栈)小节，以及 [`cairo_save`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-save) 函数。

## `scale`

**`scale sxy`**

与 [`scalexy`](#scalexy) 类似，但两个轴使用相同的值。它等价于：

**`scalexy sxy sxy`**

## `scalexy`

**`scalexy sx sy`**

通过将 X 和 Y 用户空间轴分别缩放 \<sx\> 和 \<sy\> 来修改当前的[变换矩阵](#变换)。

详见 [`cairo_scale`](https://www.cairographics.org/manual/cairo-Transformations.html#cairo-scale) 函数的文档，了解更多细节。

组合多个变换的示例见 [`rotate`](#rotate)。

## `setcolor`

**`setcolor color`**

将纯色设为描边和填充操作的[当前图案](#图案)。

详见上文的 [颜色](#颜色) 小节，了解更多细节。

## `setdash`

**`setdash length`**    — [*可为隐式*](#隐式命令)

设置 [`stroke`](#stroke) 将使用的虚线图案。

每次调用 [`setdash`](#setdash) 都会向图案添加一个长度，在描边的 on 与 off 部分之间交替。

调用 [`setdash`](#setdash) 之后，需要 [`resetdash`](#resetdash) 来创建新图案或丢弃当前图案。

详见 [`cairo_set_dash`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-dash) 函数的文档，了解更多细节。

## `setdashoffset`

**`setdashoffset offset`**

设置描边应在虚线图案中开始的位置偏移。

[`setdash`](#setdash) 必须在 [`setdashoffset`](#setdashoffset) *之前*调用。

详见 [`cairo_set_dash`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-dash) 函数的文档，了解更多细节。

<div class="sidebar">

<div class="title">

示例

</div>

下一个动画展示了 [`setdashoffset`](#setdashoffset) 的参数随时间变化时的效果。

``` text
scalexy w h
M 0.5 1
curveto 0 0.5, 1 0.5, 0.5 0
resetmatrix

setdash 20 5 // 20 on, 5 off
setdashoffset (t * 100)

setlinewidth 20
stroke
```

</div>

## `sethsla`

**`sethsla h s l a`**

根据*色相*、*饱和度*、*亮度*和 *alpha* 分量，将[当前图案](#图案)设为纯色。

h 是*色相*，取值为 `0` 到 `359`。负值被钳制为 `0`，大于 `359` 的值按模 360 解释。

s（*饱和度*）、l（*亮度*）和 a（*alpha*）是 `0` 到 `1` 之间的值。

到 RGB 的转换按照[维基百科上的公式](https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB)实现。

## `setlinecap`

**`setlinecap cap`**

设置当前线帽样式，它决定绘制线条端点所用的形状。

\<cap\> 必须是以下名称之一：

- `butt`

- `round`

- `square`

它调用 [`cairo_set_line_cap`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-line-cap) 来设置线帽样式。

<div class="sidebar">

<div class="title">

示例

</div>

这个例子绘制 3 条等长的线，每条使用不同的线帽样式：

``` text
setlinewidth 40

setlinecap butt
setcolor tomato
M 60 40 v 100 stroke

setlinecap round
setcolor seagreen
M 120 40 v 100 stroke

setlinecap square
setcolor skyblue
M 180 40 v 100 stroke

M 20 40 H 220 m 0 100 H 20
setcolor black@0.5
setlinewidth 2
stroke
```

</div>

## `setlinejoin`

**`setlinejoin join`**

设置当前线条连接样式，它决定连接两条线段所用的形状。

\<join\> 必须是以下名称之一：

- `bevel`

- `miter`

- `round`

它调用 [`cairo_set_line_join`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-line-join) 来设置线条连接样式。

<div class="sidebar">

<div class="title">

示例

</div>

这个例子绘制 3 条等长的线，每条使用不同的线条连接样式：

``` text
setlinewidth 30

setlinejoin bevel
setcolor tomato
M 70 20 l 50 50 50 -50 stroke

setlinejoin miter
setcolor seagreen
M 70 90 l 50 50 50 -50 stroke

setlinejoin round
setcolor skyblue
M 70 160 l 50 50 50 -50 stroke
```

</div>

## `setlinewidth`

**`setlinewidth width`**

设置 [`stroke`](#stroke) 的线宽。

\<width\> 受[变换矩阵](#变换)影响。

要指定不受其他变换影响的线宽，可以在 [`save`](#save) / [`restore`](#restore) 之间使用 [`resetmatrix`](#resetmatrix)：

``` text
save

resetmatrix
setlinewidth 1
stroke

// Restore matrix after stroke.
restore
```

详见 [`cairo_set_line_width`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-line-width) 函数的文档，了解更多细节。

## `setrgba`

**`setrgba r g b a`**

根据*红*、*绿*、*蓝*和 *alpha* 分量，将[当前图案](#图案)设为纯色。

所有分量都是 `0` 到 `1` 之间的值。超出该范围的值会被钳制到该范围内。

## `setvar`

**`setvar varname value`**

将变量 \<varname\> 设为 \<value\>。

详见上文的 [用户变量](#用户变量) 小节，了解更多细节。

## `stroke`

**`stroke`**

按照当前的线宽、线条连接、线帽和虚线设置描边当前路径。

操作完成后路径会被清除，除非在 [`stroke`](#stroke) 之前使用了 [`preserve`](#preserve) 命令。

详见 [`cairo_stroke`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-stroke) 函数的文档，了解更多细节。

## `S`, `s`

**`S, s x2 y2 x y`**    — [*可为隐式*](#隐式命令)

从[当前点](#当前点)向 \<x, y\> 指定的*终点*绘制平滑三次贝塞尔曲线。*终止控制点*由 \<x2, y2\> 指定。

*起始控制点*是前一条曲线命令的*终止控制点*关于*当前点*的镜像。

其行为与 [SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path) 中的 `S` 命令完全相同。更多细节请参阅 [MDN 上的三次贝塞尔曲线](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d#cubic_b%C3%A9zier_curve)以及 [MDN 路径教程的曲线命令小节](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths#curve_commands)。

[`s`](#s-s) 与 [`S`](#s-s) 类似，但坐标相对于[当前点](#当前点)。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
M 20 120

c 25 -50, 25 50, 50 0

repeat 3 {
    s 20 50, 50 0
}

stroke
```

</div>

## `translate`

**`translate tx ty`**

通过将用户空间原点平移 \<tx, ty\> 来修改当前的[变换矩阵](#变换)。

详见 [`cairo_translate`](https://www.cairographics.org/manual/cairo-Transformations.html#cairo-translate) 函数的文档，了解更多细节。

## `T`, `t`

**`T, t x y`**    — [*可为隐式*](#隐式命令)

从[当前点](#当前点)向 \<x, y\> 指定的*终点*绘制平滑二次贝塞尔曲线。

*控制点*是前一条曲线命令的*控制点*关于*当前点*的镜像。

其行为与 [SVG 的 `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path) 中的 `T` 命令完全相同。更多细节请参阅 [MDN 上的二次贝塞尔曲线](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d#quadratic_b%C3%A9zier_curve)以及 [MDN 路径教程的曲线命令小节](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths#curve_commands)。

[`t`](#t-t) 与 [`T`](#t-t) 类似，但坐标相对于[当前点](#当前点)。

<div class="sidebar">

<div class="title">

示例

</div>

``` text
M 20 120

q 10 -20, 20 0

repeat 9 {
    t 20 0
}

stroke
```

</div>

## `V`, `v`

**`V, v y`**    — [*可为隐式*](#隐式命令)

从[当前点](#当前点)向 y 绘制一条垂直线。

[`V`](#v-v) 的坐标是绝对的，而 [`v`](#v-v) 的坐标相对于[当前点](#当前点)。
