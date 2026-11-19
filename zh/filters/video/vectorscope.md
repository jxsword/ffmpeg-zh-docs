# vectorscope

Display 2 color component values in the two dimensional graph (which is called a vectorscope).

This filter accepts the following options:

- **`mode, m`** Set vectorscope mode.

  It accepts the following values:

  - **`gray`**

  - **`tint`** Gray values are displayed on graph, higher brightness means more pixels have same component color value on location in graph. This is the default mode.

  - **`color`** Gray values are displayed on graph. Surrounding pixels values which are not present in video frame are drawn in gradient of 2 color components which are set by option `x` and `y`. The 3rd color component is static.

  - **`color2`** Actual color components values present in video frame are displayed on graph.

  - **`color3`** Similar as color2 but higher frequency of same values `x` and `y` on graph increases value of another color component, which is luminance by default values of `x` and `y`.

  - **`color4`** Actual colors present in video frame are displayed on graph. If two different colors map to same position on graph then color with higher value of component not present in graph is picked.

  - **`color5`** Gray values are displayed on graph. Similar to `color` but with 3rd color component picked from radial gradient.

- **`x`** Set which color component will be represented on X-axis. Default is `1`.

- **`y`** Set which color component will be represented on Y-axis. Default is `2`.

- **`intensity, i`** Set intensity, used by modes: gray, color, color3 and color5 for increasing brightness of color component which represents frequency of (X, Y) location in graph.

- **`envelope, e`**

  - **`none`** No envelope, this is default.

  - **`instant`** Instant envelope, even darkest single pixel will be clearly highlighted.

  - **`peak`** Hold maximum and minimum values presented in graph over time. This way you can still spot out of range values without constantly looking at vectorscope.

  - **`peak+instant`** Peak and instant envelope combined together.

- **`graticule, g`** Set what kind of graticule to draw.

  - **`none`**

  - **`green`**

  - **`color`**

  - **`invert`**

- **`opacity, o`** Set graticule opacity.

- **`flags, f`** Set graticule flags.

  | Term      | Description                     |
  |-----------|---------------------------------|
  | `white` | Draw graticule for white point. |
  | `black` | Draw graticule for black point. |
  | `name`  | Draw color points short names.  |

- **`bgopacity, b`** Set background opacity.

- **`lthreshold, l`** Set low threshold for color component not represented on X or Y axis. Values lower than this value will be ignored. Default is 0. Note this value is multiplied with actual max possible value one pixel component can have. So for 8-bit input and low threshold value of 0.1 actual threshold is 0.1 \* 255 = 25.

- **`hthreshold, h`** Set high threshold for color component not represented on X or Y axis. Values higher than this value will be ignored. Default is 1. Note this value is multiplied with actual max possible value one pixel component can have. So for 8-bit input and high threshold value of 0.9 actual threshold is 0.9 \* 255 = 230.

- **`colorspace, c`** Set what kind of colorspace to use when drawing graticule.

  - **`auto`**

  - **`601`**

  - **`709`**

  Default is auto.

- **`tint0, t0`**

- **`tint1, t1`** Set color tint for gray/tint vectorscope mode. By default both options are zero. This means no tint, and output will remain gray.
