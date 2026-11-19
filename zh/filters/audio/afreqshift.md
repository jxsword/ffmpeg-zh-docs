# afreqshift

Apply frequency shift to input audio samples.

The filter accepts the following options:

- **`shift`** Specify frequency shift. Allowed range is -INT_MAX to INT_MAX. Default value is 0.0.

- **`level`** Set output gain applied to final output. Allowed range is from 0.0 to 1.0. Default value is 1.0.

- **`order`** Set filter order used for filtering. Allowed range is from 1 to 16. Default value is 8.

## Commands

This filter supports the all above options as [commands](#commands).
