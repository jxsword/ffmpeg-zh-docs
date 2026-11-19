# drawgrid

Draw a grid on the input image.

It accepts the following parameters:

- **`x`**

- **`y`** The expressions which specify the coordinates of some point of grid intersection (meant to configure offset). Both default to 0.

- **`width, w`**

- **`height, h`** The expressions which specify the width and height of the grid cell, if 0 they are interpreted as the input width and height, respectively, minus `thickness`, so image gets framed. Default to 0.

- **`color, c`** Specify the color of the grid. For the general syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`. If the special value `invert` is used, the grid color is the same as the video with inverted luma.

- **`thickness, t`** The expression which sets the thickness of the grid line. Default value is `1`.

  See below for the list of accepted constants.

- **`replace`** Applicable if the input has alpha. With `1` the pixels of the painted grid will overwrite the video's color and alpha pixels. Default is `0`, which composites the grid onto the input, leaving the video's alpha intact.

The parameters for \<x\>, \<y\>, \<w\> and \<h\> and \<t\> are expressions containing the following constants:

- **`dar`** The input display aspect ratio, it is the same as (\<w\> / \<h\>) \* \<sar\>.

- **`hsub`**

- **`vsub`** horizontal and vertical chroma subsample values. For example for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

- **`in_h, ih`**

- **`in_w, iw`** The input grid cell width and height.

- **`sar`** The input sample aspect ratio.

- **`x`**

- **`y`** The x and y coordinates of some point of grid intersection (meant to configure offset).

- **`w`**

- **`h`** The width and height of the drawn cell.

- **`t`** The thickness of the drawn cell.

  These constants allow the \<x\>, \<y\>, \<w\>, \<h\> and \<t\> expressions to refer to each other, so you may for example specify `y=x/dar` or `h=w/dar`.

## Examples

- Draw a grid with cell 100x100 pixels, thickness 2 pixels, with color red and an opacity of 50%:

  ``` text
  drawgrid=width=100:height=100:thickness=2:color=red@0.5
  ```

- Draw a white 3x3 grid with an opacity of 50%:

  ``` text
  drawgrid=w=iw/3:h=ih/3:t=2:c=white@0.5
  ```

## Commands

This filter supports same commands as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
