# waveform

Video waveform monitor.

The waveform monitor plots color component intensity. By default luma only. Each column of the waveform corresponds to a column of pixels in the source video.

It accepts the following options:

- **`mode, m`** Can be either `row`, or `column`. Default is `column`. In row mode, the graph on the left side represents color component value 0 and the right side represents value = 255. In column mode, the top side represents color component value = 0 and bottom side represents value = 255.

- **`intensity, i`** Set intensity. Smaller values are useful to find out how many values of the same luminance are distributed across input rows/columns. Default value is `0.04`. Allowed range is \[0, 1\].

- **`mirror, r`** Set mirroring mode. `0` means unmirrored, `1` means mirrored. In mirrored mode, higher values will be represented on the left side for `row` mode and at the top for `column` mode. Default is `1` (mirrored).

- **`display, d`** Set display mode. It accepts the following values:

  - **`overlay`** Presents information identical to that in the `parade`, except that the graphs representing color components are superimposed directly over one another.

    This display mode makes it easier to spot relative differences or similarities in overlapping areas of the color components that are supposed to be identical, such as neutral whites, grays, or blacks.

  - **`stack`** Display separate graph for the color components side by side in `row` mode or one below the other in `column` mode.

  - **`parade`** Display separate graph for the color components side by side in `column` mode or one below the other in `row` mode.

    Using this display mode makes it easy to spot color casts in the highlights and shadows of an image, by comparing the contours of the top and the bottom graphs of each waveform. Since whites, grays, and blacks are characterized by exactly equal amounts of red, green, and blue, neutral areas of the picture should display three waveforms of roughly equal width/height. If not, the correction is easy to perform by making level adjustments the three waveforms.

  Default is `stack`.

- **`components, c`** Set which color components to display. Default is 1, which means only luma or red color component if input is in RGB colorspace. If is set for example to 7 it will display all 3 (if) available color components.

- **`envelope, e`**

  - **`none`** No envelope, this is default.

  - **`instant`** Instant envelope, minimum and maximum values presented in graph will be easily visible even with small `step` value.

  - **`peak`** Hold minimum and maximum values presented in graph across time. This way you can still spot out of range values without constantly looking at waveforms.

  - **`peak+instant`** Peak and instant envelope combined together.

- **`filter, f`**

  | Term | Description |
  |----|----|
  | `lowpass` | No filtering, this is default. |
  | `flat` | Luma and chroma combined together. |
  | `aflat` | Similar as above, but shows difference between blue and red chroma. |
  | `xflat` | Similar as above, but use different colors. |
  | `yflat` | Similar as above, but again with different colors. |
  | `chroma` | Displays only chroma. |
  | `color` | Displays actual color value on waveform. |
  | `acolor` | Similar as above, but with luma showing frequency of chroma values. |

- **`graticule, g`** Set which graticule to display.

  | Term       | Description                                              |
  |------------|----------------------------------------------------------|
  | `none`   | Do not display graticule.                                |
  | `green`  | Display green graticule showing legal broadcast ranges.  |
  | `orange` | Display orange graticule showing legal broadcast ranges. |
  | `invert` | Display invert graticule showing legal broadcast ranges. |

- **`opacity, o`** Set graticule opacity.

- **`flags, fl`** Set graticule flags.

  | Term        | Description                                   |
  |-------------|-----------------------------------------------|
  | `numbers` | Draw numbers above lines. By default enabled. |
  | `dots`    | Draw dots instead of lines.                   |

- **`scale, s`** Set scale used for displaying graticule.

  - **`digital`**

  - **`millivolts`**

  - **`ire`**

  Default is digital.

- **`bgopacity, b`** Set background opacity.

- **`tint0, t0`**

- **`tint1, t1`** Set tint for output. Only used with lowpass filter and when display is not overlay and input pixel formats are not RGB.

- **`fitmode, fm`** Set sample aspect ratio of video output frames. Can be used to configure waveform so it is not stretched too much in one of directions.

  | Term     | Description                                          |
  |----------|------------------------------------------------------|
  | `none` | Set sample aspect ration to 1/1.                     |
  | `size` | Set sample aspect ratio to match input size of video |

  Default is `none`.

- **`input`** Set input formats for filter to pick from. Can be `all`, for selecting from all available formats, or `first`, for selecting first available format. Default is `first`.
