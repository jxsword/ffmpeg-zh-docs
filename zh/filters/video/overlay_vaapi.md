# overlay_vaapi

Overlay one video on the top of another.

It takes two inputs and has one output. The first input is the "main" video on which the second input is overlaid.

The filter accepts the following options:

- **`x`**

- **`y`** Set expressions for the x and y coordinates of the overlaid video on the main video.

  Default value is "0" for both expressions.

- **`w`**

- **`h`** Set expressions for the width and height the overlaid video on the main video.

  Default values are 'overlay_iw' for 'w' and 'overlay_ih\*w/overlay_iw' for 'h'.

  The expressions can contain the following parameters:

  - **`main_w, W`**

  - **`main_h, H`** The main input width and height.

  - **`overlay_iw`**

  - **`overlay_ih`** The overlay input width and height.

  - **`overlay_w, w`**

  - **`overlay_h, h`** The overlay output width and height.

  - **`overlay_x, x`**

  - **`overlay_y, y`** Position of the overlay layer inside of main

- **`alpha`** Set transparency of overlaid video. Allowed range is 0.0 to 1.0. Higher value means lower transparency. Default value is `1.0`.

- **`eof_action`** See [framesync](../overview.md#changing-options-at-runtime-with-a-command).

- **`shortest`** See [framesync](../overview.md#changing-options-at-runtime-with-a-command).

- **`repeatlast`** See [framesync](../overview.md#changing-options-at-runtime-with-a-command).

This filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

## Examples

- Overlay an image LOGO at the top-left corner of the INPUT video. Both inputs for this filter are yuv420p format.

  ``` text
  -i INPUT -i LOGO -filter_complex "[0:v]hwupload[a], [1:v]format=yuv420p, hwupload[b], [a][b]overlay_vaapi" OUTPUT
  ```

- Overlay an image LOGO at the offset (200, 100) from the top-left corner of the INPUT video. The inputs have same memory layout for color channels, the overlay has additional alpha plane, like INPUT is yuv420p, and the LOGO is yuva420p.

  ``` text
  -i INPUT -i LOGO -filter_complex "[0:v]hwupload[a], [1:v]format=yuva420p, hwupload[b], [a][b]overlay_vaapi=x=200:y=100:w=400:h=300:alpha=1.0, hwdownload, format=nv12" OUTPUT
  ```
