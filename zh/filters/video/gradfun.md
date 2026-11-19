# gradfun

Fix the banding artifacts that are sometimes introduced into nearly flat regions by truncation to 8-bit color depth. Interpolate the gradients that should go where the bands are, and dither them.

It is designed for playback only. Do not use it prior to lossy compression, because compression tends to lose the dither and bring back the bands.

It accepts the following parameters:

- **`strength`** The maximum amount by which the filter will change any one pixel. This is also the threshold for detecting nearly flat regions. Acceptable values range from .51 to 64; the default value is 1.2. Out-of-range values will be clipped to the valid range.

- **`radius`** The neighborhood to fit the gradient to. A larger radius makes for smoother gradients, but also prevents the filter from modifying the pixels near detailed regions. Acceptable values are 8-32; the default value is 16. Out-of-range values will be clipped to the valid range.

Alternatively, the options can be specified as a flat string: \<strength\>\[:\<radius\>\]

## Examples

- Apply the filter with a `3.5` strength and radius of `8`:

  ``` text
  gradfun=3.5:8
  ```

- Specify radius, omitting the strength (which will fall-back to the default value):

  ``` text
  gradfun=radius=8
  ```
