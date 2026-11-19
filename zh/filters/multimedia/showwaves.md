# showwaves

Convert input audio to a video output, representing the samples waves.

The filter accepts the following options:

- **`size, s`** Specify the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `600x240`.

- **`mode`** Set display mode.

  Available values are:

  | Term      | Description                                           |
  |-----------|-------------------------------------------------------|
  | `point` | Draw a point for each sample.                         |
  | `line`  | Draw a vertical line for each sample.                 |
  | `p2p`   | Draw a point for each sample and a line between them. |
  | `cline` | Draw a centered vertical line for each sample.        |

  Default value is `point`.

- **`n`** Set the number of samples which are printed on the same column. A larger value will decrease the frame rate. Must be a positive integer. This option can be set only if the value for \<rate\> is not explicitly specified.

- **`rate, r`** Set the (approximate) output frame rate. This is done by setting the option \<n\>. Default value is "25".

- **`split_channels`** Set if channels should be drawn separately or overlap. Default value is 0.

- **`colors`** Set colors separated by '\|' which are going to be used for drawing of each channel.

- **`scale`** Set amplitude scale.

  Available values are:

  | Term     | Description  |
  |----------|--------------|
  | `lin`  | Linear.      |
  | `log`  | Logarithmic. |
  | `sqrt` | Square root. |
  | `cbrt` | Cubic root.  |

  Default is linear.

- **`draw`** Set the draw mode. This is mostly useful to set for high \<n\>.

  Available values are:

  | Term      | Description                               |
  |-----------|-------------------------------------------|
  | `scale` | Scale pixel values for each drawn sample. |
  | `full`  | Draw every sample directly.               |

  Default value is `scale`.

## Examples

- Output the input file audio and the corresponding video representation at the same time:

  ``` text
  amovie=a.mp3,asplit[out0],showwaves[out1]
  ```

- Create a synthetic signal and show it with showwaves, forcing a frame rate of 30 frames per second:

  ``` text
  aevalsrc=sin(1*2*PI*t)*sin(880*2*PI*t):cos(2*PI*200*t),asplit[out0],showwaves=r=30[out1]
  ```
