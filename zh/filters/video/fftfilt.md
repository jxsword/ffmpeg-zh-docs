# fftfilt

Apply arbitrary expressions to samples in frequency domain

- **`dc_Y`** Adjust the dc value (gain) of the luma plane of the image. The filter accepts an integer value in range `0` to `1000`. The default value is set to `0`.

- **`dc_U`** Adjust the dc value (gain) of the 1st chroma plane of the image. The filter accepts an integer value in range `0` to `1000`. The default value is set to `0`.

- **`dc_V`** Adjust the dc value (gain) of the 2nd chroma plane of the image. The filter accepts an integer value in range `0` to `1000`. The default value is set to `0`.

- **`weight_Y`** Set the frequency domain weight expression for the luma plane.

- **`weight_U`** Set the frequency domain weight expression for the 1st chroma plane.

- **`weight_V`** Set the frequency domain weight expression for the 2nd chroma plane.

- **`eval`** Set when the expressions are evaluated.

  It accepts the following values:

  | Term | Description |
  |----|----|
  | `init` | Only evaluate expressions once during the filter initialization. |
  | `frame` | Evaluate expressions for each incoming frame. |

  Default value is `init`.

  The filter accepts the following variables:

- **`X`**

- **`Y`** The coordinates of the current sample.

- **`W`**

- **`H`** The width and height of the image.

- **`N`** The number of input frame, starting from 0.

- **`WS`**

- **`HS`** The size of FFT array for horizontal and vertical processing.

## Examples

- High-pass:

  ``` text
  fftfilt=dc_Y=128:weight_Y='squish(1-(Y+X)/100)'
  ```

- Low-pass:

  ``` text
  fftfilt=dc_Y=0:weight_Y='squish((Y+X)/100-1)'
  ```

- Sharpen:

  ``` text
  fftfilt=dc_Y=0:weight_Y='1+squish(1-(Y+X)/100)'
  ```

- Blur:

  ``` text
  fftfilt=dc_Y=0:weight_Y='exp(-4 * ((Y+X)/(W+H)))'
  ```
