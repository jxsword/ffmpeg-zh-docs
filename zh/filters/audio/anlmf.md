# anlmf, anlms

Apply Normalized Least-Mean-(Squares\|Fourth) algorithm to the first audio stream using the second audio stream.

This adaptive filter is used to mimic a desired filter by finding the filter coefficients that relate to producing the least mean square of the error signal (difference between the desired, 2nd input audio stream and the actual signal, the 1st input audio stream).

A description of the accepted options follows.

- **`order`** Set filter order.

- **`mu`** Set filter mu.

- **`eps`** Set the filter eps.

- **`leakage`** Set the filter leakage.

- **`out_mode`** It accepts the following values:

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

## Examples

- One of many usages of this filter is noise reduction, input audio is filtered with same samples that are delayed by fixed amount, one such example for stereo audio is:

  ``` text
  asplit[a][b],[a]adelay=32S|32S[a],[b][a]anlms=order=128:leakage=0.0005:mu=.5:out_mode=o
  ```

## Commands

This filter supports the same commands as options, excluding option `order`.
