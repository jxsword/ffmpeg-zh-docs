# aap

Apply Affine Projection algorithm to the first audio stream using the second audio stream.

This adaptive filter is used to estimate unknown audio based on multiple input audio samples. Affine projection algorithm can make trade-offs between computation complexity with convergence speed.

A description of the accepted options follows.

- **`order`** Set the filter order.

- **`projection`** Set the projection order.

- **`mu`** Set the filter mu.

- **`delta`** Set the coefficient to initialize internal covariance matrix.

- **`out_mode`** Set the filter output samples. It accepts the following values:

  - **`i`** Pass the 1st input.

  - **`d`** Pass the 2nd input.

  - **`o`** Pass difference between desired, 2nd input and error signal estimate.

  - **`n`** Pass difference between input, 1st input and error signal estimate.

  - **`e`** Pass error signal estimated samples.

    Default value is \<o\>.

- **`precision`** Set which precision to use when processing samples.

  | Term     | Description                                                  |
  |----------|--------------------------------------------------------------|
  | `auto`   | Auto pick internal sample format depending on other filters. |
  | `float`  | Always use single-floating point precision sample format.    |
  | `double` | Always use double-floating point precision sample format.    |
