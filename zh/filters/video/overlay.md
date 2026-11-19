# overlay

Overlay one video on top of another.

It takes two inputs and has one output. The first input is the "main" video on which the second input is overlaid.

It accepts the following parameters:

A description of the accepted options follows.

- **`x`**

- **`y`** Set the expression for the x and y coordinates of the overlaid video on the main video. Default value is "0" for both expressions. In case the expression is invalid, it is set to a huge value (meaning that the overlay will not be displayed within the output visible area).

- **`eof_action`** See [framesync](../overview.md#changing-options-at-runtime-with-a-command).

- **`eval`** Set when the expressions for `x`, and `y` are evaluated.

  It accepts the following values:

  - **`init`** only evaluate expressions once during the filter initialization or when a command is processed

  - **`frame`** evaluate expressions for each incoming frame

  Default value is `frame`.

- **`shortest`** See [framesync](../overview.md#changing-options-at-runtime-with-a-command).

- **`format`** Set the format for the output video.

  It accepts the following values:

  | Term          | Description                          |
  |---------------|--------------------------------------|
  | `yuv420`    | force YUV 4:2:0 8-bit planar output  |
  | `yuv420p10` | force YUV 4:2:0 10-bit planar output |
  | `yuv422`    | force YUV 4:2:2 8-bit planar output  |
  | `yuv422p10` | force YUV 4:2:2 10-bit planar output |
  | `yuv444`    | force YUV 4:4:4 8-bit planar output  |
  | `yuv444p10` | force YUV 4:4:4 10-bit planar output |
  | `rgb`       | force RGB 8-bit packed output        |
  | `gbrp`      | force RGB 8-bit planar output        |
  | `auto`      | automatically pick format            |

  Default value is `yuv420`.

- **`repeatlast`** See [framesync](../overview.md#changing-options-at-runtime-with-a-command).

- **`alpha`** Set format of alpha of the overlaid video, it can be \<straight\> or \<premultiplied\>, or \<auto\> to choose the alpha mode automatically. Default is \<auto\>.

The `x`, and `y` expressions can contain the following parameters.

- **`main_w, W`**

- **`main_h, H`** The main input width and height.

- **`overlay_w, w`**

- **`overlay_h, h`** The overlay input width and height.

- **`x`**

- **`y`** The computed values for \<x\> and \<y\>. They are evaluated for each new frame.

- **`hsub`**

- **`vsub`** horizontal and vertical chroma subsample values of the output format. For example for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

- **`n`** the number of input frame, starting from 0

- **`pos`** the position in the file of the input frame, NAN if unknown; deprecated, do not use

- **`t`** The timestamp, expressed in seconds. It's NAN if the input timestamp is unknown.

This filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

Note that the \<n\>, \<t\> variables are available only when evaluation is done *per frame*, and will evaluate to NAN when `eval` is set to `init`.

Be aware that frames are taken from each input video in timestamp order, hence, if their initial timestamps differ, it is a good idea to pass the two inputs through a \<setpts=PTS-STARTPTS\> filter to have them begin in the same zero timestamp, as the example for the \<movie\> filter does.

You can chain together more overlays but you should test the efficiency of such approach.

## Commands

This filter supports the following commands:

- **`x`**

- **`y`** Modify the x and y of the overlay input. The command accepts the same syntax of the corresponding option.

  If the specified expression is not valid, it is kept at its current value.

## Examples

- Draw the overlay at 10 pixels from the bottom right corner of the main video:

  ``` text
  overlay=main_w-overlay_w-10:main_h-overlay_h-10
  ```

  Using named options the example above becomes:

  ``` text
  overlay=x=main_w-overlay_w-10:y=main_h-overlay_h-10
  ```

- Insert a transparent PNG logo in the bottom left corner of the input, using the `ffmpeg` tool with the `-filter_complex` option:

  ``` text
  ffmpeg -i input -i logo -filter_complex 'overlay=10:main_h-overlay_h-10' output
  ```

- Insert 2 different transparent PNG logos (second logo on bottom right corner) using the `ffmpeg` tool:

  ``` text
  ffmpeg -i input -i logo1 -i logo2 -filter_complex 'overlay=x=10:y=H-h-10,overlay=x=W-w-10:y=H-h-10' output
  ```

- Add a transparent color layer on top of the main video; `WxH` must specify the size of the main input to the overlay filter:

  ``` text
  color=color=red@.3:size=WxH [over]; [in][over] overlay [out]
  ```

- Play an original video and a filtered version (here with the deshake filter) side by side using the `ffplay` tool:

  ``` text
  ffplay input.avi -vf 'split[a][b]; [a]pad=iw*2:ih[src]; [b]deshake[filt]; [src][filt]overlay=w'
  ```

  The above command is the same as:

  ``` text
  ffplay input.avi -vf 'split[b], pad=iw*2[src], [b]deshake, [src]overlay=w'
  ```

- Make a sliding overlay appearing from the left to the right top part of the screen starting since time 2:

  ``` text
  overlay=x='if(gte(t,2), -w+(t-2)*20, NAN)':y=0
  ```

- Compose output by putting two input videos side to side:

  ``` text
  ffmpeg -i left.avi -i right.avi -filter_complex "
  nullsrc=size=200x100 [background];
  [0:v] setpts=PTS-STARTPTS, scale=100x100 [left];
  [1:v] setpts=PTS-STARTPTS, scale=100x100 [right];
  [background][left]       overlay=shortest=1       [background+left];
  [background+left][right] overlay=shortest=1:x=100 [left+right]
  "
  ```

- Mask 10-20 seconds of a video by applying the delogo filter to a section

  ``` text
  ffmpeg -i test.avi -codec:v:0 wmv2 -ar 11025 -b:v 9000k
  -vf '[in]split[split_main][split_delogo];[split_delogo]trim=start=360:end=371,delogo=0:0:640:480[delogoed];[split_main][delogoed]overlay=eof_action=pass[out]'
  masked.avi
  ```

- Chain several overlays in cascade:

  ``` text
  nullsrc=s=200x200 [bg];
  testsrc=s=100x100, split=4 [in0][in1][in2][in3];
  [in0] lutrgb=r=0, [bg]   overlay=0:0     [mid0];
  [in1] lutrgb=g=0, [mid0] overlay=100:0   [mid1];
  [in2] lutrgb=b=0, [mid1] overlay=0:100   [mid2];
  [in3] null,       [mid2] overlay=100:100 [out0]
  ```
