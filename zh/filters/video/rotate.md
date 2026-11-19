# rotate

Rotate video by an arbitrary angle expressed in radians.

The filter accepts the following options:

A description of the optional parameters follows.

- **`angle, a`** Set an expression for the angle by which to rotate the input video clockwise, expressed as a number of radians. A negative value will result in a counter-clockwise rotation. By default it is set to "0".

  This expression is evaluated for each frame.

- **`out_w, ow`** Set the output width expression, default value is "iw". This expression is evaluated just once during configuration.

- **`out_h, oh`** Set the output height expression, default value is "ih". This expression is evaluated just once during configuration.

- **`bilinear`** Enable bilinear interpolation if set to 1, a value of 0 disables it. Default value is 1.

- **`fillcolor, c`** Set the color used to fill the output area not covered by the rotated image. For the general syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`. If the special value "none" is selected then no background is printed (useful for example if the background is never shown).

  Default value is "black".

The expressions for the angle and the output size can contain the following constants and functions:

- **`n`** sequential number of the input frame, starting from 0. It is always NAN before the first frame is filtered.

- **`t`** time in seconds of the input frame, it is set to 0 when the filter is configured. It is always NAN before the first frame is filtered.

- **`hsub`**

- **`vsub`** horizontal and vertical chroma subsample values. For example for the pixel format "yuv422p" \<hsub\> is 2 and \<vsub\> is 1.

- **`in_w, iw`**

- **`in_h, ih`** the input video width and height

- **`out_w, ow`**

- **`out_h, oh`** the output width and height, that is the size of the padded area as specified by the \<width\> and \<height\> expressions

- **`rotw(a)`**

- **`roth(a)`** the minimal width/height required for completely containing the input video rotated by \<a\> radians.

  These are only available when computing the `out_w` and `out_h` expressions.

## Examples

- Rotate the input by PI/6 radians clockwise:

  ``` text
  rotate=PI/6
  ```

- Rotate the input by PI/6 radians counter-clockwise:

  ``` text
  rotate=-PI/6
  ```

- Rotate the input by 45 degrees clockwise:

  ``` text
  rotate=45*PI/180
  ```

- Apply a constant rotation with period T, starting from an angle of PI/3:

  ``` text
  rotate=PI/3+2*PI*t/T
  ```

- Make the input video rotation oscillating with a period of T seconds and an amplitude of A radians:

  ``` text
  rotate=A*sin(2*PI/T*t)
  ```

- Rotate the video, output size is chosen so that the whole rotating input video is always completely contained in the output:

  ``` text
  rotate='2*PI*t:ow=hypot(iw,ih):oh=ow'
  ```

- Rotate the video, reduce the output size so that no background is ever shown:

  ``` text
  rotate=2*PI*t:ow='min(iw,ih)/sqrt(2)':oh=ow:c=none
  ```

## Commands

The filter supports the following commands:

- **`a, angle`** Set the angle expression. The command accepts the same syntax of the corresponding option.

  If the specified expression is not valid, it is kept at its current value.
