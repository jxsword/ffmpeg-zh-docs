# ahistogram

Convert input audio to a video output, displaying the volume histogram.

The filter accepts the following options:

- **`dmode`** Specify how histogram is calculated.

  It accepts the following values:

  | Term         | Description                              |
  |--------------|------------------------------------------|
  | `single`   | Use single histogram for all channels.   |
  | `separate` | Use separate histogram for each channel. |

  Default is `single`.

- **`rate, r`** Set frame rate, expressed as number of frames per second. Default value is "25".

- **`size, s`** Specify the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `hd720`.

- **`scale`** Set display scale.

  It accepts the following values:

  | Term     | Description         |
  |----------|---------------------|
  | `log`  | logarithmic         |
  | `sqrt` | square root         |
  | `cbrt` | cubic root          |
  | `lin`  | linear              |
  | `rlog` | reverse logarithmic |

  Default is `log`.

- **`ascale`** Set amplitude scale.

  It accepts the following values:

  | Term    | Description |
  |---------|-------------|
  | `log` | logarithmic |
  | `lin` | linear      |

  Default is `log`.

- **`acount`** Set how much frames to accumulate in histogram. Default is 1. Setting this to -1 accumulates all frames.

- **`rheight`** Set histogram ratio of window height.

- **`slide`** Set sonogram sliding.

  It accepts the following values:

  | Term        | Description                     |
  |-------------|---------------------------------|
  | `replace` | replace old rows with new ones. |
  | `scroll`  | scroll from top to bottom.      |

  Default is `replace`.

- **`hmode`** Set histogram mode.

  It accepts the following values:

  | Term     | Description                      |
  |----------|----------------------------------|
  | `abs`  | Use absolute values of samples.  |
  | `sign` | Use untouched values of samples. |

  Default is `abs`.
