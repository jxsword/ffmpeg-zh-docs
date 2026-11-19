# showcwt

Convert input audio to video output representing frequency spectrum using Continuous Wavelet Transform and Morlet wavelet.

The filter accepts the following options:

- **`size, s`** Specify the video size for the output. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `640x512`.

- **`rate, r`** Set the output frame rate. Default value is `25`.

- **`scale`** Set the frequency scale used. Allowed values are:

  - **`linear`**

  - **`log`**

  - **`bark`**

  - **`mel`**

  - **`erbs`**

  - **`sqrt`**

  - **`cbrt`**

  - **`qdrt`**

  - **`fm`**

  Default value is `linear`.

- **`iscale`** Set the intensity scale used. Allowed values are:

  - **`linear`**

  - **`log`**

  - **`sqrt`**

  - **`cbrt`**

  - **`qdrt`**

  Default value is `log`.

- **`min`** Set the minimum frequency that will be used in output. Default is `20` Hz.

- **`max`** Set the maximum frequency that will be used in output. Default is `20000` Hz. The real frequency upper limit depends on input audio's sample rate and such will be enforced on this value when it is set to value greater than Nyquist frequency.

- **`imin`** Set the minimum intensity that will be used in output.

- **`imax`** Set the maximum intensity that will be used in output.

- **`logb`** Set the logarithmic basis for brightness strength when mapping calculated magnitude values to pixel values. Allowed range is from `0` to `1`. Default value is `0.0001`.

- **`deviation`** Set the frequency deviation. Lower values than `1` are more frequency oriented, while higher values than `1` are more time oriented. Allowed range is from `0` to `10`. Default value is `1`.

- **`pps`** Set the number of pixel output per each second in one row. Allowed range is from `1` to `1024`. Default value is `64`.

- **`mode`** Set the output visual mode. Allowed values are:

  - **`magnitude`** Show magnitude.

  - **`phase`** Show only phase.

  - **`magphase`** Show combination of magnitude and phase. Magnitude is mapped to brightness and phase to color.

  - **`channel`** Show unique color per channel magnitude.

  - **`stereo`** Show unique color per stereo difference.

  Default value is `magnitude`.

- **`slide`** Set the output slide method. Allowed values are:

  - **`replace`**

  - **`scroll`**

  - **`frame`**

- **`direction`** Set the direction method for output slide method. Allowed values are:

  | Term | Description                   |
  |------|-------------------------------|
  | `lr` | Direction from left to right. |
  | `rl` | Direction from right to left. |
  | `ud` | Direction from up to down.    |
  | `du` | Direction from down to up.    |

- **`bar`** Set the ratio of bargraph display to display size. Default is 0.

- **`rotation`** Set color rotation, must be in \[-1.0, 1.0\] range. Default value is `0`.
