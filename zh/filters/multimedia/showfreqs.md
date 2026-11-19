# showfreqs

Convert input audio to video output representing the audio power spectrum. Audio amplitude is on Y-axis while frequency is on X-axis.

The filter accepts the following options:

- **`size, s`** Specify size of video. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default is `1024x512`.

- **`rate, r`** Set video rate. Default is `25`.

- **`mode`** Set display mode. This set how each frequency bin will be represented.

  It accepts the following values:

  - **`line`**

  - **`bar`**

  - **`dot`**

  Default is `bar`.

- **`ascale`** Set amplitude scale.

  It accepts the following values:

  | Term     | Description        |
  |----------|--------------------|
  | `lin`  | Linear scale.      |
  | `sqrt` | Square root scale. |
  | `cbrt` | Cubic root scale.  |
  | `log`  | Logarithmic scale. |

  Default is `log`.

- **`fscale`** Set frequency scale.

  It accepts the following values:

  | Term     | Description                |
  |----------|----------------------------|
  | `lin`  | Linear scale.              |
  | `log`  | Logarithmic scale.         |
  | `rlog` | Reverse logarithmic scale. |

  Default is `lin`.

- **`win_size`** Set window size. Allowed range is from 16 to 65536.

  Default is `2048`

- **`win_func`** Set windowing function.

  It accepts the following values:

  - **`rect`**

  - **`bartlett`**

  - **`hanning`**

  - **`hamming`**

  - **`blackman`**

  - **`welch`**

  - **`flattop`**

  - **`bharris`**

  - **`bnuttall`**

  - **`bhann`**

  - **`sine`**

  - **`nuttall`**

  - **`lanczos`**

  - **`gauss`**

  - **`tukey`**

  - **`dolph`**

  - **`cauchy`**

  - **`parzen`**

  - **`poisson`**

  - **`bohman`**

  - **`kaiser`**

  Default is `hanning`.

- **`overlap`** Set window overlap. In range `[0, 1]`. Default is `1`, which means optimal overlap for selected window function will be picked.

- **`averaging`** Set time averaging. Setting this to 0 will display current maximal peaks. Default is `1`, which means time averaging is disabled.

- **`colors`** Specify list of colors separated by space or by '\|' which will be used to draw channel frequencies. Unrecognized or missing colors will be replaced by white color.

- **`cmode`** Set channel display mode.

  It accepts the following values:

  - **`combined`**

  - **`separate`**

  Default is `combined`.

- **`minamp`** Set minimum amplitude used in `log` amplitude scaler.

- **`data`** Set data display mode.

  It accepts the following values:

  - **`magnitude`**

  - **`phase`**

  - **`delay`**

  Default is `magnitude`.

- **`channels`** Set channels to use when processing audio. By default all are processed.
