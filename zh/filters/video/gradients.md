# gradients

Generate several gradients.

- **`size, s`** Set frame size. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is "640x480".

- **`rate, r`** Set frame rate, expressed as number of frames per second. Default value is "25".

- **`c0, c1, c2, c3, c4, c5, c6, c7`** Set 8 colors. Default values for colors is to pick random one.

- **`x0, y0, y0, y1`** Set gradient line source and destination points. If negative or out of range, random ones are picked.

- **`nb_colors, n`** Set number of colors to use at once. Allowed range is from 2 to 8. Default value is 2.

- **`seed`** Set seed for picking gradient line points.

- **`duration, d`** Set the duration of the sourced video. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax.

  If not specified, or the expressed duration is negative, the video is supposed to be generated forever.

- **`speed`** Set speed of gradients rotation.

- **`type, t`** Set type of gradients. Available values are:

  - **`linear`**

  - **`radial`**

  - **`circular`**

  - **`spiral`**

  - **`square`**

  Default type is \<linear\>.

## Commands

This source supports the some above options as [commands](#commands).
