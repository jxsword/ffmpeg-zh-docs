# blend

Blend two video frames into each other.

The `blend` filter takes two input streams and outputs one stream, the first input is the "top" layer and second input is "bottom" layer. By default, the output terminates when the longest input terminates.

The `tblend` (time blend) filter takes two consecutive frames from one single stream, and outputs the result obtained by blending the new frame on top of the old frame.

A description of the accepted options follows.

- **`c0_mode`**

- **`c1_mode`**

- **`c2_mode`**

- **`c3_mode`**

- **`all_mode`** Set blend mode for specific pixel component or all pixel components in case of \<all_mode\>. Default value is `normal`.

  Available values for component modes are:

  - **`addition`**

  - **`and`**

  - **`average`**

  - **`bleach`**

  - **`burn`**

  - **`darken`**

  - **`difference`**

  - **`divide`**

  - **`dodge`**

  - **`exclusion`**

  - **`extremity`**

  - **`freeze`**

  - **`geometric`**

  - **`glow`**

  - **`grainextract`**

  - **`grainmerge`**

  - **`hardlight`**

  - **`hardmix`**

  - **`hardoverlay`**

  - **`harmonic`**

  - **`heat`**

  - **`interpolate`**

  - **`lighten`**

  - **`linearlight`**

  - **`multiply`**

  - **`multiply128`**

  - **`negation`**

  - **`normal`**

  - **`or`**

  - **`overlay`**

  - **`phoenix`**

  - **`pinlight`**

  - **`reflect`**

  - **`screen`**

  - **`softdifference`**

  - **`softlight`**

  - **`stain`**

  - **`subtract`**

  - **`vividlight`**

  - **`xor`**

- **`c0_opacity`**

- **`c1_opacity`**

- **`c2_opacity`**

- **`c3_opacity`**

- **`all_opacity`** Set blend opacity for specific pixel component or all pixel components in case of \<all_opacity\>. Only used in combination with pixel component blend modes.

- **`c0_expr`**

- **`c1_expr`**

- **`c2_expr`**

- **`c3_expr`**

- **`all_expr`** Set blend expression for specific pixel component or all pixel components in case of \<all_expr\>. Note that related mode options will be ignored if those are set.

  The expressions can use the following variables:

  - **`N`** The sequential number of the filtered frame, starting from `0`.

  - **`X`**

  - **`Y`** the coordinates of the current sample

  - **`W`**

  - **`H`** the width and height of currently filtered plane

  - **`SW`**

  - **`SH`** Width and height scale for the plane being filtered. It is the ratio between the dimensions of the current plane to the luma plane, e.g. for a `yuv420p` frame, the values are `1,1` for the luma plane and `0.5,0.5` for the chroma planes.

  - **`T`** Time of the current frame, expressed in seconds.

  - **`TOP, A`** Value of pixel component at current location for first video frame (top layer).

  - **`BOTTOM, B`** Value of pixel component at current location for second video frame (bottom layer).

The `blend` filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

## Examples

- Apply transition from bottom layer to top layer in first 10 seconds:

  ``` text
  blend=all_expr='A*(if(gte(T,10),1,T/10))+B*(1-(if(gte(T,10),1,T/10)))'
  ```

- Apply linear horizontal transition from top layer to bottom layer:

  ``` text
  blend=all_expr='A*(X/W)+B*(1-X/W)'
  ```

- Apply 1x1 checkerboard effect:

  ``` text
  blend=all_expr='if(eq(mod(X,2),mod(Y,2)),A,B)'
  ```

- Apply uncover left effect:

  ``` text
  blend=all_expr='if(gte(N*SW+X,W),A,B)'
  ```

- Apply uncover down effect:

  ``` text
  blend=all_expr='if(gte(Y-N*SH,0),A,B)'
  ```

- Apply uncover up-left effect:

  ``` text
  blend=all_expr='if(gte(T*SH*40+Y,H)*gte((T*40*SW+X)*W/H,W),A,B)'
  ```

- Split diagonally video and shows top and bottom layer on each side:

  ``` text
  blend=all_expr='if(gt(X,Y*(W/H)),A,B)'
  ```

- Display differences between the current and the previous frame:

  ``` text
  tblend=all_mode=grainextract
  ```

## Commands

This filter supports same [commands](#commands) as options.
