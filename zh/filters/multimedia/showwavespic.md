# showwavespic

Convert input audio to a single video frame, representing the samples waves.

The filter accepts the following options:

- **`size, s`** Specify the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `600x240`.

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

- **`draw`** Set the draw mode.

  Available values are:

  | Term      | Description                               |
  |-----------|-------------------------------------------|
  | `scale` | Scale pixel values for each drawn sample. |
  | `full`  | Draw every sample directly.               |

  Default value is `scale`.

- **`filter`** Set the filter mode.

  Available values are:

  | Term        | Description                                       |
  |-------------|---------------------------------------------------|
  | `average` | Use average samples values for each drawn sample. |
  | `peak`    | Use peak samples values for each drawn sample.    |

  Default value is `average`.

## Examples

- Extract a channel split representation of the wave form of a whole audio track in a 1024x800 picture using `ffmpeg`:

  ``` text
  ffmpeg -i audio.flac -lavfi showwavespic=split_channels=1:s=1024x800 waveform.png
  ```
