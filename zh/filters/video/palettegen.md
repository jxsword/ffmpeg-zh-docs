# palettegen

Generate one palette for a whole video stream.

It accepts the following options:

- **`max_colors`** Set the maximum number of colors to quantize in the palette. Note: the palette will still contain 256 colors; the unused palette entries will be black.

- **`reserve_transparent`** Create a palette of 255 colors maximum and reserve the last one for transparency. Reserving the transparency color is useful for GIF optimization. If not set, the maximum of colors in the palette will be 256. You probably want to disable this option for a standalone image. Set by default.

- **`transparency_color`** Set the color that will be used as background for transparency.

- **`stats_mode`** Set statistics mode.

  It accepts the following values:

  - **`full`** Compute full frame histograms.

  - **`diff`** Compute histograms only for the part that differs from previous frame. This might be relevant to give more importance to the moving part of your input if the background is static.

  - **`single`** Compute new histogram for each frame.

  Default value is \<full\>.

The filter also exports the frame metadata `lavfi.color_quant_ratio` (`nb_color_in / nb_color_out`) which you can use to evaluate the degree of color quantization of the palette. This information is also visible at \<info\> logging level.

## Examples

- Generate a representative palette of a given video using `ffmpeg`:

  ``` text
  ffmpeg -i input.mkv -vf palettegen palette.png
  ```
