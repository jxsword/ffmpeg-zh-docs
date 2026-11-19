# showspatial

Convert stereo input audio to a video output, representing the spatial relationship between two channels.

The filter accepts the following options:

- **`size, s`** Specify the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `512x512`.

- **`win_size`** Set window size. Allowed range is from \<1024\> to \<65536\>. Default size is \<4096\>.

- **`win_func`** Set window function.

  It accepts the following values:

  - **`rect`**

  - **`bartlett`**

  - **`hann`**

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

  Default value is `hann`.

- **`rate, r`** Set output framerate.
