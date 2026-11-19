# acrossover

Split audio stream into several bands.

This filter splits audio stream into two or more frequency ranges. Summing all streams back will give flat output.

The filter accepts the following options:

- **`split`** Set split frequencies. Those must be positive and increasing.

- **`order`** Set filter order for each band split. This controls filter roll-off or steepness of filter transfer function. Available values are:

  | Term     | Description        |
  |----------|--------------------|
  | `2nd`  | 12 dB per octave.  |
  | `4th`  | 24 dB per octave.  |
  | `6th`  | 36 dB per octave.  |
  | `8th`  | 48 dB per octave.  |
  | `10th` | 60 dB per octave.  |
  | `12th` | 72 dB per octave.  |
  | `14th` | 84 dB per octave.  |
  | `16th` | 96 dB per octave.  |
  | `18th` | 108 dB per octave. |
  | `20th` | 120 dB per octave. |

  Default is \<4th\>.

- **`level`** Set input gain level. Allowed range is from 0 to 1. Default value is 1.

- **`gains`** Set output gain for each band. Default value is 1 for all bands.

- **`precision`** Set which precision to use when processing samples.

  | Term     | Description                                                  |
  |----------|--------------------------------------------------------------|
  | `auto`   | Auto pick internal sample format depending on other filters. |
  | `float`  | Always use single-floating point precision sample format.    |
  | `double` | Always use double-floating point precision sample format.    |

  Default value is `auto`.

## Examples

- Split input audio stream into two bands (low and high) with split frequency of 1500 Hz, each band will be in separate stream:

  ``` text
  ffmpeg -i in.flac -filter_complex 'acrossover=split=1500[LOW][HIGH]' -map '[LOW]' low.wav -map '[HIGH]' high.wav
  ```

- Same as above, but with higher filter order:

  ``` text
  ffmpeg -i in.flac -filter_complex 'acrossover=split=1500:order=8th[LOW][HIGH]' -map '[LOW]' low.wav -map '[HIGH]' high.wav
  ```

- Same as above, but also with additional middle band (frequencies between 1500 and 8000):

  ``` text
  ffmpeg -i in.flac -filter_complex 'acrossover=split=1500 8000:order=8th[LOW][MID][HIGH]' -map '[LOW]' low.wav -map '[MID]' mid.wav -map '[HIGH]' high.wav
  ```
