# drawbox_vaapi

Draw a colored box on the input image.

It accepts the following parameters:

- **`x`**

- **`y`** The expressions which specify the top left corner coordinates of the box. It defaults to 0.

- **`width, w`**

- **`height, h`** The expressions which specify the width and height of the box; if 0 they are interpreted as the input width and height. It defaults to 0.

- **`color, c`** Specify the color of the box to write. For the general syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

- **`thickness, t`** The expression which sets the thickness of the box edge. A value of `fill` will create a filled box. Default value is `3`.

  See below for the list of accepted constants.

- **`replace`** With value `1`, the pixels of the painted box will overwrite the video's color and alpha pixels. Default is `0`, which composites the box onto the input video.

The parameters for \<x\>, \<y\>, \<w\> and \<h\> and \<t\> are expressions containing the following constants:

- **`in_h, ih`**

- **`in_w, iw`** The input width and height.

- **`x`**

- **`y`** The x and y offset coordinates where the box is drawn.

- **`w`**

- **`h`** The width and height of the drawn box.

- **`t`** The thickness of the drawn box.

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
