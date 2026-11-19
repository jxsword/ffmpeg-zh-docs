# drawbox

Draw a colored box on the input image.

It accepts the following parameters:

- **`x`**

- **`y`** The expressions which specify the top left corner coordinates of the box. It defaults to 0.

- **`width, w`**

- **`height, h`** The expressions which specify the width and height of the box; if 0 they are interpreted as the input width and height. It defaults to 0.

- **`color, c`** Specify the color of the box to write. For the general syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`. If the special value `invert` is used, the box edge color is the same as the video with inverted luma.

- **`thickness, t`** The expression which sets the thickness of the box edge. A value of `fill` will create a filled box. Default value is `3`.

  See below for the list of accepted constants.

- **`replace`** Applicable if the input has alpha. With value `1`, the pixels of the painted box will overwrite the video's color and alpha pixels. Default is `0`, which composites the box onto the input, leaving the video's alpha intact.

The parameters for \<x\>, \<y\>, \<w\> and \<h\> and \<t\> are expressions containing the following constants:

- **`dar`** The input display aspect ratio, it is the same as (\<w\> / \<h\>) \* \<sar\>.

- **`hsub`**

- **`vsub`** horizontal and vertical chroma subsample values. For example for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

- **`in_h, ih`**

- **`in_w, iw`** The input width and height.

- **`sar`** The input sample aspect ratio.

- **`x`**

- **`y`** The x and y offset coordinates where the box is drawn.

- **`w`**

- **`h`** The width and height of the drawn box.

- **`box_source`** Box source can be set as side_data_detection_bboxes if you want to use box data in detection bboxes of side data.

  If \<box_source\> is set, the \<x\>, \<y\>, \<width\> and \<height\> will be ignored and still use box data in detection bboxes of side data. So please do not use this parameter if you were not sure about the box source.

- **`t`** The thickness of the drawn box.

  These constants allow the \<x\>, \<y\>, \<w\>, \<h\> and \<t\> expressions to refer to each other, so you may for example specify `y=x/dar` or `h=w/dar`.

## Examples

- Draw a black box around the edge of the input image:

  ``` text
  drawbox
  ```

- Draw a box with color red and an opacity of 50%:

  ``` text
  drawbox=10:20:200:60:red@0.5
  ```

  The previous example can be specified as:

  ``` text
  drawbox=x=10:y=20:w=200:h=60:color=red@0.5
  ```

- Fill the box with pink color:

  ``` text
  drawbox=x=10:y=10:w=100:h=100:color=pink@0.5:t=fill
  ```

- Draw a 2-pixel red 2.40:1 mask:

  ``` text
  drawbox=x=-t:y=0.5*(ih-iw/2.4)-t:w=iw+t*2:h=iw/2.4+t*2:t=2:c=red
  ```

## Commands

This filter supports same commands as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
