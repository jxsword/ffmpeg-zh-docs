# Introduction

drawvg (*draw vector graphics*) is a language to draw two-dimensional graphics on top of video frames. It is not intended to be used as a general-purpose language. Since its scope is limited, it prioritizes being concise and easy to use.

For example, using the [Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) we can render a triangle running this code in a Web browser:

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

The same triangle can be written with this drawvg script:

``` text
moveto 125 50
lineto 100 100 150 100
closepath
stroke
```

It can be shortened using the aliases for [`moveto`](#cmd_005fmoveto), [`lineto`](#cmd_005flineto), and [`closepath`](#cmd_005fclosepath):

``` text
M 125 50
L 100 100 150 100
Z
stroke
```

Both newlines (`U+000A`) and spaces (`U+0020`) can be used interchangeably as delimiters, so multiple commands can appear on the same line:

``` text
M 125 50 L 100 100 150 100 Z
stroke
```

Finally, drawvg can use section "FFmpeg expressions" in `ffmpeg-utils` and frame metadata in command arguments. In this example, we are using the variables \<w\> (frame width) and \<h\> (frame height) to create a circle in the middle of the frame.

``` text
circle (w / 2) (h / 2) (w / 3)
stroke
```

Many commands are a direct equivalent to a function in the [Cairo graphics library](https://www.cairographics.org/). For such commands, the reference below provides a link to the related Cairo documentation.

# Syntax

The syntax is heavily inspired by languages like [Magick Vector Graphics](https://imagemagick.org/script/magick-vector-graphics.php), or [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path). Many command names are taken from [PostScript](https://en.wikipedia.org/wiki/PostScript).

## Structure

A drawvg script consists of a series of commands to describe 2D graphics.

A command is an identifier (like [`setcolor`](#cmd_005fsetcolor) or [`lineto`](#cmd_005flineto)) followed by its arguments. Each item in the code (command name, arguments, etc.) is separated by any of the following characters:

- Space (`' '`)

- Comma (`','`)

- Newline (`'\n'`)

- Tabs (`'\t'`)

- Return (`'\r'`)

The beginning of the item indicates how it will be interpreted:

| Term                  | Description                      |
|-----------------------|----------------------------------|
| `//`                  | Comment                          |
| `0`, …, `9`, `+`, `-` | Number literal                   |
| `(`                   | Expression                       |
| `{`, `}`              | Block delimiters                 |
| Anything else         | Name of a command, a color, etc. |

## Comments

Comments start with two slashes (`//`), and stop at the end of the line (either a `\n`, or the end of the script).

``` text
circle 100 100 50 // this is ignored
fill

// this is also ignored
```

`//` must appear after a space, or at the beginning of the line. If `//` is preceded by any non-blank character, the parser will consider `//` as part of the previous item.

For example, in this script:

``` text
circle 10 10 50// something
```

The parser throws an error because it tries to parse `50//` as a number literal.

## Commands

The way commands are parsed is inspired by [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path):

- Every command in the script starts with its name, and it is followed by zero or more arguments.

- There are no explicit delimiters between commands or arguments.

  Most programming languages expect characters like parenthesis, commas, or semicolons, to separate items. For example:

  ``` c
  moveto(10, 10); lineto(20, 30);
  ```

  The equivalent in drawvg is:

  ``` text
  moveto 10 10 lineto 20 30
  ```

- If the command has no arguments (like [`closepath`](#cmd_005fclosepath) or [`stroke`](#cmd_005fstroke)), the next command starts at the next item.

<div class="sidebar">

<div class="title">

Example

</div>

In the next script there are 4 different commands:

``` text
newpath rect 10 20 30 40 setcolor teal fill
```

1.  [`newpath`](#cmd_005fnewpath) requires no arguments.

2.  [`rect`](#cmd_005frect) requires 4 arguments, so it takes the next 4 numbers.

3.  [`setcolor`](#cmd_005fsetcolor) requires 1 argument, so it takes the word `teal`.

4.  [`fill`](#cmd_005ffill) requires no arguments.

</div>

### Single-Letter Aliases

Most commands in [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path) are also present in drawvg. For some of them, there is an alias to a longer name:

- [`curveto`](#cmd_005fcurveto) for [`C`](#cmd_005fC).

- [`rcurveto`](#cmd_005frcurveto) for [`c`](#cmd_005fc).

- [`lineto`](#cmd_005flineto) for [`L`](#cmd_005fL).

- [`rlineto`](#cmd_005frlineto) for [`l`](#cmd_005fl).

- [`moveto`](#cmd_005fmoveto) for [`M`](#cmd_005fM).

- [`rmoveto`](#cmd_005frmoveto) for [`m`](#cmd_005fm).

- [`closepath`](#cmd_005fclosepath) for [`Z`](#cmd_005fZ), [`z`](#cmd_005fz).

Other commands only exist in a single-letter form:

- [`H`](#cmd_005fH), [`h`](#cmd_005fh)

- [`Q`](#cmd_005fQ), [`q`](#cmd_005fq)

- [`S`](#cmd_005fS), [`s`](#cmd_005fs)

- [`V`](#cmd_005fV), [`v`](#cmd_005fv)

- [`T`](#cmd_005fT), [`t`](#cmd_005ft)

This makes it possible to use a path in SVG to create the same shape in a drawvg script.

### Implicit Commands

For many commands, the name can be omitted when it is used multiple times in successive calls.

In the reference below, these commands has a *Can be Implicit* note in their signature.

<div class="sidebar">

<div class="title">

Example

</div>

For example, in this script:

``` text
M 50 50
l 10 10
l 10 -10
l 10 10
l 10 -10
l 10 10
stroke
```

After the first call to [`l`](#cmd_005fl) (alias to [`rlineto`](#cmd_005frlineto)), the command can be executed without the name, so it can be written as:

``` text
M 50 50
l 10 10 10 -10 10 10 10 -10 10 10
stroke
```

</div>

To reuse the same command ([`l`](#cmd_005fl), in the previous example), the parser checks if the item after the last argument is a numeric value, like a number literal or a FFmpeg expression.

<div class="sidebar">

<div class="title">

Example

</div>

In this example:

``` text
l 10 20 30 40 stroke
```

[`l`](#cmd_005fl) requires 2 arguments, and can be implicit, so the parser performs this operation:

1.  Takes the two next items (`10` and `20`) and emits the first instruction.

2.  Checks if the item after `20` is a numeric value. Since it is `30`, it takes `30` and `40` and emits the second instruction (`l 30 40`).

3.  Checks if the next item after `40` is a numeric value, but it is a command ([`stroke`](#cmd_005fstroke)), so it stops reusing [`l`](#cmd_005fl).

</div>

This is another feature taken from [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path). An important difference with SVG is that the separator between items is always required. In SVG, it can be omitted in some cases. For example, the expression `m1-2` is equivalent to `m 1 -2` in SVG, but a syntax error in drawvg.

## Arguments

Most commands expect numeric arguments, like number literals, variable names, or expressions.

[`setcolor`](#cmd_005fsetcolor) and [`colorstop`](#cmd_005fcolorstop) expect a color.

[`setlinecap`](#cmd_005fsetlinecap) and [`setlinejoin`](#cmd_005fsetlinejoin) expect a constant value.

### Number Literals

A number literal is an item in the script that represents a constant value. Any item that starts with a decimal digit (between `0` and `9`), a `-` or a `+`, is interpreted as a number literal.

The value is parsed with [`av_strtod`](https://ffmpeg.org/doxygen/trunk/eval_8c.html#a7d21905c92ee5af0bb529d2daf8cb7c3). It supports the prefix `0x` to write a value with hexadecimal digits, and [many units](https://ffmpeg.org/ffmpeg-utils.html#:~:text=The%20evaluator%20also%20recognizes%20the%20International%20System%20unit%20prefixes) (like `K` or `GiB`).

In the next example, all literals represent the same value:

``` text
10000
1e4
10K
0x2710
```

### Expressions

section "FFmpeg expressions" in `ffmpeg-utils` can be used as arguments for any command that expects a numeric argument. The expression must be enclosed in parenthesis.

<div class="sidebar">

<div class="title">

Example

</div>

The variables \<w\> and \<h\> represent the width and height of the frame. We can compute the center of the frame by dividing them by `2`:

``` text
M (w / 2) (h / 2)
```

They can also contain parenthesis (to group operations, to call functions, etc):

``` text
moveto
    ((w + 10) / 2)      // x
    (h / (2 * cos(t)))  // y
```

</div>

The variables \<n\> and \<t\> can be used to compute a value that changes over time.

<div class="sidebar">

<div class="title">

Example

</div>

To draw a circle oscillating from left to right, we can use an expression based on `sin(t)` for the `x` coordinate:

``` text
circle
    (w / 2 + sin(2 * t) * w / 4)  // x
    (h / 2)                       // y
    (w / 5)                       // radius

stroke
```

</div>

Expressions can be split in multiple lines, but they can't contain comments within them.

``` text
moveto   // This is a comment.
    (w   // This is part of the expression, not a comment.
     + h)
```

### Variable Names

When an expression is only a reference to a variable, the parenthesis can be omitted, and the item is just the variable name.

<div class="sidebar">

<div class="title">

Example

</div>

The next 3 expressions are equivalent: in all cases, they create a rectangle covering the whole frame.

``` text
rect (0) (0) (w) (h)

rect 0 0 w h

rect (0) 0 (w) h
```

</div>

It is possible to create a variable with the same name of a command, and then use it as an argument. In the previous example, the item \<h\> is a reference to a variable (frame height), but in other contexts it may be a command ([`h`](#cmd_005fh)).

For [implicit commands](#implicit-commands), the parser prioritizes commands over variable names when it has to determine if the command is reused.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, the variable \<c\> is used as the first argument in two calls to [`l`](#cmd_005fl). However, only the first one is valid, because in the second call the parser recognizes [`c`](#cmd_005fc) as a command.

``` text
setvar c 5
l c 10 c 15
```

This issue can be fixed by surrounding the start of the second call with parenthesis:

``` text
setvar c 5
l c 10 (c) 15
```

</div>

### Colors

The color to stroke and to fill paths can be set with [`setcolor`](#cmd_005fsetcolor). Its argument has the same syntax for colors in FFmpeg:

- A section "predefined color name" in `ffmpeg-utils`.

- In `#RRGGBB` format.

- Optionally, an `@a` suffix can be added to set the alpha value, where `a` is a number between `0` and `1`.

``` text
circle 70 70 60
setcolor #FF0000
fill

circle 170 170 60
setcolor blue@0.5
fill
```

The color can be a variable name. In that case, it must be assigned with [`defrgba`](#cmd_005fdefrgba), [`defhsla`](#cmd_005fdefhsla), or [`setvar`](#cmd_005fsetvar) and a color.

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

The commands [`setrgba`](#cmd_005fsetrgba) and [`sethsla`](#cmd_005fsethsla) allow setting colors using expressions. Similar to [`defrgba`](#cmd_005fdefrgba) and [`defhsla`](#cmd_005fdefhsla), but with no intermediate variable.

### Constants

The argument for [`setlinecap`](#cmd_005fsetlinecap) and [`setlinejoin`](#cmd_005fsetlinejoin) is an identifier referring to a constant value.

``` text
setlinecap round
```

# Guide

## Paths

A path is a complex shape, composed by lines and curves, that can be used to fill a region, to stroke an outline, or to establish a clip region.

In order to draw anything on top of a video frame, first we have to define a path, and then use [`stroke`](#cmd_005fstroke) or [`fill`](#cmd_005ffill).

The [tutorial on paths in MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths) is a good introduction to the topic. It is focused on [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path), but the same concepts can be applied in drawvg.

### Current Point

Some commands require a *current point*. Initially, the *current point* is set to [`NaN`](https://en.wikipedia.org/wiki/NaN). It is initialized with [`M`](#cmd_005fM) or [`moveto`](#cmd_005fmoveto). Other commands, like [`lineto`](#cmd_005flineto) or [`curveto`](#cmd_005fcurveto), updates the *current point* to the new end of the shape.

The *current point* can be cleared with [`newpath`](#cmd_005fnewpath). Commands that clear the path, like [`stroke`](#cmd_005fstroke) or [`fill`](#cmd_005ffill), also clear the *current point*.

<div class="sidebar">

<div class="title">

Example

</div>

[`rlineto`](#cmd_005frlineto) uses coordinates relative to the *current point*.

Given this script:

``` text
moveto 20 100
rlineto 150 -90
rlineto -50 200
closepath
stroke
```

These are the coordinates of the *current point* after executing each command:

| Command           | Current Point |
|-------------------|---------------|
| `moveto 20 100`   | `20, 100`     |
| `rlineto 150 -90` | `170, 10`     |
| `rlineto -10 50`  | `140, 210`    |
| `closepath`       | `20, 100`     |

The same script can be written with single-letter aliases:

``` text
M 20 100 l 150 -90 -50 200 z stroke
```

</div>

### Defining a Shape

A path is defined by adding lines, curves, or basic shapes.

- Basic shapes

  - [`circle`](#cmd_005fcircle)

  - [`ellipse`](#cmd_005fellipse)

  - [`rect`](#cmd_005frect)

  - [`roundedrect`](#cmd_005froundedrect)

- Lines

  - [`M`](#cmd_005fM), [`moveto`](#cmd_005fmoveto)

  - [`m`](#cmd_005fm), [`rmoveto`](#cmd_005frmoveto)

  - [`H`](#cmd_005fH), [`h`](#cmd_005fh)

  - [`V`](#cmd_005fV), [`v`](#cmd_005fv)

  - [`L`](#cmd_005fL), [`lineto`](#cmd_005flineto)

  - [`l`](#cmd_005fl), [`rlineto`](#cmd_005frlineto)

  - [`Z`](#cmd_005fZ), [`z`](#cmd_005fz), [`closepath`](#cmd_005fclosepath)

- Curves

  - [`arc`](#cmd_005farc), [`arcn`](#cmd_005farcn)

  - [`C`](#cmd_005fC), [`curveto`](#cmd_005fcurveto),

  - [`c`](#cmd_005fc), [`rcurveto`](#cmd_005frcurveto)

  - [`Q`](#cmd_005fQ), [`q`](#cmd_005fq)

  - [`S`](#cmd_005fS), [`s`](#cmd_005fs)

  - [`T`](#cmd_005fT), [`t`](#cmd_005ft)

Single-letter commands are taken from [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path).

### Fill

The region within the shape defined by a path can be filled with [`fill`](#cmd_005ffill) or [`eofill`](#cmd_005feofill). Each command uses a different [fill rule](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-fill-rule-t):

- [`fill`](#cmd_005ffill) uses the [winding rule](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-WINDING:CAPS), also known as [nonzero rule](https://en.wikipedia.org/wiki/Nonzero-rule).

- [`eofill`](#cmd_005feofill) uses the [even–odd rule](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS).

<div class="sidebar">

<div class="title">

Example

</div>

This script shows the difference between the [winding](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-WINDING:CAPS) and [even–odd](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS) rules:

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

### Stroke

[`stroke`](#cmd_005fstroke) draws a line around the shape defined by the path. The stroke can be configured with different commands:

- [`setdash`](#cmd_005fsetdash)

- [`setdashoffset`](#cmd_005fsetdashoffset)

- [`setlinecap`](#cmd_005fsetlinecap)

- [`setlinejoin`](#cmd_005fsetlinejoin)

- [`setlinewidth`](#cmd_005fsetlinewidth)

- [`resetdash`](#cmd_005fresetdash)

<div class="sidebar">

<div class="title">

Example

</div>

This example use [`setdashoffset`](#cmd_005fsetdashoffset) to animate the stroke:

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

### Clip

A [clip region](https://en.wikipedia.org/wiki/Clipping_(computer_graphics)) can be established with [`clip`](#cmd_005fclip) and [`eoclip`](#cmd_005feoclip).

If there is an active clip region, the new clip region will be the intersection between the existing one and the path. [`resetclip`](#cmd_005fresetclip) reset the clip region to the whole frame.

[`eoclip`](#cmd_005feoclip) uses the [even–odd rule](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS) to compute the clip region.

<div class="sidebar">

<div class="title">

Example

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

### Preserving Paths

The path is cleared after any operation on it, like [`fill`](#cmd_005ffill) or [`stroke`](#cmd_005fstroke). To reuse the same path in multiple operations, [`preserve`](#cmd_005fpreserve) must be called before them.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, each path is used twice.

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

## Variables

A drawvg can use some variables, provided by the interpreter, to compute values in section "FFmpeg expressions" in `ffmpeg-utils`:

- **\<cx\>** X coordinate of the [current point](#current-point).

- **\<cy\>** Y coordinate of the [current point](#current-point).

- **\<w\>** Width, in pixels, of the frame.

- **\<h\>** Height, in pixels, of the frame.

- **\<i\>** The loop counter in repeat blocks.

- **\<n\>** Frame number.

- **\<t\>** Timestamp, in seconds.

- **\<ts\>** Timestamp, in seconds, of the first frame.

- **\<duration\>** Duration, in seconds, of the frame.

### User Variables

New variables can be created with the [`setvar`](#cmd_005fsetvar) command. It associates a name with a numeric value.

The name must follow these rules:

- It must start with an ASCII letter or an underscore (`_`).

- It can contain only ASCII letters, underscores, and digits.

- It must not match the name of a variable provided by the interpreter (like \<w\> or \<t\>).

The same variable can be assigned multiple times.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, the result of an expression is stored in a variable with the name \<progress\>. Then, it is used for the \<x\> and \<width\> arguments of [`rect`](#cmd_005frect).

``` text
setvar progress (w * (pow(mod(t / 2 + 0.5, 1), 2.5)))

rect ((w - progress) / 2) 0 progress h

setcolor darkblue
fill
```

</div>

Currently, a script can contain only 20 different variable names, but this limit can be modified in the future.

## Patterns

The pattern for fill and stroke operations can be either a solid color, or a gradient.

- Solid colors.

  - [`setcolor`](#cmd_005fsetcolor)

  - [`sethsla`](#cmd_005fsethsla)

  - [`setrgba`](#cmd_005fsetrgba)

- Gradients.

  - [`lineargrad`](#cmd_005flineargrad)

  - [`radialgrad`](#cmd_005fradialgrad)

The pattern is not cleared after being used in a fill or stroke operation, but it is replaced by any command that sets a new pattern.

### Gradients

To configure a gradient, first call to [`lineargrad`](#cmd_005flineargrad) or [`radialgrad`](#cmd_005fradialgrad), and then add color stops by calling [`colorstop`](#cmd_005fcolorstop) for each stop.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, the whole frame is filled with a linear gradient:

``` text
lineargrad 0 0 w h
colorstop 0 skyblue
colorstop 1 darkblue

rect 0 0 w h
fill
```

In this example, a radial gradient is used to simulate a sphere:

``` text
radialgrad 90 90 5 120 120 100
colorstop 0.0 #90DDFF
colorstop 0.9 #000030
colorstop 1.0 #000000

rect 0 0 w h
fill
```

</div>

### Variables

[`setcolor`](#cmd_005fsetcolor) and [`colorstop`](#cmd_005fcolorstop) accept a variable name as the argument. The variable must be assigned with [`defrgba`](#cmd_005fdefrgba), [`defhsla`](#cmd_005fdefhsla), or [`setvar`](#cmd_005fsetvar) and a color.

<div class="sidebar">

<div class="title">

Example

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

If a variable has the same name of a section "known color" in `ffmpeg-utils`, the variable has preference, and will be used instead of the predefined color.

<div class="sidebar">

<div class="title">

Example

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

[`defrgba`](#cmd_005fdefrgba) and [`defhsla`](#cmd_005fdefhsla) assign a color to a variable, by providing an expression for each color component:

- For [`defrgba`](#cmd_005fdefrgba): *red*, *green*, *blue*, and *alpha*.

- For [`defhsla`](#cmd_005fdefhsla): *hue*, *saturation*, *lightness*, and *alpha*.

Each color component must be in range `0` to `1`, except *hue*, which is `0` to `360`.

<div class="sidebar">

<div class="title">

Example

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

## Transformations

The coordinates for each command can be scaled, rotated, and translated, by using the following commands:

- [`rotate`](#cmd_005frotate)

- [`scale`](#cmd_005fscale)

- [`scalexy`](#cmd_005fscalexy)

- [`translate`](#cmd_005ftranslate)

The transformations are applied when the command is executed. They have no effect on the existing path, only on the new segments added to it.

They are done by updating the [current transformation matrix](https://www.cairographics.org/manual/cairo-Transformations.html) in the Cairo context. To reset the matrix to its original state, before any transformation, use [`resetmatrix`](#cmd_005fresetmatrix).

The transform origin for scale and rotation is initially at `0, 0`, but it can be adjusted with [`translate`](#cmd_005ftranslate).

<div class="sidebar">

<div class="title">

Example

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

## State Stack

The state of a drawvg script contains all parameters used for drawing operations, like the current color, the transformation matrix, the stroke configuration, etc.

The [`save`](#cmd_005fsave) command pushes a snapshot of the state to an internal stack. Later, [`restore`](#cmd_005frestore) pops the latest snapshot from the stack, and uses it as the new state.

The parameters that can be saved and restored are:

- Pattern for stroke and fill operations.

  - [`lineargrad`](#cmd_005flineargrad)

  - [`radialgrad`](#cmd_005fradialgrad)

  - [`setrgba`](#cmd_005fsetrgba)

  - [`setcolor`](#cmd_005fsetcolor)

  - [`sethsla`](#cmd_005fsethsla)

- Transformation matrix.

  - [`resetmatrix`](#cmd_005fresetmatrix)

  - [`rotate`](#cmd_005frotate)

  - [`scale`](#cmd_005fscale)

  - [`scalexy`](#cmd_005fscalexy)

  - [`translate`](#cmd_005ftranslate)

- Stroke configuration.

  - [`setdash`](#cmd_005fsetdash)

  - [`setdashoffset`](#cmd_005fsetdashoffset)

  - [`setlinecap`](#cmd_005fsetlinecap)

  - [`setlinejoin`](#cmd_005fsetlinejoin)

  - [`setlinewidth`](#cmd_005fsetlinewidth)

- Clip region

  - [`clip`](#cmd_005fclip)

  - [`resetclip`](#cmd_005fresetclip)

## Frame Metadata

Some FFmpeg filters add metadata to frames. The command [`getmetadata`](#cmd_005fgetmetadata) can read metadata items containing a numeric value, and store it in a variable that can be used for command arguments.

<div class="sidebar">

<div class="title">

Example

</div>

The `cropdetect` filter computes the parameters to remove empty regions around the video. These parameters are accessible in the `lavfi.cropdetect` keys of the frame metadata.

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

To test the script, copy it to a `drawcropdetect.vgs` file, and then execute a command like this:

``` text
ffplay -i example-video.webm -vf 'cropdetect, drawvg=file=drawcropdetect.vgs'
```

</div>

## `if` / `repeat` Statements

There is limited support for control flow statements: only [`if`](#cmd_005fif) and [`repeat`](#cmd_005frepeat).

Both commands receive two arguments: an expression and a block.

``` text
if (condition) {
    // commands
}

repeat (count) {
    // commands
}
```

[`if`](#cmd_005fif) executes its block if the result of `(condition)` is not zero.

[`repeat`](#cmd_005frepeat) executes its block the number of times specified by `(count)`. In each iteration, the variable \<i\> is used as a [loop counter](https://en.wikipedia.org/wiki/For_loop#Loop_counters).

If the result of the expression is not a finite number (like [`NaN`](https://en.wikipedia.org/wiki/NaN)) the block is not executed.

### Comparison and Logical Operators

section "FFmpeg expressions" in `ffmpeg-utils` only supports arithmetic operators (like `+` for addition). Comparison operators (like `!=`) are supported via functions, while logical operators (like `&&` for `AND`) can be emulated with arithmetic operations.

| Expression  | FFmpeg Equivalent  |
|-------------|--------------------|
| `x = y`     | `eq(x, y)`         |
| `x < y`     | `lt(x, y)`         |
| `x > y`     | `gt(x, y)`         |
| `x ≤ y`     | `lte(x, y)`        |
| `x ≥ y`     | `gte(x, y)`        |
| `a ≤ x ≤ b` | `between(x, a, b)` |

Logical operators can be emulated with multiplication (for `AND`), or addition (for `OR`):

| Expression | FFmpeg Equivalent |
|------------|-------------------|
| `x OR y`   | `x + y`           |
| `x AND y`  | `x * y`           |

<div class="sidebar">

<div class="title">

Example

</div>

In other programming languages, a code like this:

``` text
if (x > y && z != 1) {
    // …
}
```

Can be written for drawvg like this:

``` text
if (gt(x, y) * not(eq(z, 1))) {
    // …
}
```

</div>

### Early Exit

[`break`](#cmd_005fbreak) causes a [`repeat`](#cmd_005frepeat) loop to be terminated immediately.

If it is executed outside a [`repeat`](#cmd_005frepeat) block, it terminates the whole script, or the current procedure.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, we are using the [`randomg`](#func_002drandomg) function to draw a line with random segments.

The loop can be executed `500` times, but it is interrupted if the X coordinate of the [current point](#current-point) (\<cx\>) exceeds the frame width (\<w\>). The [current point](#current-point) is updated after each call to [`rlineto`](#cmd_005frlineto).

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

## Procedures

A procedure is a name associated with a block that can be executed multiple times. It can take between 0 and 6 parameters.

[`proc`](#cmd_005fproc) is used to set the parameter names and the block for a procedure:

``` text
proc p0 {
    // …
}

proc p1 param1 param2 {
    // …
}
```

Inside the block, the arguments can be accessed as regular variables:

``` text
proc square center_x center_y side {
    rect
        (center_x - side / 2) (center_y - side / 2)
        side side
}
```

[`call`](#cmd_005fcall) executes the block assigned to the procedure name. It requires the name of the procedure, and the value for each parameter defined in the call to [`proc`](#cmd_005fproc).

``` text
call p0

call p1 1 2

call square (w / 2) (h / 2) (w / t)
```

<div class="sidebar">

<div class="title">

Example

</div>

In this example, the procedure `zigzag` draws multiple lines from the [current point](#current-point).

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

The color and the Y coordinate of the starting point can be sent as procedure arguments:

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

When the procedure returns, the value of the variable for each argument is restored to the value it had before calling the procedure. Changes in other variables (with [`setvar`](#cmd_005fsetvar), [`getmetadata`](#cmd_005fgetmetadata), [`defhsla`](#cmd_005fdefhsla), and [`defrgba`](#cmd_005fdefrgba)) are preserved.

<div class="sidebar">

<div class="title">

Example

</div>

In the next example, the variable \<A\> has the value `0` before calling the procedure \<P\>. During the execution of \<P\>, `A` is `1`, but after it, \<A\> is `0` again.

``` text
setvar A 0

proc P A {
    print A
}

print A
call P 1
print A
```

It writes the following messages:

``` text
[7:7] A = 0.000
[4:8] A = 1.000
[9:7] A = 0.000
```

</div>

[`break`](#cmd_005fbreak) causes the script to leave the current procedure, similar to the [`return` statement](https://en.wikipedia.org/wiki/Return_statement) in other programming languages, unless it is called within a [`repeat`](#cmd_005frepeat) loop.

The body of the procedure must be defined with [`proc`](#cmd_005fproc) *before* using [`call`](#cmd_005fcall).

<div class="sidebar">

<div class="title">

Example

</div>

In this example, when the procedure `notyet` is called, its body has not yet defined, so the execution fails with the error `Missing body for procedure 'notyet'`.

``` text
call notyet

proc notyet {
    // ...
}
```

</div>

A procedure can be redefined by other calls to [`proc`](#cmd_005fproc) with the same name. In such case, [`call`](#cmd_005fcall) invokes the last assigned block.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, the procedure `example` has two different blocks.

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

## Functions in Expressions

There are some functions specific to drawvg available in section "FFmpeg expressions" in `ffmpeg-utils`.

### Function `p`

`p(x, y)` returns the color of the pixel at coordinates `x, y`, as a `0xRRGGBBAA` value. It can be assigned to a variable, so the color can be available for [`setcolor`](#cmd_005fsetcolor) and [`colorstop`](#cmd_005fcolorstop) commands.

If a single expression contains multiple calls to the function, it must return the value of the last call in order to use it as a color.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, the first call to `p(0, 0)` is stored in the variable \<0\> of the expression. Then, the same expression makes a second call to `p(1, 1)`, and finally it returns the value in the variable \<0\>.

``` c
setvar pixel (st(0, p(0, 0)); p(1, 1); ld(0))
```

Since the result of the expression is not the last call to `p`, the variable \<pixel\> can not be used as a color, but it still can be used as a numeric `0xRRGGBBAA` value.

</div>

If the coordinates are outside the frame, or any of the arguments is not a finite number (like [`NaN`](https://en.wikipedia.org/wiki/NaN)), the function returns `NaN`.

The [transformation matrix](#transformation-matrix) is applied to the arguments. To use the original frame coordinates, call [`resetmatrix`](#cmd_005fresetmatrix) between [`save`](#cmd_005fsave) and [`restore`](#cmd_005frestore):

``` text
save
resetmatrix
setvar pixel (p(0, 0))    // top-left pixel of the frame.
restore

setcolor pixel
```

Bitwise operations can be used to extract individual color components:

``` text
setvar pixel (p(x, y))

if (not(isnan(pixel))) {
    setvar px_red   (pixel / 0x1000000)
    setvar px_green (bitand(pixel / 0x10000, 0xFF))
    setvar px_blue  (bitand(pixel / 0x100, 0xFF))
    setvar px_alpha (bitand(pixel, 0xFF))
}
```

### Function `pathlen`

`pathlen(n)` computes the length of the current path, by adding the length of each line segment returned by [`cairo_copy_path_flat`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-copy-path-flat).

The function expects an argument \<n\>, as the maximum number of line segments to add to the length, or `0` to add all segments.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, `pathlen` is used to animate the stroke of a spiral, in a 5 seconds loop.

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

### Function `randomg`

`randomg(idx)` is similar to the `random(idx)` function, available in section "FFmpeg expressions" in `ffmpeg-utils`, but its state is global to the frame, instead of specific to each expression.

To understand the difference, we need to dive into how `random(idx)` works inside a drawvg script.

First, each expression in FFmpeg has a set of 10 internal variables, which can be written with `st(idx, value)`, and can be read with `ld(idx)`. \<idx\> is a value between `0` and `9`. These variables are initialized to `0`.

When a drawvg script is parsed, each expression is compiled with [`av_expr_parse`](https://ffmpeg.org/doxygen/8.0/eval_8h.html#ad3bf8f3330d1fd139de2ca156c313f34), from [libavutil](https://ffmpeg.org/libavutil.html), and these compiled expressions are reused for every frame. The changes in the internal variables (with `st(idx, value)`) are visible between frames, but they are not shared between expressions.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, the expression for the X coordinate updates its internal variable `0` in every frame:

``` text
circle
    (st(0, mod(ld(0) + 15, w))) // X
    120                         // Y
    (ld(0) + 20)                // radius

fill
```

`st(idx, value)` returns the updated value, so it can be used as the result of the expression.

The radius is not affected because its internal variable (from `ld(0)`) is not updated by the other expression.

Also, note that this example is just to show how internal variables are kept between frames. A better approach to create this animation is to use the variables n or t:

``` text
circle (mod(n * 15, w)) 120 20
fill
```

</div>

The function `random(idx)` returns a [pseudorandom](https://en.wikipedia.org/wiki/Pseudorandom_number_generator) value between `0` and `1`. \<idx\> is the internal variable that is used both as the seed and to keep the state of the number generator.

<div class="sidebar">

<div class="title">

Example

</div>

The next example uses `random(0)` to generate a random value for the center of a circle:

``` text
circle
    (random(0) * w)
    (random(0) * h)
    10

fill
```

The circle in every frame is at a different position, but always on the diagonal line of the frame. This happens because the values for the coordinates X and Y are identical, since both number generators use the same seed.

To distribute the circles over the whole frame we need different seeds for each expression. This can be achieved by writing a non-zero value (like `0xF0F0`) to the internal variable of one of expressions, but only when its value is `0`:

``` c
circle
    (random(0) * w)
    (st(0, if(ld(0), ld(0), 0xF0F0)); random(0) * h)
    10

fill
```

This approach is only useful if we need completely different positions in each frame. In the next example, random values are used to distribute many circles over the frame, but the position is fixed. The only change over time is the fill color:

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

This is achieved by using a precomputed state before calling `random(0)`. The variable \<i\>, updated by [`repeat`](#cmd_005frepeat), is needed to compute different states in each iteration.

</div>

The `randomg(idx)` function, which is specific to drawvg scripts, is similar to `random(idx)`, but intended to solve the previous problems:

- All frames have the same seed.

- The state is shared between expressions.

The parameter \<idx\> has two uses:

- The last two bits are the index of an internal state, so it is possible to have 4 different number generators.

- The first call to `randomg` with a specific index will use the argument as the seed for the number generator in that index.

In a script like this:

``` text
M (randomg(0xFF1)) (randomg(0xFF0))
l (randomg(0xAA1)) (randomg(0xFF0))
```

There are 4 calls to `randomg`:

1.  The first call, with the argument `0xFF1`, uses the internal state at index `1` (because `0xFF1` modulo `4` is `1`).

    Since this is the first use of that index, the number generator is initialized with the seed `0xFF1`.

2.  The second call has the same behaviour: it initializes the state at index `0` with the value `0xFF0`.

3.  The third call has the argument `0xAA1`, and it uses index `1`. Since that state is already initialized (with the seed `0xFF1`), the value `0xAA1` is ignored, and it returns the next number.

<div class="sidebar">

<div class="title">

Example

</div>

This example renders a simple rain animation, moving lines from top to bottom.

`randomg` is used to distribute the lines over the frame, and to apply different speeds to each one.

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

## Tracing with `print`

It is possible to trace the execution of a drawvg script by printing the value of an expression, either with the [`print`](#cmd_005fprint) command, or with the print function.

In both cases, the values are written to the FFmpeg log.

Printing expressions may have a noticeable impact on the performance, so it is preferable to use it only when necessary.

### Function print

The function `print(t)` writes the value of t, and returns its argument.

<div class="sidebar">

<div class="title">

Example

</div>

Given a line line this:

``` text
M (sin(2 * PI * t) * w) 0
```

We can see the values of `sin(2 * PI * t)` by surrounding it with a call to `print()`:

``` text
M (print(sin(2 * PI * t)) * w) 0
```

Executing this script with a 1 second / 8 FPS video shows the expected values for the sine function.

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

### Command `print`

The command [`print`](#cmd_005fprint) accepts an arbitrary number of arguments, and for each one it writes:

- The source location (line and column).

- The source code of the expression.

- The result of evaluating the expression.

When there are multiple expressions, they are separated by the `|` character.

<div class="sidebar">

<div class="title">

Example

</div>

The next script prints the position of the [current point](#current-point) after the [`l`](#cmd_005fl) command:

``` text
M 10 20
l 100 100
print cx cy
stroke
```

For each frame, it produces this output:

``` text
[3:7] cx = 110.000000 | [3:10] cy = 120.000000
```

The next example prints the values of `random(0)`:

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

# Commands

## `arc`

**`arc xc yc radius angle1 angle2`**    — [*Can be implicit*](#implicit-commands)

Adds a circular arc of the given \<radius\> to the current path. The arc is centered at \<xc, yc\>, begins at \<angle1\> and proceeds in the direction of increasing angles to end at \<angle2\>.

If there is a [current point](#current-point), a line is added from it to the beginning of the arc. If this is not desired, use [`newpath`](#cmd_005fnewpath) before [`arc`](#cmd_005farc) to clear the [current point](#current-point).

See the documentation of the [`cairo_arc`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-arc) function for more details.

<div class="sidebar">

<div class="title">

Example

</div>

``` text
arc 120 120 60 0 (3 * PI / 2)
stroke
```

</div>

## `arcn`

**`arcn xc yc radius angle1 angle2`**    — [*Can be implicit*](#implicit-commands)

Similar to [`arc`](#cmd_005farc), but it differs in the direction of the arc between the two angles.

See the documentation of the [`cairo_arc_negative`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-arc-negative) function for more details.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, both [`arc`](#cmd_005farc) and [`arcn`](#cmd_005farcn) have the same angles, but they render different arcs:

``` text
arc  120  90 60 (PI / 2) 0

newpath
arcn 120 150 60 (PI / 2) 0

stroke
```

</div>

[`newpath`](#cmd_005fnewpath) is needed to prevent a line between the two arcs.

## `break`

**`break`**

[`break`](#cmd_005fbreak) terminates the execution of the innermost block, either a [`repeat`](#cmd_005frepeat) loop or a procedure.

If it is used outside of a [`repeat`](#cmd_005frepeat) / [`proc`](#cmd_005fproc) block, it terminates the script for the current frame.

## `call`

**`call name args*`**

Invokes a procedure defined by [`proc`](#cmd_005fproc).

See the [Procedures](#Procedures) section above for more details.

## `circle`

**`circle xc yc radius`**    — [*Can be implicit*](#implicit-commands)

Adds a circle of the given \<radius\> to the current path. The circle is centered at \<xc, yc\>. The [current point](#current-point) is cleared before and after adding the circle.

This is a convenience wrapper for [`arc`](#cmd_005farc). A call to [`circle`](#cmd_005fcircle) is equivalent to:

``` text
newpath
arc xc yc radius (0) (2 * PI)
newpath
```

## `clip`, `eoclip`

**`clip, eoclip`**

Establishes a new clip region by intersecting the current clip region with the current path as it would be filled by [`fill`](#cmd_005ffill) or [`eofill`](#cmd_005feofill).

[`eoclip`](#cmd_005feoclip) uses the [even–odd rule](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS). See [fill rules](#fill-rules) for more details.

The path is cleared after updating the clip region, unless the [`preserve`](#cmd_005fpreserve) command is used before [`clip`](#cmd_005fclip) or [`eoclip`](#cmd_005feoclip).

See the documentation of the [`cairo_clip`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-clip) function for more details.

## `Z`, `z`, `closepath`

**`Z, z, closepath`**

Adds a line segment to the path from the [current point](#current-point) to the beginning of the current sub-path, and closes this sub-path. The beginning is set by any of the *move* commands ([`M`](#cmd_005fM), [`m`](#cmd_005fm), [`moveto`](#cmd_005fmoveto), [`rmoveto`](#cmd_005frmoveto)).

See the documentation of the [`cairo_close_path`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-close-path) function for more details.

## `colorstop`

**`colorstop offset color`**    — [*Can be implicit*](#implicit-commands)

Adds a color stop to a gradient pattern.

\<offset\> is a value between `0` and `1`, and it specifies the location along the gradient's control vector.

This command must be executed after [`lineargrad`](#cmd_005flineargrad) or [`radialgrad`](#cmd_005fradialgrad).

Color stops can be added in any number of calls to [`colorstop`](#cmd_005fcolorstop). In the next example, the 3 blocks define the same gradient:

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

See the documentation of the [`cairo_pattern_add_color_stop_rgba`](https://www.cairographics.org/manual/cairo-cairo-pattern-t.html#cairo-pattern-add-color-stop-rgba) function for more details.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, color stops are added in a [`repeat`](#cmd_005frepeat) loop.

``` text
lineargrad 0 0 w h

repeat 6 {
    defhsla s (i * 60) 0.8 0.5 1
    colorstop (i / 5) s
}

rect 0 0 w h
fill
```

It is possible to avoid transitions between color stops by repeating the same color in two stops:

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

**`C, curveto x1 y1 x2 y2 x y`**    — [*Can be implicit*](#implicit-commands)

Draw a cubic Bézier curve from the [current point](#current-point) to the *end point* specified by \<x, y\>. The *start control point* is specified by \<x1, y1\> and the *end control point* is specified by \<x2, y2\>.

The behaviour is identical to the [`C`](#cmd_005fC) command in [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path). For more details, see [Cubic Bézier Curve on MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d#cubic_b%C3%A9zier_curve), and the [Curve Commands section of the Paths tutorial on MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths#curve_commands).

<div class="sidebar">

<div class="title">

Example

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

**`c, rcurveto dx1 dy1 dx2 dy2 dx dy`**    — [*Can be implicit*](#implicit-commands)

Like [`curveto`](#cmd_005fcurveto), but the coordinates are relative to the [current point](#current-point).

## `defhsla`

**`defhsla varname h s l a`**

Similar to [`sethsla`](#cmd_005fsethsla), but instead of establishing the color for stroke and fill operations, the computed color is assigned to the variable \<varname\>.

\<varname\> can then be used as a color for [`setcolor`](#cmd_005fsetcolor) and [`colorstop`](#cmd_005fcolorstop).

See [`sethsla`](#cmd_005fsethsla) for more details on how the color is computed.

## `defrgba`

**`defrgba varname r g b a`**

Computes a color from the *red*, *green*, *blue*, and *alpha* components, and assigns it to the variable \<varname\>.

All components are values between `0` and `1`. Values outside that range are clamped to it.

## `ellipse`

**`ellipse cx cy rx ry`**    — [*Can be implicit*](#implicit-commands)

Adds an ellipse to the current path. Similar to [`circle`](#cmd_005fcircle), but it is possible to use different radius for both axes.

<div class="sidebar">

<div class="title">

Example

</div>

``` text
ellipse 120 120 75 50
stroke
```

</div>

## `fill`, `eofill`

**`fill, eofill`**

Fill the current path, using the [current pattern](#current-pattern) (either a solid color or a gradient).

[`eofill`](#cmd_005feofill) uses the [even–odd rule](https://www.cairographics.org/manual/cairo-cairo-t.html#CAIRO-FILL-RULE-EVEN-ODD:CAPS). See [fill rules](#fill-rules) for more details.

The path is cleared after the operation, unless the [`preserve`](#cmd_005fpreserve) command is used before [`fill`](#cmd_005ffill) or [`eofill`](#cmd_005feofill).

See the documentation of the [`cairo_fill`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-fill) function for more details.

## `getmetadata`

**`getmetadata varname key`**

Get the value of a metadata entry created by another filter, and assign it to the variable \<varname\>.

If there is no metadata entry for \<key\>, or its value is not a number, \<varname\> is set to [`NaN`](https://en.wikipedia.org/wiki/NaN).

See the [Frame Metadata](#Frame-Metadata) section above for an example.

## `H`, `h`

**`H, h x`**    — [*Can be implicit*](#implicit-commands)

Draw a horizontal line from the [current point](#current-point) to x.

The coordinate for [`H`](#cmd_005fH) is absolute, and for [`h`](#cmd_005fh) it is relative to the [current point](#current-point).

## `if`

**`if condition { block }`**

Executes a block if the value of \<condition\> is not zero, and a finite number (unlike [`NaN`](https://en.wikipedia.org/wiki/NaN)).

See the [Comparison and Logical Operators](#comp_002doperators) section above for more details on how to write conditional expressions.

## `lineargrad`

**`lineargrad x0 y0 x1 y1`**

Set the [current pattern](#current-pattern) to a new linear gradient, along the line from the coordinates \<x0, y0\> to \<x1, y1\>.

This gradient can be used for stroke and fill operations.

Use [`colorstop`](#cmd_005fcolorstop) to set the color for each position in the gradient.

## `L`, `lineto`

**`L, lineto x y`**    — [*Can be implicit*](#implicit-commands)

Draw a line from the [current point](#current-point) to the coordinates at \<x, y\>.

See the documentation of the [`cairo_line_to`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-line-to) function for more details.

## `l`, `rlineto`

**`l, rlineto dx dy`**    — [*Can be implicit*](#implicit-commands)

Like [`lineto`](#cmd_005flineto), but the coordinates are relative to the [current point](#current-point).

## `M`, `moveto`

**`M, moveto x y`**    — [*Can be implicit*](#implicit-commands)

Begin a new sub-path, and set the [current point](#current-point) to \<x, y\>.

## `m`, `rmoveto`

**`m, rmoveto dx dy`**    — [*Can be implicit*](#implicit-commands)

Like [`moveto`](#cmd_005fmoveto), but the coordinates are relative to the [current point](#current-point).

## `newpath`

**`newpath`**

Begin a new sub-path. Like [`moveto`](#cmd_005fmoveto), but there is no [current point](#current-point) after it.

<div class="sidebar">

<div class="title">

Example

</div>

In the next example, [`newpath`](#cmd_005fnewpath) is used in the path on the right to prevent the line connecting both arcs.

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

Indicates that the next operation to fill, stroke, or clip, must preserve the path, so the same path can be used in multiple operations.

It has effect on these commands:

- [`clip`](#cmd_005fclip)

- [`eoclip`](#cmd_005feoclip)

- [`eofill`](#cmd_005feofill)

- [`fill`](#cmd_005ffill)

- [`stroke`](#cmd_005fstroke)

The script can contain any command between [`preserve`](#cmd_005fpreserve) and the associated operation. This allows modifying other properties, like the current color.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, the same path is used for both [`fill`](#cmd_005ffill) and [`stroke`](#cmd_005fstroke), but with different colors.

``` text
circle (w / 2) (h / 2) (w / 3)

setcolor skyblue
preserve fill

setlinewidth 10
setcolor seagreen
stroke
```

</div>

[`preserve`](#cmd_005fpreserve) can be called multiple times, if the same path has to be used in 3 or more operations.

<div class="sidebar">

<div class="title">

Example

</div>

In this example, the path created by [`circle`](#cmd_005fcircle) is used by [`fill`](#cmd_005ffill), [`stroke`](#cmd_005fstroke), and [`clip`](#cmd_005fclip). After [`clip`](#cmd_005fclip), the path is cleared.

``` text
circle 100 100 50

preserve fill
preserve stroke
clip
```

</div>

## `print`

**`print expr`**    — [*Can be implicit*](#implicit-commands)

Print its arguments to the FFmpeg log.

See the [Command print](#Command-print) section above for more details.

## `proc`

**`proc name params* { block }`**

Assign the block and the parameters for the procedure \<name\>. The procedure can be called multiple times with the [`call`](#cmd_005fcall) command.

See the [Procedures](#Procedures) section above for more details.

## `Q`

**`Q x1 y1 x y`**

Draw a quadratic Bézier curve from the [current point](#current-point) to the *end point* specified by \<x, y\>. The *control point* is specified by \<x1, y1\>.

The behaviour is identical to the `Q` command in [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path). For more details, see [Quadratic Bézier curve on MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d#quadratic_b%C3%A9zier_curve), and the [Curve Commands section of the Paths tutorial on MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths#curve_commands).

<div class="sidebar">

<div class="title">

Example

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

Like [`Q`](#cmd_005fQ), but the coordinates are relative to the [current point](#current-point).

## `radialgrad`

**`radialgrad cx0 cy0 radius0 cx1 cy1 radius1`**

Creates a new radial gradient between the two circles defined by \<cx0 cy0 radius0\> and \<cx1 cy1 radius1\>. Each set of arguments is the coordinates of the center and the radius.

This gradient can be used for stroke and fill operations.

Use [`colorstop`](#cmd_005fcolorstop) to set the color for each position in the gradient.

<div class="sidebar">

<div class="title">

Example

</div>

The animation in the next example shows how the two circles defined in the [`radialgrad`](#cmd_005fradialgrad) arguments interact with each other.

The red circle represent the circle for the \<cx0 cy0 radius0\> arguments, and the yellow circle is the one for the \<cx1 cy1 radius1\> arguments.

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

Adds a rectangle of the given size (\<width\> × \<height\>), at position \<x, y\>, to the current path. The [current point](#current-point) is cleared before and after adding the rectangle.

See the documentation of the [`cairo_rectangle`](https://www.cairographics.org/manual/cairo-Paths.html#cairo-rectangle) function for more details.

## `repeat`

**`repeat count { block }`**

Executes a block the number of times indicated by \<count\>.

In each iteration, the variable \<i\> is used as a [loop counter](https://en.wikipedia.org/wiki/For_loop#Loop_counters). It takes the values from `0` to `count - 1`. When the loop is terminated, the variable is restored to the value before starting the loop.

If \<count\> is less than `1`, or it is not a finite number (like [`NaN`](https://en.wikipedia.org/wiki/NaN)), the block is not executed.

## `resetclip`

**`resetclip`**

Reset the current clip region to its original state, covering the whole frame.

See the documentation of the [`cairo_reset_clip`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-reset-clip) function for more details.

## `resetdash`

**`resetdash`**

Disable the dash pattern to be used by [`stroke`](#cmd_005fstroke). This reverts any change made by [`setdash`](#cmd_005fsetdash) and [`setdashoffset`](#cmd_005fsetdashoffset).

It calls [`cairo_set_dash`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-dash) with `num_dashes` set to `0`.

## `resetmatrix`

**`resetmatrix`**

Resets the current [transformation matrix](#transformation-matrix).

## `restore`

**`restore`**

Restores the state saved by a preceding call to [`save`](#cmd_005fsave).

For more details, see the [State Stack](#State-Stack) section above, and the [`cairo_restore`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-restore) function.

## `rotate`

**`rotate angle`**

Modifies the current [transformation matrix](#transformation-matrix) by rotating the user-space axes by \<angle\> radians.

See the documentation of the [`cairo_rotate`](https://www.cairographics.org/manual/cairo-Transformations.html#cairo-rotate) function for more details.

<div class="sidebar">

<div class="title">

Example

</div>

In this example:

- [`scalexy`](#cmd_005fscalexy) maps the coordinates to a 1x1 frame.

- [`translate`](#cmd_005ftranslate) put `0, 0` at the center of the frame.

- [`rotate`](#cmd_005frotate) rotates 45°.

- [`resetmatrix`](#cmd_005fresetmatrix) reverts the transformations before [`stroke`](#cmd_005fstroke), so the line width is not affected by the scale.

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

**`roundedrect x y width height radius`**    — [*Can be implicit*](#implicit-commands)

Like [`rect`](#cmd_005frect), but a circular arc is used for the corners.

<div class="sidebar">

<div class="title">

Example

</div>

The next example shows the same rectangle, with different values for the corner radius.

The radius is computed by multiplying \<i\> (the [loop counter](https://en.wikipedia.org/wiki/For_loop#Loop_counters)) by `4.5`. This number is chosen to make the last shape a perfect circle.

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

Saves a copy of the current state on an internal stack. This copy can be restored later with [`restore`](#cmd_005frestore).

For more details, see the [State Stack](#State-Stack) section above, and the [`cairo_save`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-save) function.

## `scale`

**`scale sxy`**

Similar to [`scalexy`](#cmd_005fscalexy), but the same value is used for both axes. It is equivalent to:

**`scalexy sxy sxy`**

## `scalexy`

**`scalexy sx sy`**

Modifies the current [transformation matrix](#transformation-matrix) by scaling the X and Y user-space axes by \<sx\> and \<sy\> respectively.

See the documentation of the [`cairo_scale`](https://www.cairographics.org/manual/cairo-Transformations.html#cairo-scale) function for more details.

See [`rotate`](#cmd_005frotate) for an example on combining multiple transformations.

## `setcolor`

**`setcolor color`**

Set a solid color as the [current pattern](#current-pattern) for stroke and fill operations

See the [Colors](#Colors) section above for more details.

## `setdash`

**`setdash length`**    — [*Can be implicit*](#implicit-commands)

Sets the dash pattern to be used by [`stroke`](#cmd_005fstroke).

Each call to [`setdash`](#cmd_005fsetdash) adds a length to the pattern, alternating between *on* and *off* portions of the stroke.

After a call to [`setdash`](#cmd_005fsetdash), [`resetdash`](#cmd_005fresetdash) is needed either to create a new pattern, or to discard the current one.

See the documentation of the [`cairo_set_dash`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-dash) function for more details.

## `setdashoffset`

**`setdashoffset offset`**

Set the offset into the dash pattern at which the stroke should start.

[`setdash`](#cmd_005fsetdash) must be called *before* [`setdashoffset`](#cmd_005fsetdashoffset).

See the documentation of the [`cairo_set_dash`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-dash) function for more details.

<div class="sidebar">

<div class="title">

Example

</div>

The next animation shows the effect of [`setdashoffset`](#cmd_005fsetdashoffset) when its argument changes over time.

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

Set the [current pattern](#current-pattern) to a solid color, given the *hue*, *saturation*, and *lightness*, and *alpha* components.

h is the *hue*, a value between `0` and `359`. Negative values are clamped to `0`, and values greater than `359` are interpreted as modulo 360.

s (*saturation*), l (*lightness*), and a (*alpha*), are values between `0` and `1`.

The conversion to RGB is implemented according to the [formulae from Wikipedia](https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB).

## `setlinecap`

**`setlinecap cap`**

Set the current line cap style, which determines the shape used to draw the end points of lines.

\<cap\> must be one of the following names:

- `butt`

- `round`

- `square`

It calls to [`cairo_set_line_cap`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-line-cap) to set the line cap style.

<div class="sidebar">

<div class="title">

Example

</div>

This example draws 3 lines with the same length, each one with a different line cap style:

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

Sets the current line join style, which determines the shape used to join two line segments.

\<join\> must be one of the following names:

- `bevel`

- `miter`

- `round`

It calls to [`cairo_set_line_join`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-line-join) to set the line join style.

<div class="sidebar">

<div class="title">

Example

</div>

This example draws 3 lines with the same length, each one with a different line join style:

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

Set the line width for [`stroke`](#cmd_005fstroke).

\<width\> is affected by the [transformation matrix](#transformation-matrix).

To specify a width that is not affected by other transformations, [`resetmatrix`](#cmd_005fresetmatrix) can be used between [`save`](#cmd_005fsave) / [`restore`](#cmd_005frestore):

``` text
save

resetmatrix
setlinewidth 1
stroke

// Restore matrix after stroke.
restore
```

See the documentation of the [`cairo_set_line_width`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-set-line-width) function for more details.

## `setrgba`

**`setrgba r g b a`**

Set the [current pattern](#current-pattern) to a solid color, given the *red*, *green*, *blue*, and *alpha* components.

All components are values between `0` and `1`. Values outside that range are clamped to it.

## `setvar`

**`setvar varname value`**

Set the variable \<varname\> to \<value\>.

See the [User Variables](#User-Variables) section above for more details.

## `stroke`

**`stroke`**

Strokes the current path according to the current line width, line join, line cap, and dash settings.

The path is cleared after the operation, unless the [`preserve`](#cmd_005fpreserve) command is used before [`stroke`](#cmd_005fstroke).

See the documentation of the [`cairo_stroke`](https://www.cairographics.org/manual/cairo-cairo-t.html#cairo-stroke) function for more details.

## `S`, `s`

**`S, s x2 y2 x y`**    — [*Can be implicit*](#implicit-commands)

Draw a smooth cubic Bézier curve from the [current point](#current-point) to the *end point* specified by \<x, y\>. The *end control point* is specified by \<x2, y2\>.

The *start control point* is the reflection of the *end control point* of the previous curve command about the *current point*.

The behaviour is identical to the `S` command in [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path). For more details, see [Cubic Bézier Curve on MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d#cubic_b%C3%A9zier_curve), and the [Curve Commands section of the Paths tutorial on MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths#curve_commands).

[`s`](#cmd_005fs) is like [`S`](#cmd_005fS), but the coordinates are relative to the [current point](#current-point).

<div class="sidebar">

<div class="title">

Example

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

Modifies the current [transformation matrix](#transformation-matrix) by translating the user-space origin by \<tx, ty\>.

See the documentation of the [`cairo_translate`](https://www.cairographics.org/manual/cairo-Transformations.html#cairo-translate) function for more details.

## `T`, `t`

**`T, t x y`**    — [*Can be implicit*](#implicit-commands)

Draw a smooth quadratic Bézier curve from the [current point](#current-point) to the *end point* specified by \<x, y\>.

The *control point* is the reflection of the *control point* of the previous curve command about the *current point*.

The behaviour is identical to the `T` command in [SVG's `<path>`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path). For more details, see [Quadratic Bézier curve on MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d#quadratic_b%C3%A9zier_curve), and the [Curve Commands section of the Paths tutorial on MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorials/SVG_from_scratch/Paths#curve_commands).

[`t`](#cmd_005ft) is like [`T`](#cmd_005fT), but the coordinates are relative to the [current point](#current-point).

<div class="sidebar">

<div class="title">

Example

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

**`V, v y`**    — [*Can be implicit*](#implicit-commands)

Draw a vertical line from the [current point](#current-point) to y.

The coordinate for [`V`](#cmd_005fV) is absolute, and for [`v`](#cmd_005fv) it is relative to the [current point](#current-point).
