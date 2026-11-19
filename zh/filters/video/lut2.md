# lut2, tlut2

The `lut2` filter takes two input streams and outputs one stream.

The `tlut2` (time lut2) filter takes two consecutive frames from one single stream.

This filter accepts the following parameters:

- **`c0`** set first pixel component expression

- **`c1`** set second pixel component expression

- **`c2`** set third pixel component expression

- **`c3`** set fourth pixel component expression, corresponds to the alpha component

- **`d`** set output bit depth, only available for `lut2` filter. By default is 0, which means bit depth is automatically picked from first input format.

The `lut2` filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

Each of them specifies the expression to use for computing the lookup table for the corresponding pixel component values.

The exact component associated to each of the \<c\*\> options depends on the format in inputs.

The expressions can contain the following constants:

- **`w`**

- **`h`** The input width and height.

- **`x`** The first input value for the pixel component.

- **`y`** The second input value for the pixel component.

- **`bdx`** The first input video bit depth.

- **`bdy`** The second input video bit depth.

All expressions default to "x".

## Commands

This filter supports the all above options as [commands](#commands) except option `d`.

## Examples

- Highlight differences between two RGB video streams:

  ``` text
  lut2='ifnot(x-y,0,pow(2,bdx)-1):ifnot(x-y,0,pow(2,bdx)-1):ifnot(x-y,0,pow(2,bdx)-1)'
  ```

- Highlight differences between two YUV video streams:

  ``` text
  lut2='ifnot(x-y,0,pow(2,bdx)-1):ifnot(x-y,pow(2,bdx-1),pow(2,bdx)-1):ifnot(x-y,pow(2,bdx-1),pow(2,bdx)-1)'
  ```

- Show max difference between two video streams:

  ``` text
  lut2='if(lt(x,y),0,if(gt(x,y),pow(2,bdx)-1,pow(2,bdx-1))):if(lt(x,y),0,if(gt(x,y),pow(2,bdx)-1,pow(2,bdx-1))):if(lt(x,y),0,if(gt(x,y),pow(2,bdx)-1,pow(2,bdx-1)))'
  ```
