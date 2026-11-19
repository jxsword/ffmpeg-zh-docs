# pad_vaapi

Add paddings to the input image, and place the original input at the provided \<x\>, \<y\> coordinates.

It accepts the following options:

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

- **`aspect`** Pad to an aspect instead to a resolution.

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
