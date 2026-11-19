# arls

Apply Recursive Least Squares algorithm to the first audio stream using the second audio stream.

This adaptive filter is used to mimic a desired filter by recursively finding the filter coefficients that relate to producing the minimal weighted linear least squares cost function of the error signal (difference between the desired, 2nd input audio stream and the actual signal, the 1st input audio stream).

A description of the accepted options follows.

- **`order`** Set the filter order.

- **`lambda`** Set the forgetting factor.

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
