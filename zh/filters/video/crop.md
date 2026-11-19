# crop

Crop the input video to given dimensions.

It accepts the following parameters:

- **`w, out_w`** The width of the output video. It defaults to `iw`. This expression is evaluated only once during the filter configuration, or when the `w` or `out_w` command is sent.

- **`h, out_h`** The height of the output video. It defaults to `ih`. This expression is evaluated only once during the filter configuration, or when the `h` or `out_h` command is sent.

- **`x`** The horizontal position, in the input video, of the left edge of the output video. It defaults to `(in_w-out_w)/2`. This expression is evaluated per-frame.

- **`y`** The vertical position, in the input video, of the top edge of the output video. It defaults to `(in_h-out_h)/2`. This expression is evaluated per-frame.

- **`keep_aspect`** If set to 1 will force the output display aspect ratio to be the same of the input, by changing the output sample aspect ratio. It defaults to 0.

- **`exact`** Enable exact cropping. If enabled, subsampled videos will be cropped at exact width/height/x/y as specified and will not be rounded to nearest smaller value. It defaults to 0.

The \<out_w\>, \<out_h\>, \<x\>, \<y\> parameters are expressions containing the following constants:

- **`x`**

- **`y`** The computed values for \<x\> and \<y\>. They are evaluated for each new frame.

- **`in_w`**

- **`in_h`** The input width and height.

- **`iw`**

- **`ih`** These are the same as \<in_w\> and \<in_h\>.

- **`out_w`**

- **`out_h`** The output (cropped) width and height.

- **`ow`**

- **`oh`** These are the same as \<out_w\> and \<out_h\>.

- **`a`** same as \<iw\> / \<ih\>

- **`sar`** input sample aspect ratio

- **`dar`** input display aspect ratio, it is the same as (\<iw\> / \<ih\>) \* \<sar\>

- **`hsub`**

- **`vsub`** horizontal and vertical chroma subsample values. For example for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

- **`n`** The number of the input frame, starting from 0.

- **`pos`** the position in the file of the input frame, NAN if unknown; deprecated, do not use

- **`t`** The timestamp expressed in seconds. It's NAN if the input timestamp is unknown.

The expression for \<out_w\> may depend on the value of \<out_h\>, and the expression for \<out_h\> may depend on \<out_w\>, but they cannot depend on \<x\> and \<y\>, as \<x\> and \<y\> are evaluated after \<out_w\> and \<out_h\>.

The \<x\> and \<y\> parameters specify the expressions for the position of the top-left corner of the output (non-cropped) area. They are evaluated for each frame. If the evaluated value is not valid, it is approximated to the nearest valid value.

The expression for \<x\> may depend on \<y\>, and the expression for \<y\> may depend on \<x\>.

## Examples

- Crop area with size 100x100 at position (12,34).

  ``` text
  crop=100:100:12:34
  ```

  Using named options, the example above becomes:

  ``` text
  crop=w=100:h=100:x=12:y=34
  ```

- Crop the central input area with size 100x100:

  ``` text
  crop=100:100
  ```

- Crop the central input area with size 2/3 of the input video:

  ``` text
  crop=2/3*in_w:2/3*in_h
  ```

- Crop the input video central square:

  ``` text
  crop=out_w=in_h
  crop=in_h
  ```

- Delimit the rectangle with the top-left corner placed at position 100:100 and the right-bottom corner corresponding to the right-bottom corner of the input image.

  ``` text
  crop=in_w-100:in_h-100:100:100
  ```

- Crop 10 pixels from the left and right borders, and 20 pixels from the top and bottom borders

  ``` text
  crop=in_w-2*10:in_h-2*20
  ```

- Keep only the bottom right quarter of the input image:

  ``` text
  crop=in_w/2:in_h/2:in_w/2:in_h/2
  ```

- Crop height for getting Greek harmony:

  ``` text
  crop=in_w:1/PHI*in_w
  ```

- Apply trembling effect:

  ``` text
  crop=in_w/2:in_h/2:(in_w-out_w)/2+((in_w-out_w)/2)*sin(n/10):(in_h-out_h)/2 +((in_h-out_h)/2)*sin(n/7)
  ```

- Apply erratic camera effect depending on timestamp:

  ``` text
  crop=in_w/2:in_h/2:(in_w-out_w)/2+((in_w-out_w)/2)*sin(t*10):(in_h-out_h)/2 +((in_h-out_h)/2)*sin(t*13)
  ```

- Set x depending on the value of y:

  ``` text
  crop=in_w/2:in_h/2:y:10+10*sin(n/10)
  ```

## Commands

This filter supports the following commands:

- **`w, out_w`**

- **`h, out_h`**

- **`x`**

- **`y`** Set width/height of the output video and the horizontal/vertical position in the input video. The command accepts the same syntax of the corresponding option.

  If the specified expression is not valid, it is kept at its current value.
