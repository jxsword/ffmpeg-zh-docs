# lut, lutrgb, lutyuv

Compute a look-up table for binding each pixel component input value to an output value, and apply it to the input video.

\<lutyuv\> applies a lookup table to a YUV input video, \<lutrgb\> to an RGB input video.

These filters accept the following parameters:

| Term | Description |
|----|----|
| `c0` | set first pixel component expression |
| `c1` | set second pixel component expression |
| `c2` | set third pixel component expression |
| `c3` | set fourth pixel component expression, corresponds to the alpha component |
| `r` | set red component expression |
| `g` | set green component expression |
| `b` | set blue component expression |
| `a` | alpha component expression |
| `y` | set Y/luma component expression |
| `u` | set U/Cb component expression |
| `v` | set V/Cr component expression |

Each of them specifies the expression to use for computing the lookup table for the corresponding pixel component values.

The exact component associated to each of the \<c\*\> options depends on the format in input.

The \<lut\> filter requires either YUV or RGB pixel formats in input, \<lutrgb\> requires RGB pixel formats in input, and \<lutyuv\> requires YUV.

The expressions can contain the following constants and functions:

- **`w`**

- **`h`** The input width and height.

- **`val`** The input value for the pixel component.

- **`clipval`** The input value, clipped to the \<minval\>-\<maxval\> range.

- **`maxval`** The maximum value for the pixel component.

- **`minval`** The minimum value for the pixel component.

- **`negval`** The negated value for the pixel component value, clipped to the \<minval\>-\<maxval\> range; it corresponds to the expression "maxval-clipval+minval".

- **`clip(val)`** The computed value in \<val\>, clipped to the \<minval\>-\<maxval\> range.

- **`gammaval(gamma)`** The computed gamma correction value of the pixel component value, clipped to the \<minval\>-\<maxval\> range. It corresponds to the expression "pow((clipval-minval)/(maxval-minval)\\\<gamma\>)\*(maxval-minval)+minval"

All expressions default to "clipval".

## Commands

This filter supports same [commands](#commands) as options.

## Examples

- Negate input video:

  ``` text
  lutrgb="r=maxval+minval-val:g=maxval+minval-val:b=maxval+minval-val"
  lutyuv="y=maxval+minval-val:u=maxval+minval-val:v=maxval+minval-val"
  ```

  The above is the same as:

  ``` text
  lutrgb="r=negval:g=negval:b=negval"
  lutyuv="y=negval:u=negval:v=negval"
  ```

- Negate luma:

  ``` text
  lutyuv=y=negval
  ```

- Remove chroma components, turning the video into a graytone image:

  ``` text
  lutyuv="u=128:v=128"
  ```

- Apply a luma burning effect:

  ``` text
  lutyuv="y=2*val"
  ```

- Remove green and blue components:

  ``` text
  lutrgb="g=0:b=0"
  ```

- Set a constant alpha channel value on input:

  ``` text
  format=rgba,lutrgb=a="maxval-minval/2"
  ```

- Correct luma gamma by a factor of 0.5:

  ``` text
  lutyuv=y=gammaval(0.5)
  ```

- Discard least significant bits of luma:

  ``` text
  lutyuv=y='bitand(val, 128+64+32)'
  ```

- Technicolor like effect:

  ``` text
  lutyuv=u='(val-maxval/2)*2+maxval/2':v='(val-maxval/2)*2+maxval/2'
  ```
