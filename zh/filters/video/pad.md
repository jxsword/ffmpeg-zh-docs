# pad

Add paddings to the input image, and place the original input at the provided \<x\>, \<y\> coordinates.

It accepts the following parameters:

- **`width, w`**

- **`height, h`** Specify an expression for the size of the output image with the paddings added. If the value for \<width\> or \<height\> is 0, the corresponding input size is used for the output.

  The \<width\> expression can reference the value set by the \<height\> expression, and vice versa.

  The default value of \<width\> and \<height\> is 0.

- **`x`**

- **`y`** Specify the offsets to place the input image at within the padded area, with respect to the top/left border of the output image.

  The \<x\> expression can reference the value set by the \<y\> expression, and vice versa.

  The default value of \<x\> and \<y\> is 0.

  If \<x\> or \<y\> evaluate to a negative number, they'll be changed so the input image is centered on the padded area.

- **`color`** Specify the color of the padded area. For the syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

  The default value of \<color\> is "black".

- **`eval`** Specify when to evaluate \<width\>, \<height\>, \<x\> and \<y\> expression.

  It accepts the following values:

  - **`init`** Only evaluate expressions once during the filter initialization or when a command is processed.

  - **`frame`** Evaluate expressions for each incoming frame.

  Default value is `init`.

- **`aspect`** Pad to aspect instead to a resolution.

The value for the \<width\>, \<height\>, \<x\>, and \<y\> options are expressions containing the following constants:

- **`in_w`**

- **`in_h`** The input video width and height.

- **`iw`**

- **`ih`** These are the same as \<in_w\> and \<in_h\>.

- **`out_w`**

- **`out_h`** The output width and height (the size of the padded area), as specified by the \<width\> and \<height\> expressions.

- **`ow`**

- **`oh`** These are the same as \<out_w\> and \<out_h\>.

- **`x`**

- **`y`** The x and y offsets as specified by the \<x\> and \<y\> expressions, or NAN if not yet specified.

- **`a`** same as \<iw\> / \<ih\>

- **`sar`** input sample aspect ratio

- **`dar`** input display aspect ratio, it is the same as (\<iw\> / \<ih\>) \* \<sar\>

- **`hsub`**

- **`vsub`** The horizontal and vertical chroma subsample values. For example for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

## Examples

- Add paddings with the color "violet" to the input video. The output video size is 640x480, and the top-left corner of the input video is placed at column 0, row 40

  ``` text
  pad=640:480:0:40:violet
  ```

  The example above is equivalent to the following command:

  ``` text
  pad=width=640:height=480:x=0:y=40:color=violet
  ```

- Pad the input to get an output with dimensions increased by 3/2, and put the input video at the center of the padded area:

  ``` text
  pad="3/2*iw:3/2*ih:(ow-iw)/2:(oh-ih)/2"
  ```

- Pad the input to get a squared output with size equal to the maximum value between the input width and height, and put the input video at the center of the padded area:

  ``` text
  pad="max(iw\,ih):ow:(ow-iw)/2:(oh-ih)/2"
  ```

- Pad the input to get a final w/h ratio of 16:9:

  ``` text
  pad="ih*16/9:ih:(ow-iw)/2:(oh-ih)/2"
  ```

- In case of anamorphic video, in order to set the output display aspect correctly, it is necessary to use \<sar\> in the expression, according to the relation:

  ``` text
  (ih * X / ih) * sar = output_dar
  X = output_dar / sar
  ```

  Thus the previous example needs to be modified to:

  ``` text
  pad="ih*16/9/sar:ih:(ow-iw)/2:(oh-ih)/2"
  ```

- Double the output size and put the input video in the bottom-right corner of the output padded area:

  ``` text
  pad="2*iw:2*ih:ow-iw:oh-ih"
  ```
