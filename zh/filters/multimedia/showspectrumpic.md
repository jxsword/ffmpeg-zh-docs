# showspectrumpic

Convert input audio to a single video frame, representing the audio frequency spectrum.

The filter accepts the following options:

- **`size, s`** Specify the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `4096x2048`.

- **`mode`** Specify display mode.

  It accepts the following values:

  | Term         | Description                                 |
  |--------------|---------------------------------------------|
  | `combined` | all channels are displayed in the same row  |
  | `separate` | all channels are displayed in separate rows |

  Default value is `combined`.

- **`color`** Specify display color mode.

  It accepts the following values:

  | Term          | Description                                               |
  |---------------|-----------------------------------------------------------|
  | `channel`   | each channel is displayed in a separate color             |
  | `intensity` | each channel is displayed using the same color scheme     |
  | `rainbow`   | each channel is displayed using the rainbow color scheme  |
  | `moreland`  | each channel is displayed using the moreland color scheme |
  | `nebulae`   | each channel is displayed using the nebulae color scheme  |
  | `fire`      | each channel is displayed using the fire color scheme     |
  | `fiery`     | each channel is displayed using the fiery color scheme    |
  | `fruit`     | each channel is displayed using the fruit color scheme    |
  | `cool`      | each channel is displayed using the cool color scheme     |
  | `magma`     | each channel is displayed using the magma color scheme    |
  | `green`     | each channel is displayed using the green color scheme    |
  | `viridis`   | each channel is displayed using the viridis color scheme  |
  | `plasma`    | each channel is displayed using the plasma color scheme   |
  | `cividis`   | each channel is displayed using the cividis color scheme  |
  | `terrain`   | each channel is displayed using the terrain color scheme  |

  Default value is `intensity`.

- **`scale`** Specify scale used for calculating intensity color values.

  It accepts the following values:

  | Term      | Description          |
  |-----------|----------------------|
  | `lin`   | linear               |
  | `sqrt`  | square root, default |
  | `cbrt`  | cubic root           |
  | `log`   | logarithmic          |
  | `4thrt` | 4th root             |
  | `5thrt` | 5th root             |

  Default value is `log`.

- **`fscale`** Specify frequency scale.

  It accepts the following values:

  | Term    | Description |
  |---------|-------------|
  | `lin` | linear      |
  | `log` | logarithmic |

  Default value is `lin`.

- **`saturation`** Set saturation modifier for displayed colors. Negative values provide alternative color scheme. `0` is no saturation at all. Saturation must be in \[-10.0, 10.0\] range. Default value is `1`.

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

- **`orientation`** Set orientation of time vs frequency axis. Can be `vertical` or `horizontal`. Default is `vertical`.

- **`gain`** Set scale gain for calculating intensity color values. Default value is `1`.

- **`legend`** Draw time and frequency axes and legends. Default is enabled.

- **`rotation`** Set color rotation, must be in \[-1.0, 1.0\] range. Default value is `0`.

- **`start`** Set start frequency from which to display spectrogram. Default is `0`.

- **`stop`** Set stop frequency to which to display spectrogram. Default is `0`.

- **`drange`** Set dynamic range used to calculate intensity color values. Default is 120 dBFS. Allowed range is from 10 to 200.

- **`limit`** Set upper limit of input audio samples volume in dBFS. Default is 0 dBFS. Allowed range is from -100 to 100.

- **`opacity`** Set opacity strength when using pixel format output with alpha component.

## Examples

- Extract an audio spectrogram of a whole audio track in a 1024x1024 picture using `ffmpeg`:

  ``` text
  ffmpeg -i audio.flac -lavfi showspectrumpic=s=1024x1024 spectrogram.png
  ```
