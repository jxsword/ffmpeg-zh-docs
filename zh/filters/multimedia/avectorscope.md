# avectorscope

Convert input audio to a video output, representing the audio vector scope.

The filter is used to measure the difference between channels of stereo audio stream. A monaural signal, consisting of identical left and right signal, results in straight vertical line. Any stereo separation is visible as a deviation from this line, creating a Lissajous figure. If the straight (or deviation from it) but horizontal line appears this indicates that the left and right channels are out of phase.

The filter accepts the following options:

- **`mode, m`** Set the vectorscope mode.

  Available values are:

  | Term             | Description                      |
  |------------------|----------------------------------|
  | `lissajous`    | Lissajous rotated by 45 degrees. |
  | `lissajous_xy` | Same as above but not rotated.   |
  | `polar`        | Shape resembling half of circle. |

  Default value is `lissajous`.

- **`size, s`** Set the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `400x400`.

- **`rate, r`** Set the output frame rate. Default value is `25`.

- **`rc`**

- **`gc`**

- **`bc`**

- **`ac`** Specify the red, green, blue and alpha contrast. Default values are `40`, `160`, `80` and `255`. Allowed range is `[0, 255]`.

- **`rf`**

- **`gf`**

- **`bf`**

- **`af`** Specify the red, green, blue and alpha fade. Default values are `15`, `10`, `5` and `5`. Allowed range is `[0, 255]`.

- **`zoom`** Set the zoom factor. Default value is `1`. Allowed range is `[0, 10]`. Values lower than \<1\> will auto adjust zoom factor to maximal possible value.

- **`draw`** Set the vectorscope drawing mode.

  Available values are:

  | Term       | Description                                                 |
  |------------|-------------------------------------------------------------|
  | `dot`    | Draw dot for each sample.                                   |
  | `line`   | Draw line between previous and current sample.              |
  | `aaline` | Draw anti-aliased line between previous and current sample. |

  Default value is `dot`.

- **`scale`** Specify amplitude scale of audio samples.

  Available values are:

  | Term     | Description  |
  |----------|--------------|
  | `lin`  | Linear.      |
  | `sqrt` | Square root. |
  | `cbrt` | Cubic root.  |
  | `log`  | Logarithmic. |

- **`swap`** Swap left channel axis with right channel axis.

- **`mirror`** Mirror axis.

  | Term     | Description         |
  |----------|---------------------|
  | `none` | No mirror.          |
  | `x`    | Mirror only x axis. |
  | `y`    | Mirror only y axis. |
  | `xy`   | Mirror both axis.   |

## Examples

- Complete example using `ffplay`:

  ``` text
  ffplay -f lavfi 'amovie=input.mp3, asplit [a][out1];
               [a] avectorscope=zoom=1.3:rc=2:gc=200:bc=10:rf=1:gf=8:bf=7 [out0]'
  ```

## Commands

This filter supports the all above options as commands except options `size` and `rate`.
